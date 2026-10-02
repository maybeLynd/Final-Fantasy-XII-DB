# Audit-spec review: OPUS cloudint interior citations (opus-section-004-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SECTION-004-CLOUDINT-1002` · Package: `_index/candidates/opus-section-004-cloudint-1002/` · evidence commit `8e4dd05e2`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows, 5 anchors, rejected/skipped/missing 0.
- Semantic sample: all 1 rows (full population) read against the certified image -- 003DFCC0 exact: five-way early-out (null qword 02B59D58, byte+7 unsigned-below-0x32, signed jge vs word+8, ecx==0, ecx-1 unsigned >8) then word at +0xC+ecx*4.
- Limits hold: body statements only.
