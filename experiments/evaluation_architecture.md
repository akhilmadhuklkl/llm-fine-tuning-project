# Evaluation architecture

The project reports three layers separately:

1. Raw unconstrained model output
2. Model output with JSON-schema-constrained decoding
3. Hybrid output after transparent taxonomy and escalation normalization

This separation preserves honest attribution of improvements and keeps the held-out test set unchanged.
