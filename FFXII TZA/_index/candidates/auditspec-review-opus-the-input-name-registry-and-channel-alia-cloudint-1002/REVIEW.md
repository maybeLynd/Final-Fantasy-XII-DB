# Audit-spec review: OPUS cloudint interior citations (opus-the-input-name-registry-and-channel-alia-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-INPUT-NAME-REGISTRY-AND-CHANNEL-ALIA-CL` · Package: `_index/candidates/opus-the-input-name-registry-and-channel-alia-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing 0.
- Semantic sample: all 1 rows read against the certified image — 001E0E00 exact: 00796E20() -> +0xDF8 qword, ecx+1, 0079E6D0, movzx al.
- Limits hold: body statements only.
