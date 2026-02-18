#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

PYBIN="${PYBIN:-python}"
if ! command -v "$PYBIN" >/dev/null 2>&1; then
  PYBIN="python3"
fi

"$PYBIN" -m venv .venv
source .venv/bin/activate
"$PYBIN" -m pip install -U pip
"$PYBIN" -m pip install -e .
"$PYBIN" -m pip install -r requirements-dev.txt
echo "bootstrap:ok"
