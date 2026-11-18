# Development Environment

## Verified host

The initial environment check was performed on 18 November 2026.

- Python: 3.14.4
- Git: 2.56.0
- Docker: 29.5.2
- GPU: NVIDIA GeForce RTX 3060 Laptop GPU
- GPU memory: 6144 MiB
- NVIDIA driver: 592.00

The project virtual environment currently has a CPU-only PyTorch wheel (`2.15.0+cpu`). The NVIDIA GPU is visible to the operating system, but PyTorch reports `CUDA available: False`. This is acceptable for data preparation and code validation; before full fine-tuning, we should install and verify a CUDA-enabled PyTorch build or use cloud GPU compute.

On 18 November 2026, an attempted installation of the official Windows CUDA 12.8 wheel (`torch==2.11.0`) stalled while downloading its approximately 2.7 GB package. The CPU environment remains intact. Retry this download only when a stable connection and sufficient disk space are available.

## Setup

Create and activate a virtual environment from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify the environment:

```powershell
python scripts/verify_environment.py
```

## Hardware note

The 6 GB GPU is suitable for small experiments and parameter-efficient fine-tuning with LoRA or QLoRA. Large-model training may require reduced sequence length, gradient accumulation, quantization, or cloud compute.
