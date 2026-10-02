# Audit-spec review: OPUS cloudint interior citations (opus-the-six-vfx-display-layers-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SIX-VFX-DISPLAY-LAYERS-CLOUDINT-1002` · Package: `_index/candidates/opus-the-six-vfx-display-layers-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 5 rows applied, 23 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 5 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 5 rows exact: 0017FDE0/0017FE60/0017FEE0 (01F7F598 getter -> per-arm helper -> byte+8 gate -> qword+0 or 0), 001B2600 (157-byte helper then byte+0x98 nonzero -> tail 38-byte helper with 3), 003A3990 (dword 02AEF414-re-read loop over 02AEF420 qwords calling helper(qword,2) then zeroes the count).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
