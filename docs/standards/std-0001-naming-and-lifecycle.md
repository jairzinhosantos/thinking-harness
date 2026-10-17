---
id: std-0001
title: "Naming and document lifecycle"
status: in-review
revision: 6
created: 2026-09-29
updated: 2026-10-16
---

# Naming and document lifecycle


## Names and identity
Use English as the primary language; paper reviews also have a Spanish translation.
File and directory names use ASCII
and lowercase kebab-case; Python uses snake_case. Preserve conventional tool names:
README.md, AGENTS.md, LICENSE, CITATION.cff, and Dockerfile.
Controlled documents use `<type>-<four-digit-sequence>-<description>.md`.
Types: std, dec, prd, pap, case, exp, and doc. Each type has an independent sequence
within its repository. Never reuse or renumber IDs; gaps are valid.
Check docs/catalog.csv and research/literature/catalog.csv before allocating an ID.

## Paper review pairs
Keep the English primary path `<pap-id>-<description>.md` and place its Spanish translation
beside it as `<pap-id>-<description>.es.md`. For example, pap-0011-self-harness.md and
pap-0011-self-harness.es.md are two language versions of one review, not separate paper records.
English remains implicit in the primary filename so existing links stay stable.

Only the primary file carries `id` and appears in docs/catalog.csv. The translation uses
`translation_of` with the same paper ID, `language: es`, `source` with the primary filename,
`source_revision`, `title`, `status`, `created`, and `updated`. Keep metadata keys, the
metadata title, and status values in English; the visible heading and body use Spanish.
Copy `source_revision` and `status` from the primary document. Keep translation dates accurate.
The translation has no independent document ID or revision sequence. Literature catalog
records, bibliographic keys, and reading states remain shared.

See the [translation workflow](std-0004-writing-and-diagrams.md#paper-review-translations).

## Compact case-folder exception
Case-0003 uses one Spanish primary file:
research/proposals/case-0003-debt-negotiation/README.es.md. It retains id: case-0003,
language: es and its revision sequence. Its title and prose are Spanish; metadata keys and
status values stay English. The catalog points to this file, not a separate English README.
Case, objective, modeling, setup and result explanation share this guide. Markdown files
within this case use `.es.md`; its notebooks remain bilingual and share execution evidence.

The Spanish primary exception is limited to this exact case folder. Other matching case
READMEs directly under research/proposals/case-NNNN-description/ may retain the established
README.md layout. This does not migrate other cases or paper reviews.
See the [proposal index](../../research/proposals/README.md) for the scoped language rules.

## STOP study-folder pilot
STOP uses `research/literature/reviews/pap-0001-stop/README.md` and `README.es.md` as a
scoped pilot. The primary README retains `id: pap-0001`; the directory carries the ID and
English description. Its translation uses `source: README.md`. The catalog points to the
primary README, with no duplicate document identity. Code excerpts, mathematical explanations,
and local inspection guidance share this review. Its downloaded original source stays in
`_local/upstream/`, excluded from Git; pinned upstream links remain usable on GitHub.

Only STOP is migrated. Other reviews and the general template retain the existing layout
until the pilot is reviewed. No notebook or execution environment is required for source
inspection. Future paper-folder READMEs must have an ID matching their immediate directory;
ordinary controlled documents still require the ID in their filename.

## Revisions
Keep paths stable during editing; Git records changes. A formal revision increments
revision and produces an issued r001, r002, or subsequent delivery when appropriate.
States: draft, in-review, accepted, superseded, withdrawn.
Fixing a typo does not require a new formal revision. Superseded documents link to their
replacement. Earlier decisions remain discoverable. Iteration notes use YYYY-MM-DD-description.md.

## Retention
Use Git for edit history and deliverables for immutable issued documents.
_archive holds retired material worth retaining; index.csv records its date, reason,
and replacement. Superseded decisions remain under docs/decisions with status superseded.
Discarded prototypes may be removed after preserving their evidence and a recoverable commit.
Reproducible temporary files may be deleted; retain negative experimental evidence.
Store large data and logs outside Git, with manifests and checksums. Never archive private
material in the public repository.

## Catalog
Simple YAML front matter contains id, title, status, revision, created, and updated.
Run `python3 scripts/check_repository.py --write-catalog` to generate docs/catalog.csv.
Do not use nested YAML structures in these fields. Quote titles containing a colon.

## Revision history
Revision 6 consolidates case-0003 into a Spanish primary README.es.md on 2026-10-16.
Its notebooks remain bilingual and historical evidence retains its original protocol.

Revision 5 adds the STOP-only study-folder pilot on 2026-10-16 while preserving the accepted
case-folder exception from revision 4. Generalizing the study layout remains pending review.

Revision 4 adds the authorized case-0003 folder exception on 2026-10-16. Existing case paths
remain stable; case-0002 is retained as a superseded reference.

Revision 3 adds paired English and Spanish paper-review filenames and derived translation
metadata on 2026-10-01; see [dec-0004](../decisions/dec-0004-bilingual-paper-reviews.md).

Revision 2 adopts the English-only convention approved on 2026-09-30.
The former Spanish-content allowance is superseded by
[dec-0002](../decisions/dec-0002-branching-and-english-standard.md).
Stable identities, paths, and retention rules are unchanged.
