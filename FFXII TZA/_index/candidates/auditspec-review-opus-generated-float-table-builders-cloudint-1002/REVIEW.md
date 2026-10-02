# Audit-spec review: OPUS cloudint interior citations (opus-generated-float-table-builders-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-GENERATED-FLOAT-TABLE-BUILDERS-CLOUDINT-100` · Package: `_index/candidates/opus-generated-float-table-builders-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 1 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all rows exact vs the certified image, including the generated table-fill loops (constants, strides, bounds and store order).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
