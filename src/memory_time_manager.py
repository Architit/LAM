# -*- coding: utf-8 -*-
"""Integration layer for memory management and temporal reasoning."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .memory_core import MemoryCore
from .time_sense import TimeSense


class MemoryTimeManager:
    """Combine :class:`MemoryCore` with :class:`TimeSense`."""

    def __init__(
        self,
        memory: Optional[MemoryCore] = None,
        time_sense: Optional[TimeSense] = None,
    ) -> None:
        self.memory = memory or MemoryCore()
        self.time_sense = time_sense or TimeSense()

    def add_event_memory(self, event_data: Dict[str, Any]) -> None:
        """Store an event in memory."""
        timestamp = event_data.get("timestamp", datetime.utcnow().isoformat())
        entry = {
            "name": event_data.get("name", "event"),
            "timestamp": timestamp,
            "content": json.dumps(
                event_data.get("content", {}),
                ensure_ascii=False,
            ),
            "importance": float(event_data.get("importance", 0.5)),
            "associations": event_data.get("associations", []),
            "tags": event_data.get("tags", []),
            "attributes": event_data.get("attributes", {}),
        }
        self.memory.add_memory(entry)

    def retrieve_recent_events(self, interval: str) -> List[Dict[str, Any]]:
        """Return events within the last ``interval``.

        The ``interval`` string accepts formats like ``"60m"`` or ``"1d"`` for
        minutes or days respectively.
        """
        now = datetime.utcnow()
        if interval.endswith("m"):
            start = now - timedelta(minutes=int(interval[:-1]))
        elif interval.endswith("d"):
            start = now - timedelta(days=int(interval[:-1]))
        else:
            raise ValueError("Unsupported interval format")

        results: List[Dict[str, Any]] = []
        for mem in self.memory.get_memories():
            base = None
            try:
                parsed = self.time_sense.parse(mem.timestamp)
                base = parsed.base
            except ValueError:
                try:
                    base = datetime.fromisoformat(
                        mem.timestamp.replace("≈", "")
                    )
                except ValueError:
                    pass
            if base and base >= start:
                results.append(mem.to_dict())
        return results


__all__ = ["MemoryTimeManager"]
