# -*- coding: utf-8 -*-
"""Proactive autonomous engine for LAM."""

from __future__ import annotations

from typing import Any, Dict, Set

import aiohttp
import asyncio
import signal

from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
    ) -> None:
        self.event_manager = event_manager
        self.comm_layer = comm_layer
        self.memory_time = memory_time
        self.ethics = ethics
        self.endpoint = endpoint
        self._shutdown_event = asyncio.Event()
        self._tasks: Set[asyncio.Task] = set()
        self.scheduler: AsyncIOScheduler | None = None

    def _setup_signal_handlers(self) -> None:
        """Register handlers for clean shutdown."""
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._shutdown_event.set)
            except NotImplementedError:
                # Windows may not support some signals
                signal.signal(sig, lambda _s, _f: self._shutdown_event.set())

    async def _schedule_evaluate(self) -> None:
        task = asyncio.create_task(self.evaluate_and_act())
        self._tasks.add(task)
        try:
            await task
        finally:
            self._tasks.discard(task)

    async def start(self, interval: int = 60) -> None:
        """Begin periodic evaluation loop until shutdown."""
        self._setup_signal_handlers()
        self.scheduler = AsyncIOScheduler(event_loop=asyncio.get_running_loop())
        async with self.comm_layer:
            self.scheduler.add_job(
                self._schedule_evaluate,
                "interval",
                seconds=interval,
            )
            self.scheduler.start()
            await self._shutdown_event.wait()
            await self.shutdown()

    async def shutdown(self) -> None:
        """Cancel running tasks and stop scheduler."""
        self._shutdown_event.set()
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        for task in list(self._tasks):
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)

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
