# Dataset Statistics

Generated from `data/sample_incidents.jsonl`.

## Overview

- Total examples: **24**
- Unique IDs: **24**
- Average user-message characters: **120.1**
- Maximum user-message characters: **171**
- Average target JSON characters: **488.5**

## Split sizes

- `test`: 4
- `train`: 15
- `validation`: 5

## Categories

- `cache_failure`: 2
- `certificate_expiry`: 2
- `data_integrity`: 1
- `database_latency`: 2
- `dependency_timeout`: 2
- `deployment_failure`: 1
- `healthy_system`: 2
- `missing_information`: 2
- `monitoring_false_positive`: 2
- `queue_backlog`: 1
- `rate_limit`: 2
- `regional_outage`: 2
- `security_sensitive`: 2
- `service_degradation`: 1

## Severity distribution

- `SEV-1`: 3
- `SEV-2`: 8
- `SEV-3`: 7
- `none`: 4
- `unknown`: 2

## Incident types

- `authentication_issue`: 1
- `cache_failure`: 2
- `certificate_expiry`: 2
- `credential_exposure`: 2
- `data_integrity`: 1
- `database_latency`: 2
- `dependency_timeout`: 2
- `deployment_failure`: 1
- `monitoring_false_positive`: 2
- `no_incident`: 2
- `performance_degradation`: 1
- `queue_backlog`: 1
- `rate_limit`: 2
- `regional_outage`: 1
- `service_degradation`: 1
- `service_outage`: 1

## Escalation labels

- `False`: 17
- `True`: 7

## Interpretation

The dataset is intentionally small and synthetic. Category coverage is broad but not yet balanced enough for a production-quality fine-tuning claim. The statistics should be regenerated after every dataset change.
