---
experiment: EXP-115
title: Transform primitives — shipped bodies 00398F90 (TransformPointByWorkbenchMatrix) and 00397910 (ComposeTransforms) isolated under Unicorn with __security_check_cookie 00808C40 real
contract: ../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md
method: B
live_game: false
tool: evidence/transform-primitives-exec/check.py
---
# EXP-115 — transform-primitives-exec

**Status:** complete · **24/24 functional cases, 21/21 mutants, stable
across three processes**
**Evidence:** `evidence/transform-primitives-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The transform-primitives contract carries two already-proven laws from
a first isolated-execution instrument (`diff_transform.py`, 123+123
cases, 0 mismatches). This experiment re-executes the same two shipped
bodies under a **second, independent Unicorn harness** and adds three
things the first instrument did not: a byte-exact compare of the whole
`0x22D8F80..0x22D9330` globals window in one shot, a **byte-precise
mutation campaign on the shipped bytes** (every site verified against
the EXE before patching), and `__security_check_cookie` executed
**real** with the `__report_gsfailure` abort path exercised by a
deliberate cookie-corruption mutant.

| VA | role | execution |
|---|---|---|
| `00398F90` | TPT — TransformPointByWorkbenchMatrix | **real** (377 B, 68 insns, 0 calls) |
| `00397910` | CT — ComposeTransforms | **real** (567 B, 119 insns, 1 call) |
| `00808C40` | `__security_check_cookie` | **real** (79 B, 24 insns) |
| `00809654` | `__report_gsfailure` | disclosed fault-token boundary |

The GS check reads the shipped cookie at `q[0x01F44830]` out of the
mapped image — nothing injected. Reaching `0x809654` means the real
process would fast-fail (`int 0x29`); the harness records the reach as
a `gsfail` fault token and stops instead of emulating the abort.

## Measured semantics (native execution, not static reading)

**TPT `00398F90(rcx=in, rdx=out)`:** `out[j] = in[0]·M[j] +
in[1]·M[4+j] + in[2]·M[8+j] + w·M[12+j]` over the workbench matrix at
`0x022D91B0`, accumulated left-to-right with the `w` term added last.
`in[3]` is **loaded but never multiplied** — `w` is read live from
`f[0x01EF93FC]` (LEAF_G element 3; `1.0` on the shipped reset value).
Four side-effect deposits inside the observed window: the
pre-translation accumulator at `0x022D91A0` (products of rows 0–2
only), the input copied verbatim at `0x022D9300`, the assembled result
at `0x022D9310`, and the result again at `0x022D8F90`. The caller's
`[rdx]` gets the same result; when `rdx` lands inside the window
(`tpt-out-mat`) the observation reads it back correctly. `xmm6`/`xmm7`
are saved and restored.

**CT `00397910(rcx=a, rdx=b, r8=out)`:** staged `b×a` — `out[4r+j] =
a[j]·b[4r] + a[4+j]·b[4r+1] + a[8+j]·b[4r+2] + a[12+j]·b[4r+3]`, row
per loop pass, sequential `f32` adds in the body's order. Both inputs
are copied to the stack frame **before** the first multiply, so
`out==a`, `out==b`, and `a==b==out` all produce the distinct-buffer
result. `xmm6`–`xmm15` saved/restored; `q[0x01F44830] ^ rsp` checked
through a real `call 00808C40`; mismatch → `jmp 00809654`.

## Execution findings (beyond the static reading)

1. **`w` is a live global read, not a constant.** The contract's
   "forced to `1.0` from the constant at `01EF93FC`" is loose — the
   body executes `movss xmm4, [0x1EF93FC]` on every call. `tpt-leaf2`
   (element 3 = `2.0`) gains `2·M[3][c]`; `tpt-leaf0` drops the
   translation row entirely. `0x1EF93F0` is the same vec4 EXP-114's
   LEAF `0036DD80` resets to `[0,0,0,1]` — the "constant" is
   maintained state, and a reimplementation baking `1.0` would diverge
   under any writer that changes it.
2. **`in[3]` is copied to `0x22D9300` but never used.** `tpt-w-ignored`
   (`in[3]=99`) and `tpt-w-zero` (`in[3]=0`) produce byte-identical
   output and deposits — the input's fourth lane reaches the input
   deposit verbatim, nothing else.
3. **Triple-aliasing is safe.** `ct-alias-ab` (`a==b==out` at one
   buffer) computes `mata²` correctly — the stack staging precedes
   every store, so no source byte is consumed after being overwritten.
4. **The cookie check is real and load-bearing.** `m-c-cookie`
   (stored-cookie immediate `C4`→`C0`) reaches `00809654` — the fault
   token proves the comparison is against the shipped
   `q[0x01F44830]`, executed at `00808C40` in full (`cmp` + top-16-zero
   `rol` test + `bnd jne`).
5. **CT touches no globals besides the cookie.** The entire
   `0x22D8F80..0x22D9330` window stays at fixture init across all ten
   compose cases — the deposits belong to TPT alone.

## Mutation campaign

21 byte-precise mutations, every site verified against shipped bytes
before patching:

- **TPT (10):** three `shufps`/`pshufd` immediates broadcasting a wrong
  input lane (`55`→`54`, `00`→`01`, `AA`→`A9`), four `mulss`/`mulps`→
  `addss`/`subss` opcode swaps, three operand displacements — matrix
  `+0x15`→`+0x25`, leaf `CE`→`CA`, store `8F`→`90`.
- **CT (11):** loop counter `cmp r10d,4`→`3` (early exit), column
  stride `+4`→`+8`, loop `jne`→`je`, four element/row displacements
  (`+0x4`→`+0x8`, `+0x10`→`+0x14`, `+0xE0`→`+0xF0` ×2, `+0x2C`→`+0x30`),
  `mulss`→`addss`, `addss`→`subss`, store-row displacement, and the
  cookie-store immediate (fault token on the gsfailure path).

**21/21 killed.** Zero coverage-gap survivors — the 24-case fixture
discriminates every site on the first campaign.

## Limitations

- This is a **second** isolated-execution instrument over the same two
  bodies; the laws were already PROVEN by `diff_transform.py`
  (contract §13). What is new here: byte-exact whole-window compare,
  shipped-byte mutation kills, the real cookie check, the gsfailure
  observable, the live-`w` finding, and the `a==b==out` alias mode.
- `__report_gsfailure` is not emulated past its entry — the fault
  token records that control reached it; the real path ends in
  `int 0x29` fast-fail, which is process death, not a data observable.
- Matrix, input vector, `a`/`b`/`out` buffers, and LEAF_G are planted
  fixtures; the matrix's producers (`0039AF70` and the install sites)
  are outside this package.
- `bodies.json` holds body span + sha256 over shipped bytes;
  instruction-start coverage convention matches EXP-107–114.
