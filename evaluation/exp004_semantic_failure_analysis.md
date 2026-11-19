# Experiment 004 semantic failure analysis

## Summary

- Test examples reviewed: 6
- Complete JSON contracts: 5
- Invalid JSON: 1 (`sample-014`)
- Severity accuracy: 0%
- Incident-type accuracy: 0%
- Escalation accuracy: 16.7% (1/6)
- Main semantic pattern: the model maps incidents to generic or invented labels instead of the dataset taxonomy

## Important failures

### `sample-013` and `sample-032`

The model recognized queue or delivery problems but produced `DELIVERY_DELAY` or free-form email labels instead of `queue_backlog`, and used the wrong severity. It also omitted or emptied important observed facts.

### `sample-014`

The output was structurally invalid because generation stopped before a complete JSON object. The content also used `Duplicate Order Records` instead of the required `data_integrity` taxonomy label.

### `sample-033`

The model identified schema/export context but used `schema_change` rather than `data_integrity` and incorrectly set escalation to false.

### `sample-018` and `sample-023`

The model failed to recognize the `rate_limit` taxonomy, using `normal` and `Partner Integration`, and produced incorrect escalation decisions.

## Conclusion

Constrained decoding solved much of the formatting problem, but semantic taxonomy alignment remains weak. The next data improvement should add explicit taxonomy demonstrations and severity/escalation contrast examples, while keeping the held-out test set unchanged.
