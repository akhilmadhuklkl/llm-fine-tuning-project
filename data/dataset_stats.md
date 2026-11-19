# Dataset Statistics

Generated from `data/sample_incidents.jsonl`.

## Overview

- Total examples: **33**
- Unique IDs: **33**
- Average user-message characters: **120.1**
- Maximum user-message characters: **171**
- Average target JSON characters: **492.5**

## Split sizes

- `test`: 6
- `train`: 21
- `validation`: 6

## Categories

- `cache_failure`: 2
- `certificate_expiry`: 2
- `data_integrity`: 2
- `database_latency`: 3
- `dependency_timeout`: 2
- `deployment_failure`: 2
- `healthy_system`: 3
- `missing_information`: 3
- `monitoring_false_positive`: 2
- `queue_backlog`: 2
- `rate_limit`: 2
- `regional_outage`: 3
- `security_sensitive`: 3
- `service_degradation`: 2

## Severity distribution

- `SEV-1`: 4
- `SEV-2`: 12
- `SEV-3`: 9
- `none`: 5
- `unknown`: 3

## Incident types

- `authentication_issue`: 1
- `cache_failure`: 2
- `certificate_expiry`: 2
- `checkout_issue`: 1
- `credential_exposure`: 3
- `data_integrity`: 2
- `database_latency`: 3
- `dependency_timeout`: 2
- `deployment_failure`: 2
- `monitoring_false_positive`: 2
- `no_incident`: 3
- `performance_degradation`: 1
- `queue_backlog`: 2
- `rate_limit`: 2
- `regional_outage`: 2
- `service_degradation`: 2
- `service_outage`: 1

## Escalation labels

- `False`: 22
- `True`: 11

## Interpretation

The dataset is intentionally small and synthetic. Category coverage is broad but not yet balanced enough for a production-quality fine-tuning claim. The statistics should be regenerated after every dataset change.
