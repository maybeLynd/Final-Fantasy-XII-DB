# SD-169: `+0x9C` is the VRAM-copy width (BITBLTBUF / TRXREG); `+0xA0` reaches no register (OPUS, 2026-09-30)

Register row SD-169 was registered by SWE2-DATA ([where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md),
the ruling on `022D8E10`). It asks which GS register, if any, the draw-surface cells `022D8EAC` (`+0x9C`) and
`022D8EB0` (`+0xA0`) correspond to. `00244200` shifts the `+0x9C` width right by 6 and packs it beside `0x333C`.

This record is static. The checker is `sd169_cells.py` (output `sd169_cells.out`, `FAILS 0`). GS register numbers are
the PS2 map the Legacy-PS2-GS pages use: `0x50` BITBLTBUF, `0x51` TRXPOS, `0x52` TRXREG, `0x53` TRXDIR.

## The answer (OPUS)

- **G1: boot values.** `0036D280` sets `+0x9C` = 512, `+0xA0` = 512, `022D8EB4` = 448 and `022D8EA8` = 0.
- **G2: `+0x9C` is the width of a local-to-local VRAM copy.** `00244200` builds a GIF A+D packet (tag
  `0x1000000000008007`: NLOOP 7, EOP, one A+D register per loop). It writes:
  - `0x50` **BITBLTBUF**:

    | field | value |
    |---|---|
    | SBP (source base) | `[022D8EA8] × [022D8EB4] × width >> 6` |
    | SBW (source width) | width >> 6 |
    | DBP (destination base) | `0x333C` |
    | DBW (destination width) | width >> 6 |

  - `0x51` **TRXPOS**, `0x52` **TRXREG** and `0x53` **TRXDIR** = 2 (local → local);
  - then further TRXPOS / TRXREG pairs whose TRXREG width is `+0x9C` and whose height is 16 lines.

  So `+0x9C` is the transfer width in pixels. It is the GS TRXREG width directly, and BITBLTBUF's source and
  destination widths after the `>> 6`. The `0x333C` beside it is the destination block. The same id is what `00244200`
  passes to `0039D0C0`, which looks up a 512 × 448 surface (`0x200`, `0x1C0`) by it.
- **G3: `+0xA0` reaches nothing.** ~~It has one writer (the boot `0036D280`) and one reader, `0036D2F0`.~~ It has one writer (the boot `0036D280`). Its one use is `0036D2F0`'s word
  read (`0036D342`), which passes it only to the bare `ret` `0016D6A0`. Three qword loads of `+0x9C` also load it as
  their high half: `00244224` (in `00244200`), `002443E7` (in `002443D0`) and `004FDDC7` (in `004FDDA0`). None of
  them uses that half. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd169-0930/REVIEW.md))* That reader
  passes it only as an argument to `0016D6A0`, the shared bare `ret`. It corresponds to no GS register and has no
  effect in this build: a PS2-era parameter left on a stubbed call.

**For modding:** the frame copy moves a `+0x9C`-pixel-wide band in 16-line strips into the `0x333C` block. Changing
`+0xA0` does nothing.

## Limits (OPUS)

- **The other packet fields.** The TRXPOS offsets and the packet's other values are read as registers, not traced to
  their sources.
- **The emulation.** What the emulated GS does with the transfer is not read (`0039D0C0` and the kick).
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
