---
id: std-0003
title: "Branching and formal baselines"
status: accepted
revision: 1
created: 2026-09-30
updated: 2026-10-01
---

# Branching and formal baselines


## Permanent branches

| Branch | Purpose | Entry condition |
|---|---|---|
| main | Reviewed baselines for presentation, submission, or release | Promotion PR, passing CI, and explicit human acceptance |
| develop | Integrated research and implementation work | Task PR, passing CI, and review of its criteria |

main remains the repository default. Select develop explicitly when opening a task PR.
The bootstrap commits predate this workflow and are not a formal scientific release.

```mermaid
flowchart LR
    D[develop] --> T[Task branch]
    T --> Q[Task PR and checks]
    Q --> D
    D --> P[Promotion PR]
    P --> A[Human acceptance]
    A --> M[main]
    M --> S[Sync PR to develop]
    S --> D
```

## Task branches
Use `<type>/<issue-number>-<short-description>` in lowercase English.
Types: docs, research, feat, fix, chore, refactor, and test.
Example: docs/12-english-documentation. Agent roles are issue assignments, not branch names.
Create from current develop, keep one bounded objective, and delete after integration.
There is one writer per task branch; concurrent agents use separate branches or checkouts.

```sh
git fetch origin
git switch -c docs/12-english-documentation origin/develop
# Edit, validate, commit, and push the task branch.
gh pr create --base develop --head docs/12-english-documentation --body-file pr-body.md
```

The command is an example; allocate the actual issue and branch before using it.
Commits use `type: concise English description`; an optional scope is allowed.

## Merge and review rules
Squash task PRs into develop. Use merge commits for develop-to-main promotions and
main-to-develop synchronization so shared ancestry is preserved.
Do not squash or rebase a permanent-branch promotion. Do not enforce linear history on
permanent branches because synchronization uses merge commits.
A task PR states its problem, result, issue, evidence, checks, and remaining decisions.
Use `Refs #N`; close the task issue explicitly after acceptance into develop.

main and develop require PRs, passing Repository checks (job: validate), up-to-date
branches, and resolved conversations. Disable force pushes and deletion; apply protection
to administrators too. Initially require zero GitHub approval reviews to avoid a sole
maintainer being unable to approve their own PR. This does not remove human review:
record explicit human acceptance in the promotion PR before merging it.
Branch protection enforces checks and PR use; it cannot establish scientific validity
or verify that a conversational acceptance occurred.

## Formal promotion
1. Select a coherent snapshot of develop; its criteria must pass on the exact proposed head.
2. Open a promotion PR to main with scope, validation, known limits, and deliverable references.
3. Obtain explicit human acceptance for that snapshot. Material changes invalidate it.
4. Merge using a merge commit and tag the accepted main commit.
5. Synchronize main back into develop through a PR, also using a merge commit.

Research tags use `milestone/<name>-rNNN`, such as milestone/research-plan-r001.
Software tags use `vMAJOR.MINOR.PATCH` when a software release exists.
Never move an issued tag; supersede it with a new revision. Branches are mutable working
references; cite a commit or tag in a delivery or experiment manifest.

## Exceptions
If presentation preparation must proceed independently, create a temporary
release/<milestone>-rNNN branch from the chosen develop commit. It receives only baseline
preparation fixes, is promoted by PR, synchronized back, then deleted.
For an urgent formal-baseline correction, branch fix/<issue>-<description> from main,
review through a PR into main, issue a new revision, then sync to develop.
Do not introduce these branches until needed.

## Reference
[GitHub branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
