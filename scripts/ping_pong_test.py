from pathlib import Path
import sys
import types

# ─── добавить пути к исходникам агентов ────────────────────────────────────────
BASE = Path(__file__).resolve().parents[1]              # …/LAM
COMM_SRC = BASE / "LAM/default/agents/comm-agent/src"
CODEX_SRC = BASE / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

# ─── псевдоним, чтобы import "agents.com_agent" внутри Codex-агента не падал ──
from interfaces import com_agent_interface as _com_mod  # noqa: E402

sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

# ─── настоящие импорты после настройки путей ──────────────────────────────────
from interfaces.com_agent_interface import ComAgent  # noqa: E402
from codex_agent.core import Core  # noqa: E402

# ─── быстрый ручной прогон ────────────────────────────────────────────────────
if __name__ == "__main__":
    com = ComAgent()
    codex = Core()
    com.register_agent("codex", codex)

    com.send_data("codex", {"msg": "ping"})
    sender, payload = com.receive_data()
    print(f"CommAgent получил от {sender}: {payload}")

    answer = codex.answer(payload["msg"])
    print(f"Codex ответил: {answer}")
