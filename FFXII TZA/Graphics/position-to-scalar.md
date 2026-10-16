---
title: "Position to scalar: the distance fade colour of effect elements"
kind: "system"
category: "Graphics"
summary: "The function that turns an effect element's 3-D position into one distance and then into the alpha of a modulate colour: its three distance modes, the four fade kinds of the fade record, the container flags that further scale the alpha (owner fade, status-display denial, the time-stop dimming ramp), and the 76 draw sites that multiply the result into what they draw."
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
`0x80808080` (`002F1F98`), and computes its byte 3, the alpha. `element + 0x20` is the element's
definition; its byte `+0x44` is the element kind. Kinds `0x40` and `0xA0` and above skip the
distance fade and keep alpha `0x80`.

The fade record is the one at `+0x2F0` of the effect container being drawn, `[02F97348]`, unless
that record's first byte is `0xFF`; then it is the definition's own record at `+0x50`. A record
whose kind byte is 0 leaves the alpha at `0x80`.

### The three distance modes

Byte `+1` of the record picks how the position becomes a distance:

| Mode | Distance |
|---|---|
| 0 | `0039B550` installs the matrix `02AEECB0` in the workbench and `0039ABF0` returns lane 3 (w) of the transformed point (`0039ADA7` `psrldq xmm1, 0xC`, `0039ADAC` `movd eax, xmm1`) |
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
| 1 | `+0x06` | `+0x0A` | `+0x03` | |
| 2 | `+0x04` | `+0x08` | `+0x02` | |
| 4 | both pairs | | | each pair as above; the smaller alpha wins |
| 3 | global | global | global | the mode-0 depth against the global fade settings, below |

A pair with `a == b` gives alpha `0x80`.

Kind 3 reads the global settings through `003ED0E0`: near `02EBB7E4`, far `02EBB7E8` and the byte
`02EBB7EF`, whose complement `255 - byte` is the floor. `003ECF70` sets near 10 and far 100. When the
record's float `+0x0C` is not 1.0 the floor becomes `255 - (255 - floor) x +0x0C`, kept in 0 to 256.
The alpha is then `(far - w) x 255 / (far - near)` with `w` from mode 0, capped and floored as above.

### The container's modifiers

After the fade, the flag word `+0x368` of the container applies, in this order (each result clamped
to 0 to 255):

| Bit | Effect on the colour |
|---|---|
| `0x8` | multiplied (`0026EE00`) by the container colour `+0x334`, or `+0x398` for element kind `0x40` |
| `0x400` | alpha x the float `02EBF278[container byte +0x377]` |
| `0x1000` | alpha x `+0x35C` when the element's `+0x208` differs from the container's `+0x37C` |
| `0x2000` | alpha x `+0x35C` when they are equal |
| `0x10` | alpha x the owner character's fade `0042FB20` (fade channel `0xB` / 4096); alpha 0 when `003A3FD0` finds no owner or `0041E590` reports it not drawn |
| `0x20` | alpha 0 while `003E7DE0` returns non-zero (the byte `02B59D71`) |
| `0x4` | alpha x the global scale `020926E8` |

### The global dimming ramp

`0024BFD0(0)` moves `020926E8` while bits 8 and 9 of `020926E4` hold 1 or 2: it counts `020926E6`
down, adds the step `020926F0`, and at zero stores the target `020926EC` and clears the two bits;
for the value 2 it then calls `002FD060` and `003B1000`. The ramp is started by `0024FB90` and `0024FBF0`, the time-stop fades on
[Time stop and freeze](../Engine-Core/time-stop-and-freeze.md).

### The callers

`002F1F40` has 76 call sites in 75 functions, from `00442550` to `00537410`
([census](position-to-scalar-fade-node-consumers.tsv)). At 67 of them the next call is the colour
multiply `0026EE00`. The smallest, `00442550`, calls the node with the element's position `+0x230`,
multiplies the result by the element's colour `+0x240`, and draws the point in that colour
(`0039C550`).

## Layouts

The fade record (in the container at `+0x2F0`, or in the element definition at `+0x50`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | kind: 0 none, 1, 2, 3 global, 4 both pairs |  |
| `01` | `u8` | distance mode: 0 depth, 1 distance, 2 distance without lane 1 |  |
| `02` | `u8` | floor for the +0x04/+0x08 pair |  |
| `03` | `u8` | floor for the +0x06/+0x0A pair |  |
| `04` | `i16` | full-alpha distance, pair 2 |  |
| `06` | `i16` | full-alpha distance, pair 1 |  |
| `08` | `i16` | zero-alpha distance, pair 2 |  |
| `0A` | `i16` | zero-alpha distance, pair 1 |  |
| `0C` | `f32` | kind 3: floor scale |  |

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
- [Character fades](character-fades.md): the owner fade bit `0x10` multiplies in.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the dimming ramp.
- [PS2 CPU emulation](../Engine-Core/ps2-cpu-emulation.md): the workbench the transforms use.
