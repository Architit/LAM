from src.deadloop_resume_gate import evaluate_resume_gate


def test_resume_gate_holds_without_operator_confirmation() -> None:
    res = evaluate_resume_gate(
        code_delta_refs=["src/deadloop_gate.py"],
        test_delta_refs=["tests/test_deadloop_gate.py"],
        validation_command=[".venv/bin/pytest -q tests/test_deadloop_gate.py"],
        validation_result="PASS",
        operator_confirmed=False,
    )
    assert res.decision == "HOLD_BY_DEADLOOP_BREAK_PROTOCOL"
    assert "operator_confirmation" in res.missing_fields


def test_resume_gate_holds_when_validation_not_pass() -> None:
    res = evaluate_resume_gate(
        code_delta_refs=["src/deadloop_gate.py"],
        test_delta_refs=["tests/test_deadloop_gate.py"],
        validation_command=[".venv/bin/pytest -q tests/test_deadloop_gate.py"],
        validation_result="FAIL",
        operator_confirmed=True,
    )
    assert res.decision == "HOLD_BY_DEADLOOP_BREAK_PROTOCOL"
    assert res.reason == "validation_result is not PASS"


def test_resume_gate_passes_with_complete_tuple() -> None:
    res = evaluate_resume_gate(
        code_delta_refs=["src/deadloop_gate.py"],
        test_delta_refs=["tests/test_deadloop_gate.py"],
        validation_command=[".venv/bin/pytest -q tests/test_deadloop_gate.py"],
        validation_result="PASS",
        operator_confirmed=True,
    )
    assert res.decision == "PASS"
