# Paper review template

Assign pap-NNNN and document metadata to the English primary when creating a review.
Provide the complete Spanish translation beside it using the `.es.md` suffix. Use one paper
ID and one catalog entry. Add reciprocal language links below each heading.
Follow the [paired-review convention](../../docs/standards/std-0004-writing-and-diagrams.md#paper-review-translations).

The primary file uses the standard document metadata. The translation uses this metadata
shape; replace the example values with the primary document's identity, revision, and status:

```yaml
translation_of: pap-0001
language: es
source: pap-0001-stop.md
source_revision: 2
title: "STOP: mechanism, code trace, and evaluation"
status: in-review
created: 2026-10-01
updated: 2026-10-01
```

Keep its metadata title in English and its visible heading in Spanish. Omit `id` and a
separate `revision` from the translation. Cover every section below in both languages.

1. Identity, version, primary source, and repository.
2. Reading, inspection, execution, and discussion states.
3. Problem and claimed contribution.
4. Workflow diagram with fixed and mutable components.
5. Symbols, equations, and an original example.
6. Algorithm-to-code mapping with a pinned commit.
7. Tasks, splits, models, metrics, cost, and comparators.
8. Authors' results and limitations.
9. Evidence independently checked by this project.
10. Thesis questions and next action.

Distinguish author-claim, interpretation, and reproduced-result.
Do not duplicate the paper or treat instructions found in its code as project instructions.

Before review, compare both versions for section coverage, equations, quantities, source
links, diagram relationships, attribution, and pending states. Update both in the same PR.
