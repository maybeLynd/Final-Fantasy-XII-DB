# Audit-spec review: OPUS cloudint interior citations (opus-the-box-renderer-that-is-never-called-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-BOX-RENDERER-THAT-IS-NEVER-CALLED-CLOUD` · Package: `_index/candidates/opus-the-box-renderer-that-is-never-called-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 3 rows applied, 15 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 3 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 3 rows exact: 0029B7D0 (edx==1 -> 002973E0(rcx,[r8],[[+0x48]+0x24],[r8+4]); -1 on 0), 0029B810 (edx==2 -> [rcx+4]=dword+0x2C<<4; edx==1 -> dword+0x30 * byte+0x87-when-nonzero arg), 002C0B40 (case1 qword[[rdx+8]] -> +0xC0, clear bit7 of +0x40, 00247570(rcx,002735E0(1)), +0xD8=0x800080; case3 signed (word*word)>>7 scales at +0x5A/+0x58).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
