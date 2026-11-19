# Training resource check

The machine has an NVIDIA GeForce RTX 3060 Laptop GPU with 6 GB memory, but the active Python environment uses CPU-only PyTorch:

- PyTorch: `2.15.0+cpu`
- CUDA available to PyTorch: `false`
- CUDA device count: `0`
- Installed GPU driver: `592.00`

The GPU is visible to the operating system but unavailable to the current training environment. Experiment 002 remains deferred rather than running a 20-step CPU job that would consume excessive time and resources.
