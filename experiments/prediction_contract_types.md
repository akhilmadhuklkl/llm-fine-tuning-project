# Prediction contract type validation

The prediction checker now validates severity values, string-list fields, and the boolean escalation decision in addition to JSON parsing and required-field presence. This provides a complete contract check for future model outputs.

The current Experiment 001 outputs remain `invalid_json`, so no type-level findings were possible for that run.
