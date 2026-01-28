# ruff: noqa: E402
from __future__ import annotations
from pathlib import Path
import sys
import time

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

    # demo message
    comm.send_data("roaudter", {"msg": "ping", "intent": "chat"})

    # simple loop: 1 iteration demo
    recipient, payload = comm.receive_data()
    print("RECEIVED:", recipient, payload)

    if recipient == "roaudter":
        out = roaudter.answer(payload)
        comm.send_data("comm-agent", out)  # обратно "в comm-agent" как получателю
        print("SENT BACK:", out)


if __name__ == "__main__":
    main()
