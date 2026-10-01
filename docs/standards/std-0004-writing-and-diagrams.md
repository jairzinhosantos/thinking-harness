---
id: std-0004
title: "Writing and diagram conventions"
status: accepted
revision: 3
created: 2026-09-30
updated: 2026-10-01
---

# Writing and diagram conventions


## Language and tone
Use English for prose, README files, code comments, docstrings, configuration descriptions,
diagram labels, commits, PRs, issue bodies, and Project metadata.
Paper reviews additionally include a Spanish translation, with translated prose and explanatory
diagram labels, under the scoped rules below.
Keep exact bibliographic titles and attributed quotations. Explicit approval
is required for an academic submission in another language.
Use plain words, concrete verbs, and short paragraphs. Avoid emojis, em dashes, marketing
claims, repetition, and filler. Add detail when explaining a mechanism, assumption, or result.
Define concepts and symbols before equations. Separate author claims, interpretations,
and reproduced evidence. Translation must not change evidence or completion states.

## Paper review translations
Every paper review has a primary English file and a full Spanish `.es.md` translation in
the same directory. Add reciprocal language links below the heading. The Spanish version
is a derived reading aid with the same scope, uncertainty, and evidence as the primary.
It does not create another review or advance reading, discussion, or reproduction status.
This exception was adopted on 2026-10-01; see
[dec-0004](../decisions/dec-0004-bilingual-paper-reviews.md).

Keep filenames, metadata keys and controlled values, code, symbols, bibliographic titles,
source URLs, and identifiers unchanged. Translate headings, prose, tables, link labels,
and explanatory diagram labels. Preserve diagram relationships and use the same format.
For Mermaid, translate labels in the paired Markdown and render both versions.

Update both files in the same task PR. Revise the English source first, update the full
Spanish counterpart, and copy the source revision and document status into its metadata.
Check equations, quantities, source links, examples, section coverage, and caveats together.
A correction discovered while translating must also be applied to the English primary.
Do not publish a partial summary as the equivalent translation.

Git preserves both histories; no second repository or independent translation release is
needed. The revision field records the source baseline but does not automatically detect
changes within that revision. Synchronization and semantic equivalence require paired
editorial review; existing CI checks links, document structure, and diagram rendering.

## Authorial voice
Write from the project author's perspective. State the research and project content directly,
using impersonal or project-centered sentences by default. First-person language may be used
when a document's format calls for it, but must remain consistent within that document.
Do not describe personal preferences, requests, or conversations through an assistant's
external narration. Remove conversational explanations that do not belong in the artifact.

Examples of the intended voice:

- Progress will be tracked through observable evidence.
- The evaluation will compare candidate harnesses against a fixed baseline.
- This policy was adopted on 2026-09-30.
- The progress-measurement model remains open.
- Promotion into main requires explicit human acceptance.

Apply this convention to every project-authored document, README, review, summary, decision,
iteration note, template, metadata field, issue, PR, and diagram label. Operational roles
such as builder, QA, and human review remain explicit where they explain responsibility.
Preserve third-party attribution and exact quotations. Authorship voice must not imply that
assisted inspection equals completed personal reading, validation, or reproduction.

Repository validation rejects selected recurring external-narration phrases in Markdown
prose, CSV fields, and Draw.io labels. It is a regression check, not a semantic guarantee.
Attributed block quotations, inline code, and fenced code are excluded from Markdown lint;
review diagram labels and other excluded content manually. PR review must check authorial
voice throughout the actual artifact, including formats the lint does not cover.

## README structure
The root README welcomes readers, defines the project and harness concept, states current
maturity, points to a starting path, explains the workflow and every top-level directory,
and gives validation, contribution, licensing, and citation guidance.
Directory READMEs stay short: purpose, expected contents, and relevant constraints.
Use relative documentation links. Avoid duplicating live Project statuses in static files.

## Diagram choice
Use Mermaid for flows, sequences, dependencies, and architecture that remain readable
with automatic layout. Keep its fenced source beside the explanation in Markdown.
Split a complex diagram before increasing its density. Each diagram needs a clear purpose,
short labels in the document language, a consistent reading direction, and surrounding explanation.

Use Draw.io when manual placement or visual complexity requires it. Store uncompressed
editable XML under diagrams/source and a generated SVG preview under diagrams/exports.
The .drawio file is authoritative; never edit its SVG as an independent diagram.
Embed the SVG and link the source. Do not maintain a second Mermaid version of the same view.

## Regeneration and verification
Export Draw.io with a white background and readable labels:

```sh
# macOS example; adapt the executable path to the local installation.
"/Applications/draw.io.app/Contents/MacOS/draw.io" --export --format svg --embed-diagram --output diagrams/exports/agentic-development-workflow.svg diagrams/source/agentic-development-workflow.drawio
python3 scripts/check_diagrams.py --record-drawio
```

The recording command updates diagrams/exports/manifest.json with source and preview SHA-256
values. Run it only after actually exporting and visually reviewing the changed diagram.
Checks detect missing previews, malformed XML, and stale recorded hashes; they cannot prove
visual equivalence. Review the source and preview together in the PR.

```sh
python3 scripts/check_repository.py
npm ci
npm run check:diagrams
```

The diagram command renders every Markdown Mermaid block using the pinned CLI. CI performs
the same rendering. Rendering verifies syntax and exportability, not explanatory quality;
review the resulting layout as well. Temporary Mermaid renders are not committed.
Language and tone are reviewed editorially; CI does not pretend to prove English prose.

## Reference
[GitHub Markdown diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)

## Revision history
Revision 3 adds paired paper reviews on 2026-10-01, including translated diagram labels
and paired editorial review. See [dec-0004](../decisions/dec-0004-bilingual-paper-reviews.md).

Revision 2 adopts the project-author voice convention on 2026-10-01.
See [dec-0003](../decisions/dec-0003-project-author-voice.md).
