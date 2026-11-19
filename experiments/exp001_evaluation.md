# Experiment 001: Baseline Comparison

## What was tested

The three-step LoRA adapter was evaluated on all six held-out test incidents. The same local SmolLM2-135M base model was used for the comparison, with deterministic generation and a maximum of 64 new tokens.

## Results

| Metric | Base baseline | LoRA adapter |
|---|---:|---:|
| Test coverage | 100% | 100% |
| Valid JSON responses | 0% | 0% |
| Required fields present | 0% | 0% |
| Severity accuracy | 0% | 0% |
| Incident-type accuracy | 0% | 0% |
| Escalation accuracy | 0% | 0% |

## Interpretation

The adapter ran successfully and produced responses for every test item, but this three-step run did not produce measurable task-quality improvement. Outputs were mostly refusal or generic troubleshooting text rather than the required incident-triage JSON structure. This is expected from an infrastructure-sized run and is not evidence that LoRA cannot improve the model.

The practical blocker is CPU time: a single training step takes about one minute on the current machine. A proper quality experiment should therefore be run in a scheduled or accelerated environment, with more steps, validation loss, and checkpoint comparison. For this resource-constrained local workflow, the next safe step is to improve prompt formatting and evaluation diagnostics before spending more CPU time.
