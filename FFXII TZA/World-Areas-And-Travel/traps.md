---
title: "Traps: how walking onto a trap fires it, the trap table, the two outcomes and their odds, and re-arming by settrapresource"
kind: "system"
category: "World, areas and travel"
addresses: "0x002F8060, 0x002FB8C0, 0x002FB3B0, 0x002FA230, 0x002FA740, 0x002FAEC0, 0x002341C0, 0x002641B0, 0x00265770, 0x00355400, 0x002E9A60, 0x00263F80, 0x002EB7A0, 0x003EC630, 0x002EBD60, 0x002E3DC0, 0x002FB560, 0x003EC5B0, 0x003EC720, 0x003EC770, 0x00355E00, 0x003EC6C0, 0x003EB720, 0x002ED3A0, 0x003EC700, 0x002E7410, 0x002F82F0, 0x0030C300, 0x00234590, 0x00310DB0, 0x00322C50, 0x002EACD0, 0x00385F60, 0x003112F0, 0x0046A9D0, 0x0046AB10, 0x00320A30, 0x0032AD70, 0x0032AA60, 0x00379CD0, 0x003A1920, 0x00265020, 0x0031B810, 0x003148F0, 0x00377C20, 0x00237DF0, 0x00233C10, 0x0038CD60"
---

## What the player sees

Some fields hide traps. Walking onto one makes it go off: the party member who stepped on it, or
everyone near it, takes damage, loses MP, catches a status, loses gil, or is healed, and a line in
the battle log says that someone triggered a trap. A trap that has gone off stays spent until the
field is loaded again; every load rolls each trap's arm chance afresh, whether or not it went off
before. With Libra on a party member, the traps show as markers on the ground; without it
they are invisible.

## How it works

### The trap table in the zone script

Every trap belongs to the field's zone script. The script header's word `+0x6C` points at
`{u32 count = 1; u32 packedRef}`, and `0x002641B0(slot, index)` resolves entry `index` of that list
for manager `slot` ([section 000](../EBP-Script-Files/ebp-script-image.md)):

1. the reference's tag (bits 24-26) must not be 2, and a zero reference means the script has no
   table;
2. the table is `0x00265770(slot, tag) + (reference & 0xFFFFFF)`; for tag 3, every shipped
   reference, the base is the script image plus its header word `+0x40`
   ([the storage classes](../Scripts-And-Script-Commands/script-variables.md));
3. the table is `{u32 count; u32 offset[count]}`, each offset relative to the table's own start,
   and each record is twelve bytes (Layouts).

### Arming the traps

The script verb `settrapresource` (`0x53B`, handler `0x00355400`) arms a field's traps. It pops one
operand, resolves it through `0x002E9A60` (a packed reference `0x1000000` or above goes through the
manager's `+0x100` table by `0x00263F80`; a small number is mapped by `0x002EB7A0`: 0 and 1 to
`0x630000`, 8 and 9 to `0x6E0001`, 12 and 13 to `0x770002`) and calls `0x003EC630(resource)`:

1. the previous marker resource `0x02B5EC94`, if any, is released (`0x002EBD60(prev, 0)`,
   `0x002E3DC0(prev)`);
2. the new resource is stored, its load flag set (`0x002EBD60(resource, 1)`: bit 0 of byte `+0x19`
   of the matching entry in the resource lists at `0x0215FD58` and `0x0215FD78`), and the arming walk
   `0x002FA740` runs (its only caller, `0x003EC679`).

`0x002FA740`:

1. clears the Libra state byte `0x022BE944`, takes the current field id (`0x003148F0`) and binds the
   table `0x002641B0(0, 0)` to `0x022BE948`; with no table it returns;
2. for each record `i` below `min(count, 32)`: the record is skipped when its flag id (`+0x04`)
   is not `0xFF` and that flag is set (`0x0032AA60`); otherwise it rolls `0x00379CD0() % 100`, and
   when the roll is below the arm chance (`+0x05`) it sets bit `i` of the mask and places marker
   `i` at `(x / 10, z / 10)` (`0x002FB560`);
3. it stores the mask for the field in the ring at `0x02EC3EA0` (below): over the field's existing
   entry when there is one, else at the write index `0x02EC3EC4`, which then advances modulo 3, with
   the count `0x02EC3EC8` capped at 3.

`0x002FB560(i, x, z)` places the marker: `0x003EC5B0(i)` (`0x003EB200(i, 0x02B5EC94, 0, 1, 0)` for `i`
below 16 outside a town), `0x003EC720(i, x, h, z)` with the ground height `h` that `0x0026E350`
resolves, and `0x003EC770(i, angle, hit, 0)` with the slope angle from the navmesh query
(`0x003355A0`, `0x0033CBF0`, `atanf`).

The table pointer `0x022BE948` is cleared by `0x002FAEC0`, which `0x002341C0` runs from the manager
unload `0x002695A0`.

### The ring of fired traps

The live mask of a field is one `u32`, and the engine keeps three of them: a ring of `{field,
mask}` records at `0x02EC3EA0`. `0x002FB3B0(ring, field, mask)` stores a mask: when the field is already
present the mask is replaced and 1 is returned; otherwise the record is written at the write index
`+0x24` (`0x02EC3EC4`), the count `+0x28` (`0x02EC3EC8`) is incremented and capped at 3, and the index
advances modulo 3. `0x002FA230` zeroes the whole ring; it runs from the battle runtime reset
`0x00237DF0` and from the battle-state block bind `0x00233C10` (`0x00233CC0`).

A cleared bit therefore stays cleared only until the next `settrapresource` for the field, which
rolls every trap again and replaces the field's ring entry without reading the old mask
(`0x002FA740`); the ring keeps the three most recent fields' masks, but nothing restores a spent trap
from it.

### Who can spring a trap

The trigger walk is `0x002F8060(unit, out, count)`, called once per party member from the periodic
tick `0x00310DB0` (`0x00310FC9`). The tick reaches it only for a unit whose stats record is a party
member (kind 0) outside the Esper band 27-39, outside a town (`0x00377C20`), while the battle state
`0x022C2160` is neither 5 nor 6, when `0x00265680()` is non-zero, `0x0030B770()` and `0x0030B7F0(unit)` are
0 and unit flag bit 36 is clear. `0x002F8060` itself refuses, returning -1, when the unit's stats:

- carry bit 26 in the combined status words `+0x3C | +0x64`;
- carry bit 5 in either layer byte `+0x6C` or `+0x7C`: augment 37 (Tread Lightly, "Move safely past traps"),
  the Float status's effect ([the two layers](../Status-Effects-And-KO/statuses.md),
  [battle text banks](../Game-Files-And-Data-Tables/battle-text-tables.md));
- have kind 1, or kind 0 with the type byte `+0x04` in 27-39.

### The proximity test

For each live bit `i` of the field's mask, in index order, the walk reads record `i`, forms the
point `(x / 10, 0, z / 10)` (the divisor `10.0` at `0x008F8180`), takes the unit's position through
`0x00265020` with its height overwritten by 0 (`0x002F8150`), and calls `0x003A1920`, the plain
three-dimensional distance (`sqrtf` of the squared differences). The trap fires when that distance
is at most `1.2999999523162842`, the `f32` at `0x00901B34` (`0x002F81F4 comiss xmm7, xmm0`). Both
heights are zero, so the radius is horizontal and a unit above or below the point is as close as
one beside it.

### The roll and what fires

On a hit, in order:

1. `0x00379CD0()`, the Mersenne Twister draw, is reduced modulo 100; below 75 (`0x002F8231 cmp r8d,
   0x4B`) the action is the record's `+0x06`, otherwise its `+0x08`;
2. when the flag id `+0x04` is not `0xFF`, `0x0032AD70(id, 1)` sets that persistent flag
   ([persistent flag banks](../Story-Events-And-Hunts/story-flags.md));
3. `0x002FB8C0(record, unit, out)` gathers the units the trap reaches: with radius `+0x0A` = 0 only
   the triggering unit; otherwise each of the four party members (`0x0031B810(0..3)`) whose stats
   pass the same three refusals plus the out-of-play mask `0x80000003`, and whose position
   (height zeroed) is within the radius of the point;
4. `0x0046A9D0(stats, action)` posts the battle message: row 3 for action `0x103`, row 1 for
   `0x104`, row 2 for `0x105`, row 0 for anything else ([battle log](../Battle-Actions/battle-log.md));
5. `0x003EC700(i, 3)` retires marker `i` (`0x002E7410`: render record `+0x294` bit 27 set, `+0x304`
   top five bits = 3);
6. the bit is cleared in the ring (`0x002FB3B0`) and the walk returns the action id. At most one
   trap fires per call, and the first in index order wins when two overlap.

### What a trap does

The tick takes the returned action id and, when `0x00322C50(0x14, id)` accepts it, applies it to
every gathered unit ([the action definition row](../Battle-Actions/action-definition-row.md)):

1. `0x002EACD0(handle, 1, &handle, row word +0x24 & 0x7FFF)` plays the row's effect;
2. `0x00385F60(id, 0, stats, result)` and `0x003112F0(result, 0, stats, id)` resolve and apply the
   action on a zeroed result record.

The sixteen rows the shipped traps name are 246 to 261; their recipes are single slots
([the count clock and bank recipes](../Damage-And-Battle-Formulas/weapon-formulas.md)):

| Rows | Slot | Effect |
|---|---|---|
| 246, 247, 248 | 106 (`0x0038CD60`) | HP damage `(1 + roll % power) × (1 + roll % level)`, `power` the row's `+0x10` (30, 90, 180), `level` the target's `+0x1C2`, into `0x02AEE004` |
| 249, 257 | 107 (`0x0038CE40`) | the same product into the MP loss slot `0x02AEE00C` (power 20, 100) |
| 260 | 108 (`0x0038CF20`) | the same product into the HP gain slot `0x02AEE008` (power 80): "healing nearby allies" |
| 261 | 109 (`0x0038D000`) | the same product into the MP gain slot `0x02AEE010` (power 50): "energizing nearby allies" |
| 259 | 163 (`0x0038F6F0`) | gil loss `(1 + roll % 99) × (1 + roll % level)`: "Your pockets feel lighter" |
| 250 to 256, 258 | 181 | the row's `+0x18` status mask: Sap; Confuse and Berserk; Petrify; Blind; Silence; Reverse and Disable; Disease; Oil |

### Marking the trap's effect

Between steps 1 and 2 above, the tick hands the effect handle `0x002EACD0` returned to `0x0024ED50`
(`0x00311070`-`0x00311072`). `0x0024ED50` routes it by the handle's top four bits and sets bit 11 (`0x800`)
of the effect record's `u16` at `+0x36A`:

| Top four bits | Body | Record lookup |
|---:|---|---|
| 1 | `0x002FCFB0` | slot = the handle's low six bits, below 48; the slot's dword at `0x02EC32E0` + slot·`0x38` must equal the handle, and its pointer at `+0x10` must be set (`0x002FCFE1`) |
| 5, 6, 9 | `0x003B0F30` | the 36 entries of 24 bytes at `0x02EBEC00`, walked until the first dword equals the handle; a zero first dword ends the walk; the entry's pointer `+0x08` must be set (`0x003B0F76`) |
| any other | none | returns (`0x0024ED76`) |

The only other caller, `0x00319E40`, does the same for the handle `0x0030CA50()` returns, after passing it
with the ids of the units in the list at `+0x780` (count `+0x77C`) to `0x002EAD00`, when `0x00237420()` is
non-zero (`0x00319F10`).

### Showing the markers

`settrapshowstatus(v)` (`0x547`, handler `0x00355E00` → `0x003EC6C0`) shows or hides all sixteen
marker slots at once outside a town: `0x002ED3A0(0x003EB720(i), v)` sets bit 1 of the marker's render
record `+0x304` to `v` and bit 4 of `+0x290`. `0x003EB720(i)` returns slot `i` of the marker table
`0x02B5EA20` (`i` below 32, byte `+0x40` set) plus `0x10`.

Libra reveals the live traps. `0x002F82F0`, run from the world tick's per-slot pre-pass `0x00234590`
(`0x00234861`), tests `0x0030C300()`: any of the nine party slots (`0x00320AB0(i, 1)`) alive or in a
town whose status words carry bit 30, Libra. On the change from no Libra to Libra the byte
`0x022BE944` becomes 1 and every live trap's marker gets mode 1 (`0x003EC700(i, 1)`); on the change
back it becomes 0 and the markers get mode 2.

## Layouts

Struct TrapRecord base=trapTable+offset[i] size=`0x0C`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | x | tenths of a world unit (`0x002F81BE`, `0x002FA82C`) |
| `+0x02` | `i16` | z | tenths of a world unit |
| `+0x04` | `u8` | flagId | persistent flag set on firing and tested at arming; `0xFF` = none (`0x002F8243`, `0x002FA7E8`) |
| `+0x05` | `u8` | armChance | percent; roll % 100 below it arms the trap (`0x002FA7FC`) |
| `+0x06` | `u16` | action75 | the action row chosen below 75 (`0x002F8237`) |
| `+0x08` | `u16` | action25 | the action row chosen at 75 and above (`0x002F823E`) |
| `+0x0A` | `u8` | radius | world units; 0 = the triggering unit alone (`0x002FB8E0`) |
| `+0x0B` | `u8` | zero | 0 in every shipped record |

Struct TrapRing base=`0x02EC3EA0` size=`0x2C`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | field0 | the field id of entry 0 |
| `+0x04` | `u32` | mask0 | its live mask, bit i = trap i armed |
| `+0x0C` | `i32` | field1 |  |
| `+0x10` | `u32` | mask1 |  |
| `+0x18` | `i32` | field2 |  |
| `+0x1C` | `u32` | mask2 |  |
| `+0x24` | `i32` | writeIndex | next entry to fill, 0 to 2 (`0x002FB3B0`, `0x002FA740`) |
| `+0x28` | `i32` | count | entries in use, at most 3 |

```python
fires(unit, trap) = eligible(unit) && armed(field, trap) && sqrt((trap.x/10 - unit.x)^2 + (trap.z/10 - unit.z)^2) <= 1.2999999523
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
- `0x002F8060` is one of two functions in the image that both draw the generator and call a
  persistent-flag setter (the other is the treasure chest resolver `0x002FAFD0`,
  [persistent flag banks](../Story-Events-And-Hunts/story-flags.md)); with every
  shipped flag id `0xFF`, the trap's setter never runs in shipped play.

- The two access tables beside this page, `traps-live-entry-accesses.tsv` and
  `traps-live-set-accesses.tsv`, list every reach into the ring's entries and into the live set,
  each instruction checked against the executable.

## State

| Address | Kind | Role |
|---|---|---|
| `0x022BE948` | ptr | the bound trap table of manager 0 (`0x002FA740` sets, `0x002FAEC0` clears) |
| `0x022BE944` | u8 | the Libra marker state the pre-pass toggles |
| `0x02EC3EA0`-`0x02EC3ECB` | struct | the ring of three `{field, mask}` entries, write index and count |
| `0x02B5EC94` | i32 | the marker resource `settrapresource` loaded |
| `0x02B5EA20` | ptr[32] | the marker slots `0x003EB720` indexes |
| `0x0208D320`, `0x0208D324` | u32 | not used here; the status sets the heal reads |

## Modding notes

- To add a trap, add a twelve-byte record and its offset to the zone script's table (count at
  most 32) and make sure the script calls `settrapresource`; the coordinates are tenths of a unit
  and the height is ignored.
- To make a trap one-shot across saves, give it a flag id below 256 in `+0x04`: the arming walk
  then skips it once the flag is set. No shipped trap does this.
- The odds cannot be authored per trap; a trap with one outcome names the same row twice, as 129
  shipped traps do. The arm chance can, and two shipped traps use 60.
- A trap's effect is an ordinary action row (246 to 261 ship); naming another row works when
  `0x00322C50(0x14, id)` accepts it.

## Related

- [Persistent flag banks](../Story-Events-And-Hunts/story-flags.md): the flag the firing sets and the arming tests.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md): Libra (bit 30) and the statuses the trap rows inflict.
- [What the periodic tick does](../Status-Effects-And-KO/status-timers.md): the caller of the trigger walk.
- [Battle log](../Battle-Actions/battle-log.md): the four trap messages.
- [The action definition row](../Battle-Actions/action-definition-row.md) and [the count clock and bank recipes](../Damage-And-Battle-Formulas/weapon-formulas.md): the rows and their slots.
- [Section 000 of the script container](../EBP-Script-Files/ebp-script-image.md): the header word `+0x6C` and the tag-3 region.
- [Area flags](area-flags-navimapdata.md): the town flag that disables arming, markers and triggering.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the tick's per-slot pre-pass that runs the Libra toggle.
