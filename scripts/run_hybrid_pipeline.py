"""Run taxonomy normalization and both evaluation reports for model predictions."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions")
    parser.add_argument("prompts")
    parser.add_argument("--output-dir", default="evaluation/hybrid")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized = output_dir / "normalized_predictions.jsonl"
    metrics = output_dir / "metrics.json"
    format_report = output_dir / "format_report.json"
    safety_report = output_dir / "safety_report.json"
    run([sys.executable, "scripts/normalize_predictions.py", args.predictions, args.prompts, "--output", str(normalized)])
    run([sys.executable, "scripts/evaluate_predictions.py", str(normalized), "--references", args.prompts, "--output", str(metrics)])
    run([sys.executable, "scripts/check_prediction_format.py", str(normalized), "--output", str(format_report)])
    run([sys.executable, "scripts/check_safety_outputs.py", str(normalized), "--output", str(safety_report)])
    print(f"Hybrid evaluation written to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
