# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
"""Test package initialization to set import paths."""

import sys
from pathlib import Path

# Prepend the ``src`` directory to ``sys.path`` so tests work without installation
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Also prepend roaudter-agent/src so `import roaudter_agent` works in tests (submodule layout).
ROAUDTER_SRC = Path(__file__).resolve().parents[1] / 'LAM/default/agents/roaudter-agent/src'
if str(ROAUDTER_SRC) not in sys.path:
    sys.path.insert(0, str(ROAUDTER_SRC))
