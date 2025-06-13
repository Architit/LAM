# -*- coding: utf-8 -*-
"""Utility class for parsing and comparing fuzzy timestamps.

This module defines :class:`TimeSense` which supports several timestamp
representations used by the memory subsystem. It allows parsing timestamps
with various precision levels, comparing them and generating fuzzy
representations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ParsedTime:
    """Internal representation of parsed time."""

    base: Optional[datetime]
    approx: bool = False
    tolerance: int = 0  # in minutes
    fuzzy: Optional[str] = None


class TimeSense:
    """Work with timestamps of varying precision."""

    EXACT_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{4})\s*:\s*(\d{2}):(\d{2})$")
    APPROX_RE = re.compile(r"^≈(\d{2})\.(\d{2})\.(\d{4})\s*:\s*≈?(\d{2})$")
    INTERVAL_RE = re.compile(
        r"^Δ\[(\d{2})\.(\d{2})\.(\d{4}):(\d{2}):(\d{2})±(\d+)мин\]$"
    )
    FUZZY_RE = re.compile(r"^≈([а-яА-Яa-zA-Z/_]+)$")

    DEFAULT_APPROX_TOLERANCE = 60  # minutes

    def parse(self, timestamp: str) -> ParsedTime:
        """Parse a timestamp string into :class:`ParsedTime`."""
        timestamp = timestamp.strip()
        m = self.EXACT_RE.match(timestamp)
        if m:
            dt = datetime(
                int(m.group(3)), int(m.group(2)), int(m.group(1)), int(m.group(4)), int(m.group(5))
            )
            return ParsedTime(base=dt)

        m = self.APPROX_RE.match(timestamp)
        if m:
            dt = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), int(m.group(4)))
            return ParsedTime(base=dt, approx=True, tolerance=self.DEFAULT_APPROX_TOLERANCE)

        m = self.INTERVAL_RE.match(timestamp)
        if m:
            dt = datetime(
                int(m.group(3)), int(m.group(2)), int(m.group(1)), int(m.group(4)), int(m.group(5))
            )
            return ParsedTime(base=dt, tolerance=int(m.group(6)))

        m = self.FUZZY_RE.match(timestamp)
        if m:
            return ParsedTime(base=None, fuzzy=m.group(1))

        raise ValueError(f"Unrecognized timestamp format: {timestamp}")

    def compare(self, time_a: ParsedTime | str, time_b: ParsedTime | str) -> int:
        """Compare two times considering tolerance."""
        if isinstance(time_a, str):
            time_a = self.parse(time_a)
        if isinstance(time_b, str):
            time_b = self.parse(time_b)

        if time_a.base is None or time_b.base is None:
            return 0

        tolerance = max(time_a.tolerance, time_b.tolerance)
        if time_a.approx or time_b.approx:
            tolerance = max(tolerance, self.DEFAULT_APPROX_TOLERANCE)

        diff = (time_a.base - time_b.base).total_seconds() / 60
        if abs(diff) <= tolerance:
            return 0
        return -1 if diff < 0 else 1

    def interval_between(self, time_a: ParsedTime | str, time_b: ParsedTime | str) -> int:
        """Return interval in minutes between two times."""
        if isinstance(time_a, str):
            time_a = self.parse(time_a)
        if isinstance(time_b, str):
            time_b = self.parse(time_b)

        if time_a.base is None or time_b.base is None:
            raise ValueError("Cannot compute interval for fuzzy time")

        diff = time_b.base - time_a.base
        return int(diff.total_seconds() / 60)

    def generate_fuzzy(self, exact_time: datetime | str) -> str:
        """Generate fuzzy time description from exact time."""
        if isinstance(exact_time, str):
            exact_time = self.parse(exact_time).base  # type: ignore[assignment]
        if exact_time is None:
            raise ValueError("Exact time required for fuzzy generation")

        hour = exact_time.hour
        if 0 <= hour < 6:
            return "≈ночь"
        if 6 <= hour < 12:
            return "≈утро"
        if 12 <= hour < 18:
            return "≈день"
        return "≈вечер"


__all__ = ["TimeSense", "ParsedTime"]
