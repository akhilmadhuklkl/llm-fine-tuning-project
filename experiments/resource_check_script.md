# Reproducible resource check

Run this before training:

```powershell
\.venv\Scripts\python.exe scripts/check_training_resources.py
```

The script reports the active Python/PyTorch versions, CUDA availability, device count, and GPU memory when available. The current environment reports CPU-only PyTorch, so the longer Experiment 002 remains deferred.
