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


def test_comm_agent_enforces_envelope_on_legacy_reply_payload() -> None:
    comm = ComAgent()
    comm.register_agent("x", Dummy())

    legacy_reply = {"reply": "pong"}

    comm.send_data("x", legacy_reply)
    _, out = comm.receive_data()

    assert out["status"] == "ok"
    assert "context" in out and isinstance(out["context"], dict)
    assert out["error"] is None
    assert "metrics" in out and isinstance(out["metrics"], dict)

    # legacy допускается, но result должен существовать
    assert "result" in out
    # и внутри result ожидаем увидеть reply (минимум)
    if isinstance(out["result"], dict):
        assert out["result"].get("reply") == "pong"
