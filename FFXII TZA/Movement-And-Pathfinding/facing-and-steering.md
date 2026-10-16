---
title: "Facing and steering: how a character turns, the steering request and its two slots, scripted moves and turns, and what resumes after a cutscene"
kind: "system"
category: "Movement and pathfinding"
addresses: "0026B5A0, 0026B620, 0026B6A0, 0026C090, 002E5E10, 002E5F90, 002E5FB0, 00265200, 0026A0D0, 0026A060, 0026AE90, 002E45E0, 002E55C0, 0026AE30, 0026ADF0, 0026B450, 0026A640, 00269C30, 0026AF10, 00357A20, 00357980, 0026C120, 002E5750, 002690D0, 0026C330, 0026C300, 002E60C0, 003A1C50, 003A19C0, 003A1AD0, 002EBE50, 002E8EE0, 002EC3F0, 002EC2C0, 002EBFA0, 002EC140, 002EC1C0, 002EC380, 0026A8E0, 0026A870, 0026A950, 0026AAD0, 002E5B60, 002E5B90, 0026A1A0, 00269F90, 002627C0, 002EAB80, 002EAAA0, 00263230, 00263050, 0026AFE0, 003EC040, 002EA780, 00263CC0, 00265600, 00264460, 0025DF00, 003A1BB0, 0026D630, 00265580"
---

## What the player sees

Point Vaan at something behind him and he turns the short way round. The direction, left or
right, is chosen once when the new heading is set and then spent over the following frames at
nine degrees a frame. Which way a character is pointing and which way it is travelling are
separate numbers: a party member can back away from a foe while facing it, and a pivot looks
like a pivot rather than a slide.

A scripted walk has a speed and, optionally, a ramp: constant, accelerating from the start,
decelerating into the target, or both. The walk ends when the character is within one frame's
travel of its goal, measured flat on the ground for a walker and in three dimensions for a flier.

A cutscene, a conversation or any script that takes an actor interrupts whatever it was doing,
and when the script ends the actor goes back to its walk. It can, because every steerable
character carries two complete steering states and the engine flips between them: one is handed
to the interruption, the other keeps the walk. The depth is exactly one; a second interruption
while one is outstanding does nothing.

## How it works

### Three angles and two wraps

Only a class-3 actor (`(byte +0x03 & 0xE0) == 0x60`) steers; every setter below returns silently
for any other class. Its movement context at `+0xB8` holds a pitch at `+0xA0`, a desired heading
(yaw) at `+0xA4` and the facing at `+0xA8`. The facing is what the rest of the engine reads:
`00265200` returns `+0xA8` for class 3 and `+0x38` for class 1 (a placed object), 0 otherwise, and
has 37 call sites. The yaw and the pitch drive the step ([movement
step](heading-speed-to-position-delta.md)).

Two normalisers fold an angle into a single turn, and they are different functions:

```
facing wrap (0026A0D0, 0026A060, 0026B5A0, 0026B620, 0026B6A0, 0026C090, 002E5E10, 0026A8E0 ...)
  b = (a >= 0) ? pi : -pi                       pi 01CEBC50, -pi 00915620
  wrapped = ((a + b) - trunc((a + b) / 2pi) * 2pi) - b     2pi 01CEBC78; one pass

loop normaliser (003A1C50, 003A19C0, 003A1AD0)
  while (x < -pi) x += 2pi;  while (x > pi) x -= 2pi;      -2pi 00915624
```

The one-pass form maps an exact `+pi` to `-pi` and back, so the number of wraps on a path decides
the stored sign at the antipode, and it perturbs an in-range value by an ulp or two. The loop form
leaves an in-range value exactly alone and returns the closed interval `[-pi, pi]`; past
`|x| >= 2^27` adding `2pi` no longer changes `x` and it cannot make progress. A reimplementation
must keep each call site's form. `00325E60` is the loop form with the two loops in the other order
(the upper bound first), used by the formation placement `0031BAC0`.

`003A1BB0(facing, half, x0, z0, x1, z1)` is the facing-window test built on the loop form: it takes
`atan2(x1 - x0, z1 - z0) - facing`, folds it with the two loops, and returns whether its magnitude
is below `half`. The talk tests `0025BAD0` (class 3) and `0025BE50` (class 1) use it, and so do the
verbs `isrange(angle, actor)` (`0x0295`, `00346780`) and `isrange_296(angle, x, z)` (`0x0296`,
`00346EF0`), which pass the actor's facing (`00265200`) and half the popped angle.

### Setting the facing

`0026B5A0(actor, angle)` and `0026B620(actor, angle)` are the same 29 instructions but for one:
the first passes mode 0 and the second mode 1 to `0026B6A0(actor, wrapped, mode)`, then both
tail-call `0026C090(actor, wrapped)`. `0026B6A0` wraps again and, for class 1, writes the context's
`+0x38` and `+0x48`; for class 3 it jumps to `002E5FB0(actor, angle, mode)`, which keeps the
context's `+0xAC` and calls the facing writer. `0026C090` wraps once more and writes the steering
record's target heading `+0x34` for class 3, or calls `0026B6A0(actor, angle, 1)` for class 1.

The facing writer `002E5E10(actor, angle, aux, commit)` does nothing without a controller at
`+0xC0`. With one it stores `aux` at `+0xAC`, the wrapped angle at `+0xA8`, copies the angle into
the context's `+0x58` (`003DA850` on `+0x50`), into `+0x78` and `+0x68` unless actor byte `+0x0D`
has bit 5, and, when the controller has a movement body at `+0x138`, into the body's `+0xF8`
followed by a rebuild of the body's placement (`003DAF20` with the context's `+0x104`-`+0x106`).

When the controller's render record id is not -1 it hands `{aux, angle, 0}` to the render record
(`003EC260`), which stages the triple for `commit` = 0 and stages and commits it for 1. So variant
0 stages a facing and variant 1 stages and commits it, a difference only a class-3 actor shows.

`002E5F90(actor, aux, commit)` re-runs the writer with the current facing and a new `+0xAC`.

The yaw setter `0026A0D0` and the pitch setter `0026A060` write their wrapped angle to `+0xA4` and
`+0xA0`. `0026A8E0`, `0026A870` and `0026A950` write the steering record's `+0x70`, `+0x74` and the
context's `+0x224` the same way; `0026AAD0` writes `+0x6C` = `wrapped * [01DFE0BC]`.

### The steering record and its two slots

The context's `+0xF0` is a cursor, not an owning pointer: `00269F90(context)` sets it to
`context + 0x120 + 0x80 * [+0xDC]` when the selector byte `+0xDC` is 0 or 1 and leaves it alone
otherwise. Two `0x80`-byte records live inline at `+0x120` and `+0x1A0`; nothing allocates or
frees them.

`002EAB80(actor)` pushes: for a class-3 actor whose byte `+0x18` is not 1 and whose selector is 0,
`002627C0` copies slot 0 over slot 1, the selector becomes 1, the cursor is re-selected, and the
new slot is handed over clean with `0026AE90(actor, 0)` and `0026C120(actor, 0)`.

`002EAAA0(actor)` pops: with the selector at 1 it becomes 0, the cursor is re-selected first, and
the saved walk is replayed by the shape now under the cursor (slot 0's) in `+0x62` bits 0-2: shape 0 passes the triple at `+0x10` to `002EC2C0` by
address, shape 1 passes `+0x10`, `+0x14`, `+0x18` to `002EBFA0` by value, any other shape resumes
nothing; then `002EC3F0` and `002E8EE0` run. A push while pushed and a pop with nothing pushed do
nothing.

The interruption is a script taking the actor. `00263230(record, 1)` runs when an actor-resource
entry starts script execution. When no script is running on the roster (`02099DB4` at or below 0)
it registers `00226BE0(6, 0, 0, 0, 4, 00377700() != 0)` when `0209A2A8` is set and the record's
byte `+0x0C` is non-negative, and resolves the party focus actor with `02099D70` pointed at slot 0
for the lookup.

The focus actor is then made to look at the starting actor: `002EC2C0` with its position for a
class-1 record, `002EBFA0` with its handle and `0x30B` for class 3, then `002EC380(focus, 2, 6.0)`,
`002EBE50(focus, 1)`, `+0x62` bit 7, `002E8EE0` and `002ED040(focus, 1)`. In every case the script
is counted at the manager's `+0x1E0` and the record's steering pushed (`002EAB80`). A record with a
battle unit also has its speed set to 0 (`0026D6F0(record, 0, 2)`) and `0035AE10(record, 1)`.

`00263050(record, op)` ends it. Op 1 decrements the count and, when none remain, runs
`002E1CD0(1)`, zeroes `02099DE5`, sets `02099DE7` to `0xFF`, calls `00263480(record, 2 when +0x0C
bit 7 is set, else 1)` and, with `0209A2A8` set and `+0x0C` non-negative, `00225CD0(6, 4)`; it then
releases the focus actor's look (`002EBE50(focus, 0, 0)`, `002E8EE0`, `002ED040(focus, 0)`). In
every case it clears record byte `+0x0B` bit 3.

It then pops at once (`0026320A`) unless the record's `+0x1C` bit 17 is set and either `+0x18` is
1 or the entry names a non-negative id (`+0xEA` when not `0xFFFF`, else the word at `+0x24` of the
entry resolved from `+0x40`, which must hold at least `0x12` words). The deferred case sets `+0x0B`
bit 4, and op 4, run on the entry's removal, pops (`00263076`) and clears the bit. Op 3 tail-calls
`0025B500`.

### The steering request

A move verb fills the current slot and starts a steer. `00357A20` (the move-to-position family)
pops four floats: `0026D6A0(actor, speed)` scales the speed by `[01DFE0BC]` into `+0x24` and the
context's `+0xD0`, `0026A640` keeps the raw speed at `+0x7C`, `0026AE30` stores the target
`{x, y, z, 1.0}` at `+0x00` with kind byte `+0x2A` = 0, `0026AF10` snapshots the start position
(context `+0x00`-`+0x0F` to `+0x30`), and `0026AE90(actor, mode)` sets the steering mode: 1 when
`+0x2C` is 0, else `+0x2B`.

`00357980` (the move-to-actor family) does the same with
`0026ADF0(actor, ordinal, manager)` storing an actor target (`+0x2A` = 1; a negative manager index
means the party focus).

`0026AE90(actor, mode)` collapses modes 2-4 to 1 when `+0x2C` is exactly 0.0, stores the mode at
`+0x29`, and for mode 0 clears actor byte `+0x0D` bit 4, cancels (`002E55C0`: `+0x29` = 0,
`0026C120(actor, 0)` when `+0x28 & 0x7F` is 2, `+0x24` and the context's `+0xD0` zeroed) and zeroes
`+0x7C`. It has 13 direct call sites; only the two move handlers hand in a non-zero mode, and
`movecancel`, `ucmovecancel`, the `setpos` family, `setposparty`, the push and the actor teardown
`002693D0` (twice) all hand in 0.

`00269C30(actor, accel, mode)` (`setaccr`) stores `+0x2C` = `accel * [01DFE0BC]` and `+0x2B` =
`mode`; `0026B450` (`setreachr`) stores the reach `+0x20`.

While `+0x29` is non-zero the wait resolver `0025DF00` re-issues `0026D6F0(actor, +0x7C *
[01DFE0BC], ...)` every frame (`0025DF83`), which is why mode 0 zeroes `+0x7C`.

### Steering toward the target

`002E45E0(actor, context)` runs from the movement step's driver when `+0x29` is 1 to 4. Each frame:

1. the target point: kind 0 is the stored position with reach `+0x20`; kind 1 resolves the actor
   (`003587C0`, or `003590D0` → `003588B0` for a negative manager index), reads its position, and
   adds to the reach both bodies' radii (`003DA6A0`: `sqrt(003DA730(a)) + a.+0x5C` for each over the
   two `+0x50` sub-blocks); an unresolvable actor target is the origin;
2. the bearing (`003A19C0`): yaw `atan2(dx, dz)` and pitch `atan2(dy, sqrt(dx^2 + dz^2))`, looped
   into range; the desired yaw `+0xA4` and pitch `+0xA0` each approach them by at most the caps
   `+0x50` and `+0x54` (`003A1AD0`: wrap the difference, step by `min(|diff|, cap)` and snap when
   below the cap);
3. when the manager's skip flag (`00267310(actor +0x15)`) is set, `0026AFE0` places the actor on the
   target at once;
4. the remaining distance is `distance - reach`, three-dimensional (`003A1920`) when `00264460` or
   actor byte `+0x08` bit 2 says so, else flat (`004686D0`);
5. the ramp, with `v = +0x24` and `a = +0x2C`: mode 1 leaves `v`; mode 2 uses the distance from the
   start snapshot `d0`, and when `max(a, d0) < v^2 / 2a` sets `v = max(a, sqrt(2a * max(a, d0)))`;
   mode 3 does the same with the remaining distance; mode 4 both. `v` goes to the context's `+0xD0`
   and `+0xF8`;
6. actor byte `+0x0D` bit 4 (near) is set when `[02164200] * +0x24 > remaining`; `02164200` is 3.0
   at run time: its only writer is the setter `002EBE40`, called by `00266D10` at boot and by the
   verb `debug_charmovestopvelrratio` (`0050D320`);
7. arrival, when `[01DFE0B8] * v > remaining`: for a position target (`+0x2A` = 0) a zero reach
   snaps the actor onto it (`0026AFE0`) and `+0x24`, `+0xD0` and `+0x2C` are zeroed; for every
   target `+0x29` = 0, a movement mode 2 is torn down (`0026C120(actor, 0)`), and `+0x24` and
   `+0xD0` are zeroed again.

The classical `v = sqrt(2 a d)` with `a` floored in keeps a stopping distance from going negative;
the arrival scale makes a 60 fps walk end one frame earlier in distance than a 30 fps one.

### The movement mode and the turn direction

`0026C120(actor, mode)`, 28 direct call sites, reads the old mode byte `+0x28`, stores the new one and:

- mode 0: when `+0x65` is set, `002EBE50(actor, 0, 0)` and `002E8EE0(actor)`; then
  `002E6300(actor, context, old)`, which returns `+0x64` when the old mode had bit 7;
- modes 2 and 3: the turn direction bit, `+0x62` bit 6 set when `wrap(+0x34 - +0xA8)` (`003A1C50`)
  is negative, else cleared; `+0x58` = `pi/20` (`0x3E20D97C`, nine degrees) and `+0x5C` = `pi`
  (`0x40490FDB`), the second a store nothing reads;
- mode 4: the direction bit; then, when the frame count `+0x68` is at most `[01DFE0B4]` (unsigned),
  the facing is set to `+0x34` through `0026B620` and the mode reset to 0;
- any other mode: stored and nothing else.

So a character turns the short way round because the difference is wrapped before its sign is
taken, once, when the mode is set.

### The per-frame integrator

`002E5750(actor, direct)` runs once per actor from the wait resolver (`0025E3AA`) and is skipped
when actor byte `+0x18` is 1 or the controller's `+0x14F` has bit 0. With `direct` non-zero it adds
the two floats of its third argument to the heading and pitch instead. Otherwise it reads the mode
`+0x28 & 0x7F` (`00265600`) and the turn step `+0x58` (`00264750` → `002E4BC0`), floors the step at
`0x3C0EFA35` (half a degree) for any active mode (`0026AC70` → `002E5B90`), and dispatches:

| Mode | Each frame |
|---|---|
| 1 | the facing advances by the spin rate `+0x3C` (`002E60C0`, verb `setvelrotangzx`), through `0026B5A0` |
| 2 | the facing approaches the desired heading `+0xA4` (`00263CC0`) by at most the step (`003A1AD0`), through `0026B5A0` |
| 3 | the facing approaches the target `+0x34`: by the step, or, when `+0x28` bit 7 is set (an untimed turn), by the frame-counted path: first, when `00265510(actor)` is non-zero and `00265530(actor)` is at most the `00265630` index, `0026C070(actor, 0)` and, with a render record, `003DDAD0(actor, controller byte +0x12, 0x1000000)`; then with no render record `003A1AD0` and `0026C300(index + 1)`, with one `003EC040`'s animation-driven step; the skip flag snaps to the target; when the facing equals the target, `0026C120(actor, 0)` |
| 4 | timed interpolation from the start heading `+0x38` to `+0x34`: `t = +0x78 / +0x68`, `heading = start + wrap(target - start) * t`, `+0x78 += 1` (`0026C300`); at `t >= 1`, or when the skip flag forces it, the final heading and `0026C120(actor, 0)` |
| 5 | waits while `002EA780` reports the render record's turn still running (`003E6AF0` and `002EA910` = 1); when it stops, `0026C120(actor, 0)` |

`002EA910` is 1 for an actor without a live render record or without an active entry (`003E6DF0`);
otherwise it returns the render entry's own test `003E2C00` ([character render
records](../Graphics/character-render-records.md)).

`003EC040(id, target, direction, mode)` reads the render record: it returns 0 for a record whose
save block is armed with word `+0x06` set, the record's own `+0x124` for the animation states
`0x35`, `0x36` and `0x0D`, the target unchanged without an active entry, and otherwise steps the
record's `+0x124` toward the target by the entry's rate `+0x24` or `+0x28` scaled by `[01DFE0BC]`.

The remaining angle goes through `003EC510(angle, direction)`, which loops it into range and then,
when non-zero, makes it positive for direction 0 or negative for direction 1 by a full turn, so the
step always goes the chosen way round; `003A1980(a, cap)` is `min(|a|, cap)`, and a remainder below
the rate snaps to the target.

### Untimed and timed turns

`002690D0(actor)` is the untimed turn body behind `raturn`, `raturna`, `raturnya` and their
relatives:

1. it takes the wrapped delta from the facing to `+0x34` and computes a frame count from the step
   (`|delta / +0x58|`, or through `003EBF60` when the render selector `002E9B60()` is not
   negative), scaled by the context's `+0x98` or `+0x9C` (by resume shape 1 or not) and floored
   at 1;
2. it writes the target to `+0x70` (`0026A8E0`) and zeroes `+0x74` and the context's `+0x224`;
3. when the delta is at least `pi/3`, or `+0x65` is set, or the actor has no armed render entry
   (`002E7600` = 0), it takes the body turn: `002EC380(actor, 1, frames)` (bits 3-5 of `+0x62` =
   1, `+0x60` = `frames / [01DFE0BC]`), `+0x28` |= `0x80`, `+0x68` = `(target - facing) / +0x58`
   (the raw difference; only the frame count uses the wrapped one);
4. the body turn goes on with `+0x78` = `[01DFE0B4]`, `+0x64` = 1, `003DDAD0(actor, 0, 0x1000004 -
   direction)` with `direction` = `+0x62` bit 6 as read at entry, and `+0x66` = the curve value;
5. otherwise the animation turn: `002EC380(actor, 2, frames)` and `+0x28` = 5;
6. both end with `002EBE50(actor, 1, 1)`.

`0026C330(actor, frames)` (`turnt`, `rturnt`, `rturnat`, `dira`) sets `+0x68` = `+0x66` =
`[01DFE0B4] + frames / [01DFE0BC]` (0 for a non-positive count) and `+0x78` = `[01DFE0B4]`; its
callers then set mode 4.

### The steer channel and the head

`002EBE50(actor, op, force)` starts or clears the steer channel. Op 0 zeroes the context's `+0xB4`
and `+0x224`. Otherwise, when `+0x63` is 0 or `force` is set, `+0xB4` takes the facing and
`+0x224` 0; the deltas `wrap(+0x70 - +0xB4)` and, with `+0x62` bit 7 clear, `wrap(+0x74 - +0x224)`
are taken; `+0xB4` and `+0x224` become `+0x70` and `+0x74`; and when `+0x62` bits 3-5 are 0 they
become 2 with `+0x60` = `max(1, |delta / +0x6C|)` frames (1 when `+0x6C` is not positive). `+0x63`
= `op`; then `002EC3F0` and `002E8EE0`.

`002E8EE0(actor)` pushes `+0x62` bit 7 (`003E6BD0`) and `+0x63` (`003E6BC0`) into the render record
and sets its `+0x290` bit 11.

`002EC3F0(actor)` stages the head-look request by the shape (bits 0-2) and the selector (bits
3-5) of `+0x62`, with the one-shot latch `+0x6A` bit 0 remapping selector 2 to 1:

- shapes 0-1 go to `002E7650` (selector 1) or `002E79A0` (selector 2);
- shapes 2-3 with selector 1 go to `003E6B90(record, 0, +0x10, +0x14)` and `003E6C00(record, 1,
  id, 0x30B)` for shape 3, else `002E7720`;
- shapes 2-3 with selector 2 go to `003E6B70(record, 1, +0x10, +0x14)` for shape 3, else `002E77F0`
  ([the staged look
  command](../17-Presentation-Rendering/character-rig-and-look.md
)).

The look-at verbs set the shapes:

- `002EC140(actor, a, b)` stores the raw pair at `+0x10`/`+0x14` with shape 2 and writes `+0x70`,
  `+0x74` and `+0x224` from them and runs `0026A9C0(actor, 0)`; `002EC1C0` stores the wrapped pair with shape 3;
- `002EC2C0(actor, vec)` stores a position with shape 0 and sets `+0x70` from the bearing to it,
  `+0x74` and `+0x224` to 0;
- `002EBFA0(actor, ordinal, manager, id)` stores an actor target with shape 1 and its handle at
  `+0x1C`; it falls back to the position form with `0026A1A0(actor, 1)` (bit 7) when the target has
  no render record, and clears the channel (`002E64E0`) when the actor does not resolve.

Shapes 4-7 are never written. `002EC510(shape, actor, target)`, called by the `raturn` verbs
(`0034E710`, `0034EFE0`, `0034F4F0`) and `003578B0`, `0050F6E0`, picks the look-at verb by shape for a
class-3 actor with a movement context: 0 `002EC2C0` with the target as a position, 1 `002EBFA0` with
the target's byte `+0x15` and word `+0x00` and `0x30B`, 2 and 3 `002EC140` and `002EC1C0` with the
float at `+0x04` and 0.

`00263B90(actor, slot)` returns steering slot 0 or 1 (`context + 0x120 + 0x80 * slot`) of a class-3
actor, null for any other; `0026AC00` (verb `sethomingangzx`) runs `002E5B60` for a class-3 actor.

`0026D630` is the class-3 test in front of `002E60C0` for the verb `setvelrotangzx` (`0x003C`,
`003535C0`): the popped float becomes the spin rate `+0x3C` of the selected slot.
`00265580(actor, i)`, behind the verb `getdestrotangzx_227` (`0x0227`, `00341250`), returns the
target heading `+0x34` of slot `i` (`context + 0x154 + 0x80 * i`), with `i` capped at the selector
`+0xDC` and the selected slot for a negative `i`; it returns 0 for any other class.

## Layouts

Movement context (actor +`0xB8`), class 3:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `030` | `f32[4]` | start | snapshot of the position (`0026AF10`) |
| `038` | `f32` | heading of a class-1 object (also +0x48) |  |
| `098` | `f32 / +0x9C f32` | untimed-turn frame scales, by resume shape |  |
| `0A0` | `f32` | pitch | +`0xA4` f32 desired heading (yaw) |
| `0A8` | `f32` | facing | +`0xAC` f32 facing aux (pitch lane of the render triple) |
| `0B4` | `f32` | steer channel heading mirror | +`0x224` f32 steer channel pitch mirror |
| `0DC` | `u8` | slot selector 0 or 1 | +`0xF0` ptr cursor to the selected slot |
| `120` | `SteeringRecord[0]` | +0x1A0 SteeringRecord[1] | `0x80` bytes each |

Struct SteeringRecord size=`0x80`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `f32[4]` | target | position {x, y, z, 1.0}, or {ordinal, manager} for an actor target |
| `10` | `f32[3] resume parameters` | +0x1C u32 resume target handle |  |
| `20` | `f32` | reach (setreachr) | +`0x24` f32 requested speed, scaled |
| `28` | `u8` | movement mode (bit 7 = untimed turn) | +`0x29` u8 steering mode 0-4 |
| `2A` | `u8` | target kind 0 position, 1 actor | +`0x2B` u8 configured ramp mode (setaccr) |
| `2C` | `f32` | ramp acceleration, scaled; 0.0 collapses modes 2-4 to 1 |  |
| `34` | `f32` | target heading | +`0x38` f32 turn start heading |
| `3C` | `f32` | spin rate (mode 1) |  |
| `50` | `f32` | yaw approach cap | +`0x54` f32 pitch approach cap (`002E5B60` / `002E5B90`) |
| `58` | `f32` | turn step, pi/20 | +`0x5C` f32 pi, never read |
| `60` | `i16` | steer channel frames +0x62 u8 flags: bits 0-2 shape, 3-5 selector, 6 direction, 7 initiator |  |
| `63` | `u8` | steer arm state | +`0x64` u8 returned by `002E6300`   +`0x65` u8 teardown gate |
| `66` | `i16` | curve / total frames +0x68 i16 turn frames |  |
| `6A` | `u8` | bit 0 one-shot latch +0x6C f32 initiator turn step |  |
| `70` | `f32` | steer target heading +0x74 f32 steer target pitch |  |
| `78` | `f32` | turn frame index | +`0x7C` f32 raw move speed (re-armed each frame) |

## Shipped data

| Constant | Value | Role |
|---|---|---|
| `0x3E20D97C` | pi/20, 9 degrees | the turn step of modes 2 and 3 |
| `0x3C0EFA35` | pi/360, half a degree | the integrator's floor on the step |
| `1.0471976` | pi/3 | the untimed turn's threshold between a body turn and an animation turn |
| `02164200` | 3.0 at run time | the near-flag multiple of the requested speed |
| `01DFE0B4`, `01DFE0B8`, `01DFE0BC` | 1, 1.0, 1.0 | the time base, the arrival scale, the speed and acceleration scale |

In the shipped scripts `setaccr` is called twice in the whole corpus, so almost every scripted move
runs in ramp mode 1.

## Operations

A scripted move: the verb stores the speed, the target and the start snapshot and sets the ramp
mode; every frame the steer update aims the yaw and pitch, ramps the speed and tests arrival, the
movement step moves the actor, and the resolver re-arms the speed.

A turn: the verb writes the
target heading and the mode, the mode setter chooses the direction, and the integrator advances
the facing each frame until it meets the target and tears the mode down. An interruption: the
script start pushes the slot and hands the clean one over in mode 0; the script's end pops it and
replays the saved walk by its shape.

## State

The context's angles, mirrors and selector; the two steering records; actor bytes `+0x0D` bits 4
and 5, `+0x0B` bits 3 and 4 and `+0x1C` bit 17; the render record's `+0x124`, `+0x284`, `+0x290` and
its staged triple; the globals `02164200` and `02099DB4`.

## Modding notes

- Never store an unwrapped heading: every comparison downstream assumes a single turn. Keep the
  call site's normaliser; the one-pass wrap and the loop disagree on most inputs.
- Hooking one facing variant and not the other changes the render commit on class-3 actors only.
- A steering mode you set may not be the mode that sticks: with `+0x2C` at 0.0 modes 2-4 become 1.
  Call `setaccr` before the move for a ramp.
- `+0x5C` is a dead store; `+0x58` is both the per-frame cap and the divisor of the untimed turn's
  frame count.
- Mode 4's end depends on the Frame Rate setting through `[01DFE0B4]`, and a 60 fps walk arrives
  one frame earlier in distance.
- Writing the selector `+0xDC` directly switches slots; a value above 1 keeps the old cursor.
  Copying `+0x120` over `+0x1A0` copies a whole steering state.
- A look-at (shapes 2 and 3) is not resumed by the pop; only a walk (shapes 0 and 1) is.

## Related

- [Movement step](heading-speed-to-position-delta.md): the driver that runs the steer and the step.
- [Battle locomotion](battle-locomotion.md): the combat steering that feeds the unit's intent.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the resolver that calls the integrator.
- [Actor record](../Characters-And-Objects/actor-record.md): the class byte and the contexts.
- [The staged look command](../17-Presentation-Rendering/character-rig-and-look.md
): the head requests.
