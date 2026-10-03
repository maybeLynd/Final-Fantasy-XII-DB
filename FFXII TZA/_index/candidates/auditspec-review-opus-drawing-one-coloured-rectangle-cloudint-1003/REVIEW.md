# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-drawing-one-coloured-rectangle-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-DRAWING-ONE-COLOURED-RECTANGLE-CLOUDI-837E5` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-drawing-one-coloured-rectangle-cloudint-1003/` · Page: `99-Unresolved-Residual/drawing-one-coloured-rectangle.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 3 rows, 15 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 3 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 3, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `002DD3C0`: `edx` = dword `[o+0x10]` - `eax` (low dword of `p`) - 0x10, then `shr 4` (unsigned). Dwords `p+8`/`p+0xc` are zeroed through the stack copy. The call is `0016D6A0(&t, edx)`; then `mov ecx, [t]; sub ecx, [o+8]` (32-bit, zero-extended), `and rcx, ~0xF`, `add [[o]+8], rcx`, and `003A1DB0(rcx, rdx = [o])`. Exact.
  - `002BC9C0`: the chain `sub 1; je` / `sub 3; je` / `cmp 0xa; je` selects 1 / 4 / 0xE, and any other value tail-jumps to `005C5230(rcx)`. Case 1 has both null guards and the stores (word `+0x9c`, dword `+0x98` = 0, word `+0x9e`). Case 4 has the null `+0xc0` guard, `00403F00([+0x38], rcx+0x98, [+0xc0], xmm3 = 1.0 at 01CEBBA8)`, and returns 0. Exact except for the mutable cells (narrowing N3).
  - `001B0190` (read in full): checked `001B2000`, the `js` early return (which also skips `001B0100`), the inclusive signed `jle` loop re-reading `+0x3928`, `cmp ebp, 0x3f; ja` (unsigned), and `r` = `rcx+0x2328 + i*0x58`. The divide by 0x30 is a signed magic divide (`0x2AAAAAAAAAAAAAAB`, `sar 3`, sign add). Also checked: the `[r]`-null split (slots `+0x48`/`+0x70` plus the two dword copies, vs. slot `+0x68(rcx+0x3930)`), slots `+0x78`/`+0x88`, the `+0x80` loop, slot `+0xa0`, `001FB840`/`001FB810(.., 0x20)` on `[rsp+0x28]`, the four resets, and `001B0100`. Two clauses overstate (N1, N2).
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing (exact wording)

**N1 (row `001B0190`).** When `001A1470` returns null, `001B0213 je` sets `b` = 0 (`r15`) and `001FBB40` is not called. Replace "takes `b` = `001FBB40(001A1470(qword 01F7F4C0, 0x238))`" with:

> takes `b` = `001FBB40(m)` for `m` = `001A1470(qword 01F7F4C0, 0x238)`, or 0 without that call when `m` is null

**N2 (row `001B0190`).** The four `movaps` loads read rows `008C5F80`, `008C5F90`, `008C5FB0` and `008C5FD0`. Read raw, these are (1,0,0,0), (0,1,0,0), (0,0,1,0) and (0,0,0,1). The range `008C5F80`..`008C5FD0` also contains `008C5FA0` = (0,-1,0,0) and `008C5FC0` = (0,0,-1,0), so read as a contiguous block it is not an identity. Replace "the identity matrix from `008C5F80`..`008C5FD0`" with:

> the identity matrix whose rows are loaded from `008C5F80`, `008C5F90`, `008C5FB0` and `008C5FD0`

**N3 (row `002BC9C0`).** `01E0C1D8`/`01E0C1DC` are `.data` dwords that `0024B120` writes: 0x780/0x438 when its `ecx` is non-zero, 0x200/0x1C0 when it is zero. These are the only writers a rip sweep of `.text` finds. Make two replacements:

- Replace "dword `01E0C1D8` (0x200)" with "dword `01E0C1D8` (0x200 in the image; `0024B120` stores 0x780 or 0x200)".
- Replace "dword `01E0C1DC` (0x1C0)" with "dword `01E0C1DC` (0x1C0 in the image; `0024B120` stores 0x438 or 0x1C0)".

The producer applies N1-N3. No anchor changes.
