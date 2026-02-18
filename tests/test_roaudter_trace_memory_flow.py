# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent

from src.memory_core import MemoryCore


def test_trace_context_propagates_to_memory(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("LAM_MEMORY_PATH", str(tmp_path / "memstore"))
    monkeypatch.setenv("ROAUDTER_MEMORY_TRACE", "1")
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("GROK_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    trace_id = "tr-dl3-e2"
    task_id = "t-dl3-e2"

    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data(
        "roaudter",
        {
            "msg": "Say only: pong",
            "intent": "chat",
            "context": {"trace_id": trace_id, "task_id": task_id},
        },
    )
    _, payload = comm.receive_data()
    out = roaudter.answer(payload)

    assert out["context"]["trace_id"] == trace_id
    assert out["context"]["task_id"] == task_id

    mem = MemoryCore(Path(tmp_path / "memstore"))
    rows = mem.retrieve_memory({"associations": [trace_id]})
    assert rows, "expected at least one memory record linked to trace_id"

    matched = [r for r in rows if r.get("attributes", {}).get("task_id") == task_id]
    assert matched, "expected trace-linked memory record with matching task_id"
