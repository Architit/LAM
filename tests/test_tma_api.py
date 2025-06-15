import os
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

os.environ['TMA_CONFIG'] = str(Path(__file__).resolve().parents[1] / 'tma.yaml')
from src.tma.api import create_app
from src.tma.storage import Metrics


@pytest.mark.asyncio
async def test_trigger_endpoint(http_client):
    with patch('src.tma.api.schedule') as schedule:
        app = create_app()
        session, base = await http_client(app)
        async with session.post(f"{base}/trigger", json={'matrix': ['a']}) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data['status'] == 'scheduled'
        schedule.assert_called_once_with(['a'])


@pytest.mark.asyncio
async def test_metrics_endpoint(http_client):
    metrics = Metrics(3, 0, 1)
    store = patch('src.tma.api.MetricsStore', autospec=True)
    with store as store_mock:
        store_instance = store_mock.return_value
        store_instance.load.return_value = metrics
        app = create_app()
        session, base = await http_client(app)
        async with session.get(f"{base}/metrics") as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data == metrics.__dict__
