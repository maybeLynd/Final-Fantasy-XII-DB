# Audit-spec review: ASTRA filecache fill failure

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/filecache-fill-and-failure/`
Board task: `ASTRA-REQ-SPEC-FILECACHE-FILL-FAILURE-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-filecache-fill-and-failure.py` → exit 0; fresh result byte-identical to retained `filecache-fill-and-failure-result-01.json`.
- **Control re-run in disposable copy:** `qualify-filecache-failure-thunks.py` — PASS — 'QUALIFIED RETAINED ORIGINAL THUNKS 4 14' with the malloc IAT binding reproduced.
- **Control re-run in disposable copy:** `control-filecache-fill-and-failure.py` — PASS_FOUR_ACTUAL_REFUSALS ×4.

## Narrowing / notes

- Prover requires the qualified-thunks JSON produced by `qualify-filecache-failure-thunks.py`; ran qualify first in the disposable copy, then the prover.
- `prove-filecache-fill-and-failure-before-correlated-arm-01.py` refuses at HEAD ('cache lookup does not dominate fill') — per README the retained first positive that correctly refused unconditioned CFG domination; the current prover is operative.
