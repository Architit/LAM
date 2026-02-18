from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class DeadloopPreflightMetrics:
    governance_only_streak: int
    non_doc_code_delta_count: int
    test_delta_count: int
    journal_only_delta: bool
    engineering_evidence_state: str
    decision: str
    reason: str


_NUMBERING_SURFACE_FILES = {
    "task_list.md",
    "roadmap.md",
    "dev_logs.md",
    "workflow_snapshot_state.md",
}


def _is_non_doc_code(path: str) -> bool:
    p = path.strip().lower()
    if not p:
        return False
    if p.startswith("tests/"):
        return False
    if p.endswith(".md") or p.endswith(".txt") or p.endswith(".rst"):
        return False
    if p.endswith(".yaml") or p.endswith(".yml") or p.endswith(".json"):
        return False
    return p.endswith(".py") or p.endswith(".sh")


def _is_test_delta(path: str) -> bool:
    p = path.strip().lower()
    if not p:
        return False
    return p.startswith("tests/") and p.endswith(".py")


def _touches_numbering_surface(changed_paths: Iterable[str]) -> bool:
    for raw in changed_paths:
        p = (raw or "").strip().lower()
        if not p:
            continue
        leaf = p.rsplit("/", 1)[-1]
        if leaf in _NUMBERING_SURFACE_FILES:
            return True
    return False


def split_delta_refs(changed_paths: Iterable[str]) -> tuple[list[str], list[str]]:
    changed = [p for p in changed_paths if p and p.strip()]
    code_refs = [p for p in changed if _is_non_doc_code(p)]
    test_refs = [p for p in changed if _is_test_delta(p)]
    return code_refs, test_refs


def evaluate_deadloop_preflight(
    *,
    governance_only_streak: int,
    changed_paths: Iterable[str],
    validation_passed: bool,
) -> DeadloopPreflightMetrics:
    changed = [p for p in changed_paths if p and p.strip()]
    code_refs, test_refs = split_delta_refs(changed)
    code_count = len(code_refs)
    test_count = len(test_refs)
    journal_only_delta = bool(changed) and code_count == 0 and test_count == 0

    evidence_ok = code_count > 0 and test_count > 0 and validation_passed
    engineering_state = "PASS" if evidence_ok else "MISSING_OR_FAILED"

    if journal_only_delta and _touches_numbering_surface(changed):
        return DeadloopPreflightMetrics(
            governance_only_streak=governance_only_streak,
            non_doc_code_delta_count=code_count,
            test_delta_count=test_count,
            journal_only_delta=journal_only_delta,
            engineering_evidence_state=engineering_state,
            decision="HOLD_BY_DEADLOOP_BREAK_PROTOCOL",
            reason="numbering/journal-only cycle without structural delta",
        )

    if governance_only_streak >= 3 and (code_count == 0 or test_count == 0):
        return DeadloopPreflightMetrics(
            governance_only_streak=governance_only_streak,
            non_doc_code_delta_count=code_count,
            test_delta_count=test_count,
            journal_only_delta=journal_only_delta,
            engineering_evidence_state=engineering_state,
            decision="HOLD_BY_DEADLOOP_BREAK_PROTOCOL",
            reason="streak>=3 with missing code/test delta",
        )

    if not evidence_ok:
        return DeadloopPreflightMetrics(
            governance_only_streak=governance_only_streak,
            non_doc_code_delta_count=code_count,
            test_delta_count=test_count,
            journal_only_delta=journal_only_delta,
            engineering_evidence_state=engineering_state,
            decision="HOLD_BY_DEADLOOP_BREAK_PROTOCOL",
            reason="engineering evidence tuple is incomplete or validation failed",
        )

    return DeadloopPreflightMetrics(
        governance_only_streak=governance_only_streak,
        non_doc_code_delta_count=code_count,
        test_delta_count=test_count,
        journal_only_delta=journal_only_delta,
        engineering_evidence_state=engineering_state,
        decision="PASS",
        reason="preflight conditions satisfied",
    )


def build_preflight_payload(
    *,
    metrics: DeadloopPreflightMetrics,
    changed_paths: Iterable[str],
    validation_command: list[str],
    validation_result: str,
) -> dict[str, object]:
    code_refs, test_refs = split_delta_refs(changed_paths)
    return {
        "governance_only_streak": metrics.governance_only_streak,
        "non_doc_code_delta_count": metrics.non_doc_code_delta_count,
        "test_delta_count": metrics.test_delta_count,
        "journal_only_delta": metrics.journal_only_delta,
        "engineering_evidence_state": metrics.engineering_evidence_state,
        "decision": metrics.decision,
        "reason": metrics.reason,
        "code_delta_refs": code_refs,
        "test_delta_refs": test_refs,
        "validation_command": validation_command,
        "validation_result": validation_result,
    }
