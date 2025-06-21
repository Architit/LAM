from pathlib import Path
import sys

# Подключаем src-папки обоих агентов
BASE = Path(__file__).resolve().parents[1]          # <repo>/LAM
COMM_SRC  = BASE / "LAM/default/agents/comm-agent/src"
CODEX_SRC = BASE / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])
import types
from interfaces import com_agent_interface as _com_mod

# делаем псевдоним, чтобы import "agents.com_agent" внутри Codex-агента не падал
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

from interfaces.com_agent_interface import ComAgent    # из comm-agent
from codex_agent.core import Core                       # из codex-agent

# ── ping → pong ───────────────────────────────────────
comm  = ComAgent()
codex = Core()

comm.register_agent("codex", codex)

comm.send_data("codex", {"msg": "ping"})          # ping
agent, data = comm.receive_data()
print(f"CommAgent получил от {agent}: {data}")

reply = codex.answer(data["msg"])                 # pong
print(f"Codex ответил: {reply}")
