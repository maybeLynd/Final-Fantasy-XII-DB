# Audit-spec review: FABLE cloudint interior citations (fable-the-text-element-dispatch-table-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-TEXT-ELEMENT-DISPATCH-TABLE-CLOUDI` · Package: `_index/candidates/fable-the-text-element-dispatch-table-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 5 rows applied, 25 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 5 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 5 rows exact: 002477A0 (bits 16-18 of dword+0x44 replaced by dx&7, shl 0xD/sar 0x1D re-read; bit18-set arm stores 0xF9 selectively; clear arm stores 0xF9/6 via cmovne), 0029B870 (six sequential w-tests -> codes 3/8/6/2/4/5 with handler call+continue-on-zero except code3; neg/sbb/cmove bit6-minus-bit4 for x and y; 002975B0; n==b -> 7-via-0029B790 else entry-word updates at 0x160 stride + byte+0xB48=n + ret 1), 0029C770/0029C9D0 (00273A20 gate then eight-call init sequence + per-entry loops over byte+0xB42), 00299090 (byte-map + offset-table dispatch decoded: six arms verified).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
