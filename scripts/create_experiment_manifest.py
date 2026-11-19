"""Create a reproducibility manifest for an experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, cwd=Path.cwd()).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--output-dir", default="experiments")
    parser.add_argument("--model-config", default="configs/model.yaml")
    parser.add_argument("--training-config", default="configs/training.yaml")
    args = parser.parse_args()

    files = [
        "data/sample_incidents.jsonl",
        "data/splits/train.jsonl",
        "data/splits/validation.jsonl",
        "data/splits/test.jsonl",
        args.model_config,
        args.training_config,
    ]
    manifest = {
        "experiment": args.name,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_value("rev-parse", "HEAD"),
        "git_branch": git_value("branch", "--show-current"),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "files": {path: {"sha256": sha256(Path(path)), "bytes": Path(path).stat().st_size} for path in files},
        "model_config": yaml.safe_load(Path(args.model_config).read_text(encoding="utf-8")),
        "training_config": yaml.safe_load(Path(args.training_config).read_text(encoding="utf-8")),
    }
    output = Path(args.output_dir) / f"{args.name}.yaml"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    print(f"Wrote experiment manifest to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
