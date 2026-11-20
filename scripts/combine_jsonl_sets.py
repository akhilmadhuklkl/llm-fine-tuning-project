"""Combine ordered JSONL prediction or prompt sets for aggregate evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    records = []
    seen = set()
    for input_path in args.inputs:
        for line in Path(input_path).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if record["id"] in seen:
                raise ValueError(f"Duplicate record id: {record['id']}")
            seen.add(record["id"])
            records.append(record)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")
    print(f"Combined {len(records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
