# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ['TMA_CONFIG'] = str(Path(__file__).resolve().parents[1] / 'tma.yaml')
from src.tma import aggregator
import yaml


class AggregatorReportTest(unittest.TestCase):
    def test_reports_and_metrics_created(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                def fake_run(cmd, check=False, env=None):
                    Path('reports').mkdir(exist_ok=True)
                    Path('reports/results.xml').write_text(
                        '<testsuite tests="2" failures="1" skipped="1"/>',
                        encoding='utf-8',
                    )
                    return subprocess.CompletedProcess(cmd, 0)

                with patch('subprocess.run', side_effect=fake_run):
                    result = aggregator.aggregate_results([])

                metrics_file = Path('reports/metrics.yaml')
                self.assertTrue(metrics_file.exists())
                data = yaml.safe_load(metrics_file.read_text())
                self.assertEqual(data, {'tests': 2, 'failures': 1, 'skipped': 1})
                self.assertTrue(Path(result['html']).exists())
            finally:
                os.chdir(cwd)
