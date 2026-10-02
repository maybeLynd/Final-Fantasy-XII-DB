# Audit-spec review: ASTRA s33 visual retirement clock

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/s33-visual-retirement-clock/`
Board task: `ASTRA-REQ-SPEC-S33-VISUAL-RETIREMENT-CLOCK-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove.py` → exit 0; fresh result byte-identical to retained `result with 75 instruction assertions, 5 closed bodies`.
- **Control re-run in disposable copy:** `control.py` — PASS — failed-capture/missing-source/zero-bodies all refused.

## Narrowing / notes

- Retained pre-repair drivers refuse as designed: `prove-before-call-target-strings.py`/`prove-before-call-tuples.py` pin the superseded call-graph API (string/tuple TypeError); `check-import-prefix-before-syntax.py` is the documented syntax-broken launcher.
- `check_import_prefix.py` now fails its peer-preimage pins because the demanded OPUS repair **landed**: `s33-opus-replay-op1-real/check.py` at `fa6764a48` adds `upstream_guard.verdict(C)` gating with exit-2 refusal — exactly the README-demanded 'require checked nonempty upstream results' repair. Verified at source; the preimage-move refusal is the intended post-repair state.
