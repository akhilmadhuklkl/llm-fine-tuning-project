# Experiment 003 plan

Experiment 003 uses the same data, model, LoRA settings, and 20-step GPU budget as Experiment 002. The only intentional change is an explicit output-contract system instruction listing the required JSON keys and value types.

Success criteria: improve JSON parse rate and complete-contract rate on the unchanged six-example test set without introducing unsafe recommendations.
