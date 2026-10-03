# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PPostProcessing module part 2 (opus-member-es-registered-before-main-phyre-ppostprocessing-module-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ES-REGISTERED-BEFORE-MAIN-PHYR-79EAB` · Package: `_index/candidates/opus-member-es-registered-before-main-phyre-ppostprocessing-module-2/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows read are exact at the bytes; this record has no corrections of its own. The narrowing is the batch-wide count sentence in the README and in `rows.json` `method`, which is shared by the 10 PAnimation and PPostProcessing records of 6a52fe414.

**Narrowing (exact wording).** In `README.md` and in `rows.json` `method`, replace "read every one of the 295 rows of this batch against the disassembly: 286 stood, 9 rows were corrected in 14 clauses (signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)" with:

> read every one of the 275 rows of this batch against the disassembly: 267 stood, 8 rows were corrected in 11 clauses (six signed compares worded above/below, two missing pass-through arguments, one wrong value on a path, one overgeneralised compare direction, one 16-bit edge)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 27 functions, 132 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 27 rows, 132 anchors, mode `member`, family `Phyre PPostProcessing module`. Rejected 0, missing 0, corrections none. Skipped 11, each "too large for one precise sentence": `006491B0`, `006497E0`, `0064A500`, `0064AA20`, `006508C0`, `006515C0`, `006525F0`, `00652A90`, `00653E80`, `00654170` and `00654470`.
- Semantic pass: **15 of 27 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` field names resolved:
  - `00647A90`, `00647BC0`, `00647DA0`, `00647EC0` and `00647F50` exact. Each ends with the shared 00D61E50 tail (free gated on bit 31 clear, a masked count above 1 (`jbe`, unsigned) and non-null; both fields zeroed). The delete sizes are 0xB0, 0x3248, 0x50, 0x68 and 0x68; `00647BC0` first calls `00646920(rcx+0x50)`.
  - `00648620` exact: five registrations with `[rsp+0x28]` = 0 (flags 0) and offsets 0x58 / 0x5C / 0x60 / 0x64 / 0x74; types `006301F0()` x3 and `006B19A0()` x2; every guard dword and exit routine matches.
  - `00648C70` exact: "m_focusPlaneDistance" / "m_focusRange" / "m_focusBlurRange" at 0x50 / 0x54 / 0x58.
  - `00648FB0` exact: "m_velocityScale", offset 0xD10.
  - `006496A0` exact: "m_minReflectionDirZ" (0x50) and "m_marchStepFactor" (0x54).
  - `0064AEA0` exact: base `[rcx+0x58] - 8` (`cmove` 0); slot `+8` (e, 0, 0) then slot `+0x10` (e); the first non-zero result is returned.
  - `00650490` exact. `0060DD70` gets the incoming `edx`, `r8d` and `r9` unchanged and `[rsp+0x20]` = 0. The fifth and sixth arguments are `[rsp+0x60]` and `[rsp+0x68]`.
  - `00652940` exact. Block `b` = `r11-0x40..-0x30` = (0x42, 02D35140, `r8`); the early `001B81B0` return comes before `o` is built. The stop-at-first-non-zero chain matches. `0060CD70(x, 0, 6, 7)` (`lea r9d,[rax+7]`, `lea r8d,[rax+6]` with `rax` = 0). `0060B980(x, [02D34710], &p, 0, [rsp+0x20] = dword [x+0x220], [rsp+0x28] = byte 0)` with `p` = (008C6C98, `rcx+0x30`). `0016D6A0(&o)` runs on both exits.
  - `00653B30` and `00653BB0` exact.
  - `00653CE0` exact. The bound tests are `cmp ecx,[r10]; jbe` and `cmp r9w,4; jae` (unsigned "exceeds" / "below"). Both `0065CC90` blocks carry 0x43. The final call passes `/4` values made by `shr 2` (unsigned) in `r9d`, `[rsp+0x20]` and `[rsp+0x28]`, and its result is returned.
- Batch-wide sentence (shared by the 10 PAnimation and PPostProcessing records of 6a52fe414, and the reason for this record's narrowing). "295 rows … 286 stood, 9 rows were corrected in 14 clauses" does not match the records or the verifier's own output:
  - The 10 `rows.json` hold 275 rows in all.
  - Their corrections total 11 entries in 8 functions.
  - `Tools/work/OPUS/cloud/verify_panim_ppost_1003.json` agrees with the records: 275 functions, 267 OK, and 11 FIX entries in 8 functions. The full breakdown is in the PAnimation part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
