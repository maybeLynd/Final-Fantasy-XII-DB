# Audit-spec review: OPUS cloudint interior citations (opus-the-code-the-function-list-does-not-cont-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-CODE-THE-FUNCTION-LIST-DOES-NOT-CONT-CL` · Package: `_index/candidates/opus-the-code-the-function-list-does-not-cont-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 4 rows applied, 18 anchors, rejected/skipped/missing 0.
- Semantic pass: all 4 rows exact vs the certified image: 001274D0 (movdqu->movdqa 32-byte row copy 4/pass while count>=4 signed with unconditional first pass, then single rows to 0; xmm6/7 saved+restored), 00129870 (16 rows movdqa rcx-row vs lddqu r8-row+0/1/2 psadbw into three paddw accumulators, each accumulator's two 64-bit halves summed, dwords at +0/+4/+8 of stack arg5), 0012A290 (8x16B rows at stride 2*rdx, three paddw/psubw butterfly stages, wd/dq/qdq 8x8 transpose, three more stages, stores r8+0..+0x70, xmm6-9 saved+restored), 0026A420 (byte+3 &0xE0 ==0x60 -> tail 002E5B00 else ret).
- Limits hold: body statements only.
