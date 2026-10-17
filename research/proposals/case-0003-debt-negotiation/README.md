---
id: case-0003
title: "Synthetic debt negotiation harness"
status: in-review
revision: 1
created: 2026-10-16
updated: 2026-10-16
---

# Synthetic debt negotiation harness

English (primary) | [Español](README.es.md)

## 1. Case and objective

A fictional lender offers payment plans for three debts from a previous year. The assistant
seeks an explicit agreement for the largest feasible debt, within permitted terms and the
customer's stated capacity. A refusal may require clarification or another plan before
considering a smaller debt. A no-agreement outcome is valid when the customer declines or no plan fits.

| Debt | Amount in fictional units | One payment | Two equal monthly payments |
|---|---:|---:|---:|
| A | 200 | 200 | 100 each |
| B | 300 | 300 | 150 each |
| C | 600 | 600 | 300 each |

Initial simplification: at most one debt per agreement, first payment in the current period,
second in the next, unchanged monthly capacity, no interest, discounts, or real payments.
Amounts, rules, and conversations are synthetic; no institutional data or implementation is reused.
An agreement measures committed amount, not money recovered or future repayment probability.

**Research question:** can changes to a bounded negotiation harness improve valid agreements
and interaction quality compared with a fixed harness under the same resources?
This is an active candidate alongside [code repair](../case-0001-code-repair-harness.md),
not a final thesis-method selection. The earlier [service case](../case-0002-service-workflow-harness.md)
is retained as a superseded reference.

## 2. Model and derived features

| Part | Initial definition |
|---|---|
| Visible inputs | Debt list, authorized plans, customer messages, and conversation history |
| Derived features | Proposed installment, installment minus stated capacity, known refusal reason, remaining permitted plans, and remaining turns |
| Tools | `list_debts`, `get_allowed_plans`, `present_offer`, and `record_acceptance` in a simulated backend |
| Output | Explicitly accepted debt and plan, or a truthful no-agreement outcome |
| Mutable harness | Initially one bounded offer-selection policy: ask, choose a permitted plan, or stop |
| Fixed environment | Model/version, tool contracts, permitted plans, consent checks, budgets, customer simulator, and evaluator |
| Future optimizer | Proposes candidate changes to that policy; cannot edit the environment or final evaluation |

Capacity is unknown until disclosed; a missing value is not zero. The agent cannot read
hidden simulator preferences or reference answers. Example: a 300 installment and a stated
capacity of 150 produce an installment gap of 150. This transformation is feature engineering;
the full input/tool/output definition is system modeling. It does not require model training.

```mermaid
flowchart TD
    S[Visible task and conversation] --> F[Extract observable features]
    F --> H[Harness: ask, offer, or stop]
    H --> T[Fixed simulated tools]
    T --> U[Simulated customer response]
    U --> S
    H --> O[Agreement or no agreement]
    O --> E[Independent evaluator]
    R[Protected scenario rules] --> E
```

## 3. Seed harness and construction

The harness does not start from nothing. `H0` is a minimal runnable scaffold with fixed tool
interfaces, conversation state, stop limits, and a simple initial offer policy. It can be
written manually or generated from a specification and then reviewed. The pretrained model
already supplies language capability; neither its weights nor the tool backend are rebuilt.

A first policy might offer C in one payment, clarify a rejection, try an affordable permitted
plan, then consider B or A. This is a baseline hypothesis, not a prescribed optimal conversation.
For example, after a disclosed capacity of 150, C in two payments is still infeasible, while
B in two payments fits. Acceptance must still be explicit.

A candidate `H1` might ask about capacity before selecting a plan or retain the refusal reason
more reliably. Only the declared offer-policy surface may change. Better wording, a valid
agreement, or passing one scenario does not by itself establish a better harness.

## 4. Proposed golden scenarios and evaluator

The golden set would specify initial state, hidden customer behavior, visible disclosures,
permitted outcomes, and evaluation rules. It is not one mandatory transcript: different
conversations may satisfy the same outcome. These are proposed fixtures, not a built or
validated dataset. Capacity is disclosed when asked; the first three profiles accept a valid,
affordable offer, while the fourth declines every offer.

| Profile | Reference behavior under these assumptions |
|---|---|
| Monthly capacity 300 | C in two payments is feasible and preferred by the lender's objective |
| Monthly capacity 150 | B in two payments is the largest feasible agreement |
| Monthly capacity 80 | No authorized plan fits; truthful no agreement |
| Declines negotiation | Stop without an agreement, regardless of capacity |

The fixed evaluator reads the conversation trace and final backend state. It first checks
allowed terms, explicit consent, no fabricated outcome,
capacity consistency, and turn limits. A violation invalidates the result. Among valid runs,
report committed amount and agreement rate on eligible scenarios separately from correct
no-agreement outcomes. Also record repeated rejected offers, unnecessary turns, tokens, and
latency. A short human-reviewed rubric would assess clarity, relevance, and response to refusal;
an uncalibrated model judge is insufficient. An always-stop policy must not score as success
on eligible, willing profiles.

Reserve development scenarios for construction feedback, validation scenarios for candidate
selection, and untouched final scenarios for the final comparison. Group related profile
variants when splitting. Final answers and hidden state remain outside constructor input.
Synthetic behavior demonstrates simulator performance, not effectiveness with real customers.

## 5. Improvement and recursive improvement

Golden scenarios supply evidence; they do not construct the workflow by themselves. A fixed
coordinator gives development failures and the editable harness source to a constructor.
A constructor agent using a fixed LLM proposes a candidate; protected evaluation checks it
on multiple scenarios.
A predefined selection rule retains or rejects it within a search budget. The final test set
is not used in that loop. Improvement is not guaranteed.

```mermaid
flowchart TD
    H[Current harness Ht and development feedback] --> B[Constructor proposes a policy change]
    B --> C[Separate candidate copy]
    C --> E[Fixed evaluator: development and validation]
    E --> G{Meets predefined selection rule?}
    G -->|Yes| N[Keep candidate as next Ht]
    G -->|No| K[Retain current Ht and record failure]
    N --> H
    K --> H
    H -->|After search ends| F[Freeze version for untouched final evaluation]
```

Two future stages must remain distinct:

- **Automatic harness improvement:** a fixed constructor improves the negotiation policy.
- **Recursive construction:** the accepted harness also runs the constructor that builds its
  successor. Merely passing its source to an unchanged constructor is insufficient.

The negotiation policy alone does not necessarily help construct code. A recursive study
would need a shared component, such as feedback selection or planning, exercised in both
negotiation and construction. It would compare a constructor running through `H0` against
one running through `Ht`, with the same total budget. That component and protocol remain open.
A negotiation loop alone therefore does not yet demonstrate RSI.

## 6. Delivery and next steps

Only this bilingual specification and diagrams exist in this folder. Next, refine the
scenario schema and evaluator examples; then implement `scenarios.json` and `demo.py` here.
The first demo would calculate features, run a fixed policy against a deterministic customer,
and print decisions and evaluation. It would not rewrite code or call a model.

A deterministic baseline may already solve all four proposed profiles. These fixtures first
check the measurement setup; they do not establish a useful optimization problem. Further
scenario design must reveal a measurable limitation before testing improvement.

Later optimization requires a separate approved protocol, resource budget, and stop rule.
Keep traces of rejected candidates and compare against the fixed baseline. A successful demo
is a measurement instrument, not a completed self-improvement solution.

The compact layout is scoped to this case; PRs #26 and #27 remain separate proposals.
The agent prepares work up to Review. Only Jairzinho decides PR integration, issue completion,
Done, and Completed date. No automatic closure or merge is enabled.
