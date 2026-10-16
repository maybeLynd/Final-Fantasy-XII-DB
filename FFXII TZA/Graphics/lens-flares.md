---
title: "Lens flares: the eight flare slots, the occlusion queries that measure them and the scene dimming they drive"
kind: "system"
category: "Graphics"
addresses: "02ADBB40, 02ADBB30, 02ADBB34, 00376350, 00376990, 00376470, 00376AC0, 00376D80, 00376A80, 00377010, 00377100, 00377130, 00377160, 003770D0, 00377090, 003769F0, 00376A20, 00376A50, 01F811F0, 001B29F0, 001B2630, 001B2680, 001849E0, 001B26F0, 001B2A30, 001B27E0, 00184AA0, 00184A70, 001B26D0, 001F3A00, 0017ED50, 0017E7E0, 00461090, 00461270, 00461250"
---

## What the player sees

A bright light in a scene, such as the sun, can carry a flare: glow and ghost shapes that brighten as
the light nears the centre of the screen. When a wall, a character or the edge of the screen hides the
light, the flare fades out over a few frames instead of popping, and a flare that is set to dazzle also
darkens the rest of the picture and lights the characters from the light's direction while it shows.

## How it works

### The flare slots

The game keeps eight flare slots of `90`<sub>h</sub> bytes at `02ADBB40`. `00376350(rect, depth, with light)`
takes the first slot whose handle `+00`<sub>h</sub> is 0: it raises the slot count `02ADBB30` and the serial
`02ADBB34` (wrapping from `FFFFFF`<sub>h</sub> to 1), makes the handle `serial << 8 | slot`, stores the depth (0 from its
only caller, `004610EE`) at `+04`<sub>h</sub>, zeroes the fades and the light handle, sets bit `4`<sub>h</sub> and clears bit `8`<sub>h</sub> of
the flags `+54`<sub>h</sub>, and
copies the 16-byte rectangle to `+70`<sub>h</sub>. With the third argument set it also creates a light
(`003AB960`) and keeps its handle at `+50`<sub>h</sub>.

The light request is type 1, priority 0, subtype 2, scope 1, sub-kind 9 and class 16 (`+7` = `40`<sub>h</sub>):
a directional light that every character takes and that is re-aimed from the camera
([how a character is lit](character-lighting-and-shadows.md)).

`00376990(handle)` frees a slot whose handle still matches: it lowers `02ADBB30`, clears the handle and
releases the light (`003ABCA0`). `00376A80` empties all eight slots and both counters. Every accessor
checks that `slot[handle & FFh]` still holds the handle and does nothing, or returns 0, otherwise:

| Function | Does |
|---|---|
| `00377010(handle, settings)` | copies flag bits 0 and 1, the three fade radii `+34`<sub>h</sub> to `+3C`<sub>h</sub>, the dimming strength `+40`<sub>h</sub> and the light colour `+44`<sub>h</sub> to `+4C`<sub>h</sub> |
| `00377100(handle, rect)` | the test square in GS pixels, `+70`<sub>h</sub> |
| `00377130(handle, rect)` | the same square as floats, `+80`<sub>h</sub> |
| `003770D0(handle, depth)` | the 24-bit depth `+04`<sub>h</sub> |
| `00377160(handle, vector)` | the light direction `+60`<sub>h</sub> |
| `00377090(handle, on)` | flag bit 2 |
| `003769F0(handle)` | the visibility `+08`<sub>h</sub> |
| `00376A50(handle)`, `00376A20(handle)` | the fades `+28`<sub>h</sub> and `+2C`<sub>h</sub> |

### The flare element

Effect element type `A1`<sub>h</sub>, named `TsElementType_VLENSFLARE` by `002FBA60`, owns a slot when its definition's byte `+1B4`<sub>h</sub> has bit 2 set. Its birth
`00461090` takes a slot (`00376350`, with the light when bit 5 of the definition word `+1CE`<sub>h</sub> is
set) and keeps the handle at element `+294`<sub>h</sub>. With bit 5 it also calls `001827B0(1)`, which sets byte
`+ED`<sub>h</sub> of the render-parameter block (`0018D640`). It then fills the settings from the definition
with `00377010`:

- flag bit 0 from bit 5 of `+1CE`<sub>h</sub> and flag bit 1 from bit 4;
- radii from `+1F0`<sub>h</sub>, `+1F4`<sub>h</sub> and `+1F8`<sub>h</sub>;
- the dimming strength from `+1DC`<sub>h</sub> and the light colour from `+1E0`<sub>h</sub> to `+1E8`<sub>h</sub>.

Then it projects the element's position `+230`<sub>h</sub> through `02AEECB0` (`0039B550`, `00399600`) and
stores the test square, the GS screen position `x / 16 − 700h` and `y / 16 − 720h` plus and minus
the half size `+1B6`<sub>h</sub> (`00377100`), and the depth (`003770D0`). The release `00461250` frees the slot.

Each draw `00461270` repeats the projection, stores the square again in both forms (`00377130`,
`00377100`) and the depth, and for a bit-5 flare sets the light direction from `02AEEAD0` with w 1.0
(`00377160`) and clears flag bit 2. When the projection fails, a bit-5 flare sets flag bit 2 instead.
A bit-5 flare also passes its screen position, `(x − 1792) / 512` and `(y − 1824) / 448`, to
`00182830`, which stores it at render-parameter block `+36C`<sub>h</sub> and `+370`<sub>h</sub> (`00194470`);
`0018EEE0` copies the pair into the post-process command at `+44`<sub>h</sub> and `+48`<sub>h</sub> (`0018F3F5`).

### How the parts use the slot

`00461270` takes the slot's visibility (`003769F0`) as the element's intensity `02AEA3D8` (1.0 for an
element without a slot), scaled by the alpha byte of the element's colour over 128 unless that byte is
`80`<sub>h</sub>, and reads the two fades (`00376A50`, `00376A20`). The parts it draws come from the model at definition `+208`<sub>h</sub>: the count
`+1B2`<sub>h</sub> of parts at the light, then up to `+1B3`<sub>h</sub> further parts, each with an offset from the table
at `+170`<sub>h</sub>. With bit 3 of `+1B4`<sub>h</sub> each part also carries the angle of the light about the screen
centre, `atan2(y − 2048, x − 2048)`.

With bit 4 of `+1CE`<sub>h</sub> set each part gets a scale from the fades, chosen by the part's bits in
`+1CE`<sub>h</sub> (the parts at the light) or in `+1CC`<sub>h</sub> and `+1CA`<sub>h</sub> (the others):

- `fade A × +1D0h + 1` when its first bit is clear;
- `fade A × +1D4h` when its second bit is clear;
- `fade B × +1D8h` otherwise.

Without bit 4 every part has scale 1.

### The per-frame pass

The field frame runs `00376470` between its two draws ([the frame](../PhyreEngine/the-frame.md)).
It reads back last frame's query results (`00184AA0`), resets the light scale (`003AC870`), clears the
query list (`00184A70`), and for each slot with a handle and flag bit 3 clear:

1. When flag bit 1 or 0 is set it measures `d`, the distance of the test square's centre from the
   centre of the 512 by 448 GS screen (`022D8EAC`, `022D8EB4`).
2. For each fade it computes `t = 1 − d / radius`, passes a positive `t` through the easing curve
   `0046FAE0(t, 1, 2)` (0 otherwise), takes `min(1.5 × value, 1)` as the target and moves the fade 40%
   of the way to it. Flag bit 1 runs fade A (`+10`<sub>h</sub>, radius `+34`<sub>h</sub>, copied to `+28`<sub>h</sub>) and fade B
   (`+18`<sub>h</sub>, radius `+38`<sub>h</sub>, copied to `+2C`<sub>h</sub>); flag bit 0 runs fade C (`+20`<sub>h</sub>, radius `+3C`<sub>h</sub>,
   copied to `+30`<sub>h</sub>).
3. The visibility target is 0 when the test square leaves the GS screen: `y0` beyond the height,
   `y1` below 1, `x1` beyond the width or `x0` below 1. Otherwise it is the query
   result whose handle matches the slot's, or the result at the slot's own position when none does.
   The visibility `+08`<sub>h</sub> moves 40% of the way to the target.
4. Flag bit 0 runs the dimming `00376AC0` (below).
5. The four corners of the float square, at the slot's depth, are transformed by the matrix
   `02AEEB20` and then by the render manager's matrix `+6C8`<sub>h</sub> (`0017ED50`, which applies it with
   the row transform `0017E7E0` and keeps the product at `01F7F550`), each divided by its w. The first and
   last corners, the depth and the current visibility go into the query list (`001849E0`).

A slot without a handle still adds an empty entry. The pass ends with `00182530`. The two
screen-capture states run `00376D80` instead, which sets flag bit 3 on every live slot, freezing its
fades, and copies `+08`<sub>h</sub>, `+10`<sub>h</sub>, `+18`<sub>h</sub> and `+20`<sub>h</sub> into the word after each.

### Dimming and the flare light

`00376AC0(slot)` computes `f = 1 − strength +40h × fade C +30h × visibility +08h`. It multiplies the
scene colour `020926C0` to `020926C8` by `f` and the light scale `02B3F51C` by `f` (`003AC900`, which
also sets `02B3F503`).

When the slot has a light, it writes into the light's request (`003ABD00`): the direction `+60`<sub>h</sub> to `+68`<sub>h</sub> at request `+20`<sub>h</sub>, the words `01F004E0` and `01F084E0` at `+40`<sub>h</sub> and
`+44`<sub>h</sub>, and with `s = min(1.5 × visibility, 1) × fade C` the colour `s × +44h`, `s × +48h`,
`s × +4Ch` with alpha 1.0. When `s` is 0.0001 or less it sets the skip bit 1 of request byte `+7`
instead, and clears it otherwise.

### The occlusion query manager

`001B29F0` builds the query manager `[01F811F0]`, `240`<sub>h</sub> bytes (`001B2630`: a lock at `+218`<sub>h</sub>,
everything else zero); `001B31D0` returns it. `001B2680` appends one entry, seven words, to the list
at `+04`<sub>h</sub> and raises the count `+00`<sub>h</sub>; `001B26D0` clears the list.

`ZBufferObj`, the render command with vtable `00903290`, runs `001F3A00` as its execute slot: after
its scene-begin calls it runs `001B26F0`, which, when any of the eight entries has a handle, queues
`001B2A30` on the render context (`005FEB30`) with a copy of the `E0`<sub>h</sub>-byte list.

`001B2A30` runs on the render side with the primitive renderer of the context (`00624660`). On first
use it creates eight occlusion queries and keeps them at `+1D0`<sub>h</sub> (`+1C8`<sub>h</sub> points there). For each
entry:

- with no handle it clears the slot's pending byte `+210h + i`;
- it asks the slot's query for its 64-bit sample count. When the count is ready, the visibility is the
  count divided by the rectangle's area in back-buffer pixels (width `00182EB0`, height `00182E80`),
  0 when the area is 10 pixels or less, clamped to 0 to 1. A rectangle outside the screen or a depth
  outside 0 to 1 gives 0 and no new query;
- when the count is not ready it keeps last frame's value and issues a new query only if none is
  pending;
- to issue, it begins the query, draws the rectangle as a six-vertex quad at depth `z × 0.5 + 0.5`,
  ends the query and sets the pending byte.

Last it copies the eight entries, with their visibility, to `+E4`<sub>h</sub> under the lock. `001B27E0`, through
`00184AA0`, copies them out under the lock and clamps each visibility again.

## Layouts

`FlareSlot` (`90`<sub>h</sub> bytes, offsets from the start of the 02ADBB40+`90`<sub>h</sub>*slot):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle | serial << 8 \| slot; 0 = free |
| `04`<sub>h</sub> | `u32` | depth | 24-bit screen depth (`003770D0`) |
| `08`<sub>h</sub> | `f32` | visibility | 0 to 1, eased toward the query result |
| `0C`<sub>h</sub> | `f32` | visibilityFrozen | copy of +`08`<sub>h</sub> (`00376D80`) |
| `10`<sub>h</sub> | `f32` | fadeA | eased, radius +`34`<sub>h</sub> |
| `14`<sub>h</sub> | `f32` | fadeAFrozen | copy (`00376D80`) |
| `18`<sub>h</sub> | `f32` | fadeB | eased, radius +`38`<sub>h</sub> |
| `1C`<sub>h</sub> | `f32` | fadeBFrozen | copy (`00376D80`) |
| `20`<sub>h</sub> | `f32` | fadeC | eased, radius +`3C`<sub>h</sub> |
| `24`<sub>h</sub> | `f32` | fadeCFrozen | copy (`00376D80`) |
| `28`<sub>h</sub> | `f32` | fadeAOut | read by `00376A50` |
| `2C`<sub>h</sub> | `f32` | fadeBOut | read by `00376A20` |
| `30`<sub>h</sub> | `f32` | fadeCOut | read by `00376AC0` |
| `34`<sub>h</sub> | `f32` | radiusA | definition +`1F0`<sub>h</sub> |
| `38`<sub>h</sub> | `f32` | radiusB | definition +`1F4`<sub>h</sub> |
| `3C`<sub>h</sub> | `f32` | radiusC | definition +`1F8`<sub>h</sub> |
| `40`<sub>h</sub> | `f32` | dimStrength | definition +`1DC`<sub>h</sub> |
| `44`<sub>h</sub> | `f32[3]` | lightColour | definition +`1E0`<sub>h</sub> to +`1E8`<sub>h</sub> |
| `50`<sub>h</sub> | `u32` | light | light handle, 0 = none |
| `54`<sub>h</sub> | `u16` | flags | bit 0 dimming and light, bit 1 fades A and B, bit 2 set at creation and while unprojected, bit 3 frozen |
| `60`<sub>h</sub> | `f32[4]` | lightDirection | request +`20`<sub>h</sub> (`00377160`) |
| `70`<sub>h</sub> | `i32[4]` | testSquare | y0, y1, x1, x0 in GS pixels (`00377100`) |
| `80`<sub>h</sub> | `f32[4]` | floatSquare | x0, x1, y0, y1 in GS coordinates; the query corners (`00377130`) |

`OcclusionEntry` (`1C`<sub>h</sub> bytes, offsets from the start of the 01F811F0+`04`<sub>h</sub>+`1C`<sub>h</sub>*i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle | flare slot handle; 0 = unused |
| `04`<sub>h</sub> | `f32` | y0 | first corner, normalised device coordinates |
| `08`<sub>h</sub> | `f32` | x0 |  |
| `0C`<sub>h</sub> | `f32` | x1 | opposite corner |
| `10`<sub>h</sub> | `f32` | y1 |  |
| `14`<sub>h</sub> | `f32` | depth | accepted from 0 to 1 |
| `18`<sub>h</sub> | `f32` | visibility | in: the slot's current value; out: the measured fraction |

`OcclusionManager` (`240`<sub>h</sub> bytes, offsets from the start of the 01F811F0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u32` | count | entries appended this frame |
| `004`<sub>h</sub> | `u8[224]` | pending | eight OcclusionEntry, filled by `001B2680` |
| `0E4`<sub>h</sub> | `u8[224]` | results | eight OcclusionEntry, written by `001B2A30` under the lock |
| `1C8`<sub>h</sub> | `u64` | queries | pointer to +`1D0`<sub>h</sub> once the queries exist |
| `1D0`<sub>h</sub> | `u64[8]` | query | pointers, one occlusion query per entry |
| `210`<sub>h</sub> | `u8[8]` | issued | a query is in flight |
| `218`<sub>h</sub> | `u8[40]` | lock | initialised by `005CC8A0` |

## State

| Address | What |
|---|---|
| `02ADBB30` | live flare slots |
| `02ADBB34` | handle serial, 1 to `FFFFFF`<sub>h</sub> |
| `02ADBB40` | the eight flare slots |
| `01F811F0` | the occlusion query manager |
| `01F7F550` | the product matrix `0017ED50` returns |
| `020926C0` | the scene colour the dimming scales |

## Modding notes

- Only eight flares can exist at once; a ninth element of type `A1`<sub>h</sub> with bit 2 of `+1B4`<sub>h</sub> gets
  handle 0, so its visibility and fades read 0 and it draws with intensity 0.
- The test square's half size is definition `+1B6`<sub>h</sub> in GS pixels; a rectangle that covers 10
  back-buffer pixels or less always reads as hidden.
- Visibility and the fades move 40% of the way a frame, so a hidden light's flare drops below 1% of
  its brightness after nine frames.
- The dimming strength `+1DC`<sub>h</sub> of 0 keeps the scene colour unchanged while the flare light still
  shines.

## Related

- [How a character is lit](character-lighting-and-shadows.md): the light pool and the light scale.
- [Post-processing](post-processing.md): the render-parameter block and the post-process command.
- [The frame](../PhyreEngine/the-frame.md): where the field frame runs the per-frame pass.
- [Position to scalar](position-to-scalar.md): the projection matrix `02AEECB0`.
