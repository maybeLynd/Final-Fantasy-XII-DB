# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 9 (opus-member-modules-registered-before-main-phyre-phyrecore-module-9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-D7CB3` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-9/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 30 functions, 121 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 30 rows, 121 anchors, mode `member`, family `Phyre PhyreCore module`. Missing 0, corrections none.
  - Rejected 7, each "not an entry-only frontier function of the page": `006BAAD0`, `006CBA20`, `006CBB20`, `006CE570`, `006CE650`, `006DA6C0` and `007A39C0`.
  - Skipped 3, each "too large for one precise sentence": `006BAB40`, `006CB2A0` and `006D9FC0`.
- Semantic pass: **15 of 30 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with imports resolved:
  - `006BADF0` exact. `b` is chosen from the pre-increment dword `+0x78`. The loop bound is dword `+0x10`, tested `jbe`/`jb` (unsigned). Each entry stores the previous end in `+8`, then `b + 8*((+0x8C * (i+1)) / +0x10)` (32-bit `imul`, unsigned `div`) in `+0x10`. The final call is `005CD650(rcx+0x38+(k<<4), dword +0x10, 0)`.
  - `006BB000` exact: `006BB0A0(rcx, dword +0x78 - 2)`; the 0xE test is `cmp ecx,[rcx+0x24]; jb` (unsigned "at least"); the store index is the old dword `+0x88`.
  - `006BB0A0` exact: `sub eax,edx; cmp 2; ja` (unsigned, stated); the call count re-reads dword `+0x10`.
  - `006C88B0` exact: slot `+0x168` of `[[rcx+0x848]+0x110]` with (`o`, 1, `rcx+0x20900`); `00629680(rcx+0x208, byte +0x20920)`; the copy and zero of dword `+0x208` run on both paths.
  - `006CB690` exact: vtable 00D86B80, delete size 0x88.
  - `006CB770` exact.
  - `006CC980` exact: vtable 00D89B00. The qword is zeroed even when its re-read is null (006CC9D4 is the target of that test). The tail is `jmp 00800140`.
  - `006CE6C0` exact: no null test before `00584730`.
  - `006DA470` exact. The mode uses `js` / `cmp 1; jle` / `cmp 4; jg` (signed). The sixth argument is at `[rsp+0x68]` and the fifth at `[rsp+0x60]`. The refill loop is `ja 0x2AA` / `jbe 0x4000` (unsigned). The word copy goes to `rcx + 2*(dword+8 + 8)`. The add-back loop runs from the old count to the new total. The 0x30-stride copy goes to `rcx+0x8020`. The new word count is stored last.
  - `006DA6D0` exact.
  - `006DA790` exact: `t = dword+8 + 2*edx + (edx - 6)`; `ja 0x4000`; the even and odd triple orders follow `test r9b,1`, with positions `ebx`, `r10-1` and `r10`.
  - `0079B0B0` exact: `GetForegroundWindow` is at IAT slot `008C2800`.
  - `0079F9D0`, `007A39F0` (vtable 01CB3EF8, size 0x20) and `007A3A30` exact.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
