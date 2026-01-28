#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMM_SRC="$ROOT/LAM/default/agents/comm-agent/src"
CODEX_SRC="$ROOT/LAM/default/agents/codex-agent/src"
LAM_SRC="$ROOT/src"

export PYTHONPATH="$LAM_SRC:$COMM_SRC:$CODEX_SRC${PYTHONPATH:+:$PYTHONPATH}"

exec "$@"
