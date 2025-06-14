import asyncio
from unittest.mock import AsyncMock, patch

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


@pytest.mark.asyncio
async def test_start_runs_with_comm_layer():
    engine = AutonomousEngine(
        EventManager(),
        CommunicationLayer(),
        MemoryTimeManager(),
        EthicsSecurityModule(),
    )

    with patch.object(engine, "evaluate_and_act", new=AsyncMock()) as mock_eval:
        start_task = asyncio.create_task(engine.start(interval=0.01))
        await asyncio.sleep(0.05)
        engine._shutdown_event.set()
        await start_task
        assert mock_eval.await_count > 0
