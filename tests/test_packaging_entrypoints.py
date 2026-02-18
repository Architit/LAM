from __future__ import annotations

import tomllib
from pathlib import Path


def test_project_scripts_include_cli_entrypoints() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    assert scripts.get("lam") == "lam_cli:main"
    assert scripts.get("tma") == "tma.cli:main"
