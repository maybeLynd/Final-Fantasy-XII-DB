# Audit-spec review: ASTRA ov21 bank capacity domain

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/ov21-bank-capacity-domain/`
Board task: `ASTRA-REQ-SPEC-OV21-BANK-CAPACITY-DOMAIN-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result-03.json — 'PROVED conditional located boot local store320, overlapping reset clear and distinct allocator-failure paths'`.
- **Prover re-run fresh:** `prove-02-driver.py` → exit 0; fresh result byte-identical to retained `result-02.json`.
- **Control re-run in disposable copy:** `control.py` — PASS — three cause-specific refusals plus prior positive.

## Narrowing / notes

- `prove-01-driver.py` refuses at HEAD ('unclosed local CFG 0x5211f0') — per README this is the preserved failed proof-01 invocation (the local CFG omitted the tail callee); prove-02/prove-03 are the operative proofs.
