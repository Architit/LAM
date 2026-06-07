# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
ROAUDTER_SRC = ROOT / "LAM/default/agents/roaudter-agent/src"
sys.path.extend([str(COMM_SRC), str(ROAUDTER_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


class Sink:
    """Mailbox sink for reply targets (e.g. 'comm-agent')."""

    def answer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "ok", "result": None, "error": None, "metrics": {}, "context": payload.get("context") or {}}


def _ensure_recipient(comm: ComAgent, name: str) -> None:
    if name and name not in comm.list_agents():
        comm.register_agent(name, Sink())


def main() -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()

    comm.register_agent("roaudter", roaudter)
    _ensure_recipient(comm, "comm-agent")

    ok = comm.send_data("roaudter", {"msg": "ping", "intent": "chat", "reply_to": "comm-agent"})
    if not ok:
        raise SystemExit("send_data to roaudter failed")

    # receive 1st message (roaudter task)
    recipient, payload = comm.receive_data()
    if recipient != "roaudter":
        raise SystemExit(f"unexpected recipient: {recipient}")

    out = roaudter.answer(payload)

    reply_to = payload.get("reply_to") or "comm-agent"
    _ensure_recipient(comm, str(reply_to))

    ok2 = comm.send_data(str(reply_to), out)
    if not ok2:
        raise SystemExit(f"send_data to reply_to failed: {reply_to}")

    # receive reply back from queue
    recipient2, payload2 = comm.receive_data()
    print("ROAUDTER_REPLY_RECIPIENT:", recipient2)
    print("ROAUDTER_REPLY:", payload2)

    # if queue still has leftovers, show once (no infinite loop)
    recipient3, payload3 = comm.receive_data()
    if recipient3:
        print("EXTRA:", recipient3, payload3)
    else:
        time.sleep(0.01)


if __name__ == "__main__":
    main()
