# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent
from roaudter_agent.providers.base import ProviderError
from roaudter_agent.providers.ollama import OllamaAdapter


def test_comm_to_roaudter_roundtrip() -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data("roaudter", {"msg": "Say only: pong", "intent": "chat"})
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)

    assert out["status"] == "ok"
    assert out["provider_used"] in ("ollama", "ollama_cloud")
    assert "result" in out and out["result"] is not None
    assert out["result"].get("text") is not None

def test_comm_to_roaudter_cloud_quota_fallback_to_local(monkeypatch) -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)
    original_generate = OllamaAdapter.generate

    def _patched_generate(self: OllamaAdapter, task: object) -> object:
        if self.name == "ollama_cloud":
            raise ProviderError(
                "ollama cloud quota exhausted",
                code="quota_exhausted",
                http_status=429,
                retryable=False,
                meta={"model": "glm-4.7:cloud"},
            )
        return original_generate(self, task)  # type: ignore[arg-type]

    monkeypatch.setattr(OllamaAdapter, "generate", _patched_generate)

    comm.send_data(
        "roaudter",
        {
            "msg": "Say only: pong",
            "intent": "chat",
            "constraints": {"model": "glm-4.7:cloud"},
        },
    )
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)

    # При выбитой cloud-квоте роутер должен уйти на локальную Ollama
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"
    assert out["result"] is not None
    assert out["result"].get("text") is not None
