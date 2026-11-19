# Experiment 001 Failure Analysis

## Run details

- Experiment: `exp001`
- Model: `HuggingFaceTB/SmolLM2-135M-Instruct` with LoRA
- Dataset: six held-out test incidents from the grouped test split
- Evaluation date: 2026-11-19
- Reviewer: project owner / AI Engineering workflow

## Summary

- Total examples reviewed: 6
- Successful responses: 0
- Failed responses: 6
- Safety failures: 0 observed
- Invalid JSON responses: 6
- Main failure pattern: generic refusal or unrelated free-form answer instead of the required incident-triage JSON

## Failure categories

| Category | Count | Notes |
|---|---:|---|
| Incorrect severity | 6 | Cannot evaluate because no response contained the required structure |
| Incorrect incident type | 6 | Cannot evaluate for the same reason |
| Missing observed facts | 6 | Required structured field absent |
| Facts presented as hypotheses | 0 | No structured facts were produced |
| Unsupported hypothesis | 0 | No structured hypotheses were produced |
| Unsafe or destructive recommendation | 0 | No dangerous action observed |
| Incorrect escalation decision | 6 | Required field absent |
| Invalid JSON or missing fields | 6 | Primary failure |
| Secret or private-data handling failure | 0 | No secret exposure observed |
| Unclear or overly verbose response | 6 | Refusals or truncated generic prose |

## Root cause assessment

The base model is too weakly aligned with this specialized task for a three-step CPU LoRA run. It appears to retain generic assistant behavior and does not reliably follow the system instruction to emit JSON. The training data and evaluator agree on the required schema, so this is primarily a model/training-duration issue rather than a test-set issue.

## Corrective actions

1. Keep the held-out test set unchanged.
2. Add a small format-focused validation check that reports JSON parse rate separately from field accuracy.
3. Run a longer experiment only in an accelerated or otherwise isolated environment.
4. Compare against a stronger small instruct model if resource limits permit.
5. Require valid JSON and required-field coverage before considering semantic accuracy.

## Release recommendation

- [x] Not ready for deployment review
- [x] Continue data and model improvement
- [x] Run another smoke test after the next controlled change
- [ ] Run a full fine-tuning experiment locally on CPU
- [ ] Ready for later deployment review
