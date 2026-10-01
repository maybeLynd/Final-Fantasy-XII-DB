# Audit-spec review: ASTRA summon selector authored sites

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/summon-selector-authored-sites/`
Board task: `ASTRA-REQ-SPEC-SUMMON-SELECTOR-AUTHORED-SITES-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `reduce.py` → exit 0; fresh result byte-identical to retained `result-01.json (10,045-entry composite, 0 literal target calls)`.
- **Control re-run in disposable copy:** `control.py` — PASS — unrelated-upstream-fail/empty-suffix/coherent-gap-literal all refused with expected diagnostics.

## Narrowing / notes

None required.
