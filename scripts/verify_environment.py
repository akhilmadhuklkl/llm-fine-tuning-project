"""Check the local environment required for the fine-tuning project."""

from __future__ import annotations

import importlib.util
import platform
import sys


REQUIRED_MODULES = {
    "torch": "PyTorch",
    "transformers": "Transformers",
    "datasets": "Datasets",
    "peft": "PEFT",
    "trl": "TRL",
    "accelerate": "Accelerate",
    "evaluate": "Evaluate",
    "pandas": "Pandas",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
}


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print("Packages:")

    missing = []
    for module, display_name in REQUIRED_MODULES.items():
        installed = importlib.util.find_spec(module) is not None
        status = "OK" if installed else "MISSING"
        print(f"  {display_name}: {status}")
        if not installed:
            missing.append(display_name)

    try:
        import torch

        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"CUDA build: {torch.version.cuda}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory // (1024**2)} MiB")
    except Exception as exc:  # pragma: no cover - diagnostic output
        print(f"PyTorch runtime check failed: {exc}")
        return 1

    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        return 1

    print("Environment verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
