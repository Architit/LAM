from src.snapshot_pointer import upsert_active_next_target


def test_upsert_active_pointer_appends_when_missing() -> None:
    text = "# WORKFLOW SNAPSHOT\n\nbody\n"
    out = upsert_active_next_target(text, "S27_RESUME", "2026-02-17T22:20:00Z")
    assert "## Active Pointer" in out
    assert "- active_next_target: S27_RESUME" in out


def test_upsert_active_pointer_replaces_existing() -> None:
    text = (
        "# WORKFLOW SNAPSHOT\n\n"
        "## Active Pointer\n"
        "- active_next_target: OLD\n"
        "- updated_utc: 2026-01-01T00:00:00Z\n"
    )
    out = upsert_active_next_target(text, "S27_RESUME", "2026-02-17T22:20:00Z")
    assert out.count("## Active Pointer") == 1
    assert "- active_next_target: S27_RESUME" in out
    assert "- active_next_target: OLD" not in out
