# SD-140: the kind-`0x54` `+0x28` entries are per-corner vertex colours and `+0x2C` are per-corner texture coordinates (SWE2-ORACLE, 2026-09-30)

Register row SD-140 asks two things:

- what the vertex-prep byte kernel does to a kind-`0x54` record's `+0x28` entries with the `+0x40` block;
- how the three draw paths pack `+0x28` / `+0x2C` into the emitted vertex, which decides whether they are colours and
  texture coordinates.

The page is [effect-mesh-records-kind-54.md](../../../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md)
section 8. DATA's consumer checks are `dd-data-4-0930/fx54_consumers.py`.

**On screen:** a type-`0x05` effect mesh (for example a spell's glow shell) gets its tint from these bytes. Each corner
of each triangle or quad carries its own colour and its own texture position. The effect's current colour scales that
tint, and a second mesh can cross-fade it. The same four bytes then reach the GPU as the corner's vertex colour. The two
floats become the corner's texture coordinate, shifted by a per-pass scroll.

The checker is `sd140_kernel.py`. Its output is `sd140_kernel.out`, which ends `FAILS 0` (23 checks). It uses three
instruments:

- **Static.** `txt(addr)` compares the exact capstone text at every cited site. `ripref(addr)` resolves rip-relative
  targets.
- **Census.** The published kind-`0x54` census TSV (`effect-mesh-54-records.tsv`, 2,252 records) is an authored-data
  control.
- **Execution.** `sd140_emu.py` runs shipped bodies in Unicorn. The image is mapped at its own base, and the PS2
  register bank `022D8F10..` and the globals are the image's own BSS. Each E-check compares the native result with a
  Python model over seeded random trials. **The model is the claim and the native run is the control.**

The instrument is not vacuous:

- E1 and E3 also score rival models against the same native outputs. They reject `e·c >> 8`, `e·c / 255` and the
  unbiased lerp, which miss 2,850, 2,850 and 842 bytes.
- The first draft of the `00432CC0` model (all four lanes scaled) missed 611 of 804 bytes against the native code. It
  was corrected from the code.
- Five hand mutations of the checker were each caught:
  - the kernel shift;
  - the lerp bias;
  - the colour scale;
  - the bit-4 branch;
  - the census corner formula.

## The staging buffer (SWE2-ORACLE)

Both consumers and all three draw paths address one staging buffer at `[02AEED50]` the same way (A1, A3):

| region | offset from `[02AEED50]` | per entry |
|---|---|---|
| `+0x24` vectors copy | `0` | 16 B × `c16` |
| lit per-normal table (written by `00394E50`/`003952D0`/`003954E0`/`00395050`) | `16·c16` | 16 B × `c16` |
| screen vertices (GS XYZ: u16 X, u16 Y in 12.4, 24-bit Z, per `0039CDC0`), from `0039A150` | `32·c16` | 16 B × `c14` |
| **prepared colour** (the kernel's output) | `32·c16 + 16·c14` | 4 B × `c18` |
| per-pass colour | colour `+ 4·c18` | 4 B × `c18` |
| **UV** (`+0x2C` copy or blend) | colour `+ 8·c18` | 8 B × `c18` |
| per-pass UV | UV `+ 8·c18` | 8 B × `c18` |
| per-position `Q` (`0039A150`'s `r8` output) | UV `+ 16·c18` | 4 B |

The census gives the key count relation (C1): **`c18 = c1A = 3·tri + 4·quad` in all 2,252 records.** The `+0x28` and
`+0x2C` arrays hold one entry per primitive corner, and the draw loops consume them by a running corner number
(`+3` per triangle, `+4` per quad; A5, A6). They are not indexed through `+0x170`. Positions go through `+0x170`,
normals through `+0x174`, and colour and UV are per corner.

## The byte kernel `00432300` (SWE2-ORACLE)

The consumer `00435050` makes the call `00432300(rcx = rec +0x28, rdx = param + 0x40, r8 = prepared colour, r9d = c18)`
(A1).

**Formula, execution-proven** (E1, 2,912 bytes, no stubs):

```text
out[i].byte[c] = min(255, (rec28[i].byte[c] * param40.byte[c]) >> 7)      c = 0..3
```

- **This is the PS2 colour modulate, where `0x80` = 1.0.** `0x80808080` is the exact identity (E2). The draw paths skip
  the per-pass call when the pass colour is `0x80808080` (A4). The census reports `0x80808080` as 47 % of shipped `+0x28`
  entries.
- **Only the first dword of the `+0x40` block is read** (E2): one RGBA8 colour, not a block.
- **It reads `n + 1` source entries** (E2). The extra read is a one-past-the-end prefetch whose value is unused.
- **Count 0 still writes one entry** (a do-while loop, E2). No consumer reaches this, because `c18 ≥ 1` in every record
  (C2).

**The operand is the draw parameter block's `+0x40`.** The page calls it "the element's `+0x40`", but it is the `rdx` of
`004355D0`: the block at `[01FD4A78] + 0x800`, whose `+0x40` is written by `0026EE00` from the element instance's `+0x240`
(X4, static). `0026EE00` itself was not decoded.

### The two-mesh path `00434CD0` (SWE2-ORACLE)

When the walk blends toward a next mesh (`+0x1E8`), `00434CD0` runs (A2):

- **`+0x1F1` bit 4 set:** it calls the kernel on the current record's own `+0x28`, with no blend.
- **Bit 4 clear:** it calls `00433830(cur +0x28, next +0x28, out, c18, t = 1 − w)`, where `w = param +0x1EC`. It then
  runs the kernel in place.

**`00433830`, execution-proven** (E3, 2,396 bytes, no stubs):

```text
out.byte[c] = trunc(a.byte[c]·t + 0.5 + b.byte[c]·(1 − t))
```

With A2's operands this is `round(cur·(1 − w) + next·w)`. It is the same `cur·(1 − t) + next·t` convention as the
position lerp `00431F10`, with round-half-up in float32.

## Per pass, the draw paths re-colour (SWE2-ORACLE)

For each of the `param +0x1F0` passes `p`, the three paths `004355D0` (inline), `00437130` and `00438860` run the same
stage (A4). The colour anchors are static. The `00432CC0` arithmetic is execution-proven (E4).

1. **Flat colour.** If byte `param +0x1A8+p` is non-zero, the kernel computes one colour, `param+0x40 × param+0x138+4p`,
   and broadcasts it to all `c18` corners.
2. **Per corner.** Otherwise, if `param +0x138+4p ≠ 0x80808080`, the kernel computes `prepared × pass colour` into the
   per-pass colour region. Otherwise that region aliases the prepared colour.
3. **Alpha.** If byte `param +0x1A4+p` is non-zero, `00432CC0(src, dst, lit, +0x174 list, c18, c16)` runs. **RGB is
   copied, and `alpha = trunc(alpha · L[n].w) mod 256`**, where `L` is the lit per-normal table and `n` is the corner's
   `+0x174` normal index reduced mod `c16`. Entry 0 uses its index unreduced (Q1); shipped normal indices are below
   `c16` anyway. What the lighting routines put in `L.w` was not read.

## How the three draw paths pack `+0x28` / `+0x2C` (SWE2-ORACLE)

All three paths call the same builder family, and `00438860` adds four n-gon builders for clipped polygons. Byte
`param +0x130+p` picks the pass mode (A5, A6):

- **5:** untextured.
- **1:** textured, with the texture slot at `param + 16·(+0x188 primitive byte + 11)`.
- **Anything else:** textured, with the per-pass slot `param + 0x70 + 16p`.

`02AEE900` (byte `param +0x134+p`) picks the ordered builders (those with a sort key and the `02F8F2F8` slot) over the
unordered ones.

| builders (execution, E6) | colour (4 B per corner in) | `+0x2C` (UV per corner in) |
|---|---|---|
| `0039E820` / `0039EC30` / `0039E6B0` / `0039EA70` (tri / quad, untextured) | lane `c` of the vertex colour slot = `float(byte c)`, **unscaled 0..255**, 16 B per vertex | not taken |
| `0039F4B0` / `0039F9F0` / `0039F2B0` / `0039F780` (tri / quad, textured) | the same | `U = S/Q`, `V = T/Q` into the vertex UV slot (16 B stride) |
| `0043D8F0` / `0043E440` (n-gon, untextured; `00438860` clip path) | the same | not taken |
| `0043DB90` / `0043DF80` (n-gon, textured; clip path) | the same | `S/Q`, `T/Q` |

**The UV route, execution-proven** (E5, E7):

- `0039B840` / `0039B860` compute `S = (u + ou)·Q` and `T = (v + ov)·Q` per corner. This is the GS STQ form. `(ou, ov)`
  is the pass's float pair `param +0x50+8p`, and `Q` is the corner's per-position value.
- The textured builder divides back.
- **The emitted UV is the prepared `+0x2C` pair plus the pass offset**, to float round-trip precision (max error
  2.4e-7).
- It is never scaled to texels.

Between the copy and the ST step, a pass may replace or transform the pairs. Pass byte `+0x1AC+p` selects
`0043E7B0` / `00434630` / `00434760`, byte `+0x1B0+p` selects a regeneration from the lit normal table or the screen positions (`00396F20`, `00394B70`), and `param +0x1F2` bits 0–1 select
`0043E840`. Those operators were not characterised.

**The clip path in `00438860`** (A7, E8) applies when a projected corner comes back zero:

- **Colour** travels as `float(byte)` in the clip vertex (`00431D30`, then `+0x10`) and comes back as bytes by truncation
  of the low byte (`003AFDD0`, no clamp).
- **The UV pair** travels as the clip vertex's `+0x20` qword.
- The clipper `00521450` itself was not executed. That it interpolates both linearly is inference.

**Answer.** `+0x28` is a per-corner RGBA8 vertex colour on the GS `0x80` = 1.0 scale. `+0x2C` is a per-corner float
texture coordinate.

## What is proven how (SWE2-ORACLE)

| claim | class |
|---|---|
| kernel formula, identity, operand extent, count semantics; blend formula; `00432CC0` alpha rule; ST form; builder byte→float and S/Q packing; the ST→UV chain; clip colour carriers | **execution** (E1–E8, Q1); stubs only in E6/E7 (below) |
| which arrays each call receives, the bit-4 / pass / mode selection, the per-corner running index, the staging offsets, the parameter-block identity | **static read** (A1–A7, X4) |
| one entry per corner (`c18 = 3·tri + 4·quad`), `c18 ≥ 1` | **census** (C1, C2) |
| byte order R, G, B, A (byte 3 = alpha); `Q` = the projection's 1/w-like value; the backend treats the colour slot as vertex colour and the UV slot as the texture coordinate; the clipper interpolates linearly | **inference**. Alpha at byte 3 rests on the GS RGBAQ layout, on byte 3 being dominated by `0x80` in the census, and on `00432CC0` touching only byte 3. |

**Stubs in E6/E7:** `0020E680` (returns a context), `008642A0` (returns a primitive whose `+0/+8/+0x10` are three 16 B
arrays, the layout `00864210` allocates), `00864D10` (a 0x100-byte quad object; vertices at `+0`, UV at `+0x40`, colour at
`+0x80`, as `0039F9F0` addresses it), `0039CDC0` (the GS-XYZ-to-float vertex conversion, not measured), and `0020E670`,
`0020E630`, `00182F50` (return), and `0024E460` / `003A3D20` / `003A2C70` (return 0). **No stub writes the UV or colour
arrays the checks read.** E1–E5, E8 and Q1 run with no stubs at all.

## What stays narrowed (SWE2-ORACLE)

- **The per-pass UV operators are not characterised:** `0043E840`, `0043E7B0`, `00434630`, `00434760`, the
  normal-driven regenerators (`00396560`, `00396A30`, `003962F0`, `00394B70`, `00395CF0`, `00395780`) and the
  `1/1.15`, `×1.15`, `+0.5` pass-offset rewrite at `00435CC5`–`00435DA2`.
- **The lighting routines that fill `L` are not read**, so what `L.w` means (for example a rim or fresnel factor) is open.
- **`0026EE00`**, which fills `param +0x40` from instance `+0x240`, is not decoded.
- **The draw backend after the builders is not read:** what consumes the primitive's colour and UV slots, and the
  material at `+0x30` / `+0xD8`. So "vertex colour" and "texture coordinate" name the slots by the GS STQ / RGBAQ form
  and by the texture operand. The GPU-side use is not measured.
- **The `00521450` clipper was not executed.**
- **No authored effect was driven end to end.** The executions are per function, not a whole `004355D0` frame.

## Contradictions with published text (reported to OPUS, not edited) (SWE2-ORACLE)

- **X1.** [the-two-transform-primitives.md](../../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md),
  "The `00434CD0` exclusive subtree", says bit 4 sends `+0x28` through `00433830`, bit 5 sends `+0x2C` through `004344C0`
  (clear → copy), and bit 6 sends `+0x24` through `00432030` (clear → copy). **All three polarities are inverted.** Each
  blend runs when the bit is **clear**; a set bit selects the copy (or, for bit 4, the unblended kernel).
- **X2.** The same page calls `00432300` "pure staging … no external calls". It has no calls, but it is the modulate
  kernel and stores one packed dword per entry.
- **X3.** The same page describes `0043DB90` and `0043E440` as record-walk "field math" helpers and `0043D8F0` as an
  authored-number channel converter. All three, and `0043DF80`, are n-gon primitive builders for `00438860`'s clipped
  polygons.
- **X4 (precision).** Page §8 says "the element's `+0x40` block". It is the draw parameter block's `+0x40` colour (one
  dword).
- **§8 precision.** The table row for `00434CD0` says `+0x28` is "blended per channel, then the same byte kernel". That
  holds only when `+0x1F1` bit 4 is clear; when it is set, the record's own `+0x28` goes straight to the kernel.
- **§22.5 BI-3a (the-largest-unclassified-functions.md) precision.** It reads the `00435CE3`–`00435DA2` block as "a float
  pair scaled by 1.15 and offset by 0.5 over a `+0x1A`-counted array". The 1.15 / 0.5 arithmetic is on the single pass
  offset pair `param +0x50+8p`. The `+0x1A`-counted array is processed by `0043E840`.

## Files (SWE2-ORACLE)

- `sd140_kernel.py`: the checker (S, A1–A7, C1–C2, E1–E8, Q1, X1–X4).
- `sd140_kernel.out`: its output, ending `FAILS 0`.
- `sd140_emu.py`: the Unicorn harness (image mapping, disclosed stubs, read watch).

Reproduce with `python -B sd140_kernel.py`. It needs `unicorn`, `pefile`, `numpy` and capstone through `retool.py`, and
the certified image at `Database/Tools/work/exe/FFXII_TZA.exe`.
