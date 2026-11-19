# Resource-aware validation

Validation is now controlled by `eval_every_n_steps`. The real CPU experiment evaluates at its final step (`3`), avoiding repeated full validation passes that would multiply runtime. The tiny smoke configuration evaluates every step so the feature itself remains covered by a fast test.

The tiny test completed successfully and saved training history with a final validation loss of `5.0396`.
