# Audit-spec review: ASTRA mode summon tail

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/mode-summon-tail/`
Board task: `ASTRA-REQ-SPEC-MODE-SUMMON-TAIL-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result with 32-byte native prefix zero, receiver 0x22ca408, 26 pins, raw-argument countermodel`.
- **Control re-run in disposable copy:** `control.py` — PASS — failed-stack-capture/missing-stack-source/coherent-store-width all refused with expected diagnostics.

## Narrowing / notes

None required.
