---
id: std-0002
title: "Experiment versioning and resources"
status: accepted
revision: 1
created: 2026-09-29
updated: 2026-09-30
---

# Experiment versioning and resources


## Version layers
Identify code by commit. Use SemVer for published software once an interface exists;
initial software development uses 0.x. Documents use rNNN revisions.
Protocols, cases, datasets, and evaluators carry an ID and revision or hash.
A run uses exp-NNNN-YYYYMMDDtHHMMSSz-<unique-suffix>, in UTC.
Candidates use cand-NNNN within a run; record parent_id and the modification.
Each retry has a new identity and links to the previous attempt. Record costs and failures.

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

## References
- [SemVer](https://semver.org/)
- [Compose project names](https://docs.docker.com/compose/how-tos/project-name/)
- [Azure naming](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
