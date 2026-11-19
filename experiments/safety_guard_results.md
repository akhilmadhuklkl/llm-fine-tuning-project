# Safety guard results

The safety guard was rerun after adding healthy-system restraint and handling both `rollback` and `roll back` wording.

- JSON validity: 100%
- Complete contracts: 100%
- Severity accuracy: 83.3%
- Incident-type accuracy: 83.3%
- Escalation accuracy: 83.3%
- Unsafe raw actions replaced: secret exposure, alert suppression, destructive deletion, and unsupported rollback

The guard prevents the observed unsafe actions, but the safety set remains small and semantic accuracy is below a release threshold. More adversarial examples and manual review are still required.
