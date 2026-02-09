from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Literal, Optional


Status = Literal["ok", "error"]


@dataclass(slots=True)
class EnvelopeContext:
    trace_id: str
    task_id: str
    parent_task_id: Optional[str] = None
    span_id: Optional[str] = None


@dataclass(slots=True)
class ResultEnvelope:
    """
    Envelope Standard v1

    Required:
      - status: "ok" | "error"
      - context: {trace_id, task_id, parent_task_id?, span_id?}
      - result: JSON-serializable payload (can be None)
      - error: dict or None (must be non-None when status="error")
      - metrics: dict (can be empty but present)
    """
    status: Status
    context: EnvelopeContext
    result: Any = None
    error: Optional[Dict[str, Any]] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status == "error" and self.error is None:
            raise ValueError("ResultEnvelope: status='error' requires non-None error")
        if self.status == "ok" and self.error is not None:
            raise ValueError("ResultEnvelope: status='ok' requires error=None")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # asdict turns dataclasses into dicts recursively; good for JSON dumps.
        return d

    @staticmethod
    def ok(*, context: EnvelopeContext, result: Any = None, metrics: Optional[Dict[str, Any]] = None) -> "ResultEnvelope":
        return ResultEnvelope(status="ok", context=context, result=result, error=None, metrics=metrics or {})

    @staticmethod
    def err(*, context: EnvelopeContext, error: Dict[str, Any], metrics: Optional[Dict[str, Any]] = None) -> "ResultEnvelope":
        return ResultEnvelope(status="error", context=context, result=None, error=error, metrics=metrics or {})
