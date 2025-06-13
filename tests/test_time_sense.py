import unittest
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.time_sense import TimeSense, ParsedTime


class TimeSenseTest(unittest.TestCase):
    def setUp(self):
        self.ts = TimeSense()

    def test_parse_exact(self):
        p = self.ts.parse("12.06.2025 : 14:30")
        self.assertIsInstance(p.base, datetime)
        self.assertFalse(p.approx)
        self.assertEqual(p.base.year, 2025)

    def test_parse_approx(self):
        p = self.ts.parse("≈12.06.2025 : ≈14")
        self.assertTrue(p.approx)
        self.assertEqual(p.base.hour, 14)

    def test_parse_interval(self):
        p = self.ts.parse("Δ[12.06.2025:14:30±30мин]")
        self.assertEqual(p.tolerance, 30)

    def test_generate_fuzzy(self):
        dt = datetime(2025, 6, 12, 3, 0)
        self.assertEqual(self.ts.generate_fuzzy(dt), "≈ночь")

    def test_compare(self):
        a = self.ts.parse("Δ[12.06.2025:14:30±30мин]")
        b = self.ts.parse("12.06.2025 : 14:45")
        self.assertEqual(self.ts.compare(a, b), 0)


if __name__ == "__main__":
    unittest.main()
