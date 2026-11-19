# Constrained decoding with 384-token budget

Using the Qwen2.5-0.5B LoRA adapter and the tightened incident JSON schema:

- Test coverage: 100%
- Valid JSON: 83.3% (5/6)
- Complete contracts: 83.3% (5/6)
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 33.3%

Increasing the generation budget from 192 to 384 tokens raised valid and complete contract rates from 50% to 83.3%. One response still truncated because the model generated an excessively long `next_steps` value. The next task should shorten output targets or impose bounded array/text lengths while preserving the schema.
