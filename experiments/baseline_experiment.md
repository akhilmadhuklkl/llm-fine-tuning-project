# Baseline Experiment Checklist

## Experiment identity

- Experiment name: `baseline_smollm2_135m`
- Model: `HuggingFaceTB/SmolLM2-135M-Instruct`
- Purpose: measure untouched base-model behavior before fine-tuning
- Resource mode: CPU-safe, one prompt at a time, maximum 128 generated tokens

## Preflight

- [ ] Activate `.venv`
- [ ] Run `scripts/verify_environment.py`
- [ ] Run `scripts/run_quality_gate.py`
- [ ] Run `scripts/prepare_dataset.py`
- [ ] Confirm the model cache has enough free disk space
- [ ] Confirm no real secrets or personal data are present
- [ ] Generate an experiment manifest

## Execution

```powershell
\.venv\Scripts\python.exe scripts/run_baseline.py `
  --max-new-tokens 128 `
  --output evaluation/baseline_results.jsonl
```

## Expected outputs

- `evaluation/baseline_results.jsonl`
- `evaluation/metrics.json`
- A completed experiment manifest
- A human-review sample of the generated responses

## Evaluation

After baseline inference:

```powershell
\.venv\Scripts\python.exe scripts/evaluate_predictions.py `
  evaluation/baseline_results.jsonl `
  --references data/sample_incidents.jsonl
```

Review JSON validity, severity, incident type, escalation, safety, and communication quality.

## Acceptance criteria

The baseline experiment is complete when:

- Every test prompt has a response
- Results are saved with the model identifier
- Metrics are generated
- Human review is recorded
- Failures are categorized
- The experiment manifest identifies the exact dataset and configuration

## Current status

The scripts and checklist are ready. Execution is currently blocked because Hugging Face model-weight downloads stall before the SmolLM2 checkpoint is complete. The local random tiny-model smoke test is not a substitute for this baseline and must not be reported as model-quality evidence.
