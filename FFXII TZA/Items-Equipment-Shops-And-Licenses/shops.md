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
ladder, each ladder's data, each list and each list's data (`0x00238678`-`0x0023881D`).

The slot store is the slot's low 32 bits plus the section, zero-extended (`0x00238678`-`0x00238686`): the section
address while the slot is empty. The three data offsets `+0x08` are rebased only when not 0 (`0x00238698`,
`0x00238739`, `0x002387F8`); each shop's ladder and each ladder row's list are rebased even when 0 (`0x00238726`,
`0x002387E5`).

It has three levels, each
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
(`0x002FAD56`-`0x002FAE23`). The ladder is `0x0020E600(shop +0x04)`: its word `+0x06` counts the entries, its word
`+0x04` is the row size and its dword `+0x08` the offset of the rows (`0x002FAD56`-`0x002FADBF`). A kind above 3 never
passes, and a ladder with no entries gives 0 (`0x002FAD73`-`0x002FAD75`, `0x002FAE0F`-`0x002FAE21`). The thresholds are
compared as signed values (`0x002FADEC`, `0x002FAE0D`, `0x002FAE1F`):

| Kind | Condition | Test |
|---|---|---|
| `0` | no condition | always passes (`0x002FADC5`-`0x002FADCA`) |
| `1` | story operand | operand bank element *operand* at least the threshold (`0x002FADD0`-`0x002FADEC`); no shipped entry uses it |
| `2` | story progress | operand bank element 0 at least the threshold (`0x002FADF3`-`0x002FAE0D`) |
| `3` | clan rank | the clan rank at least the threshold (`0x002FAE14`-`0x002FAE1F`) |

Kinds 1 and 2 read the story operand bank through `0x00321190(3, 0, operand)`, a signed 16-bit value; element 0 is
the main story counter, the word at the start of the save payload ([Story progress](../Story-Events-And-Hunts/story-progress.md), [Save data](../Saving-Loading-And-Settings/save-data-fields.md)). When no
entry passes, the last entry of the ladder is returned, so its list is sold anyway (`0x002FAE21`-`0x002FAE2D`).

Of the shipped ladders, 43 end in an entry with no condition, two in a story threshold of 0 (Dyce, shops 17 and
18) and the Clan Provisioner's in clan rank 1, which is always met. Eleven end in a story threshold above 0, so a
player below it gets that last list through the fallback: shops 43, 44 and 51 at 500, 21 at 1,580, 22 at 1,982,
26, 27, 48 and 49 at 3,100, and 54 and 55 at 3,250.

Story progress is a signed 16-bit value; the values the scripts write in reachable code run from 13 to 7,150 ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), and no story script writes 500 or 960. It goes from 490 (After the captive Penelo) to 520 (After the floating continent), and from 930 (After the Leviathan tutorial) to 966 (After the battle with the lesser judges). The test passes at the threshold or any higher value (`0x002FAE09` `cmp`, `0x002FAE0D` `jge`), so a list that waits on 500 is sold from 520 and one that waits on 960 from 966.

Of the 23 lists at 500 or 960, 17 go on sale at 520. The other six are sold from the start: shop 24's lists 25 (960), 27 and 35 (500) come after its list 15, which has no condition, and the 500 lists of shops 43, 44 and 51 are the last of their ladders. The story test reads story progress only, so no clan rank opens these lists. The `on_sale` column gives the point from which each list is sold.

### What the menu shows

`0x002FA920(shop, mode, category, out)` builds the menu's list (`0x002FA920`-`0x002FABC3`). In mode 1 it skips the
ladder's entries until it reaches the one `0x002FAD40` chose, then copies the ids of that list and of every list
after it whose menu category is the one asked for (`0x002FAA1E`-`0x002FAB9A`). `0x002FAD30` is the same call with no
output buffer, used to count. Mode 2 lists the bazaar goods on offer instead (`0x002FA9C9`-`0x002FAA1C`).

`0x002FABD0(id)` gives an id its menu category (`0x002FABD0`-`0x002FAD24`):

| Ids | Category |
|---|---|
| the empty id `0xFFFF` | -1 |
| equipment of the main-hand slot | 0 |
| equipment of the off-hand, head and body slots, except ammunition | 1 |
| accessories | 2 |
| ammunition, classes 23-26 | 3 |
| items | 4 |
| technicks | 5 |
| magicks | 6 |
| loot | 7 |
| gambit presets, `0x5000`-`0x5FFF` | 8 |
| gambits, the gambit conditions `0x6000`-`0x6FFF` | 9 |
| class 12 ids, `0x7000`-`0x7FFF`, which no table holds | 10 |

The answers come from two eight-entry tables the function builds on its stack (`0x002FABE3`-`0x002FAC14`). An id that
is not equipment takes entry `id >> 12` of the second, 4, -1, 7, 6, 5, 8, 9, 10 (`0x002FAD20`). Equipment takes entry
`slot` of the first, 0, 1, 1, 1, 2 for slots 0-4 (`0x002FAD1A`), the slot being bits `0xE0` of row byte `+7`
(`0x002FAC9D`-`0x002FACA1`); an off-hand row of class 23-26, byte `+9`, answers 3 instead (`0x002FACE1`-`0x002FAD13`).

`0xFFFF` gives -1 (`0x002FAC1A`-`0x002FAC1F`). The categories come from two tables built on the stack. By slot,
`+0x07 >> 5`: 0 for slot 0, 1 for slots 2 and 3, 2 for slot 4, 4 for slot 6 and -1 for slot 7, while slot 1 gives
3 for classes 23-26 and 1 otherwise (`0x002FAC9D`-`0x002FAD1A`). By class nibble: 4, -1, 7, 6, 5, 8, 9 and 10 for
nibbles 0-7 (`0x002FAD20`).

Slot 5 reads the stack dword after the slot table, which the function does not write, and a nibble of 8 or more
reads past the class table into the frame's later slots: the stack cookie copy, the saved `rdi` and the return
address, and for nibbles `0xE` and `0xF` the caller's home space (`0x002FABF8`-`0x002FAC14`, `0x002FAC34`).

`0x002FABD0` is called by the list builder `0x002FA920` (`0x002FAB59`), by `0x003933D0` (`0x003933D4`) and at `0x003F4206`.
The shop screens `0x0057B500`, `0x0057B6F0`, `0x0057CF20` and `0x0057D620` call `0x002FA920` or its counting form `0x002FAD30`
(`0x0057B5F4`, `0x0057B617`, `0x0057B715`, `0x0057B736`, `0x0057CFC4`-`0x0057D07B`, `0x0057D6B4`, `0x0057D6D7`); the first two
pass the shop number held at byte `+0xC0` of the shop menu (`0x0057B5F4`, `0x0057B715`). `0x003933D0(id)` answers 1 for
categories 0-3, the equipment; the shop's transaction function `0x0056D370` asks it (`0x0056D630`).

The id `0x0056D630` gives it is word `+8` of the chosen row (`0x0056D5E8`). The list keeps that row at `+0xD0`: the
row the message's `+0x10` numbers among the tab's rows at `+0xC8` (`0x0056D55D`-`0x0056D56F`), the rows
`0x0057CF20` builds, which `0x0056E410` hands over (`0x0056E535`-`0x0056E55A`). On the Bazaar tab, help kind `0xB`
(`+0xE4` under mask `0x3FC0` equal to `0x2C0`), the id goes to `0x0057A480` instead (`0x0056D604`-`0x0056D61E`);
`0x0056DC30` gives `0xB` only to tab id 0 (`0x0056DC91`), which of the three shop tab lists only the Bazaar's holds
(`0x00D23C60`).

So `0x002FABD0` gets, through `0x003933D0`, the id of a Buy row, one of the stock ids above, or of a Sell row, from the
party's lists 0 to 4 and 11 (items, equipment and loot). The 267 lists hold 2,512 ids, all of nibbles 0, 1, 2, 3, 4
and 6, and the 557 rows of the equipment table carry slots 0 to 4 only, so neither the unwritten slot 5 dword nor
the reads past the class table are reached from here. Key items, `0x8000`-`0x81FF`, have list 10 of their own,
which `0x0057CF20` reads only for the Inventory's Key Items, kind 7 (`0x0057D0E9`-`0x0057D103`), never for a shop tab.

### The shop's name

The name id of shop *n* is the first word of its row, returned by `0x002FAE40(n)` (`0x002FAE85`-`0x002FAEA4`). The
script verb `0x4A9` `setshopname(n)` gives an actor that name (`0x0034C183`-`0x0034C18A`), and it is shown through the
NPC-name dictionary `npcdic.bin` ([NPC names](../Characters-And-Objects/npc-names.md)); the shop screens read it too
(`0x0057B98F`, `0x0057C022`). A name id's pair has a second name, shown once its story flag in Bank2048 is set ([Story flags](../Story-Events-And-Hunts/story-flags.md)): shops 10,
11 and 23 carry one.

For a shop number not below the row count `+0x06` of `[0x02EBF158]`, or with no shop table bound, `0x002FAE40` returns
0 (`0x002FAE4A`-`0x002FAE66`).

### Clan rank

`0x00315390` returns the highest rank, 12 down to 1, whose three requirements the player meets
(`0x003153B5`-`0x003153E1`): the clan points, achievement counter 17 at `+0x3868` of the block `0x002536A0` returns
(`0x0031539A`-`0x003153A4`); the count `0x00316480` returns; and the number of the thirty awards at `+0x3844` of that
block that are earned, `0x00316670`. The twelve rows are at `0x00D105D0`, eight bytes each; the word at `+0x06` is the rank's name, which `0x003153F0(rank)` resolves through `0x002F9860` (`0x003153FF`-`0x0031540A`); `0x0056F470` passes it the rank `0x00315390` returns (`0x0056F482`, `0x0056F4AE`):

| Rank | Name | Clan points | Count | Awards |
|---:|---|---:|---:|---:|
| 1 | Moppet | 0 | 0 | 0 |
| 2 | Hedge Knight | 700 | 2 | 0 |
| 3 | Rear Guard | 8,000 | 4 | 0 |
| 4 | Vanguard | 20,000 | 8 | 0 |
| 5 | Headhunter | 30,000 | 10 | 0 |
| 6 | Ward of Justice | 40,000 | 12 | 0 |
| 7 | Brave Companion | 100,000 | 14 | 0 |
| 8 | Riskbreaker | 200,000 | 16 | 0 |
| 9 | Paragon of Justice | 250,000 | 24 | 0 |
| 10 | High Guardian | 300,000 | 28 | 0 |
| 11 | Knight of the Round | 500,000 | 32 | 0 |
| 12 | Order of Ambrosia | 1,000,000 | 44 | 30 |

`0x00316480` counts the entries of the quest list at `0x022C2550` whose quest is ordered or cleared and whose
scenario value reaches the entry's minimum (`0x00316520`-`0x0031654D`).

What each rank brings is in [`clan-ranks.tsv`](clan-ranks.tsv). Montblanc's talk in The Clan Hall (Rabanastre) (`rbn_a14`) gives reward package `0x902E` plus the rank for each rank reached since the last one he rewarded ([Reward package list](../Rewards-EXP-Gil-And-Loot/reward-package-list.md)). The Clan Provisioner, shop 2, sells list 12 minus the rank and every list after it. The clan boards and Montblanc post the hunts whose rank test the rank meets ([Hunts](../Story-Events-And-Hunts/hunts.md)).

### The shipped ladders

The 57 shops hold 267 lists: 45 with no condition, 210 on story progress and 12 on clan rank, all of the
clan-rank lists in shop 2, the Clan Provisioner. The story thresholds run from 0, on two of Dyce's lists, to
5,350. Shops 29-36 share one name, Assistant Storekeeper; the other repeated names are Traveling Merchant (0, 1,
21, 22), Tetran (14, 20) and Dyce (15, 17, 18).

### Where each shop is

A shop is opened for the player in one of two ways, both from the zone script of its map:

- the vendor actor's script calls `setshopname` with the shop's number, directly or through a list whose elements carry `0x1000` + the shop (an actor that reads such a list calls `setnpcname` for an element below `0x1000` and `setshopname` with the low 12 bits of any other);
- the talk that sells calls `openfullscreenmenu_48d(2, shop)` (verb `0x48D`, `0x003462D0`), which opens the shop screen on that shop.

`place` gives the map (region) and script of each zone script that does either. Every one of the 57 shops has one; the Street Vendor's shop 13 and Dyce's shop 18 have two. Shop 16, the Baknamy Merchant, is opened only by the second route: in Cloister of the Highborn (Necrohol of Nabudis) the Baknamy merchant actor of `bds_b01` opens it (`openfullscreenmenu_48d(2, 16)`) after the party is placed before it, and is never given a shop name.

The Clan Provisioner's actor in Muthru Bazaar (Rabanastre) is a Mysterious Merchant until bit `0x1` of script global byte `0x041D` is set, and takes the shop's name only after that (`rbn_a02`). Montblanc sets the bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`). The shop's rank-1 list is therefore on sale from joining the clan.

## Columns

[`shops.tsv`](shops.tsv), one row per stock list, in the order the ladder is walked:

| Column | Meaning |
|---|---|
| `shop` | the shop's row in the table, the number `setshopname` takes |
| `name` | its name from the `us` `npcdic.bin`; "(later X)" gives the second name of the pair |
| `list` | the list's place in the ladder, 0 first |
| `condition` | `no condition`, `story progress` or `clan rank` |
| `threshold` | the value the condition needs, or `-` |
| `classes` | the kinds of goods in the list |
| `stock_ids` | the list's encoded ids, in order |
| `stock` | their names from the shipped text tables, in the same order |
| `place` | the map (region) and script whose script gives an actor the shop ("Where each shop is" above), `or` between two |
| `on_sale` | the point from which the list is sold: from the start, from a clan rank, or from a story progress value with the story point that first meets it ("Choosing a list" above) |

A list is sold when its own entry or an earlier one in the ladder is the first whose condition the player meets.

[`clan-ranks.tsv`](clan-ranks.tsv), one row per clan rank ("Clan rank" above):

| Column | Meaning |
|---|---|
| `rank` | the rank, 1 to 12 |
| `name` | its name |
| `clan_points`, `hunt_count`, `awards` | the clan points, the count `0x00316480` returns and the earned awards the rank needs |
| `reward_package` | the package Montblanc gives for reaching the rank |
| `reward` | what the package gives |
| `provisioner_list` | the Clan Provisioner's list (shop 2) the rank opens |
| `provisioner_stock` | that list's stock; the lists of the lower ranks stay on sale |
| `hunts` | the hunts whose rank test is this rank, with who posts each and from which story progress, or `-` when no hunt tests this rank |

## Related

- [Equipment row](equipment-row.md) - the price and the cannot-sell bit of each piece of equipment.
- [NPC names](../Characters-And-Objects/npc-names.md) - where a shop's name is shown from.
- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the operand bank the story conditions read.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the gambits the shops sell.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Core runtime: `0x003462D0` calls `0x00229EB0`; those functions are documented on
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
