---
title: "Augment list: every augment with its name, text, value, the code that reads the value, and its timer"
kind: "reference"
category: "Damage and battle formulas"
addresses: "02EBF040, 0031C5D0, 002FEF30, 002F95D0, 002F8410, 00387FD0, 0038DD20, 0038DF00, 0038E2D0, 0030EA40"
---

## What it lists

`augment-list.tsv` holds one line for each of the 129 rows of the augment table that registry slot `02EBF040`
reaches (`battle_pack.bin` directory entry `+0xEC`). Row *n* is augment id *n*, the id whose bit
[Augments](augments.md) sets in a unit's two effect layers.

- 89 rows carry a shipped name and 40 are named `NOT USED`. 19 of those 40 have no other text; three of the 19 are
  the timed effects 55-57.
- 77 rows have a non-zero value at `+0x04`. 63 are read by a function that picks the row by number, 3 are the
  default timers of the three timed effects, and 11 (the ten gambit-slot rows 104-113 and row 128) are read by no
  function, as the scope below states.

### How it is built

`Database/Tools/catalogues/augments.py`, with the shared readers in `ffxii_text.py`:

1. the `st2e` table at entry `+0xEC`: 129 rows of 8 bytes from the section's `+0x20`;
2. the name word `+0x02` through the word banks at entry `+0xF8`, and the text id `+0x00` through the text groups,
   both as `0031C5D0`'s class-29 arm reads them (`0031E494`-`0031E559`);
3. the reader of `+0x04` for each row, from the functions that load `02EBF040` (below);
4. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | textId | an extra text, through `002F9860`; 0 for none |
| `+0x02` | `u16` | nameWord | the name: bank 10, row = the augment id, on every row |
| `+0x04` | `u16` | value | the augment's number; its reader decides what it means (table below) |
| `+0x06` | `u8` | timerSlot | 3, 4 and 5 on ids 55-57, `0xFF` (no timer) on the others ([Battle buffs](../Status-Effects-And-KO/battle-buffs.md), `0030EA40`) |
| `+0x07` | `u8` | | 0 on every row |

The readers of `+0x04`:

| Rows | Reader | What the value does |
|---|---|---|
| 35, 42-47, 60-68 | `002FEF30` | added to Strength, [Stats](stats.md) (`002FF581`-`002FF77A`) |
| 19, 22, 24, 26, 69-73, 87, 97-102 | `002FEF30` | added to Magick Power, [Stats](stats.md) |
| 74-85 | `002FEF30` | added to max HP, [Stats](stats.md) |
| 91-93 | `002F95D0` | percent taken off a magick's MP cost ([MP](../Status-Effects-And-KO/mp.md)) |
| 94-96 | `002F8410` | percent taken off the charge time ([Action phases](../Battle-Actions/action-phases.md)) |
| 3, 88-90 | `00387FD0`, `00389370` | added to the shield-block chance ([Damage formula](damage-formula.md)) |
| 119-121 | `0038DD20` | added to 100 percent of the heal it computes (`02AEE054` × `02AEE058`), for each of the user's bits 119-121 set in the bitset at its third argument's `+0x1A` (`0038DD3A`-`0038DE0B`) |
| 122-124 | `0038DF00` | the same, for bits 122-124, into `02AEE010` (`0038DF1A`-`0038DFEB`) |
| 125-127 | `0038E2D0` | added to the action's power `+0x10` for bits 125-127, the percent of the target's max HP it restores, capped at 100 (`0038E335`-`0038E3F6`) |
| 55-57 | `00387020` | the default timer, value × 30 × the frame base `01DFE0B4`, which `0030EA40` and `0038FF20` store in the slot `+0x06` names |

### The scope of "read by no function"

Fifteen functions load `02EBF040` (111 references): `002FEF30`, `002F95D0`, `002F8410`, `00387FD0`,
`00389370`, `0038DD20`, `0038DF00`, `0038E2D0`, `0030EA40`, `00387020`, `00385570`, `0038FF20`, the query filler
`0031C5D0`, the validator `00322C50` and the loader `00236C30`.

- The first eight pick their rows by number and name only the rows in the table above.
- `0030EA40`, `00385570` and `0038FF20` take any id. `0030EA40` reads `+0x04` through `00387020` and `0038FF20`
  computes the same product inline (`0039005D`-`00390088`), both only for a slot `+0x06` below 8; `00385570` reads
  `+0x06` only.
- `0031C5D0` reads `+0x00` and `+0x02`.

So no function reads the value of rows 104-113 (1 each) or 128 (20).

### Checks

- The table's header gives 129 rows of 8 bytes, and the TSV has 129 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts byte `+0x07` = 0, the name word = bank 10, row *n*, and that only ids 55-57 have a timer
  slot.
- Rows compared with their readers: row 74 "Increases max HP by 30." has value 30, the bonus [Stats](stats.md)
  lists for it; rows 94-96 have value 12, the percentage `002F8410` sums for "Reduces action time by 10%";
  rows 55-57 have slots 3, 4 and 5 and value 120, the two minutes [Battle buffs](../Status-Effects-And-KO/battle-buffs.md)
  states.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the augment id (the row) and its shipped name |
| `text_id`, `text` | `+0x00` and its shipped text; empty for 0 |
| `value` | `+0x04` |
| `value_reader`, `value_use` | the function that reads this row's value and what it does with it; empty when none does |
| `timer_slot` | `+0x06`; empty for `0xFF` |
| `explanation` | a one-line summary: the name (or the extra text when the name is `NOT USED`), the value and its use |

## Related

- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](augments.md)
- [Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps](stats.md)
- [Battle buffs: what Battle Cry, Enrage, Magick Barrier, Perfect Defense and the other enemy abilities switch on, and how long they last](../Status-Effects-And-KO/battle-buffs.md)
