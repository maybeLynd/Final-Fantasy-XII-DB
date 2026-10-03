# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 1 (opus-member-modules-registered-before-main-phyre-phyrecore-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-F7B59` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 17 rows read are exact at the bytes, and the record's four corrections are right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 26 functions, 116 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 26 rows, 116 anchors, mode `member`, family `Phyre PhyreCore module`. Skipped 0, missing 0. Rejected 14, each "not an entry-only frontier function of the page": `0016EE70`, `0017D670`, `0017D6B0`, `0017E440`, `0017ED20`, `00182F70`, `00185800`, `001867A0`, `001867E0`, `00186990`, `001869E0`, `0018B0B0`, `00195440` and `001954B0`. Corrections 4, in 3 functions.
- Corrections, all 4 confirmed at the bytes and present in the rows:
  - `00186670`: `cmp [rax+0xa8],-1; jl` (0018669E), now "less than -1 (signed)".
  - `00194A30`: `test eax,eax; jle` (00194A41), now "greater than 0 (signed)".
  - `001967D0`, outer bound: `cmp r14,0x150; jl` (0019693E), now "less than 0x150 (signed)".
  - `001967D0`, missed path: the byte copy into `u` runs only when `v - 1` is above 2 (`ja` 0019686C). A null `p` with `v` in 1..3 jumps to 001968BA and does nothing; the row now says so.
- Semantic pass: **17 of 26 rows**, spread over the package and including the three corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings, constants and imports resolved:
  - `00158FE0` exact: the `lock add +1` and `lock add -1` bracket every path; a non-zero `00158F60(0)` result jumps straight to the decrement.
  - `00159180` exact: the fifth argument of `f` is read at `[rsp+0x70]` (entry `+0x28`) and passed at `[rsp+0x20]`.
  - `0017DAC0` exact: `SystemParametersInfoW` is the import at IAT slot `008C2818`, with `ecx` 0x3A then 0x3B; `shr 2; and 1` extracts bit 0x4; `cmovne` selects set or clear.
  - `0017FE50` exact.
  - `00185DA0` exact: `movsxd rdx,r8d` (sign-extended index). The `0060D190` args are `xmm1..xmm3` = 0 and `[rsp+0x20]` = 01CEBBA8 = 1.0.
  - `00186670` exact (corrected row): the stores go to `b+0xD0` / `+0xC8` / `+0xD4` from `g+0xC10` / `+0xC14` / `+0xC18`, each followed by `call [rdx+8]`. The `00189130` floats are `xmm2` = `[g]`, `xmm3` = `[g+4]` and `[rsp+0x20]` = `[g+0xC1C]`. Both the condition-fail path and the copy path return `0018A620()` + 8.
  - `001893C0` exact. The three `005DC190` targets are `rsp+0x50` (a), `+0x68` (b) and `+0x38` (c). The `0060F6B0` call takes `r9d` = `w` and `[rsp+0x20]` = `h`, with `[rsp+0x28]` = 0. The release order is c, b, a.
  - `00189560` exact.
  - `00189C20` exact: 008C5F70 = 1.570796 and 01CEBB70 = 0.5. `s * [+0xD4]` divided by `[+0xC8]` goes to `+0x38`. `(b + a) * (1 / (a - b))` goes to `+0x60`. `addss xmm5,xmm5` doubles `b*a*(1/(a-b))` for `+0x70`. The five qword zero stores and the dword zero store all match.
  - `00193940` exact: `jns` handles the negative case; `cmovg` caps at 3 (signed, stated).
  - `00193A00` exact: the second gate is re-tested before the `maxss` store; the tail is `jmp 001939A0`.
  - `00194240` exact.
  - `00194A30` exact (corrected row).
  - `001955B0` exact.
  - `00195C10` exact: `(rcx - (rcx+0x70) + 0x72) >> 1` = 1.
  - `001967D0` exact (corrected row). `v` comes from `01DF1738 + 4*(0xD + (m != 0))` at stride 0x15C, three times. In the second phase, `neg; sbb; lea edi,[rax+2]` gives `k` = 1 for non-zero `m`, else 2. That phase covers 17 bytes `q+0x30..q+0x40` for `o` = 0x88..0x110.
  - `001997F0` exact. Each set zeroes four qwords from `set+8` (through `set+0x20`) before the allocator call; the allocator argument is the `rax` returned by the stack `001EDF00(…, "EASTL set")` call. The grow and shrink arms split on `jbe` (unsigned) with `count = (end - begin) >> 4`. `b` = byte `[rsp+0x90]`, which is the entry `+0x18` home slot (7 pushes + 0x40); the body writes only the `rcx` and `rdx` home slots.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions. Every FIX entry equals a `rows.json` correction, and its `new` text is in the row.
  - The commit subject's "40+6 clauses" reads the same way; the PhyreCore part is 34.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
