# Experiment 001: Short LoRA Training Run

## Purpose

Verify that the selected minimum-resource model can complete a short supervised LoRA training run on the local CPU environment.

## Configuration

- Base model: `HuggingFaceTB/SmolLM2-135M-Instruct`
- Training data: `data/processed/train_chat.jsonl`
- Validation data: `data/processed/validation_chat.jsonl`
- Training steps: 3
- Batch size: 1
- Gradient accumulation: 1
- Learning rate: 0.0002
- LoRA rank: 4
- LoRA alpha: 8
- LoRA dropout: 0.05
- Maximum sequence length: 256 tokens
- Device: CPU

## Observed run

| Step | Loss |
|---:|---:|
| 1 | 6.0425 |
| 2 | 6.2554 |
| 3 | 7.8650 |

## Result

**Completed successfully.** The adapter was saved to the ignored local directory `models/smollm2-lora-exp001`.

This is an infrastructure smoke experiment, not a quality result. Three steps are too few to judge whether the model learned the incident-triage task; the increasing loss also shows that a longer, controlled experiment is needed before drawing conclusions. The run confirms that the data loader, tokenizer, LoRA attachment, CPU training loop, and adapter save process work together within the chosen resource budget.

## Next experiment

Run a longer training experiment with evaluation checkpoints and compare its predictions against the base-model baseline using the evaluation rubric.
