# Audit-spec review: ASTRA accounting dispatch index

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/accounting-dispatch-index/`
Board task: `ASTRA-REQ-SPEC-ACCOUNTING-DISPATCH-INDEX-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `tag-boolean unboundedness result`.
- **Control re-run in disposable copy:** `control.py` — PASS — four actual producer refusals and upstream-before-output control.

## Narrowing / notes

None required.
