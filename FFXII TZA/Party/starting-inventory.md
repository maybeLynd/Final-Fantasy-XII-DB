---
title: "Starting inventory: the shoki_data table the party-block reset adds to the inventory, empty in the shipped game"
kind: "reference"
category: "Party"
addresses: "0x02EBF048, 0x0023AF50, 0x00237DF0, 0x00300BA0, 0x003008A0"
---

## What it lists

`starting-inventory.tsv` holds one line for each of the 32 rows of the table that registry slot `0x02EBF048` reaches
(`battle_pack.bin` directory entry `+0xAC`). Every shipped row is the id `0xFFFF` with count 0, so the table adds
nothing; the items a new party holds come from the first-join lists of the
[Party table](party-table.md) ([Party members](party-members.md)).

### The reader

`0x0023AF50` is the only function that reads the table (`0x0023AF50`-`0x0023B01A`):

1. it resets the party block with `0x002370C0` ([Party data](party-data.md));
2. for each row, while the row number is below the table's count, it calls `0x00300BA0(+0x00, +0x02, 0)`, which is
   `0x003008A0(id, count, 1, 1, 0)`, the inventory change of
   [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md);
3. `0x003008A0` returns -1 at once for id `0xFFFF` (`0x003008C0`-`0x003008C5`).

`0x0023AF50` runs at the start of `0x00237DF0`, which then builds the forty member records with `0x0023AC80`;
`0x00237DF0` is called by `0x00233C10`, `0x00238A80`, `0x00239960` and `0x00394460`. The last is the title asset's factory,
which the title script verb `fsttl_initialize` (`0x00511EA0`) runs, calling `0x00237DF0` at `0x00394486`
([Widgets](../Menus-And-HUD/widgets.md), [Verb table](../Scripts-And-Script-Commands/verb-table.md)).

### Where the values come from

The rows are the `st2e` table at `battle_pack.bin` entry `+0xAC`: 32 rows of 4 bytes from the section's `+0x20`.

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u16` | id | `0x0023AF50` | an inventory id; `0xFFFF` on every row |
| `+0x02` | `u16` | count | `0x0023AF50` | the count to add; 0 on every row |

The table is loaded only by `0x0023AF50` and the loader `0x00236C30` (`0x00236F54`).

### Properties of the shipped rows

- The table's header gives 32 rows of 4 bytes, one TSV line each.
- Every row is `0xFFFF` and 0, the value `0x003008A0` refuses before it reads the inventory.

## Columns

| Column | Meaning |
|---|---|
| `row` | the row |
| `id`, `count` | `+0x00` and `+0x02` |
| `name` | the id's shipped name; empty for `0xFFFF` |
| `explanation` | what the row adds |

## Related

- [Party table: every party member, guest, Esper and the Chocobo with their starting stats, equipment, gambits, Quickenings, first-join items and model](party-table.md)
- [Party members and guests: who can join, how the story adds and removes them, where a guest sits, and what a join brings](party-members.md)
- [Inventory: how items, equipment, loot, magicks, technicks, gambits and key items are stored and counted, what changes them, and the gil purse](../Items-Equipment-Shops-And-Licenses/inventory.md)
