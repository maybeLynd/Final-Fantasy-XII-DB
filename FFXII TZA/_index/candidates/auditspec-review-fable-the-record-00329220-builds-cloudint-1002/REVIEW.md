# Audit-spec review: FABLE cloudint interior citations (fable-the-record-00329220-builds-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-RECORD-00329220-BUILDS-CLOUDINT-10` · Package: `_index/candidates/fable-the-record-00329220-builds-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 17 rows applied, 81 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 17 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 17 rows exact vs the certified image, including the record-build body (field writes, stride and count semantics) and its helper calls.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
