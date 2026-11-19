"""Evaluate the transparent taxonomy classifier against reference labels offline."""

from __future__ import annotations

import json
from pathlib import Path

from normalize_predictions import classify_text


def main() -> int:
    records = [
        json.loads(line)
        for line in Path("data/sample_incidents.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    recognized = 0
    correct = 0
    failures = []
    for record in records:
        text = " ".join(message["content"] for message in record["messages"])
        predicted, severity = classify_text(text)
        expected = record["expected_output"]
        if predicted:
            recognized += 1
        if predicted != expected["incident_type"] or severity != expected["severity"]:
            failures.append({"id": record["id"], "predicted": predicted, "expected": expected["incident_type"]})
        else:
            correct += 1
    report = {
        "total": len(records),
        "recognized": recognized,
        "coverage": recognized / len(records),
        "exact_taxonomy_and_severity": correct,
        "accuracy": correct / len(records),
        "failures": failures,
    }
    output = Path("data/taxonomy_rule_report.json")
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
