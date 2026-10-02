# Audit-spec review: OPUS cloudint interior citations (opus-contract-actor-record-pool-and-region-ma-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-ACTOR-RECORD-POOL-AND-REGION-MA-CL` · Package: `_index/candidates/opus-contract-actor-record-pool-and-region-ma-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 3 rows applied, 15 anchors, rejected/skipped/missing 0.
- Semantic pass: all 3 rows exact vs the certified image (actor-record pool/region management bodies incl. the dword 0208E6A0-indexed scan with non-null + byte+5==1 + byte+0xE98==0 gates).
- Limits hold: body statements only.
