import asyncio
from unittest.mock import patch

import pytest

pytest.importorskip("opentelemetry")

from src.autonomous_engine import AutonomousEngine
from src.communication_layer import CommunicationLayer
from src.event_manager import EventManager
from src.ethics_security import EthicsSecurityModule
from src.memory_time_manager import MemoryTimeManager

pytestmark = pytest.mark.optional


@pytest.mark.asyncio
async def test_start_runs_with_comm_layer():
    engine = AutonomousEngine(
        EventManager(),
        CommunicationLayer(),
        MemoryTimeManager(),
        EthicsSecurityModule(),
        interval=0.01,
    )

    async def dummy_action():
        await asyncio.sleep(0)

    with patch.object(engine, "evaluate_and_act", side_effect=dummy_action):
        await engine.start()
        await asyncio.sleep(0.05)
        await engine.shutdown()


@pytest.mark.asyncio
async def test_shutdown_timeout_when_evaluate_hangs(monkeypatch):
    """Engine.shutdown should finish quickly even if evaluate_and_act hangs."""
    engine = AutonomousEngine(
        EventManager(),
        CommunicationLayer(),
        MemoryTimeManager(),
        EthicsSecurityModule(),
        interval=0.01,
    )

    async def hanging_action() -> None:
        await asyncio.Event().wait()

    monkeypatch.setattr(engine, "evaluate_and_act", hanging_action)

    await engine.start()
    await asyncio.sleep(0.02)
    await asyncio.wait_for(engine.shutdown(timeout=0.05), 0.2)
