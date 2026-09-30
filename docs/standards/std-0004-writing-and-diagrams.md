---
id: std-0004
title: "Writing and diagram conventions"
status: accepted
revision: 1
created: 2026-09-30
updated: 2026-09-30
---

# Writing and diagram conventions


## Language and tone
Use English for prose, README files, code comments, docstrings, configuration descriptions,
diagram labels, commits, PRs, issue bodies, and Project metadata.
Keep exact bibliographic titles and attributed quotations. Explicit researcher approval
is required for an academic submission in another language.
Use plain words, concrete verbs, and short paragraphs. Avoid emojis, em dashes, marketing
claims, repetition, and filler. Add detail when explaining a mechanism, assumption, or result.
Define concepts and symbols before equations. Separate author claims, interpretations,
and reproduced evidence. Translation must not change evidence or completion states.

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
short English labels, a consistent reading direction, and surrounding explanation.

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
