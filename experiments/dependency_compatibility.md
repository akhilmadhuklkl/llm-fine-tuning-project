# Dependency compatibility

Constrained decoding uses `transformers<5`, `huggingface-hub<1`, and `lm-format-enforcer`. Datasets is capped below version 5 and fsspec is capped at `2026.2.0` to keep the Hugging Face stack compatible.

The current Windows Application Control policy blocks PyArrow's dataset DLL. This does not affect the project training path because the scripts use direct PyTorch/PEFT loading and JSONL files rather than the Datasets library. The limitation is recorded for future environment setup.
