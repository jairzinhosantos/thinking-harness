---
id: pap-0001
title: "STOP: mechanism, code trace, and evaluation"
status: in-review
revision: 4
created: 2026-09-29
updated: 2026-10-10
---

# STOP: mechanism, code trace, and evaluation

English (primary) | [Español](README.es.md)

STOP is a useful reference for separating a task solution from the program that improves it.
For thinking-harness, the immediate question is which component should be allowed to change
and how its improvement can be measured independently of the search that produced it.
This review prepares that discussion; it does not select the thesis method.

**Study path:**

1. [Sources and review state](#1-sources-and-review-state)
2. [Contribution and evidence](#2-contribution-and-evidence)
3. [Mechanism step by step](#3-mechanism-step-by-step)
4. [Original code walkthrough](#4-original-code-walkthrough)
5. [Local inspection and execution](#5-local-inspection-and-execution)
6. [Critical reading and application](#6-critical-reading-and-application)

STOP-only layout pilot: the review and code analysis share this README. Other papers
and the general review template retain their current structure.

## 1. Sources and review state

**Paper:** Eric Zelikman, Eliana Lorch, Lester Mackey, and Adam Kalai,
*Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation*.
[Version 3, 16 August 2024, COLM 2024](https://arxiv.org/abs/2310.02304v3).
The bibliographic key is `zelikman2023stop`, retaining the initial preprint year.

**Affiliations printed on page 1 of v3:**

| Author | Listed affiliation | Institution type / note |
|---|---|---|
| Eric Zelikman | Stanford University | University; starred note: work done at Microsoft Research New England |
| Eliana Lorch | Not stated in the paper header | No affiliation inferred from the repository owner |
| Lester Mackey | Microsoft Research | Industrial research organization |
| Adam Kalai | OpenAI | AI research company; starred note: work done at Microsoft Research New England |

These are the affiliations in this paper version, not a claim about current employment.
The repository's `microsoft` namespace does not make every author a Microsoft employee.
Source: [v3 title page and affiliation footnote](https://arxiv.org/pdf/2310.02304v3#page=1).

**Code:** [microsoft/stop](https://github.com/microsoft/stop/tree/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4),
commit `0d6780c54306b2486dd36e9c4ae9b49aceb27ea4`. All code links below use this snapshot.

| Activity | State and scope |
|---|---|
| Assisted source inspection | Abstract, introduction, sections 3-8, Algorithm 1, Figures 2 and 4, Table 1, and Appendix K; partial inspection of A.1-A.2 |
| Complete paper reading | Partial; related work, proofs, and remaining appendices need further study |
| Static code inspection | Runner, seed improvers, meta-utility, parity utility, model wrapper, loader, configuration, and transfer entry point |
| Execution | Upstream code not run; no third-party imports, model calls, or scientific experiments. Only the original deterministic teaching snippets in section 3.2 were executed to check their values |
| Guided discussion | Pending; document preparation does not establish completed personal reading |
| Reproduction | No reproduced results |

`author-claim` denotes a reported finding. `interpretation` denotes project analysis or
an illustrative proposal. `static-inspection` denotes directly inspected source behavior,
which remains unverified at runtime. `reproduced-result` is reserved for measured evidence.

## 2. Contribution and evidence

**Author-claim.** The central contribution is to use an improver to revise its own code,
while keeping the language model fixed. The paper builds the argument in three parts:

- **Mechanism, sections 3-4:** define a task utility, an improver, and a meta-utility that
  scores the solutions produced by that improver. Use this meta-utility to search for a
  better improver. The editable object is software, not the model's weights.
- **Empirical evidence, section 5:** examine improvement on one task family, transfer to
  other tasks, and dependence on the underlying model. These answer different questions.
- **Limits, sections 6-7 and appendices A/K:** examine evaluator exploitation, constraint
  circumvention, generalization assumptions, and computational cost. Observed improvement
  is not a guarantee that every recursive update succeeds.

```mermaid
flowchart TD
    Q[Can an improver improve its own code?] --> M[Sections 3-4: define the mechanism]
    M --> E[Section 5: test the resulting improvers]
    E --> A[5.1: same task family]
    E --> B[5.2: transfer to new tasks]
    E --> C[5.3: weaker models]
    M --> L[Sections 6-7 and appendices: limits and cost]
```

The evidence should be read at its reported scope:

| Evidence | What is evaluated | What it does not establish |
|---|---|---|
| Section 5.1: noisy parity with GPT-4 | Mean performance over five independent STOP runs; comparison with the seed, chain-of-thought, and greedy improvers | Every individual trajectory improves monotonically |
| Section 5.2: transfer | One selected evolved improver on five new tasks | The distribution of transfer performance across all evolved improvers |
| Section 5.3: model dependence | Failures with weaker models | Any model can reliably improve its scaffolding |
| Appendix A: theory | Generalization under assumptions including bounded programs and independently sampled tasks | Unconditional guarantees for practical recursive updates |
| Appendix K: cost | Roughly 3,000 GPT-4 calls per iteration per run | A current monetary estimate or an equivalence between wrapper calls and API requests |

In section 5.1, the task utility averages **20 development instances** of noisy parity.
The meta-utility uses **five repeated copies of the same task/starting-solution pair** because
model calls are stochastic. Generalization is evaluated on **50 held-out instances**.
Separately, the plot aggregates **five independent STOP runs**. These are distinct levels of
repetition, not five task families. Section 3.3 below describes the implementation's inner data.

Historical models are `gpt-4-0314`, `gpt-3.5-turbo-0613`, and
`Mixtral-8x7B-Instruct-v0.1`. Source: [paper v3](https://arxiv.org/pdf/2310.02304v3).

## 3. Mechanism step by step

### 3.1. The two improvement levels

**Static-inspection and interpretation.** The seed function receives code, an evaluator,
and a model interface. It generates alternatives and selects by score. At the task level,
that code is a solution. At the outer level, that code is the improver itself.
See the [seed implementation](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_seed_algorithm.py#L3-L23).

This diagram is an original teaching view of the inspected call structure.

```mermaid
sequenceDiagram
    participant O as Current improver
    participant E as Meta-evaluator
    participant J as Candidate improver J
    participant U as Task evaluator
    Note over O,U: The language model remains fixed
    loop Outer improvement round
        O->>O: Propose candidate J using the model
        O->>E: Score J
        loop Tasks or repetitions
            E->>J: Improve a starting solution
            J->>U: Score candidates generated with the model
            U-->>J: Candidate scores
            J-->>E: Return selected solution
            E->>U: Evaluate returned solution
            U-->>E: Task score
        end
        E-->>O: Mean task score
        O->>O: Select next improver
    end
```

Fixed for a controlled comparison: model, evaluator, task split, and resource limits.
Mutable: candidate solution code inside an evaluation, and improver code across outer rounds.
A changed prompt or search strategy does not by itself imply updated model weights.

### 3.2. Concrete example

**Interpretation: original teaching example, not STOP measurements.** Addition,
multiplication, and maximum replace the paper's harder tasks so that every score can be
traced. The functions and model responses below are written in advance. There are no model
calls, learning, or reproduced STOP results in this example.

#### 3.2.1. Separate the three objects

| Object | Role | Output |
|---|---|---|
| Solution `s_A` | Code that attempts task A, such as adding two numbers | A number, for example `5` |
| Task evaluator `u_A` | Runs that solution on fixed cases and assigns a score | A score, for example `0.6` |
| Improver `I_0` | Uses model `L` to propose solution code, scores candidates, and returns one | A program, not its score |

`A` in `u_A` identifies **task A**. It is not a recursive call or an iteration number.
`0` in `I_0` identifies the **initial improver**. Candidate improvers `I_A` and `I_B` below
are alternative programs, not the evaluators `u_A` and `u_B`.
The evaluator stays fixed while the candidate code changes.

#### 3.2.2. What exactly produces a score of 0.6?

Task A is to add two integers. Start with a faulty solution that ignores the second input.
A proposed revision handles non-negative second inputs but still fails on negative ones:

**`add_start` is used.** It is the deliberately incorrect starting solution: `add_start(2, 3)`
returns `2`, although the required sum is `5`. A `def` statement only defines a function;
it does not run its body. Later, `u_A(add_start)` passes that function to the evaluator.
Inside `score_cases`, `solution(a, b)` actually calls it once per case, ten times.

The three definitions are separate handwritten versions, not automatic changes to one function:

| Function | Purpose here | Where it is used |
|---|---|---|
| `add_start` | Faulty starting program: ignores `b` | Scored below, then supplied to `I_0` in section 3.2.3 |
| `add_nonnegative_b` | Partially correct candidate | Scored below and included among `demo_model` responses |
| `add_exact` | Fully correct comparison for these cases | Scored below; **not** offered by `demo_model` in section 3.2.3 |

The comment in the code identifies a handwritten teaching example. It does not disable the
functions or mean they are unused. All three are evaluated by the final three `print` lines:

```mermaid
flowchart TD
    D[Define three separate programs] --> S[add_start]
    D --> P[add_nonnegative_b]
    D --> E[add_exact]
    S --> US[u_A calls add_start on ten cases]
    P --> UP[u_A calls add_nonnegative_b on ten cases]
    E --> UE[u_A calls add_exact on ten cases]
    US --> RS[1 pass out of 10: 0.1]
    UP --> RP[6 passes out of 10: 0.6]
    UE --> RE[10 passes out of 10: 1.0]
```

```python
# Three handwritten solution versions, evaluated by the print calls below.
def add_start(a, b):
    return a


def add_nonnegative_b(a, b):
    return a + max(b, 0)


def add_exact(a, b):
    return a + b


cases_A = [(2, b, 2 + b) for b in range(-4, 6)]


def score_cases(solution, cases):
    passed = 0
    for a, b, expected in cases:
        actual = solution(a, b)
        if actual == expected:
            passed += 1
    return passed / len(cases)


def u_A(solution):
    return score_cases(solution, cases_A)


print(u_A(add_start))          # 0.1
print(u_A(add_nonnegative_b))  # 0.6
print(u_A(add_exact))          # 1.0
```

The partial candidate succeeds when `b` is **non-negative, including zero**. Its internal
branch can be read without executing the whole evaluator:

```mermaid
flowchart TD
    X[Receive a and b] --> Q{Is b at least zero?}
    Q -->|Yes| P[max of b and zero is b]
    Q -->|No| N[max of b and zero is zero]
    P --> A[Return a plus b: correct sum]
    N --> B[Return a: ignores negative b]
    A --> C[Six of the ten cases pass]
    B --> F[Four of the ten cases fail]
```

For `(2, 3)`, the partial candidate returns `2 + 3 = 5`. For `(2, -3)`, it returns
`2 + 0 = 2`, instead of `-1`. The six/four counts belong to the chosen test set; they are
not universal proportions of possible inputs.

`range(-4, 6)` supplies ten values: -4 through 5. The evaluator passes each input to
`add_nonnegative_b`, compares its return value with the fixed expected sum, and counts:

| Case | Inputs `(a, b)` | Expected | Actual | Credit |
|---|---|---:|---:|---:|
| 1 | `(2, -4)` | -2 | 2 | 0 |
| 2 | `(2, -3)` | -1 | 2 | 0 |
| 3 | `(2, -2)` | 0 | 2 | 0 |
| 4 | `(2, -1)` | 1 | 2 | 0 |
| 5 | `(2, 0)` | 2 | 2 | 1 |
| 6 | `(2, 1)` | 3 | 3 | 1 |
| 7 | `(2, 2)` | 4 | 4 | 1 |
| 8 | `(2, 3)` | 5 | 5 | 1 |
| 9 | `(2, 4)` | 6 | 6 | 1 |
| 10 | `(2, 5)` | 7 | 7 | 1 |
| Total | Ten fixed cases | | | 6 |

Therefore `u_A(add_nonnegative_b) = 6 / 10 = 0.6`. This means **six of these ten cases pass**.
It does not mean the model is 60% confident, each answer is 60% correct, or an arbitrary future
input has a proven 60% success probability. Here, each case is binary but the aggregate score
has intermediate values. A different evaluator could award partial credit per case.

**Connection to the paper, section 3.** STOP allows a bounded real-valued utility, potentially
stochastic; it does not require a binary pass/fail function. For example, an independently
chosen partial-credit rule could be `max(0, 1 - abs(actual - expected) / 10)`: expected `5`
and actual `3` would earn `0.8`. This rule is an alternative illustration, not the rule used
in the table or a STOP result. Noisy parity in section 5.1 uses prediction accuracy, so its
aggregate utility can also lie between zero and one. The evaluator must be specified before
comparing candidates; changing it mid-comparison would change what the score means.

#### 3.2.3. Open the nested expression, one operation at a time

A small improver can choose between two proposed programs. `demo_model` supplies fixed
responses only to make this example deterministic; a real `L` would generate code from a
prompt containing the initial solution and the utility description.

This diagram follows only the addition call. The caller receives a program first, then
asks for its score. The evaluator is used during selection and again after the return:

```mermaid
sequenceDiagram
    participant C as Caller
    participant I as Improver I_0
    participant M as demo_model
    participant U as Evaluator u_A
    C->>I: Supply u_A, add_start, demo_model
    I->>M: Request candidates for add_start
    M-->>I: add_start and add_nonnegative_b
    I->>U: Score add_start on ten cases
    U-->>I: 0.1
    I->>U: Score add_nonnegative_b on ten cases
    U-->>I: 0.6
    Note over I,M: Select higher score: 0.6
    I-->>C: Return add_nonnegative_b as solution_after
    C->>U: Score solution_after
    U-->>C: 0.6
```

`add_exact` is absent from these proposals, so it cannot win this selection even though
section 3.2.2 showed its score of `1.0`. The improver only compares the candidates it receives.

```python
def demo_model(initial_solution):
    return [initial_solution, add_nonnegative_b]


def I_0(utility, initial_solution, model):
    candidates = model(initial_solution)
    return max(candidates, key=utility)


solution_after = I_0(u_A, add_start, demo_model)
score_after = u_A(solution_after)
print(solution_after.__name__)  # add_nonnegative_b
print(score_after)              # 0.6
```

Read this execution in order:

1. Supply `u_A`, the starting program `add_start`, and the model interface.
2. Receive two candidates: `add_start` and `add_nonnegative_b`.
3. Evaluate both with `u_A`: their scores are `0.1` and `0.6`.
4. `max(..., key=utility)` returns the **program** with the larger score, `add_nonnegative_b`.
5. The outer `u_A(solution_after)` evaluates the returned program and obtains `0.6` again.
   This last call scores the improver's output; it does not generate another revision.

In the formula below, `s_A` names the starting source and `s'_A` names the returned
solution. The prime means "after improvement", not a derivative. Parentheses mean a
function call: first obtain a program, then score it.

Thus the compact expression has two operations, not a recursive evaluator:

$$
s'_A=I_0(u_A,s_A,L),\qquad u_A(s'_A)=6/10=0.6.
$$

Writing `u_A(I_0(u_A,s_A,L)) = 0.6` simply nests those two operations. `I_0` **receives**
`u_A` to compare candidates; the surrounding `u_A` **scores** its returned solution.

This toy uses Python callables for readability; STOP passes solution source strings and loads
programs through its implementation. It also retains the starting solution among the toy
candidates. The inspected STOP seed selects only among generated candidates, so preserving
the starting program is not a guarantee of that seed. The toy does not model exceptions,
timeouts, resource accounting, or isolation and is not a runner for untrusted code.

#### 3.2.4. Where does the mean `(0.6 + 0.7 + 0.5) / 3` come from?

Repeat task-level improvement for tasks B and C. Suppose the returned programs are
`multiply_magnitude` and `maximum_left`. Their results can also be calculated directly:

```python
def multiply_magnitude(a, b):
    return abs(a * b)


def maximum_left(a, b):
    return a


cases_B = [(a, 2, a * 2) for a in range(-3, 7)]
cases_C = [(a, 5, max(a, 5)) for a in range(10)]


def u_B(solution):
    return score_cases(solution, cases_B)


def u_C(solution):
    return score_cases(solution, cases_C)


task_scores = [
    u_A(solution_after),
    u_B(multiply_magnitude),
    u_C(maximum_left),
]
meta_score = sum(task_scores) / len(task_scores)
print(task_scores)        # [0.6, 0.7, 0.5]
print(round(meta_score, 3))  # 0.6
```

| Task | What its returned solution does | Why it gets that score |
|---|---|---|
| A: addition | Ignores negative `b` | Six non-negative `b` cases pass: `6/10 = 0.6` |
| B: multiplication | Removes the product's sign | Inputs `a=0,...,6` pass; `a=-3,-2,-1` fail: `7/10 = 0.7` |
| C: maximum | Always returns the left input | Inputs `a=5,...,9` pass; `a=0,...,4` fail: `5/10 = 0.5` |

The resulting mean is `(0.6 + 0.7 + 0.5) / 3 = 1.8 / 3 = 0.6`. It assigns a score to the
**improver**, based on the three solutions it returned. The code above supplies the B/C
outputs explicitly; it does not simulate their model calls. In a full evaluator, those outputs
would come from calling the same candidate improver on each task:

```python
def meta_utility(improver, tasks, model):
    scores = []
    for utility, initial_solution in tasks:
        solution_after = improver(utility, initial_solution, model)
        scores.append(utility(solution_after))
    return sum(scores) / len(scores)
```

This definition shows the loop; it needs actual task pairs and a matching model interface to
be invoked. `D` denotes that task collection, `n` its number of entries, and
`hat u_D` denotes this empirical mean:

$$
\widehat{u}_D(I)=\frac{1}{n}\sum_{j=1}^{n}u_j\bigl(I(u_j,s_j,L)\bigr).
$$

**Read the symbols before substituting values.** This is the review's explanatory notation
for the empirical meta-utility, not a claim that every symbol is transcribed from the paper.

| Symbol | Read as | Object or operation |
|---|---|---|
| `I` | Improver | A program that returns solution code |
| `L` | Language model interface | Used to propose code; weights stay fixed |
| `D` | Evaluation collection | Entries consisting of a utility and starting solution |
| `j` | Entry index | Selects one pair; not a power or derivative |
| `u_j`, `s_j` | Utility and starting solution for entry j | A scoring function and program source |
| `n` | Number of entries | The denominator of the mean; not cases inside one utility |
| `hat u_D` | Estimated utility on D | The hat marks an empirical estimate, not exact future performance |
| `sum`, written as Σ | Sum | Add the scores from entry 1 through entry n |

Read the expression **inside out**:

1. `I(u_j, s_j, L)` returns an improved solution for entry `j`.
2. `u_j(...)` scores that returned solution.
3. `sum` adds the scores: `0.6 + 0.7 + 0.5 = 1.8`.
4. Divide by `n = 3`: `1.8 / 3 = 0.6`, the score assigned to the improver.

```mermaid
flowchart TD
    I[Evaluate the same improver I] --> A[Entry A: return solution and score 0.6]
    I --> B[Entry B: return solution and score 0.7]
    I --> C[Entry C: return solution and score 0.5]
    A --> S[Sum scores: 1.8]
    B --> S
    C --> S
    S --> M[Divide by three entries: 0.6]
```

The diagram uses the fictional three-task example. The inspected STOP configuration repeats
the same noisy-parity improvement problem five times, with model sampling, rather than using
these three arithmetic tasks. Section 3.3 explains the data inside that problem.

There are two different divisions: **ten cases** to score each solution, then **three tasks**
to score the improver. The mean happens to equal `18/30` because the tasks have equal case
counts; unequal counts would distinguish an equal-task mean from a pooled-case fraction.
Likewise, scores `3/10`, `5/10`, and `8/10` would give a meta-score of approximately `0.5333`,
not `0.6`. Those are a different set of example outcomes.

#### 3.2.5. Where does recursive self-improvement happen?

So far, a fixed improver has produced task solutions. The **outer round** changes the
improver itself. Instead of supplying addition code as the editable input, supply the code of
`I_0`. Instead of using `u_A` to judge addition, use `hat u_D` to judge candidate improvers by
running them on downstream tasks. Keep the model and comparison budget fixed.

For illustration, suppose `I_0` uses `L` to propose two alternative improver programs:

- `I_A`: a feedback-based repair strategy.
- `I_B`: a strategy that explores alternative repair paths.

These names denote programs, not scores. The following are **hypothetical returned-solution
scores**, not outputs generated by the toy model and not guaranteed effects of those strategies:

| Improver being evaluated | Task A | Task B | Task C | Meta-score |
|---|---:|---:|---:|---:|
| Current `I_0` | 0.6 | 0.7 | 0.5 | 0.6000 |
| Candidate `I_A` | 1.0 | 0.7 | 0.5 | 0.7333 |
| Candidate `I_B` | 1.0 | 1.0 | 0.5 | 0.8333 |

For A, the exact addition function shown above illustrates a score of `1.0`. For B, replacing
`abs(a * b)` with `a * b` would pass all ten cases. C remains incorrect on half the cases.
Evaluating a candidate improver means running it to produce these task solutions, not running
the improver itself as the addition function. The current program is shown as a reference;
the inspected seed does not automatically include it in candidate selection.

```mermaid
flowchart TD
    I0[Current improver I0] --> P[Use fixed model to propose improver code]
    P --> IA[Candidate IA]
    P --> IB[Candidate IB]
    IA --> EA[Run on A, B, C: mean 0.7333]
    IB --> EB[Run on A, B, C: mean 0.8333]
    EA --> S[Select IB and load it as I1]
    EB --> S
    S --> N[Next round: I1 proposes edits to its own code]
```

Select `I_B` in this illustration and call it `I_1`: `B` identifies the candidate; `1` identifies
the next round. At that point the optimizer used in the next round has changed. The recursive
update can now be read as:

$$
I_{t+1}=\mathrm{load}\left(I_t\left(\widehat{u}_D,\mathrm{code}(I_t),L\right)\right).
$$

**Read the update as four operations.** `t` is a round index; `t + 1` is the next round.
The subscript is not multiplication. `code` and `load` name conceptual operations in this
review; the Python implementation uses source strings and `temp_override`.

| Operation | Input | Output in the hypothetical example |
|---|---|---|
| `code(I_t)` | Running improver I0 | Its source text |
| `I_t(hat u_D, code(I_t), L)` | Source, meta-evaluator, fixed model | Selected candidate IB as source text |
| `load(...)` | Selected source text | An executable improver |
| Assign `I_{t+1}` | That executable | I1, used to construct the following candidate |

The equality defines the next program; it does not state that its score necessarily increases.

- `code(I_t)` is the current improver's source, supplied as editable input.
- `I_t(...)` uses the model and the meta-utility to return proposed improver source.
- `load(...)` makes the selected source the executable next improver; it is not a sandbox design.
- The next round uses `I_{t+1}` to perform the search. A loop can implement this; no recursive
  self-call inside `u_A` is required. Repeatedly repairing addition with unchanged `I_0` would
  remain task-level optimization, not improvement of the improver.

The mathematical argument order is `(utility, solution, model)`. The upstream Python
implementation uses `(initial_solution, utility, language_model)`; follow names when mapping
between them. These small, deterministic examples explain the interfaces. The published
noisy-parity experiment has the additional instance/repetition levels described in section 2.

A meta-score of `0.8333` here does not establish future-task performance. An untouched test set
can reverse the ranking. Selecting repeatedly against that test set would turn it into search
data. A thesis protocol therefore needs separate selection and final-test evidence, repeated
independent runs, and resource limits.

### 3.3. Data and evaluation

**Static-inspection.** The parity task generates synthetic data: 10 bits, 100 labeled training
examples, and 20 test inputs per instance. Noise affects training labels. Development utility
averages 20 instances and test utility 50, using different base seeds. The score is mean
prediction accuracy; the attempted timeout is two seconds per instance. These nested sample
counts describe different units and must not be pooled as independent experiment runs.
Source: [parity evaluator](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/parity_noise/secret_utility.py#L21-L85).

**Interpretation for the thesis.** A method that changes code while holding model weights
fixed still needs data for search and evaluation. It does not automatically require a
fine-tuning dataset. Public coding tasks, generated game instances, or simulated business
cases could provide that evidence. The selected case must support repeatable scoring and
separation between search feedback and final evaluation.

### 3.4. Cost accounting

**Static-inspection.** Defaults specify six outer iterations, four model-wrapper calls per
improver invocation, six responses per call, 25 utility calls, 25 meta-utility calls, and five
meta-evaluation repetitions. These are separate budgets, not one global spending cap.
Source: [configuration](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/config.py#L1-L20).

**Interpretation: a smaller, invented budget to explain the arithmetic.** A wrapper call is
an invocation of the software interface around the language model. It is not one unit test,
one token, or necessarily one API request. The numbers below describe a prospective protocol,
not the defaults above or a reconstruction of STOP's spending.

| Symbol | What it counts | Example allowance |
|---|---|---:|
| `T` | Outer improvement rounds | 2 rounds |
| `B_o` | Model-wrapper calls to propose improvers in one outer round | 1 call per round |
| `K` | Candidate improvers evaluated in that round | 2 candidates |
| `n` | Downstream task-improvement invocations per candidate, including any allocated repetitions | 3 invocations per candidate |
| `B` | Model-wrapper calls within each downstream improvement invocation | 2 calls per invocation |
| `N_wrapper` | Total wrapper-call allowance for these two activities across all rounds | 26 calls |

The subscript in `B_o` is the letter **o**, for outer proposals, not the number zero.
Lowercase `n` counts improvement invocations, not the ten test cases used by `u_A`.
Those ten arithmetic checks execute Python; they do not each require a model call.

#### 3.4.1. Follow the budget for one round

```mermaid
flowchart TD
    R[One outer round] --> P[Propose improvers: B_o = 1 call]
    P --> K[Evaluate K = 2 candidate improvers]
    K --> A[Candidate IA: n = 3 task invocations]
    K --> B[Candidate IB: n = 3 task invocations]
    A --> CA[3 invocations times 2 calls = 6]
    B --> CB[3 invocations times 2 calls = 6]
    CA --> E[Candidate evaluation: 6 plus 6 = 12 calls]
    CB --> E
    E --> S[Round total: 1 proposal call plus 12 = 13]
    S --> T[T = 2 rounds: 2 times 13 = 26 calls]
```

Read the nested budgets from the inside out:

1. One candidate improves one task: allowance of **2** model-wrapper calls (`B`).
2. That candidate is evaluated through three task invocations: **3 × 2 = 6** calls (`nB`).
3. Evaluate two candidates: **2 × 6 = 12** calls (`KnB`).
4. Add the outer call that proposed them: **1 + 12 = 13** calls (`B_o + KnB`).
5. Repeat the allocation for two outer rounds: **2 × 13 = 26** calls.

Thus the general allowance is:

$$
N_{\mathrm{wrapper}} = T(B_o + KnB).
$$

For the example, substitute values only after identifying their units:

$$
N_{\mathrm{wrapper}} = 2(1 + 2\cdot3\cdot2)=2(13)=26.
$$

The sum separates **proposing improvers** from **evaluating them by running downstream
improvements**. The products count repeated work. Actual usage can be smaller if a candidate
stops early or does not use its full allocation.

#### 3.4.2. What this total includes and leaves out

The 26 calls cover only the two activities specified above. Add baseline scoring, incumbent
checks, additional repetitions beyond `n`, and final evaluation separately. If an evaluator
itself calls a model, account for those calls separately too. There is no such model call in
the arithmetic evaluator used in section 3.2.

At most four responses per wrapper call would yield an allowance of **26 × 4 = 104
responses**. Responses are still not tokens or money. Token usage depends on the length of
inputs and outputs; elapsed time also includes code execution and evaluation.

In the inspected wrapper, identical prompts can be grouped, responses requested together,
and failed requests retried. Therefore wrapper calls, API requests, generated responses, and
billed tokens are not interchangeable. Capture all four separately, plus evaluation time.
Source: [request dispatch and retries](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/language_model.py#L294-L356).

For reuse, compare total search cost plus deployment cost across `m` tasks against the same
`m` tasks with a fixed improver. Include human review effort separately. A higher task score
alone cannot establish lower development cost.

## 4. Original code walkthrough

**Static-inspection.** This is a dependency trace, not a verified execution trace.
The descriptive `utility.py` files supplied to generated code differ from the evaluators
implemented in `secret_utility.py`.

| Responsibility | Pinned source | Observation |
|---|---|---|
| Initial proposals | [Seed, lines 18-23](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_seed_algorithm.py#L18-L23) | One batch; extraction; candidate selection with `max` |
| Outer iteration | [Runner, lines 122-179](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/run_improver.py#L122-L179) | Invokes the current improver; evaluates its result; saves and reloads returned code |
| Meta-evaluation | [Meta-utility, lines 65-143](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_utility.py#L65-L143) | Repeats downstream improvement; returns mean validation score; optionally logs test scores |
| Task evaluation | [Parity utility, lines 9-95](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/parity_noise/secret_utility.py#L9-L95) | Generates instances, invokes the solution, and scores predictions |
| Model budget | [Wrapper, lines 226-250](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/language_model.py#L226-L250) | Counts wrapper invocations and limits responses per invocation |
| Loading generated code | [Helpers, lines 52-77 and 154-192](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/helpers.py#L52-L192) | Writes source to a temporary module and imports it |
| Transfer entry point | [Transfer evaluation, lines 207-214](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/transfer_eval.py#L207-L214) | Chooses a stored improver and invokes the task evaluator |


### 4.1. Follow the original code in four steps

**Original excerpts**, with indentation adjusted for reading; omitted surrounding code remains
in the linked files. These are not standalone scripts. Code: Microsoft and contributors,
[MIT license](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/LICENSE). The arithmetic examples in section 3.2 are **illustrative code**,
not excerpts from this repository.

**A. Propose and select solution source.**
[Seed, lines 18-23](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_seed_algorithm.py#L18-L23):

```python
n_messages = min(language_model.max_responses_per_call, utility.budget)
new_solutions = language_model.batch_prompt(expertise, [message] * n_messages, temperature=0.7)
new_solutions = extract_code(new_solutions)
print("new_solutions:", new_solutions)
best_solution = max(new_solutions, key=utility)
return best_solution
```

- **Input:** `initial_solution` is source text; the preceding prompt includes it and `utility.str`.
- **Operation:** bound the number of responses, ask the model for candidates, extract code,
  then call `utility` on each candidate through `max(..., key=utility)`.
- **Output:** `best_solution` is source text, not its score. It may be task code or improver
  code depending on the input and evaluator. The original seed does not retain the starting
  source among its candidates automatically.

**B. Test a candidate improver by asking it to improve a downstream solution.**
[`get_improver`, lines 33-35](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_utility.py#L33-L35):

```python
new_improve_algorithm = temp_override(improve_str, "improve_algorithm")
improved_algorithm_str = new_improve_algorithm(base_algorithm_str, utility, language_model)
return improved_algorithm_str
```

- **Input:** `improve_str` is candidate improver source.
- **Operation:** load its `improve_algorithm` function and call it on `base_algorithm_str`,
  the downstream starting program, with that task's utility and model interface.
- **Output:** `improved_algorithm_str` is the resulting task solution. This name does not
  mean it is another improver: its role depends on this call's inputs.

**C. Turn returned solutions into a score for the candidate improver.**
Two separate original lines from [`meta_utility`](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_utility.py#L123-L138):

```python
new_utility_val = utility_wrapped(improved_algorithm_str, mode="val")
```

```python
expected_utility_val += new_utility_val / n_tests
```

The first line scores a returned task solution. The second adds its contribution to the
mean. For the teaching values `0.6`, `0.7`, `0.5` with `n_tests = 3`, the contributions are
`0.2`, about `0.2333`, and about `0.1667`, totaling `0.6`. These are illustrative values;
the inspected default is five repeated improvements. `meta_utility` returns that mean.

**D. Load the returned improver for the next round.**
[Runner, lines 175-179](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/run_improver.py#L175-L179), inside its successful-return branch:

```python
if config["iterative"]:
    improver_str = new_algorithm_str
algorithm_to_improve = new_algorithm_str
previous_improve_algorithm = improve_algorithm
improve_algorithm = temp_override(improver_str, "improve_algorithm")
```

With `config["iterative"] = True`, the returned source becomes the next active improver.
The runner's success check rejects a zero score, but does not require beating the incumbent.
This is why **loading a new version is not evidence of improvement**.

```mermaid
flowchart TD
    A[Current improver proposes source for candidate J] --> B[meta_utility receives source J]
    B --> C[get_improver loads J]
    C --> D[J returns downstream solution source]
    D --> E[Task utility scores the solution]
    E --> F[meta_utility averages repeated scores]
    F --> G[Current improver selects source by that score]
    G --> H[Runner checks return and loads next improver]
```

This is a static reading path. It omits error paths and resource wrappers; the source map
above and the limitations in section 5.2 locate those details.

## 5. Local inspection and execution

### 5.1. Open the unchanged source

| Field | Inspected snapshot |
|---|---|
| Repository | [microsoft/stop](https://github.com/microsoft/stop) |
| Commit | `0d6780c54306b2486dd36e9c4ae9b49aceb27ea4` |
| Downloaded | 2026-10-10 |
| Local path, relative to this README | `_local/upstream/` |
| Scope | All 37 tracked files, including 31 Python files; 100,939 bytes excluding Git history |
| Integrity | Detached at the pinned commit; clean checkout, no source changes |
| Paper correspondence | Public implementation associated with STOP; exact historical execution environment is not established |
| Execution | Not run or imported; no dependencies installed and no model calls |

The original repository is local only and excluded from Git. It is not included when another
reader clones thinking-harness; the pinned web links remain available. Its own README and
license remain inside `_local/upstream/`. Preserve this folder before deleting or archiving
a worktree, or download the same commit again.

**Reading order:** open `config.py`, then the seed, meta-utility, runner, and model wrapper
listed in section 4. Read the text in the editor; opening a file does not require Python.

To obtain the same source in a fresh checkout, run these Git commands **from this paper's
folder**, only when `_local/upstream/` does not already exist. They download code, not dependencies:

```sh
git clone --no-checkout https://github.com/microsoft/stop.git _local/upstream
git -C _local/upstream checkout --detach 0d6780c54306b2486dd36e9c4ae9b49aceb27ea4
git -C _local/upstream rev-parse HEAD
git -C _local/upstream status --short
```

The hash should match the table; a pristine checkout produces no status entries.

**Execution prerequisites, inspected but not installed:** imports reference `numpy`, `pebble`,
`tqdm`, `openai`, and `jsonlines`. The wrapper also imports a local `api_key.py` configuration
and uses historical API conventions. The snapshot contains no requirements file, project
manifest, dependency lock, or declared supported Python version. This is an import inventory,
not a tested installation recipe.

No notebook or repaired version is included yet. A later execution decision would specify
compatible dependencies/model, isolation, budget, and deviations in a separate working copy.
Downloading and understanding the source does not require making it run.

### 5.2. Reproduction gaps and validity risks

These observations concern the pinned snapshot. No runtime failures or exploits were executed.

| Finding | Evidence | Consequence for a future reproduction |
|---|---|---|
| Transfer path inconsistency | [Lines 207-212](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/transfer_eval.py#L207-L212) assign `improve_algorithm_base` in the default `improved` branch, then open `improve_algorithm_path` | If reached under that configuration, the open expression references an undefined name |
| Limited transfer selection | [Line 21](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/transfer_eval.py#L21) selects only `three_sat` | The entry point does not currently enumerate the full transfer task set |
| No incumbent comparison in the outer acceptance check | [Runner, lines 140-144](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/run_improver.py#L140-L144) rejects zero, without comparing the previous score | A successful return is not evidence of a better improver |
| Initial source omitted from seed selection | [Seed, lines 18-23](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/tasks/meta_optimization/secret_seed_algorithm.py#L18-L23) maximizes over generated candidates | A candidate can replace a better starting solution |
| Limited isolation | [Reliability guard](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/helpers.py#L80-L94) explicitly disclaims a security sandbox | File naming and Python function restrictions do not enforce evaluator or credential isolation |
| Historical environment incomplete | [Source tree](https://github.com/microsoft/stop/tree/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4) contains no dependency lock; [model wrapper](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/language_model.py#L20-L38) uses historical identifiers and API configuration | Compatibility and model availability remain unverified; substitutions would be adaptations |

**Interpretation.** A reproduction proposal needs an external execution boundary, read-only
final evaluation, fixed accounting, and an explicit list of deviations from the original.
Source files named `secret_utility.py` are not an access-control mechanism. Test-mode scoring
is available through the same Python evaluator interface, so a trusted orchestration boundary
would be needed to restrict access. This is an architectural observation, not a demonstrated
leak or evidence that the published experiments were compromised.

## 6. Critical reading and application

### 6.1. What is independently established

- Pinned source inspection supports the call map and the identified transfer-path inconsistency.
- Static parsing of the downloaded Python files found no syntax errors. It does not establish
  importability, dependency compatibility, runtime correctness, or numerical reproduction.
- The original Python teaching snippets in section 3.2 were executed locally: addition scores 0.1, 0.6, and 1.0; task scores 0.6, 0.7, and 0.5; their mean is 0.6. The outer candidate table remains hypothetical, with its arithmetic checked. This validates the explanation, not STOP.
- The article's performance claims remain attributed claims. No measured project result exists.

The review is ready for discussion. Complete reading, runtime inspection, proof checking,
and reproduction remain separate activities.

### 6.2. Implications and next discussion

**Interpretation.** Compare three possible scopes before selecting a method:

| Scope | Mutable object | Main question |
|---|---|---|
| Fixed improver, evolving harness | A bounded harness configuration or module | Can a fixed search process improve task performance within budget? |
| Evolving improver and harness | Search procedure plus its output | Does recursion add value beyond an equally funded fixed improver? |
| Learning or planning alternative | A policy, planner, or search rule | Would another optimization method answer the same practical need more simply? |

For a coding case, the editable object might be a repair loop. For a simulated business case,
it might be routing or tool-retry policy. Restrict the first comparison to one such object;
whole-harness rewriting would introduce additional attribution and validation problems.
These are candidate directions, not a selected thesis contribution.

The guided discussion should answer:

1. Can the original example be traced from a task score to selection of a new improver?
2. Which part of a harness could change while its evaluator and budget remain fixed?
3. What fixed-improver baseline would isolate the added value of recursion?
4. Can that case provide independent test tasks at a manageable evaluation cost?

Then review Self-Harness using the same dimensions: mutable object, update mechanism,
evaluation boundary, search cost, and transfer evidence. Its mechanism and results still need
verification. Track the next reading in [issue #4](https://github.com/jairzinhosantos/thinking-harness/issues/4).
The broader metadata audit remains in [issue #3](https://github.com/jairzinhosantos/thinking-harness/issues/3).
