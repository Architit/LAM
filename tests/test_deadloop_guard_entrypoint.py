from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "deadloop_guard_entrypoint.py"


def test_guard_entrypoint_holds_without_operator_confirmation() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--governance-only-streak",
            "0",
            "--changed-path",
            "src/deadloop_gate.py",
            "--changed-path",
            "tests/test_deadloop_gate.py",
            "--validation-result",
            "PASS",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 6
    assert "HOLD_BY_DEADLOOP_BREAK_PROTOCOL" in proc.stdout


def test_guard_entrypoint_passes_with_full_tuple_and_confirmation() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--governance-only-streak",
            "0",
            "--changed-path",
            "src/deadloop_gate.py",
            "--changed-path",
            "tests/test_deadloop_gate.py",
            "--validation-command",
            ".venv/bin/pytest -q tests/test_deadloop_gate.py",
            "--validation-result",
            "PASS",
            "--operator-confirmed",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert '"decision": "PASS"' in proc.stdout
