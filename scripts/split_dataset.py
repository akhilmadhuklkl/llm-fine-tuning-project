"""Create deterministic train, validation, and test JSONL splits."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_incidents.jsonl")
    parser.add_argument("--output-dir", default="data/splits")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    records = [json.loads(line) for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    random.Random(args.seed).shuffle(records)

    test_count = max(1, round(len(records) * 0.2))
    validation_count = max(1, round(len(records) * 0.2))
    test = records[:test_count]
    validation = records[test_count : test_count + validation_count]
    train = records[test_count + validation_count :]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, split in (("train", train), ("validation", validation), ("test", test)):
        path = output_dir / f"{name}.jsonl"
        path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in split), encoding="utf-8")
        print(f"{name}: {len(split)} examples -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
