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

    async def test_event_emitted_during_dispatch(self):
        manager = EventManager()
        events = []

        async def handler(data):
            events.append(data["value"])
            if data["value"] == 1:
                manager.emit_event("test", {"value": 2})

        manager.register_listener("test", handler)
        manager.emit_event("test", {"value": 1})
        await manager.dispatch()
        self.assertEqual(events, [1, 2])


if __name__ == "__main__":
    unittest.main()
