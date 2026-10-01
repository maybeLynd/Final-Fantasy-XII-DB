# SD-102: the two glyph emitters build PS2 VIF/GIF packets and mirror the state into the draw context (OPUS, 2026-09-30)

Register row SD-102 was registered by SWE2-DATA ([the-widget-tree-draw-pass.md](../../../99-Unresolved-Residual/the-widget-tree-draw-pass.md)
section 9). It asks what the two glyph emitters `002DAF30` and `002DAC70` put in their render commands.

This record is static. The checker is `sd102_emitters.py` (output `sd102_emitters.out`, `FAILS 0`). The GIF and VIF
field layouts are the PS2 hardware formats. The database's Legacy-PS2-GS pages decode them the same way
(`17-Presentation-Rendering/Legacy-PS2-GS/members/gen_gif_tags.py`, the GIF tag field split).

## `002DAC70`: the state packet (OPUS)

- **E4: it first closes the open chunk.** At the chunk's start `+0x18` / `+0x1C` it writes:
  - VIF `FLUSHE` (`0x10000000`);
  - `UNPACK V4-32`, with the FLG bit, VU address 0 and NUM = the chunk's quadwords after its 0x20-byte header.

  A chunk holding only the 7-quadword minimum is sealed and kicked at once (`0016D6A0`, `003A1DB0`).
- **E5: then it opens a new chunk.** It writes `FLUSHE` + `UNPACK V4-32` NUM 6 to VU address `0x100`, a GIF tag
  (NLOOP 5, NREG 1, REGS = A+D) and five A+D register writes:

  | GS register | value |
  |---|---|
  | `TEX0_1` (`0x06`), plus `TEX2_1` (`0x16`) for a 4-bit texture | the texture record's `+0x30` qword (E6) |
  | `0x7F` | 0 (not a documented GS register; the payload is 0) |
  | `TEX1_1` (`0x14`) | 0 |
  | `TEST_1` (`0x47`) | the argument's `+0x80` |
  | `ALPHA_1` (`0x42`) | the argument's `+0x78` |

- **E6: the texture word.** The PSM field sits at the record's `+0x38`, bits 8–13.
  - **PSM `0x14` (PSMT4).** PSM is rewritten to `0x13` (bits 20–25) and CBP (bit 37) gains 4 × flags[7:4]. A `TEX2_1`
    write then carries CSA = flags[3:0] (bit 56).
  - **PSM `0x13` (PSMT8).** CBP gains a flag-derived offset.
  - **Flag bit 16.** The record's TEX0 is used with fixed CLUT bits (`0x6878000000000`).
- **E7: the call.**
  - `002DD350` appends VIF `MSCAL` (command `0x14`) at microprogram address `02EBB764 >> 3`, then seals and kicks the
    chunk.
  - `002DAC70` then sets **the same state on the draw context `[01F811E8]`** (`001B1C00`):
    - `001819A0`: the texture, with the width/height words of the record's `+0x20` object, the palette byte and a
      flag;
    - `00181910`: the TEST word, then to `001B22E0`;
    - `001816B0`: the ALPHA word, then to `001B22D0`;
    - `00181330`, then to `001B03D0`.

## `002DAF30`: the quad packet (OPUS)

- **E1: the data.** It opens a chunk on the packet row `02EBEFC0 + 24 × [02EBEFF0]` (buffer `+0x20`, leaving the
  header `002DAC70` patches), then writes:
  - 64 bytes from its argument, a 4 × 4 also kept at `022D8F30`..`022D8F6F`;
  - an A+D pair, `TEX1_1` = `[arg+0x88]`;
  - four ints: word `+0x5A` three times, then word `+0x58`.
- **E2: the GIF tag.**
  - `0xD000400000000001 | PRIM << 47`: NLOOP 1, PRE, PACKED, NREG 13, REGS `0x431431431431E` = A+D, then
    (RGBAQ, UV, XYZF2) four times.
  - PRIM is `0x15C` (TRISTRIP, Gouraud, textured, alpha-blended, UV coordinates) when the third argument is non-zero,
    else `0x154` (the same, flat).
  - So each call is **one textured, blended four-vertex strip, a glyph quad**. Its register list is a template that
    the VU1 program completes, which is the pattern the Legacy-PS2-GS pages document for these packets.
- **E3: the same values go to the draw context.** `00181560` → `001B1910`; `001816F0` with the same four ints
  (`+0x5A`, `+0x5A`, `+0x5A`, `+0x58`) → `001B1F80`; `00181870(3)` → `001B2490`.

**For modding:** every glyph is drawn twice over, as a legacy PS2 packet for the emulated VU1 path and as state and
draw calls on the PC draw context. Both carry the same TEX / TEST / ALPHA words and the same four ints, so a text
colour or blend change has to reach both.

## Limits (OPUS)

- **Register `0x7F`.** Its meaning in this emulation is not established (payload 0).
- **The four ints.** Their reading as a colour (three equal components and a fourth) comes from their shape and
  their use in both paths, and is not proven.
- **What the VU1 microprogram at `02EBB764` does** with the unpacked cells is not read here.
- **The downstream bodies.** `001B1910`, `001B1F80`, `001B2490`, `001B22D0`, `001B22E0` and `001B03D0` are named,
  not read.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
