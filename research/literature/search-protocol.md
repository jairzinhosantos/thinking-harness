# Initial search protocol

Objective: map methods for constructing and improving harnesses and select comparators.
Initial cutoff: 2026-09-29. Update the search when reviewing scope and before final evaluation.
The 2026-10-11 expansion verifies ten approved candidates; it does not extend an exhaustive
search cutoff or recover results from the inaccessible scheduled task.

## Sources
Official papers and proceedings, arXiv, OpenReview, ACL Anthology, PMLR, and repositories
linked by authors. Use search engines for discovery. Distinguish reviewed publications,
preprints, and technical projects.

## Families and queries
- "recursive self-improvement" AND (agent OR harness OR scaffolding)
- "agentic workflow" AND (optimization OR search OR planning)
- "harness" AND ("self-improving" OR adaptive OR evolution)
- "reinforcement learning" AND (agent OR workflow OR tool-use)
- References and citing works for central studies.

## Inclusion and extraction
Prioritize explicit mechanisms, relevance, and interpretable evaluation.
Record title, primary source, version, code, mutable object, fixed components, method,
evaluation, budget, limitations, and inclusion decision. Deduplicate versions of the same work.
A repository is not automatically a paper. Do not infer prestige, publication, or code
availability from a previous conversation.

## Independent states
- Bibliography: pending/verified.
- Reading: not-started/initial-review/partial/complete.
- Code: not-inspected/partial-inspection/inspected/not-applicable.
- Execution: not-run/smoke-tested/partial-reproduction/reproduced.
- Guided discussion: pending/discussed.

An initial source inspection does not establish complete personal reading or discussion.
Record assisted source inspection and guided discussion separately.
Verified bibliography establishes the source record; venue and code verification may remain pending.

## Classification and local originals

The [catalog](catalog.csv) separates these dimensions:

| Field | Meaning |
|---|---|
| `theme` | Primary lens: `harness-evolution`, `metaoptimization`, `evaluation-generalization`, `model-harness-coevolution`, or `data-synthesis` |
| `proximity` | `direct`: informs harness/improver design or evaluation; `complementary`: relevant extension with a different objective or training regime; `contextual`: background |
| `reference_role` | Intended use in the study, such as a baseline, adaptive-improver candidate, or evaluation design reference |
| `priority` | Reading order: P0 for the next comparison, P1 for supporting analysis, P2 for later extensions; not a quality rating |
| `classification_basis` | `preliminary-source-screening` identifies an assessment from abstracts, selected PDF passages, and available author-linked repository descriptions |
| `classification_notes` | Reason for inclusion and the main distinction or uncertainty to investigate |
| `pdf_filename` | Versioned original filename for local lookup; not a repository attachment |

The new classification fields are populated for pap-0014 through pap-0023. Blank fields
on earlier records mean classification is pending, not that those papers are less relevant.
Existing reading priorities and states remain unchanged. These classifications are working
interpretations, not completed paper reviews or conclusions about novelty.
Use the [research map](../synthesis/research-options.md#literature-map) to select the next reading.

Keep originals outside Git in `paper-library/originals/`, with
`<pap-id>-<short-slug>-v<arxiv-version>.pdf`, for example `pap-0019-rrsi-v3.pdf`.
Keep manual annotations separately in `paper-library/annotated/`. Never overwrite an original
with annotations or silently replace its version. Import the chosen original into Goodnotes;
an imported copy is not assumed to synchronize back to the local file.

Before registering a download, match its title and arXiv version stamp to the source record,
check that the PDF opens, and inspect its cover. A missing `code_url` means unverified here,
not that no implementation exists. An available repository does not establish reproducibility.

## Search record
Record query, source, date, retained candidates, and scope for each search.
Counts describe retained candidates, not every search-engine result.
Systematic screening remains pending; the initial batch verifies seed works.
Use PRISMA-ScR and PRISMA-S as reporting guidance, not certification.

## References
- [PRISMA-ScR](https://www.prisma-statement.org/scoping)
- [PRISMA-S](https://www.prisma-statement.org/prisma-search)
