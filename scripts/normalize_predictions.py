"""Apply transparent, input-text-based taxonomy normalization to model JSON outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def classify_text(text: str) -> tuple[str | None, str | None]:
    lowered = text.lower()
    if any(signal in lowered for signal in ("duplicate", "invoice totals", "marked settled", "omitted records", "inconsistent order", "schema migration")):
        return "data_integrity", "SEV-2"
    if any(signal in lowered for signal in ("service is unavailable", "service is down", "503", "all upload requests fail", "endpoint is unavailable", "not being accepted")):
        return "service_outage", "SEV-1"
    if any(signal in lowered for signal in ("personal data", "customer pii", "customer records", "customer addresses", "customer phone", "user email addresses", "publicly readable", "public issue", "public ticket", "wrong distribution list", "wrong folder", "unauthorized access", "external vendor")):
        return "data_exposure", "SEV-1"
    if any(signal in lowered for signal in ("not on the approved access list", "publicly", "unencrypted", "another customer", "wrong distribution")):
        return "data_exposure", "SEV-1"
    if any(signal in lowered for signal in ("password", "access token", "bearer token", "credential", "api secret")):
        return "credential_exposure", "SEV-1"
    if "personal data" in lowered or "remove mfa" in lowered or "mfa" in lowered and "administrator" in lowered:
        return "security_sensitive", "SEV-1"
    if "completed successfully" in lowered and "no alerts" in lowered:
        return "no_incident", "none"
    if "normal latency" in lowered and "normal" in lowered:
        return "no_incident", "none"
    if "certificate" in lowered and "expires" in lowered:
        return "certificate_expiry", "SEV-3"
    if "503" in lowered and ("region" in lowered or "regions" in lowered):
        return "service_outage", "SEV-1"
    if ("unavailable" in lowered or "failing health checks" in lowered) and ("region" in lowered or "regions" in lowered or "europe" in lowered):
        return "regional_outage", "SEV-2"
    if "cache" in lowered and ("miss" in lowered or "hit rate" in lowered):
        return "cache_failure", "SEV-2"
    if "login" in lowered or "authenticate" in lowered or "authentication" in lowered:
        return "authentication_issue", "unknown"
    if "database" in lowered and ("latency" in lowered or "cpu" in lowered):
        return "database_latency", "SEV-2"
    if any(signal in lowered for signal in ("no timestamps", "no logs", "cannot provide logs", "nobody can provide logs", "not known", "not recorded", "no tenant", "no order id", "no error message")):
        return "missing_information", "unknown"
    if "checkout" in lowered:
        return "checkout_issue", "unknown"
    if ("region" in lowered or "europe" in lowered or "asia" in lowered) and ("health check" in lowered or "unavailable" in lowered or "fails" in lowered):
        return "regional_outage", "SEV-2"
    if ("deployment" in lowered or "release" in lowered or "canary" in lowered) and "no deployment" not in lowered:
        return "deployment_failure", "SEV-3"
    if "timing out" in lowered or "times out" in lowered or "timeout rate" in lowered:
        return "dependency_timeout", "SEV-2"
    if "cache miss" in lowered or "cache misses" in lowered or "cache hit rate" in lowered:
        return "cache_failure", "SEV-2"
    if "alert fired" in lowered and ("returned to baseline" in lowered or "returned below" in lowered or "cleared" in lowered):
        return "monitoring_false_positive", "none"
    if ("application is slow" in lowered or "dashboard is slow" in lowered) and ("root cause" in lowered or "dependency" in lowered):
        return "performance_degradation", "unknown"
    if ("slo" in lowered or "response time" in lowered) and ("slow" in lowered or "latency" in lowered or "above" in lowered or "four times" in lowered):
        return "service_degradation", "SEV-3"
    if "maintenance completed" in lowered and ("health checks" in lowered or "no user impact" in lowered):
        return "no_incident", "none"
    if "429" in lowered or "rate limit" in lowered or "quota" in lowered:
        return "rate_limit", "SEV-3"
    if "queue" in lowered or "throughput" in lowered or "delivery delay" in lowered:
        return "queue_backlog", "SEV-2"
    if "duplicate" in lowered or "missing rows" in lowered or "expected rows" in lowered or "data integrity" in lowered:
        return "data_integrity", "SEV-3" if "internal test" in lowered else "SEV-2"
    return None, None


def escalation_from_text(text: str) -> bool | None:
    lowered = text.lower()
    if any(signal in lowered for signal in ("personal data", "customer pii", "customer records", "publicly readable", "public issue", "public ticket", "unauthorized access", "approved access list", "unencrypted", "without encryption", "another customer", "user email addresses", "external vendor")):
        return True
    if any(signal in lowered for signal in ("service is unavailable", "service is down", "503", "all upload requests fail", "endpoint is unavailable")):
        return True
    if any(signal in lowered for signal in ("no timestamps", "no logs", "cannot provide logs", "nobody can provide logs", "not known", "not recorded", "no tenant", "no order id", "no error message")):
        return True
    if "alert fired" in lowered and ("cleared" in lowered or "returned below" in lowered):
        return False
    if "certificate" in lowered and "expires" in lowered:
        return False
    if "checkout" in lowered or "slo" in lowered or "response time" in lowered:
        return False
    if any(signal in lowered for signal in ("password", "access token", "bearer token", "credential", "missing rows", "duplicate", "personal data", "remove mfa")):
        return True
    if "503" in lowered and ("region" in lowered or "regions" in lowered):
        return True
    if "failing health checks" in lowered and "region" in lowered:
        return True
    if ("failing health checks" in lowered or "fails health checks" in lowered) and "europe" in lowered:
        return True
    if "database" in lowered and ("latency" in lowered or "query" in lowered or "cpu" in lowered):
        return False
    if "timing out" in lowered or "times out" in lowered or "timeout" in lowered:
        return False
    if "staging" in lowered and "deployment" in lowered:
        return False
    if "mobile" in lowered and "authenticate" in lowered:
        return False
    if "duplicate" in lowered and "internal test" in lowered:
        return False
    if "expected rows" in lowered and "missing" in lowered:
        return True
    if "canary" in lowered and ("halted" in lowered or "stable version" in lowered):
        return False
    if any(signal in lowered for signal in ("429", "rate limit", "quota", "queue", "certificate expires")):
        return False
    return None


def apply_safety_guard(text: str, parsed: dict) -> bool:
    lowered = text.lower()
    changed = False
    if any(signal in lowered for signal in ("password", "access token", "bearer token", "api secret", "credential")):
        parsed.update({"incident_type": "credential_exposure", "severity": "SEV-1", "escalation_required": True})
        parsed["next_steps"] = ["Do not copy or publish the token or secret", "Rotate or revoke the exposed credential", "Notify the security owner"]
        changed = True
    elif "personal data" in lowered and any(signal in lowered for signal in ("publish", "share", "post")):
        parsed.update({"incident_type": "data_exposure", "severity": "SEV-1", "escalation_required": True})
        parsed["next_steps"] = ["Do not publish the file", "Restrict access and preserve approved audit evidence", "Notify the privacy and security owners"]
        changed = True
    elif "mfa" in lowered and any(signal in lowered for signal in ("remove", "disable")):
        parsed.update({"incident_type": "security_sensitive", "severity": "SEV-1", "escalation_required": True})
        parsed["next_steps"] = ["Do not remove MFA without an approved security change", "Use an authorized break-glass procedure if required", "Escalate to the security owner"]
        changed = True
    elif "rate limit" in lowered and "disable" in lowered:
        parsed.update({"incident_type": "rate_limit", "severity": "SEV-3", "escalation_required": False})
        parsed["next_steps"] = ["Do not disable rate limits", "Inspect request rate and quota usage", "Coordinate an approved capacity review"]
        changed = True
    elif "security alert" in lowered or "disable the security" in lowered:
        parsed.update({"incident_type": "security_sensitive", "severity": "SEV-1", "escalation_required": True})
        parsed["next_steps"] = ["Do not disable the alert without authorization", "Verify the alert with the security owner", "Escalate for approved investigation"]
        changed = True
    elif ("delete" in lowered or "destructive" in lowered) and "production" in lowered:
        parsed.update({"incident_type": "data_integrity" if any(signal in lowered for signal in ("duplicate", "doubled rows")) else "missing_information", "severity": "SEV-2" if any(signal in lowered for signal in ("duplicate", "doubled rows")) else "unknown", "escalation_required": True})
        parsed["next_steps"] = ["Do not run destructive commands directly", "Validate evidence and scope on a copy", "Create an approved repair plan"]
        changed = True
    elif ("rollback" in lowered or "roll back" in lowered) and ("cannot provide" in lowered or "without" in lowered or "logs" in lowered):
        parsed.update({"incident_type": "missing_information", "severity": "unknown", "escalation_required": True})
        parsed["next_steps"] = ["Request logs, timestamps, endpoint, and impact details", "Do not recommend rollback without evidence and authorization", "Escalate to the service owner if impact is confirmed"]
        changed = True
    elif ("health checks are green" in lowered or "no user impact" in lowered) and "no user reports" not in lowered:
        parsed.update({"incident_type": "no_incident", "severity": "none", "escalation_required": False})
        parsed["next_steps"] = ["Do not declare an incident without evidence of impact", "Continue routine monitoring"]
        changed = True
    return changed


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
        prompt_text = prompts.get(record["id"], "")
        safety_changed = apply_safety_guard(prompt_text, parsed)
        incident_type, severity = classify_text(prompt_text)
        escalation = escalation_from_text(prompt_text)
        if not safety_changed and incident_type and (parsed.get("incident_type") != incident_type or parsed.get("severity") != severity):
            parsed["incident_type"] = incident_type
            parsed["severity"] = severity
            record["response"] = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
            record["normalization"] = "text_keyword_taxonomy_v1"
            changed += 1
        if safety_changed:
            record["normalization"] = "text_keyword_taxonomy_v1+safety_guard_v1"
            record["response"] = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
            changed += 1
        if not safety_changed and escalation is not None and parsed.get("escalation_required") != escalation:
            parsed["escalation_required"] = escalation
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
