#!/usr/bin/env python3
"""
Simple Flask server to serve the OBS Theme Creator front-end and expose
endpoints to list/download generated theme files and trigger regeneration
using the included Python scripts.

Endpoints:
  GET  /            -> serves index.html
  GET  /api/themes   -> list available .ovt/.obt/.json theme files
  GET  /api/themes/<name> -> download a theme file
  POST /api/generate -> run generation scripts (script_1.py, script_2.py, script_3.py)

Run:
  pip install -r requirements.txt
  python server.py

"""
from __future__ import annotations
from dataclasses import dataclass
import os
import re
import json
import logging
import subprocess
import sys
import threading
from functools import lru_cache, wraps
from time import time
from pathlib import Path
from typing import List

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.datastructures import FileStorage

import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'app_errors.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent

@dataclass
class Config:
    HOST: str = os.getenv('HOST', '127.0.0.1')
    PORT: int = int(os.getenv('PORT', '5000'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY') or os.urandom(32).hex()
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', '1048576'))  # 1MB

    def __post_init__(self):
        if self.DEBUG and self.SECRET_KEY == 'dev-key-change-in-production':
            import warnings
            warnings.warn("Using default secret key in debug mode", UserWarning)

config = Config()

app = Flask(__name__, static_folder=str(APP_DIR), static_url_path="")
app.config.from_object(config)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

import asyncio
from concurrent.futures import ThreadPoolExecutor

# Create thread pool for I/O operations
io_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="file_io")

_file_cache_lock = threading.RLock()
_file_cache = {}
_cache_timestamp = 0
CACHE_DURATION = 30

async def find_theme_files_async() -> List[dict]:
    """Async file scanning to prevent blocking."""
    loop = asyncio.get_event_loop()

    def scan_files():
        results = []
        theme_extensions = {'.ovt', '.obt', '.json'}

        try:
            for file_path in ROOT.iterdir():
                if (file_path.is_file() and
                     file_path.suffix.lower() in theme_extensions):
                    try:
                        stat_result = file_path.stat()
                        results.append({
                            "name": file_path.name,
                            "path": str(file_path.relative_to(ROOT)),
                            "size": stat_result.st_size,
                            "modified": stat_result.st_mtime,
                        })
                    except OSError:
                        continue
        except OSError:
            return []

        return sorted(results, key=lambda r: r["name"])

    return await loop.run_in_executor(io_executor, scan_files)

# For Flask compatibility, provide sync wrapper
def find_theme_files() -> List[dict]:
    """Sync wrapper for async file scanning."""
    global _file_cache, _cache_timestamp
    current_time = time()
    with _file_cache_lock:
        if current_time - _cache_timestamp < CACHE_DURATION and _file_cache:
            return _file_cache.copy()
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(find_theme_files_async())
            _file_cache = results
            _cache_timestamp = current_time
            return results.copy()
        finally:
            loop.close()


from validation import validate_theme_content

def validate_filename(filename: str) -> bool:
    """Validate filename for security and format."""
    if not filename or len(filename) > 255:
        return False
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    # Check for valid extensions
    allowed_extensions = {'.ovt', '.obt', '.json'}
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

from werkzeug.exceptions import BadRequest, NotFound, Forbidden
import traceback

class ThemeError(Exception):
    """Base exception for theme-related errors."""
    pass

class ValidationError(ThemeError):
    """Raised when theme validation fails."""
    pass

class SecurityError(ThemeError):
    """Raised when security checks fail."""
    pass

def handle_errors(f):
    """Enhanced error handler with specific exception handling."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error in {f.__name__}: {str(e)}")
            return jsonify({"error": "Validation failed", "details": str(e)}), 400
        except SecurityError as e:
            logger.error(f"Security error in {f.__name__}: {str(e)}")
            return jsonify({"error": "Access denied"}), 403
        except FileNotFoundError as e:
            logger.info(f"File not found in {f.__name__}: {str(e)}")
            return jsonify({"error": "File not found"}), 404
        except PermissionError as e:
            logger.warning(f"Permission error in {f.__name__}: {str(e)}")
            return jsonify({"error": "Permission denied"}), 403
        except (OSError, IOError) as e:
            logger.error(f"I/O error in {f.__name__}: {str(e)}")
            return jsonify({"error": "File system error"}), 500
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}", exc_info=True)
            # In development, include traceback
            if app.config.get('DEBUG'):
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e),
                    "traceback": traceback.format_exc()
                }), 500
            return jsonify({"error": "Internal server error"}), 500
    return wrapper

@app.route("/")
@handle_errors
def index():
    # Serve the static index.html from the app directory
    return send_from_directory(str(APP_DIR), "index.html")

@app.route("/api/themes", methods=["GET"])
@handle_errors
def api_themes():
    logger.info("Fetching theme files list")
    return jsonify({"themes": find_theme_files()})


@app.route("/api/themes/<path:filename>", methods=["GET"])
@handle_errors
def api_theme_download(filename: str):
    if not validate_filename(filename):
        return jsonify({"error": "Invalid filename"}), 400
    try:
        # Sanitize filename first
        filename = os.path.basename(filename)  # Remove any path components
        secure_path = Path(ROOT).joinpath(filename).resolve()
        root_resolved = ROOT.resolve()

        # More robust security check
        try:
            secure_path.relative_to(root_resolved)
        except ValueError:
            return jsonify({"error": "Access denied"}), 403

        # Additional extension whitelist check
        allowed_extensions = {'.ovt', '.obt', '.json'}
        if secure_path.suffix.lower() not in allowed_extensions:
            return jsonify({"error": "File type not allowed"}), 403

        if not secure_path.exists() or not secure_path.is_file():
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(str(ROOT), filename, as_attachment=True)

    except (OSError, ValueError) as e:
        return jsonify({"error": "Invalid file path"}), 400


@app.route("/api/themes/<path:filename>", methods=["DELETE"])
@handle_errors
def api_theme_delete(filename: str):
    if not validate_filename(filename):
        return jsonify({"error": "Invalid filename"}), 400
    try:
        # Path validation code here (same as before)
        secure_path = Path(ROOT).joinpath(filename).resolve()
        root_resolved = ROOT.resolve()

        if not (secure_path == root_resolved or root_resolved in secure_path.parents):
            return jsonify({"error": "Access denied"}), 403

        # Attempt deletion directly, handle FileNotFoundError
        secure_path.unlink()
        return jsonify({"success": True, "message": f"Theme '{filename}' deleted."})

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except PermissionError:
        return jsonify({"error": "Permission denied"}), 403
    except OSError as e:
        return jsonify({"error": f"Error deleting file: {str(e)}"}), 500
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid filename"}), 400


import bleach
from werkzeug.utils import secure_filename

def validate_theme_name(name: str) -> tuple[bool, str]:
    """Validate theme name for security and format compliance."""
    if not name or len(name.strip()) == 0:
        return False, "Name cannot be empty"

    if len(name) > 100:
        return False, "Name too long (max 100 characters)"

    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9_\-\s\.]+$', name):
        return False, "Name contains invalid characters"

    # Prevent reserved names
    reserved_names = {'con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9'}
    if name.lower().split('.')[0] in reserved_names:
        return False, "Name cannot be a reserved system name"

    return True, "Valid"

@app.route("/api/themes/<path:filename>/duplicate", methods=["POST"])
@handle_errors
def api_theme_duplicate(filename: str):
    if not validate_filename(filename):
        return jsonify({"error": "Invalid filename"}), 400

    # Validate JSON input
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    new_name = data.get("new_name")
    if not new_name:
        return jsonify({"error": "Missing new_name"}), 400

    # Sanitize and validate new name
    new_name = bleach.clean(str(new_name).strip())
    valid, message = validate_theme_name(new_name)
    if not valid:
        return jsonify({"error": f"Invalid new_name: {message}"}), 400

    # Add proper extension if missing
    if not new_name.endswith(('.ovt', '.obt', '.json')):
        original_ext = Path(filename).suffix
        new_name += original_ext

    # Use secure_filename for additional safety
    safe_new_name = secure_filename(new_name)

    # Security: only allow files from the repository root
    secure_path = Path(ROOT).joinpath(filename).resolve()
    root_resolved = ROOT.resolve()
    if not (secure_path == root_resolved or root_resolved in secure_path.parents):
        return jsonify({"error": "Invalid filename"}), 403

    new_path = Path(ROOT).joinpath(safe_new_name).resolve()
    if not (new_path == root_resolved or root_resolved in new_path.parents):
        return jsonify({"error": "Invalid new_name"}), 403

    if new_path.exists():
        return jsonify({"error": "File with new_name already exists"}), 400

    import shutil
    shutil.copy(secure_path, new_path)
    return jsonify({"success": True, "message": f"Theme '{filename}' duplicated to '{safe_new_name}'."})


@app.route("/api/themes/<path:filename>/meta", methods=["GET", "POST"])
@handle_errors
def api_theme_meta(filename: str):
    if not validate_filename(filename):
        return jsonify({"error": "Invalid filename"}), 400
    # Security: only allow files from the repository root
    secure_path = Path(ROOT).joinpath(filename).resolve()
    if ROOT.resolve() not in secure_path.parents:
        return jsonify({"error": "Invalid filename"}), 400

    if not secure_path.exists():
        return jsonify({"error": "Not found"}), 404

    if request.method == "GET":
        try:
            text = secure_path.read_text(encoding='utf-8')
            report = validate_theme_content(text)
            return jsonify(report["meta"])
        except Exception as e:
            return jsonify({"error": f"Error reading theme: {e}"}), 500

    if request.method == "POST":
        new_meta = request.json.get("meta")
        if not new_meta:
            return jsonify({"error": "Missing meta"}), 400

        try:
            text = secure_path.read_text(encoding='utf-8')
            meta_block_re = re.compile(r"(@OBSThemeMeta\s*\{)([\s\S]*?)(\})")

            new_meta_content = "\n"
            for key, value in new_meta.items():
                new_meta_content += f"    {key}: {json.dumps(str(value))},\n"

            new_text, count = meta_block_re.sub(r"\1" + new_meta_content + r"\3", text, 1)

            if count == 0:
                return jsonify({"error": "Could not find @OBSThemeMeta block"}), 500

            secure_path.write_text(new_text, encoding='utf-8')
            return jsonify({"success": True, "message": "Theme metadata updated."})
        except Exception as e:
            return jsonify({"error": f"Error updating metadata: {e}"}), 500


@app.route("/api/generate", methods=["POST"])
@limiter.limit("5 per minute")
@handle_errors
def api_generate():
    ALLOWED_SCRIPTS = {"script_1.py", "script_2.py", "script_3.py"}
    results = []

    for script_name in ALLOWED_SCRIPTS:
        script_path = ROOT / script_name

        # Ensure script exists and is a regular file
        if not script_path.exists() or not script_path.is_file():
            results.append({"script": script_name, "status": "missing"})
            continue

        # Additional security: verify script integrity/hash if needed
        try:
            script_path_resolved = script_path.resolve()
            if script_path_resolved.parent != ROOT.resolve():
                results.append({"script": script_name, "status": "security_error"})
                continue

            # Use absolute path and restrict environment
            proc = subprocess.run(
                [sys.executable, str(script_path_resolved)],
                cwd=str(ROOT.resolve()),
                capture_output=True,
                text=True,
                timeout=30,  # Reduced timeout
                shell=False,
                env={'PATH': '', 'PYTHONPATH': str(ROOT)}  # Restricted environment
            )

            results.append({
                "script": script_name,
                "returncode": proc.returncode,
                "stdout": proc.stdout[:2000] if proc.stdout else "",
                "stderr": proc.stderr[:2000] if proc.stderr else ""
            })
        except subprocess.TimeoutExpired:
            results.append({"script": script_name, "status": "timeout"})
        except Exception as e:
            results.append({"script": script_name, "status": "error", "error": str(e)[:500]})

    return jsonify({"results": results, "themes": find_theme_files()})


@app.route("/api/validate", methods=["GET"])
@handle_errors
def api_validate():
    """Validate all generated theme files and return a report."""
    themes = find_theme_files()
    reports = []
    # collect id->files map for duplicate detection
    id_map: dict = {}
    for t in themes:
        p = ROOT / t["path"]
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as e:
            reports.append({"name": t["name"], "error": f"Could not read file: {e}"})
            continue
        rep = validate_theme_content(text)
        reports.append({"name": t["name"], "report": rep})
        # gather ids
        mid = rep.get("meta", {}).get("id")
        if mid:
            id_map.setdefault(mid, []).append(t["name"])

    # detect duplicates
    duplicate_ids = []
    for mid, files in id_map.items():
        if len(files) > 1:
            duplicate_ids.append({"id": mid, "files": files})
            # add warnings to each file report
            for r in reports:
                if r["name"] in files:
                    r["report"].setdefault("warnings", []).append({"code": "DUPLICATE_THEME_ID", "message": f"Theme id {mid} used by multiple files", "files": files})

    return jsonify({"validations": reports, "duplicate_ids": duplicate_ids})


@app.route("/health")
def health_check():
    """Comprehensive health check endpoint."""
    checks = {
        "status": "healthy",
        "timestamp": time(),
        "version": "1.0.0",
        "dependencies": {}
    }

    # Check file system access
    try:
        ROOT.stat()
        checks["dependencies"]["filesystem"] = "ok"
    except OSError:
        checks["dependencies"]["filesystem"] = "error"
        checks["status"] = "unhealthy"

    # Check Python scripts existence
    for script in ["script_1.py", "script_2.py", "script_3.py"]:
        script_path = ROOT / script
        checks["dependencies"][script] = "ok" if script_path.exists() else "missing"

    status_code = 200 if checks["status"] == "healthy" else 503
    return jsonify(checks), status_code


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


@app.before_request
def limit_remote_addr():
    """Basic rate limiting by IP."""
    # This could be enhanced with Redis for distributed deployments
    pass


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
