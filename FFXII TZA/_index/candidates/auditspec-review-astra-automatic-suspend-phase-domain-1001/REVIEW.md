# Audit-spec review: ASTRA automatic suspend phase domain

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/automatic-suspend-phase-domain/`
Board task: `ASTRA-REQ-SPEC-AUTOMATIC-SUSPEND-PHASE-DOMAIN-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-01.json — 'PROVED ordinary phase>=6 snapshot refusal; eligible allocation can still fail'`.
- **Control re-run in disposable copy:** `control.py` — PASS — three cause-specific refusals plus prior positive.

## Narrowing / notes

None required.
