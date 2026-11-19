# Experiment 002 plan

Experiment 001 established that the pipeline works but three CPU steps do not improve the output contract. Experiment 002 is prepared as a 20-step run with assistant-only loss and validation every five steps.

It is intentionally not launched on the current CPU-only PyTorch environment. The observed SmolLM2 CPU runtime is approximately one minute per training step before validation overhead.

Acceptance criteria:

1. Training completes without errors.
2. `training_history.json` contains validation checkpoints at steps 5, 10, 15, and 20.
3. JSON parse rate improves over the Experiment 001 result of 0%.
4. Required-field coverage and semantic metrics are reported on the unchanged six-example test set.
5. The run is rejected if it introduces unsafe recommendations or secret exposure.
