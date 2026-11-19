# Failure Analysis Template

Use this template for every baseline or fine-tuning evaluation run.

## Run details

- Experiment:
- Model:
- Dataset version / commit:
- Evaluation date:
- Reviewer:

## Summary

- Total examples reviewed:
- Successful responses:
- Failed responses:
- Safety failures:
- Invalid JSON responses:
- Main failure pattern:

## Failure categories

| Category | Count | Notes |
|---|---:|---|
| Incorrect severity |  |  |
| Incorrect incident type |  |  |
| Missing observed facts |  |  |
| Facts presented as hypotheses |  |  |
| Unsupported hypothesis |  |  |
| Unsafe or destructive recommendation |  |  |
| Incorrect escalation decision |  |  |
| Invalid JSON or missing fields |  |  |
| Secret or private-data handling failure |  |  |
| Unclear or overly verbose response |  |  |

## Individual failure record

Copy this section once for each important failure.

### Failure: `<example-id>`

- Category:
- Severity: `low` / `medium` / `high` / `critical`
- Expected behavior:
- Actual behavior:
- Why it failed:
- Safety impact:
- Dataset issue, model issue, or evaluation issue:
- Proposed correction:
- New training example required: `yes` / `no`
- Retest required: `yes` / `no`

## Corrective-action rules

- Add a training example only when the desired behavior is clear and representative.
- Correct the dataset when the reference answer is wrong or inconsistent.
- Change the training configuration only when the data and evaluation are sound.
- Never hide failures by removing difficult test cases.
- Re-run the same held-out test set after each correction.
- Record whether a failure is fixed, unchanged, or newly introduced.

## Release recommendation

- [ ] Not ready for further experimentation
- [ ] Continue data improvement
- [ ] Run another smoke test
- [ ] Run a full fine-tuning experiment
- [ ] Ready for later deployment review
