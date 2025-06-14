import unittest

from src.event_manager import EventManager


class EventManagerTest(unittest.IsolatedAsyncioTestCase):
    async def test_event_dispatch(self):
        manager = EventManager()
        events = []

        def handler(data):
            events.append(data["value"])

        manager.register_listener("test", handler)
        manager.emit_event("test", {"value": 42})
        await manager.dispatch()
        self.assertEqual(events, [42])


if __name__ == "__main__":
    unittest.main()
