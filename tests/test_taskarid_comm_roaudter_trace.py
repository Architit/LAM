# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent

from src.taskarid_agent import TaskaridAgent


def test_taskarid_to_comm_to_roaudter_trace_roundtrip() -> None:
    # 1) taskarid builds a plan (mission -> tasks)
    taskarid = TaskaridAgent()
    plan_out = taskarid.answer({"goal": "Say only: pong", "intent": "chat", "provider_hint": "ollama"})
    assert plan_out["status"] == "ok"
    trace_id = plan_out["context"]["trace_id"]
    task_id = plan_out["context"]["task_id"]

    task = plan_out["plan"][0]
    expected_task_id = task["context"]["task_id"]

    # 2) comm-agent injects/keeps context + taskarid while enqueuing
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data("roaudter", task)
    _, payload = comm.receive_data()

    assert "context" in payload
    assert payload["context"]["trace_id"] == trace_id
    assert payload["context"]["task_id"] == expected_task_id
    assert "taskarid" in payload

    # 3) roaudter answers and must echo context back.
    # Provider availability is validated in dedicated router/provider tests.
    out = roaudter.answer(payload)

    assert out["status"] in ("ok", "error")
    assert "context" in out
    assert out["context"]["trace_id"] == trace_id
    assert out["context"]["task_id"] == expected_task_id
    assert "taskarid" in out
