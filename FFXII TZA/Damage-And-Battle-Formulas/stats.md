---
title: "Stats: how max HP, MP, Strength, Magick Power, Vitality, Speed, Attack Power, Defense, Magick Resist and evade are built, and their caps"
kind: "system"
category: "Damage and battle formulas"
addresses: "002FEF30, 0030FED0, 002F8E50, 002F9180, 0031E9A0, 003105D0"
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

## How it works

### The rebuild

`002FEF30(stats, out, equipment)` computes the stats block. With `out` and `equipment` null it writes the
record's own block at `+24`<sub>h</sub> and reads the five equipment words at `+50`<sub>h</sub> (`002FEF95`-`002FEFAB`). It
clears the block first (`002FEFB9`-`002FEFC8`).

The augment rebuild `0030FED0` calls it (`003103AD`); [Augments](augments.md) lists that function's 25
callers. The equipment comparison `0030A4E0` calls it with its own block (`0030A6B7`).

### A party member's base

For a party record (stats `+05`<sub>h</sub> = 0), the base comes from the character row of table `02EBF130` that
the type byte `+04`<sub>h</sub> selects (`002FF02E`-`002FF0DC`):

```python
maxHp = (row[+0x18] + 1) * stats[+0x08] * row[+0x19] / 100  # 002F8E50
maxMp = stats[+0x0C] * row[+0x1D] / 100                   # 002F9180
Strength, Magick Power, Vitality, Speed = (int) the floats stats[+0x10], [+0x14], [+0x18], [+0x1C]
innate evade = row[+0x2A]
```

Both divisions truncate towards zero. The four floats are the character's grown values
([Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)). The row's status
words `+4C`<sub>h</sub> and `+48`<sub>h</sub> are ORed into stats `+38`<sub>h</sub> and `+3C`<sub>h</sub> (`002FF0A3`-`002FF0D9`).

### An enemy's base

For any other record the base comes from three area tables, found through the unit's row of `02EBF120`
(selected by `+04`<sub>h</sub>): the base row of `02EBF148` its word `+22`<sub>h</sub> names and the growth row of `02EBF140`
its word `+24`<sub>h</sub> names (`002FF0E1`-`002FF1A4`). With `d` = the unit's level `+1C2`<sub>h</sub> minus its reference
level `+88`<sub>h</sub> (`002FF1EE`-`002FF200`), each stat is:

```python
stat = growth[field] * d + base[field] + stats[adjustment]
```

| Stat | Base and growth field | Adjustment word |
|---|---|---|
| max HP | `+20`<sub>h</sub> (`u32`) | none |
| max MP | `+24`<sub>h</sub> (`i16`) | none |
| Strength | `+26`<sub>h</sub> | `+08`<sub>h</sub> |
| Magick Power | `+27`<sub>h</sub> | `+0A`<sub>h</sub> |
| Vitality | `+28`<sub>h</sub> | `+0C`<sub>h</sub> |
| Speed | `+29`<sub>h</sub> | `+0E`<sub>h</sub> |
| innate evade | `+2A`<sub>h</sub> | `+16`<sub>h</sub> |
| Defense | `+2B`<sub>h</sub> | `+12`<sub>h</sub> |
| Magick Resist | `+2C`<sub>h</sub> | `+14`<sub>h</sub> |

Attack Power starts from the adjustment word `+10`<sub>h</sub>, and the evades from `+18`<sub>h</sub>, `+1A`<sub>h</sub>, `+1C`<sub>h</sub>, `+1E`<sub>h</sub>
and `+20`<sub>h</sub> (`002FF202`-`002FF2F5`). Two bits of the `02EBF120` row's byte `+15`<sub>h</sub> switch sources
(`002FF325`-`002FF3C8`):

- **bit 0:** Attack Power adds base and growth `+2D`<sub>h</sub>, weapon evade adds `+2E`<sub>h</sub>, and the equipped
  weapon's Attack Power and evade are not added;
- **bit 1:** shield evade adds base and growth `+02`<sub>h</sub>, magick evade `+03`<sub>h</sub>, and the shield's values are
  not added.

### Equipment

Each of the five equipment words that names an item (`00322C50(6, id)`) adds by the item's group from
`0031E9A0` (`002FF3F0`-`002FF4A4`):

| Group | Equipment classes | Adds |
|---|---|---|
| `1` | weapons and ammunition | row `+1A`<sub>h</sub> to Attack Power, row `+1D`<sub>h</sub> to weapon evade |
| `2` | shields | row `+18`<sub>h</sub> to shield evade, row `+19`<sub>h</sub> to magick evade |
| `3` | helms, armor, accessories | row `+18`<sub>h</sub> to Defense, row `+19`<sub>h</sub> to Magick Resist |

Every item then adds its attribute record, whatever its group (`002FF4A7`-`002FF571`): `u16 +00h` to max
HP, `u16 +02h` to max MP, bytes `+04`<sub>h</sub>-`+07`<sub>h</sub> to Strength, Magick Power, Vitality and Speed; it ORs
`+0C`<sub>h</sub> into stats `+38`<sub>h</sub> and `+08`<sub>h</sub> into stats `+3C`<sub>h</sub>, and its elements into the affinity bytes
([Elements](elements.md)).

### Augments that add stats

Three lists of effect ids add a bonus when the id is set in either effect layer, `+68`<sub>h</sub> or `+78`<sub>h</sub>
(`002FF581`-`002FF77A`). The bonus is the `u16` at `+04`<sub>h</sub> of the id's row in the augment table
`02EBF040`; each id's text is entry *id* of the augment text bank:

| List | Ids | Adds to | Bonus | Licenses |
|---|---|---|---|---|
| `00D10290` | `35`, `42`-`47`, `60`-`68` | Strength | 1 each | Battle Lore |
| `00D102A0` | `19`, `22`, `24`, `26`, `69`-`73`, `87`, `97`-`102` | Magick Power | 1 each | Magick Lore |
| `00D102B0` | `74`-`85` | max HP | 30, 70, 110, 150, 190, 230, 270, 310, 350, 390, 435, 500 | +30 HP to +500 HP |

### Totals and caps

After the sums, the rebuild limits and stores each value (`002FF780`-`002FF96D`):

| Stats offset | Value | Limits |
|---|---|---|
| `24`<sub>h</sub> | max HP | 1 to 9,999 for a party record, 1 to 1,000,000,000 otherwise (`002FF7B1`-`002FF7E2`) |
| `24`<sub>h</sub> | max HP of an Esper (party type `1B`<sub>h</sub>-`27`<sub>h</sub>) | 1 to 32,767, over the first store (`002FF7E5`-`002FF805`) |
| `28`<sub>h</sub> | max MP | 0 to 999 |
| `2A-2D`<sub>h</sub> | Strength, Magick Power, Vitality, Speed | 0 to 99 |
| `2E`<sub>h</sub>, `2F`<sub>h</sub>, `30`<sub>h</sub> | Attack Power, Defense, Magick Resist | 0 to 255 |
| `31-34`<sub>h</sub> | innate, weapon, shield and magick evade | 0 to 100 |
| `35`<sub>h</sub> | Evade: innate + weapon + shield evade, plus `+1E`<sub>h</sub> for an enemy | 0 to 100 |
| `36`<sub>h</sub> | Magick Evade: magick evade, plus `+20`<sub>h</sub> for an enemy | 0 to 100 |
| `37`<sub>h</sub> | MP bars, a party member's stats `+20`<sub>h</sub> | at most 3 |

The 9,999 and 1,000,000,000 are literals that one `cmove` picks by the party byte (`002FF7BD`-`002FF7C8`).

### Confuse and Berserk cancel the action in flight

For a party record with a battle unit, the rebuild compares stats `+3C`<sub>h</sub> with its value on entry. When
Confuse (status 5) or Berserk (status 27) changed (mask `8000020`<sub>h</sub>, `002FF982`-`002FF98E`), it cancels
the unit's current action with `003105D0` (`002FF9C7`), except in these cases:

- the unit word's bit 24 is set (`002FF99C`);
- the action id `+714`<sub>h</sub> is at most `21E`<sub>h</sub> and byte `+6B4`<sub>h</sub> is at least 9 (`002FF9A3`-`002FF9BD`);
- the action id is `113`<sub>h</sub> (`002FF9BF`).

It then clears the unit's `+6F8`<sub>h</sub>, `+748`<sub>h</sub>, `+770`<sub>h</sub>, `+750`<sub>h</sub> and `+74C`<sub>h</sub>, bit 10 of `+788`<sub>h</sub> and bit 1
of `+6B0`<sub>h</sub>, sets bit 21 of `+04`<sub>h</sub>, clears bit 14 of the unit word unless `+BA0`<sub>h</sub> holds `113`<sub>h</sub> or `95`<sub>h</sub>,
and calls `00307D10` (`002FF9CC`-`002FFA40`).

## Modding notes

- The caps are immediates in `002FEF30`: `270F`<sub>h</sub>, `3B9ACA00`<sub>h</sub>, `7FFF`<sub>h</sub>, `3E7`<sub>h</sub>, `63`<sub>h</sub>, `FF`<sub>h</sub> and
  `64`<sub>h</sub>.
- An item's flat bonuses are its attribute record; several items can share one record.
- The three augment lists are bytes in the executable at `00D10290`, `00D102A0` and `00D102B0`; the bonus
  sizes are data in the augment table.
- An enemy's stats grow with the difference between its level and its reference level; the same
  difference sets its reward ([Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)).

## Related

- [Elements](elements.md) - the affinity bytes the same rebuild fills.
- [HP and KO](hp-and-ko.md) - the HP cap and the HP write.
- [Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) - where the grown
  values come from.
- [Battle orders](../Battle-Actions/battle-orders.md) - the orders that adjust an enemy's stats.
