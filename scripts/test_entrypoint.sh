#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# WSL/CI-friendly temp defaults.
export TMPDIR=/tmp
export TEMP=/tmp
export TMP=/tmp

profile="full"
if [[ "${1:-}" == "--profile" ]]; then
  profile="${2:-}"
  shift 2 || true
fi

# Always verify local import path before tests.
bash scripts/lam_env.sh python -c "import lam_logging; print('lam_logging:ok')"

if [[ "$#" -gt 0 ]]; then
  bash scripts/lam_env.sh python -m pytest -q -p no:cacheprovider "$@"
  exit 0
fi

case "${profile}" in
  ci)
    bash scripts/lam_env.sh python -m pytest -q -p no:cacheprovider \
      tests/test_envelope_standard.py \
      tests/test_taskarid_comm_roaudter_trace.py \
      tests/test_comm_agent_envelope_enforcement.py
    ;;
  smoke)
    bash scripts/lam_env.sh python -m pytest -q -p no:cacheprovider \
      tests/test_envelope_standard.py \
      tests/test_taskarid_comm_roaudter_trace.py \
      tests/test_comm_agent_envelope_enforcement.py \
      tests/test_runtime_smoke.py
    ;;
  full)
    bash scripts/lam_env.sh python -m pytest -q -p no:cacheprovider
    ;;
  *)
    echo "unknown profile: ${profile}" >&2
    echo "allowed profiles: ci | smoke | full" >&2
    exit 2
    ;;
esac
