# Audit-spec review: ASTRA title queue consumption

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/title-queue-consumption/`
Board task: `ASTRA-REQ-SPEC-TITLE-QUEUE-CONSUMPTION-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-title-queue-consumption.py` → exit 0; fresh result byte-identical to retained `title-queue-consumption-result-01.json`.
- Four-bank callback consumption claim: the prove re-derives the INC32(index)&3 pre-snapshot mutation, pair+0/pair+8 call convention, 16-byte step and post-call index reread from the pinned source JSON against the certified image identity.

## Narrowing / notes

None required.
