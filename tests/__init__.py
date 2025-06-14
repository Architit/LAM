"""Test package initialization to set import paths."""

import sys
from pathlib import Path

# Prepend the repository root to sys.path so tests can import modules from src
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

