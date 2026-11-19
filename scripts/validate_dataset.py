"""Validate JSONL incident examples against the project schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", default="data/sample_incidents.jsonl", nargs="?")
    parser.add_argument("--schema", default="data/dataset_schema.json")
    args = parser.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    records = []
    errors = []
    for line_number, line in enumerate(Path(args.dataset).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            records.append(record)
            errors.extend((line_number, error.message) for error in validator.iter_errors(record))
        except json.JSONDecodeError as exc:
            errors.append((line_number, f"invalid JSON: {exc.msg}"))

    ids = [record.get("id") for record in records]
    if len(ids) != len(set(ids)):
        errors.append((0, "duplicate example IDs found"))

    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for line_number, message in errors:
            prefix = f"line {line_number}: " if line_number else ""
            print(f"- {prefix}{message}")
        return 1

    print(f"Validated {len(records)} incident example(s) successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
