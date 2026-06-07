# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import json

from roaudter_agent import RoaudterComAgent


def test_roaudter_emits_route_result_deliver_logs_jsonl(capsys, monkeypatch):
    monkeypatch.setenv("LAM_LOG_LEVEL", "info")
    monkeypatch.setenv("LAM_LOG_EVENTS", "roaudter.route,roaudter.result,roaudter.deliver")

    r = RoaudterComAgent()

    payload = {
        "task_id": "t-1",
        "agent": "comm-agent",
        "intent": "chat",
        "msg": "Say only: pong",
        "context": {"trace_id": "tr-123", "task_id": "t-1"},
    }

    out = r.answer(payload)
    assert isinstance(out, dict)
    assert out.get("task_id") == "t-1"

    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert len(lines) >= 2  # минимум route + deliver (result тоже должен быть)

    events = []
    for ln in lines:
        try:
            events.append(json.loads(ln))
        except Exception as e:
            raise AssertionError(f"Non-JSON log line: {ln!r}") from e

    names = [e.get("event") for e in events]
    assert "roaudter.route" in names
    assert "roaudter.result" in names
    assert "roaudter.deliver" in names

    route = next(e for e in events if e.get("event") == "roaudter.route")
    assert route.get("level") == "info"
    assert route.get("intent") == "chat"
    assert route.get("task_id") == "t-1"
    assert route.get("trace_id") == "tr-123"

    deliver = next(e for e in events if e.get("event") == "roaudter.deliver")
    assert deliver.get("level") == "info"
    assert deliver.get("recipient") == "comm-agent"
    assert deliver.get("task_id") == "t-1"
    assert deliver.get("trace_id") == "tr-123"
