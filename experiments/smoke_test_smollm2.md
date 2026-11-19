# SmolLM2 LoRA Smoke Test

## Configuration

- Model: `HuggingFaceTB/SmolLM2-135M-Instruct`
- Local checkpoint: `models/smollm2-135m`
- Dataset: 21 prepared training examples
- Sequence length: 256
- Batch size: 1
- Gradient accumulation: 1
- Training steps: 1
- LoRA rank: 4
- LoRA alpha: 8
- Device: CPU

## Result

- Trainable parameters: 460,800
- Total parameters: 134,975,808
- Trainable percentage: 0.3414%
- Step 1 loss: 6.0425
- Status: Passed

## Interpretation

The real pretrained checkpoint loads correctly, the LoRA adapter attaches to the target modules, the prepared dataset is consumable, and one training step completes. This validates the training path. It is not yet a meaningful quality experiment because the run used only one step.
