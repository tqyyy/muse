#!/usr/bin/env python3
"""Run local visual analysis and prompt-contract compilation as one verified workflow."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
VISION = SCRIPT_DIR / "analyze_video_with_vision.py"
COMPILER = SCRIPT_DIR / "compile_prompt_contract.py"


def run(command):
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip() or "subprocess failed"
        raise RuntimeError(message)
    return result


def main():
    parser = argparse.ArgumentParser(description="Run authorized-video visual analysis through a complete original Prompt Contract workflow.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--rights-confirmation", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--original-brief", required=True)
    parser.add_argument("--model", default="qwen2.5vl:7b")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/generate")
    parser.add_argument("--allow-remote-ollama", action="store_true", help="Explicitly permit the vision stage to upload frames to a remote endpoint.")
    parser.add_argument("--sample-interval", type=float, default=1.0)
    parser.add_argument("--max-frames", type=int, default=60)
    args = parser.parse_args()

    output = args.output_dir.expanduser().resolve()
    vision_command = [
        sys.executable, str(VISION),
        "--source", str(args.source),
        "--output-dir", str(output),
        "--rights-confirmation", args.rights_confirmation,
        "--purpose", args.purpose,
        "--original-brief", args.original_brief,
        "--model", args.model,
        "--ollama-url", args.ollama_url,
        *( ["--allow-remote-ollama"] if args.allow_remote_ollama else [] ),
        "--sample-interval", str(args.sample_interval),
        "--max-frames", str(args.max_frames),
    ]
    run(vision_command)
    review = output / "review.json"
    if not review.is_file():
        raise RuntimeError("vision analysis completed without review.json")
    run([sys.executable, str(COMPILER), "--review", str(review), "--output-dir", str(output)])
    contract = output / "production_prompt_contract.json"
    if not contract.is_file():
        raise RuntimeError("prompt compilation completed without production_prompt_contract.json")
    print(json.dumps({
        "output_dir": str(output),
        "vision_analysis": str(output / "vision_analysis.json"),
        "review": str(review),
        "prompt_contract": str(contract),
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
