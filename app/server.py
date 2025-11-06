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
import bleach
from werkzeug.utils import secure_filename
import shutil

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
            for file_path in (ROOT / "packages").iterdir():
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


from app.routes.theme_routes import theme_bp
app.register_blueprint(theme_bp)




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
