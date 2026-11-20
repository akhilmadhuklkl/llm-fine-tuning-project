# Deployment package

Status: **prepared; deployment deferred**

This document defines what would be shipped later. It does not start a hosted service
or publish the model.

## Included application pieces

- LoRA adapter: `models/qwen2.5-0.5b-lora-exp005`
- Base model configuration: `configs/model_qwen_local.yaml`
- Local inference CLI: `scripts/triage_incident.py`
- Custom browser UI and local API server: `ui/` and `scripts/serve_ui.py`
- Frozen evaluation evidence: `evaluation/`
- Regression tests: `tests/`
- Environment specification: `requirements.txt` and `.env.example`

## Local startup contract

```powershell
python scripts\serve_ui.py --host 127.0.0.1 --port 8501
```

The service should remain bound to localhost during local testing. A later hosted
deployment must add authentication, HTTPS, request logging, rate limiting, and an
explicit model-loading strategy.

## Resource policy

- Use the smallest approved model and the existing LoRA adapter.
- Keep generation bounded by the CLI/UI token limit.
- Prefer one model process per machine.
- Do not include training caches, virtual environments, or temporary outputs in an image.
- Keep deployment GPU/CPU limits explicit and stop idle replicas where possible.

## Required release gates before deployment

- Recreate the environment from a clean lock or pinned dependency set.
- Install and verify training-only packages (`trl` and `evaluate`) if retraining is part of
  the release process.
- Run the full regression and frozen benchmark suites.
- Confirm JSON validity, contract completeness, semantic thresholds, and safety gates.
- Perform a security review of inputs, logs, model files, and exposed endpoints.
- Add authentication, HTTPS, rate limiting, health checks, and rollback instructions.
- Define monitoring for latency, errors, malformed outputs, safety blocks, and GPU memory.

## Current approval decision

The package is documented and the local application is ready for demonstration. Hosting,
public serving, and deployment approval remain deferred by project decision.
