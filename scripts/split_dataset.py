"""Create deterministic category-grouped train, validation, and test splits."""

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
    grouped: dict[str, list[dict]] = {}
    for record in records:
        grouped.setdefault(record["category"], []).append(record)
    categories = list(grouped)
    random.Random(args.seed).shuffle(categories)

    test_category_count = max(1, round(len(categories) * 0.2))
    validation_category_count = max(1, round(len(categories) * 0.2))
    test_categories = set(categories[:test_category_count])
    validation_categories = set(categories[test_category_count : test_category_count + validation_category_count])
    test = [record for category in test_categories for record in grouped[category]]
    validation = [record for category in validation_categories for record in grouped[category]]
    train = [record for category in categories if category not in test_categories | validation_categories for record in grouped[category]]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, split in (("train", train), ("validation", validation), ("test", test)):
        path = output_dir / f"{name}.jsonl"
        path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in split), encoding="utf-8")
        split_categories = sorted({record["category"] for record in split})
        print(f"{name}: {len(split)} examples, categories={split_categories} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
