"""Convert incident records into chat fine-tuning JSONL files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SYSTEM_MESSAGE = (
    "You are an IT incident triage assistant. Return only valid JSON. "
    "Separate observed facts from hypotheses, recommend safe diagnostic steps, "
    "and escalate when information or authority is insufficient."
)


def prepare_record(record: dict) -> dict:
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    messages.extend(record["messages"])
    messages.append(
        {
            "role": "assistant",
            "content": json.dumps(record["expected_output"], ensure_ascii=False, separators=(",", ":")),
        }
    )
    return {"id": record["id"], "category": record["category"], "messages": messages}


def read_records(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/splits")
    parser.add_argument("--output-dir", default="data/processed")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for split in ("train", "validation", "test"):
        source = input_dir / f"{split}.jsonl"
        destination = output_dir / f"{split}_chat.jsonl"
        records = read_records(source)
        prepared = [prepare_record(record) for record in records]
        destination.write_text(
            "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in prepared),
            encoding="utf-8",
        )
        total += len(prepared)
        print(f"{split}: {len(prepared)} examples -> {destination}")
    print(f"Prepared {total} total chat examples.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
