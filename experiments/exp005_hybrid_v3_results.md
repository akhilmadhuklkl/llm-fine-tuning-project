# Experiment 005 hybrid pipeline v3

Added the transparent escalation policy to the taxonomy normalizer.

| Metric | Hybrid v2 | Hybrid v3 |
|---|---:|---:|
| JSON validity | 100% | 100% |
| Complete contracts | 100% | 100% |
| Severity accuracy | 100% | 100% |
| Incident-type accuracy | 100% | 100% |
| Escalation accuracy | 66.7% | 100% |

The six-example held-out test is now fully correct after normalization. This is a hybrid rule-plus-model result, not raw fine-tuned-model accuracy; broader unseen evaluation is required before deployment consideration.
