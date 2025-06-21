from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]              # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
CODEX_SRC = ROOT / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

from interfaces import com_agent_interface as _com_mod  # noqa: E402

sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

from interfaces.com_agent_interface import ComAgent  # noqa: E402
from codex_agent.core import Core  # noqa: E402


def test_ping_pong() -> None:
    comm = ComAgent()
    codex = Core()
    comm.register_agent("codex", codex)

    comm.send_data("codex", {"msg": "ping"})
    _, payload = comm.receive_data()

    assert payload["msg"] == "ping"
    reply = codex.answer(payload["msg"])
    assert reply.startswith("Processed")
