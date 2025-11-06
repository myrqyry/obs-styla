from flask import Blueprint, jsonify, send_from_directory, request
from app.services.file_service import FileService
import logging
from pathlib import Path
import bleach
from werkzeug.utils import secure_filename
import re
import shutil
import json
from validation import validate_theme_content

theme_bp = Blueprint('themes', __name__)
logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent.parent.parent
file_service = FileService(ROOT)

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


@theme_bp.route("/api/themes/<path:filename>", methods=["GET"])
def download_theme(filename: str):
    is_valid, file_path, message = file_service.validate_and_resolve_path(filename)
    if not is_valid:
        return jsonify({"error": message}), 400
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    try:
        return send_from_directory(
            str(file_path.parent),
            file_path.name,
            as_attachment=True
        )
    except OSError as e:
        logger.error(f"File access error: {e}")
        return jsonify({"error": "File access error"}), 500

@theme_bp.route("/api/themes/<path:filename>", methods=["DELETE"])
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

@theme_bp.route("/api/themes/<path:filename>/duplicate", methods=["POST"])
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

    shutil.copy(secure_path, new_path)
    return jsonify({"success": True, "message": f"Theme '{filename}' duplicated to '{safe_new_name}'."})


@theme_bp.route("/api/themes/<path:filename>/meta", methods=["GET", "POST"])
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
