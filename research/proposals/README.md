# Research proposals

Case specifications define candidate problems, mutable harness components, fixed evaluation,
and criteria to continue or discard a direction. They do not establish implemented systems
or select the final thesis contribution. English is primary; cases 1-3 and their paired
scenario plans, plus the draft extension below, have authorized Spanish reading versions
with shared identities and evidence states.

## Active candidates

| Case | Focus | Reading |
|---|---|---|
| case-0001 | Code repair: feedback and bounded task-solving loops | [English](case-0001-code-repair-harness.md) / [Español](case-0001-code-repair-harness.es.md) |
| case-0003 | Synthetic debt negotiation: offers, consent, features, and future harness improvement | [English](case-0003-debt-negotiation/README.md) / [Español](case-0003-debt-negotiation/README.es.md) |

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

Case-0003 keeps its specification and future small demonstration together:

```text
case-0003-debt-negotiation/
  README.md       # Primary specification, id: case-0003
  README.es.md    # Spanish counterpart, source: README.md
```

Future scenarios.json and demo.py will live beside these documents when their design and
implementation are authorized. They do not exist yet. Keep small case-specific fixtures
and demonstration code here; shared infrastructure and formal experiment evidence retain
their repository locations. Do not duplicate the specification in another folder.

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
