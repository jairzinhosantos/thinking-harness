---
id: dec-0005
title: "Human integration and baseline promotion"
status: accepted
revision: 1
created: 2026-10-02
updated: 2026-10-02
---

# Human integration and baseline promotion

## Decision

Task integration and formal baseline promotion each require human review and a merge
performed by the human maintainer:

1. Task branch, task PR, passing checks, human acceptance, then a squash merge into develop.
2. A separate decision to propose a baseline, promotion PR, passing checks, explicit
   baseline acceptance, then a merge commit into main.

Review baseline readiness approximately every one or two weeks. This is an indicative
cadence; promotion depends on readiness and a human decision, not elapsed time.
Synchronization from main back into develop also uses a PR, passing checks, human review,
and a maintainer-performed merge commit.

Agents may prepare authorized changes, evidence, checks, and PRs. They do not merge into
permanent branches or enable auto-merge under this workflow. A passing CI run is technical
evidence, not human acceptance. The maintainer's reviewed task merge records task acceptance;
baseline acceptance is additionally recorded explicitly in the promotion PR.

## Rationale

The previous branch diagram drew a direct arrow from task PR checks to develop while
showing human acceptance only before main. The text required review of task criteria but
did not state the human merge action clearly. Both gates must be visible so preparation,
acceptance, and integration cannot be mistaken for one automatic step.

## Scope

This clarifies the branch policy in [dec-0002](dec-0002-branching-and-english-standard.md)
and updates [std-0003](../standards/std-0003-branching-and-releases.md) to revision 2.
It addresses the integration-review portion of
[issue 11](https://github.com/jairzinhosantos/thinking-harness/issues/11).

The progress metric, research case, and experiment budgets remain separate decisions.
No schedule, reminder, auto-merge setting, or branch-protection configuration is changed.
The documentation correction does not itself accept or merge a pending PR.
