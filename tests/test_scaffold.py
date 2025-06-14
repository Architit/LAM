import subprocess
import tempfile
from pathlib import Path
import unittest

from src import lam_cli


class ScaffoldLintTest(unittest.TestCase):
    def test_generated_files_lint(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir)
            lam_cli.scaffold(Path("100_GenomicYAML_Template.yaml"), out)
            files = [out / "membrane.go", out / "nucleus.go", out / "guardian" / "guardian.go"]
            for f in files:
                result = subprocess.run([
                    "gofmt",
                    "-e",
                    str(f),
                ], capture_output=True, text=True)
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"gofmt errors for {f}: {result.stderr}",
                )


if __name__ == "__main__":
    unittest.main()
