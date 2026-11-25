import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "compile_prompt_contract.py"


class PromptContractCompilerTests(unittest.TestCase):
    def write_review(self, directory: Path, payload: dict) -> Path:
        path = directory / "review.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def valid_review(self) -> dict:
        return {
            "project": {
                "title": "Original Evidence Cards",
                "platform": "short-form vertical video",
                "aspect_ratio": "9:16",
                "duration_seconds": 6,
                "creative_brief": "Turn scattered research into an original, clear production plan.",
                "global_negative_constraints": [
                    "No reference footage or copied frames",
                    "No third-party logos, people, music, dialogue, or pseudo-text",
                ],
            },
            "beats": [
                {
                    "id": "B01",
                    "start_seconds": 0,
                    "end_seconds": 3,
                    "evidence_ids": ["F001", "F002"],
                    "observable_evidence": "The reviewed source changes from one stable visual state to another.",
                    "reusable_mechanism": "A clear state change creates an early pattern interrupt.",
                    "original_adaptation": "Abstract note fragments organize into evidence cards.",
                    "prompt": {
                        "scene": "A dark editorial workspace made only of abstract paper shapes.",
                        "visual": "Three off-white note fragments float against a charcoal background.",
                        "action": "The fragments align into one clean evidence card.",
                        "camera": "Slow centered push-in, no handheld motion.",
                        "sound": "Three soft paper clicks followed by a restrained tonal lift.",
                        "continuity": "Use charcoal, muted teal, and one amber accent; no text or logos.",
                        "negative_constraints": ["No recognizable people", "No copied composition"],
                    },
                },
                {
                    "id": "B02",
                    "start_seconds": 3,
                    "end_seconds": 6,
                    "evidence_ids": ["F003"],
                    "observable_evidence": "A second visual state holds after the transition.",
                    "reusable_mechanism": "A resolved state gives the viewer a simple payoff.",
                    "original_adaptation": "Evidence cards expand into a new storyboard grid.",
                    "prompt": {
                        "scene": "The same abstract workspace after the cards have aligned.",
                        "visual": "The evidence card opens into a small luminous storyboard grid.",
                        "action": "The grid settles and reveals one warm focal tile.",
                        "camera": "Continue the centered push-in and finish on a stable frame.",
                        "sound": "One clean chime, then a short natural decay.",
                        "continuity": "Keep the same palette and geometry from B01.",
                        "negative_constraints": ["No brand marks", "No reference-frame recreation"],
                    },
                },
            ],
        }

    def test_compiles_a_standardized_markdown_and_json_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            review = self.write_review(root, self.valid_review())
            output = root / "contract"

            result = self.run_cli("--review", str(review), "--output-dir", str(output))

            self.assertEqual(result.returncode, 0, result.stderr)
            markdown = (output / "production_prompt_contract.md").read_text(encoding="utf-8")
            compiled = json.loads((output / "production_prompt_contract.json").read_text(encoding="utf-8"))
            self.assertIn("## Beat B01 · 0.0s–3.0s", markdown)
            self.assertIn("### Generator prompt", markdown)
            self.assertIn("No reference footage or copied frames", markdown)
            self.assertEqual(compiled["schema_version"], "0.1.0")
            self.assertEqual(compiled["beats"][0]["evidence_ids"], ["F001", "F002"])
            self.assertIn("scene", compiled["beats"][0]["prompt"])

    def test_rejects_non_finite_timestamps_and_duration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = self.valid_review()
            payload["project"]["duration_seconds"] = float("nan")
            payload["beats"][0]["start_seconds"] = float("nan")
            review = self.write_review(root, payload)

            result = self.run_cli("--review", str(review), "--output-dir", str(root / "contract"))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("finite", result.stderr)

    def test_rejects_a_beat_without_original_adaptation_or_negative_constraints(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = self.valid_review()
            del payload["beats"][0]["original_adaptation"]
            payload["beats"][0]["prompt"]["negative_constraints"] = []
            review = self.write_review(root, payload)

            result = self.run_cli("--review", str(review), "--output-dir", str(root / "contract"))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("original_adaptation", result.stderr)


if __name__ == "__main__":
    unittest.main()
