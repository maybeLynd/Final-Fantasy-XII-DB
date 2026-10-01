# Audit-spec review: ASTRA suspend restore copy origin

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/suspend-restore-copy-origin/`
Board task: `ASTRA-REQ-SPEC-SUSPEND-RESTORE-COPY-ORIGIN-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-01.json — 'PROVED original restore/snapshot origin6B0, exact4F0 footprint and incoming release pointer'`.
- **Control re-run in disposable copy:** `control.py` — PASS — three cause-specific refusals plus prior positive.

## Narrowing / notes

None required.
