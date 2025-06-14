# -*- coding: utf-8 -*-
"""Proactive autonomous engine for LAM."""

from __future__ import annotations

from typing import Any, Dict

from .communication_layer import CommunicationLayer
from .event_manager import EventManager
from .ethics_security import EthicsSecurityModule
from .memory_time_manager import MemoryTimeManager


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

    async def evaluate_and_act(self) -> None:
        """Example proactive behaviour based on recent events."""
        recent = self.memory_time.retrieve_recent_events("60m")
        if not recent:
            return

        payload: Dict[str, Any] = {
            "action": "notify",
            "content": "Recent activity detected",
        }
        if not self.ethics.is_action_ethical(payload):
            return
        try:
            await self.comm_layer.autonomous_interaction(
                self.endpoint,
                payload,
            )
            self.event_manager.emit_event("outgoing_message", payload)
        except Exception:
            # Communication errors are ignored for this demo
            pass

        await self.event_manager.dispatch()


__all__ = ["AutonomousEngine"]
