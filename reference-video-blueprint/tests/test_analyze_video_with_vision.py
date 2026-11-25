import base64
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "analyze_video_with_vision.py"


def make_fixture(path: Path) -> None:
    command = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=160x90:d=1:r=8",
        "-f", "lavfi", "-i", "color=c=white:s=160x90:d=1:r=8",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
        "-map", "[v]", str(path),
    ]
    subprocess.run(command, check=True, capture_output=True)


class FakeOllamaHandler(BaseHTTPRequestHandler):
    requests = []
    response_queue = []
    response_body = {
        "response": json.dumps({
            "scene": "an abstract dark visual field",
            "subjects": ["no people visible"],
            "action": "no visible motion can be confirmed from one frame",
            "composition": "full-frame field",
            "visible_text": [],
            "possible_protected_elements": [],
            "unknowns": ["audio", "motion between frames"],
            "confidence": "medium",
            "reusable_mechanism": "A stable opening state creates contrast for a later transition.",
            "required_replacements": ["Any source-specific color treatment"],
            "original_adaptation": "New abstract note fragments organize into evidence cards.",
            "prompt": {
                "scene": "An original charcoal editorial workspace.",
                "visual": "Abstract paper-note fragments with muted teal edge light.",
                "action": "Fragments drift inward without forming a copy of the source.",
                "camera": "Stable centered view.",
                "sound": "No source audio; use a new restrained tonal texture.",
                "continuity": "Keep an original charcoal, teal, and amber palette.",
                "negative_constraints": ["No source frame recreation", "No logos or recognizable people"]
            },
        })
    }

    def log_message(self, format, *args):
        return

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        type(self).requests.append(body)
        response_body = type(self).response_queue.pop(0) if type(self).response_queue else type(self).response_body
        payload = json.dumps(response_body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class VisionAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        FakeOllamaHandler.requests = []
        FakeOllamaHandler.response_queue = []
        FakeOllamaHandler.response_body = {
            "response": json.dumps({
                "scene": "an abstract dark visual field",
                "subjects": ["no people visible"],
                "action": "no visible motion can be confirmed from one frame",
                "composition": "full-frame field",
                "visible_text": [],
                "possible_protected_elements": [],
                "unknowns": ["audio", "motion between frames"],
                "confidence": "medium",
                "reusable_mechanism": "A stable opening state creates contrast for a later transition.",
                "required_replacements": ["Any source-specific color treatment"],
                "original_adaptation": "New abstract note fragments organize into evidence cards.",
                "prompt": {
                    "scene": "An original charcoal editorial workspace.",
                    "visual": "Abstract paper-note fragments with muted teal edge light.",
                    "action": "Fragments drift inward without forming a copy of the source.",
                    "camera": "Stable centered view.",
                    "sound": "No source audio; use a new restrained tonal texture.",
                    "continuity": "Keep an original charcoal, teal, and amber palette.",
                    "negative_constraints": ["No source frame recreation", "No logos or recognizable people"]
                },
            })
        }
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeOllamaHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_sends_extracted_frames_to_a_vision_model_and_writes_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            output = root / "output"
            make_fixture(source)

            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(output),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--sample-interval", "0.5",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            analysis = json.loads((output / "vision_analysis.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(analysis["frame_analysis"]), 3)
            self.assertEqual(analysis["frame_analysis"][0]["source_label"], "model_inference")
            self.assertIn("unknowns", analysis["frame_analysis"][0])
            review = json.loads((output / "review.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(review["beats"]), 3)
            self.assertEqual(review["beats"][0]["evidence_ids"], ["F001"])
            self.assertIn("negative_constraints", review["beats"][0]["prompt"])
            self.assertIn("No source frame recreation", review["beats"][0]["prompt"]["negative_constraints"])
            self.assertGreaterEqual(len(FakeOllamaHandler.requests), 3)
            first_request = FakeOllamaHandler.requests[0]
            self.assertEqual(first_request["model"], "fake-vision")
            self.assertEqual(first_request["format"]["type"], "object")
            self.assertIn("visible_text", first_request["format"]["required"])
            self.assertTrue(first_request["images"])
            self.assertGreater(len(base64.b64decode(first_request["images"][0])), 100)

    def test_rejects_a_non_loopback_ollama_endpoint_without_explicit_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            make_fixture(source)

            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(root / "output"),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--ollama-url", "https://example.invalid/api/generate",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("loopback", result.stderr)
            self.assertEqual(FakeOllamaHandler.requests, [])

    def test_marks_review_partial_when_frame_cap_omits_video_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            output = root / "output"
            make_fixture(source)

            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(output),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
                "--sample-interval", "0.5",
                "--max-frames", "1",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            review = json.loads((output / "review.json").read_text(encoding="utf-8"))
            self.assertEqual(review["project"]["analysis_coverage"]["status"], "partial")
            self.assertLess(review["project"]["analysis_coverage"]["analyzed_until_seconds"], review["project"]["duration_seconds"])

    def test_rejects_model_output_with_invalid_confidence(self) -> None:
        invalid = json.loads(FakeOllamaHandler.response_body["response"])
        invalid["confidence"] = "certain"
        FakeOllamaHandler.response_body = {"response": json.dumps(invalid)}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            make_fixture(source)
            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(root / "output"),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("confidence", result.stderr)

    def test_normalizes_an_empty_frame_action_to_an_explicit_unknown(self) -> None:
        invalid = json.loads(FakeOllamaHandler.response_body["response"])
        invalid["action"] = ""
        FakeOllamaHandler.response_queue = [
            {"response": json.dumps(invalid)},
            FakeOllamaHandler.response_body,
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            output = root / "output"
            make_fixture(source)
            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(output),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            analysis = json.loads((output / "vision_analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(analysis["frame_analysis"][0]["analysis"]["action"], "unknown from this single frame")

    def test_rejects_placeholder_analysis_text_before_contract_generation(self) -> None:
        invalid = json.loads(FakeOllamaHandler.response_body["response"])
        invalid["reusable_mechanism"] = "abstract visual/attention mechanism only"
        FakeOllamaHandler.response_body = {"response": json.dumps(invalid)}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            make_fixture(source)
            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(root / "output"),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("placeholder", result.stderr)

    def test_rejects_model_copying_language_before_contract_generation(self) -> None:
        invalid = json.loads(FakeOllamaHandler.response_body["response"])
        invalid["original_adaptation"] = "Exactly reproduce the source frame and its original expression."
        FakeOllamaHandler.response_body = {"response": json.dumps(invalid)}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            make_fixture(source)
            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(root / "output"),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("copying language", result.stderr)

    def test_rejects_model_output_missing_required_uncertainty_fields(self) -> None:
        FakeOllamaHandler.response_body = {"response": json.dumps({"scene": "only a scene"})}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            make_fixture(source)

            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(root / "output"),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("subjects", result.stderr)
    def test_repairs_one_malformed_model_response_before_accepting_analysis(self) -> None:
        FakeOllamaHandler.response_queue = [
            {"response": json.dumps({
                "scene": "a dark blue field",
                "subjects": [],
                "action": "None",
                "composition": "full-frame field",
                "visible_text": [],
                "possible_protected_elements": [],
                "unknowns": ["audio"],
                "confidence": "low",
                "reusable_mthing": "",
                "required_replacements": [],
                "original_adaptation": "",
                "prompt": {"scene": "x"},
            })},
            FakeOllamaHandler.response_body,
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.mp4"
            make_fixture(source)
            result = self.run_cli(
                "--source", str(source),
                "--output-dir", str(root / "output"),
                "--rights-confirmation", "I own this fixture and authorize analysis.",
                "--purpose", "Study a general visual transition mechanism.",
                "--original-brief", "Create a materially new abstract research-to-storyboard micro explainer.",
                "--model", "fake-vision",
                "--ollama-url", "http://127.0.0.1:{0}/api/generate".format(self.server.server_port),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreaterEqual(len(FakeOllamaHandler.requests), 3)
            self.assertIn("repair", FakeOllamaHandler.requests[1]["prompt"].lower())


if __name__ == "__main__":
    unittest.main()
