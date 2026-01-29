from __future__ import annotations
from dataclasses import dataclass
try:
    from src.lam_logging import set_context  # type: ignore
except Exception:
    set_context = None  # type: ignore

from typing import Any, Dict, List
import uuid


def _ensure_context(payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx = payload.get("context")
    if not isinstance(ctx, dict):
        ctx = {}

    if not ctx.get("trace_id"):
        ctx["trace_id"] = uuid.uuid4().hex

    if not ctx.get("task_id"):
        ctx["task_id"] = payload.get("task_id") or f"t_{uuid.uuid4().hex[:12]}"

    payload["context"] = ctx
    payload.setdefault("taskarid", f"{ctx['trace_id']}:{ctx['task_id']}")
    return payload


@dataclass(slots=True)
class TaskaridAgent:
    """
    Mission control (v0):
    - takes a mission/goal
    - returns a simple plan (list of tasks) sharing trace_id
    """
    name: str = "taskarid"

    def answer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload = _ensure_context(payload)
        ctx = payload["context"]
        if set_context:
            set_context(**ctx)

        goal = payload.get("goal") or payload.get("mission") or payload.get("msg") or ""

        plan: List[Dict[str, Any]] = [
            {
                "agent": "roaudter",
                "intent": payload.get("intent", "chat"),
                "msg": str(goal),
                "provider_hint": payload.get("provider_hint"),
                "context": {"trace_id": ctx["trace_id"], "task_id": f"{ctx['task_id']}.1", "parent_task_id": ctx["task_id"]},
                "taskarid": f"{ctx['trace_id']}:{ctx['task_id']}.1",
            }
        ]

        return {
            "status": "ok",
            "context": ctx,
            "taskarid": payload["taskarid"],
            "goal": str(goal),
            "plan": plan,
        }
