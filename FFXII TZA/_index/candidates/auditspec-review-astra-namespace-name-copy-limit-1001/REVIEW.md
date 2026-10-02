# Audit-spec review: ASTRA namespace name copy limit

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/namespace-name-copy-limit/`
Board task: `ASTRA-REQ-SPEC-NAMESPACE-NAME-COPY-LIMIT-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result with 29 instruction assertions and 3 symbolic partitions`.
- **Control re-run in disposable copy:** `control.py` — TWO_ACTUAL_RETAINED_ADMISSION_REFUSALS — mixed-parent and missing-source both refused.

## Narrowing / notes

None required.
