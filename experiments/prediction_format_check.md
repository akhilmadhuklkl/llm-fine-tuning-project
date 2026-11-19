# Prediction format check

Added `scripts/check_prediction_format.py` to measure JSON parse rate and complete contract rate independently from semantic accuracy. It checks the seven required incident-triage fields and records per-example failure reasons.

Applied to the final Experiment 001 predictions:

- Predictions: 6
- Valid JSON: 0 (0%)
- Complete contracts: 0 (0%)
- Failure reason for every example: `invalid_json`

This diagnostic will make future improvements visible even before severity or incident-type accuracy changes.
