# Taxonomy normalization results

Applied `text_keyword_taxonomy_v1` to Experiment 005 outputs without reading the reference categories.

| Metric | Raw model | Normalized output |
|---|---:|---:|
| JSON validity | 100% | 100% |
| Complete contracts | 100% | 100% |
| Incident-type accuracy | 0% | 100% |
| Severity accuracy | 0% | 83.3% |
| Escalation accuracy | 66.7% | 66.7% |

This demonstrates that a small transparent rule stage can correct obvious taxonomy aliases, but it is not a replacement for a learned classifier. The rules must be expanded carefully and tested against edge cases before any deployment review.
