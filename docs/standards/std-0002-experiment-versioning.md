---
id: std-0002
title: "Experiment versioning and resources"
status: in-review
revision: 2
created: 2026-09-29
updated: 2026-10-16
---

# Experiment versioning and resources


## Version layers
Identify code by commit. Use SemVer for published software once an interface exists;
initial software development uses 0.x. Documents use rNNN revisions.
Protocols, cases, datasets, and evaluators carry an ID and revision or hash.
Separate the procedure being evaluated from its executions and saved prompt versions:

| Layer | Convention | Example |
|---|---|---|
| Protocol | `<case-id>-<study-slug>-vN`; increment for material changes | `case-0003-prompt-search-v3` |
| Run | `YYYYMMDDTHHMMSSZ-<8-lowercase-hex>` in UTC | `20261017T011558Z-f5eca942` |
| Prompt version | `p` plus a zero-padded integer of at least three digits, scoped to a run | `p000`, `p001`, `p002` |

Runs stay under their case's `results/<run-id>/` when published. Local raw output may stay
in ignored `runs/`; publication retains the run ID and documents sanitization and provenance.
Prompt versions live under `prompts/`, with their parent, hash and evaluation in the run record.
For the current prompt-search pilot, `p000` is the seed and `p001` is the generated baseline;
later IDs identify proposals, not accepted improvements. Other artifact types define their
local identity in their protocol instead of adopting a prompt-specific prefix.

A standalone controlled protocol document may retain an `exp-NNNN` document ID. It is not
a run ID and is not required for every small pilot: the case guide may contain the protocol,
provided the runner records its version and source hashes. Existing IDs remain valid.
Each new execution or retry gets a new run ID; link retries to the earlier attempt in provenance.
Record costs and failures. Do not rename historical run or prompt IDs to apply this convention.

## Minimum manifest
Record commit and local changes, protocol, case, resolved configuration, model/provider/parameters,
dataset/splits/checksums, evaluator, seeds, image digest, hardware, budget, start/end, and
termination reason. A seed does not guarantee exact reproducibility with a remote provider.
Do not overwrite evidence from an issued run.

## Resources
Prefix: th. Compose projects: th-case0001-dev-01 or th-case0001-eval-01.
Functional service names: agent, evaluator, request-api, postgres.
Avoid fixed container_name values. Isolate ports and storage between runs.
Labels: project, case-id, experiment-id, run-id, environment, owner, expires-at.
Adapt cloud resource names to provider restrictions; keep versions in manifests.
Pushing code does not automatically start cloud resources or model calls.

## Revision history

Revision 2 separates protocol, run and prompt identities and replaces the unused composite
run/candidate naming from revision 1. The recorded pilot is unchanged; see
[dec-0006](../decisions/dec-0006-active-research-cleanup.md).

## References
- [SemVer](https://semver.org/)
- [Compose project names](https://docs.docker.com/compose/how-tos/project-name/)
- [Azure naming](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
