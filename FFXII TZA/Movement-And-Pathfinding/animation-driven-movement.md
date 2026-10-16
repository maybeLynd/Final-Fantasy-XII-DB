---
title: "Animation-driven movement: how an authored animation command steps and turns a character toward its target"
kind: "system"
category: "Movement and pathfinding"
summary: "The lunge and swing-round an attack animation asks for: the authored command that names a movement profile, the request the command handler builds from the battle unit's target, the global pool of 128 requests and the per-character lists they hang on, the profile tables in every animation container with their speed and turn-rate curves, the once-a-frame consumer that sums a clamped step and a turn, and the actor update that feeds both into the movement step and the facing."
addresses: ["00520C10", "003E6340", "0041F2F0", "002ED500", "0031ADB0", "00424370", "003AF2B0", "003AED70", "003AF320", "0041D220", "00423B10", "003E6E60", "003E6EF0", "003AF220", "003AEF90", "003E68B0", "003E6A70", "003AEF20", "003AEF50", "0025DF00", "002E5750", "0026B6A0", "0026B520", "002651C0"]
---

# Animation-driven movement: how an authored animation command steps and turns a character toward its target

## What the player sees

When a character attacks, it steps in and swings round to face what it is hitting; when it dodges,
it slides. None of it is walking or baked into the bone motion. An animation
asks for it with one authored command that names a profile, a hit asks for the knockback slide
the same way, and the actor update carries it out
frame by frame, adding a small clamped step and a small turn toward the target along curves stored
in the character's own animation container. A lunge covers the same share of the gap whatever the
gap is, and a swing closes the angle and stops when it is closed.

## How it works

### The command and the request

Authored command `0x1A` ([authored
commands](../17-Presentation-Rendering/authored-presentation-commands.md
))
is handled by `00520C10`: when the current render record (`00422D50`) has a motion section
(`+0x370`) it calls `003E6340(record, mode)` on its own record argument with the command's word
`+2` (the gate reads the current record, the request is built on the argument). The builder returns at
once without a list owner (`003E6E60` = 0).

Otherwise it asks the unit for a view: `0041F2F0(record,
0x0C, view)` zeroes 64 bytes, stamps `+0x00` with the record's word `+0xCC` and `+0x30` with its
`+0x110` (both overwritten: the builder zeroes the view again), and hands the view to the battle
unit's view builder (`002ED500` → `0031ADB0`) with selector bits 2 and 3.

Bit 2 writes the world position of the actor behind the unit's target handle `+0x2C` (`00265020`)
into the view's `+0x10`-`+0x18` while the battle-state word `02089340` has bit 4.

Bit 3 writes the
reach point into `+0x20`-`+0x28`: when `00322280()` holds, the target actor exists, either
`02089340` has neither bit 9 nor bit 10 or the unit's `+0x698` record has byte `+5` = 1, and the
unit's reach `00320E10(unit, 0)` is non-zero, it is the unit's position moved by the reach along the
bearing to the target (the sine table at `01F004E0`, the unit's own heading `+0x160` when the two
coincide) and the view's `+0x3C` takes bit 0 (otherwise `+0x20` and `+0x28` are written as 0 and the bit
stays clear).

Its y is the unit's `+0xE4`, or the target's y plus
1.0 when the unit's `+0x698` record has byte `+5` = 1 and its definition `+0x28` bit 0.

Nothing is queued when the target position equals the record's position `+0x140`/`+0x148` in x and
z. Otherwise the request is built: for mode `0x10` and modes 3 and 4 the direction is the unit
vector from the target position to the record's position, a step away from the target, with
distance 1.0; for every other mode it is the vector from the record to the reach point, with the
distance `|vector|` kept only when the view's `+0x3C` has bit 0 and zeroed otherwise (with the
reach point unset the vector points at the world origin and only the turn acts).

The relative heading is the angle from the record's facing frame
`+0x180` to the target position (`00424370`, an `atan2` taken only when both transformed x and z
are non-zero; a target on a frame axis leaves the result undefined); mode `0x0A` with record byte `+0x2AF` = 3 and a
non-negative heading takes the long way round (heading minus `2pi`). The request goes to the
record's list at `+0x550` (`003AED70`).

```
struct MoveTurnRequest  (0x20 bytes, on the builder's stack)
+0x00  u16     0                       +0x02  u16  mode (the command's word +2)
+0x04  f32     distance                +0x08  f32  0 (left as it was for mode 0x10)
+0x0C  f32     relative heading        +0x10  f32[3] unit direction   +0x1C f32 1.0
```

### The pool

`003AF2B0`, from the character render system's initialiser (`00426C34`), allocates 128 entries of
`0x60` bytes at `[02B3F530]` once (arena class 6, `0x3000` bytes), clears every entry's active
byte, and zeroes the serial `02B3F538` and the two switches `02B3F53C` and `02B3F540`. The pool is
global; each render record owns a list at `+0x550` whose entries are linked through the pool.

`003AED70(list, request)` refuses, returning 0, while the first switch `02B3F53C` is set, the
list's `+0x28` is non-zero (`003AF320` sets it), or the list's `+0x00` is zero; it then takes the
first inactive entry (128 tested in order; none free returns 0), bumps the serial (wrapping past
`0xFFFFFF` to 1) and returns `serial << 8 | index`.

The entry gets the request at `+0x20`, the
counter `+4` = -1, the turn byte `+1` and move byte `+2` armed, the signs of the request's `+8` and
`+0xC` at `+8`/`+0xC` (1.0 or -1.0), `+0x10`/`+0x14` = `|angle| * 2 / pi` when the angle exceeds
`pi/2` else 1.0, the accumulators `+0x18`/`+0x1C` = 0, and is linked at the list's tail (`+0x18`
head, `+0x20` tail, entry `+0x40` previous, `+0x48` next); every older entry's turn byte is cleared,
so only the newest request turns.

### The knockback request

`003AED70` has a second producer. The knockback impulse `00323350(attacker, victim, distance, flag)`
(from `00307300`) builds a request on its stack: mode `0xE`, or `0xF` with the flag; the distance;
`+8` = 0; the relative heading as the bearing from the victim to the attacker minus the victim's
heading `+0x160` (the heading itself when the two coincide), wrapped; the direction `(victim -
attacker) / hypot` in x and z, away from the attacker; `w` = 1.0.

A zero distance between the two skips it, as does the combination of `02089340` bits 9 and 10, a victim `+0x698` record with byte
`+5` = 0, victim byte `+0` bit 4, and status words `+0x3C | +0x64` clear of `0x80000003` (or
`00377C20()` set).

The request goes through `002E70E0(victim handle, request)`, which needs the victim actor's byte
`+0x0D` bit 1 and a valid render record, to `003E65E0(record, request)`: for modes `0xE` and `0xF`,
with `003E56C0()` null or its byte `+0x111` zero the heading is zeroed, otherwise a heading beyond
90 degrees either way is flipped by `pi` and wrapped; then `003AED70` as usual. Modes 14 and 15 are
the two profile rows no authored command names.

### The profiles

Every animation container carries one `@FRM` child ([container](../17-Presentation-Rendering/model-files-cm-ca.md
)).
When a presentation entry is set up (`0041D220`) it looks the child up by tag (`00409660`,
`00409A30`) and, when the child's size `+8` exceeds `0x30`, keeps the body `child + 0x30` at the
entry's `+0x378` and the profile table `body + [body + 8]` at `+0x37C` (-1 for none).

When a
motion starts on the record (`00423B10`, after a successful `00424D80`), the entry's `+0x37C` and
the resource handle `+0x68` go to the record's `+0xE8`/`+0xD8` with `+0xF0`/`+0x100` zeroed, or,
when `004233D0(record, motion)` finds no slot (-1), to `+0x100`/`+0xF0` with the first pair left
alone. `00423B10` also resolves the bases into `+0xE0`/`+0xF8` (`003AB7F0` of the handles) and fills the
list's `+0x08`/`+0x10` directly; `003E6E60`, with a current record (`00422D50`), re-derives them
from `+0xE0 + +0xE8` and `+0xF8 + +0x100` each time it is asked.

```
table[mode]   u32   offset of the profile from the table (a 0 is not tested: the consumer reads the table head as the profile)
profile       +0x00 u32  duration, frames      +0x04 u16 moveFrames    +0x06 u16 turnFrames
              +0x08 f32  scale                 +0x0C u32 offset of the speed curve from the profile
              +0x10 u16[turnFrames][2]  the two turn-rate curves
speed curve   u16[moveFrames]
```

### The step, once a frame

The actor update (`0025DF00`, below) calls `003E6EF0(record, &move, &turn, maxStep)`, which, with a
list owner, runs `003AF220`: `003AEF90` over the list, then the clamp: the move is normalised
(`00380800`) and scaled, `w` included, by `min(maxStep, |move|)`. `003AEF90` zeroes both outputs, returns at once
while the second switch `02B3F540` is set or the list's `+0x00` is zero, and for each entry:

1. its profile is the table's entry for the mode (`table + table[mode]`), or for mode `0x16` the
   list's own profile `+0x10`; mode `0x16` with no own profile unlinks and frees the entry;
2. the counter `+4` goes up; at `duration * [01DFE0B4]` the entry is unlinked and freed;
3. while the counter is below `moveFrames * [01DFE0B4]` and the move byte is set, `move += direction
   * speed[counter / [01DFE0B4]] * distance * scale * [01DFE0BC]` and `move.w` = the request's
   `+0x1C`; at `moveFrames` the move byte clears;
4. while the counter is below `turnFrames * [01DFE0B4]` and the turn byte is set, with `f = counter /
   [01DFE0B4]`: when the request's word `+0` is non-zero, `inc = min((|+0x28| - +0x18) * [01DFE0BC],
   rate0[f] * scale)`, `+0x18 += inc`, `turn.x = inc * sign0`; then `inc = min((|+0x2C| - +0x1C) *
   [01DFE0BC], rate1[f] * scale * [01DFE0BC])`, `+0x1C += inc`, `turn.y = inc * sign1`; at
   `turnFrames` the turn byte clears.

The builder always writes 0 to the request's word `+0`, so the first turn axis never runs in the
shipped game: `turn.x` stays 0 and the turn is `turn.y`, the relative heading closed along the
second curve. The speed curve is a share of the distance at the moment of the command, so a lunge
covers the same fraction of the gap whatever the gap is; the two accumulators stop each axis once
the request's angle is closed. The last entry written wins `turn` outright; `move` is a sum.

`003E68B0` reports whether the list is enabled and non-empty (`003AEF20`); `003E6A70` returns bit 0
when any entry has its turn byte set and bit 1 when any has its move byte set (`003AEF50`).

### The actor update

`0025DF00` resolves the actor's wait state and then, for an actor that passes the input gate (byte
`+0x13` bit 0 clear and `+0x10C` zero, or byte `+0x0B` bit 5; others run `002E6310`) with a render
entry whose record id is valid, computes `maxStep` as the smaller of the two radii `003DA710` reads
from the movement context's `+0x50` for a class-3 actor (two uninitialised locals otherwise; `1e6`
when actor byte `+0x13` has bit 7) and calls `003E6EF0`.

It reads `003E68B0` and, when that holds and actor byte `+0x0D` has bit 1, `003E6A70`. The render entry's
byte `+0x10` bit 2 and actor byte `+0x0C` bit 4 take the move bit (set here, never cleared here).

Then `002E5030(actor, moveBit, &move)` runs the movement step with the summed move as the
pass-through vector when the bit is set ([movement step](heading-speed-to-position-delta.md)), and
`002E5750(actor, turnBit, &turn)` runs the integrator: with the bit set it adds `turn.y` to the
facing (`00265200` + `turn.y` → `0026B6A0(actor, angle, 0)`) and `turn.x` to the pitch (`002651C0`
+ `turn.x` → `0026B520`), instead of the steering modes ([facing and
steering](facing-and-steering.md)).

The second output float is the heading and the first the
pitch, which is why the dead first axis costs nothing. The integrator returns at once for a
captured party member (actor `+0x18` = 1) or a controller with `+0x14F` bit 0, so those actors get
neither arm.

## Layouts

```
pool entry (0x60 bytes, 128 at [02B3F530])
+0x00  u8   active     +0x01 u8 turn armed   +0x02 u8 move armed   +0x04 i32 counter (-1 at take)
+0x08  f32  sign of request +8       +0x0C f32 sign of request +0xC
+0x10  f32  |angle0| * 2/pi or 1.0   +0x14 f32 the same for angle1
+0x18  f32  accumulator axis 0       +0x1C f32 accumulator axis 1
+0x20  MoveTurnRequest (0x20 bytes): +0x20 u16 0, +0x22 u16 mode, +0x24 f32 distance, +0x28 f32 angle0,
       +0x2C f32 relative heading, +0x30 f32[3] direction, +0x3C f32 w
+0x40  ptr  previous   +0x48 ptr next   +0x50 u32 serial << 8 | index

record list (render record +0x550)
+0x00  u32  enabled   +0x08 ptr profile table   +0x10 ptr own profile (mode 0x16)
+0x18  ptr  head      +0x20 ptr tail            +0x28 u32 disabled (003AF320)

render record: +0xD8 handle, +0xE0 resolved base, +0xE8 offset of the table; +0xF0 handle, +0xF8 resolved base, +0x100 offset of the own profile
presentation entry: +0x370 motion section; +0x378 @FRM body; +0x37C profile table (-1 none)
globals: 02B3F530 pool; 02B3F538 serial; 02B3F53C refuses new requests; 02B3F540 stops the step
```

## Shipped data

Every `.ca` container under `ps2data` (3,164 of 3,164 are `@FRP`), walking the `@FMC` command
streams and each container's own `@FRM` table:

| Fact | Value |
|---|---|
| `0x1A` commands | 12,876 |
| mode `0x16`, the record's own profile | 1,652 |
| naming a table slot | 11,224: 11,200 present, 24 an empty slot in their own container (read as the table head) |
| present profiles | all 11,200 have both `moveFrames` and `turnFrames` non-zero, durations 1 to 30 frames, curves inside the file |
| modes authored | 0-7, 9-12, 16, 21, 22; commonest 12 (2,344), 16 (2,145), 6 (1,908) |
| blocks | `attack` 4,495, `avoid` 1,216, then `magic`, `ev_treasure`, `ability`, `steal`, `pary_weapon`, `pary_shield` at 608 each |
| scale | small floats near `5e-6` (`0x36C19F01` in 2,782 profiles), so a `u16` curve value times the scale is a per-frame share below 0.4 |
| pool | 128 entries of `0x60` bytes; the serial wraps at `0xFFFFFF` |

## Operations

Per authored command: one view request, one request built and one pool entry taken; per knockback
impulse: one request built and one entry taken. Per frame per
actor with a render record: the list is walked, each live entry adds its frame of the step and
rewrites the turn, the step is clamped to the body's smaller radius, and the movement step and the
integrator consume the pair.

## State

The pool, its serial and two switches; each render record's list and its two profile pointers;
each entry's counter, armed bytes and two accumulators.

## Modding notes

- The step is proportional to the distance at the command, shaped by the speed curve, clamped per
  frame by the actor's smaller collision radius; it is not root motion, and the bone data does not
  contain it.
- A command with no target still turns nothing and moves nothing; the target is whatever the unit's
  target handle names when the command fires.
- 128 requests exist for the whole scene; a 129th is dropped silently, and the first switch or a
  disabled list refuses requests while the second switch only freezes the step.
- Only the newest request turns; every older entry's turn byte is cleared at the take.
- The first turn axis is authored dead (word `+0` is always 0); a port that enables it turns the
  pitch.
- Knockback is the second producer; a port that replays only authored commands loses the slide
  and the turn toward the attacker.
- Position changes here are part of combat spacing; two machines playing different animations
  diverge in position.

## Related

- [Movement step](heading-speed-to-position-delta.md): the pass-through path that consumes `move`.
- [Facing and steering](facing-and-steering.md): the integrator's direct arm that consumes `turn`.
- [Authored commands](../17-Presentation-Rendering/authored-presentation-commands.md
):
  the command stream and the other handlers.
- [FRP container](../17-Presentation-Rendering/model-files-cm-ca.md
):
  the `@FRM` child.
