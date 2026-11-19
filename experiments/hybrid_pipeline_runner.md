# Hybrid pipeline runner

Run the complete post-generation workflow with:

```powershell
\.venv\Scripts\python.exe scripts\run_hybrid_pipeline.py evaluation/exp005_predictions.jsonl data/splits/test.jsonl
```

The command writes normalized predictions, semantic metrics, format metrics, and a safety report under `evaluation/hybrid/`. It exits nonzero if direct unsafe actions are found.
