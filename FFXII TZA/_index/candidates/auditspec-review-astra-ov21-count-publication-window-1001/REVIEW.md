# Audit-spec review: ASTRA ov21 count publication window

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/ov21-count-publication-window/`
Board task: `ASTRA-REQ-SPEC-OV21-COUNT-PUBLICATION-WINDOW-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `page-before-total count-store result`.
- **Control re-run in disposable copy:** `control.py` — PASS — four actual cause-specific refusals plus prior actual positive; no native/game.

## Narrowing / notes

None required.
