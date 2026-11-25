# Reference Video Blueprint

**Agent Skill — Reference Video → Original Prompt Contract**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![GitHub stars](https://img.shields.io/github/stars/masonmosen/reference-video-blueprint.svg)](https://github.com/masonmosen/reference-video-blueprint/stargazers)

**Analyze an authorized reference video frame by frame, then produce a complete, original video Prompt Contract.**

**逐步分析你有权使用的参考视频，产出一份完整的原创视频 Prompt Contract。**

## Demo

![Evidence frames: 6 frames of Mason's own 6-second MOSEN intro](docs/demo/mosen-intro-6frames.jpg)

Example run: Mason's own 6-second brand intro → a 6-beat original Prompt Contract for a fictional paper-craft studio, PAPERFIELD (“one fold, one flight.”). Read it: [production_prompt_contract.md](docs/demo/production_prompt_contract.md) ([JSON](docs/demo/production_prompt_contract.json)).

> **Honest note:** the local Ollama vision-model step did **not** run in this demo — this machine has no Ollama and not enough memory for the 7B vision model, so frames were reviewed by eye and `analysis_coverage` is marked `partial`. This demo shows the contract workflow, not a full Ollama run.
>
> **诚实声明：** 本 Demo 没有跑本地 Ollama 视觉模型那一步（本机无 Ollama、内存不够跑 7B 模型），逐帧改为人工目视审查，`analysis_coverage` 标为 `partial`。本 Demo 展示的是 Contract 工作流，不是完整的 Ollama 全流程。

## Install

```bash
git clone https://github.com/masonmosen/reference-video-blueprint.git
cd reference-video-blueprint
ollama pull qwen2.5vl:7b
python3 scripts/run_video_blueprint.py --source /path/to/authorized-reference.mp4 --output-dir output/reference-study --rights-confirmation "I own or am authorized to analyze this video." --purpose "Study the hook, visual-change rhythm, and payoff structure." --original-brief "Create an original 9:16 explainer about a creator turning scattered research into a production plan." --sample-interval 1
```

Or install via the Skills CLI (`npx skills add masonmosen/reference-video-blueprint`) — it will ask which agent to install into.

## What you get

- Timestamped evidence frames from an authorized local video, with source SHA-256 and rights confirmation.
- Frame-level visual review with evidence / inference / unknown labels + confidence.
- Protected-element replacement decisions, so the output is original — not a copy.
- A complete Prompt Contract in JSON + Markdown, marked `requires_human_approval`.

`Reference Video Blueprint` is a local-first Agent Skill for creators who need to turn an authorized local video into a usable production handoff—not a folder of frames or an empty prompt template.

```text
Authorized local video
→ timestamped evidence frames
→ local vision-model analysis for every sampled frame
→ evidence / inference / unknown labels + confidence
→ protected-element replacement decisions
→ original beat-by-beat review.json
→ complete Prompt Contract (JSON + Markdown)
```

> **This is original-production analysis, not source duplication.** It does not download social videos, recover a source creator's hidden prompt, reproduce protected people/voices/music/brands/characters, or generate a final MP4 automatically.

## What it actually does

- Extracts timestamped JPEG evidence frames from an authorized local video.
- Records source SHA-256, metadata, rights confirmation, study purpose, and an original creative brief.
- Sends each sampled frame to a **local Ollama vision model**.
- Produces a visual review for every frame with observable scene/subjects/action/composition, visible text, possible protected elements, unknowns, and confidence.
- Produces a materially new adaptation for each beat and enforces prompt fields for scene, visual, action, camera, sound, continuity, and negative constraints.
- Compiles the review into `production_prompt_contract.json` and human-readable `production_prompt_contract.md`.

## Requirements

- Python 3
- `ffmpeg` and `ffprobe` on `PATH`
- [Ollama](https://ollama.com/) running locally
- A local vision model; the tested default is `qwen2.5vl:7b` (about 6 GB, free, no API key)
- A video you own or are authorized to analyze

Install the tested local vision model once:

```bash
ollama pull qwen2.5vl:7b
```

This product defaults to loopback-only Ollama (`127.0.0.1`, `localhost`, or `::1`), so frames stay on the machine. A non-loopback endpoint is rejected unless the user explicitly passes `--allow-remote-ollama`; that opt-in uploads extracted frames to the selected server. The model download is external network traffic.

## Quick start

Run the complete workflow on an authorized file:

```bash
python3 scripts/run_video_blueprint.py \
  --source /path/to/authorized-reference.mp4 \
  --output-dir output/reference-study \
  --rights-confirmation "I own or am authorized to analyze this video." \
  --purpose "Study the hook, visual-change rhythm, and payoff structure." \
  --original-brief "Create an original 9:16 explainer about a creator turning scattered research into a production plan." \
  --sample-interval 1
```

The `--original-brief` is required. It ensures the result is a new production direction, not a disguised request to copy the reference.

### Outputs

```text
output/reference-study/
├── frames/                           extracted timestamped evidence JPEGs
├── vision_analysis.json              frame-level model inference with uncertainty labels
├── review.json                       original beat review, ready for a downstream tool
├── production_prompt_contract.json   structured complete prompt contract
└── production_prompt_contract.md     readable beat-by-beat production handoff
```

`analysis_coverage.status` is `complete` only when every sampled frame was analyzed. If `--max-frames` limits the run, the review and contract are marked `partial` with the analyzed cutoff. Every generated contract is marked `requires_human_approval`; model output is not a production or publication authorization.

## Prompt Contract structure

Every produced beat contains:

```text
Evidence IDs and timestamps
Observable evidence
Reusable attention mechanism
Original adaptation
Scene / visual / action / camera / sound / continuity
Global and beat-level negative constraints
```

The JSON contract is designed for downstream Agent, video-generation, or editing workflows. It is renderer-neutral: a user must still map it to their selected execution tool and review the result before rendering or publishing.

## What the labels mean

| Label | Meaning |
|---|---|
| `observable_evidence` | What the visual model says is visible in one sampled frame. |
| `model_inference` | A model-generated interpretation, not forensic fact. |
| `unknowns` | Audio, motion between samples, intent, identity, or other details not safely established from the frame. |
| `confidence` | The model's own certainty level; it is not a guarantee. |
| `possible_protected_elements` | Items that must be replaced, excluded, or independently authorized before production. |

## Use the output safely

The workflow supports **original re-production of abstract mechanisms**—for example, a before/after progression, a reveal rhythm, an information-state change, or a visual metaphor.

It does not support:

- downloading, redistributing, or analyzing video without permission;
- one-to-one or near-substitute recreation of the source;
- copying source frames, composition, dialogue, subtitles, music, visual identity, products, logos, recognizable people, voices, characters, or story beats;
- treating model output as proof of copyright clearance, source prompt recovery, camera metadata, viewer psychology, or performance.

Review every output before rendering. If an element is uncertain, treat it as unknown and replace/exclude it.

## Verification

Automated tests use copyright-safe synthetic fixtures and a local fake Ollama server to verify the code path—not model quality:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/analyze_video.py scripts/analyze_video_with_vision.py scripts/compile_prompt_contract.py scripts/run_video_blueprint.py
```

Before treating a release as production-ready, also run the full command above on a real video that you own or are authorized to analyze, and inspect the evidence, review, and generated contract.

## Repository layout

```text
SKILL.md                              Agent workflow and quality gates
scripts/analyze_video.py              basic local evidence extractor
scripts/analyze_video_with_vision.py  local Ollama frame analysis + review generation
scripts/compile_prompt_contract.py    review → standardized JSON / Markdown contract
scripts/run_video_blueprint.py        one-command end-to-end workflow
examples/                             synthetic copyright-safe input/output shapes
tests/                                dependency-free code-path tests
```

## Versioning and marketplace boundary

GitHub is the free, functional core. A future Capafy version must provide a **clearly verified, meaningful enhancement** beyond this GitHub workflow; it must not repackage the same core function under a price tag.

## License

[MIT](LICENSE) © 2026 Mason Mosen.

---

## More from MOSEN

- [muse-video-prompt-skill](https://github.com/masonmosen/muse-video-prompt-skill) — Prompt engineering workflow for Muse built-in video generation.
- [ip-picture-workshop](https://github.com/masonmosen/ip-picture-workshop) — Photo + text → multi-page illustrated IP carousel.
- [mason-opc-motion-video](https://github.com/masonmosen/mason-opc-motion-video) — Talking-head video + script → editable motion-graphics video.
- [mosen-ad-studio](https://github.com/masonmosen/mosen-ad-studio) — Brand ads & product promos made entirely as code.
- [remake-depth-breakdown](https://github.com/masonmosen/remake-depth-breakdown) — Reference video → depth video + Seedance-ready prompts.
- [cueshot-starter-skills](https://github.com/masonmosen/cueshot-starter-skills) — Free starter skills for AI video shot planning & review.
