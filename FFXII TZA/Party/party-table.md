---
title: "Party table: every party member, guest, Esper and the Chocobo with their starting stats, equipment, gambits, Quickenings, first-join items and model"
kind: "reference"
category: "Party"
addresses: "02EBF130, 0023AC80, 0030C470, 0030C650, 002FEF30, 0023A570, 00316DF0, 00317480, 003060E0, 0031C2F0"
---

## What it lists

`party-table.tsv` holds one line for each of the 40 rows of the party table that registry slot `02EBF130` reaches
(`battle_pack.bin` directory entry `+44`<sub>h</sub>). Row *n* belongs to the stats record whose type byte `+04`<sub>h</sub> is *n*:
`0023AC80` builds a party record from it, and every reader below takes its row by that byte.

| Rows | Kind | Test |
|---|---|---|
| 0-6 | the main characters, Vaan to Reks | `003172E0` refuses a selector above 6 |
| 7-25 | guests; rows 17-25 are named No name and hold no data | `00322350`, type − 7 ≤ `12`<sub>h</sub> |
| 26 | the Chocobo | |
| 27-39 | the thirteen Espers, Belias to Zodiark | `002FF007`, type − `1B`<sub>h</sub> ≤ `0C`<sub>h</sub> |

What a join, the catch-up and the growth do with these values is on [Party members](party-members.md),
[Stat growth on level-up](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) and
[Battle unit construction](../Characters-And-Objects/battle-unit-construction.md); this page is the shipped content.

### How it is built

`Database/Tools/catalogues/party_table.py`, with the shared readers in `ffxii_text.py` and `ids.py`:

1. the `st2e` table at entry `+44`<sub>h</sub>: 40 rows of 128 bytes from the section's `+20`<sub>h</sub>;
2. the name word `+30`<sub>h</sub> through the word banks, as `0031C5D0`'s class-2 arm reads it (`0031C6B1`-`0031C6FA`);
3. the equipment words and the list at `+58`<sub>h</sub> named by `ids.py`, the Quickenings and the Esper attacks by their
   action row's name word `+34`<sub>h</sub>;
4. the status bits named by text bank 5, entry *s* for bit *s*, the names [Statuses](../Status-Effects-And-KO/statuses.md) uses;
5. the augment bits named by the augment row's name word `+02`<sub>h</sub>, or its text when the name is NOT USED, as on
   [Augment list](../Damage-And-Battle-Formulas/augment-list.md);
6. the gambit preset's lines from `gambit-preset-list.tsv` ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

### The row layout

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `00`<sub>h</sub> | `u32` | equipForbidMask | `00317930` (`00317AD1`-`00317AD6`) | bit *c* refuses equipment of class *c*, the equipment row's `+09`<sub>h</sub>; 0 on every row |
| `04`<sub>h</sub> | `u8[3]` | quickenings | `0030A310`, `0030A330`, `00313120`, `002F88B0` | the action rows of the member's three Quickenings, `D0`<sub>h</sub>-`E1`<sub>h</sub> |
| `07`<sub>h</sub> | `u8` | cameraType | `0031B8E0` | the field camera type `0025A160` selects (below) |
| `0A`<sub>h</sub> | `u16[5]` | equipment | `0023AC80` (`0031A630`), `00316DF0` | starting equipment, slots 0-4 (main hand, off hand, head, body, accessory) |
| `14`<sub>h</sub> | `u16` | gambitPreset | `0023AC80`, `00328BD0` (`00327CB0`), `00235AF0` | the preset gambit list, `5000`<sub>h</sub> + row of `gambit_data` |
| `16`<sub>h</sub> | `u16` | startHp | `0030C470` | max HP at level 0 |
| `18`<sub>h</sub> | `u8` | hpFactor | `002FEF30` (`002F8E50`) | max HP = (`+18`<sub>h</sub> + 1) × HP × `+19`<sub>h</sub> / 100 |
| `19`<sub>h</sub> | `u8` | hpPercent | `002FEF30` | the percentage in that product |
| `1A`<sub>h</sub> | `u16` | startMp | `0030C470` | max MP at level 0 |
| `1D`<sub>h</sub> | `u8` | mpPercent | `002FEF30` (`002F9180`) | max MP = MP × `+1D`<sub>h</sub> / 100 |
| `1E`<sub>h</sub> | `u8[11]` | stats | `0030C470`, `0030C650` | Strength `+1E`<sub>h</sub>/`+1F`<sub>h</sub>, Magick Power `+21`<sub>h</sub>/`+22`<sub>h</sub>, Vitality `+24`<sub>h</sub>/`+25`<sub>h</sub>, Speed `+27`<sub>h</sub>/`+28`<sub>h</sub>: base and growth in 1/128 per level |
| `2A`<sub>h</sub> | `u8` | evade | `002FEF30` (`002FF095`) | innate evade |
| `2B`<sub>h</sub> | `u8` | size | `0023A570` | unit `+68`<sub>h</sub> = this byte, unit `+6C`<sub>h</sub> = this byte × 1.5 |
| `2C`<sub>h</sub> | `u8` | flags | `0023AC80`, `00317480` | bits 3-4 the catch-up rule; bit 6 sets stats `+00`<sub>h</sub> bit 2 (below) |
| `2E`<sub>h</sub> | `u8` | levelBonus | `0023AC80`, `00317480` | the starting level (0 means 1), and the levels added to the catch-up average |
| `30`<sub>h</sub> | `u16` | nameWord | `0031C5D0`, `0023A570`, `00329220`, `00536310` | the name, bank 8 |
| `32`<sub>h</sub> | `u8` | summonTime | `002FA0E0` | the Esper's summon timer: `00306760` stores it as a float at `[02EBF190]` `+5AD8`<sub>h</sub> and `+5ADC`<sub>h</sub> (`00306995`-`003069B7`) |
| `34`<sub>h</sub> | `u8[10]` | listCounts | `00316DF0` | the count of each entry of the list `+58`<sub>h</sub> |
| `3E`<sub>h</sub> | `u16` | gil | `00316DF0` (`0031701B`-`00317034`) | gil added on the first join |
| `44`<sub>h</sub> | `u16` | lpBonus | `0023AC80` (`00323790`), `00317480` | the starting LP, and the LP added to the catch-up average |
| `46`<sub>h</sub> | `u8` | mistBars | `0030C470` | stats `+20`<sub>h</sub>, the MP bars, raised to `00324100(record)` when that is larger; 0 on every row |
| `47`<sub>h</sub> | `u8` | startMpPercent | `0030C470` | the share of max MP a new record starts with |
| `48`<sub>h</sub> | `u32` | permanentStatuses | `002FEF30` (`002FF0D6`) | ORed into stats `+3C`<sub>h</sub>, bit *s* = status *s* |
| `4C`<sub>h</sub> | `u32` | immunities | `002FEF30` (`002FF0A3`) | ORed into stats `+38`<sub>h</sub>, the statuses that cannot be added |
| `50`<sub>h</sub> | `u32[2]` | augments | `0030FED0` (`0030FF1F`-`00310018`) | augments 0-31 and 32-63 the member always has |
| `58`<sub>h</sub> | `i16[10]` | list | `00316DF0`, `003060E0` | ids: first-join items and the actions a guest or Esper may use (below) |
| `70`<sub>h</sub> | `u32` | model | `0031C2F0` | the bound model id, letter class in bits 16-23 |
| `7A`<sub>h</sub> | `i16` | separation | `00238BF0` (`00238C65`), `00317400` (`0031744B`) | a positive value / 10 is the separation weight `0026DAC0` sets |

The bytes `+02`<sub>h</sub>-`+03`<sub>h</sub>, `+1C`<sub>h</sub>, `+20`<sub>h</sub>, `+23`<sub>h</sub>, `+26`<sub>h</sub>, `+29`<sub>h</sub>, `+2F`<sub>h</sub>, `+33`<sub>h</sub>, `+40`<sub>h</sub>-`+43`<sub>h</sub>,
`+6C`<sub>h</sub>-`+6F`<sub>h</sub> and `+7E`<sub>h</sub>-`+7F`<sub>h</sub> are 0 on every row. The fields `+08`<sub>h</sub>, `+2D`<sub>h</sub>, `+74`<sub>h</sub>, `+76`<sub>h</sub>, `+78`<sub>h</sub> and
`+7C`<sub>h</sub>, and bit 0 of `+2C`<sub>h</sub>, are read by no function in the scope below; the TSV gives them raw.

### The Quickening slots

The three bytes `+04`<sub>h</sub>-`+06`<sub>h</sub> are read as one list. `0030A310(row, k)` returns byte `+04`<sub>h</sub> + *k* for *k*
below 3, and `0030A330(row, action)` the slot that holds an action.

- `00323910`, granting one of the eighteen Quickening licences (id below `12`<sub>h</sub>), adds the action of slot
  (licence count − 1) to the inventory (`00323AAF`, `00300B80`).
- `00323EC0` allows Quickening action `D0`<sub>h</sub>-`E1`<sub>h</sub> to a main character only when its slot is below the
  licence count `00324020`.
- `002F88B0` fills the Quickening chain's choices from the slots, up to the licence count, and `00313120`
  finds the slot of the action just used (`0031335E`).

On the Esper rows the bytes are `A0`<sub>h</sub>-`B9`<sub>h</sub> in pairs; there only `00329220` reads them, copying slots 0-2 into
the member's menu record (`00329645`).

### The list at `+58`<sub>h</sub>

The ten words mean different things by kind:

- **Main characters and guests (rows 0-25):** on the first join `00316DF0` adds each id whose count `+34`<sub>h</sub> is not
  0 to the inventory (`00316FE1`-`00317019`): items, magicks, technicks, gambit conditions and key items.
- **Guests and Espers (rows 7-25, 27-39):** `003060E0` lets such a member use an action of kind 1, 2, 5 or 6
  (action row `+1E`<sub>h</sub>) only when the action's `+22`<sub>h</sub> is in the list (`003062B8`-`003062D2`); otherwise it returns
  refusal code `0F`<sub>h</sub> ([Command availability](../Battle-Actions/command-availability.md)). Any other member is
  tested by `0030B0E0(+22h)` instead (`003062DC`).

The Esper rows hold their two attacks first, the action rows `B6`<sub>h</sub>-`CF`<sub>h</sub>, then magick ids. The attacks are kind
9, which `003060E0` allows an Esper before it reaches the list, and no action row has a `+22`<sub>h</sub> in
`00B6`<sub>h</sub>-`00CF`<sub>h</sub>.

### Flags and the camera type

- `+2C`<sub>h</sub> bits 3-4 are the catch-up rule of [Party members](party-members.md): 1 on the first join, 2 on every
  join, anything else never (`003174D9`-`0031750D`).
- `+2C`<sub>h</sub> bit 6 makes `0023AC80` set stats `+00`<sub>h</sub> bit 2. `00305AB0` then sends the unit to the order set at unit
  `+6E0`<sub>h</sub> instead of the queued `+6F8`<sub>h</sub> (`00305BFB`-`00305C58`).
- `+07`<sub>h</sub> is returned by `0031B8E0(row)`. Its callers are the two jumps of `0031B950(seat)`, which reads the
  selector in seat *seat* of slot map 4; the chocobo handlers `00304060` and `00304140` hand the value to
  `0025A160`, the field camera type ([Field camera](../Graphics/field-camera.md)). The Chocobo's row
  holds 14.

### The scope of "no reader"

Every function that loads `02EBF130` was decompiled: `0023AC80`, `0030C470`, `0030C650`, `0030FED0`, `002FEF30`,
`003060E0`, `00317930`, `00329220`, `00323910`, `00323EC0`, `0023A570`, `00316DF0`, `00317480`, `0031C2F0`,
`00536310`, `00235AF0`, `002F88B0`, `002FA0E0`, `0031B8E0`, `00328BD0`, `0031C5D0`, the validator `00322C50`
(the row count only) and the loader `00236C30`. The image holds no image-base-relative form of the address.

`0023A570` stores the row at unit `+E60`<sub>h</sub>. That pointer is loaded at 27 sites in 21 functions:

- `00313120` reads `+04`<sub>h</sub>-`+06`<sub>h</sub>, and `00238BF0` and `00317400` read `+7A`<sub>h</sub>, on party units;
- `00236210`, `00238BF0`'s other two loads, `00239E10`, `002FDDA0`, `00301AD0`, `003112F0`, `00312280`'s
  `003180F0`, `0031AA30`, `0031BE30`, `0031C000`, `0031C540`, `003202F0`, `003212E0`, `00390390`, `00390680`,
  `0046A870` and `00536310` read it only after a test for an enemy record (stats `+05`<sub>h</sub> = 1);
- `0023A410` reads the spawn record `+6A0`<sub>h</sub> first, which a party unit does not have (`0023A570` stores 0);
- `00239040`, a script verb's handler (`00510580`), tests no kind and reads `+50`<sub>h</sub>-`+56`<sub>h</sub> as order rows.

The pointers these functions pass on (`0030A310`, `0030A330`, `002F8E50`, `002F9180`, `00327CB0`, `0031A630`) take
values, not the row, except `0030A310` and `0030A330`, which read only `+04`<sub>h</sub>-`+06`<sub>h</sub>.

### Checks

- The table's header gives 40 rows of 128 bytes, and the TSV has 40 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts the zero bytes listed above, that a main character's slots are Quickening rows, that every
  list id has a shipped name, that the Esper attacks are `B6`<sub>h</sub>-`CF`<sub>h</sub>, and that no Esper or Chocobo row has a count.
- Rows compared with their readers: row 0, Vaan, has start HP 46 and percent 147, so `002F8E50` gives
  (0 + 1) × 46 × 147 / 100 = 67 at level 0; his growth bytes 72, 67, 48, 18 are the ones
  [Stat growth on level-up](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) lists; his slots are Red
  Spiral, White Whorl and Pyroclasm, actions `D0`<sub>h</sub>-`D2`<sub>h</sub>.
- Row 1, Ashe, has flags `09`<sub>h</sub> (catch-up on the first join) and LP bonus 100, as on
  [Party members](party-members.md); row 27, Belias, has summon time 250 and model `s0`.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `row`, `name`, `kind` | the row, its shipped name, and main, guest, chocobo or Esper |
| `model` | `+70`<sub>h</sub> as letter class and number (`c0` for Vaan), or the raw id when the class is 0 |
| `quickenings`, `slot_bytes` | the main characters' three Quickenings, and the bytes `+04`<sub>h</sub>-`+06`<sub>h</sub> |
| `camera_type` | `+07`<sub>h</sub> |
| `equip_forbid_mask` | `+00`<sub>h</sub> |
| `equipment` | `+0A`<sub>h</sub>-`+13`<sub>h</sub>, each name with its slot |
| `gambit_preset`, `gambit_lines` | `+14`<sub>h</sub> and the preset's lines |
| `start_hp`, `hp_factor`, `hp_percent` | `+16`<sub>h</sub>, `+18`<sub>h</sub>, `+19`<sub>h</sub> |
| `start_mp`, `mp_percent` | `+1A`<sub>h</sub>, `+1D`<sub>h</sub> |
| `strength`, `magick_power`, `vitality`, `speed` | base + growth/128 |
| `evade`, `size` | `+2A`<sub>h</sub>, `+2B`<sub>h</sub> |
| `flags`, `catch_up`, `level_bonus` | `+2C`<sub>h</sub>, its bits 3-4, and `+2E`<sub>h</sub> |
| `summon_time` | `+32`<sub>h</sub> |
| `list_ids`, `list` | the ids of `+58`<sub>h</sub> other than `FFFF`<sub>h</sub>, and their names with the counts above 1 |
| `gil`, `lp_bonus` | `+3E`<sub>h</sub>, `+44`<sub>h</sub> |
| `mist_bars`, `start_mp_percent` | `+46`<sub>h</sub>, `+47`<sub>h</sub> |
| `permanent_statuses`, `immunities` | the statuses of `+48`<sub>h</sub> and `+4C`<sub>h</sub> |
| `augments` | the augments of `+50`<sub>h</sub>-`+57`<sub>h</sub>, each with its id |
| `separation` | `+7A`<sub>h</sub> divided by 10 |
| `unread_08`, `unread_2D`, `unread_74`, `unread_76`, `unread_78`, `unread_7C` | the fields no function reads, raw |
| `explanation` | a one-line summary of the row |

## Related

- [Party members and guests: who can join, how the story adds and removes them, where a guest sits, and what a join brings](party-members.md)
- [Stat growth on level-up: HP, MP, Strength, Magick Power, Vitality and Speed per level, starting stats, and the level-up notices](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)
- [Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition](../Characters-And-Objects/battle-unit-construction.md)
- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](../Battle-Actions/quickenings-and-summons.md)
- [Gambits: how a character's gambit list is checked top to bottom, what runs before it, the three gambit sets and the authored presets](../Enemy-AI-And-Gambits/gambits.md)
- [Equipment: the five slots, what can be worn where, two-handed weapons, shields and ammunition, Optimise, and what happens when you equip](../Items-Equipment-Shops-And-Licenses/equipment.md)
