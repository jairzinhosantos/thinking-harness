---
id: doc-0002
title: "Research plan"
status: in-review
revision: 2
created: 2026-09-29
updated: 2026-10-16
---

# Research plan

## Objective
Select a bounded thesis question about improving an agent harness, supported by an understood
mechanism, a feasible comparison, and traceable evidence. Whether improving the improver adds
value over a fixed procedure remains an open research question.

## Current position

| Area | Evidence and remaining work |
|---|---|
| Literature | 23 cataloged papers; bilingual STOP and Self-Harness reviews remain partial. Complete guided reading and outstanding bibliographic checks. |
| Code repair, case-0001 | Case, scenario plan and separate harness-participation proposal; no executed experiment. Decide whether and how to test the extension. |
| Debt negotiation, case-0003 | Implemented bounded prompt search with a fixed optimizer. One v2 pilot stopped at its token guard without an accepted candidate or final comparison. The current v3 objective has not been measured. |
| Thesis | Final case, method and contribution remain open. No paper reproduction or demonstrated recursive improvement is claimed. |

The [case index](../research/cases/README.md) links specifications and evidence.
The retired service-workflow case is not an active research track.

## Next bounded steps

| Step | Reviewable output | Decision supported |
|---|---|---|
| Understand the mechanism | Explain STOP and Self-Harness with code and mathematical examples; use the [literature map](../research/synthesis/research-options.md#literature-map) to compare fixed and adaptive improvers | What changes, what stays fixed, and what would count as recursion |
| Diagnose the existing pilot | Inspect the recorded budget stop, baseline violations, evaluator assumptions and task coverage without new model calls | Whether the negotiation case warrants another bounded test |
| Specify the next comparison | Choose one case and a versioned protocol with splits, baseline, acceptance criteria, total budget and a stop rule that accounts for final evaluation | Whether execution is informative and affordable |
| Execute after authorization | Produce a new run record and report failure, incomplete evaluation or measured outcomes without overwriting prior evidence | Retain, revise or reject the proposed method |
| Draft the thesis plan | Map the selected question, variables, evaluation and limitations to [academic requirements](academic/requirements.csv) | Whether the academic plan is supported by evidence |

AFlow and DGM remain comparator candidates after the guided readings; they do not require
additional parallel reading tasks.

These are dependencies, not dates or automatic execution commitments. A change of objective,
model, evaluator or split requires a protocol revision. Do not reinterpret the v2 pilot as v3 evidence.

## Work model

Keep one deep reading task and one technical task in progress. Each review should produce
an explanation, evidence, or a decision. Hours do not create quotas; the specific progress
measurement choice remains open in [progress and HITL](designs/doc-0004-progress-and-hitl.md).
The [Project](project-links.md) owns task status; this plan owns research direction.
Only human review and acceptance advance integration or formal baselines.

The [builder and independent-QA design](designs/doc-0003-agentic-development-strategy.md)
remains a future bounded pilot. New shared infrastructure, training, cloud services and
additional folders require a demonstrated need; see the [evolution plan](project-evolution.md).

## Revision

Revision 2 replaces the initial-cycle plan while preserving doc-0002. It reflects the
expanded literature, two active cases and the incomplete negotiation pilot as of 2026-10-16.
