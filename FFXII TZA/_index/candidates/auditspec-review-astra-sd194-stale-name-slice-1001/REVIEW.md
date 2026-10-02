# Audit-spec review: ASTRA sd194 stale name slice

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/sd194-stale-name-slice/`
Board task: `ASTRA-REQ-SPEC-SD194-STALE-NAME-SLICE-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result with 33,930 partitions, 69 operation assertions, 9 overlap countermodel states`.
- **Control re-run in disposable copy:** `control.py` — FOUR_ACTUAL_PREREQUISITE_REFUSALS — all four cases refused.
- **Control re-run in disposable copy:** `control-before-diagnostics.py` — FOUR_ACTUAL_PREREQUISITE_REFUSALS — identical refusals reproduced.

## Narrowing / notes

None required.
