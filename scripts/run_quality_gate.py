"""Run every dataset quality check as one pre-training gate."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(command: list[str]) -> bool:
    print(f"\n>>> {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode == 0


def main() -> int:
    checks = [
        [PYTHON, "scripts/validate_dataset.py"],
        [PYTHON, "scripts/validate_dataset.py", "data/splits/train.jsonl"],
        [PYTHON, "scripts/validate_dataset.py", "data/splits/validation.jsonl"],
        [PYTHON, "scripts/validate_dataset.py", "data/splits/test.jsonl"],
        [PYTHON, "scripts/validate_chat_dataset.py"],
        [PYTHON, "scripts/check_duplicates.py"],
        [PYTHON, "scripts/check_sensitive_data.py"],
        [PYTHON, "scripts/check_quality_rules.py"],
    ]
    failures = [command for command in checks if not run(command)]
    if failures:
        print(f"\nQUALITY GATE FAILED: {len(failures)} check(s) failed.")
        return 1
    print("\nQUALITY GATE PASSED: all dataset checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
