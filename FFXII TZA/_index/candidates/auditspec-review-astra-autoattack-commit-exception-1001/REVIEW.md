# Audit-spec review: ASTRA autoattack commit exception

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/autoattack-commit-exception/`
Board task: `ASTRA-REQ-SPEC-AUTOATTACK-COMMIT-EXCEPTION-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-01.json — 'PROVED knownmode0 fixedAttack and conditional specialpath exclusion'`.
- **Control re-run in disposable copy:** `control.py` — PASS — three cause-specific refusals plus prior positive.

## Narrowing / notes

None required.
