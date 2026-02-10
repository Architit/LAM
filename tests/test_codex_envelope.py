from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
CODEX_SRC = ROOT / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

from interfaces import com_agent_interface as _com_mod  # noqa: E402
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

from codex_agent.core import Core  # noqa: E402


def test_codex_answer_payload_returns_envelope_v1() -> None:
    codex = Core()
    payload = {
        "msg": "ping",
        "context": {"trace_id": "t-1", "task_id": "task-1"},
    }
    out = codex.answer(payload)

    assert out["status"] == "ok"
    assert out["context"]["trace_id"] == "t-1"
    assert out["context"]["task_id"] == "task-1"
    assert out["error"] is None
    assert isinstance(out["metrics"], dict)
    assert out["result"]["reply"] == "pong"
