# Audit-spec review: ASTRA filecache key preprocessing

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/filecache-key-preprocessing/`
Board task: `ASTRA-REQ-SPEC-FILECACHE-KEY-PREPROCESSING-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-filecache-key-preprocessing.py` → exit 0; fresh result byte-identical to retained `filecache-key-preprocessing-result-02.json`.
- **Control re-run:** `control-filecache-key-preprocessing.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — mutated-upstream cases refused as documented.

## Narrowing / notes

- `prove-filecache-key-preprocessing-before-immediate-encoding-01.py` refuses at HEAD ('required original instruction pin mismatch: 0x20c497') — per README the retained refusal record of the superseded pre-encoding interpretation; the current prover is operative.
