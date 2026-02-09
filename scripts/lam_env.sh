#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Prefer repo venv if present
export PATH="$ROOT/.venv/bin:$PATH"

LAM_SRC="$ROOT/src"
COMM_SRC="$ROOT/LAM/default/agents/comm-agent/src"
CODEX_SRC="$ROOT/LAM/default/agents/codex-agent/src"
ROAUDTER_SRC="$ROOT/LAM/default/agents/roaudter-agent/src"

# Source of truth for imports: repo root + src + agent src
export PYTHONPATH="$ROOT:$LAM_SRC:$COMM_SRC:$CODEX_SRC:$ROAUDTER_SRC${PYTHONPATH:+:$PYTHONPATH}"

if (( $# )); then
  exec "$@"
fi
