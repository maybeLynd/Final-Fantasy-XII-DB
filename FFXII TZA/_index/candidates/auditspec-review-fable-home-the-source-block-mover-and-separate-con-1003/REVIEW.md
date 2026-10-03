# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-source-block-mover-and-separate-con-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SOURCE-BLOCK-MOVER-AND-SEPARA` · Package: `_index/candidates/fable-home-the-source-block-mover-and-separate-con-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md`

## SWE2-AUDIT-SPEC verdict: REJECT

**Both hosts are wrong, and one sentence names the wrong argument registers.**

- Both bodies are dirty-state handlers of the 0x740-stride character render record. `RenderRecords_ProcessDirtyState` (`00427DE0`) runs them for `+0x290` bits 2 and 3.
- This page cites `00427DE0` only for its skip rule (`record+0x288 == -1`, lines 122 and 208, the latter inside a Presentation cross-subsystem paragraph). The function belongs to `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`, which reads its five passes (line 785 on) and already describes the `+0x180` model matrix and the neighbouring `004209C0`.
- `00420860`'s sentence says "`rdx`, `r8` and `r9` passed through". The arguments that are passed through and used are the floats in `xmm1`, `xmm2` and `xmm3`.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 6 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 220 and both rows (lines 226-227) match `rows.json` byte for byte.
- **rows.json.** 2 rows, 6 anchors. Rejected 0, skipped 0, missing 0.
- **`00420860` (0x23 B), read in full.**
  - `movss xmm0, [01CEBBA8]` (1.0) / `add rcx, 0x210` / `movss [rsp+0x20], xmm0` / `call 006C0520` at +0x19 / `ret`. The site, the fifth stack argument and the anchors are right.
  - The callee `006C0520` reads `xmm1`, `xmm2`, `xmm3` and `[rsp+0x28]` and stores them to floats `+0`, `+4`, `+8` and `+0xC` of `rcx`. It never reads `rdx`, `r8` or `r9`.
  - The caller loads `xmm1`/`xmm2`/`xmm3` from floats `+0x380`/`+0x384`/`+0x388` of the record (`00427E9C`-`00427EAF`) and sets no integer argument register.
  - "`rdx`, `r8` and `r9` passed through" is true of registers this body does not touch, but it names the wrong argument registers.
- **`004209F0` (0x16 B), read in full.** `or dword [rcx+0x284], 0x200` / `add rcx, 0x180` / `jmp 0046D100` at +0x11 (`Matrix4x4f_Copy`, which jumps to `00202C70`). The caller passes `rdx = rbx+0x340`. The sentence is exact.
- **entered_from.** `00427DE0` + 0xD7 = `00427EB7` and + 0xA2 = `00427E82`, both direct calls. They are the only callers (raw index). They sit in pass 1, under `test byte [rbx+0x290], 8` and `test byte [rbx+0x290], 4`, and each bit is cleared after its call.
- **Host fit: the defect.**
  - This page's subject is the original arena source movement and the separate consumer refresh. It cites `00427DE0` only for the delivery skip on `+0x288`.
  - Neither body touches source blocks or that rule. They write the record's `+0x210` float quad and its `+0x180` matrix and set `+0x284` bit 9.
  - `the-character-render-record-array.md` (DOCUMENTED) reads `00427DE0` pass by pass (lines 785-811), names `+0x180` as the model rotation matrix (line 227), and describes `004209C0`, the function right before `004209F0`, as copying record fields into the model (line 1134).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove both rows from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home both rows on `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`, which cites `00427DE0` in its own text. `004209F0` moves unchanged.
3. `00420860`, replacement wording: "calls the site `00420860` + 0x19 with `rcx+0x210`, the floats `xmm1`, `xmm2` and `xmm3` passed through, and 1.0 (`01CEBBA8`) as the fifth (stack) argument, then returns". The anchors stay.
