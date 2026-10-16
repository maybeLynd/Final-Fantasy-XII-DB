---
title: "Enemy spawning: the spawn table, how a zone picks where a monster appears, the ground height, and when it vanishes out of range"
kind: "system"
category: "Enemy spawning"
addresses: "0023A2E0, 002395A0, 00236100, 002360D0, 0023A520, 0023A1D0, 0023A1F0, 00239020, 00235340, 00235330, 00235720, 00308D90, 00234AF0, 00234DA0, 002374E0, 00319390, 00328370, 002354F0, 00235360, 002355A0, 00236450, 00239840, 0023A3B0, 0023A570, 00233AD0, 00239E10, 0023A410, 003208C0, 00300310, 00239410, 00239210, 002391C0, 002396B0, 0023A200, 00236860, 00238FC0, 002350C0, 00300E40, 00306E60, 00233F70, 002342F0, 002368D0, 0031B810, 003273B0, 003272A0, 00320940, 003209C0, 003A1960, 005102D0"
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
lane naming a record in the live keep bank, `0xFF` for none. `00236100(map, lane)` returns
`[0208E690] + slot * 0x250` and `002360D0(map, lane)` the slot; both refuse a null map, a negative
lane, a lane at or past the count and the `0xFF` slot. The record is [the spawn
record](spawn-record-fields.md); its back-pointer is unit `+0x6A0`.

Verb `0x3016` `btlAtelSetTotalEntryNumber` (`00510620`) resolves its scope-3 operand to a pointer
into the script's data area and jumps to `0023A2E0(actor, map)`, which stores the map at unit
`+0x40` and, for every mapped record with flags `& 5 == 0` (neither retired nor released), writes
`+0x16` = `0xFF`, clears flag bits 0, 2 and 7, zeroes `+0x78`-`+0x7C` and restores the persistence
key `+0x17` from `+0x18`.

Verb `0x3018` `btlAtelSetEntryStruct` (`005106D0`) resolves its operand the same way and jumps to
`002395A0(table)`, which rolls each uncommitted record's death limit and cooldown from the table's
rows and writes its persistence key ([enemy respawning](enemy-respawning.md)).

### The tunables and their script defaults

Seven globals steer placement. All are BSS, zero at load, and installed at run time:

| Global | Meaning | Installed by | Read by |
|---|---|---|---|
| `02089358` | heading arc, degrees (i32) | `0023A520`: 180; `0023A1F0` (verb `0x305B`, float truncated) | `00234AF0` |
| `02089360` | minimum spawn distance (f32) | `0023A520`: 39.0; `0023A1D0` | `00235720` |
| `02089364` | maximum spawn distance (f32) | `0023A520`: 42.0; `0023A1D0` | `00235720` |
| `02089368` | retire range (f32) | `0023A520`: 43.0; `0023A1D0` | `002350C0` |
| `0208D457` | placement attempts (u8, read signed) | `0023A520`: 1; `00239020` (verb `0x3038`, clamped below 1) | `00235720` |
| `0208D458` | active cap (u8, read signed) | `002342F0`: 28 at every area entry; verb `0x304E` (`00510320`) | `00235720` |
| `0208936C` | return window, seconds (i32) | `002368D0`: 300; `00235340` (verb `0x306C`, negative restores 300) | `00233780` |

`0023A520` is nine instructions (`0023A520`-`0023A561`): the three floats from `009146EC`,
`009146F0` and `009146F4`, the arc and the attempt byte. Its only entry is the jump at `00510710`,
the handler of verb `0x3053` `btlAtelSetupActorStart`. Verb `0x300B` `btlAtelSetSpawnDistance`
(`0050F410`) pops three floats and tail-jumps `0023A1D0(retire, max, min)`, which stores them at
`02089368`, `02089364` and `02089360`, so in a script the arguments read `(min, max, retire)`.

`00308D90` counts, over the `00236850()` battle-unit slots through `00236820`, the units whose flag
word has bit 21, the bit the bind sets; verb `0x3050` returns
it and `0x304F` the cap byte.

A zone that never runs the reset has every float at 0: the candidate generator refuses an empty
band on its first test, and the mode-1 retire fires for every monster on its first frame. The
shipped scripts never get there (Shipped data).

### Automatic placement

Verb `0x301A` `btlAtelDecideEntryPointAuto` (`0050F520`) calls `00235720(actor)` and pushes its
result: the winning lane, or -1. The selector:

1. returns -1 when `00308D90()` is at or above the signed cap byte `0208D458` (`00235753`-`00235763`),
   or the unit, its candidate table `[unit + 0x38]` or its lane map is null;
2. computes `seconds = counter / (int)(30.0 * [01DFE0B8])` from `0032A150` (`002357D9`-`002357F9`);
3. walks lanes 1 to `table[0] - 1`, the candidate table's count word (lane 0 is never offered; a
   lane past the lane map's own count is skipped). A lane is skipped when its record has
   died out (`+0x0A` non-zero and `+0x08 >= +0x0A`), or is committed and not retired (flag bit 1 set,
   bit 0 clear) with a non-zero cooldown `+0x10` and `seconds - +0x0C < +0x10` unsigned;
4. sets the minimum distance to `02089360` when the unit's flag word has bit 45 or bit 49
   (`test qword ptr [rsi], r10` with `0x0002200000000000`, `002358EB`), else 0.0;
5. for each candidate id of the lane (the table's words from `table[1 + lane]` to
   `table[2 + lane] - 1`, a short; `0x00FF` is the sentinel, `00235919`-`00235925`, and a -1 is passed
   on and fails the record fetch), tries `00234AF0(id, &pos, minR, 02089364, &observed, 0)` for
   attempts `0` to `n - 1`, `n` = `0208D457` read signed;
6. an attempt is accepted when the call returns non-zero and `observed` is below `02F973B8` (the
   shared maximum squared distance, `+INF` from `002368D0`);
7. a hit records the lane and the position, and both loops run on, so the last accepted candidate
   of the highest accepting lane wins;
8. on a win it stores the position at the record's `+0x50` and `+0x60` as whole 16-byte moves
   (`00235A08`, `00235A0F`), sets unit flag bit 26 and returns the lane.

Bit 49 is set once per unit by the activation `00233AD0` (`00233B8C`) and never cleared, not even by
the unit reset `00236A60` (mask `0xFFFF7FFDFFE7FFFD`, [battle units](../Characters-And-Objects/battle-units.md));
bit 45 is set by verb `0x304D` `btlAtelCanselInitialSpawnFlag` (`005102D0`), which the zone scripts
call on the fresh-placement branch. So the minimum applies to a monster that has lived once or
that the script declared not an arrival placement.

### Generating a candidate

`00234AF0(id, out, minR, maxR, outObserved, allSlots)` refuses when `maxR - minR == 0.0`, then
fetches format-class-0 record `id` of the field data through `003209C0` (0 on success, -1 on
failure; `003DFD00(0, id, rec)`) and copies the record's point at `+0x10` into `out` before any
further test, so a 0 return can leave that point in the caller's buffer (the selector ignores it).

It needs the
party leader (`003272A0`: the focus handle's unit, with `02089340` bit 4 set and the unit's flag
bit 3), takes the leader's position (`00265020`) and heading (`00265200`), and branches on the
record's first byte:

- byte 0: point mode. The authored point stands. `0031AC90` gives the heading from the leader to
  the point (`atan2(dx, dz)`, or the leader's heading when the two coincide), `0031A930` the
  absolute wrapped difference, and the point passes the arc when that is at most
  `(arcDeg / 2) * 2pi / 360` with an integer halving (`00234C0B`-`00234C2B`); then
  `00234DA0(out, minR^2, maxR^2, outObserved, allSlots)` decides;
- any other byte: area mode. Two draws of `00328370`: `r = (draw % (int)((maxR - minR) * 100)) / 100
  + minR`, quantised to a hundredth, and `theta = wrap(heading + ((draw % arcDeg) - arcDeg / 2) *
  2pi / 360)` (`00316DA0`);
- `00319390` then builds `leader + (r * sin(theta), ?, r * cos(theta))` through the 32,768-entry
  sine table at `01F004E0` (`cos = sin[(0x2000 - i) & 0x7FFF]`), writing x and z only. The point
  is accepted when `002374E0` places it inside the record's region; no distance test runs.

`002374E0(point, rec)` transforms the point into the record's frame (`00325EA0`, centre `+0x10`,
heading `+0x1C`) and accepts a type-1 record when `|x| <= w/2` and `|z| <= d/2` (`w` at `+4`, `d` at
`+8`), a type-2 record when `x^2/(w/2)^2 + z^2/(d/2)^2 <= 1`, and nothing else. Each `00328370` call
steps the shared generator three times, so an area placement advances it six steps; point mode
draws nothing. Neither divisor is tested: a band under a hundredth wide, or an arc of 0, divides
by zero.

The y written in area mode is whatever the stack slot at `rsp + 0x54` held: `00319390` never
writes `[rdx + 4]` and `00234AF0` copies the slot into `out.y` (`00234CDD`, `00234CF2`). It rides
along to the record and is replaced at activation (the height section).

### The distance test

`00234DA0(cand, minD2, maxD2, outObserved, allSlots)` walks party slots 0-3 through `0031B810`
(the unit of the party-record byte at `[02EBF190] + 0x5A5A + 2 * i`, when `00322C50(0x17, i)` allows
the slot). A slot counts when it has a stats record whose status words `+0x64 | +0x3C` have none of
`0x80000003`, or the field waives that (`00377C20`), and, with `allSlots` = 0, when its handle
`+0x08` is the party focus (`003273B0` against `003590D0()`).

For each counted slot it measures the squared planar distance `(dx^2 + dz^2)` (`003A1960`) and returns 0 at once when a bound is given
and violated (`d2 < min` or `d2 > max`); it publishes `d2` to `outObserved` for the focus slot and
returns 1 only when at least one slot was counted. No counted slot is a rejection.

The spawn path passes `allSlots` = 0, so exactly one character is measured: the one the player is
steering. `00308040` is the other caller, with `allSlots` = 1 and a minimum only.

### Bringing a banked monster back

Two selectors look for a record the keep banks preserved. Both set unit flag bit 26 on success:

- verb `0x304B` `btlAtelDecideEntryGroupByPreviousMap` (`00510230`) calls `002354F0`, which walks
  the lane map from lane 0 and returns the first lane whose record has flag bit 2 (released), or -1;
- verb `0x305F` `btlAtelDecideEntryGroupByContinuous` (`00510260`) calls `00235360`, which, for each
  mapped record with a non-zero key `+0x17`, scans the 64 history-bank records for one with flag bit
  1 set, bit 0 or 2 set and the same key, and copies that whole `0x250`-byte record over the live
  one (`00235460`-`002354DD`), returning the lane; -1 when the history bank is null or nothing
  matches.

Verb `0x303C` `btlAtelSetEntryPositionForce` (`0050FCB0`) pops two floats and jumps to
`00239410(actor, z, x)`, which writes `{x, 0, z, -}` to the unit's own record (lane `+0x57`) at
`+0x50` and `+0x60` and sets bit 26; it returns -1 on a bad lane.

### Binding and the unit's own candidate

Verb `0x305C` `btlAtelSetKeepWorkGroup(selection, lane)` (`005103F0`; the first pop is the last
script argument) jumps to `00239840(actor, lane, selection)`. With a negative lane it uses the
selection as the lane. It writes the lane to unit `+0x57`, the selection
(or -1 for a negative lane) to the record's `+0x16`, clears flag bits 0 and 2 when the selection
changed (`002398C2`), restores `+0x17` from `+0x18` on a fresh record and sets unit flag bit 21, the
bit the active cap counts.

Verb `btlAtelSetUnit(id)` (`00510160`, one pop) applies a definition: `0023A3B0(actor, id)` first
runs `002355A0`, then `0023A570(unit, id | 0x100)`, or `0xFFFF` for an id of `0xFF` ([battle unit
construction](../Characters-And-Objects/battle-unit-construction.md)); when `00237650(actor)` is then
non-zero the handler runs `0037CF50(context, actor, -1)`.

`002355A0` returns 1 at once when bit 26
is already set, and 0 when the unit's lane `+0x57` is not below the candidate table's count word,
when the lane's range is empty, or when the drawn id is negative; otherwise it draws one candidate
id of that lane with `00328370` and generates a position with `00236450(id, &pos)`:

- record type 0: the authored point;
- type 1: a random offset inside the box, `x = (draw % (int)(w/2 * 100)) / 100`, the same for z,
  each negated when a further draw has bit 4 set;
- type 2: a random x the same way, then `z` drawn up to `sqrt((d/2)^2 - x^2 (d/2)^2 / (w/2)^2)`,
  each sign drawn;

the offset is rotated into the record's frame by `00319390` with the record's heading. On success
the position is stored at `+0x50` and `+0x60` and bit 26 set.

### Activation and the height

`00233AD0(actor)` runs the applied definition: for an active unit (flag bit 2) it posts `0x2001`
outside a town, refreshes the actor (`00238BF0`), and returns early only when the definition is
already applied (bit 3, `00233B3A`) and `0037C8C0(actor)` is 0. Otherwise it runs `00324450(unit)`,
sets bit 3, runs `00239E10`, sets bit 49, sets the record's flag bit 1 for a kind-1 unit
(`00233BA8`), and publishes the position (`00311F70(0, unit, 1)`) when bit 26 is clear, the status
gate passes and `003278C0()` is 0. For an inactive unit it clears bit 26.

`00239E10` writes the placement-height byte `+0x1F6`: 1 for a kind-0 stats record; for any other
kind, or no stats record, from the definition record's byte `+0x18` (`[unit + 0xE68]`): 8 when bit
4 is set, else 2 when bit 5 is set, else 1, with 4 added when bit 6 is set. For a kind-1 unit with
the probe bit it also stores `00236210(unit)` at `+0x188`, the vertical lift; otherwise `+0x188` = 0.

Verb `0x304C` `btlAtelSetUnitFinish` (`00510250`, a jump) runs `0023A410(actor)` on the unit's own
record:

1. for a fresh record (flags `& 5 == 0`) whose definition row's dword `+0x18` is non-zero,
   `00300520(stats, row.dw_18, 0, 0x297)`: an authored starting HP;
2. flag bits 2 and 0 cleared;
3. `002FED60` or `002FEDC0(unit, 1)` by `00308010(unit, 1)`, then `00238BF0(unit)`;
4. when `+0x1F6` has bit 3, `003208C0(x, z, &y)` probes the ground under the record's `+0x60`/`+0x68`:
   it asks `0026E3C0([02EC1370], {x, 1.0, z, 1.0})` and writes the surface height, or 0.0 when the
   query returns -1; the return value is ignored, and `+0x188` is added (`0023A4D5`);
5. `00300310(unit, record + 0x60, 0, 1)` places the unit at the record's candidate position, then
   `0030FED0(stats, 0x297)` and `00386C10(stats)`.

A spot with no collision under it therefore gives a monster at world height 0 plus its lift, and
no error.

### Facing, inhibit, category and the lifecycle float

- `00239210(actor, degrees)` (verb handler `0051077C`): a negative argument draws `00328370() % 360`;
  the angle in radians is wrapped (`00316DA0`) and stored at the record's `+0x70`, then applied to
  the actor (`0026A0D0`, `0026B620`).
- verb `0x3015` `btlAtelSetCallGroup(tag)` (`00510370`) → `002391C0`: on a record not released, clears
  flag bit 4 and `+0x15`, then sets both to the tag when it is non-zero.
- verb `0x3005` `btlAtelSetUnitType(n)` (`00510340`) → `002396B0`: unit `+0x58` from the table
  `{1, 5, 3, 4}` at `01E09EE8` for `n` below 4, else 0; on a fresh record clears flag bit 5 and sets
  it when the byte became 4.
- verb `0x3017` `btlAtelSetSpecialSpawnRange(f)` (`005107C0`) → `0023A200`: unit flag bit 40 set
  for a non-zero `f`, cleared for 0; on a fresh record `+0x04` and bits 3 and 6 cleared, then `+0x04`
  = `f` with bit 3 for `f > 0`, or `-f` with bit 6 for `f < -1.0`.
- verb `0x305E` `btlAtelIgnoreKeepWork(lane, ignored)` (`005104D0`) → `00236860(actor, _, lane)`:
  clears bits 0, 2 and 7,
  sets the word `+0x16` to `0x00FF` and zeroes `+0x78`-`+0x7C` of the lane's record.

### The despawn mode

Verb `0x3019` `btlAtelSetDeSpawnType(mode, threshold, anchor)` (`0050F4A0`, three pops, the first
pop being the last script argument) calls `00238FC0(actor, anchor, threshold, mode)`, which stores
the mode at unit `+0x50` always and, for mode 2, the threshold `+0x4C` = `threshold / 10.0` (6.0
when 0) and the anchor `+0x51`. The shipped scripts call it with `(1, 0, 0)` 4,937 times and
`(0, 0, 0)` 1,809 times; no shipped script authors mode 2.

### Range retirement

The per-unit frame `00233F70` (the record's `+0x38` callback, [field
runtime](../Characters-And-Objects/field-runtime.md)) calls `002350C0(actor)` at `00234022` for a bound unit
with flag bits 3 and 4 whose status gate passes. `002350C0` returns 0 unless the record's `+0x0D`
bit 6 is set (`002672F0`, the drive loop's "scheduled this pass" bit), the unit exists with a non-zero
mode `+0x50`, its stats record has a non-zero kind byte, unit flag bit 4 is set, the status words pass
the `0x80000003` gate or the field waives it, and the record's flag bit 4 is clear. Then:

- mode 1: for party slots 0-3, a slot counts when it has flag bit 4, a stats record passing the gate,
  and is the party focus. The unit is kept when any counted slot's squared planar distance is below
  `02089368^2` (`0023527D`, `comiss`/`ja`); it retires when at least one slot counted and none was
  nearer. At exactly the range it retires;
- mode 2: needs the leader and the anchor point `00320940(+0x51)`; retires when the leader's
  navigation position (unit `+0xE0`) is within `(+0x4C)^2` of it (`comiss`/`jbe`);
- any other mode: 0.

Retiring sets the record's flag bit 0 (`002352A6`), tears the unit down with `00300E40(unit, 1)`,
the one call that keeps the record's transient state, and unregisters the member from its group
with `00306E60(unit, 0)`. A NaN distance retires in both modes; a party with no counted focus slot
never retires a mode-1 unit.

## Layouts

Globals (BSS):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `02089358` | `i32` | heading arc degrees | `02089360`  f32  min distance   `02089364`  f32  max distance |
| `02089368` | `f32` | retire range | `0208D457`  u8   attempts (signed use) |
| `0208D458` | `u8` | active cap (signed use) | `0208936C`  i32  return window, seconds |
| `02F973B8` | `f32` | max considered squared distance, +INF (002368F0); shared with AI targeting and loot |  |
| `01F004E0` | `f32[32768]` | sine table, table[i] = sin(2 pi i / 32768) |  |
| `009146EC` | `/ 009146F0 / 009146F4` | f32 | 39.0 / 42.0 / 43.0, the script defaults |

BattleUnit fields this page uses:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u64` | flags: bit 2 active, 3 definition applied, 4 drive, 21 cap-tracked, 26 candidate prepared, | 40 special range, 45 not an initial placement, 49 activated once |
| `038` | `void*` | candidate table: u16 count, then u16 offsets per lane, then i16 candidate ids |  |
| `040` | `void*` | lane map: u8 count, u8 slot per lane (0xFF none) |  |
| `04C` | `f32` | mode-2 threshold | +`0x50` u8 despawn mode 0/1/2     +`0x51` u8 anchor record |
| `057` | `i8` | the unit's own lane | +`0x58` u8 category byte |
| `188` | `f32` | vertical lift | +`0x1F6` u8 height mode: bit 3 = probe |
| `698` | `void*` | stats record (+0x05 kind) | +`0x6A0` ptr spawn record   +`0xE68` ptr definition record |

Field format-class-0 record (`003DFD00`(0, id, rec)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | type: 0 point, 1 box, 2 ellipse |  |
| `04` | `f32` | width | +`0x08`  f32  depth |
| `10` | `f32[3]` | position | or centre |
| `1C` | `f32` | heading |  |

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

## Operations

A zone's battle setup runs `btlAtelSetupActorStart`, then any overrides, then per entry
`btlAtelSetTotalEntryNumber`, `btlAtelSetEntryStruct`, and for each spawn either the continuing or
previous-map selection, `btlAtelSetKeepWorkGroup`, `btlAtelSetUnit`, `btlAtelDecideEntryPointAuto`
or `btlAtelSetEntryPositionForce`, `btlAtelSetEventFlagGroup`, `btlAtelSetDeSpawnType`, and
`btlAtelSetUnitFinish`, which places the body. The area initialiser `002342F0` resets the cap to 28
and rotates the banks before any of this runs.

## State

The seven globals, the two keep banks, the unit's lane map, candidate table, lane byte, mode bytes
and flag bits 21, 26, 45 and 49, and the record's position, candidate and flag fields. The
shared generator `00328370` advances six steps per area placement and three per random candidate
draw.

## Modding notes

- Change the three floats at `009146EC`-`009146F4` to change the default band and range for every
  zone at once; change a zone's `btlAtelSetSpawnDistance` call, placed after
  `btlAtelSetupActorStart`, for one zone. A call before the reset is overwritten.
- Keep `retire > max`: with `retire <= max` a monster can satisfy mode-1 retirement on the frame it
  is placed. `min == max` disables automatic placement, because the generator refuses an empty band.
- The minimum distance is per unit and opt-in: without flag bit 45 or 49 a monster may appear on
  top of the player. `btlAtelCanselInitialSpawnFlag` on the fresh branch is the only way to
  enforce it before the unit's first activation.
- The arc is halved with an integer divide, so an odd arc loses half a degree and 180 means plus or
  minus 90.
- Height is decided by the definition's byte `+0x18` bit 4 and the lift the definition supplies;
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
- [Random number generators](../Random-Numbers/random-number-generators.md): `00328370`.
- [Heading, speed and position](../Movement-And-Pathfinding/heading-speed-to-position-delta.md): the sine convention.
