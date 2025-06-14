import unittest
from datetime import datetime

from src.memory_time_manager import MemoryTimeManager


class MemoryTimeManagerTest(unittest.TestCase):
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
