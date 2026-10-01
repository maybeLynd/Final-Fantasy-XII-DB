# Audit-spec review: ASTRA title queue pump boundary

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/title-queue-pump-boundary/`
Board task: `ASTRA-REQ-SPEC-TITLE-QUEUE-PUMP-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-title-queue-pump-boundary.py` → exit 0; fresh result byte-identical to retained `title-queue-pump-boundary-result-01.json`.
- Helper integrity gate verified: the prover sha256-pins `prove-title-queue-consumption.py` before reuse, and the retained `title-queue-pump-controls-01` receipts attest the three refusal cases.

## Narrowing / notes

None required.
