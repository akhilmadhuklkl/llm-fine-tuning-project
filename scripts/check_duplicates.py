"""Find exact and near-duplicate incident examples."""

from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", text.lower())).strip()


def user_text(record: dict) -> str:
    return " ".join(message["content"] for message in record["messages"] if message["role"] == "user")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_incidents.jsonl")
    parser.add_argument("--output", default="data/duplicate_report.md")
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()

    records = [json.loads(line) for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    normalized = {record["id"]: normalize(user_text(record)) for record in records}
    exact_groups: dict[str, list[str]] = {}
    for record_id, text in normalized.items():
        exact_groups.setdefault(text, []).append(record_id)
    exact_duplicates = [ids for ids in exact_groups.values() if len(ids) > 1]

    near_duplicates = []
    ids = list(normalized)
    for index, left_id in enumerate(ids):
        for right_id in ids[index + 1 :]:
            score = SequenceMatcher(None, normalized[left_id], normalized[right_id]).ratio()
            if score >= args.threshold and normalized[left_id] != normalized[right_id]:
                near_duplicates.append((left_id, right_id, score))

    lines = ["# Duplicate Report", "", f"Input: `{args.input}`", f"Near-duplicate threshold: **{args.threshold:.2f}**", ""]
    lines.append(f"- Exact duplicate groups: **{len(exact_duplicates)}**")
    lines.append(f"- Near-duplicate pairs: **{len(near_duplicates)}**")
    lines.extend(["", "## Exact duplicates", ""])
    lines.extend(f"- {', '.join(ids)}" for ids in exact_duplicates) or lines.append("- None")
    lines.extend(["", "## Near duplicates", ""])
    if near_duplicates:
        lines.extend(f"- `{left}` ↔ `{right}`: similarity `{score:.3f}`" for left, right, score in near_duplicates)
    else:
        lines.append("- None")
    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Exact duplicate groups: {len(exact_duplicates)}")
    print(f"Near-duplicate pairs: {len(near_duplicates)}")
    return 1 if exact_duplicates else 0


if __name__ == "__main__":
    raise SystemExit(main())
