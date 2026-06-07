# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
from src.taskarid_agent import TaskaridAgent


def test_taskarid_returns_plan_with_shared_trace():
    a = TaskaridAgent()
    out = a.answer({"goal": "Say only: pong", "intent": "chat"})

    assert out["status"] == "ok"
    assert "context" in out and out["context"]["trace_id"]
    assert "plan" in out and len(out["plan"]) >= 1
    assert out["plan"][0]["context"]["trace_id"] == out["context"]["trace_id"]
