"""Run semantic quality checks on incident targets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_incidents.jsonl")
    parser.add_argument("--output", default="data/quality_rules_report.md")
    args = parser.parse_args()

    findings = []
    for line_number, line in enumerate(Path(args.input).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        target = record["expected_output"]
        category = record["category"]
        record_id = record["id"]
        prefix = f"{record_id} (line {line_number})"

        if not target["next_steps"]:
            findings.append(f"{prefix}: next_steps is empty")
        if target["escalation_required"] and not target["next_steps"]:
            findings.append(f"{prefix}: escalation requires at least one next step")
        if target["severity"] == "unknown" and not target["escalation_required"]:
            findings.append(f"{prefix}: unknown severity should require escalation")
        if category == "healthy_system":
            if target["severity"] != "none" or target["incident_type"] != "no_incident" or target["escalation_required"]:
                findings.append(f"{prefix}: healthy_system target is inconsistent")
        if category == "security_sensitive":
            if target["severity"] != "SEV-1" or not target["escalation_required"]:
                findings.append(f"{prefix}: security-sensitive target should be SEV-1 and escalated")

        facts = {norm(item) for item in target["observed_facts"]}
        hypotheses = {norm(item) for item in target["hypotheses"]}
        overlap = facts & hypotheses
        if overlap:
            findings.append(f"{prefix}: fact/hypothesis overlap: {sorted(overlap)}")

    lines = ["# Semantic Quality Rules Report", "", f"Input: `{args.input}`", "", f"- Findings: **{len(findings)}**", ""]
    if findings:
        lines.extend(["## Findings", "", *[f"- {finding}" for finding in findings]])
    else:
        lines.extend(["## Findings", "", "- None detected by the configured rules."])
    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Semantic quality findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
