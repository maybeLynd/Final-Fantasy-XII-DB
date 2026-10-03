# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PAnimation module part 3 (opus-member-modules-registered-before-main-phyre-panimation-module-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-8C8E8` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-panimation-module-3/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 16 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 27 functions, 128 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 27 rows, 128 anchors, mode `member`, family `Phyre PAnimation module`. Rejected 0, missing 0, corrections 1 (`005B81A0`). Skipped 12, each "too large for one precise sentence": `005B14E0`, `005B1900`, `005B2D60`, `005B3DE0`, `005B45B0`, `005B5460`, `005B57A0`, `005B7AC0`, `005BF290`, `005BFC40`, `005C04B0` and `005C22B0`.
- Correction confirmed at the bytes: in `005B81A0` the entry base uses `(word [h+6] + 3) AND 0xFFFFFFFC` in 64-bit registers (`add rdx,3; and rdx,rbp` at 005B820F/005B8216), while the stored header word uses the 16-bit `and ax,di` (005B820C). The row now distinguishes `w2` from `w`.
- Semantic pass: **16 of 27 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved. For every registration row the record, type, name and each stack argument, guard dword and exit routine were matched:
  - `005B1D90` exact. Both getters run unguarded: `005B4E00(qword 01F2D110)` gets 00D329D8 "PArray<PUInt32>", and `005B6E00(qword 01F2D118)` gets "PArray<PAnimationSlotFilterDeferredLoad>". The two `00632A10` calls take (0x18, 0, 3, 4) and (0x30, 0, 3, 8), with stores 00D329F0 / 00D32A80. Both `or 0x10` (02CB33D8, 02CB34A8) are targets of their guards' exits.
  - `005B20D0` exact: four registrations, including `m_interp` through `00632BE0(…, 8, 0x10, 3)`.
  - `005B23B0` exact.
  - `005B2560` exact: all six registrations (types 02CAD840 / 02CAEFE0 / 02CAF0E0 / 02CADD50 / `006301F0()` x2, offsets 0 / 0x10 / 0x38 / 0x58 / 0xC / 8).
  - `005B2990` and `005B2BB0` exact.
  - `005B80E0` exact. The early return passes a non-zero `006AADD0` result through. The record base is `[rcx+0x58] - 8`, with `cmove` 0 when null. Two gates guard `005C6980(e, 0, p)`: a masked count of 1 (`btr; cmp 1; jne`), and a zero from `005C7130(e, p)`.
  - `005B81A0` exact (corrected row). The 16-bit header word is computed in `cx` with `add cx,cx` twice, `+0x17` and `and cx,0xFFF0`. The entry base is `h + 2*(w2 + 2*(word[h+4] + word[h+2] + 2))`, rounded up to 8 with `neg; and 7; add`. Each entry stores `[[o+0x48]+0x10]` and `[o+0x58]`.
  - `005BED30` exact.
  - `005BEF70` exact: `00584740(0x28)`, `0067FFB0(p, 0x20, 0x80, 8, [rsp+0x20] = 00D32738 "ANIThreadPoolJobs")`; the store happens before the null test.
  - `005BF070` exact.
  - `005BF0E0` and `005BFEA0` exact: the 5th and 6th arguments are forwarded from `[rsp+0x70]` / `[rsp+0x78]` to `[rsp+0x20]` / `[rsp+0x28]`, and 005B3DE0 / 005B45B0 go in `[rsp+0x30]`.
  - `005C03D0` exact: `lea eax,[r8+7]` for a null `t`; the `+0x80` save and restore around `005C04B0(rcx+0x90, rcx+0x70, 0, 0)`; the other arm `005B2D60(rcx+0x90, rcx+0x70, t, x+0x18)`.
  - `005C1000` exact: the 0 and 1 early returns, and the class-chain walk to 02E518D0. The name loop does not stop at the first match (no break after the stores), so "for every match" holds.
  - `005C2FE0` exact. The bit-set size is `((n*4 + 0x1C) AND 0xFFFFFFE0) >> 3` bytes, allocated through `00808F10` and cleared by `memset`. The bit index is `dword +0x40 | (dword [[e+0x38]+0x14] << 2)`. Each bit is set and counted once; cookie 01F44830.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
