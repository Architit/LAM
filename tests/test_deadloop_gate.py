from src.deadloop_gate import evaluate_deadloop_preflight


def test_deadloop_gate_holds_when_streak_high_and_no_test_delta() -> None:
    m = evaluate_deadloop_preflight(
        governance_only_streak=5,
        changed_paths=["src/event_manager.py", "DEV_LOGS.md"],
        validation_passed=True,
    )
    assert m.decision == "HOLD_BY_DEADLOOP_BREAK_PROTOCOL"
    assert m.non_doc_code_delta_count == 1
    assert m.test_delta_count == 0


def test_deadloop_gate_holds_for_numbering_journal_only_cycle() -> None:
    m = evaluate_deadloop_preflight(
        governance_only_streak=0,
        changed_paths=["TASK_LIST.md", "ROADMAP.md", "DEV_LOGS.md"],
        validation_passed=True,
    )
    assert m.decision == "HOLD_BY_DEADLOOP_BREAK_PROTOCOL"
    assert m.journal_only_delta is True
    assert m.reason == "numbering/journal-only cycle without structural delta"


def test_deadloop_gate_holds_when_validation_failed() -> None:
    m = evaluate_deadloop_preflight(
        governance_only_streak=1,
        changed_paths=["src/event_manager.py", "tests/test_event_manager.py"],
        validation_passed=False,
    )
    assert m.decision == "HOLD_BY_DEADLOOP_BREAK_PROTOCOL"
    assert m.engineering_evidence_state == "MISSING_OR_FAILED"


def test_deadloop_gate_passes_when_tuple_complete() -> None:
    m = evaluate_deadloop_preflight(
        governance_only_streak=2,
        changed_paths=["src/tma/api.py", "tests/test_tma_aggregator.py", "ROADMAP.md"],
        validation_passed=True,
    )
    assert m.decision == "PASS"
    assert m.non_doc_code_delta_count == 1
    assert m.test_delta_count == 1
    assert m.journal_only_delta is False
    assert m.engineering_evidence_state == "PASS"
