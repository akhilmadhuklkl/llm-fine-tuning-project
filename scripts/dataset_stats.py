"""Generate model-independent statistics for the incident dataset."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bullets(counter: Counter[str]) -> str:
    return "\n".join(f"- `{key}`: {value}" for key, value in sorted(counter.items())) or "- None"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/sample_incidents.jsonl")
    parser.add_argument("--split-dir", default="data/splits")
    parser.add_argument("--output", default="data/dataset_stats.md")
    args = parser.parse_args()

    records = load_jsonl(Path(args.dataset))
    categories = Counter(record["category"] for record in records)
    severities = Counter(record["expected_output"]["severity"] for record in records)
    incident_types = Counter(record["expected_output"]["incident_type"] for record in records)
    escalations = Counter(record["expected_output"]["escalation_required"] for record in records)
    user_lengths = [len(message["content"]) for record in records for message in record["messages"] if message["role"] == "user"]
    assistant_lengths = [len(json.dumps(record["expected_output"])) for record in records]

    split_counts = {}
    for split in ("train", "validation", "test"):
        split_counts[split] = len(load_jsonl(Path(args.split_dir) / f"{split}.jsonl"))

    report = f"""# Dataset Statistics

Generated from `{args.dataset}`.

## Overview

- Total examples: **{len(records)}**
- Unique IDs: **{len({record['id'] for record in records})}**
- Average user-message characters: **{sum(user_lengths) / len(user_lengths):.1f}**
- Maximum user-message characters: **{max(user_lengths)}**
- Average target JSON characters: **{sum(assistant_lengths) / len(assistant_lengths):.1f}**

## Split sizes

{bullets(Counter(split_counts))}

## Categories

{bullets(categories)}

## Severity distribution

{bullets(severities)}

## Incident types

{bullets(incident_types)}

## Escalation labels

{bullets(Counter({str(key): value for key, value in escalations.items()}))}

## Interpretation

The dataset is intentionally small and synthetic. Category coverage is broad but not yet balanced enough for a production-quality fine-tuning claim. The statistics should be regenerated after every dataset change.
"""
    output = Path(args.output)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote statistics report to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
