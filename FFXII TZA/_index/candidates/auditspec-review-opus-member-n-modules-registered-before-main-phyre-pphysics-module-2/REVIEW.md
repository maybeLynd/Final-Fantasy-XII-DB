# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPhysics module part 2 (opus-member-n-modules-registered-before-main-phyre-pphysics-module-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-N-MODULES-REGISTERED-BEFORE-MA-FFD57` · Package: `_index/candidates/opus-member-n-modules-registered-before-main-phyre-pphysics-module-2/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

15 of the 16 rows read are exact at the bytes, and the record's one correction (`0069ED80`, signed compare) is right and applied. One clause in that same row states its copy guard wrongly.

**Narrowing (exact wording).** In the `0069ED80` row, replace "copies the `n` 0x30-byte elements of qword `[rcx+0x30]` into it (when `p` is non-null)" with:

> copies the `n` 0x30-byte elements of qword `[rcx+0x30]` into it (each destination element address is tested for null, so a null `p` skips only element 0)

The loop at 0069EDF7..0069EE24 is not gated on `p`. It walks `rcx` = `p` + 0x30·`i` and tests each destination address (`test rcx,rcx; je`). With `p` = 0 only element 0 is passed over, and elements 1.. would be written to 0x30, 0x60 and so on. The row's other per-element guard ("into element `n` (when its address is non-null)") is already worded this way.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 32 functions, 158 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 32 rows, 158 anchors, mode `member`, family `Phyre PPhysics module`. Rejected 0, missing 0, corrections 1 (`0069ED80`). Skipped 6, each "too large for one precise sentence": `00692080`, `00692290`, `006928B0`, `00692AC0`, `00698720` and `0069E970`.
- Correction confirmed at the bytes: `cmp ecx,edi; jge` at 0069EDBA skips the growth when `c >= m` (signed). The row now says "`c` is less than `m` … (signed)".
- Semantic pass: **16 of 32 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `00691FC0` and `00692800` exact: each listed byte, dword and qword copy matches, and no other offset is copied.
  - `00692660` exact. The first 0x30 bytes are one `movups`, one `movsd` and three qword moves. `00693C40(n, [rdx+0x38])` follows, with its free gated `!= p`, non-null and bit 31 clear. The tail 0x58 bytes are five `movups` and one `movsd`.
  - `00693160`, `006935C0` and `006937B0` exact: vtable 00D79790, delete sizes 0x80 / 0x78 / 0x68.
  - `006932A0`, `006933E0` and `006934C0` exact (identical bodies): vtable 00D79998; slot `+0` of `[rcx+0x80]` with (obj, 1); zeroing of `+0x80` and `+0x68`; vtable 00D79790; size 0x88.
  - `006936D0` exact: vtable 00D79A88; slot `+0` with (`o`, 0); `00584730` on the re-read qword, then zeroed.
  - `00693850` and `00693920` exact: vtable 00D79830, the `+0x78` object, size 0x80.
  - `00693CD0` (`lea [rax+rax*8]; shl 2` = 0x24, align 4) and `00693E30` (0x30, align 8) exact.
  - `0069ED50` exact: `0069EFA0(rcx, rdx, r8, &v, [rsp+0x20] = r9d)`; `cmove ecx,[rsp+0x30]` returns `v` on 0, else -1.
  - `0069ED80`: the growth test, `m` (`lea edi,[rax+rax]` or 1), `0085E680(m*0x30, 0x10)`, the `0085E710` free gated on non-null and byte `+0x38`, and the stores of `p`, 1 and `m` are exact. The final element copy, the `inc` and the `r8d` store into element `n` are also exact. Only the copy-guard parenthetical is narrowed above.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
