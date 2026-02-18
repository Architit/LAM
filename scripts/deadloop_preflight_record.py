#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEV_LOGS = ROOT / "DEV_LOGS.md"
SNAPSHOT = ROOT / "WORKFLOW_SNAPSHOT_STATE.md"


def _load_gate_module() -> Any:
    module_path = ROOT / "src" / "deadloop_gate.py"
    spec = importlib.util.spec_from_file_location("deadloop_gate_module", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load deadloop gate module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _git_changed_paths() -> list[str]:
    cmd = ["git", "diff", "--name-only", "HEAD"]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _append_dev_logs(ts_human: str, payload: dict[str, object]) -> None:
    line = (
        f"{ts_human} UTC — Governance: DEADLOOP_PREFLIGHT_GATE payload — "
        f"governance_only_streak={payload['governance_only_streak']}, "
        f"non_doc_code_delta_count={payload['non_doc_code_delta_count']}, "
        f"test_delta_count={payload['test_delta_count']}, "
        f"engineering_evidence_state={payload['engineering_evidence_state']}, "
        f"decision={payload['decision']}, "
        f"code_delta_refs={payload['code_delta_refs']}, "
        f"test_delta_refs={payload['test_delta_refs']}, "
        f"validation_command={payload['validation_command']}, "
        f"validation_result={payload['validation_result']}."
    )
    with open(DEV_LOGS, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _append_snapshot(ts_iso: str, payload: dict[str, object]) -> None:
    ts_human = ts_iso.replace("T", " ").replace("Z", "")
    block = [
        "",
        "## Governance Sync",
        f"- {ts_human} UTC — deadloop-preflight-payload-record-v1",
        "- protocol_source: RADRILONIUMA-PROJECT",
        "- pointer_ref: `INTERACTION_PROTOCOL.md` + `P4_PHASE43_DEADLOOP_BREAK_PROTOCOL_CONTRACT.md`",
        f"- governance_only_streak: {payload['governance_only_streak']}",
        f"- non_doc_code_delta_count: {payload['non_doc_code_delta_count']}",
        f"- test_delta_count: {payload['test_delta_count']}",
        f"- engineering_evidence_state: {payload['engineering_evidence_state']}",
        f"- deadloop_preflight_decision: {payload['decision']}",
        f"- deadloop_preflight_reason: {payload['reason']}",
        f"- code_delta_refs: {payload['code_delta_refs']}",
        f"- test_delta_refs: {payload['test_delta_refs']}",
        f"- validation_command: {payload['validation_command']}",
        f"- validation_result: {payload['validation_result']}",
        "- branch: phase2/observability",
        "- git_status: ## phase2/observability...origin/phase2/observability",
    ]
    with open(SNAPSHOT, "a", encoding="utf-8") as fh:
        fh.write("\n".join(block) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="deadloop_preflight_record",
        description="Evaluate deadloop preflight and optionally persist canonical payload.",
    )
    parser.add_argument("--governance-only-streak", type=int, required=True)
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--validation", choices=["pass", "fail"], default="pass")
    parser.add_argument("--validation-command", action="append", default=[])
    parser.add_argument("--write-dev-logs", action="store_true")
    parser.add_argument("--write-snapshot", action="store_true")
    args = parser.parse_args()

    gate = _load_gate_module()
    changed = args.changed_path or _git_changed_paths()
    metrics = gate.evaluate_deadloop_preflight(
        governance_only_streak=args.governance_only_streak,
        changed_paths=changed,
        validation_passed=args.validation == "pass",
    )
    payload = gate.build_preflight_payload(
        metrics=metrics,
        changed_paths=changed,
        validation_command=args.validation_command,
        validation_result="PASS" if args.validation == "pass" else "FAIL",
    )

    print(json.dumps({"metrics": asdict(metrics), "payload": payload}, ensure_ascii=False))

    now = datetime.now(timezone.utc)
    ts_iso = now.isoformat().replace("+00:00", "Z")
    ts_human = now.strftime("%Y-%m-%d %H:%M")
    if args.write_dev_logs:
        _append_dev_logs(ts_human, payload)
    if args.write_snapshot:
        _append_snapshot(ts_iso, payload)

    return 0 if metrics.decision == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
