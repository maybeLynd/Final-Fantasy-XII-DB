# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PScene module (opus-member-een-modules-registered-before-main-phyre-pscene-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-EEN-MODULES-REGISTERED-BEFORE-93BE6` · Package: `_index/candidates/opus-member-een-modules-registered-before-main-phyre-pscene-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 6a52fe414)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 8 functions, 38 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 8 rows, 38 anchors, mode `member`, family `Phyre PScene module`; rejected 0, skipped 0, missing 0, corrections none.
- Semantic pass: **all 8 rows** (the request asks for at least 15; the record has 8) read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table):
  - `006B3E40` exact. The root `rdx` is tested first, then the walk starts at `[rdx+0x10]`. The next node is the child when present (`cmovne`), else the sibling. The climb follows `+8` and stops when it reaches `rdx` (both `cmp rax,r9` exits). A match needs a non-null `s` and a non-zero bit-0-stripped name with equal bytes, and each match overwrites `[rcx+8]`. It returns 0.
  - `006B4000` exact. The self-unlink and the `[rcx+8]` = 0 store both sit inside the non-null-`p` branch. The child loop reads next before unlinking and zeroes `[c+8]`. The `[rcx+0x60]` release is gated on non-null with bit 0 clear.
  - `006B40C0` exact: four qwords and 16 dwords copied; `001EAD40(rcx+0x60, [rdx+0x60] - (byte AND 1))` is skipped only when the two fields share an address.
  - `006B56D0` exact: the stack pair `[rsp+0x20]` = `rdx`, `[rsp+0x28]` = 0; `006B3E40(&pair, rcx)`; it returns `[rsp+0x28]`.
  - `006B5CB0` exact: `[rdx+8]` = 0 is stored on the found, not-found and empty-list paths alike, all inside the `[rdx+8] == rcx` test.
  - `006B5CF0` exact.
  - `006B6050` exact.
  - `006B60B0` exact. Row 1 lanes go to `+0..+0xC`, row 2 to `+0x10..+0x1C` and row 3 to `+0x20..+0x28`. Then `r0.x`, `r0.y` and `r0.z` overwrite `+0xC`, `+0x1C` and `+0x2C` (stores at 006B614B / 006B6154 / 006B6159), which matches the row's "final values" note.
- Batch-wide sentence (shared by the 8 PFramework, PHierarchy, PProfiling, PScene and PPhysics records of 6a52fe414): "154 rows … 150 stood, 4 rows were corrected in 4 clauses (three signed compares, one operand grouping)" matches the records and `verify_pphys_small_1003.json`, as checked in the PFramework record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
