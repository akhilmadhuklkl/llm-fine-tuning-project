# Dataset Statistics

Generated from `data/sample_incidents.jsonl`.

## Overview

- Total examples: **19**
- Unique IDs: **19**
- Average user-message characters: **117.3**
- Maximum user-message characters: **171**
- Average target JSON characters: **484.0**

## Split sizes

- `test`: 4
- `train`: 11
- `validation`: 4

## Categories

- `cache_failure`: 1
- `certificate_expiry`: 1
- `data_integrity`: 1
- `database_latency`: 2
- `dependency_timeout`: 1
- `deployment_failure`: 1
- `healthy_system`: 2
- `missing_information`: 2
- `monitoring_false_positive`: 1
- `queue_backlog`: 1
- `rate_limit`: 1
- `regional_outage`: 2
- `security_sensitive`: 2
- `service_degradation`: 1

## Severity distribution

- `SEV-1`: 3
- `SEV-2`: 6
- `SEV-3`: 5
- `none`: 3
- `unknown`: 2

## Incident types

- `authentication_issue`: 1
- `cache_failure`: 1
- `certificate_expiry`: 1
- `credential_exposure`: 2
- `data_integrity`: 1
- `database_latency`: 2
- `dependency_timeout`: 1
- `deployment_failure`: 1
- `monitoring_false_positive`: 1
- `no_incident`: 2
- `performance_degradation`: 1
- `queue_backlog`: 1
- `rate_limit`: 1
- `regional_outage`: 1
- `service_degradation`: 1
- `service_outage`: 1

## Escalation labels

- `False`: 12
- `True`: 7

## Interpretation

The dataset is intentionally small and synthetic. Category coverage is broad but not yet balanced enough for a production-quality fine-tuning claim. The statistics should be regenerated after every dataset change.
