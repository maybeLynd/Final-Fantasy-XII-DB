# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PAnimation module part 4 (opus-member-modules-registered-before-main-phyre-panimation-module-4)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-2D39E` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-panimation-module-4/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 16 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 33 functions, 122 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 33 rows, 122 anchors, mode `member`, family `Phyre PAnimation module`; rejected 0, skipped 0, missing 0, corrections 1 (`005C68B0`).
- Correction confirmed at the bytes: `005C68B0` leaves `rdx` unchanged before `call 005C3480` at 005C68D0. The search string is therefore passed through, and the row now writes `005C3480(qword [rcx+0x20], rdx)`.
- Semantic pass: **16 of 33 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `005C37B0` exact. The start index loop runs `comiss xmm1,[key]; jbe` until the key is not below `xmm1`. The wrap arm is taken when `comiss xmm1,xmm2` is above. The second loop stops on `comiss xmm2,[key]; jb`. The fifth argument is `[rsp+0x70]`.
  - `005C39A0`, `005C3A10`, `005C4D10`, `005C5140`, `005C5180`, `005C51B0`, `005C51D0` and `005C5320` exact.
  - `005C3AD0` exact: the bound is `jae` (unsigned "below"), stride `shl 7`, and the tail is `jmp [rax+0x20]` with `rcx` = `e+0x10`.
  - `005C5400` exact. A null `k` or a zero count (`cmp 1; jae`) returns 7. The first channel stores the first and last floats. Later channels use `minss`/`maxss` into `[rdx]`/`[r8]`. `n` = 0 with `comiss lo,hi; ja` returns 7. The final clamp is skipped when `comiss hi,lo; jb`.
  - `005C5B20` and `005C5BA0` exact: the masked-count test (`test …,0x7fffffff; jbe`) and the bound `jae`, with tail `jmp 005C5B40`.
  - `005C61A0` exact. The four-way unrolled body indexes floats `4k..4k+3` through `r15/rsi/r14 + r10` and the indices `[r10-8]`, `[r10-4]`, `[r10]` and `[r10+4]`. The `jp`-then-`je` pair counts unordered as not equal. The tail loop covers the remainder.
  - `005C6770` exact. The order of stores and calls matches the row (`-[02CACF14]` and 1.0, then `v1`, the old `[rcx+0xC]` into `+0x50`, then `v2`). The 0x11 return is `lea eax,[r9+0x11]` with `r9` = 0. The membership search picks inline or out-of-line storage by `cmp 1; jbe`. `cmovns r10,rsi` with a null `r10` gives 0x13. Both stack floats start at 0 for `005C5400`.
  - `005C68B0` exact (corrected row).
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
