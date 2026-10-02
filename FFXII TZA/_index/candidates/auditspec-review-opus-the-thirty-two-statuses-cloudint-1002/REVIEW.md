# Audit-spec review: OPUS cloudint interior citations (opus-the-thirty-two-statuses-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-THIRTY-TWO-STATUSES-CLOUDINT-1002` · Package: `_index/candidates/opus-the-thirty-two-statuses-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 8 anchors, rejected/skipped/missing 0.
- Semantic pass: both rows exact vs the certified image: 00238640 (rcx = 02F973C0 + movsxd(ecx)*8, tail 003845F0) and 0030AE30 (cx==0xFFFF or (cx&0xF000)>0xE000 unsigned -> -1; record 01EEBCC0+(word>>12)*0x58; low12 > dword+0x3C-1 signed or null qword+0x50 -> 0; else tail-jump qword+0x50 with ecx=word, edx=1).
- Limits hold: body statements only.
