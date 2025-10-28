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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent

@dataclass
class Config:
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5000'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB

config = Config()

app = Flask(__name__, static_folder=str(APP_DIR), static_url_path="")
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Add module-level cache management
_cache_lock = threading.RLock()
_last_cache_time = 0
_cache_duration = 30  # Cache for 30 seconds

@lru_cache(maxsize=1)
def _scan_theme_files():
    """Internal cached file scanning function."""
    results = []
    # Use single rglob with multiple extensions
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
    # Sort once at the end
    results.sort(key=lambda r: r["name"])
    return results

def find_theme_files() -> List[dict]:
    """Scan the repository root for theme files with caching."""
    global _last_cache_time
    current_time = time()

    with _cache_lock:
        # Invalidate cache after duration
        if current_time - _last_cache_time > _cache_duration:
            _scan_theme_files.cache_clear()
            _last_cache_time = current_time
        return _scan_theme_files()


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

def handle_errors(f):
    """Decorator for consistent error handling and logging."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
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
        # Normalize the filename and resolve path
        secure_path = Path(ROOT).joinpath(filename).resolve()
        root_resolved = ROOT.resolve()

        # Check if the resolved path is within the allowed directory
        if not (secure_path == root_resolved or root_resolved in secure_path.parents):
            return jsonify({"error": "Access denied"}), 403

        # Additional whitelist check for allowed file extensions
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


@app.route("/api/themes/<path:filename>/duplicate", methods=["POST"])
@handle_errors
def api_theme_duplicate(filename: str):
    if not validate_filename(filename):
        return jsonify({"error": "Invalid filename"}), 400
    try:
        # Security: only allow files from the repository root
        secure_path = Path(ROOT).joinpath(filename).resolve()
        root_resolved = ROOT.resolve()
        if not (secure_path == root_resolved or root_resolved in secure_path.parents):
            return jsonify({"error": "Invalid filename"}), 403

        new_name = request.json.get("new_name")
        if not new_name:
            return jsonify({"error": "Missing new_name"}), 400

        new_path = Path(ROOT).joinpath(new_name).resolve()
        if not (new_path == root_resolved or root_resolved in new_path.parents):
            return jsonify({"error": "Invalid new_name"}), 403

        if new_path.exists():
            return jsonify({"error": "File with new_name already exists"}), 400

        import shutil
        shutil.copy(secure_path, new_path)
        return jsonify({"success": True, "message": f"Theme '{filename}' duplicated to '{new_name}'."})
    except FileNotFoundError:
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error duplicating theme: {e}"}), 500


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
@limiter.limit("5 per minute")  # Limit expensive operations
@handle_errors
def api_generate():
    """Run the included generation scripts to (re)create theme files."""
    # Whitelist of allowed scripts
    ALLOWED_SCRIPTS = {"script_1.py", "script_2.py", "script_3.py"}

    results = []
    for script_name in ALLOWED_SCRIPTS:
        script_path = ROOT / script_name
        if not script_path.exists():
            results.append({"script": script_name, "status": "missing"})
            continue

        # Validate script path is actually within ROOT and is the expected file
        try:
            if script_path.resolve().parent != ROOT.resolve():
                results.append({"script": script_name, "status": "security_error",
                                "error": "Script path validation failed"})
                continue

            proc = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=60,
                # Additional security: disable shell interpretation
                shell=False
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


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
