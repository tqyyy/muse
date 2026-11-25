# Changelog

## 0.2.0 — 2026-08-26

- Added a local Ollama vision-analysis workflow that sends sampled evidence frames to a vision-language model using a strict JSON Schema.
- Added frame-level visual evidence labels: observable evidence, model-inference source label, confidence, and unknowns.
- Added automatic originalized beat-review generation and complete Prompt Contract compilation in one command: `scripts/run_video_blueprint.py`.
- Added model-response validation with one explicit repair pass; a second invalid answer stops the workflow rather than inventing output.
- Added code-path tests for vision requests, malformed response rejection/repair, and the full analysis-to-contract pipeline.
- Updated GitHub community edition requirements to local Ollama + `qwen2.5vl:7b`; no API key is required.
- Kept Capafy publication frozen: a paid release requires a verified enhancement beyond the complete free GitHub core.

## 0.1.3 — 2026-08-26

- Recorded approved Capafy launch setting: US$5 one-time download and US$0.99 first-publication certification fee.

## 0.1.2 — 2026-08-26

- Added a Capafy-ready Agent Card, upload exclusion list, and documented publication approval gates.

## 0.1.1 — 2026-08-26

- Added a GitHub Actions validation workflow for synthetic tests and syntax checks.

## 0.1.0 — 2026-08-26

- First public beta of the local, evidence-first reference video workflow.
- Added explicit rights confirmation before analysis.
- Added synthetic-fixture tests for evidence-ledger and originalization output.
- Added model-neutral production blueprint templates and marketplace material.
