# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def test_roaudter_metrics_mirrors_top_level_v11_minimum() -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data("roaudter", {"msg": "Say only: pong", "intent": "chat"})
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)

    assert out["status"] == "ok"
    assert "metrics" in out and isinstance(out["metrics"], dict)

    # Phase 1.1 minimum: эти поля должны быть и сверху, и в metrics
    for k in ("provider_used", "latency_ms", "attempts"):
        assert k in out
        assert k in out["metrics"]
        assert out["metrics"][k] == out[k]
