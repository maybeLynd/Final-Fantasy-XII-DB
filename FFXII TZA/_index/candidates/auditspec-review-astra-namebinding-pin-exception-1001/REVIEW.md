# Audit-spec review: ASTRA namebinding pin exception

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/namebinding-pin-exception/`
Board task: `ASTRA-REQ-SPEC-NAMEBINDING-PIN-EXCEPTION-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-namebinding-pin-exception.py` → exit 0; fresh result byte-identical to retained `namebinding-pin-exception-result-01.json`.
- **Control re-run:** `control-namebinding-pin-exception.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — all mutated-case refusals reproduced, each emitting the expected error and no result.

## Narrowing / notes

None required.
