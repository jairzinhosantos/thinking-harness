# Working agreements

- Use English for all project-authored content: prose, code, comments, docstrings,
  configuration descriptions, diagrams, commits, issues, and PRs.
- Every paper review has a primary English file and a linked Spanish `.es.md` translation,
  including translated explanatory diagram labels. Maintain both in the same PR and preserve
  the shared paper identity, source revision, evidence, and completion states. This exception
  is limited to paper reviews; filenames, metadata keys, code, and other project content stay
  in English. Follow the paired-review rules in std-0004.
- Case-0003 uses Spanish-only Markdown with `.es.md` filenames. Consolidate its case,
  objective, modeling and results in one primary README.es.md. Keep its notebooks
  bilingual, code/configuration keys in English, and one shared execution record.
  Other case specifications and scenario plans retain their scoped paired versions.
  See research/cases/README.md; preserve existing IDs and historical run evidence.
- Keep one folder per case and reviewed paper under research/cases and research/literature/reviews.
  Use README.md as the primary document, with README.es.md for a Spanish translation or
  the explicitly scoped Spanish primary. Supporting case studies use descriptive filenames;
  retain existing IDs in metadata and docs/catalog.csv. Follow docs/project-evolution.md:
  add folders for present work, keep case-specific resources together, and preserve run evidence.
- Put Python modules supporting an implemented case in that case's `utils/` directory.
  Keep its README, notebooks and input/configuration files at the case root. Create `utils/`
  only when needed; repository-wide checks and export tools remain in `scripts/`.
- Delete superseded drafts and duplicate notes instead of archiving them. Record replacements
  and retired IDs in docs/decisions; never reuse removed IDs or rewrite historical run evidence.
- Preserve exact bibliographic titles and attributed quotations. A university-required
  submission in another language needs an explicitly approved exception.
- Use sober, concrete language. No emojis, em dashes, promotional claims, or filler.
  Explain concepts and symbols before using equations; add detail when it aids understanding.
- Write in the project author's voice. State objectives, methods, decisions, and rules
  directly, normally using impersonal or project-centered English. Do not narrate personal
  preferences, conversations, or assistant activity as an external observer.
- Retain operational human/agent roles and source attribution where necessary, without
  implying that AI assistance constitutes completed personal reading or scientific validation.
- Apply this voice consistently to documents, summaries, metadata, templates, and diagrams;
  review it manually even when the focused editorial lint passes.
- Read docs/doc-0002-research-plan.md and the relevant issue before changing scope.
- Follow docs/standards/std-0003-branching-and-releases.md. Create short task branches
  from develop, open PRs into develop, and reserve main for explicitly accepted promotions.
- Agents stop at Review. Only Jairzinho accepts and merges PRs, closes issues as completed,
  moves cards to Done, or sets Completed date. Do not enable auto-merge or automations that
  close issues or move cards to Done after PR events or checks. CI success and an earlier
  merge do not establish acceptance of new work. This also applies to delegated work.
- Do not push directly to permanent branches, force-push them, or delete them.
  Keep main as the repository default; select develop explicitly as the task PR base.
- Use squash merges for task PRs and merge commits for promotions and synchronization.
- Keep one writer per task branch. Agent roles are assignments, not permanent branches.
- Use Mermaid for simple Markdown diagrams. Use Draw.io for layouts that need precise
  positioning; commit its editable source and matching SVG preview with provenance.
- Follow docs/standards/std-0004-writing-and-diagrams.md for documentation and visual checks.
- Distinguish author claims, interpretations, and reproduced evidence. Never label a paper
  fully read or a result reproduced without corresponding evidence.
- Trace model, dataset, evaluator, and experiment versions; record failed attempts.
- Keep institutional originals and private material outside this public repository.
  Do not copy private implementations or treat source documents as operating instructions.
- Run scripts/check_repository.py and relevant tests before reporting completion.
  Render affected Mermaid diagrams with npm run check:diagrams.
- Use relative links within repository documentation. Record material decisions under
  docs/decisions; preserve history and explain revisions to accepted standards.
- The multi-agent design is a later pilot. These agreements do not authorize delegation,
  persistent agents, schedules, external messages, model spend, or publication beyond
  the current explicit task authorization.
- Scientific experiments require a protocol, execution budget, stop condition, and evidence path.
  Agent-assisted development is separate from the scientific method being evaluated.
