import unittest
import tempfile
import os
from pathlib import Path

from src import memory_core
from src.memory_core import MemoryCore


class MemoryCoreTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        memory_core.MEMORY_PATH = Path(self.tmpdir.name)
        memory_core.LOG_DIR = memory_core.MEMORY_PATH / "logs"
        memory_core.METADATA_DIR = memory_core.MEMORY_PATH / "metadata"
        memory_core.DATA_DIR = memory_core.MEMORY_PATH / "data"
        memory_core.MEMORY_FILE = memory_core.DATA_DIR / "memory_items.json"
        memory_core.CATEGORY_FILE = memory_core.METADATA_DIR / "categories.json"
        self.core = MemoryCore()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_get(self):
        self.core.add_memory(
            {
                "name": "test",
                "timestamp": "2025-01-01T00:00:00",
                "content": "hello",
            }
        )
        memories = self.core.get_memories()
        self.assertEqual(len(memories), 1)
        retrieved = self.core.retrieve_memory({})
        self.assertEqual(len(retrieved), 1)

    def test_categories_persist(self):
        self.core.add_memory(
            {
                "name": "cat",
                "timestamp": "2025-01-01T00:00:00",
                "content": "hello world",
            }
        )
        categories_first = dict(self.core.categories)
        new_core = MemoryCore()
        self.assertEqual(new_core.categories, categories_first)

    def test_env_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["LAM_MEMORY_PATH"] = tmp
            memory_core._update_paths(memory_core.DEFAULT_MEMORY_PATH)
            core = MemoryCore()
            self.assertEqual(memory_core.MEMORY_PATH, Path(tmp))
            del os.environ["LAM_MEMORY_PATH"]
