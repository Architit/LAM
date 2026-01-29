from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def test_result_contains_unified_usage_fields() -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data(
        "roaudter",
        {"msg": "Say only: pong", "intent": "chat", "provider_hint": "ollama"},
    )
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)

    assert out["status"] == "ok"
    assert "latency_ms" in out

    # unified usage fields (must exist even if provider doesn't report them)
    assert "tokens" in out
    assert "usage" in out
    assert out["usage"] is None or isinstance(out["usage"], dict)
