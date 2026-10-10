# Research proposals

Each brief covers the question, close prior work, candidate contribution, case, metrics,
budget, risks, and criteria to continue or discard it. No experimental proposal is selected.

## Reading the filenames

- `case-NNNN` identifies a candidate use-case specification: the problem, research boundary,
  worked example, and comparison to consider.
- `doc-NNNN` identifies a supporting document. Here, doc-0005 and doc-0006 expand the two
  cases into scenario matrices and EDA plans; they are not additional use cases.
- `.es.md` is the complete Spanish reading version of the English `.md` source.

Read the case first, then its linked scenario and EDA plan. Code repair means correcting
faulty code; service workflow means coordinating tool actions and handling uncertain
results. Neither name implies that an implementation or experimental result exists.

## Candidate cases

The following Markdown specifications support case selection. They contain fictional
examples, three complexity levels, proposed EDA, and evaluation boundaries. No case has
been implemented or selected as the thesis contribution.

Both case specifications have complete Spanish reading versions:
[case-0001](case-0001-code-repair-harness.es.md) and
[case-0002](case-0002-service-workflow-harness.es.md).
English remains primary. This scoped language exception covers these two cases and their paired scenario/EDA plans.
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

## Scenario matrices and EDA plans

| Case | English plan | Spanish plan | Planned coverage | Provisional baseline sample |
|---|---|---|---|---|
| case-0001 | [Code repair](doc-0005-code-repair-scenarios-and-eda.md) | [Español](doc-0005-code-repair-scenarios-and-eda.es.md) | Two L0 controls and six scenario templates across L1-L3 | 12 development instances × 3 repetitions = 36 runs |
| case-0002 | [Service workflow](doc-0006-service-workflow-scenarios-and-eda.md) | [Español](doc-0006-service-workflow-scenarios-and-eda.es.md) | Two L0 controls and seven scenario templates across L1-L3 | 14 development instances × 3 repetitions = 42 runs |

L0 checks the evaluator and is outside agent-performance scores. Sample counts are
proposals for a later budgeted feasibility pilot, not executed runs or statistical
justification for effectiveness. The plans distinguish scenario acceptance, run acceptance,
and later improvement claims; both include proposed EDA before and after baseline runs.

Review these Markdown plans before selecting a case or authorizing implementation.
An exp-NNNN execution protocol and budget are required before any scientific run.
Agents stop at Review; Jairzinho decides integration and manually handles Done, issue
completion, and Completed date. No status or closure automation is introduced.
