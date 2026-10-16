---
title: "Player movement: how the left stick moves the controlled character, the walk and run bands, the camera-relative turn, and the locks that stop it"
kind: "system"
category: "Movement and pathfinding"
summary: "The one actor per tick that receives analogue movement: which handle the stick drives and how it changes, the stick vector with its dead zone and the four magnitude bands that pick walk or run speed, the keyboard walk toggle, the camera-relative rotation and the yaw smoothing, the per-tick application of speed, facing, desired heading and animation mode, the motion-flag word on the body, and the suppression word and four lock bytes that scripts, status and the party controller use to stop the character."
addresses: "00358C60, 00358CB0, 003594E0, 00358A20, 004742A0, 00264DF0, 0026D810, 002EC5B0, 002E9BB0, 0026B5A0, 0026A0D0, 002681D0, 00317E60, 00235EA0, 003045A0, 002E7E50, 00265680, 00265720, 00265830, 00267330, 00358B40, 00358BC0, 003593A0, 003590E0, 00359410, 00358EE0, 00358F90, 00359200, 00359250, 003592C0, 00359330, 0023B040, 0026D6D0"
---

## What the player sees

Push the stick and your character walks, then runs as you push further, turning toward the
direction you push relative to the camera, quickly but not instantly. Let go and they stop. A light
push walks, a hard push runs, and a key on the keyboard toggles walking so the character never
breaks into a run. During a conversation, a scene, a status that holds the body or while riding, the
stick does nothing. The other party members never respond to the stick: they follow or fight on
their own.

## How it works

### Who receives the stick

Once per simulation tick in mode 0 the world tick (`00314020`, `003140D4`) calls `00358C60`: it
zeroes the result vector `022C7FD0` (w = 1.0), runs `0025A520(2)`, and hands one actor handle to
`00358CB0`: the override `022C7FEC` when it is non-zero, else the controlled character `022C7FE0`
when manager slot 0 is active (`002671F0(0)`) and the handle is positive.

The override exists for one debug verb: its only setter `003593A0(handle)` is called by
`debug_setdebugpc` (`0x2032`, `0050D2F0`), which no shipped script calls, and the field-transition
reset `003590E0` (from `002695A0` and `0026DB30`) clears it with the controlled handle, the pending
handle `022C7FE4`, the second handle `022C7FE8`, `022C7FF8`, the suppression word `022C8000` and
the four lock bytes, and resets the camera basis (`004745B0(022C7FA0)`) and `022C7FF0`. In retail
play the stick always goes to `022C7FE0`.

The controlled character changes through a request: `003594B0(handle)` stores the pending handle
at `022C7FE4` and the kind byte `022C7FF8` = 1 (from the party roster's slot assignment `00269C70`
and `0050C610` and the default-actor selection `00326500`), and `003594C0`, tail-jumped from the
verb `changetosummonparty` (`0034ED30`), overwrites the kind with its argument while a request is
pending.

`00358BC0` (via `00358BB0`), with a kind set and the pending handle different, clears the old one
(`00358B40`: `0025D650` resets the talk-request block at `0209A2B0`, then stop, motion flags 0 and
the animation mode), runs `00259800(0)` and the camera retarget (`0025A690(old, 0)` when the old
handle was 0 or the kind is 2, else `0025A680(old, 0)`), then stores the pending handle, clears the
kind and refreshes the new actor's animation mode. A second handle `022C7FE8`
(`00359410`, from `0035356E`/`00353581`) gets the camera update below in slot 1 but never the stick.

### From stick to vector

`003594E0(out)` first handles the walk toggle and zeroes `022C7FFC`: while `001E0C10()` is non-zero `022C800C` is cleared;
otherwise a press edge of the walk key `0017DFC0()` (latch `022C7FF9`) flips it. Then it reads the
stick from the input history (`0035EEB0(0, 2)` and `(0, 3)`): `x = byte2 - 128`, `z = 128 - byte3`,
`m = min(sqrt(x^2 + z^2), 128)`, `022C8008 = m / 128`. With `m` at or below the dead zone
`01EF9220` (50.0) the vector is `{0, 0, 0, 1}`; otherwise it is `(x, z, 0)` normalised and scaled
by `00358A20(m / 128)`.

`00358A20(m)` is the magnitude-to-speed map. `walkRatio` is the controlled actor's walk value
(`002E7E50(actor, 1)`, the character parameter `0x9000000`) divided by the run speed `00235EA0()`,
times `[01DFE0BC]`; 0.5 without an actor. `m` is clamped to `[0, 1]` and walked through the band
widths at `01EF9228`: 0.2, 0.7, 0.05 and 1.0 (`01EF9234`, rewritten to 1.0 on every call), with
`t` the position inside the band; with the walk toggle `022C800C` set every iteration re-enters
band 1, so every magnitude yields `walkRatio`.

| Band | `m` | Result |
|---|---|---|
| 0 | 0 to 0.2 | `lerp(0.1, walkRatio, t)`, the floor from `01EF9224` |
| 1 | 0.2 to 0.9 | `walkRatio` flat |
| 2 | 0.9 to 0.95 | `lerp(walkRatio, 1.0, t)` |
| 3 | above 0.95 | 1.0 |

The clamp and the widths, which sum to 1.95, put every magnitude in a band. `00235EA0()` is the run
speed: while riding (`00303EC0()`
non-zero) the chocobo definition's speed (`003045A0`: `003204E0(00263750(3), 1)`, doubled when the
battle-state block's `+0x5AE0` has bit 1); otherwise the party leader's (`003272A0`) battle unit
float `+0x17C`, or `5.0 / (30.0 * [01DFE0B8])` without a leader.

### Camera-relative, and applied

`00358CB0(handle)` runs only while every active manager has its three bytes `+4`-`+6` non-zero
(`00265720`) and slot 0's skip flag (`00267330(0)`, byte `+0` bit 7) is clear. With the actor
(`003588B0`) and its body placement (`00265970`, the body's `+0x30`) it stores the placement's
`+0x98` (the body's `+0xC8`) `= [01DFE0B8] * 30 * 3.6 * 00235EA0()`, builds the stick vector, and
rotates it into camera space with `004742A0(022C7FA0, 022C7FD0, v, placement)`.

The rotation keeps a camera basis at `022C7FA0`: a vector shorter than 0.01 zeroes the output and
marks the basis stale (`+0`); `002DDCF0()` or a stick yaw (`atan2(v.x, v.z)`) more than `0.3927`
from the cached yaw `+8` also marks it stale, and a stale basis is rebuilt from the two camera rows
`02AEDF30 + 16 k` (`k` from `00D22690`, y zeroed, normalised).

The output is `(row0.x v.x - row1.x
v.z, 0, row0.z v.x - row1.z v.z)` normalised and scaled by `|v| * placement +0x98 / ([01DFE0B8] * 30 *
3.6)`, which is `|v|` times the run speed; `+0xC` follows the output's bearing by at most 0.25 per
call and its negative goes to `out.w`.

Then `speed = |022C7FD0|`, forced to 0 when the stick is not live (`00265680`: slot 0 active,
`02098E21` bit 0 and `02098E20` bit 7 clear, every active manager's byte `+7` bits 0-1 set,
`002E0540()` = 0 and `00265720()`) or the suppression word `022C8000` is non-zero; `yaw =
atan2(x, z)`. The vector, speed and yaw are computed on every call, so `022C7FD0` is refreshed
for a locked actor too; only an actor that accepts input (`00264DF0`: byte `+0x13` bit 0 clear and
`+0x10C` zero) gets the applications, with `lock` the OR of the four bytes `022C8004`-`022C8007`:

1. unless `lock` bit 0: `002EC5B0(actor, 0)`, the speed `0026D810(actor, speed)`, and `00317E60()`
   when the speed is positive;
2. when the steering request's speed `00265830` is 0: `002EC5B0(actor, 8)`; otherwise, unless `lock`
   bit 1, the facing: toward the render record's turn target when `002E9B60` names one
   (`003EC040(id, yaw, 2)`), else from the current facing toward `yaw` by at most `pi/8`
   (`003A1AD0(facing, yaw, 0.3927)`), through `0026B5A0`; and, unless `lock` bit 2, the desired
   heading `0026A0D0(actor, yaw)`, wrapped into the context's `+0xA4`;
3. the animation mode `002681D0(actor)`.

`0026D810(actor, speed)` (class 3 only) writes the steering request's `+0x24` and the context's
`+0xD0`, the body's animation rate `+0xC8 = [01DFE0B8] * 30 * 3.6 * speed`, and rebuilds the
motion-flag word: the body's `+0x110` (`002E9BB0`) with bit 2 cleared, then for a party row (actor
`+0x12` below 4) bit 2 set when the speed is 0, or bit 10 when the actor is the party focus
(`003590D0` → `003588B0`); `002EC5B0` stores the word.

Bit 2 is stopped, bit 3 no scripted speed,
bit 10 the focus actor moving; the cell registration reads the mask ([movement
bodies](movement-bodies-and-separation.md)).

`00317E60()`: with `02089340` bit 4, the focus actor's battle unit (`00263E30`) whose flag bit 3 is
set gets flag bit 32 and its locomotion block reset (`0033C9B0(unit + 0x80)`); then `0025AAD0(1)`.

### The animation mode word

`002681D0(actor)` (the null-checked entry; its body is `002681E0`), for a class-3 actor with a
controller, picks a mode from the controller's byte
`+0x152` and writes it to the body's `+0x80` (u16) and the controller's `+0x153`:

| `+0x152` | Mode |
|---|---|
| 0, the focus actor | 0, or 1 with actor `+0x0C` bit 4 and a live stick; 1 when `002672B0()` is 0; 5 while riding (`00303EC0`) |
| 0, any other actor | 1 |
| 2 | 3 |
| 3 | 5 |
| anything else | 2 |

### The camera-side update

The world tick also runs `00358EE0(p)` (`00314278`): with the override set and any of managers 1-3
active, `0025A620(0)` and `00358F90(override, 0, p)`; otherwise `00358F90(022C7FE0, 0, p)` when slot
0 is active and the handle is set, and `00358F90(022C7FE8, 1, p)` with `0025A620(1)` for the second
handle.

`00358F90` for a class-3 actor with `p` = 0, a live stick, a valid render entry and actor
`+0x0C` bit 4 clear measures the frame's displacement between the context's `+0x00` and `+0x10`
(`003A1920`), keeps `max(002640E0(actor), d / [01DFE0BC])` at `022C7FF0` (the previous value at
`022C7FF4`) and calls `00317230(d)` for a positive `d`; it then runs `0025A180(actor, slot)`,
`0025A520(2)` and `0025A500(2)`.

### The locks

Three things stop the controlled character, and every setter stops it at once (`0026D6D0`, which
is `0026D6F0(actor, 0, 2)`) when the result holds:

- the suppression word `022C8000`, a bit set edited by `00359200(on, bit)`: bit 0 by the verb
  `setuclockstatus` (`0x3C0`, `00347E00`), bit 1 by the lock evaluator below, bit 2 by the group
  completion `00307140`, and bits from the manager unload `002628B0` and bind `0026C8C0`; any set
  bit forces the speed to 0;
- the four lock bytes `022C8004`-`022C8007`: `00359250(bit, on)` edits byte 0 (verb
  `setucpcmovelockstatus`, `0x3E1`, `0034E580`), `003592C0(bit, on)` byte 1 (the evaluator and the
  verb `debug_TkRequireUCPCMoveLockStatus`, `0x2084`, `0050D2B0`), `00359330(index, bit, on)` any
  byte (`00307140`: byte 2 bit 1); the OR's bit 0 blocks the speed, bit 1 the facing, bit 2 the
  desired heading, and the setters stop the character when the OR has bit 0;
- the actor's own gate `00264DF0`, which scripts and scenes hold through `+0x13` bit 0 and `+0x10C`.

The evaluator `0023B040`, from the field frame (`00234533`, `002346E5`) and three battle sites
(`0030108F`, `003010C0`, `00301123`), starts a mask as all ones when `02089340` has bit 6, else 0,
and derives it from the leader's unit only while not riding (`00303EC0`), not in a cutscene
(`00377C20`) and with a leader unit (`003272A0`); riding, the cutscene bit or no leader leave the
start value, which then clears the evaluator's locks.

Inside the derivation every bit is set by: no `+0x698` record, or its status words `+0x3C | +0x64`
holding `0x80000003` without `00377C20`; `02089340` bits 9 or 10; unit qword bit 46; `00322600`
on `002E8100(unit + 8)` or the unit's `+0x5C`; byte `+0x6B7`; or, in mode `003135C0`, the unit of
`003137F0()` lacking a record or holding those status bits. Bit 1 is set by `00322920` on the same
two values, unit bit 24, or an action `+0x714` below `0x21F` with `+0x6B4` above 8. The status
words set bits 0 and 2 under `0x8800403B` and bit 1 under `0x8800003B`.

The tail writes lock byte 1 bit 1 (the facing lock) from mask bit 2, suppression bit 1 (the speed)
from mask bit 0, and the byte `0209A2C5` (`0026BD40`, read by `00265460` and `0026DFB0`, also
written by `0026C8C0` and `002628B0`) from the inverse of mask bit 1, which is not a stick lock.

## Layouts

```
globals
022C7FA0  camera basis: +0 u32 stale, +8 f32 cached stick yaw, +0xC f32 smoothed output bearing,
          +0x10 f32[4] row 0, +0x20 f32[4] row 1
022C7FD0  f32[4]  the camera-relative movement vector this tick
022C7FE0  u32  controlled character handle (also read by 00338490)   022C7FE4 u32 pending handle   022C7FE8 u32 second handle
022C7FEC  u32  override handle (debug only)  022C7FF0/022C7FF4 f32 displacement, this and last
022C7FF8  u8   handle change kind (1 request, 2 summon party)   022C7FF9 u8 walk-key latch   022C7FFC u32 zeroed by the stick read
022C8000  u32  suppression bit set           022C8004..022C8007 u8[4] lock bytes
022C8008  f32  stick magnitude / 128         022C800C u32 walk toggle
01EF9220  f32  dead zone 50.0                01EF9224 f32 floor 0.1
01EF9228  f32[4] band widths 0.2, 0.7, 0.05, 1.0

body placement (00265970): +0x98 f32 [01DFE0B8] * 30 * 3.6 * run speed (the body's +0xC8)
movement context: +0xA4 f32 desired heading   +0xD0 f32 speed
body: +0x80 u16 animation mode   +0xC8 f32 animation rate   +0x110 u32 motion flags
```

## Shipped data

| Fact | Value |
|---|---|
| dead zone, floor, band widths | 50.0; 0.1; 0.2, 0.7, 0.05, 1.0 (read from the image at `01EF9220`-`01EF9234`) |
| frame scales | `01DFE0B8` = 1.0, `01DFE0BC` = 1.0, `01DFE0B4` = 1 in the image |
| turn per tick | `pi/8` (`0.3927`), and 0.25 for the basis bearing |
| `debug_setdebugpc`, `debug_TkRequireUCPCMoveLockStatus` | no calls in the 1,114 zone scripts |
| `setuclockstatus` | 3 calls in 1 zone script |
| `setucpcmovelockstatus` | 6 calls in 1 zone script |

## Operations

Per simulation tick: the stick is read once, scaled by the band, rotated by the camera, and
applied to one actor as speed, facing, desired heading and animation mode; the camera-side update
records the frame's displacement. The movement step page's driver then turns the speed and heading
into the actor's displacement.

## State

The handles and the pending request; the camera basis and its cached yaw; the suppression word, the
lock bytes, the walk toggle and its latch; the context's speed and desired heading.

## Modding notes

- The engine applies stick movement to exactly one handle per tick; the four calls it makes
  (`0026D810`, `0026B5A0`, `0026A0D0`, `002681D0`) are the native way to move any class-3 body the
  way the stick moves the leader, and `002681D0` gives a non-focus body mode 1.
- Scripts and scenes stop the stick through the actor's `+0x13` bit 0 and `+0x10C`; a body driven by
  the four calls directly bypasses that gate and must honour it itself.
- The bands are read from `.data` on every call; a run-time edit of `01EF9228` changes the walk
  threshold, but `01EF9234` is rewritten to 1.0 each time.
- The walk toggle only caps the speed at the walk ratio; it is not a run toggle.
- `01DFE0B8` scales both the speed context and the animation rate; a frame-rate change moves both.

## Related

- [Movement step](heading-speed-to-position-delta.md): what the driver does with the speed and
  heading.
- [Facing and steering](facing-and-steering.md): the facing setter and the steering request.
- [Movement bodies and separation](movement-bodies-and-separation.md): the motion-flag word's
  reader.
