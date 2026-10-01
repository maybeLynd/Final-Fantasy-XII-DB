# Audit-spec review: ASTRA bj1 guard preparation

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/bj1-guard-preparation/`
Board task: `ASTRA-REQ-SPEC-BJ1-GUARD-PREPARATION-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `check_bj1_preparation.py` → exit 0; fresh result byte-identical to retained `coverage/preparation receipts reproduce against the package inputs`.
- **Control re-run:** `control_bj1_prerequisites.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS.
- **Control re-run:** `control_bj1_guard_capture-before-read-diagnostic-01.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS_TRANSPORT_ONLY_CONTEXT_STILL_REQUIRED.
- **Control re-run:** `control_bj1_guard_capture-before-pid-handshake-02.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS.
- **Control re-run:** `control_bj1_guard_capture-before-launcher-regression-03.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS.

## Narrowing / notes

- `control_bj1_guard_capture.py` fails on this host with 'expected observed host redirector boundary changed' — the transport observation is pinned to the authoring machine's Python redirector behaviour (the method doc records the Windows venv redirector as the diagnosed cause). Environment-dependent observation, not an evidence defect; all before-variant controls and the preparation check reproduce.
