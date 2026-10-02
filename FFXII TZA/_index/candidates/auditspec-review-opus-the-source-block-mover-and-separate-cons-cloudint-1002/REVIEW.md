# Audit-spec review: OPUS cloudint interior citations (opus-the-source-block-mover-and-separate-cons-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SOURCE-BLOCK-MOVER-AND-SEPARATE-CONS-CL` · Package: `_index/candidates/opus-the-source-block-mover-and-separate-cons-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 3 rows applied, 14 anchors, rejected/skipped/missing 0.
- Semantic sample: all 3 rows read against the certified image — all 3 exact, incl. 00369C60's bt-gate + edx-conditioned repeat loop and 00369CF0's null-record-when-above-14 (ecx=0 fallback verified), 003A3A00's /16 signed-divide rounding.
- Limits hold: body statements only.
