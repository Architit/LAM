# ruff: noqa: E402
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # …/LAM
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
sys.path.extend([str(COMM_SRC)])

from interfaces.com_agent_interface import ComAgent  # type: ignore
from roaudter_agent import RoaudterComAgent


def main() -> None:
    comm = ComAgent()
    roaudter = RoaudterComAgent()
    comm.register_agent("roaudter", roaudter)

    print("COMM LOOP STARTED. Send ping -> roaudter")

    # demo message (reply_to можно менять на "codex" / "comm-agent" / etc)
    comm.send_data("roaudter", {"msg": "ping", "intent": "chat", "reply_to": "comm-agent"})

    recipient, payload = comm.receive_data()
    print("RECEIVED:", recipient, payload)

    if recipient == "roaudter":
        out = roaudter.answer(payload)

        reply_to = payload.get("reply_to") or "comm-agent"
        comm.send_data(reply_to, out)

        print("SENT BACK TO:", reply_to)
        print("REPLY:", out)


if __name__ == "__main__":
    main()
