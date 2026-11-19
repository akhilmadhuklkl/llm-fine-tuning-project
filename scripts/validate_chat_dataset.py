"""Validate generated chat-format JSONL files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(path: Path) -> tuple[int, list[str]]:
    errors = []
    count = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            record = json.loads(line)
            messages = record["messages"]
            roles = [message["role"] for message in messages]
            if roles[0] != "system" or roles[-1] != "assistant":
                errors.append(f"line {line_number}: conversation must start with system and end with assistant")
            if not any(role == "user" for role in roles):
                errors.append(f"line {line_number}: conversation has no user message")
            json.loads(messages[-1]["content"])
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"line {line_number}: {exc}")
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/processed")
    args = parser.parse_args()

    total = 0
    errors = []
    for split in ("train", "validation", "test"):
        path = Path(args.input_dir) / f"{split}_chat.jsonl"
        count, split_errors = validate(path)
        total += count
        errors.extend(f"{split}: {error}" for error in split_errors)
        print(f"{split}: {count} chat examples")

    if errors:
        print("Chat validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Validated {total} prepared chat examples successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
