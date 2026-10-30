---
title: "Enemy spawning: the spawn table, how a zone picks where a monster appears, the ground height, and when it vanishes out of range"
kind: "system"
category: "Enemy spawning"
addresses: "0x0023A2E0, 0x002395A0, 0x00236100, 0x002360D0, 0x0023A520, 0x0023A1D0, 0x0023A1F0, 0x00239020, 0x00235340, 0x00235330, 0x00235720, 0x00308D90, 0x00234AF0, 0x00234DA0, 0x002374E0, 0x00319390, 0x00328370, 0x002354F0, 0x00235360, 0x002355A0, 0x00236450, 0x00239840, 0x0023A3B0, 0x0023A570, 0x00233AD0, 0x00239E10, 0x0023A410, 0x003208C0, 0x00300310, 0x00239410, 0x00239210, 0x002391C0, 0x002396B0, 0x0023A200, 0x00236860, 0x00238FC0, 0x002350C0, 0x00300E40, 0x00306E60, 0x00233F70, 0x002342F0, 0x002368D0, 0x0031B810, 0x003273B0, 0x003272A0, 0x00320940, 0x003209C0, 0x003A1960, 0x005102D0"
---

## What the player sees

Monsters appear around you, not on top of you, and usually ahead of you. A zone script asks the
engine for a spot: a random distance in a band around the party leader, at a random angle inside
an arc centred on the way the leader faces. The default band is 39 to 42 units and the arc a
forward half-circle, but almost every zone that cares replaces the band with something much
tighter, 5 to 12 units being the commonest, so monsters in those zones appear close.

The first monsters you meet on entering a zone can stand anywhere, including right next to you:
the minimum distance is switched off for a monster that has never been alive on this visit. Once
it has lived once, or the zone script says so, every later placement is pushed out to the minimum.

Walk far enough from a monster and it vanishes. The default range is 43 units, just outside the
band it appeared in, and the distance is measured flat on the ground to the character you are
steering, so a monster on a cliff above you counts as next to you. Some monsters instead vanish
when the leader comes near an authored point. A monster that vanished this way comes straight back
when you return, with no cooldown, because vanishing is not dying.

Monsters stand on the ground because, at the moment one is placed, the engine asks the terrain for
the floor under its spot and drops it there, plus a small lift authored per monster. Only monsters
whose definition asks for the probe get it.

## How it works

### The lane map and the spawn table

Every spawning actor's battle unit holds a lane map at `+0x40`: a count byte, then one slot byte per
lane naming a record in the live keep bank, `0xFF` for none. `0x00236100(map, lane)` returns
`[0x0208E690] + slot * 0x250` and `0x002360D0(map, lane)` the slot; both refuse a null map, a negative
lane, a lane at or past the count and the `0xFF` slot. The record is [the spawn
record](spawn-record-fields.md); its back-pointer is unit `+0x6A0`.

Verb `0x3016` `btlAtelSetTotalEntryNumber` (`0x00510620`) resolves its scope-3 operand to a pointer
into the script's data area and jumps to `0x0023A2E0(actor, map)`, which stores the map at unit
`+0x40` and, for every mapped record with flags `& 5 == 0` (neither retired nor released), writes
`+0x16` = `0xFF`, clears flag bits `0x1`, `0x4` and `0x80`, zeroes `+0x78`-`+0x7C` and restores the persistence
key `+0x17` from `+0x18`.

Verb `0x3018` `btlAtelSetEntryStruct` (`0x005106D0`) resolves its operand the same way and jumps to
`0x002395A0(table)`, which rolls each uncommitted record's death limit and cooldown from the table's
rows and writes its persistence key ([enemy respawning](enemy-respawning.md)).

### The tunables and their script defaults

Seven globals steer placement. All are BSS, zero at load, and installed at run time:

| Global | Meaning | Installed by | Read by |
|---|---|---|---|
| `0x02089358` | heading arc, degrees (i32) | `0x0023A520`: 180; `0x0023A1F0` (verb `0x305B`, float truncated) | `0x00234AF0` |
| `0x02089360` | minimum spawn distance (f32) | `0x0023A520`: 39.0; `0x0023A1D0` | `0x00235720` |
| `0x02089364` | maximum spawn distance (f32) | `0x0023A520`: 42.0; `0x0023A1D0` | `0x00235720` |
| `0x02089368` | retire range (f32) | `0x0023A520`: 43.0; `0x0023A1D0` | `0x002350C0` |
| `0x0208D457` | placement attempts (u8, read signed) | `0x0023A520`: 1; `0x00239020` (verb `0x3038`, clamped below 1) | `0x00235720` |
| `0x0208D458` | active cap (u8, read signed) | `0x002342F0`: 28 at every area entry; verb `0x304E` (`0x00510320`) | `0x00235720` |
| `0x0208936C` | return window, seconds (i32) | `0x002368D0`: 300; `0x00235340` (verb `0x306C`, negative restores 300) | `0x00233780` |

`0x0023A520` is nine instructions (`0x0023A520`-`0x0023A561`): the three floats from `0x009146EC`,
`0x009146F0` and `0x009146F4`, the arc and the attempt byte. Its only entry is the jump at `0x00510710`,
the handler of verb `0x3053` `btlAtelSetupActorStart`. Verb `0x300B` `btlAtelSetSpawnDistance`
(`0x0050F410`) pops three floats and tail-jumps `0x0023A1D0(retire, max, min)`, which stores them at
`0x02089368`, `0x02089364` and `0x02089360`, so in a script the arguments read `(min, max, retire)`.

`0x00308D90` counts, over the `0x00236850()` battle-unit slots through `0x00236820`, the units whose flag
word has bit `0x200000`, the bit the bind sets; verb `0x3050` returns
it and `0x304F` the cap byte.

A zone that never runs the reset has every float at 0: the candidate generator refuses an empty
band on its first test, and the mode-1 retire fires for every monster on its first frame. The
shipped scripts never get there (Shipped data).

### Automatic placement

Verb `0x301A` `btlAtelDecideEntryPointAuto` (`0x0050F520`) calls `0x00235720(actor)` and pushes its
result: the winning lane, or -1. The selector:

1. returns -1 when `0x00308D90()` is at or above the signed cap byte `0x0208D458` (`0x00235753`-`0x00235763`),
   or the unit, its candidate table `[unit + 0x38]` or its lane map is null;
2. computes `seconds = counter / (int)(30.0 * [0x01DFE0B8])` from `0x0032A150` (`0x002357D9`-`0x002357F9`);
3. walks lanes 1 to `table[0] - 1`, the candidate table's count word (lane 0 is never offered; a
   lane past the lane map's own count is skipped). A lane is skipped when its record has
   died out (`+0x0A` non-zero and `+0x08 >= +0x0A`), or is committed and not retired (flag bit `0x2` set,
   bit `0x1` clear) with a non-zero cooldown `+0x10` and `seconds - +0x0C < +0x10` unsigned;
4. sets the minimum distance to `0x02089360` when the unit's flag word has bit `0x200000000000` or bit `0x2000000000000`
   (`test qword ptr [rsi], r10` with `0x0002200000000000`, `0x002358EB`), else 0.0;
5. for each candidate id of the lane (the table's words from `table[1 + lane]` to
   `table[2 + lane] - 1`, a short; `0x00FF` is the sentinel, `0x00235919`-`0x00235925`, and a -1 is passed
   on and fails the record fetch), tries `0x00234AF0(id, &pos, minR, 0x02089364, &observed, 0)` for
   attempts `0` to `n - 1`, `n` = `0x0208D457` read signed;
6. an attempt is accepted when the call returns non-zero and `observed` is below `0x02F973B8` (the
   shared maximum squared distance, `+INF` from `0x002368D0`);
7. a hit records the lane and the position, and both loops run on, so the last accepted candidate
   of the highest accepting lane wins;
8. on a win it stores the position at the record's `+0x50` and `+0x60` as whole 16-byte moves
   (`0x00235A08`, `0x00235A0F`), sets unit flag bit `0x4000000` and returns the lane.

Bit `0x2000000000000` is set once per unit by the activation `0x00233AD0` (`0x00233B8C`) and never cleared, not even by
the unit reset `0x00236A60` (mask `0xFFFF7FFDFFE7FFFD`, [battle units](../Characters-And-Objects/battle-units.md));
bit `0x200000000000` is set by verb `0x304D` `btlAtelCanselInitialSpawnFlag` (`0x005102D0`), which the zone scripts
call on the fresh-placement branch. So the minimum applies to a monster that has lived once or
that the script declared not an arrival placement.

### Generating a candidate

`0x00234AF0(id, out, minR, maxR, outObserved, allSlots)` refuses when `maxR - minR == 0.0`, then
fetches format-class-0 record `id` of the field data through `0x003209C0` (0 on success, -1 on
failure; `0x003DFD00(0, id, rec)`) and copies the record's point at `+0x10` into `out` before any
further test, so a 0 return can leave that point in the caller's buffer (the selector ignores it).

It needs the
party leader (`0x003272A0`: the focus handle's unit, with `0x02089340` bit `0x10` set and the unit's flag
bit `0x8`), takes the leader's position (`0x00265020`) and heading (`0x00265200`), and branches on the
record's first byte:

- byte 0: point mode. The authored point stands. `0x0031AC90` gives the heading from the leader to
  the point (`atan2(dx, dz)`, or the leader's heading when the two coincide), `0x0031A930` the
  absolute wrapped difference, and the point passes the arc when that is at most
  `(arcDeg / 2) * 2pi / 360` with an integer halving (`0x00234BF8`-`0x00234C2B`); then
  `0x00234DA0(out, minR^2, maxR^2, outObserved, allSlots)` decides;
- any other byte: area mode. Two draws of `0x00328370`: `r = (draw % (int)((maxR - minR) * 100)) / 100
  + minR`, quantised to a hundredth, and `theta = wrap(heading + ((draw % arcDeg) - arcDeg / 2) *
  2pi / 360)` (`0x00316DA0`);
- `0x00319390` then builds `leader + (r * sin(theta), ?, r * cos(theta))` through the 32,768-entry
  sine table at `0x01F004E0` (`cos = sin[(0x2000 - i) & 0x7FFF]`), writing x and z only. The point
  is accepted when `0x002374E0` places it inside the record's region; no distance test runs.

`0x002374E0(point, rec)` transforms the point into the record's frame (`0x00325EA0`, centre `+0x10`,
heading `+0x1C`) and accepts a type-1 record when `|x| <= w/2` and `|z| <= d/2` (`w` at `+4`, `d` at
`+8`), a type-2 record when `x^2/(w/2)^2 + z^2/(d/2)^2 <= 1`, and nothing else. Each `0x00328370` call
steps the shared generator three times, so an area placement advances it six steps; point mode
draws nothing. Neither divisor is tested: a band under a hundredth wide, or an arc of 0, divides
by zero.

The y written in area mode is whatever the stack slot at `rsp + 0x54` held: `0x00319390` never
writes `[rdx + 4]` and `0x00234AF0` copies the slot into `out.y` (`0x00234CDD`, `0x00234CF2`). It rides
along to the record and is replaced at activation (the height section).

### The distance test

`0x00234DA0(cand, minD2, maxD2, outObserved, allSlots)` walks party slots 0-3 through `0x0031B810`
(the unit of the party-record byte at `[0x02EBF190] + 0x5A5A + 2 * i`, when `0x00322C50(0x17, i)` allows
the slot). A slot counts when it has a stats record whose status words `+0x64 | +0x3C` have none of
`0x80000003`, or the field waives that (`0x00377C20`), and, with `allSlots` = 0, when its handle
`+0x08` is the party focus (`0x003273B0` against `0x003590D0()`).

For each counted slot it measures the squared planar distance `(dx^2 + dz^2)` (`0x003A1960`) and returns 0 at once when a bound is given
and violated (`d2 < min` or `d2 > max`); it publishes `d2` to `outObserved` for the focus slot and
returns 1 only when at least one slot was counted. No counted slot is a rejection.

The spawn path passes `allSlots` = 0, so exactly one character is measured: the one the player is
steering. `0x00308040` is the other caller, with `allSlots` = 1 and a minimum only.

### Bringing a banked monster back

Two selectors look for a record the keep banks preserved. Both set unit flag bit `0x4000000` on success:

- verb `0x304B` `btlAtelDecideEntryGroupByPreviousMap` (`0x00510230`) calls `0x002354F0`, which walks
  the lane map from lane 0 and returns the first lane whose record has flag bit `0x4` (released), or -1;
- verb `0x305F` `btlAtelDecideEntryGroupByContinuous` (`0x00510260`) calls `0x00235360`, which, for each
  mapped record with a non-zero key `+0x17`, scans the 64 history-bank records for one with flag bit
  `0x2` set, bit `0x1` or `0x4` set and the same key, and copies that whole `0x250`-byte record over the live
  one (`0x00235460`-`0x002354DD`), returning the lane; -1 when the history bank is null or nothing
  matches.

Verb `0x303C` `btlAtelSetEntryPositionForce` (`0x0050FCB0`) pops two floats and jumps to
`0x00239410(actor, z, x)`, which writes `{x, 0, z, -}` to the unit's own record (lane `+0x57`) at
`+0x50` and `+0x60` and sets bit `0x4000000`; it returns -1 on a bad lane.

### Binding and the unit's own candidate

Verb `0x305C` `btlAtelSetKeepWorkGroup(selection, lane)` (`0x005103F0`; the first pop is the last
script argument) jumps to `0x00239840(actor, lane, selection)`. With a negative lane it uses the
selection as the lane. It writes the lane to unit `+0x57`, the selection
(or -1 for a negative lane) to the record's `+0x16`, clears flag bits `0x1` and `0x4` when the selection
changed (`0x002398C2`), restores `+0x17` from `+0x18` on a fresh record and sets unit flag bit `0x200000`, the
bit the active cap counts.

Verb `btlAtelSetUnit(id)` (`0x00510160`, one pop) applies a definition: `0x0023A3B0(actor, id)` first
runs `0x002355A0`, then `0x0023A570(unit, id | 0x100)`, or `0xFFFF` for an id of `0xFF` ([battle unit
construction](../Characters-And-Objects/battle-unit-construction.md)); when `0x00237650(actor)` is then
non-zero the handler runs `0x0037CF50(context, actor, -1)`.

`0x002355A0` returns 1 at once when bit `0x4000000`
is already set, and 0 when the unit's lane `+0x57` is not below the candidate table's count word,
when the lane's range is empty, or when the drawn id is negative; otherwise it draws one candidate
id of that lane with `0x00328370` and generates a position with `0x00236450(id, &pos)`:

- record type 0: the authored point;
- type 1: a random offset inside the box, `x = (draw % (int)(w/2 * 100)) / 100`, the same for z,
  each negated when a further draw has bit `0x10` set;
- type 2: a random x the same way, then `z` drawn up to `sqrt((d/2)^2 - x^2 (d/2)^2 / (w/2)^2)`,
  each sign drawn;

the offset is rotated into the record's frame by `0x00319390` with the record's heading. On success
the position is stored at `+0x50` and `+0x60` and bit `0x4000000` set.

### Activation and the height

`0x00233AD0(actor)` runs the applied definition: for an active unit (flag bit `0x4`) it posts `0x2001`
outside a town, refreshes the actor (`0x00238BF0`), and returns early only when the definition is
already applied (bit `0x8`, `0x00233B3A`) and `0x0037C8C0(actor)` is 0.

Otherwise it runs `0x00324450(unit)`,
sets bit `0x8`, runs `0x00239E10`, sets bit `0x2000000000000`, sets the record's flag bit `0x2` for a kind-1 unit
(`0x00233BA8`), and publishes the position (`0x00311F70(0, unit, 1)`) when bit `0x4000000` is clear, the status
gate passes and `0x003278C0()` is 0. For an inactive unit it clears bit `0x4000000`.

`0x00239E10` loads twelve unit parameters through `0x003204D0` (`0x00239E78`-`0x00239F5B`), ten of them into fields
between `+0x164` and `+0x1B0` and numbers 24 and 26 into locals the later writes use, with alternate parameter numbers for a kind-1 unit whose definition byte `+0x13` is not `0xFF`; it also sets
`+0x1F0` bit `0x4`, `+0x1F5`, `+0x17C`, `+0x150`, `+0x19C` and `+0x1F4`, pushes `+0x184` into the render record
(`0x002E86B0`), and ends with the battle-unit refresh `0x00236300`.

Among those writes is the placement-height
byte `+0x1F6`: 1 for a kind-0 stats record; for any other
kind, or no stats record, from the definition record's byte `+0x18` (`[unit + 0xE68]`): 8 when bit
`0x10` is set, else 2 when bit `0x20` is set, else 1, with 4 added when bit `0x40` is set. For a kind-1 unit with
the probe bit it also stores `0x00236210(unit)` at `+0x188`, the vertical lift; otherwise `+0x188` = 0.

Verb `0x304C` `btlAtelSetUnitFinish` (`0x00510250`, a jump) runs `0x0023A410(actor)` on the unit's own
record:

1. for a fresh record (flags `& 5 == 0`) whose definition row's dword `+0x18` is non-zero,
   `0x00300520(stats, row.dw_18, 0, 0x297)`: an authored starting HP;
2. flag bits `0x4` and `0x1` cleared;
3. `0x002FED60` or `0x002FEDC0(unit, 1)` by `0x00308010(unit, 1)`, then `0x00238BF0(unit)`;
4. when `+0x1F6` has bit `0x8`, `0x003208C0(x, z, &y)` probes the ground under the record's `+0x60`/`+0x68`:
   it asks `0x0026E3C0([0x02EC1370], {x, 1.0, z, 1.0})` and writes the surface height, or 0.0 when the
   query returns -1; the return value is ignored, and `+0x188` is added (`0x0023A4D5`);
5. `0x00300310(unit, record + 0x60, 0, 1)` places the unit at the record's candidate position, then
   `0x0030FED0(stats, 0x297)` and `0x00386C10(stats)`.

A spot with no collision under it therefore gives a monster at world height 0 plus its lift, and
no error.

### Facing, inhibit, category and the lifecycle float

- `0x00239210(actor, degrees)` (verb handler `0x0051077C`): a negative argument draws `0x00328370() % 360`;
  the angle in radians is wrapped (`0x00316DA0`) and stored at the record's `+0x70`, then applied to
  the actor (`0x0026A0D0`, `0x0026B620`).
- verb `0x3015` `btlAtelSetCallGroup(tag)` (`0x00510370`) → `0x002391C0`: on a record not released, clears
  flag bit `0x10` and `+0x15`, then sets both to the tag when it is non-zero.
- verb `0x3005` `btlAtelSetUnitType(n)` (`0x00510340`) → `0x002396B0`: unit `+0x58` from the table
  `{1, 5, 3, 4}` at `0x01E09EE8` for `n` below 4, else 0; on a fresh record clears flag bit `0x20` and sets
  it when the byte became 4.
- verb `0x3017` `btlAtelSetSpecialSpawnRange(f)` (`0x005107C0`) → `0x0023A200`: unit flag bit `0x10000000000` set
  for a non-zero `f`, cleared for 0; on a fresh record `+0x04` and bits `0x8` and `0x40` cleared, then `+0x04`
  = `f` with bit `0x8` for `f > 0`, or `-f` with bit `0x40` for `f < -1.0`.
- verb `0x305E` `btlAtelIgnoreKeepWork(lane, ignored)` (`0x005104D0`) → `0x00236860(actor, _, lane)`:
  clears bits `0x1`, `0x4` and `0x80`,
  sets the word `+0x16` to `0x00FF` and zeroes `+0x78`-`+0x7C` of the lane's record.

### The despawn mode

Verb `0x3019` `btlAtelSetDeSpawnType(mode, threshold, anchor)` (`0x0050F4A0`, three pops, the first
pop being the last script argument) calls `0x00238FC0(actor, anchor, threshold, mode)`, which stores
the mode at unit `+0x50` always and, for mode 2, the threshold `+0x4C` = `threshold / 10.0` (6.0
when 0) and the anchor `+0x51`. The shipped scripts call it with `(1, 0, 0)` 4,937 times and
`(0, 0, 0)` 1,809 times; no shipped script authors mode 2.

### Range retirement

The per-unit frame `0x00233F70` (the record's `+0x38` callback, [field
runtime](../Characters-And-Objects/field-runtime.md)) calls `0x002350C0(actor)` at `0x00234022` for a bound unit
with flag bits `0x8` and `0x10` whose status gate passes. `0x002350C0` returns 0 unless the record's `+0x0D`
bit `0x40` is set (`0x002672F0`, the drive loop's "scheduled this pass" bit), the unit exists with a non-zero
mode `+0x50`, its stats record has a non-zero kind byte, unit flag bit `0x10` is set, the status words pass
the `0x80000003` gate or the field waives it, and the record's flag bit `0x10` is clear. Then:

- mode 1: for party slots 0-3, a slot counts when it has flag bit `0x10`, a stats record passing the gate,
  and is the party focus. The unit is kept when any counted slot's squared planar distance is below
  `0x02089368^2` (`0x0023527D`, `comiss`/`ja`); it retires when at least one slot counted and none was
  nearer. At exactly the range it retires;
- mode 2: needs the leader and the anchor point `0x00320940(+0x51)`; retires when the leader's
  navigation position (unit `+0xE0`) is within `(+0x4C)^2` of it (`comiss`/`jbe`);
- any other mode: 0.

Retiring sets the record's flag bit `0x1` (`0x002352A6`), tears the unit down with `0x00300E40(unit, 1)`,
the one call that keeps the record's transient state, and unregisters the member from its group
with `0x00306E60(unit, 0)`. A NaN distance retires in both modes; a party with no counted focus slot
never retires a mode-1 unit.

## Layouts

Globals (BSS):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02089358` | `i32` | heading arc degrees |  |
| `0x02089360` | `f32` | min distance |  |
| `0x02089364` | `f32` | max distance |  |
| `0x02089368` | `f32` | retire range |  |
| `0x0208D457` | `u8` | attempts (signed use) |  |
| `0x0208D458` | `u8` | active cap (signed use) |  |
| `0x0208936C` | `i32` | return window, seconds |  |
| `0x02F973B8` | `f32` | max considered squared distance, +INF (0x002368F0); shared with AI targeting and loot |  |

Initialised .data:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01F004E0` | `f32[32768]` | sine table, table[i] = sin(2 pi i / 32768); entry 0x2000 at 0x01F084E0 = 1.0 |  |

.rdata:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x009146EC` | `f32` | 39.0, the script default |  |
| `0x009146F0` | `f32` | 42.0, the script default |  |
| `0x009146F4` | `f32` | 43.0, the script default |  |

BattleUnit fields this page uses:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u64` | flags: bit 0x4 active, 3 definition applied, 4 drive, 21 cap-tracked, 26 candidate prepared, | 40 special range, 45 not an initial placement, 49 activated once |
| `+0x038` | `void*` | candidate table: u16 count, then u16 offsets per lane, then i16 candidate ids |  |
| `+0x040` | `void*` | lane map: u8 count, u8 slot per lane (0xFF none) |  |
| `+0x04C` | `f32` | mode-2 threshold |  |
| `+0x050` | `u8` | despawn mode 0/1/2 |  |
| `+0x051` | `u8` | anchor record |  |
| `+0x057` | `i8` | the unit's own lane |  |
| `+0x058` | `u8` | category byte |  |
| `+0x188` | `f32` | vertical lift |  |
| `+0x1F6` | `u8` | height mode: bit 0x8 = probe |  |
| `+0x698` | `void*` | stats record (+0x05 kind) |  |
| `+0x6A0` | `void*` | spawn record |  |
| `+0xE68` | `void*` | definition record |  |

Field format-class-0 record (`0x003DFD00`(0, id, rec)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | type: 0 point, 1 box, 2 ellipse |  |
| `+0x04` | `f32` | width |  |
| `+0x08` | `f32` | depth |  |
| `+0x10` | `f32[3]` | position or centre |  |
| `+0x1C` | `f32` | heading |  |

## Shipped data

Over the 1,114 zone scripts, every one of the 502 that defines a unit and every one of the 258
that runs the automatic selector calls `btlAtelSetupActorStart` first, exactly once (515 scripts in
all; 13 install the defaults and spawn nothing). What the overriding zones author:

- `btlAtelSetSpawnDistance`, 70 scripts: `(5, 12, 43)` in 8, `(8, 12, 43)` in 7, `(6, 20, 43)` in 6,
  `(4, 12, 43)` in 5, `(50, 60, 70)` in 3, `(10, 90, 100)`, `(6, 8, 43)`, `(4, 24, 43)` and
  `(39, 100, 110)` in 2 each, `(12, 16, 43)` in 1, and `(0, 25, 30)` in the 32 test zones; every
  triple keeps `retire > max`;
- `btlAtelSetSpawnLimitDegree`, 12 scripts: 180 in 9, 360 in 2, 270 in 1;
- `btlAtelSetDeSpawnType`: `(1, 0, 0)` 4,937 times and `(0, 0, 0)` 1,809 times, never mode 2;
- `btlAtelSetDecidingEntryPointTimes`, 210 scripts, always 3;
- `btlAtelSetActiveActorMax`, 234 scripts: 6 in 147, 7 in 30, 5 in 27, 4 in 12, 8 in 11, 3 in 5,
  2 and 9 in 1 each; the native 28 is never authored;
- `btlAtelCanselInitialSpawnFlag`, 253 scripts, 11,571 calls, on the fresh-placement branch;
- `btlAtelSetMapJumoKeep`: no script.

[`enemy-placement-conditions.tsv`](enemy-placement-conditions.tsv) gives the spawn condition of each of the 6,229
placements in [`enemy-placements.tsv`](enemy-placements.tsv), in 23,242 rows. A placement is the `entryNN` function of
its actor. The actor's `spawnNN` and `respawnNN` functions enter it by a `requestreentry` step after `setentrygroup`
names its group and `btlAtelSetKeepWorkGroup` its lane (`0x00239840`; a negative lane uses the group as the lane). Each
row is one such step on one path, and gives:

- the group's source: a constant; the lane `btlAtelDecideEntryPointAuto` returns, or that lane plus an offset (the rare
  variant of a lane in the `rbl` zones); a bank return from `btlAtelDecideEntryGroupByPreviousMap` or
  `btlAtelDecideEntryGroupByContinuous`; the selection `btlAtelGetKeepWorkRealGroup` keeps for a lane; or the script's
  loop register; and the lane's source the same way;
- the tests on that path in five columns: story (シナリオフラグ, read directly or through the variables its writers
  set), weather, count (death counts, elapsed and respawn times, a death counter), random (call `0x0029`, play time)
  and other;
- the lane's respawn table row, decoded from the operand bytes: death limit and cooldown, base and range;
- for a lane the automatic selector offers, the gates of `0x00235720` with their instruction addresses and the values the
  script sets for them (cap, attempts, distance band, arc), or the defaults;
- the steps it comes from.

3,999 placements are entered at a lane the automatic selector offers, and 2,230 by the script's choice alone. By test:
1,406 placements have a count test, 956 a random test, 303 a story test, 68 a weather test and 3,122 another test;
3,726 have a path with no script test.

The Larva Eater placed by unique_monster_00 in `gil_e01`, `gil_e04`, `gil_e06`, `gil_f01`, `gil_f05`, `gil_g01` and
`gil_g04` enters from the area start:

1. `0x0026CE60` binds every record to group 0: `entry00` in slot 0 (`0x0026CFC7`) and `spawn00` in slot 7 (`0x0026D070`).
2. `0x0025D9E0` files `spawn00` on channel 2 and `entry00` on channel 1 (`0x00269860` at `0x0025DD37`, `0x00269640` at
   `0x002699B3`).
3. The higher channel runs first (`0x003DB6E0`). This `spawn00` has no `requestreentry` step: it ends in a loop around
   `wait 1` with no exit step, so `entry00` stays queued behind it on channel 1.

The Larva Eater of `gil_i`, `gil_j` and `gil_k` (levels 61 to 62) is entered by its own `spawn00`.

[`enemy-spawn-variables.tsv`](enemy-spawn-variables.tsv) lists the 1,442 variables those tests read, by place
(`file +0x00C0`, `scratch2 +0x40`), with every step that writes them. For `scratch2`, the writers include the zone scripts
of the same field group. 48 are death counters: a step adds 1 to them when `btlAtelGetRespawnCause()` returns 0.

## Operations

A zone's battle setup runs `btlAtelSetupActorStart`, then any overrides, then per entry
`btlAtelSetTotalEntryNumber`, `btlAtelSetEntryStruct`, and for each spawn either the continuing or
previous-map selection, `btlAtelSetKeepWorkGroup`, `btlAtelSetUnit`, `btlAtelDecideEntryPointAuto`
or `btlAtelSetEntryPositionForce`, `btlAtelSetEventFlagGroup`, `btlAtelSetDeSpawnType`, and
`btlAtelSetUnitFinish`, which places the body. The area initialiser `0x002342F0` resets the cap to 28
and rotates the banks before any of this runs.

## State

The seven globals, the two keep banks, the unit's lane map, candidate table, lane byte, mode bytes
and flag bits `0x200000`, `0x4000000`, `0x200000000000` and `0x2000000000000`, and the record's position, candidate and flag fields. The
shared generator `0x00328370` advances six steps per area placement and three per random candidate
draw.

## Modding notes

- Change the three floats at `0x009146EC`-`0x009146F4` to change the default band and range for every
  zone at once; change a zone's `btlAtelSetSpawnDistance` call, placed after
  `btlAtelSetupActorStart`, for one zone. A call before the reset is overwritten.
- Keep `retire > max`: with `retire <= max` a monster can satisfy mode-1 retirement on the frame it
  is placed. `min == max` disables automatic placement, because the generator refuses an empty band.
- The minimum distance is per unit and opt-in: without flag bit `0x200000000000` or `0x2000000000000` a monster may appear on
  top of the player. `btlAtelCanselInitialSpawnFlag` on the fresh branch is the only way to
  enforce it before the unit's first activation.
- The arc is halved with an integer divide, so an odd arc loses half a degree and 180 means plus or
  minus 90.
- Height is decided by the definition's byte `+0x18` bit `0x10` and the lift the definition supplies;
  a monster sunk in the floor is a definition problem, not a placement one. The candidate y is
  uninitialised until the probe runs, and a missed probe places the monster at world height 0.
- The attempt byte is stored unclamped above 1 and read signed: 0 and 128 to 255 skip every
  attempt, 256 stores 0. The cap byte is also compared signed.
- The distance test measures the steered character only, and the random path consumes the shared
  gameplay generator; both matter to anything that wants two machines to agree on a placement.

## Related

- [Enemy respawning](enemy-respawning.md): death counts, cooldowns, the group table and the banks.
- [Spawn record fields](spawn-record-fields.md): the record the lane map resolves to.
- [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md): the definition apply.
- [Battle units](../Characters-And-Objects/battle-units.md): the slot pool and the flag word.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the per-unit frame that runs retirement.
- [Random number generators](../Random-Numbers/random-number-generators.md): `0x00328370`.
- [Heading, speed and position](../Movement-And-Pathfinding/heading-speed-to-position-delta.md): the sine convention.
