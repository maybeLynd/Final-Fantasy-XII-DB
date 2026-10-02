# Audit-spec review: OPUS cloudint interior citations (opus-where-mp-comes-from-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHERE-MP-COMES-FROM-CLOUDINT-1002` · Package: `_index/candidates/opus-where-mp-comes-from-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 13 rows applied, 54 anchors, rejected/skipped/missing 0.
- Semantic sample: all 13 rows read against the certified image — all 13 exact, incl. the 00263F10-resolve/two-pop/tail family (00341140/00341690/00341EE0/00342500), 00342150's cmove-equality select, 0034A4C0's three-pop double-resolve, and 00473A90's bts/cmove flag-word builder with null-rcx -> -1.
- Limits hold: body statements only.
