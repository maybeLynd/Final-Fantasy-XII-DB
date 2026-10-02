# Audit-spec review: FABLE cloudint interior citations (fable-the-phyre-post-effect-class-family-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-PHYRE-POST-EFFECT-CLASS-FAMILY-CLO` · Package: `_index/candidates/fable-the-phyre-post-effect-class-family-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 8 rows applied, 36 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 8 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 8 rows exact vs the certified image, including 00658470 (ten unordered-aware ucomiss float pairs, the +0x198..+0x178 descriptor walk with tags 0x42/0x43, table picks 02D36FC0/02D37FC0/02D36FA0) and the sibling validation bodies (bounds, 0x1FFF length masks, error/fallback vtables).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
