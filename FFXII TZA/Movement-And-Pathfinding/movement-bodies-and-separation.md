---
title: "Movement bodies and separation: the collision body every steerable actor carries, its placement on the field, and the tick that pushes overlapping bodies apart"
kind: "system"
category: "Movement and pathfinding"
summary: "The pool of movement bodies behind every steerable actor: how a body is allocated, attached after the presentation and released with it, how its ellipse, height and base are sized from the actor's contexts, the placement record that holds the field cell, the ground height and the cell attributes, the per-frame registration into thirty-two angular sectors around the mean of all bodies, the per-tick separation pass that visits each pair once, the pair resolver with its layer, owner, vertical and ellipse tests and its weight rule, and how the push is consumed on the next candidate position."
addresses: ["003DAE30", "003DA8A0", "003DAD00", "002E3500", "00269EC0", "002682D0", "002685F0", "00268380", "003DAF20", "00380D30", "003808A0", "003DB1B0", "003DB020", "0046AD20", "003DAA40", "003DAC70", "003DAAB0", "003DAB50", "00314F30", "00314F50", "003DA5A0", "003DA730", "00314E10", "003DA9F0", "002E5180", "002E5380", "003B7730", "00266D10"]
---

# Movement bodies and separation: the collision body every steerable actor carries, its placement on the field, and the tick that pushes overlapping bodies apart

## What the player sees

Characters and foes crowding a doorway slide apart instead of standing inside one another, a
frame late. A heavy body pushes a light one further, two bodies on different layers pass through
each other, and an actor that stops registering with the world, because it left it, stops
participating on the very next tick. Every steerable actor stands on the ground at the height the
field gives it, and the cell it stands on tells the engine what kind of ground that is.

## How it works

### The pool

`02B4E4C0` holds 128 bodies of `0x130` bytes linked through `u16` indices: `+0` previous, `+2`
next, `+4` the body's own index, `0xFFFF` the null link. The free-list head is the word `02B57CC4`,
the active-list head `02B57CC0`. `003DAE30`, from the actor system's initialiser `00266D10`
(`00267141`), links every body to its neighbours (the first's previous and the last's next
`0xFFFF`), zeroes `+0x10`-`+0x17` and `+7`, sets the free head to 0 and the active head to empty,
zeroes `02B57CC8` and `02B57CD0`, and zeroes the 32 sector masks at `02B57CE0`.

`003DA8A0()` pops the free head and returns null when it is `0xFFFF`; it links the body at the
head of the active list, zeroes `+0x30`-`+0xDF`, sets `+0x82` = `0xFFFF`, `+0x88` = 0, runs
`00380B80` on the placement, sets `+8` = 1.0, `+6` = 0, `+0x10`-`+0x27` = 0, `+0xE8` = 0, runs
`003DA830` on `+0xF0` (overwritten by the shape writer below), and zeroes `+0x100`-`+0x10B`,
`+0x110`/`+0x114` and `+0x118`.

`003DAD00(body)` unlinks it from the active list, pushes it on the free list, writes `{0, -1.0, 0,
-1.0}` at `+0xF0` and clears `+7`; the -1.0 at `+0xF4` is what makes a freed body fail the
resolver's positive-radii test if it is ever handed to it.
Until the first release the n-th body allocated in an area is index `n - 1`.

### Attachment

`002E3500(record)` is the one creator. It returns at once without a secondary context at `+0xC0`;
otherwise it releases any body at `[+0xC0] + 0x138`, allocates one and stores the result there,
null included.

It then runs the five consumers: `00269EC0(record, 0)` sets the layer byte `+6`;
`002681D0`; `002682D0` copies the context's `+0x151` bits 0-1 into the body's flags `+0x90`;
`002685F0` copies the context's float `+0x148` into the weight `+8`; `00268380` sizes the shape.
Every consumer tests the chain and does nothing on a null body, so the 129th actor has no
collision body and silently drops out of the pass.

Its callers are the actor's presentation set-up `002E28E0` and `002E3580`, which releases the
presentation and re-creates; the releasers `002E3D00` and `002E3AF0` run from the per-type
presentation release and the manager release ([actor record](../Characters-And-Objects/actor-record.md)).
A body lives exactly as long as its actor's presentation.

### The shape

`00268380(record)`: for a class-3 actor the radii pair comes from the movement context's `+0x50`
(`003DA710`); for any other class the two radii handed on are uninitialised stack values, so a
class-1 body's `+0xF0`/`+0xF4` hold whatever the stack held. The height is the movement context's `+0x68` for class 1 or `+0xC0 * +0x24` for
class 3; the heading `+0x38` for class 1 or `+0xA8` for class 3, else 0; the base is the secondary
context's `+0x140 + +0x144`; the three percentages are the movement context's bytes
`+0x104`-`+0x106` for class 3, else `{37, 50, 37}`.

`006C0520` writes `{radiusA, radiusB, heading,
0}` at the body's `+0xF0`, the height goes to `+0xE0` (`003DB130`), the base to `+0xE4`
(`003DB120`).

`003DAF20(body, a, b, c)` finishes: `+0x40`/`+0x48` = `cos`/`sin` of the heading
with `+0x44` = 0 and `+0x4C` = 1.0, the radii and height copied to `+0x94`-`+0x9C`, and the inner
shape `+0xA0` = `a * radiusA / 50`, `+0xA8` = `b * height / 50 + base`, `+0xA4` = `c * radiusB / 50`.
The facing writer re-sizes the same way ([facing and steering](facing-and-steering.md)).

### The placement record

The body's `+0x30` is the actor's field placement. `00380D30(placement, candidate)` resolves the
field (`0026E500(0)`) and the candidate's cell (`00233050`, `00233110`); when the cell `+0x52` is
valid it stores the field's blocked-class mask (`00232090`) at `+0x5E` and, unless the placement's
class byte `+0x50` is in it, copies the candidate's four floats, stores the ground height
(`00231890`) at `+0x7C` and into the position's y unless flag `+0x60` bit 0 holds; a blocked class
sets the cell to -2.

`003808A0(placement, field)` then returns at once with `+0x54` = `0xFFFF`
when the cell is negative (the -2 included), so a blocked placement keeps its stale attribute
words; otherwise it reads the cell record (`[field + 0x10] + cell
* 32`, attribute dword `+0xC`) through the mask table `0209A2D0` (`00232020`): bits 13-17 to `+0x56`,
bits 3-6 to `+0x58`, `00231F80`'s bits to `+0x5A`, attribute bit 12 to flag bit 2; `00231A90`; the
second cell `+0x54`'s height to `+0x90` with flag bit 3 when above the ground height; and its tail
steps `+0x80`/`+0x84` toward `+0x64`/`+0x68` by at most 0.25 per step, re-resolving the cell
(`00233050`, `00232760`) until within 0.01.

`003DB1B0(body)` runs the placement on `body + 0x30` and returns whether the cell is valid; the
movement step reaches it through `002E5C90`. In body terms the fields are `+0x30` position, `+0x70`
displacement, `+0x80` cell class, `+0x82` cell (-2 refused), `+0x84` second cell, `+0x86`/`+0x88`/
`+0x8A` the attribute words, `+0x8E` the blocked mask, `+0x90` flags, `+0xAC` ground height, `+0xC0`
second height, `+0xC8` requested speed.

### Registering every frame

The movement step's driver (`002E5030`) calls `003DB020(body, x, z, 0, &radii)` when `002EA7F0`
passes ([movement step](heading-speed-to-position-delta.md)). It sets `+7`, active this tick, and
when the two-globals gate `003B7730` holds computes the body's sector bits with
`0046AD20(body + 0x120, x, z, max(radii))` and ORs the body's own bit into the 128-bit mask of every
sector set (`02B57CE0`, sixteen bytes per sector).

`0046AD20` is not a grid. It keeps a running mean of every registered position (`02CA6040`/
`02CA6048` sums, `02CA604C` count) and a centre at `02CA6034`/`02CA603C`; the body's offset from the
centre gives a distance `d` and a sector `floor(angle / 2pi * 32)` of 32 around it. With `d > r`
the body occupies its sector widened by `floor(atan2(r, sqrt(d^2 - r^2)) / pi * 16) + 1` sectors
each side; with `d <= r` all 32.

The result is `+0x120` the bits, `+0x124` the sector, `+0x128`
`d - r` (0 when `d <= r`) and `+0x12C` `d + r`; a negative radius clears all four. The sums and
the count are updated even when the record pointer is null.

### The separation pass

`World_UpdateSimulationTick` first runs `003DAA40` (`003140C5`): the 32 masks are zeroed and every
body's `+7` cleared, so a body that does not register during the frame is not active for the pass.
Its tail runs `003DAC70(00314F30)` (`00314244`) over the active list:

1. `003DAAB0(bits, self)` builds the candidate set at `02B57EE0`: the OR of the masks of the body's
   sectors, with its own bit and every lower index cleared, so each pair is visited once;
2. `003DAB50(dMin, dMax, body, callback)` walks the candidate set a byte at a time and, at each
   position that is a candidate or whose bit is still set in the body's pair bitmap `+0x18`, clears
   the pair bit, calls the callback with the two bodies, and sets the bit again when it returns
   non-zero.

The walk drifts in two ways. Its byte loop runs over each candidate qword while the remaining
value is non-zero, so it stops at the highest non-zero byte; the body pointer advances eight
bodies per byte processed and is not reset between the two qwords, so trailing zero bytes of
qword 0 shift the body pointer for every candidate of qword 1 (a first qword of `0x00..00FF` leaves
it at body 8, and candidate 64 is resolved against body 8).

Its pair-bit index advances once per
bit stepped inside a non-zero byte, so remembered bits past byte 0 are written at the wrong
indices (candidate 9 alone is resolved against body 9 but remembered at index 1).

A remembered bit is therefore visited only below the highest candidate of a non-zero byte, and a
pair whose candidate has a high index can go untested. The resolver re-tests whatever pair it is
handed, so a mis-indexed call pushes only when the bodies really overlap.

### The pair resolver

`00314F30(A, B)` calls `00314F50(A, B, 1, &out)`. In push mode (`mode` 1) it refuses, returning 0,
unless both bodies have positive radii `+0xF0` and `+0xF4`, both are active this tick, their layer
bytes `+6` are equal, and A's owner byte `+0x119` is zero or differs from B's; query mode (`mode`
0, from `00313F80`) skips the active test and every write.

With `003DAE00` reading each position
offset by the accumulated pushes `+0x100`/`+0x108`, the vertical spans `[y + base, y + base +
height]` must overlap, and `003DA5A0` must return a negative separation: the horizontal distance
minus each body's ellipse extent along the joining line (`003DA730`: the offset rotated by the
body's heading, `(x^2 + z^2) / (x^2 / a^2 + z^2 / b^2)`) and the margins `+0xFC`.

The weights `+8` (both negated when both negative, both 1 when both zero) go through `00314E10`,
which returns A's share `w = wB / (wA + wB)`, or 0 when the sum is 0 (a cancelling pair such as 1
and -1, which the negative rules then decide), overridden by the masks `+0x110 | +0x114`: each
body's low byte is masked by the complement of the union's bits 8-15, and with either masked byte
non-zero an overlap with the union's bits 16-23 returns 0, and unequal values give 0 when A's is
larger, else 1; with both masked bytes zero the ratio stands. A negative `wA` gives 0, a negative
`wB` 1.

Then A receives `w * separation` and B `(1 - w) * separation` along the joining
direction, added to `+0x100` (x) and `+0x108` (z), each body's `+0xE8` holding the squared length
of the other's increment and `+0xEC` set.

`w` = 0 counts and marks (`+0xED`, `+0xEE` = 1) B only; `w` = 1 A only; otherwise both count and
both `+0xEE` are cleared. In push mode every resolved pair returns 1. In query mode nothing is
written to the bodies, `w` goes to `out`, and the return is 3 for `w` = 0, 4 for `w` = 1, else 2.

Pairs resolved later in the tick see the pushes of pairs resolved earlier, because the resolver
reads the accumulators it writes.

### Consuming the push

`002E5180(record)`, from the world tick's per-slot step (`002623A0`, `0025E400`), clears the
controller's `+0x151` bit 2, stores the ground height (`003DADE0`) at the movement context's
`+0xD4` and, when the body's `+0xEC` is set, re-runs the integrator with a zero delta and mode 1
(`002E5610`), adds the measure to `+0xB8` and sets bit 2; when clear it zeroes the accumulators
(`003DA9F0`: `+0x100`-`+0x108`, `+0xE8`, `+0xEC`, `+0xED`, `+0xEE`) and `+0xEF`.

The re-run's
`002E5380` adds the accumulators into the candidate delta and then zeroes them itself, so a push
moves the actor on its next candidate position and is gone the tick after.

The step then measures
the frame's displacement (planar unless record byte `+0x08` bit 2), zeroes it when record byte
`+0x0D` has bit 2 or 4 (clearing both), caps it by `002E8000` for the focus actor when positive
and `+0x0C` bit 4 is clear, stores it at the context's `+0xEC`, hands it to the render record
(`00420A10`) and the unit (`00329A80`), runs `002E4A40` and `002E6000(record, 0)`, and clears
`+0x0C` bit 4.

## Layouts

```
struct MovementBody base=02B4E4C0 count=128 size=0x130
+0x000  u16  prev   +0x002 u16 next   +0x004 u16 self   (0xFFFF none)
+0x006  u8   layer (00269EC0)          +0x007 u8 activeThisTick
+0x008  f32  weight (context +0x148)   +0x018 u64[2] pairBits
+0x030  placement: +0x30 f32[4] position, +0x40 f32[4] orientation, +0x50/+0x60 derived positions,
        +0x70 f32[4] displacement, +0x80 u8 cellClass, +0x82 i16 cell, +0x84 i16 secondCell,
        +0x86 u16 attr bits 13-17, +0x88 u16 attr bits 3-6, +0x8A u16 00231F80 bits, +0x8E u16 blockedMask,
        +0x90 u32 flags (bits 0-1 context +0x151, bit 2 attr bit 12, bit 3 second height above, bit 4 solver moved),
        +0x94/+0x98/+0x9C copies of the radii and height, +0xA0/+0xA4/+0xA8 inner shape,
        +0xAC f32 groundHeight, +0xB0/+0xB4 stepped radii, +0xC0 f32 secondHeight, +0xC8 f32 requestedSpeed
+0x0E0  f32  height  +0x0E4 f32 base   +0x0E8 f32 partner's push squared
+0x0EC  u8   pushed  +0x0ED u8 contacts  +0x0EE u8 soleMover  +0x0EF u8
+0x0F0  f32  radiusA +0x0F4 f32 radiusB  +0x0F8 f32 heading  +0x0FC f32 margin
+0x100  f32  pushX   +0x104 f32 pushY    +0x108 f32 pushZ
+0x110  u32  maskA   +0x114 u32 maskB    +0x119 u8 owner
+0x120  u32  sectorBits  +0x124 u32 sector  +0x128 f32 d - r  +0x12C f32 d + r

globals
02B57CC0  u16  active head    02B57CC4  u16  free head
02B57CE0  u64[32][2]  sector masks   02B57EE0  u64[2]  candidate set
02CA6034 / 02CA603C  f32  sector centre   02CA6040 / 02CA6048 / 02CA604C  the running mean
```

## Shipped data

| Constant | Value | Role |
|---|---|---|
| 128 | bodies, sectors' mask width, candidate bits | the pool and the pass are fixed |
| 32 | sectors | `0046AD20` |
| 50 | the percentage divisor | the inner shape |
| `{37, 50, 37}` | default percentages | non-class-3 actors |
| 0.25, 0.01 | the radius stepping | the placement tail |

## Operations

Per frame, each steerable actor's driver places its body and registers it in its sectors. Per
tick, the masks and active flags are reset, the active list is walked, each candidate pair is
resolved once in list order with pushes accumulating as it goes, and the per-slot step consumes the
push into the next candidate position.

## State

The pool and its two list heads, the 32 masks and the candidate set, the running mean and its
centre, each body's placement, accumulators, counters and pair bitmap.

## Modding notes

- Layers and owners are the cheap switches: equal layers pair, equal non-zero owners never do,
  an owner of zero contacts anything.
- The weight decides who yields: a mask bit `00314E10` honours gives one body the whole
  separation; a zero weight against a positive one makes the zero-weight body take all of it, and
  two zero weights split it evenly.
- The pass is order-dependent; a port that gathers all contacts and applies them afterwards
  produces different positions from the same inputs.
- The push lives in one subsystem and is consumed by another; keep the clear after the consume,
  not before.
- The pool is capped at 128; the 129th actor has no body and no collision, silently.
- The walk's index drift is shipped behaviour: a port that indexes both pointers by body reproduces
  the design, not the game.

## Related

- [Movement step](heading-speed-to-position-delta.md): the driver that registers the body.
- [Facing and steering](facing-and-steering.md): the facing writer that re-sizes the shape.
- [Actor record](../Characters-And-Objects/actor-record.md): the contexts the shape is sized from.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the per-slot step that consumes the push.
- [Area flags and navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md): the cell attributes.
