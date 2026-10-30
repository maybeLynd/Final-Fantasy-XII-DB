---
title: "Facing and steering: how a character turns, the steering request and its two slots, scripted moves and turns, and what resumes after a cutscene"
kind: "system"
category: "Movement and pathfinding"
addresses: "0x0026B5A0, 0x0026B620, 0x0026B6A0, 0x0026C090, 0x002E5E10, 0x002E5F90, 0x002E5FB0, 0x00265200, 0x0026A0D0, 0x0026A060, 0x0026AE90, 0x002E45E0, 0x002E55C0, 0x0026AE30, 0x0026ADF0, 0x0026B450, 0x0026A640, 0x00269C30, 0x0026AF10, 0x00357A20, 0x00357980, 0x0026C120, 0x002E5750, 0x002690D0, 0x0026C330, 0x0026C300, 0x002E60C0, 0x003A1C50, 0x003A19C0, 0x003A1AD0, 0x002EBE50, 0x002E8EE0, 0x002EC3F0, 0x002EC2C0, 0x002EBFA0, 0x002EC140, 0x002EC1C0, 0x002EC380, 0x0026A8E0, 0x0026A870, 0x0026A950, 0x0026AAD0, 0x002E5B60, 0x002E5B90, 0x0026A1A0, 0x00269F90, 0x002627C0, 0x002EAB80, 0x002EAAA0, 0x00263230, 0x00263050, 0x0026AFE0, 0x003EC040, 0x002EA780, 0x00263CC0, 0x00265600, 0x00264460, 0x0025DF00, 0x003A1BB0, 0x0026D630, 0x00265580"
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
`0x00265200` returns `+0xA8` for class 3 and `+0x38` for class 1 (a placed object), 0 otherwise, and
has 37 call sites. The yaw and the pitch drive the step ([movement
step](heading-speed-to-position-delta.md)).

Two normalisers fold an angle into a single turn, and they are different functions:

```python
facing wrap (0x0026A0D0, 0x0026A060, 0x0026B5A0, 0x0026B620, 0x0026B6A0, 0x0026C090, 0x002E5E10, 0x0026A8E0 ...)
  b = (a >= 0) ? pi : -pi                       pi 0x01CEBC50, -pi 0x00915620
  wrapped = ((a + b) - trunc((a + b) / 2pi) * 2pi) - b     2pi 0x01CEBC78; one pass

loop normaliser (0x003A1C50, 0x003A19C0, 0x003A1AD0)
  while (x < -pi) x += 2pi;  while (x > pi) x -= 2pi;      -2pi 0x00915624
```

The one-pass form maps an exact `+pi` to `-pi` and back, so the number of wraps on a path decides
the stored sign at the antipode, and it perturbs an in-range value by an ulp or two. The loop form
leaves an in-range value exactly alone and returns the closed interval `[-pi, pi]`; past
`|x| >= 2^27` adding `2pi` no longer changes `x` and it cannot make progress. A reimplementation
must keep each call site's form. `0x00325E60` is the loop form with the two loops in the other order
(the upper bound first), used by the formation placement `0x0031BAC0`.

`0x003A1BB0(facing, half, x0, z0, x1, z1)` is the facing-window test built on the loop form: it takes
`atan2(x1 - x0, z1 - z0) - facing`, folds it with the two loops, and returns whether its magnitude
is below `half`. The talk tests `0x0025BAD0` (class 3) and `0x0025BE50` (class 1) use it, and so do the
verbs `isrange(angle, actor)` (`0x0295`, `0x00346780`) and `isrange_296(angle, x, z)` (`0x0296`,
`0x00346EF0`), which pass the actor's facing (`0x00265200`) and half the popped angle.

### Setting the facing

`0x0026B5A0(actor, angle)` and `0x0026B620(actor, angle)` are the same 29 instructions but for one:
the first passes mode 0 and the second mode 1 to `0x0026B6A0(actor, wrapped, mode)`, then both
tail-call `0x0026C090(actor, wrapped)`. `0x0026B6A0` wraps again and, for class 1, writes the context's
`+0x38` and `+0x48`; for class 3 it jumps to `0x002E5FB0(actor, angle, mode)`, which keeps the
context's `+0xAC` and calls the facing writer. `0x0026C090` wraps once more and writes the steering
record's target heading `+0x34` for class 3, or calls `0x0026B6A0(actor, angle, 1)` for class 1.

The facing writer `0x002E5E10(actor, angle, aux, commit)` does nothing without a controller at
`+0xC0`. With one it stores `aux` at `+0xAC`, the wrapped angle at `+0xA8`, copies the angle into
the context's `+0x58` (`0x003DA850` on `+0x50`), into `+0x78` and `+0x68` unless actor byte `+0x0D`
has bit `0x20`, and, when the controller has a movement body at `+0x138`, into the body's `+0xF8`
followed by a rebuild of the body's placement (`0x003DAF20` with the context's `+0x104`-`+0x106`).

When the controller's render record id is not -1 it hands `{aux, angle, 0}` to the render record
(`0x003EC260`), which stages the triple for `commit` = 0 and stages and commits it for 1. So variant
0 stages a facing and variant 1 stages and commits it, a difference only a class-3 actor shows.

`0x002E5F90(actor, aux, commit)` re-runs the writer with the current facing and a new `+0xAC`.

The yaw setter `0x0026A0D0` and the pitch setter `0x0026A060` write their wrapped angle to `+0xA4` and
`+0xA0`. `0x0026A8E0`, `0x0026A870` and `0x0026A950` write the steering record's `+0x70`, `+0x74` and the
context's `+0x224` the same way; `0x0026AAD0` writes `+0x6C` = `wrapped * [0x01DFE0BC]`.

### The steering record and its two slots

The context's `+0xF0` is a cursor, not an owning pointer: `0x00269F90(context)` sets it to
`context + 0x120 + 0x80 * [+0xDC]` when the selector byte `+0xDC` is 0 or 1 and leaves it alone
otherwise. Two `0x80`-byte records live inline at `+0x120` and `+0x1A0`; nothing allocates or
frees them.

`0x002EAB80(actor)` pushes: for a class-3 actor whose byte `+0x18` is not 1 and whose selector is 0,
`0x002627C0` copies slot 0 over slot 1, the selector becomes 1, the cursor is re-selected, and the
new slot is handed over clean with `0x0026AE90(actor, 0)` and `0x0026C120(actor, 0)`.

`0x002EAAA0(actor)` pops: with the selector at 1 it becomes 0, the cursor is re-selected first, and
the saved walk is replayed by the shape now under the cursor (slot 0's) in `+0x62` bits `0x7`: shape 0 passes the triple at `+0x10` to `0x002EC2C0` by
address, shape 1 passes `+0x10`, `+0x14`, `+0x18` to `0x002EBFA0` by value, any other shape resumes
nothing; then `0x002EC3F0` and `0x002E8EE0` run. A push while pushed and a pop with nothing pushed do
nothing.

The interruption is a script taking the actor. `0x00263230(record, 1)` runs when an actor-resource
entry starts script execution. When no script is running on the roster (`0x02099DB4` at or below 0)
it registers `0x00226BE0(6, 0, 0, 0, 4, 0x00377700() != 0)` when `0x0209A2A8` is set and the record's
byte `+0x0C` is non-negative, and resolves the party focus actor with `0x02099D70` pointed at slot 0
for the lookup.

The focus actor is then made to look at the starting actor: `0x002EC2C0` with its position for a
class-1 record, `0x002EBFA0` with its handle and `0x30B` for class 3, then `0x002EC380(focus, 2, 6.0)`,
`0x002EBE50(focus, 1)`, `+0x62` bit `0x80`, `0x002E8EE0` and `0x002ED040(focus, 1)`. In every case the script
is counted at the manager's `+0x1E0` and the record's steering pushed (`0x002EAB80`). A record with a
battle unit also has its speed set to 0 (`0x0026D6F0(record, 0, 2)`) and `0x0035AE10(record, 1)`.

`0x00263050(record, op)` ends it. Op 1 decrements the count and, when none remain, runs
`0x002E1CD0(1)`, zeroes `0x02099DE5`, sets `0x02099DE7` to `0xFF`, calls `0x00263480(record, 2 when +0x0C
bit 0x80 is set, else 1)` and, with `0x0209A2A8` set and `+0x0C` non-negative, `0x00225CD0(6, 4)`; it then
releases the focus actor's look (`0x002EBE50(focus, 0, 0)`, `0x002E8EE0`, `0x002ED040(focus, 0)`). In
every case it clears record byte `+0x0B` bit `0x8`.

It then pops at once (`0x0026320A`) unless the record's `+0x1C` bit `0x20000` is set and either `+0x18` is
1 or the entry names a non-negative id (`+0xEA` when not `0xFFFF`, else the word at `+0x24` of the
entry resolved from `+0x40`, which must hold at least `0x12` words). The deferred case sets `+0x0B`
bit `0x10`, and op 4, run on the entry's removal, pops (`0x00263076`) and clears the bit. Op 3 tail-calls
`0x0025B500`.

### The steering request

A move verb fills the current slot and starts a steer. `0x00357A20` (the move-to-position family)
pops four floats: `0x0026D6A0(actor, speed)` scales the speed by `[0x01DFE0BC]` into `+0x24` and the
context's `+0xD0`, `0x0026A640` keeps the raw speed at `+0x7C`, `0x0026AE30` stores the target
`{x, y, z, 1.0}` at `+0x00` with kind byte `+0x2A` = 0, `0x0026AF10` snapshots the start position
(context `+0x00`-`+0x0F` to `+0x30`), and `0x0026AE90(actor, mode)` sets the steering mode: 1 when
`+0x2C` is 0, else `+0x2B`.

`0x00357980` (the move-to-actor family) does the same with
`0x0026ADF0(actor, manager, number)` storing an actor target: the running manager slot's index
(`+0x28`, `0x003579CB`) at `+0x00`, the popped actor number at `+0x04` (`0x0026AE08`, `0x0026AE11`) and
`+0x2A` = 1; a negative actor number means the party focus.

`0x0026AE90(actor, mode)` collapses modes 2-4 to 1 when `+0x2C` is exactly 0.0, stores the mode at
`+0x29`, and for mode 0 clears actor byte `+0x0D` bit `0x10`, cancels (`0x002E55C0`: `+0x29` = 0,
`0x0026C120(actor, 0)` when `+0x28 & 0x7F` is 2, `+0x24` and the context's `+0xD0` zeroed) and zeroes
`+0x7C`. It has 13 direct call sites; only the two move handlers hand in a non-zero mode, and
`movecancel`, `ucmovecancel`, the `setpos` family, `setposparty`, the push and the actor teardown
`0x002693D0` (twice) all hand in 0.

`0x00269C30(actor, accel, mode)` (`setaccr`) stores `+0x2C` = `accel * [0x01DFE0BC]` and `+0x2B` =
`mode`; `0x0026B450` (`setreachr`) stores the reach `+0x20`.

While `+0x29` is non-zero the wait resolver `0x0025DF00` re-issues `0x0026D6F0(actor, +0x7C *
[0x01DFE0BC], ...)` every frame (`0x0025DF83`), which is why mode 0 zeroes `+0x7C`.

### Steering toward the target

`0x002E45E0(actor, context)` runs from the movement step's driver when `+0x29` is 1 to 4. Each frame:

1. the target point: kind 0 is the stored position with reach `+0x20`; kind 1 resolves the actor
   (`0x003587C0` with the manager index `+0x00`, or `0x003590D0` → `0x003588B0` when the actor number
   `+0x04` is negative, `0x002E4641`-`0x002E465C`), reads its position, and
   adds to the reach both bodies' radii (`0x003DA6A0`: `sqrt(0x003DA730(a)) + a.+0x5C` for each over the
   two `+0x50` sub-blocks); an unresolvable actor target is the origin;
2. the bearing (`0x003A19C0`): yaw `atan2(dx, dz)` and pitch `atan2(dy, sqrt(dx^2 + dz^2))`, looped
   into range; the desired yaw `+0xA4` and pitch `+0xA0` each approach them by at most the caps
   `+0x50` and `+0x54` (`0x003A1AD0`: wrap the difference, step by `min(|diff|, cap)` and snap when
   below the cap);
3. when the manager's skip flag (`0x00267310(actor +0x15)`) is set, `0x0026AFE0` places the actor on the
   target at once;
4. the remaining distance is `distance - reach`, three-dimensional (`0x003A1920`) when `0x00264460` or
   actor byte `+0x08` bit `0x4` says so, else flat (`0x004686D0`);
5. the ramp, with `v = +0x24` and `a = +0x2C`: mode 1 leaves `v`; mode 2 uses the distance from the
   start snapshot `d0`, and when `max(a, d0) < v^2 / 2a` sets `v = max(a, sqrt(2a * max(a, d0)))`;
   mode 3 does the same with the remaining distance; mode 4 both. `v` goes to the context's `+0xD0`
   and `+0xF8`;
6. actor byte `+0x0D` bit `0x10` (near) is set when `[0x02164200] * +0x24 > remaining`; `0x02164200` is 3.0
   at run time: its only writer is the setter `0x002EBE40`, called by `0x00266D10` at boot and by the
   verb `debug_charmovestopvelrratio` (`0x0050D320`);
7. arrival, when `[0x01DFE0B8] * v > remaining`: for a position target (`+0x2A` = 0) a zero reach
   snaps the actor onto it (`0x0026AFE0`) and `+0x24`, `+0xD0` and `+0x2C` are zeroed; for every
   target `+0x29` = 0, a movement mode 2 is torn down (`0x0026C120(actor, 0)`), and `+0x24` and
   `+0xD0` are zeroed again.

The classical `v = sqrt(2 a d)` with `a` floored in keeps a stopping distance from going negative;
the arrival scale makes a 60 fps walk end one frame earlier in distance than a 30 fps one.

### The movement mode and the turn direction

`0x0026C120(actor, mode)`, 28 direct call sites, reads the old mode byte `+0x28`, stores the new one and:

- mode 0: when `+0x65` is set, `0x002EBE50(actor, 0, 0)` and `0x002E8EE0(actor)`; then
  `0x002E6300(actor, context, old)`, which returns `+0x64` when the old mode had bit `0x80`;
- modes 2 and 3: the turn direction bit, `+0x62` bit `0x40` set when `wrap(+0x34 - +0xA8)` (`0x003A1C50`)
  is negative, else cleared; `+0x58` = `pi/20` (`0x3E20D97C`, nine degrees) and `+0x5C` = `pi`
  (`0x40490FDB`), the second a store nothing reads;
- mode 4: the direction bit; then, when the frame count `+0x68` is at most `[0x01DFE0B4]` (unsigned),
  the facing is set to `+0x34` through `0x0026B620` and the mode reset to 0;
- any other mode: stored and nothing else.

So a character turns the short way round because the difference is wrapped before its sign is
taken, once, when the mode is set.

### The per-frame integrator

`0x002E5750(actor, direct)` runs once per actor from the wait resolver (`0x0025E3AA`) and is skipped
when actor byte `+0x18` is 1 or the controller's `+0x14F` has bit `0x1`. With `direct` non-zero it adds
the two floats of its third argument to the heading and pitch instead. Otherwise it reads the mode
`+0x28 & 0x7F` (`0x00265600`) and the turn step `+0x58` (`0x00264750` → `0x002E4BC0`), floors the step at
`0x3C0EFA35` (half a degree) for any active mode (`0x0026AC70` → `0x002E5B90`), and dispatches:

| Mode | Each frame |
|---|---|
| 1 | the facing advances by the spin rate `+0x3C` (`0x002E60C0`, verb `setvelrotangzx`), through `0x0026B5A0` |
| 2 | the facing approaches the desired heading `+0xA4` (`0x00263CC0`) by at most the step (`0x003A1AD0`), through `0x0026B5A0` |
| 3 | the facing approaches the target `+0x34`: by the step, or, when `+0x28` bit `0x80` is set (an untimed turn), by the frame-counted path: first, when `0x00265510(actor)` is non-zero and `0x00265530(actor)` is at most the `0x00265630` index, `0x0026C070(actor, 0)` and, with a render record, `0x003DDAD0(actor, controller byte +0x12, 0x1000000)`; then with no render record `0x003A1AD0` and `0x0026C300(index + 1)`, with one `0x003EC040`'s animation-driven step; the skip flag snaps to the target; when the facing equals the target, `0x0026C120(actor, 0)` |
| 4 | timed interpolation from the start heading `+0x38` to `+0x34`: `t = +0x78 / +0x68`, `heading = start + wrap(target - start) * t`, `+0x78 += 1` (`0x0026C300`); at `t >= 1`, or when the skip flag forces it, the final heading and `0x0026C120(actor, 0)` |
| 5 | waits while `0x002EA780` reports the render record's turn still running (`0x003E6AF0` and `0x002EA910` = 1); when it stops, `0x0026C120(actor, 0)` |

`0x002EA910` is 1 for an actor without a live render record or without an active entry (`0x003E6DF0`);
otherwise it returns the render entry's own test `0x003E2C00` ([character render
records](../Graphics/character-render-records.md)).

`0x003EC040(id, target, direction, mode)` reads the render record: it returns 0 for a record whose
save block is armed with word `+0x06` set, the record's own `+0x124` for the animation states
`0x35`, `0x36` and `0x0D`, the target unchanged without an active entry, and otherwise steps the
record's `+0x124` toward the target by the entry's rate `+0x24` or `+0x28` scaled by `[0x01DFE0BC]`.

The remaining angle goes through `0x003EC510(angle, direction)`, which loops it into range and then,
when non-zero, makes it positive for direction 0 or negative for direction 1 by a full turn, so the
step always goes the chosen way round; `0x003A1980(a, cap)` is `min(|a|, cap)`, and a remainder below
the rate snaps to the target.

### Untimed and timed turns

`0x002690D0(actor)` is the untimed turn body behind `raturn`, `raturna`, `raturnya` and their
relatives:

1. it takes the wrapped delta from the facing to `+0x34` and computes a frame count from the step
   (`|delta / +0x58|`, or through `0x003EBF60` when the render selector `0x002E9B60()` is not
   negative), scaled by the context's `+0x98` or `+0x9C` (by resume shape 1 or not) and floored
   at 1;
2. it writes the target to `+0x70` (`0x0026A8E0`) and zeroes `+0x74` and the context's `+0x224`;
3. when the delta is at least `pi/3`, or `+0x65` is set, or the actor has no armed render entry
   (`0x002E7600` = 0), it takes the body turn: `0x002EC380(actor, 1, frames)` (bits `0x38` of `+0x62` =
   1, `+0x60` = `frames / [0x01DFE0BC]`), `+0x28` |= `0x80`, `+0x68` = `(target - facing) / +0x58`
   (the raw difference; only the frame count uses the wrapped one);
4. the body turn goes on with `+0x78` = `[0x01DFE0B4]`, `+0x64` = 1, `0x003DDAD0(actor, 0, 0x1000004 -
   direction)` with `direction` = `+0x62` bit `0x40` as read at entry, and `+0x66` = the curve value;
5. otherwise the animation turn: `0x002EC380(actor, 2, frames)` and `+0x28` = 5;
6. both end with `0x002EBE50(actor, 1, 1)`.

`0x0026C330(actor, frames)` (`turnt`, `rturnt`, `rturnat`, `dira`) sets `+0x68` = `+0x66` =
`[0x01DFE0B4] + frames / [0x01DFE0BC]` (0 for a non-positive count) and `+0x78` = `[0x01DFE0B4]`; its
callers then set mode 4.

### The steer channel and the head

`0x002EBE50(actor, op, force)` starts or clears the steer channel. Op 0 zeroes the context's `+0xB4`
and `+0x224`. Otherwise, when `+0x63` is 0 or `force` is set, `+0xB4` takes the facing and
`+0x224` 0; the deltas `wrap(+0x70 - +0xB4)` and, with `+0x62` bit `0x80` clear, `wrap(+0x74 - +0x224)`
are taken; `+0xB4` and `+0x224` become `+0x70` and `+0x74`; and when `+0x62` bits `0x38` are 0 they
become 2 with `+0x60` = `max(1, |delta / +0x6C|)` frames (1 when `+0x6C` is not positive). `+0x63`
= `op`; then `0x002EC3F0` and `0x002E8EE0`.

`0x002E8EE0(actor)` pushes `+0x62` bit `0x80` (`0x003E6BD0`) and `+0x63` (`0x003E6BC0`) into the render record
and sets its `+0x290` bit `0x800`.

`0x002EC3F0(actor)` stages the head-look request by the shape (bits `0x7`) and the selector (bits
`0x38`) of `+0x62`, with the one-shot latch `+0x6A` bit `0x1` remapping selector 2 to 1:

- shapes 0-1 go to `0x002E7650` (selector 1) or `0x002E79A0` (selector 2);
- shapes 2-3 with selector 1 go to `0x003E6B90(record, 0, +0x10, +0x14)` and `0x003E6C00(record, 1,
  id, 0x30B)` for shape 3, else `0x002E7720`;
- shapes 2-3 with selector 2 go to `0x003E6B70(record, 1, +0x10, +0x14)` for shape 3, else `0x002E77F0`
  ([the staged look
  command](../Graphics/character-rig-and-look.md)).

The look-at verbs set the shapes:

- `0x002EC140(actor, a, b)` stores the raw pair at `+0x10`/`+0x14` with shape 2 and writes `+0x70`,
  `+0x74` and `+0x224` from them and runs `0x0026A9C0(actor, 0)`; `0x002EC1C0` stores the wrapped pair with shape 3;
- `0x002EC2C0(actor, vec)` stores a position with shape 0 and sets `+0x70` from the bearing to it,
  `+0x74` and `+0x224` to 0;
- `0x002EBFA0(actor, ordinal, manager, id)` stores an actor target with shape 1 and its handle at
  `+0x1C`; it falls back to the position form with `0x0026A1A0(actor, 1)` (bit `0x80`) when the target has
  no render record, and clears the channel (`0x002E64E0`) when the actor does not resolve.

Shapes 4-7 are never written. `0x002EC510(shape, actor, target)`, called by the `raturn` verbs
(`0x0034E710`, `0x0034EFE0`, `0x0034F4F0`) and `0x003578B0`, `0x0050F6E0`, picks the look-at verb by shape for a
class-3 actor with a movement context: 0 `0x002EC2C0` with the target as a position, 1 `0x002EBFA0` with
the target's byte `+0x15` and word `+0x00` and `0x30B`, 2 and 3 `0x002EC140` and `0x002EC1C0` with the
float at `+0x04` and 0.

`0x00263B90(actor, slot)` returns steering slot 0 or 1 (`context + 0x120 + 0x80 * slot`) of a class-3
actor, null for any other; `0x0026AC00` (verb `sethomingangzx`) runs `0x002E5B60` for a class-3 actor.

`0x0026D630` is the class-3 test in front of `0x002E60C0` for the verb `setvelrotangzx` (`0x003C`,
`0x003535C0`): the popped float becomes the spin rate `+0x3C` of the selected slot.
`0x00265580(actor, i)`, behind the verb `getdestrotangzx_227` (`0x0227`, `0x00341250`), returns the
target heading `+0x34` of slot `i` (`context + 0x154 + 0x80 * i`), with `i` capped at the selector
`+0xDC` and the selected slot for a negative `i`; it returns 0 for any other class.

## Layouts

Movement context (actor `+0xB8`), class 3:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x030` | `f32[4]` | start snapshot of the position (0x0026AF10) |  |
| `+0x038` | `f32` | heading of a class-1 object (also +0x48) |  |
| `+0x098` | `f32` | untimed-turn frame scales by resume shape | with `+0x9C` |
| `+0x09C` | `f32` | untimed-turn frame scales by resume shape | with `+0x98` |
| `+0x0A0` | `f32` | pitch |  |
| `+0x0A4` | `f32` | desired heading (yaw) |  |
| `+0x0A8` | `f32` | facing |  |
| `+0x0AC` | `f32` | facing aux (pitch lane of the render triple) |  |
| `+0x0B4` | `f32` | steer channel heading mirror |  |
| `+0x224` | `f32` | steer channel pitch mirror |  |
| `+0x0DC` | `u8` | slot selector 0 or 1 |  |
| `+0x0F0` | `void*` | cursor to the selected slot |  |
| `+0x120` | `SteeringRecord` | slot 0, 0x80 bytes |  |
| `+0x1A0` | `SteeringRecord` | slot 1, 0x80 bytes |  |

Struct SteeringRecord size=`0x80`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | target position {x, y, z, 1.0}, or {ordinal, manager} for an actor target |  |
| `+0x10` | `f32[3]` | resume parameters |  |
| `+0x1C` | `u32` | resume target handle |  |
| `+0x20` | `f32` | reach (setreachr) |  |
| `+0x24` | `f32` | requested speed, scaled |  |
| `+0x28` | `u8` | movement mode (bit 0x80 = untimed turn) |  |
| `+0x29` | `u8` | steering mode 0-4 |  |
| `+0x2A` | `u8` | target kind 0 position, 1 actor |  |
| `+0x2B` | `u8` | configured ramp mode (setaccr) |  |
| `+0x2C` | `f32` | ramp acceleration, scaled; 0.0 collapses modes 2-4 to 1 |  |
| `+0x34` | `f32` | target heading |  |
| `+0x38` | `f32` | turn start heading |  |
| `+0x3C` | `f32` | spin rate (mode 1) |  |
| `+0x50` | `f32` | yaw approach cap |  |
| `+0x54` | `f32` | pitch approach cap (0x002E5B60 / 0x002E5B90) |  |
| `+0x58` | `f32` | turn step, pi/20 |  |
| `+0x5C` | `f32` | pi, never read |  |
| `+0x60` | `i16` | steer channel frames |  |
| `+0x62` | `u8` | flags: mask 0x7 shape, mask 0x38 selector, bit 0x40 direction, bit 0x80 initiator |  |
| `+0x63` | `u8` | steer arm state |  |
| `+0x64` | `u8` | returned by 0x002E6300 |  |
| `+0x65` | `u8` | turn lock (0x0026A18D; read at 0x002692A8 and by the teardown) |  |
| `+0x66` | `i16` | curve / total frames |  |
| `+0x68` | `i16` | turn frames |  |
| `+0x6A` | `u8` | bit 0x1 one-shot latch |  |
| `+0x6C` | `f32` | initiator turn step |  |
| `+0x70` | `f32` | steer target heading |  |
| `+0x74` | `f32` | steer target pitch |  |
| `+0x78` | `f32` | turn frame index |  |
| `+0x7C` | `f32` | raw move speed (re-armed each frame) |  |

## Shipped data

| Constant | Value | Role |
|---|---|---|
| `0x3E20D97C` | pi/20, 9 degrees | the turn step of modes 2 and 3 |
| `0x3C0EFA35` | pi/360, half a degree | the integrator's floor on the step |
| `1.0471976` | pi/3 | the untimed turn's threshold between a body turn and an animation turn |
| `0x02164200` | 3.0 at run time | the near-flag multiple of the requested speed |
| `0x01DFE0B4`, `0x01DFE0B8`, `0x01DFE0BC` | 1, 1.0, 1.0 | the time base, the arrival scale, the speed and acceleration scale |

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

The context's angles, mirrors and selector; the two steering records; actor bytes `+0x0D` bits `0x10`
and 5, `+0x0B` bits `0x8` and `0x10` and `+0x1C` bit `0x20000`; the render record's `+0x124`, `+0x284`, `+0x290` and
its staged triple; the globals `0x02164200` and `0x02099DB4`.

## Modding notes

- Never store an unwrapped heading: every comparison downstream assumes a single turn. Keep the
  call site's normaliser; the one-pass wrap and the loop disagree on most inputs.
- Hooking one facing variant and not the other changes the render commit on class-3 actors only.
- A steering mode you set may not be the mode that sticks: with `+0x2C` at 0.0 modes 2-4 become 1.
  Call `setaccr` before the move for a ramp.
- `+0x5C` is a dead store; `+0x58` is both the per-frame cap and the divisor of the untimed turn's
  frame count.
- Mode 4's end depends on the Frame Rate setting through `[0x01DFE0B4]`, and a 60 fps walk arrives
  one frame earlier in distance.
- Writing the selector `+0xDC` directly switches slots; a value above 1 keeps the old cursor.
  Copying `+0x120` over `+0x1A0` copies a whole steering state.
- A look-at (shapes 2 and 3) is not resumed by the pop; only a walk (shapes 0 and 1) is.

## Related

- [Movement step](heading-speed-to-position-delta.md): the driver that runs the steer and the step.
- [Battle locomotion](battle-locomotion.md): the combat steering that feeds the unit's intent.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the resolver that calls the integrator.
- [Actor record](../Characters-And-Objects/actor-record.md): the class byte and the contexts.
- [The staged look command](../Graphics/character-rig-and-look.md): the head requests.
