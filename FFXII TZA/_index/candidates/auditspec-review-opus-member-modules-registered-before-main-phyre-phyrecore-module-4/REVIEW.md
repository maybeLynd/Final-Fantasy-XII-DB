# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 4 (opus-member-modules-registered-before-main-phyre-phyrecore-module-4)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-07F84` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-4/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 17 rows read are exact at the bytes, and all 7 of the record's corrections are right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 29 functions, 145 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 29 rows, 145 anchors, mode `member`, family `Phyre PhyreCore module`. Missing 0. Corrections 7, in 7 functions.
  - Rejected 8, each "not an entry-only frontier function of the page": `002125A0`, `00212710`, `00212760`, `002164D0`, `00216540`, `00217FD0`, `00219400` and `0021A9F0`.
  - Skipped 3, each "too large for one precise sentence": `00211BC0`, `002196A0` and `0021AC90`.
- Corrections, all 7 confirmed at the bytes and present in the rows. Each concerns the inline allocator object passed as `this`, whose vtable is the qword at that address:
  - `002118E0`: `rcx+0x18`.
  - `00211AC0`: `rcx+0x68` (`lea rcx,[rsi+0x10]` with `rsi` = `rcx`+0x58).
  - `00218100`: `rcx+0x18`.
  - `002187D0`, `002199C0` and `0021AF80`: `rcx+0x50`.
  - `0021A340`: `d+0x88` (`lea rcx,[rbx+0x28]` with `rbx` = `d`+0x60).
- Semantic pass: **17 of 29 rows**, spread over the package and including all seven corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings, imports and division magics resolved:
  - `002116B0` exact: same set layout as `001997F0`; `002123E0(rcx, edx)`; stride 0x128; `b` = byte `[rsp+0x90]`, the entry `r8` home slot.
  - `002118E0` exact (corrected row): magic 0x3759F22983759F23 with `sar 6` (signed /0x128), then `imul 0x128`.
  - `00211AC0` exact (corrected row): vtable 00906C80, `005CD330(rcx+8, rsp+0x40)`, then the five calls in order and the list walk with next read before each call.
  - `00212130` exact: `005CC8C0(&p, 002125F0)`; dword `p+0x18` = 0, `p+8` = 0x10000; name 00906C88 "AudioFileLoadManager".
  - `002133D0` exact: `cmp ebp,0x1e0; cmovg` (signed min, stated). The `memcpy` source is `r8 + movsxd(d)*0x30` with length `k*0x30`. The three slot calls take (rdx), (rdx, 0) and (rdx, 2, q, k).
  - `002165B0` exact. The escape-byte update runs for every `c`, after the in-string byte may have changed. `sputn` (`008C2668`) is called with count `dword 01FD4060 - edx` and clears `cl`. `sputc` (`008C2660`) is called only while `cl` is set.
  - `00218100` exact (corrected row): element loop `jae`/`jb` with stride 0x58; magic 0x2E8BA2E8BA2E8BA3 with `sar 4` (/0x58).
  - `002187D0` exact (corrected row): the tail is `002226A0(v)` for non-null `v`, else 0.
  - `00218F40` exact: the backward walk (`rdi` = `s`+0x20), `002181A0(d+8, s+8)`, and all fourteen field copies, including the unaligned dword at `+0x45`; it returns the destination start.
  - `002190B0` exact: the same field list from the single source.
  - `00219240` exact: vtable 00907B48 is stored after `00217F10(d, s)`, then the nine field copies.
  - `002199C0` exact (corrected row): tail `00222CB0(v)`.
  - `00219B20` exact. `b` is byte `[rsp+0x50]` (entry `+8`, the `rcx` home slot, two pushes + 0x38), read at 00219B4B before the first write at 00219B70. The final store is `sete` on byte `+0x90`.
  - `0021A340` exact (corrected row). The tree empty-out uses `001AF2B0(d+0x58, [node])` with next at `+8`, and frees each node through `d+0x88` (size 0x30). The reset and the rebuild through `001AE6B0(d+0x58, [s+0x70], d+0x60)` follow. The leftmost and rightmost walks use `+0` and `+8`.
  - `0021A5A0` exact: `001AE4B0(d+0x58, s+0x58)`.
  - `0021A750` exact: vtable 00907D80, `0021A920(d+0x58, s+0x58)`.
  - `0021AF80` exact (corrected row): tail `002235F0(v)`.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
