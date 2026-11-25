---
name: cueshot-review-room-starter
description: Use when reviewing an AI video or keyframes with a lightweight director-style checklist.
version: 0.1.0
license: MIT
---

# CueShot Review Room Starter

Review an AI video result using visible evidence. This free Starter helps decide whether a clip is usable, needs simple repair, or should be regenerated.

## Use when

- The user has one AI video, keyframes, or screenshots.
- The user asks “can this publish?”, “why does it feel fake?”, or “how do I fix it?”.
- The user needs a basic Hold / Ship decision.

## Workflow

1. Identify the goal if provided; otherwise assume general pre-publish QC.
2. Check visible evidence only. Do not invent hidden metadata or exact camera settings.
3. Review five modules:
   - character / identity
   - motion / physics
   - scene / continuity
   - cinematography / readability
   - AI artifacts / text / logos / deformation
4. Decide:
   - `Ship` — usable as-is.
   - `Post-fix` — minor edit or masking can solve it.
   - `Regenerate segment` — a local section needs redo.
   - `Reject` — core idea or identity fails.
   - `Insufficient evidence` — not enough readable material.
5. Write a concise repair prompt when a repair is possible.

## Output format

```markdown
## Decision
Ship | Post-fix | Regenerate segment | Reject | Insufficient evidence

## Visible evidence
- ...

## Issues
| Severity | Observation | Impact | Fix |
| --- | --- | --- | --- |

## Repair prompt
...

## Re-check after repair
- ...
```

## Compliance

This skill does not provide copyright clearance, platform approval, or legal advice. It reviews visible AI video quality and gives creative repair guidance.
