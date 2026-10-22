---
title: "Battle locomotion: how a combat unit picks its step and heading, the turn limiter, spacing and avoidance, detour and stall recovery, and the corridor probes"
kind: "system"
category: "Movement and pathfinding"
addresses: "0x00325BB0, 0x0033A720, 0x00339DF0, 0x0033B6F0, 0x00337470, 0x00335180, 0x0033CC80, 0x0033A240, 0x0033D890, 0x00337C10, 0x00336CE0, 0x00336710, 0x003394A0, 0x0033BED0, 0x00339BF0, 0x003364D0, 0x0033CB70, 0x00334120, 0x0033A570, 0x00338140, 0x0033D660, 0x003343D0, 0x0033C870, 0x00334E00, 0x0033E1F0, 0x0033C200, 0x0033BD70, 0x00334950, 0x003347C0, 0x0033C310, 0x0033BFB0, 0x00339F00, 0x0033CEF0, 0x0033D200, 0x0033CE60, 0x0033CDE0, 0x0033BAA0, 0x0033BC80, 0x00334AB0, 0x00334C30, 0x00335B60, 0x003357B0, 0x0033D3E0, 0x00335E50, 0x0033A3D0, 0x00335F90, 0x00391410, 0x00312730, 0x00253B90, 0x0030A130"
---

## What the player sees

A unit closing on its target slows into place rather than halting, and creeps the last fraction
rather than snapping onto it. Big reversals swing round fast and then visibly ease as the unit
lines up; small course corrections produce no turn at all, so units in battle drift and strafe
rather than aim exactly where they walk. Two units never settle on the same spot: each keeps a
spacing from the other and tests its next step against every moving body before taking it.

A unit whose way is blocked tries a sidestep, and which side it picks is not reproducible: the
choice comes from the C runtime's random generator, shared with everything else in the process.
A unit that makes no progress for about a second is treated as stuck and looks for a point along
its own route it can still reach.

## How it works

### The navigation step

Combat asks for movement; the movement system does not act on its own. `0x00325BB0(unit)` runs from
four combat sites (`0x002FDBE9`, `0x002FDD69`, `0x00304D5B`, `0x00308341`): it routes the unit across the
mesh and follows the route to the next waypoint ([navigation mesh and
pathfinding](navigation-mesh-and-pathfinding.md)), refreshes the locomotion flags, and hands the
locomotion block at unit `+0x80` to the solver `0x00336CE0(block, block)`.

The solver writes its results back: the block's `+0xD8` from the context's speed `+0xB0`; `+0xDC`,
`+0xF4` and `+0xE0` from the desired heading, pitch and limited heading `+0xB4`-`+0xBC`; `+0x170`
from the flags copy `+0xCC`; `+0xC0`-`+0xC8` from the detour point `+0x50`-`+0x58` (written by
`0x0033C870` and `0x0033BD70`); and the block's `+0x18`/`+0x1C` from the context's x and z (`+0x00`,
`+0x08`), the position at this solve.

### The solver context

`0x00336710(ctx, block, 1)` fills a working context from the block: four positions at `+0x60`,
`+0x70`, `+0x80` and `+0x90` into `ctx + 0x00`, `+0x10`, `+0x20` and `+0x30` with `w` = 1.0; the
larger collision radius `max(+0x10C, +0x110)` at `+0xA0`; the three heading floats `+0xDC`, `+0xF4`,
`+0xE0` at `+0xB4`, `+0xB8`, `+0xBC`; the unit from the slot byte `+0x177` (`0x00236820`) at `+0xF0`
and its actor handle's record at `+0xD8`; the flags `+0x170` at `+0xCC`; the step scale `+0x108`
at `+0xC0`, raised to 2.0 below 2.0 unless the unit's definition byte `+0x18` has mode 2.

It also stores the party leader's actor at `+0xE8` and its position at `+0x60`, and the distance
to the goal at `+0xC8`.

When the goal kind `+0x160` is 3, or `+0x40` is 1 or 2, the target unit of the handle `+0x150`
(`0x0031B7E0`, `0x003588B0`) is stored at `+0xF8`/`+0xE0`, its position at `+0x40`, its radius at
`+0xA4`, its bearing at `+0xA8` and the distance to it at `+0xC8`. The stop distance `+0xAC` is
`radius + targetRadius + 0.1` when `+0x40` is 1, else the block's `+0xD0`.

For a unit with order
`0x4124`, or `0x4022` while the party is fleeing (`0x00253B90` non-zero, [force fight mode](../Engine-Core/force-fight-mode.md)), `0x0033D3E0(ctx, leader, 1)`
sets `+0xD0` bit 0 when it does not return 1: the leader is reachable in a straight walk.

### Which solver runs

`0x00336CE0` reads the unit's definition record `[unit + 0xE68]` byte `+0x18` bits 1-3: mode 1 and 3
return without solving, mode 2 runs the class solver `0x003394A0`, anything else the default solver
`0x0033BED0`.

The class solver: with the goal kind `+0x40` non-zero it stops (`+0xB0` = 0) and only limits the
heading toward the goal; otherwise it takes the step distance, and when the unit is
over 16 units from field point 8 (`0x00320940(8)`) with `ctx + 0x04` below 5.7 it stops with a
pitch of `pi/2`; else it faces the goal `+0x20` (`0x0033CEF0`) and takes the pitch toward the step point `+0x10`
raised by `+0xC0 + 3.2` (`0x00468700`).

### The default solver

`0x0033BED0(ctx)`: when `0x00336040()` is 0 it zeroes the speed and runs `0x00469A50` on the unit pair.
Otherwise it sets the speed `+0xB0` from the step distance, clears `+0xCC` bit 7, and runs in order
the detour recovery `0x0033C870` and the stall recovery `0x0033C200`; when neither claims the step and
the flag word's countdown bits (`0x7FE0`) are clear, it runs the spacing pass `0x00338140` for goal
kind 1 or the heading constraint `0x0033A570` otherwise; with a countdown running it runs the
steering dispatcher `0x00339F00` instead.

Those three paths end in `0x0033BFB0`; a step claimed by
`0x0033C870` or `0x0033C200`, and the `0x00336040` = 0 path, return without it.

### The step distance

`0x00339BF0(ctx)` is a quadratic arrival curve on the horizontal distance `d` to the destination `+0x30` (block `+0x90`;
`0x004686D0` ignores y):

```python
party unit (kind 0) with order 0x4022 while fighting (0x00253B90 zero) : return speedB (+0xFC)
flags +0x170 bit 0 : speedA (+0xF8)     bit 1 : speedB
goal kind +0x40 == 1, unit +0x768 >= +0x76C, d > stop (+0xD0)    : speedB
rem = max(0, d - stop);  kind 2 also subtracts the actor's smaller radius + 0.5
rem /= 7                      when the mover class +0x174 is 2 or more
rem = dstart / 5 or * 0.25    when ctx +0xD0 bit 0, from the distance to +0x60 (fleeing: * 0.25; fighting: / 5)
rem /= 3 or 1.5               otherwise (fleeing: 1.5; fighting: 3)
v = rem * rem * speedB;  speed = clamp(v, speedA, speedB)
speed > d                     : speed = d * 0.99
```

The `0.99` keeps a unit from stepping past its goal; it lands one percent short every frame and
creeps in. The force-fight predicate `0x00253B90` is reached through the thunk `0x0030C0D0`.

### The turn limiter

`0x003364D0(ctx, desired)` limits the heading `+0xE0` of the block. With `a = |wrap(cur - desired)|`
(`0x0033CB70`): above 45 degrees (`0.785398`) it raises the turning flag (block `+0x38` bit 3), and
without that flag it returns the heading unchanged.

- Above 120 degrees (`2.0944`) it latches the fast rate (`+0x3C` bit 0) when `+0x170` has all of
  bits 2-4, and steps the heading by the latched rate (`+0xF0` fast, `+0xEC` slow) in the direction the pair
  `+0x21` bits 1-2 recorded, unconditionally; with no direction recorded it steps by the sign of
  the wrapped difference and snaps to `desired` when within the rate.
- Below 20 degrees (`0.349066`) it clears the latch and uses the slow rate; between, it keeps
  whatever is latched. The step snaps to `desired` when within the rate.
- The direction pair is rewritten as clear-then-set, and reaching `desired` clears both the latch
  and the turning flag.

So the three angles are one hysteresis loop: entry at 45, escalation past 120 only for a unit
whose model authors `@FCP` slot 41, whose flag bit 23 is up and which is mid-cast of something
other than Attack (the three bits the navigation step maintains), release inside 20. The same
error produces different behaviour depending on history.

`0x0033CB70` normalises by repeated `2pi`
steps within `+-4pi`; beyond that it returns `x - 2pi * trunc(x / 2pi)` once
(`0x0033CBCD`-`0x0033CBE8`), whose magnitude is below `2pi` but can be above `pi`; `0x00334120(cur, target, rate)` is the
approach helper the modes use: snap within the rate, else step by it and wrap.

### The steering modes

The block's flag word `+0x00` carries the mode in bits 0-4, a countdown in bits 5-14 and the orbit
direction in bit 15. `0x00339F00(ctx)` runs while the countdown is non-zero: it projects the step
point `+0x10` from the target `+0x40` back by `+0x110 + +0xA4 + 0.1` (the block's second collision
radius plus the target radius) along the heading, takes the
pitch toward it for class 3 (0 otherwise), dispatches on the mode, clears the countdown when the
speed exceeds the distance to that point, and otherwise counts it down by one.

| Mode | Body | What it does |
|---|---|---|
| 1, 4 | `0x0033CEF0` | turn while moving: the rate is `+0xE4` above the speed threshold `+0x104`, else `+0xE8`; below 60 degrees the rate eases by `(1 - cos(3a)) / 2` toward one degree; the limited heading `+0xBC` follows the target by the rate, or snaps to the current heading when the distance is under `speedB`; past `speedA * a / +0xE8` the desired heading `+0xB4` is also capped by `+0x118`; arms a countdown of 6, or 5 with force-fight on for a unit under order `0x4022` whose definition record `[+0x698]` has byte `+5` zero |
| 2 | `0x0033D200` | when `0x00334220` allows, a straight approach by the rate and returns 5; else the rate scales by `20 + 80 * a / 45deg` percent inside 45 degrees, snaps to the current heading within `5 * speedA`, arms a countdown of 10 |
| 3 | `0x0033CE60` | stop and turn: speed 0, both headings approach the target by the slow rate `+0xEC`, countdown 10, cleared on arrival |
| 5 | `0x0033CDE0` | turn while moving at `+0xE4` or `+0xE8` without stopping |
| 6 | `0x0033BAA0` | orbit: the orbit heading `0x00334AB0` is probed (`0x00335B60(ctx, heading, 0, 1.0, 0.8, 0)`); when the probe rejects and the pair clearance `0x0033D660` returns 0, the countdown is cleared and the speed zeroed; else `+0xB4` takes the orbit heading, the pitch 0, the speed `speedA`, `0x0033BC80` runs on the point 0.1 ahead, and the limited heading `+0xBC` approaches the target bearing `+0xA8` by `1.5 * (speedA / circumference) * 2pi` |

### The heading search

`0x0033A720(ctx)` chooses the heading of a step by trying a fan of headings around the bearing to the
step point. The default solver reaches it through `0x0033A570` when the unit is farther than its stop
distance `+0xAC` from the destination `+0x30`, or under order `0x4124` when the straight walk to the
goal is blocked (`0x0033D3E0`); otherwise `0x0033A570` stops the unit. The spacing pass runs it for bit
1. It works in this order:

1. The field row: the current map (`0x003148F0`) is looked up by its first `u16` in the `move_support`
   table (`0x02EBF010`, [authored data
   tables](../Game-Files-And-Data-Tables/authored-data-tables.md)); the first matching row
   gives a distance cap (byte `+2` / 10) and a narrow-fan flag (byte `+4` bit 0).
2. A flier (mover class `+0x174` = 3) has the goal's height `+0x24` set to the terrain height
   (`0x003208C0`) plus its step scale `+0xC0`.
3. The step point `+0x10` is the goal `+0x20`, or the look-ahead point `0x00335180` when the corridor
   to the goal is blocked (`0x00335F90`). Its flat distance `d` (`0x004686D0`), its bearing (`0x004687F0`)
   and the pitch `0x00337470` are taken.
4. The probe distance is `min(3.0, d)` when the step point is not the goal. At the goal it is the
   smaller of the row's cap (3.0 without a row) plus the second radius `+0x110`, and `d - +0xAC +
   +0x110` (for goal kind 2, `d - +0xAC` minus the target's smaller radius); a row also caps it at its
   own distance (plus `+0x110` unless goal kind 2). It is never negative.
5. `0x0033B6F0` updates the zig-zag memory (below), and the fan is tried.

The fan comes from three tables on the stack, picked by the mover class and the side the last
detour took (block `+0x38` bits 6-7: 0 none, 1 the positive side, 2 the negative side):

| Fan | Side none | Side 1 | Side 2 |
|---|---|---|---|
| mover class 0-1, 12 entries | 0, 30, -30, 60, -60, 90, -90, 135, -135, 0, 0, 0 | 0, 30, 60, 90, -30, -60, -90, 135, -135, 0, 0, 0 | 0, -30, -60, -90, 30, 60, 90, -135, 135, 0, 0, 0 |
| the row's narrow flag, 10 entries | 0, 30, -30, 60, -60, 90, -90, 0, 0, 0 | 0, 30, 60, 90, -30, -60, -90, 0, 0, 0 | 0, -30, -60, -90, 30, 60, 90, 0, 0, 0 |
| mover class 2 and up, 7 entries | 0, 45, -45, 90, -90, 135, -135 | 0, 45, 90, -40, -90, 135, -135 | 0, -45, -90, 45, 90, -135, 135 |

Angles are degrees added to the bearing. The -40 in the class-2 side-1 fan is the shipped value
(`0xBF32B8C3`, -0.6981 rad), not -45. A flier tries each heading at the pitches 0, 30 and 45
degrees added to `0x00337470`'s pitch; every other unit at that pitch alone. For each candidate:

1. it is skipped, and that memory consumed, when it lies within 45 degrees of a remembered heading
   (block bytes `+0x2F`/`+0x30`, live while `+0x31`/`+0x32` are non-zero);
2. it is skipped when it is more than 150 degrees from the last chosen heading (byte `+0x2C`, `byte
   * pi / 128`), or its pitch is not within 90 degrees;
3. a candidate of 135 degrees, once an earlier candidate came back 2 (moving units in the way, none
   blocking), is replaced by that earlier candidate, taken without a probe;
4. otherwise the forward clearance `0x00335B60` probes it at the probe distance (at `+0x110 + 1.8`
   for the 135-degree entries), with tolerance `1 - attempts / 10` and flags 8 for the straight
   heading, plus 4 under order `0x4124` or `0x4022` while fleeing, else 2. A result of 0 takes it; a
   result of 2 is remembered.

A taken heading gets its steering mode from `0x00339DF0` (below). Mode 2 needs a second clear probe
along the limited heading `+0xBC` (distance 1.0, tolerance 0.8) and then runs `0x0033D200`, whose
result replaces the mode; a blocked second probe makes it mode 1. Mode 1 runs `0x0033CEF0`. Mode 3
stops the unit, steps both `+0xB4` and `+0xBC` from the current heading toward the candidate by the
slow rate `+0xEC`, and starts a countdown of 10 when none runs (cleared when the heading arrives).

The pitch goes to `+0xB8`, the heading to byte `+0x2C`, `0x0033CC80` records the aim, the side bits
are set by the sign of the offset (both cleared for 0), and the attempt counter (block `+0x3C` bits
4-7) is cleared. When no candidate is taken, `0x0033CEF0` runs toward the bearing, `0x0033CC80` records
mode 4, and the attempt counter rises by one up to 10, which lowers the next search's tolerance.

`0x0033CC80(ctx, mode, heading, pitch, distance)` writes the aim: when the distance exceeds the
speed `+0xB0`, the mode goes to the flag word's bits 0-4 and the point `distance` ahead along the
heading and pitch (`0x01F004C0`, `{0, 0, 1}`, scaled, turned about x by the pitch and about y by the
heading) to block `+0x04`-`+0x0C`, the same `+0x04` mode 6 uses as its orbit radius; otherwise the
mode and countdown are cleared.

The vector helpers here: `0x004687F0` is the flat bearing of a vector, `acos(z / |v|)` from the table
`0x00D12590`, negated for a negative x; `0x004692F0` rescales a vector to a length (`0x00469320`
normalises it, leaving zero for a vector within `1e-6` of zero, and `0x00202FE0` scales);
`0x00202F00`, `0x00202E90` and `0x00202F70` copy a matrix and turn it about y, x and z (`0x00217880`,
`0x00217790`, `0x00217970`).

`0x00203170` writes the identity matrix that `0x0033CC80`, `0x0033D890` and the
collision sweep's `0x0022EF20` start from. The same vector library holds `0x00203030` (a four-float
vector times a scalar), `0x00202CA0` (the four floats times the reciprocal of a scalar), `0x00202CF0`
(x, y and z divided by a scalar) and `0x002030E0` (a matrix copy with a vector added to its
translation row); their callers are presentation and text code outside this category.

### The steering mode table

`0x00339DF0(ctx, heading)` turns the angle `a = |wrap(heading - +0xE0)|` into a steering mode. It
indexes 48 rows of 12 bytes at `0x01EED4C0` by block byte `+0x175` (values above 7 read as 1) times
6, plus 3 when flag `+0x170` bit 3 is clear, plus the speed band (0 at rest, 1 up to the threshold
`+0x104`, 2 above). A row holds two angles in degrees and two mode bytes: `a` above 0.01 and above
the first angle returns 3; `a` below the second angle returns the first byte plus 1; anything else
the second byte plus 1.

### The zig-zag memory

`0x0033B6F0(ctx)` counts down the two memories `+0x31`/`+0x32`, takes the bearing of the unit's move
since the last call (from the position kept at block `+0x24`/`+0x28`, then updated), and keeps the
last two move headings as bytes at `+0x2E` (latest) and `+0x2D`.

When those two differ by more than
90 degrees and the latest also differs from this move by more than 90, the unit is reversing
direction: unless a live memory already lies 130 degrees or more from byte `+0x2C`, the first free
memory takes `+0x2C` with a life of 5 solves. A move more than 30 degrees from `+0x2E` shifts it
into `+0x2D` and stores the new bearing.

### The flier's pitch and the look-ahead point

`0x00337470(ctx)` returns 0 for any mover class but 3. A flier takes a reference point: the target
position `+0x40` when the goal is kind 1, the step point is the goal and the unit is not of
definition mode 2; else the step point. Two points lie along the route toward the current region's
waypoint (the path record's `+0x90`): `A` at `+0x110 + 0.1`, `B` at the waypoint's flat distance
plus `+0x110`.

Each takes the terrain height (`0x003208C0`) when its ground is walkable for the mover class
(`0x0026E100`), else the reference's. The aim is `B` or the reference, whichever is higher, when `A`
plus the step scale is not above the unit; otherwise the higher of `A` and `B` when either is above
the reference, else the reference. The pitch is `0x00468700` toward the aim raised by the step scale.

`0x00335180(out, ctx)` is the look-ahead point. Starting from the route's start region (path `+0x04`)
it takes that region's waypoint, and while the region is not the goal and has a next region it
advances when the unit's position lies inside a triangle of the next region (all three edge crosses
of one sign) or within 0.2 of one of its edges (`0x00468F70`); at most 128 steps. The point's height
is the terrain height plus the step scale for a flier, else the unit's own.

### The definition modes and the circling formation

`0x0033A240(block)`, run from the per-unit frame `0x00233F70` (`0x00234076`) and from `0x00308610`, gives an
enemy its own locomotion by its definition. It builds the solver context (`0x00336710(ctx, block,
0)`) and acts only for a unit whose stats record is an enemy's (byte `+5` = 1), whose class row
(`[unit + 0xE68]`) has a non-zero mode in byte `+0x18` bits 1-3, whose step flags `+0x1F0` have
neither `0x1000` nor `0x2000`, and whose flag bit 18 is clear or speed `+0x158` is 0.

While no action is being shown (`0x02089350` = 0) it runs the mode's body: 1 `0x0033DFD0`, 2
`0x0033D890`, 3 `0x0033DB60`. Either way it writes the context's speed, desired heading, pitch and
limited heading back to the block's `+0xD8`, `+0xDC`, `+0xF4` and `+0xE0`.

`0x0033D890(ctx)` is mode 2. While the unit's status words (`+0x3C | +0x64` of the stats record) lack
KO (bit 0) and the battle-state word `0x02089340` lacks bit 5, the unit moves at `speedA` along its
limited heading with pitch 0. A KO'd mode-2 unit whose `0x40`-byte slot record (`0x0208DE80` indexed
by unit byte `+0xEA9`) has `+0x1C` bit 0 joins the circling formation instead:

1. the first such unit in a frame runs `0x00337C10`, which counts the KO'd mode-2 enemies into
   `0x022C7CEB`, finds an enemy of mode 5 (the last one in the unit table) and advances the shared
   angle `0x022C7CE0` by `0x02EC0F84`;
2. `0x00337C10` also samples the centre `0x022C7CF0` from that enemy's position: on a call
   with the counter `0x022C7D00` at 0, which starts counting when the enemy moves (speed `+0x158`
   non-zero); then, from the tenth call on, on every call until a call finds it stopped and resets
   the counter; it sets `0x022C7D04` bit 0;
3. each circling unit takes the next place `0x022C7CE9`: its goal `+0x20` is 1.0 from the centre at
   the angle `0x022C7CE0 + place * 2pi / count` (0 apart with fewer than two), raised to its step scale
   plus 3.2, and its step scale `+0x108` becomes 1.5;
4. within 0.1 of the goal the slot record's `+0x1C` bit 1 is set; until then the speed is `3.0 / (30
   * [0x01DFE0B8])`, after it the distance capped at `7.0 / (30 * [0x01DFE0B8])`;
5. the desired heading and pitch aim at the goal (`0x004687F0`, `0x00468700`) and the limited heading
   faces the centre.

The field frame clears `0x022C7D04` bit 0 and the place counter `0x022C7CE9` each frame (`0x0033B6D0`, after
`0x00338490`), and the area initialisation clears the block (`0x0033A380`). `0x00337A00`, at start-up, sets the angle step
`0x02EC0F84` to `2 / (30 * [0x01DFE0B4])` radians and stores `[0x01DFE0B4] * 240` beside it at `0x02EC0F80`.
`[0x01DFE0B4]` is the integer 1 in the image, so the formation turns 2 radians a second.

### Spacing and avoidance

`0x00338140(ctx)`, for goal kind 1: when the target is the unit itself, or the distance to the target
position `+0x40` is under 0.1, it stops and clears the countdown.

Otherwise, with `D` the distance
to the destination `+0x30`, it sets block `+0x38` bit 1 when `D` exceeds `min(+0x124 + 2, +0x128)`,
bit 2 when `D` is within `reach + 0.05` (reach = `+0x120`, or the target's own `+0x1A0` when the
target's target is this unit and its `+0x1A4` is below `+0x124`) and `0x003341A0` holds, clears bit
1 inside the stop radius `+0xD0` and bit 2 outside it, and sets bit 1 when the pair clearance
`0x0033D660` returns 0.

Then:

- bit 1: `0x00337A50`, the heading constraint `0x0033A720`, and the countdown cleared on success;
- bit 2: the bearing from the step point back to the position (away from it) is probed with
  `0x00335B60(ctx, bearing, 0, 0.1, 0.8, 0)`; when clear the speed is `speedA`, `+0xB4` that reverse
  bearing and `+0xBC` the limiter's result for the forward bearing; else bit 2 is cleared;
- neither: the randomised manoeuvre `0x003343D0`, then `0x0033BAA0` when it starts;
- with neither bit and no countdown: speed 0, the limiter, and `0x0033BC80`.

`0x0033D660(ctx, a, b)` is the pair clearance: with both radii from `0x00265090` it takes
`b.+0x1A8 - (ra + rb)`, halved for a party unit and divided by 3 otherwise, and returns 1 when the
distance to `b` is below `+0x1A8` and either unit's definition byte `+0x12` is negative, or
`0x00334C90` is at most that margin, and the raised segment between them (`0x00318CA0`) returns below 2.

`0x003343D0(ctx)` starts a sidestep:

1. it refuses when the target unit is the unit itself, the distance to the target is within
   `+0xA0`, the mode is 6, the odds `+0x130` are -1, or the unit (`0x00335760`) is not engaged and
   not under order `0x96`; after the angle tests it also refuses while the turning flag (block
   `+0x38` bit 3) is set;
2. `0x003357B0` is asked about the corridor to the target; the odds halve when it reports blockers;
   `rand() % odds` must be 0;
3. the target must lie within 120 degrees of the actor's facing and the actor within 45 degrees of
   its heading;
4. a `rand()` bit picks the side (flag bit 15); `0x00335B60` probes `0x00334AB0`'s orbit heading, the
   other side on failure, and both failing refuses;
5. otherwise the countdown is set to `+0x12C / 0x00334C30` quarter turns (halved for `0x0031EA90`
   class 4), the mode to 6, and the orbit radius `+0x04` to the current distance plus or minus
   `(rand() % 5 + 5) / 100`.

### Detour and stall recovery

`0x0033C870(ctx)`: with `+0xCC` bit 10 set it finishes a detour: `0x00334E00` picks the point into
`+0x50`, for goal kind 1 the limited heading `+0xBC` takes the bearing from that point to the
target, bit 10 becomes bit 7, `0x0033E1F0` resets the avoidance state, block `+0x3C` bit 3 is
cleared, and the step is claimed. Otherwise, when `+0x176` bit 2 is set, `+0x170` bit 0 is clear,
and either `+0x3C` bit 3, `+0x170` bit 1 or the goal `+0x20` is beyond `+0x110 + +0xA4 + 5` away, a
reachable random detour (`0x00334E00`) claims the step with bit 10 set, the countdown cleared and
speed 0.

`0x00334E00(ctx, out)`: for a goal of kind 1 it searches around the target position `+0x40` at
`radius + target radius + 0.1`. For any other goal it first tests the goal `+0x20` itself
(`0x003377C0`): on the mesh it returns the goal, or the position with result 0 when within 0.1, with
no random draw; only an off-mesh goal starts the search around it at `+0xAC - 0.1`.

The search
tries eight directions, two rounds of four at right angles from a random start (`rand() % 360`
degrees), keeping the first that is on the mesh and reachable (`0x0033D3E0` not 1); it falls back
to the unit's own position with result 0.

`0x0033E1F0` re-rolls the step scale `+0x108` to `2.5 + (rand() % 100) / 100` for a definition mode
2 unit, clears the mode and countdown (the orbit bit stays), sets `+0x10` to 256.0, zeroes the
counters, puts `rand() % 3 & 1` into the low nibble of `+0x38`, and in `+0x3C` clears bits 0-2,
sets bit 3 to `rand() % 10 == 0` (a one in ten draw) and sets bit 8.

`0x0033C200(ctx)` runs for a leader under order `0x4124` or `0x4022` with a battle in progress
(`0x002F8E70() & 7`): `0x0033BD70` and `0x0033C310` can claim the step; otherwise, with the leader not
animating a move (`0x00265830` = 0), the remaining path distance `0x00334950` (the sum of the route's
remaining legs from the unit's region) is compared with the stored `+0x10`: a drop of over 0.01
re-stores it and zeroes the counter `+0x14`, a rise past it plus 1.5 re-stores it, anything else
counts up to 60; when `0x0033C310` returned 2 the step is then claimed as well.

`0x0033BD70` fires at 60: with the goal at least 20 units away and no action running, it samples the
route at 1, 2, ... 20 units ahead (`0x003347C0`) and takes the first point on the mesh as a detour
(`+0xCC` bit 7, `+0x50`).

`0x0033C310` runs under the same order gate (`0x4124`, or `0x4022` while fleeing) with the
leader present and not animating a move and the remaining route under 6 units. When the unit's
actor is active (`0x002EA7F0`) it lists the actors in the corridor (`0x00391D10` for a point,
`0x003920F0` for a segment, 32 at most) and with any candidate or blocker among them zeroes the
speed and returns 1.

With none, and the stall counter under 60, it aims a point `+0xAC + 0.1`
ahead along the last move (from block `+0x18`/`+0x1C`); when that direction differs from the
current heading by over 5 degrees, is reachable (`0x0033D3E0` not 1) and on walkable terrain
(`0x0026E100`), the desired heading takes the byte `+0x2C`, `+0xBC` the approach helper's result,
the countdown is cleared and 2 is returned, else 0. With the counter at 60 it zeroes the speed
and returns 1.

### Finalising the step

`0x0033BFB0(ctx)` handles a unit whose flags `+0x170` have bit 9: when the angle between the
block's `+0x140` direction and the step exceeds 135 degrees, it probes the heading stored as a
byte at block `+0x2C` (`byte * pi / 128`) and, when clear and `+0x21` bit 0 set, takes that
heading with the rate `+0xE8` and clears the countdown. Otherwise it stores the desired heading as
that byte, `(wrap(h) * 128 / pi)`, 0-256 wrapped, and sets `+0x21` bit 0.

`0x0033BC80(ctx, point)` is the ground check for class 3 against a non-class-3 target: it probes the
terrain height under the point (`0x003208C0`), floors it at the target's y (`+0x44`), and when
`probed + +0xC0 - unit y` (the step scale is added, as the code has it) is 0.3 or more in
magnitude sets the pitch to `+-pi/2` by its sign and the speed to `+0xE8`.

### The corridor probes

Five predicates test a step. Every non-zero exit returns a literal small integer:

| Probe | Returns |
|---|---|
| `0x0033D3E0(A, B, class)` (the straight walk) | 0 when `A` is off the mesh or the walk reaches `B`'s region through portals open to `class` (`0x0026E300` 1, or 0 with the mask bit) and the segment crosses each portal (`0x00468880`); 1 when `B` is off the mesh or a region has no crossable portal: blocked |
| `0x00335E50(A, B, w, class)` (the width walk) | 1 when the walk offset by `+w`, the walk offset by `-w`, or the lateral segment across `B` from `+w` to `-w` is blocked |
| `0x00335B60(ctx, angle, pitch, distance, tolerance, flags)` (forward step clearance) | 0 at once for a zero distance; otherwise 0 usable; 1 rejected by the obstruction query returning 1, the mode-3 segment test `0x00318CA0`, the width walk at `0.9 * +0x10C` (or the straight walk with flags bit 3), the grid query `0x00391410`, or the terrain test `0x0026E100`; 2 only when the obstruction query returned 2 |
| `0x003357B0(A, B, radius, unit, exclude, flags)` (dynamic obstruction) | 0 at once unless `flags` bit 5 is set or the asker's actor is active (`0x002EA7F0`); otherwise 0 nothing in the corridor; 1 a candidate accepted as blocking; 2 candidates counted but none blocking. The candidates come from the grid's actor list (`0x00391D10` for a point, `0x003920F0(..., 32, ~(flags >> 4) & 8 \| 0x14)` for a segment, at most 32); a unit of definition mode 1 against a mode-4 asker, the excluded unit and the asker itself are skipped; the rest pass the kind filters of `flags` bits 1-4 and 6, then `0x00314EB0` and `0x00313F80` decide blocking (results 1-3 count as candidates, others as blockers) |
| `0x0033A3D0(A, B)` (path width) | 1 when the walk `B` to `A` is clear, or when a half-way lateral detour at `+-45` degrees is fully clear; 0 only when the direct walk and both detours have a blocked leg |
| `0x00335F90(ctx)` (corridor blocked) | 1 when the width walk at `0.9 * +0x10C`, the straight walk, or, for class 3, the segment test blocks; else 0 |

The probes read the mover class `+0x174` afresh at each test. The forward clearance clamps its
tolerance to `[0.2, 0.8]` (callers hand in 0.8) and divides the distance by `cos(pitch)` for a
non-zero pitch; callers hand in distances of 0.1 or 1.0.

### The order goal decoder

`0x00312730(unit, order, outTarget, outGoal, outReach)` turns an order word at `+0x714` into a goal:
`0x4000`-`0x401F` index `0x00312DF0` with the order's parameter word; `0x4020` uses the spawn record's
`+0x50` for a kind-1 unit; `0x4022` the leader's `+0x120` and the target's `+0xD0` for a kind-0
unit; `0x4023` the target of `+0x710` with the parameter as reach; `0x4024` the party leader;
`0x4026`-`0x4035` the unit of definition selector `order - 0x4026` (`0x002367A0`).

`0x4124`, `0x4125`, `0x414A`, `0x414E` and `0x4165` are five higher sources; `0x4021`, `0x4025` and
everything else reject. The reach returned is the larger of the actor's radii plus the target's
where one exists; for `0x4022` it is `0x00309B10(unit)`, the unit's larger radius plus 0.1, plus
`0x00309A90()`. `0x00312DF0` draws random points until `0x00317DE0(unit, point, flag)` accepts one: it
tests a copy of the point with `0x00337700` (no shaped obstacle at the point, on the mesh, and walkable
at the unit's larger radius for its mover class `+0x1F4`, `0x00336390`) or, with the flag, `0x003377C0`.

## Layouts

```
locomotion block (unit +0x80; the solver's "state" and "flag block" are the same record)
+0x00   u32  flag word: bits 0-4 steering mode, 5-14 countdown, 15 orbit direction
+0x04   f32  orbit radius   +0x10 f32 stored path distance   +0x14 u8 stall counter (60)   +0x18/+0x1C f32 last solve x, z
+0x21   u8   bit 0 heading byte valid; bits 1-2 last turn direction
+0x2C   u8   heading as byte * pi/128
+0x38   u32  bit 1 too far, bit 2 within reach, bit 3 turning, bits 6-7 detour side
+0x3C   u32  bit 0 fast latch, bit 3 detour pending, bits 4-7 attempt counter
+0x40   i32  goal kind (1 unit, 2 unit with margin)
+0x60 .. +0x90  f32[4] x4  the four positions the context copies
+0xD0   f32  stop radius   +0xD8 f32 speed   +0xDC f32 desired heading   +0xF4 f32 pitch   +0xE0 f32 current heading
+0xE4   f32  turn rate moving        +0xE8 f32 turn rate standing
+0xEC   f32  slow turn rate          +0xF0 f32 fast turn rate
+0xF8   f32  speedA                  +0xFC f32 speedB     +0x104 f32 speed threshold
+0x108  f32  step scale (2.0 floor)  +0x10C/+0x110 f32 collision radii   +0x118 f32 heading cap
+0x120/+0x124/+0x128  f32 reach values     +0x12C f32 orbit length    +0x130 i32 sidestep odds
+0x140  f32[3] direction             +0x150 u32 target handle   +0x160 i32 goal kind
+0x170  u32  flags (unit +0x1F0): bit 0 speedA, bit 1 speedB, bits 2-4 the fast-latch condition, bit 9
+0x174  u8   mover class (unit +0x1F4)   +0x176 u8 bit 2 detours allowed   +0x177 u8 slot

solver context (stack, 0x110 bytes)
+0x00 position (block +0x60)  +0x10 step point (+0x70)  +0x20 route goal (+0x80)
+0x30 destination (+0x90; the step and spacing distances)  +0x40 target position  +0x50 detour point  +0x60 leader position
+0xA0 radius  +0xA4 target radius  +0xA8 target bearing  +0xAC stop distance
+0xB0 speed out  +0xB4 desired heading  +0xB8 pitch  +0xBC limited heading
+0xC0 step scale  +0xC8 distance to the route goal, or to the target  +0xCC flags copy (bit 7, bit 10 detour)  +0xD0 bit 0 leader reachable
+0xE0 target actor  +0xE8 leader actor  +0xF0 unit  +0xF8 target unit  +0x100 / +0x108 the block
```

## Shipped data

| Constant | Value | Role |
|---|---|---|
| `0.785398`, `2.0944`, `0.349066` | 45, 120, 20 degrees | the turn limiter's entry, escalation and release |
| `1.0471976`, `2.617994`, `2.3561945` | 60, 150, 135 degrees | the mode 1 easing band, the detour and finalise thresholds |
| 7, 5, 3, 1.5, 0.25 | the arrival divisors | by class, goal and the fleeing state |
| 0.99 | the overshoot guard | |
| 60 | frames | the stall counter's limit |
| 5.0 (`0x009146E4`), 0.5 (`0x01CEBB70`), 3.0 (`0x008F311C`) | | the detour range and the pair margins |
| `0x3FB4FDF4` = 1.414 | | the navigation radius factor |
| `move_support` (`0x02EBF010`) | 120 rows; caps 1.5 (6 rows), 2.0 (102), 2.5 (12); one narrow row (map 311); map 290 listed twice, the first row (1.5) wins; every row is in [move-support.tsv](move-support.tsv) (`Database/Tools/catalogues/move_support.py`) | the heading search field row |
| `0x01EED4C0`, by byte `+0x175` | 0: above 120 degrees mode 3, below 90 (45 in the fast band) mode 2, else 1; 1: always 1; 2 and 4: always 2; 3: above 45 mode 3, else 2; 5: below 30 mode 1, else 2; 6: above 0.01 rad mode 3, else 2; 7: 2, or 1 in the slow band; the halves for flag bit 3 are identical | the steering mode table |

## Operations

Each navigation step: route, follow, refresh the three latch bits, solve. The solver builds its
context, picks its variant, computes the step distance, runs the recoveries, then either the
spacing pass or the heading constraint or the running steering mode, and finalises. The results go
back into the block and the unit, and the movement step page's driver turns them into motion.

## State

The locomotion block's flag word, headings, rates, counters and reach values; the context is
rebuilt every step. Three recovery bodies draw from the C runtime `rand()` (IAT `0x008C3098`), the
process-wide stream, so a detour is not reproducible from the game's own generators.

## Modding notes

- The step is quadratic in the remaining distance; the seven constants are one curve with a
  divisor, not seven speeds. Keep the `0.99` guard or units overshoot.
- The limiter is history-dependent: the same error turns fast or slow depending on whether the
  unit passed through 120 degrees. The fast rate also needs the three latch bits.
- Keep the direction pair mutually exclusive and the snap-on-arrival; a port that steps by the
  rate unconditionally orbits the target.
- Avoidance and detours use the CRT generator; two machines running the same battle pick
  different sidesteps, and nothing short of replacing the draw changes that.
- The stack arguments of the forward clearance and obstruction probes are at the callee's
  `+0x28`/`+0x30`; every non-zero result is a literal 1 or 2, never a probe's own value.
- The mode byte is re-read inside the probes; a port that caches it once is not equivalent.

## Related

- [Navigation mesh and pathfinding](navigation-mesh-and-pathfinding.md): the route and the obstacle grid.
- [Movement step](heading-speed-to-position-delta.md): the driver that moves the unit.
- [Battle unit fields](../Characters-And-Objects/battle-unit-fields.md): the locomotion block in the unit.
- [Battle orders](../Battle-Actions/battle-orders.md): the order ids the decoder reads.
- [Random number generators](../Random-Numbers/random-number-generators.md): the CRT stream.
