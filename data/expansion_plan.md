# Dataset Expansion Plan

## Goal

Build a dataset large enough to support meaningful fine-tuning and evaluation while preserving the current safety and leakage controls.

## Target size

Target at least 150 examples before the first serious fine-tuning comparison:

- 10 examples for each of 12 core categories: 120 examples
- 30 known-category test examples
- 30 unseen-category or unseen-pattern test examples

The exact totals may overlap by source pool, but no evaluation example may appear in training data.

## Core categories

1. Database latency
2. Regional outage
3. Missing information
4. Security-sensitive event
5. Healthy system / no incident
6. Service degradation
7. Deployment failure
8. Queue backlog
9. Data integrity
10. Dependency timeout
11. Rate limiting
12. Monitoring false positive

## Variation requirements

Each category should include variations in:

- Wording and message length
- Severity signals
- Affected-service detail
- Time references
- Presence or absence of metrics
- Single-service and multi-service impact
- Correct escalation outcome
- Cases where the correct response is uncertainty

## Evaluation pools

### Known-category test set

Contains categories represented in training, but uses new wording, metrics, and incident combinations. This measures in-distribution performance.

### Unseen-pattern test set

Uses incident combinations, service relationships, and phrasing not copied into training. This measures generalization.

### Unseen-category test set

Uses a small number of categories withheld entirely from training. This measures broader transfer, but should not replace known-category testing.

## Quality gates

Every new example must pass:

1. JSON schema validation
2. Unique-ID validation
3. Secret and personal-data review
4. Fact-versus-hypothesis review
5. Safety review of recommended actions
6. Category and severity review
7. Duplicate and near-duplicate review
8. Split-leakage check

## Data creation order

1. Add five variations to each core category.
2. Review and validate the new examples.
3. Add a second five-example variation set.
4. Freeze the first evaluation pool.
5. Generate training-only variations.
6. Regenerate grouped splits.
7. Recalculate dataset statistics.
8. Run a human review sample before fine-tuning.

## Current status

The repository currently contains 19 synthetic examples. They are suitable for pipeline validation, but not for claiming model-quality improvement. Expansion should happen before the first real fine-tuning experiment.
