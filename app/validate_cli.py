#!/usr/bin/env python3
import json
from pathlib import Path
import sys

# Ensure the project root is on sys.path so `from app.server import ...` works
# even when this script is executed from another process or a different cwd.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.server import find_theme_files, validate_theme_content

def main():
    reports = []
    for t in find_theme_files():
        p = ROOT / t['path']
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as e:
            reports.append({'name': t['name'], 'error': str(e)})
            continue
        rep = validate_theme_content(text)
        reports.append({'name': t['name'], 'report': rep})
    print(json.dumps({'validations': reports}))

if __name__ == '__main__':
    main()
