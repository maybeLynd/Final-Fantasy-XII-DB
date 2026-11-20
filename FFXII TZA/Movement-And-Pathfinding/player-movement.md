[Home](../../README.md) / [Movement and pathfinding](README.md) / Player movement

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Player movement: how the left stick moves the controlled character, the walk and run bands, the camera-relative turn, and the locks that stop it | system | Movement and pathfinding | How actors move | The one actor per tick that receives analogue movement: which handle the stick drives and how it changes, the stick vector with its dead zone and the four magnitude bands that pick walk or run speed, the keyboard walk toggle, the camera-relative rotation and the yaw smoothing, the per-tick application of speed, facing, desired heading and animation mode, the motion-flag word on the body, and the suppression word and four lock bytes that scripts, status and the party controller use to stop the character. | 0x00358C60, 0x00358CB0, 0x003594E0, 0x00358A20, 0x004742A0, 0x00264DF0, 0x0026D810, 0x002EC5B0, 0x002E9BB0, 0x0026B5A0, 0x0026A0D0, 0x002681D0, 0x00317E60, 0x00235EA0, 0x003045A0, 0x002E7E50, 0x00265680, 0x00265720, 0x00265830, 0x00267330, 0x00358B40, 0x00358BC0, 0x003593A0, 0x003590E0, 0x00359410, 0x00358EE0, 0x00358F90, 0x00359200, 0x00359250, 0x003592C0, 0x00359330, 0x0023B040, 0x0026D6D0 |

## What the player sees

Push the stick and your character walks, then runs as you push further, turning toward the
direction you push relative to the camera, quickly but not instantly. Let go and they stop. A light
push walks, a hard push runs, and a key on the keyboard toggles walking so the character never
breaks into a run. During a conversation, a scene or a status that holds the body, the stick does
nothing; while riding a chocobo it steers the chocobo at the chocobo's own speed. The other party members never respond to the stick: they follow or fight on
their own.

## How it works

### Who receives the stick

Once per simulation tick in mode 0 the world tick¹ calls `0x00358C60`: it
zeroes the result vector `0x022C7FD0` (w = 1.0), runs `0x0025A520(2, 0)`, and hands one actor handle to
`0x00358CB0`: the override `0x022C7FEC` when it is non-zero, else the controlled character `0x022C7FE0`
when manager slot 0 is active (`0x002671F0(0)`) and the handle is positive.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00314020`, `0x003140D4` |

</details>

The override exists for two debug verbs: its only setter `0x003593A0(handle)` is called by
`debug_setdebugpc` (`0x2032`, `0x0050D2F0`), which no shipped script calls, and with 0 by `debug_cleardebugpc`
(`0x2033`, `0x0050D330`, `0x0050D332`).

The field-transition
reset `0x003590E0` (from `0x002695A0` and `0x0026DB30`) clears it with the controlled handle, the pending
handle `0x022C7FE4`, the second handle `0x022C7FE8`, `0x022C7FF8`, the suppression word `0x022C8000` and
the four lock bytes, and resets the camera basis (`0x004745B0(0x022C7FA0)`) and zeroes `0x022C7FF0` with
`0x022C7FF4` in one 8-byte store¹. In retail
play the stick always goes to `0x022C7FE0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00359130` |

</details>

The reset `0x004745B0(basis)` stores 1 at the basis's dword `+0x00`, the stale mark, `0x12` at its dword `+0x04` and 0
at its dword `+0x0C`, and nothing else¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004745B0`-`0x004745BD` |

</details>

`0x003593A0` stops the controlled character¹ when it sets an override while no override is set². When a different override is already set, also on the clearing call with 0, it stops that
override's actor and runs `0x00259800(0)`³. The handle is then stored⁴; a call
with the override's own handle, or with 0 while no override is set, only stores it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026D6D0` |
| ² | `0x003593B2`-`0x003593C9` |
| ³ | `0x003593D4`-`0x003593F0` |
| ⁴ | `0x003593F5` |

</details>

The controlled character changes through a request: `0x003594B0(handle)` stores the pending handle
at `0x022C7FE4` and the kind byte `0x022C7FF8` = 1 (from the party roster's slot assignment `0x00269C70`
and `0x0050C610` and the default-actor selection `0x00326500`), and `0x003594C0`, tail-jumped from the
verb `changetosummonparty`¹, overwrites the kind with its argument while a request is
pending.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034ED30` |

</details>

`0x00358BC0` (via `0x00358BB0`), with a kind set and the pending handle different, clears the old one
(`0x00358B40`: `0x0025D650` resets the talk-request block at `0x0209A2B0`, zeroes `0x022C7FE0`¹,
then stop, motion flags 0 and
the animation mode), runs `0x00259800(0)` and the camera retarget (`0x0025A690(old, 0)` when the old
handle was 0 or the kind is 2, else `0x0025A680(old, 0)`), then stores the pending handle, clears the
kind and refreshes the new actor's animation mode.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00358B6B` |

</details>

`0x00358B40` does nothing while manager slot 0 is inactive or `0x022C7FE0` is 0¹, and skips the
stop, the flags and the mode when the handle resolves to no actor²; it is also called at `0x00262CEA`.
With a kind set and the pending handle equal to `0x022C7FE0`, `0x00358BC0` skips the release and the camera calls but
still stores the handle and clears the kind³. The mode refresh runs only when the new
handle resolves to an actor⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00358B46`-`0x00358B57` |
| ² | `0x00358B78` |
| ³ | `0x00358BE4`, `0x00358C2F` |
| ⁴ | `0x00358C49` |

</details>

A second handle `0x022C7FE8`
(`0x00359410`, from `0x0035356E`/`0x00353581`) gets the camera update below in slot 1 but never the stick.

`0x00359410(handle)` with a non-zero handle runs `0x0025A280(2, 1)` and, when the handle differs from `0x022C7FE8`,
`0x00259800(1)` and `0x0025A680(actor, 1)`¹; when `0x022C7FE8` is then 0 and the handle is
`0x022C7FE0` it runs `0x002593D0()`². With 0, the call at `0x00353581`, it runs `0x00259470()` when
`0x022C7FE8` equals `0x022C7FE0`, then `0x0025A280(2, 0)`³. Every path stores the handle at
`0x022C7FE8`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00359424`-`0x00359454` |
| ² | `0x00359464`-`0x00359470` |
| ³ | `0x00359481`-`0x00359499` |
| ⁴ | `0x00359475`, `0x0035949E` |

</details>

### From stick to vector

`0x003594E0(out)` first handles the walk toggle and zeroes `0x022C7FFC`: while `0x001E0C10()` is non-zero `0x022C800C` is cleared;
otherwise a press edge of the walk key `0x0017DFC0()` (latch `0x022C7FF9`) flips it. Then it reads the
stick from the input history (`0x0035EEB0(0, 2)` and `(0, 3)`): `x = byte2 - 128`, `z = 128 - byte3`,
`m = min(sqrt(x^2 + z^2), 128)`, `0x022C8008 = m / 128`. With `m` at or below the dead zone
`0x01EF9220` (50.0) the vector is `{0, 0, 0, 1}`; otherwise it is `(x, z, 0)` normalised and scaled
by `0x00358A20((m - 50) / 78)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003595ED`-`0x003595FB` |

</details>

The argument is the magnitude past the dead zone over the 78 units between it and 128¹, so the four
bands below start at a stick magnitude `m` of 50, 65.6, 120.2 and 124.1. `w` stays 1.0²; the function
returns the scale, or 0.0 inside the dead zone, and `0x00358CB0` does not read it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F3A2C` |
| ² | `0x00359599` |

</details>

`0x00358A20(m)` is the magnitude-to-speed map. `walkRatio` is the controlled actor's walk value
(`0x002E7E50(actor, 1)`, the character parameter `0x9000000`) divided by the run speed `0x00235EA0()`,
times `[0x01DFE0BC]`, `walkRatio = w / 0x00235EA0() × [0x01DFE0BC]` for the walk value `w`¹;
0.5 in place of the quotient without an actor².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00358A56`, `0x00358A73` |
| ² | `0x00358A5C` |

</details>

`m` is clamped to `[0, 1]`, `m < 0 ? 0 : m > 1 ? 1 : m` (`maxss`, `minss`, `0x00358A93`-`0x00358A9C`), and walked
through the band
widths at `0x01EF9228`: 0.2, 0.7, 0.05 and 1.0 (`0x01EF9234`, rewritten to 1.0 on every call), with
`t` the position inside the band; with the walk toggle `0x022C800C` set every iteration re-enters
band 1, so every magnitude yields `walkRatio`.

| Band | `m` | Result |
|---|---|---|
| 0 | 0 to 0.2 | `lerp(0.1, walkRatio, t)`, the floor from `0x01EF9224` |
| 1 | 0.2 to 0.9 | `walkRatio` flat |
| 2 | 0.9 to 0.95 | `lerp(walkRatio, 1.0, t)` |
| 3 | above 0.95 | 1.0 |

The clamp and the widths, which sum to 1.95, put every magnitude in a band. `0x00235EA0()` is the run
speed: while riding (`0x00303EC0()`
non-zero) the chocobo definition's speed (`0x003045A0`: `0x003204E0(0x00263750(3), 1)`, doubled when the
party block's `+0x5AE0` has bit `0x2`); otherwise the party leader's¹ battle unit
float `+0x17C`, or `5.0 / (30.0 * [0x01DFE0B8])` without a leader.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003272A0` |

</details>

### Camera-relative, and applied

`0x00358CB0(handle)` runs only while every active manager has its three bytes `+0x14`-`+0x16` non-zero¹ and slot 0's skip flag (`0x00267330(0)`, slot byte `+0x10` bit `0x80`; a slot whose `+0x10` bit `0x1` is clear counts as
skipping, `0x00267348`) is clear. With the actor² and its body placement (`0x00265970`, the body's `+0x30`) it stores the placement's
`+0x98` (the body's `+0xC8`) `= [0x01DFE0B8] * 30 * 3.6 * 0x00235EA0()`, builds the stick vector, and
rotates it into camera space with `0x004742A0(0x022C7FA0, 0x022C7FD0, v, placement)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00265720` |
| ² | `0x003588B0` |

</details>

A null placement, from a null actor, controller `+0xC0` or body `+0x138`¹, returns before the store
and leaves `0x022C7FD0` as `0x00358C60` zeroed it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00265970` |
| ² | `0x00358D03` |

</details>

The rotation keeps a camera basis at `0x022C7FA0`: a vector of length 0.01 or less sets the output to (0, 0, 0, 1.0)¹ and marks the basis stale (`+0`); `0x002DDCF0()` or a stick yaw (`atan2(v.x, v.z)`) more
than `0.3927` from the cached yaw `+8` also marks it stale, and a stale basis is rebuilt from the two camera rows
`0x02AEDF30 + 16 k` (`k` from `0x00D22690`, y zeroed, normalised).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0047457D`-`0x0047458E` |

</details>

The output is `(row0.x v.x - row1.x
v.z, 0, row0.z v.x - row1.z v.z)` normalised and scaled by `|v| * placement +0x98 / ([0x01DFE0B8] * 30 *
3.6)`, which is `|v|` times the run speed; `+0xC` follows the output's bearing by at most 0.25 per
call and its negative goes to `out.w`.

Then `speed = |0x022C7FD0|`, forced to 0 when the stick is not live (`0x00265680`: slot 0 active,
`0x02098E21` bit `0x1` and `0x02098E20` bit `0x80` clear, every active manager's byte `+0x17` bits `0x1` and `0x2` set,
`0x002E0540()` = 0 and `0x00265720()`) or the suppression word `0x022C8000` is non-zero; `yaw =
atan2(x, z)`. The vector, speed and yaw are computed on every call, so `0x022C7FD0` is refreshed
for a locked actor too; only an actor that accepts input (`0x00264DF0`: byte `+0x13` bit `0x1` clear and
`+0x10C` zero) gets the applications, with `lock` the OR of the four bytes `0x022C8004`-`0x022C8007`:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | unless `lock` bit `0x1`: `0x002EC5B0(actor, 0)`, the speed `0x0026D810(actor, speed)`, and `0x00317E60()` through its thunk `0x00268620` when the speed is positive; | `0x00358E16`-`0x00358E1B` |
| 2 | when the steering request's speed `0x00265830` ([battle locomotion](battle-locomotion.md#detour-and-stall-recovery)) is 0: `0x002EC5B0(actor, 8)`; otherwise:<br>• unless `lock` bit `0x2`, the facing: toward the render record's turn target when `0x002E9B60` names one (`0x003EC040(id, yaw, 2, 1)`, direction 2 and mode 1, so the entry's rate `+0x28`, `0x00358E50`-`0x00358E5D`), else from the current facing toward `yaw` by at most `pi/8` (`0x003A1AD0(facing, yaw, 0.3927)`), through `0x0026B5A0`;<br>• unless `lock` bit `0x4`, the desired heading `0x0026A0D0(actor, yaw)`, wrapped into the context's `+0xA4`; |   |
| 3 | the animation mode `0x002681D0(actor)`, which the zero-speed case of step 2 reaches with no facing or heading call. | `0x00358E3C` |

`0x0026D810(actor, speed)` (class 3 only) writes the steering request's `+0x24` and the context's
`+0xD0`, the body's animation rate `+0xC8 = [0x01DFE0B8] * 30 * 3.6 * speed`, and rebuilds the
motion-flag word: the body's `+0x110`¹ with bit `0x4` cleared, then for a party row (actor
byte `+0x12` 0 to 3, compared unsigned, `0x0026D89F`) bit `0x4` set when the speed is 0, or bit `0x400` when
the actor is the party focus
(`0x003590D0` → `0x003588B0`); `0x002EC5B0` stores the word.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9BB0` |

</details>

The rate store is skipped when the controller `+0xC0` or its body `+0x138` is null¹; any
class other than 3 returns at once².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026D859`, `0x0026D865` |
| ² | `0x0026D829` |

</details>

Bit `0x4` is stopped, bit `0x8` no scripted speed,
bit `0x400` the focus actor moving; the cell registration reads the mask ([movement
bodies](movement-bodies-and-separation.md)).

`0x00317E60()`: with `0x02089340` bit `0x10`, the focus actor's battle unit¹ whose flag bit `0x8` is
set gets flag bit `0x100000000` and its locomotion block reset (`0x0033C9B0(unit + 0x80)`); then `0x0025AAD0(1)`.
The focus actor is `0x003588B0(0x003590D0())`, and a null actor or a null unit skips the flag write². The tail is `0x0025AAD0(1, 0)`³: with handle 0 `0x003588B0`
returns 0 and the non-zero first argument skips the rest, so it changes nothing⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263E30` |
| ² | `0x00317E64`-`0x00317E8E` |
| ³ | `0x00317EA9`-`0x00317EB2` |
| ⁴ | `0x003588B4`, `0x0025AAE1` |

</details>

### The animation mode word

`0x002681D0(actor)` (the null-checked entry; its body is `0x002681E0`), for a class-3 actor with a
controller, picks a mode from the controller's byte
`+0x152` and writes it to the body's `+0x80` (u16) and the controller's `+0x153`:

| `+0x152` | Mode |
|---|---|
| 0, the focus actor | 0, or 1 with actor `+0x0C` bit `0x10` while `0x00265680()` is non-zero (`0x00268256`-`0x0026826A`); 1 when `0x002672B0()` is 0 (`0x00268270`-`0x00268277`); 5 while riding, which overrides both (`0x0037C860`, a jump to `0x00303EC0`; `0x0026827A`-`0x00268283`) |
| 0, any other actor | 1 |
| 2 | 3 |
| 3 | 5 |
| anything else | 2 |

### The camera-side update

The world tick also runs `0x00358EE0(p)`¹: with the override set and any of managers 1-3
active, `0x0025A620(0)` and `0x00358F90(override, 0, p)`, and with the override set and managers 1-3 all
inactive nothing²; otherwise `0x0025A620(0)` and `0x00358F90(0x022C7FE0, 0, p)` when slot
0 is active and the handle is set, and then, whatever that test gave, `0x00358F90(0x022C7FE8, 1, p)` with
`0x0025A620(1)` when the second handle is set³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00314278` |
| ² | `0x00358F6B` |
| ³ | `0x00358EF1`-`0x00358F42` |

</details>

`0x00358F90` for a class-3 actor with `p` = 0, a live stick, a valid render entry and actor
`+0x0C` bit `0x10` clear measures the frame's displacement between the context's `+0x00` and `+0x10`¹, keeps `max(0x002640E0(actor), d / [0x01DFE0BC])` at `0x022C7FF0` (the previous value at
`0x022C7FF4`) and calls `0x00317230(d)` for a positive `d`; it then runs `0x0025A180(actor, slot)` for any
class-3 actor, then `0x0025A520(2, 1)` and `0x0025A500(2, 1)` on every call, also when the handle resolves to
no actor or to another class².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A1920` |
| ² | `0x00358FAF`-`0x00358FBF`, `0x0035906B`-`0x0035908F` |

</details>

### The locks

Three things stop the controlled character, and every setter stops it at once (`0x0026D6D0`, which
is `0x0026D6F0(actor, 0, 2)`) when the result holds:

- the suppression word `0x022C8000`, a bit set edited by `0x00359200(on, bit)`, which sets or clears bit value
  `1 << bit`¹: bit `0x1` by the verb
  `setuclockstatus` (`0x3C0`, `0x00347E00`), bit `0x2` by the lock evaluator below, bit `0x4` by the group
  completion `0x00307140`, and bit `0x8` by the manager bind and unload (below); any set
  bit forces the speed to 0;
  - bit `0x8` is set by the manager bind `0x0026C8C0`² and cleared by the unload `0x002628B0`
  for manager 3³;
- the four lock bytes `0x022C8004`-`0x022C8007`: `0x00359250(bit, on)` edits byte 0 (verb
  `setucpcmovelockstatus`, `0x3E1`, `0x0034E580`), `0x003592C0(bit, on)` byte 1 (the evaluator and the
  verb `debug_TkRequireUCPCMoveLockStatus`, `0x2084`, `0x0050D2B0`), `0x00359330(index, bit, on)` any
  byte (`0x00307140`: byte 2 bit `0x2`); each takes a bit index and sets or clears bit value `1 << bit`
 ⁴;
  - the OR's bit `0x1` blocks the speed, bit `0x2` the facing, bit `0x4` the
  desired heading, and the setters stop the character when the OR has bit `0x1`;
- the actor's own gate `0x00264DF0`, which scripts and scenes hold through `+0x13` bit `0x1` and `+0x10C`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00359215`, `0x0035921B` |
| ² | `0x0026CCBA` |
| ³ | `0x002628F0`-`0x002628F9` |
| ⁴ | `0x0035925F`, `0x003592CF`, `0x00359349` |

</details>

The evaluator `0x0023B040`, from the field frame¹ and three battle sites², starts a mask as all ones when `0x02089340` has bit `0x40`, else 0,
and derives it from the leader's unit only while not riding³, not in a town
(the town flag `0x00377C20`, through its thunk `0x00313F60`) and with a leader unit⁴; riding,
the town flag or no leader leave the
start value, which then clears the evaluator's locks when it is 0 and raises all of them when it is all ones
(`0x0023B06C`, `0x0023B079` and `0x0023B08F` jump to the tail).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00234533`, `0x002346E5` |
| ² | `0x0030108F`, `0x003010C0`, `0x00301123` |
| ³ | `0x00303EC0` |
| ⁴ | `0x003272A0` |

</details>

Inside the derivation every bit is set by: no `+0x698` record, or its status words `+0x3C | +0x64` holding
`0x80000003` without `0x00377C20`; `0x02089340` bits `0x200` or `0x400`; unit qword bit `0x400000000000`; `0x00322600` on
`0x002E8100(unit + 8)` or the unit's `+0x5C`; byte `+0x6B7`; or, in mode `0x003135C0`, the unit of `0x003137F0()` lacking a
record or holding those status bits; a missing unit there adds nothing¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023B194` |

</details>

A leader unit with no `+0x698` record sets every bit¹ but never reaches the tail: the status-word read at
`0x0023B152`-`0x0023B15E` reloads `+0x698` with no null test and reads address `0x64`, so that path faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023B0C7` |

</details>

Bit `0x2` is set by `0x00322920` on the same
two values, unit bit `0x1000000`, or an action `+0x714` below `0x21F` with `+0x6B4` above 8. The status
words set bits `0x1` and `0x4` under `0x8800403B` and bit `0x2` under `0x8800003B`.

`0x00322600(value)` answers 1 for `0x2006`, `0x2037`, `0x2039`, `0x203A`, `0x203B` and `0x203C` and 0 for every other
dword: it tests bit `value - 0x2006` of the mask `0x7A000000000001` when that difference, unsigned, is `0x36` or less¹. `0x00322920(value)` answers 0 for `0x2001`, `0x2009` and `0x2031` and 1 for every other dword,
from bit `value - 0x2001` of the mask `0x1000000000101` for a difference of `0x30` or less².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00322600`-`0x00322623` |
| ² | `0x00322920`-`0x00322943` |

</details>

The tail writes lock byte 1 bit `0x2` (the facing lock) from mask bit `0x4`, suppression bit `0x2` (the speed)
from mask bit `0x1`, and the byte `0x0209A2C5` (`0x0026BD40`, read by `0x00265460` and `0x0026DFB0`, also
written by `0x0026C8C0` and `0x002628B0`) from the inverse of mask bit `0x2`, which is not a stick lock.

## Layouts

<details>
<summary>Show the memory layouts</summary>

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022C7FA0` | `...` |  | camera basis (fields below) |
| `0x022C7FD0` | `f32[4]` |  | the camera-relative movement vector this tick |
| `0x022C7FE0` | `u32` |  | controlled character handle (also read by `0x00338490`) |
| `0x022C7FE4` | `u32` | pending handle |  |
| `0x022C7FE8` | `u32` | second handle |  |
| `0x022C7FEC` | `u32` |  | override handle (debug only) |
| `0x022C7FF0` | `f32` | displacement, this tick |  |
| `0x022C7FF4` | `f32` | displacement, last tick |  |
| `0x022C7FF8` | `u8` |  | handle change kind (1 request, 2 summon party) |
| `0x022C7FF9` | `u8` | walk-key latch |  |
| `0x022C7FFC` | `u16` | stored by 0x003591F0 (its argument) and 0x00359552 |  |
| `0x022C8000` | `u32` |  | suppression bit set |
| `0x022C8004` | `u8[4]` |  | lock bytes `0x022C8004`..0x022C8007 |
| `0x022C8008` | `f32` |  | stick magnitude / 128 |
| `0x022C800C` | `u32` | walk toggle |  |
| `0x01EF9220` | `f32` |  | dead zone 50.0 |
| `0x01EF9224` | `f32` | floor 0.1 |  |
| `0x01EF9228` | `f32[4]` |  | band widths 0.2, 0.7, 0.05, 1.0 |

Camera basis at `0x022C7FA0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | stale |  |
| `+0x04` | `u32` |  | `0x12` at the reset `0x004745B0` (`0x004745B6`) |
| `+0x08` | `f32` |  | cached stick yaw |
| `+0x0C` | `f32` |  | smoothed output bearing |
| `+0x10` | `f32[4]` |  | row 0 |
| `+0x20` | `f32[4]` |  | row 1 |

```
body placement (0x00265970): +0x98 f32 [0x01DFE0B8] * 30 * 3.6 * run speed (the body's +0xC8)
movement context: +0xA4 f32 desired heading   +0xD0 f32 speed
body: +0x80 u16 animation mode   +0xC8 f32 animation rate   +0x110 u32 motion flags
```

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| dead zone, floor, band widths | 50.0; 0.1; 0.2, 0.7, 0.05, 1.0 (read from the image at `0x01EF9220`-`0x01EF9234`) |
| frame scales | `0x01DFE0B8` = 1.0, `0x01DFE0BC` = 1.0, `0x01DFE0B4` = 1 in the image |
| turn per tick | `pi/8` (`0.3927`), and 0.25 for the basis bearing |
| `debug_setdebugpc`, `debug_TkRequireUCPCMoveLockStatus` | no calls in the 1,114 `us` scripts, zone and event |
| `setuclockstatus` | 3 calls in 1 zone script |
| `setucpcmovelockstatus` | 6 calls in 1 zone script |

</details>

## Operations

Per simulation tick: the stick is read once, scaled by the band, rotated by the camera, and
applied to one actor as speed, facing, desired heading and animation mode; the camera-side update
records the frame's displacement. The movement step page's driver then turns the speed and heading
into the actor's displacement.

## State

<details>
<summary>Show the state it keeps</summary>

The handles and the pending request; the camera basis and its cached yaw; the suppression word, the
lock bytes, the walk toggle and its latch; the context's speed and desired heading.

</details>

## Modding notes

- The engine applies stick movement to exactly one handle per tick; the four calls it makes
 ¹ are the native way to move any class-3 body the
  way the stick moves the leader, and `0x002681D0` gives a non-focus body mode 1.
- Scripts and scenes stop the stick through the actor's `+0x13` bit `0x1` and `+0x10C`; a body driven by
  the four calls directly bypasses that gate and must honour it itself.
- The bands are read from `.data` on every call; a run-time edit of `0x01EF9228` changes the walk
  threshold, but `0x01EF9234` is rewritten to 1.0 each time.
- The walk toggle only caps the speed at the walk ratio; it is not a run toggle.
- `0x01DFE0B8` scales both the speed context and the animation rate; a frame-rate change moves both.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026D810`, `0x0026B5A0`, `0x0026A0D0`, `0x002681D0` |

</details>

## Related

- [Movement step](heading-speed-to-position-delta.md): what the driver does with the speed and
  heading.
- [Facing and steering](facing-and-steering.md): the facing setter and the steering request.
- [Movement bodies and separation](movement-bodies-and-separation.md): the motion-flag word's
  reader.

---

[Movement step →](heading-speed-to-position-delta.md)
