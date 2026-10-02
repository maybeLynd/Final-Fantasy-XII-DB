# Audit-spec review: FABLE cloudint interior citations (fable-the-menu-screen-atlas-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-MENU-SCREEN-ATLAS-CLOUDINT-1002` · Package: `_index/candidates/fable-the-menu-screen-atlas-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 13 rows applied, 62 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 13 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 13 rows exact vs the certified image, including 002C1000's license-grid arm (lea ecx,[rax+0x50] with rax=1 -> 0x51), 00560210's license-details arm (color-pair split 0xFC/0xFA vs 0xFD/0xFB, b/a/c reordering, all child writes), and the remaining atlas dispatcher bodies.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
