# Hybrid pipeline runner

Run the complete post-generation workflow with:

```powershell
\.venv\Scripts\python.exe scripts\run_hybrid_pipeline.py evaluation/exp005_predictions.jsonl data/splits/test.jsonl
```

The command writes normalized predictions, semantic metrics, and format metrics under `evaluation/hybrid/`.
