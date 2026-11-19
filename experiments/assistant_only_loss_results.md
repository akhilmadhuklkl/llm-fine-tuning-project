# Assistant-only loss rerun

## Run

- Base model: `HuggingFaceTB/SmolLM2-135M-Instruct`
- LoRA training steps: 3
- Device: CPU
- Loss masking: system and user tokens ignored; assistant answer tokens trained

Training losses were `6.7322`, `6.7924`, and `9.3658`. The adapter saved successfully.

## Evaluation

The updated adapter produced responses for all six test incidents, but metrics remained unchanged:

- Coverage: 100%
- Valid JSON: 0%
- Required field coverage: 0%
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 0%

The implementation change is correct and the training pipeline remains healthy, but three CPU steps are not enough to teach the model the target format. The next model-quality run should use more steps in an environment with practical acceleration or a smaller purpose-built model.
