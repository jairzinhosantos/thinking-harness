---
id: dec-0006
title: "Active research cleanup and execution identity"
status: in-review
revision: 1
created: 2026-10-16
updated: 2026-10-16
---

# Active research cleanup and execution identity

## Decision
Keep active research units and useful decisions. Delete superseded case documents and
redundant iteration notes instead of moving them to an archive. Git retains their history.
Keep all recorded execution evidence unchanged, including unsuccessful and incomplete runs.

| Change | Reason or replacement |
|---|---|
| Retire case-0002 and its scenario study doc-0006, including translations | Case-0003 replaces the service-workflow direction; its objectives and evaluation are separate |
| Remove the bootstrap and English-migration iteration notes | Current standards and dec-0001 through dec-0004 retain the relevant decisions |
| Remove the initial backlog list from project-links.md | GitHub issues and the Project already provide task history and status |
| Rename the initial plan to [research plan](../doc-0002-research-plan.md), retaining doc-0002 | Keep direction and current evidence in one maintained plan |
| Separate protocol, run and prompt identities in [std-0002](../standards/std-0002-experiment-versioning.md) | Match the implemented pilot without renaming historical evidence |

**Reserved IDs:** case-0002 and doc-0006 must never be reused. Their last pre-cleanup
contents are available at commit `5375d204846584d67a29dff287671ea438028571`.
The document catalog lists files currently present; this decision preserves retirement identity.

## Boundaries
Case-0001 and its harness-participation proposal remain separate until their scope is decided.
Case-0003 code, notebooks, inputs, PDF and run records remain unchanged. The v2 recorded run
is not evidence for the unmeasured v3 objective. Moving notebook helpers is a separate proposal.

No scientific result is accepted by this cleanup. Human review and merge remain required.
