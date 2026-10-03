# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PAnimation module part 2 (opus-member-modules-registered-before-main-phyre-panimation-module-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-708F1` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-panimation-module-2/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 35 functions, 164 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 35 rows, 164 anchors, mode `member`, family `Phyre PAnimation module`. Rejected 0, missing 0, corrections none. Skipped 2, both "too large for one precise sentence": `005AF3B0` and `005AFBC0`.
- Semantic pass: **15 of 35 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` field names resolved. For every registration row the record, type and name registers and each stack argument `[rsp+0x20..0x38]` were matched:
  - `005ACAA0`, `005ACBF0`, `005ACCA0` and `005ACE90` exact: vtables 00D317D8 / 00D312C0 / 00D312C0 / 00D31280 and sizes 0x10 / 0x10 / 8 / 0x18 under `test dl,1`.
  - `005ACB50` and `005ACFF0` exact: vtable 00D312F0; bit 0x4 selects `0016D6A0(rcx, 0x18)` / `(rcx, 0x20)` over `00584730(rcx)`.
  - `005ACEF0` exact: vtable 00D31298; the `[rcx+8]` release has only the null test, as stated.
  - `005AD140` exact: `shl 4`, alignment 0x10, both qwords zeroed per element.
  - `005AD6E0` exact: the copied prefix uses `movups` + `movsd`. The tail elements get qword `+0` = 0, qword `+8` = 3 (`[rax-4]` with `rax` = elem+0xC) and dword `+0x10` = 0.
  - `005AEFB0` exact. The unguarded `005B57A0(qword 01F2D0A8)` gets 00D31CB8, the name "PArray<PAnimationDataSource *>". `00632A10` takes (0x18, 0, 3, 8), followed by the store of 00D31CE0 and exit routine 008AA540. The `or [02CB1568],0x10` is the target of both guard exits.
  - `005AF280` exact. "m_keyType" is registered by `00632960(…, 005A65B0(), name, 0x38, 0x12, 0, 0)`. "m_interp" is registered by `00632BE0(…, 00630110(), name, 0x40, 0x10, 3)`, which takes three stack arguments. The exit routines are 008AA3C0 and 008AA360.
  - `005B0700` exact: the `or [02CADC3C],0x10` comes before the guards; the four registrations have offsets 0 / 2 / 4 / 6 with f 0x10, and guards and exit routines as listed.
  - `005B0C70` and `005B12C0` exact: the record/type pairs (02CAD840, 02CAEEE0, 02CAE150), offsets 0x18 / 0x20, f 0x12.
  - `005B0E70` exact. All six guarded registrations match. `m_inputIndex` goes through `00632A70` with (0xC, 0, 0x20). The `or [02CB2AA8],0x10` is the target of the third guard's exits. The last three offsets are 0x8C / 0x90 / 0x94.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all: 36 + 35 + 27 + 33 + 35 + 6 + 33 + 27 + 22 + 21.
  - Their corrections total 11 entries in 8 functions: 6 signed compares, 2 missing pass-through arguments, 1 wrong value on a path, 1 compare direction and 1 16-bit edge.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The details are in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
