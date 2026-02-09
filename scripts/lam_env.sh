#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$ROOT/.venv/bin:$PATH"
COMM_SRC="$ROOT/LAM/default/agents/comm-agent/src"
CODEX_SRC="$ROOT/LAM/default/agents/codex-agent/src"
ROAUDTER_SRC="$ROOT/LAM/default/agents/roaudter-agent/src"
LAM_SRC="$ROOT/src"

export PYTHONPATH="$LAM_SRC:$COMM_SRC:$CODEX_SRC:$ROAUDTER_SRC${PYTHONPATH:+:$PYTHONPATH}"

if (( $# )); then
  exec "$@"
fi
