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
import os
import subprocess
import sys
from pathlib import Path
from typing import List

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=str(APP_DIR), static_url_path="")
CORS(app)


def find_theme_files() -> List[dict]:
    """Scan the repository root for theme files we generated.

    Returns a list of dicts with keys: name, path (relative), size
    """
    patterns = ["*.ovt", "*.obt", "*.json"]
    results = []
    for pattern in patterns:
        for p in ROOT.glob(pattern):
            try:
                stat = p.stat()
                results.append({
                    "name": p.name,
                    "path": str(p.relative_to(ROOT)),
                    "size": stat.st_size,
                })
            except OSError:
                continue
    # sort by name
    results.sort(key=lambda r: r["name"])
    return results


from .validation import validate_theme_content


@app.route("/")
def index():
    # Serve the static index.html from the app directory
    return send_from_directory(str(APP_DIR), "index.html")


@app.route("/api/themes", methods=["GET"])
def api_themes():
    return jsonify({"themes": find_theme_files()})


@app.route("/api/themes/<path:filename>", methods=["GET"])
def api_theme_download(filename: str):
    # Security: only allow files from the repository root
    # A more robust way to secure this is to have a whitelist of allowed files/directories
    # or to use a library like safe-join.
    # For now, let's make the check more explicit.
    secure_path = Path(ROOT).joinpath(filename).resolve()
    if ROOT.resolve() not in secure_path.parents:
        return jsonify({"error": "Invalid filename"}), 400

    if not secure_path.exists():
        return jsonify({"error": "Not found"}), 404

    return send_from_directory(str(ROOT), filename, as_attachment=True)


@app.route("/api/themes/<path:filename>", methods=["DELETE"])
def api_theme_delete(filename: str):
    # Security: only allow files from the repository root
    secure_path = Path(ROOT).joinpath(filename).resolve()
    if ROOT.resolve() not in secure_path.parents:
        return jsonify({"error": "Invalid filename"}), 400

    if not secure_path.exists():
        return jsonify({"error": "Not found"}), 404

    try:
        secure_path.unlink()
        return jsonify({"success": True, "message": f"Theme '{filename}' deleted."})
    except OSError as e:
        return jsonify({"error": f"Error deleting theme: {e}"}), 500


@app.route("/api/themes/<path:filename>/duplicate", methods=["POST"])
def api_theme_duplicate(filename: str):
    # Security: only allow files from the repository root
    secure_path = Path(ROOT).joinpath(filename).resolve()
    if ROOT.resolve() not in secure_path.parents:
        return jsonify({"error": "Invalid filename"}), 400

    if not secure_path.exists():
        return jsonify({"error": "Not found"}), 404

    new_name = request.json.get("new_name")
    if not new_name:
        return jsonify({"error": "Missing new_name"}), 400

    new_path = Path(ROOT).joinpath(new_name).resolve()
    if ROOT.resolve() not in new_path.parents:
        return jsonify({"error": "Invalid new_name"}), 400

    if new_path.exists():
        return jsonify({"error": "File with new_name already exists"}), 400

    try:
        import shutil
        shutil.copy(secure_path, new_path)
        return jsonify({"success": True, "message": f"Theme '{filename}' duplicated to '{new_name}'."})
    except Exception as e:
        return jsonify({"error": f"Error duplicating theme: {e}"}), 500


@app.route("/api/themes/<path:filename>/meta", methods=["GET", "POST"])
def api_theme_meta(filename: str):
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
def api_generate():
    """Run the included generation scripts to (re)create theme files.

    This runs script_1.py, script_2.py, script_3.py in the repository root.
    """
    scripts = ["script_1.py", "script_2.py", "script_3.py"]
    results = []
    for s in scripts:
        script_path = ROOT / s
        if not script_path.exists():
            results.append({"script": s, "status": "missing"})
            continue

        try:
            # Run using the same Python executable
            proc = subprocess.run([sys.executable, str(script_path)],
                                   cwd=str(ROOT),
                                   capture_output=True,
                                   text=True,
                                   timeout=60)
            results.append({
                "script": s,
                "returncode": proc.returncode,
                "stdout": proc.stdout[:2000],
                "stderr": proc.stderr[:2000]
            })
        except Exception as e:
            results.append({"script": s, "status": "error", "error": str(e)})

    return jsonify({"results": results, "themes": find_theme_files()})


@app.route("/api/validate", methods=["GET"])
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
    port = int(os.environ.get("PORT", "5000"))
    print(f"Starting server on http://127.0.0.1:{port} (serving app/index.html)")
    app.run(host="0.0.0.0", port=port, debug=False)
