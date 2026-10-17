---
title: "Party table: every party member, guest, Esper and the Chocobo with their starting stats, equipment, gambits, Quickenings, first-join items and model"
kind: "reference"
category: "Party"
addresses: "02EBF130, 0023AC80, 0030C470, 0030C650, 002FEF30, 0023A570, 00316DF0, 00317480, 003060E0, 0031C2F0"
---

## What it lists

`party-table.tsv` holds one line for each of the 40 rows of the party table that registry slot `02EBF130` reaches
(`battle_pack.bin` directory entry `+0x44`). Row *n* belongs to the stats record whose type byte `+0x04` is *n*:
`0023AC80` builds a party record from it, and every reader below takes its row by that byte.

| Rows | Kind | Test |
|---|---|---|
| 0-6 | the main characters, Vaan to Reks | `003172E0` refuses a selector above 6 |
| 7-25 | guests; rows 17-25 are named No name and hold no data | `00322350`, type − 7 ≤ `0x12` |
| 26 | the Chocobo | |
| 27-39 | the thirteen Espers, Belias to Zodiark | `002FF007`, type − `0x1B` ≤ `0x0C` |

What a join, the catch-up and the growth do with these values is on [Party members](party-members.md),
[Stat growth on level-up](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) and
[Battle unit construction](../Characters-And-Objects/battle-unit-construction.md); this page is the shipped content.

### How it is built

`Database/Tools/catalogues/party_table.py`, with the shared readers in `ffxii_text.py` and `ids.py`:

1. the `st2e` table at entry `+0x44`: 40 rows of 128 bytes from the section's `+0x20`;
2. the name word `+0x30` through the word banks, as `0031C5D0`'s class-2 arm reads it (`0031C6B1`-`0031C6FA`);
3. the equipment words and the list at `+0x58` named by `ids.py`, the Quickenings and the Esper attacks by their
   action row's name word `+0x34`;
4. the status bits named by text bank 5, entry *s* for bit *s*, the names [Statuses](../Status-Effects-And-KO/statuses.md) uses;
5. the augment bits named by the augment row's name word `+0x02`, or its text when the name is NOT USED, as on
   [Augment list](../Damage-And-Battle-Formulas/augment-list.md);
6. the gambit preset's lines from `gambit-preset-list.tsv` ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

### The row layout

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u32` | equipForbidMask | `00317930` (`00317AD1`-`00317AD6`) | bit *c* refuses equipment of class *c*, the equipment row's `+0x09`; 0 on every row |
| `+0x04` | `u8[3]` | quickenings | `0030A310`, `0030A330`, `00313120`, `002F88B0` | the action rows of the member's three Quickenings, `0xD0`-`0xE1` |
| `+0x07` | `u8` | cameraType | `0031B8E0` | the field camera type `0025A160` selects (below) |
| `+0x0A` | `u16[5]` | equipment | `0023AC80` (`0031A630`), `00316DF0` | starting equipment, slots 0-4 (main hand, off hand, head, body, accessory) |
| `+0x14` | `u16` | gambitPreset | `0023AC80`, `00328BD0` (`00327CB0`), `00235AF0` | the preset gambit list, `0x5000` + row of `gambit_data` |
| `+0x16` | `u16` | startHp | `0030C470` | max HP at level 0 |
| `+0x18` | `u8` | hpFactor | `002FEF30` (`002F8E50`) | max HP = (`+0x18` + 1) × HP × `+0x19` / 100 |
| `+0x19` | `u8` | hpPercent | `002FEF30` | the percentage in that product |
| `+0x1A` | `u16` | startMp | `0030C470` | max MP at level 0 |
| `+0x1D` | `u8` | mpPercent | `002FEF30` (`002F9180`) | max MP = MP × `+0x1D` / 100 |
| `+0x1E` | `u8[11]` | stats | `0030C470`, `0030C650` | Strength `+0x1E`/`+0x1F`, Magick Power `+0x21`/`+0x22`, Vitality `+0x24`/`+0x25`, Speed `+0x27`/`+0x28`: base and growth in 1/128 per level |
| `+0x2A` | `u8` | evade | `002FEF30` (`002FF095`) | innate evade |
| `+0x2B` | `u8` | size | `0023A570` | unit `+0x68` = this byte, unit `+0x6C` = this byte × 1.5 |
| `+0x2C` | `u8` | flags | `0023AC80`, `00317480` | bits 3-4 the catch-up rule; bit 6 sets stats `+0x00` bit 2 (below) |
| `+0x2E` | `u8` | levelBonus | `0023AC80`, `00317480` | the starting level (0 means 1), and the levels added to the catch-up average |
| `+0x30` | `u16` | nameWord | `0031C5D0`, `0023A570`, `00329220`, `00536310` | the name, bank 8 |
| `+0x32` | `u8` | summonTime | `002FA0E0` | the Esper's summon timer: `00306760` stores it as a float at `[02EBF190]` `+0x5AD8` and `+0x5ADC` (`00306995`-`003069B7`) |
| `+0x34` | `u8[10]` | listCounts | `00316DF0` | the count of each entry of the list `+0x58` |
| `+0x3E` | `u16` | gil | `00316DF0` (`0031701B`-`00317034`) | gil added on the first join |
| `+0x44` | `u16` | lpBonus | `0023AC80` (`00323790`), `00317480` | the starting LP, and the LP added to the catch-up average |
| `+0x46` | `u8` | mistBars | `0030C470` | stats `+0x20`, the MP bars, raised to `00324100(record)` when that is larger; 0 on every row |
| `+0x47` | `u8` | startMpPercent | `0030C470` | the share of max MP a new record starts with |
| `+0x48` | `u32` | permanentStatuses | `002FEF30` (`002FF0D6`) | ORed into stats `+0x3C`, bit *s* = status *s* |
| `+0x4C` | `u32` | immunities | `002FEF30` (`002FF0A3`) | ORed into stats `+0x38`, the statuses that cannot be added |
| `+0x50` | `u32[2]` | augments | `0030FED0` (`0030FF1F`-`00310018`) | augments 0-31 and 32-63 the member always has |
| `+0x58` | `i16[10]` | list | `00316DF0`, `003060E0` | ids: first-join items and the actions a guest or Esper may use (below) |
| `+0x70` | `u32` | model | `0031C2F0` | the bound model id, letter class in bits 16-23 |
| `+0x7A` | `i16` | separation | `00238BF0` (`00238C65`), `00317400` (`0031744B`) | a positive value / 10 is the separation weight `0026DAC0` sets |

The bytes `+0x02`-`+0x03`, `+0x1C`, `+0x20`, `+0x23`, `+0x26`, `+0x29`, `+0x2F`, `+0x33`, `+0x40`-`+0x43`,
`+0x6C`-`+0x6F` and `+0x7E`-`+0x7F` are 0 on every row. The fields `+0x08`, `+0x2D`, `+0x74`, `+0x76`, `+0x78` and
`+0x7C`, and bit 0 of `+0x2C`, are read by no function in the scope below; the TSV gives them raw.

### The Quickening slots

The three bytes `+0x04`-`+0x06` are read as one list. `0030A310(row, k)` returns byte `+0x04` + *k* for *k*
below 3, and `0030A330(row, action)` the slot that holds an action.

- `00323910`, granting one of the eighteen Quickening licences (id below `0x12`), adds the action of slot
  (licence count − 1) to the inventory (`00323AAF`, `00300B80`).
- `00323EC0` allows Quickening action `0xD0`-`0xE1` to a main character only when its slot is below the
  licence count `00324020`.
- `002F88B0` fills the Quickening chain's choices from the slots, up to the licence count, and `00313120`
  finds the slot of the action just used (`0031335E`).

On the Esper rows the bytes are `0xA0`-`0xB9` in pairs; there only `00329220` reads them, copying slots 0-2 into
the member's menu record (`00329645`).

### The list at +0x58

The ten words mean different things by kind:

- **Main characters and guests (rows 0-25):** on the first join `00316DF0` adds each id whose count `+0x34` is not
  0 to the inventory (`00316FE1`-`00317019`): items, magicks, technicks, gambit conditions and key items.
- **Guests and Espers (rows 7-25, 27-39):** `003060E0` lets such a member use an action of kind 1, 2, 5 or 6
  (action row `+0x1E`) only when the action's `+0x22` is in the list (`003062B8`-`003062D2`); otherwise it returns
  refusal code `0x0F` ([Command availability](../Battle-Actions/command-availability.md)). Any other member is
  tested by `0030B0E0(+0x22)` instead (`003062DC`).

The Esper rows hold their two attacks first, the action rows `0xB6`-`0xCF`, then magick ids. The attacks are kind
9, which `003060E0` allows an Esper before it reaches the list, and no action row has a `+0x22` in
`0x00B6`-`0x00CF`.

### Flags and the camera type

- `+0x2C` bits 3-4 are the catch-up rule of [Party members](party-members.md): 1 on the first join, 2 on every
  join, anything else never (`003174D9`-`0031750D`).
- `+0x2C` bit 6 makes `0023AC80` set stats `+0x00` bit 2. `00305AB0` then sends the unit to the order set at unit
  `+0x6E0` instead of the queued `+0x6F8` (`00305BFB`-`00305C58`).
- `+0x07` is returned by `0031B8E0(row)`. Its callers are the two jumps of `0031B950(seat)`, which reads the
  selector in seat *seat* of slot map 4; the chocobo handlers `00304060` and `00304140` hand the value to
  `0025A160`, the field camera type ([Field camera](../Graphics/field-camera.md)). The Chocobo's row
  holds 14.

### The scope of "no reader"

Every function that loads `02EBF130` was decompiled: `0023AC80`, `0030C470`, `0030C650`, `0030FED0`, `002FEF30`,
`003060E0`, `00317930`, `00329220`, `00323910`, `00323EC0`, `0023A570`, `00316DF0`, `00317480`, `0031C2F0`,
`00536310`, `00235AF0`, `002F88B0`, `002FA0E0`, `0031B8E0`, `00328BD0`, `0031C5D0`, the validator `00322C50`
(the row count only) and the loader `00236C30`. The image holds no image-base-relative form of the address.

`0023A570` stores the row at unit `+0xE60`. That pointer is loaded at 27 sites in 21 functions:

- `00313120` reads `+0x04`-`+0x06`, and `00238BF0` and `00317400` read `+0x7A`, on party units;
- `00236210`, `00238BF0`'s other two loads, `00239E10`, `002FDDA0`, `00301AD0`, `003112F0`, `00312280`'s
  `003180F0`, `0031AA30`, `0031BE30`, `0031C000`, `0031C540`, `003202F0`, `003212E0`, `00390390`, `00390680`,
  `0046A870` and `00536310` read it only after a test for an enemy record (stats `+0x05` = 1);
- `0023A410` reads the spawn record `+0x6A0` first, which a party unit does not have (`0023A570` stores 0);
- `00239040`, a script verb's handler (`00510580`), tests no kind and reads `+0x50`-`+0x56` as order rows.

The pointers these functions pass on (`0030A310`, `0030A330`, `002F8E50`, `002F9180`, `00327CB0`, `0031A630`) take
values, not the row, except `0030A310` and `0030A330`, which read only `+0x04`-`+0x06`.

### Checks

- The table's header gives 40 rows of 128 bytes, and the TSV has 40 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts the zero bytes listed above, that a main character's slots are Quickening rows, that every
  list id has a shipped name, that the Esper attacks are `0xB6`-`0xCF`, and that no Esper or Chocobo row has a count.
- Rows compared with their readers: row 0, Vaan, has start HP 46 and percent 147, so `002F8E50` gives
  (0 + 1) × 46 × 147 / 100 = 67 at level 0; his growth bytes 72, 67, 48, 18 are the ones
  [Stat growth on level-up](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) lists; his slots are Red
  Spiral, White Whorl and Pyroclasm, actions `0xD0`-`0xD2`.
- Row 1, Ashe, has flags `0x09` (catch-up on the first join) and LP bonus 100, as on
  [Party members](party-members.md); row 27, Belias, has summon time 250 and model `s0`.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `row`, `name`, `kind` | the row, its shipped name, and main, guest, chocobo or Esper |
| `model` | `+0x70` as letter class and number (`c0` for Vaan), or the raw id when the class is 0 |
| `quickenings`, `slot_bytes` | the main characters' three Quickenings, and the bytes `+0x04`-`+0x06` |
| `camera_type` | `+0x07` |
| `equip_forbid_mask` | `+0x00` |
| `equipment` | `+0x0A`-`+0x13`, each name with its slot |
| `gambit_preset`, `gambit_lines` | `+0x14` and the preset's lines |
| `start_hp`, `hp_factor`, `hp_percent` | `+0x16`, `+0x18`, `+0x19` |
| `start_mp`, `mp_percent` | `+0x1A`, `+0x1D` |
| `strength`, `magick_power`, `vitality`, `speed` | base + growth/128 |
| `evade`, `size` | `+0x2A`, `+0x2B` |
| `flags`, `catch_up`, `level_bonus` | `+0x2C`, its bits 3-4, and `+0x2E` |
| `summon_time` | `+0x32` |
| `list_ids`, `list` | the ids of `+0x58` other than `0xFFFF`, and their names with the counts above 1 |
| `gil`, `lp_bonus` | `+0x3E`, `+0x44` |
| `mist_bars`, `start_mp_percent` | `+0x46`, `+0x47` |
| `permanent_statuses`, `immunities` | the statuses of `+0x48` and `+0x4C` |
| `augments` | the augments of `+0x50`-`+0x57`, each with its id |
| `separation` | `+0x7A` divided by 10 |
| `unread_08`, `unread_2D`, `unread_74`, `unread_76`, `unread_78`, `unread_7C` | the fields no function reads, raw |
| `explanation` | a one-line summary of the row |

## Related

- [Party members and guests: who can join, how the story adds and removes them, where a guest sits, and what a join brings](party-members.md)
- [Stat growth on level-up: HP, MP, Strength, Magick Power, Vitality and Speed per level, starting stats, and the level-up notices](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)
- [Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition](../Characters-And-Objects/battle-unit-construction.md)
- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](../Battle-Actions/quickenings-and-summons.md)
- [Gambits: how a character's gambit list is checked top to bottom, what runs before it, the three gambit sets and the authored presets](../Enemy-AI-And-Gambits/gambits.md)
- [Equipment: the five slots, what can be worn where, two-handed weapons, shields and ammunition, Optimise, and what happens when you equip](../Items-Equipment-Shops-And-Licenses/equipment.md)
