import unittest
import tempfile
import os
import importlib

import src.memory_core as memory_core


class MemoryCoreTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        os.environ["LAM_MEMORY_PATH"] = self.tmpdir.name
        importlib.reload(memory_core)
        self.core = memory_core.MemoryCore()

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("LAM_MEMORY_PATH", None)
        importlib.reload(memory_core)

    def test_add_and_get(self):
        self.core.add_memory({"name": "test", "timestamp": "2025-01-01T00:00:00", "content": "hello"})
        memories = self.core.get_memories()
        self.assertEqual(len(memories), 1)
        retrieved = self.core.retrieve_memory({})
        self.assertEqual(len(retrieved), 1)
