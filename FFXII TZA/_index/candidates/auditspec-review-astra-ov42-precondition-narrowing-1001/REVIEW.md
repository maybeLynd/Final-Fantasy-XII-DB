# Audit-spec review: ASTRA ov42 precondition narrowing

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/ov42-precondition-narrowing/`
Board task: `ASTRA-REQ-SPEC-OV42-PRECOND-NARROWING-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `check-special-admission.py` → exit 0; fresh result byte-identical to retained `special-admission-result-02.json`.
- **Prover re-run fresh:** `check-special-admission-before-returned-review-1001.py` → exit 0; fresh result byte-identical to retained `special-admission-result-01.json (pre-narrowing state)`.
- **Control re-run:** `control-special-admission-source.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — mutated source cases refused as documented.

## Narrowing / notes

None required.
