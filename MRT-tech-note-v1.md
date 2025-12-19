MRT: A Minimal Artifact-Level Evaluation Gate
Technical Note v1.0

TAS Alignment Framework — This Repo = Operational Entry Point

This repository is not just a standalone evaluation idea.
It is the operational v0.1 entry module of a broader, unified alignment and civilization-safety framework called TAS (Tectonic Alignment System).

❗ Problem Context

Current AI alignment work is mostly model-centric.
However, the core risk vector is not only in model behavior, but in:

I-risk (inner motivational drift)

C-risk (civilizational misalignment)

amplified by F (capability-force) at planetary scale

In short:

If F grows faster than C,
and I is not governed,
we do not just get “misuse risk”,
we get civilization-level instability.

✅ What This Repo Provides

This repo delivers the first measurable, testable operational primitive:

MRT — Motivational / Intent Consistency Evaluation

It is designed to:

detect intent drift

quantify internal reasoning coherence

expose early signals of I-risk

and serve as a foundational sensor in a much larger governance system

🧩 Where This Fits in TAS

MRT is one module inside a structured system:

Layer	Purpose
HLS	Human-Level State — core mind / motivation dynamics
I-Risk Vector	how motivation deviates under power & incentives
CI-64 / CHI	civilization positioning & stability modeling
PQ-R	macro risk telemetry
IxF Framework	how intention × power generates systemic outcomes
📍 This Repo	Operational v0.1 entry: measurable I-risk baseline

This is intentionally the first step because:
1️⃣ It is testable
2️⃣ It integrates into real eval pipelines
3️⃣ It generates evidence, not philosophy

🚧 Roadmap (Short)

extend MRT → full I-vector

integrate with macro stability telemetry (PQ-R)

connect with national security / AGI governance scenarios

deliver full civilization-alignment dashboard

🎯 Why share publicly?

Because alignment is not only a technical discipline,
and civilization safety cannot be delayed until after capability scaling.

This repo is the piece that can be used now,
not “a future theoretical promise”.

1. Motivation: Why Artifact-Level Evaluation Matters

Most current evaluation practices focus on model behavior at the semantic level (e.g., response quality, alignment, robustness).
However, in real-world pipelines, failures frequently originate before any model inference occurs—at the level of the input artifact itself.

Common failure modes include:

Structurally malformed inputs

Missing or inconsistent fields

Invalid value ranges

Implicit assumptions not enforced by any contract

When such artifacts are passed directly into model-based evaluation, the model may still produce fluent outputs, masking upstream defects and creating false confidence.

MRT addresses this gap by introducing a minimal, explicit artifact-level gate prior to any semantic or model-based evaluation.

2. Scope and Design Goals

MRT (Minimal Requirements Test) is intentionally narrow in scope.

Design goals:

Artifact-level only: MRT does not inspect prompts, responses, or semantics.

Pre-model gate: MRT runs before any model inference or evaluation.

Domain-agnostic: No domain-specific assumptions are embedded.

Fast sanity-check: Designed to be executable in seconds, not minutes.

Explicit contract: All checks are defined in a human-readable spec.

Non-goals:

Replacing semantic evaluation frameworks

Inferring intent or correctness

Enforcing alignment or policy decisions

3. Core Concept: Minimal Requirements Test (MRT)

MRT formalizes a simple question:

Does this artifact meet the minimal structural requirements to be evaluated at all?

An artifact that fails MRT is not “bad”—it is simply not evaluable yet.

Conceptually, MRT acts as a binary or graded gate:

Artifact → MRT → (Pass) → Model / Semantic Eval
                   ↓
                (Fail)


This separation ensures that downstream evaluation results are not contaminated by upstream structural defects.

4. Specification Format (MRT-EVAL.md)

The MRT specification is defined in a standalone document (MRT-EVAL.md) with the following principles:

Human-readable

Deterministic

Auditable

Versionable

Typical specification elements include:

Required fields

Optional fields

Type constraints

Value ranges

Consistency rules

Allowable failure modes

The spec is treated as a contract, not a heuristic.

5. Reference Implementation Overview

A minimal reference implementation is provided to demonstrate feasibility, not completeness.

Included components:

CLI entrypoint (run-mrt.py)

CSV-based input example

Structured output indicating pass/fail and reasons

30-second sanity-check path

The implementation is intentionally simple to emphasize clarity over optimization.

6. 30-Second Sanity Check Workflow

The repository includes a minimal workflow designed for rapid validation:

Prepare a minimal input artifact (e.g., CSV)

Run MRT via CLI

Observe deterministic evaluation output

This workflow allows reviewers to answer, within seconds:

What MRT checks

How failures are surfaced

How it integrates into an evaluation pipeline

No prior knowledge of the domain or model is required.

7. Relationship to Model-Level Evaluation

MRT does not compete with existing evaluation frameworks.
Instead, it acts as a precondition layer.

Relationship summary:

MRT ensures inputs are structurally valid

Semantic eval ensures outputs are behaviorally valid

Alignment frameworks address policy and intent

Separating these concerns reduces error coupling and improves debuggability.

8. Failure Modes and Trade-offs

Known limitations:

MRT cannot detect semantic errors

Over-strict specs may reject usable artifacts

Under-strict specs may allow noisy inputs

Design trade-off:

MRT intentionally favors explicit rejection over silent acceptance

This bias is deliberate, as silent acceptance is harder to audit and debug.

9. Extensibility

Although the reference implementation uses CSV, the MRT concept generalizes to:

JSON artifacts

Log structures

Evaluation traces

Structured prompts

Dataset manifests

Future extensions may include:

Schema-driven generation

Versioned contracts

Integration hooks for eval harnesses

10. Conclusion

MRT demonstrates that a minimal, artifact-level gate can significantly improve the reliability and interpretability of downstream model evaluation without entangling semantic or alignment assumptions.

By making evaluation conditional on explicit structural validity, MRT shifts part of evaluation rigor upstream—where many silent failures originate.

Repository

https://github.com/LeeYuan2025/intent-consistency-eval

Uncertainties and Open Questions

Optimal strictness levels across domains

Interaction with probabilistic or partially structured artifacts

Standardization of artifact-level contracts across eval ecosystems
