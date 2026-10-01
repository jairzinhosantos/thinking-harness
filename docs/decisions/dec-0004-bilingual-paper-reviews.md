---
id: dec-0004
title: "Bilingual paper reviews"
status: accepted
revision: 1
created: 2026-10-01
updated: 2026-10-01
---

# Bilingual paper reviews

## Decision
Maintain a primary English version and a complete Spanish translation of every paper review.
This scoped language exception was adopted on 2026-10-01 and is tracked in
[issue 17](https://github.com/jairzinhosantos/thinking-harness/issues/17).
The translation supports study while the primary version remains the project reference.

## Identity and maintenance
Keep both files in research/literature/reviews, with `.es.md` identifying the Spanish version.
Preserve the primary English path and one paper identity, catalog record, and bibliography.
Link the two versions and record the primary revision in the translation metadata.
Update and review both in the same PR, including translated explanatory diagram labels.

A translation preserves sources, mathematical notation, code, quantities, limitations, and
reading, discussion, execution, and reproduction states. It adds no independent conclusions.
Existing validation supports structural checks; paired editorial review establishes
translation completeness and meaning. No separate repository or translation automation is needed.

## Scope
This amends the English-only rule in [dec-0002](dec-0002-branching-and-english-standard.md)
for paper-review prose and explanatory diagram labels only. Filenames, code, metadata keys,
controlled values, and other project-authored content remain in English.
The [project-author voice](dec-0003-project-author-voice.md) applies in both languages.
The thesis method, progress model, and scientific evidence states are unchanged.

## Standards
- [Naming and lifecycle](../standards/std-0001-naming-and-lifecycle.md)
- [Writing and translations](../standards/std-0004-writing-and-diagrams.md#paper-review-translations)
- [Paper review template](../../research/literature/review-template.md)
