# Research proposals

Each brief covers the question, close prior work, candidate contribution, case, metrics,
budget, risks, and criteria to continue or discard it. No experimental proposal is selected.

## Candidate cases

The following Markdown specifications support case selection. They contain fictional
examples, three complexity levels, proposed EDA, and evaluation boundaries. No case has
been implemented or selected as the thesis contribution.

Both case specifications have complete Spanish reading versions:
[case-0001](case-0001-code-repair-harness.es.md) and
[case-0002](case-0002-service-workflow-harness.es.md).
English remains primary. This scoped language exception covers these two cases.
Each translation shares the source identity, revision, status, and evidence boundaries;
its `translation_of` metadata avoids a duplicate catalog record. Keep paired content and
diagrams synchronized in the same PR. It does not establish translations for all documents.

| Case | Proposed focus | Main feasibility tradeoff |
|---|---|---|
| [case-0001: Code repair harness](case-0001-code-repair-harness.md) | Feedback selection within a bounded coding repair loop | A small local setup, but task and test quality need careful control |
| [case-0002: Simulated service workflow harness](case-0002-service-workflow-harness.md) | Recovery from ambiguous tool outcomes in cancellations and simulated refunds | Explicit state-based evaluation, with additional simulator and policy design |

Start by comparing objective evaluation, data availability, total cost, reproducibility,
and relevance to harness construction. Complexity levels describe proposed conditions;
their actual difficulty requires baseline evidence. The game alternative remains in
[research options](../synthesis/research-options.md); this pair does not close case selection.

Case specifications remain here. Future tasks and evaluators belong in `benchmarks/`,
dataset metadata in `data/`, and protocols, manifests, and findings in `experiments/`.
Each implementation should link to its case specification rather than duplicate it.
