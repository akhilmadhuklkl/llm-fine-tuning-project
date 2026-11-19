# Training improvement: assistant-only loss

The training loop now masks system and user tokens with `-100` in the labels. PyTorch ignores those positions when calculating causal-language-model loss, so the adapter is optimized only on the expected assistant JSON answer.

This prevents the small model from spending its limited update capacity learning to reproduce the prompt. The setting is enabled in `configs/training_exp001.yaml` as `assistant_only_loss: true`.

Validation on the first training example produced 73 masked prompt tokens and 183 trainable answer tokens within the 256-token limit. The next training run should use this setting and then be evaluated using the same held-out test set.
