# Validation-loss tracking

The training loop now evaluates the adapter on `data/processed/validation_chat.jsonl` after each training step and saves `training_history.json` beside the adapter. Each history record contains the step number, training loss, and validation loss.

The change was verified with the local tiny-model smoke configuration:

```text
step=1 train_loss=5.0820 validation_loss=5.0402 device=cpu
```

This keeps the real SmolLM2 run unchanged in size while providing the signal needed to select checkpoints in a future longer run.
