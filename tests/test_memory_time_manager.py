import unittest
from datetime import datetime
import os
import tempfile
import importlib

import src.memory_core as memory_core
import src.memory_time_manager as memory_time_manager


class MemoryTimeManagerTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        os.environ["LAM_MEMORY_PATH"] = self.tmpdir.name
        importlib.reload(memory_core)
        importlib.reload(memory_time_manager)
        self.mgr = memory_time_manager.MemoryTimeManager()

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("LAM_MEMORY_PATH", None)
        importlib.reload(memory_core)
        importlib.reload(memory_time_manager)

    def test_add_and_retrieve(self):
        self.mgr.add_event_memory({"name": "test", "timestamp": datetime.utcnow().isoformat(), "content": "data"})
        recent = self.mgr.retrieve_recent_events("1d")
        self.assertTrue(len(recent) >= 1)


if __name__ == "__main__":
    unittest.main()
