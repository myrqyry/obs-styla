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


def validate_theme_content(text: str) -> dict:
    """Full validation pipeline for OBS theme files.

    Produces a structured report with:
      - meta: parsed metadata keys
      - vars: list of parsed variables with type hints
      - errors: fatal issues
      - warnings: non-fatal suggestions
      - summary counts
    """
    import re

    # helpers / regexes
    HEX_RE = re.compile(r"^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
    RGB_RE = re.compile(r"^rgba?\(.*\)$", re.I)
    VAR_REF_RE = re.compile(r"var\(--([a-zA-Z0-9_-]+)\)")
    ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)+$")

    report = {
        "meta": {},
        "vars": [],
        "errors": [],
        "warnings": [],
        "summary": {}
    }

    # --- find blocks (flexible parsing) ---
    meta_match = re.search(r"@OBSThemeMeta\s*\{([\s\S]*?)\}", text)
    vars_match = re.search(r"@OBSThemeVars\s*\{([\s\S]*?)\}", text)

    if not meta_match:
        report["errors"].append({"code": "META_BLOCK_MISSING", "message": "Missing @OBSThemeMeta section"})
        meta_block = ""
    else:
        meta_block = meta_match.group(1)

    if not vars_match:
        report["errors"].append({"code": "VARS_BLOCK_MISSING", "message": "Missing @OBSThemeVars section"})
        vars_block = ""
    else:
        vars_block = vars_match.group(1)

    # --- parse meta (key: value pairs, allow ' or " or bare words) ---
    for line in (meta_block or "").splitlines():
        line = line.strip().rstrip(',;')
        if not line or line.startswith('//') or line.startswith('/*'):
            continue
        m = re.match(r'([a-zA-Z0-9_-]+)\s*:\s*(?:\'([^\']*)\'|"([^"]*)"|([^,;]+))', line)
        if m:
            key = m.group(1)
            value = m.group(2) or m.group(3) or m.group(4) or ""
            value = value.strip()
            report["meta"][key] = value

    # required meta keys
    for key in ("id", "name", "dark"):
        if key not in report["meta"]:
            report["errors"].append({"code": "META_FIELD_MISSING", "message": f"Missing metadata field: {key}", "field": key})

    # id format
    if "id" in report["meta"]:
        if not ID_RE.match(report["meta"]["id"]):
            report["errors"].append({"code": "META_ID_INVALID", "message": f"Metadata 'id' does not match expected reverse-domain format: {report['meta']['id']}", "value": report["meta"]["id"]})

    # normalize dark
    if "dark" in report["meta"]:
        d = str(report["meta"]["dark"]).strip().lower()
        if d in ("true", "false"):
            report["meta"]["dark"] = d == "true"
        else:
            report["errors"].append({"code": "META_DARK_INVALID", "message": f"Metadata 'dark' must be true/false: {report['meta']['dark']}", "value": report["meta"]["dark"]})

    # --- parse vars block ---
    declared = {}
    line_no = 0
    for raw_line in (vars_block or "").splitlines():
        line_no += 1
        line = raw_line.strip()
        if not line or line.startswith('//') or line.startswith('/*') or line.startswith('#'):
            continue

        # CSS-style: --var-name: value;
        m = re.match(r"--([a-zA-Z0-9_-]+)\s*:\s*(.+?);?$", line)
        if m:
            name = m.group(1)
            value = m.group(2).strip()
            entry = {"name": name, "value": value, "line": line_no}
            # detect color-like
            looks_like_color = False
            if value.startswith('#') or value.lower().startswith(('rgb', 'hsl')):
                looks_like_color = True
            entry["looks_like_color"] = looks_like_color
            # validate color if color-like
            if looks_like_color:
                valid_color = bool(HEX_RE.match(value) or RGB_RE.match(value))
                entry["color_valid"] = valid_color
                if not valid_color:
                    report["errors"].append({"code": "VAR_COLOR_INVALID", "message": f"Variable {name} contains invalid color value: {value}", "line": line_no, "value": value})

            report["vars"].append(entry)
            if name in declared:
                report["warnings"].append({"code": "VAR_DUPLICATE", "message": f"Duplicate variable declaration: {name}", "first_line": declared[name], "line": line_no, "name": name})
            declared[name] = line_no
            continue

        # YAML-like: name: value
        m2 = re.match(r"([a-zA-Z0-9_-]+)\s*:\s*(.+)$", line)
        if m2:
            name = m2.group(1)
            value = m2.group(2).strip().rstrip(',;')
            entry = {"name": name, "value": value, "line": line_no, "looks_like_color": False}
            if value.startswith('#') or value.lower().startswith(('rgb', 'hsl')):
                entry["looks_like_color"] = True
                entry["color_valid"] = bool(HEX_RE.match(value) or RGB_RE.match(value))
                if not entry.get("color_valid", True):
                    report["errors"].append({"code": "VAR_COLOR_INVALID", "message": f"Variable {name} contains invalid color value: {value}", "line": line_no, "value": value})
            report["vars"].append(entry)
            if name in declared:
                report["warnings"].append({"code": "VAR_DUPLICATE", "message": f"Duplicate variable declaration: {name}", "first_line": declared[name], "line": line_no, "name": name})
            declared[name] = line_no
            continue

        # unrecognized line inside vars
        if line:
            report["errors"].append({"code": "VARS_PARSE_ERROR", "message": f"Could not parse line in @OBSThemeVars: {line}", "line": line_no, "raw": line})

    # --- resolve var references var(--x) -> check existence ---
    for v in report["vars"]:
        val = v.get("value")
        if not isinstance(val, str):
            continue
        refs = VAR_REF_RE.findall(val)
        for r in refs:
            if r not in declared:
                # If meta extends present, demote to warning; otherwise error
                if "extends" in report["meta"]:
                    report["warnings"].append({"code": "VAR_REF_UNDEFINED", "message": f"Variable {v.get('name')} references undefined var --{r} (may be provided by extends)", "line": v.get("line"), "ref": r})
                else:
                    report["errors"].append({"code": "VAR_REF_UNDEFINED", "message": f"Variable {v.get('name')} references undefined var --{r}", "line": v.get("line"), "ref": r})

    # --- required semantic variables (configurable) ---
    REQUIRED_VARS = [
        "base", "mantle", "crust",
        "surface0", "surface1", "surface2",
        "overlay0", "overlay1", "overlay2",
        "text", "subtext0", "subtext1",
    ]
    present = set(declared.keys())
    for rv in REQUIRED_VARS:
        if rv not in present:
            report["warnings"].append({"code": "VAR_REQUIRED_MISSING", "message": f"Recommended semantic variable missing: {rv}", "var": rv})

    # --- duplicate theme id detection will be done at caller level across files ---

    # summary
    report["summary"] = {"errors": len(report["errors"]), "warnings": len(report["warnings"]), "vars_count": len(report["vars"])}

    return report


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
