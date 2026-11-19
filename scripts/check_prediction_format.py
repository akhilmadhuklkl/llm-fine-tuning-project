"""Check generated incident-triage predictions for JSON contract compliance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "severity",
    "incident_type",
    "affected_services",
    "observed_facts",
    "hypotheses",
    "next_steps",
    "escalation_required",
}
SEVERITIES = {"SEV-0", "SEV-1", "SEV-2", "SEV-3", "none", "unknown"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", help="JSONL containing id and response fields")
    parser.add_argument("--output", default="evaluation/prediction_format_report.json")
    args = parser.parse_args()

    records = [
        json.loads(line)
        for line in Path(args.predictions).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    valid_json = 0
    complete = 0
    failures = []
    for record in records:
        response = record.get("response", "")
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            failures.append({"id": record.get("id"), "reason": "invalid_json"})
            continue
        valid_json += 1
        if not isinstance(parsed, dict):
            failures.append({"id": record.get("id"), "reason": "json_not_object"})
            continue
        missing = sorted(REQUIRED_FIELDS - set(parsed))
        if missing:
            failures.append({"id": record.get("id"), "reason": "missing_fields", "fields": missing})
            continue
        type_errors = []
        if parsed["severity"] not in SEVERITIES:
            type_errors.append("invalid_severity")
        for field in ("affected_services", "observed_facts", "hypotheses", "next_steps"):
            if not isinstance(parsed[field], list) or not all(isinstance(item, str) for item in parsed[field]):
                type_errors.append(f"invalid_{field}")
        if not isinstance(parsed["escalation_required"], bool):
            type_errors.append("invalid_escalation_required")
        if type_errors:
            failures.append({"id": record.get("id"), "reason": "invalid_types", "fields": type_errors})
        else:
            complete += 1

    total = len(records)
    report = {
        "total_predictions": total,
        "valid_json": valid_json,
        "json_parse_rate": valid_json / total if total else 0.0,
        "complete_contracts": complete,
        "complete_contract_rate": complete / total if total else 0.0,
        "failures": failures,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
