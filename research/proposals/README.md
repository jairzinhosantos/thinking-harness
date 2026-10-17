# Research proposals

Case specifications define candidate problems, mutable harness components, fixed evaluation,
and criteria to continue or discard a direction. They do not establish implemented systems
or select the final thesis contribution. Cases 1-2 and their scenario plans retain English/Spanish pairs. Case-0003 uses one Spanish
Markdown guide with bilingual notebooks and shared execution evidence. The draft extension
below retains its paired reading versions.

## Active candidates

| Case | Focus | Reading |
|---|---|---|
| case-0001 | Code repair: feedback and bounded task-solving loops | [English](case-0001-code-repair-harness.md) / [Español](case-0001-code-repair-harness.es.md) |
| case-0003 | Synthetic debt negotiation: offers, consent, and bounded prompt optimization | [Español](case-0003-debt-negotiation/README.es.md) |

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

Case-0003 keeps one [Spanish guide](case-0003-debt-negotiation/README.es.md) for its case,
objective, modeling, setup and observed results. All Markdown in this case uses `.es.md`.
The guide is the primary controlled document, id: case-0003, with language: es.
It is not a translation of a separate English document.

```text
case-0003-debt-negotiation/
  README.es.md           # Case, objective, model, setup and results
  golden-set.yaml        # Partitioned synthetic fixtures
  prompt.yaml            # Mutable policy seed
  config.yaml            # Model, budget and live opt-in
  .env.example           # Local credential template
  requirements.txt       # Notebook dependencies
  prompt-search.ipynb    # English notebook
  prompt-search.es.ipynb # Spanish notebook, same evidence
  prompt_search.py       # Testable runtime and bounded search
  results/               # Recorded report, YAML versions, usage and provenance
```

The notebooks default to replaying the saved pilot without API calls. The runtime extracts
only the marked objective section, excluding measured results. Future runs use protocol v3
with the Spanish objective; the recorded v2 evidence is unchanged. Live calls require explicit
opt-in, model access and a budget. No recursive improvement or completed final test is claimed.

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
