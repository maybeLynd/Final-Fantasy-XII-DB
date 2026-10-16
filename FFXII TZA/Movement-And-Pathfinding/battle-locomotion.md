---
title: "Battle locomotion: how a combat unit picks its step and heading, the turn limiter, spacing and avoidance, detour and stall recovery, and the corridor probes"
kind: "system"
category: "Movement and pathfinding"
summary: "The solver that moves a battle unit each step: the navigation step that routes it and builds the solver context, the two solver variants chosen by the unit's definition, the quadratic arrival curve that sets the step distance, the heading turn limiter with its three angles and two rates, the six steering modes a countdown runs, the spacing and avoidance pass with its randomised manoeuvre, the detour and stall recoveries, the corridor probes that test a step against moving units, walls and the obstacle grid, the order goal decoder, and what the solver writes back."
addresses: ["00325BB0", "00336CE0", "00336710", "003394A0", "0033BED0", "00339BF0", "003364D0", "0033CB70", "00334120", "0033A570", "00338140", "0033D660", "003343D0", "0033C870", "00334E00", "0033E1F0", "0033C200", "0033BD70", "00334950", "003347C0", "0033C310", "0033BFB0", "00339F00", "0033CEF0", "0033D200", "0033CE60", "0033CDE0", "0033BAA0", "0033BC80", "00334AB0", "00334C30", "00335B60", "003357B0", "0033D3E0", "00335E50", "0033A3D0", "00335F90", "00391410", "00312730", "00253B90", "0030A130"]
---

# Battle locomotion: how a combat unit picks its step and heading, the turn limiter, spacing and avoidance, detour and stall recovery, and the corridor probes

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

Combat asks for movement; the movement system does not act on its own. `00325BB0(unit)` runs from
four combat sites (`002FDBE9`, `002FDD69`, `00304D5B`, `00308341`): it routes the unit across the
mesh and follows the route to the next waypoint ([navigation mesh and
pathfinding](navigation-mesh-and-pathfinding.md)), refreshes the locomotion flags, and hands the
locomotion block at unit `+0x80` to the solver `00336CE0(block, block)`.

The solver writes its results back: the block's `+0xD8` from the context's speed `+0xB0`; `+0xDC`,
`+0xF4` and `+0xE0` from the desired heading, pitch and limited heading `+0xB4`-`+0xBC`; `+0x170`
from the flags copy `+0xCC`; `+0xC0`-`+0xC8` from the detour point `+0x50`-`+0x58` (written by
`0033C870` and `0033BD70`); and the block's `+0x18`/`+0x1C` from the context's x and z (`+0x00`,
`+0x08`), the position at this solve.

### The solver context

`00336710(ctx, block, 1)` fills a working context from the block: four positions at `+0x60`,
`+0x70`, `+0x80` and `+0x90` into `ctx + 0x00`, `+0x10`, `+0x20` and `+0x30` with `w` = 1.0; the
larger collision radius `max(+0x10C, +0x110)` at `+0xA0`; the three heading floats `+0xDC`, `+0xF4`,
`+0xE0` at `+0xB4`, `+0xB8`, `+0xBC`; the unit from the slot byte `+0x177` (`00236820`) at `+0xF0`
and its actor handle's record at `+0xD8`; the flags `+0x170` at `+0xCC`; the step scale `+0x108`
at `+0xC0`, raised to 2.0 below 2.0 unless the unit's definition byte `+0x18` has mode 2.

It also stores the party leader's actor at `+0xE8` and its position at `+0x60`, and the distance
to the goal at `+0xC8`.

When the goal kind `+0x160` is 3, or `+0x40` is 1 or 2, the target unit of the handle `+0x150`
(`0031B7E0`, `003588B0`) is stored at `+0xF8`/`+0xE0`, its position at `+0x40`, its radius at
`+0xA4`, its bearing at `+0xA8` and the distance to it at `+0xC8`. The stop distance `+0xAC` is
`radius + targetRadius + 0.1` when `+0x40` is 1, else the block's `+0xD0`.

For a unit with order
`0x4124`, or `0x4022` while the party is fleeing (`00253B90` non-zero, [force fight mode](../Engine-Core/force-fight-mode.md)), `0033D3E0(ctx, leader, 1)`
sets `+0xD0` bit 0 when it does not return 1: the leader is reachable in a straight walk.

### Which solver runs

`00336CE0` reads the unit's definition record `[unit + 0xE68]` byte `+0x18` bits 1-3: mode 1 and 3
return without solving, mode 2 runs the class solver `003394A0`, anything else the default solver
`0033BED0`.

The class solver: with the goal kind `+0x40` non-zero it stops (`+0xB0` = 0) and only limits the
heading toward the goal; otherwise it takes the step distance, and when the unit is
over 16 units from field point 8 (`00320940(8)`) with `ctx + 0x04` below 5.7 it stops with a
pitch of `pi/2`; else it faces the goal `+0x20` (`0033CEF0`) and takes the pitch toward the step point `+0x10`
raised by `+0xC0 + 3.2` (`00468700`).

### The default solver

`0033BED0(ctx)`: when `00336040()` is 0 it zeroes the speed and runs `00469A50` on the unit pair.
Otherwise it sets the speed `+0xB0` from the step distance, clears `+0xCC` bit 7, and runs in order
the detour recovery `0033C870` and the stall recovery `0033C200`; when neither claims the step and
the flag word's countdown bits (`0x7FE0`) are clear, it runs the spacing pass `00338140` for goal
kind 1 or the heading constraint `0033A570` otherwise; with a countdown running it runs the
steering dispatcher `00339F00` instead.

Those three paths end in `0033BFB0`; a step claimed by
`0033C870` or `0033C200`, and the `00336040` = 0 path, return without it.

### The step distance

`00339BF0(ctx)` is a quadratic arrival curve on the horizontal distance `d` to the destination `+0x30` (block `+0x90`;
`004686D0` ignores y):

```
party unit (kind 0) with order 0x4022 while fighting (00253B90 zero) : return speedB (+0xFC)
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
creeps in. The force-fight predicate `00253B90` is reached through the thunk `0030C0D0`.

### The turn limiter

`003364D0(ctx, desired)` limits the heading `+0xE0` of the block. With `a = |wrap(cur - desired)|`
(`0033CB70`): above 45 degrees (`0.785398`) it raises the turning flag (block `+0x38` bit 3), and
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
error produces different behaviour depending on history. `0033CB70` normalises by repeated `2pi`
steps within `+-4pi` and leaves larger values alone; `00334120(cur, target, rate)` is the
approach helper the modes use: snap within the rate, else step by it and wrap.

### The steering modes

The block's flag word `+0x00` carries the mode in bits 0-4, a countdown in bits 5-14 and the orbit
direction in bit 15. `00339F00(ctx)` runs while the countdown is non-zero: it projects the step
point `+0x10` from the target `+0x40` back by `+0x110 + +0xA4 + 0.1` (the block's second collision
radius plus the target radius) along the heading, takes the
pitch toward it for class 3 (0 otherwise), dispatches on the mode, clears the countdown when the
speed exceeds the distance to that point, and otherwise counts it down by one.

| Mode | Body | What it does |
|---|---|---|
| 1, 4 | `0033CEF0` | turn while moving: the rate is `+0xE4` above the speed threshold `+0x104`, else `+0xE8`; below 60 degrees the rate eases by `(1 - cos(3a)) / 2` toward one degree; the limited heading `+0xBC` follows the target by the rate, or snaps to the current heading when the distance is under `speedB`; past `speedA * a / +0xE8` the desired heading `+0xB4` is also capped by `+0x118`; arms a countdown of 6, or 5 with force-fight on for a unit under order `0x4022` whose definition record `[+0x698]` has byte `+5` zero |
| 2 | `0033D200` | when `00334220` allows, a straight approach by the rate and returns 5; else the rate scales by `20 + 80 * a / 45deg` percent inside 45 degrees, snaps to the current heading within `5 * speedA`, arms a countdown of 10 |
| 3 | `0033CE60` | stop and turn: speed 0, both headings approach the target by the slow rate `+0xEC`, countdown 10, cleared on arrival |
| 5 | `0033CDE0` | turn while moving at `+0xE4` or `+0xE8` without stopping |
| 6 | `0033BAA0` | orbit: the orbit heading `00334AB0` is probed (`00335B60(ctx, heading, 0, 1.0, 0.8, 0)`); when the probe rejects and the pair clearance `0033D660` returns 0, the countdown is cleared and the speed zeroed; else `+0xB4` takes the orbit heading, the pitch 0, the speed `speedA`, `0033BC80` runs on the point 0.1 ahead, and the limited heading `+0xBC` approaches the target bearing `+0xA8` by `1.5 * (speedA / circumference) * 2pi` |

### Spacing and avoidance

`00338140(ctx)`, for goal kind 1: when the target is the unit itself, or the distance to the target
position `+0x40` is under 0.1, it stops and clears the countdown.

Otherwise, with `D` the distance
to the destination `+0x30`, it sets block `+0x38` bit 1 when `D` exceeds `min(+0x124 + 2, +0x128)`,
bit 2 when `D` is within `reach + 0.05` (reach = `+0x120`, or the target's own `+0x1A0` when the
target's target is this unit and its `+0x1A4` is below `+0x124`) and `003341A0` holds, clears bit
1 inside the stop radius `+0xD0` and bit 2 outside it, and sets bit 1 when the pair clearance
`0033D660` returns 0.

Then:

- bit 1: `00337A50`, the heading constraint `0033A720`, and the countdown cleared on success;
- bit 2: the bearing from the step point back to the position (away from it) is probed with
  `00335B60(ctx, bearing, 0, 0.1, 0.8, 0)`; when clear the speed is `speedA`, `+0xB4` that reverse
  bearing and `+0xBC` the limiter's result for the forward bearing; else bit 2 is cleared;
- neither: the randomised manoeuvre `003343D0`, then `0033BAA0` when it starts;
- with neither bit and no countdown: speed 0, the limiter, and `0033BC80`.

`0033D660(ctx, a, b)` is the pair clearance: with both radii from `00265090` it takes
`b.+0x1A8 - (ra + rb)`, halved for a party unit and divided by 3 otherwise, and returns 1 when the
distance to `b` is below `+0x1A8` and either unit's definition byte `+0x12` is negative, or
`00334C90` is at most that margin, and the raised segment between them (`00318CA0`) returns below 2.

`003343D0(ctx)` starts a sidestep:

1. it refuses when the target unit is the unit itself, the distance to the target is within
   `+0xA0`, the mode is 6, the odds `+0x130` are -1, or the unit (`00335760`) is not engaged and
   not under order `0x96`; after the angle tests it also refuses while the turning flag (block
   `+0x38` bit 3) is set;
2. `003357B0` is asked about the corridor to the target; the odds halve when it reports blockers;
   `rand() % odds` must be 0;
3. the target must lie within 120 degrees of the actor's facing and the actor within 45 degrees of
   its heading;
4. a `rand()` bit picks the side (flag bit 15); `00335B60` probes `00334AB0`'s orbit heading, the
   other side on failure, and both failing refuses;
5. otherwise the countdown is set to `+0x12C / 00334C30` quarter turns (halved for `0031EA90`
   class 4), the mode to 6, and the orbit radius `+0x04` to the current distance plus or minus
   `(rand() % 5 + 5) / 100`.

### Detour and stall recovery

`0033C870(ctx)`: with `+0xCC` bit 10 set it finishes a detour: `00334E00` picks the point into
`+0x50`, for goal kind 1 the limited heading `+0xBC` takes the bearing from that point to the
target, bit 10 becomes bit 7, `0033E1F0` resets the avoidance state, block `+0x3C` bit 3 is
cleared, and the step is claimed. Otherwise, when `+0x176` bit 2 is set, `+0x170` bit 0 is clear,
and either `+0x3C` bit 3, `+0x170` bit 1 or the goal `+0x20` is beyond `+0x110 + +0xA4 + 5` away, a
reachable random detour (`00334E00`) claims the step with bit 10 set, the countdown cleared and
speed 0.

`00334E00(ctx, out)`: for a goal of kind 1 it searches around the target position `+0x40` at
`radius + target radius + 0.1`. For any other goal it first tests the goal `+0x20` itself
(`003377C0`): on the mesh it returns the goal, or the position with result 0 when within 0.1, with
no random draw; only an off-mesh goal starts the search around it at `+0xAC - 0.1`.

The search
tries eight directions, two rounds of four at right angles from a random start (`rand() % 360`
degrees), keeping the first that is on the mesh and reachable (`0033D3E0` not 1); it falls back
to the unit's own position with result 0.

`0033E1F0` re-rolls the step scale `+0x108` to `2.5 + (rand() % 100) / 100` for a definition mode
2 unit, clears the mode and countdown (the orbit bit stays), sets `+0x10` to 256.0, zeroes the
counters, puts `rand() % 3 & 1` into the low nibble of `+0x38`, and in `+0x3C` clears bits 0-2,
sets bit 3 to `rand() % 10 == 0` (a one in ten draw) and sets bit 8.

`0033C200(ctx)` runs for a leader under order `0x4124` or `0x4022` with a battle in progress
(`002F8E70() & 7`): `0033BD70` and `0033C310` can claim the step; otherwise, with the leader not
animating a move (`00265830` = 0), the remaining path distance `00334950` (the sum of the route's
remaining legs from the unit's region) is compared with the stored `+0x10`: a drop of over 0.01
re-stores it and zeroes the counter `+0x14`, a rise past it plus 1.5 re-stores it, anything else
counts up to 60; when `0033C310` returned 2 the step is then claimed as well.

`0033BD70` fires at 60: with the goal at least 20 units away and no action running, it samples the
route at 1, 2, ... 20 units ahead (`003347C0`) and takes the first point on the mesh as a detour
(`+0xCC` bit 7, `+0x50`).

`0033C310` runs under the same order gate (`0x4124`, or `0x4022` while fleeing) with the
leader present and not animating a move and the remaining route under 6 units. When the unit's
actor is active (`002EA7F0`) it lists the actors in the corridor (`00391D10` for a point,
`003920F0` for a segment, 32 at most) and with any candidate or blocker among them zeroes the
speed and returns 1.

With none, and the stall counter under 60, it aims a point `+0xAC + 0.1`
ahead along the last move (from block `+0x18`/`+0x1C`); when that direction differs from the
current heading by over 5 degrees, is reachable (`0033D3E0` not 1) and on walkable terrain
(`0026E100`), the desired heading takes the byte `+0x2C`, `+0xBC` the approach helper's result,
the countdown is cleared and 2 is returned, else 0. With the counter at 60 it zeroes the speed
and returns 1.

### Finalising the step

`0033BFB0(ctx)` handles a unit whose flags `+0x170` have bit 9: when the angle between the
block's `+0x140` direction and the step exceeds 135 degrees, it probes the heading stored as a
byte at block `+0x2C` (`byte * pi / 128`) and, when clear and `+0x21` bit 0 set, takes that
heading with the rate `+0xE8` and clears the countdown. Otherwise it stores the desired heading as
that byte, `(wrap(h) * 128 / pi)`, 0-256 wrapped, and sets `+0x21` bit 0.

`0033BC80(ctx, point)` is the ground check for class 3 against a non-class-3 target: it probes the
terrain height under the point (`003208C0`), floors it at the target's y (`+0x44`), and when
`probed + +0xC0 - unit y` (the step scale is added, as the code has it) is 0.3 or more in
magnitude sets the pitch to `+-pi/2` by its sign and the speed to `+0xE8`.

### The corridor probes

Five predicates test a step. Every non-zero exit returns a literal small integer:

| Probe | Returns |
|---|---|
| `0033D3E0(A, B, class)` (the straight walk) | 0 when `A` is off the mesh or the walk reaches `B`'s region through portals open to `class` (`0026E300` 1, or 0 with the mask bit) and the segment crosses each portal (`00468880`); 1 when `B` is off the mesh or a region has no crossable portal: blocked |
| `00335E50(A, B, w, class)` (the width walk) | 1 when the walk offset by `+w`, the walk offset by `-w`, or the lateral segment across `B` from `+w` to `-w` is blocked |
| `00335B60(ctx, angle, pitch, distance, tolerance, flags)` (forward step clearance) | 0 at once for a zero distance; otherwise 0 usable; 1 rejected by the obstruction query returning 1, the mode-3 segment test `00318CA0`, the width walk at `0.9 * +0x10C` (or the straight walk with flags bit 3), the grid query `00391410`, or the terrain test `0026E100`; 2 only when the obstruction query returned 2 |
| `003357B0(A, B, radius, unit, exclude, flags)` (dynamic obstruction) | 0 at once unless `flags` bit 5 is set or the asker's actor is active (`002EA7F0`); otherwise 0 nothing in the corridor; 1 a candidate accepted as blocking; 2 candidates counted but none blocking. The candidates come from the grid's actor list (`00391D10` for a point, `003920F0(..., 32, ~(flags >> 4) & 8 | 0x14)` for a segment, at most 32); a unit of definition mode 1 against a mode-4 asker, the excluded unit and the asker itself are skipped; the rest pass the kind filters of `flags` bits 1-4 and 6, then `00314EB0` and `00313F80` decide blocking (results 1-3 count as candidates, others as blockers) |
| `0033A3D0(A, B)` (path width) | 1 when the walk `B` to `A` is clear, or when a half-way lateral detour at `+-45` degrees is fully clear; 0 only when the direct walk and both detours have a blocked leg |
| `00335F90(ctx)` (corridor blocked) | 1 when the width walk at `0.9 * +0x10C`, the straight walk, or, for class 3, the segment test blocks; else 0 |

The probes read the mover class `+0x174` afresh at each test. The forward clearance clamps its
tolerance to `[0.2, 0.8]` (callers hand in 0.8) and divides the distance by `cos(pitch)` for a
non-zero pitch; callers hand in distances of 0.1 or 1.0.

### The order goal decoder

`00312730(unit, order, outTarget, outGoal, outReach)` turns an order word at `+0x714` into a goal:
`0x4000`-`0x401F` index `00312DF0` with the order's parameter word; `0x4020` uses the spawn record's
`+0x50` for a kind-1 unit; `0x4022` the leader's `+0x120` and the target's `+0xD0` for a kind-0
unit; `0x4023` the target of `+0x710` with the parameter as reach; `0x4024` the party leader;
`0x4026`-`0x4035` the unit of definition selector `order - 0x4026` (`002367A0`).

`0x4124`, `0x4125`, `0x414A`, `0x414E` and `0x4165` are five higher sources; `0x4021`, `0x4025` and
everything else reject. The reach returned is the larger of the actor's radii plus the target's
where one exists.

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
| 5.0 (`009146E4`), 0.5 (`01CEBB70`), 3.0 (`008F311C`) | | the detour range and the pair margins |
| `0x3FB4FDF4` = 1.414 | | the navigation radius factor |

## Operations

Each navigation step: route, follow, refresh the three latch bits, solve. The solver builds its
context, picks its variant, computes the step distance, runs the recoveries, then either the
spacing pass or the heading constraint or the running steering mode, and finalises. The results go
back into the block and the unit, and the movement step page's driver turns them into motion.

## State

The locomotion block's flag word, headings, rates, counters and reach values; the context is
rebuilt every step. Three recovery bodies draw from the C runtime `rand()` (IAT `008C3098`), the
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
