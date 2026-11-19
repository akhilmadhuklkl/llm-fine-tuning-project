# Project audit

Audit status: **ready for the next accelerated experiment; deployment remains deferred.**

- Regression tests: 10 passed
- Unified quality gate: passed
- Dataset: 33 examples; 21 train, 6 validation, 6 test
- Duplicate findings: 0 exact groups, 0 near-duplicate pairs
- Sensitive-data findings: 0
- Local model and prepared data: available
- Experiment 002: completed on GPU; validation loss improved to 2.1089
- Experiment 005: completed on GPU; JSON contract reached 100% with constrained decoding
- Hybrid pipeline: 100% JSON, taxonomy, severity, and escalation accuracy on the six-example test set
- Raw model semantic accuracy: remains weak and is reported separately
- GPU training: enabled through CUDA PyTorch on RTX 3060
- Deployment: intentionally deferred

The repository is clean and all current safeguards are passing. The next substantive stage is broader unseen-data validation and deployment review; deployment itself remains deferred.
