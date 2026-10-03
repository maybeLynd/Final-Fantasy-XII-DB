# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PText module (opus-member-teen-modules-registered-before-main-phyre-ptext-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-TEEN-MODULES-REGISTERED-BEFORE-MAIN` · Package: `_index/candidates/opus-member-teen-modules-registered-before-main-phyre-ptext-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 399ce7caf)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 7 functions, 33 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 7 rows, mode `member`, family `Phyre PText module`; rejected 0, skipped 0, missing 0, corrections none.
- Semantic pass: **all 7 rows** (the request asks for at least 15; the record has 7) read clause by clause against `disr.py` output of the certified image, field-name strings resolved from `.rdata`:
  - `0067CC20` exact: two (count, pointer) pairs `+0x20/+0x28` then `+0x10/+0x18`; `shr 0x1f; not al; test al,1; je` skips the free when bit 31 is SET, so `00584730` runs only with the bit clear and a non-null pointer; pointer then count zeroed (`0067CC54/58`, `0067CC76/7A`).
  - `0067CE70` exact: `ecx==0` -> 0 (`0067CEEF`); `0017D260(ecx*0x30, 4)` (`lea rcx,[rsi+rsi*2]; shl rcx,4`); three `movups` per element; returns `rdx`=p, or 0 from the failed allocation.
  - `0067CF00` exact: copy loop count `esi`=`r8d`; tail fill `edi-esi` elements, element base `rax-8`: dword `+0`, qwords `+4/+0xC/+0x14/+0x1C/+0x24` (five from `+4`), byte `+0x2C`; returns `r8`=p; 0 on `ecx==0` or null allocation.
  - `0067CFE0` exact: all seven names confirmed (`m_fontSize` 00D6D9E0 ... `m_bitmapFontTexture` 00D6DA40); stack args of every `00632960` call (`[rsp+0x20]`=n 4/0/8/0xC, `+0x28`=0x10, `+0x30`=0, `+0x38`=0) and of both `00632A10` calls (0x10/0x20, 0, 3, 4); records, types, guard pattern (`cmp guard,epoch; jle`; `_Init_thread_header` 008092FC / footer 0080929C; atexit 00808B90), the two stores `00D6D988`->02E40070 and `00D69508`->02E400E0, the unguarded `0067D810(qword 01F2EAB8)`, `00630110()`, `00668E10(qword 01F2EAC0)`, the `or 0x10` on 02E40098 / 02E40108, `m_bitmapFontTexture` with r8 = 02CBB900, n 0x30, 0x12, and the tail `jmp 00639450` with rcx = 02E3FA60.
  - `0067D3B0` exact: nine names and n values confirmed; the three `00632A70` calls take (n, 0, 2) at `[rsp+0x20/0x28/0x30]`; `or 0x10` on 02E3FCA8 / 02E3FDD8 / 02E3FE48 each after its `00632A70` group; tail `jmp 00639450(02E3F960)`.
  - `0067E250` exact: early `je` compares `edx` with the full dword `[rcx]`; `btr r8d,0x1f` then `cmovb` gives the minimum; `lea eax,[rsi+0xd]` with `rsi`=0 returns 0xD only when `edi`!=0; free gate `cmp rcx,rsi; je` / bit-31 test / null test; stores `rsi`, `edi`; returns 0.
  - `006CCD60` exact.
- Advisory, not a defect: in `0067E250` the `min` is an unsigned minimum (`cmovb`, 0067E273); the sentence does not claim a signedness, and with the second operand masked to 31 bits it differs from a signed minimum only when `edx` has bit 31 set. OPUS may add "(unsigned)" in a later pass.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
- Batch-wide sentence, not this record's rows: the README's "262 stood, 10 clauses in 8 functions were corrected" (shared by all 11 records of 399ce7caf) does not match the `rows.json` corrections, which total 12 entries in 10 functions across the 11 records. The narrowing is recorded once, in `auditspec-review-opus-phyre-members-399ce7caf`.
