"""Scan incident examples for common sensitive-data patterns."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone": re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{7,}\d)(?!\d)"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "secret_assignment": re.compile(r"\b(?:api[_ -]?key|token|password|secret)\s*[:=]\s*\S+", re.I),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_incidents.jsonl")
    parser.add_argument("--output", default="data/sensitive_data_report.md")
    args = parser.parse_args()

    findings = []
    for line_number, line in enumerate(Path(args.input).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        text = json.dumps(record, ensure_ascii=False)
        for pattern_name, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append((record["id"], line_number, pattern_name))

    lines = ["# Sensitive-Data Scan", "", f"Input: `{args.input}`", ""]
    lines.append(f"- Findings: **{len(findings)}**")
    lines.append("")
    if findings:
        lines.append("## Findings")
        lines.append("")
        lines.extend(f"- `{record_id}` (line {line_number}): `{pattern_name}`" for record_id, line_number, pattern_name in findings)
    else:
        lines.extend(["## Findings", "", "- None detected by the configured patterns."])
    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Sensitive-data findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
