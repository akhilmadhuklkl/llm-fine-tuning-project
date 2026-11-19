# Experiment 002 results

## Training

- Model: `HuggingFaceTB/SmolLM2-135M-Instruct`
- Device: NVIDIA RTX 3060 Laptop GPU (`cuda:0`)
- Steps: 20
- Assistant-only loss: enabled
- Validation interval: every 5 steps

| Step | Training loss | Validation loss |
|---:|---:|---:|
| 5 | 8.1941 | 5.7892 |
| 10 | 5.5232 | 4.4929 |
| 15 | 3.1303 | 2.9409 |
| 20 | 1.9100 | 2.1089 |

Validation loss improved consistently, indicating that the adapter learned from the training data.

## Held-out evaluation

- Coverage: 100%
- Valid JSON: 0%
- Complete output contracts: 0%
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 0%

The longer GPU run improved loss substantially but did not yet produce the required JSON format on the six-example test set. This indicates that lower language-model loss alone is not sufficient for task success; the next iteration should focus on stronger format learning or constrained decoding while preserving the unchanged test set.
