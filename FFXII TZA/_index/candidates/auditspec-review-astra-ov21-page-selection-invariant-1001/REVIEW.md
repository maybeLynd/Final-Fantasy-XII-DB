# Audit-spec review: ASTRA ov21 page selection invariant

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/ov21-page-selection-invariant/`
Board task: `ASTRA-REQ-SPEC-OV21-PAGE-SELECTION-INVARIANT-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-02.json`.
- **Prover re-run fresh:** `prove-01-driver.py` → exit 0; fresh result byte-identical to retained `retained earlier-wording proof`.
- **Control re-run in disposable copy:** `control.py` — PASS — four cause-specific refusals (two retained receipts re-verified, two new).

## Narrowing / notes

- `control-01-driver.py` reproduces the documented `INVALID_INCOMPLETE` state ('control not discriminating failed-retained-capture') — per README the original control-01's expected diagnostic was wrong and the retained-input hash guard correctly refused earlier. control.py (control-02) is the operative checker.
