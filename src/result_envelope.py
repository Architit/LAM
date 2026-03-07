from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Literal, Optional, Tuple


# DIRECTIVE-GMN-20260303-01 Compliance:
# New Status Registry
Status = Literal["SUCCESS", "HOLD", "ERROR", "PENDING"]


@dataclass(slots=True)
class EnvelopeContext:
    trace_id: str
    task_id: str
    parent_task_id: Optional[str] = None
    span_id: Optional[str] = None


@dataclass(slots=True)
class ResultEnvelope:
    """
    ResultEnvelope Standard v2 (Compliance: DIRECTIVE-GMN-20260303-01)
    Goal: Eradicate 'Blind Echo' via evidence-backed results.

    Required fields:
      - timestamp_utc: ISO 8601 (Creation time)
      - status: "SUCCESS" | "HOLD" | "ERROR" | "PENDING"
      - message: Human-readable fruit of the deed
      - data: Result payload (can be None)
      - evidence: Tuple of evidence (hashes, links, instruction refs, test outputs)
      - context: {trace_id, task_id, parent_task_id?, span_id?} (Legacy compatibility)
    """
    status: Status
    message: str
    data: Any = None
    evidence: Tuple[str, ...] = field(default_factory=tuple)
    timestamp_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    context: Optional[EnvelopeContext] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def success(cls, *, message: str, data: Any = None, evidence: Tuple[str, ...] = (), context: Optional[EnvelopeContext] = None) -> "ResultEnvelope":
        return cls(status="SUCCESS", message=message, data=data, evidence=evidence, context=context)

    @classmethod
    def hold(cls, *, message: str, data: Any = None, evidence: Tuple[str, ...] = (), context: Optional[EnvelopeContext] = None) -> "ResultEnvelope":
        return cls(status="HOLD", message=message, data=data, evidence=evidence, context=context)

    @classmethod
    def error(cls, *, message: str, data: Any = None, evidence: Tuple[str, ...] = (), context: Optional[EnvelopeContext] = None) -> "ResultEnvelope":
        return cls(status="ERROR", message=message, data=data, evidence=evidence, context=context)

    @classmethod
    def pending(cls, *, message: str, data: Any = None, evidence: Tuple[str, ...] = (), context: Optional[EnvelopeContext] = None) -> "ResultEnvelope":
        return cls(status="PENDING", message=message, data=data, evidence=evidence, context=context)
