# -*- coding: utf-8 -*-
"""Event management subsystem for LAM.

This module implements a simple publish-subscribe event manager with an
internal asynchronous queue. It allows registration of listeners for
specific event types and dispatches events in a coroutine-friendly way.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .logging_utils import get_json_logger
from .lam_logging import log as lam_log

logger = get_json_logger(__name__)
_SENSITIVE_KEYS = {
    "authorization",
    "api_key",
    "token",
    "password",
    "secret",
    "access_token",
    "refresh_token",
}


def _sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for key, value in obj.items():
            if isinstance(key, str) and key.lower() in _SENSITIVE_KEYS:
                out[key] = "***"
            else:
                out[key] = _sanitize(value)
        return out
    if isinstance(obj, list):
        return [_sanitize(item) for item in obj]
    return obj

EventHandler = Callable[[Dict[str, Any]], Awaitable[None] | None]


class EventManager:
    """Manage events and listeners."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[EventHandler]] = defaultdict(list)
        self._queue: asyncio.Queue[Tuple[str, Dict[str, Any]]] = asyncio.Queue()

    def register_listener(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for a specific event type."""
        self._listeners[event_type].append(handler)
        logger.info(
            "listener_registered",
            extra={"event_type": event_type, "total": len(self._listeners[event_type])},
        )

    def emit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Place a new event into the processing queue."""
        logger.info(
            "event_emitted",
            extra={"event_type": event_type, "data": _sanitize(data)},
        )
        lam_log(
            "info",
            "evt.emit",
            "emit_event",
            event_type=event_type,
            queue_size=self._queue.qsize(),
        )
        self._queue.put_nowait((event_type, data))

    async def dispatch(self) -> None:
        """Process all events currently in the queue."""
        if self._queue.empty():
            logger.info("dispatch_done")
            return

        while True:
            event_type, data = await self._queue.get()
            try:
                logger.info("event_dispatch", extra={"event_type": event_type})
                lam_log(
                    "info",
                    "evt.dispatch",
                    "dispatch",
                    event_type=event_type,
                    listeners_count=len(self._listeners.get(event_type, [])),
                    queue_size=self._queue.qsize(),
                )
                for handler in self._listeners.get(event_type, []):
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(data)
                        else:
                            handler(data)
                    except Exception as exc:
                        logger.exception(
                            "handler_error",
                            extra={"event_type": event_type, "error": str(exc)},
                        )
                        lam_log(
                            "error",
                            "evt.handler_error",
                            "listener_failed",
                            event_type=event_type,
                            error=str(exc),
                        )
            finally:
                self._queue.task_done()
            if self._queue.empty():
                break
        logger.info("dispatch_done")


__all__ = ["EventManager", "EventHandler"]
