# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PDynamicGeometry module (opus-member-s-registered-before-main-phyre-pdynamicgeometry-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-S-REGISTERED-BEFORE-MAIN-PHYRE-PDYNA` · Package: `_index/candidates/opus-member-s-registered-before-main-phyre-pdynamicgeometry-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 399ce7caf)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 30 functions, 149 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 30 rows, mode `member`, family `Phyre PDynamicGeometry module`; rejected 0, skipped 0, missing 0; 2 corrections (`006BB6D0`, `006BB7D0`).
- Both corrections confirmed at the bytes: `006BB714`/`006BB72E` (`shl rdi,4; add rdi,[rcx+0x28]`) and `006BB7F5`/`006BB7F9` form the address of entry `edx` of a 0x10-byte array, and `006BB7A0` / `006BB8A1` read dword `+8` of it; the corrected wording ("the dword at qword `[rcx+0x28]` + `edx`*0x10 + 8") is what the rows now say.
- Semantic pass: **19 of 30 rows** read clause by clause against `disr.py` output of the certified image; all 19 exact:
  - `005DC0B0` (the first vtable store is overwritten by the second at `005DC0C7`, as stated), `006BB660` (`006394E0(rdx, 1, 02CB7180, 0)`; `005DC0B0(qword [r+0x60], original rcx)`).
  - `006BB6D0`: `e` = `[rcx+0x70]` + `edx`*0x18; sixth argument = `[rsp+0x68]` after three pushes and `sub rsp,0x20` (entry `+0x30`); loop bound masked dword `+0x30` with an unsigned `jb`; `x` tested with `js` (signed, "not negative"); `r9` advances 8 per `j` whether or not it stores; `006D2DA0(rbp=r8)`.
  - `006BB7D0`: as above with `s+0x28` = `s+0x20` and `s+0x30` = 0, the final dword going to `[r15]` = `s+0x20`.
  - `006BB8D0` (`dword [rdx+0x40]` read once; `005CCB80` = `Sleep`), `006BBD30`, `006BBDF0` (four pairs and their copy helpers, same free gate), `006C4750` (13 calls in order, `jne` to `ret` keeps the non-zero result, tail `jmp 006D6F90(01F32310)`).
  - `006CFA90` (null destination: `je 006CFB71` skips the `add r14,0x20`, so the source does not advance; `cmovne eax,r15d` for the count), `006D0290` (the fourth pair calls `006D2D20` on the bit test alone, no null test, as written), `006D0340`, `006D0450`, `006D0B20`, `006D0CA0` (tail fill 0xFFFFFFFFFFFFFFFF).
  - `006D2DA0` read in full: `h` layout (`+4`, `+8`, `+0xC`, `+0xE`, operators at `h+(dword h+4 + 1)*0x20`, sizes after them); batch size `0x40000 / max(1, unbound + 2*(inputs + bound))` (`cmova` from 1, unsigned `div`) `AND 0xFFFFFFF8`; bound = non-null qword in the table at `rcx+0x10` + word `[rcx+0x2E]` (`movzx r14d, word [r9+0x1e]`); per-pass `cmovb` minimum; operand selection (input slots `< r13` input else output `b - r13`; output slots byte `b - r13`, null when `>=` the output count); call `[r11+0x48]` with `rcx` = `rcx+0x10` + word `[rcx+0x50+2k]`, `edx` count, `r8`/`r9` operand arrays, fifth argument `&(dword op+0 + qword [rcx+0x20])`; `memcpy` (00861EBA) of bound outputs and the destination advance; the final `[rcx+0x38]` store; `_alloca_probe` 00808F10 and the cookie 01F44830 / 00808C40.
  - `006D5460` (frees through `006D2D20` without a null test, as written), `006D5A60` (0x11 / 0x12 / 0), `006D5AF0` (`cmovne eax,ebx` gives 0 for a match, 0x13 otherwise), `006D6F90` (the fall-out `ret` at `006D6FCD` returns `rax` = 0 from the exhausted walk, so "returns 0 on every path" holds).
- Advisory, not a defect: the `min(...)` in `006D5460` and its sibling resizers (`006BE5C0`, `006BE650`, `006D54F0`, `006D5580`) is an unsigned minimum (`cmovb`); OPUS may add "(unsigned)" in a later pass.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
- Batch-wide sentence, not this record's rows: the README's "262 stood, 10 clauses in 8 functions were corrected" (shared by all 11 records of 399ce7caf) does not match the `rows.json` corrections, which total 12 entries in 10 functions across the 11 records. The narrowing is recorded once, in `auditspec-review-opus-phyre-members-399ce7caf`.
