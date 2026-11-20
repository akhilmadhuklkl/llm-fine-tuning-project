# Project audit

Audit status: **quality-gate benchmark passed; pre-deployment review remains; deployment is deferred.**

- Regression tests: 18 total, with focused safety/normalization tests passing
- Unified quality gate: passed
- Dataset: 33 examples; 21 train, 6 validation, 6 test
- Duplicate findings: 0 exact groups, 0 near-duplicate pairs
- Sensitive-data findings: 0
- Local model and prepared data: available
- Experiment 002: completed on GPU; validation loss improved to 2.1089
- Experiment 005: completed on GPU; JSON contract reached 100% with constrained decoding
- Hybrid pipeline: 100% JSON, taxonomy, severity, and escalation accuracy on the six-example test set
- Adversarial safety evidence: 20 frozen examples; the latest six-example safety run reached 100% semantic metrics with zero unsafe-action findings
- Aggregate unseen benchmark: 84 incidents; 100% JSON and contract completeness, 92.9% severity, 92.9% taxonomy, 97.6% escalation, and zero unsafe-action findings
- Raw model semantic accuracy: remains weak and is reported separately
- GPU training: enabled through CUDA PyTorch on RTX 3060
- Deployment: intentionally deferred

The next substantive stage is final QA and deployment-package approval. Combined frozen unseen evidence is 84 incidents and adversarial evidence is 20 incidents. Deployment remains deferred.
