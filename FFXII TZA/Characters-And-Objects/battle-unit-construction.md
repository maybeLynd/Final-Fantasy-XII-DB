---
title: "Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition"
kind: "system"
category: "Characters and objects"
addresses: "0023A570, 0023AC80, 0030C470, 0030C650, 002F8F20, 00236100, 002B58B0, 00322050, 003220E0, 00322C50, 00323790, 0031A630, 00323910, 00327CB0, 00326030, 00327DE0, 002F8E90, 002F90C0, 002F8BB0, 0050FF20, 00309230, 00254A40"
---

## What the player sees

A battle unit becomes something when a definition is applied to it: Vaan with his level, equipment,
licences and gambits, or a Wolf with its stats, its one weapon and its loot flags. Party members
come from one authored table and enemies from the area's enemy table, and every piece of combat
code can tell the two apart by one byte in the unit's stats record. A narrower split of the party
side, by the type number, decides who earns experience and licence points and who is only a guest
or a summoned creature.

## How it works

### The installer and the definition id

`0023A570(unit, id)` applies definition `id` to a unit. The id's high byte is the kind (0 party, 1
enemy, anything else installs nothing and clears unit flag bit 26) and its low byte the row index.
Before anything else the installer:

1. remembers the unit's previous id, the stats record's word `+04`<sub>h</sub>, when unit flag bit 2 is set
   (`FFFF`<sub>h</sub> otherwise), and resets the unit with `00236A60` ([battle unit fields](battle-unit-fields.md));
2. returns 0 when the battle system is down (`02089300` = 0);
3. re-keys the unit (`00322050`) when the kind byte is not 0 or the previous id differs from both
   the new id and `FFFF`<sub>h</sub>; with `00303EC0()` set, the check is skipped only when `00304630()`
   (`FF`<sub>h</sub> read as `FFFF`<sub>h</sub>) equals the previous id and the new id is `FFFF`<sub>h</sub>.

`00322050(unit)` zeroes the attacker mask `+EA4`<sub>h</sub> and count `+EA8`<sub>h</sub> and stores
`003220E0(actor)` at `+08`<sub>h</sub>: that function encodes the actor's current handle, advances the actor's
discriminator (`002659D0`), encodes the new handle, and, when the party focus record `00327150()`
held the old handle, stores the re-keyed unit's stats byte `+04`<sub>h</sub> (or `FF`<sub>h</sub>) as a dword at
`[02EBF190] + 5AA4h` and runs `00326500`, which picks the default controlled member and requests its handle
([Party leader](../Party/party-leader.md)).

### The enemy path

With kind 1 the unit must have flag bit 26 set. The installer then:

1. takes row `index` of the enemy table `02EBF120` (count at `+04`<sub>h</sub>, row stride at `+08`<sub>h</sub>,
   rows from the section at `+0C`<sub>h</sub>), and the class row the enemy row's word `+00`<sub>h</sub> names in
   `02EBF150`; the row's words `+50`<sub>h</sub>, `+22`<sub>h</sub> and `+24`<sub>h</sub> must be below the counts of `02EBF168`
   (word `+0`), `02EBF148` and `02EBF140`, else it returns 0;
2. resolves the spawn record: `00236100(unit +40h, unit +57h)` reads the lane map's byte
   `1 + lane` (lane below the map's count byte, entry not `FF`<sub>h</sub>) and returns
   `0208E690 + entry * 250h`; no record returns 0. The stats record is that record's `+80`<sub>h</sub>;
3. for a fresh record (record byte `+0` without bits 0 and 2) it initialises the stats record
   (`0023AC80`, below) and sets the steal bits at record `+14`<sub>h</sub>: bits 0, 1 and 2 when the row's
   words `+32`<sub>h</sub>, `+34`<sub>h</sub> and `+36`<sub>h</sub> are not `FFFF`<sub>h</sub>;
4. still for a fresh record, when the row's byte `+02`<sub>h</sub> is not `FF`<sub>h</sub>, it reads the spawn counter
   `0208D354 + (0208D454 * 64 + byte) * 2`, stores the old value's low byte at record `+12`<sub>h</sub> and
   writes back `old + 1`, or 1 once `old` reaches `00254A40()`; with a byte of `FF`<sub>h</sub> it stores 0 at
   `+12`<sub>h</sub>;
4. resolves the name text: the row's word `+08`<sub>h</sub> split as bank (high 5 bits) and entry (low 11
   bits) through `02EBF170`, then `002B58B0(block, 0)`;
5. stores `+E60`<sub>h</sub> = the enemy row, `+E68`<sub>h</sub> = the class row, `+6E0`<sub>h</sub> = the `02EBF168` row named by
   word `+50`<sub>h</sub>, `+E70`<sub>h</sub> = the `02EBF148` row named by word `+22`<sub>h</sub>, `+E78`<sub>h</sub> = the `02EBF140` row
   named by word `+24`<sub>h</sub>;
6. registers the unit (`00328FF0(0, row byte +03h & 3, unit +EA9h)`: the class to `02EC1384` and
   the slot to `02EC1380`, written only when the class is not 0 or the slot is negative), and sets
   flag bit 43 when `row byte +03h & 3` or `row byte +15h` bit 2 is set, else clears it.

The common stores then take, from the class row: `+64`<sub>h</sub> = byte `+22`<sub>h</sub> times 2π/360, `+55`<sub>h</sub> =
byte `+04`<sub>h</sub>, `+68`<sub>h</sub> = float(byte `+23`<sub>h</sub>), `+56`<sub>h</sub> = byte `+05`<sub>h</sub>, `+6C`<sub>h</sub> = float(byte `+27`<sub>h</sub>),
`+52`<sub>h</sub> = word `+06`<sub>h</sub>.

### The party path

With kind 0 the index must pass `00322C50(2, index, 1)`, the party table's count. The installer
takes row `index` of the party table `02EBF130`, points the stats at the battle-state block's
element `[02EBF190] + 8 + index * 1C8h` with no spawn record, resolves the name from the row's
word `+30`<sub>h</sub> the same way, and stores `+6E0`<sub>h</sub> = `02089378 + index * 170h`, `+6F0`<sub>h</sub> = `01E09350`,
`+E60`<sub>h</sub> = the row, `+64`<sub>h</sub> = 2π, `+6C`<sub>h</sub> = row byte `+2B`<sub>h</sub> times 1.5, `+68`<sub>h</sub> = float(row byte
`+2B`<sub>h</sub>), `+55`<sub>h</sub> = `FF`<sub>h</sub>, `+56`<sub>h</sub> = `FF`<sub>h</sub>, `+52`<sub>h</sub> = `FFFF`<sub>h</sub>.

### The common stores

Both paths end with: `+48`<sub>h</sub> = 0 (the HP floor), `+698`<sub>h</sub> = the stats record, `+6A0`<sub>h</sub> = the spawn
record or null, `+18`<sub>h</sub> = the name text, `+54`<sub>h</sub> = `FF`<sub>h</sub>, then `00237040(unit)` and
`002FEAB0(unit)`. When the stats record is null, or its status words `+3Ch | +64h` carry bits 0, 1
or 31 outside a town (`00377C20`), flag bit 26 is cleared and bit 1 set. Bit 2 is set and the
installer returns 1.

### The fresh stats record

`0023AC80(record, id)` fills a stats record from nothing:

1. `memset` of `1C8`<sub>h</sub> bytes, then `+50`<sub>h</sub> = all ones (8 bytes), `+58`<sub>h</sub> = `FFFF`<sub>h</sub>, `+1C3`<sub>h</sub> = `FFFF`<sub>h</sub>,
   `+1C5`<sub>h</sub> = `FF`<sub>h</sub>; with `02089300` = 0 it returns 0;
2. kind 0 takes the party row and the level `max(row byte +2Eh, 1)`; kind 1 takes the enemy row and
   level 1; any other kind returns 0;
3. `+04`<sub>h</sub> = the whole id, so the byte `+05`<sub>h</sub> is the kind by construction; then the level grower
   `0030C470(record, level, kind)`;
4. kind 0: the LP `00323790(record, row word +44h)`; for an index below 7, every licence entry of
   `02EBF038` whose byte `+07`<sub>h</sub> has bit `index` set is granted (`00323910(record, entry, 1)`);
5. kind 0: equipment slots 0-4 from the row's words `+0A`<sub>h</sub>, `+0C`<sub>h</sub>, `+0E`<sub>h</sub>, `+10`<sub>h</sub>, `+12`<sub>h</sub>
   (`0031A630`); the gambit preset `00327CB0(record, row word +14h)`, `00326030([02EBF190], index)`
   and `00327DE0([02EBF190] + 8 + index * 1C8h)`; and record `+00`<sub>h</sub> bit 2 when the row's byte
   `+2C`<sub>h</sub> has bit 6;
6. kind 1: equipment slot 0 from the row's word `+16`<sub>h</sub>, slot 1 from `+1C`<sub>h</sub>, slots 2-4 `FFFF`<sub>h</sub>.

### The level grower

`0030C470(record, level, kind)` starts from level 0 and grows up:

1. `+1C2`<sub>h</sub> = 0; for kind 0 the base values come from the party row named by `+04`<sub>h</sub>: `+08`<sub>h</sub> =
   word `+16`<sub>h</sub>, `+0C`<sub>h</sub> = word `+1A`<sub>h</sub>, `+10`<sub>h</sub>, `+14`<sub>h</sub>, `+18`<sub>h</sub>, `+1C`<sub>h</sub> = the floats of bytes
   `+1E`<sub>h</sub>, `+21`<sub>h</sub>, `+24`<sub>h</sub>, `+27`<sub>h</sub>, `+20`<sub>h</sub> = the larger of byte `+46`<sub>h</sub> and the licence rank
   `00324100(record)`; for kind 1 only `+88`<sub>h</sub> = the kind argument (1 from the initialiser); any
   other kind returns;
2. `0030C650(record, level, 2)` grows to the level ([stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md));
3. `+18C`<sub>h</sub> = `min(002F8F20(level - 1), 99999999)`, the experience of the level reached
   ([EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md));
4. when the status masks `0208D320` or `0208D324` are non-zero, the statuses in their union are
   removed (`0030F690(record, union)`); HP and MP are reconciled to their capacities (`0030F340`,
   `0030F5A0`);
5. the starting MP: `cap` = `+28`<sub>h</sub> when the layer bytes `+6C`<sub>h</sub> and `+7C`<sub>h</sub> are both non-negative,
   else 0; kind 0 sets `+4C`<sub>h</sub> = `cap * row byte +47h / 100`, kind 1 sets `+4C`<sub>h</sub> = `cap`;
6. `0030FED0(record, 0)` rebuilds the derived state ([augments](../Damage-And-Battle-Formulas/augments.md)).

### The kind byte and the type partition

Stats byte `+05`<sub>h</sub> is the kind: 0 for a party-table unit, 1 for an enemy. Stats byte `+04`<sub>h</sub> is the
row index, and for kind 0 it is the type the code partitions:

| Type | Span | `0050FF20` class | Experience (`002F8BB0`) | Licence points (`002F90C0`) |
|---|---|---|---|---|
| 0-6 | the main characters | 0 | yes | yes |
| 7-25 | the guest range | 1 | yes | no |
| 26 | the Chocobo | 3 | yes, but not counted in the split | yes |
| 27-39 | the thirteen Espers, Belias to Zodiark | 2 | no | no |
| 40 and above | | 0 | yes | yes |

- `002F8E90(record)` classifies a record: kind 0 gives 2 for an Esper and 1 otherwise; kind 1 gives
  4 when the owning unit's actor class nibble (`00263C20`) is 3, 8 when it is 1, 2 or 7, else 16.
- `002F8BB0(recipient, source)` pays experience only for a kind-0 recipient with a unit, outside the
  Espers (the Chocobo, type 26, included), without a terminal status, from a kind-1 source. The amount is
  `(source level +1C2h - +88h) * [source +E78h] +34h + [source +E70h] +34h`.
- When `003135C0()` is 0 that amount becomes `amount / n` (`idiv`, `002F8D1C`-`002F8D1D`; 0 when
  `n` is 0) for the count `n` of party members (`0031B810(0..3)`) that are alive, not Espers
  and not the Chocobo (type 26); otherwise it is paid whole to the `00313800` member. It is doubled when
  `(+6Bh | +7Bh) & 08h` and zeroed when `(+6Bh | +7Bh) & 20h` (`002F8D26`-`002F8D40`).
- `002F90C0(recipient, source)` pays licence points, when `00264150()` is 0, for a kind-0 recipient
  of type 26 (the Chocobo), below 7 or above 39 without a terminal status, from a kind-1 source: `(level - +88h) * [source +E78h] +2Fh + [source +E70h] +2Fh`,
  doubled when `(+6Bh | +7Bh) & 10h` (`002F914B`-`002F9157`).
- `00309230(unit, actionRow)` returns the row's word `+24`<sub>h</sub> as the presentation code, except for
  action row `113`<sub>h</sub>, where an Esper type gets `42 + 3 * (type - 27)`.
- `0050FF20`, a script verb's handler, resolves its operand through `00320AB0(value, 3)` and pushes
  -2 for no record, -1 for kind 1, and the class above for kind 0.

## Layouts

```python
definition id (u16)
bits 8-15  kind       0 party table 02EBF130, 1 enemy table 02EBF120, other: nothing installed
bits 0-7   index      the row; for kind 0 also the type byte at stats +0x04
```

Struct EnemyRow table=`02EBF120` (stride at table +`08`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | classRow | row of `02EBF150` (the class row at unit +`E68`<sub>h</sub>) |
| `02`<sub>h</sub> | `u8` | counterSlot | spawn counter index, `FF`<sub>h</sub> for none |
| `03`<sub>h</sub> | `u8` | flags | bits 0-1 the tracked-HP class (`00328FF0`, flag bit 43); bit 4: unit +`58`<sub>h</sub> = 7 (`00238BF0`), the motion height without its random part (`002362A4`), a test of the gambit selector (`0030268D`); bit 5: the shadow kind, through `002E8A10` |
| `08`<sub>h</sub> | `u16` | nameRef | bank << 11 \| entry into `02EBF170` |
| `0A`<sub>h</sub> | `i16[3] scalePercent` | 0 means 100; divided by 100 and handed to 002E5FD0 (00238D1B-00238D68) |  |
| `11`<sub>h</sub> | `u8[2] variant` | `+12`<sub>h</sub> then `+11`<sub>h</sub>, the model's variant bytes (0031C5AB, 0031C5B1) |  |
| `13`<sub>h</sub> | `u8` | animSet | `FF`<sub>h</sub> for the weapon's (`003202F0`) |
| `15`<sub>h</sub> | `u8` | flags2 | bit 0 Attack and weapon evade, bit 1 shield and magick evade from the stat rows (`002FEF30`); bit 2 also sets flag bit 43; bit 3 (`0031AACF`) and bits 3-4 (`0031AB39`) in the target-information query `0031AA30` |
| `16`<sub>h</sub> | `u16` | equipment0 |  |
| `18`<sub>h</sub> | `u32` | startHp | 0 for none (`0023A410`) |
| `1C`<sub>h</sub> | `u16` | equipment1 |  |
| `22`<sub>h</sub> | `u16` | rewardRow | row of `02EBF148` (unit +`E70`<sub>h</sub>) |
| `24`<sub>h</sub> | `u16` | rewardLevelRow | row of `02EBF140` (unit +`E78`<sub>h</sub>) |
| `26`<sub>h</sub> | `i16` | voiceBank | negative for the model's (`003212E0`) |
| `28`<sub>h</sub> | `u16[5] drops` | the five drop slots (003180F0) |  |
| `32`<sub>h</sub> | `u16` | steal0 | `FFFF`<sub>h</sub> for none; record +`14`<sub>h</sub> bit 0 |
| `34`<sub>h</sub> | `u16` | steal1 | bit 1 |
| `36`<sub>h</sub> | `u16` | steal2 | bit 2 |
| `38`<sub>h</sub> | `u32[2] partIds` | part 8 entries 0 and 1 of the model rebuild (0031C000 through 0031BEC0) |  |
| `40`<sub>h</sub> | `u8[2] partLinks` | their attach links, 00D107F8[byte] (0031BE30) |  |
| `42`<sub>h</sub> | `u8[2] extraChance` | the two Monograph drop chances (003180F0) |  |
| `44`<sub>h</sub> | `u16[2] poach` | 95 % and 5 % (00390680) |  |
| `48`<sub>h</sub> | `u16[4] extraDrops` | key item, item, key item, item (003180F0) |  |
| `50`<sub>h</sub> | `u16[4] logicRows` | rows of 02EBF168 for orders 0-3; `+50`<sub>h</sub> at install (unit `+6E0`<sub>h</sub>), all four | through `002FDDA0` and `00239040` |

Struct PartyRow table=`02EBF130` (stride at table +`08`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0A`<sub>h</sub> | `u16[5] equipment` | slots 0-4 |  |
| `14`<sub>h</sub> | `u16` | gambitPreset |  |
| `16`<sub>h</sub> | `u16` | baseHp |  |
| `1A`<sub>h</sub> | `u16` | baseMp |  |
| `1E`<sub>h</sub> | `u8` | baseStat0 | with +`21`<sub>h</sub>, +`24`<sub>h</sub>, +`27`<sub>h</sub>: the four float stats |
| `2B`<sub>h</sub> | `u8` | scale | unit +`68`<sub>h</sub> and +`6C`<sub>h</sub> (times 1.5) |
| `2C`<sub>h</sub> | `u8` | flags | bit 6 sets record +`00`<sub>h</sub> bit 2 |
| `2E`<sub>h</sub> | `u8` | startLevel | 0 means 1 |
| `30`<sub>h</sub> | `u16` | nameRef |  |
| `44`<sub>h</sub> | `u16` | startLp |  |
| `46`<sub>h</sub> | `u8` | baseStat4 | unit stat +`20`<sub>h</sub>, raised to the licence rank |
| `47`<sub>h</sub> | `u8` | startMpPercent |  |

Class row (`02EBF150`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | model | a bound id, letter class in bits 16-23 (`0031C2F0`) |
| `04`<sub>h</sub> | `u8` | type | unit +`55`<sub>h</sub> |
| `05`<sub>h</sub> | `u8` | kind | unit +`56`<sub>h</sub> |
| `06`<sub>h</sub> | `u16` | clanEntry | unit +`52`<sub>h</sub> |
| `10`<sub>h</sub> | `i16` | separation | tenths; a positive value / 10 to `0026DAC0` (`00238CEB`) |
| `12`<sub>h</sub> | `u8` | flags | bits 0-2 the effect column (`00329FB3`); bit 4 actor +`09`<sub>h</sub> bit 6 (`0026A3A0`); bit 5 the view query's kind (`0031B394`); bit 6 actor +`08`<sub>h</sub> bit 3 and +`09`<sub>h</sub> bit 6 (`0026A430`); bit 7 `003879C0`, `00390AB0`, `0033D660` |
| `18`<sub>h</sub> | `u8` | group | bits 1-3 a movement group, 4 noticing every unit (`003248F8`); bits 4-6 the placement height (`00239E10`) |
| `20`<sub>h</sub> | `u8` | comboCap | hits at most this - 1 (`00388845`) |
| `21`<sub>h</sub> | `u8` | flags21 | bit 1 an enemy may back off (`00334204`) |
| `22`<sub>h</sub> | `u8` | facing | unit +`64`<sub>h</sub> = value * 2π / 360 |
| `23`<sub>h</sub> | `u8` | scale | unit +`68`<sub>h</sub> |
| `25`<sub>h</sub> | `u8` | sightRadius | `003247F0` |
| `26`<sub>h</sub> | `u8` | lowHpRadius | units below 40 % HP (`003247F0`) |
| `27`<sub>h</sub> | `u8` | scale2 | unit +`6C`<sub>h</sub> |
| `28`<sub>h</sub> | `u8` | flags28 | bit 0 the view query's height (`0031B08D`); bit 1 no chain (`00317F09`) |
| `29`<sub>h</sub> | `u8[5] affinity` | absorb, halve, nullify, weak, potency (002FEF30) |  |
| `30`<sub>h</sub> | `u16[8] words30` | no reader among the four readers of 02EBF150 and the 47 loads of unit | +`E68`<sub>h</sub>, each followed to its fields |
| `40`<sub>h</sub> | `u16` | modelFamily | the same-model run (`00317F77`) |
| `52`<sub>h</sub> | `u16` | species | `FFFF`<sub>h</sub> none (`003171C0`) |

## Modding notes

- An enemy's statuses and augments are not in its row: the installer writes none, and the masks
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
