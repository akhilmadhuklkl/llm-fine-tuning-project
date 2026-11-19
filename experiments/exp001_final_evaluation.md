# Experiment 001: Final adapter evaluation

The latest three-step adapter was evaluated against all six held-out test incidents using deterministic generation with a 64-token output limit.

Results:

- Coverage: 100%
- Valid JSON: 0%
- Required field coverage: 0%
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 0%

The adapter produces responses for every test item, but they remain generic refusals or free-form troubleshooting text. The run therefore confirms evaluation reproducibility and full test coverage, but not task-quality improvement. The next quality-focused run requires substantially more optimization steps or a better-suited base model, which should be performed in an accelerated environment to preserve the user's resource constraints.
