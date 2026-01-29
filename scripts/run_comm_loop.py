from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]  # .../LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


class Sink:
    """Mailbox sink for recipients like 'comm-agent' used as reply_to target."""

    def answer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # do nothing, just accept payload
        return {"status": "ok", "result": None, "error": None, "metrics": {}, "context": payload.get("context")}


def _ensure_recipient(comm: ComAgent, name: str) -> None:
    """Make sure 'name' is registered so comm.send_data(name, ...) never fails."""
    if not name:
        return
    if name not in comm.list_agents():
        comm.register_agent(name, Sink())


def main() -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()

    comm.register_agent("roaudter", roaudter)
    _ensure_recipient(comm, "comm-agent")  # default reply target

    print("COMM LOOP STARTED (Ctrl+C to stop)")

    # seed message
    comm.send_data("roaudter", {"msg": "ping", "intent": "chat", "reply_to": "comm-agent"})

    while True:
        recipient, payload = comm.receive_data()
        if not recipient:
            time.sleep(0.05)
            continue

        print("RECEIVED:", recipient, payload)

        if recipient == "roaudter":
            out = roaudter.answer(payload)

            reply_to = payload.get("reply_to") or "comm-agent"
            _ensure_recipient(comm, str(reply_to))

            ok = comm.send_data(str(reply_to), out)
            if ok:
                print("SENT BACK TO:", reply_to)
            else:
                print("SEND FAILED TO:", reply_to)

            print("REPLY:", out)

        time.sleep(0.01)


if __name__ == "__main__":
    main()
