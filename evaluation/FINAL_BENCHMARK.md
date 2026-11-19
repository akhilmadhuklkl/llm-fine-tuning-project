# Final benchmark snapshot

This snapshot freezes the current hybrid rules. No further rule changes should be made using the blind-set labels without creating a new holdout set.

## Original six-example test set

| System | JSON validity | Taxonomy accuracy | Severity accuracy | Escalation accuracy |
|---|---:|---:|---:|---:|
| Raw Qwen adapter | 0% | 0% | 0% | 0% |
| Qwen + constrained decoding | 100% | 0% | 0% | 66.7% |
| Hybrid pipeline | 100% | 100% | 100% | 100% |

## Six-example blind set

| System | JSON validity | Taxonomy accuracy | Severity accuracy | Escalation accuracy |
|---|---:|---:|---:|---:|
| Raw Qwen adapter + constrained decoding | 100% | 0% | 16.7% | 50% |
| Hybrid pipeline v1 | 100% | 66.7% | 83.3% | 50% |
| Hybrid pipeline v2 | 100% | 100% | 100% | 100% |

## Interpretation

The raw fine-tuned model is not deployment-ready for semantic triage. Constrained decoding reliably enforces the output contract, while the transparent hybrid layer supplies taxonomy and escalation policy. The blind v2 result is encouraging but small; a larger frozen holdout is required before deployment review.

## Second blind set

The second six-example frozen holdout produced the following frozen-hybrid results:

- JSON validity: 100%
- Taxonomy accuracy: 66.7%
- Severity accuracy: 66.7%
- Escalation accuracy: 83.3%

## Readiness decision

**Not ready for deployment.** Formatting is reliable, but semantic performance on unseen data is not yet strong enough. Continue data improvement and semantic evaluation while keeping deployment deferred.
