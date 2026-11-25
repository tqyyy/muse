# Production Contract Schema

Use this structure after human review of `shot_ledger.json`. It records an original production plan; it is not a similarity target.

```json
{
  "project": {
    "title": "Original product explainer",
    "target_platform": "short-form vertical",
    "duration_seconds": 24,
    "source_reference_hash": "sha256..."
  },
  "rights": {
    "reference_authorized": true,
    "protected_elements_replaced": true,
    "human_reviewer": "required before generation"
  },
  "beats": [
    {
      "id": "B01",
      "source_evidence": ["F001", "F002"],
      "observable_evidence": "A bold opening composition changes quickly.",
      "inferred_attention_mechanism": "Pattern interrupt + result promise.",
      "original_adaptation": "Open with a new product-specific visual contradiction.",
      "must_not_copy": ["original actor", "original wording", "original music"],
      "image_prompt": "Original subject and scene only...",
      "video_prompt": "One readable action, one camera movement...",
      "sound_plan": "Original sound or licensed music; define entry and ending.",
      "continuity": {"character": "new", "product": "new", "palette": "brand-defined"},
      "qc": ["first-frame clarity", "protected elements absent", "action visible"]
    }
  ]
}
```

## Confidence labels

- `observed`: directly visible or audible in a timecoded source.
- `inferred`: plausible interpretation that needs reviewer confirmation.
- `unknown`: insufficient evidence; do not turn into a generation claim.
