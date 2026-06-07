# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore


def test_comm_agent_logs_enqueue_dequeue_jsonl(capsys, monkeypatch):
    # включаем только нужные события (и уровень), чтобы шум был минимальный
    monkeypatch.setenv("LAM_LOG_EVENTS", "comm.enqueue,comm.dequeue")
    monkeypatch.setenv("LAM_LOG_LEVEL", "info")

    comm = ComAgent()
    comm.register_agent("worker", object())

    payload = {
        "intent": "ping",
        "context": {"trace_id": "t-123", "task_id": "task-1"},
        "data": {"hello": "world"},
    }

    assert comm.send_data("worker", payload) is True
    sender, data = comm.receive_data()
    assert sender == "worker"
    assert data == payload

    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert len(lines) >= 2

    events = []
    for ln in lines:
        try:
            events.append(json.loads(ln))
        except Exception as e:
            raise AssertionError(f"Non-JSON log line: {ln!r}") from e

    names = [e.get("event") for e in events]
    assert "comm.enqueue" in names
    assert "comm.dequeue" in names

    enqueue = next(e for e in events if e.get("event") == "comm.enqueue")
    assert enqueue.get("level") == "info"
    assert enqueue.get("recipient") == "worker"
    assert enqueue.get("intent") == "ping"
    assert enqueue.get("task_id") == "task-1"
    assert enqueue.get("trace_id") == "t-123"
    assert enqueue.get("msg") in ("enqueue", "queued", "comm.enqueue", "enqueue message", "enqueue")  # tolerant

    dequeue = next(e for e in events if e.get("event") == "comm.dequeue")
    assert dequeue.get("level") == "info"
    assert dequeue.get("sender") == "worker"
    assert dequeue.get("task_id") == "task-1"
    assert dequeue.get("trace_id") == "t-123"
