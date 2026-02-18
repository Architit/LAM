import json

import pytest

from roaudter_agent import RoaudterComAgent
from src.event_manager import EventManager
from src.memory_core import MemoryCore

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore  # noqa: E402


# comm-agent is a submodule; import path stays stable in repo layout


@pytest.mark.asyncio
async def test_observability_smoke_e2e(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("LAM_LOG_LEVEL", "info")
    monkeypatch.setenv(
        "LAM_LOG_EVENTS",
        ",".join(
            [
                # comm
                "comm.enqueue",
                "comm.dequeue",
                # roaudter
                "roaudter.route",
                "roaudter.result",
                "roaudter.deliver",
                # memory
                "mem.write",
                "mem.read",
                "mem.search",
                # events
                "evt.emit",
                "evt.dispatch",
            ]
        ),
    )
    monkeypatch.setenv("LAM_MEMORY_PATH", str(tmp_path / "memstore"))

    # --- comm -> roaudter roundtrip (minimal) ---
    comm = ComAgent()
    comm.register_agent("roaudter", object())  # registry check only

    payload = {
        "task_id": "t-e2e",
        "agent": "comm-agent",
        "intent": "chat",
        "msg": "Say only: pong",
        "context": {"trace_id": "tr-e2e", "task_id": "t-e2e"},
    }
    assert comm.send_data("roaudter", payload) is True
    sender, task = comm.receive_data()
    assert sender == "roaudter"
    assert isinstance(task, dict)

    ro = RoaudterComAgent()
    _reply = ro.answer(task)
    assert isinstance(_reply, dict)
    assert _reply.get("task_id") == "t-e2e"

    # --- memory ops (force mem.* logs) ---
    mem = MemoryCore()
    mem.add_memory(
        {
            "name": "n1",
            "timestamp": "2026-01-01T00:00:00",
            "content": "hello world memory smoke test",
        }
    )
    _ = mem.retrieve_memory({"tags": ["hello"]})
    _ = mem.retrieve_by_embedding([0.1, 0.2, 0.3], k=1)

    # --- event ops (force evt.* logs) ---
    mgr = EventManager()
    seen = {"count": 0}

    async def h(_data):
        seen["count"] += 1

    mgr.register_listener("x", h)
    mgr.emit_event("x", {"k": "v"})
    await mgr.dispatch()
    assert seen["count"] == 1

    # --- parse stdout JSONL and assert presence ---
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert lines, "No JSONL logs captured on stdout"

    events = []
    for ln in lines:
        try:
            events.append(json.loads(ln))
        except Exception as e:
            raise AssertionError(f"Non-JSON log line: {ln!r}") from e

    names = {e.get("event") for e in events}
    required = {
        "comm.enqueue",
        "comm.dequeue",
        "roaudter.route",
        "roaudter.result",
        "roaudter.deliver",
        "mem.write",
        "mem.read",
        "mem.search",
        "evt.emit",
        "evt.dispatch",
    }
    missing = required - names
    assert not missing, f"Missing events: {sorted(missing)}"
