# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent

from src.taskarid_agent import TaskaridAgent


def _assert_envelope(x: dict) -> None:
    assert isinstance(x, dict)
    for k in ("status", "context", "result", "error", "metrics"):
        assert k in x, f"missing envelope field: {k}"
    assert isinstance(x["context"], dict)
    assert x["context"].get("trace_id")
    assert x["context"].get("task_id")
    assert isinstance(x["metrics"], dict)


def test_taskarid_envelope_standard() -> None:
    out = TaskaridAgent().answer({"goal": "ping", "intent": "chat", "provider_hint": "ollama"})
    _assert_envelope(out)


def test_roaudter_envelope_standard_roundtrip() -> None:
    plan_out = TaskaridAgent().answer({"goal": "Say only: pong", "intent": "chat", "provider_hint": "ollama"})
    task = plan_out["plan"][0]

    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data("roaudter", task)
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)
    _assert_envelope(out)
