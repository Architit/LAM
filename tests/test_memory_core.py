# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import unittest
import tempfile
import os
from pathlib import Path
import pytest

pytest.importorskip("opentelemetry")

from src import memory_core
from src.memory_core import MemoryCore

pytestmark = pytest.mark.optional


class MemoryCoreTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.core = MemoryCore(Path(self.tmpdir.name))

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
        new_core = MemoryCore(Path(self.tmpdir.name))
        self.assertEqual(new_core.categories, categories_first)

    def test_categories_file_recreated_on_init(self):
        self.core.add_memory(
            {
                "name": "regen",
                "timestamp": "2025-01-01T00:00:00",
                "content": "check",
            }
        )
        os.remove(self.core.category_file)
        self.assertFalse(self.core.category_file.exists())
        new_core = MemoryCore(Path(self.tmpdir.name))
        self.assertTrue(new_core.category_file.exists())
        self.assertTrue(new_core.categories)

    def test_env_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["LAM_MEMORY_PATH"] = tmp
            core = MemoryCore()
            self.assertEqual(core.base_path, Path(tmp))
            del os.environ["LAM_MEMORY_PATH"]

    def test_relative_env_path(self):
        with tempfile.TemporaryDirectory(dir=memory_core.REPO_ROOT) as tmp:
            relative = os.path.relpath(tmp, memory_core.REPO_ROOT)
            os.environ["LAM_MEMORY_PATH"] = relative
            core = MemoryCore()
            self.assertEqual(core.base_path, Path(tmp).resolve())
            del os.environ["LAM_MEMORY_PATH"]

    def test_nested_env_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = Path(tmp) / "nested" / "lam"
            os.environ["LAM_MEMORY_PATH"] = str(nested)
            core = MemoryCore()
            self.assertEqual(core.base_path, nested.resolve())
            self.assertTrue(core.memory_file.exists())
            self.assertTrue(core.category_file.exists())
            del os.environ["LAM_MEMORY_PATH"]

    def test_retrieve_by_embedding(self):
        self.core.add_memory(
            {
                "name": "emb1",
                "timestamp": "2025-01-01T00:00:00",
                "content": "A",
                "embedding": [1.0, 0.0, 0.0],
            }
        )
        self.core.add_memory(
            {
                "name": "emb2",
                "timestamp": "2025-01-01T00:00:00",
                "content": "B",
                "embedding": [0.0, 1.0, 0.0],
            }
        )
        results = self.core.retrieve_by_embedding([1.0, 0.0, 0.0])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "emb1")
