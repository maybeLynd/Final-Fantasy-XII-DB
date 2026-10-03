# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-game-settings-ini-and-runtime-config-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-GAME-SETTINGS-INI-AND-RUNTIME-CONFIG-H` · Package: `_index/candidates/fable-game-settings-ini-and-runtime-config-homing-1003/` · Page: `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 17 functions, 82 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 1843, and every sentence is on the page verbatim.
- **rows.json.** 17 rows, 82 anchors. Rejected 0, skipped 0, missing 0. 1 FABLE correction (`00798AC0`, "zeroing P+2" widened to P+2 to P+9). The correction is right: `00798C9B` is `mov qword [rdi+2], r12`.
- **Semantic pass.** All 17 rows were read clause by clause against `disr.py` output of the certified image, not just 15.
- **`0023CAF0`.** Every branch was traced.
  - When `+0xC8` is 0: R = P4. S runs `002F9860(i + 0x53F)` at +0x126, then clears P0, P1 and P3, sets P4 and clears P2.
  - Otherwise: R = P3, S(`001E0B00` at +0x3F on `[rcx+0xD0+i*4]`, then `002F9860` at +0x46), set P3, clear P4.
    - If `+0xE8` = i: set P0, clear P1 and P2, and run S(0x46DD) at +0xAE when `+0xEC` is non-zero.
    - Else, if `+0xDC+i*4` and `+0xD0+i*4` differ (`je` not taken): set P2, clear P1 and P0. If they are equal: clear P0, set P1, clear P2.
  - Every path ends with `0029FAD0(R)` and returns 1.
  - The sentence lists the first arm's clears in a slightly different order than they run; nothing reads between them.
- **`0026A660`.**
  - `edx` = 0 reaches only `and byte [+0xC], 0xDF`, followed by `setne` (0) shifted left 5 and ORed.
  - Otherwise R comes from the low 32 bits of `0020E600([[rcx+0x40]+0x18])` (`mov ecx, eax`), used against the qword at `02098E10 + byte[+0x15]*0x288`.
  - `cmp ax(5), word [R]` / `jge` gives the self-loop for a signed word of 5 or less. `movsx [R+0xC]` / `jns` gives the same loop when it is negative.
  - Then the second, discarded `0020E600`, and the final bit `0x20`.
  - Exact. A `+0xD2` that is not `0xFFFF` takes `movzx` / `jns` and never loops, which the sentence's "when ... is 0xffff" covers.
- **`002A7C70`.** In the `r9d` = 0 arm, the `and` and the `[rdx]` copy. In the other arm, the zero of `+0x20` is gated on word `+0x40` = 0 and `001EDDA0()` = 0. The byte differences use `al` = the low byte of the just-reloaded `+0x20`, then `+0x21`..`+0x23`. Then word `+0x40` = 0 and `r9w` to `+0x42`. Exact.
- **`002D5590`.**
  - Case 1: the `0x28` / `[rdx+8]` stores, `00247570(rcx, 00917180)` at +0x80, then `002432B0(rcx+0x50, [[0209AC30]+0x18], 4|5|3, rcx)` at +0xBD by `+0xC0` = 1/2/other, the word copies and the `0x80` clear.
  - Case 2: `001EDEC0`, `jle`, `dec`, `jg`, then `00244F00(rcx)` at +0x56.
  - Any other value takes the tail at +0x1D.
  - Exact.
- **The tables and flags rows.**
  - `00551610` and `00552050`: the `jbe` on byte `+2` is a zero test; `00552050` tests byte `+0x14` bit 0 instead. Both copy bit 1 to bit 0 with the `xor`/`and`/`xor` idiom and end with the `+0x18`/`+0x20` stores.
  - `005516A0`: A, B and C from signed indexes. v = `((movsx +0x14 >> 7) * movsx [r8+0x58]) >> 7`. `[rsp+0x33]` = the low byte, so the 0x80808080 dword gets it as its top byte, stored to A and C `+0x28..+0x34`.
    - Case 0: `rbx + (3i+5)*8` = `rcx+0x28+i*0x18` into `00551610` at +0x140.
    - Case 3: `00552050(rcx+0x28, A, B, C)` at +0xB4.
    - Case 1 matches clause by clause.
    - Return 1.
  - `00556F50`: `rcx+0xD0+(movsxd r9d << 8)`.
  - All exact.
- **The rest.**
  - `001F3A00`: offsets +0x11, +0x1B, +0x32 and the tail at +0x44 with `(rdx, 3)`.
  - `003484A0`, `00348A70` and `00348DA0`: `00263FF0(3)`, then tails at +0x15.
  - `00357170`: `00264160` at +0x10 with no argument loaded. `cmp eax, 2` / `je` skips the `or byte [+0x17], 4`, and `eax` is returned.
  - `003E0860`: five resolve-twice-then-call blocks, at +0x29, +0x46, +0x63, +0x80 and +0x9D, for dwords `+8`, `+0x28`, `+0x34`, `+0x3C` and `+0x24`.
  - `00616560`: every call and offset, including the three `eh_vector_destructor_iterator` calls (element sizes 0x190, 0x18 and 0x18) and the two conditional `0062B890` calls.
  - `0067ACF0`: `cmovne` takes `[rdx+8]`, then `btr 0x1F` before `0067B100` and `memcpy`.
  - `00798AC0`: the BMP header stores, the swap loop (H rows by W groups at stride S), the `0x38 + S*H` sizes, the 0xD/9/F+8 return values and the cleanup order.
  - All exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
