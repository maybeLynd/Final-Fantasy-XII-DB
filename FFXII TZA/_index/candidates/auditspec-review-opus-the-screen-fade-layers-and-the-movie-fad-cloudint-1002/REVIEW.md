# Audit-spec review: OPUS cloudint interior citations (opus-the-screen-fade-layers-and-the-movie-fad-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SCREEN-FADE-LAYERS-AND-THE-MOVIE-FAD-CL` · Package: `_index/candidates/opus-the-screen-fade-layers-and-the-movie-fad-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 7 rows applied, 29 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 7 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all rows exact vs the certified image, including the fade-layer and movie-fade bodies (state machines, globals and the ordered calls).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
