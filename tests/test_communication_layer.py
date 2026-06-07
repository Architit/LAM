# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
from unittest.mock import patch

import pytest

pytest.importorskip("opentelemetry")

from src.communication_layer import CommunicationLayer

pytestmark = pytest.mark.optional


@pytest.mark.asyncio
async def test_send_request():
    async with CommunicationLayer() as layer:
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

        with patch.object(
            layer._session,
            "post",
            return_value=FakeResponse(),
        ):
            response = await layer.send_request("http://test", {"a": 1})
            assert response == {"ok": True}


@pytest.mark.asyncio
async def test_session_closed_on_exception():
    layer = CommunicationLayer()
    with pytest.raises(RuntimeError, match="boom"):
        async with layer:
            raise RuntimeError("boom")
    assert layer._session is None
