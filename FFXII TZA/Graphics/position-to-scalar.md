[Home](../../README.md) / [Graphics](README.md) / Position to scalar

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Position to scalar: the distance fade colour of effect elements | system | Graphics | Visual effects / Effect Elements And Drawing | The function that turns an effect element's 3-D position into one distance and then into the alpha of a modulate colour: its three distance modes, the four fade kinds of the distance-fade record, the container flags that further scale the alpha (owner fade, status-display denial, the time-stop dimming ramp), and the 76 draw sites that multiply the result into what they draw. | 0x002F1F40, 0x002F1D90, 0x0039B550, 0x0039ABF0, 0x0039AF70, 0x00398F90, 0x02F97348, 0x02AEECB0, 0x02AEEA20, 0x02AED5F0, 0x003ED0E0, 0x003ECF70, 0x0026EE00, 0x003A3FD0, 0x0042FB20, 0x003E7DE0, 0x0024BFD0, 0x020926E8, 0x00442550 |

## What the player sees

Spell and ability effects fade out with distance: a particle, a mesh piece or a glow drawn far from
the camera becomes transparent between two distances its effect file authors, and some fade by
ground distance only. The same colour also fades an effect with the character it belongs to, hides
it while status display is denied, and dims it while a time stop is running.

## How it works

### The call

`0x002F1F40(element, position, out)` writes one packed colour to `out`, starting from the neutral
`0x80808080`¹, and computes its byte 3, the alpha. `element + 0x20` is the element's
definition; its byte `+0x44` is the element kind. Kinds `0x40` and `0xA0` and above skip the
distance fade and keep alpha `0x80`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F1F98` |

</details>

The distance-fade record is the one at `+0x2F0` of the effect container being drawn, `[0x02F97348]`, unless
that record's first byte is `0xFF`; then it is the definition's own record at `+0x50`. A record
whose kind byte is 0, or 5 or more, leaves the alpha at `0x80`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F1FBC`, `0x002F2072`-`0x002F2093` |

</details>

### The three distance modes

Byte `+1` of the record picks how the position becomes a distance:

| Mode | Distance |
|---|---|
| 0 | `0x0039B550` installs the matrix `0x02AEECB0` in the workbench as the rows `vf01` to `vf04` (`0x0039B569`-`0x0039B5D4`) and raises lane 2 of `vf04` (`0x022D91E8`) by the depth offset `[0x02AEE7F0]` as a float (`0x0039B5F3`-`0x0039B60A`, [menu effects](menu-effects.md)), a lane that does not enter w. On the way it leaves the sign-extended offset in both halves of `v0` (`0x022D8F30`) and its four 32-bit words converted to float in `vf26` (`0x022D9340`) (`0x0039B55F`-`0x0039B5FA`). `0x0039ABF0` returns lane 3 (w) of the transformed point (`0x0039ADA7` `psrldq xmm1, 0xC`, `0x0039ADAC` `movd eax, xmm1`) |
| 1 | the point goes through the matrix `0x02AEEA20` (`0x0039AF70`, `0x00398F90`), then `0x002F1D90` returns its Euclidean distance from the vector `0x02AED5F0` |
| 2 | as mode 1, with lane 1 zeroed in the vector before the transform (`0x002F1FF2`) and in the point after it (`0x002F200F`): a distance in the other two axes |
| 3 or more | no call: the distance stays 0.0 (`0x002F1F8F`, `0x002F1FD6`), and kinds 1, 2 and 4 fade with that |

In mode 0, `0x0039ABF0(p)` computes the depth `w = p.x × vf01.w + p.y × vf02.w + p.z × vf03.w + vf04.w` from
the rows `vf01` to `vf04` (`0x022D91B0` to `0x022D91EC`) that `0x0039B550` fills¹; the
point's own lane 3 takes no part, and the last row is weighted by lane 3 of `vf00`, 1.0². It
returns `w` in `eax`³, the register both calls in `0x002F1F40` read⁴, and
leaves the product's `(x, y, z, w)` in `vf22`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039AC54`-`0x0039AD29` |
| ² | `0x0039AC9D` |
| ³ | `0x0039ADAC` |
| ⁴ | `0x002F206A`, `0x002F21F5` |
| ⁵ | `0x022D9300`, `0x0039ADB0`, `0x0039ADB8`, `0x0039AD35`, `0x0039AD61` |

</details>

`0x002F1D90(a, b)` returns `sqrtf(dx × dx + dy × dy + dz × dz)` with `d = b - a`, the square root of the
summed squared differences in lanes 0 to 2 (`0x002F1DC8`-`0x002F1E54`; `sqrtf` `0x00861F14` at `0x002F1E66`); lane 3
takes no part.

It copies `a` into `vf20`¹ and `b` into `vf21`² and then overwrites both. It leaves
`vf20` = `(dx, dy, dz, a.w)`³ and
`vf21` = `(vf00.x + root, dy × dy, dz × dz, b.w)`⁴. The root also goes
to `Q`⁵. It then adds the float at `0x01EF93F0`, which ships as 0.0: that is lane 0 of `vf00`,
re-stored as `(0, 0, 0, 1)` by `0x0036DD80` at `0x002F1E17`, so the result is the distance itself.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x022D92E0` |
| ² | `0x022D92F0` |
| ³ | `0x002F1DFF`-`0x002F1E0F` |
| ⁴ | `0x002F1E3C`, `0x002F1E48`, `0x002F1E7F` |
| ⁵ | `0x022D9198` |

</details>

`0x002F1D90` saves the workbench register `t0`¹ on entry and restores it on the way out
(`0x0036D930` at `0x002F1DAC`, `0x0036D8E0` at `0x002F1E9B`), so its copy of the result into `t0`²
does not last.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x022D8F90` |
| ² | `0x002F1E8E` |

</details>

The vector `0x02AED5F0` is written by `0x003820C0`¹, the camera update of
[Scripted camera](scripted-camera.md). All three matrices and the vector are past the raw end of `.data`, so
the image holds no values for them.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00382460` |

</details>

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

`0x003ED0E0(out)` fills four floats: the floor `255 - [0x02EBB7EF]` at `+0x00`¹, 0 at
`+0x04`², the slope `255.0 / (far - near)` at `+0x08`, with `far - near` taken in whole
numbers³, and `far` at `+0x0C`⁴. The caller takes the alpha as
`(out[+0x0C] - w) × out[+0x08]`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003ED10F`, `0x003ED130` |
| ² | `0x003ED111` |
| ³ | `0x003ED0F8`, `0x003ED11F` |
| ⁴ | `0x003ED11A` |
| ⁵ | `0x002F21F0`-`0x002F21FD` |

</details>

`0x003ECF70` resets the whole settings block¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003ECF70`-`0x003ECFC3` |

</details>

- near `0x02EBB7E4` = 10¹ and the eight bytes at `0x02EBB7E8` = 100²: far 100 and the
  colour word `0x02EBB7EC` 0, so the byte `0x02EBB7EF` is 0 and the floor `255 - 0` is 255;
- `0x02EBB7E0` = 0³ and the kept priority `0x02EBB7D0` = −1⁴;
- the map defaults: near `0x02EBB7F8` = 10 and far `0x02EBB7FC` = 100⁵, and 0 in the eight
  bytes at `0x02EBB804`, the default colour and the loaded flag `0x02EBB808`⁶;
- `0x02EBB800` = `0xFFFFFFFF`⁷ and 0 in the eight bytes at `0x02EBB7F0`⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003ECFAE` |
| ² | `0x003ECFB8` |
| ³ | `0x003ECF8A` |
| ⁴ | `0x003ECFA4` |
| ⁵ | `0x003ECF72`, `0x003ECF90` |
| ⁶ | `0x003ECF83` |
| ⁷ | `0x003ECF9A` |
| ⁸ | `0x003ECF7C` |

</details>

### Where the global settings come from

The settings at `0x02EBB7E0` are the winner of a request round. A request is 16 bytes: a priority, the
near and far distances, and a colour word whose top byte is the floor byte. `0x003ED170(request)`,
from `0x00377520` and `0x003B6C70`, keeps the request at `0x02EBB7D0` when its priority is higher than the
one kept. `0x003ED7F0(clear)`, from `0x0036F410` and `0x0036F530`, copies a kept request (priority 0 or
more) to `0x02EBB7E0`–`0x02EBB7EF` and, when `clear` is non-zero, drops the kept priority to −1.

The map's own request is built at `0x02EBB7C0` with priority 0 by `0x003ECCA0` while a map's settings are loaded
(`0x02EBB808` and `0x0209A660` set). `0x003ECAC0(request, target, t)` moves it toward a target: for `t`
above `0.99609375` it copies the target's near, far and colour, for `t` above `0.00390625` it
interpolates them, and otherwise does nothing. Each distance becomes `v = cur x (1 - t) + target x t`
stored as `trunc(v)`, plus 1 when `v - trunc(v) > 0.5`; each colour byte (split by `0x00466140`, packed by
`0x00466170`) becomes `trunc(cur x (1 - t) + target x t)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003ECAC0`-`0x003ECC9C` |

</details>

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

For bit `0x10`, `0x002F1F40` asks `0x003A3FD0(−1)` for the owner¹. With bit `0x200` of the
container's word `+0x378` set, `0x003A3FD0` passes the slot-0 target `[0x02096A20]` through `0x002E9B80`². Otherwise it goes by the container's kind byte `+0x00`: kind 3 returns the owner
`+0x08` as stored³; kinds 5, 6 and 9 look up the request `0x003B0BF0(+0x04)`, give −1
when it is missing⁴ and `+0x08` as stored when its byte `+0x11` is 1⁵; every other
case passes `+0x08` through `0x002E9B80`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F2438` |
| ² | `0x003A3FE5`, `0x003A404C` |
| ³ | `0x003A3FF1`, `0x003A4043` |
| ⁴ | `0x003A400D` |
| ⁵ | `0x003A400F` |
| ⁶ | `0x003A403C`, `0x003A4052` |

</details>

`0x002E9B80` returns the first dword of the `+0xC0` object of the actor `0x003588B0` finds, or −1¹. `0x002F1F40` sets the alpha to 0 when the owner is −1 or its low 16 bits are
`0xFFFF`², or when the record `index × 0x740 + [0x022C6F28]` has `+0x284`
= 0³, before it asks `0x0041E590`. With the fade `f` the alpha becomes
`min(trunc(alpha × f), 255)`, and 0 when that is negative⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9B84`-`0x002E9BA1` |
| ² | `0x002F2440`-`0x002F2449`, `0x002F24A7` |
| ³ | `0x002F245D`-`0x002F246A` |
| ⁴ | `0x002F248C`-`0x002F24A2` |

</details>

`0x0042FB20(index)` returns 1.0 for index −1¹ and for a record `index × 0x740 + [0x022C6F28]` that
is null or has `+0x284` = 0²; otherwise it returns the signed 16-bit fade channel
`0xB` of `0x003E48E0(record, 0xB)` × 1/4096³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0042FB24` |
| ² | `0x0042FB42`-`0x0042FB52` |
| ³ | `0x00908E14`, `0x0042FB59`-`0x0042FB68` |

</details>

### The global dimming ramp

`0x0024BFD0(0)` moves `0x020926E8` while bits `0x100` and `0x200` of `0x020926E4` hold 1 or 2: it counts `0x020926E6`
down, adds the step `0x020926F0`, and at zero stores the target `0x020926EC`, calls `0x002FD060` and `0x003B1000`
when the two bits hold 2¹, and then clears the two bits². The ramp is started by `0x0024FB90` and `0x0024FBF0`, the
time-stop fades on [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024C037`, `0x0024C03C` |
| ² | `0x0024C046` |

</details>

With a non-zero argument `0x0024BFD0` returns at once¹, and with the two bits at 0 or 3 it returns
without a step². The two calls at the end of a value-2 ramp clear bit `0x4` of `+0x368`, the alpha x
`0x020926E8` modifier above: `0x002FD060` on every instance of the kind-1 list `0x02EC3D60`³, `0x003B1000` on
the instance `+0x08` of each of the 36 request entries at `0x02EBEC00`, up to the first whose dword `+0` is 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024BFD6` |
| ² | `0x0024BFE9` |
| ³ | `0x002FD07A` |
| ⁴ | `0x003B1010`-`0x003B1030` |

</details>

### The callers

`0x002F1F40` has 76 call sites in 75 functions, from `0x00442550` to `0x00537410`
([table](position-to-scalar-fade-node-consumers.tsv)). At 67 of them the next call is the colour
multiply `0x0026EE00`. The smallest, `0x00442550`, calls the node with the element's position `+0x230`,
multiplies the result by the element's colour `+0x240`, and draws the point in that colour¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039C550` |

</details>

### Columns of position-to-scalar-fade-node-consumers.tsv

One row per `call 0x002F1F40` in the code section, 76 rows. From each call the table follows up to 24 further
instructions, stopping at a `ret` or `int3`, and gives the first direct call among them.

| Column | Holds |
|---|---|
| `caller` | the start address of the function that holds the call, from the disassembly's function list (75 functions; `0x004427D0` holds two calls) |
| `site` | the address of the `call 0x002F1F40` |
| `first_call_after` | the target of the first direct call after it: `0x0026EE00`, the colour multiply, at 67 sites; `0x003A2B20` at 3, `0x0042FDB0` at 2, and `0x002F1F40`, `0x003D8E20` and `0x00808C40` once each; `-` at `0x00464CF7`, where no call comes within 24 instructions |
| `instructions_between` | how many instructions that walk decoded, counting the call it found: 4 to 12 (4 at 45 sites, 6 at 20); 25 on the `-` row, where the walk ran out |

## Layouts

<details>
<summary>Show the memory layouts</summary>

The distance-fade record (in the container at `+0x2F0`, or in the element definition at `+0x50`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | kind: 0 no scalar, 1, 2, 3 global, 4 both pairs |
| `+0x01` | `u8` |  | distance mode: 0 depth, 1 distance, 2 distance without lane 1 |
| `+0x02` | `u8` |  | floor for the `+0x04`/`+0x08` pair |
| `+0x03` | `u8` |  | floor for the `+0x06`/`+0x0A` pair |
| `+0x04` | `i16` |  | full-alpha distance, pair 2 |
| `+0x06` | `i16` |  | full-alpha distance, pair 1 |
| `+0x08` | `i16` |  | zero-alpha distance, pair 2 |
| `+0x0A` | `i16` |  | zero-alpha distance, pair 1 |
| `+0x0C` | `f32` |  | kind 3: floor scale |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Holds |
|---|---|
| `0x02F97348` | the effect container being drawn; written by `0x0024B270`, `0x0024B580`, `0x0024C460`, `0x0024D540`, `0x0024DB80`, `0x0024ED80`, `0x0024EEE0`, `0x0024F4D0` and `0x002F3860` |
| `0x02AEECB0`, `0x02AEEA20` | the depth matrix and the distance matrix |
| `0x02AED5F0` | the vector distances are measured from |
| `0x02EBB7E4`, `0x02EBB7E8`, `0x02EBB7EF` | the global fade near, far and floor complement |
| `0x020926E4` to `0x020926F0` | the dimming ramp: flags, count, value, target, step |

One more word of the settings block is written. `0x003ECCA0` builds the map's request from the map's defaults: near
`0x02EBB7F8`, far `0x02EBB7FC` and colour `0x02EBB804`¹. The word between far and colour is not part
of it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003ECCBF`-`0x003ECCED` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBB800` | `u32` | 0 (zero-filled tail of `.data`) | set to `0xFFFFFFFF` when `0x003ECF70` resets the settings, between the map's default far distance and its default colour; read by no function | `0x003ECF70` (`0x003ECF9A`) | no function |

Two requests are kept in globals: the map's own request at `0x02EBB7C0` (its priority at `0x02EBB7C0`, near at `0x02EBB7C4`) and the
fog request that a new map leaves at `0x02ADD108`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBB7C8` | `i32` | 0 (zero-filled tail) | the map request's far distance, a whole number | `0x003ECCA0`, the map default `0x02EBB7FC` (`0x003ECCE1`); `0x003ECAC0`, the target's far or the blend, through its first argument, which `0x003ECCA0` passes as `0x02EBB7C0` (`0x003ECAF8`, `0x003ECB9D`) | `0x003ECAC0` (`0x003ECB53`); `0x003ECE60`, in the 16-byte load of the request (`0x003ECE91`) |
| `0x02EBB7CC` | `u32` | 0 | the map request's colour word, the floor byte on top | `0x003ECCA0`, the map default `0x02EBB804` (`0x003ECCED`); `0x003ECAC0` (`0x003ECAFE`, `0x003ECC7A`) | `0x003ECAC0` (`0x003ECB9A`); `0x003ECE60` (`0x003ECE91`, scaling red, green and blue before it submits) |
| `0x02ADD108` | `i32` | 0 | the priority of the fog request `0x02ADD108`-`0x02ADD117`: 10 | `0x00378120`, 10 when a map is set up (`0x003781D6`), after copying the environment's near, far and colour to `0x02ADD10C`-`0x02ADD114` (`0x003781AB`-`0x003781C9`) | `0x003ED170`, as the request's priority, compared signed with the kept one (`0x003ED176`-`0x003ED178`); `0x00377520` passes `0x02ADD108` (`0x0037753F`) |
| `0x02ADD115` | `u8` | 0 (zero-filled tail) | byte 1 of the fog request's colour `0x02ADD114`, the second value of the verb `seteventfogcolor` (`0x120`) | `0x00378120`, with the colour word from the map default `0x02EBB804` (`0x003781C9`); `0x00379950`, its second argument (`0x00379956`), entered by the tail jump of the verb's handler `0x00351AA0` (`0x00351B37`), which clamps each value to 0-255 (`0x00351AE0`) | `0x003ED170` (`0x003ED17A`), in the 16-byte copy of the request into the kept request `0x02EBB7D0` when its priority is higher |
| `0x02ADD116` | `u8` | 0 (zero-filled tail) | byte 2 of the fog request's colour `0x02ADD114`, the third value of the verb `seteventfogcolor` (`0x120`) | `0x00378120`, with the colour word from the map default `0x02EBB804` (`0x003781C9`); `0x00379950`, its third argument (`0x0037995C`), entered by the tail jump of the verb's handler `0x00351AA0` (`0x00351B37`), which clamps each value to 0-255 (`0x00351AE0`) | `0x003ED170` (`0x003ED17A`), in the 16-byte copy of the request into the kept request `0x02EBB7D0` when its priority is higher |

`0x00377520`, from `0x0022A770`, `0x0022B0B0` and `0x00314820`, submits the fog request while `0x02ADD118` is set and
`0x02EBF9C8` is non-zero¹, then clears `0x02ADD0F4`². It also submits when `0x02ADD0F4`
is non-zero³, but every store to `0x02ADD0F4` writes 0⁴, so only
`0x02EBF9C8` triggers the request.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00377524`-`0x00377546` |
| ² | `0x0037754B` |
| ³ | `0x00377536` |
| ⁴ | `0x0037754B`, `0x0037832E`, `0x00378A8C` |

</details>

</details>

## Modding notes

- An effect's own fade distances are the four `i16` words of its distance-fade record; setting both of a
  pair equal turns that fade off.
- Mode 2 ignores the axis in lane 1, so an effect authored with it does not fade as the camera rises.
- The result is a modulate (128 is unchanged), so the alpha never exceeds the element's own.

## Related

- [Effect element runtime](effect-element-runtime.md): the containers.
- [Effect drawing](effect-drawing.md): the element draws.
- [Character fades](character-fades.md): the owner fade bit `0x10` multiplies in.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the dimming ramp.
- [PS2 CPU emulation](../Engine-Core/ps2-cpu-emulation.md): the workbench the transforms use.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 19 calls with 6 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E9B80`](effect-anchors-and-targets.md) (on effect anchors and targets) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x0036DD80`](position-to-scalar.md) | is called by | [`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names) |
| [`0x00378120`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) | calls | [`0x00332130`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Controls and input** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0022A770`](../Engine-Core/frame-update-order.md) (on frame update order) | calls | [`0x0017DE60`](../Controls-And-Input/on-screen-keyboard.md) (on on screen keyboard)<br>[`0x002498B0`](../Controls-And-Input/controls.md) (on controls)<br>[`0x00250180`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0035AE30`](../Controls-And-Input/vibration.md) (on vibration)<br>[`0x0035AF20`](../Controls-And-Input/vibration.md) (on vibration)<br>[`0x0035E9A0`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0035FF90`](../Controls-And-Input/controls.md) (on controls)<br>[`0x0036FDF0`](../Controls-And-Input/controls.md) (on controls)<br>[`0x0036FF70`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses)<br>[`0x0036FFD0`](../Controls-And-Input/controls.md) (on controls) |

**Steam and achievements** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0022A770`](../Engine-Core/frame-update-order.md) (on frame update order) | calls | [`0x00316930`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Scripts and script commands** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00351AA0`](position-to-scalar.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00379950`](position-to-scalar.md) | is called by | [`0x00351AA0`](position-to-scalar.md) |

**World, areas and travel** (explained on [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [debug logging](../Engine-Core/debug-logging.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00378120`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) | calls | [`0x003C63A0`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |
| [`0x0022A770`](../Engine-Core/frame-update-order.md) (on frame update order) | calls | [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x00378120`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) | is called by | [`0x003775D0`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |

</details>
