---
title: "Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps"
kind: "system"
category: "Damage and battle formulas"
addresses: "0x002FEF30, 0x0030FED0, 0x002F8E50, 0x002F9180, 0x0031E9A0, 0x003105D0"
---

## What the player sees

A character's numbers on the status screen are a sum, worked out again every time anything changes:
the character's own values, plus equipment, plus augments from the License Board and gear. Nothing is
added on top of an old value.

| Stat | Cap |
|---|---:|
| max HP | 9,999 for the party, 32,767 for Espers |
| max MP | 999 |
| Strength, Magick Power, Vitality, Speed | 99 |
| Attack Power, Defense, Magick Resist | 255 |
| Evade, Magick Evade and their parts | 100 |

No stat goes below 0, and max HP never goes below 1.

On the Equip screen, highlighting a piece that would take another piece off, or that cannot be used with what is
worn, replaces the help line with a warning such as "Equipping a two-handed weapon will remove your shield." (the
full list is under [The equipment comparison's warnings](#the-equipment-comparisons-warnings)).

## How it works

### The rebuild

`0x002FEF30(stats, out, equipment)` computes the stats block. With `out` and `equipment` null it writes the
record's own block at `+0x24` and reads the five equipment words at `+0x50` (`0x002FEF95`-`0x002FEFAB`). It
clears the block first (`0x002FEFB9`-`0x002FEFC8`).

The augment rebuild `0x0030FED0` calls it (`0x003103AD`); [Augments](augments.md) lists that function's 25
callers. The equipment comparison `0x0030A4E0` calls it with its own block (`0x0030A6B7`).

### The equipment comparison

`0x0030A4E0(member, candidate, out)` builds a member's stats as they would be with five other equipment words
(`candidate`, laid out like stats `+0x50`). `out` is a `0x2C`-byte record: the `0x24`-byte stats block, then a
warning code at `+0x24` (`u32`) and an equipment id at `+0x28` (`u16`). In order:

1. It finds the member's stats with `0x00320AB0(member, 3)`; with none it returns -1 and writes nothing
   (`0x0030A503`-`0x0030A513`).
2. It writes 0 to `out+0x24` and `0xFFFF` to `out+0x28` (`0x0030A518`-`0x0030A524`). With no candidate it goes to step 6.
3. The slot it judges is the highest of the five whose candidate word differs from the worn one
   (`0x0030A565`-`0x0030A5C3`); the piece is that slot's candidate word.
4. It runs the hand check `0x00318B40(candidate, slot, 0)` ([Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md))
   and stores the new word of the highest slot the check changed at `out+0x28` (`0x0030A5D5`-`0x0030A640`).
5. It stores the warning code at `out+0x24` (below).
6. It builds the stats into `out` with `0x002FEF30(stats, out, words)` (`0x0030A6B7`) and returns that result.

### The equipment comparison's warnings

The code is `0x10` when the license test `0x00323C60` refuses the piece (`0x0030A64F`-`0x0030A658`). An empty slot
(`0xFFFF`) fails that test's id check, so taking a piece off always gives `0x10`. Otherwise `0x00309480` answers
(`0x0030A691`) from the slot, the piece's and the worn pieces' categories, and whether the hand check changed the off
hand.

The categories come from `0x0031EA90` through the byte map `0x0031EA74`
([Equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md)):

| Category | Pieces |
|---|---|
| `0` | an empty slot |
| `1` | Unarmed |
| `2` | one-handed weapons |
| `3` | two-handed weapons |
| `4` | bows, crossbows, guns and hand-bombs |
| `5` | ammunition |
| `6` | shields |
| `7`, `8`, `9` | head (class 19), body (class 20), accessories (classes 21-22); `0x00309480` treats them like any category it does not list |

A ranged weapon's ammunition is at hand when `0x003096F0(weapon, worn off hand)` returns 1: the worn off hand holds
ammunition (ids `0x1184`-`0x11A3`) of the class the weapon's `+0x11` names, or the party holds at least one of
those ammunition ids (the equipment class's query handler, `0x00309801`-`0x0030988D`).

| Code | Slot | When | Help line |
|---:|---|---|---|
| `0` | any | none of the rows below applies, as for every head, body or accessory piece the license test accepts | the screen's own line |
| `1` | off hand | a shield, under a worn two-handed weapon | "Equipping a shield will remove your two-handed weapon." (3229) |
| `2` | off hand | a shield, under a worn ranged weapon | "Equipping a shield will remove your ranged weapon." (3248) |
| `3` | main hand | a two-handed weapon, over a worn shield | "Equipping a two-handed weapon will remove your shield." (3231) |
| `4` | main hand | a ranged weapon whose ammunition is at hand, over a worn shield | "Equipping a ranged weapon will remove your shield." (3232) |
| `5` | main hand | over worn ammunition: a weapon that is not ranged; or a ranged weapon whose ammunition is at hand when the hand check changes the off hand | "Changing your equipped weapon will remove all ammunition." (3255) |
| `6` | off hand | arrows (class 23) under a worn Unarmed, one-handed or two-handed weapon, or under a worn ranged weapon when the hand check changes the off hand | "You must equip a bow before equipping arrows." (3250) |
| `7` | off hand | bolts (class 24), as for `6` | "You must equip a crossbow before equipping bolts." (3251) |
| `8` | off hand | shot (class 25), as for `6` | "You must equip a gun before equipping shot." (3252) |
| `9` | off hand | bombs (class 26), as for `6` | "You must equip a hand-bomb before equipping bombs." (3253) |
| `0xE` | main hand | a ranged weapon whose ammunition is not at hand, over an empty off hand, ammunition or a shield | "You lack the proper ammunition to equip this weapon." (3321) |
| `0xF` | off hand | a piece of category 0, under a worn ranged weapon, with ammunition worn | text 3322 |
| `0x10` | the slot | the license test refuses the piece, including an empty slot | the screen's own line |

Text 3322 begins with its terminator in the English and Italian `help_menu.bin`, so it shows nothing; the French
and German rows say that taking the ammunition off removes the ranged weapon, and the Spanish row reads `DUMMY`. No
shipped equipment row has a class outside 0-26, so the only category-0 piece is the empty slot, which the license
test refuses first: `0xF` is not produced with the shipped tables.

When no slot differs, the license test is given the stack word at `[rsp+0x46]`, which the function never writes
(`0x0030A644`-`0x0030A64F` with slot -1), and `0x00309480` returns 0 for slot -1: the code is 0 or `0x10`, and the help
line is the screen's own either way.

The help window shows the code as follows:

- The Equip screen's two refreshers `0x003FE720` and `0x003FEAD0` copy the code to the menu block's byte `+0xDE2` and the
  id to the word `+0xDE4` (`0x003FE9E7`, `0x003FECBB`; the word stores `0x003FE9F8`, `0x003FECD0`).
- `0x002CA490` reads `+0xDE2` through the 17-entry jump table at `0x002CA574` and puts the line in the help window
  (`[0x0209BE80] + 0x8FA0`, through `0x002F9860`, `0x00291D70` and `0x00291D80`). For codes 1-9, `0xE` and `0xF` it does so
  only when the code differs from the last one, kept at `+0xDE3`.
- Codes `0xA`-`0xD`, which `0x00309480` never returns, have no line (their table rows go to `0x002CA522` with id 0).
- Codes 0 and `0x10` show the line the caller passes: "Change equipment." (`0x003FE2A2`), the text at `+0x180` of the
  menu block's widget `+0x108` (`0x003FF97D`) or, in the shop, "Select a character to equip." (`0x0057B3BF`).
- No instruction of the 456 functions that load `[0x0209AC30]` reads `+0xDE4`. The member panel `0x002CA7C0` calls the
  comparison for its numbers and reads neither field.

### A party member's base

For a party record (stats `+0x05` = 0), the base comes from the character row of table `0x02EBF130` that
the type byte `+0x04` selects (`0x002FF02E`-`0x002FF0DC`):

```python
maxHp = (row[+0x18] + 1) * stats[+0x08] * row[+0x19] / 100  # 0x002F8E50
maxMp = stats[+0x0C] * row[+0x1D] / 100                   # 0x002F9180
Strength, Magick Power, Vitality, Speed = (int) the floats stats[+0x10], [+0x14], [+0x18], [+0x1C]
innate evade = row[+0x2A]
```

Both divisions truncate towards zero. The four floats are the character's grown values
([Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)). The row's status
words `+0x4C` and `+0x48` are ORed into stats `+0x38` and `+0x3C` (`0x002FF0A3`-`0x002FF0D9`).

### An enemy's base

For any other record the base comes from three area tables, found through the unit's row of `0x02EBF120`
(selected by `+0x04`): the base row of `0x02EBF148` its word `+0x22` names and the growth row of `0x02EBF140`
its word `+0x24` names (`0x002FF0E1`-`0x002FF1A4`). With `d` = the unit's level `+0x1C2` minus its reference
level `+0x88` (`0x002FF1EE`-`0x002FF200`), each stat is:

```python
stat = growth[field] * d + base[field] + stats[adjustment]
```

| Stat | Base and growth field | Adjustment word |
|---|---|---|
| max HP | `+0x20` (`u32`) | none |
| max MP | `+0x24` (`i16`) | none |
| Strength | `+0x26` | `+0x08` |
| Magick Power | `+0x27` | `+0x0A` |
| Vitality | `+0x28` | `+0x0C` |
| Speed | `+0x29` | `+0x0E` |
| innate evade | `+0x2A` | `+0x16` |
| Defense | `+0x2B` | `+0x12` |
| Magick Resist | `+0x2C` | `+0x14` |

Attack Power starts from the adjustment word `+0x10`, and the evades from `+0x18`, `+0x1A`, `+0x1C`, `+0x1E`
and `+0x20` (`0x002FF202`-`0x002FF2F5`). Two bits of the `0x02EBF120` row's byte `+0x15` switch sources
(`0x002FF325`-`0x002FF3C8`):

- **bit 0:** Attack Power adds base and growth `+0x2D`, weapon evade adds `+0x2E`, and the equipped
  weapon's Attack Power and evade are not added;
- **bit 1:** shield evade adds base and growth `+0x02`, magick evade `+0x03`, and the shield's values are
  not added.

### Equipment

Each of the five equipment words that names an item (`0x00322C50(6, id)`) adds by the item's group from
`0x0031E9A0` (`0x002FF3F0`-`0x002FF4A4`):

| Group | Equipment classes | Adds |
|---|---|---|
| `1` | weapons and ammunition | row `+0x1A` to Attack Power, row `+0x1D` to weapon evade |
| `2` | shields | row `+0x18` to shield evade, row `+0x19` to magick evade |
| `3` | helms, armor, accessories | row `+0x18` to Defense, row `+0x19` to Magick Resist |

Every item then adds its attribute record, whatever its group (`0x002FF4A7`-`0x002FF571`): `u16 +0x00` to max
HP, `u16 +0x02` to max MP, bytes `+0x04`-`+0x07` to Strength, Magick Power, Vitality and Speed; it ORs
`+0x0C` into stats `+0x38` and `+0x08` into stats `+0x3C`, and its elements into the affinity bytes
([Elements](elements.md)).

### Augments that add stats

Three lists of augment ids add a bonus when the id is set in either augment layer, `+0x68` or `+0x78`
(`0x002FF581`-`0x002FF77A`). The bonus is the `u16` at `+0x04` of the id's row in the augment table
`0x02EBF040`; each id's text is entry *id* of the augment text bank:

| List | Ids | Adds to | Bonus | Licenses |
|---|---|---|---|---|
| `0x00D10290` | `35`, `42`-`47`, `60`-`68` | Strength | 1 each | Battle Lore |
| `0x00D102A0` | `19`, `22`, `24`, `26`, `69`-`73`, `87`, `97`-`102` | Magick Power | 1 each | Magick Lore |
| `0x00D102B0` | `74`-`85` | max HP | 30, 70, 110, 150, 190, 230, 270, 310, 350, 390, 435, 500 | +30 HP to +500 HP |

### Totals and caps

After the sums, the rebuild limits and stores each value (`0x002FF780`-`0x002FF96D`):

| Stats offset | Value | Limits |
|---|---|---|
| `+0x24` | max HP | 1 to 9,999 for a party record, 1 to 1,000,000,000 otherwise (`0x002FF7B1`-`0x002FF7E2`) |
| `+0x24` | max HP of an Esper (party type `0x1B`-`0x27`) | 1 to 32,767, over the first store (`0x002FF7E5`-`0x002FF805`) |
| `+0x28` | max MP | 0 to 999 |
| `+0x2A-0x2D` | Strength, Magick Power, Vitality, Speed | 0 to 99 |
| `+0x2E`, `+0x2F`, `+0x30` | Attack Power, Defense, Magick Resist | 0 to 255 |
| `+0x31-0x34` | innate, weapon, shield and magick evade | 0 to 100 |
| `+0x35` | Evade: innate + weapon + shield evade, plus `+0x1E` for an enemy | 0 to 100 |
| `+0x36` | Magick Evade: magick evade, plus `+0x20` for an enemy | 0 to 100 |
| `+0x37` | MP bars, a party member's stats `+0x20` | at most 3 |

The 9,999 and 1,000,000,000 are literals that one `cmove` picks by the party byte (`0x002FF7BD`-`0x002FF7C8`).

### Confuse and Berserk cancel the action in flight

For a party record with a battle unit, the rebuild compares stats `+0x3C` with its value on entry. When
Confuse (status 5) or Berserk (status 27) changed (mask `0x8000020`, `0x002FF982`-`0x002FF98E`), it cancels
the unit's current action with `0x003105D0` (`0x002FF9C7`), except in these cases:

- the unit word's bit 24 is set (`0x002FF99C`);
- the action id `+0x714` is at most `0x21E` and byte `+0x6B4` is at least 9 (`0x002FF9A3`-`0x002FF9BD`);
- the action id is `0x113` (`0x002FF9BF`).

It then clears the unit's `+0x6F8`, `+0x748`, `+0x770`, `+0x750` and `+0x74C`, bit 10 of `+0x788` and bit 1
of `+0x6B0`, sets bit 21 of `+0x04`, clears bit 14 of the unit word unless `+0xBA0` holds `0x113` or `0x95`,
and calls `0x00307D10` (`0x002FF9CC`-`0x002FFA40`).

## Modding notes

- The caps are immediates in `0x002FEF30`: `0x270F`, `0x3B9ACA00`, `0x7FFF`, `0x3E7`, `0x63`, `0xFF` and
  `0x64`.
- An item's flat bonuses are its attribute record; several items can share one record.
- The three augment lists are bytes in the executable at `0x00D10290`, `0x00D102A0` and `0x00D102B0`; the bonus
  sizes are data in the augment table.
- An enemy's stats grow with the difference between its level and its reference level; the same
  difference sets its reward ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)).

## Related

- [Elements](elements.md) - the affinity bytes the same rebuild fills.
- [HP and KO](hp-and-ko.md) - the HP cap and the HP write.
- [Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) - where the grown
  values come from.
- [Battle orders](../Battle-Actions/battle-orders.md) - the orders that adjust an enemy's stats.
