# Constrained JSON decoding

Added an optional `--constrain-json` mode to `scripts/run_baseline.py`. It uses a JSON schema to constrain generation to the required incident-triage object and its seven fields. The mode is optional so unconstrained baseline results remain comparable.
