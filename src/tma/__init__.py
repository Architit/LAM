# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
"""Test Matrix Aggregator (TMA) package."""
from __future__ import annotations

from pathlib import Path
import os
import yaml
from typing import Any, Dict

_CONFIG_PATH = Path(os.getenv("TMA_CONFIG", Path(__file__).resolve().parent.parent / "tma.yaml"))


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
