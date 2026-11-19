# Taxonomy normalizer idempotence

The regression suite now runs normalization twice and verifies byte-for-byte identical output. This prevents repeated pipeline execution from causing further semantic changes.
