# Experiment 005 results

Experiment 005 added explicit incident taxonomy and severity guidance to the system instruction while keeping Qwen2.5-0.5B, LoRA settings, constrained decoding, and the 20-step GPU budget unchanged.

## Training

- Validation loss at step 5: `1.1735`
- Validation loss at step 10: `0.9497`
- Validation loss at step 15: `0.8520`
- Validation loss at step 20: `0.7936`

## Held-out evaluation

- Coverage: 100%
- Valid JSON: 100% (6/6)
- Complete contracts: 100% (6/6)
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 66.7%

This is a major format improvement over Experiment 004. The model now always produces a complete contract under constrained decoding, but it still invents incident labels such as `notification_queue`, `schema_change`, and `SERVICE_ERROR` instead of selecting the exact project taxonomy. The next task should focus on taxonomy classification, potentially as a separate classification stage before JSON generation.
