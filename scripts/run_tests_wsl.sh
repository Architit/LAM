#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
bash scripts/lam_env.sh python -m pytest -q -p no:cacheprovider "$@"
