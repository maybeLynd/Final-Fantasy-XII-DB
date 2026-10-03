# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 2 (opus-member-modules-registered-before-main-phyre-phyrecore-module-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-96B6B` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-2/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 18 rows read are exact at the bytes, and all 10 of the record's corrections are right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 33 functions, 148 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 33 rows, 148 anchors, mode `member`, family `Phyre PhyreCore module`. Missing 0. Corrections 10, in 7 functions.
  - Rejected 6, each "not an entry-only frontier function of the page": `0019A0A0`, `0019B190`, `001A7750`, `001DAD60`, `001DB640` and `001DBA40`.
  - Skipped 1: `001B2A30`, "too large for one precise sentence" (1950 B).
- Corrections, all 10 confirmed at the bytes and present in the rows:
  - `0019B200`: `00809054` gets `rcx` = qword `[rcx+0x10]` itself (= `b`+8, 0019B21C), and only `00809950` gets `b`.
  - `0019B480` x2: `lea rcx,[rbx-0xa0]` = `rcx`+8 for `0019B400`, and `lea rcx,[rbx-0x98]` = `rcx`+0x10 for the ostream destructor.
  - `0019DAD0`, `0019F6F0` and `0019F930` x2: `this` is the inline allocator object (`lea rcx,[rbx+0x18]` / `[rdi+0xb0]` / `[rdi+0x10]` with `rdi` = `rcx`+0x50), and the vtable is the qword at that address.
  - `001B26F0`: `00189120()` is called at 001B26F9 before the all-zero scan.
  - `001C3C30` x2: `jle` at 001C3CBE and at 001C3D04 (signed).
- Semantic pass: **18 of 33 rows**, spread over the package and including all seven corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings, imports and division magics resolved:
  - `00199F60` exact. The stack block is `p` = `rsp+0x20`. The stores are dword `p+0x18` = 2, dword `p+8` = 0x10000, qword `p+0x20` = name and qword `p+0x10` = `rcx`. `cmovne` picks 008F3C88 "AsyncJobManager No Read No Write Thread" when dword `[rcx+0x150]` is non-zero, else 008F3C70.
  - `0019A2A0` exact: three `00210EC0(0x18)` blocks, the unconditional first-byte stores through the three qwords, and the `00809950` call under the just-zeroed dword.
  - `0019AE70` exact: `CryptAcquireContextW` is the import at IAT slot `008C2000`, with args (`rcx`, 0, 0, 1, `[rsp+0x20]` = 0xF0000000); the tail is `jmp [008C20B0]` = `InitializeCriticalSection`.
  - `0019B200` exact (corrected row): the size is `mul` + `cmovo` and `add 8` + `cmovb` (all ones on overflow). `00808FE4` takes (`a`+8, 0x98, `n`, 0019A3B0, `[rsp+0x20]` = 0019A500). `CloseHandle` is at `008C23E0` and `CreateSemaphoreW` at `008C2100`.
  - `0019B480` exact (corrected row): vtable 008F3F48 stored at `rcx`+`v`; dword at `rcx`+`v`-4 = `v` - 0xA8; the destructors are MSVCP140 basic_ostream<char> (`008C25D0`) and basic_ios<char> (`008C25E8`, tail jump with `rcx`+0xA8).
  - `0019B540` exact.
  - `0019DAD0` exact (corrected row): magic 0x0EA0EA0EA0EA0EA1 with `sar 4` (signed /0x118), then `imul 0x118`.
  - `0019F6F0` exact (corrected row): magic 0x6666666666666667 with `sar 7` (/0x140), then `*5 << 6`.
  - `0019F930` exact (corrected row): vtable 008F46F0; magic 0x2AAAAAAAAAAAAAAB with `sar 2` (/0x18). The list walk reads next before each call and passes (`rcx+0x60`, node, 0x18).
  - `001A11F0` exact.
  - `001B10D0` exact. The fifth and sixth arguments are at `[rsp+0x50]` / `[rsp+0x58]`. The descent goes to child `+0` when the node key is below the search key (`jb`, unsigned) and to `+8` otherwise, keeping the last node that was not below. The exact-match test is `jae`. Both `001FB720` argument sets match.
  - `001B26F0` exact (corrected row): the scan counts eight 0x1C-stride dwords from `rcx+4`. The `005FEB30` first argument is qword `+8` of the result of that first `00189120()` call. The copy is 14 `movups` = 0xE0 bytes.
  - `001BD7D0` exact.
  - `001C3C30` exact (corrected row). The `sete` flips; `cmove ecx,eax` on the old 01F81284 value (1). The second `cmove eax,edi` uses the ZF from `sub edx,1`. The final `cmovne ecx,ebx` stores `ecx` only on a non-zero `al`.
  - `001D6BE0`, `001DC480` (01CEBB70 = 0.5), `001DE3B0` and `001DE4A0` exact.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
