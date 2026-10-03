# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPostProcessing module part 4 (opus-member-es-registered-before-main-phyre-ppostprocessing-module-4)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ES-REGISTERED-BEFORE-MAIN-PHYR-08FA0` · Package: `_index/candidates/opus-member-es-registered-before-main-phyre-ppostprocessing-module-4/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 21 functions, 101 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 21 rows, 101 anchors, mode `member`, family `Phyre PPostProcessing module`. Rejected 0, missing 0, corrections none. Skipped 16, each "too large for one precise sentence": `00657870`, `00657A20`, `00657BC0`, `00657D60`, `006580D0`, `00658BA0`, `00659080`, `00659EC0`, `0065BA00`, `0065C080`, `0065C330`, `0065C4D0`, `0065C760`, `0065CD60`, `0065D310` and `0065D720`.
- Semantic pass: **15 of 21 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table). Stack arguments were checked against the frame (entry `rsp+0x28` / `+0x30` = fifth / sixth):
  - `00657830` exact: the same shape as `006576D0`, with `0065CA10` receiving `rcx`, `edx` and `r8d` unchanged.
  - `00657F70` exact. Block `a` = `[rcx+0x1B8]` with 0x4D / 02D34718 / `[rcx+0x140]`; 5 when byte `[a+2]` is not 0x4D; the three bound tests are `jbe` / `jae` (unsigned). `001B81B0(t, [rcx+0x198], &b)` with `b` = (0x42, 02D34718, `[rcx+0x128]`); 02D36E60 then `[x+0x80]`; `006007B0(x, [[rcx+0x58]], t, [+0x6C] >> 2, [+0x70] >> 2, 1)`.
  - `0065B270` exact. Slot `+8` gets (`[r9+0x28]`, `[r9+0x2C]`) or two zeros; 5 on a null `r9`; the slot `+0x10` chain matches; 0x15; `00658470(rcx, rdx, r8, r9, fifth = [rsp+0x60])`.
  - `0065B340` exact: `006587F0(rcx, rdx, r8, r9)`.
  - `0065B4C0` exact: `00658BA0(rcx, rdx, [rdx+0xA8], r9, [rsp+0x20] = fifth, [rsp+0x28] = r8)`.
  - `0065B590` exact: `0065A640(rcx, rdx, r8, r9, byte 1)`.
  - `0065B650` exact. `00652940(rcx, rdx, r9)` comes first, then `00659080(rcx, rdx, r8, r9, s, 1)` with `s` = `[m]` when byte `[m+8]` is 0, else 0.
  - `0065B820` exact. The 5 return is `lea eax,[rdi+5]` with `rdi` = the null `r9`. The final call is `00659C20(rcx, rdx, r8, [rdx+0xA8], [rsp+0x20] = r9, [rsp+0x28] = [rsp+0x60] = fifth)`.
  - `0065B920` exact. The sixth argument (`[rsp+0x68]` after `push` + `sub 0x30`) is tested and a null one jumps back to the shared 5 return at 0065B96A. `0065BA00` gets `[rsp+0x20]` = fifth and `[rsp+0x28]` = sixth.
  - `0065CA10` exact. `w` and `h` come from `shr 1` (unsigned). All three of `m` = `[rcx+0x58]`, `[rcx+0x68]` and `[rcx+0x60]` share the 1 exit at 0065CB7F. Equal sizes skip to the next `m`. `0060DD70(t, w, h, [t], [rsp+0x20] = 0)` follows the `00625F00` / `0062BCB0` pair, and the function returns 0 at 0065CB64.
  - `0065CB90` and `0065CC10` exact (0x4D / 0x4E). `n` = word `[rdx+0x12]` AND 0x1FFF and `o` = word `[rdx+0x10]`. The bound tests are `cmp ecx,[r11]; jbe` and `cmp r9w,4; jb` (unsigned "exceeds" / "below"). `00861EBA(rcx + o, r8, n)`, then the function returns 0.
  - `0065D200` exact: block `b` = `rsp+0x20..+0x30` = (0x42, 02D34718, `r8`); `rcx` = `[[rcx+0x78]+8]`.
  - `0065D4F0` exact. The kind dispatch is 0 -> `00625F00` / `0062BCB0`, 1 -> `00625F10` / `0062BF40`, 2 -> `00625F20` / `0062C100`. Every non-null slot of `+0xA0..+0xB0` is zeroed at 0065D5AC whatever its kind. Then `006505A0` runs on each non-null slot of `+0xB8..+0xC8` and on `+0xD0`, and each is zeroed.
  - `0065D700` exact: `0063A540(02D35600)`, then the function returns 0.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the PAnimation part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
