# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPhysics module part 1 (opus-member-n-modules-registered-before-main-phyre-pphysics-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-N-MODULES-REGISTERED-BEFORE-MA-EA845` · Package: `_index/candidates/opus-member-n-modules-registered-before-main-phyre-pphysics-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 33 functions, 157 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 33 rows, 157 anchors, mode `member`, family `Phyre PPhysics module`. Rejected 0, missing 0, corrections none. Skipped 7, each "too large for one precise sentence": `00631290`, `0063CD20`, `00667C80`, `00684860`, `00690BF0`, `00691570` and `00691C00`.
- Semantic pass: **15 of 33 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `0063A960` exact: block at `rsp+0x20` = (0, `r8`, `rdx`, byte 0).
  - `00670FF0` exact: the 8 and 0xC byte tests; the widening loop (`movzx eax,word`, unsigned `jbe`/`jb` on dword `[rcx]`) runs only after `00672560(rdx, dword [rcx])` returns 0.
  - `00672560` exact.
  - `00684A10` exact: `00684860(rcx+0x28, edx+0x28)`; `cmove` maps a zero count to 1; the null test on `p+0x10` is present as stated.
  - `00685A80` exact: tail `jmp [rax+0x40]` with `o` = `[rcx+8] - 8` (`cmove` 0 when null).
  - `0068A300` exact: slot `+0` gets (`o`, 0); `00584730` is called on the re-read `[rcx+0x80]`.
  - `0068EA90` exact: `005CDAA0(2, 00D7A4F0)` (the string begins "WARN"); returns 0x17.
  - `0068EC80` exact: vtable 00D79790, delete size 0x88.
  - `0068F1C0` exact.
  - `00690E20` exact.
  - `00690FC0` exact. The qword stores of 0x3F800000 at `+0x48`, `+0x5C`, `+0x70`, `+0x88`, `+0x9C` and `+0xB0`, plus the dword stores at `+0x84` and `+0xC4`, put 1.0 on the diagonals (+0, +0x14, +0x28, +0x3C from each matrix base) and 0 elsewhere. The six constant dwords and the final `00681640(rcx+0x118)` match.
  - `006911B0` exact: replaying the overlapping stores gives the row's twelve final dwords at `+0x20..+0x4C` (the late stores 1.0 to `+0x2C`, 0 to `+0x3C` and 0 to `+0x4C` included); vtable 00D799C0; dword `+0x60` = 2.
  - `006912F0` exact: replaying the stores leaves 1.0 only at `+0xC`, `+0x14` and `+0x20` in `+0..+0x40`, and only at `+0x54` in `+0x48..+0x60`; `+0x44` is never written. The remaining stores and `00681640(rcx+0x100)` match.
  - `00691490` exact: all constant stores, the `rep stosw` of 15 words of 0xFFFF at `+0x78`, then `and word [+0x7A],0xFFFD` and word `+0x7C` = 3.
  - `00691B30` exact: `006A4870(w, rcx)`; the walk reads next first, stores `[d+0xC8]` = 0, and unlinks from `[rcx+8]` (link `+0`) and, when `w` is non-null, from `[w+0x58]` (link `+0xD8`).
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
