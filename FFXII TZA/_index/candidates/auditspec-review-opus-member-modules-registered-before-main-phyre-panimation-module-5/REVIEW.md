# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PAnimation module part 5 (opus-member-modules-registered-before-main-phyre-panimation-module-5)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-94C54` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-panimation-module-5/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 16 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 35 functions, 167 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 35 rows, 167 anchors, mode `member`, family `Phyre PAnimation module`. Rejected 0, missing 0, corrections 1 (`005C6BF0`). Skipped 3, each "too large for one precise sentence": `005C8130`, `005C8900` and `005CA460`.
- Correction confirmed at the bytes: `005C6BF0` leaves `rdx` unchanged before `call 005C3480` at 005C6C10. The row now writes `005C3480(qword [rcx+0x20], rdx)`.
- Semantic pass: **16 of 35 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `005C6980` exact. The 3 bound is `jb` (unsigned). The 1 return is `lea eax,[r8+1]`. `e` = `[rcx+0x30] + (edx << 7)`. The slot store matches `[rcx+0x48]` with `[e+0x68]` (`[rcx+0x10]` with `rcx` = `e+0x58`). Both index bounds are `jae`. It ends with `005C03D0(rcx)` and the `+0x80` copy.
  - `005C6A90` exact. The prologue matches `005C6770`, and so does the list search (inline storage when the count is at most 1). After `005C5400` the code picks `x` by `comiss [rcx+0xC],0; jbe`, stores 0 / 0x49742400 / 0, makes the third slot `+0x20` call, then stores `+0x78` = `rcx+0x38` and `+0x54` = `x - v`.
  - `005C6BF0` exact (corrected row): tail `005C6CC0(rcx, 0, p)` when `005C7130` returns 0.
  - `005C6C60` exact: `mov rdx,r8` before `005C3480`; tail `jmp 005C6CC0` with (`rcx`, `edx`, `p`).
  - `005C6ED0` exact: the header stores, then `memcpy(r8+0x14, [rcx+0x20], n*4)`, returning `((n*4 + 0x13) AND 0xFFFFFFF0) + 0x10`.
  - `005C7130` exact. The zero-count arm calls `005C8900(rcx, 0, 1)` and falls back to `n` = 1. The 1.0 store is gated by `test …,0x7fffffff; jbe`. The unrolled zeroing from index 1 re-tests each index against the masked dword `+0x60`. The first-element slot store requires three tests: non-null, equal to `+0x68`, and a non-zero masked `+0x50`.
  - `005C86C0` exact: `005AA840(d, s)`, the qword `+0x38` copy and the 16-byte `+0x48` copy are skipped when `d == s`; the tail is `jmp 005C9390` with `n - 1`.
  - `005C8850` exact. `0060C340(rcx, dword 02CACF18)` is called first. `n` = `edx*r8d` (32-bit `imul`). The allocation is `0017D260(n*2, 2)` (`lea edx,[rax+2]` with `rax` = 0 on this path). The `+0x20` copy and the `+0x28` store also run when `n` is unchanged.
  - `005C9000` exact: `005AD640` and `005B8050`.
  - `005C9120` exact: the per-element vtable stores at `+0x10`, `+0x38` and `+0x58` (`[rax-0x28]`, `[rax]` and `[rax+0x20]` with `rax` = elem+0x38), over the old masked count.
  - `005C9390` exact: `005A5CC0(p, old, k)` and `005BEDC0(p + 0x58k, edx - k)`. The qword `[rcx]` = 0 store also runs on the unchanged-count path.
  - `005C9590` exact. The 7 return uses `cmp 1; jae` on the masked count. The `+0x88` store runs only for a non-null `rdx`. The first list pointer is chosen out of line, inline or as 0. A changed null `rdx` still zeroes `[e]`. The 0x11, 0x13 and 3 exits follow, and the tail returns `005C03D0(rcx)` for a non-null `rdx`.
  - `005C98B0` exact.
  - `005CA0A0` exact: `xmm2` goes to `[e+0xC]` before the first slot `+0x20` call and to `[e+0x50]` before the second; `+0x54 += v1 - v2`.
  - `005CA420` exact.
  - `005CB620` exact: the first check is slot `+8` (`rdx`, `rcx`); the optional check is `o`'s slot `+0x18` (`o`, `rdx`, `rcx`); the final call is slot `+0x18` (`rdx`, `rcx`, `r8`), then `al` = 1.
- Advisory, not a defect: in `005C9590` the phrase "while qword `[rcx+0x20]` is non-null" describes a per-element test (`cmp [rbx+0x20],0; je` to the next element). That qword was just set to `rdx` and does not change in the loop, so it reads the same as "when `rdx` is non-null". OPUS may write "when" in a later pass.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
