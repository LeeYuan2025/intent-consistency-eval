# MRT-EVAL v1.0  
**Minimal Reproducible Test — Artifact Evaluation**

---

## 1. Purpose

MRT-EVAL is a **domain-agnostic, artifact-level evaluation component** designed to
assess whether input CSV artifacts are structurally valid, quality-bounded,
and deliverable to downstream AI systems.

It explicitly operates **before any semantic, model, or domain-specific processing**.

The goal is not to interpret data, but to determine whether data **should be
allowed to reach interpretation layers at all**.

---

## 2. Design Scope

### MRT-EVAL DOES
- Evaluate CSV artifacts at the **structural and quality level**
- Detect delimiter and encoding
- Count rows and columns
- Identify empty rows and duplicate rows (byte-level, non-semantic)
- Produce **machine-decidable status signals** (`PASS / WARN / FAIL`)
- Always emit evaluation artifacts for auditability

### MRT-EVAL DOES NOT
- ❌ Interpret semantic meaning
- ❌ Assume any data domain (finance, NLP, vision, etc.)
- ❌ Enforce schemas or field semantics
- ❌ Clean, normalize, or transform data
- ❌ Evaluate model performance or accuracy

---

## 3. Input Specification

- Input root directory: `./input/`
- Accepted format: `*.csv`
- Directory structure: recursive scanning allowed
- No assumptions are made about:
  - column names
  - column meanings
  - data ranges
  - data correctness

MRT-EVAL treats all CSV content as **opaque artifacts**.

---

## 4. Output Artifacts

All outputs are written to: `./work/`

### 4.1 `mrt_eval.json` — Primary Evaluation Artifact

This is the authoritative, machine-consumable evaluation output.

```json
{
  "generated_at": "YYYY-MM-DDTHH:MM:SS",
  "input_root": "./input",
  "overall_status": "PASS | WARN | FAIL",
  "pass_count": 0,
  "warn_count": 0,
  "fail_count": 0,
  "files": [
    {
      "file": "relative/path.csv",
      "status": "PASS | WARN | FAIL",
      "rows": 0,
      "cols": 0,
      "detected_delimiter": ", | ; | \\t",
      "encoding_used": "utf-8-sig | cp950(replace)",
      "empty_rows": 0,
      "duplicate_rows_est": {
        "scanned": 0,
        "dups": 0
      },
      "notes": [],
      "errors": []

    }
  ]
}
