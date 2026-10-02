# Audit-spec review: OPUS cloudint interior citations (opus-how-the-engine-chooses-3d-or-flat-moveme-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-THE-ENGINE-CHOOSES-3D-OR-FLAT-MOVEME-CL` · Package: `_index/candidates/opus-how-the-engine-chooses-3d-or-flat-moveme-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 16 rows applied, 76 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 16 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all rows exact vs the certified image, including the movement-mode selection bodies (flag tests, the 3D/flat branches and the shared tails).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
