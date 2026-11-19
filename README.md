# LLM Fine-Tuning Project

An AI engineering project for fine-tuning an open-source language model for a real-world task.

## Project status

Core local workflow is complete through baseline evaluation, LoRA smoke experiments, failure analysis, reproducibility checks, and resource safeguards. Deployment is intentionally deferred to a later stage.

Current status:

- Model: local `HuggingFaceTB/SmolLM2-135M-Instruct` checkpoint
- Dataset: 33 validated incident examples with grouped train/validation/test splits
- Quality gate: passed; 10 regression tests currently pass
- Experiment 001: completed; three-step CPU run did not improve JSON output quality
- Experiment 002: configured and preflighted, but deferred because PyTorch is CPU-only
- Deployment: deferred

## Planned workflow

1. Define the use case and success criteria
2. Select a suitable open-source base model
3. Create, clean, and validate the training dataset
4. Establish a baseline with the original model
5. Fine-tune with supervised fine-tuning and LoRA/QLoRA
6. Evaluate, analyze failures, and iterate
7. Package the final checkpoint and documentation
8. Deploy later as a separate stage

## Repository structure

```text
data/          Datasets and dataset documentation
configs/       Training and experiment configuration
scripts/       Reproducible data, training, and evaluation scripts
models/        Local model artifacts (ignored by Git)
evaluation/    Evaluation results and reports
notebooks/     Exploratory analysis notebooks
```

## Notes

- Do not commit model weights, secrets, private customer data, or raw credentials.
- Each completed project task will be committed and pushed with a focused commit message.

## Useful commands

```powershell
\.venv\Scripts\python.exe scripts\run_quality_gate.py
\.venv\Scripts\python.exe -m unittest discover -s tests -v
\.venv\Scripts\python.exe scripts\check_training_resources.py
\.venv\Scripts\python.exe scripts\preflight_experiment.py --model-config configs/model_local.yaml
```

The longer run is protected by a CPU safety guard. Do not set `allow_slow_cpu: true` unless the resource cost is explicitly accepted.
