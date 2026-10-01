# Audit-spec review: ASTRA ov58d order switch

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/ov58d-order-switch/`
Board task: `ASTRA-REQ-SPEC-OV58D-ORDER-SWITCH-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-ov58d-order-switch.py` → exit 0; fresh result byte-identical to retained `ov58d-order-switch-result-02.json`.
- **Prover re-run fresh:** `prove-ov58d-order-switch-before-direct-reference-gate-01.py` → exit 0; fresh result byte-identical to retained `ov58d-order-switch-result-01.json (before-state)`.
- **Control re-run:** `control-ov58d-order-switch.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — mutated-source cases refused; captured role controls (w/addr/rw) intact.

## Narrowing / notes

None required.
