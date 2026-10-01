---
id: doc-0001
title: "Research charter"
status: draft
revision: 1
created: 2026-09-29
updated: 2026-10-01
---

# Research charter


## Motivation
Building agentic solutions requires designing and adjusting instructions, tools, workflows,
memory, controls, and evaluation. The objective is to study how to automate part of this work and
measure its relationship with quality, cost, and human intervention.

## Provisional question
Under a bounded budget, which mechanism can construct or improve a harness for a specific
family of tasks compared with a defined baseline?

## Open alternatives
Recursive improvement, fixed-improver optimization, evolutionary computation, planning,
and reinforcement learning (RL). Fixed models are the starting point for feasibility;
training a controller or model needs justification and a resource estimate.
Feedback alone does not imply RL.

## Scope to decide
Select a primary case among a simulated process, a game, or coding tasks.
Institutional collaboration is optional. Do not implement multiple frameworks in advance.
Compare the candidate contribution with close prior work and an independent evaluation.

## Candidate measures
Quality, time to acceptance, human intervention, total cost, generalization, and stability.
Define these operationally before confirmatory comparisons.

## Proposed method
Use DSRM for construction and evaluation, FEDS for evaluation planning, and selected
PRINCE2 and Kanban practices for management. This combination is an adaptation for this project,
not a single certified standard.

## Methodological references
- [DSRM](https://doi.org/10.2753/MIS0742-1222240302)
- [FEDS](https://doi.org/10.1057/ejis.2014.36)
- [Kanban](https://kanbanguides.org/the-kanban-guide/)
