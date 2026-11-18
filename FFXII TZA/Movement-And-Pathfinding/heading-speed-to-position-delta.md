[Home](../../README.md) / [Movement and pathfinding](README.md) / Movement step

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Movement step: how yaw, pitch and speed become a character's per-frame displacement, when motion is flat, and how animation takes the wheel | system | Movement and pathfinding | How actors move | The innermost movement seam: the per-frame driver that runs steering, computes the step, publishes the angles and integrates the position; the class gate every movement call shares; the spherical decomposition of yaw, pitch and speed and the flat branch that drops the pitch; the two controller flags and the runtime gate that choose flat or three-dimensional motion; the animation-state override that replaces or decays the step; the pass-through path; the two integration paths and the displacement measure; and the setters that feed the angles and the speed, including the battle unit's intent. | 0x002E5030, 0x002E4380, 0x00424080, 0x002E5610, 0x002E5380, 0x002E54A0, 0x002E5C10, 0x00329B00, 0x0026D6F0, 0x0026D6A0, 0x0026A330, 0x002E55C0, 0x0026A0D0, 0x0026A060, 0x0023A070, 0x00265200, 0x00265020, 0x00267260, 0x00264460, 0x003B7730, 0x003B6ED0, 0x003B7E10, 0x003B7E20, 0x003A1D30, 0x002E9BB0, 0x002EC5B0, 0x0025DF00, 0x00263C80 |

## What the player sees

Every character, monster and NPC moves as a sequence of small steps, each computed from a facing,
a climb angle and a speed. A character the game steers toward a point above or below it aims its
step at that point: part of the speed goes into the climb, so it covers less ground per frame
than one steered toward a point at its own height, and the steeper the aim the less of the speed
goes forward. A creature flagged as a ground mover gets the flat version instead, where the whole
speed goes forward whatever the aim.

Some things never walk. The engine checks an actor's class before it accepts a speed or a heading
or produces a step, and anything outside that class silently refuses: no error, no movement, a
zero step.

Animation can take over the step. When a character that has been in one animation state for at
least one second (30 frames at 30 fps, 60 at 60) is given a speed of 0, the step keeps the facing
and speed the character had a moment before, shrinking to 0.83 of itself each frame with no
lower limit, and lets go once that speed is 0.05 or less: the character slides to a halt instead
of stopping dead, and the facing and speed the game sets meanwhile are
set aside. Two other animation states lower the speed each frame, and one holds it at 0.

## How it works

### The class gate

Movement belongs to one actor class: the top three bits of the byte at actor `+0x03` must be 3
(`(byte & 0xE0) == 0x60`). The same test opens the speed setter `0x0026D6F0`, the yaw setter
`0x0026A0D0`, the pitch setter `0x0026A060`, the delta `0x002E4380` and, twice, the frame driver
`0x002E5030`. A refusal returns without a status. The position reader `0x00265020` tests the same
byte as a value and admits classes 1 and 3, and on refusal writes zeros into its three outputs
([actor record](../Characters-And-Objects/actor-record.md)).

### The per-frame driver

`0x002E5030(actor, mode, override)` runs once per field-runtime pass for each scheduled record
(`0x0025E39B` in the wait resolver `0x0025DF00`, [field runtime](../Characters-And-Objects/field-runtime.md)).
It refuses when the record's lifecycle byte `+0x18` is 1, the controller `+0xC0` is null or its
byte `+0x14F` has bit `0x1`, or the class is not 3. Otherwise, with the movement context `+0xB8` and
the movement body `[controller + 0x138]`:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | when the steering request's mode byte (`[context + 0xF0] + 0x29`) is 1 to 4, it runs the steering update `0x002E45E0` ([facing and steering](facing-and-steering.md)); |   |
| 2 | it computes the step: `0x002E4380(actor, &delta, mode, override)`; |   |
| 3 | it publishes pitch `+0xA0` and yaw `+0xA4` to the render record (`0x002E5C10`, the record's `+0x240`, `+0x244`, `+0x248` = 0, when `[0x022C6F28] + id * 0x740` has a non-zero `+0x284`; it writes nothing when the actor or its controller is null, the controller's dword `+0x00` is -1, its low word `id` is -1 or the record address comes out 0, `0x002E5C13`-`0x002E5C4A`); |   |
| 4 | it integrates: `context + 0xB8` = `0x002E5610(actor, body, context, &delta, 0)`, the squared displacement, with mode 0; | `0x002E50F0` |
| 5 | when `0x002EA7F0(actor)` is non-zero it registers the body's cell from the context's position, plus the offset at `+0x40`/`+0x48` when byte `+0x107` has bit `0x2` (`0x003DB020`, [movement bodies and separation](movement-bodies-and-separation.md); its arguments are `(body, x, z, &radii)`, the radii being the body's `+0xF0`, `0x002E5136`); |   |
| 6 | it runs `0x002E6330(actor)` when the class is still 3, the driver's second class test. | `0x002E5145`-`0x002E515A` |

The driver's own `mode` and `override` arrive from the resolver and are passed to the delta
unchanged; from the walking path `mode` is 0.

### The step

`0x002E4380(actor, out, passThrough, vector)` zeroes `out.xyz` first and writes `out.w` = 1.0 on
every exit, so a refused call returns `{0, 0, 0, 1}` and nothing distinguishes refusal from a
computed zero. With `passThrough` non-zero it copies the caller's vector into `out`, stores
`sqrtf(|x^2 + y^2 + z^2|)` (`0x003A1D30`, which masks the sign and tail-calls `sqrtf`) at the
context's `+0xF8` and returns; yaw, pitch and speed play no part. The caller's vector has to be
a separate buffer from the output, because the zeroing comes first.

Otherwise it reads the speed `+0xD0`, repairs a negative `+0xF8` to that speed, and wraps yaw
`+0xA4` and pitch `+0xA0` into a single turn each: with `b = (a >= 0) ? pi : -pi`,
`wrap(a) = ((a + b) - trunc((a + b) / 2pi) * 2pi) - b` (`pi` at `0x01CEBC50`, `-pi` at `0x00915620`,
`2pi` at `0x01CEBC78`). The truncation rounds toward zero, which is why the bias follows the sign;
an exact `+pi` comes back as `-pi` and `-pi` as `+pi`.

When the controller exists and its first dword is not -1, the animation override `0x00424080`
receives that dword's low word as the record id¹, the wrapped yaw and the speed by address (next
section). Then, with the possibly rewritten values:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E44FD` |

</details>

```python
speed == 0                                  : out = {0, 0, 0, 1}
flat (0x00267260 != 0 and 0x00264460 == 0)      : out = {sin(yaw) * speed, 0, cos(yaw) * speed, 1}
otherwise                                   : out = {sin(yaw) * cos(pitch) * speed,
                                                     sin(pitch) * speed,
                                                     cos(yaw) * cos(pitch) * speed, 1}
```

`sinf` and `cosf` are the CRT imports. On the three-dimensional path the horizontal components
are scaled by `speed * cos(pitch)`, so a climbing actor covers less ground per frame than one on
the flat at the same requested speed.

The wrapped angles and the override's yaw and speed live only in locals: nothing writes them back to `+0xA0`,
`+0xA4` or `+0xD0`. The step's one store into the context is `+0xF8`, the repair on the normal path¹
or the magnitude on the pass-through².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E445C` |
| ² | `0x002E43E6` |

</details>

### Flat or three-dimensional

Two predicates on the controller at actor `+0xC0` decide the branch, and three-dimensional is the
default:

- `0x00264460(actor)` returns `(b | b >> 1) & 1` for the controller's byte `+0x151`: either bit `0x1` or
  bit `0x2` selects three-dimensional motion. A null actor or controller returns 0.
- `0x00267260(actor)` returns actor byte `+0x08` bit `0x2` when all of these hold: `0x003B7730()` is
  non-zero, the controller is null or has `+0x14F` bit `0x1` clear and a body at `+0x138`, and actor
  byte `+0x09` has bit `0x1`.

`0x003B7730` is `0x02B40530 != 0 && 0x02B40534 != 0`. Both are zero in the image. `0x003B6ED0`, the actor
module's reset, sets both to 1; `0x02B40530` also has the setter `0x003B7E10`, called with 1 from
`0x0024C6B0`, `0x0024C870` and `0x00262870` and with 0 from `0x0024B6F0` and twice from `0x003B8670`; and
`0x02B40534` is cleared at the head of the bulk actor walk `0x003B7E20` and set again by `0x003B7BB0`
and `0x003B7C60`, with four more writers in `0x003B7E00`, `0x003B72F0`, `0x003B6F30` and `0x003B7080`. So
the flat path is switched off mid-session while the actor list is being
rewritten, not only before bring-up.

The reset `0x003B6ED0` sets `0x02B40534` first¹ and `0x02B40530` last². Between them it zeroes
the 32 bytes at `0x02EBCA80` and `0x02EBCA90`³, the dword `0x02EBCAA0`, the summon group's
unique count `0x02EBCBC0`, its 32 handles at `0x02EBCBE0`⁴, its requested count `0x02EBCC60` and the leader
handle `0x02EBCC70`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B6ED7` |
| ² | `0x003B6F1A` |
| ³ | `0x003B6F12`, `0x003B6F24` |
| ⁴ | `0x003B6EF9` |

</details>

### The animation override

`0x00424080(id, &yaw, &speed)` indexes the character render record array at `[0x022C6F28]` by
`id * 0x740` and returns at once for an empty record (word `+0` = -1). With the record's state
`s = word +0xCC & 0xFFF`:

- latched (`+0x62C` bit `0x1`): `+0x624 *= 0.83`, then `yaw = +0x620` and `speed = +0x624`; the latch
  clears once that speed is at most 0.05, and the call returns there
 ¹, so the last step below runs only on a call that finds the latch clear;
- not latched, when `+0x284` has bit `0x8000000` and word `+0x06` is -1, with `s == 0x10`, `speed == 0`
  and the frame counter at byte `+0x457` (read signed, compared unsigned, so 0x80-0xFF qualify) at
  least `[0x01DFE0B4] * 30`: it enters the latch (`+0x624 *= 0.83`, `yaw = +0x620`, `speed =
  +0x624`, set bit `0x1` of `+0x62C`);
- not latched, same bit `0x8000000` and -1, but any of those three failing: it moves the saved group
  `+0x610`-`+0x61F` to `+0x620`-`+0x62F`, saves the incoming yaw and speed at `+0x610` and
  `+0x614`, and clears `+0x61C` bit `0x1`;
- then, when dword `+0xC4` is not -1 and its action entry resolves (`0x0020E600` on dword `+0x10`,
  `0x0051F240`, an entry whose byte `+1` is 1): states `0x35` and `0x36` multiply the accumulator
  `+0x618` by 0.9 and the speed by the result, state `0x0D` forces the speed to 0, and any other
  state stores 1.0 into the accumulator and touches nothing else (`+0x61C` keeps its value).
  - The 1.0 goes to `+0x628` instead when the latch was entered in this same call².
    The multiply never reaches `+0x628`: the latch is entered only in state `0x10`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0042411A` |
| ² | `0x004241F3` |

</details>

The record is Presentation's ([character render record
array](../Graphics/character-render-records.md));
this is Presentation writing back into Movement.

### Integration and the displacement measure

`0x002E5610(actor, body, context, &delta, mode)` returns the squared distance moved and stores the
new position:

- without a body, the candidate is `position + delta`; with a body it is `0x002E5380 → 0x002E54A0`
  (below);
- when the actor has a battle unit at `+0x30`, it publishes the move to the unit: `0x00329B00(handle,
  moved, vector)` with the body's `+0x70` vector and its `+0x90` bit `0x10` (the cell solver moved the
  body), or, without a body, `0x00329B00(handle, 0, NULL)`, the handle being `0x003589B0(actor)`
 ¹;
- `0x00329B00` acts only when `0x02089340` bit `0x10` is set, and returns at once when `0x003588B0(handle)` or the unit
  `0x00263E30` of that actor is null². With `moved` non-zero the unit's `+0x1F0` bit `0x200`
  is set and `+0x1C0` receives all 16 bytes of the vector³; with `moved` 0 it clears bit
  `0x200` and leaves `+0x1C0` as it was⁴;
- the measure is planar, `dx^2 + dz^2`, when `0x00264460` is 0 and actor byte `+0x08` bit `0x4` is clear,
  else three-dimensional;
- the context's position `+0x00`-`+0x08` becomes the candidate through three stores before the return⁵: the commit of each record the per-frame driver `0x002E5030` does not refuse⁶, and
  of each record that `0x002E5180` (from `0x002623A0` or `0x0025E400`) runs on whose `+0x18` is not 1, whose `+0xC0` context
  is of class 3 and whose body `+0x138` has a non-zero `+0xEC`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E5654`, `0x002E56A3` |
| ² | `0x00329B0A`-`0x00329B2D` |
| ³ | `0x00329B33`-`0x00329B40` |
| ⁴ | `0x00329B52` |
| ⁵ | `0x002E5729`, `0x002E5730`, `0x002E573B` |
| ⁶ | `0x002E5101` |
| ⁷ | `0x002E5197`-`0x002E5257` |

</details>

`0x002E5380` does extra work only when `mode` is non-zero, which the walking path never passes: it
sets the body's `+0xEF` from `+0xEC`, `+0xE8` and `+0xEE`, adds the body's `+0x100`-`+0x108` to the
delta, computes two `0x003A1D30` magnitudes under `+0xEC` that nothing reads, and clears the
accumulators (`0x003DA9F0`: `+0x100`-`+0x108`, `+0xE8`, `+0xEC`, `+0xED` and `+0xEE`, not `+0xEF`). It does not
rebuild the body.

`+0xEF` becomes 1 when `+0xEC` is non-zero, `+0xE8` is exactly 0.0 and `+0xEE` is non-zero, else 0¹. The two magnitudes are of the context's `+0x00`/`+0x08` less `+0x10`/`+0x18` and of the
delta's x and z². With mode 0 it only jumps on to `0x002E54A0`³. Its
one call site is `0x002E5647` in `0x002E5610`, which forwards its own `mode`; `0x002E5180` reaches it through `0x002E5610`⁴ with mode 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E53AB`-`0x002E53D8` |
| ² | `0x002E5422`-`0x002E545F` |
| ³ | `0x002E53A5`, `0x002E548C` |
| ⁴ | `0x002E5257` |

</details>

It always ends in `0x002E54A0(actor, body, context, &delta)`. On the three-dimensional path
(`0x00267260` = 0) the delta is offset by the context's `+0x40` triple when byte `+0x107` has bit `0x2`
and placed on the body by `0x003DB150(context, body, &delta)`, and the candidate is the context
position plus the delta as it was before the offset. On the flat path (`0x00267260` non-zero)
`0x003DB140` and `0x003DAE00` solve the delta and the offset is subtracted after.

`0x003DB150` adds the context position to the delta, copies the sum to the body's `+0x30`-`+0x38` and its y also to
`+0xAC`, and sets the body's word `+0x82` to `0xFFFF`¹; it runs no collision move.
`0x002E54A0` then overwrites the delta with the context position plus the delta it saved before the offset², so the body takes the offset point and the candidate does not.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DB150`-`0x003DB1A6` |
| ² | `0x002E557C`-`0x002E559E` |

</details>

`0x003DB150` tests the body pointer after the three sums are stored in the delta: with a null body it
returns there, the delta holding the context position plus the old delta and nothing else written¹. The values copied to the body are read back from the delta, its y a second
time for `+0xAC`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DB150`-`0x003DB183` |
| ² | `0x003DB185`-`0x003DB19D` |

</details>

On the flat path `0x003DB140(body, &delta)` runs the collision-mesh move `0x00380C40(placement, move)` on the body's
placement `+0x30` ([collision mesh movement](collision-mesh-movement.md)), and `0x003DAE00(body, &delta)` copies the
body's `+0x30`-`+0x38` back into the delta¹. The candidate is the solved body position,
less the offset when bit `0x2` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E54C7`, `0x002E54D2` |
| ² | `0x002E54E4`-`0x002E550A` |

</details>

### Setting the speed

`0x0026D6F0(actor, speed, mode)`, behind the class gate, stores the speed in the steering request
(`[context + 0xF0] + 0x24`) and at `+0xD0`, sets actor byte `+0x0C` bit `0x10` (changed) for mode 2 or
for mode 1 when the value differs, writes the body's `+0xC8` = `[0x01DFE0B8] * 30.0 * 3.6 * speed`
(108 × speed as shipped) when the body exists.

It then rewrites the body's mask word `+0x110` through `0x002E9BB0`/`0x002EC5B0`: bit `0x4` cleared, then for a
party-roster record (`+0x12` below 4, from 0 to 3, `0x0026D7AB`) bit `0x4` set when the speed is 0¹;
with a non-zero speed, bit `0x400` set when the actor is the party focus (`0x003590D0` → `0x003588B0`, `0x0026D7D8`),
and for that focus mode 1 also clears bit `0x8`², bit `0x4` staying clear. Any other record keeps the
word as read with bit `0x4` cleared. Without a body `0x002E9BB0` reads 0 and `0x002EC5B0` writes nothing. It has ten
call sites.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026D7BA` |
| ² | `0x0026D7E1` |

</details>

`0x0026D6A0(actor, authored)` is the scaled form: `0x0026D6F0(actor, [0x01DFE0BC] * authored, authored >
0 ? 0 : 2)`. `0x0026A330(actor, speed)` calls `0x0026D6F0(actor, speed, speed > 0)` unless
`0x002E9780(actor)` is set. `0x002E55C0(actor, context)` cancels: the request's mode byte `+0x29` = 0,
`0x0026C120(actor, 0)` when `+0x28 & 0x7F` is 2, and both speeds zeroed.

### Setting the angles

`0x0026A0D0(actor, yaw)` writes the wrapped yaw to `+0xA4` and `0x0026A060(actor, pitch)` the wrapped
pitch to `+0xA0`, both behind the class gate. The facing a character shows is a third angle,
`+0xA8`, returned by `0x00265200` for class 3 (`+0x38` for class 1) and written only by the facing
writer; it is the [facing and steering](facing-and-steering.md) page's.

`0x00263C80(actor)` reads the pitch back: `+0xA0` for class 3, the context's `+0x54` for class 1, 0
otherwise. The battle-unit refresh `0x00236300` copies the yaw¹, this pitch and the facing² into unit `+0x15C`, `+0x174` and `+0x160`, the fields the producer `0x0023A070` reads.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263CC0` |
| ² | `0x00265200` |

</details>

For a battle unit the producer is `0x0023A070(unit)`, run from the per-unit frame `0x00233F70`¹: when `0x02089340` has a bit of `0x600` and the unit's stats record is kind
0 it sets the speed to 0 (`0x0026A330(actor, 0)`); otherwise it writes the yaw from unit `+0x15C`,
the pitch from `+0x174`, the facing from `+0x160`² and, unless unit flag bit `0x40000` is set,
the speed from `+0x158`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00234019`, `0x0023407E` |
| ² | `0x0026B5A0` |

</details>

A unit without a stats record (`+0x698` null) takes the second path¹. A null unit is sent
there too², and that path's first read, unit `+0x15C` at `0x0023A0AF`, faults on it. The actor every setter gets is the unit's `+0x10`, the flag bit `0x40000` is in the
unit's dword `+0x00`³, and both speed calls are tail jumps⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A091`-`0x0023A094` |
| ² | `0x0023A085`-`0x0023A088` |
| ³ | `0x0023A0E2` |
| ⁴ | `0x0023A0AA`, `0x0023A0FC` |

</details>

The unit fields `+0x158`, `+0x15C`, `+0x160` and `+0x174` are the `+0xD8`, `+0xDC`, `+0xE0` and `+0xF4` of the
locomotion block at unit `+0x80`, into which [battle locomotion](battle-locomotion.md) writes its speed, headings and
pitch back: the solver `0x00336CE0` (`0x00336D95`-`0x00336DC5`, not for definition modes 1 and 3, `0x00336D36`, `0x00336D4D`)
and `0x0033A240`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0033A334`-`0x0033A35E` |

</details>

`0x0033A240` skips its write-back for a unit without a stats record, one that is not an enemy (byte `+0x05` not 1), one
without a definition record `+0xE68`¹, one of definition mode 0, one with `+0x1F0` bit `0x1000` or
`0x2000`, and one with bit `0x40000` set and a non-zero `+0x158`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0033A2A3` |
| ² | `0x0033A289`-`0x0033A2E5` |

</details>

The unit frame `0x00233F70` reaches the producer on two paths, each after the refresh `0x00236300`. On the first
(`0x00233FF9`, producer `0x00234019`), `0x00310DB0`¹, `0x003247F0`² and `0x00308610`³ run in
between.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00234001` |
| ² | `0x00234009` |
| ³ | `0x00234011` |

</details>

`0x00308610` calls `0x0033A240`¹ only when `0x0030DA30` answers 0², and `0x00307BE0`³ only when, besides, `0x00307DF0` answers 0, `+0x708` is not null⁴, and `0x002FFB60`,
which runs only with `+0x708` set, answers 0⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030867A` |
| ² | `0x00308650`-`0x00308657` |
| ³ | `0x00308754` |
| ⁴ | `0x00308682`-`0x00308693` |
| ⁵ | `0x003086FC`-`0x00308703` |

</details>

For an action id `+0x714` up to `0x21E` `0x00307BE0` calls `0x00304850`, whose approach calls the solver's caller
`0x00325BB0`¹, and otherwise the order table through `0x00305080`², whose
handlers `0x002FDA60` and `0x002FDC30` call `0x00325BB0` too³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307C10`-`0x00307C19`, `0x00304D5B` |
| ² | `0x00307C20` |
| ³ | `0x002FDBE9`, `0x002FDD69` |

</details>

On the second (`0x0023406A`, producer `0x0023407E`), only `0x0033A240` runs in between¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00234076` |

</details>

The refresh, after copying the actor's angles, clears bit `0x40000` and zeroes `+0x158`, and sets the bit again only
with a requested speed that is not 0.0 (`0x00265830`, the steering request's `+0x24`), for the focus or a unit with
`+0x1F0` bit `0x1000`¹ ([enemy spawning](../Enemy-Spawning/enemy-spawning.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00236363`-`0x002363AA` |

</details>

The unit frame runs the refresh on these two paths only: not on its early returns¹, the path
for a unit without drive bit `0x10`², the exit for a unit with bit `0x2`³, or the path that
zeroes the speed itself⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00233F8B`-`0x00233FBD` |
| ² | `0x00233FC6` |
| ³ | `0x0023403C` |
| ⁴ | `0x002340AC` |

</details>

So where the unit frame reaches the producer, which comes before the per-frame driver `0x002E5030` in the record's visit
([field runtime](../Characters-And-Objects/field-runtime.md), steps 3 and 4), the producer writes over a script `move`'s
speed: for a unit whose bit `0x40000` is clear when the producer runs, with the `+0x158` written since the refresh (0
unless one of the writers named here raised it), and for a kind-0 unit while `0x02089340` has a bit of `0x600`, with 0
whatever the bit¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A076`-`0x0023A0AA` |

</details>

`0x002E9780(actor)`, the test in `0x0026A330`, answers bit `0x40` of the controller's byte `+0x11` for a class-3 actor
with a controller `+0xC0`, and 0 otherwise¹. The verb `ignorebattlemovectrl` sets or clears
that bit through `0x002EBC40(actor, v)`, which does nothing for another class or no controller²
and otherwise writes `v & 1` there³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9780`-`0x002E979D` |
| ² | `0x002EBC48`, `0x002EBC54` |
| ³ | `0x002EBC56`-`0x002EBC60` |

</details>

So while that bit is set `0x0026A330` skips its call at `0x0026A35D`¹ and the producer's speed
writes do nothing, while on the producer's own second path its yaw, pitch and facing writes still run².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026A341`-`0x0026A348` |
| ² | `0x0023A0AF`-`0x0023A0DD` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

WorldActor (actor record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x03` | `u8` | classAndSequence | movement: (v & `0xE0`) == `0x60`; position read: v >> 5 in {1, 3} |
| `+0x08` | `u8` | flags08 | bit `0x2` flat-motion enable; bit `0x4` measure displacement in 3-D |
| `+0x09` | `u8` | flags09 | bit `0x1` required for flat motion |
| `+0x0C` | `u8` | flags0C | bit `0x10` set by the speed setter on a change |
| `+0x18` | `u8` | lifecycle | 1 refuses the frame driver |
| `+0x30` | `void*` | battleUnit |  |
| `+0xB8` | `void*` | movementContext |  |
| `+0xC0` | `void*` |  | controller (secondary context) |

Movement context (actor `+0xB8`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `f32[3]` | position |  |
| `+0x040` | `f32[3]` |  | offset added on the three-dimensional path when `+0x107` bit `0x2` (subtracted after the flat solve) |
| `+0x0A0` | `f32` | pitch |  |
| `+0x0A4` | `f32` | yaw |  |
| `+0x0A8` | `f32` | facing (facing page) |  |
| `+0x0B8` | `f32` |  | last squared displacement |
| `+0x0D0` | `f32` |  | requested speed |
| `+0x0F0` | `void*` |  | steering request: `+0x24` f32 speed, `+0x28` u8 kind, `+0x29` u8 mode |
| `+0x0F8` | `f32` |  | pass-through magnitude; negative = unset, repaired to the speed |
| `+0x107` | `u8` |  | bit `0x2` apply the `+0x40` offset |

Controller (actor `+0xC0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i32` |  | render record id, -1 no record |
| `+0x138` | `void*` |  | movement body |
| `+0x14F` | `u8` |  | bit `0x1` refuses movement |
| `+0x151` | `u8` |  | bit `0x1` or bit `0x2` = three-dimensional motion |

Movement body (controller `+0x138`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x070` | `f32[4]` | the cell solver's displacement |  |
| `+0x090` | `u32` | bit 0x10 the solver moved the body |  |
| `+0x0C8` | `f32` |  | published locomotion rate, 108 * speed |
| `+0x110` | `u32` |  | mask word (`0x002E9BB0` / `0x002EC5B0`) |

Character render record ([`0x022C6F28`] + id * `0x740`, 160 records):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i16` |  | id, -1 empty |
| `+0x006` | `i16` |  | -1 required for the save/latch block |
| `+0x0CC` | `u16` |  | state & `0xFFF` |
| `+0x240` | `f32[3]` |  | pitch, yaw, 0.0 from `0x002E5C10` |
| `+0x284` | `u32` |  | bit `0x8000000` gates the save/latch block; non-zero gates the publish |
| `+0x457` | `i8` |  | frame counter, against [`0x01DFE0B4`] * 30 |
| `+0x610` | `f32` | yaw | the incoming group |
| `+0x614` | `f32` | speed | the incoming group |
| `+0x618` | `f32` | accumulator | the incoming group |
| `+0x61C` | `u16` | flags | the incoming group |
| `+0x620` | `f32` | yaw | the previous group |
| `+0x624` | `f32` | speed | the previous group |
| `+0x628` | `f32` | accumulator | the previous group |
| `+0x62C` | `u16` | flags | the previous group; bit `0x1` = latch |

Battle unit:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x158` | `f32` |  | speed; while the unit's flag bit `0x40000` is set the producer leaves the speed alone |
| `+0x15C` | `f32` | yaw |  |
| `+0x160` | `f32` | facing |  |
| `+0x174` | `f32` | pitch |  |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Constant | Value | Where |
|---|---|---|
| `0x01DFE0B4` | 1 | the time-base integer, 2 at 60 fps: the latch waits 30 × it frames, 30 at 30 fps and 60 at 60 |
| `0x01DFE0B8` | 1.0 | the frame-rate scale: 30 × 3.6 × 1.0 = 108 per unit of speed |
| `0x01DFE0BC` | 1.0 | the authored-speed scale |
| `0x008F8D80`, `0x00915734` | 30.0, 3.6 | the rate multipliers |
| `0x01CEBC50`, `0x00915620`, `0x01CEBC78` | pi, -pi, 2pi | the wrap constants |
| decay, release threshold, state factor | 0.83, 0.05, 0.9 | the override's constants; the decayed speed is returned as it is, not held at 0.05 (`0x00424103`) |

</details>

## Operations

One frame of walking: the resolver calls the driver; the driver runs steering when a request is
active, computes the step from the wrapped angles and the speed after the animation override,
publishes the angles to the render record, integrates through the body when there is one, stores
the squared displacement, registers the body's cell and runs the tail. Nothing in the chain
returns a status; a refused actor simply does not move.

## State

<details>
<summary>Show the state it keeps</summary>

The movement context's position, two angles, speed and `+0xF8`; the steering request's speed and
mode; the body's `+0x70`, `+0x90`, `+0xC8` and `+0x110`; the render record's `+0x240` triple and
`+0x610`-`+0x62F`; the two gate globals `0x02B40530` and `0x02B40534`; the unit's `+0x1C0` and `+0x1F0`.

</details>

## Modding notes

- The class gate is the first thing to check when an actor will not move; it refuses the speed
  setter, the angle setters and the step alike.
- Do not model the step as `sin(heading) * speed`: that is the flat branch only. The general
  case scales both horizontal components by `cos(pitch)`.
- `+0xA0` is a pitch. Writing a yaw into it tilts the step out of the ground plane.
- The pass-through is the door for an exact displacement; the engine records its magnitude at
  `+0xF8`, a field the normal path also uses as a negative sentinel.
- Animation takes precedence: while the render record's latch is set the step uses the record's
  yaw and speed, decaying at 0.83 per call until the latch lets go at a speed of 0.05 or less, and
  state `0x0D` forces the speed to 0. If the class gate passes and an actor still will not move, look at its animation state.
- Which integration path runs is not a caller choice: the driver always passes the controller's
  body, so the plain addition runs only when that pointer is null.
- Actor byte `+0x08` bit `0x4` changes the reported displacement, not the movement.
- The flat path can be switched off mid-session by the actor-list rewrite; a creature's flat flag
  alone does not guarantee flat motion.

## Related

- [Facing and steering](facing-and-steering.md): the facing angle, the steering request and the turn.
- [Movement bodies and separation](movement-bodies-and-separation.md): the body the step is solved against.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the resolver that calls the driver.
- [Battle units](../Characters-And-Objects/battle-units.md): the unit fields the intent is read from.
- [Character render record array](../Graphics/character-render-records.md): the record the override reads.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Combat** (explained on [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x003206E0`](../Characters-And-Objects/battle-units.md) (on battle units) |

</details>

---

[← Player movement](player-movement.md) | [Facing and steering →](facing-and-steering.md)
