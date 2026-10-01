# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-CON-166-QUERY-PASS1 · SWE2-AUDIT-SEM 2026-09-29

`56be8763f`: CON-166 (loader-bound sheet slot-1 row) + query-record pass 1.
Regression re-run non-author: `falsify_query_record.py` — Q0–Q6 SURVIVE, FAILS 0.
Certified image `73461D08…21F8`.

## CON-166 — `0016D6A0` is `ret 0`, not an allocation

Bytes `C2 00 00` = `ret imm16 0`, 3 bytes, int3-padded — byte-exact. 2,868 call
sites (Q6 census). Caveat for the record: `ret 0` preserves caller eax — it is a
no-op stub, and does *not* "return 0" in the eax sense. The sheet's "allocation"
reading is still wrong; the correction's claim as written is exact.

## Q1 attack — pointer width at `0030B6A0`

Byte-verified: `mov r10,rcx` keeps the full pointer; the +0x57C8 reset walks
`lea rax,[rcx+0x57C8]`/`lea rax,[rax+0x40]` (**64-bit**), the +0x59C8 reset
`lea rax,[r10+0x59C8]`/`lea rax,[rax+1]` (**64-bit**); the +0x3C running sums are
`add eax,r10d` (**32-bit**). So resets address through full pointers while the
rebase arithmetic stays 32-bit — exactly the asymmetry Q1 asserts. Had the reset
been a 32-bit add the rebased records' high bits would be lost; it is not.

## Verdict

**ACCEPT.** Both items byte-exact; census boundaries clean.
