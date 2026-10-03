# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 5 (opus-member-modules-registered-before-main-phyre-phyrecore-module-5)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-E114D` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-5/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 18 rows read are exact at the bytes, and all 7 of the record's corrections are right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 31 functions, 155 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 31 rows, 155 anchors, mode `member`, family `Phyre PhyreCore module`. Missing 0. Corrections 7, in 7 functions.
  - Rejected 7, each "not an entry-only frontier function of the page": `0021BDB0`, `0021CC10`, `00221140`, `002211B0`, `00221220`, `00221FB0` and `00222CB0`.
  - Skipped 2, both "too large for one precise sentence": `0021BFD0` and `0021CE30`.
- Corrections, all 7 confirmed at the bytes and present in the rows:
  - Six are inline allocator objects passed as `this`, with the vtable at that address: `0021BE80`, `0021CCE0` and `0021E730` (`rcx+0x18`), `0021C280` (`rcx+0x50`), `00220B80` (`t+0x30`) and `002236B0` (`rcx+0x30`).
  - `002240B0`: the tree descent uses `jl` at 00224113 on the signed key.
- Semantic pass: **18 of 31 rows**, spread over the package and including all seven corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings and division magics resolved:
  - `0021B160` exact: `0021B350(rcx, edx)`; stride 0xA0. `b` is byte `[rsp+0x50]` (the `rcx` home slot), read at 0021B18B before its first write at 0021B1B0. The final store is `sete` on byte `+0x90`.
  - `0021B8F0` exact: the backward walk and all fifteen field copies; it returns the destination start.
  - `0021BA60` exact: the same field list from the single source.
  - `0021BBF0` exact: vtable 00907F90 after `00217F10(d, s)`, then the nine copies at `+0x38..+0x60`.
  - `0021BE80` exact (corrected row): element loop `jae`/`jb` with stride 0x68; magic 0x4EC4EC4EC4EC4EC5 with `sar 5` (/0x68).
  - `0021C280` exact (corrected row): tail `00224BF0(v)` for non-null `v`, else 0.
  - `0021C330` exact: `0021B9B0(r8, end, rdx)`. The end adjustment is `imul` by 0xB13B13B13B13B13B (the negated /0x68 magic), `sar 5`, `imul 0x68`, then `add [rcx+8]`; it moves end back by the erased whole elements. It returns `rdx`.
  - `0021C4F0` exact: `t` = `rsp+0x30`; the split is `cmp edi,edx; jbe` (unsigned); the shrink arm calls `0021C330(rcx, begin + edx*0x68, end)`.
  - `0021C960` exact: forward walk with stride 0x48; it returns the destination end.
  - `0021CA90` exact: vtable 009081A0.
  - `0021CCE0` exact (corrected row): magic 0x0E38E38E38E38E39 with `sar 2` (/0x48), then `*9 << 3`.
  - `0021D440` exact: `0021D580`; stride 0x48.
  - `0021E730` exact (corrected row): magic 0x6666666666666667 with `sar 2` (/0xA), then `*5 + *5`.
  - `00220B80` exact (corrected row). The walk calls `00809950([node+0x28])` with `edx` unset, then `0016D6D0(node)` for next. After the tree empty-out and reset come the three `005CD6D0` calls and the tail `jmp 005CD6D0` with `rcx+0x378`.
  - `002235F0` exact: `00221780(rcx, 2)`, vtable 00907D80, the map built from 008F4120 "EASTL map", dword `+0x90` = 2.
  - `002236B0` exact (corrected row).
  - `00223730` exact: `00809950([rcx+0x50])` with `edx` unset; tail `jmp 00221870`.
  - `002240B0` exact (corrected row). Magic 0x10624DD3 with `sar 6` gives the signed /1000 compared with 0x96. The search keys are `jl`/`jge` (signed, stated). `0016D6A0` takes (`setne cl`, `rdx` = `rcx+0x60`). `test byte [rax+9],0x69` gates the slot `+0x48` call with (`rcx`, `rdx`, `r8d`).
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
