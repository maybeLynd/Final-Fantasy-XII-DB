---
title: "Animation-driven movement: how an authored animation command steps and turns a character toward its target"
kind: "system"
category: "Movement and pathfinding"
addresses: "00520C10, 003E6340, 0041F2F0, 002ED500, 0031ADB0, 00424370, 003AF2B0, 003AED70, 003AF320, 0041D220, 00423B10, 003E6E60, 003E6EF0, 003AF220, 003AEF90, 003E68B0, 003E6A70, 003AEF20, 003AEF50, 0025DF00, 002E5750, 0026B6A0, 0026B520, 002651C0"
---

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

Authored command `1A`<sub>h</sub> ([authored
commands](../17-Presentation-Rendering/authored-presentation-commands.md
))
is handled by `00520C10`: when the current render record (`00422D50`) has a motion section
(`+370`<sub>h</sub>) it calls `003E6340(record, mode)` on its own record argument with the command's word
`+2` (the gate reads the current record, the request is built on the argument). The builder returns at
once without a list owner (`003E6E60` = 0).

Otherwise it asks the unit for a view: `0041F2F0(record,
0Ch, view)` zeroes 64 bytes, stamps `+00`<sub>h</sub> with the record's word `+CC`<sub>h</sub> and `+30`<sub>h</sub> with its
`+110`<sub>h</sub> (both overwritten: the builder zeroes the view again), and hands the view to the battle
unit's view builder (`002ED500` → `0031ADB0`) with selector bits 2 and 3.

Bit 2 writes the world position of the actor behind the unit's target handle `+2C`<sub>h</sub> (`00265020`)
into the view's `+10`<sub>h</sub>-`+18`<sub>h</sub> while the battle-state word `02089340` has bit 4.

Bit 3 writes the
reach point into `+20`<sub>h</sub>-`+28`<sub>h</sub>: when `00322280()` holds, the target actor exists, either
`02089340` has neither bit 9 nor bit 10 or the unit's `+698`<sub>h</sub> record has byte `+5` = 1, and the
unit's reach `00320E10(unit, 0)` is non-zero, it is the unit's position moved by the reach along the
bearing to the target (the sine table at `01F004E0`, the unit's own heading `+160`<sub>h</sub> when the two
coincide) and the view's `+3C`<sub>h</sub> takes bit 0 (otherwise `+20`<sub>h</sub> and `+28`<sub>h</sub> are written as 0 and the bit
stays clear).

Its y is the unit's `+E4`<sub>h</sub>, or the target's y plus
1.0 when the unit's `+698`<sub>h</sub> record has byte `+5` = 1 and its definition `+28`<sub>h</sub> bit 0.

Nothing is queued when the target position equals the record's position `+140`<sub>h</sub>/`+148`<sub>h</sub> in x and
z. Otherwise the request is built: for mode `10`<sub>h</sub> and modes 3 and 4 the direction is the unit
vector from the target position to the record's position, a step away from the target, with
distance 1.0; for every other mode it is the vector from the record to the reach point, with the
distance `|vector|` kept only when the view's `+3C`<sub>h</sub> has bit 0 and zeroed otherwise (with the
reach point unset the vector points at the world origin and only the turn acts).

The relative heading is the angle from the record's facing frame
`+180`<sub>h</sub> to the target position (`00424370`, an `atan2` taken only when both transformed x and z
are non-zero; a target on a frame axis leaves the result undefined); mode `0A`<sub>h</sub> with record byte `+2AF`<sub>h</sub> = 3 and a
non-negative heading takes the long way round (heading minus `2pi`). The request goes to the
record's list at `+550`<sub>h</sub> (`003AED70`).

Struct MoveTurnRequest  (`20`<sub>h</sub> bytes, on the builder's stack):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | 0 | +`02`<sub>h</sub>  u16  mode (the command's word +2) |
| `04`<sub>h</sub> | `f32` | distance | +`08`<sub>h</sub>  f32  0 (left as it was for mode `10`<sub>h</sub>) |
| `0C`<sub>h</sub> | `f32` | relative heading | +`10`<sub>h</sub>  f32[3] unit direction   +`1C`<sub>h</sub> f32 1.0 |

### The pool

`003AF2B0`, from the character render system's initialiser (`00426C34`), allocates 128 entries of
`60`<sub>h</sub> bytes at `[02B3F530]` once (arena class 6, `3000`<sub>h</sub> bytes), clears every entry's active
byte, and zeroes the serial `02B3F538` and the two switches `02B3F53C` and `02B3F540`. The pool is
global; each render record owns a list at `+550`<sub>h</sub> whose entries are linked through the pool.

`003AED70(list, request)` refuses, returning 0, while the first switch `02B3F53C` is set, the
list's `+28`<sub>h</sub> is non-zero (`003AF320` sets it), or the list's `+00`<sub>h</sub> is zero; it then takes the
first inactive entry (128 tested in order; none free returns 0), bumps the serial (wrapping past
`FFFFFF`<sub>h</sub> to 1) and returns `serial << 8 | index`.

The entry gets the request at `+20`<sub>h</sub>, the
counter `+4` = -1, the turn byte `+1` and move byte `+2` armed, the signs of the request's `+8` and
`+C`<sub>h</sub> at `+8`/`+C`<sub>h</sub> (1.0 or -1.0), `+10`<sub>h</sub>/`+14`<sub>h</sub> = `|angle| * 2 / pi` when the angle exceeds
`pi/2` else 1.0, the accumulators `+18`<sub>h</sub>/`+1C`<sub>h</sub> = 0, and is linked at the list's tail (`+18`<sub>h</sub>
head, `+20`<sub>h</sub> tail, entry `+40`<sub>h</sub> previous, `+48`<sub>h</sub> next); every older entry's turn byte is cleared,
so only the newest request turns.

### The knockback request

`003AED70` has a second producer. The knockback impulse `00323350(attacker, victim, distance, flag)`
(from `00307300`) builds a request on its stack: mode `E`<sub>h</sub>, or `F`<sub>h</sub> with the flag; the distance;
`+8` = 0; the relative heading as the bearing from the victim to the attacker minus the victim's
heading `+160`<sub>h</sub> (the heading itself when the two coincide), wrapped; the direction `(victim -
attacker) / hypot` in x and z, away from the attacker; `w` = 1.0.

A zero distance between the two skips it, as does the combination of `02089340` bits 9 and 10, a victim `+698`<sub>h</sub> record with byte
`+5` = 0, victim byte `+0` bit 4, and status words `+3Ch | +64h` clear of `80000003`<sub>h</sub> (or
`00377C20()` set).

The request goes through `002E70E0(victim handle, request)`, which needs the victim actor's byte
`+0D`<sub>h</sub> bit 1 and a valid render record, to `003E65E0(record, request)`: for modes `E`<sub>h</sub> and `F`<sub>h</sub>,
with `003E56C0()` null or its byte `+111`<sub>h</sub> zero the heading is zeroed, otherwise a heading beyond
90 degrees either way is flipped by `pi` and wrapped; then `003AED70` as usual. Modes 14 and 15 are
the two profile rows no authored command names.

### The profiles

Every animation container carries one `@FRM` child ([container](../17-Presentation-Rendering/model-files-cm-ca.md
)).
When a presentation entry is set up (`0041D220`) it looks the child up by tag (`00409660`,
`00409A30`) and, when the child's size `+8` exceeds `30`<sub>h</sub>, keeps the body `child + 30h` at the
entry's `+378`<sub>h</sub> and the profile table `body + [body + 8]` at `+37C`<sub>h</sub> (-1 for none).

When a
motion starts on the record (`00423B10`, after a successful `00424D80`), the entry's `+37C`<sub>h</sub> and
the resource handle `+68`<sub>h</sub> go to the record's `+E8`<sub>h</sub>/`+D8`<sub>h</sub> with `+F0`<sub>h</sub>/`+100`<sub>h</sub> zeroed, or,
when `004233D0(record, motion)` finds no slot (-1), to `+100`<sub>h</sub>/`+F0`<sub>h</sub> with the first pair left
alone. `00423B10` also resolves the bases into `+E0`<sub>h</sub>/`+F8`<sub>h</sub> (`003AB7F0` of the handles) and fills the
list's `+08`<sub>h</sub>/`+10`<sub>h</sub> directly; `003E6E60`, with a current record (`00422D50`), re-derives them
from `+E0h + +E8h` and `+F8h + +100h` each time it is asked.

```python
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
while the second switch `02B3F540` is set or the list's `+00`<sub>h</sub> is zero, and for each entry:

1. its profile is the table's entry for the mode (`table + table[mode]`), or for mode `16`<sub>h</sub> the
   list's own profile `+10`<sub>h</sub>; mode `16`<sub>h</sub> with no own profile unlinks and frees the entry;
2. the counter `+4` goes up; at `duration * [01DFE0B4]` the entry is unlinked and freed;
3. while the counter is below `moveFrames * [01DFE0B4]` and the move byte is set, `move += direction
   * speed[counter / [01DFE0B4]] * distance * scale * [01DFE0BC]` and `move.w` = the request's
   `+1C`<sub>h</sub>; at `moveFrames` the move byte clears;
4. while the counter is below `turnFrames * [01DFE0B4]` and the turn byte is set, with `f = counter /
   [01DFE0B4]`: when the request's word `+0` is non-zero, `inc = min((|+28h| - +18h) * [01DFE0BC],
   rate0[f] * scale)`, `+18h += inc`, `turn.x = inc * sign0`; then `inc = min((|+2Ch| - +1Ch) *
   [01DFE0BC], rate1[f] * scale * [01DFE0BC])`, `+1Ch += inc`, `turn.y = inc * sign1`; at
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
`+13`<sub>h</sub> bit 0 clear and `+10C`<sub>h</sub> zero, or byte `+0B`<sub>h</sub> bit 5; others run `002E6310`) with a render
entry whose record id is valid, computes `maxStep` as the smaller of the two radii `003DA710` reads
from the movement context's `+50`<sub>h</sub> for a class-3 actor (two uninitialised locals otherwise; `1e6`
when actor byte `+13`<sub>h</sub> has bit 7) and calls `003E6EF0`.

It reads `003E68B0` and, when that holds and actor byte `+0D`<sub>h</sub> has bit 1, `003E6A70`. The render entry's
byte `+10`<sub>h</sub> bit 2 and actor byte `+0C`<sub>h</sub> bit 4 take the move bit (set here, never cleared here).

Then `002E5030(actor, moveBit, &move)` runs the movement step with the summed move as the
pass-through vector when the bit is set ([movement step](heading-speed-to-position-delta.md)), and
`002E5750(actor, turnBit, &turn)` runs the integrator: with the bit set it adds `turn.y` to the
facing (`00265200` + `turn.y` → `0026B6A0(actor, angle, 0)`) and `turn.x` to the pitch (`002651C0`
+ `turn.x` → `0026B520`), instead of the steering modes ([facing and
steering](facing-and-steering.md)).

The second output float is the heading and the first the
pitch, which is why the dead first axis costs nothing. The integrator returns at once for a
captured party member (actor `+18`<sub>h</sub> = 1) or a controller with `+14F`<sub>h</sub> bit 0, so those actors get
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
| `1A`<sub>h</sub> commands | 12,876 |
| mode `16`<sub>h</sub>, the record's own profile | 1,652 |
| naming a table slot | 11,224: 11,200 present, 24 an empty slot in their own container (read as the table head) |
| present profiles | all 11,200 have both `moveFrames` and `turnFrames` non-zero, durations 1 to 30 frames, curves inside the file |
| modes authored | 0-7, 9-12, 16, 21, 22; commonest 12 (2,344), 16 (2,145), 6 (1,908) |
| blocks | `attack` 4,495, `avoid` 1,216, then `magic`, `ev_treasure`, `ability`, `steal`, `pary_weapon`, `pary_shield` at 608 each |
| scale | small floats near `5e-6` (`36C19F01`<sub>h</sub> in 2,782 profiles), so a `u16` curve value times the scale is a per-frame share below 0.4 |
| pool | 128 entries of `60`<sub>h</sub> bytes; the serial wraps at `FFFFFF`<sub>h</sub> |

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
