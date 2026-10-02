# Audit-spec review: OPUS cloudint interior citations (opus-ebp2-container-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-EBP2-CONTAINER-CLOUDINT-1002` · Package: `_index/candidates/opus-ebp2-container-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing 0.
- Semantic sample: all 1 rows read against the certified image — 00297640 exact: cmp edx,7 unsigned gate, and the 8-entry offset table at 002976E8 decoded against the image (0->1, 1->BB00/C60(1), 2->+0x318 bit1, 3->299B90 word+0x14, 4/5/7->0, 6->C60(5) then 0).
- Limits hold: body statements only.
