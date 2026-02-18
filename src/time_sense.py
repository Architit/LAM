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
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass
class ParsedTime:
    """Internal representation of parsed time."""

    base: Optional[datetime]
    approx: bool = False
    tolerance: int = 0  # in minutes
    fuzzy: Optional[str] = None
    duration: Optional[timedelta] = None


class TimeSense:
    """Work with timestamps of varying precision."""

    EXACT_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{4})\s*:\s*(\d{2}):(\d{2})$")
    APPROX_RE = re.compile(r"^≈(\d{2})\.(\d{2})\.(\d{4})\s*:\s*≈?(\d{2})$")
    INTERVAL_RE = re.compile(
        r"^Δ\[(\d{2})\.(\d{2})\.(\d{4}):(\d{2}):(\d{2})±(\d+)мин\]$"
    )
    FUZZY_RE = re.compile(r"^≈([а-яА-Яa-zA-Z/_]+)$")
    DURATION_RE = re.compile(
        r"^P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$"
    )

    DEFAULT_APPROX_TOLERANCE = 60  # minutes

    def parse(self, timestamp: str) -> ParsedTime:
        """Parse a timestamp string into :class:`ParsedTime`."""
        timestamp = timestamp.strip()
        m = self.EXACT_RE.match(timestamp)
        if m:
            dt = datetime(
                int(m.group(3)),
                int(m.group(2)),
                int(m.group(1)),
                int(m.group(4)),
                int(m.group(5)),
            )
            return ParsedTime(base=dt)

        m = self.APPROX_RE.match(timestamp)
        if m:
            dt = datetime(
                int(m.group(3)),
                int(m.group(2)),
                int(m.group(1)),
                int(m.group(4)),
            )
            return ParsedTime(
                base=dt,
                approx=True,
                tolerance=self.DEFAULT_APPROX_TOLERANCE,
            )

        m = self.INTERVAL_RE.match(timestamp)
        if m:
            dt = datetime(
                int(m.group(3)),
                int(m.group(2)),
                int(m.group(1)),
                int(m.group(4)),
                int(m.group(5)),
            )
            return ParsedTime(
                base=dt,
                tolerance=int(m.group(6)),
            )

        m = self.FUZZY_RE.match(timestamp)
        if m:
            return ParsedTime(base=None, fuzzy=m.group(1))

        m = self.DURATION_RE.match(timestamp)
        if m:
            delta = timedelta(
                days=int(m.group("days") or 0),
                hours=int(m.group("hours") or 0),
                minutes=int(m.group("minutes") or 0),
                seconds=int(m.group("seconds") or 0),
            )
            return ParsedTime(base=None, duration=delta)

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

    def interval_between(
        self, time_a: ParsedTime | str, time_b: ParsedTime | str
    ) -> int:
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
            exact_base = self.parse(exact_time).base
            if exact_base is None:
                raise ValueError("Exact time required for fuzzy generation")
            exact_time = exact_base

        hour = exact_time.hour
        if 0 <= hour < 6:
            return "≈ночь"
        if 6 <= hour < 12:
            return "≈утро"
        if 12 <= hour < 18:
            return "≈день"
        return "≈вечер"

    def humanize(
        self, value: datetime | timedelta, reference: datetime | None = None
    ) -> str:
        """Return human-friendly phrase for a time delta."""
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            else:
                value = value.astimezone(timezone.utc)
            reference = reference or datetime.now(timezone.utc)
            if reference.tzinfo is None:
                reference = reference.replace(tzinfo=timezone.utc)
            else:
                reference = reference.astimezone(timezone.utc)
            delta = value - reference
        else:
            delta = value

        seconds = int(delta.total_seconds())
        past = seconds < 0
        seconds = abs(seconds)

        if seconds < 60:
            num = seconds
            unit = "second"
        elif seconds < 3600:
            num = seconds // 60
            unit = "minute"
        elif seconds < 86400:
            num = seconds // 3600
            unit = "hour"
        else:
            num = seconds // 86400
            unit = "day"

        if num != 1:
            unit += "s"

        phrase = f"{num} {unit}"
        if past:
            return f"{phrase} ago"
        return f"in {phrase}"


__all__ = ["TimeSense", "ParsedTime"]
