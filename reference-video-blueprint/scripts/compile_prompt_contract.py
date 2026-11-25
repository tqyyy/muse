#!/usr/bin/env python3
"""Compile reviewed video evidence into a standardized original prompt contract."""

import argparse
import json
import math
import sys
from pathlib import Path


REQUIRED_PROJECT_FIELDS = (
    "title",
    "platform",
    "aspect_ratio",
    "duration_seconds",
    "creative_brief",
    "global_negative_constraints",
)
REQUIRED_BEAT_FIELDS = (
    "id",
    "start_seconds",
    "end_seconds",
    "evidence_ids",
    "observable_evidence",
    "reusable_mechanism",
    "original_adaptation",
    "prompt",
)
REQUIRED_PROMPT_FIELDS = (
    "scene",
    "visual",
    "action",
    "camera",
    "sound",
    "continuity",
    "negative_constraints",
)


def fail(message):
    raise ValueError(message)


def require_text(mapping, key, location):
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        fail("{0}.{1} is required".format(location, key))
    return value.strip()


def require_list(mapping, key, location):
    value = mapping.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        fail("{0}.{1} must be a non-empty list of text values".format(location, key))
    return [item.strip() for item in value]


def require_finite_number(value, location):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        fail("{0} must be a finite number".format(location))
    return float(value)


def validate(review):
    if not isinstance(review, dict):
        fail("review must be a JSON object")
    project = review.get("project")
    if not isinstance(project, dict):
        fail("project must be an object")
    for key in REQUIRED_PROJECT_FIELDS:
        if key == "duration_seconds":
            value = require_finite_number(project.get(key), "project.duration_seconds")
            if value <= 0:
                fail("project.duration_seconds must be a positive number")
        elif key == "global_negative_constraints":
            require_list(project, key, "project")
        else:
            require_text(project, key, "project")

    beats = review.get("beats")
    if not isinstance(beats, list) or not beats:
        fail("beats must be a non-empty list")

    previous_end = 0.0
    for index, beat in enumerate(beats, 1):
        location = "beats[{0}]".format(index)
        if not isinstance(beat, dict):
            fail("{0} must be an object".format(location))
        for key in REQUIRED_BEAT_FIELDS:
            if key not in beat:
                fail("{0}.{1} is required".format(location, key))
        require_text(beat, "id", location)
        require_list(beat, "evidence_ids", location)
        require_text(beat, "observable_evidence", location)
        require_text(beat, "reusable_mechanism", location)
        require_text(beat, "original_adaptation", location)
        start = require_finite_number(beat.get("start_seconds"), location + ".start_seconds")
        end = require_finite_number(beat.get("end_seconds"), location + ".end_seconds")
        if start < 0 or end <= start:
            fail("{0} must have a non-negative start_seconds and a later end_seconds".format(location))
        if start < previous_end:
            fail("{0}.start_seconds must not overlap the preceding beat".format(location))
        previous_end = float(end)
        prompt = beat.get("prompt")
        if not isinstance(prompt, dict):
            fail("{0}.prompt must be an object".format(location))
        for key in REQUIRED_PROMPT_FIELDS:
            if key == "negative_constraints":
                require_list(prompt, key, location + ".prompt")
            else:
                require_text(prompt, key, location + ".prompt")


def normalized_review(review):
    project = review["project"]
    project_payload = {
        "title": require_text(project, "title", "project"),
        "platform": require_text(project, "platform", "project"),
        "aspect_ratio": require_text(project, "aspect_ratio", "project"),
        "duration_seconds": float(project["duration_seconds"]),
        "creative_brief": require_text(project, "creative_brief", "project"),
        "global_negative_constraints": require_list(project, "global_negative_constraints", "project"),
    }
    if "analysis_coverage" in project:
        coverage = project["analysis_coverage"]
        if not isinstance(coverage, dict) or coverage.get("status") not in {"complete", "partial"}:
            fail("project.analysis_coverage must declare complete or partial status")
        project_payload["analysis_coverage"] = coverage
    if "approval_status" in project:
        if project["approval_status"] != "requires_human_approval":
            fail("project.approval_status must be requires_human_approval")
        project_payload["approval_status"] = project["approval_status"]
    beats = []
    for beat in review["beats"]:
        prompt = beat["prompt"]
        beats.append({
            "id": require_text(beat, "id", "beat"),
            "start_seconds": float(beat["start_seconds"]),
            "end_seconds": float(beat["end_seconds"]),
            "evidence_ids": require_list(beat, "evidence_ids", "beat"),
            "observable_evidence": require_text(beat, "observable_evidence", "beat"),
            "reusable_mechanism": require_text(beat, "reusable_mechanism", "beat"),
            "original_adaptation": require_text(beat, "original_adaptation", "beat"),
            "prompt": {
                field: require_text(prompt, field, "prompt")
                for field in REQUIRED_PROMPT_FIELDS if field != "negative_constraints"
            } | {"negative_constraints": require_list(prompt, "negative_constraints", "prompt")},
        })
    return {
        "schema_version": "0.1.0",
        "project": project_payload,
        "beats": beats,
    }


def beat_prompt(beat, project):
    prompt = beat["prompt"]
    return " ".join([
        "Create an original {ratio} {platform} beat from {start:.1f}s to {end:.1f}s.".format(
            ratio=project["aspect_ratio"], platform=project["platform"],
            start=beat["start_seconds"], end=beat["end_seconds"],
        ),
        "Scene: {0}".format(prompt["scene"]),
        "Visual: {0}".format(prompt["visual"]),
        "Action: {0}".format(prompt["action"]),
        "Camera: {0}".format(prompt["camera"]),
        "Sound: {0}".format(prompt["sound"]),
        "Continuity: {0}".format(prompt["continuity"]),
        "Original adaptation: {0}".format(beat["original_adaptation"]),
        "Negative constraints: {0}.".format("; ".join(project["global_negative_constraints"] + prompt["negative_constraints"])),
    ])


def markdown(contract):
    project = contract["project"]
    lines = [
        "# Production Prompt Contract",
        "",
        "## Project",
        "- Title: {0}".format(project["title"]),
        "- Platform: {0}".format(project["platform"]),
        "- Aspect ratio: {0}".format(project["aspect_ratio"]),
        "- Duration: {0:g}s".format(project["duration_seconds"]),
        "- Creative brief: {0}".format(project["creative_brief"]),
        "",
        "## Global negative constraints",
    ]
    lines.extend("- {0}".format(item) for item in project["global_negative_constraints"])
    for beat in contract["beats"]:
        lines.extend([
            "",
            "## Beat {0} · {1:.1f}s–{2:.1f}s".format(beat["id"], beat["start_seconds"], beat["end_seconds"]),
            "- Evidence IDs: {0}".format(", ".join(beat["evidence_ids"])),
            "- Observable evidence: {0}".format(beat["observable_evidence"]),
            "- Reusable mechanism: {0}".format(beat["reusable_mechanism"]),
            "- Original adaptation: {0}".format(beat["original_adaptation"]),
            "",
            "### Generator prompt",
            "```text",
            beat_prompt(beat, project),
            "```",
        ])
    lines.extend([
        "",
        "## Human approval gate",
        "1. Confirm each beat is materially new and does not reproduce protected source elements.",
        "2. Confirm sound, text, people, logos, and brands are authorized or newly created.",
        "3. Render only after a provider, budget, and intended publication use are approved.",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Compile reviewed evidence into an original production prompt contract.")
    parser.add_argument("--review", type=Path, required=True, help="Reviewed evidence JSON input.")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        review = json.loads(args.review.read_text(encoding="utf-8"))
    except OSError as error:
        parser.error("could not read review: {0}".format(error))
    except json.JSONDecodeError as error:
        parser.error("review is not valid JSON: {0}".format(error))
    try:
        validate(review)
        contract = normalized_review(review)
    except ValueError as error:
        parser.error(str(error))

    output = args.output_dir.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "production_prompt_contract.json").write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    (output / "production_prompt_contract.md").write_text(markdown(contract), encoding="utf-8")
    print(json.dumps({"output_dir": str(output), "beats": len(contract["beats"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
