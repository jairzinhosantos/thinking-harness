---
id: doc-0004
title: "Progress measurement and human review"
status: draft
revision: 1
created: 2026-09-29
updated: 2026-10-01
---

# Progress measurement and human review


## Pending decision
Work can be initiated through voice or text instructions, delegated within defined limits,
and reviewed at agreed checkpoints. Availability is a reference, not a progress measure.
This proposal sets no quotas, calendar commitments, or running agents.

| Option | Unit of progress | Benefit | Limitation |
|---|---|---|---|
| A. Weekly evidence and decisions | A question resolved through a review, test, or comparison, with a recorded decision | Suits research uncertainty | Requires agreement on sufficient evidence |
| B. Milestones with exit criteria | Literature, scope, protocol, pilot, and thesis plan | Shows overall maturity | Can hide incremental progress |
| C. Accepted work flow | Accepted outputs, cycle time, and corrections | Useful during implementation | Tasks differ in difficulty |

Proposal: use A for weekly review, B as the overall map, and C once implementation provides
meaningful signals. A progress-measurement model must be selected before adoption as a standard.
A documented negative result counts as progress when it reduces uncertainty.
Commit count, lines of code, and downloaded papers are not scientific success measures.

## Proposed weekly report
- Priority question and expected evidence.
- Evidence obtained, link, and limitations.
- Decision: continue, adjust, discard, or request review.
- Remaining uncertainty.
- Next task with a closure criterion and agreed cost limit.

## Human-in-the-loop (HITL)
1. Define the objective through voice or text instructions.
2. The coordinator defines scope, inputs, criteria, permissions, and budget, asking only
   for missing decisions that are necessary to proceed.
3. A builder or research-reviewer prepares changes or evidence within that scope.
4. QA checks independently, records results, and returns specific defects.
5. Review the proposal, diff or reading note, supporting checks, limitations, and required
   decision. Human review determines whether to accept, adjust, or reject the result.
6. Integrate accepted work and record learning for the next task.

Existing authorization remains valid. Do not request approval for every routine step.
Escalate changes to scope, budget, information exposure, or scientific conclusions not
previously agreed. Each agent's credentials must match its task and environment.

## Work between human reviews
Readings, authorized local tests, and task-branch changes are candidates for bounded delegation.
Execution needs an active process and task contract. Do not assume work continues after a
session ends. Define attempt, cost, duration, and resource limits before a pilot.
At a limit or unresolved dependency, preserve evidence and move to Review.
Do not deploy, publish data, change scientific criteria, or incur costs outside existing
authorization. Correction loops must be bounded.

## First proposed pilot
Use one small technical task with objective criteria. Compare assisted work with builder
plus QA on acceptance, detected faults, corrections, cost, and human-review effort.
One pilot does not establish causality or thesis results.
See the [agentic development strategy](doc-0003-agentic-development-strategy.md).
