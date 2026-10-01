# Working agreements

- Use English for all project-authored content: prose, code, comments, docstrings,
  configuration descriptions, diagrams, commits, issues, and PRs.
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
- Read docs/doc-0002-initial-plan.md and the relevant issue before changing scope.
- Follow docs/standards/std-0003-branching-and-releases.md. Create short task branches
  from develop, open PRs into develop, and reserve main for explicitly accepted promotions.
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
