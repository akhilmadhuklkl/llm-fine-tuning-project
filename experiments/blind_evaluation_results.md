# Blind evaluation results

Experiment 005 was evaluated on six records that were not used for training or rule development.

| Metric | Raw constrained model | Hybrid pipeline |
|---|---:|---:|
| JSON validity | 100% | 100% |
| Complete contracts | 100% | 100% |
| Severity accuracy | 16.7% | 83.3% |
| Incident-type accuracy | 0% | 66.7% |
| Escalation accuracy | 50% | 50% |

The hybrid rules generalized partially but did not reproduce the perfect six-example test-set result. This is useful evidence against overclaiming readiness. More unseen examples and improved escalation handling are required before deployment review.
