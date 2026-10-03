# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 8 (opus-member-modules-registered-before-main-phyre-phyrecore-module-8)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-74C8A` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-8/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 32 functions, 141 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 32 rows, 141 anchors, mode `member`, family `Phyre PhyreCore module`. Missing 0, corrections none.
  - Rejected 7, each "not an entry-only frontier function of the page": `0063B9E0`, `0063BB00`, `0063BC70`, `0063D300`, `006AA230`, `006ADF90` and `006AFDC0`.
  - Skipped 1: `006AA3A0`, "too large for one precise sentence" (608 B).
- Semantic pass: **15 of 32 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `0063BAF0` exact.
  - `0063C020` exact: `neg ecx; movsxd`, then `cmovne` keeps 0 for a null `a`.
  - `0063D010` exact: both null tests, the tail `jmp 00684080` with (`rdx`, `a + offset`, `rcx`), and the other arm `0080F420(rdx, 1)` plus tail `jmp 00810620`.
  - `0063D9C0` exact. `b` is selected by `cmp 1; jbe` and `cmove`. The calls are `006396C0(rcx, edx, b, cmovb-min)` and `0063DCA0(rcx, p, edx, b, [rsp+0x20] = count)`.
  - `006750C0` exact. The count adjustment `neg (bit0); inc` adds 1 only when bit 0x1 is clear. The `sets dl` index chooses `x+0x10` on a negative compare, else `x+8`. An equal key returns `x+8`. At a link equal to `rcx`, the code stores `slot base + bit0` to `n+0x18` and `n+8` into `[base + dl*8]`, then returns 0.
  - `00675460` exact. The second gate is `[rcx+0x18] - (byte AND 1) != rcx+8`. The six self-stores of 01F2EA70 sit under guard 02D3EC9C with exit routine 008B1C00. Then come `0067FE20(01F2EA70, rcx+8)` and the unlock; the final `[rcx+0x30]` release runs on every path.
  - `00676450` exact. The 0x15 return is taken after the `r+0x48` store and before any lock. The unlock (`005CD820`) runs before both the 0x12 return and the next record. The record walk uses `inc ebp; cmp; jae`.
  - `00677BA0` exact: `lea eax,[rdi+0x15]` with `rdi` = 0; `cmove ebx,ebp` keeps 0x12.
  - `00684300` exact: `0080FA50(rcx, 0xFFF0B9D8, 00D70154 "Vector")`, `00810F60(rcx, -2)`, then one `movups`.
  - `006AA1B0` exact.
  - `006AB540` exact: the first chain walk runs from `t` and must meet 02E4E720, else the result is -1. The per-node walk runs from `[b+0x10]` and must meet `t`. The count is `esi`.
  - `006ABFA0` exact. The descent is `cmp [node+0x18],v; jbe` then `jae` (unsigned), and `shr eax,0x1f` picks child `+0` for above and `+8` for below. An equal key skips through `test r8; jne 006AC094`. The parent store adds `d`'s bit 0x1, and `0067F700(01F2EB40, d)` follows.
  - `006AF6B0` exact: `006AE270`; free gated `!= p`, bit 31 clear, non-null.
  - `006B3610` exact: the block at `rsp_entry - 0x58` holds the four rows as stated, with the 1.0 from 01CEBBA8 last; `00684130(rcx, &block)`.
  - `006B68D0` exact: vtable 00D80970, the unlink (`[next+8] = prev`, `[prev] = next`) and self-link, vtable 00D31168, delete size 0x60.
- Advisory, not a defect: `0063D9C0` and `006AF6B0` take an unsigned `min` (`cmovb`), as noted in the part 6 record. OPUS may add "(unsigned)".
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
