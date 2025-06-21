from pathlib import Path
import sys, types

ROOT = Path(__file__).resolve().parents[1]          # .../LAM
COMM_SRC  = ROOT / "LAM/default/agents/comm-agent/src"
CODEX_SRC = ROOT / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

from interfaces import com_agent_interface as _com_mod
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

from interfaces.com_agent_interface import ComAgent
from codex_agent.core import Core


def test_ping_pong():
    comm, codex = ComAgent(), Core()
    comm.register_agent("codex", codex)

    comm.send_data("codex", {"msg": "ping"})
    _, data = comm.receive_data()
    reply = codex.answer(data["msg"])

    assert data["msg"] == "ping"
    assert reply.startswith("Processed")
