# Dataset Card

## Purpose

This is a small synthetic dataset for training and evaluating an IT incident triage assistant. It is designed for pipeline development, not production use.

## Current contents

- 19 examples
- Incident reports paired with structured JSON targets
- Categories covering outages, degradation, dependencies, data integrity, security, operations, and non-incidents
- Sanitized fictional service names only

## Quality controls

- Every record has a unique ID
- Every record is validated against `data/dataset_schema.json`
- Observed facts and hypotheses are stored separately
- Security-sensitive cases explicitly test redaction and escalation
- Healthy-system cases test whether the assistant avoids opening unnecessary incidents
- Train, validation, and test splits are generated with a fixed seed

## Limitations

- The dataset is too small for a reliable quality claim
- Examples are synthetic and may not represent real incident language
- Category balance is still approximate
- Reference answers represent a fictional operational policy
- Human review is still required before using the data for serious training experiments

## Expansion plan

Before full fine-tuning, expand each category with varied wording, incomplete reports, conflicting signals, and realistic but sanitized timelines. Keep a held-out test set that is not copied into training examples.
