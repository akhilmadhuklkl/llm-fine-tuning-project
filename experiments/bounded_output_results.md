# Bounded output results

The constrained schema now limits each list to three items and each item to a bounded string length. The six-example Qwen test produced:

- JSON validity: 83.3% (5/6)
- Complete contracts: 83.3% (5/6)
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 16.7%

The format rate matched the 384-token unconstrained-length schema run, while reducing runaway text. One response remained invalid JSON. The model’s semantic accuracy is still insufficient for deployment review.
