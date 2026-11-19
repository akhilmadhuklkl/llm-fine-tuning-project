# Experiment 004 results

## Model change

This experiment replaced SmolLM2-135M with `Qwen/Qwen2.5-0.5B-Instruct`, a 0.5B instruct model selected for stronger structured-output behavior while fitting the local 6 GB GPU.

## Training

- Device: RTX 3060 (`cuda:0`)
- LoRA trainable parameters: 540,672
- Validation loss at step 5: `3.8996`
- Validation loss at step 10: `2.0945`
- Validation loss at step 15: `1.7036`
- Validation loss at step 20: `1.5920`

## Held-out evaluation

- Coverage: 100%
- Valid JSON: 0%
- Complete output contracts: 0%
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 0%

Qwen produced more relevant troubleshooting responses than SmolLM2, but still generated prose rather than the required JSON. The next task should implement constrained JSON decoding or a post-generation contract strategy; further ordinary LoRA training is unlikely to solve formatting by itself.
