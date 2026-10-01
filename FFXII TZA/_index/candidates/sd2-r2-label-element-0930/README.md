# SD-2: the R2 label widget draws the word FLEEING, letter by letter (OPUS, 2026-09-30)

Register row SD-2 was registered by SWE2-DATA ([r2-force-fight-toggle.md](../../../15-Input/Modal-Toggles/r2-force-fight-toggle.md)
section 7). It asks which element of `battle_4_c` the R2 label widget `00366B80` draws, and whether it is the
`FLEEING` text.

The checker is `sd2_check.py` (output `sd2_check.out`, `FAILS 0`). The evidence is of three kinds:

- **W1–W4 are static**, read from the certified image.
- **D1–D3 read the shipped data** (us language). D3 writes `battle_4_c-letters.png`, a crop of the atlas's letter
  cells.
- **The letter reading is by eye**, from that crop.

## The answer (OPUS)

**Yes: the widget draws `FLEEING`, and it draws the word rather than one element.**

- **W1: what it binds.** The construct arm binds layout record `0xC` of the package at `[0209AC30]+8` through
  `002432B0`, and looks up its atlas through the name pointer `[01E0C1E8]` = `battle_4_c`.
- **W2: where the binder puts it.** `002432B0` stores the record at widget `+0x58` and an item pointer array at
  `+0x60`.
- **W3: what it draws.** The draw arm walks the items while the index is below the record's `+0xC`. It reveals item
  *i* once the toggle block's counter, shifted left by 8, passes *i* × (threshold `022CBE08` × 128) / (`+0xC` + 1).
  **So the letters appear one after another while R2 is held**, in step with the arming counter §2g measured.
- **W4: which image.** `battle_4_c` is `tex2pack_ys` directory entry 0: the loader registers slot `+0x338` from
  `[01E0C1E8]`, and the binder binds slot `+0x338` to directory offset 0.
- **D1: the record.** Record 12 of `mrppack_ys` unit 1 (us) has 12 items. Its `+0xC` is 7, so the widget draws the
  first seven.
- **D2: the drawn items.** All seven are type-2 items in `battle_4_c`, each 46 × 42 at y 14 and x 390…597. Their
  cells are `0 1 2 2 5 6 7`.
- **D3: the letters.** `battle_4_c` (1024 × 512, 8-bit indexed) carries eight letter cells in rows of three at its
  lower left: **F L E / A P I / N G**. Read row-major, cells `0 1 2 2 5 6 7` are **F L E E I N G**. The repeated E
  falls on the repeated cell 2.

This agrees with EXP-025, which saw `FLEEING` with the flag at 0, and with FM-1's reading that the label follows the
toggle state. It also explains why the label starts during arming: its letters are paced by the arming counter.

## Limits (OPUS)

- **The cell-to-rectangle mapping is inferred.** That cell *n* is the *n*-th letter cell read row-major is inferred
  from the crop and the matching repeats. The item → atlas-rectangle table was not decoded.
- **Items 7–11 are not drawn by this widget** (cells `6 1 7 8 9`), and what they serve is not read.
- **Only us is checked.** Other languages carry 12 (de, es, fr, it) or 8 (ch, cn, in, in_sdver, kr) items in the
  same record; their `+0xC` values and atlases were not checked.
- **W4's package slot comes from a generator, not from this record's own read.** That `[0209AC30]+8` is unit 1
  (`00280980` fills 8-byte slots from unit 0) is taken from
  [`gen_atlas_name_census.py`](../../../02-Resource-And-Asset-Pipeline/members/gen_atlas_name_census.py)'s documented
  static read.
