# Audit-spec review: OPUS cloudint interior citations (opus-section-008-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SECTION-008-CLOUDINT-1002` · Package: `_index/candidates/opus-section-008-cloudint-1002/` · evidence commit `481cee72b`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows, 10 anchors, rejected/skipped/missing 0.
- Semantic sample: all 2 rows (full population) read against the certified image -- both exact: 0034E9B0 = pop a, pop b, 003DA330(002640C0(), b&0xFFFFFF, a), tail 0026B4E0(rcx,result); 0034EDB0 prepends 00267F90(r9,-1) via or edx,-1.
- Limits hold: body statements only.
