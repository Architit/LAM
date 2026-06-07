# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore


class Dummy:
    pass


def test_comm_agent_enforces_envelope_on_reply_like_payload() -> None:
    comm = ComAgent()
    comm.register_agent("x", Dummy())

    reply_like = {
        "status": "ok",
        "provider_used": "dummy",
        "context": {"trace_id": "t", "task_id": "x"},
        "task_id": "x",
    }

    comm.send_data("x", reply_like)
    _, out = comm.receive_data()

    assert out["status"] == "ok"
    assert out["context"]["trace_id"] == "t"
    assert out["context"]["task_id"] == "x"
    assert "result" in out
    assert "error" in out
    assert "metrics" in out and isinstance(out["metrics"], dict)
