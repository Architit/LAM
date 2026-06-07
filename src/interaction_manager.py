# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# -*- coding: utf-8 -*-
"""Manage interactions with users and other agents."""

from __future__ import annotations

from typing import Any, Dict, List
import asyncio

from .communication_layer import CommunicationLayer
from .event_manager import EventManager


class InteractionManager:
    """High level interface for communications."""

    def __init__(
        self, comm_layer: CommunicationLayer, event_manager: EventManager
    ) -> None:
        self.comm_layer = comm_layer
        self.event_manager = event_manager

    async def initiate_interaction(
        self, target: str, message: str
    ) -> Dict[str, Any]:
        """Send a message asynchronously to a single ``target``."""
        payload = {"message": message}
        response = await self.comm_layer.send_request(target, payload)
        self.event_manager.emit_event(
            "new_interaction",
            {"target": target, "message": message, "response": response},
        )
        return response

    async def broadcast_message(
        self, targets: List[str], message: str
    ) -> Dict[str, Any]:
        """Send the same message to multiple ``targets`` asynchronously."""
        tasks = {
            target: asyncio.create_task(self.initiate_interaction(target, message))
            for target in targets
        }
        return {t: await task for t, task in tasks.items()}


__all__ = ["InteractionManager"]
