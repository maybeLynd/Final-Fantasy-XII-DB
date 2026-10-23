---
title: "Shops: every shop with its name, its stock lists and the story or clan-rank condition that opens each list"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF158, 0x00238660, 0x002FAD40, 0x002FA920, 0x002FAE40, 0x002FABD0, 0x00315390"
---

## What it lists

A shop's stock is a ladder of lists, most advanced first. The menu finds the first list whose condition the
player meets and sells that list together with every list after it, so a shop's stock grows as the story goes
on or the clan rank rises.

### The table

The shop table is section 39 of `battle_pack.bin`, the section its directory entry at file offset `+0xA0` points
to. The battle data binder hands it to `0x00238660` (`0x00236F28`-`0x00236F2E`), which stores the section address in
the registry slot `0x02EBF158` and adds it to every offset in the table: the header's data offset, each shop's
ladder, each ladder's data, each list and each list's data (`0x00238678`-`0x0023881D`). It has three levels, each
with the same 12-byte header, `ShopLevelHeader`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | tag | `0x64` shops, `0x164` ladders, `0x264` lists |
| `+0x04` | `u16` | stride | bytes per row |
| `+0x06` | `u16` | count | rows |
| `+0x08` | `u32` | data | offset of the first row, made an address by `0x00238660` |

A shop row, 8 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | name | the shop's name id |
| `+0x02` | `u8[2]` | pad | read and written by no function: `0x02EBF158` is loaded only by `0x00238660`, which rebases the offsets, `0x002FA920` and `0x002FAE40`, and no instruction of those three or of the ladder walker `0x002FAD40` reads or writes a shop row's `+0x02`. The word reads of `+0x02` in `0x002FAD40` (`0x002FADE4`, `0x002FAE05`, `0x002FAE19`) are of a ladder row's threshold: their base is the ladder's data plus the entry index times the ladder's row size (`0x002FAD90`-`0x002FADBF`). Nothing fixes the width of the shop row's `+0x02` |
| `+0x04` | `u32` | ladder | offset of the shop's ladder |

A ladder row, 8 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | kind | condition kind |
| `+0x01` | `u8` | operand | condition operand |
| `+0x02` | `u16` | threshold | condition threshold, read by `0x002FAD40` (`0x002FADE4`, `0x002FAE05`, `0x002FAE19`) |
| `+0x04` | `u32` | list | offset of the list the rung selects |

A list row is one `u16`, an encoded id: `0x0xxx` item, `0x1xxx` equipment, `0x2xxx` loot, `0x3xxx` magick, `0x4xxx`
technick, `0x6xxx` gambit.

### Choosing a list

`0x002FAD40(shop)` walks the shop's ladder in order and returns the first entry whose condition passes
(`0x002FAD56`-`0x002FAE23`):

| Kind | Condition | Test |
|---|---|---|
| `0` | none | always passes (`0x002FADC5`-`0x002FADCA`) |
| `1` | story operand | operand bank element *operand* at least the threshold (`0x002FADD0`-`0x002FADEC`); no shipped entry uses it |
| `2` | story progress | operand bank element 0 at least the threshold (`0x002FADF3`-`0x002FAE0D`) |
| `3` | clan rank | the clan rank at least the threshold (`0x002FAE14`-`0x002FAE1F`) |

Kinds 1 and 2 read the story operand bank through `0x00321190(3, 0, operand)`, a signed 16-bit value; element 0 is
the word at the start of the save payload ([Save data](../Saving-Loading-And-Settings/save-data-fields.md)). When no
entry passes, the last entry of the ladder is returned, so its list is sold anyway (`0x002FAE21`-`0x002FAE2D`).

Of the shipped ladders, 43 end in an entry with no condition, two in a story threshold of 0 (Dyce, shops 17 and
18) and the Clan Provisioner's in clan rank 1, which is always met. Eleven end in a story threshold above 0, so a
player below it gets that last list through the fallback: shops 43, 44 and 51 at 500, 21 at 1,580, 22 at 1,982,
26, 27, 48 and 49 at 3,100, and 54 and 55 at 3,250.

### What the menu shows

`0x002FA920(shop, mode, category, out)` builds the menu's list (`0x002FA920`-`0x002FABC3`). In mode 1 it skips the
ladder's entries until it reaches the one `0x002FAD40` chose, then copies the ids of that list and of every list
after it whose menu category is the one asked for (`0x002FAA1E`-`0x002FAB9A`). `0x002FAD30` is the same call with no
output buffer, used to count. Mode 2 lists the bazaar goods on offer instead (`0x002FA9C9`-`0x002FAA1C`).

`0x002FABD0(id)` gives an id its menu category (`0x002FABD0`-`0x002FAD24`):

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

The shop screens `0x0057B500`, `0x0057B6F0`, `0x0057CF20` and `0x0057D620` call it; the first two pass the shop number
held at byte `+0xC0` of the shop menu (`0x0057B5F4`, `0x0057B715`). `0x003933D0(id)` answers 1 for categories 0-3,
the equipment; the shop's transaction function `0x0056D370` asks it (`0x0056D630`).

### The shop's name

The name id of shop *n* is the first word of its row, returned by `0x002FAE40(n)` (`0x002FAE85`-`0x002FAEA4`). The
script verb `0x4A9` `setshopname(n)` gives an actor that name (`0x0034C183`-`0x0034C18A`), and it is shown through the
NPC-name dictionary `npcdic.bin` ([NPC names](../Characters-And-Objects/npc-names.md)); the shop screens read it too
(`0x0057B98F`, `0x0057C022`). A name id's pair has a second name, shown once its persistent flag is set: shops 10,
11 and 23 carry one.

### Clan rank

`0x00315390` returns the highest rank, 12 down to 1, whose three requirements the player meets
(`0x003153B5`-`0x003153E1`): the clan points, achievement counter 17 at `+0x3868` of the block `0x002536A0` returns
(`0x0031539A`-`0x003153A4`); the count `0x00316480` returns; and the number of the thirty awards at `+0x3844` of that
block that are earned, `0x00316670`. The twelve rows are at `0x00D105D0`, eight bytes each:

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

`0x00316480` counts the entries of the quest list at `0x022C2550` whose quest is ordered or cleared and whose
scenario value reaches the entry's minimum (`0x00316520`-`0x0031654D`).

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
