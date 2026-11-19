# Frozen blind evaluation v2 results

The current Qwen adapter and frozen hybrid pipeline were evaluated on six additional unseen examples without changing the rules.

| Metric | Raw constrained model | Frozen hybrid |
|---|---:|---:|
| JSON validity | 100% | 100% |
| Complete contracts | 100% | 100% |
| Severity accuracy | 16.7% | 66.7% |
| Incident-type accuracy | 0% | 66.7% |
| Escalation accuracy | 66.7% | 83.3% |

The hybrid pipeline improves all semantic dimensions, but the unseen result is below deployment-ready standards. The main remaining work is broader data coverage and improved semantic classification, not deployment.
