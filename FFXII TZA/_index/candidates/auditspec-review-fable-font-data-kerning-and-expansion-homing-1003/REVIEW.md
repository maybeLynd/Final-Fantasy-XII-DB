# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-font-data-kerning-and-expansion-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-FONT-DATA-KERNING-AND-EXPANSION-HOMING` · Package: `_index/candidates/fable-font-data-kerning-and-expansion-homing-1003/` · Page: `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 1126, and both sentences are on the page verbatim.
- **rows.json.** 2 rows, 10 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** Both rows were read clause by clause against `disr.py` output of the certified image.
  - `001B5140`:
    - `001B4930(rcx)` runs first. Then `rbx = [rdi+8]`, and `cmp rbx, [rdi+0x10]` / `je` skips everything.
    - Each pass zeroes 0x18 bytes at `rsp+0x20` (a 16-byte `movdqu` plus the qword at `rsp+0x30`).
    - Then `001EDF00(rsp+0x38, E+0x18)`. `rsp+0x38` is the qword just past B.
    - Then `001A4BF0(B, [E], [E+8])` and `001B5610(rcx, B)` at +0x58.
    - `add rbx, 0x20` / `cmp rbx, [rdi+0x10]` / `jne` re-reads the end on every pass.
    - Exact.
  - `00679ED0`:
    - `cmp [rcx+0x258], 1` / `je` returns 0.
    - The loop calls `005CD840(rcx+0x4F8)` at +0x27. `00679BF0(rcx)` runs when `+0x268` is 1 (`je`) or 2 (`jne` skips otherwise), and only when `cmp [+0x25C], 2` / `je` does not skip.
    - It loops `jne` until `+0x258` reads 1, then returns `xor eax, eax`.
    - Exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
