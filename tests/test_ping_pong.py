"""Integration-тест связи ComAgent ↔ Codex Core."""

from pathlib import Path
import sys
import types

# ── динамически подключаем src-папки подмодулей ─────────────────────────────────
ROOT      = Path(__file__).resolve().parents[1]               # …/LAM
COMM_SRC  = ROOT / "LAM/default/agents/comm-agent/src"
CODEX_SRC = ROOT / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

# делаем алиасы, чтобы import "agents.com_agent" внутри Codex-агента не падал
from interfaces import com_agent_interface as _com_mod        # type: ignore
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

# ── сами классы ────────────────────────────────────────────────────────────────
from interfaces.com_agent_interface import ComAgent
from codex_agent.core import Core


def test_ping_pong_roundtrip() -> None:
    """ComAgent ↔ Codex: ping → pong."""
    comm, codex = ComAgent(), Core()
    comm.register_agent("codex", codex)

    # ping
    assert comm.send_data("codex", {"msg": "ping"})

    # pong
    sender, payload = comm.receive_data()
    assert sender == "codex"
    assert payload == {"msg": "ping"}

    reply = codex.answer(payload["msg"])
    assert reply == {"reply": "pong"}
