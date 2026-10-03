# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 7 (opus-member-modules-registered-before-main-phyre-phyrecore-module-7)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-AD5B4` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-7/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 36 functions, 172 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 36 rows, 172 anchors, mode `member`, family `Phyre PhyreCore module`. Missing 0. Corrections 1 (`00633880`).
  - Rejected 1: `00639A40`, "not an entry-only frontier function of the page".
  - Skipped 3, each "too large for one precise sentence": `0062E1C0`, `0062E5A0` and `0062FC90`.
- Correction confirmed at the bytes: in `00633880` the fourth argument of `0063DCA0` is `rcx`'s element pointer (`r9` from 006338C1 / 006338C9), and the row now says `0063DCA0(rcx, x, n, e, c)` with `e` = `rcx`'s elements.
- Semantic pass: **15 of 36 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `0062A9E0` exact: every stack argument was mapped through `push rbx` + `sub 0x20`. `[rsp+0x50]` is the 5th, `+0x58/+0x60/+0x68` the 6th to 8th, `+0x70` the 9th, `+0x78` the 10th, and `+0x90/+0x98/+0xA0` the 13th to 15th. The destination of each matches the row.
  - `0062DDE0` exact. All twelve inputs are loaded before the first store at 0062DE50. The three recomputed values are `[+0x28/+0x2C/+0x30] + [+0x18/+0x1C/+0x20] * (-s)`, with `-s` formed by XOR with the 01CEBDA0 mask. In the copy-back, `+0x14` and `+0x24` are briefly written with the zero lanes, then rewritten from `[+0x38]` / `[+0x3C]`, so the final state is as the row states.
  - `0062F0A0` exact.
  - `00630780`, `006308C0` and `00630AA0` exact. The record fields are dword `+4` from the class's dword, qword `+8` = `rcx`+0x30 (with `cmove` 0) or `rcx`, and byte `+0x10` = 1. The walk starts at the link qword at `T+0x80`, passes `link - 8`, follows `[link]`, and stops at the sentinel, null or `link - 8 == 0`. Parents come from `[T+0x78]`.
  - `00630C80`, `00630E60` and `00631040` exact: the reverse walk starts at `T+0x88` and follows `[link+8]` (`[rbx+0x10]`), with byte `+0x10` = 0 and qword `+8` = `rcx`+8 (or 0), `rcx`, or `rcx`+0x10 (or 0).
  - `00633880` exact (corrected row): both element selections use `cmp 1; jbe` and `cmove`; `[rsp+0x20]` = `c`.
  - `00634050` exact: vtable 00D580B0. The slot `+0x48` call on `[rcx+0x18]` runs only when `[rcx+8] != rcx+8`. Then `006B6700(rcx+0x38)`, the `[rcx+0x28]` bit-0 test before `00584730([rcx+0x20])`, and the delete flags with size 0x68.
  - `00634310` exact.
  - `00637800` exact: every store into 01F2E410..01F2E458 matches the row (the 1s at `+0x38/+0x3C`, the self-links at `+8/+0x10/+0x18`, 00D58AA8 "PChar" at `+0x30`, vtable 00D58A68, and the zeros); exit routine 008AFE00.
  - `00639650` exact: `cmp edi,1; jbe` keeps `p` = `rcx+8` for one element.
  - `0063A770` exact: tail `jmp [rax+0x50]`.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
