---
title: "Bazaar: every bazaar good, the loot you must sell to unlock it, its price, what it gives, and how unlocking and buying work"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF058, 0030B270, 0030B180, 002FEEB0, 00310870, 0030B570, 002FD780"
---

## What it lists

A bazaar good is an id `D000h + good`, a bundle that gives up to three items when bought. Selling enough of
its loots unlocks it; buying it uses up the loot sold.

### The table

The goods are section 57 of `battle_pack.bin`, the section its directory entry at file offset `+E8`<sub>h</sub> points to,
bound to `02EBF058` by the battle data binder (`00236F6E`-`00236F7C`). It is an `st2e` table of 128 rows of 36
bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | name | name word, read by the query filler `0031C5D0` |
| `02`<sub>h</sub> | `u16` | description | description text id, read by the query filler |
| `04`<sub>h</sub> | `u16` | item0 | first item given (`002FD780`, `002FD7F2`-`002FD85D`) |
| `06`<sub>h</sub> | `u8` | count0 | its count; 0 for none |
| `08`<sub>h</sub> | `u16` | item1 | second item given |
| `0A`<sub>h</sub> | `u8` | count1 | its count |
| `0C`<sub>h</sub> | `u16` | item2 | third item given |
| `0E`<sub>h</sub> | `u8` | count2 | its count |
| `10`<sub>h</sub> | `u32` | price | price in gil, copied to the query record's `+28`<sub>h</sub> (`0031DA1F`) |
| `14`<sub>h</sub> | `u16` | flags | bit `1`<sub>h</sub> it can come back, bit `2`<sub>h</sub> a script sets it (`0030B33F`, `0030B5F6`) |
| `16`<sub>h</sub> | `u16` | loot0 | first loot to sell; an unused slot is id 0 with count 0 (`0030B375`-`0030B45F`) |
| `18`<sub>h</sub> | `u8` | lootCount0 | its count |
| `1A`<sub>h</sub> | `u16` | loot1 | second loot to sell |
| `1C`<sub>h</sub> | `u8` | lootCount1 | its count |
| `1E`<sub>h</sub> | `u16` | loot2 | third loot to sell |
| `20`<sub>h</sub> | `u8` | lootCount2 | its count |
| `22`<sub>h</sub> | `u16` | c22 | 120 on every row, copied to the query record's `+2C`<sub>h</sub> (`0031DA32`-`0031DA36`) |

### Unlocking a good

Each loot id has a sold tally, one byte in the inventory at `+57C8h + loot`, kept between 0 and 99
([Inventory](inventory.md)). A sale through `00310870` takes the loot from the inventory, adds the gil (`003108AB`-`003108BD`), adds the
quantity to the tally (`003108D1`-`003108E8`) and then runs the refresh `0030B270` (`003108ED`), its only caller.

The refresh checks every good (`0030B270`-`0030B468`):

1. A good already unlocked once, flag byte bit 0, is skipped unless it can come back (`0030B33F`-`0030B34C`).
2. A good on offer now, flag bit 1, is skipped (`0030B352`-`0030B359`).
3. A good with no loot to sell is skipped (`0030B35F`-`0030B36F`).
4. Each of its three loots must have a tally at least its count (`0030B375`-`0030B45F`). An unused slot is id 0
   with count 0, so it compares item 0's tally, always 0, with 0 and passes; an id of `FFFF`<sub>h</sub> would read as -1
   and fail.
5. When all three are met, flag bits 0 and 1 are set (`0030B461`).

The flag bytes are one per good at `+59C8`<sub>h</sub> of the party block. The shop menu lists every good whose bit 1 is
set (mode 2 of `002FA920`, [Shops](shops.md)).

### Buying a good

The shop's transaction function `0056D370` reads the price from the good's query record, clears its bit 31 and
multiplies it by the quantity (`0056D461`-`0056D473`). The purchase `002FEEB0(id, quantity, price, flags)` adds the
good through `003008A0`, which hands out its
items (`002FEEDB`, `002FD780`), takes the price from the gil, floored at 0, through `00253690` and `00254EE0` (`002FEEE0`-`002FEEF3`; [Gil](../Rewards-EXP-Gil-And-Loot/gil.md)), and calls
`0030B180` (`002FEF0A`).

For a bazaar id, `0030B180` clears flag bit 1, so the good leaves the list, and sets the
tally of each of its three loots back to 0 (`0030B203`-`0030B256`). A good that can come back therefore needs its
loots sold again from zero; any other good stays unlocked once and does not return. Both the sale and the purchase
are called only by the shop's transaction function `0056D370` (`0056D478`, `0056D49A`).

### Goods a script offers

The seven goods with flag bit 1, all named Forgotten Grimoire, have no loot to sell. Script verbs `2F7`<sub>h</sub>
`sethoridashi` and `2F6`<sub>h</sub> `clearhoridashi` set or clear their offer bit through `0032AB50` and `0030B570`
(`0034C710`, `0034C2C0`), which writes it only for a good with that flag (`0030B5F6`-`0030B619`). The third
verb, `2F5`<sub>h</sub> `ishoridashi`, cannot read it: its handler `0034BD90` calls `005C5230`, which returns 0.

### Clearing

Whenever the party block is bound, by `00233C10` (`00233C3A`) or `00238A80` (`00238A99`), the rebaser `0030B6A0`
clears every sold tally (`0030B702`-`0030B737`) and
bits 0-2 of every flag byte (`0030B739`-`0030B75B`).

## Columns

`bazaar.tsv`, one row per good:

| Column | Meaning |
|---|---|
| `good` | the row, 0-127 |
| `id` | its encoded id, `D000h + good` |
| `name` | its name from the shipped text |
| `price` | gil |
| `gives` | the items it gives, with counts and ids |
| `unlocked_by_selling` | the loots and the counts that must be sold, with ids; `-` for none |
| `repeatable` | flag bit 0: it can come back after it is bought |
| `script_sets_availability` | flag bit 1: a script offers it |

The 128 goods cost from 70 to 600,000 gil. Fifteen can come back: goods 87-94, 103, 104 and 106-110. The seven
script goods are 99-102 and 124-126.

## Related

- [Shops](shops.md) - the shop menu that lists the goods.
- [Inventory](inventory.md) - the sold tally and the bundle ids.
- [Equipment row](equipment-row.md) - the equipment some goods give.
