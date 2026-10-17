---
title: "Shops: every shop with its name, its stock lists and the story or clan-rank condition that opens each list"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF158, 00238660, 002FAD40, 002FA920, 002FAE40, 002FABD0, 00315390"
---

## What it lists

A shop's stock is a ladder of lists, most advanced first. The menu finds the first list whose condition the
player meets and sells that list together with every list after it, so a shop's stock grows as the story goes
on or the clan rank rises.

### The table

The shop table is section 39 of `battle_pack.bin`, the section its directory entry at file offset `+A0`<sub>h</sub> points
to. The battle data binder hands it to `00238660` (`00236F28`-`00236F2E`), which stores the section address in
the registry slot `02EBF158` and adds it to every offset in the table: the header's data offset, each shop's
ladder, each ladder's data, each list and each list's data (`00238678`-`0023881D`). It has three levels, each
with the same 12-byte header, `ShopLevelHeader`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | tag | `64`<sub>h</sub> shops, `164`<sub>h</sub> ladders, `264`<sub>h</sub> lists |
| `04`<sub>h</sub> | `u16` | stride | bytes per row |
| `06`<sub>h</sub> | `u16` | count | rows |
| `08`<sub>h</sub> | `u32` | data | offset of the first row, made an address by `00238660` |

A shop row, 8 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | name | the shop's name id |
| `02`<sub>h</sub> | `u16` | pad | padding |
| `04`<sub>h</sub> | `u32` | ladder | offset of the shop's ladder |

A ladder row, 8 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | kind | condition kind |
| `01`<sub>h</sub> | `u8` | operand | condition operand |
| `02`<sub>h</sub> | `u16` | threshold | condition threshold |
| `04`<sub>h</sub> | `u32` | list | offset of the list the rung selects |

A list row is one `u16`, an encoded id: `0XXXh` item, `1XXXh` equipment, `2XXXh` loot, `3XXXh` magick, `4XXXh`
technick, `6XXXh` gambit.

### Choosing a list

`002FAD40(shop)` walks the shop's ladder in order and returns the first entry whose condition passes
(`002FAD56`-`002FAE23`):

| Kind | Condition | Test |
|---|---|---|
| `0` | none | always passes (`002FADC5`-`002FADCA`) |
| `1` | story operand | operand bank element *operand* at least the threshold (`002FADD0`-`002FADEC`); no shipped entry uses it |
| `2` | story progress | operand bank element 0 at least the threshold (`002FADF3`-`002FAE0D`) |
| `3` | clan rank | the clan rank at least the threshold (`002FAE14`-`002FAE1F`) |

Kinds 1 and 2 read the story operand bank through `00321190(3, 0, operand)`, a signed 16-bit value; element 0 is
the word at the start of the save payload ([Save data](../Saving-Loading-And-Settings/save-data-fields.md)). When no
entry passes, the last entry of the ladder is returned, so its list is sold anyway (`002FAE21`-`002FAE2D`).

Of the shipped ladders, 43 end in an entry with no condition, two in a story threshold of 0 (Dyce, shops 17 and
18) and the Clan Provisioner's in clan rank 1, which is always met. Eleven end in a story threshold above 0, so a
player below it gets that last list through the fallback: shops 43, 44 and 51 at 500, 21 at 1,580, 22 at 1,982,
26, 27, 48 and 49 at 3,100, and 54 and 55 at 3,250.

### What the menu shows

`002FA920(shop, mode, category, out)` builds the menu's list (`002FA920`-`002FABC3`). In mode 1 it skips the
ladder's entries until it reaches the one `002FAD40` chose, then copies the ids of that list and of every list
after it whose menu category is the one asked for (`002FAA1E`-`002FAB9A`). `002FAD30` is the same call with no
output buffer, used to count. Mode 2 lists the bazaar goods on offer instead (`002FA9C9`-`002FAA1C`).

`002FABD0(id)` gives an id its menu category (`002FABD0`-`002FAD24`):

| Ids | Category |
|---|---|
| equipment of the main-hand slot | 0 |
| equipment of the off-hand, head and body slots, except ammunition | 1 |
| accessories | 2 |
| ammunition, classes 23-26 | 3 |
| items | 4 |
| technicks | 5 |
| magicks | 6 |
| loot | 7 |
| gambits | 9 |

The shop screens `0057B500`, `0057B6F0`, `0057CF20` and `0057D620` call it; the first two pass the shop number
held at byte `+C0`<sub>h</sub> of the shop menu (`0057B5F4`, `0057B715`). `003933D0(id)` answers 1 for categories 0-3,
the equipment; the shop's transaction function `0056D370` asks it (`0056D630`).

### The shop's name

The name id of shop *n* is the first word of its row, returned by `002FAE40(n)` (`002FAE85`-`002FAEA4`). The
script verb `4A9`<sub>h</sub> `setshopname(n)` gives an actor that name (`0034C183`-`0034C18A`), and it is shown through the
NPC-name dictionary `npcdic.bin` ([NPC names](../Characters-And-Objects/npc-names.md)); the shop screens read it too
(`0057B98F`, `0057C022`). A name id's pair has a second name, shown once its persistent flag is set: shops 10,
11 and 23 carry one.

### Clan rank

`00315390` returns the highest rank, 12 down to 1, whose three requirements the player meets
(`003153B5`-`003153E1`): the clan points, achievement counter 17 at `+3868`<sub>h</sub> of the block `002536A0` returns
(`0031539A`-`003153A4`); the count `00316480` returns; and the number of the thirty awards at `+3844`<sub>h</sub> of that
block that are earned, `00316670`. The twelve rows are at `00D105D0`, eight bytes each:

| Rank | Clan points | Count | Awards |
|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 700 | 2 | 0 |
| 3 | 8,000 | 4 | 0 |
| 4 | 20,000 | 8 | 0 |
| 5 | 30,000 | 10 | 0 |
| 6 | 40,000 | 12 | 0 |
| 7 | 100,000 | 14 | 0 |
| 8 | 200,000 | 16 | 0 |
| 9 | 250,000 | 24 | 0 |
| 10 | 300,000 | 28 | 0 |
| 11 | 500,000 | 32 | 0 |
| 12 | 1,000,000 | 44 | 30 |

`00316480` counts the entries of the quest list at `022C2550` whose quest is ordered or cleared and whose
scenario value reaches the entry's minimum (`00316520`-`0031654D`).

### The shipped ladders

The 57 shops hold 267 lists: 45 with no condition, 210 on story progress and 12 on clan rank, all of the
clan-rank lists in shop 2, the Clan Provisioner. The story thresholds run from 0, on two of Dyce's lists, to
5,350. Shops 29-36 share one name, Assistant Storekeeper; the other repeated names are Traveling Merchant (0, 1,
21, 22), Tetran (14, 20) and Dyce (15, 17, 18).

## Columns

`shops.tsv`, one row per stock list, in the order the ladder is walked:

| Column | Meaning |
|---|---|
| `shop` | the shop's row in the table, the number `setshopname` takes |
| `name` | its name from the `us` `npcdic.bin`; "(later X)" gives the second name of the pair |
| `list` | the list's place in the ladder, 0 first |
| `condition` | `none`, `story progress` or `clan rank` |
| `threshold` | the value the condition needs, or `-` |
| `classes` | the kinds of goods in the list |
| `stock_ids` | the list's encoded ids, in order |
| `stock` | their names from the shipped text tables, in the same order |

A list is sold when its own entry or an earlier one in the ladder is the first whose condition the player meets.

## Related

- [Equipment row](equipment-row.md) - the price and the cannot-sell bit of each piece of equipment.
- [NPC names](../Characters-And-Objects/npc-names.md) - where a shop's name is shown from.
- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the operand bank the story conditions read.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the gambits the shops sell.
