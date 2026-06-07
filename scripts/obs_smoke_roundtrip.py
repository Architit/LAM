# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent
from src.taskarid_agent import TaskaridAgent


class Sink:
    """Mailbox sink for reply targets (e.g. 'comm-agent')."""

    def answer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "ok",
            "result": None,
            "error": None,
            "metrics": {},
            "context": payload.get("context") or {},
        }


def _ensure_agent(comm: ComAgent, name: str, obj: Any) -> None:
    if name not in comm.list_agents():
        comm.register_agent(name, obj)


def _pop(comm: ComAgent) -> Tuple[str, Dict[str, Any]]:
    recipient, payload = comm.receive_data()
    if not recipient:
        raise SystemExit("queue empty unexpectedly")
    if not isinstance(payload, dict):
        raise SystemExit(f"payload not dict: {type(payload)}")
    return recipient, payload


def main() -> None:
    # минимальный шум: включаем только нужные события
    os.environ.setdefault(
        "LAM_LOG_EVENTS",
        "comm.enqueue,comm.dequeue,roaudter.route,roaudter.result,roaudter.deliver",
    )
    os.environ.setdefault("LAM_LOG_LEVEL", "info")

    comm = ComAgent()
    _ensure_agent(comm, "roaudter", RoaudterComAgent())
    _ensure_agent(comm, "comm-agent", Sink())

    # 1) Taskarid формирует план с trace_id/task_id
    taskarid = TaskaridAgent()
    plan_out = taskarid.answer({"goal": "Say only: pong", "intent": "chat"})
    plan = plan_out.get("plan") or []
    if not plan:
        raise SystemExit("taskarid returned empty plan")
    task = plan[0]
    if not isinstance(task, dict):
        raise SystemExit("taskarid plan[0] not dict")

    # 2) кладём в очередь задачу для roaudter
    ok = comm.send_data("roaudter", task)
    if not ok:
        raise SystemExit("send_data to roaudter failed")

    # 3) имитируем comm-loop ровно 1 итерацию: достали -> вызвали -> отправили reply
    recipient1, payload1 = _pop(comm)
    if recipient1 != "roaudter":
        raise SystemExit(f"expected recipient roaudter, got {recipient1}")

    roaudter: RoaudterComAgent = comm._registry["roaudter"]  # type: ignore[attr-defined]
    out = roaudter.answer(payload1)

    reply_to = payload1.get("reply_to") or "comm-agent"
    _ensure_agent(comm, str(reply_to), Sink())
    ok = comm.send_data(str(reply_to), out)
    if not ok:
        raise SystemExit(f"send_data to reply_to failed: {reply_to}")

    # 4) забираем reply из очереди (с enforce envelope, если reply-like)
    recipient2, payload2 = _pop(comm)

    print("ROUNDTRIP_OK")
    print("RECIPIENT:", recipient2)
    print("STATUS:", payload2.get("status"))
    print("CONTEXT:", json.dumps(payload2.get("context") or {}, ensure_ascii=False))


if __name__ == "__main__":
    main()
