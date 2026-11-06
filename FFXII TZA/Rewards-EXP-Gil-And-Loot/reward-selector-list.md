---
title: "Reward selector list: every package selector and the packages it chooses between"
kind: "reference"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0x02EBF068, 0x002FD640, 0x0031C5D0, 0x0031D712, 0x00322C50"
---

## What it lists

[`reward-selector-list.tsv`](reward-selector-list.tsv) holds one line for each of the 256 rows of the selector table that registry slot
`0x02EBF068` reaches (`battle_pack.bin` directory entry `+0x9C`). Row *n* is selector id `0xA000` + *n*, inventory
class 15 ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)).

- 45 selectors, `0xA080`-`0xA0AC`, name one reward package each in their first triple, and no selector uses its second
  triple.
- The other 211 rows hold `0xFFFF` in all six ids.

### Where the values come from

The selector table is the `st2e` table at entry `+0x9C` (256 rows of 12 bytes from the section's `+0x20`); each
named package is described by its own row of [Reward package list](reward-package-list.md).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u16[3]` | first | the ids the class-15 handler `0x002FD640` grants, each tested for `0xFFFF` on its own; it acts only on a relative give on channel 1 (`0x002FD64F`-`0x002FD65C`), grants each id through `0x003008A0(id, give's count, 0, 1, flags)`, and returns 0. Nothing guards the row: when the slot `0x02EBF068` is null or its decoded row base is 0, the row address is 0 (`0x002FD66E`-`0x002FD6AA`) and the first id read, `0x002FD6C0` or `0x002FD704`, faults, because the first 64 KB of a Windows x64 process are never mapped |
| `+0x06` | `u16[3]` | second | granted instead when the give's flag bit `0x2` is set: the sixth id whenever the fifth is not `0xFFFF` |

`0x0031C5D0`'s class-15 arm copies the first triple to the query record and its class-31 arm the second
(`0x0031D712`-`0x0031D73A`).

Class 30 shares that arm and copies the first triple too. `0x0030AAC0(id, &a, &b, &c, flags)`, from the hunt pane
`0x003F4C30` (`0x003F4CAD`), reads a selector that way: it fills its own record with class 30, or 31 when `flags` has
bit `0x2` (`0x0030AADC`-`0x0030AAF1`), and the id, calls `0x0031C5D0`, and returns the three words at the record's `+0x38`,
`+0x3A` and `+0x3C`, or -1 when the fill fails.

## Columns

| Column | Meaning |
|---|---|
| `id` | the selector id |
| `first`, `second` | the ids of each triple other than `0xFFFF` |
| `explanation` | each named package with what it gives, or that the selector is empty |

## Related

- [Reward package list: every reward package with its gil and items, and where it is named](reward-package-list.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
