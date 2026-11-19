# Experiment 003 results

## Change from Experiment 002

The system instruction explicitly listed the seven required JSON keys and their value types. Training used the same 20-step GPU budget, LoRA configuration, dataset, and unchanged test split.

## Training

- Device: RTX 3060 (`cuda:0`)
- Validation loss at step 5: `2.5080`
- Validation loss at step 10: `2.4782`
- Validation loss at step 15: `2.4413`
- Validation loss at step 20: `2.3986`

## Held-out evaluation

- Coverage: 100%
- Valid JSON: 0%
- Complete output contracts: 0%
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 0%

The explicit schema instruction lowered training and validation loss relative to the first steps, but did not change the held-out output contract metrics. The 135M model continues to produce generic refusals and free-form text. Further training of this model is not justified without a different output strategy or stronger base model.
