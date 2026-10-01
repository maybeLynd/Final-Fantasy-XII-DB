# Audit-spec review: ASTRA heading flag class mask

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/heading-flag-class-mask/`
Board task: `ASTRA-REQ-SPEC-HEADING-FLAG-CLASS-MASK-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-flag-class-mask.py` → exit 0; fresh result byte-identical to retained `flag-class-mask-result-01.json`.
- **Control re-run:** `control-flag-class-mask.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — all mutated-source cases refused as documented.
- Source dir `heading-class-effects-slice` re-used as the retained-role adapter input; certified-image sha pin inside the prover confirmed against the shipping EXE identity.

## Narrowing / notes

None required.
