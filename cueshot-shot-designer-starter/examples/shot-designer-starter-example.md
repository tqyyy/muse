# Example｜CueShot Shot Designer Starter

## Input

```text
A student stands outside a rainy convenience store at night, holding a warm food cup, suddenly remembering home.
```

## Output

### Shot mode

`single shot`

Reason: the scene is one emotional beat with one subject, one location, and one action change: pause → remember → hold emotion.

### Shot plan

- **Narrative purpose:** show a quiet memory trigger, not plot action.
- **Subject placement:** student on the right third, glass door frame as partial foreground obstruction.
- **Camera:** medium shot, eye-level, slow push-in only after the subject pauses.
- **Light:** cool rain street background, warm spill from the convenience store on the food cup and lower face.
- **Continuity:** same clothes, same hand holding the cup, no extra shoppers entering frame.

### Model-neutral prompt

```text
Rainy night outside a small convenience store, one student in a light hoodie stands near the wet glass door holding a warm food cup; the student stops walking and looks through the rain-covered glass as if suddenly remembering home; medium shot with the student on the right third, door frame and raindrops as soft foreground layers, wet pavement reflecting cool street lights; eye-level camera begins still and then slowly pushes closer after the pause; warm indoor light touches the cup and lower face, background remains cool and blurred; identity, hoodie, cup, glass door position, rain direction and light direction stay consistent.
```

### Negative constraints

```text
No extra people entering frame, no readable logo, no burned-in text, no face change, no floating cup, no unmotivated spinning camera.
```

### Suggested settings

- Duration: 6–8 seconds.
- Aspect ratio: 9:16 for short video, 16:9 if the street depth matters more.
- Note: if the model struggles with the slow push-in, generate as a still medium shot and add motion in editing.
```
