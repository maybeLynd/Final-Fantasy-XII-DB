# Audit-spec review: OPUS cloudint interior citations (opus-referenced-code-the-list-never-had-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-REFERENCED-CODE-THE-LIST-NEVER-HAD-CLOUDINT` · Package: `_index/candidates/opus-referenced-code-the-list-never-had-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows applied, 10 anchors, rejected/skipped/missing 0.
- Semantic pass: all 4 rows exact vs the certified image: 00263A30 ('NOACTOR' 00915708 default; ecx<=4, 0x288-record at 02098E10 byte+0x10 bit0, non-null qword+0, edx < dword+0x20 signed, 00358940 non-null + non-null qword+0x40 -> returns qword+0 + dword+0x4C + sext(dword[+0x40])), 0034ED80 (tail 002EC3C0 rcx=rdx edx=1), 00350320 (tail 0026DC50 rcx=rdx edx=0), 00354950 (ecx=1 tail 003DE3E0).
- Limits hold: body statements only.
