# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 3 (opus-member-modules-registered-before-main-phyre-phyrecore-module-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-F309D` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-3/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 18 rows read are exact at the bytes, and the record's three corrections are right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 27 functions, 129 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 27 rows, 129 anchors, mode `member`, family `Phyre PhyreCore module`. Skipped 0, missing 0. Rejected 13, each "not an entry-only frontier function of the page": `001EE7C0`, `001F2870`, `001F4120`, `002045E0`, `002104D0`, `002104E0`, `00210510`, `00210520`, `00210560`, `002105A0`, `002105B0`, `00210930` and `00210AF0`. Corrections 3, in 3 functions.
- Corrections, all 3 confirmed at the bytes and present in the rows:
  - `001F41A0`: `00809054` gets `rcx` = qword `[rcx+0xA8]` itself (= `b`+8, 001F41F2), and only `00809950` gets `b` (001F4225).
  - `001F5B80` and `001F8B30`: `this` is the inline allocator object (`lea rcx,[rsi+0x50]` / `[rdi+0x88]`), and the vtable is the qword at that address.
- Semantic pass: **18 of 27 rows**, spread over the package and including the three corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings, imports and division magics resolved:
  - `001EE410` exact. `d` is 0 unless both `a` and `[a+0x60]` are non-null. The assignment is skipped when `d+0x80 == &temp` (`rsp+0x70`). The `0060E410` args are `rdx` = `rsp+0x38` = floats `m+0/4/8` and `r8` = `rsp+0x28` = floats `m+0x18/0x1C/0x20`. `o` stays 0 when either lookup fails. The slot `+8` call takes (`[q+8]`, `rdx`).
  - `001EF4B0` exact.
  - `001F0A00` exact: `-w` and `-d` are formed by `xorps` with the sign mask at 01CEBDA0. The stack args are `[rsp+0x20]` = `d`, `+0x28` = `[rcx+0xC0]` and `+0x30` = `[rcx+0xC4]`. The 16 dwords are copied from the returned pointer; `001F05B0` returns `rcx` (`mov rax,rcx` at 001F0607), so the source is `m`.
  - `001F4060` exact: six self-links at `+8..+0x30`; `0067FFB0(rcx+0x38, 0x30, 8, 8, [rsp+0x20] = 009038E0 "PMapPair")`.
  - `001F41A0` exact (corrected row): `lea rdx,[rax+rax*2]; shl 4; add 8` = `count*0x30 + 8`.
  - `001F51E0` exact: magics 0x0E38E38E38E38E39 with `sar 1` (/0x24) and 0xA57EB50295FAD40B with `add`/`sar 9` (/0x318); `and ~7` and `and ~0xF`; tail `jmp 00212C80`.
  - `001F55F0` exact. The source-in-range test is `jb`/`jae` (unsigned). The full path computes `k` in 32 bits (`lea ebp,[rdx+rdx]`, then `test ebp`). The free size truncates to 32 bits (`mov eax,eax`). Capacity becomes new + `k`*0x24.
  - `001F5B80` exact (corrected row): `cmp [rcx+0x48],0; jbe` = zero test; `v` is read before the decrement.
  - `001F86F0` exact: the count is recomputed after each pair of calls (`jb`).
  - `001F8B30` exact (corrected row): qword keys with `jb`/`jae` (unsigned, stated).
  - `001FBBF0` exact: `w` = `[rsp+0xA0]` (fifth argument); each `j` sums `y*m[4+j] + x*m[j]` first, then `z*m[8+j]` and `w*m[12+j]`; the entry index is `movsxd` (signed) * 0x30.
  - `00204660` exact: both arms store vtable 009058C0 at the end.
  - `0020B150` exact: same set layout as `001997F0`; `0020C560(rcx, edx)`; stride 0x18; `b` = byte `[rsp+0x90]`, the `r8` home slot.
  - `0020B2E0` exact. The allocator string is 008F4120 "EASTL map". The two size compares are `ja` 0x270F and `cmovb` 0xF4240 (unsigned).
  - `0020D720` exact: `FreeLibrary` is at IAT slot `008C2128`; magic 0x2AAAAAAAAAAAAAAB with `sar 1` (/0xC).
  - `002105E0` exact: the sizes and constructors pair as stated, and the stores land in the order `+0`, `+8`, `+0x10`, `+0x20`, `+0x18`.
  - `00211480` and `00211600` exact: 2 x 0x80 + 0x28 = 0x128 bytes per element.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
