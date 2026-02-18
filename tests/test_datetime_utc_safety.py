from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.memory_core import MemoryCore
from src.memory_time_manager import MemoryTimeManager


def test_memory_time_manager_retrieve_recent_events_handles_aware_timestamps(
    tmp_path: Path,
) -> None:
    manager = MemoryTimeManager(memory=MemoryCore(tmp_path / "memory"))
    manager.add_event_memory({"name": "evt", "content": {"k": "v"}})
    recent = manager.retrieve_recent_events("60m")
    assert recent


def test_memory_core_time_ops_handle_naive_iso_timestamps(tmp_path: Path) -> None:
    memory = MemoryCore(tmp_path / "memory")
    memory.add_memory(
        {
            "name": "evt",
            "timestamp": datetime.now().isoformat(),
            "content": "payload",
            "importance": 0.5,
        }
    )

    memory.update_importance()
    memory.forget(max_age="1")
