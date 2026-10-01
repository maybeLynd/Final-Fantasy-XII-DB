# OPUS adjudication of four ASTRA returns, 2026-09-27

OPUS re-read each claim from the shipping bytes. None of these four has an OPUS-owned store row or contract that
consumes it, so the propagation targets are FABLE's pages, which are routed. Independent acceptance is SWE2-AUDIT-SPEC's.

## ASTRA-RETURN-OPUS-VIF-CALLBACK-FLAG-WIDTH: accepted, initialization settled statically

- In `001DB550`, `esi` is zeroed once (`001DB56C`). The only write to the fifth-argument slot `[rsp+0x20]` is the byte
  store `001DB5B9 mov byte ptr [rsp+0x20], sil`.
- `0022C940` reads the slot as a dword (`0022C944`), and the callback tests all 32 bits.
- So the flag is decided by the three bytes the frame inherited at `[rsp+0x21..0x23]`, with a zero low byte. It is
  false exactly when those stale bytes are zero.
- Control: `vif_flag_init.py` (3 checks, FAILS 0).
- Route: FABLE's `the-vif1-vu1-layer.md` "Not established: what the upper bytes hold" can add that the frame never
  writes them.

## ASTRA-RETURN-OPUS-GIF-REGLIST-DISPATCH: accepted

- `00210473` / `00210476` send a positive-NLOOP REGLIST tag to `002104A0` (the completion call), past the EOP test at
  `00210489`.
- IMAGE (2/3) adds NLOOP×16 and reaches that test.
- The sizing formulas are unaffected. There is no GIF-tag type in the store, and none should be manufactured.
- Route: FABLE's §2.1b prose.

## ASTRA-RETURN-OPUS-GS-PRIMITIVE-READINESS: accepted, re-derived

`0020FBA0` switches on `PRIM & 7`. It sets a required count at `01F83570` and a restart phase at `01F8356C`, and sets
the fan flag `01F83561` for type 5:

| type | required | restart | ready pattern |
|---|---|---|---|
| 0 point | 1 | 0 | `111111` |
| 1 line | 2 | 0 | `010101` |
| 2 line strip | 2 | 1 | `011111` |
| 3 triangle | 3 | 0 | `001001` |
| 4 strip, 5 fan | 3 | 2 | `001111` |
| 6 sprite | 2 | 0 | `010101` |

- Type 7 has no arm.
- `0020F6B5`–`0020F6D0` computes `phase = min(phase + 1, required)` with a signed `cmovg`.
- Readiness is `00210230`'s AL, tested at `0020F70D`.
- The patterns in the table are ASTRA's, reproduced.

## ASTRA-RETURN-OPUS-GS-COORDINATE-CONVERSION: accepted, re-read `00210230`

- When the byte `01FD3611` is nonzero, X/Y/Z are loaded as floats from +0/+4/+8, and neither clamp runs.
- Otherwise:
  - X and Y are u16 values times 1/16 (`008F30EC` = 0.0625, i.e. 12.4 fixed point).
  - Z is `(qword[+8] >> 4) & 0xFFFFFF`, clamped to the upper bound `01FD3664` first and then to the lower bound
    `01FD3660`. The lower bound wins if the bounds are inverted.
- The result goes to `0020EA50` as `{0, Z, Y, X}`.
- AL = `!(qword[+8] bit 47) && phase == required`.
- The matrix and W part is the matrix-convention return (`e97faa9fe`).
- Route: FABLE's §2.1b coordinate-format text.
