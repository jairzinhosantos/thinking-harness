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
implemented and checked offline. No live improvement result or paper reproduction is claimed.

`main` holds reviewed baselines. `develop` integrates ongoing work through task PRs.
Both task integration and baseline promotion require human review and a merge performed
by the human maintainer; passing CI does not merge a PR.
The initial bootstrap predates this workflow; it is not a formal research release.
See the [branch standard](docs/standards/std-0003-branching-and-releases.md).

## Start here

- Read the [research charter](docs/doc-0001-research-charter.md) and [initial plan](docs/doc-0002-initial-plan.md).
- Explore the [paper catalog](research/literature/catalog.csv) and [partial STOP review](research/literature/reviews/pap-0001-stop/README.md).
- Use the [literature map](research/synthesis/research-options.md#literature-map) to compare research roles and choose the next reading.
- Compare the [active cases](research/proposals/README.md), including the [debt negotiation model](research/proposals/case-0003-debt-negotiation/README.md).
- Read the [negotiation model](research/proposals/case-0003-debt-negotiation/modeling.md), then open the notebook in [English](research/proposals/case-0003-debt-negotiation/prompt-search.ipynb) or [Spanish](research/proposals/case-0003-debt-negotiation/prompt-search.es.ipynb). Live execution is pending local API-key setup.
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
| `docs/` | Charter, plan, operating model, standards, decisions, designs, and iteration notes |
| `research/` | Paper catalog, bilingual study notes, synthesis, proposals, and the case-specific negotiation prototype |
| `src/` | Future implementation of the selected method; currently a placeholder |
| `tests/` | Repository and diagram checks, plus offline evaluator, budget, and prompt-search tests |
| `configs/` | Shareable experiment configuration, without credentials |
| `benchmarks/` | Future reference tasks, scenarios, and evaluators |
| `environments/` | Local service definitions when the selected case requires them |
| `experiments/` | Protocols, execution manifests, and evidence-based reports |
| `data/` | Dataset catalog, provenance, licenses, splits, and checksums |
| `manuscripts/` | Academic requirements and thesis manuscript sources |
| `templates/` | Reusable paper-review, experiment, agent-handoff, and academic templates |
| `diagrams/` | Editable Draw.io sources and generated SVG previews |
| `assets/` | Original or licensed resources with recorded provenance |
| `scripts/` | Repository validation and documentation tooling |
| `deliverables/` | Issued, versioned documents and their manifests |
| `_archive/` | Retired material with a recorded reason and replacement |
| `.github/` | CI workflows and issue and PR templates |

The directory structure establishes boundaries; it does not imply that each component
has already been implemented. [Controlled documents](docs/catalog.csv) have stable IDs.

## Validate a change

Use Python 3.11 or newer. The repository checker uses the standard library; the prompt-search tests also require the case dependencies:

```sh
python3 -m pip install -r research/proposals/case-0003-debt-negotiation/requirements.txt
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
