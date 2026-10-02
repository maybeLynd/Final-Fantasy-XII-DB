# Audit-spec review: ASTRA render removal phase contracts

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `ASTRA-REQ-SPEC-RENDER-REMOVAL-PHASE-CONTRACTS-1002` · Package: `_experiments/evidence/render-removal-phase-contracts/`

## Verdict: ACCEPT

## What was checked

- `prove.py` re-run fresh in a disposable copy → exit 0; result byte-identical to retained `result-01.json`:
  original mark/no-op/unlink-clear contracts and count-before-cleanup order
- Shared pinned driver `prove_owner_reload_order.py` re-run against `evidence/owner-reload-order` (argv[2], per the
  driver's src signature) → exit 0, output byte-identical to the shared retained
  `owner-reload-order-result-01.json` (CONDITIONAL_RELOAD_ORDER: 11 static partitions; local waits require live
  group0 AND nonzero byte gate; lifetime remains OPEN).
- `control.py` re-run in the disposable copy (immutable controls stripped) → exit 0: PASS — four actual producer refusals and upstream-before-output control.

## Notes

- STATIC_ONLY / static partitions: no native, game or live execution; lifetime/reuse questions remain OPEN by
  design, as the results themselves state.
