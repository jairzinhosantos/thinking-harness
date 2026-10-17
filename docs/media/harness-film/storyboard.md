# Thinking Harness / Research film

A 45-second conceptual sequence about assembling an agent harness, evaluating changes,
and using the selected harness to help construct its successor. Designed for silent
viewing, with English text and restrained motion.

[Watch the video](thinking-harness.mp4) · [Review gallery](index.html) ·
[Editable animation](film.html)

The video is 1920 × 1080 at 24 frames per second, encoded as H.264 MP4 without audio.
Individual components move during assembly and replacement. The selected successor takes
the construction role only after the illustrated external evaluation.

## Scope

The film illustrates a research direction. It does not report measured improvement.
The [current pilot](../../../research/cases/case-0003-debt-negotiation/README.es.md)
changes a YAML prompt while keeping the optimizer, model and evaluator fixed.
The broader component assembly and recursive construction shown here remain conceptual.

A harness connects instructions, context, tools and execution around a model.
`H₀` denotes the initial harness, `H₁` a selected version and `H₂` its successor candidate.
The model, objective and external evaluator remain fixed throughout the sequence.
Acceptance requires evidence against the same criteria; a new version is not automatically better.

## Sequence

| Time | Action | On-screen text |
|---|---|---|
| 00:00–00:02 | The model core and assembly surface appear. | A system around the model. |
| 00:02–00:11 | Policy, context, tools and control descend independently and settle into `H₀`. | Assemble the harness. |
| 00:11–00:15 | The policy component lifts out while the other parts remain in place. | Lift one component. Keep the rest fixed. |
| 00:15–00:19 | Three candidate configurations receive visibly different policy components. | Propose. Evaluate. Retain. |
| 00:19–00:27 | Each candidate enters the same evaluator. Two fade after rejection; the retained configuration becomes `H₁`. This selection is illustrative. | Retain the qualifying configuration. |
| 00:27–00:34 | `H₁` participates in assembling `H₂`. The policy is retained and the control component is revised. | Improve how the next system is built. |
| 00:34–00:40 | `H₂` goes to the fixed external evaluator. After illustrative acceptance, it takes the constructor position and begins the next candidate, `H₃`. | The accepted version takes the construction role. |
| 00:40–00:45 | Motion settles into the project name and research question. | Thinking Harness / Can a harness improve how it improves? |

The distinction is visible in the final transition: ordinary improvement changes the
task-solving configuration; the recursive direction lets an accepted configuration
participate in constructing later configurations. Neither guarantees progress.
If a candidate fails, the current harness remains in place.

## Keyframes

### 01 / Assembly

An exploded view introduces the parts before they form one system.

![Initial harness assembly](01-assembly.png)

[Editable SVG](01-assembly.svg)

### 02 / Selection

Three candidate assemblies enter one fixed evaluator. Rejection and retention are explicit.
No score or performance curve is invented for the scene.

![Candidate evaluation and selection](02-selection.png)

[Editable SVG](02-selection.svg)

### 03 / Recursion

The selected harness participates in building its successor. Evaluation stays outside the
mutable system. The dashed return path denotes conditional promotion into the constructor role.

![Recursive construction with external evaluation](03-recursion.png)

[Editable SVG](03-recursion.svg)

## Visual direction

- Graphite background, off-white type, cyan for retained structures and amber for candidate changes.
- Isometric modules, fine edges and a faint spatial grid. No humanoids, holographic dashboards or decorative data streams.
- Continuous camera direction, slow assembly and short pauses at evaluation. No flashes or rapid cuts.
- Optional low ambient sound; the meaning remains complete without audio.
- The conceptual-sequence label remains visible. Component labels appear before movement and fade when no longer needed.

The three frames share a 1920 × 1080 canvas. Their authoritative source is
[storyboard.py](storyboard.py), which generates editable SVGs and the
[review gallery](index.html). The [renderer](render_storyboard.cjs) produces matching PNGs.
The animation source is [film.js](film.js), with deterministic time-based component motion.
[render_film.cjs](render_film.cjs) exports the MP4 and [poster](poster.png) from that source.
These are motion-design assets rather than repository architecture diagrams.
