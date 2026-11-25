---
name: reference-video-blueprint
description: Analyze authorized videos into original prompt contracts.
version: 0.2.0
author: Mason Mosen, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video-analysis, vision-language-model, shot-breakdown, original-production]
    related_skills: []
---

# Reference Video Blueprint

Turn a user-owned or authorized local reference video into frame-level visual evidence, a safe original-production review, and a complete renderer-neutral Prompt Contract. It uses local `ffmpeg` plus a local Ollama vision model; it does not download social videos, recover hidden source prompts, or reproduce protected source expression.

## When to Use

- A creator has rights to analyze a local video and needs an actual visual breakdown, not a generic prompt template.
- A team wants an evidence-linked production handoff containing scene, action, composition, camera, sound, continuity, and negative constraints per beat.
- A user wants to reuse a general mechanism—such as a reveal, before/after state, pacing, or visual metaphor—inside a materially new production brief.

Do not use for unlicensed media, source-shot duplication, likeness/voice imitation, copying original dialogue/music/brands/characters, or claiming the output is recovered source code.

## Prerequisites

- A local video file the user owns or is authorized to analyze.
- Python 3, `ffmpeg`, and `ffprobe` on `PATH`.
- Local Ollama running at `http://127.0.0.1:11434`.
- The tested vision model:

```bash
ollama pull qwen2.5vl:7b
```

The model download is free but uses local disk space. No API key is required. The default endpoint is loopback-only; non-loopback endpoints require `--allow-remote-ollama` because they receive extracted video frames.

## Quick Start

Use `terminal` to run the complete workflow:

```bash
python3 scripts/run_video_blueprint.py \
  --source /path/to/authorized-reference.mp4 \
  --output-dir output/reference-study \
  --rights-confirmation "I own or am authorized to analyze this video." \
  --purpose "Study the hook, visual-change rhythm, and payoff structure." \
  --original-brief "Create an original 9:16 explainer about a creator turning scattered research into a production plan." \
  --model qwen2.5vl:7b \
  --sample-interval 1
```

This produces:

```text
output/reference-study/
├── frames/                           evidence JPEGs with timestamps
├── vision_analysis.json              model-inferred visual evidence + uncertainty
├── review.json                       originalized beat review
├── production_prompt_contract.json   structured downstream handoff
└── production_prompt_contract.md     readable prompt packet
```

## Procedure

1. **Confirm rights and set a materially new brief.** Record authorization, study purpose, and an original target production.
   - Completion: `--rights-confirmation`, `--purpose`, and `--original-brief` are all supplied.
2. **Extract and inspect evidence frames.** The runner samples local frames at the chosen interval and records source SHA-256.
   - Completion: `frames/` and `vision_analysis.json` exist with evidence IDs and timestamps.
3. **Run local visual analysis.** Each sampled frame is sent to Ollama with a strict JSON Schema.
   - Completion: every frame contains `observable_evidence`, `unknowns`, `confidence`, and `source_label: model_inference`.
4. **Originalize each beat.** The model must identify possible protected elements, required replacements, an abstract reusable mechanism, and a new adaptation under the supplied original brief.
   - Completion: `review.json` has a non-empty beat list with evidence IDs, replacement decisions, and negative constraints.
5. **Compile the Prompt Contract.** The runner invokes `scripts/compile_prompt_contract.py` automatically.
   - Completion: JSON and Markdown contracts exist; every beat has `scene`, `visual`, `action`, `camera`, `sound`, `continuity`, and `negative_constraints`; contract coverage is marked `complete` or `partial`.
6. **Human review gate.** Every contract carries `approval_status: requires_human_approval`; review unknowns, possible protected elements, source-specific text/people/brands, and all prompt content before any rendering or publishing.
   - Completion: the intended production is materially new and downstream tool/provider use is approved.

## Evidence Rules

- A frame analysis is `model_inference`, not forensic fact.
- `unknowns` must capture unsupported claims, especially audio, motion between sampled frames, intent, identity, and off-screen context.
- One malformed model response receives one schema-repair pass. A second invalid response fails the run; the tool does not silently invent a complete analysis.
- Do not equate a source frame with a target composition. The target must satisfy the new original brief, not imitate the reference.

## Originalization Rules

Always replace or exclude recognizable people, voices, copyrighted characters, source dialogue/subtitles/music, trademarks, logos, product packaging, and distinctive story expression. Keep only abstract mechanisms such as information-state change, before/after contrast, reveal rhythm, visual metaphor, or action-to-payoff progression.

## Verification

Run the deterministic code-path suite:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/analyze_video.py scripts/analyze_video_with_vision.py scripts/compile_prompt_contract.py scripts/run_video_blueprint.py
```

Before calling any release user-ready, run the full workflow on a real user-owned or explicitly authorized video, inspect every beat, and verify that the output can be used by the intended downstream renderer or editor.

## Pitfalls

- A small visual model can hallucinate or omit fields. The schema, evidence IDs, confidence, unknowns, and human gate are safeguards, not a guarantee of semantic correctness.
- Sampling frames is not a forensic camera-motion measurement. Use closer intervals and human review for fast action.
- Do not ship user video, evidence frames, or local outputs in the public repository.
- Paid generation, rendering, or publishing requires a separate provider/budget/approval decision.
