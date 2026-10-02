# Audit-spec review: ASTRA rig owner rebind preconditions

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/rig-owner-rebind-preconditions/`
Board task: `ASTRA-REQ-SPEC-RIG-OWNER-REBIND-PRECONDITIONS-1002`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `rig-owner width/rebinder-boundary result`.
- **Control re-run in disposable copy:** `control.py` — PASS — four actual producer refusals and upstream-before-output control.

## Narrowing / notes

None required.
