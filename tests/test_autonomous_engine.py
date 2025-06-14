import asyncio
from unittest.mock import patch

import pytest

from src.autonomous_engine import AutonomousEngine
from src.communication_layer import CommunicationLayer
from src.event_manager import EventManager
from src.ethics_security import EthicsSecurityModule
from src.memory_time_manager import MemoryTimeManager


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
