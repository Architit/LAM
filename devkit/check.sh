#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# WSL-friendly temp
export TMPDIR=/tmp TEMP=/tmp TMP=/tmp

# Minimal sanity: import + pytest
bash scripts/lam_env.sh python -c "import lam_logging; print('lam_logging:ok')"
bash scripts/lam_env.sh python -m pytest -q -p no:cacheprovider "$@"
