import os
import unittest
from pathlib import Path
from unittest.mock import patch

from src.tma import scheduler


class SchedulerTest(unittest.TestCase):
    def test_schedule_uses_delay(self):
        with patch.object(scheduler.run_tests, 'delay', return_value='ok') as delay:
            result = scheduler.schedule(['x'])
            delay.assert_called_once_with(['x'])
            self.assertEqual(result, 'ok')

    def test_run_tests_calls_aggregator(self):
        with patch('src.tma.scheduler.aggregate_results', return_value={'t': 1}) as agg:
            result = scheduler.run_tests(['m'])
            agg.assert_called_once_with(['m'])
            self.assertEqual(result, {'t': 1})
