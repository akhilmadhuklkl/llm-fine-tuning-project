# Bounded output schema

The constrained decoder now limits each output list to at most three strings and limits string lengths while preserving every observed test reference. This reduces runaway explanations and leaves enough generation budget to close the JSON object.
