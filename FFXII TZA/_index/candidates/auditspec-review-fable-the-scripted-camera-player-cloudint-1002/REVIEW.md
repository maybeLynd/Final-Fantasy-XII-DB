# Audit-spec review: FABLE cloudint interior citations (fable-the-scripted-camera-player-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-SCRIPTED-CAMERA-PLAYER-CLOUDINT-10` · Package: `_index/candidates/fable-the-scripted-camera-player-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 15 rows applied, 69 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 15 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 15 rows exact vs the certified image, including the script-parameter extraction, float conversion and radius tests, squared-distance comparisons, tail-jump argument placement, bitfield updates and the four-way vs two-axis distance logic.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
