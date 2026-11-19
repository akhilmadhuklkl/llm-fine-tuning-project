# Local Smoke-Test Report

## Purpose

This is an infrastructure test only. It uses a randomly initialized local GPT-2-style model created by `scripts/create_tiny_model.py`; it is not a language-quality benchmark.

## Result

- Tiny model created successfully from the prepared dataset vocabulary
- One-step LoRA training completed on CPU
- Baseline inference completed on the test split
- Automated evaluator completed successfully
- Generated outputs were not valid JSON, which is expected from a random model

## Interpretation

The data preparation, tokenizer, inference, LoRA, and evaluation components are connected correctly. No quality conclusion should be drawn from the smoke-test metrics. The real baseline must be run with the selected pretrained SmolLM2 checkpoint once Hugging Face downloads are available.
