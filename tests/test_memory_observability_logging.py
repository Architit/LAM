# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import json
from pathlib import Path

from src.memory_core import MemoryCore


def test_memory_emits_write_read_search_logs_jsonl(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("LAM_LOG_LEVEL", "info")
    monkeypatch.setenv("LAM_LOG_EVENTS", "mem.write,mem.read,mem.search")
    monkeypatch.setenv("LAM_MEMORY_PATH", str(tmp_path / "memstore"))

    mem = MemoryCore()

    mem.add_memory(
        {
            "name": "n1",
            "timestamp": "2026-01-01T00:00:00",
            "content": "hello world memory log test",
        }
    )

    _ = mem.retrieve_memory({"tags": ["hello"]})
    _ = mem.retrieve_by_embedding([0.1, 0.2, 0.3], k=1)

    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert len(lines) >= 3

    events = []
    for ln in lines:
        try:
            events.append(json.loads(ln))
        except Exception as e:
            raise AssertionError(f"Non-JSON log line: {ln!r}") from e

    names = [e.get("event") for e in events]
    assert "mem.write" in names
    assert "mem.read" in names
    assert "mem.search" in names

    w = next(e for e in events if e.get("event") == "mem.write")
    assert w.get("level") == "info"
    assert isinstance(w.get("memory_id"), str) and w["memory_id"]

    r = next(e for e in events if e.get("event") == "mem.read")
    assert r.get("level") == "info"
    assert r.get("results_count") is not None

    s = next(e for e in events if e.get("event") == "mem.search")
    assert s.get("level") == "info"
    assert s.get("k") == 1
    assert s.get("results_count") is not None
