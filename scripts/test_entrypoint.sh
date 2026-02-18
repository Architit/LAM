#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# WSL/CI-friendly temp defaults.
export TMPDIR=/tmp
export TEMP=/tmp
export TMP=/tmp

profile="full"
deadloop_guard=0
deadloop_streak="${DEADLOOP_GOVERNANCE_STREAK:-0}"
deadloop_operator_confirmed=0
declare -a deadloop_changed_paths=()
if [[ "${1:-}" == "--profile" ]]; then
  profile="${2:-}"
  shift 2 || true
fi

while [[ "$#" -gt 0 ]]; do
  case "${1}" in
    --deadloop-guard)
      deadloop_guard=1
      shift
      ;;
    --governance-only-streak)
      deadloop_streak="${2:-0}"
      shift 2
      ;;
    --operator-confirmed)
      deadloop_operator_confirmed=1
      shift
      ;;
    --changed-path)
      deadloop_changed_paths+=("${2:-}")
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

# Always verify local import path before tests.
bash scripts/lam_env.sh python -c "import lam_logging; print('lam_logging:ok')"

if [[ "${deadloop_guard}" -eq 1 ]]; then
  guard_cmd=(python3 scripts/deadloop_guard_entrypoint.py --governance-only-streak "${deadloop_streak}" --validation-result PASS)
  for p in "${deadloop_changed_paths[@]}"; do
    if [[ -n "${p}" ]]; then
      guard_cmd+=(--changed-path "${p}")
    fi
  done
  guard_cmd+=(--validation-command ".venv/bin/ruff check src tests scripts LAM/default/agents/roaudter-agent/src")
  guard_cmd+=(--validation-command ".venv/bin/mypy src")
  guard_cmd+=(--validation-command ".venv/bin/pytest -q")
  if [[ "${deadloop_operator_confirmed}" -eq 1 ]]; then
    guard_cmd+=(--operator-confirmed)
  fi
  "${guard_cmd[@]}"
fi

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
