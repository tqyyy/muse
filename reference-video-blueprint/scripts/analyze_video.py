#!/usr/bin/env python3
"""Create evidence artifacts from an authorized local reference video."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run(command):
    return subprocess.run(command, text=True, capture_output=True, check=False)


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path):
    result = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,width,height,r_frame_rate",
        "-of", "json", str(path),
    ])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    payload = json.loads(result.stdout)
    duration = float(payload.get("format", {}).get("duration", 0))
    video = next((item for item in payload.get("streams", []) if item.get("codec_type") == "video"), {})
    return {
        "duration_seconds": round(duration, 3),
        "width": video.get("width"),
        "height": video.get("height"),
        "frame_rate": video.get("r_frame_rate"),
    }


def extract_frames(source, frames_dir, duration, interval):
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old_frame in frames_dir.glob("*.jpg"):
        old_frame.unlink()
    pattern = str(frames_dir / "evidence_%04d.jpg")
    result = run([
        "ffmpeg", "-y", "-v", "error", "-i", str(source), "-vf",
        "fps=1/{0}".format(interval), "-q:v", "3", pattern,
    ])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "ffmpeg frame extraction failed")
    frames = []
    for index, frame in enumerate(sorted(frames_dir.glob("*.jpg"))):
        timestamp = min(round(index * interval, 3), duration)
        frames.append({
            "evidence_id": "F{0:03d}".format(index + 1),
            "timestamp_seconds": timestamp,
            "frame": "frames/{0}".format(frame.name),
            "observations": [],
            "confidence": "unreviewed",
        })
    return frames


def blueprint(source, purpose, frames):
    rows = []
    for frame in frames:
        rows.append(
            "| {id} | {time:.3f}s | `{frame}` | _review required_ | _review required_ | "
            "Replace all protected people, brands, script, music, and unique story elements. |".format(
                id=frame["evidence_id"], time=frame["timestamp_seconds"], frame=frame["frame"]
            )
        )
    return """# Originalization Blueprint\n\n## Purpose\n{purpose}\n\n## Source Boundary\n- Local reference file: `{source}`\n- This document records observable evidence and hypotheses. It does not authorize copying.\n- Analyze only media you own or are authorized to use.\n\n## Must replace before production\n- Recognizable people, voices, copyrighted characters, trademarks, product packaging, original dialogue, subtitles, music, and distinctive plot beats.\n- Any uncertain element must be reviewed by a human before a production prompt is used.\n\n## Evidence-to-originalization ledger\n| Evidence | Time | Frame | Observable evidence | Reusable mechanism | Original adaptation |\n|---|---:|---|---|---|---|\n{rows}\n\n## Human review gate\n1. Label each observation as **observable evidence** or **creative inference**.\n2. Identify the hook, attention promise, visual change cadence, payoff, sound cue, and ending mechanism.\n3. Design a materially new subject, scene, copy, visuals, sound, and brand treatment.\n4. Create a generator-specific prompt only after protected elements are replaced.\n5. Validate the generated result against the new brief, not against frame-by-frame similarity to the reference.\n""".format(source=source.name, purpose=purpose, rows="\n".join(rows))


def main():
    parser = argparse.ArgumentParser(description="Create an evidence-first reference-video blueprint.")
    parser.add_argument("--source", type=Path, required=True, help="Authorized local video file.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--rights-confirmation", help="Required statement confirming authorization.")
    parser.add_argument("--purpose", required=True, help="What reusable mechanism you are studying.")
    parser.add_argument("--sample-interval", type=float, default=1.0)
    args = parser.parse_args()

    if not args.rights_confirmation or not args.rights_confirmation.strip():
        parser.error("rights confirmation is required before analysis")
    if args.sample_interval <= 0:
        parser.error("sample interval must be greater than zero")
    source = args.source.expanduser().resolve()
    if not source.is_file():
        parser.error("source file does not exist: {0}".format(source))
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("ffmpeg and ffprobe must be available on PATH")

    output = args.output_dir.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    metadata = probe(source)
    frames = extract_frames(source, output / "frames", metadata["duration_seconds"], args.sample_interval)
    ledger = {
        "schema_version": "0.1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {"filename": source.name, "sha256": sha256_file(source), **metadata},
        "rights_confirmation": args.rights_confirmation.strip(),
        "study_purpose": args.purpose.strip(),
        "evidence_frames": frames,
        "limitations": [
            "Frames are evidence samples, not a claim of camera-motion certainty.",
            "Creative intent, protected elements, and prompt language require human review.",
        ],
    }
    (output / "shot_ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "originalization_blueprint.md").write_text(
        blueprint(source, args.purpose.strip(), frames), encoding="utf-8"
    )
    print(json.dumps({"output_dir": str(output), "frames": len(frames)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
