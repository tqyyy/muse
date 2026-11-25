import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "analyze_video.py"


def make_fixture(path: Path) -> None:
    command = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=320x180:d=1:r=12",
        "-f", "lavfi", "-i", "color=c=white:s=320x180:d=1:r=12",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
        "-map", "[v]", str(path),
    ]
    subprocess.run(command, check=True, capture_output=True)


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class AnalyzeVideoTests(unittest.TestCase):
    def test_requires_explicit_rights_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "reference.mp4"
            make_fixture(source)

            result = run_cli(
                "--source", str(source),
                "--output-dir", str(root / "out"),
                "--purpose", "Study an original explainer pacing pattern.",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("rights confirmation", result.stderr.lower())

    def test_creates_evidence_ledger_and_originalization_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "reference.mp4"
            output = root / "out"
            make_fixture(source)

            result = run_cli(
                "--source", str(source),
                "--output-dir", str(output),
                "--rights-confirmation", "I own or am authorized to analyze this video.",
                "--purpose", "Learn the pacing for an original product explainer.",
                "--sample-interval", "0.5",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            ledger = json.loads((output / "shot_ledger.json").read_text(encoding="utf-8"))
            blueprint = (output / "originalization_blueprint.md").read_text(encoding="utf-8")
            self.assertTrue(ledger["source"]["sha256"])
            self.assertEqual(ledger["rights_confirmation"], "I own or am authorized to analyze this video.")
            self.assertGreaterEqual(len(ledger["evidence_frames"]), 3)
            self.assertTrue(all(item["timestamp_seconds"] >= 0 for item in ledger["evidence_frames"]))
            self.assertIn("Must replace before production", blueprint)
            self.assertIn("Observable evidence", blueprint)


if __name__ == "__main__":
    unittest.main()
