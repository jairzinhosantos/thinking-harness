# Research proposals

Case specifications define candidate problems, mutable harness components, fixed evaluation,
and criteria to continue or discard a direction. They do not establish implemented systems
or select the final thesis contribution. English is primary; cases 1-3 and their paired
scenario plans, case-0003 modeling and notebooks, plus the draft extension below, have authorized Spanish reading versions
with shared identities and evidence states.

## Active candidates

| Case | Focus | Reading |
|---|---|---|
| case-0001 | Code repair: feedback and bounded task-solving loops | [English](case-0001-code-repair-harness.md) / [Español](case-0001-code-repair-harness.es.md) |
| case-0003 | Synthetic debt negotiation: offers, consent, and bounded prompt optimization | [English](case-0003-debt-negotiation/README.md) / [Español](case-0003-debt-negotiation/README.es.md) |

The code-repair [scenario plan](doc-0005-code-repair-scenarios-and-eda.md)
([Español](doc-0005-code-repair-scenarios-and-eda.es.md)) remains a proposed feasibility
study, not executed evidence. Its 36-run sample does not authorize negotiation experiments.

## Superseded service case

[case-0002](case-0002-service-workflow-harness.md)
([Español](case-0002-service-workflow-harness.es.md)) and its
[doc-0006 scenario plan](doc-0006-service-workflow-scenarios-and-eda.md)
([Español](doc-0006-service-workflow-scenarios-and-eda.es.md)) remain readable with their
original IDs. They describe cancellations and refunds, not negotiation. Their proposed
42-run sample, evaluation rules, and complexity levels do not transfer to case-0003.

## Compact case folder

Case-0003 keeps its specification, examples, and first executable prototype together:

```text
case-0003-debt-negotiation/
  README.md       # Primary specification, id: case-0003
  README.es.md    # Spanish counterpart, source: README.md
  objective.md    # Fixed negotiation objective
  modeling.md / modeling.es.md # Definitions, features, evaluator and protocol
  golden-set.yaml # Synthetic development, validation, and test fixtures
  prompt.yaml     # Mutable policy seed
  config.yaml     # Fixed run configuration and opt-in
  .env.example    # Local credential template
  requirements.txt # Notebook dependencies
  prompt-search.ipynb / prompt-search.es.ipynb # Paired walkthroughs and opt-in execution
  prompt_search.py    # Testable runtime, evaluation, and search
```

The [notebook](case-0003-debt-negotiation/prompt-search.ipynb) starts offline. Live calls require
an explicit model, prices, budget, and environment API key. The prototype changes only the
policy prompt; it does not implement full conversations or a recursive optimizer. No live
improvement result is claimed. Keep small fixtures and demonstration code here; shared
infrastructure and formal experiment evidence retain their repository locations.

This folder exception is scoped to case-0003. Existing case IDs and paths remain stable.
A controlled case README must sit directly in research/proposals/case-NNNN-description/,
with a matching ID. Only its primary README appears in docs/catalog.csv. The translation
uses translation_of, language, source, source_revision, title, status, created, and updated.
Keep both language versions and their Mermaid diagrams aligned in the same PR.

## Review boundaries

Start with the case model and evaluator examples. A fixed-policy demonstration is distinct
from an optimization experiment. Scientific execution requires a protocol, budget, and stop
condition; no proposed sample count is execution approval.

Agents stop at Review. Jairzinho decides integration and manually handles Done, issue
completion, and Completed date. No status or closure automation is introduced.

## Draft extension

[Harness participation in self-improvement](doc-0007-harness-participation-proposal.md)
([Español](doc-0007-harness-participation-proposal.es.md)) explores using the current harness
to construct its next version, compared with a fixed constructor. It is a separate draft,
not an additional case or a replacement for case-0001. Review whether to extend case-0001, replace
it, or keep the proposal separate before changing existing case specifications and EDA plans.
