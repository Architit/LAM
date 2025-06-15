import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import subprocess

from src.tma import aggregator


class AggregatorMatrixTest(unittest.TestCase):
    def test_matrix_passed_to_pytest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            os.chdir(tmpdir)
            os.environ['TMA_REPORTS_DIR'] = 'out/nested/reports'
            try:
                def fake_run(cmd, check=False, env=None):
                    Path('out/nested/reports').mkdir(parents=True, exist_ok=True)
                    Path('out/nested/reports/results.xml').write_text(
                        '<testsuite tests="1" failures="0" skipped="0"></testsuite>',
                        encoding='utf-8',
                    )
                    # verify command contains the matrix expression
                    self.assertIn('-k', cmd)
                    idx = cmd.index('-k')
                    self.assertEqual(cmd[idx + 1], 'a and b')
                    # verify environment variables present
                    self.assertIsNotNone(env)
                    self.assertEqual(env.get('MATRIX_0'), 'a')
                    self.assertEqual(env.get('MATRIX_1'), 'b')
                    return subprocess.CompletedProcess(cmd, 0)

                with patch('subprocess.run', side_effect=fake_run) as run_mock:
                    result = aggregator.aggregate_results(['a', 'b'])

                self.assertEqual(result['tests'], 1)
                self.assertTrue(Path(result['xml']).exists())
                self.assertTrue(Path(result['html']).exists())
                run_mock.assert_called_once()
            finally:
                os.chdir(cwd)
                os.environ.pop('TMA_REPORTS_DIR')


if __name__ == '__main__':
    unittest.main()
