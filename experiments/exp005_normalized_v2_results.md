# Experiment 005 hybrid pipeline results

Experiment 005 raw model output was passed through the expanded transparent taxonomy normalizer and evaluated on the unchanged six-example test set.

| Metric | Raw model | Normalized v2 |
|---|---:|---:|
| JSON validity | 100% | 100% |
| Complete contracts | 100% | 100% |
| Severity accuracy | 0% | 100% |
| Incident-type accuracy | 0% | 100% |
| Escalation accuracy | 66.7% | 66.7% |

The hybrid pipeline now produces correct taxonomy and severity on this small test set. This result must not be described as raw fine-tuned-model accuracy: it includes a separately logged, input-text-based rule stage. Larger and unseen-test validation is still required.
