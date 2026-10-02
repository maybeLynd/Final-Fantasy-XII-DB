# Audit-spec review: OPUS cloudint interior citations (opus-sloc-menumap-container-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SLOC-MENUMAP-CONTAINER-CLOUDINT-1002` · Package: `_index/candidates/opus-sloc-menumap-container-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing 0.
- Semantic sample: all 1 rows read against the certified image — 00377400 exact: unsigned 0..3 gate on movsxd ecx, byte store 02ADD0E8, table-indexed 003C63A0 call, tail 00379870(ecx).
- Limits hold: body statements only.
