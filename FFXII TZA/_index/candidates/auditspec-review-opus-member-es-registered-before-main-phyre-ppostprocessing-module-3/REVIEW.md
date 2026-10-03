# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPostProcessing module part 3 (opus-member-es-registered-before-main-phyre-ppostprocessing-module-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ES-REGISTERED-BEFORE-MAIN-PHYR-3741B` · Package: `_index/candidates/opus-member-es-registered-before-main-phyre-ppostprocessing-module-3/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes, and the record's one correction is right and applied. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 22 functions, 109 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 22 rows, 109 anchors, mode `member`, family `Phyre PPostProcessing module`. Rejected 0, missing 0, corrections 1 (`00655A10`). Skipped 12, each "too large for one precise sentence": `00654610`, `00654830`, `00654B00`, `00654E20`, `00655180`, `006553D0`, `00655690`, `00655F10`, `006566D0`, `006568D0`, `00656B20` and `00656F20`.
- Correction confirmed at the bytes: in the second stage of `00655A10`, when `w` (or `h`) is still 0 and the second `s` is null, the stored value is the 0x500 preloaded in `ebp` (or the 0x2D0 in `ebx`, 00655A3D / 00655A52), not the kept zero. The row now says so.
- Semantic pass: **15 of 22 rows**, spread over the package and including the corrected function, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `00655A10` exact (corrected row): both stages call `005FD050()` and add 0x520 (the null test reads ZF from the `add`); `w` goes to `+0x44`, `h` to `+0x48`, and 1 to byte `+0x40`.
  - `00655AC0` exact. `00655690(rcx, 02D35600, w, h, [rsp+0x20] = 0)` comes first. On a zero result the second stage stores the second `s`'s dwords, or the preloaded 0x500 / 0x2D0, without regard to `w` and `h`.
  - `00655C10`, `00655CA0` and `00655E30` exact. They call `006560E0` / `00654170` / `00654610(rcx, 02D35600, w, h)` respectively. The fallback `00655DC0(rcx, edx, r8d)` receives the original `edx` and `r8d` (saved in `edi` and `ebx`).
  - `00655EC0` exact: `0064A500(rdx, 8)` goes to `+0x4120` and `006497E0(rdx, 0x10)` to `+0x4128`.
  - `006571E0`, `00657250`, `006574A0`, `00657570` and `00657610` exact. They share one shape with the callees `006561D0` / `006566D0` / `00656B20` / `00655180` / `00656F20`, each taking (`rcx`, 02D35600, `00653B10(rcx)`). The tail stores `+0x18`, `+0x20` = `[p+8]` or 0, and `+0x28` = `[q+0x18]` or 0.
  - `00657330` exact. `00654E20(rcx, 02D35600, d)` is called first, then six `0018D240(d, name)` stores to `+0xA0..+0xC8`. The names resolve to 00D62E68 "ColorInput", 00D62A78 "DepthBuffer", 00D62E78 "NearProcessed", 00D62E88 "DoFCompositeNearInput", 00D62EA0 "DoFCompositeBlurInput" and 00D62EB8 "DoFCompositeColorInput".
  - `006576D0` and `006577F0` exact: `0065C4D0` / `0065C910` receive `rcx`, `edx` and `r8d` unchanged.
  - `00657710` exact. The 1 return covers a null `m`, a non-zero `[m+8]` and a null `t`. On equal sizes the code jumps straight to the stores. `0060DD70(t, edx, r8d, [t], [rsp+0x20] = 0)` follows the `00625F00` / `0062BCB0` pair.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions. This record's "wrong value on a path" is one of them.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the PAnimation part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
