# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-character-render-object-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CHARACTER-RENDER-OBJECT-1003` · Package: `_index/candidates/fable-home-character-render-object-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `17-Presentation-Rendering/Character-Rendering/character-render-object.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes. Its caller `001FA1A0` is a method in this page's own method table, so the host fits.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 1282 and the row (line 1288) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0.
- **`00186840` (0x5D B), read in full.**
  - `call 001EDE70` at +0xD (`0018684D`) / `test eax, eax` / `je` / `call 001EDDA0` at +0x16 (`00186856`).
  - Then `cmp byte [rbx+0xDBB], 0` and `mov edi, [rbx+0xDD0]`. On non-zero, `call 0017F280` at +0x2A (`0018686A`), and a non-zero result returns `[rbx + rax*8 + 0xB50]`. Every other path returns `[rbx + rax*8 + 0xB48]`.
  - The index is `mov eax, edi`, so it is zero-extended, and "i the dword" is right. The sentence is exact. All 5 anchors are on these instructions.
- **entered_from.** `001FA1A0` + 0x104 = `001FA2A4`, `call 00186840`, with `rcx` = `00189120()` (the `0xDD8`-byte singleton at `[01F7F598]`). The raw index gives a second caller, `0017FE60` + 0x1F (`0017FE7F`).
- **Host fit.** The page's method table lists `001FA1A0` as entry 24, `MaterialOverrideParameterPropagation` (line 157). That is a body citation of this class's own method, and the body is the buffer pick that method makes when `[rdi+0x664]` matches. Apart from `_index/ADDRESS-INDEX.md`, no other page cites `00186840`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- The twin `001868A0` (the same selection without the `0017F280` gate) is homed on `17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md` (line 289) from `0017FE60` + 0x10. Row 278 on that page already describes `0017FE60` as choosing between "a 66-byte helper" and "a 93-byte helper": the 93-byte one is this body. A cross-reference in either direction would join the pair.
