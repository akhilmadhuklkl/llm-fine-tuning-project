"""Apply transparent, input-text-based taxonomy normalization to model JSON outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def classify_text(text: str) -> tuple[str | None, str | None]:
    lowered = text.lower()
    if "password" in lowered or "access token" in lowered or "credential" in lowered:
        return "credential_exposure", "SEV-1"
    if "completed successfully" in lowered and "no alerts" in lowered:
        return "no_incident", "none"
    if "normal latency" in lowered and "normal" in lowered:
        return "no_incident", "none"
    if "certificate" in lowered and "expires" in lowered:
        return "certificate_expiry", "SEV-3"
    if "503" in lowered and ("region" in lowered or "regions" in lowered):
        return "service_outage", "SEV-1"
    if ("unavailable" in lowered or "failing health checks" in lowered) and ("region" in lowered or "regions" in lowered):
        return "regional_outage", "SEV-2"
    if "login" in lowered or "authentication" in lowered:
        return "authentication_issue", "unknown"
    if "database" in lowered and ("latency" in lowered or "cpu" in lowered):
        return "database_latency", "SEV-2"
    if "checkout" in lowered:
        return "checkout_issue", "unknown"
    if ("deployment" in lowered or "release" in lowered or "canary" in lowered) and "no deployment" not in lowered:
        return "deployment_failure", "SEV-3"
    if "timing out" in lowered or "timeout rate" in lowered:
        return "dependency_timeout", "SEV-2"
    if "cache miss" in lowered or "cache misses" in lowered or "cache hit rate" in lowered:
        return "cache_failure", "SEV-2"
    if "alert fired" in lowered and ("returned to baseline" in lowered or "returned below" in lowered):
        return "monitoring_false_positive", "none"
    if "application is slow" in lowered and "root cause" in lowered:
        return "performance_degradation", "unknown"
    if ("slo" in lowered or "response time" in lowered) and ("slow" in lowered or "latency" in lowered or "above" in lowered or "four times" in lowered):
        return "service_degradation", "SEV-3"
    if "maintenance completed" in lowered and ("health checks" in lowered or "no user impact" in lowered):
        return "no_incident", "none"
    if "429" in lowered or "rate limit" in lowered or "quota" in lowered:
        return "rate_limit", "SEV-3"
    if "queue" in lowered or "throughput" in lowered or "delivery delay" in lowered:
        return "queue_backlog", "SEV-2"
    if "duplicate" in lowered or "missing rows" in lowered or "data integrity" in lowered:
        return "data_integrity", "SEV-3" if "internal test" in lowered else "SEV-2"
    return None, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions")
    parser.add_argument("prompts")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    prompts = {
        record["id"]: " ".join(message["content"] for message in record["messages"])
        for record in (json.loads(line) for line in Path(args.prompts).read_text(encoding="utf-8").splitlines())
        if record.get("messages")
    }
    changed = 0
    output_records = []
    for line in Path(args.predictions).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        try:
            parsed = json.loads(record["response"])
        except json.JSONDecodeError:
            output_records.append(record)
            continue
        incident_type, severity = classify_text(prompts.get(record["id"], ""))
        if incident_type and (parsed.get("incident_type") != incident_type or parsed.get("severity") != severity):
            parsed["incident_type"] = incident_type
            parsed["severity"] = severity
            record["response"] = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
            record["normalization"] = "text_keyword_taxonomy_v1"
            changed += 1
        output_records.append(record)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in output_records), encoding="utf-8")
    print(f"Normalized records: {changed}/{len(output_records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
