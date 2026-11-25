---
name: cueshot-shot-designer-starter
description: Use when turning a rough AI video idea into a basic shot plan and model-neutral prompt.
version: 0.1.0
license: MIT
---

# CueShot Shot Designer Starter

Turn a rough scene idea into a simple, shootable AI video prompt. This free Starter focuses on core shot planning, not full director-pack routing.

## Use when

- The user has a scene, emotion, product moment, story beat, or reference-image description.
- The user needs a model-neutral prompt for AI video.
- The user wants less vague language than “cinematic” or “movie-like”.

## Workflow

1. Preserve fixed facts: subject, setting, action, time, mood, props, wardrobe, and any reference-image locks.
2. Choose one of:
   - `single shot` when the brief has one action or one emotional beat.
   - `2–3 shots` when the brief has reveal → reaction → action, confrontation, environmental reveal, or location/time change.
3. Define each shot by:
   - narrative purpose
   - subject placement
   - camera distance / angle / movement
   - light direction / color / contrast
   - continuity constraints
4. Write a model-neutral prompt using concrete visual instructions.
5. Add negative constraints only for likely failure points.
6. Add recommended aspect ratio / duration outside the prompt.

## Output format

```markdown
## Shot mode
single shot | 2–3 shots

## Shot plan
- Shot 1: ...
- Shot 2: ...

## Model-neutral prompt
...

## Negative constraints
...

## Suggested settings
- Duration:
- Aspect ratio:
- Notes:
```

## Compliance

Director or film references, if mentioned by the user, are treated only as learning/planning references. The executable prompt must not rely on a director name, film title, character, brand, or protected scene.
