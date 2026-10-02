# Audit-spec review: OPUS cloudint interior citations (opus-how-a-combo-continues-and-what-it-blocks-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-A-COMBO-CONTINUES-AND-WHAT-IT-BLOCKS-CL` · Package: `_index/candidates/opus-how-a-combo-continues-and-what-it-blocks-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 10 anchors, rejected/skipped/missing 0.
- Semantic pass: both rows exact vs the certified image: 0031B4B0 (rcx->00263E30(rcx) or 0 when null, tail 0031ADB0 with edx/r8 preserved) and 003592C0 (bts/btr bit ecx of 022C8005 on edx; OR of 022C8004/005/006/007 bit 0 + 003588B0(dword 022C7FE0) non-null -> tail 0026D6D0).
- Limits hold: body statements only.
