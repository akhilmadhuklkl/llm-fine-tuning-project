# Experiment Manifests

Experiment manifests record the exact inputs and environment for each baseline or training run.

Generate one from the project root with:

```powershell
\.venv\Scripts\python.exe scripts/create_experiment_manifest.py --name experiment_001
```

Manifests should be committed with the code or configuration change that produced the experiment.
