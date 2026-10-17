# Research options

This matrix records working hypotheses, not conclusions about novelty.

| Option | Question | Evidence needed |
|---|---|---|
| Fixed improver | What feedback improves in a bounded harness | Baseline and per-candidate cost |
| Recursive improvement | What modifying the improver adds | Fixed-improver ablation with comparable budgets |
| Evolution | What maintaining a population or archive adds | Comparison with local search |
| Planning | What planning construction operations adds | Action model and search cost |
| RL | What a construction policy can learn | Training cost and generalization across tasks |

Candidate cases: a small game, simulated process, or coding tasks.
Select for evaluability, cost, problem relevance, and reproducibility.
Review Self-Harness before claiming harness improvement is an unexplored gap.

## Literature map

Question: what does improving the improver add over a fixed improvement procedure,
under comparable budgets and evaluation on unseen tasks?

The 2026-10-11 screening adds ten distinct works to the thirteen existing records.
The [catalog](../literature/catalog.csv) stores classification and reading states;
the [search protocol](../literature/search-protocol.md#classification-and-local-originals)
defines their meaning. The map below explains provisional research roles from abstracts,
selected PDF passages, and author-linked repository descriptions. It does not report
full reviews, reproduced results, or proven applicability to the proposed case.

| Paper and pinned source | Priority | Proximity | Role and key distinction |
|---|---|---|---|
| pap-0020 [Meta-Harness v1](https://arxiv.org/abs/2603.28052v1) | P0 | Direct | Baseline candidate: search over harness code with prior scores and traces. Fixed proposal guidance can still use changing feedback. |
| pap-0021 [MetaSkill-Evolve v1](https://arxiv.org/abs/2607.05297v1) | P0 | Direct | Adaptive-improver candidate: task skills and slower meta-skills co-evolve under one frozen backbone. The mutable objects are skill files. |
| pap-0017 [Mixture of Self-Improving Branches v1](https://arxiv.org/abs/2609.37834v1) | P0 | Direct | Adaptive-improver candidate: branch proposal guidance and development subsets evolve. Optimizer code is not rewritten. |
| pap-0019 [RRSI v3](https://arxiv.org/abs/2609.24972v3) | P0 | Direct | Regularized-search comparator: constrain proposals and selection to examine generalization and execution cost. |
| pap-0015 [SO-RSI v2](https://arxiv.org/abs/2610.05701v2) | P0 | Direct | Diagnostic-search comparator: investigate recurring failures before editing workflows. "Second-order" denotes diagnostic inquiry, not automatically self-modifying optimizer code. |
| pap-0018 [Harness Evolution as Learning v1](https://arxiv.org/abs/2609.36892v1) | P1 | Direct | Evaluation and theory: approximation, generalization, and optimization limits in personal-agent settings. Check whether its assumptions transfer to code repair. |
| pap-0022 [RHI v1](https://arxiv.org/abs/2607.15524v1) | P1 | Direct | Prompt-harness comparator: revise an agent-loop specification through pairwise feedback. Separate prompt evolution from optimizer-code evolution. |
| pap-0023 [HELIX v1](https://arxiv.org/abs/2608.13951v1) | P1 | Complementary | Traceable harness representation and training-data extraction. Its reported code-repair experiment covers one evolution round, not a demonstrated repeated co-evolution loop. |
| pap-0014 [MASS v1](https://arxiv.org/abs/2610.12176v1) | P2 | Complementary | Training extension: alternate workflow evolution and fine-tuning. Model changes introduce a different comparison and compute budget. |
| pap-0016 [Reasoning Data Synthesis v1](https://arxiv.org/abs/2610.03548v1) | P2 | Complementary | Data-generation extension: evolve synthesis skills and workflows while weights and verification criteria remain fixed. Producing harder tasks differs from solving a fixed repair suite. |

New to the catalog does not mean newly published in October. Meta-Harness dates from March;
MetaSkill-Evolve and RHI from July; HELIX from August. Versions are pinned for repeatable
reading. No peer-reviewed venue is asserted for this batch.

## Reading sequence and evidence to extract

Continue STOP and Self-Harness before opening several full reviews at once. Then read
Meta-Harness, MetaSkill-Evolve, Mixture, RRSI, and SO-RSI in that order. Priority is adjustable;
Harness Evolution as Learning can move earlier when formalizing generalization assumptions.

For each comparison, identify:

1. **Mutable object:** task solution, harness code, proposal instructions, meta-skills,
   evaluation data, or model weights. Record exactly what stays fixed.
2. **Improvement operator:** who constructs the next version, what changes its behavior,
   and whether it runs its own updated procedure in subsequent rounds.
3. **Attribution:** compare fixed and adaptive improvers with the same backbone, starting
   harness, task splits, and budget. Isolate changes to proposal policy, development subsets,
   routing, and training instead of attributing all gains to recursion.
4. **Generalization and cost:** distinguish search/development feedback from held-out tests;
   report search cost separately from the cost of executing the selected harness.

Mixture's Section 4.5 factorial analysis is particularly relevant: it separates proposal
adaptation from development pruning and reports that proposal adaptation alone does not
improve on its independent-search comparison. This is a reason to study the ablation,
not evidence that an adaptive improver will always help our case.

## Source and implementation boundaries

- Five author-linked repositories were verified at the landing-page level:
  [MASS](https://github.com/SakanaAI/mass),
  [Harness Evolution as Learning](https://github.com/ZyGan1999/self-evolving-harness-as-learning),
  [RRSI](https://github.com/google-research/rrsi),
  [Meta-Harness artifact](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact), and
  [HELIX](https://github.com/HKUDS/HELIX). Implementation inspection and execution remain pending.
- The Meta-Harness link provides an optimized Terminal-Bench harness artifact. Do not treat
  it as a verified release of the complete search system. MASS also documents differences
  between its packaged implementation and reported experiments.
- Code links for the remaining five works remain unverified. No missing link is filled
  from a similarly named repository or a cited baseline.
- All ten originals remain in the local PDF library, outside Git. No review completion,
  guided discussion, code inspection, or reproduction state advances from this screening.
- The initial thirteen records still have unresolved venue/code checks and incomplete
  BibTeX coverage. This expansion does not complete the broader bibliographic-verification issue.
