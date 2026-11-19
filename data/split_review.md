# Split Review

## Current design

The splitter assigns complete incident categories to one split. This prevents examples from the same category appearing in both training and evaluation, making the test set a measure of generalization to unseen incident types.

Current result:

| Split | Examples | Categories |
|---|---:|---:|
| Training | 13 | 8 |
| Validation | 3 | 3 |
| Test | 3 | 3 |

There is no category overlap between any two splits.

## Assessment

The grouped design is appropriate for leakage prevention, but the current dataset is too small for reliable model-quality conclusions:

- Validation has only three examples.
- Test has only three examples.
- Every test category has one example, so one response can change the percentage by roughly 33 percentage points.
- Some categories have only one example and cannot measure within-category variation.
- The test categories are unseen during training, so this evaluates generalization to new categories rather than normal performance on known categories.

## Decision

Keep the grouped split for the current engineering phase because it is safer and makes leakage visible. Do not treat its metrics as production-quality evidence.

Before a meaningful fine-tuning comparison, expand the dataset to at least:

- 10 examples per category for categories used in evaluation
- 30 or more test examples overall
- Multiple wording variations for each incident pattern
- A separate known-category test set for in-distribution performance
- An unseen-category test set for generalization performance

The future evaluation should report both test types instead of combining them into one score.
