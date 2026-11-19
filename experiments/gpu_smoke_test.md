# GPU smoke test

After replacing CPU-only PyTorch with the CUDA-enabled project-local build, the tiny LoRA training configuration completed on the GPU:

- PyTorch: `2.11.0+cu128`
- Device: `cuda`
- GPU: NVIDIA GeForce RTX 3060 Laptop GPU
- Training loss: `5.0904`
- Validation loss: `5.0397`
- Regression tests after the change: 10 passed

The environment is now ready for the guarded Experiment 002 run.
