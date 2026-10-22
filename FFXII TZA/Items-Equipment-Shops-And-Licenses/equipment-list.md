---
title: "Equipment list: every weapon, shield, armor, accessory and ammunition row with its name, class, price, stats, elements, statuses and bonuses"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF0F8, 0x0031C5D0, 0x0031C911, 0x0031C981, 0x002FEF30, 0x0031E9F0, 0x00388409, 0x0038BE30"
---

## What it lists

`equipment-list.tsv` holds one line for each of the 557 rows of the equipment table that registry slot `0x02EBF0F8`
reaches (`battle_pack.bin` directory entry `+0x38`). The meaning of every field, and the code that reads it, is on
[Equipment row](equipment-row.md); this page is the shipped content of that table.

- Rows 0-419 are the equipment the party can hold, ids `0x1000`-`0x11A3`, the 420 counts of the inventory's
  equipment class ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): 200 main-hand
  weapons, 52 off-hand items (shields and ammunition), 60 head pieces, 60 body pieces and 48 accessories.
- Thirteen of the main-hand rows, 179-191, are named Reserve: classes 5, 0 and 8 and a price of 1, with weapon
  stats (Attack 61-201, reach, recipe, knockback on three) and element sets of their own, and empty bonus stats. An
  inventory count reaches them; their explanation says so and lists their Attack and element sets.
- Rows 420-556, ids `0x11A4`-`0x122C`, are past the inventory's 420 counts, so the party cannot hold them. Their
  names are "NOT USED" (124 rows) or "Reserve" (13 rows). The id check `0x00322C50` still accepts them, since it
  bounds class 6 by the table's own 557 rows (`0x1000` to `0x1000` + 557 - 1).
- Enemies are given these ids: 958 of the 1,146 enemy definitions hold one of them in their main-hand word
  `+0x16`, which `0x0023AC80` installs ([Bestiary](../Enemy-Spawning/bestiary.md)).

### How it is built

`Database/Tools/catalogues/equipment.py` reads the `us` `battle_pack.bin`:

1. the `st2e` table at entry `+0x38`: 557 rows of 52 bytes from the section's `+0x20`, and each row's 24-byte bonus
   record at section `+0x7144` plus the row's `+0x28`;
2. the name word `+0x02` through the word banks at entry `+0xF8`, as `0x0031C5D0` does (`0x0031C911`);
3. the class name: the name word (second `u16`) of row *class* of the category table at entry `+0x18`, which
   `0x0031C5D0` reads through id kind 28 (`0x0031E3DB`-`0x0031E435`). Its rows 0-26 carry the names of the classes 0-26
   ("Unarmed", "Sword (1H)", "Shield", "Arrows" and the others), and the decoder pairs them by number. The shipped name
   of row 22 is "NOT USED crown";
4. the element bits by the names on [Elements](../Damage-And-Battle-Formulas/elements.md), and the status bits by the names in
   [Statuses](../Status-Effects-And-KO/statuses.md)' table;
5. every one-byte text code through the glyph table of the shipped `us` font `font00.dat` (records of `0x24` bytes
   from `+0x28`, key = byte - `0x20`, the glyph's UTF-8 at `+0x04`, as [Fonts](../Menus-And-HUD/fonts.md) describes).

Every name word read here starts with the two zero bytes that `0x002B58B0` skips, so its other branch, for a row without
them, is not exercised by this table.

The group of a row's class decides which of `+0x18`, `+0x19` and `+0x1A` fill the weapon, shield or armor columns,
as the stats rebuild `0x002FEF30` reads them ([Equipment row](equipment-row.md), "The class byte and the group").

### Checks

- The table's own header gives 557 rows of 52 bytes, and the TSV has 557 data lines.
- Two runs over the same file give byte-identical output.
- Rows compared with the readers: row 1, Broadsword, has `+0x12` = `0x0186` (390 gil, the price `0x0031C981` reads),
  `+0x1A` = 14 (Attack) and `+0x11` = 18 (it takes a shield in the off hand); row 0, Unarmed, has Attack 12 and the
  class name Unarmed.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `id` | the equipment id, `0x1000` + row |
| `row` | the row number |
| `name` | the item's shipped name |
| `slot` | main hand, off hand, head, body or accessory (bits 7-5 of `+0x07`) |
| `class`, `class_name` | the class `+0x09` and its shipped category name |
| `sub_type` | `+0x04`, the kind of item copied to the query record `+0x2C` (`0x0031C9C4`) |
| `sort_key` | `+0x06`, the Optimise tie-break (`0x002F7C3C`) |
| `ordinal` | `+0x08`, the row's order inside its class (`0x0031C9CB`) |
| `price` | buy price in gil (`+0x12`) |
| `attack`, `reach_tenths`, `recipe` | weapons and ammunition: Attack Power `+0x1A`; weapons: reach in tenths `+0x18` and the damage recipe `+0x19` ([Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md)) |
| `defense`, `magick_resist`, `augment` | head, body and accessories: Defense `+0x18`, Magick Resist `+0x19`, and the augment `+0x1A` by its term on [Augment list](../Damage-And-Battle-Formulas/augment-list.md) with its id (empty for none; [Augments](../Damage-And-Battle-Formulas/augments.md)) |
| `shield_evade`, `magick_evade` | shields: `+0x18` and `+0x19` |
| `knockback`, `combo`, `weapon_evade` | weapons (classes 0-17): `+0x1B`, `+0x1C`, `+0x1D`; empty on ammunition, where all three are 0 |
| `element` | weapons and ammunition: the attack element `+0x1E` (`0x0038BE30`) |
| `status_chance`, `statuses_inflicted` | weapons and ammunition: the on-hit chance `+0x1F` and the statuses `+0x20` |
| `charge_base` | weapons (classes 0-17): the charge time base `+0x27` |
| `charge_weight` | `+0x10`, summed over the equipped items while the battle flag slows the charge |
| `off_hand_class` | `+0x11`, the class the off-hand item must have; -1 for none |
| `hp`, `mp`, `strength`, `magick_power`, `vitality`, `speed` | the bonus record's stat bonuses |
| `statuses_held`, `status_immune` | the bonus record's statuses the wearer has, and those it cannot get |
| `absorb`, `nullify`, `halve`, `weak`, `potency` | the bonus record's element sets |
| `no_license`, `hits_flying`, `cannot_sell` | `yes` for bits 4, 2 and 1 of `+0x07` |
| `b24` | weapons (classes 0-17): `+0x24`, one value per weapon kind |
| `reach_kind` | weapons (classes 0-17): `+0x25`, the range pair that sets the near and middle distance (`0x00320D93`) |
| `motion_class` | weapons (classes 0-17): `+0x26`, the attack motion class (`0x0032041E`) |
| `attack_effect` | weapons (classes 0-17): `+0x2C`, the effect a plain Attack shows in its low 15 bits (`0x0030AD56`) |
| `bonus_record` | the bonus record's index: `+0x28` / 24 |
| `model_id` | weapons, ammunition and shields: the held model `+0x30` |
| `explanation` | a one-line summary built from the row's own fields; for the Reserve rows 179-191 and the rows past the inventory's 420, what the row is |

## Related

- [Equipment row: every field of a weapon, shield, armor, accessory or ammunition data row and its bonus record](equipment-row.md)
- [Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script](../Damage-And-Battle-Formulas/augments.md)
