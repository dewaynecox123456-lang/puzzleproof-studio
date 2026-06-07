#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
if ! python -c "import tkinter" >/dev/null 2>&1; then
  echo "Tkinter is required. On Fedora, install it with: sudo dnf install python3-tkinter" >&2
  exit 1
fi
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/main.py
