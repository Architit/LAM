# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def test_strict_provider_openai_bang_returns_error_when_key_missing(monkeypatch) -> None:
    # В strict-режиме (!) fallback запрещён.
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data(
        "roaudter",
        {"msg": "Say only: pong", "intent": "chat", "provider_hint": "openai!"},
    )
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)

    assert out["status"] == "error"
    # Важно: provider_used НЕ должен становиться ollama/ollama_cloud
    assert out.get("provider_used") not in ("ollama", "ollama_cloud")
    assert out.get("error")  # любое непустое описание ошибки


def test_strict_provider_ollama_bang_succeeds(monkeypatch) -> None:
    # STRICT на доступном провайдере должен отрабатывать как обычно (просто без fallback).
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    comm.send_data(
        "roaudter",
        {"msg": "Say only: pong", "intent": "chat", "provider_hint": "ollama!"},
    )
    _, payload = comm.receive_data()

    out = roaudter.answer(payload)

    assert out["status"] == "ok"
    assert out.get("provider_used") == "ollama"
