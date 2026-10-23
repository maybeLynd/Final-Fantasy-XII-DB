---
title: "Position to scalar: the distance fade colour of effect elements"
kind: "system"
category: "Graphics"
addresses: "0x002F1F40, 0x002F1D90, 0x0039B550, 0x0039ABF0, 0x0039AF70, 0x00398F90, 0x02F97348, 0x02AEECB0, 0x02AEEA20, 0x02AED5F0, 0x003ED0E0, 0x003ECF70, 0x0026EE00, 0x003A3FD0, 0x0042FB20, 0x003E7DE0, 0x0024BFD0, 0x020926E8, 0x00442550"
---

## What the player sees

Spell and ability effects fade out with distance: a particle, a mesh piece or a glow drawn far from
the camera becomes transparent between two distances its effect file authors, and some fade by
ground distance only. The same colour also fades an effect with the character it belongs to, hides
it while status display is denied, and dims it while a time stop is running.

## How it works

### The call

`0x002F1F40(element, position, out)` writes one packed colour to `out`, starting from the neutral
`0x80808080` (`0x002F1F98`), and computes its byte 3, the alpha. `element + 0x20` is the element's
definition; its byte `+0x44` is the element kind. Kinds `0x40` and `0xA0` and above skip the
distance fade and keep alpha `0x80`.

The fade record is the one at `+0x2F0` of the effect container being drawn, `[0x02F97348]`, unless
that record's first byte is `0xFF`; then it is the definition's own record at `+0x50`. A record
whose kind byte is 0 leaves the alpha at `0x80`.

### The three distance modes

Byte `+1` of the record picks how the position becomes a distance:

| Mode | Distance |
|---|---|
| 0 | `0x0039B550` installs the matrix `0x02AEECB0` in the workbench and `0x0039ABF0` returns lane 3 (w) of the transformed point (`0x0039ADA7` `psrldq xmm1, 0xC`, `0x0039ADAC` `movd eax, xmm1`) |
| 1 | the point goes through the matrix `0x02AEEA20` (`0x0039AF70`, `0x00398F90`), then `0x002F1D90` returns its Euclidean distance from the vector `0x02AED5F0` |
| 2 | as mode 1, with lane 1 zeroed in the vector before the transform (`0x002F1FF2`) and in the point after it (`0x002F200F`): a distance in the other two axes |

`0x002F1D90` takes the square root of the summed squared differences under the workbench lock and adds
the float at `0x01EF93F0`, which ships as 0.0. The vector `0x02AED5F0` is written by `0x003820C0`
(`0x00382460`), the camera update of [Scripted camera](scripted-camera.md). All three matrices and the
vector are past the raw end of `.data`, so the image holds no values for them.

### The four fade kinds

Byte `+0` of the record is the kind. With `d` the distance, each arm computes
`v = (d - b) / (a - b) x 255`, caps it at 256, raises it to the floor byte, and stores `v x 0.5`
truncated, so the alpha runs from half the floor to 128, full at `a` and zero at `b`:

| Kind | `a` | `b` | Floor | Notes |
|---|---|---|---|---|
| 1 | `+0x06` | `+0x0A` | `+0x03` | |
| 2 | `+0x04` | `+0x08` | `+0x02` | |
| 4 | both pairs | | | each pair as above; the smaller alpha wins |
| 3 | global | global | global | the mode-0 depth against the global fade settings, below |

A pair with `a == b` gives alpha `0x80`.

Kind 3 reads the global settings through `0x003ED0E0`: near `0x02EBB7E4`, far `0x02EBB7E8` and the byte
`0x02EBB7EF`, whose complement `255 - byte` is the floor. `0x003ECF70` sets near 10 and far 100. When the
record's float `+0x0C` is not 1.0 the floor becomes `255 - (255 - floor) x +0x0C`, kept in 0 to 256.
The alpha is then `(far - w) x 255 / (far - near)` with `w` from mode 0, capped and floored as above.

### Where the global settings come from

The settings at `0x02EBB7E0` are the winner of a request round. A request is 16 bytes: a priority, the
near and far distances, and a colour word whose top byte is the floor byte. `0x003ED170(request)`,
from `0x00377520` and `0x003B6C70`, keeps the request at `0x02EBB7D0` when its priority is higher than the
one kept. `0x003ED7F0(clear)`, from `0x0036F410` and `0x0036F530`, copies a kept request (priority 0 or
more) to `0x02EBB7E0`–`0x02EBB7EF` and, when `clear` is non-zero, drops the kept priority to −1.

The map's own request is built at `0x02EBB7C0` with priority 0 by `0x003ECCA0` while a map's settings are loaded
(`0x02EBB808` and `0x0209A660` set). `0x003ECAC0(request, target, t)` moves it toward a target: for `t`
above `0.99609375` it copies the target's near, far and colour, for `t` above `0.0x00390625` it
interpolates them, and otherwise does nothing. Each distance becomes `v = cur x (1 - t) + target x t`
stored as `trunc(v)`, plus 1 when `v - trunc(v) > 0.5`; each colour byte (split by `0x00466140`, packed by
`0x00466170`) becomes `trunc(cur x (1 - t) + target x t)` (`0x003ECAC0`-`0x003ECC9C`).

`0x003ECE60` then scales the colour's red, green and blue by `0x0209A380`–`0x0209A388` times
`0x0209A3D0`–`0x0209A3D8` where a product is below `0.99609375`, stores the colour at `0x022D8ED8` when
`[0x0209A660]` is −1, and submits the request as `0x003ED170` does.

### The container's modifiers

After the fade, the flag word `+0x368` of the container applies, in this order (each result clamped
to 0 to 255):

| Bit | Effect on the colour |
|---|---|
| `0x8` | multiplied (`0x0026EE00`, each byte channel `min((a x b) >> 7, 255)`, `psrlw` 7 and the clamp at `0x0026F287`-`0x0026F2D6`) by the container colour `+0x334`, or `+0x398` for element kind `0x40` |
| `0x400` | alpha x the float `0x02EBF278[container byte +0x377]` |
| `0x1000` | alpha x `+0x35C` when the element's `+0x208` differs from the container's `+0x37C` |
| `0x2000` | alpha x `+0x35C` when they are equal |
| `0x10` | alpha x the owner character's fade `0x0042FB20` (fade channel `0xB` / 4096); alpha 0 when `0x003A3FD0` finds no owner or `0x0041E590` reports it not drawn |
| `0x20` | alpha 0 while `0x003E7DE0` returns non-zero (the byte `0x02B59D71`) |
| `0x4` | alpha x the global scale `0x020926E8` |

### The global dimming ramp

`0x0024BFD0(0)` moves `0x020926E8` while bits 8 and 9 of `0x020926E4` hold 1 or 2: it counts `0x020926E6`
down, adds the step `0x020926F0`, and at zero stores the target `0x020926EC` and clears the two bits;
for the value 2 it then calls `0x002FD060` and `0x003B1000`. The ramp is started by `0x0024FB90` and `0x0024FBF0`, the time-stop fades on
[Time stop and freeze](../Engine-Core/time-stop-and-freeze.md).

### The callers

`0x002F1F40` has 76 call sites in 75 functions, from `0x00442550` to `0x00537410`
([census](position-to-scalar-fade-node-consumers.tsv)). At 67 of them the next call is the colour
multiply `0x0026EE00`. The smallest, `0x00442550`, calls the node with the element's position `+0x230`,
multiplies the result by the element's colour `+0x240`, and draws the point in that colour
(`0x0039C550`).

## Layouts

The fade record (in the container at `+0x2F0`, or in the element definition at `+0x50`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | kind: 0 none, 1, 2, 3 global, 4 both pairs |  |
| `+0x01` | `u8` | distance mode: 0 depth, 1 distance, 2 distance without lane 1 |  |
| `+0x02` | `u8` | floor for the +0x04/+0x08 pair |  |
| `+0x03` | `u8` | floor for the +0x06/+0x0A pair |  |
| `+0x04` | `i16` | full-alpha distance, pair 2 |  |
| `+0x06` | `i16` | full-alpha distance, pair 1 |  |
| `+0x08` | `i16` | zero-alpha distance, pair 2 |  |
| `+0x0A` | `i16` | zero-alpha distance, pair 1 |  |
| `+0x0C` | `f32` | kind 3: floor scale |  |

## State

| Address | Holds |
|---|---|
| `0x02F97348` | the effect container being drawn; written by `0x0024B270`, `0x0024B580`, `0x0024C460`, `0x0024D540`, `0x0024DB80`, `0x0024ED80`, `0x0024EEE0`, `0x0024F4D0` and `0x002F3860` |
| `0x02AEECB0`, `0x02AEEA20` | the depth matrix and the distance matrix |
| `0x02AED5F0` | the vector distances are measured from |
| `0x02EBB7E4`, `0x02EBB7E8`, `0x02EBB7EF` | the global fade near, far and floor complement |
| `0x020926E4` to `0x020926F0` | the dimming ramp: flags, count, value, target, step |

One more word of the settings block is written. `0x003ECCA0` builds the map's request from the map's defaults: near
`0x02EBB7F8`, far `0x02EBB7FC` and colour `0x02EBB804` (`0x003ECCBF`-`0x003ECCED`). The word between far and colour is not part
of it.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBB800` | `u32` | 0 (zero-filled tail of `.data`) | set to `0xFFFFFFFF` when `0x003ECF70` resets the settings, between the map's default far distance and its default colour; read by no function | `0x003ECF70` (`0x003ECF9A`) | no function |

## Modding notes

- An effect's own fade distances are the four `i16` words of its fade record; setting both of a
  pair equal turns that fade off.
- Mode 2 ignores the axis in lane 1, so an effect authored with it does not fade as the camera rises.
- The result is a modulate (128 is unchanged), so the alpha never exceeds the element's own.

## Related

- [Effect element runtime](effect-element-runtime.md): the containers.
- [Effect drawing](effect-drawing.md): the element draws.
- [Character fades](character-fades.md): the owner fade bit `0x10` multiplies in.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the dimming ramp.
- [PS2 CPU emulation](../Engine-Core/ps2-cpu-emulation.md): the workbench the transforms use.
