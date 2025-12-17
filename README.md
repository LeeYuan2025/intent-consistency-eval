# Intent Consistency Evaluation

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

