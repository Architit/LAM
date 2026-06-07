# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import subprocess
import shutil
from pathlib import Path

import pytest

from src import lam_cli

def test_generated_files_lint(tmp_path: Path) -> None:
    """Generated Go files should pass ``gofmt``."""
    if not shutil.which("gofmt"):
        pytest.skip("gofmt not installed")

    lam_cli.scaffold(Path("100_GenomicYAML_Template.yaml"), tmp_path)
    files = [
        tmp_path / "membrane.go",
        tmp_path / "nucleus.go",
        tmp_path / "guardian" / "guardian.go",
    ]

    for f in files:
        result = subprocess.run(["gofmt", "-e", str(f)], capture_output=True, text=True)
        assert result.returncode == 0, f"gofmt errors for {f}: {result.stderr}"
