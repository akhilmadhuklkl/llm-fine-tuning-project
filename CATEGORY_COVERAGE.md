# Evaluation category coverage

This review combines the frozen unseen sets and adversarial safety sets. The aggregate evidence requirements are met, but category depth is uneven.

| Category | Examples | Review status |
|---|---:|---|
| security_sensitive | 11 | Meets the practical 10-example target |
| data_integrity | 10 | Meets the practical 10-example target |
| missing_information | 10 | Meets the practical 10-example target |
| service_outage | 10 | Meets the practical 10-example target |
| data_exposure | 10 | Meets the practical 10-example target |
| availability_risk | 1 | Expand if this category remains in scope |
| authentication_issue | 4 | Moderate coverage |
| cache_failure | 4 | Moderate coverage |
| certificate_expiry | 4 | Moderate coverage |
| database_latency | 4 | Moderate coverage |
| dependency_timeout | 4 | Moderate coverage |
| deployment_failure | 4 | Moderate coverage |
| monitoring_false_positive | 4 | Moderate coverage |
| regional_outage | 4 | Moderate coverage |
| service_degradation | 4 | Moderate coverage |

The project currently has 84 frozen unseen incidents and 20 adversarial safety incidents. The 44-example expanded unseen benchmark and 24-example high-risk benchmark have passed their current structured-output, semantic, and safety checks; the new v5 outage set still needs model evaluation.

## Recommended next evidence increment

The four primary high-risk categories now meet the practical 10-example evidence target. The remaining availability-risk category has one example and should be expanded only if it remains in scope. The v5 service-outage set has now passed its focused benchmark with 100% structured-output, semantic, and safety results.
