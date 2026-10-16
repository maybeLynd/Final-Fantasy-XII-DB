---
title: "Movement bodies and separation: the collision body every steerable actor carries, its placement on the field, and the tick that pushes overlapping bodies apart"
kind: "system"
category: "Movement and pathfinding"
addresses: "003DAE30, 002E8E20, 0026B2E0, 0026BBC0, 0026BF60, 00265390, 0026B170, 003DA8A0, 003DAD00, 002E3500, 00269EC0, 002682D0, 002685F0, 00268380, 003DAF20, 00380D30, 003808A0, 003DB1B0, 003DB020, 0046AD20, 003DAA40, 003DAC70, 003DAAB0, 003DAB50, 00314F30, 00314F50, 003DA5A0, 003DA730, 00314E10, 003DA9F0, 002E5180, 002E5380, 003B7730, 00266D10, 00269E60, 0026ABD0, 0026B9D0, 00263810, 0026A560, 0026BE00, 00263640, 002E86B0, 0026AB60, 0026BEE0, 0026BDD0, 002640E0"
---

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

`0026A7C0(record, on)` (verb `setfloatstatus`) sets or clears the controller's `+0x151` bit 1 and
re-runs `002682D0`; `0026ACE0` writes the same byte's bit 5. `002646A0` returns an actor's body,
`00264670` the ground height kept at the movement context's `+0xD4`, and `002644C0` and `00264EA0`
the controller's `+0x151` bits 0 and 7.

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

`0026A490(record)` sets the three percentages from the actor's character parameters (`003E6150`
of the render record id, times 50): `0x9002322` to `+0x104`, `0x9002524` to `+0x105` and `0x9002423`
to `+0x106`, or `{37, 50, 37}` without a render record, and re-sizes.

### Scale, radii and the interaction ellipses

A class-3 actor's movement context holds the scale and three `Ellipse` records, each kept as an
authored base and a scaled copy:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `020` | `f32[3]` | scale | x, y and z |
| `040` | `f32[3]` | offset | moves the interaction point (and the body, see `+0x107`) |
| `050` | `Ellipse` | body | the body radii: base `+0x80` scaled by the scale's x and z, read by `003DA710` |
| `060` | `Ellipse` | touch | base `+0x88` scaled |
| `070` | `Ellipse` | talk | base `+0x90` scaled |
| `080` | `f32[2]` | bodyBase | authored body radii |
| `088` | `f32[2]` | touchBase | authored touch radii |
| `090` | `f32[2]` | talkBase | authored talk radii |
| `0BC` | `f32` | talkHalfAngle | the facing window of the talk test |
| `0C8` | `f32` | talkHeight | band above, times the scale's y |
| `0CC` | `f32` | talkDepth | band below, times the scale's y |
| `0DD` | `u8` | noHeightTest | set by a negative talk height |
| `0DE` | `u8` | talkFollowsBody | the talk ellipse copies the body radii |
| `0DF` | `u8` | touchFollowsBody | the touch ellipse copies the body radii |
| `0FC` | `f32` | margin | separation margin, the mean of the scaled body radii |
| `107` | `u8` | offsetUse | bit 0 the offset moves the interaction point, bit 1 it moves the body |

`Ellipse` (0x10 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `f32` | a | radius |
| `04` | `f32` | b | radius |
| `08` | `f32` | angle | written by `003DA850` |
| `0C` | `f32` | margin | added by `003DA5A0` |

`002E8E20(record)`, called by the scale setters `0026B720` and `002E5FD0` (identical; verbs
`setscale`, `setscale_164`, `debug_setscale`), hands the scale to the render record (`002EE050`)
and re-applies the three bases. `0026B2E0(record, a, b)` sets the body base and scaled radii
(`003DA860`), sets the margin `+0xFC` to the mean of the two scaled radii (at least 0.01), and while
`+0xDE` or `+0xDF` is set copies the body radii into the talk or touch ellipse, with that ellipse's
own margin (`003DA890`); `0026B2D0` (verb `setradius`) passes one radius for both.

`0026BBC0(record, a, b)` sets the talk ellipse and clears `+0xDE`; `0026BF60` sets the touch ellipse
and clears `+0xDF`. For a class-1 object the same setters write the context's `+0x40` and `+0x30`
pairs unscaled, and `0026BF60` also sets `+0x5D` bit 1. The verbs reach them through:

- `0026BB50` (one radius for both; verb `debug_settalkradius`), `00239370(record, angle, height,
  radius)` (verb `btlAtelSetEventData`: each value only when not negative, through `0026BB50`,
  `0026BA00` and `0026B940`);
- `0023B260` (verb `btlAtelTreasureInit`: talk 1.5, touch 4.0) and `0023B2A0(record, touch, talk)`
  (verb `btlAtelTreasureInitWithRange`);
- `0026BD50` and `0026BFF0` (verbs `settalkwh`, `setwh`, `setrect`, `settouchwh`, `fieldsign`), which
  take absolute values; for a class-1 object they set `+0x5D` bit 2 or 1 and keep the inner (talk)
  pair no larger than the outer (touch) pair.

`0026B940` (verb `talkang`) sets the talk half-angle `+0xBC` (class 1 `+0x50`); `0026BA00` (verb
`settalkheight`) sets `+0xC8` with `+0xDD` raised for a negative height (class 1 `+0x68` and `+0x5C`)
and re-sizes; `0026BC70` (verb `fieldsign`) writes the angle of the touch and talk ellipses
(`003DA850`) and the wrapped angle to `+0x48`, which for a class-3 actor is the offset's z.

The offset: `0026B170(record, x, y, z)` stores it, sets actor byte `+0x0D` bit 5 when it is non-zero
(clears it for zero) and, when `+0x107` bit 1 is set and the offset changed, re-places the actor at its
position (`0026B0C0`). `0026B230(record, bits)` writes `+0x107` bits 0 and 1 and re-places the
actor when bit 1 changes; the verb `setposoffset` runs both. `0026BA70` (verb `settalkradiusoffset`)
stores the offset, sets bit 0 and clears bit 1, re-placing when bit 1 was set; `0026BB00` (verb
`fieldsign`) gives it an absolute point and stores the difference from the position.

The interaction point is what `00265390(record, &x, &y, &z)` returns: a class-1 object's `+0x10`
triple; for class 3 the position raised by the controller's `+0x140 + +0x144`, plus the offset when
`+0x107` bit 0 is set.

The talk test `0025BAD0` builds the same point, refuses a focus actor outside
the height band (`+0xC8` above, `+0xCC` below, both times the scale's y) unless `+0xDD` (the lower edge also less the focus actor's own height), needs the
focus body's ellipse to overlap the talk ellipse (`003DA5A0`), and checks the focus facing against
the half-angle (`003A1BB0`). The touch test `0025C230` uses the touch and talk ellipses
([script requests](../Scripts-And-Script-Commands/script-requests.md)).

### Heights, walk speed and the margin

These verbs write the rest of the context. Each setter tests the class first: a class-3 actor's
context or a class-1 object's is written, any other actor is left alone.

| Verb | Id | Handler | Setter | What it writes |
|---|---|---|---|---|
| `setheight(h)` | `0x00A7` | `0034D260` | `00269E60(h)`, then `0026ABD0(h * 0.25)` | class 3: height `+0xC0` and talk height `+0xC8` = `h`, `+0xDD` = `h < 0`, then `+0xC4` and the talk depth `+0xCC` = `h / 4`; class 1: `+0x68` = `h`, `+0x5C` = `h < 0`; the body is re-sized (`00268380`) |
| `setunderheight(v)` | `0x00A8` | `0034D6D0` | `0026ABD0` | class 3 only: `+0xC4` and `+0xCC` = `v` |
| `settalkheight(h)` | `0x018D` | `0034CAC0` | `0026BA00(h)`, then `0026B9D0(h * 0.25)` | the talk height (above), then the talk depth = `h / 4` |
| `settalkunderheight(v)` | `0x018E` | `0034CE60` | `0026B9D0` | the talk depth: class 3 `+0xCC`, class 1 `+0x6C` |
| `getdefaultheight()` | `0x02B0` | `003503D0` | `00263810` | a float result (`0026B4C0`): for class 3 the model's parameter `0x09001D1E` (`002E9630`, 0 without a render record), for class 1 `+0x68`, else 0 |
| `setwalkspeed(v)` | `0x020E` | `00352530` | `0026A560` | class 3 only: `+0xE0` = `v` |
| `setwalkthresholdspeed(v)` | `0x0247` | `0034CEA0` | `0026BE00` | class 3 only: `+0xE4` = `v`, then the render record's copy (`002E86B0`) |
| `setfreetargetw(n)` | `0x0264` | `00352500` | `0026AB60` | the integer `n` as a float, at least 0.01: class 3 the margin `+0xFC`, class 1 `+0x70` |
| `touchradius(r)` | `0x0051` | `00356000` | `0026BEE0` | class 3: the touch ellipse takes the body radii with `r` as its own margin (`003DA890`) and `+0xDF` is set; class 1: the touch pair `+0x30`/`+0x34` = `r` (`003DA860`) |

`00263810` also holds a branch that returns `+0xC0 * +0x24` for class 3, but the class-3 test in
front of it jumps to `002E9630` first (`0026381B`), so the branch never runs. The parameter it
reads is the one the presentation set-up hands to `00269E60`, so `getdefaultheight` answers the
model's authored height whatever `setheight` stored since.

The presentation set-up `002E28E0` gives `+0xE0` the model's parameter `0x09000606` and `+0xE4`
the parameter `0x09000707` times `[01DFE0BC]`, both 0 without a render record, and then runs
`00263640` (`002E2CF6`), which hands `+0xE4` to the render record as the verb does. The verb stores
its value as given, without the `[01DFE0BC]` factor.

`002E86B0(actor, v)` writes the render record's `+0x420` (`[022C6F28] + id * 0x740`, only when its
`+0x284` is non-zero). The locomotion selectors `004256E0` and `004255B0` compare the render
record's `+0x23C` with it: at or above it `004255B0` picks state 2 and `004256E0` state 2 or a
direction state 9 to 11; below it, down to the lower bound `003E58B0`, both pick state 1 or a
direction state 3 to 5. `0041F730` starts `+0x420` at 0.013333.

`002640E0(actor)` reads `+0xE0` back (0 for any class but 3). The move verbs push it as the speed
argument before running their body: `rcmove`/`cmove` (`0x003E`/`0x0059`, `003548B0`),
`rcmovea`/`cmovea` (`0x0040`/`0x005B`, `00348240`), `rmove`/`move` (`0x0042`/`0x005D`, `003488B0`),
`rmovea`/`movea` (`0x0044`/`0x005F`, `00349080`), `ramove` (`0x04CE`, `00349680`) and `ramovea`
(`0x04D0`, `00349D90`). The camera-side update reads it too ([player movement](player-movement.md)).

`fieldsign` (`00355A00`) also reads a third point record, or reuses the one it read last when the
third index is negative: `0026BDD0` stores its three coordinates at a class-1 object's
`+0x20`-`+0x28`, and `0026AB60` sets the margin to the mean of its two widths.

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

The driver's tail `002E6330` also appends the body's placement to a frame list (head `02B57CC8`,
tail `02B57CD0`, linked through the placement's `+0xA0`; `003DB0D0`) when actor byte `+0x09` has bit
6, `002E9FE0` holds and the controller's `+0x14E` is set; while `00263FB0()` is 1 it also needs the
controller's `+0x151` bit 7 (`00264EA0`). `003DAE20` returns the list's head; the highest-top search
`0046DB50` walks it ([geometry primitives](geometry-primitives.md)).

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
moves the actor on its next candidate position and is gone the tick after. `0025D540(record)`
clears the same accumulators (`003DA9F0`) and `+0xEF` outside the tick unless the lifecycle byte
`+0x18` is 1; the `setpos2` verbs run it.

The step then measures
the frame's displacement (planar unless record byte `+0x08` bit 2), zeroes it when record byte
`+0x0D` has bit 2 or 4 (clearing both), caps it by `002E8000` for the focus actor when positive
and `+0x0C` bit 4 is clear, stores it at the context's `+0xEC`, hands it to the render record
(`00420A10`) and the unit (`00329A80`), runs `002E4A40` and `002E6000(record, 0)`, and clears
`+0x0C` bit 4.

### The mask word

`0025B470(record, w)`, run by the verbs `bindp`, `bindhitobj` and `setweight`, keeps only bit 4 of
the body's mask word `+0x110` (`002E9BB0`, `002EC5B0`) and, for a negative `w` outside a cutscene
(`00377C20`) with actor byte `+0x15` zero, sets bit 4.

## Layouts

`MovementBody`: 128 records of `0x130` bytes at `02B4E4C0`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u16` | prev | previous body in its list, `FFFF` none |
| `002` | `u16` | next | next body in its list, `FFFF` none |
| `004` | `u16` | self | the body's own index |
| `006` | `u8` | layer | set by `00269EC0`; only equal layers pair |
| `007` | `u8` | activeThisTick | set by `003DB020`, cleared by `003DAA40` |
| `008` | `f32` | weight | the context's `+0x148` |
| `018` | `u64[2]` | pairBits | the pair bitmap the walk `003DAB50` remembers |
| `030` | `f32[4]` | position | start of the placement (placement `+0x00`); `{0, 0, 0, 1.0}` at allocation (`00380B80`) |
| `040` | `f32[4]` | orientation | the heading's direction pair, `+0x44` = 0, `+0x4C` = 1.0; `{0, 0, 1.0, 1.0}` at allocation (`00380B80`) |
| `050` | `f32[4]` | placement20 | four 1.0 at allocation (`00380B80`) |
| `060` | `f32[4]` | groundTint | vertex colours of the type-2 polygon underfoot, blended by `00231A90`; `0209A3A0` without one; four 1.0 (white) at allocation (`00380B80`) |
| `070` | `f32[4]` | displacement | the cell solver's push of the last move |
| `080` | `u8` | cellClass | the kind the floor overrides test (`00230A40`); its word is -1 at allocation (`00380B80`) |
| `082` | `i16` | cell | polygon underfoot, `-2` refused; -1 at allocation (`00380B80`) |
| `084` | `i16` | secondCell | the type-4 marker polygon |
| `086` | `u16` | floorGroup | attribute bits 13-17; `FFFF` at allocation (`00380B80`) |
| `088` | `u16` | mjGroup | attribute bits 3-6; `FFFF` at allocation (`00380B80`) |
| `08A` | `u16` | groundField | `00231F80`'s bits; `FFFF` at allocation (`00380B80`) |
| `08E` | `u16` | blockedMask | the field's blocked kinds (`00232090`) |
| `090` | `u32` | flags | bits 0-1 from the controller's `+0x151`, bit 2 attribute bit 12, bit 3 second height above, bit 4 the solver moved the body; bits 0-4 cleared at allocation (`00380B80`) |
| `094` | `f32[3]` | sizeCopy | copies of the two radii and the height; 0.5, 0.5, 2.0 at allocation (`00380B80`) |
| `0A0` | `f32[3]` | innerShape | the percentage-scaled radii and top; 0.5, 0.5, 2.0 at allocation (`00380B80`) |
| `0AC` | `f32` | groundHeight | plane height underfoot; 0 at allocation (`00380B80`) |
| `0B0` | `f32[2]` | steppedRadii | step toward `+0x94`/`+0x98` by 0.25; zero at allocation (`00380B80`) |
| `0C0` | `f32` | secondHeight | the second cell's height; zero at allocation (`00380B80`) |
| `0C8` | `f32` | requestedSpeed | `[01DFE0B8] * 30 * 3.6 * speed`; 18.0 at allocation (`00380B80`), the slot `00358CB0` later overwrites with the run speed |
| `0D0` | `void*` | frameLink | next placement in the frame list (`003DB0D0`); zero at allocation (`00380B80`) |
| `0E0` | `f32` | height | from `00268380` |
| `0E4` | `f32` | base | from `00268380` |
| `0E8` | `f32` | partnerPushSq | squared length of the partner's increment |
| `0EC` | `u8` | pushed | a pair pushed this body this tick |
| `0ED` | `u8` | contacts | counted by the pair resolver for each pair that moves the body |
| `0EE` | `u8` | soleMover | 1 when the body took a pair's whole push, cleared when a push was split |
| `0EF` | `u8` | pushSummary | set by `002E5380` from `+0xEC`, `+0xE8` and `+0xEE`; cleared with the accumulators |
| `0F0` | `f32` | radiusA | ellipse radius |
| `0F4` | `f32` | radiusB | ellipse radius; -1.0 on a freed body |
| `0F8` | `f32` | heading | the ellipse's angle |
| `0FC` | `f32` | margin | added to the separation |
| `100` | `f32[3]` | push | accumulated x, y and z |
| `110` | `u32` | maskA | the mask word `00314E10` and `0025B470` read |
| `114` | `u32` | maskB | the second mask word |
| `119` | `u8` | owner | equal non-zero owners never pair |
| `120` | `u32` | sectorBits | from `0046AD20` |
| `124` | `u32` | sector | the body's own sector |
| `128` | `f32` | nearDistance | `d - r`, 0 when `d <= r` |
| `12C` | `f32` | farDistance | `d + r` |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `02B57CC0` | `u16` | activeHead | first active body |
| `02B57CC4` | `u16` | freeHead | first free body |
| `02B57CC8` | `void*` | frameListHead | first placement linked by `003DB0D0` |
| `02B57CD0` | `void*` | frameListTail | last placement linked |
| `02B57CE0` | `u64[64]` | sectorMasks | 32 sectors, two words each |
| `02B57EE0` | `u64[2]` | candidates | the candidate set of `003DAAB0` |
| `02CA6034` | `f32` | centreX | sector centre x (`02CA603C` z) |
| `02CA6040` | `f32` | sumX | running sum of x (`02CA6048` z, `02CA604C` the count) |

`MovementContextHeights` (offsets from the start of the context):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `C0` | `f32` | height | class 3; setheight (`00269E60`), read by the shape `00268380` and the talk and touch tests |
| `C4` | `f32` | underHeight | class 3; written with the talk depth by `0026ABD0` |
| `E0` | `f32` | walkSpeed | class 3; model parameter `0x09000606`, setwalkspeed; read by `002640E0` |
| `E4` | `f32` | walkThreshold | class 3; parameter `0x09000707` times [`01DFE0BC`], setwalkthresholdspeed; copied to render +`0x420` |

`ObjectContextHeights` (offsets from the start of the context):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `20` | `f32[3]` | fieldsignPoint | the third fieldsign point (`0026BDD0`) |
| `30` | `f32[2]` | touch | touch radii (`0026BEE0`) |
| `5C` | `u8` | noHeightTest | h < 0 (`00269E60`, `0026BA00`) |
| `68` | `f32` | talkHeight | the band above (`00269E60`, `0026BA00`) |
| `6C` | `f32` | talkDepth | the band below (`0026B9D0`) |
| `70` | `f32` | margin | setfreetargetw (`0026AB60`) |

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
