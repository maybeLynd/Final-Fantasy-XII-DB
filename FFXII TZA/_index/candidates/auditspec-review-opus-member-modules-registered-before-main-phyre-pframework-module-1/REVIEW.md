# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PFramework module (opus-member-modules-registered-before-main-phyre-pframework-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-ECBA1` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-pframework-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 31 functions, 137 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 31 rows, 137 anchors, mode `member`, family `Phyre PFramework module`. Rejected 0, missing 0. Corrections 2, in 2 functions: `00799A80` and `00799DD0`.
  - Skipped 8, each "too large for one precise sentence": `0079D730`, `007A05D0`, `007A10A0`, `007A15A0`, `007A1790`, `007A1A50`, `007A2140` and `008744F0`.
- Corrections, both confirmed at the bytes and present in the rows:
  - `00799A80`: `jle` at 00799AF3 skips when `d` <= dword 01F40188 (signed); the row now says "greater than … (signed)".
  - `00799DD0`: `cmp r8d,0x1c; jge` at 00799DDD; the row now says "less than 0x1C (signed)".
- Semantic pass: **16 of 31 rows**, spread over the package and including both corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with imports and both jump tables resolved:
  - `007934F0` exact. The vtable is 01CB23F8. Slot `+0x40`, then slot `+0x10`, each re-read from `[d+8]`. Then `00584730(d)`, `00809054(rcx+0x30, 0x48, 6, 0016D6A0)` (`lea r8d,[rdx-0x42]`) and the final vtable 01CB23C0.
  - `00793F10` exact: vtable 01CB24A8, the null-tested `[rcx+0x28]` release, zeroing of `+0x28`, `+0x30` and `+0x40`, `00793410(rcx)`, then `00809950(rcx, 0x48)`.
  - `00794080`, `00794110` (delete size 0x338), `00794200` and `007942E0` exact. The last two have identical bodies: `00809054(rcx+0xB0, 0x48, 4, 0016D6A0)` and delete size 0x458.
  - `00796180` exact: the qword store of 0x1E0 at `+0x30` writes 0 into dword `+0x34`; `al` = 1 also when `rcx` is null.
  - `00799A80` exact (corrected row). `_Xtime_get_ticks` (`008C2578`) is divided by 10,000,000 through magic 0xD6BF94D5E57A42BD with `add` and `sar 0x17`. The first dword of `_localtime64` (`008C3050`) is `v`. The minute wrap is `jge` then `+0x3C`.
  - `00799DD0` exact (corrected row): the slot pointer is `rcx + 0x231 + movsxd(r8d - 0x1C)`, followed by the tail link.
  - `00799F40` exact. The first range is `lea eax,[r8-0xb]; cmp 0x10; ja`. The second is `lea eax,[r8-1]; cmp 9; ja`, dispatched through the table at 0079A050. That table's ten entries load 0x414, 0x420, 0x42C, 0x418, 0x424, 0x430, 0x41C, 0x428, 0x434 and 0x438 for `r8d` = 1..10, in the row's order.
  - `0079A5F0` exact. The table at 0079A68C sends `k` = 1, 2, 4 and 5 to the flag entry 0079A61D, `k` = 3 and 6 to 0079A620, and `k` = 7..10 to 0079A637. The divisors are 008C5B40 = 255.0 and 00D6B968 = 1023.0. The halving is `cdq; sub; sar 1` (signed). The final test compares `[rcx+0x24]` with `|v|` (`andps` with mask 01CEBD80) using `comiss; jbe`.
  - `0079B850` exact. `h` is the caller's `r9` home slot (`rax+0x20`, read back at `[rsp+0x78]`). The copy of the 24 bytes at `r9` to `rax-0x20` is not read afterwards. The two calls take (`rdx`, x0, `h - y1`, `x1 - x0`, `[rsp+0x20]` = `y1 - y0`, `[rsp+0x28]` = -1) and (`rdx`, 2, running sum, dword `[e]`).
  - `0079BFA0` exact: the fifth argument is `[rsp+0x60]` and the sixth `[rsp+0x68]`.
  - `0079D630` (`jl`, signed) and `0079D670` (`ja`, unsigned) exact.
  - `007A0340` exact: stack pair `[rsp+0x30]` = 0, `[rsp+0x34]` = `n`; `007A3FC0(rcx+0x48, dword [[01F82D20]+8])`; tail `jmp [g+0xD18]` with `g`.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414), checked once: "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares worded above/below, one operand grouping)" matches the records.
  - The 8 `rows.json` hold 31 + 11 + 1 + 8 + 33 + 32 + 29 + 9 = 154 rows.
  - The corrections are `00799A80`, `00799DD0` and `0069ED80` (signed) and `006A0B60` (grouping): 4 entries in 4 functions.
  - `Tools/work/OPUS/cloud/verify_pphys_small_1003.json` shows 150 OK and 4 FIX.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
