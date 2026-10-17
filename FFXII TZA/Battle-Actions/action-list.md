---
title: "Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts"
kind: "reference"
category: "Battle actions"
addresses: "02EBF138, 0031C5D0, 0031DBB1, 0031DBBE, 002F9860, 00305F10, 003093D0, 00320D70"
---

## What it lists

`action-list.tsv` holds one line for each of the 543 rows of the action table that registry slot `02EBF138`
reaches (`battle_pack.bin` directory entry `+3C`<sub>h</sub>). Row *n* is action id *n*. What every field does, and the code
that reads it, is on [Action definition row](action-definition-row.md); this page is the shipped content.

By kind: 1 Attack, 81 magicks, 24 technicks, 51 items, 13 summons, 18 Quickenings, 235 Foecraft moves, 16 traps,
26 Esper attacks, 16 Concurrences, the six special rows 151 and 153-157 (`actstop`, `escape`, `escapestop` and three
Reserve rows), and 56 rows of kind 255. Of those 56, 47 are named `NOT USED` or Reserve; the other nine are named rows
with no linked id (`+22`<sub>h</sub> = `FFFF`<sub>h</sub>): `Do nothing.` (146), Mount (148), Dismount (149), `sousachange` (152), three
Mist Charge rows (242-244), Chain Bonus (245) and Dismiss (275).

### How it is built

`Database/Tools/catalogues/actions.py`, with the shared readers in `ffxii_text.py`:

1. the `st2e` table at entry `+3C`<sub>h</sub>: 543 rows of 60 bytes from the section's `+20`<sub>h</sub>;
2. the name word `+34`<sub>h</sub> through the word banks at entry `+F8`<sub>h</sub> (`00305F10`);
3. the help line `+00`<sub>h</sub> (4000 for none) and the description `+2E`<sub>h</sub> through the text groups, group `id / 1000` and
   row `id % 1000` as `002F9860` resolves them for `0031C5D0` (`0031DBB1`, `0031DBBE`);
4. every one-byte text code through the glyph table of the shipped `us` font `font00.dat` (records of `24`<sub>h</sub> bytes
   from `+28`<sub>h</sub>, key = byte - `20`<sub>h</sub>, the glyph's UTF-8 at `+04`<sub>h</sub>, as [Fonts](../Menus-And-HUD/fonts.md) describes);
   token `02`<sub>h</sub> (line break) is written as a space;
5. element bits by the names on [Elements](../Damage-And-Battle-Formulas/elements.md), status bits by the names in
   [Statuses](../Status-Effects-And-KO/statuses.md)' table;
6. each flag word kept as hex, with beside it only the bits that have a named effect on
   [Action definition row](action-definition-row.md); `+2C`<sub>h</sub> bits 12 and 15 take their names from
   [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) (`0030846A`, `003084B3`).

### Checks

- The table's header gives 543 rows of 60 bytes, and the TSV has 543 data lines.
- Two runs over the same files give byte-identical output.
- The kind counts equal the shipped counts on [Action definition row](action-definition-row.md), "The kind byte".
- Rows compared with their readers: row 0 Cure (kind 1, 8 MP, power 20, help "Restore a small amount of HP to one
  ally."), row 150 Attack (kind 0, help 4000, description "Attack with weapon in hand."), row 169 Steal (kind 2,
  linked id `400B`<sub>h</sub>, cost 0, flags `00004688`<sub>h</sub>, help "Steal from one foe.").
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name` | the action id (the row) and its shipped name |
| `kind`, `kind_name` | `+1E`<sub>h</sub> and its name from the kind table (`none` for 255) |
| `category` | `+1C`<sub>h</sub>, which picks the presentation event |
| `linked_id` | `+22`<sub>h</sub>, the magick, technick, item or ability id the row stands for |
| `cost` | `+0A`<sub>h</sub>: MP, or Mist charges for summons and Quickenings |
| `b0B` | `+0B`<sub>h</sub>, 1-3 on rows 182-207 only |
| `charge_base`, `power`, `power2`, `hit`, `recipe` | `+09`<sub>h</sub>, `+10`<sub>h</sub>, `+11`<sub>h</sub>, `+12`<sub>h</sub>, `+08`<sub>h</sub> (0 = the weapon's recipe) |
| `element`, `status_chance`, `statuses`, `boost_percent` | `+13`<sub>h</sub>, `+14`<sub>h</sub>, `+18`<sub>h</sub>, `+15`<sub>h</sub> |
| `range_near_tenths`, `range_middle_tenths`, `reach_tenths` | `+02`<sub>h</sub>, `+03`<sub>h</sub>, `+05`<sub>h</sub> |
| `area_radius`, `area_angle` | `+06`<sub>h</sub>, `+07`<sub>h</sub> (0 = the target alone) |
| `knockback` | `+04`<sub>h</sub> |
| `enmity_direct`, `enmity_spread`, `enmity_others` | `+1D`<sub>h</sub>, `+1F`<sub>h</sub>, `+20`<sub>h</sub> |
| `effect_class`, `effect_id`, `cinematic_id`, `event` | `+21`<sub>h</sub>, `+24`<sub>h</sub>, `+28`<sub>h</sub>, `+30`<sub>h</sub> |
| `esper` | summons: the Esper's party-table row `+26`<sub>h</sub> |
| `menu_page`, `menu_row`, `ai_reaction` | `+38`<sub>h</sub>, `+39`<sub>h</sub>, `+3A`<sub>h</sub> |
| `flags`, `flag_names` | `+0C`<sub>h</sub> as hex and the bits with a named effect |
| `flags2`, `flag2_names` | `+2C`<sub>h</sub> as hex and the bits with a named effect |
| `target_flags`, `target_flag_names` | `+36`<sub>h</sub> as hex and the bits with a named effect |
| `help_id`, `help` | `+00`<sub>h</sub> and its shipped line (4000 = none) |
| `desc_id`, `description` | `+2E`<sub>h</sub> and its shipped line |
| `explanation` | a one-line summary built from the row's own fields: "an unused row" for the `NOT USED` and Reserve rows, "kind 255, no linked id" for the nine named kind-255 rows |

## Related

- [Action definition row: power, targeting, range, element and flag fields of a battle action](action-definition-row.md)
- [Equipment list: every weapon, shield, armor, accessory and ammunition row with its name, class, price, stats, elements, statuses and bonuses](../Items-Equipment-Shops-And-Licenses/equipment-list.md)
