# Audit-spec review: FABLE cloudint interior citations (fable-how-a-camera-reaches-the-renderer-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-CAMERA-REACHES-THE-RENDERER-CLOU` · Package: `_index/candidates/fable-how-a-camera-reaches-the-renderer-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 8 rows applied, 34 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 8 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 8 rows exact, including the camera-state-to-render path (descriptor reads, slot bounds and the publish calls).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
