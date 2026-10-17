# Negotiation objective

Generate instructions for the next turn of a synthetic debt negotiation assistant.
Seek an explicit agreement for the largest feasible debt, while respecting capacity,
authorized terms, and the customer's choice. No real institution or payment is involved.

## Fixed constraints

- Debts A, B, C are 200, 300, 600 fictional units. One payment or two equal monthly
  payments are allowed. The first payment is this month; capacity stays constant.
- Negotiate at most one debt. Do not invent discounts, interest, terms, or executions.
- Ask for monthly capacity when it is unknown. Unknown does not mean zero.
- When capacity is known, offer the largest feasible debt. For this pilot, prefer
  one payment when affordable; otherwise use two. This tie-break is a modeling choice.
- Clarify an ambiguous rejection. Stop after an explicit refusal to negotiate or when
  no plan fits. A missing agreement must never be represented as an acceptance.
- Confirm an agreement only after explicit consent to that exact debt and plan.
- Keep the next message brief and consistent with the structured decision.

## Mutable component

Only the negotiator's policy prompt may change. The Python runtime, response schema,
objective, scenarios, model configuration, evaluator, and optimizer instructions stay fixed.
This document is loaded explicitly as a task specification. It is not an installed agent skill.

## Evidence

Evaluate behavior, not literal reference wording. A generic greeting is a teaching example.
The experimental baseline is a prompt generated once from this objective and development
examples. Iteration must be compared against that baseline. No improvement is guaranteed.
