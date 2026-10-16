---
title: "Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition"
kind: "system"
category: "Characters and objects"
summary: "How a battle unit becomes a party member or an enemy from a definition id: the installer's split on the id's high byte, the enemy path through the area's enemy table and the spawn record, the party path through the party table and the battle-state block, the common stores, the fresh stats record with its level, equipment, licences, gambits and starting MP, the level grower and the experience curve, the handle re-key on a definition change, the kind byte at stats +5, and the partition of the type byte that the reward, availability and script code test."
addresses: ["0023A570", "0023AC80", "0030C470", "0030C650", "002F8F20", "00236100", "002B58B0", "00322050", "003220E0", "00322C50", "00323790", "0031A630", "00323910", "00327CB0", "00326030", "00327DE0", "002F8E90", "002F90C0", "002F8BB0", "0050FF20", "00309230", "00254A40"]
---

# Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition

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

1. remembers the unit's previous id, the stats record's word `+0x04`, when unit flag bit 2 is set
   (`0xFFFF` otherwise), and resets the unit with `00236A60` ([battle unit fields](battle-unit-fields.md));
2. returns 0 when the battle system is down (`02089300` = 0);
3. re-keys the unit (`00322050`) when the kind byte is not 0 or the previous id differs from both
   the new id and `0xFFFF`; with `00303EC0()` set, the check is skipped only when `00304630()`
   (`0xFF` read as `0xFFFF`) equals the previous id and the new id is `0xFFFF`.

`00322050(unit)` zeroes the attacker mask `+0xEA4` and count `+0xEA8` and stores
`003220E0(actor)` at `+0x08`: that function encodes the actor's current handle, advances the actor's
discriminator (`002659D0`), encodes the new handle, and, when the party focus record `00327150()`
held the old handle, stores the re-keyed unit's stats byte `+0x04` (or `0xFF`) as a dword at
`[02EBF190] + 0x5AA4` and runs `00326500`.

### The enemy path

With kind 1 the unit must have flag bit 26 set. The installer then:

1. takes row `index` of the enemy table `02EBF120` (count at `+0x04`, row stride at `+0x08`,
   rows from the section at `+0x0C`), and the class row the enemy row's word `+0x00` names in
   `02EBF150`; the row's words `+0x50`, `+0x22` and `+0x24` must be below the counts of `02EBF168`
   (word `+0`), `02EBF148` and `02EBF140`, else it returns 0;
2. resolves the spawn record: `00236100(unit +0x40, unit +0x57)` reads the lane map's byte
   `1 + lane` (lane below the map's count byte, entry not `0xFF`) and returns
   `0208E690 + entry * 0x250`; no record returns 0. The stats record is that record's `+0x80`;
3. for a fresh record (record byte `+0` without bits 0 and 2) it initialises the stats record
   (`0023AC80`, below) and sets the steal bits at record `+0x14`: bits 0, 1 and 2 when the row's
   words `+0x32`, `+0x34` and `+0x36` are not `0xFFFF`;
4. still for a fresh record, when the row's byte `+0x02` is not `0xFF`, it reads the spawn counter
   `0208D354 + (0208D454 * 64 + byte) * 2`, stores the old value's low byte at record `+0x12` and
   writes back `old + 1`, or 1 once `old` reaches `00254A40()`; with a byte of `0xFF` it stores 0 at
   `+0x12`;
4. resolves the name text: the row's word `+0x08` split as bank (high 5 bits) and entry (low 11
   bits) through `02EBF170`, then `002B58B0(block, 0)`;
5. stores `+0xE60` = the enemy row, `+0xE68` = the class row, `+0x6E0` = the `02EBF168` row named by
   word `+0x50`, `+0xE70` = the `02EBF148` row named by word `+0x22`, `+0xE78` = the `02EBF140` row
   named by word `+0x24`;
6. registers the unit (`00328FF0(0, row byte +0x03 & 3, unit +0xEA9)`: the class to `02EC1384` and
   the slot to `02EC1380`, written only when the class is not 0 or the slot is negative), and sets
   flag bit 43 when `row byte +0x03 & 3` or `row byte +0x15` bit 2 is set, else clears it.

The common stores then take, from the class row: `+0x64` = byte `+0x22` times 2π/360, `+0x55` =
byte `+0x04`, `+0x68` = float(byte `+0x23`), `+0x56` = byte `+0x05`, `+0x6C` = float(byte `+0x27`),
`+0x52` = word `+0x06`.

### The party path

With kind 0 the index must pass `00322C50(2, index, 1)`, the party table's count. The installer
takes row `index` of the party table `02EBF130`, points the stats at the battle-state block's
element `[02EBF190] + 8 + index * 0x1C8` with no spawn record, resolves the name from the row's
word `+0x30` the same way, and stores `+0x6E0` = `02089378 + index * 0x170`, `+0x6F0` = `01E09350`,
`+0xE60` = the row, `+0x64` = 2π, `+0x6C` = row byte `+0x2B` times 1.5, `+0x68` = float(row byte
`+0x2B`), `+0x55` = `0xFF`, `+0x56` = `0xFF`, `+0x52` = `0xFFFF`.

### The common stores

Both paths end with: `+0x48` = 0 (the HP floor), `+0x698` = the stats record, `+0x6A0` = the spawn
record or null, `+0x18` = the name text, `+0x54` = `0xFF`, then `00237040(unit)` and
`002FEAB0(unit)`. When the stats record is null, or its status words `+0x3C | +0x64` carry bits 0, 1
or 31 outside a town (`00377C20`), flag bit 26 is cleared and bit 1 set. Bit 2 is set and the
installer returns 1.

### The fresh stats record

`0023AC80(record, id)` fills a stats record from nothing:

1. `memset` of `0x1C8` bytes, then `+0x50` = all ones (8 bytes), `+0x58` = `0xFFFF`, `+0x1C3` = `0xFFFF`,
   `+0x1C5` = `0xFF`; with `02089300` = 0 it returns 0;
2. kind 0 takes the party row and the level `max(row byte +0x2E, 1)`; kind 1 takes the enemy row and
   level 1; any other kind returns 0;
3. `+0x04` = the whole id, so the byte `+0x05` is the kind by construction; then the level grower
   `0030C470(record, level, kind)`;
4. kind 0: the LP `00323790(record, row word +0x44)`; for an index below 7, every licence entry of
   `02EBF038` whose byte `+0x07` has bit `index` set is granted (`00323910(record, entry, 1)`);
5. kind 0: equipment slots 0-4 from the row's words `+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12`
   (`0031A630`); the gambit preset `00327CB0(record, row word +0x14)`, `00326030([02EBF190], index)`
   and `00327DE0([02EBF190] + 8 + index * 0x1C8)`; and record `+0x00` bit 2 when the row's byte
   `+0x2C` has bit 6;
6. kind 1: equipment slot 0 from the row's word `+0x16`, slot 1 from `+0x1C`, slots 2-4 `0xFFFF`.

### The level grower

`0030C470(record, level, kind)` starts from level 0 and grows up:

1. `+0x1C2` = 0; for kind 0 the base values come from the party row named by `+0x04`: `+0x08` =
   word `+0x16`, `+0x0C` = word `+0x1A`, `+0x10`, `+0x14`, `+0x18`, `+0x1C` = the floats of bytes
   `+0x1E`, `+0x21`, `+0x24`, `+0x27`, `+0x20` = the larger of byte `+0x46` and the licence rank
   `00324100(record)`; for kind 1 only `+0x88` = the kind argument (1 from the initialiser); any
   other kind returns;
2. `0030C650(record, level, 2)` grows to the level ([stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md));
3. `+0x18C` = `min(002F8F20(level - 1), 99999999)`, the experience of the level reached
   ([EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md));
4. when the status masks `0208D320` or `0208D324` are non-zero, the statuses in their union are
   removed (`0030F690(record, union)`); HP and MP are reconciled to their capacities (`0030F340`,
   `0030F5A0`);
5. the starting MP: `cap` = `+0x28` when the layer bytes `+0x6C` and `+0x7C` are both non-negative,
   else 0; kind 0 sets `+0x4C` = `cap * row byte +0x47 / 100`, kind 1 sets `+0x4C` = `cap`;
6. `0030FED0(record, 0)` rebuilds the derived state ([augments](../Damage-And-Battle-Formulas/augments.md)).

### The kind byte and the type partition

Stats byte `+0x05` is the kind: 0 for a party-table unit, 1 for an enemy. Stats byte `+0x04` is the
row index, and for kind 0 it is the type the code partitions:

| Type | Span | `0050FF20` class | Experience (`002F8BB0`) | Licence points (`002F90C0`) |
|---|---|---|---|---|
| 0-6 | the main characters | 0 | yes | yes |
| 7-25 | the guest range | 1 | yes | no |
| 26 | a single value | 3 | yes, but not counted in the split | yes |
| 27-39 | the band of thirteen | 2 | no | no |
| 40 and above | | 0 | yes | yes |

- `002F8E90(record)` classifies a record: kind 0 gives 2 for the band and 1 otherwise; kind 1 gives
  4 when the owning unit's actor class nibble (`00263C20`) is 3, 8 when it is 1, 2 or 7, else 16.
- `002F8BB0(recipient, source)` pays experience only for a kind-0 recipient with a unit, outside the
  band (type 26 included), without a terminal status, from a kind-1 source. The amount is
  `(source level +0x1C2 - +0x88) * [source +0xE78] +0x34 + [source +0xE70] +0x34`.
- That amount is divided among the party members (`0031B810(0..3)`) that are alive, outside the
  band and not type 26 when `003135C0()` is 0, or paid whole to the `00313800` member otherwise;
  it is doubled by layer bit 3 at `+0x6B` or `+0x7B` and zeroed by bit 5.
- `002F90C0(recipient, source)` pays licence points, when `00264150()` is 0, for a kind-0 recipient
  of type 26, below 7 or above 39 without a terminal status, from a kind-1 source: `(level - +0x88) * [source +0xE78] +0x2F + [source +0xE70] +0x2F`,
  doubled by layer bit 4.
- `00309230(unit, actionRow)` returns the row's word `+0x24` as the presentation code, except for
  action row `0x113`, where a band type gets `42 + 3 * (type - 27)`.
- `0050FF20`, a script verb's handler, resolves its operand through `00320AB0(value, 3)` and pushes
  -2 for no record, -1 for kind 1, and the class above for kind 0.

## Layouts

```
definition id (u16)
bits 8-15  kind       0 party table 02EBF130, 1 enemy table 02EBF120, other: nothing installed
bits 0-7   index      the row; for kind 0 also the type byte at stats +0x04
```

```
struct EnemyRow table=02EBF120 (stride at table +0x08)
+0x00  u16  classRow        row of 02EBF150 (the class row at unit +0xE68)
+0x02  u8   counterSlot     spawn counter index, 0xFF for none
+0x03  u8   flags           bits 0-1 the tracked-HP class (00328FF0, flag bit 43)
+0x08  u16  nameRef         bank << 11 | entry into 02EBF170
+0x15  u8   flags2          bit 2 also sets flag bit 43
+0x16  u16  equipment0
+0x1C  u16  equipment1
+0x22  u16  rewardRow       row of 02EBF148 (unit +0xE70)
+0x24  u16  rewardLevelRow  row of 02EBF140 (unit +0xE78)
+0x32  u16  steal0          0xFFFF for none; record +0x14 bit 0
+0x34  u16  steal1          bit 1
+0x36  u16  steal2          bit 2
+0x50  u16  logicRow        row of 02EBF168 (unit +0x6E0)
```

```
struct PartyRow table=02EBF130 (stride at table +0x08)
+0x0A  u16[5] equipment     slots 0-4
+0x14  u16  gambitPreset
+0x16  u16  baseHp
+0x1A  u16  baseMp
+0x1E  u8   baseStat0        with +0x21, +0x24, +0x27: the four float stats
+0x2B  u8   scale            unit +0x68 and +0x6C (times 1.5)
+0x2C  u8   flags            bit 6 sets record +0x00 bit 2
+0x2E  u8   startLevel       0 means 1
+0x30  u16  nameRef
+0x44  u16  startLp
+0x46  u8   baseStat4        unit stat +0x20, raised to the licence rank
+0x47  u8   startMpPercent
```

```
class row (02EBF150)
+0x04  u8   type            unit +0x55
+0x05  u8   kind            unit +0x56
+0x06  u16  clanEntry       unit +0x52
+0x22  u8   facing          unit +0x64 = value * 2π / 360
+0x23  u8   scale           unit +0x68
+0x27  u8   scale2          unit +0x6C
```

## Modding notes

- An enemy's statuses and augments are not in its row: the installer writes none, and the masks
  the recompute reads come from the enemy's script ([augments](../Damage-And-Battle-Formulas/augments.md)).
- Giving a party member a starting level sets its experience to exactly that level's threshold
  and strips every status in the two masks; the MP starts at the row's percentage of capacity.
- A type between 27 and 39 earns nothing and is tested by one predicate (`type - 27 <= 12`)
  wherever the band matters; type 26 is a separate test with its own rule.

## Related

- [Battle units](battle-units.md): the pool, the bind and the handle the re-key replaces.
- [Battle unit fields](battle-unit-fields.md): the unit record the installer fills.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the stats record field by field.
- [EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md) and [stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md): the curve and the grower.
- Spawn placement and retirement: the spawn record and the lane map.
