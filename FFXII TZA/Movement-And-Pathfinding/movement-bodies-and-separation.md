---
title: "Movement bodies and separation: the collision body every steerable actor carries, its placement on the field, and the tick that pushes overlapping bodies apart"
kind: "system"
category: "Movement and pathfinding"
addresses: "0x003DAE30, 0x002E8E20, 0x0026B2E0, 0x0026BBC0, 0x0026BF60, 0x00265390, 0x0026B170, 0x003DA8A0, 0x003DAD00, 0x002E3500, 0x00269EC0, 0x002682D0, 0x002685F0, 0x00268380, 0x003DAF20, 0x00380D30, 0x003808A0, 0x003DB1B0, 0x003DB020, 0x0046AD20, 0x003DAA40, 0x003DAC70, 0x003DAAB0, 0x003DAB50, 0x00314F30, 0x00314F50, 0x003DA5A0, 0x003DA730, 0x00314E10, 0x003DA9F0, 0x002E5180, 0x002E5380, 0x003B7730, 0x00266D10, 0x00269E60, 0x0026ABD0, 0x0026B9D0, 0x00263810, 0x0026A560, 0x0026BE00, 0x00263640, 0x002E86B0, 0x0026AB60, 0x0026BEE0, 0x0026BDD0, 0x002640E0, 0x003E58B0, 0x00239E10, 0x003204D0, 0x003204E0, 0x003E6150, 0x002E28E0"
---

## What the player sees

Characters and foes crowding a doorway slide apart instead of standing inside one another, a
frame late. A heavy body pushes a light one further, two bodies on different layers pass through
each other, and an actor that stops registering with the world, because it left it, stops
participating on the very next tick. Every steerable actor stands on the ground at the height the
field gives it, and the cell it stands on tells the engine what kind of ground that is.

## How it works

### The pool

`0x02B4E4C0` holds 128 bodies of `0x130` bytes linked through `u16` indices: `+0` previous, `+2`
next, `+4` the body's own index, `0xFFFF` the null link. The free-list head is the word `0x02B57CC4`,
the active-list head `0x02B57CC0`. `0x003DAE30`, from the actor system's initialiser `0x00266D10`
(`0x00267141`), links every body to its neighbours (the first's previous and the last's next
`0xFFFF`), zeroes `+0x10`-`+0x17` and `+7`, sets the free head to 0 and the active head to empty,
zeroes `0x02B57CC8` and `0x02B57CD0`, and zeroes the 32 sector masks at `0x02B57CE0`.

`0x003DA8A0()` pops the free head and returns null when it is `0xFFFF`; it links the body at the
head of the active list, zeroes `+0x30`-`+0xDF`, sets `+0x82` = `0xFFFF`, `+0x88` = 0, runs
`0x00380B80` on the placement, sets `+8` = 1.0, `+6` = 0, `+0x10`-`+0x27` = 0, `+0xE8` = 0, runs
`0x003DA830` on `+0xF0` (overwritten by the shape writer below), and zeroes `+0x100`-`+0x10B`,
`+0x110`/`+0x114` and `+0x118`.

`0x003DAD00(body)` unlinks it from the active list, pushes it on the free list, writes `{0, -1.0, 0,
-1.0}` at `+0xF0` and clears `+7`; the -1.0 at `+0xF4` is what makes a freed body fail the
resolver's positive-radii test if it is ever handed to it.
Until the first release the n-th body allocated in an area is index `n - 1`.

### Attachment

`0x002E3500(record)` is the one creator. It returns at once without a secondary context at `+0xC0`;
otherwise it releases any body at `[+0xC0] + 0x138`, allocates one and stores the result there,
null included.

It then runs the five consumers: `0x00269EC0(record, 0)` sets the layer byte `+6`;
`0x002681D0`; `0x002682D0` copies the context's `+0x151` bits 0-1 into the body's flags `+0x90`;
`0x002685F0` copies the context's float `+0x148` into the weight `+8`; `0x00268380` sizes the shape.
Every consumer tests the chain and does nothing on a null body, so the 129th actor has no
collision body and silently drops out of the pass.

Its callers are the actor's presentation set-up `0x002E28E0` and `0x002E3580`, which releases the
presentation and re-creates; the releasers `0x002E3D00` and `0x002E3AF0` run from the per-type
presentation release and the manager release ([actor record](../Characters-And-Objects/actor-record.md)).
A body lives exactly as long as its actor's presentation.

`0x0026A7C0(record, on)` (verb `setfloatstatus`) sets or clears the controller's `+0x151` bit 1 and
re-runs `0x002682D0`; `0x0026ACE0` writes the same byte's bit 5. `0x002646A0` returns an actor's body,
`0x00264670` the ground height kept at the movement context's `+0xD4`, and `0x002644C0` and `0x00264EA0`
the controller's `+0x151` bits 0 and 7.

### The shape

`0x00268380(record)`: for a class-3 actor the radii pair comes from the movement context's `+0x50`
(`0x003DA710`); for any other class the two radii handed on are uninitialised stack values, so a
class-1 body's `+0xF0`/`+0xF4` hold whatever the stack held. The height is the movement context's `+0x68` for class 1 or `+0xC0 * +0x24` for
class 3; the heading `+0x38` for class 1 or `+0xA8` for class 3, else 0; the base is the secondary
context's `+0x140 + +0x144`; the three percentages are the movement context's bytes
`+0x104`-`+0x106` for class 3, else `{37, 50, 37}`.

`0x006C0520` writes `{radiusA, radiusB, heading,
0}` at the body's `+0xF0`, the height goes to `+0xE0` (`0x003DB130`), the base to `+0xE4`
(`0x003DB120`).

`0x003DAF20(body, a, b, c)` finishes: `+0x40`/`+0x48` = `cos`/`sin` of the heading
with `+0x44` = 0 and `+0x4C` = 1.0, the radii and height copied to `+0x94`-`+0x9C`, and the inner
shape `+0xA0` = `a * radiusA / 50`, `+0xA8` = `b * height / 50 + base`, `+0xA4` = `c * radiusB / 50`.
The facing writer re-sizes the same way ([facing and steering](facing-and-steering.md)).

`0x0026A490(record)` sets the three percentages from the actor's character parameters (`0x003E6150`
of the render record id, times 50): `0x9002322` to `+0x104`, `0x9002524` to `+0x105` and `0x9002423`
to `+0x106`, or `{37, 50, 37}` without a render record, and re-sizes.

### Scale, radii and the interaction ellipses

A class-3 actor's movement context holds the scale and three `Ellipse` records, each kept as an
authored base and a scaled copy:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x020` | `f32[3]` | scale | x, y and z |
| `+0x040` | `f32[3]` | offset | moves the interaction point (and the body, see `+0x107`) |
| `+0x050` | `Ellipse` | body | the body radii: base `+0x80` scaled by the scale's x and z, read by `0x003DA710` |
| `+0x060` | `Ellipse` | touch | base `+0x88` scaled |
| `+0x070` | `Ellipse` | talk | base `+0x90` scaled |
| `+0x080` | `f32[2]` | bodyBase | authored body radii |
| `+0x088` | `f32[2]` | touchBase | authored touch radii |
| `+0x090` | `f32[2]` | talkBase | authored talk radii |
| `+0x0BC` | `f32` | talkHalfAngle | the facing window of the talk test |
| `+0x0C8` | `f32` | talkHeight | band above, times the scale's y |
| `+0x0CC` | `f32` | talkDepth | band below, times the scale's y |
| `+0x0DD` | `u8` | noHeightTest | set by a negative talk height |
| `+0x0DE` | `u8` | talkFollowsBody | the talk ellipse copies the body radii |
| `+0x0DF` | `u8` | touchFollowsBody | the touch ellipse copies the body radii |
| `+0x0FC` | `f32` | margin | separation margin, the mean of the scaled body radii |
| `+0x107` | `u8` | offsetUse | bit 0 the offset moves the interaction point, bit 1 it moves the body |

`Ellipse` (0x10 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | a | radius |
| `+0x04` | `f32` | b | radius |
| `+0x08` | `f32` | angle | written by `0x003DA850` |
| `+0x0C` | `f32` | margin | added by `0x003DA5A0` |

`0x002E8E20(record)`, called by the scale setters `0x0026B720` and `0x002E5FD0` (identical; verbs
`setscale`, `setscale_164`, `debug_setscale`), hands the scale to the render record (`0x002EE050`)
and re-applies the three bases. `0x0026B2E0(record, a, b)` sets the body base and scaled radii
(`0x003DA860`), sets the margin `+0xFC` to the mean of the two scaled radii (at least 0.01), and while
`+0xDE` or `+0xDF` is set copies the body radii into the talk or touch ellipse, with that ellipse's
own margin (`0x003DA890`); `0x0026B2D0` (verb `setradius`) passes one radius for both.

`0x0026BBC0(record, a, b)` sets the talk ellipse and clears `+0xDE`; `0x0026BF60` sets the touch ellipse
and clears `+0xDF`. For a class-1 object the same setters write the context's `+0x40` and `+0x30`
pairs unscaled, and `0x0026BF60` also sets `+0x5D` bit 1. The verbs reach them through:

- `0x0026BB50` (one radius for both; verb `debug_settalkradius`), `0x00239370(record, angle, height,
  radius)` (verb `btlAtelSetEventData`: each value only when not negative, through `0x0026BB50`,
  `0x0026BA00` and `0x0026B940`);
- `0x0023B260` (verb `btlAtelTreasureInit`: talk 1.5, touch 4.0) and `0x0023B2A0(record, touch, talk)`
  (verb `btlAtelTreasureInitWithRange`);
- `0x0026BD50` and `0x0026BFF0` (verbs `settalkwh`, `setwh`, `setrect`, `settouchwh`, `fieldsign`), which
  take absolute values; for a class-1 object they set `+0x5D` bit 2 or 1 and keep the inner (talk)
  pair no larger than the outer (touch) pair.

`0x0026B940` (verb `talkang`) sets the talk half-angle `+0xBC` (class 1 `+0x50`); `0x0026BA00` (verb
`settalkheight`) sets `+0xC8` with `+0xDD` raised for a negative height (class 1 `+0x68` and `+0x5C`)
and re-sizes; `0x0026BC70` (verb `fieldsign`) writes the angle of the touch and talk ellipses
(`0x003DA850`) and the wrapped angle to `+0x48`, which for a class-3 actor is the offset's z.

The offset: `0x0026B170(record, x, y, z)` stores it, sets actor byte `+0x0D` bit 5 when it is non-zero
(clears it for zero) and, when `+0x107` bit 1 is set and the offset changed, re-places the actor at its
position (`0x0026B0C0`). `0x0026B230(record, bits)` writes `+0x107` bits 0 and 1 and re-places the
actor when bit 1 changes; the verb `setposoffset` runs both. `0x0026BA70` (verb `settalkradiusoffset`)
stores the offset, sets bit 0 and clears bit 1, re-placing when bit 1 was set; `0x0026BB00` (verb
`fieldsign`) gives it an absolute point and stores the difference from the position.

The interaction point is what `0x00265390(record, &x, &y, &z)` returns: a class-1 object's `+0x10`
triple; for class 3 the position raised by the controller's `+0x140 + +0x144`, plus the offset when
`+0x107` bit 0 is set.

The talk test `0x0025BAD0` builds the same point, refuses a focus actor outside
the height band (`+0xC8` above, `+0xCC` below, both times the scale's y) unless `+0xDD` (the lower edge also less the focus actor's own height), needs the
focus body's ellipse to overlap the talk ellipse (`0x003DA5A0`), and checks the focus facing against
the half-angle (`0x003A1BB0`). The touch test `0x0025C230` uses the touch and talk ellipses
([script requests](../Scripts-And-Script-Commands/script-requests.md)).

### Heights, walk speed and the margin

These verbs write the rest of the context. Each setter tests the class first: a class-3 actor's
context or a class-1 object's is written, any other actor is left alone.

| Verb | Id | Handler | Setter | What it writes |
|---|---|---|---|---|
| `setheight(h)` | `0x00A7` | `0x0034D260` | `0x00269E60(h)`, then `0x0026ABD0(h * 0.25)` | class 3: height `+0xC0` and talk height `+0xC8` = `h`, `+0xDD` = `h < 0`, then `+0xC4` and the talk depth `+0xCC` = `h / 4`; class 1: `+0x68` = `h`, `+0x5C` = `h < 0`; the body is re-sized (`0x00268380`) |
| `setunderheight(v)` | `0x00A8` | `0x0034D6D0` | `0x0026ABD0` | class 3 only: `+0xC4` and `+0xCC` = `v` |
| `settalkheight(h)` | `0x018D` | `0x0034CAC0` | `0x0026BA00(h)`, then `0x0026B9D0(h * 0.25)` | the talk height (above), then the talk depth = `h / 4` |
| `settalkunderheight(v)` | `0x018E` | `0x0034CE60` | `0x0026B9D0` | the talk depth: class 3 `+0xCC`, class 1 `+0x6C` |
| `getdefaultheight()` | `0x02B0` | `0x003503D0` | `0x00263810` | a float result (`0x0026B4C0`): for class 3 the model's parameter `0x09001D1E` (`0x002E9630`, 0 without a render record), for class 1 `+0x68`, else 0 |
| `getdefaultradiusw()` | `0x02B1` | `0x00350910` | `0x00263860` | a float result (`0x0026B4C0`): for class 3 the model's parameter `0x01002143`, or `0x01002D4F` in a town (`0x00377C20`, `0x002E9660`, 0 without a render record); for other classes the unset dword in its argument home slot `[rsp+8]`, so an undefined value |
| `getdefaultradiusd()` | `0x02B2` | `0x00350910` | `0x00263860` | the same handler, so the same value as `getdefaultradiusw` |
| `setwalkspeed(v)` | `0x020E` | `0x00352530` | `0x0026A560` | class 3 only: `+0xE0` = `v` |
| `setwalkthresholdspeed(v)` | `0x0247` | `0x0034CEA0` | `0x0026BE00` | class 3 only: `+0xE4` = `v`, then the render record's copy (`0x002E86B0`) |
| `setfreetargetw(n)` | `0x0264` | `0x00352500` | `0x0026AB60` | the integer `n` as a float, at least 0.01: class 3 the margin `+0xFC`, class 1 `+0x70` |
| `touchradius(r)` | `0x0051` | `0x00356000` | `0x0026BEE0` | class 3: the touch ellipse takes the body radii with `r` as its own margin (`0x003DA890`) and `+0xDF` is set; class 1: the touch pair `+0x30`/`+0x34` = `r` (`0x003DA860`) |

`0x00263810` also holds a branch that returns `+0xC0 * +0x24` for class 3, but the class-3 test in
front of it jumps to `0x002E9630` first (`0x0026381B`), so the branch never runs. The parameter it
reads is the one the presentation set-up hands to `0x00269E60`, so `getdefaultheight` answers the
model's authored height whatever `setheight` stored since.

The presentation set-up `0x002E28E0` gives `+0xE0` the model's parameter `0x09000606` and `+0xE4`
the parameter `0x09000707` times `[0x01DFE0BC]`, both 0 without a render record, and then runs
`0x00263640` (`0x002E2CF6`), which hands `+0xE4` to the render record as the verb does. The verb stores
its value as given, without the `[0x01DFE0BC]` factor.

`0x002E86B0(actor, v)` writes the render record's `+0x420` (`[0x022C6F28] + id * 0x740`, only when its
`+0x284` is non-zero). The locomotion selectors `0x004256E0` and `0x004255B0` compare the render
record's `+0x23C` with it: at or above it `0x004255B0` picks state 2 and `0x004256E0` state 2 or a
direction state 9 to 11; below it, down to the lower bound `0x003E58B0`, both pick state 1 or a
direction state 3 to 5. `0x0041F730` starts `+0x420` at 0.013333.

Both thresholds are `@FCP` section 9 words ([model files](../Graphics/model-files-cm-ca.md),
property ids `09 00 DD FF`):

- The walk threshold `0x003E58B0(record)` is section 9's float `+0x34`, or `+0x30` while the record's `+0x284` bit 18 is
  set (`0x003E58CF`-`0x003E58F9`), times the three scales `+0x260`, `+0x160` and `+0x26C`; 0.013333 (`0x00D117B8`) for a
  record with no `@FCP` payload or no section 9.
- The run threshold `+0x420` has three writers, all through `0x002E86B0`. The presentation set-up hands the actor's
  `+0xE4` (`0x00263640`, `0x002E2CF6`): property `0x09000707`, section 9 float slot 7, which `0x003E6150` multiplies by the
  scale `+0x26C`, then times `[0x01DFE0BC]` = 1.0 (`0x002E2CCE`-`0x002E2CEE`). The verb `setwalkthresholdspeed` hands its
  value (`0x0026BE00`). The unit set-up `0x00239E10` hands the unit's float `+0x184` (`0x0023A006`-`0x0023A012`).
- `0x00239E10` fills `+0x184` from one of two properties (`0x00239E33`-`0x00239E5F`, `0x00239EB5`-`0x00239ECC`):
  - `0x003204D0(unit, 9)`, property `0x09000707`, when the unit's row `+0x698` byte `+5` is 1 and byte `+0x13` of its
    `+0xE60` block is not `0xFF`;
  - `0x003204D0(unit, 2)`, property `0x09000101`, otherwise.
  `0x003204E0` takes both through `0x002ECE50` and multiplies them by the actor's scale, the third output of `0x00265240`
  (`0x00320545`-`0x0032057A`; [action range](../Battle-Actions/action-range.md)).
- `+0xE0`, the speed the move verbs push, is property `0x09000606`, section 9 float slot 6, scaled by `+0x26C` the
  same way (`0x002E2CA1`-`0x002E2CB3`).

`0x003E6150` returns 0 for a model without `@FCP`. A model with `@FCP` but no section 9 gets the default table
`0x01F265B0`: slot 6 is 0.0666667 and slots 1 and 7 are 0.13333.

`0x002640E0(actor)` reads `+0xE0` back (0 for any class but 3). The move verbs push it as the speed
argument before running their body: `rcmove`/`cmove` (`0x003E`/`0x0059`, `0x003548B0`),
`rcmovea`/`cmovea` (`0x0040`/`0x005B`, `0x00348240`), `rmove`/`move` (`0x0042`/`0x005D`, `0x003488B0`),
`rmovea`/`movea` (`0x0044`/`0x005F`, `0x00349080`), `ramove` (`0x04CE`, `0x00349680`) and `ramovea`
(`0x04D0`, `0x00349D90`). The camera-side update reads it too ([player movement](player-movement.md)).

`fieldsign` (`0x00355A00`) also reads a third point record, or reuses the one it read last when the
third index is negative: `0x0026BDD0` stores its three coordinates at a class-1 object's
`+0x20`-`+0x28`, and `0x0026AB60` sets the margin to the mean of its two widths.

### The placement record

The body's `+0x30` is the actor's field placement. `0x00380D30(placement, candidate)` resolves the
field (`0x0026E500(0)`) and the candidate's cell (`0x00233050`, `0x00233110`); when the cell `+0x52` is
valid it stores the field's blocked-class mask (`0x00232090`) at `+0x5E` and, unless the placement's
class byte `+0x50` is in it, copies the candidate's four floats, stores the ground height
(`0x00231890`) at `+0x7C` and into the position's y unless flag `+0x60` bit 0 holds; a blocked class
sets the cell to -2.

`0x003808A0(placement, field)` then returns at once with `+0x54` = `0xFFFF`
when the cell is negative (the -2 included), so a blocked placement keeps its stale attribute
words; otherwise it reads the cell record (`[field + 0x10] + cell
* 32`, attribute dword `+0xC`) through the mask table `0x0209A2D0` (`0x00232020`): bits 13-17 to `+0x56`,
bits 3-6 to `+0x58`, `0x00231F80`'s bits to `+0x5A`, attribute bit 12 to flag bit 2; `0x00231A90`; the
second cell `+0x54`'s height to `+0x90` with flag bit 3 when above the ground height; and its tail
steps `+0x80`/`+0x84` toward `+0x64`/`+0x68` by at most 0.25 per step, re-resolving the cell
(`0x00233050`, `0x00232760`) until within 0.01.

`0x003DB1B0(body)` runs the placement on `body + 0x30` and returns whether the cell is valid; the
movement step reaches it through `0x002E5C90`. In body terms the fields are `+0x30` position, `+0x70`
displacement, `+0x80` cell class, `+0x82` cell (-2 refused), `+0x84` second cell, `+0x86`/`+0x88`/
`+0x8A` the attribute words, `+0x8E` the blocked mask, `+0x90` flags, `+0xAC` ground height, `+0xC0`
second height, `+0xC8` requested speed.

### Registering every frame

The movement step's driver (`0x002E5030`) calls `0x003DB020(body, x, z, 0, &radii)` when `0x002EA7F0`
passes ([movement step](heading-speed-to-position-delta.md)). It sets `+7`, active this tick, and
when the two-globals gate `0x003B7730` holds computes the body's sector bits with
`0x0046AD20(body + 0x120, x, z, max(radii))` and ORs the body's own bit into the 128-bit mask of every
sector set (`0x02B57CE0`, sixteen bytes per sector).

`0x0046AD20` is not a grid. It keeps a running mean of every registered position (`0x02CA6040`/
`0x02CA6048` sums, `0x02CA604C` count) and a centre at `0x02CA6034`/`0x02CA603C`; the body's offset from the
centre gives a distance `d` and a sector `floor(angle / 2pi * 32)` of 32 around it. With `d > r`
the body occupies its sector widened by `floor(atan2(r, sqrt(d^2 - r^2)) / pi * 16) + 1` sectors
each side; with `d <= r` all 32.

The result is `+0x120` the bits, `+0x124` the sector, `+0x128`
`d - r` (0 when `d <= r`) and `+0x12C` `d + r`; a negative radius clears all four. The sums and
the count are updated even when the record pointer is null.

The driver's tail `0x002E6330` also appends the body's placement to a frame list (head `0x02B57CC8`,
tail `0x02B57CD0`, linked through the placement's `+0xA0`; `0x003DB0D0`) when actor byte `+0x09` has bit
6, `0x002E9FE0` holds and the controller's `+0x14E` is set; while `0x00263FB0()` is 1 it also needs the
controller's `+0x151` bit 7 (`0x00264EA0`). `0x003DAE20` returns the list's head; the highest-top search
`0x0046DB50` walks it ([geometry primitives](geometry-primitives.md)).

### The separation pass

`World_UpdateSimulationTick` first runs `0x003DAA40` (`0x003140C5`): the 32 masks are zeroed and every
body's `+7` cleared, so a body that does not register during the frame is not active for the pass.
Its tail runs `0x003DAC70(0x00314F30)` (`0x00314244`) over the active list:

1. `0x003DAAB0(bits, self)` builds the candidate set at `0x02B57EE0`: the OR of the masks of the body's
   sectors, with its own bit and every lower index cleared, so each pair is visited once;
2. `0x003DAB50(dMin, dMax, body, callback)` walks the candidate set a byte at a time and, at each
   position that is a candidate or whose pair bit is still set in the body's pair bitmap `+0x18`
   (the bit numbered by the walk's step count, not by the position; see the drift below), clears
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

`0x00314F30(A, B)` calls `0x00314F50(A, B, 1, &out)`. In push mode (`mode` 1) it refuses, returning 0,
unless both bodies have positive radii `+0xF0` and `+0xF4`, both are active this tick, their layer
bytes `+6` are equal, and A's owner byte `+0x119` is zero or differs from B's; query mode (`mode`
0, from `0x00313F80`) skips the active test and every write.

With `0x003DAE00` reading each position
offset by the accumulated pushes `+0x100`/`+0x108`, the vertical spans `[y + base, y + base +
height]` must overlap, and `0x003DA5A0` must return a negative separation: the horizontal distance
minus each body's ellipse extent along the joining line (`0x003DA730`: the offset rotated by the
body's heading, `(x^2 + z^2) / (x^2 / a^2 + z^2 / b^2)`) and the margins `+0xFC`.

The weights `+8` (both negated when both negative, both 1 when both zero) go through `0x00314E10`,
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

`0x002E5180(record)`, from the world tick's per-slot step (`0x002623A0`, `0x0025E400`), clears the
controller's `+0x151` bit 2, stores the ground height (`0x003DADE0`) at the movement context's
`+0xD4` and, when the body's `+0xEC` is set, re-runs the integrator with a zero delta and mode 1
(`0x002E5610`), adds the measure to `+0xB8` and sets bit 2; when clear it zeroes the accumulators
(`0x003DA9F0`: `+0x100`-`+0x108`, `+0xE8`, `+0xEC`, `+0xED`, `+0xEE`) and `+0xEF`.

The re-run's
`0x002E5380` adds the accumulators into the candidate delta and then zeroes them itself, so a push
moves the actor on its next candidate position and is gone the tick after. `0x0025D540(record)`
clears the same accumulators (`0x003DA9F0`) and `+0xEF` outside the tick unless the lifecycle byte
`+0x18` is 1; the `setpos2` verbs run it.

The step then measures
the frame's displacement (planar unless record byte `+0x08` bit 2), zeroes it when record byte
`+0x0D` has bit 2 or 4 (clearing both), caps it by `0x002E8000` for the focus actor when positive
and `+0x0C` bit 4 is clear, stores it at the context's `+0xEC`, hands it to the render record
(`0x00420A10`) and the unit (`0x00329A80`), runs `0x002E4A40` and `0x002E6000(record, 0)`, and clears
`+0x0C` bit 4.

### The mask word

`0x0025B470(record, w)`, run by the verbs `bindp`, `bindhitobj` and `setweight`, keeps only bit 4 of
the body's mask word `+0x110` (`0x002E9BB0`, `0x002EC5B0`) and, for a negative `w` outside a town
(the town flag `0x00377C20`) with actor byte `+0x15` zero, sets bit 4.

## Layouts

`MovementBody`: 128 records of `0x130` bytes at `0x02B4E4C0`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u16` | prev | previous body in its list, `FFFF` none |
| `+0x002` | `u16` | next | next body in its list, `FFFF` none |
| `+0x004` | `u16` | self | the body's own index |
| `+0x006` | `u8` | layer | set by `0x00269EC0`; only equal layers pair |
| `+0x007` | `u8` | activeThisTick | set by `0x003DB020`, cleared by `0x003DAA40` |
| `+0x008` | `f32` | weight | the context's `+0x148` |
| `+0x018` | `u64[2]` | pairBits | the pair bitmap the walk `0x003DAB50` remembers, one bit per walk step (`0x003DAB91`, `0x003DAC0B`), tested at `0x003DABD8` and rewritten at `0x003DABE8` / `0x003DABFF` |
| `+0x030` | `f32[4]` | position | start of the placement (placement `+0x00`); `{0, 0, 0, 1.0}` at allocation (`0x00380B80`) |
| `+0x040` | `f32[4]` | orientation | the heading's direction pair, `+0x44` = 0, `+0x4C` = 1.0; `{0, 0, 1.0, 1.0}` at allocation (`0x00380B80`) |
| `+0x050` | `f32[4]` | placement20 | four 1.0 at allocation (`0x00380B80`) |
| `+0x060` | `f32[4]` | groundTint | vertex colours of the type-2 polygon underfoot, blended by `0x00231A90`; `0x0209A3A0` without one; four 1.0 (white) at allocation (`0x00380B80`) |
| `+0x070` | `f32[4]` | displacement | the cell solver's push of the last move |
| `+0x080` | `u8` | cellClass | the kind the floor overrides test (`0x00230A40`); its word is -1 at allocation (`0x00380B80`) |
| `+0x082` | `i16` | cell | polygon underfoot, `-2` refused; -1 at allocation (`0x00380B80`) |
| `+0x084` | `i16` | secondCell | the type-4 marker polygon |
| `+0x086` | `u16` | floorGroup | attribute bits 13-17; `FFFF` at allocation (`0x00380B80`) |
| `+0x088` | `u16` | mjGroup | attribute bits 3-6; `FFFF` at allocation (`0x00380B80`) |
| `+0x08A` | `u16` | groundField | `0x00231F80`'s bits; `FFFF` at allocation (`0x00380B80`) |
| `+0x08E` | `u16` | blockedMask | the field's blocked kinds (`0x00232090`) |
| `+0x090` | `u32` | flags | bits 0-1 from the controller's `+0x151`, bit 2 attribute bit 12, bit 3 second height above, bit 4 the solver moved the body; bits 0-4 cleared at allocation (`0x00380B80`) |
| `+0x094` | `f32[3]` | sizeCopy | copies of the two radii and the height; 0.5, 0.5, 2.0 at allocation (`0x00380B80`) |
| `+0x0A0` | `f32[3]` | innerShape | the percentage-scaled radii and top; 0.5, 0.5, 2.0 at allocation (`0x00380B80`) |
| `+0x0AC` | `f32` | groundHeight | plane height underfoot; 0 at allocation (`0x00380B80`) |
| `+0x0B0` | `f32[2]` | steppedRadii | step toward `+0x94`/`+0x98` by 0.25; zero at allocation (`0x00380B80`) |
| `+0x0C0` | `f32` | secondHeight | the second cell's height; zero at allocation (`0x00380B80`) |
| `+0x0C8` | `f32` | requestedSpeed | `[0x01DFE0B8] * 30 * 3.6 * speed`; 18.0 at allocation (`0x00380B80`), the slot `0x00358CB0` later overwrites with the run speed |
| `+0x0D0` | `void*` | frameLink | next placement in the frame list (`0x003DB0D0`); zero at allocation (`0x00380B80`) |
| `+0x0E0` | `f32` | height | from `0x00268380` |
| `+0x0E4` | `f32` | base | from `0x00268380` |
| `+0x0E8` | `f32` | partnerPushSq | squared length of the partner's increment |
| `+0x0EC` | `u8` | pushed | a pair pushed this body this tick |
| `+0x0ED` | `u8` | contacts | counted by the pair resolver for each pair that moves the body |
| `+0x0EE` | `u8` | soleMover | 1 when the body took a pair's whole push, cleared when a push was split |
| `+0x0EF` | `u8` | pushSummary | set by `0x002E5380` from `+0xEC`, `+0xE8` and `+0xEE`; cleared with the accumulators |
| `+0x0F0` | `f32` | radiusA | ellipse radius |
| `+0x0F4` | `f32` | radiusB | ellipse radius; -1.0 on a freed body |
| `+0x0F8` | `f32` | heading | the ellipse's angle |
| `+0x0FC` | `f32` | margin | added to the separation |
| `+0x100` | `f32[3]` | push | accumulated x, y and z |
| `+0x110` | `u32` | maskA | the mask word `0x00314E10` and `0x0025B470` read |
| `+0x114` | `u32` | maskB | the second mask word |
| `+0x119` | `u8` | owner | equal non-zero owners never pair |
| `+0x120` | `u32` | sectorBits | from `0x0046AD20` |
| `+0x124` | `u32` | sector | the body's own sector |
| `+0x128` | `f32` | nearDistance | `d - r`, 0 when `d <= r` |
| `+0x12C` | `f32` | farDistance | `d + r` |

Three ranges the table above does not list:

`MovementBody` (`0x130` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x010` | `u8[8]` | cleared010 | the eight bytes before the pair bitmap `+0x18`: the allocation `0x003DA8A0` zeroes them with the bitmap (`0x003DA9A0`) and the pool initialiser `0x003DAE30` zeroes them for every body (`0x003DAE6D`) |
| `+0x050` | `f32[4]` | modelTint | the colour the actor's models are tinted with (red, green, blue, fourth): `0x002E4A40` hands the first three to `0x002EDD70` for each of the actor's models (`0x002E4AD9`-`0x002E4B44`), white when the controller's `+0x151` bit 5 is set; `0x002ED6A0` refreshes it from the ground tint `+0x60` (`0x002ED6CF`-`0x002ED6E4`) or, with actor byte `+0xB` bit 6 set, from a fresh sample at the position through `0x0026E530` (`0x0026E5A1`); four 1.0 at allocation (`0x00380C05`-`0x00380C1A`) |
| `+0x118` | `u8` | cleared118 | set to 0 with the owner byte `+0x119` by the allocation's word store (`0x003DA995`) |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02B57CC0` | `u16` | activeHead | first active body |
| `0x02B57CC4` | `u16` | freeHead | first free body |
| `0x02B57CC8` | `void*` | frameListHead | first placement linked by `0x003DB0D0` |
| `0x02B57CD0` | `void*` | frameListTail | last placement linked |
| `0x02B57CE0` | `u64[64]` | sectorMasks | 32 sectors, two words each |
| `0x02B57EE0` | `u64[2]` | candidates | the candidate set of `0x003DAAB0` |
| `0x02CA6034` | `f32` | centreX | sector centre x (`0x02CA603C` z) |
| `0x02CA6040` | `f32` | sumX | running sum of x (`0x02CA6048` z, `0x02CA604C` the count) |

`MovementContextHeights` (offsets from the start of the context):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xC0` | `f32` | height | class 3; setheight (`0x00269E60`), read by the shape `0x00268380` and the talk and touch tests |
| `+0xC4` | `f32` | underHeight | class 3; written with the talk depth by `0x0026ABD0` |
| `+0xE0` | `f32` | walkSpeed | class 3; model parameter `0x09000606`, setwalkspeed; read by `0x002640E0` |
| `+0xE4` | `f32` | walkThreshold | class 3; parameter `0x09000707` times [`0x01DFE0BC`], setwalkthresholdspeed; copied to render `+0x420` |

`ObjectContextHeights` (offsets from the start of the context):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x20` | `f32[3]` | fieldsignPoint | the third fieldsign point (`0x0026BDD0`) |
| `+0x30` | `f32[2]` | touch | touch radii (`0x0026BEE0`) |
| `+0x5C` | `u8` | noHeightTest | h < 0 (`0x00269E60`, `0x0026BA00`) |
| `+0x68` | `f32` | talkHeight | the band above (`0x00269E60`, `0x0026BA00`) |
| `+0x6C` | `f32` | talkDepth | the band below (`0x0026B9D0`) |
| `+0x70` | `f32` | margin | setfreetargetw (`0x0026AB60`) |

## Shipped data

| Constant | Value | Role |
|---|---|---|
| 128 | bodies, sectors' mask width, candidate bits | the pool and the pass are fixed |
| 32 | sectors | `0x0046AD20` |
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

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA6038` | `f32` | 0 (zero-filled tail of `.data`) | the centre's y. `0x0046AFA0`, which the tick `0x00314020` runs (`0x003140CA`), divides the sums `0x02CA6040`, `0x02CA6044` and `0x02CA6048` by the count `0x02CA604C` (1.0 when the count is 0) into `0x02CA6034`-`0x02CA603C` and zeroes the sums and the count (`0x0046AFA0`-`0x0046B017`). no instruction in the index adds to the y sum, so the centre's y stays 0.0 as far as this census reaches | `0x0046AFA0` (`0x0046B00F`) | no instruction names it |
| `0x02CA6044` | `f32` | 0 (zero-filled tail of `.data`) | the y sum: `0x0046AD20` adds only to the x and z sums, so this stays 0 | `0x0046AFA0`, 0 (`0x0046AFD9`) | `0x0046AFA0` (`0x0046AFC3`) |

## Modding notes

- Layers and owners are the cheap switches: equal layers pair, equal non-zero owners never do,
  an owner of zero contacts anything.
- The weight decides who yields: a mask bit `0x00314E10` honours gives one body the whole
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
