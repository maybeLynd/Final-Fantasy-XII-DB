# Audit-spec review: ASTRA namebinding callback inputs

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/namebinding-callback-inputs/`
Board task: `ASTRA-REQ-SPEC-NAMEBINDING-CALLBACK-INPUTS-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-namebinding-callback-inputs.py` → exit 0; fresh result byte-identical to retained `namebinding-callback-inputs-result-01.json`.
- **Control re-run:** `control-namebinding-callback-inputs.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — all mutated-case refusals reproduced, each emitting the expected error and no result.

## Narrowing / notes

None required.
