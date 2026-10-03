# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPostProcessing module part 1 (opus-member-es-registered-before-main-phyre-ppostprocessing-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ES-REGISTERED-BEFORE-MAIN-PHYR-F1FE5` · Package: `_index/candidates/opus-member-es-registered-before-main-phyre-ppostprocessing-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 33 functions, 164 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 33 rows, 164 anchors, mode `member`, family `Phyre PPostProcessing module`. Rejected 0, missing 0, corrections none. Skipped 3, each "too large for one precise sentence": `006007B0`, `0060F830` and `006458A0`.
- Semantic pass: **15 of 33 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `005FFF00` exact. The 0x16 return is gated on `test byte [rdx+8],8`. The slot vtable `+0x10` call runs on a zero `al` from `00600B30(rcx, 0, 1)`. The slot pick tests `[+0x60]+0x80` against `[+0x58]` (`jbe`, unsigned), then falls back to `[+0x50]`. A second `ja` failure stores the tried start to `+0x60` and returns 0xD. The six slot stores follow.
  - `0063A540` exact.
  - `006457E0` exact: vtable 00D62710; floats `+0x58..+0x6C` = 1.0, 0.5, 0x3F666666, 1.0, 1.0, 1.0; qword `+0x70` = 0x3F800000; float `+0x80` = 1.0; the nine zero qwords.
  - `00645D20` exact: vtable 00D61FE0; 0x40A00000, 0x40000000, 0x3F000000; 15 zero qwords `+0x60..+0xC8`.
  - `00645EC0` and `00646250` exact.
  - `00646590` exact. The vtable 00D61EA0 store comes first, then `0065D2A0(rcx)`, `006167C0(rcx+0x4130)` and vtable 00D61E50. The `+0x30`/`+0x38` release is gated on bit 31 clear, a masked count above 1 (`cmp 1; jbe`, unsigned) and a non-null pointer. Both fields are zeroed on every path.
  - `006466E0` exact: four `006505A0` calls on `+0x80..+0x98`, then the same tail.
  - `00646B10` exact: a two-pass loop over `+0x10` and `+0x18`, then the `+0`/`+8` pair.
  - `00646CB0` exact.
  - `00647140`, `006473E0`, `006476F0`, `00647820` and `00647950` exact. Each has the 00D61E50 tail with delete sizes 0xC0 / 0x80 / 0xA0 / 0xD8 / 0xB0. The last two first store 00D62440 / 00D622B0 and call `0065D4F0` / `0065D610`.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the PAnimation part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
