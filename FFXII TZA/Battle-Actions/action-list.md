---
title: "Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF138, 0x0031C5D0, 0x0031DBB1, 0x0031DBBE, 0x002F9860, 0x00305F10, 0x003093D0, 0x00320D70"
---

## What it lists

`action-list.tsv` holds one line for each of the 543 rows of the action table that registry slot `0x02EBF138`
reaches (`battle_pack.bin` directory entry `+0x3C`). Row *n* is action id *n*. What every field does, and the code
that reads it, is on [Action definition row](action-definition-row.md); this page is the shipped content.

By kind: 1 Attack, 81 magicks, 24 technicks, 51 items, 13 summons, 18 Quickenings, 235 Foecraft moves, 16 traps,
26 Esper attacks, 16 Concurrences, the six special rows 151 and 153-157 (`actstop`, `escape`, `escapestop` and three
Reserve rows), and 56 rows of kind 255. Of those 56, 47 are named `NOT USED` or Reserve; the other nine are named rows
with no linked id (`+0x22` = `0xFFFF`): `Do nothing.` (146), Mount (148), Dismount (149), `sousachange` (152), three
Mist Charge rows (242-244), Chain Bonus (245) and Dismiss (275).

The kind counts include rows named as unused: 24 of the 235 Foecraft rows are named Reserve and 8 of the 16
Concurrence rows `NOT USED`. With the 47 such rows of kind 255 and the three kind-13 Reserve rows, 82 rows in all
carry the explanation "an unused row".

### Where the values come from

Each line is read from the shipped `battle_pack.bin` in these steps:

1. the `st2e` table at entry `+0x3C`: 543 rows of 60 bytes from the section's `+0x20`;
2. the name word `+0x34` through the word banks at entry `+0xF8` (`0x00305F10`);
3. the help line `+0x00` (4000 for none) and the description `+0x2E` through the text groups, group `id / 1000` and
   row `id % 1000` as `0x002F9860` resolves them for `0x0031C5D0` (`0x0031DBB1`, `0x0031DBBE`);
4. every one-byte text code through the glyph table of the shipped `us` font `font00.dat` (records of `0x24` bytes
   from `+0x28`, key = byte - `0x20`, the glyph's UTF-8 at `+0x04`, as [Fonts](../Menus-And-HUD/fonts.md) describes);
   token `0x02` (line break) is written as a space;
5. element bits by the names on [Elements](../Damage-And-Battle-Formulas/elements.md), status bits by the names in
   [Statuses](../Status-Effects-And-KO/statuses.md)' table;
6. each flag word kept as hex, with beside it only the bits that have a named effect on
   [Action definition row](action-definition-row.md); `+0x2C` bits `0x1000` and `0x8000` take their names from
   [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) (`0x0030846A`, `0x003084B3`).

### Properties of the shipped rows

- The table's header gives 543 rows of 60 bytes, one TSV line each.
- The kind counts equal the shipped counts on [Action definition row](action-definition-row.md), "The kind byte".
- Example rows: row 0 Cure (kind 1, 8 MP, power 20, help "Restore a small amount of HP to one
  ally."), row 150 Attack (kind 0, help 4000, description "Attack with weapon in hand."), row 169 Steal (kind 2,
  linked id `0x400B`, cost 0, flags `0x00004688`, help "Steal from one foe.").

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the action id (the row) and its shipped name |
| `kind`, `kind_name` | `+0x1E` and its name from the kind table (`none` for 255) |
| `category` | `+0x1C`, which picks the presentation event |
| `linked_id` | `+0x22`, the magick, technick, item or ability id the row stands for |
| `cost` | `+0x0A`: MP, or Mist charges for summons and Quickenings |
| `b0B` | `+0x0B`, 1-3 on rows 182-207 only |
| `charge_base`, `power`, `power2`, `hit`, `recipe` | `+0x09`, `+0x10`, `+0x11`, `+0x12`, `+0x08` (0 = the weapon's recipe) |
| `element`, `status_chance`, `statuses`, `boost_percent` | `+0x13`, `+0x14`, `+0x18`, `+0x15` |
| `range_near_tenths`, `range_middle_tenths`, `reach_tenths` | `+0x02`, `+0x03`, `+0x05` |
| `area_radius`, `area_angle` | `+0x06`, `+0x07` (0 = the target alone) |
| `knockback` | `+0x04` |
| `enmity_direct`, `enmity_spread`, `enmity_others` | `+0x1D`, `+0x1F`, `+0x20` |
| `effect_class`, `effect_id`, `cinematic_id`, `event` | `+0x21`, `+0x24`, `+0x28`, `+0x30` |
| `esper` | summons: the Esper's party-table row `+0x26` |
| `menu_page`, `menu_row`, `ai_reaction` | `+0x38`, `+0x39`, `+0x3A` |
| `flags`, `flag_names` | `+0x0C` as hex and the bits with a named effect |
| `flags2`, `flag2_names` | `+0x2C` as hex and the bits with a named effect |
| `target_flags`, `target_flag_names` | `+0x36` as hex and the bits with a named effect |
| `help_id`, `help` | `+0x00` and its shipped line (4000 = none) |
| `desc_id`, `description` | `+0x2E` and its shipped line |
| `explanation` | a one-line summary built from the row's own fields: "an unused row" for the `NOT USED` and Reserve rows, "kind 255, no linked id" for the nine named kind-255 rows |

## Related

- [Action definition row: power, targeting, range, element and flag fields of a battle action](action-definition-row.md)
- [Equipment list: every weapon, shield, armor, accessory and ammunition row with its name, class, price, stats, elements, statuses and bonuses](../Items-Equipment-Shops-And-Licenses/equipment-list.md)
