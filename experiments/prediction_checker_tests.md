# Prediction checker regression test

Added an automated test covering both a valid incident-triage response and a response with missing contract fields. The test verifies that valid JSON is counted separately from complete contracts and that the failure reason is reported as `missing_fields`.
