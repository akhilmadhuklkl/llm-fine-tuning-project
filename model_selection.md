# Base Model Selection

## Selected model

**Qwen/Qwen2.5-0.5B-Instruct**

Model page: <https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct>

## Why this model

The project needs a model that can follow instructions and produce structured output for incident triage while keeping local resource use low. Qwen2.5-0.5B-Instruct is the minimum practical starting checkpoint: it is substantially smaller than the 1.5B variant while retaining instruction-tuning and the Qwen2.5 family’s structured-output capabilities.

## License

The model card lists the model under the Apache 2.0 license. We will still preserve the license and model-card information in project documentation and verify the license again before any production or commercial use.

## Known constraints

- The current PyTorch installation is CPU-only, so local model loading and training will be slow until CUDA support is configured.
- A 1.5B model is appropriate for learning the fine-tuning workflow, but it will not have the capabilities of larger production models.
- The model may produce invalid JSON or unsafe operational suggestions; validation and human review are required.
- The model should not be connected to live infrastructure or allowed to execute commands in this project stage.

## Fallback candidate

**HuggingFaceTB/SmolLM2-1.7B-Instruct** is retained as a fallback. Its official model card lists Apache 2.0 licensing and describes it as a compact model suitable for lightweight use. It may be useful for comparison if Qwen has compatibility or memory issues.

Model page: <https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct>

## Decision

Use Qwen2.5-0.5B-Instruct for the baseline and first fine-tuning experiment. Do not download the 1.5B model or the fallback unless the selected model fails a documented compatibility or quality check.
