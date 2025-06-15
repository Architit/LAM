"""Test Matrix Aggregator (TMA) package."""
from __future__ import annotations

from pathlib import Path
import os
import yaml
from typing import Any, Dict


def _find_config() -> Path:
    """Return the first existing config path from known locations."""
    env_path = os.getenv("TMA_CONFIG")
    if env_path:
        return Path(env_path)

    base = Path(__file__).resolve().parent.parent
    candidates = [
        base / "tma.yaml",
        base.parent / "tma.yaml",
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


_CONFIG_PATH = _find_config()


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML with environment overrides."""
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {_CONFIG_PATH}")
    with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}
    for key in list(config.keys()):
        env_key = f"TMA_{key.upper()}"
        if env_key in os.environ:
            config[key] = os.environ[env_key]
    return config


CONFIG = load_config()
VERSION = str(CONFIG.get("version", "0.0.0"))
