# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ruff: noqa: E402
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
COMM_SRC = ROOT / "LAM/default/agents/comm-agent/src"
CODEX_SRC = ROOT / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

from interfaces import com_agent_interface as _com_mod
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

from interfaces.com_agent_interface import ComAgent  # type: ignore
from codex_agent.core import Core
from roaudter_agent import RoaudterComAgent

from src.taskarid_agent import TaskaridAgent


def test_taskarid_to_comm_to_codex_to_comm_to_roaudter_envelope_and_trace() -> None:
    # 1) taskarid creates shared trace/context
    taskarid = TaskaridAgent()
    plan_out = taskarid.answer({"goal": "ping", "intent": "chat", "provider_hint": "ollama"})
    assert plan_out["status"] == "ok"

    trace_id = plan_out["context"]["trace_id"]
    root_task_id = plan_out["context"]["task_id"]

    # 2) comm routes to codex (dict payload → Envelope v1)
    comm = ComAgent()
    codex = Core()
    roaudter = RoaudterComAgent()

    comm.register_agent("codex", codex)
    comm.register_agent("roaudter", roaudter)

    codex_ctx = {
        "trace_id": trace_id,
        "task_id": f"{root_task_id}.codex",
        "parent_task_id": root_task_id,
    }
    codex_taskarid = f"{trace_id}:{codex_ctx['task_id']}"

    codex_payload = {
        "msg": "ping",
        "intent": "chat",
        "context": codex_ctx,
        "taskarid": codex_taskarid,
    }

    comm.send_data("codex", codex_payload)
    _, codex_in = comm.receive_data()

    codex_out = codex.answer(codex_in)

    assert codex_out["status"] == "ok"
    assert codex_out["context"]["trace_id"] == trace_id
    assert codex_out["context"]["task_id"] == codex_ctx["task_id"]
    assert codex_out["error"] is None
    assert isinstance(codex_out["metrics"], dict)
    assert codex_out["result"]["reply"] == "pong"

    # 3) comm routes codex result to roaudter, preserving trace/taskarid
    roaudter_payload = {
        "msg": codex_out["result"]["reply"],
        "intent": "chat",
        "context": codex_ctx,
        "taskarid": codex_taskarid,
    }

    comm.send_data("roaudter", roaudter_payload)
    _, roaudter_in = comm.receive_data()

    roaudter_out = roaudter.answer(roaudter_in)

    assert roaudter_out["status"] == "ok"
    assert roaudter_out["context"]["trace_id"] == trace_id
    assert roaudter_out["context"]["task_id"] == codex_ctx["task_id"]
    assert "taskarid" in roaudter_out
