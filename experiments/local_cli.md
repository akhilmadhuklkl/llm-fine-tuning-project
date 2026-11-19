# Local CLI interface

Run one incident locally:

```powershell
\.venv\Scripts\python.exe scripts\triage_incident.py "The public API returns HTTP 429 for one client."
```

The CLI performs constrained generation, taxonomy normalization, safety normalization, and a final unsafe-action check. It does not deploy or expose an API endpoint.
