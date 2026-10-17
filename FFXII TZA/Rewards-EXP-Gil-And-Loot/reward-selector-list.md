---
title: "Reward selector list: every package selector and the packages it chooses between"
kind: "reference"
category: "Rewards: EXP, LP, gil and loot"
addresses: "02EBF068, 002FD640, 0031C5D0, 0031D712, 00322C50"
---

## What it lists

`reward-selector-list.tsv` holds one line for each of the 256 rows of the selector table that registry slot
`02EBF068` reaches (`battle_pack.bin` directory entry `+9C`<sub>h</sub>). Row *n* is selector id `A000`<sub>h</sub> + *n*, inventory
class 15 ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)).

- 45 selectors, `A080`<sub>h</sub>-`A0AC`<sub>h</sub>, name one reward package each in their first triple, and none uses its second
  triple.
- The other 211 rows hold `FFFF`<sub>h</sub> in all six ids.

### How it is built

`Database/Tools/catalogues/reward_selectors.py` reads the `st2e` table at entry `+9C`<sub>h</sub> (256 rows of 12 bytes from
the section's `+20`<sub>h</sub>) and describes each named package by its own row of
[Reward package list](reward-package-list.md).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16[3]` | first | the ids the class-15 handler `002FD640` grants, each tested for `FFFF`<sub>h</sub> on its own |
| `06`<sub>h</sub> | `u16[3]` | second | granted instead when the give's flag bit 1 is set: the sixth id whenever the fifth is not `FFFF`<sub>h</sub> |

`0031C5D0`'s class-15 arm copies the first triple to the query record and its class-31 arm the second
(`0031D712`-`0031D73A`).

### Checks

- The table's header gives 256 rows of 12 bytes, and the TSV has 256 data lines.
- Two runs over the same files give byte-identical output.
- Rows compared with the handler: `A080`<sub>h</sub> names `9003`<sub>h</sub>, 300 gil, Potion x2 and Teleport Stone x1; `A0AB`<sub>h</sub> names
  `902E`<sub>h</sub>, 30,000 gil and Godslayer's Badge x1.

## Columns

| Column | Meaning |
|---|---|
| `id` | the selector id |
| `first`, `second` | the ids of each triple other than `FFFF`<sub>h</sub> |
| `explanation` | each named package with what it gives, or that the selector is empty |

## Related

- [Reward package list: every reward package with its gil and items, and where it is named](reward-package-list.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
