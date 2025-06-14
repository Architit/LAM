# -*- coding: utf-8 -*-
"""Manage interactions with users and other agents."""

from __future__ import annotations

from typing import Any, Dict, List

from .communication_layer import CommunicationLayer
from .event_manager import EventManager


class InteractionManager:
    """High level interface for communications."""

    def __init__(self, comm_layer: CommunicationLayer, event_manager: EventManager) -> None:
        self.comm_layer = comm_layer
        self.event_manager = event_manager

    async def initiate_interaction(self, target: str, message: str) -> Dict[str, Any]:
        """Send a message asynchronously to a single ``target``."""
        payload = {"message": message}
        response = await self.comm_layer.send_request(target, payload)
        self.event_manager.emit_event(
            "new_interaction",
            {"target": target, "message": message, "response": response},
        )
        return response

    async def broadcast_message(self, targets: List[str], message: str) -> Dict[str, Any]:
        """Send the same message to multiple ``targets`` asynchronously."""
        results: Dict[str, Any] = {}
        for target in targets:
            results[target] = await self.initiate_interaction(target, message)
        return results


__all__ = ["InteractionManager"]
