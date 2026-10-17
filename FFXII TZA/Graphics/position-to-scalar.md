---
title: "Position to scalar: the distance fade colour of effect elements"
kind: "system"
category: "Graphics"
addresses: "002F1F40, 002F1D90, 0039B550, 0039ABF0, 0039AF70, 00398F90, 02F97348, 02AEECB0, 02AEEA20, 02AED5F0, 003ED0E0, 003ECF70, 0026EE00, 003A3FD0, 0042FB20, 003E7DE0, 0024BFD0, 020926E8, 00442550"
---

## What the player sees

Spell and ability effects fade out with distance: a particle, a mesh piece or a glow drawn far from
the camera becomes transparent between two distances its effect file authors, and some fade by
ground distance only. The same colour also fades an effect with the character it belongs to, hides
it while status display is denied, and dims it while a time stop is running.

## How it works

### The call

`002F1F40(element, position, out)` writes one packed colour to `out`, starting from the neutral
`80808080`<sub>h</sub> (`002F1F98`), and computes its byte 3, the alpha. `element + 20h` is the element's
definition; its byte `+44`<sub>h</sub> is the element kind. Kinds `40`<sub>h</sub> and `A0`<sub>h</sub> and above skip the
distance fade and keep alpha `80`<sub>h</sub>.

The fade record is the one at `+2F0`<sub>h</sub> of the effect container being drawn, `[02F97348]`, unless
that record's first byte is `FF`<sub>h</sub>; then it is the definition's own record at `+50`<sub>h</sub>. A record
whose kind byte is 0 leaves the alpha at `80`<sub>h</sub>.

### The three distance modes

Byte `+1` of the record picks how the position becomes a distance:

| Mode | Distance |
|---|---|
| 0 | `0039B550` installs the matrix `02AEECB0` in the workbench and `0039ABF0` returns lane 3 (w) of the transformed point (`0039ADA7` `psrldq xmm1, Ch`, `0039ADAC` `movd eax, xmm1`) |
| 1 | the point goes through the matrix `02AEEA20` (`0039AF70`, `00398F90`), then `002F1D90` returns its Euclidean distance from the vector `02AED5F0` |
| 2 | as mode 1, with lane 1 zeroed in the vector before the transform (`002F1FF2`) and in the point after it (`002F200F`): a distance in the other two axes |

`002F1D90` takes the square root of the summed squared differences under the workbench lock and adds
the float at `01EF93F0`, which ships as 0.0. The vector `02AED5F0` is written by `003820C0`
(`00382460`), the camera update of [Scripted camera](scripted-camera.md). All three matrices and the
vector are past the raw end of `.data`, so the image holds no values for them.

### The four fade kinds

Byte `+0` of the record is the kind. With `d` the distance, each arm computes
`v = (d - b) / (a - b) x 255`, caps it at 256, raises it to the floor byte, and stores `v x 0.5`
truncated, so the alpha runs from half the floor to 128, full at `a` and zero at `b`:

| Kind | `a` | `b` | Floor | Notes |
|---|---|---|---|---|
| 1 | `+06`<sub>h</sub> | `+0A`<sub>h</sub> | `+03`<sub>h</sub> | |
| 2 | `+04`<sub>h</sub> | `+08`<sub>h</sub> | `+02`<sub>h</sub> | |
| 4 | both pairs | | | each pair as above; the smaller alpha wins |
| 3 | global | global | global | the mode-0 depth against the global fade settings, below |

A pair with `a == b` gives alpha `80`<sub>h</sub>.

Kind 3 reads the global settings through `003ED0E0`: near `02EBB7E4`, far `02EBB7E8` and the byte
`02EBB7EF`, whose complement `255 - byte` is the floor. `003ECF70` sets near 10 and far 100. When the
record's float `+0C`<sub>h</sub> is not 1.0 the floor becomes `255 - (255 - floor) x +0Ch`, kept in 0 to 256.
The alpha is then `(far - w) x 255 / (far - near)` with `w` from mode 0, capped and floored as above.

### Where the global settings come from

The settings at `02EBB7E0` are the winner of a request round. A request is 16 bytes: a priority, the
near and far distances, and a colour word whose top byte is the floor byte. `003ED170(request)`,
from `00377520` and `003B6C70`, keeps the request at `02EBB7D0` when its priority is higher than the
one kept. `003ED7F0(clear)`, from `0036F410` and `0036F530`, copies a kept request (priority 0 or
more) to `02EBB7E0`–`02EBB7EF` and, when `clear` is non-zero, drops the kept priority to −1.

The map's own request is built at `02EBB7C0` with priority 0 by `003ECCA0` while a map's settings are loaded
(`02EBB808` and `0209A660` set). `003ECAC0(request, target, t)` moves it toward a target: for `t`
above `0.99609375` it copies the target's near, far and colour, for `t` above `0.00390625` it
interpolates them, and otherwise does nothing. Each distance becomes `v = cur x (1 - t) + target x t`
stored as `trunc(v)`, plus 1 when `v - trunc(v) > 0.5`; each colour byte (split by `00466140`, packed by
`00466170`) becomes `trunc(cur x (1 - t) + target x t)` (`003ECAC0`-`003ECC9C`).

`003ECE60` then scales the colour's red, green and blue by `0209A380`–`0209A388` times
`0209A3D0`–`0209A3D8` where a product is below `0.99609375`, stores the colour at `022D8ED8` when
`[0209A660]` is −1, and submits the request as `003ED170` does.

### The container's modifiers

After the fade, the flag word `+368`<sub>h</sub> of the container applies, in this order (each result clamped
to 0 to 255):

| Bit | Effect on the colour |
|---|---|
| `8`<sub>h</sub> | multiplied (`0026EE00`, each byte channel `min((a x b) >> 7, 255)`, `psrlw` 7 and the clamp at `0026F287`-`0026F2D6`) by the container colour `+334`<sub>h</sub>, or `+398`<sub>h</sub> for element kind `40`<sub>h</sub> |
| `400`<sub>h</sub> | alpha x the float `02EBF278[container byte +377h]` |
| `1000`<sub>h</sub> | alpha x `+35C`<sub>h</sub> when the element's `+208`<sub>h</sub> differs from the container's `+37C`<sub>h</sub> |
| `2000`<sub>h</sub> | alpha x `+35C`<sub>h</sub> when they are equal |
| `10`<sub>h</sub> | alpha x the owner character's fade `0042FB20` (fade channel `B`<sub>h</sub> / 4096); alpha 0 when `003A3FD0` finds no owner or `0041E590` reports it not drawn |
| `20`<sub>h</sub> | alpha 0 while `003E7DE0` returns non-zero (the byte `02B59D71`) |
| `4`<sub>h</sub> | alpha x the global scale `020926E8` |

### The global dimming ramp

`0024BFD0(0)` moves `020926E8` while bits 8 and 9 of `020926E4` hold 1 or 2: it counts `020926E6`
down, adds the step `020926F0`, and at zero stores the target `020926EC` and clears the two bits;
for the value 2 it then calls `002FD060` and `003B1000`. The ramp is started by `0024FB90` and `0024FBF0`, the time-stop fades on
[Time stop and freeze](../Engine-Core/time-stop-and-freeze.md).

### The callers

`002F1F40` has 76 call sites in 75 functions, from `00442550` to `00537410`
([census](position-to-scalar-fade-node-consumers.tsv)). At 67 of them the next call is the colour
multiply `0026EE00`. The smallest, `00442550`, calls the node with the element's position `+230`<sub>h</sub>,
multiplies the result by the element's colour `+240`<sub>h</sub>, and draws the point in that colour
(`0039C550`).

## Layouts

The fade record (in the container at `+2F0`<sub>h</sub>, or in the element definition at `+50`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | kind: 0 none, 1, 2, 3 global, 4 both pairs |  |
| `01`<sub>h</sub> | `u8` | distance mode: 0 depth, 1 distance, 2 distance without lane 1 |  |
| `02`<sub>h</sub> | `u8` | floor for the `+04`<sub>h</sub>/`+08`<sub>h</sub> pair |  |
| `03`<sub>h</sub> | `u8` | floor for the `+06`<sub>h</sub>/`+0A`<sub>h</sub> pair |  |
| `04`<sub>h</sub> | `i16` | full-alpha distance, pair 2 |  |
| `06`<sub>h</sub> | `i16` | full-alpha distance, pair 1 |  |
| `08`<sub>h</sub> | `i16` | zero-alpha distance, pair 2 |  |
| `0A`<sub>h</sub> | `i16` | zero-alpha distance, pair 1 |  |
| `0C`<sub>h</sub> | `f32` | kind 3: floor scale |  |

## State

| Address | Holds |
|---|---|
| `02F97348` | the effect container being drawn; written by `0024B270`, `0024B580`, `0024C460`, `0024D540`, `0024DB80`, `0024ED80`, `0024EEE0`, `0024F4D0` and `002F3860` |
| `02AEECB0`, `02AEEA20` | the depth matrix and the distance matrix |
| `02AED5F0` | the vector distances are measured from |
| `02EBB7E4`, `02EBB7E8`, `02EBB7EF` | the global fade near, far and floor complement |
| `020926E4` to `020926F0` | the dimming ramp: flags, count, value, target, step |

## Modding notes

- An effect's own fade distances are the four `i16` words of its fade record; setting both of a
  pair equal turns that fade off.
- Mode 2 ignores the axis in lane 1, so an effect authored with it does not fade as the camera rises.
- The result is a modulate (128 is unchanged), so the alpha never exceeds the element's own.

## Related

- [Effect element runtime](effect-element-runtime.md): the containers and the element draws.
- [Character fades](character-fades.md): the owner fade bit `10`<sub>h</sub> multiplies in.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the dimming ramp.
- [PS2 CPU emulation](../Engine-Core/ps2-cpu-emulation.md): the workbench the transforms use.
