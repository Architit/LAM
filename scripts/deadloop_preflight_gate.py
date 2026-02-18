#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
from dataclasses import asdict
import sys


def _load_gate_fn():
    root = Path(__file__).resolve().parents[1]
    module_path = root / "src" / "deadloop_gate.py"
    spec = importlib.util.spec_from_file_location("deadloop_gate_module", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load deadloop gate module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.evaluate_deadloop_preflight


def _git_changed_paths() -> list[str]:
    cmd = ["git", "diff", "--name-only", "HEAD"]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
    evaluate_deadloop_preflight = _load_gate_fn()
    parser = argparse.ArgumentParser(
        prog="deadloop_preflight_gate",
        description="Evaluate DEADLOOP_PREFLIGHT_GATE metrics and decision.",
    )
    parser.add_argument(
        "--governance-only-streak",
        type=int,
        required=True,
        help="Current governance-only streak in the active S-chain.",
    )
    parser.add_argument(
        "--changed-path",
        action="append",
        default=[],
        help="Changed file path (repeatable). If omitted, reads git diff --name-only HEAD.",
    )
    parser.add_argument(
        "--validation",
        choices=["pass", "fail"],
        default="pass",
        help="Validation result for the evidence tuple.",
    )
    args = parser.parse_args()

    changed = args.changed_path or _git_changed_paths()
    metrics = evaluate_deadloop_preflight(
        governance_only_streak=args.governance_only_streak,
        changed_paths=changed,
        validation_passed=args.validation == "pass",
    )

    print(json.dumps(asdict(metrics), ensure_ascii=False))
    return 0 if metrics.decision == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
