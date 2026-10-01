# Audit-spec review: ASTRA summon kind row carrier

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/summon-kind-row-carrier/`
Board task: `ASTRA-REQ-SPEC-SUMMON-KIND-ROW-CARRIER-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-01.json — 'PROVED separate original carriers, complete local caller and qualified countermodel'`.
- **Control re-run in disposable copy:** `control.py` — PASS — three cause-specific refusals plus prior positive.

## Narrowing / notes

None required.
