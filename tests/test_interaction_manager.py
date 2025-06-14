import unittest
from typing import Any, Dict

from src.interaction_manager import InteractionManager
from src.event_manager import EventManager


class FakeComm:
    async def send_request(
        self, service: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {"service": service, **payload}


class InteractionManagerTest(unittest.IsolatedAsyncioTestCase):
    async def test_initiate_and_broadcast(self):
        comm = FakeComm()
        events = []
        manager = InteractionManager(comm, EventManager())
        manager.event_manager.emit_event = lambda t, d: events.append((t, d))

        resp = await manager.initiate_interaction("a", "hello")
        self.assertEqual(resp, {"service": "a", "message": "hello"})
        self.assertEqual(events[0][0], "new_interaction")

        events.clear()
        result = await manager.broadcast_message(["a", "b"], "hi")
        self.assertEqual(
            result,
            {
                "a": {"service": "a", "message": "hi"},
                "b": {"service": "b", "message": "hi"},
            },
        )
        self.assertEqual(len(events), 2)


if __name__ == "__main__":
    unittest.main()
