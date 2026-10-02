# Audit-spec review: OPUS cloudint interior citations (opus-five-small-bin-tables-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FIVE-SMALL-BIN-TABLES-CLOUDINT-1002` · Package: `_index/candidates/opus-five-small-bin-tables-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 5 rows applied, 17 anchors, rejected/skipped/missing 0.
- Semantic sample: all 5 rows read against the certified image — all 5 exact, incl. 0035B3E0's indexed dword-rewrite loop (count at +4, base rcx+8, low-32(rcx) addend) and 003C9950's five-arg 00249210 call with stack arg 0.
- Limits hold: body statements only.
