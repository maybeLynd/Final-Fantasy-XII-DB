---
title: "Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition"
kind: "system"
category: "Characters and objects"
addresses: "0x0023A570, 0x0023AC80, 0x0030C470, 0x0030C650, 0x002F8F20, 0x00236100, 0x002B58B0, 0x00322050, 0x003220E0, 0x00322C50, 0x00323790, 0x0031A630, 0x00323910, 0x00327CB0, 0x00326030, 0x00327DE0, 0x002F8E90, 0x002F90C0, 0x002F8BB0, 0x0050FF20, 0x00309230, 0x00254A40"
---

## What the player sees

A battle unit becomes something when a definition is applied to it: Vaan with his level, equipment,
licences and gambits, or a Wolf with its stats, its one weapon and its loot flags. Party members
come from one authored table and enemies from the area's enemy table, and every piece of combat
code can tell the two apart by one byte in the unit's stats record. A narrower split of the party
side, by the type number, decides who earns experience and licence points and who is only a guest
or a summoned creature.

An enemy whose definition names a row past the end of one of the area's battle tables is not installed and does
not appear. An area without its battle-logic table installs no enemy at all; one without its enemy or class
table makes the installer read from address 0, and the game crashes.

## How it works

### The installer and the definition id

`0x0023A570(unit, id)` applies definition `id` to a unit. The id's high byte is the kind (0 party, 1
enemy, anything else installs nothing and clears unit flag bit `0x4000000`) and its low byte the row index.
Before anything else the installer:

1. remembers the unit's previous id, the stats record's word `+0x04`, when unit flag bit `0x4` is set
   (`0xFFFF` otherwise), and resets the unit with `0x00236A60` ([battle unit fields](battle-unit-fields.md));
2. returns 0 when the battle system is down (`0x02089300` = 0);
3. re-keys the unit (`0x00322050`) when the kind byte is not 0 or the previous id differs from both
   the new id and `0xFFFF`; with `0x00303EC0()` set, the check is skipped only when `0x00304630()`
   (`0xFF` read as `0xFFFF`) equals the previous id and the new id is `0xFFFF`.

`0x00322050(unit)` zeroes the attacker mask `+0xEA4` and count `+0xEA8` and stores
`0x003220E0(actor)` at `+0x08`: that function encodes the actor's current handle, advances the actor's
discriminator (`0x002659D0`), encodes the new handle, and, when the party focus record `0x00327150()`
held the old handle, stores the re-keyed unit's stats byte `+0x04` (or `0xFF`) as a dword at
`[0x02EBF190] + 0x5AA4` and runs `0x00326500`, which picks the default controlled member and requests its handle
([Party leader](../Party/party-leader.md)).

### The enemy path

With kind 1 the unit must have flag bit `0x4000000` set. The installer then:

1. takes row `index` of the enemy table `0x02EBF120` (count at `+0x04`, row stride at `+0x08`,
   rows from the section at `+0x0C`), and the class row the enemy row's word `+0x00` names in
   `0x02EBF150`, and makes five bound tests, returning 0 (`0x0023A63A`) at the first that fails:
   - the row index against the enemy table's count (`0x0023A65D`-`0x0023A662`);
   - the enemy row's word `+0x00` against the class table's count at `+0x04` (`0x0023A6B4`-`0x0023A6BB`);
   - the word `+0x50` against the count word at `+0` of `0x02EBF168` (`0x0023A71E`-`0x0023A726`);
   - the word `+0x22` against the count at `+0x04` of `0x02EBF148` (`0x0023A73F`-`0x0023A747`);
   - the word `+0x24` against the count at `+0x04` of `0x02EBF140` (`0x0023A760`-`0x0023A768`).

   Each test compares the index with `count - 1`, the count read as 0 for a null table. Four are unsigned (`ja`):
   with a null table or a count of 0, `count - 1` is `0xFFFFFFFF` and they pass every index.

   With a count of 0
   the row taken after them lies past the table's end. With a null enemy or class table the row address is 0 and
   is read there (`0x0023A69F` and `0x0023A6B4`; `0x0023A708` and `0x0023A8E6`); a null `0x02EBF148` or `0x02EBF140` leaves
   the unit's row pointer at `+0xE70` or `+0xE78` null (`0x0023A9A3`, `0x0023A9EA`). The `+0x50` test is signed
   (`jg`) on a zero-extended word, so a null or empty `0x02EBF168` makes it refuse every enemy;
2. resolves the spawn record: `0x00236100(unit +0x40, unit +0x57)` reads the lane map's byte
   `1 + lane` (lane below the map's count byte, entry not `0xFF`) and returns
   `0x0208E690 + entry * 0x250`; no record returns 0. The stats record is that record's `+0x80`;
3. for a fresh record (record byte `+0` without bits `0x1` and `0x4`) it initialises the stats record
   (`0x0023AC80`, below) and sets the steal bits at record `+0x14`: bits `0x1`, `0x2` and `0x4` when the row's
   words `+0x32`, `+0x34` and `+0x36` are not `0xFFFF`;
4. still for a fresh record, when the row's byte `+0x02` is not `0xFF`, it reads the spawn counter
   `0x0208D354 + (0x0208D454 * 64 + byte) * 2`, stores the old value's low byte at record `+0x12` and
   writes back `old + 1`, or 1 once `old` reaches `0x00254A40()`; with a byte of `0xFF` it stores 0 at
   `+0x12`;
5. resolves the name text: the row's word `+0x08` split as bank (high 5 bits) and entry (low 11
   bits) through `0x02EBF170`, then `0x002B58B0(block, 0)`. `0x00269F20` stores that text and the `+0x12` ordinal at the
   actor's `+0xF8` and `+0x100` (`0x00238EB8`);
6. stores `+0xE60` = the enemy row, `+0xE68` = the class row, `+0x6E0` = the `0x02EBF168` row named by
   word `+0x50`, `+0xE70` = the `0x02EBF148` row named by word `+0x22`, `+0xE78` = the `0x02EBF140` row
   named by word `+0x24`;
7. registers the unit (`0x00328FF0(0, row byte +0x03 & 3, unit +0xEA9)`: the class to `0x02EC1384` and
   the slot to `0x02EC1380`, written only when the class is not 0 or the slot is negative), and sets
   flag bit `0x80000000000` when `row byte +0x03 & 3` or `row byte +0x15` bit `0x4` is set, else clears it.

The name drawer `0x00272CE0` adds a letter to that name when the actor's word `+0x102` is negative, so that the
name is the text at `+0xF8` (`0x00263990`, `0x00263A10`), and the ordinal is not 0 (`0x00272D3A`). `0x002B58F0`, through
`0x0024ABE0`, writes entry `0x21` + (ordinal - 1) mod 26 of the text the font sheet names at `+0x14`, or at `+0x18`
when the language test `0x00254A10` is true (`0x002B5957`-`0x002B5997`).

The common stores then take, from the class row: `+0x64` = byte `+0x22` times 2π/360, `+0x55` =
byte `+0x04`, `+0x68` = float(byte `+0x23`), `+0x56` = byte `+0x05`, `+0x6C` = float(byte `+0x27`),
`+0x52` = word `+0x06`.

### The party path

With kind 0 the index must pass `0x00322C50(2, index, 1)`, the party table's count. The installer
takes row `index` of the party table `0x02EBF130`, points the stats at the party block's
element `[0x02EBF190] + 8 + index * 0x1C8` with no spawn record, resolves the name from the row's
word `+0x30` the same way, and stores `+0x6E0` = `0x02089378 + index * 0x170`, `+0x6F0` = `0x01E09350`,
`+0xE60` = the row, `+0x64` = 2π, `+0x6C` = row byte `+0x2B` times 1.5, `+0x68` = float(row byte
`+0x2B`), `+0x55` = `0xFF`, `+0x56` = `0xFF`, `+0x52` = `0xFFFF`.

### The common stores

Both paths end with: `+0x48` = 0 (the HP floor), `+0x698` = the stats record, `+0x6A0` = the spawn
record or null, `+0x18` = the name text, `+0x54` = `0xFF`, then `0x00237040(unit)` and
`0x002FEAB0(unit)`. When the stats record is null, or its status words `+0x3C | +0x64` carry bits `0x1`, `0x2`
or 31 outside a town (`0x00377C20`), flag bit `0x4000000` is cleared and bit `0x2` set. Bit `0x4` is set and the
installer returns 1.

### The fresh stats record

`0x0023AC80(record, id)` fills a stats record from nothing:

1. `memset` of `0x1C8` bytes, then `+0x50` = all ones (8 bytes), `+0x58` = `0xFFFF`, `+0x1C3` = `0xFFFF`,
   `+0x1C5` = `0xFF`; with `0x02089300` = 0 it returns 0;
2. kind 0 takes the party row and the level `max(row byte +0x2E, 1)`; kind 1 takes the enemy row and
   level 1; any other kind returns 0;
3. `+0x04` = the whole id, so the byte `+0x05` is the kind by construction; then the level grower
   `0x0030C470(record, level, kind)`;
4. kind 0: the LP `0x00323790(record, row word +0x44)`; for an index below 7, every licence entry of
   `0x02EBF038` whose byte `+0x07` has bit `index` set is granted (`0x00323910(record, entry, 1)`);
5. kind 0: equipment slots 0-4 from the row's words `+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12`
   (`0x0031A630`); the gambit preset `0x00327CB0(record, row word +0x14)`, `0x00326030([0x02EBF190], index)`
   and `0x00327DE0([0x02EBF190] + 8 + index * 0x1C8)`; and record `+0x00` bit `0x4` when the row's byte
   `+0x2C` has bit `0x40`;
6. kind 1: equipment slot 0 from the row's word `+0x16`, slot 1 from `+0x1C`, slots 2-4 `0xFFFF`.

### The level grower

`0x0030C470(record, level, kind)` starts from level 0 and grows up:

1. `+0x1C2` = 0; for kind 0 the base values come from the party row named by `+0x04`: `+0x08` =
   word `+0x16`, `+0x0C` = word `+0x1A`, `+0x10`, `+0x14`, `+0x18`, `+0x1C` = the floats of bytes
   `+0x1E`, `+0x21`, `+0x24`, `+0x27`, `+0x20` = the larger of byte `+0x46` and the licence rank
   `0x00324100(record)`; for kind 1 only `+0x88` = the kind argument (1 from the initialiser); any
   other kind returns;
2. `0x0030C650(record, level, 2)` grows to the level ([stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md));
3. `+0x18C` = `min(0x002F8F20(level - 1), 99999999)`, the experience of the level reached
   ([EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md));
4. when the status masks `0x0208D320` or `0x0208D324` are non-zero, the statuses in their union are
   removed (`0x0030F690(record, union)`); HP and MP are reconciled to their capacities (`0x0030F340`,
   `0x0030F5A0`);
5. the starting MP: `cap` = `+0x28` when the layer bytes `+0x6C` and `+0x7C` are both non-negative,
   else 0; kind 0 sets `+0x4C` = `cap * row byte +0x47 / 100`, kind 1 sets `+0x4C` = `cap`;
6. `0x0030FED0(record, 0)` rebuilds the derived state ([augments](../Damage-And-Battle-Formulas/augments.md)).

### The kind byte and the type partition

Stats byte `+0x05` is the kind: 0 for a party-table unit, 1 for an enemy. Stats byte `+0x04` is the
row index, and for kind 0 it is the type the code partitions:

| Type | Span | `0x0050FF20` class | Experience (`0x002F8BB0`) | Licence points (`0x002F90C0`) |
|---|---|---|---|---|
| 0-6 | the main characters | 0 | yes | yes |
| 7-25 | the guest range | 1 | yes | no |
| 26 | the Chocobo | 3 | yes, but not counted in the split | yes |
| 27-39 | the thirteen Espers, Belias to Zodiark | 2 | no | no |
| 40 and above | | 0 | yes | yes |

- `0x002F8E90(record)` classifies a record: kind 0 gives 2 for an Esper and 1 otherwise; kind 1 gives
  4 when the owning unit's actor class nibble (`0x00263C20`) is 3, 8 when it is 1, 2 or 7, else 16.
- `0x002F8BB0(recipient, source)` pays experience only for a kind-0 recipient with a unit, outside the
  Espers (the Chocobo, type 26, included), without a terminal status, from a kind-1 source. The amount is
  `(source level +0x1C2 - +0x88) * [source +0xE78] +0x34 + [source +0xE70] +0x34`.
- When `0x003135C0()` is 0 that amount becomes `amount / n` (`idiv`, `0x002F8D1C`-`0x002F8D1D`; 0 when
  `n` is 0) for the count `n` of party members (`0x0031B810(0..3)`) that are alive, not Espers
  and not the Chocobo (type 26); otherwise it is paid whole to the `0x00313800` member. It is doubled when
  `(+0x6B | +0x7B) & 0x08` and zeroed when `(+0x6B | +0x7B) & 0x20` (`0x002F8D26`-`0x002F8D40`).
- `0x002F90C0(recipient, source)` pays licence points, when `0x00264150()` is 0, for a kind-0 recipient
  of type 26 (the Chocobo), below 7 or above 39 without a terminal status, from a kind-1 source: `(level - +0x88) * [source +0xE78] +0x2F + [source +0xE70] +0x2F`,
  doubled when `(+0x6B | +0x7B) & 0x10` (`0x002F914B`-`0x002F9157`).
- `0x00309230(unit, actionRow)` returns the row's word `+0x24` as the presentation code, except for
  action row `0x113`, where an Esper type gets `42 + 3 * (type - 27)`.
- `0x0050FF20`, a script verb's handler, resolves its operand through `0x00320AB0(value, 3)` and pushes
  -2 for no record, -1 for kind 1, and the class above for kind 0.

## Layouts

```python
definition id (u16)
mask 0xFF00  kind       0 party table 0x02EBF130, 1 enemy table 0x02EBF120, other: nothing installed
mask 0xFF   index      the row; for kind 0 also the type byte at stats +0x04
```

Struct EnemyRow table=`0x02EBF120` (stride at table `+0x08`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | classRow | row of `0x02EBF150` (the class row at unit `+0xE68`) |
| `+0x02` | `u8` | counterSlot | spawn counter index, `0xFF` for no counter |
| `+0x03` | `u8` | flags | mask `0x3` the tracked-HP class (`0x00328FF0`, flag bit `0x80000000000`); bit `0x10`: unit `+0x58` = 7 (`0x00238BF0`), the motion height without its random part (`0x002362A4`), a test of the gambit selector (`0x0030268D`); bit `0x20`: the shadow kind, through `0x002E8A10` |
| `+0x08` | `u16` | nameRef | bank << 11 \| entry into `0x02EBF170` |
| `+0x0A` | `i16[3]` | scalePercent | 0 means 100; divided by 100 and handed to `0x002E5FD0` (`0x00238D1B`-`0x00238D68`) |
| `+0x11` | `u8[2]` | variant | `+0x12` then `+0x11`, the model's variant bytes (`0x0031C5AB`, `0x0031C5B1`) |
| `+0x13` | `u8` | animSet | `0xFF` for the weapon's (`0x003202F0`) |
| `+0x15` | `u8` | flags2 | bit `0x1` Attack and weapon evade, bit `0x2` shield and magick evade from the stat rows (`0x002FEF30`); bit `0x4` also sets flag bit `0x80000000000`; bit `0x8` (`0x0031AACF`) and the bits under mask `0x18` (`0x0031AB39`) in the target-information query `0x0031AA30` |
| `+0x16` | `u16` | equipment0 |  |
| `+0x18` | `u32` | startHp | 0 for no starting HP (`0x0023A410`) |
| `+0x1C` | `u16` | equipment1 |  |
| `+0x22` | `u16` | rewardRow | row of `0x02EBF148` (unit `+0xE70`) |
| `+0x24` | `u16` | rewardLevelRow | row of `0x02EBF140` (unit `+0xE78`) |
| `+0x26` | `i16` | voiceBank | negative for the model's (`0x003212E0`) |
| `+0x28` | `u16[5]` | drops | the five drop slots (`0x003180F0`) |
| `+0x32` | `u16` | steal0 | `0xFFFF` for no item; record `+0x14` bit `0x1` |
| `+0x34` | `u16` | steal1 | bit `0x2` |
| `+0x36` | `u16` | steal2 | bit `0x4` |
| `+0x38` | `u32[2]` | partIds | part 8 entries 0 and 1 of the model rebuild (`0x0031C000` through `0x0031BEC0`) |
| `+0x40` | `u8[2]` | partLinks | their attach links, `0x00D107F8`[byte] (`0x0031BE30`) |
| `+0x42` | `u8[2]` | extraChance | the two Monograph drop chances (`0x003180F0`) |
| `+0x44` | `u16[2]` | poach | 95 % and 5 % (`0x00390680`) |
| `+0x48` | `u16[4]` | extraDrops | key item, item, key item, item (`0x003180F0`) |
| `+0x50` | `u16[4]` | logicRows | rows of `0x02EBF168` for orders 0-3; `+0x50` at install (unit `+0x6E0`), all four through `0x002FDDA0` and `0x00239040` |

Struct PartyRow table=`0x02EBF130` (stride at table `+0x08`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A` | `u16[5]` | equipment | slots 0-4 |
| `+0x14` | `u16` | gambitPreset |  |
| `+0x16` | `u16` | baseHp |  |
| `+0x1A` | `u16` | baseMp |  |
| `+0x1E` | `u8` | baseStat0 | with `+0x21`, `+0x24`, `+0x27`: the four float stats |
| `+0x2B` | `u8` | scale | unit `+0x68` and `+0x6C` (times 1.5) |
| `+0x2C` | `u8` | flags | bit `0x40` sets record `+0x00` bit `0x4` |
| `+0x2E` | `u8` | startLevel | 0 means 1 |
| `+0x30` | `u16` | nameRef |  |
| `+0x44` | `u16` | startLp |  |
| `+0x46` | `u8` | baseStat4 | unit stat `+0x20`, raised to the licence rank |
| `+0x47` | `u8` | startMpPercent |  |

Class row (`0x02EBF150`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | model | a bound id, letter class in the bits under mask `0xFF0000` (`0x0031C2F0`) |
| `+0x04` | `u8` | type | unit `+0x55` |
| `+0x05` | `u8` | kind | unit `+0x56` |
| `+0x06` | `u16` | clanEntry | unit `+0x52` |
| `+0x10` | `i16` | separation | tenths; a positive value / 10 to `0x0026DAC0` (`0x00238CEB`) |
| `+0x12` | `u8` | flags | bits `0x7` the effect column (`0x00329FB3`); bit `0x10` actor `+0x09` bit `0x40` (`0x0026A3A0`); bit `0x20` the view query's kind (`0x0031B394`); bit `0x40` actor `+0x08` bit `0x8` and `+0x09` bit `0x40` (`0x0026A430`); bit `0x80` `0x003879C0`, `0x00390AB0`, `0x0033D660` |
| `+0x18` | `u8` | group | bits `0xE` a movement group, 4 noticing every unit (`0x003248F8`); mask `0x70` the placement height (`0x00239E10`) |
| `+0x20` | `u8` | comboCap | hits at most this - 1 (`0x00388845`) |
| `+0x21` | `u8` | flags21 | bit `0x2` an enemy may back off (`0x00334204`) |
| `+0x22` | `u8` | facing | unit `+0x64` = value * 2π / 360 |
| `+0x23` | `u8` | scale | unit `+0x68` |
| `+0x25` | `u8` | sightRadius | `0x003247F0` |
| `+0x26` | `u8` | lowHpRadius | units below 40 % HP (`0x003247F0`) |
| `+0x27` | `u8` | scale2 | unit `+0x6C` |
| `+0x28` | `u8` | flags28 | bit `0x1` the view query's height (`0x0031B08D`); bit `0x2` no chain (`0x00317F09`) |
| `+0x29` | `u8[5]` | affinity | absorb, halve, nullify, weak, potency (`0x002FEF30`) |
| `+0x30` | `u16[8]` | words30 | no reader among the four readers of `0x02EBF150` and the 47 loads of unit `+0xE68`, each followed to its fields |
| `+0x40` | `u16` | modelFamily | the same-model run (`0x00317F77`) |
| `+0x52` | `u16` | species | `0xFFFF` no entry (`0x003171C0`) |

## Modding notes

- An enemy's statuses and augments are not in its row: the installer writes no status or augment, and the masks
  the recompute reads come from the enemy's script ([augments](../Damage-And-Battle-Formulas/augments.md)).
- Giving a party member a starting level sets its experience to exactly that level's threshold
  and strips every status in the two masks; the MP starts at the row's percentage of capacity.
- A type between 27 and 39 earns nothing and is tested by one predicate (`type - 27 <= 12`)
  wherever the Espers matter; the Chocobo, type 26, is a separate test with its own rule.

## Related

- [Battle units](battle-units.md): the pool, the bind and the handle the re-key replaces.
- [Battle unit fields](battle-unit-fields.md): the unit record the installer fills.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the stats record field by field.
- [EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md) and [stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md): the curve and the grower.
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md): the spawn record and the lane map.
- [Bestiary](../Enemy-Spawning/bestiary.md): every shipped enemy definition with these fields decoded.
