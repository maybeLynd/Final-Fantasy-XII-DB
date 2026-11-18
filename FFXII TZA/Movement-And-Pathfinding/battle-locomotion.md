[Home](../../README.md) / [Movement and pathfinding](README.md) / Battle locomotion

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Battle locomotion: how a combat unit picks its step and heading, the turn limiter, spacing and avoidance, detour and stall recovery, and the corridor probes | system | Movement and pathfinding | How actors move | The solver that moves a battle unit each step: the navigation step that routes it and builds the solver context, the two solver variants chosen by the unit's definition, the quadratic arrival curve that sets the step distance, the heading turn limiter with its three angles and two rates, the six steering modes a countdown runs, the spacing and avoidance pass with its randomised manoeuvre, the detour and stall recoveries, the corridor probes that test a step against moving units, walls and the obstacle grid, the order goal decoder, and what the solver writes back. | 0x00325BB0, 0x0033A720, 0x00339DF0, 0x0033B6F0, 0x00337470, 0x00335180, 0x0033CC80, 0x0033A240, 0x0033D890, 0x00337C10, 0x00336CE0, 0x00336710, 0x003394A0, 0x0033BED0, 0x00339BF0, 0x003364D0, 0x0033CB70, 0x00334120, 0x0033A570, 0x00338140, 0x0033D660, 0x003343D0, 0x0033C870, 0x00334E00, 0x0033E1F0, 0x0033C200, 0x0033BD70, 0x00334950, 0x003347C0, 0x0033C310, 0x0033BFB0, 0x00339F00, 0x0033CEF0, 0x0033D200, 0x0033CE60, 0x0033CDE0, 0x0033BAA0, 0x0033BC80, 0x00334AB0, 0x00334C30, 0x00335B60, 0x003357B0, 0x0033D3E0, 0x00335E50, 0x0033A3D0, 0x00335F90, 0x00391410, 0x00312730, 0x00253B90, 0x0030A130 |

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

The order a unit is carrying out sets its goal. Depending on the order, the goal is a randomly drawn walkable point,
the position kept in its spawn record, the party leader, its current target, or a unit the order names; some orders
give no goal.

## How it works

### The navigation step

Combat asks for movement; the movement system does not act on its own. `0x00325BB0(unit)` runs from
four combat sites (`0x002FDBE9`, `0x002FDD69`, `0x00304D5B`, `0x00308341`): it routes the unit across the
mesh and follows the route to the next waypoint ([navigation mesh and
pathfinding](navigation-mesh-and-pathfinding.md)), refreshes the locomotion flags, and hands the
locomotion block at unit `+0x80` to the solver `0x00336CE0(block, block)`.

When `0x00325D90(unit)` returns 0 it does none of this: it runs `0x0033C9B0(block)` and returns 1
(`0x00325BD7`-`0x00325BE1`). When the route search `0x00383620` returns non-zero, the step calls `0x0016D6A0` on the
unit's `+0x698` record and returns 0 before the waypoint step and the solver (`0x00325C29`-`0x00325C3C`). After the
solver, block flag bit `0x400` (`+0x170`) zeroes the block's `+0xD8` and runs `0x00313500`, and flag bit `0x80`
zeroes `+0xD8`, clears itself and calls `0x003003F0` (`0x00325D0F`-`0x00325D5C`).

`0x00325D90(unit)` answers 0 when the unit's dword `+0x1F0` has bit `0x1000` or `0x2000`; when the dwords `+0x3C` and
`+0x64` of the record `+0x698`, taken together, have a bit of `0x8000401B`; when the unit's dword `+0x60` is `0x2006`,
`0x2037` or `0x2039` to `0x203C`; when its byte `+0x6B7` is not 0; or when the object at its `+0x708` exists and bit
`0x4` of that object's byte `+0x04` is set (`0x00325D96`-`0x00325DF8`). The record pointer `+0x698` is read with no null
test.

Past those it answers 1 when `0x003590D0()` is not the unit's dword `+0x08`, when the same two record dwords have a bit
of `0x08000020`, or when the unit's word `+0x714` is `0x414E`. Otherwise it answers 0 when `0x0030BCD0(unit)` answers 0
or bit `0x40000` of the unit's dword `+0x00` is set, and 1 when neither holds (`0x00325DFA`-`0x00325E50`).

The solver writes its results back: the block's `+0xD8` from the context's speed `+0xB0`; `+0xDC`,
`+0xF4` and `+0xE0` from the desired heading, pitch and limited heading `+0xB4`-`+0xBC`; `+0x170`
from the flags copy `+0xCC`; `+0xC0`-`+0xC8` from the detour point `+0x50`-`+0x58` (written by
`0x0033C870` and `0x0033BD70`); and the block's `+0x18`/`+0x1C` from the context's x and z (`+0x00`,
`+0x08`), the position at this solve.

### The solver context

`0x00336710(ctx, block, t)` fills a working context from the block: four positions at `+0x60`, `+0x70`, `+0x80` and
`+0x90` into `ctx + 0x00`, `+0x10`, `+0x20` and `+0x30` with `w` = 1.0 (`0x00336733`-`0x003367AD`); the block's own
address at both `+0x108` and `+0x100` (`0x003367B4`-`0x003367BB`); the larger collision radius `max(+0x10C, +0x110)` at
`+0xA0`; 0 at the speed `+0xB0`; and the three heading floats `+0xDC`, `+0xF4`, `+0xE0` at `+0xB4`, `+0xB8`, `+0xBC`
(`0x003367C2`-`0x003367FF`).

The unit comes from the slot byte `+0x177`: `0x00236820(slot)` is called twice. The first answer's dword `+0x08`, read
with no null test, goes to `0x0031ABE0(handle)`, whose answer, the actor handle's record, is stored at `+0xD8`
(`0x00336805`-`0x00336819`); the second answer is the unit stored at `+0xF0` (`0x0033684F`-`0x00336869`). Between them the
flags `+0x170` go to `+0xCC`, and `0x00203080(ctx + 0x80, ctx + 0x20, ctx)` and `0x00203080(ctx + 0x70, ctx + 0x10, ctx)`
store the goal minus the position and the step point minus the position (`0x00336820`-`0x0033684A`).

The step scale `+0x108` goes to `+0xC0`; it becomes 2.0 when 2.0 is above it, unless the unit has a definition
`+0xE68` whose byte `+0x18` has mode 2 (`0x00336870`-`0x003368AC`). The builder then clears bit `0x1` of `+0xD0`
(`0x003368B6`).

When `0x003272A0()` answers a unit, the party leader, a second `0x003272A0()` call gives it again (`0x003368C7`); the actor
`+0x10` of that second answer, read with no null test, is stored at `+0xE8`, and the actor's position at `+0x60` with
`0x00265020(actor, ctx + 0x60, ctx + 0x64, ctx + 0x68)` (`0x003368BD`-`0x003368E3`); with no leader it stores 0 at `+0xE8`
(`0x0033693B`).

With a leader, for a unit with order `0x4124`, or `0x4022` while the party is fleeing (`0x0030C0D0()`, a jump to
`0x00253B90`, non-zero; [force fight mode](../Engine-Core/force-fight-mode.md)),
`0x0033D3E0(ctx, ctx + 0x60, 1)` sets `+0xD0` bit `0x1` when it does not return 1: the leader is reachable in a straight
walk (`0x003368E8`-`0x00336932`). The unit `+0xF0` is read there with no null test.

The distance to the goal, `0x004686D0(ctx, ctx + 0x20)`, goes to `+0xC8` (`0x00336942`-`0x0033694E`). The builder then
zeroes the target unit `+0xF8`, the target position `+0x40` and the vector `+0x90`, each with `w` 1.0, and the target
radius `+0xA4` (`0x00336956`-`0x00336984`).

The target is sought only when `t` is 1, and then only when the goal kind `+0x160` is 3 or the block's `+0x40` is 1 or
2 (`0x0033698B`-`0x003369AD`): `0x0031B7E0(handle)` with the block's handle `+0x150` is stored at `+0xF8` and
`0x003588B0(handle)` at `+0xE0` (`0x003369B3`-`0x003369D0`).

With both found, `0x002646C0(actor, ctx + 0x40, ctx + 0x44, ctx + 0x48)` gives the target position;
`0x00203080(ctx + 0x90, ctx, ctx + 0x40)` stores the position minus it; the radius `+0xA4` is the larger of the two
floats of `0x00265090(actor, &a, &b)`; the bearing `+0xA8` is `0x004687F0(v)` with `v` the target position minus the
position; and `+0xC8` becomes `0x004686D0(ctx, ctx + 0x40)` (`0x003369D7`-`0x00336A6D`).

`0x00336710` does not set `a` and `b` before that call, so for a target actor that is not class 3, for which `0x00265090`
writes nothing, the radius is whatever the two stack slots held. The stop distance `+0xAC` is
`[+0xA0] + [+0xA4] + 0.1` when the block's `+0x40` is 1, else the block's `+0xD0` (`0x00336A75`-`0x00336AAA`).

### Which solver runs

`0x00336CE0` reads the unit's definition record `[unit + 0xE68]` byte `+0x18` bits `0xE`: mode 1 and 3
return without solving, mode 2 runs the class solver `0x003394A0`, anything else the default solver
`0x0033BED0`.

A unit without a unit pointer `+0xF0` or without a definition record also gets the default solver (`0x00336D1C`,
`0x00336D28`, `0x00336D56`). Modes 1 and 3 skip the write-back as well, so the block keeps its speed, headings,
flags and detour point from before the call (`0x00336D36`, `0x00336D4D` to `0x00336E1D`).

The class solver: with the goal kind `+0x40` non-zero it stops (`+0xB0` = 0) and only limits the
heading toward the goal (`0x003364D0` into `+0xBC`, `0x003395DF`-`0x0033960F`); otherwise it takes the step distance,
and when the unit is over 16 units from field point 8 (`0x00320940(8)`) with `ctx + 0x04` below 5.7 it keeps that
speed, sets the desired heading `+0xB4` to 0 and the pitch to `pi/2` (`0x0033953B`-`0x00339545`); else it faces the
goal `+0x20` (`0x0033CEF0`) and takes the pitch toward the step point `+0x10` with its height replaced by `+0xC0 +
3.2` (`0x00339588`-`0x003395C4`, `0x00468700`).

The -1 that `0x00320940` returns for a missing entry 8 is not tested (`0x003394E0`); a missing entry leaves its
output, the stack slot `rsp + 0x40`, unwritten (`0x00320966`-`0x0032097F`), and the distance is then taken from what
that slot holds.

### The default solver

`0x0033BED0(ctx)`: when `0x00336040()` is 0 it calls `0x00469A50([ctx+0xF0], [ctx+0xF8])`, the unit and its target, and
zeroes the speed `+0xB0` (`0x0033BEE4`-`0x0033BF00`).
Otherwise it sets the speed `+0xB0` from the step distance, clears `+0xCC` bit `0x80`, and runs in order
the detour recovery `0x0033C870` and the stall recovery `0x0033C200`; when neither claims the step and
the flag word's countdown bits (`0x7FE0`) are clear, it runs the spacing pass `0x00338140` for goal
kind 1 or the heading constraint `0x0033A570` otherwise; with a countdown running it runs the
steering dispatcher `0x00339F00` instead.

Those three paths end in `0x0033BFB0`; a step claimed by
`0x0033C870` or `0x0033C200`, and the `0x00336040` = 0 path, return without it.

`0x00469A50(a, b)` calls `0x0046AB10(h, m, &context)` and returns what that call leaves in rax: `h` is `0x00320A30(a)`, or 0
for a null `a`, and `m` is `0x0A` when `a` equals what `0x003272A0()` answers, a null `a` against an answer of 0
included, and 8 otherwise. The context is 48 zeroed bytes with `h` at `+0x00`, `0x00320A30(b)` at `+0x08`, 0 for a null
`b`, and at `+0x28` the word `+0x714` of `a` as a dword, 0 for a null `a` (`0x00469A5C`-`0x00469AE0`).

`0x0046AB10` returns at once when that context dword `+0x28` is `0x1FF` or more, a signed test (`0x0046AB19`-`0x0046AB29`);
the order words `0x4124`, `0x4022` and `0x414E` named above are all in that range.

When `0x0033A570` stops the unit (speed `+0xB0` = 0, `0x0033A5F7`) it also turns the limited heading `+0xBC` from
the current heading by the slow rate `+0xEC` (`0x00334120`): for a block goal kind `+0x160` of 1 toward the
bearing from the point the block holds at `+0x150`-`+0x158` to the unit, `0x004687F0` on position minus point
(`0x00203080` at `0x0033A64F`, `0x0033A601`-`0x0033A67D`), for kind 2 toward the angle at `+0x150` itself
(`0x0033A685`-`0x0033A6AB`); any other kind leaves it.

On every path it then compares the limited and desired headings: when `|wrap(+0xBC - +0xB4)|` exceeds `pi/2` it
sets block `+0x3C` bit `0x2`, and bit `0x4` as well when bit `0x2` was already set (`0x0033A6BD`-`0x0033A709`).

### The step distance

`0x00339BF0(ctx)` is a quadratic arrival curve on the horizontal distance `d` to the destination `+0x30` (block `+0x90`;
`0x004686D0` ignores y):

```python
party unit (kind 0) with order 0x4022 while fighting (0x00253B90 zero) : return speedB (+0xFC)
flags +0x170 bit 0x1 : speedA (+0xF8)     bit 0x2 : speedB
goal kind +0x40 == 1, unit +0x768 >= +0x76C, d > stop (+0xD0)    : speedB
rem = max(0, d - stop);  kind 2 also subtracts the actor's smaller radius + 0.5
rem /= 7                      when the mover class +0x174 is 2 or more
rem = dstart / 5 or * 0.25    when ctx +0xD0 bit 0x1, from the distance to +0x60 (fleeing: * 0.25; fighting: / 5)
rem /= 3 or 1.5               otherwise (fleeing: 1.5; fighting: 3)
v = rem * rem * speedB;  speed = clamp(v, speedA, speedB)
speed > d                     : speed = d * 0.99
```

The `0.99` keeps a unit from stepping past its goal; it lands one percent short every frame and
creeps in. The force-fight predicate `0x00253B90` is reached through the thunk `0x0030C0D0`.

### The turn limiter

`0x003364D0(ctx, desired)` limits the heading `+0xE0` of the block. With `a = |wrap(cur - desired)|`
(`0x0033CB70`): above 45 degrees (`0.785398`) it raises the turning flag (block `+0x38` bit `0x8`), and
without that flag it returns the heading unchanged.

- Above 120 degrees (`2.0944`) it latches the fast rate (`+0x3C` bit `0x1`) when `+0x170` has all of
  mask `0x1C`, and steps the heading by the latched rate (`+0xF0` fast, `+0xEC` slow) in the direction the pair
  `+0x21` bits under mask `0x6` recorded, unconditionally; with no direction recorded it steps by the sign of
  the wrapped difference and snaps to `desired` when within the rate.
- The recorded-direction step is not wrapped: bit `0x2` alone adds the rate to the current heading, and any
  other recorded value subtracts it (`0x003365FF`-`0x00336620`).
- Below 20 degrees (`0.349066`) it clears the latch and uses the slow rate; between, it keeps
  whatever is latched. The step snaps to `desired` when within the rate.
- The direction pair is rewritten as clear-then-set, and reaching `desired` clears both the latch
  and the turning flag.
  The pair takes bit `0x2` when the result minus the current heading wraps positive and bit `0x4` otherwise, a
  zero step included (`0x003366AA`-`0x003366DB`); reaching means the result equals `desired` exactly (`0x003366DF`).
- The limited heading is returned in `xmm0`; `0x003364D0` writes no heading itself, and its callers store the
  result (`0x003366F7`).

So the three angles are one hysteresis loop: entry at 45, escalation past 120 only for a unit
whose model authors `@FCP` slot 41, whose flag bit `0x800000` is up and which is mid-cast of something
other than Attack (bits `0x4`, `0x8` and `0x10` of `+0x170`: the navigation step maintains bits `0x8` and
`0x10`, `0x00325CC0`-`0x00325CFD`, and `0x00239E10` sets or clears bit `0x4`, `0x00239F73`-`0x00239F7C`), release inside
20. The same error produces different behaviour depending on history.

`0x0033CB70` normalises by repeated `2pi`
steps within `+-4pi`; beyond that it returns `x - 2pi * trunc(x / 2pi)` once
(`0x0033CBCD`-`0x0033CBE8`), whose magnitude is below `2pi`, apart from the two cases below, but can be above `pi`;
`0x00334120(cur, target, rate)` is the approach helper the modes use: snap within the rate, else step by it and
wrap.

Within `+-4pi` the loops subtract `2pi` while the value is above `pi` and then add it while the value is below
`-pi` (`0x0033CB89`-`0x0033CBC7`). The once-only quotient and product are rounded to single precision, so that result
can land just past 0 or `2pi`: `31.415926` (10pi) gives `-1.9e-6`, and `2224.2476` gives `6.283203`, above `2pi`.
From `|x / 2pi|` of `2^31` up the conversion `cvttss2si` (`0x0033CBD5`) yields `0x80000000`, and the result is `x +
2^31 * 2pi`. A NaN fails every comparison and comes back unchanged (`0x0033CBEC`).

### The steering modes

The block's flag word `+0x00` carries the mode in the bits under mask `0x1F`, a countdown in the bits under mask
`0x7FE0` and the orbit direction in bit `0x8000`.

`0x00339F00(ctx)` runs while the countdown is non-zero. It builds a point from the target `+0x40` and `+0x110 +
+0xA4 + 0.1` (the block's second collision radius plus the target radius) along the vector `{0, 0, 1}` turned
about x by minus the pitch (`0x00339F3E`-`0x00339FAE`), but that point is overwritten before any use (`0x00339FEF`):
the step point `+0x10` becomes the aim point the block keeps at `+0x04`-`+0x0C`, with w 1.0
(`0x00339FB3`-`0x0033A00D`), and the heading handed to the mode bodies is the flat bearing from the position to it
(`0x00339FF9`).

It takes the pitch toward that aim point for class 3 (0 otherwise), dispatches on the mode, clears the countdown
when the speed exceeds the flat distance to the aim point (`0x0033A0AB`-`0x0033A0C5`), and otherwise counts it down
by one. The mode is re-read after each body and tested in the order 1, 2, 3, 4, 6, 5 (`0x0033A039`-`0x0033A09E`);
mode 6 gets no heading argument, and a mode outside 1-6 runs no body.

| Mode | Body | What it does |
|---|---|---|
| 1, 4 | `0x0033CEF0` | turn while moving: the rate is `+0xE4` above the speed threshold `+0x104`, else `+0xE8`; below 60 degrees the rate eases by `(1 - cos(3a)) / 2` toward one degree; the limited heading `+0xBC` follows the target by the rate, or snaps to the current heading when the distance is under `speedB`; past `speedA * a / +0xE8` the desired heading `+0xB4` is also capped by `+0x118`; when no countdown runs (`0x0033D16D`-`0x0033D19F`) arms one of 6, or 5 while the party is fleeing (`0x00253B90` non-zero) for a unit under order `0x4022` whose definition record `[+0x698]` has byte `+5` zero (`0x0033D1A1`-`0x0033D1E1`) |
| 2 | `0x0033D200` | the rate is `+0xE4` when the speed `+0xB0` is above 0 and above the threshold `+0x104`, else `+0xE8` (`0x0033D23A`-`0x0033D277`); when no countdown runs and `0x00334220` allows, a straight approach by the rate and returns 5: `+0xBC` takes one `0x00334120` step from the current heading `+0xE0` toward the target and `+0xB4` the target (`0x0033D27F`-`0x0033D2BA`); else the rate scales by `20 + 80 * a / 45deg` percent inside 45 degrees, with `a = \|wrap(+0xBC - target)\|` (`0x0033D2C7`-`0x0033D312`), snaps to the current heading within `5 * speedA` of the step point `+0x10` (flat distance, `0x0033D321`-`0x0033D340`, `0x0033D392`), and farther out steps the current heading toward the target by that rate, or takes the target within it, storing the result in `+0xBC` and `+0xB4` alike (`0x0033D342`-`0x0033D39E`); a snap leaves `+0xB4` at the target; arms a countdown of 10 when no countdown runs and returns 2 (`0x0033D3A6`-`0x0033D3BB`); the unit it fetches through `0x00236820` (slot byte `+0x177`, `0x0033D235`) is not used |
| 3 | `0x0033CE60` | stop and turn: speed 0 (`0x0033CE7B`), both headings approach the target by the slow rate `+0xEC`: one `0x00334120` step from the current heading `+0xE0` goes to `+0xB4` and `+0xBC` (`0x0033CE8D`-`0x0033CEAA`); countdown 10 when no countdown runs (`0x0033CEB2`-`0x0033CEC5`), cleared on arrival, when the step result equals the target exactly, a countdown already running included (`0x0033CEC7`-`0x0033CED2`) |
| 5 | `0x0033CDE0` | turn while moving at `+0xE4` or `+0xE8` without stopping: `+0xE4` when the speed `+0xB0` is above 0 and above the threshold `+0x104`, else `+0xE8` (`0x0033CDE6`-`0x0033CE2C`); `+0xB4` takes the target and `+0xBC` one `0x00334120` step from the current heading `+0xE0` toward it (`0x0033CE34`-`0x0033CE4E`); the speed, the mode and the countdown are left as they are |
| 6 | `0x0033BAA0` | orbit: the orbit heading `0x00334AB0` is probed (`0x00335B60(ctx, heading, 0, 1.0, 0.8, 0)`); when the probe rejects and the pair clearance `0x0033D660` returns 0, the countdown is cleared and the speed zeroed; else `+0xB4` takes the orbit heading, the pitch 0, the speed `speedA`, `0x0033BC80` runs on the position plus the stack slot `rsp + 0x30`, which `0x0033BAA0` never writes (the 0.1-long forward vector it builds at `rsp + 0x40` is not used, `0x0033BB5E`-`0x0033BBC9`), and the limited heading `+0xBC` approaches the target bearing `+0xA8` by `1.5 * (speedA / circumference) * 2pi`, a rate of 0 when `speedA` exceeds the circumference (`0x0033BC0D`); the pair clearance is `0x0033D660(ctx, unit, target unit)` (`0x0033BB0E`-`0x0033BB1F`) |

### The heading search

`0x0033A720(ctx)` chooses the heading of a step by trying a fan of headings around the bearing to the
step point. The default solver reaches it through `0x0033A570` when the unit is farther than its stop
distance `+0xAC` from the destination `+0x30`, or under order `0x4124` when the straight walk to the
goal is blocked (`0x0033D3E0`); otherwise `0x0033A570` stops the unit. The spacing pass runs it for bit
`0x2`. It works in this order:

1. The field row: the current map (`0x003148F0`) is looked up by its first `u16` in the `move_support`
   table (`0x02EBF010`, [authored data
   tables](../Game-Files-And-Data-Tables/authored-data-tables.md)); the first matching row
   gives a distance cap (byte `+2` / 10) and a narrow-fan flag (byte `+4` bit `0x1`).
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
detour took (block `+0x38` bits under mask `0xC0`: 0 no side, 1 the positive side, 2 the negative side):

| Fan | Side 0 | Side 1 | Side 2 |
|---|---|---|---|
| mover class 0-1, 12 entries | 0, 30, -30, 60, -60, 90, -90, 135, -135, 0, 0, 0 | 0, 30, 60, 90, -30, -60, -90, 135, -135, 0, 0, 0 | 0, -30, -60, -90, 30, 60, 90, -135, 135, 0, 0, 0 |
| the row's narrow flag, 10 entries | 0, 30, -30, 60, -60, 90, -90, 0, 0, 0 | 0, 30, 60, 90, -30, -60, -90, 0, 0, 0 | 0, -30, -60, -90, 30, 60, 90, 0, 0, 0 |
| mover class 2 and up, 7 entries | 0, 45, -45, 90, -90, 135, -135 | 0, 45, 90, -40, -90, 135, -135 | 0, -45, -90, 45, 90, -135, 135 |

Angles are degrees added to the bearing. The -40 in the class-2 side-1 fan is the shipped value
(`0xBF32B8C3`, -0.6981 rad), not -45. A flier tries each heading at the pitches 0, 30 and 45
degrees added to `0x00337470`'s pitch; every other unit at that pitch alone. For each candidate:

1. it is skipped, and that memory consumed, when it lies within 45 degrees of a remembered heading
   (block bytes `+0x2F`/`+0x30`, live while `+0x31`/`+0x32` are non-zero);
2. it is skipped when it is more than 150 degrees from the last chosen heading (byte `+0x2C`, `byte *
   pi / 128`), or its pitch is not within 90 degrees;
3. a candidate of 135 degrees, once an earlier candidate came back 2 (moving units in the way, no
   blocker), is replaced by that earlier candidate, taken without a probe;
4. otherwise the forward clearance `0x00335B60` probes it at the probe distance (at `+0x110 + 1.8`
   for the 135-degree entries), with tolerance `1 - attempts / 10` and flags 8 for the straight
   heading, plus 4 under order `0x4124` or `0x4022` while fleeing, else 2. A result of 0 takes it; a
   result of 2 is remembered.

A taken heading gets its steering mode from `0x00339DF0` (below). Mode 2 needs a second clear probe
along the limited heading `+0xBC` (distance 1.0, tolerance 0.8) and then runs `0x0033D200`, whose
result replaces the mode; a blocked second probe makes it mode 1. Mode 1 runs `0x0033CEF0`. Mode 3
stops the unit, steps both `+0xB4` and `+0xBC` from the current heading toward the candidate by the
slow rate `+0xEC`, and starts a countdown of 10 when no countdown runs (cleared when the heading arrives).

The pitch goes to `+0xB8`, the heading to byte `+0x2C`, `0x0033CC80` records the aim, the side bits
are set by the sign of the offset (both cleared for 0), and the attempt counter (block `+0x3C`
bits under mask `0xF0`) is cleared. When no candidate is taken, `0x0033CEF0` runs toward the bearing, `0x0033CC80` records
mode 4, and the attempt counter rises by one up to 10, which lowers the next search's tolerance.

`0x0033CC80(ctx, mode, heading, pitch, distance)` writes the aim: when the distance exceeds the
speed `+0xB0`, the mode goes to the flag word's bits `0x1F` and the point `distance` ahead along the
heading and pitch (`0x01F004C0`, `{0, 0, 1}`, scaled, turned about x by minus the pitch and about y by the
heading) to block `+0x04`-`+0x0C`, the same `+0x04` mode 6 uses as its orbit radius; otherwise only the
countdown is cleared.

The test is `distance - speed` above 0, a NaN included (`0x0033CCC2`-`0x0033CCD2`). The pitch is negated before the
turn about x (`0x0033CCFA`) and the heading wrapped by `0x0033CB70` before the turn about y (`0x0033CD34`); the turned
vector is added to the position `ctx + 0x00` (`0x00202B10`, `0x0033CD6C`), so the block holds a world point. The mode
is merged into the bits under mask `0x1F`, the rest of the flag word kept (`0x0033CD71`-`0x0033CD7F`).

The short path clears the countdown bits under mask `0x7FE0` alone (`and 0xFFFF801F`, `0x0033CCD4`): the mode, the
orbit bit `0x8000` and the aim point keep their values.

The vector helpers here: `0x004687F0` is the flat bearing of a vector, `acos(z / |v|)` from the table
`0x00D12590`, negated for a negative x; `0x004692F0` rescales a vector to a length (`0x00469320`
normalises it, leaving zero for a vector within `1e-6` of zero, and `0x00202FE0` scales);
`0x00202F00`, `0x00202E90` and `0x00202F70` copy a matrix and turn it about y, x and z (`0x00217880`,
`0x00217790`, `0x00217970`).

`0x00468700(v)` is the pitch of a vector: 0 when 0.01 is above its y and that y is above -0.01 (`0x00468715`-`0x00468733`).
Otherwise it makes two copies of `v` with x and z exchanged, `(z, y, x, 1.0)` and `(z, 0, x, 1.0)`, passes each to
`0x00469320(copy)`, takes `c = 0x00202D20(first, second)`, the sum of the three float products, and answers `0x0046F460(c)`,
or `0x0046F460(c - 1.0)` for a `c` above 1.0, negated when 0 is above y (`0x00468749`-`0x004687D4`).

`0x00203170` writes the identity matrix that `0x0033CC80`, `0x0033D890` and the
collision sweep's `0x0022EF20` start from. The same vector library holds `0x00203030` (x, y and z times a
scalar, the fourth float copied as it is, `0x0020306E`), `0x00202CA0` (the four floats times the reciprocal
of a scalar), `0x00202CF0`
(x, y and z divided by a scalar) and `0x002030E0` (a matrix copy with a vector added to its
translation row); their callers are presentation and text code outside this category.

### The steering mode table

`0x00339DF0(ctx, heading)` turns the angle `a = |wrap(heading - +0xE0)|` into a steering mode. It
indexes 48 rows of 12 bytes at `0x01EED4C0` by block byte `+0x175` (values above 7 read as 1) times
6, plus 3 when flag `+0x170` bit `0x8` is clear, plus the speed band (0 at rest, 1 up to the threshold
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

`0x00337470(ctx)` returns 0.0 unless the block's mover class byte `+0x174` is 3 (`0x00337490`-`0x003374A1`, `0x003376D7`). A
flier takes a reference point `R`: the context's target position `+0x40` when the block's goal kind, its `+0x40`, is
1, the step point `+0x10` equals the goal `+0x20` in x and z, and the unit `+0xF0` is null, has no definition `+0xE68`
or is not of definition mode 2; else the step point `+0x10` (`0x003374A7`-`0x003374F7`).

Two points lie along the route toward the waypoint `W` of the route's start region, `(x, 0, z, 1.0)` from the path
record's `+0x90` (`0x00337500`-`0x00337542`). The bytes read these as the block's dword `+0x184` for the region `r` and
its floats `+0x210 + 8 * r` and `+0x214 + 8 * r`: the page's path `+0x04` and path record `+0x90` are those offsets
less `0x180`, and its `+0x188` and `+0x190 + r` are path `+0x08` and `+0x10 + r`.

`0x00203080(v, W, ctx)` gives `v = W - position`, whose y is then set to 0; `0x004692F0(v, len)` rescales it and
`0x00202B10(P, v, ctx)` gives the point `P = v + position`: `A` with `len = [+0x110] + 0.1`, and `B` with
`len = 0x004686D0(W, ctx) + [+0x110]`, the waypoint's flat distance and the block's `+0x110` (`0x00337547`-`0x003375B5`).

`0x003208C0(R.x, R.z, &R.y)` first replaces the reference's own height by the terrain height under it
(`0x003375BA`-`0x003375C8`). `A` and `B` each take theirs the same way when its ground is walkable for the mover class
(`0x0026E100`): `0x0032A6A0(point, class, 0)`, a jump to `0x0026E100`, answering other than 0. A point for which it answers
0 becomes a copy of the whole reference, not only of its height (`0x003375CD`-`0x0033764B`).

With `s` the step scale `+0xC0`: when `A.y + s` is above the unit's y `+0x04`, the aim is `R` if `R.y` is at or above
both `A.y` and `B.y`, else `A` if `A.y` is at or above `B.y`, else `B`. When it is not above, the aim is `R` if `R.y`
is at or above `B.y`, else `B` (`0x0033764F`-`0x003376A9`). The aim's y is then raised by `s`, and the function returns
the pitch `0x00468700(v)`, with `v` from `0x00203080(v, aim, ctx)`, the aim minus the position; it stores it nowhere
(`0x003376AE`-`0x003376D0`).

`0x0026E100(point, w, c)` jumps to `0x00231400(part, point, w, c)` with `w` cut to a word and `c` passed as a dword; the
part is `[0x0209A678]` while the qword `0x0209A670` is not 0, and null otherwise (`0x0026E100`-`0x0026E11E`).

`0x00335180(out, ctx)` is the look-ahead point. Starting from the route's start region (path `+0x04`)
it takes that region's waypoint, and while the region is not the goal and has a next region it
advances when the unit's position lies inside a triangle of the next region (all three edge crosses
of one sign) or within 0.2 of one of its edges (`0x00468F70`); at most 128 steps. The point's height
is the terrain height plus the step scale for a flier, else the unit's own.

`0x00468F70(record, c)` jumps to `0x00469410(record, record + 0x10, w, c)` with `w` the record's float `+0x20`
(`0x00468F70`-`0x00468F7C`).

### The definition modes and the circling formation

`0x0033A240(block)`, run from the per-unit frame `0x00233F70` (`0x00234076`) and from `0x00308610`, gives an
enemy its own locomotion by its definition. It builds the solver context (`0x00336710(ctx, block,
0)`) and acts only for a unit whose stats record is an enemy's (byte `+5` = 1), whose class row
(`[unit + 0xE68]`) has a non-zero mode in byte `+0x18` bits `0xE`, whose step flags `+0x1F0` have
neither `0x1000` nor `0x2000`, and whose flag bit `0x40000` is clear or speed `+0x158` is 0.

While no action is being shown (`0x02089350` = 0) it runs the mode's body: 1 `0x0033DFD0`, 2
`0x0033D890`, 3 `0x0033DB60`. Either way it writes the context's speed, desired heading, pitch and
limited heading back to the block's `+0xD8`, `+0xDC`, `+0xF4` and `+0xE0`.

`0x0033D890(ctx)` is mode 2. While the unit's status words (`+0x3C | +0x64` of the stats record) lack
KO (bit `0x1`) and the battle-state word `0x02089340` lacks bit `0x20`, the unit moves at `speedA` along its
limited heading with pitch 0. A KO'd mode-2 unit whose `0x40`-byte slot record has `+0x1C` bit `0x1` joins the
circling formation instead; the slot record is `0x0208D480` indexed by the stats record's byte `+0x04` when that
record's byte `+0x05` is 0, and otherwise `0x0208DE80` indexed by the byte `+0xEA9` of the unit `0x0031B860` answers:

1. a circling unit runs `0x00337C10` while `0x022C7D04` bit `0x1` is clear: the first in a frame when a mode-5 enemy
   exists, every one when none does (the bit is set only once it is found, `0x00337CB4`, `0x00337D6D`). `0x00337C10` counts
   the KO'd mode-2 enemies into `0x022C7CEB`, finds an enemy of mode 5 (the last one in the unit table) and advances the
   shared angle `0x022C7CE0` by `0x02EC0F84`, wrapped by `0x0033CB70` (`0x00337CBA`-`0x00337CD6`);
2. `0x00337C10` also samples the centre `0x022C7CF0` from that enemy's position: on a call
   with the counter `0x022C7D00` at 0, which starts counting when the enemy moves (speed `+0x158`
   non-zero); then, from the tenth call on, on every call until a call finds it stopped and resets
   the counter; it sets `0x022C7D04` bit `0x1`;
3. each circling unit takes the next place `0x022C7CE9`: its goal `+0x20` is 1.0 from the centre at
   the angle `0x022C7CE0 + place * 2pi / count` (0 apart with fewer than two), its y replaced by the context's step
   scale `+0xC0` plus 3.2, and the block's step scale `+0x108` becomes 1.5;
4. within 0.1 of the goal the slot record's `+0x1C` bit `0x2` is set; until then the speed is `3.0 / (30 *
   [0x01DFE0B8])`, after it the distance capped at `7.0 / (30 * [0x01DFE0B8])`;
5. the desired heading and pitch aim at the goal (`0x004687F0`, `0x00468700`) and the limited heading
   faces the centre.

With no mode-5 enemy `0x00337C10` returns after the count, leaving the angle, the centre and `0x022C7D04` as they
were (`0x00337CB4`).

By address: `0x0033D890` reads the stats record `+0x698` of the unit at context `+0xF0`, and its two status dwords with
no null test (`0x0033D8A8`-`0x0033D8C1`). With bit `0x1` clear in both, it ends at once when the byte `0x02089340` has bit
`0x20`; otherwise it stores the limited heading `+0xBC` at `+0xB4`, the block's dword `+0xF8`, read through the
context's block pointer `+0x108`, at `+0xB0`, and 0 at `+0xB8`, and ends (`0x0033D8C3`-`0x0033D8F9`).

The slot record: when the stats record is not null and its byte `+0x05` is 0, the slot is `0x0208D480 + 0x40 * n` with
`n` its byte `+0x04`. Otherwise `0x0031B860(stats record)` answers a unit, kept at `0x02EBF188`; a null answer ends the
body, and the slot is `0x0208DE80 + 0x40 * n` with `n` that unit's byte `+0xEA9` (`0x0033D906`-`0x0033D94D`). A slot whose
byte `+0x1C` has bit `0x1` clear ends the body as well (`0x0033D953`-`0x0033D957`).

While the byte `0x022C7D04` has bit `0x1` clear it first calls `0x00337C10()` (`0x0033D95D`-`0x0033D976`). It stores 1.5 in
the block's step scale `+0x108`, through the same pointer (`0x0033D97B`-`0x0033D982`), and takes the place angle
`0x0033CB70(a)` with `a = place * (2pi / count) + [0x022C7CE0]`, the place the byte `0x022C7CE9` and the count the byte
`0x022C7CEB`; for a count of 0 or 1, an unsigned test, the quotient is not formed and the first term is 0
(`0x0033D98C`-`0x0033D9CC`).

The bit `0x1` of `0x022C7D04` and the place byte `0x022C7CE9` are the mode 1 body's too (`0x0033DFD0`): in a frame with
units of both modes the places run across both bodies, and whichever sampler sets the bit first keeps the other from
running.

The goal: `0x00202FE0(v, 0x01F004C0, 1.0)` gives `v = 1.0 * {0, 0, 1.0, 1.0}`, all four floats of the axis; `0x00203170(m)`
and `0x00202F00(m, m, 0x0033CB70(angle))` build the turn about y; `0x00202B70(v, m, v)` turns the vector; and
`0x00202B10(ctx + 0x20, 0x022C7CF0, v)` stores centre plus vector as the goal `+0x20`. Its y `+0x24` then becomes
`[ctx+0xC0] + [0x00D10B04]`, the step scale plus 3.2 (`0x0033D9D1`-`0x0033DA51`).

`d = 0x004686D0(ctx, ctx + 0x20)` is the flat distance from the position to the goal. When 0.1 is above `d` it sets bit
`0x2` of the slot's dword `+0x1C`. With that bit clear the speed `+0xB0` is `3.0 / ([0x01DFE0B8] * 30.0)`; with it set
it is `min(d, 7.0 / ([0x01DFE0B8] * 30.0))` (`0x0033DA56`-`0x0033DAC3`).

Last it takes `g = goal - position` with `0x00203080(g, ctx + 0x20, ctx)`, stores `0x004687F0(g)` at `+0xB4` and
`0x00468700(g)` at `+0xB8`; takes the centre minus the position with `0x00203080(g, 0x022C7CF0, ctx)` and stores
`0x004687F0(g)` at `+0xBC`; and makes the place byte `[0x022C7CE9] + 1` (`0x0033DACB`-`0x0033DB2E`).

The field frame clears `0x022C7D04` bit `0x1` and the place counter `0x022C7CE9` each frame (`0x0033B6D0`, after
`0x00338490`), and the area initialisation clears the block (`0x0033A380`). `0x00337A00`, at start-up, sets the angle step
`0x02EC0F84` to `2 / (30 * [0x01DFE0B4])` radians and stores `[0x01DFE0B4] * 240` beside it at `0x02EC0F80`.
`[0x01DFE0B4]` is the integer 1 in the image, so the formation turns 2 radians a second.

`0x0033A380()` stores 0 in the six qwords `0x022C7CE0`, `0x022C7CE8`, `0x022C7CF0`, `0x022C7CF8`, `0x022C7D00` and `0x022C7D08`,
calls `0x004696A0()` and then stores 0 in the dword `0x022C7D10` (`0x0033A380`-`0x0033A3B5`).

### Spacing and avoidance

`0x00338140(ctx)`, for goal kind 1: when the target is the unit itself, or the distance to the target
position `+0x40` is under 0.1, it stops and clears the countdown.

Otherwise, with `D` the distance
to the destination `+0x30`, it sets block `+0x38` bit `0x2` when `D` exceeds `min(+0x124 + 2, +0x128)`,
bit `0x4` when `D` is within `reach + 0.05` (reach = `+0x120`, or the target's own `+0x1A0` when the
target's target is this unit and its `+0x1A4` is below `+0x124`) and `0x003341A0` holds, clears bit
`0x2` inside the stop radius `+0xD0` and bit `0x4` outside it, and sets bit `0x2` when the pair clearance
`0x0033D660` returns 0.

Then:

- bit `0x2`: `0x00337A50`, the heading constraint `0x0033A720`, and the countdown cleared on success;
- bit `0x4`: the bearing from the step point back to the position (away from it) is probed with
  `0x00335B60(ctx, bearing, 0, 0.1, 0.8, 0)`; when clear the speed is `speedA`, `+0xB4` that reverse
  bearing and `+0xBC` the limiter's result for the forward bearing; else bit `0x4` is cleared;
- neither: the randomised manoeuvre `0x003343D0`, then `0x0033BAA0` when it starts;
- with neither bit and no countdown: speed 0, the limiter, and `0x0033BC80`.

`0x0033D660(ctx, a, b)` is the pair clearance: with both radii from `0x00265090` it takes
`a.+0x1A8 - (ra + rb)`, halved for a party unit `a` and divided by 3 otherwise, and returns 1 when the
distance to `b` is below `a.+0x1A8` and either unit's definition byte `+0x12` is negative, or
`0x00334C90` is at most that margin, and the raised segment between them (`0x00318CA0`) returns 0 or 1, an unsigned test,
so that its -1 fails (`0x0033D843`-`0x0033D846`).

A null `a` or `b` returns 0 (`0x0033D68C`, `0x0033D695`). Each radius is the larger of the two floats `0x00265090` gives
for the unit's actor `+0x10`, 0 without an actor (`0x0033D6D1`-`0x0033D71E`); for an actor that is not class 3 `0x00265090`
writes nothing and `0x0033D660` has not set the two stack slots, so the radius is then whatever they held.

The spacing `+0x1A8` is `a`'s (`0x0033D72E`, `0x0033D765`); `a` counts as a party unit when its record `+0x698` has byte
`+5` 0, and without a record the margin `m` is divided by 3, `m / 3.0` (`divss`, `0x0033D751`), where a party unit's is
`m × 0.5` (`mulss`, `0x0033D747`; `0x0033D723`-`0x0033D751`).

The distance is flat (`0x004686D0`), from the position `ctx + 0x00` to `b`'s actor position (`0x002646C0`, the origin
when `b` has no actor; `0x0033D69E`-`0x0033D6CD`, `0x0033D760`). The `+0x12` test counts a unit only when its record
`+0x698` has byte `+5` 1 and its definition `+0xE68` is present; it reads bit `0x80` of byte `+0x12`, `a` first
(`0x0033D776`-`0x0033D7C6`).

The segment runs from the position to `b`'s, each raised by its actor's height `0x00263940` (0 without an actor):
`0x00318CA0(from, to)` (`0x0033D7DF`-`0x0033D83E`). The 0 the caller also puts in r8d and r9d is overwritten unread
(`0x00318CB3`, `0x002315FC`). Every other path returns 0 (`0x0033D87C`).

It reads only the first 16 bytes of the context, the position. Its callers are the spacing pass `0x00338140`
(`0x003382F2`), the orbit `0x0033BAA0` (`0x0033BB1F`), the approach point `0x00339630`, which hands it a point in place of
a context (`0x0033994A`), and `0x0033A1E0(block)`, which builds a context with `0x00336710(ctx, block, 1)` and returns
`0x0033D660(ctx, unit +0xF0, target unit +0xF8)` (`0x0033A1F9`-`0x0033A221`); `0x0033A1E0`'s caller is `0x00304D15`.

`0x00265090(actor, out1, out2)` writes only for a class-3 actor (byte `+0x03 & 0xE0` = `0x60`): it jumps to
`0x003DA710(o + 0x50, out1, out2)`, `o` being the object at the actor's `+0xB8`, which copies the dwords `+0x00` and
`+0x04` it is given, that object's `+0x50` and `+0x54`, to the two outputs and skips a null output
(`0x00265090`-`0x002650A5`, `0x003DA710`-`0x003DA724`). For any other class the outputs keep what they held; neither the actor
nor its `+0xB8` pointer is tested for null.

`0x00318CA0(a, b)` answers -1 while the qword `0x02EC1378` is null, and otherwise the word `0x002315E0([0x02EC1378], a, b)`
answers, sign-extended (`0x00318CA0`-`0x00318CC4`).

`0x00334C30(ctx)` is the orbit step angle: with `c = 2pi * d`, `d` the flat distance from the target position
`+0x40` to the unit, it returns `speedA / c * 2pi` radians, or 0.0 when `speedA` exceeds `c`
(`0x00334C30`-`0x00334C79`).

`0x00334AB0(ctx)` is the orbit heading. It takes the same angle, returns 0.0 when `speedA` exceeds `c` or the
angle is 0, and negates the angle under flag bit `0x8000` (`0x00334AED`-`0x00334B3C`). It turns the unit's offset
from the target, y set to 0, about y by that angle; while a countdown runs it rescales the turned offset to `d +
(+0x04 - d) / countdown`, easing toward the orbit radius (`0x00334BA1`-`0x00334BD0`). The heading is the flat
bearing of the turned offset minus the original one (`0x00334BD5`-`0x00334BEE`).

`0x003343D0(ctx)` starts a sidestep:

1. it refuses when the target unit is the unit itself, the distance to the target is within
   `+0xA0`, the mode is 6, the odds `+0x130` are -1, or the unit (`0x00335760`) is not engaged and
   not under order `0x96`; after the angle tests it also refuses while the turning flag (block
   `+0x38` bit `0x8`) is set;
2. `0x003357B0` is asked about the corridor to the target; the odds halve when it reports blockers;
   `rand() % odds` must be 0;
3. the target must lie within 120 degrees of the actor's facing and the actor within 45 degrees of
   its heading;
4. a `rand()` bit picks the side (flag bit `0x8000`); `0x00335B60` probes `0x00334AB0`'s orbit heading, the
   other side on failure, and both failing refuses;
5. otherwise the mode becomes 6 and the orbit radius `+0x04` the current distance plus or minus
   `(rand() % 5 + 5) / 100`, after the countdown:
   - `0x00334C30` gives the turn per step in radians: the speed `[+0x108]+0xF8` over `2 pi r`, times `2 pi`,
     with `r` from `0x004686D0`, or 0.0 when the speed is above `2 pi r` (`0x00334C4F`-`0x00334C79`);
   - a turn of 0.0 refuses (`0x00334640`-`0x00334647`, against the 0.0 set at `0x003345D2`);
   - otherwise the countdown, bits `0x7FE0`, is `[+0x108]+0x12C` divided by the turn and truncated,
     `n = (int)([+0x108]+0x12C / turn)` stored as `f = (n << 5) & 0x7FE0` (`0x00334688`-`0x0033469A`), halved for
     `0x0031EA90` class 4, `f = (f >> 1) & 0x3FE0` (`0x003346B3`-`0x003346CB`);
   - a speed and `r` both 0 give a NaN turn, which passes the test and leaves a countdown of 0
     (`cvttss2si` gives `0x80000000`).

### Detour and stall recovery

`0x0033C870(ctx)`: with `+0xCC` bit `0x400` set it finishes a detour: `0x00334E00` picks the point into
`+0x50`, for goal kind 1 the limited heading `+0xBC` takes the bearing from that point to the
target, bit `0x400` becomes bit `0x80`, `0x0033E1F0` resets the avoidance state, block `+0x3C` bit `0x8` is
cleared, and the step is claimed.

Otherwise, when `+0x176` bit `0x4` is set, `+0x170` bit `0x1` is clear,
and either `+0x3C` bit `0x8`, `+0x170` bit `0x2` or the goal `+0x20` is beyond `+0x110 + +0xA4 + 5` away, a
reachable random detour (`0x00334E00`) claims the step with bit `0x400` set, the countdown cleared and
speed 0.

The point the starting call finds goes to a stack slot and is not kept (`0x0033C963`); the finish draws again into
`+0x50` and ignores that call's result (`0x0033C8A8`). With neither case it answers 0 (`0x0033C995`).

`0x00334E00(ctx, out)`: for a goal of kind 1 (the dword `+0x40` of the block `+0x108`) it searches around the target
position `+0x40` at `radius + target radius + 0.1`, `+0xA0 + +0xA4 + 0.1` (`0x00334E26`-`0x00334E58`). For any other goal
it first tests the goal `+0x20` itself (`0x003377C0` with the unit `+0xF0`, `0x00334E5A`-`0x00334E6C`): on the mesh it
returns the goal with result 1, or the position with result 0 when the flat distance `0x004686D0` is below 0.1, with no
random draw (`0x00334E6E`-`0x00334E96`); only an off-mesh goal starts the search around it at `+0xAC - 0.1`
(`0x00334E9B`-`0x00334EAD`).

The search tries eight directions in two rounds, each from its own random start, `rand() % 360` degrees, `rand()`
being the import `[0x008C3098]` (`0x00334F50`-`0x00334F86`, `0x003350D8`), stepping a right angle four times
(`0x003350C3`-`0x003350CD`); each angle is wrapped into `[-pi, pi]` (`0x00334F90`-`0x0033502A`), and the direction is the axis
`0x01F004C0` turned about y (`0x00203170`, `0x00202F00`, `0x00202B70`), with the radius as its length (`0x00202FE0`) and the
centre as its origin (`0x00202B10`, `0x0033502E`-`0x00335082`).

It keeps the first point on the mesh (`0x003377C0`) that is reachable from the centre (`0x0033D3E0` with the class
`+0x174` not 1), with result 1 (`0x00335087`-`0x003350BD`, `0x00335163`); it falls back to the unit's own position with
result 0 (`0x003350DE`-`0x003350E1`). The point goes to `out` (`0x0033513A`).

`0x0033E1F0` re-rolls the step scale `+0x108` to `2.5 + (rand() % 100) / 100` for a definition mode
2 unit, clears the mode and countdown (the orbit bit stays), sets `+0x10` to 256.0, zeroes the
counters, puts `rand() % 3 & 1` into the low nibble of `+0x38`, and in `+0x3C` clears bits `0x7`,
sets bit `0x8` to `rand() % 10 == 0` (a one in ten draw) and sets bit `0x100`.

The re-roll needs the unit `+0xF0` and its definition `+0xE68` (`0x0033E20B`-`0x0033E228`). The counters are the bytes
`+0x14` (the stall counter), `+0x20` and `+0x34` (`0x0033E283`-`0x0033E28B`). It also clears `+0x21` bit `0x1`, the
heading byte valid flag (`0x0033E278`), and zeroes the 16 bytes `+0x24`-`+0x33` (`0x0033E2F8`, `0x0033E2FC`): the last
move position, the chosen heading byte `+0x2C`, the two move headings and both zig-zag memories with their lives.

The low nibble of `+0x38` becomes 1 when `rand() % 3` is 1, else 0 (`0x0033E29C`-`0x0033E2B9`), so the too-far bit
`0x2`, the within-reach bit `0x4` and the turning flag `0x8` are cleared and the detour side bits under mask
`0xC0` stay. Two `rand()` calls are made (`0x0033E28F`, `0x0033E2BC`), three for a mode 2 unit (`0x0033E22A` first).

Besides `0x0033C870` (`0x0033C8F5`) it runs from the block reset `0x0033C9B0(block)`, which builds a context with
`0x00336710(ctx, block, 0)` and calls it (`0x0033C9D4`-`0x0033C9DE`).

The context builder is also reached outside the per-unit frame `0x00233F70`; two such routes start in the world tick
`0x00314020`. Its slot-0 step `0x00234520`, when `0x02089340 & 5` is not 1 and `0x00383C80()` answers non-zero, runs the queue
drain `0x00313CD0` (`0x00234582`), which runs `0x00305AB0(unit, 0)` for queued units (`0x00313D89`); from there `0x00305CC0`
(`0x00305BA5`), `0x003014C0` (`0x00305DD2`), `0x00301830` (`0x003015DA`), `0x0033A120` (`0x003019E4`) and `0x00336710` (`0x0033A14C`)
follow, each a conditional call, the last two only for actions `0x4124` and `0x4022`.

On this route `0x00301830` hands `0x0033A120` a stack copy of the block with `+0x80`, `+0x90` and `+0xD0` rewritten by
`0x00312730`, and the context is built from that copy with `t` = 1 (`0x00301857`-`0x003019E4`, `0x0033A13E`). The stick path's
`0x00317E60` resets the focus unit's block (`0x00317EA4`; [player movement](player-movement.md)).

The action reset `0x003105D0` runs the block reset only for a unit with a stats record (`0x003105D0`-`0x003105E9`,
`0x00310758`), both inside the frame, from `0x00308610` (`0x003086B2`, `0x003087C1`) and `0x00300E40` (`0x00300E61`), and outside
it, from `0x00300140` when its second argument is not 0 (`0x00300149`-`0x0030014D`), under `0x00234590` (`0x002346BE`).

`0x0033C200(ctx)` runs for a unit (`+0xF0`; without one it answers 0) under order `0x4124` or `0x4022` with a
battle in progress (`0x002F8E70(unit) & 7`, `0x0033C219`-`0x0033C256`): `0x0033BD70` and `0x0033C310` can claim the step.

Otherwise, with the leader not animating a move (`0x00265830` = 0, or no leader actor `+0xE8`), the remaining path
distance `0x00334950` is compared with the stored `+0x10`: a drop of over 0.01 re-stores it and zeroes the counter
`+0x14`, a rise past it plus 1.5 re-stores it, anything else counts up to 60; when `0x0033C310` returned 2 the
step is then claimed as well. With the leader animating a move it answers 0 at once, even after a 2
(`0x0033C298`-`0x0033C2A5`).

`0x00265830(actor)` answers the float `+0x24` of the object at `+0xF0` of the actor's movement context `+0xB8` for a
class-3 actor, and 0.0 for any other class, with no null test (`0x00265830`-`0x00265851`).

`0x00334950(ctx)` is the length from the unit's position along the route's waypoints, region by region from the
start region `+0x184` of the object at context `+0x108` (`0x00334987`, `0x003349B4`; `+0x188`, `+0x190` and `+0x210`
below are in the same object), until the region holding the leader position, context `+0x60` (`0x00384130`), the goal
region `+0x188` or a `0xFF` link, 128 at most (`cmp esi, 0x80`, `0x00334A2F`), plus the last leg to the leader position
(`0x003349AA`-`0x00334A44`).

`L = d(p, w[r0]) + d(w[r0], w[r1]) + ... + d(w[last], leader)`, with `d` the flat
distance `0x004686D0`, `w[r]` the route's x and z at `+0x210 + 8 × r` and the next region the byte `+0x190 + r`
(`0x003349C2`-`0x00334A35`).

`0x0033BD70` fires at 60: with the goal at least 20 units away and the unit off screen, it samples the route at 1,
2, ... 20 units ahead (`0x003347C0`) and takes the first point on the mesh as a detour (`+0xCC` bit `0x80`,
`+0x50`). It answers 0 without a unit, outside a battle, below 60 or for an order other than `0x4124` and
`0x4022` (`0x0033BDA9`-`0x0033BDE9`); off screen is `0x00322360(unit)` = 0 (`0x0033BE0F`-`0x0033BE16`), the box test of
[gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md).

A taken point also zeroes the stall counter `+0x14` and answers 1 (`0x0033BEB0`-`0x0033BEC8`); a sample whose x and
z equal the destination `+0x30` ends the search with 0 (`0x0033BE5E`-`0x0033BE78`).

`0x00322360(unit)` reads the position of the unit's actor `+0x10` through `0x00265020` (`0x00322375`-`0x0032238B`), which
copies it for a non-null actor of class 1 or 3 and otherwise gives 0, 0 and 0, and answers
`0x003223C0(actor, position)`, the box test, with the position's fourth float set to 0 (`0x00322390`-`0x003223A1`).

`0x003347C0(out, ctx, length)` walks from the position along the same waypoints, those of the object at context
`+0x108`, each with y 0. It first counts the regions of the route: from the start region `+0x184` it follows the link
bytes `+0x190 + r` until the goal region `+0x188` or a `0xFF` link, 128 links at most (`0x003347E8`-`0x00334832`).

It then copies the 16 bytes of the context's position `+0x00` to `out`, height included (`0x00334834`-`0x00334838`). A
count of 1 or less would end the function there (`0x0033483C`-`0x0033483E`); the count starts at 1 and the loop adds 1
before its first test, so it is 2 or more.

For waypoint `i`, counted from 1, it takes the region reached after `i - 1` links from the start region, stopping at
the goal region or a `0xFF` link, and the point `(x, 0, z, 1.0)` with x and z the floats `+0x210 + 8 × r` and
`+0x214 + 8 × r` of that region `r`; `d = 0x004686D0(out, waypoint)` is the flat distance to it
(`0x00334844`-`0x003348D0`).

When `d` is above the length left, the walk ends there: `0x00203080(v, waypoint, out)` gives the leg
`v = waypoint - out`, `0x004692F0(v, length)` rescales it to the length left, and `0x00202B10(out, v, out)` makes
`out = v + out` (`0x003348D5`-`0x0033491D`). Otherwise `length -= d`, `out` becomes the waypoint and the walk goes on;
when the waypoints run out, `out` is the last one (`0x003348DA`-`0x003348F1`). It returns `out`.

The rescale runs only on the leg where the walk ends, and `0x004692F0` normalises over x, y and z while `d` was flat.
When that leg is the first, `out` is still the full position while the waypoint has y 0, so the leg vector carries
minus the position's y into the rescale; on any later leg `out` is a waypoint, with y 0.

`0x0033C310` runs under the same order gate (`0x4124`, or `0x4022` while fleeing) with the
leader present and not animating a move and the remaining route under 6 units. When the unit's
actor is active (`0x002EA7F0`) it lists the actors in the corridor (`0x00391D10` for a point,
`0x003920F0` for a segment, 32 at most) and with any candidate or blocker among them zeroes the
speed and returns 1.

With neither, and the stall counter under 60, it aims a point `+0xAC + 0.1`
ahead along the last move (from block `+0x18`/`+0x1C`); when that direction differs from the
current heading by over 5 degrees, is reachable (`0x0033D3E0` not 1) and on walkable terrain
(`0x0026E100`), the desired heading takes the byte `+0x2C`, `+0xBC` the approach helper's result,
the countdown is cleared and 2 is returned, else 0. With the counter at 60 it zeroes the speed
and returns 1.

### Finalising the step

`0x0033BFB0(ctx)` handles a unit whose flags `+0x170` have bit `0x200`: when the angle between the
block's `+0x140` direction and the step exceeds 135 degrees, it probes the heading stored as a
byte at block `+0x20` (`byte * pi / 128`, less `2pi` above pi: bytes 129 to 255 give negative headings) and, when
clear and `+0x21` bit `0x1` set, takes that
heading with the rate `+0xE8` and clears the countdown. Otherwise it stores the desired heading as
that byte, the low byte of `min(n, 256)` with `n = (int)(wrap(h) * 128 / pi)` and 256 added to a negative `n`, so 0 to
255, and sets `+0x21` bit `0x1`.

The flags, the direction, the heading `+0xE0` and the rate `+0xE8` are the block's, read through the context's block
pointer `+0x108`; the byte, its flag and the countdown are read and written through `+0x100`.

The step is the step point `+0x10` minus the position, `s = [+0x10] - p` (`0x00203080`, `0x0033BFE0`-`0x0033BFEF`).
The angle is `0x0046F460` of the dot product of the two normalised vectors, `a = 0x0046F460(c > 1.0 ? c - 1.0 : c)`
with `c = dot(d, s)` (`0x004692E0`, `0x0033C045`-`0x0033C079`), with 1.0 subtracted from a dot above 1.0, taken as
`2pi - angle` when the cross product's y is negative, and folded once by `2pi` into `[-pi, pi]`
(`0x0033BFE0`-`0x0033C0DF`).

In bytes, with `d` the block's `+0x140` direction: `a = cross(d, s).y < 0 ? 2pi - a : a`, then
`a > pi ? a - 2pi : a < -pi ? a + 2pi : a` (`0x0033C090`-`0x0033C0C9`). The byte is read at `0x0033C0EC` and `0x0033C144`
and written at `0x0033C1CE`.

The probe is `0x00335B60(ctx, heading, 0, 0.1, 0.8, 0)` (`0x0033C114`-`0x0033C135`). Taking the heading sets the context's
`+0xB4` to it and the context's `+0xBC` to `0x00334120(e0, heading, e8)`, `e0` and `e8` being the block's `+0xE0` and
`+0xE8`, leaves the byte as it was and answers 1; every other
path stores the byte and answers 0 (`0x0033C164`-`0x0033C1D1`).

By address: `0x0033BFB0` reaches the block through the context's two block pointers: `+0x100` for the byte `+0x20`, its
flag byte `+0x21` and the countdown, and `+0x108` for the flags `+0x170`, the direction `d` at `+0x140`, the heading
`+0xE0` and the rate `+0xE8`. The step `s` is `0x00203080(s, ctx + 0x10, ctx)` (`0x0033BFD9`-`0x0033C02D`). With bit `0x200`
of the flags clear it goes straight to the store path (`0x0033C035`-`0x0033C03F`).

Otherwise it normalises a stack copy of the direction, `0x004692E0(d)` (the block's `+0x140` is only read: `d` is x, y,
z with `w` 1.0, copied at `0x0033C003`-`0x0033C02D`), and the step, `0x004692E0(s)`, takes `c = 0x00202D20(d, s)` and the
angle `0x0046F460(c)`, or `0x0046F460(c - 1.0)` for a `c` above 1.0, and the cross product `0x00202E10(x, d, s)`
(`0x0033C045`-`0x0033C090`); it goes on to the probe only when the absolute value of the folded angle is above
`[0x00915730]`, 3pi/4 (`0x0033C0CD`-`0x0033C0E6`).

The byte's heading is `g = byte * pi / 128`, with `[0x00915624]`, -2pi, added when `g` is above pi; it is formed twice,
for the probe and for the store to the context's `+0xB4` (`0x0033C0EC`-`0x0033C110`, `0x0033C144`-`0x0033C16B`). The heading
is taken only when the probe answers 0 and the block's byte `+0x21` has bit `0x1` (`0x0033C13A`-`0x0033C142`); taking it
stores `0x00334120`'s answer at the context's `+0xBC` and clears bits `0x7FE0` of the block's dword `+0x00`
(`0x0033C173`-`0x0033C195`).

The store path takes `n = (int)(0x0033CB70(h) * 128.0 / pi)`, `h` the context's `+0xB4`, truncated toward zero, adds 256
to a negative `n`, `n + 256`, and takes `min(n, 256)`. It sets bit `0x1` of the block's byte `+0x21` and stores the
low byte of `n` at the block's `+0x20`, so 256 is stored as 0 (`0x0033C19D`-`0x0033C1CE`).

`0x0033BC80(ctx, point)` is the ground check for class 3 against a non-class-3 target: it probes the
terrain height under the point (`0x003208C0`), floors it at the target's y (`+0x44`), and when
`probed + +0xC0 - unit y` (the step scale is added, as the code has it) is 0.3 or more in
magnitude sets the pitch to `+-pi/2` by its sign and the speed to `+0xE8`.

It reads the target unit `+0xF8` with no null test (`0x0033BCAC`), probes at the point's x and z only, replaces
the whole point by the target position `+0x40` when the target is higher (`0x0033BCE9`), and sets `+pi/2` for a
positive difference and `-pi/2` for a negative one (`0x0033BD1D`-`0x0033BD31`).

### The corridor probes

Five predicates test a step. Every non-zero exit returns a literal small integer:

| Probe | Returns |
|---|---|
| `0x0033D3E0(A, B, class)` (the straight walk) | 0 when `A` is off the mesh or the walk reaches `B`'s region through portals open to `class` (`0x0026E300` 1, or 0 with the mask bit) and the segment crosses each portal (`0x00468880`); 1 when `B` is off the mesh or a region has no crossable portal: blocked |
| `0x00335E50(A, B, w, class)` (the width walk) | 1 when the walk offset by `+w`, the walk offset by `-w`, or the lateral segment across `B` from `+w` to `-w` is blocked |
| `0x00335B60(ctx, angle, pitch, distance, tolerance, flags)` (forward step clearance) | 0 at once for a zero distance; otherwise 0 usable; 1 rejected by the obstruction query returning 1, the class-3 segment test `0x00318CA0`, the width walk at `0.9 * +0x10C` (or the straight walk with flags bit `0x8`), the grid query `0x00391410`, or the terrain test `0x0026E100`; 2 only when the obstruction query returned 2 |
| `0x003357B0(A, B, radius, unit, exclude, flags)` (dynamic obstruction) | 0 at once unless `flags` bit `0x20` is set or the asker's actor is active (`0x002EA7F0`); otherwise 0 nothing in the corridor; 1 a candidate accepted as blocking; 2 candidates counted but no blocker. The candidates come from the grid's actor list (`0x00391D10` for a point, `0x003920F0(..., 32, ~(flags >> 4) & 8 \| 0x14)` for a segment, at most 32); a unit of definition mode 1 against a mode-4 asker, the excluded unit and the asker itself are skipped; the rest pass the kind filters of `flags` bits under mask `0x5E`, then `0x00314EB0` and `0x00313F80` decide blocking (results 1-3 count as candidates, others as blockers) |
| `0x0033A3D0(A, B)` (path width) | 1 when the walk `B` to `A` is clear, or when a half-way lateral detour at `+-45` degrees is fully clear; 0 only when the direct walk and both detours have a blocked leg |
| `0x00335F90(ctx)` (corridor blocked) | 1 when the width walk at `0.9 * +0x10C`, the straight walk, or, for class 3, the segment test blocks; else 0 |

The straight walk `0x0033D3E0` goes region by region: from each region it takes the first portal, in region order,
that is open to `class` and that the segment crosses, never stepping back into the region it has just left, and
after 128 crossings without reaching `B`'s region it returns 0 (`0x0033D4A3`-`0x0033D612`).

`0x00335E50(A, B, w, class)` builds its offset `o` in four calls: `0x00203080(o, A, B)`, the difference `A - B` float by
float, after which the y of `o` is set to 0; `0x00202DE0(o, o)`; `0x00202E10(o, o, axis)`, the cross product with the axis
`{0, 1.0, 0}` at `0x01F004B0`; and `0x00202FE0(o, o, w)` (`0x00335E86`-`0x00335EC6`).

It then runs the straight walk up to three times and answers 1 at the first that returns 1:
`0x0033D3E0(A + o, B + o, class)`, `0x0033D3E0(A - o, B - o, class)` and `0x0033D3E0(B + o, B - o, class)`; otherwise it
answers 0. The sums come from `0x00202B10(out, a, b)` and the differences from `0x00203080(out, a, b)`, each over four
floats (`0x00335ECB`-`0x00335F62`).

The probes read the mover class `+0x174` afresh at each test. The forward clearance clamps its
tolerance to `[0.2, 0.8]` and divides the distance by `cos(pitch)` for a non-zero pitch; its callers hand in their own
distances and tolerances, the heading search's at `0x0033B09A` the probe distance and `1 - attempts / 10`.

`0x00335B60(ctx, angle, pitch, distance, tolerance, flags)` answers 0 at once for a zero distance
(`0x00335B98`-`0x00335BA4`); the steps above on the tolerance and the pitch are `0x00335BB4`-`0x00335BE4` (`0x00861F08`, for a
non-zero pitch). The direction is the axis `0x01F004C0` turned about x by `-pitch` and then about y by the angle wrapped
by `0x0033CB70` (`0x00203170`, `0x00202E90`, `0x00202B70`, `0x00202F00`, `0x00335BE8`-`0x00335C55`).

From the position it builds three points with `0x00202FE0` and `0x00202B10`, `+0x110` being the block `+0x108`'s: the far
point at `distance + +0x110` (`0x00335C5A`-`0x00335C88`), the near point at `distance` (`0x00335C8D`-`0x00335CB4`) and the
obstruction point at `+0x110 - +0x110 * tolerance + distance` (`0x00335CB9`-`0x00335CFC`).

The tests run in order, each answering 1 when it blocks (`0x00335D91`): the obstruction query
`0x003357B0(ctx, obstruction point, +0x110 * tolerance, unit +0xF0, exclude +0xE0, f)`, the context's unit and its
target's actor, `f` being `(flags & 4 | 0x10) << 2 | flags & 2`, at 1 (`0x00335D01`-`0x00335D41`); for class 3 the segment
test `0x00318CA0(ctx, far point, 0, 0)` at non-zero (`0x00335D43`-`0x00335D68`); with flags bit `0x8` the straight walk
`0x0033D3E0(ctx, near point, class)` at 1, else the width walk `0x00335E50(ctx, near point, 0.9 * +0x10C, class)`
(`0x008FCC8C`) at non-zero (`0x00335D6A`-`0x00335DB7`).

Then the grid query `0x00391410(ctx, obstruction point, tolerance * +0x110)` at non-zero (`0x00335DB9`-`0x00335DDC`) and the
terrain test `0x0032A6A0`, a jump to `0x0026E100`, on the far point with the class and `class == 3`, at 0
(`0x00335DDE`-`0x00335E04`). Past them it answers 2 when the obstruction query returned 2, else 0 (`0x00335E06`-`0x00335E10`).

### The order goal decoder

`0x00312730(unit, order, outTarget, outGoal, outReach)` turns an order word at `+0x714` into a goal. It reads the id as
the record's word `+0x00` and the parameter as its signed word `+0x02` (`0x00312742`-`0x00312748`), and takes `r`, the
larger of the two floats `0x00265090` gives for the unit's actor (`0x0031275A`-`0x0031277A`); for an actor that is not class
3 `0x00265090` writes nothing and `0x00312730` has not set the two stack slots, so `r` is then whatever they held.

Ids `0x4000`-`0x4024` go through a byte table (`0x00312798`-`0x003127C5`), `0x4026`-`0x4035` go to `0x002367A0`
(`0x0031278C`-`0x00312792`), and ids above `0x4035` are compared with the five higher sources (`0x00312780`-`0x00312786`,
`0x0031297D`-`0x003129A3`).

A source answers 1 with a point in `outTarget` and `outGoal`, for most sources the same 16 bytes (the goal written to
`outTarget` and copied), for `0x4022` and `0x4124` two different ones (below), and its reach in `outReach` when that
is not null (`0x00312890`, `0x00312905`, `0x0031295E`, `0x003129E9`, `0x00312A39`, `0x00312A8A`, `0x00312ACD`). It answers 0
(`0x00312AD4`) when `0x00312DF0` answers below 0 (`0x0031285D`, `0x00312A6F`) or another test of its arm fails, as listed
below. The sources:

- `0x4000`-`0x401F` call `0x00312DF0` with no centre, the number order - `0x3FFF`, which `0x00312DF0` turns into a centre
  through `0x00320940`, answering -1 when that answers below 0 (`0x00312EA3`-`0x00312EB7`), and a range of the parameter
  (`0x003127C7`-`0x003127D2`, `0x00312A60`-`0x00312A6F`);
- `0x4020`, for a kind-1 unit, calls `0x00312DF0` around the spawn record's `+0x50` with a range of the parameter
  (`0x003127D7`-`0x003127FF`);
- `0x4022`, for a kind-0 unit (`0x003128A5`-`0x003128B4`) when the unit `0x0031B7E0` resolves from the unit's dword `+0x24`
  exists, writes the unit's own `+0x120` to `outTarget` and that unit's `+0xD0` to `outGoal` (`0x0031289E`-`0x003128E4`);
- `0x4023` calls `0x00312DF0` with the `+0xD0` of the target of `+0x710`, which must exist (`0x00312812`-`0x00312815`), and
  a range of the parameter plus the target's `0x0030A130` size, truncated to a whole number (`cvttss2si r8d, xmm0` at
  `0x00312851`), or 0 for a parameter of 0 (`0x00312804`-`0x0031285D`);
- `0x4024` the party leader (`0x003272A0`, `0x00312913`);
- `0x4026`-`0x4035` the unit of definition selector `order - 0x4026` (`0x002367A0`, `0x00312970`-`0x00312976`).

For `0x4024`, `0x4026`-`0x4035` and `0x414A` the other unit must exist and not be the unit itself; its `+0xD0` is both
the target and the goal (`0x00312918`-`0x0031293D`). The five higher sources:

- `0x4124`: the unit `0x0031B7E0` resolves from the unit's dword `+0x24` must exist and not be the unit
  (`0x00312A94`-`0x00312AA1`); `outTarget` is the unit's own `+0x120` and `outGoal` its `+0x130` (`0x00312A91`-`0x00312ABC`);
- `0x4125`: `0x00312DF0` around the unit's own `+0xD0` with a range of 20 (`0x00312A50`-`0x00312A6F`);
- `0x414A`: the unit `0x0031B7E0` resolves from the unit's dword `+0x24`, through the arm of `0x4024`
  (`0x00312A43`-`0x00312A4B`);
- `0x414E`: the position `0x00265390` gives for the actor `0x0031ABE0(unit dword +0x710)`, which must exist
  (`0x003129F3`-`0x00312A25`);
- `0x4165`: `0x00319850(unit, outTarget)`, which must not answer below 0 (`0x003129A9`-`0x003129C7`).

`0x4021`, `0x4025` and everything else reject. The reach returned is:

- `r` alone for `0x4000`-`0x4020` and `0x4125` (`0x00312A81`-`0x00312A86`);
- `r` plus the other unit's `0x0030A130` size plus the parameter for `0x4024`, `0x4026`-`0x4035` and
  `0x414A` (`0x00312941`-`0x00312967`);
- `r`, plus the target's size only when the parameter is 0, for `0x4023` (`0x00312873`-`0x00312895`);
- the unit's dword `+0x154` for `0x4124` (`0x00312AC0`-`0x00312ACB`);
- 0 for `0x414E` (`0x00312A2A`-`0x00312A33`);
- `r + 1.0 - 0.1` for `0x4165` (`0x003129CC`-`0x003129E5`);
- for `0x4022` it is `0x00309B10(unit) + 0x00309A90()`, where `0x00309B10(unit)` is `max(a, b) + 0.1` for the unit's two
  `0x00265090` floats a and b (`0x003128E8`-`0x0031290A`).

`0x00312DF0` draws up to nine random points (`0x00312E40`-`0x00312E47`), answering 0 when
`0x00317DE0(unit, point, flag)` accepts one (`0x00312E9F`) and -2 when it accepts none (`0x00312EBC`). `0x00317DE0`
tests a copy of the point with `0x00337700` (no shaped obstacle at the point, on the mesh, and walkable
at the unit's larger radius for its mover class `+0x1F4`, `0x00336390`) or, with the flag, `0x003377C0`.

## Layouts

The solver context's fields, from the context builder `0x00336710` and the solvers that read them (the positions `+0x00`-`+0x3C` and the block pointers `+0x100`/`+0x108` are in the summary block below):

`CorridorNavAgent` (`0x110` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x40` | `f32[2]` | targetPosXY | x and y of the target position: `0x00336710` zeroes them (`0x0033695D`) and, when the block's goal kind `+0x160` is 3 or its `+0x40` is 1 or 2, fills x, y and z from the target actor through `0x002646C0` (`0x003369ED`-`0x003369FC`); `0x00334E00` takes `+0x40` as its probe point when the block's `+0x40` is 1 (`0x00334E4B`) |
| `+0x48` | `f32` | targetPosZ | z of the target position: 0 from `0x00336710` (`0x00336961`), then the target actor's z through `0x002646C0` (r9 = `+0x48`, `0x003369ED`) |
| `+0x4C` | `f32` | targetPosW | w of the target position, 1.0 from `0x00336710` (`0x00336965`) |
| `+0x70` | `f32[4]` | toStepPoint | the vector from the position (`+0x00`) to the step point (`+0x10`): `0x00336710` computes it with the vector subtract `0x00203080` (`0x0033683F`-`0x0033684A`; the store is `0x002030C9`) |
| `+0x80` | `f32[4]` | toRouteGoal | the vector from the position (`+0x00`) to the route goal (`+0x20`): `0x00336710` computes it with `0x00203080` (`0x00336820`-`0x0033683A`) |
| `+0xA0` | `f32` | radius | the unit's collision radius, the larger of the block's `+0x10C` and `+0x110` (`0x003367C2`-`0x003367D9`); the stop distance adds it (`0x00336A82`) and `0x003343D0` compares it with the horizontal distance to the target position (`0x00334432`) |
| `+0xA4` | `f32` | targetRadius | the target's radius: 0 from `0x00336710` (`0x00336984`), then the larger of the two floats `0x00265090` returns for the target actor (`0x00336A25`-`0x00336A42`); the stop distance adds it (`0x00336A8A`) and `0x00334E00` uses radius + targetRadius + 0.1 as its reach (`0x00334E39`-`0x00334E4F`) |
| `+0xA8` | `f32` | targetBearing | the bearing from the unit to the target: `0x004687F0` on target position minus position (`0x00336A3D`-`0x00336A5D`); `0x0033BAA0` turns the limited heading `+0xBC` toward it with `0x00334120` (`0x0033BC26`-`0x0033BC39`) |
| `+0xAC` | `f32` | stopDistance | the stop distance: radius + targetRadius + 0.1 when the block's `+0x40` is 1 (`0x00336A7C`-`0x00336A9A`), otherwise the block's `+0xD0` (`0x00336AA4`-`0x00336AAA`); `0x0033A570` compares the horizontal distance to the destination with it (`0x0033A5B5`) |
| `+0xB0` | `f32` | speed | the solver's output speed: 0 from `0x00336710` (`0x003367D2`), the step distance `0x00339BF0` from the default solver (`0x0033BF2A`) and from the class solver `0x003394A0` (`0x003394D3`), 0 from the class solver when the goal kind `+0x40` is not 0 (`0x003394BF`-`0x003394C3`, `0x003395DF`), 0 when `0x0033C870` claims a detour (`0x0033C989`); `0x00336CE0` writes it to the block's `+0xD8` (`0x00336D7C`-`0x00336D95`) |
| `+0xB4` | `f32` | desiredHeading | the desired heading: the block's `+0xDC` on entry (`0x003367E1`-`0x003367E7`); the class solver sets 0 (`0x0033953B`); `0x00336CE0` writes it back to `+0xDC` (`0x00336D85`-`0x00336DA6`) |
| `+0xB8` | `f32` | pitch | the pitch: the block's `+0xF4` on entry (`0x003367ED`-`0x003367F3`); the class solver `0x003394A0` sets pi/2 (`0x00339545`) or the pitch toward the step point (`0x003395C4`); `0x00336CE0` writes it back to `+0xF4` (`0x00336D9D`-`0x00336DB7`) |
| `+0xBC` | `f32` | limitedHeading | the limited heading: the block's `+0xE0` on entry (`0x003367F9`-`0x003367FF`); `0x0033BAA0` turns it toward the target bearing (`0x0033BC3E`), `0x0033C870` sets it to the detour bearing (`0x0033C8D6`) and the class solver stores the heading `0x003364D0` limits toward the goal (`0x0033960F`); `0x00336CE0` writes it back to `+0xE0` (`0x00336DAE`-`0x00336DC5`) |
| `+0xC0` | `f32` | stepScale | the step scale: the height above the ground at which the probes place points: the block's `+0x108` (`0x00336870`-`0x00336878`), raised to 2.0 below 2.0 unless the unit's definition byte `+0x18` has mode 2 (`0x0033689F`-`0x003368AC`); `0x0033A720` sets a point's y to the ground height `0x003208C0` plus this (`0x0033A97C`-`0x0033A990`), as does `0x00335180` (`0x0033552F`-`0x00335541`) |
| `+0xC8` | `f32` | goalDistance | the horizontal distance from the position to the route goal `+0x20` (Vector3_ComputeXZDistance `0x004686D0`, `0x00336942`-`0x0033694E`), replaced by the distance to the target position when a target is resolved (`0x00336A59`-`0x00336A6D`) |
| `+0xCC` | `u32` | flags | the block's flag word `+0x170` on entry (`0x00336827`-`0x00336834`), written back by `0x00336CE0` (`0x00336D8E`-`0x00336DD3`); bit `0x80` is set when `0x0033BD70` stores a detour point at `+0x50` (`0x0033BEBE`-`0x0033BEC8`) and cleared by the default solver `0x0033BED0` (`0x0033BF1D`); bit `0x400` is the detour in progress, tested by `0x0033C870` (`0x0033C889`), cleared with bit `0x80` set when it ends (`0x0033C8DE`-`0x0033C8EF`) and set when it starts one (`0x0033C97F`) |
| `+0xD0` | `u32` | leaderReachable | bit `0x1`: cleared by `0x00336710` (`0x003368B6`) and set when `0x0033D3E0`(ctx, leader position `+0x60`, 1) does not return 1 for a unit with order `0x4124`, or `0x4022` while the party is fleeing (`0x003368E8`-`0x00336932`); the step distance `0x00339BF0` then measures from the leader position (`0x00339D3A`-`0x00339D43`) |
| `+0xD8` | `void*` | unitActor | the unit's actor: the handle at BattleUnit `+0x8` of the block's slot `+0x177` resolved by `0x0031ABE0` (`0x00336805`-`0x00336819`) |
| `+0xE0` | `void*` | targetActor | the target's actor: the block's handle `+0x150` resolved by `0x003588B0` (`0x003369C5`-`0x003369D0`), set only when a target is sought; read for its radius by `0x00336710` (`0x00336A14`) and `0x0033A720` (`0x0033AA80`), and passed to the obstruction probe by `0x003343D0` (`0x00334484`) |
| `+0xE8` | `void*` | leaderActor | the party leader's actor, `+0x10` of the unit `0x003272A0` returns (`0x003368C7`-`0x003368DC`), or 0 with no leader (`0x0033693B`); `0x0033C200` and `0x0033C310` read it (`0x0033C28C`, `0x0033C368`) |
| `+0xF0` | `void*` | unit | the BattleUnit of the block's slot byte `+0x177` (`0x0033684F`-`0x00336869`); the solvers read its order word `+0x714` (`0x003368E8`-`0x003368F4`) |
| `+0xF8` | `void*` | targetUnit | the target's BattleUnit: 0 from `0x00336710` (`0x00336956`), then the block's handle `+0x150` resolved by `0x0031B7E0` (`0x003369B3`-`0x003369BE`); `0x0033BAA0` and `0x00338140` read it (`0x0033BB0E`, `0x003381F0`) |

Locomotion block (unit `+0x80`; the solver's "state" and "flag block" are the same record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` |  | flag word: mask `0x1F` steering mode, `0x7FE0` countdown, bit `0x8000` orbit direction |
| `+0x004` | `f32` |  | orbit radius |
| `+0x010` | `f32` | stored path distance |  |
| `+0x014` | `u8` | stall counter (60) |  |
| `+0x018` | `f32` | last solve x |  |
| `+0x01C` | `f32` | last solve z |  |
| `+0x020` | `u8` |  | heading as byte * pi/128 for the finalise step (`0x0033BFB0`) |
| `+0x021` | `u8` |  | bit `0x1` heading byte valid; bits `0x6` last turn direction |
| `+0x02C` | `u8` |  | heading as byte * pi/128 |
| `+0x038` | `u32` |  | bit `0x2` too far, bit `0x4` within reach, bit `0x8` turning, mask `0xC0` detour side |
| `+0x03C` | `u32` |  | bit `0x1` fast latch, bit `0x8` detour pending, mask `0xF0` attempt counter bits `0x2` and `0x4` heading gap (`0x0033A570`) |
| `+0x040` | `i32` |  | goal kind (1 unit, 2 unit with margin) |
| `+0x060` | `f32[4][4]` |  | the four positions the context copies |
| `+0x0D0` | `f32` |  | stop radius |
| `+0x0D8` | `f32` | speed |  |
| `+0x0DC` | `f32` | desired heading |  |
| `+0x0F4` | `f32` | pitch |  |
| `+0x0E0` | `f32` | current heading |  |
| `+0x0E4` | `f32` |  | turn rate moving |
| `+0x0E8` | `f32` | turn rate standing |  |
| `+0x0EC` | `f32` |  | slow turn rate |
| `+0x0F0` | `f32` | fast turn rate |  |
| `+0x0F8` | `f32` | speedA |  |
| `+0x0FC` | `f32` | speedB |  |
| `+0x104` | `f32` | speed threshold |  |
| `+0x108` | `f32` |  | step scale (2.0 floor) |
| `+0x10C` | `f32` | collision radii | with `+0x110` |
| `+0x110` | `f32` | collision radii | with `+0x10C` |
| `+0x118` | `f32` | heading cap |  |
| `+0x120` | `f32` | reach values | with `+0x124` and `+0x128` |
| `+0x124` | `f32` | reach values | with `+0x120` and `+0x128` |
| `+0x128` | `f32` | reach values | with `+0x120` and `+0x124` |
| `+0x12C` | `f32` | orbit length |  |
| `+0x130` | `i32` | sidestep odds |  |
| `+0x140` | `f32[3]` | direction |  |
| `+0x150` | `u32` | target handle |  |
| `+0x160` | `i32` | goal kind |  |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x0033A570` | `...` |  | reads `+0x150`-`+0x158` as a point for goal kind 1 and `+0x150` as an angle for goal kind 2 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x170` | `u32` |  | flags (unit `+0x1F0`): bit `0x1` speedA, bit `0x2` speedB, mask `0x1C` the fast-latch condition, bit `0x200` |
| `+0x174` | `u8` |  | mover class (unit `+0x1F4`) |
| `+0x176` | `u8` | bit 0x4 detours allowed |  |
| `+0x177` | `u8` | slot |  |

Solver context (stack, `0x110` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `...` |  | position (block `+0x60`) |
| `+0x010` | `...` |  | step point (`+0x70`) |
| `+0x020` | `...` |  | route goal (`+0x80`) |
| `+0x030` | `...` |  | destination (`+0x90`; the step and spacing distances) |
| `+0x040` | `...` |  | target position |
| `+0x050` | `...` |  | detour point |
| `+0x060` | `...` |  | leader position |
| `+0x0A0` | `...` | radius |  |
| `+0x0A4` | `...` |  | target radius |
| `+0x0A8` | `...` |  | target bearing |
| `+0x0AC` | `...` |  | stop distance |
| `+0x0B0` | `...` |  | speed out |
| `+0x0B4` | `...` |  | desired heading |
| `+0x0B8` | `...` | pitch |  |
| `+0x0BC` | `...` |  | limited heading |
| `+0x0C0` | `...` |  | step scale |
| `+0x0C8` | `...` |  | distance to the route goal, or to the target |
| `+0x0CC` | `...` |  | flags copy (bit `0x80`, bit `0x400` detour) |
| `+0x0D0` | `...` |  | bit `0x1` leader reachable |
| `+0x0E0` | `...` |  | target actor |
| `+0x0E8` | `...` |  | leader actor |
| `+0x0F0` | `...` | unit |  |
| `+0x0F8` | `...` |  | target unit |
| `+0x100` | `...` |  | the block; with `+0x108` |
| `+0x108` | `...` |  | the block; with `+0x100` |

## Shipped data

| Constant | Value | Role |
|---|---|---|
| `0.785398`, `2.0944`, `0.349066` | 45, 120, 20 degrees | the turn limiter's entry, escalation and release |
| `1.0471976`, `2.617994`, `2.3561945` | 60, 150, 135 degrees | the mode 1 easing band, the detour and finalise thresholds |
| 7, 5, 3, 1.5; 0.25 | the arrival divisors; the leader-distance factor, a multiplier | by class, goal and fleeing |
| 0.99 | the overshoot guard | |
| 60 | frames | the stall counter's limit |
| 5.0 (`0x009146E4`), 0.5 (`0x01CEBB70`), 3.0 (`0x008F311C`) | | the detour range and the pair margins |
| `0x3FB4FDF4` = 1.414 | | the navigation radius factor |
| `move_support` (`0x02EBF010`) | 120 rows; caps 1.5 (6 rows), 2.0 (102), 2.5 (12); one narrow row (map 311); map 290 listed twice, the first row (1.5) wins; every row is in [move-support.tsv](move-support.tsv) | the heading search field row |
| `0x01EED4C0`, by byte `+0x175` | 0: above 120 degrees mode 3, below 90 (45 in the fast band) mode 2, else 1; 1: always 1; 2 and 4: always 2; 3: above 45 mode 3, else 2; 5: below 30 mode 1, else 2; 6: above 0.01 rad mode 3, else 2; 7: 2, or 1 in the slow band; the halves for flag bit `0x8` are identical | the steering mode table |

### Columns of move-support.tsv

| Column | Holds |
|---|---|
| `narrow_fan` | `yes` when bit `0x1` of the row's byte `+0x04` is set, so the heading search uses the narrow fan; only the row of map 311 has it, and the other 119 rows are empty |
| `used` | `yes` when the row is the first with its map id, which is the row the heading search takes; `no: an earlier row has this map` on the one later row of map 290 |

## Operations

Each navigation step: route, follow, refresh the flag bits `0x1`, `0x2`, `0x8` and `0x10`, solve. The solver
builds its
context, picks its variant, computes the step distance, runs the recoveries, then either the
spacing pass or the heading constraint or the running steering mode, and finalises. The results go
back into the block and the unit, and the movement step page's driver turns them into motion.

## State

The locomotion block's flag word, headings, rates, counters and reach values; the context is
rebuilt every step. Three recovery bodies draw from the C runtime `rand()` (IAT `0x008C3098`), the
process-wide stream, so a detour is not reproducible from the game's own generators.

The circling formation keeps its centre at `0x022C7CF0` as four floats: `0x022C7CF0`, `0x022C7CF4` and `0x022C7CF8` take the
x, y and z of the sampled enemy's position through the three pointer arguments of `0x00265020`, which copies them from
`[actor+0xB8]` or writes 0 without a position (`0x00265041`-`0x00265059`), and `0x022C7CFC` stays 0. The mode 2 sampler
`0x00337C10` takes them from an enemy of mode 5, and the mode 1 sampler `0x00337D90`, called by the mode 1 body `0x0033DFD0`
(`0x0033E000`), from an enemy of mode 4. The area initialisation `0x0033A380` clears the 0x30 bytes
`0x022C7CE0`-`0x022C7D0F`.

The mode 1 and mode 3 bodies drive formations of their own with six more words of the block, which `0x0033A380` clears
with its first two 8-byte stores (`0x0033A386`, `0x0033A38D`). While `0x022C7D04` bit `0x1` is clear the mode 1 body
`0x0033DFD0` runs `0x00337D90` (`0x0033E000`): once a frame when an enemy in mode 4 exists, and on every call when none
does, as the sampler sets the bit only after finding one (`0x00337E47`, `0x0033811C`).

That sampler counts the enemies in mode 1 into `0x022C7CEA` (`0x00337DAB`,
`0x00337E17`), takes the centre from the enemy in mode 4, and runs the phase byte `0x022C7CE6` on the frame count `0x022C7CE4`,
which it lowers by one a call while it is above 0 (`0x00338115`):

- phase 0: the count becomes `150 x [0x01DFE0B4] + rand() % (150 x [0x01DFE0B4])` frames (`0x0033801D`, `0x0033804D`), and one word store
  makes the phase 1 and `0x022C7CE7` 0 (`0x00338033`); the call then goes on as in phase 1;
- phase 1: the angle `0x022C7CE0` advances by `2pi x 2 / (30 x [0x01DFE0B4] x 13.823)` radians (`0x01CEBC78`, `0x01CEBC08`, `0x00D10B10`),
  negated while `0x022C7CEC` is set (`0x003380BC`); at a count of 0 the phase becomes 2 with 15 frames (`0x00338063`, `0x0033806A`),
  and while the mode 4 enemy's order word `+0x714` is `0x13` it becomes 3 with `90 x [0x01DFE0B4]` frames (`0x00338082`, `0x00338089`);
- phase 2, a pause: at a count of 0 `0x022C7CE7` goes from 0 to 1 with `30 x [0x01DFE0B4]` frames (`0x00338002`, `0x00338008`) and from 1
  to 2 with half that (`0x00337FEB`, `0x00337FE4`); from 2 the phase returns to 0 and `0x022C7CEC` flips (`0x00337FC5`, `0x00337FCE`);
- phase 3: the centre is sampled again (`0x00337EFB`); while `0x022C7CE7` is 0 (`0x00337F00`) the angle advances by twice the
  phase 1 step, and the phase stays 3 while the order word is `0x13` and becomes 0 otherwise (`0x00337F3A`).

By address, `0x00337D90()` first stores 0 in `0x022C7CEA` (`0x00337DAB`) and walks the `0x00236850()` entries of
`0x00321170(i)`. An entry counts only when the unit is not null, its stats record `+0x698` is not null and has byte
`+0x05` equal to 1, and `0x003125E0(unit)` answers 0 (`0x00337DB2`-`0x00337DFB`). Of those, each unit with a definition
`+0xE68` (tested for null) of mode 1 adds one to `0x022C7CEA`, and the last one of mode 4 is the enemy the rest uses
(`0x00337DFD`-`0x00337E3D`).

With no entries or no mode 4 enemy the sampler returns there: the phase, the angle, the frame count and `0x022C7D04`
stay as they were (`0x00337DBC`-`0x00337DBE`, `0x00337E44`-`0x00337E47`).

The centre `0x022C7CF0` is `0x00265020(actor, 0x022C7CF0, 0x022C7CF4, 0x022C7CF8)` with the actor `0x003588B0(enemy dword +0x08)`:
three dwords, with `0x022C7CFC` not written. It is taken under the counter byte `0x022C7D00`. While the enemy's float
`+0x158` compares equal to 0.0 the counter is set to `0xFF` and the centre is taken. Otherwise a counter of `0xFF`
becomes 15 and the centre is not taken; a counter above 0, signed, becomes `counter - 1` and the centre is taken only
when that is 0 or below; a counter of 0 or below takes the centre (`0x00337E4D`-`0x00337EAC`).

The phase byte `0x022C7CE6` picks the rest (`0x00337EB1`-`0x00337ED5`); a value above 3 goes straight to the end. Phase 0
calls the import `[0x008C3098]()` and stores the word 1 at `0x022C7CE6`: that word makes the phase 1 and `0x022C7CE7` 0. It
then stores the count and goes on as phase 1 (`0x0033801D`-`0x0033804D`); a dword `[0x01DFE0B4]` of 0 gives the `div ecx` at
`0x0033803C` a zero operand.

Phase 1 tests the count first and the order word after it, so an order word of `0x13` wins over a count of 0, and it
adds the angle step to `0x022C7CE0` on every call, also on the call that moves the phase (`0x00338014`-`0x003380E9`).

Phase 2 acts only on a count of 0 (`0x00337F93`-`0x00337F9B`): `0x022C7CE7` 0 becomes 1 with a count of
`30 x word [0x01DFE0B4]`; 1 becomes 2 with `(30 x dword [0x01DFE0B4]) >> 1`; 2 makes the phase 0 and `0x022C7CEC`
`(old - 1) & 1`; any other value changes nothing (`0x00337FA1`-`0x0033800F`).

Phase 3 takes the centre again, `0x003588B0(enemy dword +0x08)` and `0x00265020(actor, 0x022C7CF0, 0x022C7CF4, 0x022C7CF8)`
(`0x00337EDB`-`0x00337EFB`). With `0x022C7CE7` not 0 it changes neither the phase nor the angle; otherwise the phase stays 3
for an order word of `0x13` and becomes 0 for any other, and `2 * step` goes onto `0x022C7CE0` on that call too
(`0x00337F00`-`0x00337F86`).

Every call that found a mode 4 enemy ends the same way: the angle `0x022C7CE0` becomes `0x0033CB70(angle)`, a count other
than 0 becomes `count - 1`, and bit `0x1` of `0x022C7D04` is set (`0x003380F1`-`0x0033811C`).

The body then places each mode 1 unit. Unit `0x022C7CE9` of the `0x022C7CEA` (`0x0033E02B`, `0x0033E005`) stands at the angle
`0x022C7CE0 + place x 2pi / count`, 0 apart with one unit, 2.2 from the centre (`0x00D10AF0`), and in phase 3 at 1.2 plus
`0x022C7CE4 / (90 x [0x01DFE0B4])` (`0x0033E04A`, `0x0033E067`, `0x008FCC90`). In phase 3 with `0x022C7CE7` at 1 its limited heading turns
by 0.4189 radians a call, the sign from `0x022C7CEC` (`0x0033E14A`, `0x0033E153`, `0x0033E164`, `0x0091602C`).

By address: while the byte `0x022C7D04` has bit `0x1` clear `0x0033DFD0` first calls `0x00337D90()` (`0x0033DFF4`-`0x0033E000`).
The place angle is `0x0033CB70(a)` with `a = place x (2pi / count) + [0x022C7CE0]`, the first term 0 for a count of 0 or
1, an unsigned test (`0x0033E005`-`0x0033E045`). The radius `r` is `[0x00D10AF0]`, 2.2, outside phase 3, the byte `0x022C7CE6`
equal to 3; in phase 3 it is `(float) [0x022C7CE4] / (float) (90 x [0x01DFE0B4]) + [0x008FCC90]`, a word over a dword
product, the last being 1.2 (`0x0033E04A`-`0x0033E088`).

The goal: `0x00202FE0(v, 0x01F004C0, r)` is given the axis `{0, 0, 1.0}` and the radius; `0x00203170(m)` and
`0x00202F00(m, m, 0x0033CB70(angle))` build the turn about y; `0x00202B70(v, m, v)` turns the vector; and
`0x00202B10(ctx + 0x20, 0x022C7CF0, v)` stores centre plus vector as the goal `+0x20`, whose 16 bytes are then copied to
the destination `+0x30` (`0x0033E090`-`0x0033E0EE`).

The speed `+0xB0` is `min(0x00339BF0(ctx), 0x004686D0(ctx + 0x20, ctx))` (`0x0033E0F3`-`0x0033E117`), and the desired heading
`+0xB4` is `0x004687F0(g)` with `g` the goal minus the position, `0x00203080(g, ctx + 0x20, ctx)` (`0x0033E11F`-`0x0033E135`).

For the limited heading it first takes the position minus the centre, `0x00203080(g, ctx, 0x022C7CF0)`
(`0x0033E12E`-`0x0033E145`). In phase 3 with the byte `0x022C7CE7` at 1 the heading is
`0x0033CB70([ctx+0xBC] + k x [0x0091602C])`, `k` being 1 while the byte `0x022C7CEC` is not 0 and -1 otherwise
(`0x0033E14A`-`0x0033E185`). In every other case it is `0x00334120(e0, 0x004687F0(g), e8)` with `e0` and `e8` the block's
floats `+0xE0` and `+0xE8`, read through the context's block pointer `+0x108` (`0x0033E18C`-`0x0033E1B7`).

Either heading is stored at `+0xBC`, and the place byte becomes `[0x022C7CE9] + 1` (`0x0033E1BC`-`0x0033E1C4`). `0x0033DFD0`'s
own instructions store nothing at the pitch `+0xB8`.

The mode 3 body `0x0033DB60` drives one walk on the same count and phase words, lowering `0x022C7CE4` by one a call while
it is above 0 (`0x0033DCFB`-`0x0033DD0F`), and branches on the phase `0x022C7CE6` (`0x0033DD16`-`0x0033DD3F`).

Its desired heading `+0xB4` is the bearing to a point 11 (`0x00915B9C`, `0x004692F0`) from field point `0x20`
(`0x00320940(0x20)`, `0x0033DB8C`-`0x0033DBC3`), on the line from that point to the unit (`0x00203080`, `0x0033DBCA`) turned by
0.0091 radians, one way while `0x022C7CE7` is 0 and the other way otherwise (`0x00D10ACC`, `0x00D10B14`; `0x0033CB70`,
`0x00203170`, `0x00202F00`, `0x00202B70`, `0x0033DBD8`-`0x0033DC29`), level, placed with `0x00202B10` and taken as a bearing with
`0x00203080` and `0x004687F0` (`0x0033DC2E`-`0x0033DC70`).

The bearing of the unturned line (`0x004687F0`, `0x0033DBD3`) is not used, and the pitch `+0xB8` is set to 0 (`0x0033DC7A`).

`0x022C7CE8` is read after that store: its quarter turns, times 90 degrees through `0x0033CB70`, turn the axis `0x01F004C0`
about y (`0x00203170`, `0x00202F00`, `0x00202B70`) to place a second point 11 from the field point (`0x004692F0`, `0x00202B10`,
`0x0033DC80`-`0x0033DCF6`), which phase 2's distance test reads (`0x0033DDE5`-`0x0033DDF8`).

Phases 1, 3 and 4 set the speed `+0xB0` as a share of the full speed, `+0xF8` of the context's block `+0x108`, over 60
(`0x008F6D54`); phase 0 stores 0 and phase 2 the full speed, and a phase above 4 sets no speed and goes to the end store
(`0x0033DD3C`-`0x0033DD3F`). The test reads the context's own unit `+0xF0`: it passes while that unit's order word
`+0x714` is `0x21F` or above or is `0x96`, or its `+0x76C` less its `+0x768` is 6000 or more:

- phase 0 (`0x0033DECD`-`0x0033DF73`): `+0xB0` = 0 (`0x0033DED9`); when the test passes and the count `0x022C7CE4` is 0
  (`0x0033DEDF`-`0x0033DF0F`), `rand()` (`[0x008C3098]`) decides whether `0x022C7CE7` flips (`0x0033DF11`-`0x0033DF34`),
  `0x022C7CE8` steps one quarter turn, up while `0x022C7CE7` is 0, wrapping from below 0 to 3 and from 4 to 0
  (`0x0033DF3A`-`0x0033DF61`), and the phase becomes 1 with 60 frames (`0x0033DF67`-`0x0033DF73`);
- phase 1 (`0x0033DE84`-`0x0033DEC8`): `+0xB0` = `(60 - count) / 60` of full, and phase 2 at a count `0x022C7CE4` of 0;
- phase 2 (`0x0033DDDE`-`0x0033DE7F`): `+0xB0` = full speed (`0x0033DDEF`); when the distance `0x004686D0` returns to the
  second point is below 30 frames of travel at full speed (`0x01CEBB70`, `0x0033DDF8`-`0x0033DE24`) the phase becomes 3 with
  60 frames (`0x0033DE26`, `0x0033DE2D`), and when the test fails it becomes 4 with 60, after the change to 3 if both hold
  (`0x0033DE34`-`0x0033DE7F`, `0x0033DF73`);
- phase 3 (`0x0033DD8E`-`0x0033DDD9`): `+0xB0` = `count / 60` of full; at a count `0x022C7CE4` of 0 the phase returns to 0
  with the count `0x02EC0F80`, `240 x [0x01DFE0B4]`;
- phase 4 (`0x0033DD45`-`0x0033DD89`): the same slowing of `+0xB0`; at a count `0x022C7CE4` of 0 phase and count return to
  0.

After the phase it stores at the limited heading `+0xBC` the bearing from the unit to the field point (`0x00203080`,
`0x004687F0`, `0x0033DF7A`-`0x0033DF93`).

The six words:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C7CE4` | `u16` | 0 (zero-filled tail) | the frame count of the mode 1 and mode 3 phases | `0x00337D90` (`0x00337FE4`, `0x00338008`, `0x0033804D`, `0x0033806A`, `0x00338089`; one less at `0x00338115`); `0x0033DB60` (`0x0033DD0F`, `0x0033DD82`, `0x0033DDCB`, `0x0033DE26`, `0x0033DF73`); `0x0033A380`, 0 (`0x0033A386`) | `0x00337D90` (`0x00337F93`, `0x00338054`, `0x003380FE`); `0x0033DB60` (`0x0033DCFB`, `0x0033DD6E`, `0x0033DDB7`, `0x0033DEB4`, `0x0033DF08`); `0x0033DFD0` (`0x0033E067`) |
| `0x022C7CE6` | `u8` | 0 (zero-filled tail) | the phase: 0 to 3 for mode 1, 0 to 4 for mode 3 | `0x00337D90` (`0x00337F3A`, `0x00337FC5`, `0x00338033` as the low byte of a word store of 1, `0x00338063`, `0x00338082`); `0x0033DB60` (`0x0033DD7B`, `0x0033DDD2`, `0x0033DE2D`, `0x0033DE78`, `0x0033DEC1`, `0x0033DF6C`); `0x0033A380`, 0 (`0x0033A386`) | `0x00337D90` (`0x00337EB1`, `0x00337F18`); `0x0033DB60` (`0x0033DD16`); `0x0033DFD0` (`0x0033E04A`, `0x0033E14A`) |
| `0x022C7CE7` | `u8` | 0 (zero-filled tail) | mode 1's pause step, 0 to 2; mode 3's turn sense, 0 or 1 | `0x00337D90` (`0x00337FEB`, `0x00338002`; 0 with the word store at `0x00338033`); `0x0033DB60` (`0x0033DF34`); `0x0033A380`, 0 (`0x0033A386`) | `0x00337D90` (`0x00337F00`, `0x00337FA1`); `0x0033DB60` (`0x0033DBD8`, `0x0033DF27`); `0x0033DFD0` (`0x0033E153`) |
| `0x022C7CE8` | `i8` | 0 (zero-filled tail) | mode 3's direction in quarter turns, 0 to 3 | `0x0033DB60` (`0x0033DF4F`, `0x0033DF61`); `0x0033A380`, 0 (`0x0033A38D`) | `0x0033DB60` (`0x0033DC80`, `0x0033DF3A`) |
| `0x022C7CEA` | `u8` | 0 (zero-filled tail) | the count of enemies in mode 1, taken again each sampler call | `0x00337D90`, 0 (`0x00337DAB`) and one more per unit (`0x00337E17`); `0x0033A380`, 0 (`0x0033A38D`) | `0x0033DFD0` (`0x0033E005`) |
| `0x022C7CEC` | `u8` | 0 (zero-filled tail) | mode 1's turn direction: the angle goes backwards while it is set | `0x00337D90`, flipped as the pause ends (`0x00337FCE`); `0x0033A380`, 0 (`0x0033A38D`) | `0x00337D90` (`0x00337F4D`, `0x00337FBC`, `0x003380BC`); `0x0033DFD0` (`0x0033E164`) |

The two rows below give every access to the two globals, including the reads and writes in the callees the code
passes their addresses to; no image-base-relative reference or disp32 displacement names either global.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C7CF8` | `f32` | 0 (zero-filled tail) | the z of the formation centre, the third float of `0x022C7CF0` | `0x0033A380`, 0 (`0x0033A39B`); `0x00265020` through its fourth argument (`0x0026504E`, `0x00265059`), passed by `0x00337C10` (`0x00337CEA`, `0x00337D2D`) and `0x00337D90` (`0x00337E94`, `0x00337EE3`) | through the address `0x022C7CF0`: `0x00202B10` (`0x00202B2D`), which adds the centre to a unit's goal offset, from `0x0033D890` (`0x0033DA35`) and `0x0033DFD0` (`0x0033E0E2`); `0x00203080`, which subtracts, at `0x0020309D` when `0x0033D890` calls it (`0x0033DB0F`) and at `0x002030A2` when `0x0033DFD0` calls it (`0x0033E145`) |
| `0x022C7D08` | `u8[8]` | 0 (zero-filled tail) | read by no instruction; nothing fixes its width | `0x0033A380`, 0 with the block (`0x0033A3A9`) | no instruction |

## Modding notes

- The step is quadratic in the remaining distance; the seven constants are one curve with a
  divisor, not seven speeds. Keep the `0.99` guard or units overshoot.
- The limiter is history-dependent: the same error turns fast or slow depending on whether the
  unit passed through 120 degrees. The fast rate also needs the three latch bits.
- Keep the direction pair mutually exclusive and the snap-on-arrival; a port that steps by the
  rate unconditionally orbits the target.
- Avoidance and detours use the CRT generator.
- The stack arguments of the forward clearance and obstruction probes are at the callee's
  `+0x28`/`+0x30`; every non-zero result is a literal 1 or 2, never a probe's own value.
- The mode byte is re-read inside the probes; a port that caches it once is not equivalent.

## Related

- [Navigation mesh and pathfinding](navigation-mesh-and-pathfinding.md): the route and the obstacle grid.
- [Movement step](heading-speed-to-position-delta.md): the driver that moves the unit.
- [Battle unit fields](../Characters-And-Objects/battle-unit-fields.md): the locomotion block in the unit.
- [Battle orders](../Battle-Actions/battle-orders.md): the order ids the decoder reads.
- [Random number generators](../Random-Numbers/random-number-generators.md): the CRT stream.
- [`navigation-mesh-corridor-agent-accesses.tsv`](navigation-mesh-corridor-agent-accesses.tsv): every access to the
  solver context, followed from its builder `0x00336710`, one row per instruction (67 rows).
- [`battle-locomotion-angle-accesses.tsv`](battle-locomotion-angle-accesses.tsv): the accesses to the
  locomotion block (unit `+0x80`) and the solver context in the navigation step, the builder and the solvers, one
  row per instruction (490 rows).

In the corridor table, `function`, `name` and `site` give the function, its name and the instruction's address,
`disp` the offset the instruction reaches from the start of the solver context, `kind` a read (`r`), a write (`w`)
or both (`rw`), `instruction` the instruction itself, and `route` `ctor-seeded 0x00336710`: the context as the builder
receives it and passes it on to the functions it calls.

In the locomotion table, the same columns hold the same, with `disp` an offset in the locomotion block or, written
`ctx+`, in the solver context. `route` follows the pointer from where the function got it to the instruction, hop by
hop:

- `ctx-builder`, `solver`, `solve-entry` and `setter`: inside the builder `0x00336710`, the solvers `0x003394A0` and
  `0x0033BED0`, the solvers `0x00336CE0` and `0x0033A240` (`arg1`: through the second argument) and `0x003DB130`, through
  the pointers they receive;
- `ctx-stack-K`: the context is the function's own local at `rsp + 0x20`, read through `rsp` (K is the frame size
  the function's prologue subtracts from `rsp`, less 0x20); `ctx-stack@S`: the call at S passes that local;
- `backtrace F->arg0 mov`: the register the function passes to F as its first argument, traced back to the `mov`
  that set it; `<rdef`: the instruction uses that `mov`'s source register instead;
- `argN@S`: passed on as argument N (0 = `rcx`, 1 = `rdx`, 2 = `r8`) by the call at S; `st@S`: the block pointer
  loaded from the context's `+0x100` or `+0x108` at S; `+slot`: kept in a stack slot;
- `note`: the nine rows that reach neither, the stack slots and home-space saves and two pointers to other objects,
  each with what it reaches instead.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Input: `0x003590D0` is called by `0x00226BE0`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md).
- World area: `0x003590D0` is called by `0x0025E400`, `0x002623A0`; those functions are documented on
  [actor record fields](../Characters-And-Objects/actor-record-fields.md),
  [frame update order](../Engine-Core/frame-update-order.md).
