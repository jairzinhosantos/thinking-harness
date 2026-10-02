---
id: dec-0002
title: "Branching and English-only project content"
status: accepted
revision: 1
created: 2026-09-30
updated: 2026-10-01
---

# Branching and English-only project content


## Decision
This policy was adopted on 2026-09-30 and is tracked in
[issue 12](https://github.com/jairzinhosantos/thinking-harness/issues/12).
Use main for reviewed formal baselines and develop for integration. Task branches start
from develop and return through PRs. Keep main as the default public entry point.
Require explicit human acceptance before a promotion into main.

Use English for all project-authored content, including GitHub planning metadata.
Use sober, concrete prose, with detail where it improves understanding.
Use Mermaid first for Markdown diagrams; use Draw.io when precise layout is needed,
with an editable source and generated SVG preview.

## Rationale
Research needs ongoing iteration while presentations and submissions need identifiable,
reviewed baselines. One working language makes documentation and engineering consistent.
Diagrams should explain relationships and remain maintainable with the relevant text.

## Migration
Create develop from the existing main, preserve the bootstrap commits, and prepare the
migration on docs/12-english-documentation. Translation preserves IDs, research states,
evidence, historical decisions, and source attribution. The earlier Spanish-prose allowance
is superseded; exact bibliographic titles and attributed quotations retain their wording.
Any future non-English academic submission requires an explicit exception.

## Boundaries
This decision does not select a thesis method, case, progress metric, or agent runtime.
It does not authorize unattended deployment or automatic promotion into main.
The completed implementation is reviewed through a task PR into develop; formal promotion
is a separate step. Until integration, main and develop retain their previous content.

## Standards
- [Branching and releases](../standards/std-0003-branching-and-releases.md)
- [Writing and diagrams](../standards/std-0004-writing-and-diagrams.md)

## Later amendment
On 2026-10-01, [dec-0004](dec-0004-bilingual-paper-reviews.md) adds Spanish translations
for paper reviews while retaining English as the primary language. The branch workflow
and language rules for other project content remain in effect.
