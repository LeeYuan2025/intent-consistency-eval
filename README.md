# MRT — Minimal Requirements Test

MRT is a **minimal, domain-agnostic artifact-level evaluation gate** designed to run **before any model-based or semantic evaluation**.

It checks whether an input artifact (e.g. CSV or other structured data) satisfies **basic structural and consistency requirements**, so downstream models and evaluators are not applied to invalid or ill-formed inputs.

MRT is intentionally simple: it is not a language model, not a semantic scorer, and not a policy framework. It exists solely to enforce **minimal input contracts** at the artifact level.

---

## Key properties

- *Artifact-level only* — checks input shape, constraints, and field consistency
- *Pre-model / pre-eval gate* — runs before any model inference or semantic scoring
- *Domain-agnostic & spec-driven* — no domain-specific assumptions
- *Fast & deterministic* — clear pass/fail reasons
- *Explicit, inspectable evaluation rules* (no implicit heuristics)
- *Includes a 30-second sanity check* (CSV artifacts + CLI)


---

## 30-second sanity check

```bash
python run-mrt.py --list
python run-mrt.py --run --dry-run
python run-mrt.py --run

# Intent Consistency Evaluation

---

## 📌 Context & Strategic Motivation

This repository contains an operational evaluation component that extends beyond conventional alignment evaluation.  
The **Intent Consistency Evaluation (MRT)** presented here is intentionally positioned as an **operational v0.1 entry module** of a larger alignment and risk framework, rather than a stand-alone idea.

The core insight driving this work is that **systemic risk in advanced AI systems is not solely a model behavior problem, but stems from motivation instability amplified by capability growth**.  
In practical terms: if system power (**F**) scales faster than stable values (**C**), and internal motivational coherence (**I**) is not tractably measurable or governed, risk can manifest at civilization-relevant scales.

As a result, this work proposes a **measurable, testable primitive** focusing on:
- quantifying internal intent coherence,
- detecting motivational drift,
- and providing a viable base signal for broader governance pipelines.

This metric is designed to serve as the first operational component of a broader alignment infrastructure that includes:
- human-level state dynamics (HLS),
- civilization positioning (CI-64, CHI),
- macro risk telemetry (PQ-R),
- motivational deviation vectors (I-Vector),
- and interaction models between intention and power (IxF).

By framing this work in this context, we provide a clear justification for early evaluation deployment rather than waiting for future speculative frameworks.

---

## Motivation

This repository is a minimal evaluation-focused prototype designed
to investigate cross-context and temporal consistency patterns in
large language model behavior. The goal is to provide earlier,
diagnostic visibility into latent model consistency instability that
may not be visible through traditional output-only evaluation.

## Overview

Current evaluation and alignment approaches constrain observable
outputs and enforce compliance criteria. However, they offer limited
visibility into potential intent-level drift under prompt variation,
extended interaction, or surface-level strategic behavior.

This work explores whether simple consistency measurements can
produce descriptively useful signals that support human-in-the-loop
evaluation and failure-mode analysis.

## Minimal Reproducible Test (MRT)

A Minimal Reproducible Test (MRT) is included to demonstrate:
- Cross-context consistency measurement
- Temporal stability across short interaction sequences
- Clearly defined operational limits

The MRT uses short dialogue snippets and controlled prompt
variations. Example code and configuration demonstrate how to
run the MRT with minimal setup.

## Scope and Limitations

- Diagnostic and research use only  
- Non-decisional and non-normative evaluation  
- No policy enforcement or automated actions  
- Not intended for commercial deployment or user-facing products  
- Intended for human-in-the-loop analysis, not autonomous usage

## Getting Started

Clone the repository and inspect the included examples to understand
how consistency signals are generated and interpreted. See example
scripts for usage patterns and minimal configuration.

## License

This repository is released under the MIT License.

