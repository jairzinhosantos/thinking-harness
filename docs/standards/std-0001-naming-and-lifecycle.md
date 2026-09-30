---
id: std-0001
title: "Naming and document lifecycle"
status: accepted
revision: 2
created: 2026-09-29
updated: 2026-09-30
---

# Naming and document lifecycle


## Names and identity
Use English throughout project-authored content. File and directory names use ASCII
and lowercase kebab-case; Python uses snake_case. Preserve conventional tool names:
README.md, AGENTS.md, LICENSE, CITATION.cff, and Dockerfile.
Controlled documents use `<type>-<four-digit-sequence>-<description>.md`.
Types: std, dec, prd, pap, case, exp, and doc. Each type has an independent sequence
within its repository. Never reuse or renumber IDs; gaps are valid.
Check docs/catalog.csv and research/literature/catalog.csv before allocating an ID.

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
Revision 2 adopts English-only content following the researcher's approval on 2026-09-30.
The former Spanish-content allowance is superseded by
[dec-0002](../decisions/dec-0002-branching-and-english-standard.md).
Stable identities, paths, and retention rules are unchanged.
