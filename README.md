# Thinking Harness

Welcome to Thinking Harness, an applied research project on the construction and
improvement of agentic harnesses. This repository brings together literature reviews,
experimental protocols, reference implementations, and thesis materials.

A harness is the application layer around a model: instructions, tools, execution flow,
memory, controls, and evaluation. The project studies how to construct or improve that layer
under measurable quality, cost, and human-review constraints.

## Current status

The project is in its research preparation stage. The thesis case, method, framework,
and final contribution remain open. A bounded negotiation prompt-search prototype is
implemented and has one live pilot. Its token guard stopped the search without an accepted
candidate or final comparison. No improvement or paper reproduction is claimed.

`main` holds reviewed baselines. `develop` integrates ongoing work through task PRs.
Both task integration and baseline promotion require human review and a merge performed
by the human maintainer; passing CI does not merge a PR.
The initial bootstrap predates this workflow; it is not a formal research release.
See the [branch standard](docs/standards/std-0003-branching-and-releases.md).

## Start here

- Read the [research charter](docs/doc-0001-research-charter.md) and [research plan](docs/doc-0002-research-plan.md).
- Explore the [paper catalog](research/literature/catalog.csv) and [partial STOP review](research/literature/reviews/pap-0001-stop/README.md).
- Use the [literature map](research/synthesis/research-options.md#literature-map) to compare research roles and choose the next reading.
- Compare the [case index](research/cases/README.md), including the [debt negotiation model](research/cases/case-0003-debt-negotiation/README.es.md).
- Read the [negotiation model](research/cases/case-0003-debt-negotiation/README.es.md#modelamiento), then open the notebook in [English](research/cases/case-0003-debt-negotiation/prompt-search.ipynb) or [Spanish](research/cases/case-0003-debt-negotiation/prompt-search.es.ipynb). Both notebooks replay the first measured run without API calls; the search stopped at its token limit with no accepted candidate.
- Follow work in the [Project](https://github.com/users/jairzinhosantos/projects/2).
- Before contributing, read [AGENTS.md](AGENTS.md), the [operating model](docs/operating-model.md),
  and the [writing and diagram standard](docs/standards/std-0004-writing-and-diagrams.md).

## Research workflow

Each cycle produces evidence that helps retain, refine, or reject a research direction.
The thesis will select one bounded case; the public laboratory can explore additional cases.

```mermaid
flowchart LR
    L[Literature review] --> P[Question and protocol]
    P --> E[Pilot and evaluation]
    E --> D[Evidence and decision]
    D --> L
```

## Repository guide

| Directory | Contents and purpose |
|---|---|
| `research/` | Literature, case studies, prototypes, evidence and synthesis |
| `docs/` | Project conventions, decisions, designs, academic requirements and templates |
| `scripts/` | Validation, notebook diagram rendering and PDF export tools |
| `tests/` | Offline repository checks and tests of implemented case behavior |
| `.github/` | CI workflows and issue/PR templates |

Each case and reviewed paper has its own folder. The README presents the main study;
related documents and resources stay beside it. Cases retain their scientific status:
reorganization does not turn a proposal into an experiment or a pilot into a validated result.
[Controlled documents](docs/catalog.csv) retain stable IDs when their filenames change.

The [evolution plan](docs/project-evolution.md) records the present structure and the conditions
for adding shared code, benchmarks, experiment infrastructure or formal deliverables.
Folders are added when they contain useful work.

## Validate a change

Use Python 3.11 or newer. The repository checker uses the standard library; the prompt-search tests also require the case dependencies:

```sh
python3 -m pip install -r research/cases/case-0003-debt-negotiation/requirements.txt
python3 scripts/check_repository.py
python3 -m unittest discover -s tests/unit -v
```

Mermaid rendering requires Node.js 22 and the pinned development dependencies:

```sh
npm ci
npm run check:diagrams
```

CI runs these checks for `main`, `develop`, and PRs targeting either branch. It validates
local references, document metadata, catalogs, recurring external-narration phrases,
Draw.io structure and previews, and Mermaid rendering. It does not run models or consume cloud resources.

## Working with agents

The [agentic development strategy](docs/designs/doc-0003-agentic-development-strategy.md)
proposes bounded tasks, a builder, independent QA, and human review. It is a future pilot;
no persistent agents or scheduled execution are enabled.
[Progress measurement and HITL options](docs/designs/doc-0004-progress-and-hitl.md)
remain open for a separate decision.

## Public scope

English is the primary project language. Each paper review also has a linked Spanish
translation for study; see the [paired-review convention](docs/standards/std-0004-writing-and-diagrams.md#paper-review-translations).
Private data, credentials, institutional source
files, and working conversations stay outside this repository. A private extension may
later consume an identified version of this public core.

## License and citation

Original repository material is licensed under [MIT](LICENSE). Linked papers and external
software retain their own licenses. Use [CITATION.cff](CITATION.cff) and identify the commit
or release used when citing this project.
