import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "run_video_blueprint.py"


def make_fixture(path: Path) -> None:
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=160x90:d=1:r=8",
        "-f", "lavfi", "-i", "color=c=white:s=160x90:d=1:r=8",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
        "-map", "[v]", str(path),
    ], check=True, capture_output=True)


class FakeOllamaHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        response = {
            "response": json.dumps({
                "scene": "a non-branded abstract field",
                "subjects": ["no people visible"],
                "action": "motion is unknown from one frame",
                "composition": "full-frame geometric field",
                "visible_text": [],
                "possible_protected_elements": [],
                "unknowns": ["audio", "motion between frames"],
                "confidence": "medium",
                "reusable_mechanism": "A state change can create a simple beat transition.",
                "required_replacements": ["Source-specific visual treatment"],
                "original_adaptation": "New note fragments become a fresh storyboard grid.",
                "prompt": {
                    "scene": "An original charcoal workspace.",
                    "visual": "New abstract paper forms with teal edge light.",
                    "action": "Forms organize into cards.",
                    "camera": "Centered stable framing.",
                    "sound": "New quiet paper clicks only.",
                    "continuity": "Use original charcoal and amber palette.",
                    "negative_constraints": ["No source-frame recreation", "No brands or people"]
                }
            })
        }
        payload = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class VideoBlueprintPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeOllamaHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def test_creates_visual_evidence_review_and_complete_prompt_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            output = root / "output"
            make_fixture(source)
            result = subprocess.run([
                sys.executable, str(SCRIPT),
                "--source", str(source),
                "--output-dir", str(output),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new research-to-storyboard explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
                "--sample-interval", "0.5",
            ], text=True, capture_output=True, check=False)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "vision_analysis.json").is_file())
            self.assertTrue((output / "review.json").is_file())
            self.assertTrue((output / "production_prompt_contract.json").is_file())
            contract = json.loads((output / "production_prompt_contract.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(contract["beats"]), 3)
            self.assertIn("negative_constraints", contract["beats"][0]["prompt"])
            self.assertEqual(contract["project"]["analysis_coverage"]["status"], "complete")
            self.assertEqual(contract["project"]["approval_status"], "requires_human_approval")


if __name__ == "__main__":
    unittest.main()
