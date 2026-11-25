# Example｜CueShot Review Room Starter

## Input

```text
Video/keyframes: one AI clip of a student outside a rainy convenience store.
Goal: publish if the emotion reads clearly and the food cup / face / rain stay stable.
```

## Output

### Decision

`Post-fix`

The clip is close to usable, but one visible artifact should be fixed or cut around before publishing.

### Visible evidence

- The subject identity and hoodie remain mostly stable.
- The rainy glass and wet street establish the intended atmosphere.
- The cup appears to slide slightly in the hand near the final beat.

### Issues

| Severity | Observation | Impact | Fix |
| --- | --- | --- | --- |
| major | Food cup position drifts during the final pause | Breaks physical believability at the emotional moment | Local regeneration or cut before the drift |
| minor | Rain streaks become slightly uniform near the edge | Noticeable but not story-breaking | Keep if platform compression hides it |

### Repair prompt

```text
Keep the same student, light hoodie, rainy convenience store entrance, warm food cup and wet glass. Repair only the final pause: the cup stays firmly held in the same hand, fingers keep consistent contact, the student's face and hoodie do not change, rain continues downward on the glass, camera remains steady with no new people or text.
```

### Re-check after repair

- Cup position stays locked through the final second.
- Face and hoodie do not change.
- Rain direction remains consistent.
- No new text, logo, or extra person appears.
```
