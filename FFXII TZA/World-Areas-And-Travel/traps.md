---
title: "Traps: how walking onto a trap fires it, the trap table, the two outcomes and their odds, and re-arming by settrapresource"
kind: "system"
category: "World, areas and travel"
summary: "The traps a field carries: the trap table in the zone script and its twelve-byte records, the arming walk the settrapresource verb runs at field load with its arm chance and its world markers, the per-field live mask kept in a ring of three, who can spring a trap and who is caught in its radius, the horizontal proximity test, the hard-coded roll between the two authored actions, the action rows a trap can name and what they do, the battle message, Libra's reveal of the markers, and the census of the shipped traps."
addresses: ["002F8060", "002FB8C0", "002FB3B0", "002FA230", "002FA740", "002FAEC0", "002341C0", "002641B0", "00265770", "00355400", "002E9A60", "00263F80", "002EB7A0", "003EC630", "002EBD60", "002E3DC0", "002FB560", "003EC5B0", "003EC720", "003EC770", "00355E00", "003EC6C0", "003EB720", "002ED3A0", "003EC700", "002E7410", "002F82F0", "0030C300", "00234590", "00310DB0", "00322C50", "002EACD0", "00385F60", "003112F0", "0046A9D0", "0046AB10", "00320A30", "0032AD70", "0032AA60", "00379CD0", "003A1920", "00265020", "0031B810", "003148F0", "00377C20", "00237DF0", "00233C10", "0038CD60"]
---

# Traps: how walking onto a trap fires it, the trap table, the two outcomes and their odds, and re-arming by settrapresource

## What the player sees

Some fields hide traps. Walking onto one makes it go off: the party member who stepped on it, or
everyone near it, takes damage, loses MP, catches a status, loses gil, or is healed, and a line in
the battle log says that someone triggered a trap. A trap that has gone off stays spent while the
party remains in that area and the two most recently visited ones; it is set again when the field
is next loaded. With Libra on a party member, the traps show as markers on the ground; without it
they are invisible.

## How it works

### The trap table in the zone script

Every trap belongs to the field's zone script. The script header's word `+0x6C` points at
`{u32 count = 1; u32 packedRef}`, and `002641B0(slot, index)` resolves entry `index` of that list
for manager `slot` (section 000):

1. the reference's tag (bits 24-26) must not be 2, and a zero reference means the script has no
   table;
2. the table is `00265770(slot, tag) + (reference & 0xFFFFFF)`; for tag 3, every shipped
   reference, the base is the script image plus its header word `+0x40`
   (the storage classes);
3. the table is `{u32 count; u32 offset[count]}`, each offset relative to the table's own start,
   and each record is twelve bytes (Layouts).

### Arming the traps

The script verb `settrapresource` (`0x53B`, handler `00355400`) arms a field's traps. It pops one
operand, resolves it through `002E9A60` (a packed reference `0x1000000` or above goes through the
manager's `+0x100` table by `00263F80`; a small number is mapped by `002EB7A0`: 0 and 1 to
`0x630000`, 8 and 9 to `0x6E0001`, 12 and 13 to `0x770002`) and calls `003EC630(resource)`:

1. the previous marker resource `02B5EC94`, if any, is released (`002EBD60(prev, 0)`,
   `002E3DC0(prev)`);
2. the new resource is stored, its load flag set (`002EBD60(resource, 1)`: bit 0 of byte `+0x19`
   of the matching entry in the resource lists at `0215FD58` and `0215FD78`), and the arming walk
   `002FA740` runs (its only caller, `003EC679`).

`002FA740`:

1. clears the Libra state byte `022BE944`, takes the current field id (`003148F0`) and binds the
   table `002641B0(0, 0)` to `022BE948`; with no table it returns;
2. for each record `i` below `min(count, 32)`: the record is skipped when its flag id (`+0x04`)
   is not `0xFF` and that flag is set (`0032AA60`); otherwise it rolls `00379CD0() % 100`, and
   when the roll is below the arm chance (`+0x05`) it sets bit `i` of the mask and places marker
   `i` at `(x / 10, z / 10)` (`002FB560`);
3. it stores the mask for the field in the ring at `02EC3EA0` (below): over the field's existing
   entry when there is one, else at the write index `02EC3EC4`, which then advances modulo 3, with
   the count `02EC3EC8` capped at 3.

`002FB560(i, x, z)` places the marker: `003EC5B0(i)` (`003EB200(i, 02B5EC94, 0, 1, 0)` for `i`
below 16 outside a town), `003EC720(i, x, h, z)` with the ground height `h` that `0026E350`
resolves, and `003EC770(i, angle, hit, 0)` with the slope angle from the navmesh query
(`003355A0`, `0033CBF0`, `atanf`).

The table pointer `022BE948` is cleared by `002FAEC0`, which `002341C0` runs from the manager
unload `002695A0`.

### The ring of fired traps

The live mask of a field is one `u32`, and the engine keeps three of them: a ring of `{field,
mask}` records at `02EC3EA0`. `002FB3B0(ring, field, mask)` stores a mask: when the field is already
present the mask is replaced and 1 is returned; otherwise the record is written at the write index
`+0x24` (`02EC3EC4`), the count `+0x28` (`02EC3EC8`) is incremented and capped at 3, and the index
advances modulo 3. `002FA230` zeroes the whole ring; it runs from the battle runtime reset
`00237DF0` and from the battle-state block bind `00233C10` (`00233CC0`).

A cleared bit therefore stays cleared only while the field keeps its ring entry: a fourth field
fired in overwrites the oldest, and the next `settrapresource` in the evicted field rolls every
trap again.

### Who can spring a trap

The trigger walk is `002F8060(unit, out, count)`, called once per party member from the periodic
tick `00310DB0` (`00310FC9`). The tick reaches it only for a unit whose stats record is a party
member (kind 0) outside the Esper band 27-39, outside a town (`00377C20`), while the battle state
`022C2160` is neither 5 nor 6, when `00265680()` is non-zero, `0030B770()` and `0030B7F0(unit)` are
0 and unit flag bit 36 is clear. `002F8060` itself refuses, returning -1, when the unit's stats:

- carry bit 26 in the combined status words `+0x3C | +0x64`;
- carry bit 5 in either layer byte `+0x6C` or `+0x7C`: effect id 37, "Move safely past traps",
  the Float status's effect (the two layers,
  battle text banks);
- have kind 1, or kind 0 with the type byte `+0x04` in 27-39.

### The proximity test

For each live bit `i` of the field's mask, in index order, the walk reads record `i`, forms the
point `(x / 10, 0, z / 10)` (the divisor `10.0` at `008F8180`), takes the unit's position through
`00265020` with its height overwritten by 0 (`002F8150`), and calls `003A1920`, the plain
three-dimensional distance (`sqrtf` of the squared differences). The trap fires when that distance
is at most `1.2999999523162842`, the `f32` at `00901B34` (`002F81F4 comiss xmm7, xmm0`). Both
heights are zero, so the radius is horizontal and a unit above or below the point is as close as
one beside it.

### The roll and what fires

On a hit, in order:

1. `00379CD0()`, the Mersenne Twister draw, is reduced modulo 100; below 75 (`002F8231 cmp r8d,
   0x4B`) the action is the record's `+0x06`, otherwise its `+0x08`;
2. when the flag id `+0x04` is not `0xFF`, `0032AD70(id, 1)` sets that persistent flag
   (persistent flag banks);
3. `002FB8C0(record, unit, out)` gathers the units the trap reaches: with radius `+0x0A` = 0 only
   the triggering unit; otherwise each of the four party members (`0031B810(0..3)`) whose stats
   pass the same three refusals plus the out-of-play mask `0x80000003`, and whose position
   (height zeroed) is within the radius of the point;
4. `0046A9D0(stats, action)` posts the battle message: row 3 for action `0x103`, row 1 for
   `0x104`, row 2 for `0x105`, row 0 for anything else ([battle log](../Battle-Actions/battle-log.md));
5. `003EC700(i, 3)` retires marker `i` (`002E7410`: render record `+0x294` bit 27 set, `+0x304`
   top five bits = 3);
6. the bit is cleared in the ring (`002FB3B0`) and the walk returns the action id. At most one
   trap fires per call, and the first in index order wins when two overlap.

### What a trap does

The tick takes the returned action id and, when `00322C50(0x14, id)` accepts it, applies it to
every gathered unit (the action definition row):

1. `002EACD0(handle, 1, &handle, row word +0x24 & 0x7FFF)` plays the row's effect;
2. `00385F60(id, 0, stats, result)` and `003112F0(result, 0, stats, id)` resolve and apply the
   action on a zeroed result record.

The sixteen rows the shipped traps name are 246 to 261; their recipes are single slots
(the count clock and bank recipes):

| Rows | Slot | Effect |
|---|---|---|
| 246, 247, 248 | 106 (`0038CD60`) | HP damage `(1 + roll % power) × (1 + roll % level)`, `power` the row's `+0x10` (30, 90, 180), `level` the target's `+0x1C2`, into `02AEE004` |
| 249, 257 | 107 (`0038CE40`) | the same product into the MP loss slot `02AEE00C` (power 20, 100) |
| 260 | 108 (`0038CF20`) | the same product into the HP gain slot `02AEE008` (power 80): "healing nearby allies" |
| 261 | 109 (`0038D000`) | the same product into the MP gain slot `02AEE010` (power 50): "energizing nearby allies" |
| 259 | 163 (`0038F6F0`) | gil loss `(1 + roll % 99) × (1 + roll % level)`: "Your pockets feel lighter" |
| 250 to 256, 258 | 181 | the row's `+0x18` status mask: Sap; Confuse and Berserk; Petrify; Blind; Silence; Reverse and Disable; Disease; Oil |

### Showing the markers

`settrapshowstatus(v)` (`0x547`, handler `00355E00` → `003EC6C0`) shows or hides all sixteen
marker slots at once outside a town: `002ED3A0(003EB720(i), v)` sets bit 1 of the marker's render
record `+0x304` to `v` and bit 4 of `+0x290`. `003EB720(i)` returns slot `i` of the marker table
`02B5EA20` (`i` below 32, byte `+0x40` set) plus `0x10`.

Libra reveals the live traps. `002F82F0`, run from the world tick's per-slot pre-pass `00234590`
(`00234861`), tests `0030C300()`: any of the nine party slots (`00320AB0(i, 1)`) alive or in a
town whose status words carry bit 30, Libra. On the change from no Libra to Libra the byte
`022BE944` becomes 1 and every live trap's marker gets mode 1 (`003EC700(i, 1)`); on the change
back it becomes 0 and the markers get mode 2.

## Layouts

```
struct TrapRecord base=trapTable+offset[i] size=0x0C
+0x00  i16  x            tenths of a world unit (002F81BE, 002FA82C)
+0x02  i16  z            tenths of a world unit
+0x04  u8   flagId       persistent flag set on firing and tested at arming; 0xFF = none (002F8243, 002FA7E8)
+0x05  u8   armChance    percent; roll % 100 below it arms the trap (002FA7FC)
+0x06  u16  action75     the action row chosen below 75 (002F8237)
+0x08  u16  action25     the action row chosen at 75 and above (002F823E)
+0x0A  u8   radius       world units; 0 = the triggering unit alone (002FB8E0)
+0x0B  u8   zero         0 in every shipped record
```

```
struct TrapRing base=02EC3EA0 size=0x2C
+0x00  i32  field0       the field id of entry 0
+0x04  u32  mask0        its live mask, bit i = trap i armed
+0x0C  i32  field1
+0x10  u32  mask1
+0x18  i32  field2
+0x1C  u32  mask2
+0x24  i32  writeIndex   next entry to fill, 0 to 2 (002FB3B0, 002FA740)
+0x28  i32  count        entries in use, at most 3
```

```
fires(unit, trap) = eligible(unit) && armed(field, trap)
                    && sqrt((trap.x/10 - unit.x)^2 + (trap.z/10 - unit.z)^2) <= 1.2999999523
action = (mt19937() % 100 < 75) ? trap.action75 : trap.action25
armed at load = (trap.flagId == 0xFF || !flag(trap.flagId)) && (mt19937() % 100 < trap.armChance)
```

## Shipped data

### The tables

Over the 1,114 `us` zone and event scripts (one file is not an `EBP2` container):

| Count | Scripts |
|---|---|
| with a trap table | 389 |
| whose table is one all-zero record (never arms: chance 0) | 246 |
| with real traps | 143 |
| real traps | 489 |

Every table reference is tag 3. Tables hold 1 to 16 records; 285 hold one. All 489 real traps
have flag id `0xFF`, so no shipped trap ever sets a persistent flag and none is ever skipped at
arming: a field's traps are rolled afresh at every load, and the persistent-flag path exists only
for authored data that does not ship. The arm chance is 100 in 487 traps and 60 in the two traps
of `rbl_n02` (rows 260 and 261 twice over). Byte `+0x0B` is 0 everywhere.

| Radius | Traps | Radius | Traps |
|---|---|---|---|
| 0 | 18 | 6 | 15 |
| 2 | 1 | 7 | 78 |
| 3 | 3 | 8 | 7 |
| 4 | 10 | 10 | 195 |
| 5 | 162 | | |

### The outcomes

| Row | In the 75 slot | In the 25 slot | Both slots |
|---|---|---|---|
| 246 | 87 | 26 | 113 |
| 247 | 86 | 71 | 157 |
| 248 | 161 | 52 | 213 |
| 249 | 14 | 53 | 67 |
| 250 | 4 | 21 | 25 |
| 251 | 3 | 32 | 35 |
| 252 | 6 | 52 | 58 |
| 253 | 5 | 39 | 44 |
| 254 | 4 | 35 | 39 |
| 255 | 10 | 18 | 28 |
| 256 | 19 | 16 | 35 |
| 257 | 13 | 24 | 37 |
| 258 | 13 | 8 | 21 |
| 259 | 9 | 13 | 22 |
| 260 | 40 | 17 | 57 |
| 261 | 15 | 12 | 27 |

129 traps name the same row in both slots, so the roll changes nothing for them; 360 differ, the
commonest pairs being 246/247 (43), 248/249 (38), 248/252 (23) and 248/254 (20).

### The verbs in the scripts

| Verb | Scripts | Calls | Operands |
|---|---|---|---|
| `settrapresource` | 390 | 390 | a tag-3 reference in every call: index 1 (364), index 5 (19), index 0 (5), index 6 (2) |
| `settrapshowstatus` | 989 | 17,280 | 1 (8,907), 0 (8,373) |

## Operations

- Arming is a field-load action of the zone script: `settrapresource` runs once per script, and
  the mask it produces is per field, kept for the three most recently armed fields.
- The trigger walk runs inside the periodic tick for party members only, so enemies and guests
  never spring a trap, and a trap fires at most once per tick call.
- The two outcomes of a trap are authored; the 75/25 split and the 1.3 radius are constants in
  the code, and the arm chance and gather radius are per record.
- `002F8060` is one of two functions in the image that both draw the generator and call a
  persistent-flag setter (the other is the treasure chest resolver `002FAFD0`,
  persistent flag banks); with every
  shipped flag id `0xFF`, the trap's setter never runs in shipped play.

- The two access tables beside this page, `traps-live-entry-accesses.tsv` and
  `traps-live-set-accesses.tsv`, list every reach into the ring's entries and into the live set,
  each instruction checked against the executable.

## State

| Address | Kind | Role |
|---|---|---|
| `022BE948` | ptr | the bound trap table of manager 0 (`002FA740` sets, `002FAEC0` clears) |
| `022BE944` | u8 | the Libra marker state the pre-pass toggles |
| `02EC3EA0`-`02EC3ECB` | struct | the ring of three `{field, mask}` entries, write index and count |
| `02B5EC94` | i32 | the marker resource `settrapresource` loaded |
| `02B5EA20` | ptr[32] | the marker slots `003EB720` indexes |
| `0208D320`, `0208D324` | u32 | not used here; the status sets the heal reads |

## Modding notes

- To add a trap, add a twelve-byte record and its offset to the zone script's table (count at
  most 32) and make sure the script calls `settrapresource`; the coordinates are tenths of a unit
  and the height is ignored.
- To make a trap one-shot across saves, give it a flag id below 256 in `+0x04`: the arming walk
  then skips it once the flag is set. No shipped trap does this.
- The odds cannot be authored per trap; a trap with one outcome names the same row twice, as 129
  shipped traps do. The arm chance can, and two shipped traps use 60.
- A trap's effect is an ordinary action row (246 to 261 ship); naming another row works when
  `00322C50(0x14, id)` accepts it.

## Related

- Persistent flag banks: the flag the firing sets and the arming tests.
- The thirty-two statuses: Libra (bit 30) and the statuses the trap rows inflict.
- What the periodic tick does: the caller of the trigger walk.
- [Battle log](../Battle-Actions/battle-log.md): the four trap messages.
- The action definition row and the count clock and bank recipes: the rows and their slots.
- Section 000 of the script container: the header word `+0x6C` and the tag-3 region.
- [Area flags](area-flags-navimapdata.md): the town flag that disables arming, markers and triggering.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the tick's per-slot pre-pass that runs the Libra toggle.
