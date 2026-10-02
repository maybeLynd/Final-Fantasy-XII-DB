# Audit-spec review: OPUS cloudint interior citations (opus-script-variables-and-their-storage-class-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SCRIPT-VARIABLES-AND-THEIR-STORAGE-CLASS-CL` · Package: `_index/candidates/opus-script-variables-and-their-storage-class-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 7 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 2 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — both rows exact: 00267560 (n<2 signed -> 14-byte helper(1) ret 0; else byte[n-1] vs byte[n-2] at +4 both==1 -> 1) and 004745B0 (dwords 1/0x12/0 at +0/+4/+0xC, +8 untouched).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
