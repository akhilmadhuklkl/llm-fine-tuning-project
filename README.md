# LLM Fine-Tuning Project

An AI engineering project for fine-tuning an open-source language model for a real-world task.

## Project status

Core local workflow is complete through Qwen LoRA fine-tuning, constrained generation, hybrid normalization, safety evaluation, aggregate benchmarking, and resource safeguards. Deployment is intentionally deferred to a later stage.

Current status:

- Model: local Qwen2.5-0.5B-Instruct with the `exp005` LoRA adapter
- Dataset: 33 validated training examples plus 84 frozen unseen evaluation incidents
- Safety evidence: 20 adversarial incidents with zero unsafe-action findings
- Aggregate benchmark: 100% JSON and contract completeness, 92.9% severity, 92.9% taxonomy, 97.6% escalation
- Regression suite: 18 tests passing
- Runtime: CUDA-enabled PyTorch on the RTX 3060; large CPU jobs are guarded
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
\.venv\Scripts\python.exe scripts\run_hybrid_pipeline.py evaluation/exp005_predictions.jsonl data/splits/test.jsonl
python scripts\triage_incident.py "The partner API is returning HTTP 429 responses for one client."
python scripts\serve_ui.py
```

The longer run is protected by a CPU safety guard. Do not set `allow_slow_cpu: true` unless the resource cost is explicitly accepted.

The custom browser UI is served locally at `http://127.0.0.1:8501` by `scripts/serve_ui.py`. It calls the same CLI pipeline and keeps all incident text local. Streamlit is not required for the primary UI.

## Evaluation interpretation

Raw fine-tuned-model evaluation and hybrid-pipeline evaluation are reported separately. The hybrid pipeline adds explicitly logged taxonomy, escalation, and safety rules after generation; its stronger metrics must not be presented as raw model accuracy. Deployment remains deferred until a deployment package and serving/monitoring plan are approved.
