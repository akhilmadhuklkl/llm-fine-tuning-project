# Experiment 001: Resource-efficient validation run

The real SmolLM2 LoRA run completed with assistant-only loss and validation performed only at the final step.

| Step | Training loss | Validation loss |
|---:|---:|---:|
| 1 | 6.7322 | skipped |
| 2 | 6.8092 | skipped |
| 3 | 9.2511 | 6.0980 |

The adapter and `training_history.json` were saved locally under `models/smollm2-lora-exp001` (ignored by Git). Validation scheduling worked as intended and avoided repeated CPU validation passes. The run is still too short to establish quality improvement, but it provides a reproducible final validation measurement for the experiment.
