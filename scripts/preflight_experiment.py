"""Check whether a real baseline or training experiment can start."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-config", default="configs/model.yaml")
    args = parser.parse_args()

    config = yaml.safe_load((ROOT / args.model_config).read_text(encoding="utf-8"))
    model_id = config["model_id"]
    checks = {
        "model_config": (ROOT / args.model_config).exists(),
        "prepared_train": (ROOT / "data/processed/train_chat.jsonl").exists(),
        "prepared_validation": (ROOT / "data/processed/validation_chat.jsonl").exists(),
        "prepared_test": (ROOT / "data/processed/test_chat.jsonl").exists(),
        "quality_gate": subprocess.run([sys.executable, "scripts/run_quality_gate.py"], cwd=ROOT).returncode == 0,
    }

    if "/" in model_id and not Path(model_id).exists():
        cache_root = Path.home() / ".cache" / "huggingface" / "hub"
        cache_name = "models--" + model_id.replace("/", "--")
        checks["model_cache"] = (cache_root / cache_name).exists()
    else:
        checks["local_model"] = Path(model_id).exists()

    print("\nExperiment preflight")
    print(f"Selected model: {model_id}")
    for name, passed in checks.items():
        print(f"- {name}: {'OK' if passed else 'BLOCKED'}")

    blocked = [name for name, passed in checks.items() if not passed]
    if blocked:
        print(f"\nExperiment blocked by: {', '.join(blocked)}")
        return 1
    print("\nExperiment preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
