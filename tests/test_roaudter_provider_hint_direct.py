# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def _run_hint(hint: str, monkeypatch) -> dict:
    # Убираем ключи, чтобы тест был стабильным и проверял fallback.
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("GROK_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data(
        "roaudter",
        {"msg": "Say only: pong", "intent": "chat", "provider_hint": hint},
    )
    _, payload = comm.receive_data()
    return roaudter.answer(payload)


def test_direct_hint_openai_falls_back_without_key(monkeypatch) -> None:
    out = _run_hint("openai", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"


def test_direct_hint_gemini_falls_back_without_key(monkeypatch) -> None:
    out = _run_hint("gemini", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"


def test_direct_hint_claude_falls_back_without_key(monkeypatch) -> None:
    out = _run_hint("claude", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"


def test_direct_hint_grok_falls_back_without_key(monkeypatch) -> None:
    out = _run_hint("grok", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"


def test_direct_hint_deepseek_falls_back_without_key(monkeypatch) -> None:
    out = _run_hint("deepseek", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"
