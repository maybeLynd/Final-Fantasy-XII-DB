# Audit-spec review: OPUS cloudint interior citations (opus-the-element-types-40-42-a0-ab-d0-d1-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-ELEMENT-TYPES-40-42-A0-AB-D0-D1-CLOUDIN` · Package: `_index/candidates/opus-the-element-types-40-42-a0-ab-d0-d1-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 14 rows applied, 63 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 14 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all rows exact vs the certified image, including the per-type arm bodies and the shared table decode.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
