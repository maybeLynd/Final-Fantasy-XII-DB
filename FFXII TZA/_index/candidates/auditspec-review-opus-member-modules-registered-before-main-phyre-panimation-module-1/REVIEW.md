# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PAnimation module part 1 (opus-member-modules-registered-before-main-phyre-panimation-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-BB3B7` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-panimation-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 16 rows read are exact at the bytes, and all 7 of the record's corrections are right and applied. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 36 functions, 178 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 36 rows, 178 anchors, mode `member`, family `Phyre PAnimation module`. Rejected 0, missing 0. Skipped 2, both "too large for one precise sentence": `005A5F10` and `005A6E40`. Corrections 7, in 4 functions.
- Corrections, all 7 confirmed at the bytes and present in the rows:
  - `005A6900`: `cmp rdx,0x28; jle` at 005A6938, now "greater than 0x28 (signed)".
  - `005A6B40` x3: `jl` at 005A6B6E, `jge`/`jl` at 005A6BDD/005A6C48, and `jge`/`jl` at 005A6C8C/005A6D01 (`cmp rbx,r8` = `i` against `h`), each now worded as signed less/greater.
  - `005A7220` x2: `jge`/`jl` at 005A7257/005A72C8 and at 005A730C/005A7371, now signed.
  - `005A7990`: `memcmp(qword [rdx+8], qword [k+8], dword [k+4])` at 005A7A02. A positive result (`shr rcx,0x1f` = 0) takes child `+0`, which means the bytes at `rdx` are larger; the row now says so.
- Semantic pass: **16 of 36 rows**, spread over the package and including all four corrected functions, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `005A65B0` exact: guard 02CB29B0; `006B6820(02CB2950, 00D312A0 "PAnimationKeyDataType", 0x18, 8, [rsp+0x20] 006CD4C0, [rsp+0x28] 005BF070)`; store 00D323B0; exit routine 008A97B0.
  - `005A6900` exact (corrected row): magic 0x2AAAAAAAAAAAAAAB with `sar 2` (signed /0x18). `s` = (`n` + 1) / 8 (signed), with byte offsets `s*0x18` and `s*0x30`. `r9` reaches all four `005A6D40` calls; the short arm keeps the original registers.
  - `005A6B40` exact (corrected row). The key is `(dword [qword [e]+0x14] or 0) << 24 | dword [e+0xC]`. The child pick is `cmp ecx,eax; cmovae` (unsigned). The sift-up exits on `jae`. The 0x18-byte moves are `movups` + `movsd`.
  - `005A7220` exact (corrected row): the value's key is read from `[r9]` / `[r9+0xC]`; top = the incoming `rdx`.
  - `005A73B0` exact: `005A7220(first, 0, (l - first)/0x18, &t, [rsp+0x20] = r8)`; the loop recomputes the count after dropping `l`.
  - `005A7620` exact: index loop `jae`/`jb` on the masked count; field order `+0x20`, `+0`..`+0x18`, the string at `+0x28` (bit-0 stripped, same pointer, or non-null and byte-equal), then `+0x30`; -1 when none.
  - `005A7990` exact (corrected row): the dword compares are `jbe`/`jae` (unsigned) on `k` against `rdx`; the length is `k`'s dword `+4`; 0 at the sentinel.
  - `005A7D90` exact. The bit-0 set is `neg; inc; add`. The compare is node key against new key, positive when the node's is larger. `memcmp` takes (new `+8`, node `+8`, node dword `+4`). The parent with bit 0 goes to `[rdx+0x10]`, and `rdx` goes into `[r14 + al*8]`.
  - `005A9560` exact. The size is `n*0x50` (`*4 + n`, `shl 4`). The per-index check re-reads the masked count. The collision message is 00D32930 "Hash…", passed with `[s+0x28]` minus bit 0.
  - `005A9E70` and `005A9FE0` exact: the last arm of `005A9FE0` is `btr; cmp 1; jbe` on the masked count.
  - `005AA4E0` exact: `imul 0x58`, `005A5CC0`, `005B7FD0`.
  - `005AA600` exact: `shl 4`, `005A5E50`, `005B8050`.
  - `005AA710` exact: qwords `+8..+0x18` come through `r8` = `rdx+8`, and `+0x20` directly; then the three sub-assignments, the scalars, and `005AA970`.
  - `005AA970` exact: three (count, buffer) pairs through `00693C40` / `005AD230` / `006BC4C0`, each free gated `!= p`, bit 31 clear, non-null, plus the scalar copies.
  - `005AC8C0` exact: vtables 00D31898 and 00D312F0, the four member destructors, delete size 0x108.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 36 + 35 + 27 + 33 + 35 + 6 (PAnimation 1-6) + 33 + 27 + 22 + 21 (PPostProcessing 1-4) = 275 rows. 295 equals 275 plus the 20 PAnimation skips.
  - Their corrections total 11 entries in 8 functions: PAnimation-1 holds 7 (4 functions); PAnimation-3, -4 and -5 and PPostProcessing-3 hold 1 each; the other five records hold none.
  - By kind: 6 signed compares, 2 missing pass-through arguments (`005C68B0`, `005C6BF0`), 1 wrong value on a path (`00655A10`), 1 compare direction (`005A7990`) and 1 16-bit edge (`005B81A0`). The kinds the README lists are right; its counts are not.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK entries, and 11 FIX entries in 8 functions. Every FIX entry equals a `rows.json` correction, and its `new` text is in the row.
  - The commit subject's "18 clauses corrected" reads the same way; the batch total is 11 + 4 = 15.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
