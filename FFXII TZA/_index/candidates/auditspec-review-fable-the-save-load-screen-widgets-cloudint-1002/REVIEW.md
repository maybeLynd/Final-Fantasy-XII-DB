# Audit-spec review: FABLE cloudint interior citations (fable-the-save-load-screen-widgets-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-SAVE-LOAD-SCREEN-WIDGETS-CLOUDINT` · Package: `_index/candidates/fable-the-save-load-screen-widgets-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 10 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 2 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — both rows exact: 003BB2C0 (5 -> dword 02B40E1C; 0 -> dwords 02B40EC0/02B40FE4/02B40E10 and qword 02B40E14; returns 0) and 0057E950 (re-cited; byte-exact).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
