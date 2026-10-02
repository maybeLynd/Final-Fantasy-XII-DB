# Audit-spec review: OPUS cloudint interior citations (opus-contract-corridor-query-family-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-CORRIDOR-QUERY-FAMILY-CLOUDINT-100` · Package: `_index/candidates/opus-contract-corridor-query-family-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 9 anchors, rejected/skipped/missing 0.
- Semantic sample: all 2 rows read against the certified image - 0030BEB0's four-way early-out + bit-23 select and 0033F7F0's nested tail-jump both exact.
- Limits hold: body statements only; the cloud draft is a pointer, OPUS's re-read stands.
