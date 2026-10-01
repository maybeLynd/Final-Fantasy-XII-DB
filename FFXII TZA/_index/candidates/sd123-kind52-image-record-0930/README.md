# SD-123: effect record kind `0x52` is the effect container's ~~paletted image (texture) record~~ image (texture) record: 4- or 8-bit indexed with one palette, or 4-byte-per-pixel direct colour (OPUS, 2026-09-30)

*(Title, answer, I2, I3 and the modding line narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd123-0930/REVIEW.md); the register row's summary is proposed for OPUS in [swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md).)*

Register row SD-123 was registered by SWE2-DATA ([the-largest-unclassified-functions.md](../../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md)
section 22.5). It asks what effect record kind `0x52` is: the kind-`0x54` mesh record's `+0x184` handles, and the
first child list of the kind-`0x50` group record. The kind census counts 13,161 kind-`0x52` records.

This record is static. The checker is `sd123_kind52.py` (output `sd123_kind52.out`, `FAILS 0`). It reads the kind's
loader `00500C00`, named in [effect-element-type-dispatch.md](../../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md)'s
record-store table (node `0x1D0`, destroy `00500AA0`).

## The answer (OPUS)

~~**A kind-`0x52` record is a CLUT-paletted image: a format, N palettes and a size, from which the loader creates the
palettes and the image surface.**~~

A kind-`0x52` record is an image: a format, a palette count and a size. The loader masks the format to 6 bits
(`00500C39`; bit 7 is kept at `+0x1CA`, bit 6 at `+0x1C8`). Format 0 is 4-bit indexed (64-byte palettes, w·h/2
pixel bytes), format 1 is 8-bit indexed (1,024-byte palettes, w·h), and formats 2 / 3 / 4 are 2 / 3 / 4 bytes per
pixel with no palette. A palette count above 0 with any format other than 0 / 1 fails the load.

- **I1: the header.**
  - Format byte → `+0xA0` (low 6 bits; `0xFF` = no image), with its bit 6 → `+0x1C8` and bit 7 → `+0x1CA`.
  - Palette count → `+0xA2`.
  - Two size pairs: `+0xA8`/`+0xAA`, copied to `+0xA4`/`+0xA6`, and `+0x1CC`/`+0x1CE`.
- **I2: the palettes.**
  - Format 1 ~~(or `0x81`)~~ takes 1,024-byte palettes (count << 10: 256 colours × 4 bytes). Format 0 ~~(or `0x80`)~~ takes
    64-byte palettes (count << 6: 16 colours × 4). Any other format fails the load. File bytes with bit 7 or 6 set
    select the same palettes through the mask. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd123-0930/REVIEW.md))*
  - ~~Each palette goes through the CLUT submit `001837A0` and `00183760`, and the two handles are stored at
    `+0xC8 + 8i` and `+0x148 + 8i`.~~ Each palette's data goes through `001837A0` (+0xC8 + 8i); `00183760` makes a same-size handle with
    no data (+0x148 + 8i). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd123-0930/REVIEW.md))*
  - That matches the 8-bit / 4-bit indexed-texture pair (PSMT8 / PSMT4) the PS2 image pages describe.
- **I3: the image.** The size pairs are tested against their power-of-two ceilings (`0017FEA0`). ~~The surface is then
  created through the render-layer calls (`00183EE0`, `00184140`, `00184130`, `00184370`, `00183A00`, `00183C60`,
  `00183EB0`), sized by `+0xA8` × `+0xAA`.~~ The live surface calls are `00183EE0` / `00184140` / `00183A00` / `00183C60` / `00183EB0`; `00184130` /
  `00184370` are the unreachable 0x80 / 0x81 arms. The surface is sized by `+0xA4` × `+0xA6` (copies of `+0xA8` /
  `+0xAA`). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd123-0930/REVIEW.md); `sd123_kind52.py` still pins `00500CF1` and `00500FA4` / `00500FB4`, which sit in the dead arms))*
- **I4: who uses them.**
  - The mesh record (kind `0x54`) resolves its `+0x1C` ids as kind-`0x52` handles (`003AA280` with `edx = 0x52`) into
    its `+0x184` array.
  - The evaluator `00431830` follows an element's `+0xB0` mesh to handle 0 and reads that record's `+0x10`.
  - So an effect mesh carries a small list of textures. Being the group record's first child list places them in
    the container's own record set, as §22.5 already observed.

**For modding:** ~~the 13,161 kind-`0x52` records are the effect containers' textures: indexed images with 16- or
256-colour palettes.~~ the 16,862 kind-`0x52` records over every EFX stream (13,161 in the .efx / .efb-only
walk) are the effect containers' textures: 11,076 indexed (1,131 with 16 colours, 9,945 with 256, one palette each)
and 5,786 direct colour at 4 bytes per pixel. No shipped record uses formats 2 or 3. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd123-0930/REVIEW.md))* Replacing an effect's look means replacing these.

## Limits (OPUS)

- **Bits 6 and 7 of the format byte** (`+0x1C8`, `+0x1CA`) are not read for meaning.
- **The second size pair** `+0x1CC`/`+0x1CE` is not named.
- **The record's `+0x10`** (what `00431830` reads) is not named.
- **`+0x188`.** That the mesh's one byte per primitive selects the texture slot is a reading, not traced here.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
