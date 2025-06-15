import os
import unittest
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock

from src.tma import cli
from src.tma.storage import Metrics


class CLITest(unittest.TestCase):
    def test_main_trigger_invokes_schedule(self):
        with patch.object(cli, 'schedule') as schedule:
            cli.main(['trigger', '--matrix', 'a', 'b'])
            schedule.assert_called_once_with(['a', 'b'])

    def test_main_status_prints_metrics(self):
        metrics = Metrics(5, 1, 0)
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['TMA_REPORTS_DIR'] = tmpdir
            store = MagicMock()
            store.load.return_value = metrics
            with patch.object(cli, 'MetricsStore', return_value=store) as ms:
                with patch('builtins.print') as mock_print:
                    cli.main(['status'])
                    ms.assert_called_once_with(Path(tmpdir) / 'metrics.yaml')
                    mock_print.assert_called_once_with(metrics)
            os.environ.pop('TMA_REPORTS_DIR')
