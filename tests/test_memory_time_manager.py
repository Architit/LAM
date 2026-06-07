# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import unittest
import tempfile
from datetime import datetime

from pathlib import Path
import pytest

pytest.importorskip("opentelemetry")

from src.memory_core import MemoryCore
from src.memory_time_manager import MemoryTimeManager

pytestmark = pytest.mark.optional


class MemoryTimeManagerTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.manager = MemoryTimeManager(memory=MemoryCore(Path(self.tmpdir.name)))

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_retrieve(self):
        mgr = self.manager
        mgr.add_event_memory(
            {
                "name": "test",
                "timestamp": datetime.utcnow().isoformat(),
                "content": "data",
            }
        )
        recent = mgr.retrieve_recent_events("1d")
        self.assertTrue(len(recent) >= 1)


if __name__ == "__main__":
    unittest.main()
