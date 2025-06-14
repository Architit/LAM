import asyncio
from unittest.mock import AsyncMock

import pytest

from src.autonomous_engine import AutonomousEngine
from src.communication_layer import CommunicationLayer
from src.event_manager import EventManager
from src.memory_time_manager import MemoryTimeManager
from src.ethics_security import EthicsSecurityModule


@pytest.mark.asyncio
async def test_schedule_evaluate_invokes_action():
    eng = AutonomousEngine(
        EventManager(),
        CommunicationLayer(),
        MemoryTimeManager(),
        EthicsSecurityModule(),
    )
    eng.evaluate_and_act = AsyncMock()
    await eng._schedule_evaluate()
    eng.evaluate_and_act.assert_awaited_once()


@pytest.mark.asyncio
async def test_shutdown_cancels_tasks():
    eng = AutonomousEngine(
        EventManager(),
        CommunicationLayer(),
        MemoryTimeManager(),
        EthicsSecurityModule(),
    )
    task = asyncio.create_task(asyncio.sleep(0.01))
    eng._tasks.add(task)
    await eng.shutdown()
    assert task.cancelled()
