# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import unittest
import tempfile
from pathlib import Path

from src.directory_utils import bfs_directory_names


class DirectoryUtilsTest(unittest.TestCase):
    def test_bfs_directory_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").mkdir()
            (root / "b").mkdir()
            (root / "a" / "c").mkdir()
            (root / "a" / "d").mkdir()
            result = bfs_directory_names(root)
            self.assertEqual(result, ["a", "b", "a/c", "a/d"])


if __name__ == "__main__":
    unittest.main()
