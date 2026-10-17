---
id: std-0001
title: "Naming and document lifecycle"
status: in-review
revision: 8
created: 2026-09-29
updated: 2026-10-16
---

# Naming and document lifecycle


## Names and identity
Use English as the primary language; paper reviews also have a Spanish translation.
File and directory names use ASCII
and lowercase kebab-case; Python uses snake_case. Preserve conventional tool names:
README.md, AGENTS.md, LICENSE, CITATION.cff, and Dockerfile.
Execution directories use the UTC run identifiers defined in
[std-0002](std-0002-experiment-versioning.md), including their uppercase `T` and `Z`.
Controlled documents retain stable IDs in YAML metadata and docs/catalog.csv.
Types: std, dec, prd, pap, case, exp, and doc. Each type has an independent sequence.
Never reuse or renumber IDs; gaps are valid. Check both document and literature catalogs
and retirement records under `docs/decisions/` before allocating an ID.
Removed IDs remain reserved, even when absent from the generated catalog.
General project documents retain `<type>-NNNN-description.md` names.
The research-unit layout below avoids repeating the folder identity in every filename.

## Research units

Cases live under `research/cases/case-NNNN-description/`. Reviewed papers live under
`research/literature/reviews/pap-NNNN-description/`. Each primary README carries the ID
of its immediate folder. A paper listed in the catalog does not need a folder until a review exists.

- `README.md` presents the primary case or paper review.
- `README.es.md` is its linked Spanish translation where applicable.
- Supporting case documents use descriptive names, such as `scenarios.md` and
  `harness-participation.md`, with their existing `doc-NNNN` IDs in metadata.
- Supporting studies have their own scope and status. Sharing a case folder does not
  make a draft extension part of the accepted case specification.
- Inputs, configuration, notebooks, local implementation and recorded results stay in the case.
  Additional subdirectories contain actual resources, such as `diagrams/` or `results/`.

The catalog maps IDs to current paths. For example, `doc-0005` remains the code-repair
scenario study even though its filename is now `scenarios.md`. A move does not create a new identity.

## Language pairs

English is the primary language. Each paper review has a complete Spanish counterpart.
Case 0001 retains its English/Spanish document pairs. Each pair has reciprocal links.
Only the primary carries `id` and appears in the document catalog. The translation uses
`translation_of`, `language: es`, `source`, `source_revision`, `title`, `status`, `created`
and `updated`. Its source filename is relative to its own directory, normally `README.md`
or the supporting document's descriptive filename. Identity, evidence and completion state
are shared; the translation has no independent ID or revision sequence.

Case 0003 retains the explicit Spanish-primary exception at
`research/cases/case-0003-debt-negotiation/README.es.md`, with `id: case-0003` and `language: es`.
Its case, objective, model and results share this guide. All Markdown within that case uses
`.es.md`; its notebooks remain bilingual. This exception does not translate other project
content or alter historical run evidence. Metadata keys, code and configuration keys stay English.

See the [writing standard](std-0004-writing-and-diagrams.md) and
[case index](../../research/cases/README.md).

## Revisions
Keep paths stable during editing; Git records changes. A formal revision increments
revision and produces an issued r001, r002, or subsequent delivery when appropriate.
States: draft, in-review, accepted, superseded, withdrawn.
Fixing a typo does not require a new formal revision. Remove superseded documents after
recording their replacement and reserved IDs in a decision. Git preserves earlier versions.

## Retention
Keep current guidance and decisions that still explain active constraints. Remove obsolete
drafts and duplicate notes instead of moving them to an archive. Record what changed, why,
and what replaces it under `docs/decisions/`; Git retains removed content.
Negative experimental evidence remains with its case, with original names, bytes and provenance.
Do not rename historical run or candidate IDs to match a later convention.
Formal delivery files and manifests belong in `deliverables/` once actual documents are issued;
they are immutable. Large data and logs stay outside Git with provenance and checksums.
Private material never enters the public repository. Growth conditions are recorded in the
[evolution plan](../project-evolution.md).

## Catalog
Simple YAML front matter contains id, title, status, revision, created, and updated.
Run `python3 scripts/check_repository.py --write-catalog` to generate docs/catalog.csv.
Do not use nested YAML structures in these fields. Quote titles containing a colon.

## Revision history
Revision 8 retires redundant material without an archive and reserves removed IDs.
See [dec-0006](../decisions/dec-0006-active-research-cleanup.md).

Revision 7 adopts research-unit folders, descriptive case-study filenames and staged repository
growth on 2026-10-16. IDs, translation pairs and historical evidence are preserved.

Revision 6 consolidates case-0003 into a Spanish primary README.es.md on 2026-10-16.
Its notebooks remain bilingual and historical evidence retains its original protocol.

Revision 5 adds the STOP-only study-folder pilot on 2026-10-16 while preserving the accepted
case-folder exception from revision 4. Generalization was pending at that revision
and is covered by revision 7.

Revision 4 adds the authorized case-0003 folder exception on 2026-10-16. Case-0002 was
retained as a superseded reference at that revision; its removal is recorded in dec-0006.

Revision 3 adds paired English and Spanish paper-review filenames and derived translation
metadata on 2026-10-01; see [dec-0004](../decisions/dec-0004-bilingual-paper-reviews.md).

Revision 2 adopts the English-only convention approved on 2026-09-30.
The former Spanish-content allowance is superseded by
[dec-0002](../decisions/dec-0002-branching-and-english-standard.md).
Stable identities, paths, and retention rules are unchanged.
