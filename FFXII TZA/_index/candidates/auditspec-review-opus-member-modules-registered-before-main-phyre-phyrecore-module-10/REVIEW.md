# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 10 (opus-member-modules-registered-before-main-phyre-phyrecore-module-10)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-7851F` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-10/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 20 functions, 73 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 20 rows, 73 anchors, mode `member`, family `Phyre PhyreCore module`; rejected 3 (`007A3D50`, `007A4150`, `008478A0`, each "not an entry-only frontier function of the page"), skipped 0, missing 0, corrections 1 (`007A3C10`).
- Correction confirmed at the bytes: in `007A3C10` both `00182F70` tail jumps take `ecx` = `w` >> 16 and `edx` = `w` AND 0xFFFF (`movzx edx,cx; shr ecx,0x10` at 007A3C91/007A3C94 and 007A3CB2/007A3CB5); the row now says `00182F70(w >> 16, w AND 0xFFFF)`.
- Semantic pass: **15 of 20 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `007A3A60` exact.
  - `007A3A80` exact.
  - `007A3AA0` exact: the store order `+0x18` (low byte of `0079E640`), `+0xC`, `+0x10` from dword `+0x2C` of qword `01F82D20`, and word `+0x19` = 0x101.
  - `007A3AF0` exact: `sub r8d,1; je` gives `e` = 1; `cmp eax,3` on `v` then `dec eax; cmp eax,1; jbe` makes `v` = 1 or 2 do nothing, and `v` = 0 or `v` >= 4 store 0.
  - `007A3B20` exact: the `sub` chain gives cases 1, 3, 4, 5 and 6, with case 6 storing `r8b` = 1. In case 4 the tail `jmp 0017D4B0` is taken only on a zero `al` from `00228480`.
  - `007A3BF0` exact: `cmove` picks 3 when dword `[rdx+4]` is 0.
  - `007A3C10` exact (corrected row): cases 0..4 with `e` - 3 compared with 1 for case 4; the case-1 tail `jmp 0079F9D0` takes rcx = `00796E20()`.
  - `007A3CE0` exact.
  - `007A3D10` exact: `dl` = 1, tail `jmp [r8+0x68]`.
  - `007A3D30` exact.
  - `007A3DC0` exact.
  - `007A3E00` exact: `cmp al,cl; cmovne ebp,ecx` makes the flag byte `[rcx+0x18]` on both arms. `GetSystemMetrics` is the import at IAT slot `008C29B0`. The rectangle differences are `[r+8]-[r]` and `[r+0xC]-[r+4]`, combined by `shl edi,0x10; or edi,eax`, and the tail `jmp [rax+0x40]` runs under the `+0xC` test.
  - `007A3EE0` exact: `005CDAA0(2, …)` and `0079EC80()` run only on a zero `al` from `0079B0B0`; the slot `+0x60` call takes `dl` = 1; the tail is `jmp [rax+0x48]` with `dl` = 1.
  - `007A3F80` exact.
  - `007A40B0` exact: `sub edx,1; je` gives 4 for `edx` = 1, and `cmp edx,1` after it gives 2 for `edx` = 2. The `+0x18` store happens only when `al` is zero (`jne 007A40F8`). The `+0x1A` arm calls `007A0FA0(cl=1)`.
- Signed versus unsigned: the only range compare in the sample (`007A3AF0`/`007A3C10`, `dec; cmp 1; jbe`) is unsigned and is worded as a set ("neither 1, 2 nor 3"), which is correct for every `v`.
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths. The 6 are `0019B200`, `0019B480` x2, `001F41A0`, `007A3C10` and `00633880`; the 2 missed paths are `001967D0`'s byte copy and `001B26F0`.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions. Every FIX entry equals a `rows.json` correction, each `new` text is in its row, and each `old` text is gone.
  - The commit subject's "40+6 clauses" reads the same way; the PhyreCore part is 34.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
