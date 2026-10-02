# Audit-spec review: FABLE cloudint interior citations (fable-how-a-line-of-text-becomes-glyph-quads-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-LINE-OF-TEXT-BECOMES-GLYPH-QUADS` · Package: `_index/candidates/fable-how-a-line-of-text-becomes-glyph-quads-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 10 rows applied, 46 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 10 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 10 rows exact, including the text-to-quad pipeline bodies (glyph lookup, vertex writes and the draw-list handoff).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
