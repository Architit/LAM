import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

os.environ['TMA_CONFIG'] = str(Path(__file__).resolve().parents[1] / 'tma.yaml')
from src.tma import cli
from src.tma.storage import Metrics


class CLITest(unittest.TestCase):
    def test_main_trigger_invokes_schedule(self):
        with patch.object(cli, 'schedule') as schedule:
            cli.main(['trigger', '--matrix', 'a', 'b'])
            schedule.assert_called_once_with(['a', 'b'])

    def test_main_status_prints_metrics(self):
        metrics = Metrics(5, 1, 0)
        store = MagicMock()
        store.load.return_value = metrics
        with patch.object(cli, 'MetricsStore', return_value=store):
            with patch('builtins.print') as mock_print:
                cli.main(['status'])
                mock_print.assert_called_once_with(metrics)
