---
id: pap-0001
title: "STOP: initial reading"
status: draft
revision: 1
created: 2026-09-29
updated: 2026-10-01
---

# STOP: initial reading


## Sources and status
[Paper v3](https://arxiv.org/abs/2310.02304v3), COLM 2024.
[Repository](https://github.com/microsoft/stop).
Partial reading: abstract, introduction, section 3, and algorithm 1.
Code: partial inspection of run_improver.py and eval_improver.py; not executed.
Guided discussion: pending. Source inspection does not establish completed personal reading.

## Documented mechanism
STOP uses an improver program I receiving a utility u, a solution s, and a model L.
It produces a candidate s'. Meta-utility measures how well the improver solves a task set D.
The improver then applies to its own code using that meta-utility. The model stays fixed;
the authors distinguish this scope from complete RSI. Source: section 3 and algorithm 1.

```text
s' = I(u, s, L)
meta(I) = average over (u,s) in D of u(I(u,s,L))
I[t+1] = I[t](meta, I[t], L)
```

Improvement is an objective, not a guarantee at each iteration. The algorithm does not
establish general optimality. Results and appendices still need critical reading.

## Questions for the next session
- How can improvement of a solution be distinguished from improvement of its constructor?
- Which small task would measure both?
- What does producing the improver cost before reuse?
- Which evaluation must remain inaccessible to proposed code?
- Which baseline isolates the effect of modifying the improver?
- What does each experiment establish, and what cannot be generalized?

## Session outline
Explain the problem, draw both levels, work through an original numerical example,
trace one code call, record questions, and select the next reading.
No third-party code has been executed and no original results are reported.

## Initial code trace
Verified commit: 0d6780c54306b2486dd36e9c4ae9b49aceb27ea4.
- [run_improver.py](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/run_improver.py):
  partial inspection of improver initialization and recovery.
- [eval_improver.py](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/eval_improver.py):
  locate the evaluation path before preparing reproduction.
- Pending: dependencies, task utilities, isolation, costs, and full correspondence
  between the publication version and repository.
