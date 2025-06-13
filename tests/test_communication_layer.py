import unittest
from unittest.mock import patch

from src.communication_layer import CommunicationLayer


class CommunicationLayerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.layer = CommunicationLayer()

    async def asyncTearDown(self):
        await self.layer.close()

    async def test_send_request(self):
        class FakeResponse:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            async def text(self):
                return '{"ok": true}'

            async def json(self):
                return {"ok": True}

            def raise_for_status(self):
                pass

        with patch.object(self.layer._session, "post", return_value=FakeResponse()):
            response = await self.layer.send_request("http://test", {"a": 1})
            self.assertEqual(response, {"ok": True})
