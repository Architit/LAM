# -*- coding: utf-8 -*-
"""Event management subsystem for LAM.

This module implements a simple publish-subscribe event manager with an
internal asynchronous queue. It allows registration of listeners for
specific event types and dispatches events in a coroutine-friendly way.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable, Coroutine, Dict, List, Tuple

EventHandler = Callable[[Dict[str, Any]], Awaitable[None] | None]


class EventManager:
    """Manage events and listeners."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[EventHandler]] = defaultdict(list)
        self._queue: asyncio.Queue[Tuple[str, Dict[str, Any]]] = asyncio.Queue()

    def register_listener(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for a specific event type."""
        self._listeners[event_type].append(handler)

    def emit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Place a new event into the processing queue."""
        self._queue.put_nowait((event_type, data))

    async def dispatch(self) -> None:
        """Process all events currently in the queue."""
        while not self._queue.empty():
            event_type, data = await self._queue.get()
            for handler in self._listeners.get(event_type, []):
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            self._queue.task_done()


__all__ = ["EventManager", "EventHandler"]
