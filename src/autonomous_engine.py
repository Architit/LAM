# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# -*- coding: utf-8 -*-
"""Proactive autonomous engine for LAM."""

from __future__ import annotations

from typing import Any, Dict, Optional

import aiohttp
import asyncio

from .communication_layer import CommunicationLayer
from .event_manager import EventManager
from .ethics_security import EthicsSecurityModule
from .memory_time_manager import MemoryTimeManager
from .logging_utils import get_json_logger

logger = get_json_logger(__name__)


class AutonomousEngine:
    """Evaluate system state and autonomously initiate actions."""

    def __init__(
        self,
        event_manager: EventManager,
        comm_layer: CommunicationLayer,
        memory_time: MemoryTimeManager,
        ethics: EthicsSecurityModule,
        endpoint: str = "https://example.com/api",
        interval: float = 60.0,
    ) -> None:
        self.event_manager = event_manager
        self.comm_layer = comm_layer
        self.memory_time = memory_time
        self.ethics = ethics
        self.endpoint = endpoint
        self.interval = interval
        self._task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()

    async def _run(self) -> None:
        """Internal scheduler loop."""
        async with self.comm_layer:
            while not self._shutdown_event.is_set():
                await self.evaluate_and_act()
                await asyncio.sleep(self.interval)

    async def start(self) -> None:
        """Begin the engine loop."""
        if self._task is None or self._task.done():
            self._shutdown_event.clear()
            self._task = asyncio.create_task(self._run())

    async def shutdown(self, timeout: float = 1.0) -> None:
        """Stop the engine loop and close resources.

        Parameters
        ----------
        timeout:
            Maximum number of seconds to wait for the running task to
            finish before it is cancelled.
        """
        if self._task is None:
            return
        self._shutdown_event.set()
        try:
            await asyncio.wait_for(self._task, timeout=timeout)
        except asyncio.TimeoutError:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None

    async def evaluate_and_act(self) -> None:
        """Example proactive behaviour based on recent events."""
        recent = self.memory_time.retrieve_recent_events("60m")
        logger.info("evaluating", extra={"recent_count": len(recent)})
        if not recent:
            return

        payload: Dict[str, Any] = {
            "action": "notify",
            "content": "Recent activity detected",
        }
        if not self.ethics.is_action_ethical(payload):
            logger.info("blocked_by_ethics", extra={"payload": payload})
            return
        try:
            await self.comm_layer.autonomous_interaction(
                self.endpoint,
                payload,
            )
            self.event_manager.emit_event("outgoing_message", payload)
        except (aiohttp.ClientError, RuntimeError) as exc:
            # Log communication issues instead of silently ignoring
            logger.error(
                "communication_error",
                extra={"error": str(exc)},
            )
            self.event_manager.emit_event("communication_error", {"error": str(exc)})

        await self.event_manager.dispatch()
        logger.info("dispatch_complete")


__all__ = ["AutonomousEngine"]
