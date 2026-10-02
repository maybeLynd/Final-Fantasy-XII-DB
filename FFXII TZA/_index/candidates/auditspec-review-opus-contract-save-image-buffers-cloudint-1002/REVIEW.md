# Audit-spec review: OPUS cloudint interior citations (opus-contract-save-image-buffers-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-SAVE-IMAGE-BUFFERS-CLOUDINT-1002` · Package: `_index/candidates/opus-contract-save-image-buffers-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 9 rows applied, 40 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 9 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 9 rows exact vs the certified image, including the buffer-setup and copy bodies (record sizes, null-guarded reads, direction and loop termination).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
