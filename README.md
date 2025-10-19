# OBS Styla - Theme Creator

This workspace contains a web-based OBS theme creator UI in `app/index.html` and several
Python scripts that generate `.ovt` and `.obt` theme files for OBS Studio.

What I added:
- `app/server.py` — small Flask server to serve the UI and provide API endpoints to list and
  download generated theme files and trigger generation.
- `app/requirements.txt` — dependencies for the server.

How to run locally:

1. Install dependencies (prefer a virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

2. Run the server:

```bash
python app/server.py
```

3. Open http://127.0.0.1:5000 in your browser to use the OBS Theme Creator UI.

Alternative: new dev setup (Vite frontend + Express backend)
--------------------------------------------------------

I've added a Vite + TypeScript frontend and an Express backend that proxies to the Python validator.

Requirements: pnpm (node + pnpm)

1. Install pnpm (if you don't have it):

```bash
# using npm
npm install -g pnpm
```

2. Install dependencies and run both frontend and backend:

```bash
pnpm install
pnpm run dev
```

This runs the Vite frontend and the Express backend concurrently. The backend executes `app/validate_cli.py` which calls the Python validator implemented in `app/server.py`.


API endpoints:
- `GET /api/themes` — list generated theme files (.ovt, .obt, .json)
- `GET /api/themes/<filename>` — download a theme file from the repo root
- `POST /api/generate` — run the theme generation scripts (`script_1.py`, `script_2.py`, `script_3.py`) and return results

Additional endpoints:
- `GET /api/validate` — run basic validation on generated theme files and return a report indicating missing metadata/sections and a simple variable analysis

Notes:
- The existing Python scripts already generate `.ovt` and `.obt` files in the repository root.
- The server simply exposes them and can re-run the scripts when requested.
