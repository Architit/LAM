import json

import pytest

from src.event_manager import EventManager


@pytest.mark.asyncio
async def test_event_manager_emits_evt_logs_jsonl(capsys, monkeypatch):
    monkeypatch.setenv("LAM_LOG_LEVEL", "info")
    monkeypatch.setenv("LAM_LOG_EVENTS", "evt.emit,evt.dispatch")

    mgr = EventManager()

    seen = {"count": 0}

    async def handler(data):
        seen["count"] += 1

    mgr.register_listener("x", handler)
    mgr.emit_event("x", {"k": "v"})
    await mgr.dispatch()
    assert seen["count"] == 1

    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert len(lines) >= 2

    events = []
    for ln in lines:
        try:
            events.append(json.loads(ln))
        except Exception as e:
            raise AssertionError(f"Non-JSON log line: {ln!r}") from e

    names = [e.get("event") for e in events]
    assert "evt.emit" in names
    assert "evt.dispatch" in names

    emit = next(e for e in events if e.get("event") == "evt.emit")
    assert emit.get("level") == "info"
    assert emit.get("event_type") == "x"

    disp = next(e for e in events if e.get("event") == "evt.dispatch")
    assert disp.get("level") == "info"
    assert disp.get("event_type") == "x"
    assert disp.get("listeners_count") == 1
