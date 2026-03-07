from src.deadloop_patterns import scan_text_for_patterns


def test_scan_text_finds_deadloop_hold_pattern() -> None:
    lines = [
        "state: HOLD_BY_DEADLOOP_BREAK_PROTOCOL",
        "no non-doc code change in chain window",
    ]
    hits = scan_text_for_patterns(lines)
    ids = {h.pattern_id for h in hits}
    assert "deadloop_hold_state" in ids
    assert "missing_delivery_delta" in ids


def test_hold_bypass_pattern_skips_protective_hold_line() -> None:
    lines = [
        "S27 resume validator: HOLD without operator confirmation, PASS with confirmation",
    ]
    hits = scan_text_for_patterns(lines)
    ids = {h.pattern_id for h in hits}
    assert "hold_bypass_attempt" not in ids


def test_deadloop_hold_pattern_skips_backticked_policy_literal() -> None:
    lines = [
        "SAFE CONTAINMENT: set `HOLD_BY_DEADLOOP_BREAK_PROTOCOL` in protocol guidance.",
    ]
    hits = scan_text_for_patterns(lines)
    ids = {h.pattern_id for h in hits}
    assert "deadloop_hold_state" not in ids
