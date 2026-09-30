---
id: dec-0001
title: "Public research core and private extension"
status: accepted
revision: 1
created: 2026-09-29
updated: 2026-09-30
---

# Public research core and private extension


## Decision
Start thinking-harness as an independent public repository.
Create thinking-harness-private only when concrete restricted work exists.
The private repository will consume an identified version of the public core without
duplicating the method.

## Rationale
Research must be developable and testable with a reproducible public case.
The thesis will select a bounded question and case; the laboratory can explore alternatives.
Existing work is a technical reference, not the system whose evolution defines the thesis.

## Implementation
Initialize a new directory and keep original source files outside the public root.
Do not automatically import previous documents or institutional assets.
Use MIT for original material created in the repository during bootstrap.
External sources and dependencies retain their own licenses.

## Status
The researcher agreed to the name and separation. The method, framework, case, and final
title remain undecided. This English translation preserves the accepted decision.
