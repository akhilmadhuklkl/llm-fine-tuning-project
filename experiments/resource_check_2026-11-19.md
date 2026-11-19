# Training resource check

The machine has an NVIDIA GeForce RTX 3060 Laptop GPU with 6 GB memory. The project environment was updated to a CUDA-enabled PyTorch build:

- PyTorch: `2.11.0+cu128`
- CUDA available to PyTorch: `true`
- CUDA version: `12.8`
- CUDA device count: `1`
- GPU tensor smoke test: passed
- Installed GPU driver: `592.00`

The blocker is resolved. Experiment 002 can now be run on the GPU with the existing CPU safety guard permitting long training when CUDA is available.
