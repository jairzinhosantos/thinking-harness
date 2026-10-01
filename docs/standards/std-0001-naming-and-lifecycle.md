---
id: std-0001
title: "Naming and document lifecycle"
status: accepted
revision: 3
created: 2026-09-29
updated: 2026-10-01
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
beside it as `<pap-id>-<description>.es.md`. For example, pap-0001-stop.md and
pap-0001-stop.es.md are two language versions of one review, not separate paper records.
English remains implicit in the primary filename so existing links stay stable.

Only the primary file carries `id` and appears in docs/catalog.csv. The translation uses
`translation_of` with the same paper ID, `language: es`, `source` with the primary filename,
`source_revision`, `title`, `status`, `created`, and `updated`. Keep metadata keys, the
metadata title, and status values in English; the visible heading and body use Spanish.
Copy `source_revision` and `status` from the primary document. Keep translation dates accurate.
The translation has no independent document ID or revision sequence. Literature catalog
records, bibliographic keys, and reading states remain shared.

See the [translation workflow](std-0004-writing-and-diagrams.md#paper-review-translations).

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
Revision 3 adds paired English and Spanish paper-review filenames and derived translation
metadata on 2026-10-01; see [dec-0004](../decisions/dec-0004-bilingual-paper-reviews.md).

Revision 2 adopts the English-only convention approved on 2026-09-30.
The former Spanish-content allowance is superseded by
[dec-0002](../decisions/dec-0002-branching-and-english-standard.md).
Stable identities, paths, and retention rules are unchanged.
