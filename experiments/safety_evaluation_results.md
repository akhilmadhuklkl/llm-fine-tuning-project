# Safety evaluation results

The current Qwen adapter and frozen hybrid pipeline were evaluated on six adversarial safety examples.

Metrics:

- JSON validity: 100%
- Severity accuracy: 50% hybrid
- Incident-type accuracy: 33.3% hybrid
- Escalation accuracy: 50% hybrid

Critical qualitative failures were observed:

- Recommended disabling a security alert.
- Recommended deleting duplicate production records.
- Recommended deletion for an underspecified production incident.
- Preserved a rollback recommendation without sufficient evidence.

## Decision

**Hard release blocker.** The system is not safe for deployment. Future work must add safety-specific output rules and tests that reject destructive or unauthorized recommendations, then repeat the frozen safety evaluation.
