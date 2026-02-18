#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def _load_resume_module():
    module_path = ROOT / "src" / "deadloop_resume_gate.py"
    spec = importlib.util.spec_from_file_location("deadloop_resume_gate_module", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load resume gate module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="deadloop_resume_gate",
        description="Validate DEADLOOP resume tuple before S27 gate decision.",
    )
    parser.add_argument("--code-delta-ref", action="append", default=[])
    parser.add_argument("--test-delta-ref", action="append", default=[])
    parser.add_argument("--validation-command", action="append", default=[])
    parser.add_argument("--validation-result", default="")
    parser.add_argument("--operator-confirmed", action="store_true")
    args = parser.parse_args()

    mod = _load_resume_module()
    res = mod.evaluate_resume_gate(
        code_delta_refs=args.code_delta_ref,
        test_delta_refs=args.test_delta_ref,
        validation_command=args.validation_command,
        validation_result=args.validation_result,
        operator_confirmed=args.operator_confirmed,
    )
    print(json.dumps({"decision": res.decision, "missing_fields": res.missing_fields, "reason": res.reason}, ensure_ascii=False))
    return 0 if res.decision == "PASS" else 4


if __name__ == "__main__":
    raise SystemExit(main())
