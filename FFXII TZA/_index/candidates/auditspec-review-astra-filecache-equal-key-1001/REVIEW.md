# Audit-spec review: ASTRA filecache equal key

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/filecache-equal-key/`
Board task: `ASTRA-REQ-SPEC-FILECACHE-EQUAL-KEY-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-filecache-equal-key.py` → exit 0; fresh result byte-identical to retained `filecache-equal-key-result-01.json`.
- **Control re-run:** `control-filecache-equal-key.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS_FOUR_ACTUAL_REFUSALS — changed-key-move/incomplete-body/upstream-failed/wrong-release-import all refused.

## Narrowing / notes

None required.
