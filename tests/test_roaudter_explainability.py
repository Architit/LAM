from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore  # noqa: E402
from roaudter_agent import RoaudterComAgent  # noqa: E402


def test_router_reply_contains_explainability_fields() -> None:
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
    assert "attempts" in out
    assert "selected_chain" in out
    assert "errors" in out
