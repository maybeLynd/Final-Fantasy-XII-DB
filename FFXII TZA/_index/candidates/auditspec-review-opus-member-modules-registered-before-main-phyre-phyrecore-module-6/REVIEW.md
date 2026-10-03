# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PhyreCore module part 6 (opus-member-modules-registered-before-main-phyre-phyrecore-module-6)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-1118F` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-phyrecore-module-6/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 16 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide correction count in the README and in `rows.json` `method`, which is shared by the 10 PhyreCore records of 83b4566ab.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "260 stood, 34 rows were corrected in 40 clauses (18 inline sub-objects written as the qword they hold, 6 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)" with:

> 264 stood, 30 rows were corrected in 34 clauses (19 inline sub-objects written as the qword they hold, 7 signed compares written as above/below, 6 wrong arguments or offsets, 2 missed paths)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 30 functions, 136 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 30 rows, 136 anchors, mode `member`, family `Phyre PhyreCore module`. Skipped 0, missing 0. Rejected 10, each "not an entry-only frontier function of the page": `00224BF0`, `00225160`, `00227D40`, `0022A540`, `00314F20`, `0039D1D0`, `0059A770`, `005CD370`, `005CDB90` and `005FEF00`. Corrections 1 (`00224290`).
- Correction confirmed at the bytes: in `00224290` the tree descent uses `jl` at 002242F3 on the signed key; the row now says "less than `k` (signed)".
- Semantic pass: **16 of 30 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` and imports resolved:
  - `00224290` exact (corrected row). The /1000 test uses magic 0x10624DD3 with `sar 6` (signed) against 0x96. The search is `jl`/`jge`. `0016D6A0` takes (`setne cl`, `rcx+0x60`). The call needs both `test cl,0x68; jne` (none of 0x68) and `test cl,1; je` (bit 0x1 set) to fall through to slot `+0x48` (`rcx`, `rdx`, `r8d`).
  - `00224C30` exact: vtable 00907F90; tail `jmp 00221870`.
  - `0022C930` exact.
  - `00598180` and `005A05A0` exact: vtables 00D26BE0 / 00D27B80; `00809950(rcx, 8)` under `test dl,1`.
  - `00598360` exact: `shl rcx,2`, align 4; only `r8d` dwords are written.
  - `005AD040` exact: vtable 00D31168; bit 0x4 picks `0016D6A0(rcx, 0x50)` over `00584730(rcx)`.
  - `005C8BF0` exact. The early exit compares with the full dword. When `edx` = 0 the code jumps to the free gate with `p` = 0, so `p` and `edx` (both 0) are stored. `cmovb` gives the min for `005A5B40`. The free is gated `!= p`, bit 31 clear, non-null.
  - `005CD380` exact. The imports are `GetCurrentThreadId` (`008C21D8`), `WaitForSingleObject` (`008C20E0`, `edx` = -1), `GetLastError` (`008C20A8`), `FormatMessageA` (`008C2208`; args 0x1300, 0, err, 0x400, `[rsp+0x20]` = `&buf`, `[rsp+0x28]` = 0, `[rsp+0x30]` = 0) and `LocalFree` (`008C21F8`). The `lock xadd -1` runs on all three exits.
  - `005CD9C0` exact: guard `cmp [02CB6158],epoch; jg` (the same test as the usual `jle`, inverted), then `005CDA30()` stored to 02CB6150, with no `00808B90` call.
  - `005E3250` exact: `shl rcx,6`, align 4, four `movups` per element.
  - `005E3AE0` exact: `001C19A0(p, rdx, r8d)`; the tail qwords from `p + r8d*8` are zeroed.
  - `0060C6C0` exact: `005E3380`; free gated `!= p`, bit 31 clear, non-null.
  - `0060CC60` exact. `b` is selected by `cmp r9d,1; jbe` and `cmove`. `005FEF00` takes (`rcx`, `edx`, `b`, `min`). The free is gated by four tests (`!= p`, `!= rcx+8`, bit 31 clear, non-null). `p` is stored only when it is not `rcx+8`.
  - `0060E410` exact.
  - `00629560` exact: `setne al; add 2` gives 2 for `edx` = 1, else 3.
- Advisory, not a defect: `005C8BF0`, `0060C6C0` and `0060CC60` take an unsigned `min` (`cmovb`). With the second operand masked to 31 bits, it differs from a signed minimum only when `edx` has bit 31 set. OPUS may add "(unsigned)".
- Batch-wide sentence (shared by the 10 PhyreCore records of 83b4566ab, and the reason for this record's narrowing). The README's and `rows.json` `method`'s "260 stood, 34 rows were corrected in 40 clauses (18 + 6 + 6 + 2)" matches neither the records nor the verifier's own output:
  - The listed kinds sum to 32, not 40.
  - The 10 records' `rows.json` corrections hold 34 entries in 30 functions: modules 1..10 hold 4, 10, 3, 7, 7, 1, 1, 0, 0 and 1.
  - By kind, those entries are 19 "one dereference too many" inline allocator objects, 7 signed compares, 6 wrong arguments or offsets, and 2 missed paths.
  - `Tools/work/OPUS/cloud/verify_phyrecore_1003.json` agrees with the records: 294 functions, 264 OK, and 34 FIX entries in 30 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
