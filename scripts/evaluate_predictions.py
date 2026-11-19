"""Evaluate JSON predictions against the incident reference outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "severity",
    "incident_type",
    "observed_facts",
    "hypotheses",
    "next_steps",
    "escalation_required",
}


def load_jsonl(path: Path) -> dict[str, dict]:
    records = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            records[record["id"]] = record
    return records


def parse_response(response: str) -> dict | None:
    try:
        parsed = json.loads(response)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", help="JSONL with id and response fields")
    parser.add_argument("--references", default="data/sample_incidents.jsonl")
    parser.add_argument("--output", default="evaluation/metrics.json")
    args = parser.parse_args()

    references = load_jsonl(Path(args.references))
    predictions = load_jsonl(Path(args.predictions))
    total = len(references)
    evaluated = 0
    valid_json = 0
    required_fields = 0
    severity_correct = 0
    type_correct = 0
    escalation_correct = 0

    for example_id, reference in references.items():
        prediction_record = predictions.get(example_id)
        if not prediction_record:
            continue
        evaluated += 1
        prediction = parse_response(prediction_record.get("response", ""))
        if prediction is None:
            continue
        valid_json += 1
        expected = reference["expected_output"]
        if REQUIRED_FIELDS.issubset(prediction):
            required_fields += 1
        severity_correct += prediction.get("severity") == expected.get("severity")
        type_correct += prediction.get("incident_type") == expected.get("incident_type")
        escalation_correct += prediction.get("escalation_required") == expected.get("escalation_required")

    denominator = evaluated or 1
    metrics = {
        "total_references": total,
        "evaluated": evaluated,
        "coverage": evaluated / total if total else 0.0,
        "json_validity": valid_json / denominator,
        "required_field_coverage": required_fields / denominator,
        "severity_accuracy": severity_correct / denominator,
        "incident_type_accuracy": type_correct / denominator,
        "escalation_accuracy": escalation_correct / denominator,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return 0 if evaluated else 1


if __name__ == "__main__":
    raise SystemExit(main())
