[Home](../../README.md) / [World, areas and travel](README.md) / Treasure chests

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Treasure chests: where each chest stands, whether it appears and comes back, and what it holds with the odds of each content | system | World, areas and travel | Chests, traps and weather | Every treasure chest the game ships: how a zone script binds a chest to its 24-byte record, the presence roll when a chest is set out and the opened flag that keeps a one-time chest away, the payout roll when the chest is opened (gil or one of two items, with the Treasure Hunter set the Diamond Armlet unlocks), the chests that share a flag, counts of the shipped chests by region, and the list of all 1,966 with map, region, place, flag, chance and every possible content with its odds. | 0x00354400, 0x00354A40, 0x00355210, 0x002650B0, 0x00265155, 0x002FAED0, 0x002FAF60, 0x002FAFD0, 0x002FB430, 0x002F7FA0, 0x002FA470, 0x0050FAF0, 0x00355830, 0x00356570, 0x0050F850, 0x0023B2A0, 0x0032AA60, 0x0032AD70, 0x00353750, 0x00353BD0, 0x00354540, 0x002F8060, 0x003272A0, 0x00379CD0, 0x00300B80, 0x003004B0, 0x003148F0, 0x02EC3E60 |

## What the player sees

A chest stands at a fixed spot on its map, facing a fixed way. Some chests are always there; most are there only
some of the time, and whether a chest is there is decided each time the game sets the chest out. Opening a chest
gives either some gil or one item, and which of these it gives is decided at the moment it is opened, not when the
chest is set out.

There are two kinds of chest:

- **Chests that come back.** Most chests have no flag and can be opened again on a later visit: each time the game
  sets the chest out it has the same chance of being there, whether or not it was opened before, and each opening
  rolls its contents afresh.
- **One-time chests.** A chest with a flag disappears for good once it has been opened. Until then it is rolled each
  time it is set out, like the others; once opened, it never appears again in that save.

The party leader's gear matters when a chest is opened. With the Diamond Armlet (the one piece of gear with the
Treasure Hunter augment) on the leader, a chest that gives an item picks from a second pair of items with different
odds, and a chest that gives gil can give a different amount. Many rare weapons only come from that second set:
the Seitengrat, for example, is a 1% chance in a chest on the Skyferry's Air Deck that is itself there 1% of the
time, and only with the armlet.

Every chest the game ships is listed in [the treasure chest list](treasure-chest-list.tsv): its map and region,
where it stands, whether it comes back, how likely it is to be there, and everything it can hold with the odds of
each, with and without the armlet. [The contents list](treasure-chest-contents.tsv) has the same contents one line
per possible content, for searching by item.

## How it works

### Binding a chest to its record

Each chest is one actor of a zone script, named `treasure_00`, `treasure_01` and so on. Its `init` function calls
four verbs, always the same ones:

```
setuptreasure(ref); npc_to_gimmick(); btlAtelTreasureInitWithRange(0.5, n); setnpcname(name);
```

and its talk function runs the opening sequence that
[reward verbs](../Scripts-And-Script-Commands/reward-verbs.md) gives (`talktreasure(ref)`,
`btlAtelOpenTreasureMessage(ref)`, `talktreasureafter(ref)` with the same `ref`). In the decompiled `us` scripts, `n`
is 5 in 1,826 of the 1,966 `btlAtelTreasureInitWithRange` calls, 1 in 110, 2 in 18, 0 in 5, 3 in 3, 4 in 3 and 50
in 1.

`ref` is a packed reference taken from the script's int pool (`PUSHI`):

- the resolver `0x002650B0` switches on bits `0x7000000` through the table at `0x00265180`;
- every shipped chest uses tag 3, which `0x00265155` resolves to the image plus the image's msp-area offset (header
  `+0x40`) plus the low 24 bits ([section 000 of the script
  container](../EBP-Script-Files/ebp-script-image.md));
- `setuptreasure`'s begin `0x00354400` resolves it at `0x0035444C` and the payout verb's begin `0x0050FAF0` at
  `0x0050FB25`, each against the script that is running the chest's function.

The record is 24 bytes (see Layouts). `btlAtelTreasureInitWithRange` (`0x0050F850` → `0x0023B2A0`) only sets the
chest actor's talk and touch ranges
([movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md)); it reads no
record field.

### When a chest is set out

A chest is set out each time its zone script starts. All 1,966 `setuptreasure` steps of the `us` zone scripts stand
in a chest actor's `init` with no condition before them. No step of a chest actor tests a condition, and no step of
another actor names a chest actor (the steps tables of the area script pages, for example
[Giza Plains scripts](../Story-Events-And-Hunts/giza-plains-scripts.md)). So a
chest has no story condition of its own: the story decides it through when its zone can be entered, and then the
opened flag and the presence roll below decide whether the chest is there.

### Is the chest there: the presence roll

`setuptreasure` hides the actor, takes the chest model from the map header and rolls through `0x002FAED0`
([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md) has the placement):

| Step | What happens | Where in the code |
|---|---|---|
| 1 | When the opened flag `record[+0x09]` is set (`0x0032AA60`, bit *n* of the 256-bit chest and trap set at `+0x14B4` of the save payload, the first half of Bank512 of the [Story flags](../Story-Events-And-Hunts/story-flags.md)), there is no chest. | `0x002FAEE2`-`0x002FAEF0` |
| 2 | Otherwise a chest when `draw % 100 < record[+0x0A]`, the draw coming from the gameplay Mersenne Twister `0x00379CD0` ([which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md)). | `0x002FAEF2`-`0x002FAF1F` |

With no chest the model is set to −1 and the actor stays hidden. The actor also stays hidden when the map header gives
no model, since the begin `0x00354400` then leaves `args[0]` at 0¹ and the result returns when
`args[0]` does not resolve ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)). With a
chest and a model the result `0x00355210` shows it, places it at `(x / 10, 0, z / 10)` from `+0x04` and `+0x06` and
faces it by the low six bits of `+0x08` in 6° steps².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00354469`, `0x00354480` |
| ² | `0x002FAF60` |

</details>

A flag byte of `0xFF` means no flag: `0x0032AA60` then tests flag 255 of the story-flag set, which nothing in shipped
play sets.

- The setter `0x0032AD70` has four callers: the trap firing `0x002F8060` and the payout `0x002FAFD0`, both of which skip
  `0xFF`¹, and the verbs `settreasurebattleflag` and `releasetreasurebattleflag`
 ², which no shipped script calls.
- The getter `0x0032AA60` has three callers: the trap arming `0x002FA740`, this presence roll, and the verb
  `istreasurebattleflag`³, which no shipped script calls either. The trap arming skips the test for flag
  `0xFF`, which every shipped trap has ([traps](traps.md)), so in shipped play a bit of this set is tested only
  when a chest is placed.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F8247`, `0x002FAFF0` |
| ² | `0x00353750`, `0x00353BD0` |
| ³ | `0x00354540` |

</details>

Both outcomes of the roll are written to the presence ledger (`0x002FB430`, a ring of three
`{field, value bits, mask bits}` entries at `0x02EC3E60`), but nothing reads that ledger to decide presence:

- the ring's address is formed only in the clear `0x002FA260`, in `0x002FA470` (an entry for the field being left), in
  this roll and in the payout `0x002FAFD0`;
- it is handed only to `0x002FB430` and the reorder `0x002F7FA0`, which keep no copy of it, and the image holds no
  absolute or image-relative copy of it.

The clear `0x002FA260` zeroes the ledger with 8-byte stores at `0x02EC3E60`, `0x02EC3E68`, `0x02EC3E70`, `0x02EC3E78` and
`0x02EC3E80` and a 4-byte store at `0x02EC3E88`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FA262`-`0x002FA285` |

</details>

`0x002FB430(ring, field, bit, value)` looks for the field among the first count entries. When it finds it, it
sets mask bit `1 << bit` and replaces that value bit with `value`¹. When it does not, it
takes the entry at the cursor: it stores the field, sets the mask to `1 << bit` alone and ORs `value << bit` into
the value bits, so the replaced entry's other value bits stay².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FB4D0`-`0x002FB4F6` |
| ² | `0x002FB460`-`0x002FB499` |

</details>

It then moves the cursor on modulo 3 and raises the count, capped at 3: the cursor `+0x24 = (+0x24 + 1) % 3` and
the count `+0x28 = min(+0x28 + 1, 3)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FB49C`-`0x002FB4C2` |

</details>

`0x002FA470` adds its entry only when no entry below the count holds field `0x022BE940`¹; it
then stores mask `0xFF`, value 0 and the field at the cursor and moves the cursor and count the same way². Both paths end in a jump to `0x002F7FA0(ring, 0x022BE940)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FA490`-`0x002FA493` |
| ² | `0x002FA4AA`-`0x002FA50E` |
| ³ | `0x002FA51A` |

</details>

`0x002F7FA0(ring, field)` takes the entries below the count in index order. For each whose field matches, it
swaps that entry with the entry one place after it and then two places after it, modulo 3, `j = (i + k) % 3` for
`k = 1, 2`, stopping at an index that is the cursor or at or past the count, `j == +0x24` or `j >= +0x28`¹. An entry moved to a later index is tested
again when the walk reaches it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F7FC0`-`0x002F8036` |

</details>

So `setuptreasure` rolls a chest whose flag is clear every time it runs, and nothing in the chest code carries an
earlier roll or opening into that roll.

### What the chest holds: the payout roll

Opening runs `0x002FAFD0` from `btlAtelOpenTreasureMessage`:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The opened flag is set first, unless it is `0xFF`, and the ledger is marked. | `0x002FAFEA`-`0x002FAFFD` |
| 2 | A first draw: `draw % 100 < record[+0x0B]` gives gil, anything else an item. | `0x002FB01D`-`0x002FB03D` |
| 3 | The Treasure Hunter test (`0x002FB03F`-`0x002FB067` for gil, `0x002FB0C3`-`0x002FB0EB` for items): the party leader exists, holds none of KO, Stone and X-Zone (`0x80000003` in its status words `+0x64 \| +0x3C`, [statuses](../Status-Effects-And-KO/statuses.md)) and has augment 25, Treasure Hunter, in either augment layer (bit `0x2` of `+0x6B` or `+0x7B`, [augments](../Damage-And-Battle-Formulas/augments.md)). | `0x003272A0` |
| 4 | Gil: the word `+0x16` with Treasure Hunter, `+0x14` without. With bit `0x40` of `+0x08` the amount is `draw % word + 1`, from 1 to the word; otherwise it is the word. A word of 0 gives nothing. | `0x002FB082`-`0x002FB090` |
| 5 | Item: a second draw `% 100`. With Treasure Hunter, below 95 gives `+0x10`, otherwise `+0x12`; without it, below 50 gives `+0x0C`, otherwise `+0x0E`. `0xFFFF` gives nothing; any other id gives one. |   |

The status words and augment bytes of step 3 are those of the record at the leader's `+0x698`, which both arms load
first (`0x002FB049` for gil, `0x002FB0CD` for items).

The verb then grants the item through `0x00300B80(item, 1, 0)`¹ or the gil through `0x003004B0(gil, 0)`², after adding the matching entry to its message record³; when the roll gave nothing it adds
no entry and grants nothing⁴, and on every path it shows the message record⁵
([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0050FBA0` |
| ² | `0x0050FB76` |
| ³ | `0x0035E500` |
| ⁴ | `0x0050FB5A` |
| ⁵ | `0x0035DF40`, `0x0050FBA8` |

</details>

So for a chest with gil chance *g*, the odds are *g*% gil and (100 − *g*)% an item. Without the armlet the two
items split the item share 50/50; with it, 95/5 between the two Treasure Hunter items. The gil chance is the same
either way. The armlet does not change whether a chest is there, only what an opened chest gives.

The Diamond Armlet is the only row of the [equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md)
whose augment is Treasure Hunter, and no licence and no character row grants it
([augment list](../Damage-And-Battle-Formulas/augment-list.md)).

### Chests that share a flag

Sixteen flags are on more than one chest. Every chest in these groups is always there until its flag is set, and
each holds one fixed content.

#### One flag, several chests on one map

Opening any of them sets the flag for all of them. They stay where they are
until the map is next loaded, and the payout does not test the flag, so the others still open as usual; from the
next load none of them appears.

| Flag | Map | Region | Chests and contents |
|---|---|---|---|
| 181 | Terminus No. 7 | Barheim Passage | Reverse Mote, Elixir |
| 190 | Gate of Wind | Giruvegan | Reverse Mote, Hastega Mote |
| 200 | Hall of Shadowlight | Sochen Cave Palace | X-Potion, Elixir, Bubble Mote, Cura Mote, Phoenix Down |
| 202 | Hall of Worth | Stilshrine of Miriam | Elixir, Bubble Mote |
| 206 | Walk of Sky | Stilshrine of Miriam | Tourmaline Ring, Tourmaline Ring |
| 211 | Southern Sluiceway | Garamsythe Waterway | Hi-Potion, Phoenix Down |
| 213 | Large Freight Stores | Dreadnought Leviathan | Reflectga Mote, Reflectga Mote |
| 217 | Hall of the Wroth God | Sochen Cave Palace | Reverse Mote, Bubble Mote, Hastega Mote |
| 220 | Energy Transitarium | Draklor Laboratory | Hastega Mote, Holy Mote |

#### One flag on two maps

Both chests hold the same thing; opening either one keeps the other away for good.

| Flag | Content | First map | Second map |
|---|---|---|---|
| 2 | Silence | Yardang Labyrinth (Dalmasca Estersand) | Shaft Entry (Lhusu Mines) |
| 4 | Sleep | Platform 1 - East Tanks (Ogir-Yensa Sandsea) | Starboard Section (Dreadnought Leviathan) |
| 9 | Regen | The Lost Way (Tchita Uplands) | Nomad Village (Giza Plains) |
| 36 | Infuse | Platform 1 - East Tanks (Ogir-Yensa Sandsea) | Sub-control Room (Dreadnought Leviathan) |
| 47 | Gil Toss | Rm 7002 East (Draklor Laboratory) | Station of Ascension (Pharos - Second Ascent) |
| 92 | Claymore | Rm 6711 West (Draklor Laboratory) | South Liavell Hills (Cerobi Steppe) |
| 120 | Makara | Phase 2 Dig (Henne Mines) | Phase 2 Shaft (Henne Mines) |

## Layouts

<details>
<summary>Show the memory layouts</summary>

Struct ChestRecord base=mspArea+refOffset size=`0x18`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | index | the chest's bit in the presence ledger (`0x002FAF14`, `0x002FB00F`) |
| `+0x01` | `u8[3]` | zero | 0 in every shipped record |
| `+0x04` | `i16` | x | tenths of a world unit (`0x002FAF60`) |
| `+0x06` | `i16` | z | tenths of a world unit; the record holds no height |
| `+0x08` | `u8` | facingFlags | mask `0x3F` facing in 6-degree steps; bit `0x40` random gil (`0x002FB07C`); bit `0x80` 0 in every record |
| `+0x09` | `u8` | flagId | opened flag, set on opening and tested at placement; `0xFF` = no flag (`0x002FAEE2`, `0x002FAFEA`) |
| `+0x0A` | `u8` | presence | percent; draw % 100 below it places the chest (`0x002FAF0D`) |
| `+0x0B` | `u8` | gilChance | percent; draw % 100 below it gives gil, otherwise an item (`0x002FB036`) |
| `+0x0C` | `u16` | item1 | given when the second draw % 100 is below 50 (`0x002FB103`) |
| `+0x0E` | `u16` | item2 | given otherwise (`0x002FB109`) |
| `+0x10` | `u16` | thItem1 | with Treasure Hunter, given below 95 (`0x002FB0F2`) |
| `+0x12` | `u16` | thItem2 | with Treasure Hunter, given otherwise (`0x002FB0F8`) |
| `+0x14` | `u16` | gil | the amount, or its upper bound with bit `0x40` of `+0x08`; 0 = nothing (`0x002FB06F`) |
| `+0x16` | `u16` | thGil | the same with Treasure Hunter (`0x002FB069`) |

Struct PresenceLedger base=`0x02EC3E60` size=`0x2C`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | field0 | the field of entry 0 |
| `+0x04` | `u32` | value0 | bit i: 1 when chest i was placed, 0 when it was not placed or has been opened (`0x002FB4F6`); an entry `0x002FB430` takes over ORs the new bit in, keeping the replaced entry's bits (`0x002FB488`) |
| `+0x08` | `u32` | mask0 | bit i = chest i has a value (`0x002FB430`) |
| `+0x0C` | `i32` | field1 |  |
| `+0x10` | `u32` | value1 |  |
| `+0x14` | `u32` | mask1 |  |
| `+0x18` | `i32` | field2 |  |
| `+0x1C` | `u32` | value2 |  |
| `+0x20` | `u32` | mask2 |  |
| `+0x24` | `i32` | cursor | next entry to fill, 0 to 2 |
| `+0x28` | `i32` | count | entries in use, at most 3 |

```python
placed = !flag(rec.flagId) && mt() % 100 < rec.presence            (flag(0xFF) tests bit 255)
th = leader && !(leader.status & (KO | Stone | X-Zone)) && augment(leader, 25)
gives gil = mt() % 100 < rec.gilChance
gil = rec.randomGil ? mt() % (th ? rec.thGil : rec.gil) + 1 : (th ? rec.thGil : rec.gil)
item = th ? (mt() % 100 < 95 ? rec.thItem1 : rec.thItem2) : (mt() % 100 < 50 ? rec.item1 : rec.item2)
```

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

### The chest list

[treasure-chest-list.tsv](treasure-chest-list.tsv) has one line for each of the 1,966 chests, in field order, then
script, then record. 1,926 stand on 382 maps; the other 40 are in three scripts that no field's zone-script entry
(resource kind 5, index 3*n*, which the area loader `0x0032FCA0` loads for field *n*) names, so no field loads them:
`bts_z01` (16 chests, each there 1% of the time with Cura or Dark Energy), `pre_a01` and `pre_b01` (12 each, always
there, with a fixed consumable).

| Column | Meaning |
|---|---|
| `zone`, `zone_name` | the field number *n* whose zone script holds the chest, and the script's name; `zone` is `-` for the three scripts no field loads |
| `map_name`, `region` | the map's name (`0x00377B60`) and its region's name (`0x003778B0`), as [Zone asset list](zone-asset-list.md) gives them; `-` for the three scripts no field loads |
| `script`, `actor` | the zone script in the archive and the chest's actor in it |
| `record`, `index` | the record's offset in the script image, and its byte `+0x00` |
| `x`, `z`, `facing` | `+0x04` and `+0x06` divided by ten, `+0x04 / 10` and `+0x06 / 10`, in world units, and the facing code, mask `0x3F` of `+0x08`, in 6° steps, `(+0x08 & 0x3F) * 6` degrees |
| `flag_id`, `comes_back` | `+0x09`, and `yes` for `0xFF` (no flag: the chest can be there again after it has been opened), `no` for a one-time chest |
| `presence` | `+0x0A`, the percent chance the chest is there each time it is set out |
| `gil_chance` | `+0x0B`, the percent chance an opening gives gil instead of an item |
| `item_1`, `item_1_name`, `item_2`, `item_2_name` | `+0x0C` and `+0x0E` and their names: the two items without Treasure Hunter, 50% each of the item share |
| `gil`, `random_gil` | `+0x14`, and `yes` when bit `0x40` of `+0x08` makes the amount 1 to that many |
| `th_item_1`, `th_item_1_name`, `th_item_2`, `th_item_2_name`, `th_gil` | `+0x10`, `+0x12` and `+0x16`: the same with Treasure Hunter, the items 95% and 5% of the item share |
| `contents` | every possible content of an opening without Treasure Hunter, with its odds |
| `contents_treasure_hunter` | the same with Treasure Hunter on the leader, or `the same` |
| `explanation` | a one-line summary |

Item names are the shipped English names of the id's table (items, equipment, loot, magicks and technicks,
[item and ability ids](../Engine-Core/item-and-ability-ids.md)). The odds are the authored percents of
the record; two contents that are the same thing are merged into one with the summed odds.

### The contents list

[treasure-chest-contents.tsv](treasure-chest-contents.tsv) has one line per chest, branch and content: 9,212 lines.

| Column | Meaning |
|---|---|
| `zone`, `zone_name`, `map_name`, `region`, `actor`, `record` | the chest, as in the chest list |
| `branch` | `normal`, or `treasure hunter` for the leader with augment 25 |
| `odds` | the chance an opening of this chest gives this content |
| `kind` | `item`, `gil` or `nothing` |
| `id`, `gil` | the item id, or the gil amount (`1-N` for a random amount) |
| `content` | the item's name, the gil in words, or `nothing` |

### The chests by region

| Region | Chests | Maps | One-time | Region | Chests | Maps | One-time |
|---|---:|---:|---:|---|---:|---:|---:|
| Trial Mode | 250 | 100 | 0 | Pharos - Subterra | 36 | 6 | 7 |
| Cerobi Steppe | 101 | 7 | 3 | Pharos - Second Ascent | 34 | 5 | 10 |
| Phon Coast | 96 | 9 | 16 | Ridorana Cataract | 29 | 4 | 3 |
| Tchita Uplands | 91 | 9 | 3 | The Great Crystal | 28 | 17 | 17 |
| Giza Plains | 87 | 14 | 2 | The Tomb of Raithwall | 23 | 4 | 8 |
| Barheim Passage | 78 | 14 | 11 | Stilshrine of Miriam | 22 | 8 | 11 |
| Dalmasca Estersand | 71 | 7 | 4 | Golmore Jungle | 21 | 7 | 2 |
| Lhusu Mines | 67 | 14 | 23 | Dreadnought Leviathan | 20 | 4 | 4 |
| The Feywood | 67 | 8 | 8 | Old Archades | 20 | 2 | 0 |
| Henne Mines | 61 | 6 | 20 | Nalbina Dungeons | 17 | 3 | 3 |
| Ogir-Yensa Sandsea | 56 | 7 | 4 | Pharos - Third Ascent | 15 | 3 | 8 |
| Paramina Rift | 56 | 8 | 3 | Draklor Laboratory | 14 | 5 | 4 |
| Nam-Yensa Sandsea | 52 | 7 | 4 | Giruvegan | 14 | 5 | 8 |
| Sochen Cave Palace | 51 | 9 | 15 | Lowtown | 11 | 2 | 0 |
| The Salikawood | 50 | 9 | 1 | Royal Palace | 7 | 2 | 7 |
| Garamsythe Waterway | 49 | 11 | 7 | Balfonheim Port | 6 | 4 | 1 |
| Ozmone Plain | 49 | 7 | 0 | Sky Fortress Bahamut | 4 | 2 | 4 |
| Dalmasca Westersand | 46 | 5 | 2 | Eruyt Village | 3 | 2 | 1 |
| Mosphoran Highwaste | 46 | 9 | 9 | Jahara | 2 | 1 | 1 |
| Zertinan Caverns | 46 | 9 | 4 | Nalbina Fortress | 2 | 1 | 0 |
| Necrohol of Nabudis | 45 | 8 | 12 | Archades | 1 | 1 | 0 |
| Nabreus Deadlands | 44 | 7 | 8 | Mt Bur-Omisace | 1 | 1 | 0 |
| Pharos - First Ascent | 36 | 8 | 15 | Skyferry | 1 | 1 | 0 |

A map here is a field the area loader enters; a place with several versions (Giza Plains in its two seasons, for
example) counts each version.

### The records

Over the 1,114 `us` zone and event scripts (one file is not an `EBP2` container), 385 carry chests, with 1,966
chest actors and 1,966 distinct records; every chest verb is called 1,966 times, once per chest. The other language
copies of the 385 scripts hold the same records byte for byte.

| Fact | Value |
|---|---|
| one-time chests (a flag below `0xFF`) | 273, all on maps; 237 of them always there until opened |
| chests that come back (`0xFF`) | 1,693 (1,653 on maps) |
| distinct flags | 253; sixteen of them on more than one chest (36 chests) |
| always there (presence 100) | 531 (507 on maps) |
| presence below 50 | 256 on maps; the lowest is 1, in 21 chests (16 of them in `bts_z01`) |
| never gil (gil chance 0) | 580; always gil (100): 13 |
| random gil amount (bit `0x40`) | 1,875; fixed amount 91; the largest word 65,000 |
| contents different with Treasure Hunter | 1,663 (1,647 on maps); the same in 303 |

Presence over all 1,966: 1 (21), 2 (5), 3 (3), 5 (21), 10 (32), 15 (2), 20 (90), 25 (19), 30 (32), 35 (25),
40 (14), 45 (8), 50 (74), 55 (13), 60 (39), 65 (55), 70 (269), 75 (382), 80 (250), 85 (3), 90 (78), 100 (531).

What the item words name, over the four words of every record:

| Kind | Words | Chests that can give one, without / with Treasure Hunter | Distinct, without / with | Only with Treasure Hunter |
|---|---:|---|---|---:|
| items | 6,097 | 1,724 / 1,541 | 50 / 39 | 1 (Meteorite) |
| equipment | 1,442 | 540 / 411 | 332 / 259 | 35 |
| loot | 25 | 17 / 2 | 3 / 2 | 0 |
| magicks | 214 | 50 / 65 | 32 / 62 | 30 |
| technicks | 86 | 18 / 25 | 16 / 23 | 7 |

No word is `0xFFFF` and no gil word is 0, so every opening gives something. The loot chests can give is Teleport
Stone, Braid Wool and Gysahl Greens.

The 35 pieces of equipment chests give only with Treasure Hunter:

- weapons: Stoneblade, Durandal, Eight-fluted Pole, Sagittarius, Gastrophetes, Scorpion Tail, Shikari Nagasa, Rod
  of Faith, Storm Staff, Grand Mace, Euclid's Sextant, Volcano, Bonebreaker, Great Trango, Seitengrat;
- shields, helms and armor: Gendarme, Bronze Shield, Venetian Shield, Horned Hat, Pirate Hat, Sorcerer's Hat, Sallet,
  Bronze
  Chestplate, Mirage Vest, Kilimweave Shirt, Scale Armor;
- accessories: Gauntlets, Steel Poleyns, Winged Boots, Cat-ear Hood;
- ammunition: Lightning Arrows, Artemis Arrows, Grand Bolts, Stone Shot, Water Bombs.

</details>

## Operations

- Per chest, each time `setuptreasure` runs: one presence draw, or no draw when the chest's flag is set.
- Per opening: the gil-or-item draw, then a draw for which item or for a random gil amount (no draw for a fixed
  amount); one grant.
- The 50/50 and 95/5 splits are constants in the code; the presence and gil chances, the four items and the two gil
  words are per record.
- A chest's contents are drawn at the moment it is opened, so anything that draws the same generator before then
  (a fight, another chest) changes what it gives.

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Kind | Role |
|---|---|---|
| save payload `+0x14B4` | bit[256] | the chest and trap flags; a chest's `+0x09` names its bit |
| `0x02EC3E60`-`0x02EC3E8B` | struct | the presence ledger, written at placement and opening, read by nothing that decides presence |
| `0x0208CD18` | u32 | the opening latch ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |

</details>

## Modding notes

- A chest is a zone-script actor whose `init` calls `setuptreasure(ref)` and whose talk function runs the opening
  sequence with the same `ref`; the 24-byte record sits in the script's msp area.
- To make a chest one-time, give it a flag id below 255 that no other chest or trap uses; to make it come back,
  `0xFF`.
- Chances are whole percents per record. To make the Treasure Hunter items an even split, the 95/5 constant in
  `0x002FB0ED` has to change; the record cannot say it.
- Clearing bit `0x40` of `+0x08` makes the gil amount exact.

## Related

- [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md): the opening sequence, the latch and the grant.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): what `setuptreasure` does in order
  and the placement decode.
- [Which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md): the presence and
  contents draws.
- [Story flags](../Story-Events-And-Hunts/story-flags.md): the chest and trap flags, in Bank512.
- [Traps](traps.md): the other user of the chest and trap flag set, and its own ring of three.
- [Augments](../Damage-And-Battle-Formulas/augments.md) and [augment list](../Damage-And-Battle-Formulas/augment-list.md): augment 25
  and the two layers.
- [Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md): the Diamond Armlet.
- [Zone asset list](zone-asset-list.md): every field with its map and region name.
- [Section 000 of the script container](../EBP-Script-Files/ebp-script-image.md): the int pool and the msp
  area.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 209 calls with 42 other topics</summary>

**Characters and objects** (explained on [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md), [party data](../Party/party-data.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps) | calls | [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) |
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts)<br>[`0x00329CC0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle slot map: initialize mapping classes (on strong and weak mode) |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | calls | [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
| [`0x00354400`](treasure-chests.md) | calls | [`0x0026E060`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings) |
| [`0x00355210`](treasure-chests.md) | calls | [`0x0026E060`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings) |
| [`0x00355830`](treasure-chests.md) | calls | [`0x0025D5E0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x00356570`](treasure-chests.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x00261F90`](chocobos-and-airships.md) (on chocobos and airships) |

**Enemy AI and gambits** (explained on [glossary](../Engine-Core/glossary.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | is called by | [`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets) |

**Battle actions** (explained on [traps](traps.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps)<br>[`0x002FA740`](traps.md) (on traps) |
| [`0x0032AA60`](treasure-chests.md) Persistent flag: query bank512 low | is called by | [`0x002FA740`](traps.md) (on traps) |
| [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low | is called by | [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps) |
| [`0x00379CD0`](treasure-chests.md) | is called by | [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps)<br>[`0x002FA740`](traps.md) (on traps) |

**Damage and battle formulas** (explained on [action definition row](../Battle-Actions/action-definition-row.md), [status timers](../Status-Effects-And-KO/status-timers.md), [augment list](../Damage-And-Battle-Formulas/augment-list.md), [damage formula](../Damage-And-Battle-Formulas/damage-formula.md), [combos](../Battle-Actions/combos.md), [bestiary](../Enemy-Spawning/bestiary.md), [formula slots](../Damage-And-Battle-Formulas/formula-slots.md), [action results](../Battle-Actions/action-results.md), [weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md), [traps](traps.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00379CD0`](treasure-chests.md) | is called by | [`0x003851F0`](../Battle-Actions/action-definition-row.md) Battle formula: build candidate status mask (on action definition row)<br>[`0x00387130`](../Battle-Actions/action-phases.md) (on action phases)<br>[`0x00387FD0`](../Damage-And-Battle-Formulas/damage-formula.md) Battle formula: roll special guard outcome (on damage formula)<br>[`0x00388350`](../Damage-And-Battle-Formulas/damage-formula.md) Battle formula: compute knockback chance (on damage formula)<br>[`0x00388440`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x003884F0`](../Damage-And-Battle-Formulas/damage-formula.md) Battle formula: roll guard parry mode (on damage formula)<br>[`0x00388660`](../Battle-Actions/combos.md) Battle formula: roll and store combo count (on combos)<br>[`0x00388B50`](../Battle-Actions/action-definition-row.md) (on action definition row)<br>[`0x00388E80`](treasure-chests.md)<br>[`0x00389140`](../Damage-And-Battle-Formulas/weapon-formulas.md) Battle formula: roll primary formula resource reaction mode2 chance (on weapon formulas)<br>[`0x00389670`](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) (on kill rewards)<br>[`0x003896B0`](../Damage-And-Battle-Formulas/damage-formula.md) Battle formula: roll avoid guard parry outcome (on damage formula) |
| [`0x00379CD0`](treasure-chests.md) | is also called by | [`0x00389820`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x00389950`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x00389A50`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x00389AB0`](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) (on kill rewards)<br>[`0x00389BE0`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x00389C60`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x00389DD0`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x00389F80`](../Damage-And-Battle-Formulas/formula-slots.md) (on formula slots)<br>[`0x0038A110`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038A1F0`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038A2D0`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038A3A0`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas) |
| [`0x00379CD0`](treasure-chests.md) | is also called by | [`0x0038A470`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038A590`](treasure-chests.md)<br>[`0x0038A680`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038A820`](treasure-chests.md)<br>[`0x0038AAF0`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038ABC0`](treasure-chests.md)<br>[`0x0038AD70`](treasure-chests.md)<br>[`0x0038AE50`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038CC10`](treasure-chests.md)<br>[`0x0038CD60`](traps.md) (on traps)<br>[`0x0038CE40`](traps.md) (on traps)<br>[`0x0038CF20`](traps.md) (on traps) |
| [`0x00379CD0`](treasure-chests.md) | is also called by | [`0x0038D000`](traps.md) (on traps)<br>[`0x0038D7E0`](treasure-chests.md)<br>[`0x0038D970`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038DA90`](treasure-chests.md)<br>[`0x0038DB10`](treasure-chests.md)<br>[`0x0038DB50`](../Damage-And-Battle-Formulas/weapon-formulas.md) (on weapon formulas)<br>[`0x0038E590`](treasure-chests.md)<br>[`0x0038E770`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x0038E950`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x0038E9D0`](treasure-chests.md)<br>[`0x0038EAB0`](treasure-chests.md)<br>[`0x0038F6F0`](traps.md) (on traps) |
| [`0x00379CD0`](treasure-chests.md) | is also called by | [`0x0038FB80`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x0038FBC0`](../Damage-And-Battle-Formulas/damage-formula.md) (on damage formula)<br>[`0x003902F0`](treasure-chests.md)<br>[`0x00390390`](../Damage-And-Battle-Formulas/steal.md) (on steal)<br>[`0x00390680`](../Enemy-Spawning/bestiary.md) Battle formula: select poach reward item95 5 (on bestiary) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FA470`](treasure-chests.md) | is called by | [`0x002341C0`](traps.md) (on traps) |
| [`0x00379CD0`](treasure-chests.md) | is called by | [`0x0022B6E0`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar)<br>[`0x0022B7E0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake) |

**Gameplay** (explained on [frame update order](../Engine-Core/frame-update-order.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FA260`](treasure-chests.md) | is called by | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x003004B0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) | is called by | [`0x00316DF0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects (on strong and weak mode) |
| [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | is called by | [`0x00316DF0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects (on strong and weak mode)<br>[`0x00323540`](../Party/party-members.md) Definition runtime: deactivate and remove configured items (on party members) |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | is called by | [`0x00312B40`](../Battle-Actions/battle-orders.md) (on battle orders) |

**Items, equipment, shops and licenses** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | calls | [`0x003008A0`](../Scripts-And-Script-Commands/reward-verbs.md) Inventory: modify encoded item and update discovery state (on reward verbs) |
| [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | is called by | [`0x00323910`](../Items-Equipment-Shops-And-Licenses/buying-a-license.md) Battle stats: set license node state and apply side effects (on buying a license) |
| [`0x0050FAF0`](treasure-chests.md) | calls | [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) |

**Movement and pathfinding** (explained on [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [traps](traps.md), [force fight mode](../Engine-Core/force-fight-mode.md), [mpk map pack](mpk-map-pack.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [bestiary](../Enemy-Spawning/bestiary.md), [party leader](../Party/party-leader.md), [party control modes](../Engine-Core/party-control-modes.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023B2A0`](treasure-chests.md) | calls | [`0x0026BBC0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026BF60`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x002FA740`](traps.md) (on traps) | calls | [`0x002FB560`](traps.md) (on traps) |
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x0033A720`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x003ED190`](mpk-map-pack.md) (on mpk map pack)<br>[`0x003ED3F0`](mpk-map-pack.md) (on mpk map pack) |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | is called by | [`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00312730`](../EBP-Script-Files/ebp-position-entries.md) Battle locomotion: decode order goal (on ebp position entries)<br>[`0x00313670`](../Party/party-slots.md) (on party slots)<br>[`0x00336040`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x00336710`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: build solver context (on battle locomotion)<br>[`0x00336E40`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over)<br>[`0x00338490`](../Party/party-leader.md) Party follow: solve formation (on party leader)<br>[`0x00339A60`](../Party/party-leader.md) (on party leader)<br>[`0x00469A50`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) |
| [`0x00355210`](treasure-chests.md) | calls | [`0x0026A0D0`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: set desired movement heading (on party during scenes)<br>[`0x0026AF80`](../Graphics/effect-file-loading.md) (on effect file loading)<br>[`0x0026B620`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002EC5B0`](../Movement-And-Pathfinding/player-movement.md) (on player movement) |
| [`0x00355830`](treasure-chests.md) | calls | [`0x0026D6D0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x0050F850`](treasure-chests.md) | calls | [`0x0023B2A0`](treasure-chests.md) |

**Party** (explained on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FAFD0`](treasure-chests.md) | calls | [`0x003272A0`](treasure-chests.md) Battle unit: get party leader |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | is called by | [`0x0023B040`](../Engine-Core/party-control-modes.md) Party control: recompute suppression from leader battle state (on party control modes) |
| [`0x00355830`](treasure-chests.md) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x00356570`](treasure-chests.md) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |

**Steam and achievements** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x003160C0`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x00377B60`](area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |

**Random numbers** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps) | calls | [`0x00379CD0`](treasure-chests.md) |
| [`0x002FA740`](traps.md) (on traps) | calls | [`0x00379CD0`](treasure-chests.md) |
| [`0x002FAED0`](treasure-chests.md) | calls | [`0x00379CD0`](treasure-chests.md) |
| [`0x002FAFD0`](treasure-chests.md) | calls | [`0x00379CD0`](treasure-chests.md) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |

**Rewards: EXP, LP, gil and loot** (explained on [item and ability ids](../Engine-Core/item-and-ability-ids.md), [debug menu](../Engine-Core/debug-menu.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md), [stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003004B0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) | calls | [`0x00253690`](../Menus-And-HUD/party-list.md) Game state: get gil (on party list)<br>[`0x00254EE0`](../Engine-Core/debug-menu.md) Game state: set gil (on debug menu) |
| [`0x003004B0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) | is called by | [`0x0032A7F0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) |
| [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | is called by | [`0x00319920`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x003F4AA0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) |
| [`0x00379CD0`](treasure-chests.md) | is called by | [`0x002F9A60`](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) (on stat growth per level)<br>[`0x002F9B20`](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) (on stat growth per level) |
| [`0x0050FAF0`](treasure-chests.md) | calls | [`0x003004B0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |
| [`0x0032AA60`](treasure-chests.md) Persistent flag: query bank512 low | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |

**Scripts and script commands** (explained on [voices](../Sound-And-Music/voices.md), [quickenings and summons](../Battle-Actions/quickenings-and-summons.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [verb dispatch](../Scripts-And-Script-Commands/verb-dispatch.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [gambit screen](../Menus-And-HUD/gambit-screen.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [bestiary](../Enemy-Spawning/bestiary.md), [which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md), [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0023B2A0`](treasure-chests.md) | is called by | [`0x0050F850`](treasure-chests.md) |
| [`0x002650B0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) | is called by | [`0x0033F100`](treasure-chests.md)<br>[`0x00344000`](../Sound-And-Music/voices.md) (on voices)<br>[`0x00348330`](../Battle-Actions/quickenings-and-summons.md) (on quickenings and summons)<br>[`0x0034B4B0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x0034F5A0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003512A0`](treasure-chests.md)<br>[`0x00351970`](treasure-chests.md)<br>[`0x003538F0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch)<br>[`0x00353ED0`](treasure-chests.md)<br>[`0x003540B0`](treasure-chests.md)<br>[`0x00354230`](treasure-chests.md)<br>[`0x00354400`](treasure-chests.md) |
| [`0x002650B0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) | is also called by | [`0x00355210`](treasure-chests.md)<br>[`0x00355570`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences)<br>[`0x00355830`](treasure-chests.md)<br>[`0x00355D20`](treasure-chests.md)<br>[`0x0050D3B0`](treasure-chests.md)<br>[`0x0050D420`](treasure-chests.md)<br>[`0x0050E060`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0050FAF0`](treasure-chests.md)<br>[`0x005103B0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x005105A0`](treasure-chests.md)<br>[`0x00510620`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x005106D0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) |
| [`0x002650B0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) | is also called by | [`0x00510B80`](../Menus-And-HUD/gambit-screen.md) (on gambit screen)<br>[`0x00510C80`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x00510E40`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x00510F30`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x00511010`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x002FAF60`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings) | is called by | [`0x00355210`](treasure-chests.md) |
| [`0x002FAFD0`](treasure-chests.md) | is called by | [`0x0050FAF0`](treasure-chests.md) |
| [`0x003004B0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) | is called by | [`0x0050FAF0`](treasure-chests.md) |
| [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors) | is called by | [`0x0050FAF0`](treasure-chests.md) |
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x0033F310`](treasure-chests.md)<br>[`0x00357450`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x0032AA60`](treasure-chests.md) Persistent flag: query bank512 low | is called by | [`0x00354540`](treasure-chests.md) |
| [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low | is called by | [`0x00353750`](treasure-chests.md)<br>[`0x00353BD0`](treasure-chests.md) |
| [`0x00353750`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00353BD0`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354400`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354540`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x00355830`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00356570`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0035DF40`](../Menus-And-HUD/message-windows.md) (on message windows) | is called by | [`0x0050FAF0`](treasure-chests.md) |
| [`0x0035E500`](treasure-chests.md) | is called by | [`0x0050FAF0`](treasure-chests.md) |
| [`0x00379CD0`](treasure-chests.md) | is called by | [`0x00354BF0`](../Random-Numbers/which-roll-uses-which-generator.md) (on which roll uses which generator)<br>[`0x00355140`](../Random-Numbers/which-roll-uses-which-generator.md) (on which roll uses which generator) |
| [`0x0050F850`](treasure-chests.md) | calls | [`0x00267DB0`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0050FAF0`](treasure-chests.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**Enemy spawning** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x00233780`](../Enemy-Spawning/enemy-respawning.md) Spawn: swap or push banks (on enemy respawning) |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | is called by | [`0x00234AF0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning) |

**Status effects and KO** (explained on [frame update order](../Engine-Core/frame-update-order.md), [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps) | is called by | [`0x00310DB0`](../Battle-Actions/action-results.md) Battle unit: run periodic combat maintenance (on action results) |
| [`0x00379CD0`](treasure-chests.md) | is called by | [`0x00386C70`](../Damage-And-Battle-Formulas/unit-stats-fields.md) Battle formula: advance status timers and build result (on unit stats fields) |

**Story, events and hunts** (explained on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002F8060`](traps.md) Battle unit: try trigger nearby authored field action (on traps) | calls | [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low |
| [`0x002FA740`](traps.md) (on traps) | calls | [`0x0032AA60`](treasure-chests.md) Persistent flag: query bank512 low |
| [`0x002FAED0`](treasure-chests.md) | calls | [`0x0032AA60`](treasure-chests.md) Persistent flag: query bank512 low |
| [`0x002FAFD0`](treasure-chests.md) | calls | [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low |
| [`0x00353750`](treasure-chests.md) | calls | [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low |
| [`0x00353BD0`](treasure-chests.md) | calls | [`0x0032AD70`](treasure-chests.md) Persistent flag: set bank512 low |
| [`0x00354540`](treasure-chests.md) | calls | [`0x0032AA60`](treasure-chests.md) Persistent flag: query bank512 low |

**Menus and HUD** (explained on [zone asset list](zone-asset-list.md), [hud](../Menus-And-HUD/hud.md), [map screens](../Menus-And-HUD/map-screens.md), [area flags navimapdata](area-flags-navimapdata.md), [battle menu](../Menus-And-HUD/battle-menu.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](treasure-chests.md) World transition: get active or pending field id | is called by | [`0x0029C530`](zone-asset-list.md) (on zone asset list)<br>[`0x003C5F00`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003C80C0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003F92B0`](../Menus-And-HUD/text-drawing.md) (on text drawing)<br>[`0x003F9720`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x003272A0`](treasure-chests.md) Battle unit: get party leader | is called by | [`0x00318CD0`](../Menus-And-HUD/battle-menu.md) (on battle menu) |
| [`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x0029C530`](zone-asset-list.md) (on zone asset list) |
| [`0x00377B60`](area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0029C530`](zone-asset-list.md) (on zone asset list) |

</details>
