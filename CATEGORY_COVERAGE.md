# Evaluation category coverage

This review combines the frozen unseen sets and adversarial safety sets. The aggregate evidence requirements are met, but category depth is uneven.

| Category | Examples | Review status |
|---|---:|---|
| security_sensitive | 11 | Meets the practical 10-example target |
| data_integrity | 5 | Expand before high-confidence release |
| missing_information | 4 | Expand before high-confidence release |
| service_outage | 2 | Expand before high-confidence release |
| data_exposure | 1 | Expand before high-confidence release |
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

The project currently has 56 frozen unseen incidents and 20 adversarial safety incidents. The 44-example expanded unseen benchmark passes the structured-output, semantic, and safety thresholds, but the category-depth gaps above remain open for a high-confidence production review.

## Recommended next evidence increment

Add focused examples for data exposure, data integrity, missing information, and service outage. Keep them frozen and separate from training data, then rerun the same hybrid benchmark and safety gates before approving deployment.
