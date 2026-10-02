# Audit-spec review: ASTRA rig index list producer

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/rig-index-list-producer/`
Board task: `ASTRA-REQ-SPEC-RIG-INDEX-LIST-PRODUCER-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-02.json`.
- **Prover re-run fresh:** `prove-01-driver.py` → exit 0; fresh result byte-identical to retained `retained earlier result`.
- **Control re-run in disposable copy:** `control.py` — PASS — four actual producer refusals and upstream-before-output control.

## Narrowing / notes

None required.
