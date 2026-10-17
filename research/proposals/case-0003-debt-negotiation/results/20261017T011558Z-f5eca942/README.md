# First live prompt-search run

English (primary) | [Español](README.es.md) | [Case](../../README.md) | [Modeling](../../modeling.md) | [Notebook](../../prompt-search.ipynb)

One English notebook was executed locally with OpenAI on October 16, 2026 (America/Lima).
The run ID uses UTC. Both published notebooks replay this same evidence without further API calls.

## Observed result

No candidate replaced the one-shot baseline. The search stopped on the token-reservation guard
before completing round two or reaching the final test. A higher validation score did not
satisfy the zero-violation selection rule. No final or generalization improvement is established.

| Version | Stage | Validation successes | Violating replies | Decision |
|---|---|---:|---:|---|
| p000 | Generic seed | Not evaluated | Not evaluated | Teaching seed |
| p001 | One-shot baseline | 9/12 (75.0%) | 1 | Retained incumbent |
| p002 | Round 1, candidate 1 | 9/12 (75.0%) | 2 | Not admissible |
| p003 | Round 1, candidate 2 | 8/12 (66.7%) | 2 | Not admissible |
| p004 | Round 2, candidate 1 | 10/12 (83.3%) | 1 | Not admissible |

The baseline offered B in one payment rather than the larger feasible C in two payments in
both repetitions of one validation case. In another repetition it offered an installment of
100 despite a stated capacity of 70. These checks distinguish the objective from fluent wording.
The optimizer received development feedback only, not these validation traces.

## Budget and limits

- Model: `gpt-5.4-mini-2026-03-17`, used for all three roles.
- 148 API calls; 83,815 provider-reported input/output tokens.
- Estimated cost: USD 0.10261125, using the recorded uncached input/output rates.
- Limits: USD 1 and 100,000 tokens across optimizer, negotiator, judge and final comparison.
- Next request reservation: 24,329 tokens; consumed plus reserved would be 108,144.
  The request was not sent. The binding limit was tokens, not dollars.
- Final test: not reached. The run is incomplete, with no uncertain provider usage.

This is a small synthetic pilot with an uncalibrated model judge. Two repetitions do not
establish statistical significance. Runtime and prompt sources are linked by hashes to the
source commit; this experiment is neither a trained model nor recursive self-improvement.

## Evidence

- [Report](report.json): evaluations, replies, judge rationales, settings and selection trace.
- YAML versions: [p000](prompts/p000.yaml), [p001](prompts/p001.yaml), [p002](prompts/p002.yaml), [p003](prompts/p003.yaml), [p004](prompts/p004.yaml).
- [Usage ledger](usage.jsonl): reservations and provider-reported usage, without request bodies or IDs.
- [Provenance](provenance.json): source/report hashes, execution overrides and budget diagnosis.

Raw requests and the local credential remain outside Git. No additional live run was made
for Spanish. Before another experiment, review the observed failures, judge calibration and
a budget that leaves room for final testing. Keep this failed search as evidence.
