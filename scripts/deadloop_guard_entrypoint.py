#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, rel_path: str) -> Any:
    module_path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _git_changed_paths() -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="deadloop_guard_entrypoint",
        description="Unified anti-deadloop gate for S* resume: preflight + resume tuple.",
    )
    parser.add_argument("--governance-only-streak", type=int, required=True)
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--validation-result", default="PASS")
    parser.add_argument("--validation-command", action="append", default=[])
    parser.add_argument("--operator-confirmed", action="store_true")
    args = parser.parse_args()

    gate = _load_module("deadloop_gate_mod", "src/deadloop_gate.py")
    resume = _load_module("deadloop_resume_mod", "src/deadloop_resume_gate.py")

    changed = args.changed_path or _git_changed_paths()
    pre = gate.evaluate_deadloop_preflight(
        governance_only_streak=args.governance_only_streak,
        changed_paths=changed,
        validation_passed=args.validation_result.strip().upper() == "PASS",
    )
    payload = gate.build_preflight_payload(
        metrics=pre,
        changed_paths=changed,
        validation_command=args.validation_command,
        validation_result=args.validation_result.strip().upper(),
    )

    if pre.decision != "PASS":
        print(json.dumps({"preflight": asdict(pre), "payload": payload}, ensure_ascii=False))
        return 5

    res = resume.evaluate_resume_gate(
        code_delta_refs=list(payload["code_delta_refs"]),
        test_delta_refs=list(payload["test_delta_refs"]),
        validation_command=list(payload["validation_command"]),
        validation_result=str(payload["validation_result"]),
        operator_confirmed=args.operator_confirmed,
    )
    out = {"preflight": asdict(pre), "payload": payload, "resume": asdict(res)}
    print(json.dumps(out, ensure_ascii=False))
    return 0 if res.decision == "PASS" else 6


if __name__ == "__main__":
    raise SystemExit(main())
