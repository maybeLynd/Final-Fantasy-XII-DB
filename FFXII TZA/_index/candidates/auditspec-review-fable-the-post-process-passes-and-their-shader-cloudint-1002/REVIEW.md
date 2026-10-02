# Audit-spec review: FABLE cloudint interior citations (fable-the-post-process-passes-and-their-shader-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-POST-PROCESS-PASSES-AND-THEIR-SHAD` · Package: `_index/candidates/fable-the-post-process-passes-and-their-shader-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 12 rows applied, 55 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 12 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 12 rows exact vs the certified image, including the pass-setup and shader-selection bodies (descriptor slots, ordered validation calls and return propagation).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
