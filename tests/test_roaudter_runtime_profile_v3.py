# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def _strip_cloud_keys(monkeypatch) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("GROK_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


def test_runtime_profile_ci_applies_when_hint_missing(monkeypatch) -> None:
    _strip_cloud_keys(monkeypatch)
    monkeypatch.setenv("ROAUDTER_RUNTIME_PROFILE", "ci")

    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data("roaudter", {"msg": "Say only: pong", "intent": "chat"})
    _, payload = comm.receive_data()
    out = roaudter.answer(payload)

    assert out["status"] == "ok"
    assert out["metrics"].get("policy_hint") == "cheap"
    assert out["metrics"].get("policy_hint_source") == "runtime_profile"


def test_explicit_hint_overrides_runtime_profile(monkeypatch) -> None:
    _strip_cloud_keys(monkeypatch)
    monkeypatch.setenv("ROAUDTER_RUNTIME_PROFILE", "smoke")

    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data(
        "roaudter",
        {"msg": "Say only: pong", "intent": "chat", "provider_hint": "best"},
    )
    _, payload = comm.receive_data()
    out = roaudter.answer(payload)

    assert out["status"] == "ok"
    assert out["metrics"].get("policy_hint") == "best"
    assert out["metrics"].get("policy_hint_source") == "explicit"
