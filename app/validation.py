import re

# Module-level constants for performance and clarity
HEX_RE = re.compile(r"^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
RGB_RE = re.compile(r"^rgba?\(.*\)$", re.I)
VAR_REF_RE = re.compile(r"var\(--([a-zA-Z0-9_-]+)\)")
ID_RE = re.compile(
    r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)+$"
)
REQUIRED_VARS = [
    "base",
    "mantle",
    "crust",
    "surface0",
    "surface1",
    "surface2",
    "overlay0",
    "overlay1",
    "overlay2",
    "text",
    "subtext0",
    "subtext1",
]


def _process_variable(name, value, line_no, declared, report):
    """Helper to process a parsed variable, checking for color and duplicates."""
    # Ensure value is a string and handle None cases
    if value is None:
        value = ""
    elif not isinstance(value, str):
        value = str(value)

    entry = {"name": name, "value": value, "line": line_no}

    # Detect and validate color-like values
    looks_like_color = (value.startswith("#") or
                        value.lower().startswith(("rgb", "hsl"))) if value else False
    entry["looks_like_color"] = looks_like_color

    if looks_like_color and value:  # Only validate non-empty color values
        valid_color = bool(HEX_RE.match(value) or RGB_RE.match(value))
        entry["color_valid"] = valid_color
        if not valid_color:
            report["errors"].append({
                "code": "VAR_COLOR_INVALID",
                "message": f"Variable {name} contains invalid color value: {value}",
                "line": line_no,
                "value": value,
            })

    report["vars"].append(entry)

    # Check for duplicates
    if name in declared:
        report["warnings"].append(
            {
                "code": "VAR_DUPLICATE",
                "message": f"Duplicate variable declaration: {name}",
                "first_line": declared[name],
                "line": line_no,
                "name": name,
            }
        )
    declared[name] = line_no


def validate_theme_content(text: str) -> dict:
    """Full validation pipeline for OBS theme files.

    Produces a structured report with:
      - meta: parsed metadata keys
      - vars: list of parsed variables with type hints
      - errors: fatal issues
      - warnings: non-fatal suggestions
      - summary counts
    """
    report = {"meta": {}, "vars": [], "errors": [], "warnings": [], "summary": {}}

    # --- find blocks (flexible parsing) ---
    meta_match = re.search(r"@OBSThemeMeta\s*\{([\s\S]*?)\}", text)
    vars_match = re.search(r"@OBSThemeVars\s*\{([\s\S]*?)\}", text)

    if not meta_match:
        report["errors"].append(
            {"code": "META_BLOCK_MISSING", "message": "Missing @OBSThemeMeta section"}
        )
        meta_block = ""
    else:
        meta_block = meta_match.group(1)

    if not vars_match:
        report["errors"].append(
            {"code": "VARS_BLOCK_MISSING", "message": "Missing @OBSThemeVars section"}
        )
        vars_block = ""
    else:
        vars_block = vars_match.group(1)

    # --- parse meta (key: value pairs, allow ' or " or bare words) ---
    for line in (meta_block or "").splitlines():
        line = line.strip().rstrip(",;")
        if not line or line.startswith("//") or line.startswith("/*"):
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
            report["errors"].append(
                {
                    "code": "META_FIELD_MISSING",
                    "message": f"Missing metadata field: {key}",
                    "field": key,
                }
            )

    # id format
    if "id" in report["meta"]:
        if not ID_RE.match(report["meta"]["id"]):
            report["errors"].append(
                {
                    "code": "META_ID_INVALID",
                    "message": f"Metadata 'id' does not match expected reverse-domain format: {report['meta']['id']}",
                    "value": report["meta"]["id"],
                }
            )

    # normalize dark
    if "dark" in report["meta"]:
        d = str(report["meta"]["dark"]).strip().lower()
        if d in ("true", "false"):
            report["meta"]["dark"] = d == "true"
        else:
            report["errors"].append(
                {
                    "code": "META_DARK_INVALID",
                    "message": f"Metadata 'dark' must be true/false: {report['meta']['dark']}",
                    "value": report["meta"]["dark"],
                }
            )

    # --- parse vars block ---
    declared = {}
    line_no = 0
    for raw_line in (vars_block or "").splitlines():
        line_no += 1
        line = raw_line.strip()
        if not line or line.startswith("//") or line.startswith("/*") or line.startswith("#"):
            continue

        # CSS-style: --var-name: value;
        m_css = re.match(r"--([a-zA-Z0-9_-]+)\s*:\s*(.+?);?$", line)
        if m_css:
            name = m_css.group(1)
            value = m_css.group(2).strip()
            _process_variable(name, value, line_no, declared, report)
            continue

        # YAML-like: name: value
        m_yaml = re.match(r"([a-zA-Z0-9_-]+)\s*:\s*(.+)$", line)
        if m_yaml:
            name = m_yaml.group(1)
            value = m_yaml.group(2).strip().rstrip(",;")
            _process_variable(name, value, line_no, declared, report)
            continue

        # unrecognized line inside vars
        if line:
            report["errors"].append(
                {
                    "code": "VARS_PARSE_ERROR",
                    "message": f"Could not parse line in @OBSThemeVars: {line}",
                    "line": line_no,
                    "raw": line,
                }
            )

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
                    report["warnings"].append(
                        {
                            "code": "VAR_REF_UNDEFINED",
                            "message": f"Variable {v.get('name')} references undefined var --{r} (may be provided by extends)",
                            "line": v.get("line"),
                            "ref": r,
                        }
                    )
                else:
                    report["errors"].append(
                        {
                            "code": "VAR_REF_UNDEFINED",
                            "message": f"Variable {v.get('name')} references undefined var --{r}",
                            "line": v.get("line"),
                            "ref": r,
                        }
                    )

    # --- required semantic variables (configurable) ---
    present = set(declared.keys())
    for rv in REQUIRED_VARS:
        if rv not in present:
            report["warnings"].append(
                {
                    "code": "VAR_REQUIRED_MISSING",
                    "message": f"Recommended semantic variable missing: {rv}",
                    "var": rv,
                }
            )

    # --- duplicate theme id detection will be done at caller level across files ---

    # summary
    report["summary"] = {
        "errors": len(report["errors"]),
        "warnings": len(report["warnings"]),
        "vars_count": len(report["vars"]),
    }

    return report
