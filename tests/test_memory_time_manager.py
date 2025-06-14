import unittest
import tempfile
from datetime import datetime

from pathlib import Path
import pytest

pytest.importorskip("opentelemetry")

from src import memory_core
from src.memory_time_manager import MemoryTimeManager

pytestmark = pytest.mark.optional


class MemoryTimeManagerTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        memory_core.MEMORY_PATH = Path(self.tmpdir.name)
        memory_core.LOG_DIR = memory_core.MEMORY_PATH / "logs"
        memory_core.METADATA_DIR = memory_core.MEMORY_PATH / "metadata"
        memory_core.DATA_DIR = memory_core.MEMORY_PATH / "data"
        memory_core.MEMORY_FILE = memory_core.DATA_DIR / "memory_items.json"
        memory_core.CATEGORY_FILE = memory_core.METADATA_DIR / "categories.json"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_retrieve(self):
        mgr = MemoryTimeManager()
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
