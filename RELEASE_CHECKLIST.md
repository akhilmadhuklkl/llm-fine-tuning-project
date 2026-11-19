# Release checklist

- [x] Dataset schema and quality gate pass
- [x] Training and validation splits are separated
- [x] Raw model baseline recorded
- [x] LoRA experiments recorded
- [x] GPU environment verified
- [x] JSON-constrained generation implemented
- [x] Hybrid taxonomy and escalation stage documented
- [x] Local incident-triage CLI implemented
- [x] CLI safety-output gate integrated
- [x] Blind evaluation sets created and frozen
- [x] Raw and hybrid metrics separated
- [ ] Semantic accuracy meets release threshold on unseen data
- [x] Safety guard review passed on 20 frozen adversarial examples with zero unsafe-action findings
- [ ] Quality gates in `QUALITY_GATES.md` pass with required evidence size
- [ ] Deployment package approved

Current decision: **continue evidence collection; deployment deferred**. Safety behavior passes the current 20-case adversarial suite, but broader unseen-data evidence is still required.
