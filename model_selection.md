# Base Model Selection

## Selected model

**Qwen/Qwen2.5-1.5B-Instruct**

Model page: <https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct>

## Why this model

The project needs a model that can follow instructions and produce reliable structured output for incident triage. Qwen2.5-1.5B-Instruct is the first checkpoint because its official model card describes improvements in instruction following, structured-data understanding, and JSON generation. The 1.5B size also keeps local experiments realistic for the available 6 GB GPU once CUDA-enabled PyTorch is configured.

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

Use Qwen2.5-1.5B-Instruct for the baseline and first fine-tuning experiment. Do not download or fine-tune the fallback unless the selected model fails a documented compatibility or quality check.
