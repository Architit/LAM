from src.deadloop_gate import build_preflight_payload, evaluate_deadloop_preflight


def test_build_preflight_payload_contains_required_fields() -> None:
    changed = ["src/deadloop_gate.py", "tests/test_deadloop_gate.py", "ROADMAP.md"]
    metrics = evaluate_deadloop_preflight(
        governance_only_streak=0,
        changed_paths=changed,
        validation_passed=True,
    )
    payload = build_preflight_payload(
        metrics=metrics,
        changed_paths=changed,
        validation_command=[".venv/bin/pytest -q tests/test_deadloop_gate.py"],
        validation_result="PASS",
    )

    assert payload["governance_only_streak"] == 0
    assert payload["non_doc_code_delta_count"] == 1
    assert payload["test_delta_count"] == 1
    assert payload["journal_only_delta"] is False
    assert payload["engineering_evidence_state"] == "PASS"
    assert payload["decision"] == "PASS"
    assert payload["code_delta_refs"] == ["src/deadloop_gate.py"]
    assert payload["test_delta_refs"] == ["tests/test_deadloop_gate.py"]
    assert payload["validation_result"] == "PASS"
