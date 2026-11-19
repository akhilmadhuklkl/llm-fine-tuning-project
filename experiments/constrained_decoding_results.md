# Constrained decoding results

The Qwen2.5-0.5B LoRA adapter was evaluated with JSON-schema-constrained decoding. The first schema allowed arbitrary severity strings and produced 66.7% parseable JSON, but invalid severity values prevented complete contracts. The schema was then tightened to the project severity enum.

The final bounded run produced six clean JSONL records after the evaluator was corrected to ignore blank lines:

- JSON validity: 50% (3/6)
- Complete contracts: 50% (3/6)
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 33.3%

This is a clear formatting improvement over 0% unconstrained validity, but truncation still causes three invalid responses at the 192-token generation budget.
