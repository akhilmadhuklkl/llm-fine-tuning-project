# Transparent taxonomy normalization

Added an optional post-generation stage that maps explicit incident-text signals (`429`/quota, queue/throughput, duplicate/missing rows) to the project taxonomy and severity policy. It does not read reference categories, and it records `normalization: text_keyword_taxonomy_v1` on changed outputs.
