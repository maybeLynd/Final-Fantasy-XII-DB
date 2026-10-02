# Audit-spec review: OPUS cloudint interior citations (opus-duplicated-function-names-and-how-to-res-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-DUPLICATED-FUNCTION-NAMES-AND-HOW-TO-RES-CL` · Package: `_index/candidates/opus-duplicated-function-names-and-how-to-res-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 6 anchors, rejected/skipped/missing 0.
- Semantic pass: both rows exact vs the certified image; 00237690 verified in full: signed bound on dword 0208E6A0, 00321170(index), non-null + non-null +0x698 + byte+5==1 + byte+0xE98==0 gates, then 00300E40(result,0).
- Limits hold: body statements only.
