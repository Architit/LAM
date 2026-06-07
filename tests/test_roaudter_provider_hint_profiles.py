# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def _run_profile(profile: str, monkeypatch) -> dict:
    # Вырубаем все внешние ключи, чтобы тест был стабильным в CI/локально.
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
        {"msg": "Say only: pong", "intent": "chat", "provider_hint": profile},
    )
    _, payload = comm.receive_data()
    return roaudter.answer(payload)


def test_profile_cheap_routes_ok(monkeypatch) -> None:
    out = _run_profile("cheap", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"
    assert out["result"] is not None
    assert out["result"].get("text") is not None


def test_profile_best_routes_ok(monkeypatch) -> None:
    out = _run_profile("best", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"
    assert out["result"] is not None
    assert out["result"].get("text") is not None


def test_profile_fast_routes_ok(monkeypatch) -> None:
    out = _run_profile("fast", monkeypatch)
    assert out["status"] == "ok"
    assert out["provider_used"] == "ollama"
    assert out["result"] is not None
    assert out["result"].get("text") is not None
