---
id: dec-0007
title: "Case-local Python utilities"
status: in-review
revision: 1
created: 2026-10-16
updated: 2026-10-16
---

# Case-local Python utilities

Use `utils/` inside each implemented case for Python modules supporting its notebooks.
Keep the primary README, notebooks, inputs and configuration at the case root. Create
directories when resources exist; a Markdown-only case does not need implementation scaffolding.

For case-0003, move both `prompt_search.py` and `notebook_view.py` into `utils/`.
The first implements bounded search; the second formats evidence for reading. Their responsibilities
and the experimental protocol remain unchanged. The folder is local to this case, not a shared library.

Notebook loading, offline tests and future source-hash paths follow the new locations.
Historical results retain their original bytes, paths and hashes. A reading-copy PDF may have
its source links updated without changing the evidence it presents.

Repository checks and export tooling stay in `scripts/`; tests stay in `tests/`.
Original paper source checkouts retain their upstream structure. Extract shared code only when
actual reuse justifies it, as described in [project evolution](../project-evolution.md).
