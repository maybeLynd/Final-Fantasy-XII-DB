# Audit-spec review: ASTRA summon selector domain

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/summon-selector-domain/`
Board task: `ASTRA-REQ-SPEC-SUMMON-SELECTOR-DOMAIN-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-02.json`.
- **Prover re-run fresh:** `prove-before-output-path-fix.py` → exit 0; fresh result byte-identical to retained `proof-01-output-invocation-original.json (pre-fix output)`.
- **Control re-run in disposable copy:** `control.py` — PASS — failed-capture/missing-source/coherent-second-pop-selector all refused with expected diagnostics.

## Narrowing / notes

- `control-before-output-path-fix.py` requires the pre-fix artefacts (`proof-01.status.json`, `result-01.json`) that the package intentionally no longer ships; retained `control-01.status.json`/`control-02.status.json` receipts attest both runs. Historical control preserved, not re-runnable.
