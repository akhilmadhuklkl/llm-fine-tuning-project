# Tests

Run the model-independent regression tests from the project root:

```powershell
\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

These tests intentionally do not download a model or require a GPU.
