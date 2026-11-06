---
title: "Party table: every party member, guest, Esper and the Chocobo with their starting stats, equipment, gambits, Quickenings, first-join items and model"
kind: "reference"
category: "Party"
addresses: "0x02EBF130, 0x0023AC80, 0x0030C470, 0x0030C650, 0x002FEF30, 0x0023A570, 0x00316DF0, 0x00317480, 0x003060E0, 0x0031C2F0"
---

## What it lists

[`party-table.tsv`](party-table.tsv) holds one line for each of the 40 rows of the party table that registry slot `0x02EBF130` reaches
(`battle_pack.bin` directory entry `+0x44`). Row *n* belongs to the stats record whose type byte `+0x04` is *n*:
`0x0023AC80` builds a member stats record from it, and every reader below takes its row by that byte.

| Rows | Kind | Test |
|---|---|---|
| 0-6 | the main characters, Vaan to Reks | `0x003172E0` refuses a selector above 6 |
| 7-25 | guests; rows 17-25 are named No name and have no equipment, gambit preset, model, list or gil | `0x00322350`, type − 7 ≤ `0x12` |
| 26 | the Chocobo | |
| 27-39 | the thirteen Espers, Belias to Zodiark | `0x002FF007`, type − `0x1B` ≤ `0x0C` |

What a join, the catch-up and the growth do with these values is on [Party members](party-members.md),
[Stat growth on level-up](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) and
[Battle unit construction](../Characters-And-Objects/battle-unit-construction.md); this page is the shipped content.

The `joins_and_leaves` column gives the scene of each join and leave. Rows 0-14 join and leave in the story; no script's join or leave call and no scenario preset seats rows 15-25, the Chocobo or the Espers. The census covers the 1,114 `us` scripts with a decoded listing, of 1,115: `evt_t0020` has no EBP2 header.

### Where the values come from

Each line is read from the shipped files in these steps:

1. the `st2e` table at entry `+0x44`: 40 rows of 128 bytes from the section's `+0x20`;
2. the name word `+0x30` through the word banks, as `0x0031C5D0`'s class-2 arm reads it (`0x0031C6B1`-`0x0031C6FA`);
3. the equipment words and the list at `+0x58` named by their ids
   ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)), the Quickenings and the Esper attacks
   by their action row's name word `+0x34`;
4. the status bits named by text bank 5, entry *s* for bit *s*, the names [Statuses](../Status-Effects-And-KO/statuses.md) uses;
5. the augment bits named by their term on [Augment list](../Damage-And-Battle-Formulas/augment-list.md): the license that
   grants the augment, or the English rendering of its Japanese name where no license grants it;
6. the gambit preset's lines from [`gambit-preset-list.tsv`](../Enemy-AI-And-Gambits/gambit-preset-list.tsv) ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

### The row layout

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u32` | equipForbidMask | `0x00317930` (`0x00317AD1`-`0x00317AD6`) | bit *c* refuses equipment of class *c*, the equipment row's `+0x09`; 0 on every row |
| `+0x04` | `u8[3]` | quickenings | `0x0030A310`, `0x0030A330`, `0x00313120`, `0x002F88B0` | the action rows of the member's three Quickenings, `0xD0`-`0xE1` |
| `+0x07` | `u8` | cameraType | `0x0031B8E0` | the field camera type `0x0025A160` selects (below) |
| `+0x08` | `u8[2]` | unread08 | no instruction | read by no instruction, and written by no instruction after `battle_pack.bin` is loaded; nothing fixes its width |
| `+0x0A` | `u16[5]` | equipment | `0x0023AC80` (`0x0031A630`), `0x00316DF0` | starting equipment, slots 0-4 (main hand, off hand, head, body, accessory) |
| `+0x14` | `u16` | gambitPreset | `0x0023AC80`, `0x00328BD0` (`0x00327CB0`), `0x00235AF0` | the preset gambit list, `0x5000` + row of `gambit_data` |
| `+0x16` | `u16` | startHp | `0x0030C470` | max HP at level 0 |
| `+0x18` | `u8` | hpFactor | `0x002FEF30` (`0x002F8E50`) | max HP = (`+0x18` + 1) × HP × `+0x19` / 100 |
| `+0x19` | `u8` | hpPercent | `0x002FEF30` | the percentage in that product |
| `+0x1A` | `u16` | startMp | `0x0030C470` | max MP at level 0 |
| `+0x1D` | `u8` | mpPercent | `0x002FEF30` (`0x002F9180`) | max MP = MP × `+0x1D` / 100 |
| `+0x1E` | `u8[11]` | stats | `0x0030C470`, `0x0030C650` | Strength `+0x1E`/`+0x1F`, Magick Power `+0x21`/`+0x22`, Vitality `+0x24`/`+0x25`, Speed `+0x27`/`+0x28`: base and growth in 1/128 per level |
| `+0x2A` | `u8` | evade | `0x002FEF30` (`0x002FF095`) | innate evade |
| `+0x2B` | `u8` | size | `0x0023A570` | unit `+0x68` = this byte, unit `+0x6C` = this byte × 1.5 |
| `+0x2C` | `u8` | flags | `0x0023AC80`, `0x00317480` | mask `0x18` the catch-up rule; bit `0x40` sets stats `+0x00` bit `0x4` (below) |
| `+0x2D` | `u8` | unread2D | no instruction | read by no instruction, and written by no instruction after `battle_pack.bin` is loaded; `0xFF` on every row |
| `+0x2E` | `u8` | levelBonus | `0x0023AC80`, `0x00317480` | the starting level (0 means 1), and the levels added to the catch-up average |
| `+0x30` | `u16` | nameWord | `0x0031C5D0`, `0x0023A570`, `0x00329220`, `0x00536310` | the name, bank 8 |
| `+0x32` | `u8` | summonTime | `0x002FA0E0` | the Esper's summon timer: `0x00306760` stores it as a float at `[0x02EBF190]` `+0x5AD8` and `+0x5ADC` (`0x00306995`-`0x003069B7`) |
| `+0x34` | `u8[10]` | listCounts | `0x00316DF0` | the count of each entry of the list `+0x58` |
| `+0x3E` | `u16` | gil | `0x00316DF0` (`0x0031701B`-`0x00317034`) | gil added on the first join |
| `+0x44` | `u16` | lpBonus | `0x0023AC80` (`0x00323790`), `0x00317480` | the starting LP, and the LP added to the catch-up average |
| `+0x46` | `u8` | mistBars | `0x0030C470` | stats `+0x20`, the MP bars, raised to `0x00324100(record)` when that is larger; 0 on every row |
| `+0x47` | `u8` | startMpPercent | `0x0030C470` | the share of max MP a new record starts with |
| `+0x48` | `u32` | permanentStatuses | `0x002FEF30` (`0x002FF0D6`) | ORed into stats `+0x3C`, bit *s* = status *s* |
| `+0x4C` | `u32` | immunities | `0x002FEF30` (`0x002FF0A3`) | ORed into stats `+0x38`, the statuses that cannot be added |
| `+0x50` | `u32[2]` | augments | `0x0030FED0` (`0x0030FF1F`-`0x00310018`), `0x00239040` (`0x00239073`) | augments 0-31 and 32-63 the member always has; the script verb handler `0x00239040` (`0x00510580`) reads word *k* of `+0x50`-`+0x57`, *k* below 4, of any unit's row as an order row |
| `+0x58` | `i16[10]` | list | `0x00316DF0`, `0x003060E0` | ids: first-join items and the actions a guest or Esper may use (below) |
| `+0x70` | `u32` | model | `0x0031C2F0` | the bound model id, letter class in the bits under mask `0xFF0000` |
| `+0x74` | `u8[6]` | unread74 | no instruction | read by no instruction, and written by no instruction after `battle_pack.bin` is loaded; nothing fixes its width |
| `+0x7A` | `i16` | pushWeight | `0x00238BF0` (`0x00238C65`), `0x00317400` (`0x0031744B`) | a positive value / 10 is the body's push weight, which `0x0026DAC0` sets (below) |
| `+0x7C` | `u8[2]` | unread7C | no instruction | read by no instruction, and written by no instruction after `battle_pack.bin` is loaded; nothing fixes its width |

The bytes `+0x02`-`+0x03`, `+0x1C`, `+0x20`, `+0x23`, `+0x26`, `+0x29`, `+0x2F`, `+0x33`, `+0x40`-`+0x43`,
`+0x6C`-`+0x6F` and `+0x7E`-`+0x7F` are 0 on every row.

No instruction writes a row after `battle_pack.bin` is loaded, and no instruction reads the bytes `+0x08`-`+0x09`,
`+0x2D`, `+0x74`-`+0x79` or `+0x7C`-`+0x7D`. With no reader and no writer nothing fixes their width, so the layout
gives them as byte arrays and the TSV as their bytes. Bit `0x1` of `+0x2C` is set on four rows (Ashe, Fran, Penelo and Amalia) and tested by no
instruction: `0x0023AC80` tests bit `0x40` (`0x0023AF22`) and `0x00317480` takes bits `0x18` (`0x003174D9`-`0x003174E7`).

### The push weight

When two bodies overlap, the separation tick moves each by the other's share of their combined weight
(`0x00314E10`: A moves by `wB / (wA + wB)`; [Movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md)),
so a heavy body is barely moved by a light one.

`+0x7A` sets that weight for a party unit: a positive value divided by 10 goes to `0x0026DAC0` (`w = w / 10.0` when
`w > 0`, with `w = (float)(i16)+0x7A`, `0x0031744B`-`0x0031745B`; `0x0026DAC0(body, w)` at `0x00317467`), so a value of 0
or below would go unchanged. The shipped weights are 60 for the main characters and guests, 500 for the
Chocobo and 3,000 for the Espers, so an Esper moves by 60 / 3,060 of an overlap with a character, about 2 %.

### The Quickening slots

The three bytes `+0x04`-`+0x06` are read as one list. `0x0030A310(row, k)` returns byte `+0x04` + *k* for *k*
below 3, and `0x0030A330(row, action)` the slot that holds an action.

- `0x00323910`, granting one of the eighteen Quickening licences (id below `0x12`), adds the action of slot
  (licence count − 1) to the inventory (`0x00323AAF`, `0x00300B80`).
- `0x00323EC0` allows Quickening action `0xD0`-`0xE1` to a main character only when its slot is below the
  licence count `0x00324020`.
- `0x002F88B0` fills the Quickening chain's choices from the slots, up to the licence count, and `0x00313120`
  finds the slot of the action just used (`0x0031335E`).

On the Esper rows the bytes are not action rows: they are `0xA0`-`0xB9` in pairs, while the Esper attacks are
`0xB6`-`0xCF` (the list at `+0x58`). Only `0x00329220` reads them there, copying slots 0-2 into the words
`+0xB4`-`+0xB8` of the member's status record (`0x00329645`, stored at `0x0032964C`), and no instruction reads
those words. The TSV gives them in `esper_bytes_04`.

### The list at +0x58

The ten words mean different things by kind:

- **Main characters and guests (rows 0-25):** on the first join `0x00316DF0` adds each id whose count `+0x34` is not
  0 to the inventory (`0x00316FE1`-`0x00317019`): items, magicks, technicks, gambit conditions and key items.
- **Guests and Espers (rows 7-25, 27-39):** `0x003060E0` lets such a member use an action of kind 1, 2, 5 or 6
  (action row `+0x1E`) only when the action's `+0x22` is in the list (`0x003062B8`-`0x003062D2`); otherwise it returns
  refusal code `0x0F` ([Command availability](../Battle-Actions/command-availability.md)). Any other member is
  tested by `0x0030B0E0(+0x22)` instead (`0x003062DC`).

The Esper rows hold their two attacks first, the action rows `0xB6`-`0xCF`, then magick ids. The attacks are kind
9, which `0x003060E0` allows an Esper before it reaches the list, and no action row has a `+0x22` in
`0x00B6`-`0x00CF`.

### Flags and the camera type

- `+0x2C` bits under mask `0x18` are the catch-up rule of [Party members](party-members.md): 1 on the first join, 2 on every
  join, anything else never (`0x003174D9`-`0x0031750D`).
- `+0x2C` bit `0x40` makes `0x0023AC80` set stats `+0x00` bit `0x4`. `0x00305AB0` then sends the unit to the order set at unit
  `+0x6E0` instead of the queued `+0x6F8` (`0x00305BFB`-`0x00305C58`).
- `+0x07` is returned by `0x0031B8E0(row)`. Its callers are the two jumps of `0x0031B950(seat)`, which reads the
  selector in seat *seat* of slot map 4; the chocobo handlers `0x00304060` and `0x00304140` hand the value to
  `0x0025A160`, the field camera type ([Field camera](../Graphics/field-camera.md)). The Chocobo's row
  holds 14.

### Properties of the shipped rows

- The table's header gives 40 rows of 128 bytes, one TSV line each.
- The bytes listed above as 0 are 0 on every row. A main character's slots are Quickening rows, except Reks's (row 6), which are 0, every list id has a
  shipped name, the Esper attacks are `0xB6`-`0xCF`, and no Esper or Chocobo row has a count.
- Example rows: row 0, Vaan, has start HP 46 and percent 147, so `0x002F8E50` gives
  (0 + 1) × 46 × 147 / 100 = 67 at level 0; his growth bytes 72, 67, 48, 18 are the ones
  [Stat growth on level-up](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) lists; his slots are Red
  Spiral, White Whorl and Pyroclasm, actions `0xD0`-`0xD2`.
- Row 1, Ashe, has flags `0x09` (catch-up on the first join) and LP bonus 100, as on
  [Party members](party-members.md); row 27, Belias, has summon time 250 and model `s0`.

## Columns

| Column | Meaning |
|---|---|
| `row`, `name`, `kind` | the row, its shipped name, and main, guest, chocobo or Esper |
| `model` | `+0x70` as letter class and number (`c0` for Vaan), or the raw id when the class is 0 |
| `quickenings` | the main characters' three Quickenings, `+0x04`-`+0x06`, each with its action row |
| `esper_bytes_04` | `+0x04`-`+0x06` on an Esper row, which are no Quickenings (above) |
| `camera_type` | `+0x07` |
| `equip_forbid_mask` | `+0x00` |
| `equipment` | `+0x0A`-`+0x13`, each name with its slot |
| `gambit_preset`, `gambit_lines` | `+0x14` and the preset's lines |
| `start_hp`, `hp_factor`, `hp_percent` | `+0x16`, `+0x18`, `+0x19` |
| `start_mp`, `mp_percent` | `+0x1A`, `+0x1D` |
| `strength`, `magick_power`, `vitality`, `speed` | base + growth/128 |
| `evade`, `size` | `+0x2A`, `+0x2B` |
| `flags`, `catch_up`, `level_bonus` | `+0x2C`, its bits under mask `0x18`, and `+0x2E` |
| `summon_time` | `+0x32` |
| `list_ids`, `list` | the ids of `+0x58` other than `0xFFFF`, and their names with the counts above 1 |
| `gil`, `lp_bonus` | `+0x3E`, `+0x44` |
| `mist_bars`, `start_mp_percent` | `+0x46`, `+0x47` |
| `permanent_statuses`, `immunities` | the statuses of `+0x48` and `+0x4C` |
| `augments` | the augments of `+0x50`-`+0x57`, each by its term with its id |
| `push_weight` | `+0x7A` divided by 10: `+0x7A / 10.0`, the weight `0x0026DAC0` receives (`0x0031745B`); every shipped `+0x7A` is positive |
| `unread_08`, `unread_2D`, `unread_74`, `unread_7C` | the bytes no instruction reads, `+0x08`-`+0x09`, `+0x2D`, `+0x74`-`+0x79` and `+0x7C`-`+0x7D` |
| `explanation` | a one-line summary of the row |
| `joins_and_leaves` | each scene that adds the row (`addpartymember` for rows 0-6, `addguestbattlemember` for guests) or removes it (`removepartymember`, `removeguestbattlemember`), or seats it through a scenario preset: the map (region), script, actor, function and step, with the story progress it runs at or sets |

## Related

- [Party members and guests: who can join, how the story adds and removes them, where a guest sits, and what a join brings](party-members.md)
- [Stat growth on level-up: HP, MP, Strength, Magick Power, Vitality and Speed per level, starting stats, and the level-up notices](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)
- [Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition](../Characters-And-Objects/battle-unit-construction.md)
- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](../Battle-Actions/quickenings-and-summons.md)
- [Gambits: how a character's gambit list is checked top to bottom, what runs before it, the three gambit sets and the authored presets](../Enemy-AI-And-Gambits/gambits.md)
- [Equipment: the five slots, what can be worn where, two-handed weapons, shields and ammunition, Optimise, and what happens when you equip](../Items-Equipment-Shops-And-Licenses/equipment.md)
