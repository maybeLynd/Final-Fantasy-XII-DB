# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PAnimation module part 6 (opus-member-modules-registered-before-main-phyre-panimation-module-6)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-C0DF3` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-panimation-module-6/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 6 rows are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 6 functions, 22 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 6 rows, 22 anchors, mode `member`, family `Phyre PAnimation module`. Rejected 0, missing 0, corrections none. Skipped 1: `005CB8D0`, "too large for one precise sentence" (999 B).
- Semantic pass: **all 6 rows** (the request asks for at least 15; the record has 6) read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `005CB780` exact: first check slot `+0x10` (`rdx`, `rcx`); optional check `[rcx+0x10]`'s slot `+0x18` (`o`, `rdx`, `rcx`); final call slot `+0x20` (`rdx`, `rcx`, `r8`), then `al` = 1.
  - `005CB800` exact. The four pairs are handled in the order 8, 0x40, 0x58, 0x18, each under `test eax,eax; je`, with the free gated non-null and bit 31 clear. The dword `+0x38` and `+0x50` stores are the jump targets of the 0x40 and 0x58 tests, so they run either way. `00584730([rcx+0x68])` has no null test.
  - `005CC680` and `005CC690` exact.
  - `005CC6A0` exact. The search stride is 0x98 (`imul 0x98`, unsigned `jb` bound). The not-found arm stores at element `n` and increments the count. The shift loop re-reads the count each pass and moves 0x98 bytes (nine `movups` + one `movsd`). The final store goes to element `n - 1`.
  - `005CC7D0` exact. The hash is seeded with 0x7B5, then `*0x21 + (byte AND 0x1F)` per byte. The key layout is `[rsp+0x20]` = hash, `+0x24` = strlen, `+0x28` = `s`. The slot index uses magic 0x6666666666666667 with `sar 4` (/0x28), truncated to 32 bits (`mov ecx,ecx`). The store happens only into an empty slot.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
