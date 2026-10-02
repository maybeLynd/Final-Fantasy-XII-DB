# Audit-spec review: OPUS cloudint interior citations (opus-the-movement-body-pool-and-the-separatio-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MOVEMENT-BODY-POOL-AND-THE-SEPARATIO-CL` · Package: `_index/candidates/opus-the-movement-body-pool-and-the-separatio-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 8 rows applied, 35 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 8 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all rows exact vs the certified image, including the body-pool walk and separation bodies (node-list traversal, unlink semantics, 60k caps).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
