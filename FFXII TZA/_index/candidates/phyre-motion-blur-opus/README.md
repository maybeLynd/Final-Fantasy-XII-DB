# PMotionBlurBase: the constructor's full body (OPUS, 2026-09-28, a correction of OPUS's own rows)

**State: PENDING INDEPENDENT REVIEW.**

**What was wrong.** OPUS's PMotionBlurBase rows from 2026-09-19 and 2026-09-20 made four claims:

- `floatDefaults0050` gave a "20-byte rhythm" with "one extra at +0x90 that does not fit".
- `unobservedSpan00D0` said "the element is 0x14, not 0x40; the identity reading is WRONG".
- It also said "the constructor initialises only SIX records".
- It also said "the setter writes nothing between +0xD0 and +0xD10".

All four came from a reading of `00646000` that stopped before its loop.

**What the constructor does.** [`motion_blur_ctor.py`](motion_blur_ctor.py) ([output](motion_blur_ctor.out)) runs checks C,
R, D and W: FAILS 0. W failed on the store before the patch.

- **C: the writes.** `00646000` writes 0x40-byte blocks. Each block has 1.0f at +0x00, +0x14, +0x28 and +0x3C and zero
  elsewhere: the 4x4 identity.
  - Two blocks sit at +0x50 and +0x90.
  - Then a 16-pass loop (`rcx = 0x10`, `rax = this + 0x528`, `rax += 0x40`) writes the block at `rax - 0x18` and at
    `rax - 0x418`. That fills +0x510..+0x90F and +0x110..+0x50F.
  - Then +0xD10 = 10.0f (`m_velocityScale`), and ten qwords at +0xD18..+0xD60 are zeroed.
- **R: the rejecting regression.**
  - A 0x14 record predicts 1.0f at +0xA0 and none at +0x90. The constructor stores 0 at +0xA0 and 1.0f at +0x90.
  - All 136 1.0f stores sit at a block base (0x10 mod 0x40) plus 0, 0x14, 0x28 or 0x3C.
  - The "+0x90 that does not fit" is the block boundary.
- **D: the constructors.**
  - `0063F580` is PMotionBlurD3D11's placement constructor, at descriptor `00D5A140` + 0x50. It runs `00646000`, installs
    `00D62120` and zeroes +0xD68.
  - `0063E9C0` is PMotionBlurBase's thunk.
- **N: who reads the matrices.** The vtable census of `00D620D0` (9 methods) and `00D62120` (10 methods) reaches nothing in
  +0x50..+0xD67. So the readers of the 34 matrices are outside the classes' own methods. Float typing therefore rests on the
  identity pattern and is marked PROBABLE.

**Not claimed:**
- what the matrices are for;
- who writes +0xD0..+0x10F and +0x910..+0xD0F. The sampled default buffer's pattern there came from a path other than this
  constructor.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PMotionBlurBase +0x50 / +0xD0 / +0xD14 | replaced by 7 rows (two matrices, two arrays of 16, three declared gaps and a zeroed qword run); old text kept verbatim in their evidence | revised-here |
| `_types/types.tsv` PMotionBlurBase / PMotionBlurD3D11 ctor column | 00646000 / 0063F580 | revised-here |
| `the-phyre-post-effect-class-family.md` §3d ("methods reach nothing at/above +0x50") | the same finding (check N) | agrees |
| the same page, "PMotionBlurBase unobserved 3,220" | a dated measurement; the carve lowers it | agrees (dated) |

**Run receipt:** `motion_blur_ctor.py` FAILS 0; `types_index.py --validate`: 0 errors; the width, reference and embed checks:
0.

## PAtmosphericsBase: its constructor's defaults (OPUS, 2026-09-28)

[`atmospherics_ctor.py`](atmospherics_ctor.py) ([output](atmospherics_ctor.out)), checks C and W: FAILS 0. W failed before the
patch.

PAtmosphericsBase's four unregistered spans said only that no reflection registration covers them. Its constructor
`00645520` (`006461B0`, then vtable `00D62800`) writes all four:

- **+0x64..+0x80: integer immediates.** 0x100, 0x40, 0x40, 0x10, 0x100, 0x80, 0x20, then 2.
- **+0xB0..+0xBC: float defaults.** 32, 128, 32, 8.
- **+0xE4..+0xF0: float defaults.** 128, 4, 32, 4.
- **Zeroed runs** fill the rest up to 0x288. +0x63, +0x10C and +0x11C are not written.

The family's methods reach none of these bytes (the post-effect page, section 3d). So the floats are typed from their stored bit
patterns (PROBABLE), and what they parameterise is not claimed.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PAtmosphericsBase `unobservedSpan0050` / `0062` / `00B0` / `00E4` | carved into 29 rows, with history in evidence | revised-here |
| `_types/types.tsv` PAtmosphericsBase ctor column | 00645520 | revised-here |
| `the-phyre-post-effect-class-family.md` §3d | the same finding (the methods reach only +0x60) | agrees |
