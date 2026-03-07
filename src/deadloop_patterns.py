from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(slots=True)
class PatternHit:
    pattern_id: str
    severity: str
    line_no: int
    line: str


PATTERN_LIBRARY: list[tuple[str, str, re.Pattern[str]]] = [
    (
        "governance_only_progress",
        "high",
        re.compile(r"governance-only|contract-only|no runtime impact", re.IGNORECASE),
    ),
    (
        "hold_bypass_attempt",
        "critical",
        re.compile(r"S27.*(OPEN|resume).*(without|bypass)", re.IGNORECASE),
    ),
    (
        "synthetic_numbering_progress",
        "high",
        re.compile(r"numbering.*progress|synthetic progress", re.IGNORECASE),
    ),
    (
        "repeated_gate_opening",
        "medium",
        re.compile(r"OPEN_.*GATE", re.IGNORECASE),
    ),
    (
        "missing_delivery_delta",
        "critical",
        re.compile(r"code/test delta.*NONE|no non-doc code change", re.IGNORECASE),
    ),
    (
        "deadloop_hold_state",
        "high",
        re.compile(r"HOLD_BY_DEADLOOP_BREAK_PROTOCOL", re.IGNORECASE),
    ),
]


def scan_text_for_patterns(lines: Iterable[str]) -> list[PatternHit]:
    hits: list[PatternHit] = []
    for idx, line in enumerate(lines, start=1):
        for pattern_id, severity, pattern in PATTERN_LIBRARY:
            if pattern.search(line):
                # Avoid false criticals on protective records like
                # "HOLD without operator confirmation".
                if pattern_id == "hold_bypass_attempt" and "HOLD" in line.upper():
                    continue
                # Ignore policy-definition examples where HOLD marker is shown
                # as a code literal in backticks; keep detection for real state lines.
                if pattern_id == "deadloop_hold_state" and re.search(r"`\s*HOLD_BY_DEADLOOP_BREAK_PROTOCOL\s*`", line, re.IGNORECASE):
                    continue
                hits.append(
                    PatternHit(
                        pattern_id=pattern_id,
                        severity=severity,
                        line_no=idx,
                        line=line.rstrip("\n"),
                    )
                )
    return hits
