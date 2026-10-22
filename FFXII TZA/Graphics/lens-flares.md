---
title: "Lens flares: the eight flare slots, the occlusion queries that measure them and the scene dimming they drive"
kind: "system"
category: "Graphics"
addresses: "0x02ADBB40, 0x02ADBB30, 0x02ADBB34, 0x00376350, 0x00376990, 0x00376470, 0x00376AC0, 0x00376D80, 0x00376A80, 0x00377010, 0x00377100, 0x00377130, 0x00377160, 0x003770D0, 0x00377090, 0x003769F0, 0x00376A20, 0x00376A50, 0x01F811F0, 0x001B29F0, 0x001B2630, 0x001B2680, 0x001849E0, 0x001B26F0, 0x001B2A30, 0x001B27E0, 0x00184AA0, 0x00184A70, 0x001B26D0, 0x001F3A00, 0x0017ED50, 0x0017E7E0, 0x00461090, 0x00461270, 0x00461250"
---

## What the player sees

A bright light in a scene, such as the sun, can carry a flare: glow and ghost shapes that brighten as
the light nears the centre of the screen. When a wall, a character or the edge of the screen hides the
light, the flare fades out over a few frames instead of popping, and a flare that is set to dazzle also
darkens the rest of the picture and lights the characters from the light's direction while it shows.

## How it works

### The flare slots

The game keeps eight flare slots of `0x90` bytes at `0x02ADBB40`. `0x00376350(rect, depth, with light)`
takes the first slot whose handle `+0x00` is 0: it raises the slot count `0x02ADBB30` and the serial
`0x02ADBB34` (wrapping from `0xFFFFFF` to 1), makes the handle `serial << 8 | slot`, stores the depth (0 from its
only caller, `0x004610EE`) at `+0x04`, zeroes the fades and the light handle, sets bit `0x4` and clears bit `0x8` of
the flags `+0x54`, and
copies the 16-byte rectangle to `+0x70`. With the third argument set it also creates a light
(`0x003AB960`) and keeps its handle at `+0x50`.

The light request is type 1, priority 0, subtype 2, scope 1, sub-kind 9 and class 16 (`+7` = `0x40`):
a directional light that every character takes and that is re-aimed from the camera
([how a character is lit](character-lighting-and-shadows.md)).

`0x00376990(handle)` frees a slot whose handle still matches: it lowers `0x02ADBB30`, clears the handle and
releases the light (`0x003ABCA0`). `0x00376A80` empties all eight slots and both counters. Every accessor
checks that `slot[handle & 0xFF]` still holds the handle and does nothing, or returns 0, otherwise:

| Function | Does |
|---|---|
| `0x00377010(handle, settings)` | copies flag bits 0 and 1, the three fade radii `+0x34` to `+0x3C`, the dimming strength `+0x40` and the light colour `+0x44` to `+0x4C` |
| `0x00377100(handle, rect)` | the test square in GS pixels, `+0x70` |
| `0x00377130(handle, rect)` | the same square as floats, `+0x80` |
| `0x003770D0(handle, depth)` | the 24-bit depth `+0x04` |
| `0x00377160(handle, vector)` | the light direction `+0x60` |
| `0x00377090(handle, on)` | flag bit 2 |
| `0x003769F0(handle)` | the visibility `+0x08` |
| `0x00376A50(handle)`, `0x00376A20(handle)` | the fades `+0x28` and `+0x2C` |

### The flare element

Effect element type `0xA1`, named `TsElementType_VLENSFLARE` by `0x002FBA60`, owns a slot when its definition's byte `+0x1B4` has bit 2 set. Its birth
`0x00461090` takes a slot (`0x00376350`, with the light when bit 5 of the definition word `+0x1CE` is
set) and keeps the handle at element `+0x294`. With bit 5 it also calls `0x001827B0(1)`, which sets byte
`+0xED` of the render-parameter block (`0x0018D640`). It then fills the settings from the definition
with `0x00377010`:

- flag bit 0 from bit 5 of `+0x1CE` and flag bit 1 from bit 4;
- radii from `+0x1F0`, `+0x1F4` and `+0x1F8`;
- the dimming strength from `+0x1DC` and the light colour from `+0x1E0` to `+0x1E8`.

Then it projects the element's position `+0x230` through `0x02AEECB0` (`0x0039B550`, `0x00399600`) and
stores the test square, the GS screen position `x / 16 − 0x700` and `y / 16 − 0x720` plus and minus
the half size `+0x1B6` (`0x00377100`), and the depth (`0x003770D0`). The release `0x00461250` frees the slot.

Each draw `0x00461270` repeats the projection, stores the square again in both forms (`0x00377130`,
`0x00377100`) and the depth, and for a bit-5 flare sets the light direction from `0x02AEEAD0` with w 1.0
(`0x00377160`) and clears flag bit 2. When the projection fails, a bit-5 flare sets flag bit 2 instead.
A bit-5 flare also passes its screen position, `(x − 1792) / 512` and `(y − 1824) / 448`, to
`0x00182830`, which stores it at render-parameter block `+0x36C` and `+0x370` (`0x00194470`);
`0x0018EEE0` copies the pair into the post-process command at `+0x44` and `+0x48` (`0x0018F3F5`).

### How the parts use the slot

`0x00461270` takes the slot's visibility (`0x003769F0`) as the element's intensity `0x02AEA3D8` (1.0 for an
element without a slot), scaled by the alpha byte of the element's colour over 128 unless that byte is
`0x80`, and reads the two fades (`0x00376A50`, `0x00376A20`). The parts it draws come from the model at definition `+0x208`: the count
`+0x1B2` of parts at the light, then up to `+0x1B3` further parts, each with an offset from the table
at `+0x170`. With bit 3 of `+0x1B4` each part also carries the angle of the light about the screen
centre, `atan2(y − 2048, x − 2048)`.

With bit 4 of `+0x1CE` set each part gets a scale from the fades, chosen by the part's bits in
`+0x1CE` (the parts at the light) or in `+0x1CC` and `+0x1CA` (the others):

- `fade A × +0x1D0 + 1` when its first bit is clear;
- `fade A × +0x1D4` when its second bit is clear;
- `fade B × +0x1D8` otherwise.

Without bit 4 every part has scale 1.

### The per-frame pass

The field frame runs `0x00376470` between its two draws ([the frame](../PhyreEngine/the-frame.md)).
It reads back last frame's query results (`0x00184AA0`), resets the light scale (`0x003AC870`), clears the
query list (`0x00184A70`), and for each slot with a handle and flag bit 3 clear:

1. When flag bit 1 or 0 is set it measures `d`, the distance of the test square's centre from the
   centre of the 512 by 448 GS screen (`0x022D8EAC`, `0x022D8EB4`).
2. For each fade it computes `t = 1 − d / radius`, passes a positive `t` through the easing curve
   `0x0046FAE0(t, 1, 2)` (0 otherwise), takes `min(1.5 × value, 1)` as the target and moves the fade 40%
   of the way to it. Flag bit 1 runs fade A (`+0x10`, radius `+0x34`, copied to `+0x28`) and fade B
   (`+0x18`, radius `+0x38`, copied to `+0x2C`); flag bit 0 runs fade C (`+0x20`, radius `+0x3C`,
   copied to `+0x30`).
3. The visibility target is 0 when the test square leaves the GS screen: `y0` beyond the height,
   `y1` below 1, `x1` beyond the width or `x0` below 1. Otherwise it is the query
   result whose handle matches the slot's, or the result at the slot's own position when none does.
   The visibility `+0x08` moves 40% of the way to the target.
4. Flag bit 0 runs the dimming `0x00376AC0` (below).
5. The four corners of the float square, at the slot's depth, are transformed by the matrix
   `0x02AEEB20` and then by the render manager's matrix `+0x6C8` (`0x0017ED50`, which applies it with
   the row transform `0x0017E7E0` and keeps the product at `0x01F7F550`), each divided by its w. The first and
   last corners, the depth and the current visibility go into the query list (`0x001849E0`).

A slot without a handle still adds an empty entry. The pass ends with `0x00182530`. The two
screen-capture states run `0x00376D80` instead, which sets flag bit 3 on every live slot, freezing its
fades, and copies `+0x08`, `+0x10`, `+0x18` and `+0x20` into the word after each.

### Dimming and the flare light

`0x00376AC0(slot)` computes `f = 1 − strength +0x40 × fade C +0x30 × visibility +0x08`. It multiplies the
scene colour `0x020926C0` to `0x020926C8` by `f` and the light scale `0x02B3F51C` by `f` (`0x003AC900`, which
also sets `0x02B3F503`).

When the slot has a light, it writes into the light's request (`0x003ABD00`): the direction `+0x60` to `+0x68` at request `+0x20`, the words `0x01F004E0` and `0x01F084E0` at `+0x40` and
`+0x44`, and with `s = min(1.5 × visibility, 1) × fade C` the colour `s × +0x44`, `s × +0x48`,
`s × +0x4C` with alpha 1.0. When `s` is 0.0001 or less it sets the skip bit 1 of request byte `+7`
instead, and clears it otherwise.

### The occlusion query manager

`0x001B29F0` builds the query manager `[0x01F811F0]`, `0x240` bytes (`0x001B2630`: a lock at `+0x218`,
everything else zero); `0x001B31D0` returns it. `0x001B2680` appends one entry, seven words, to the list
at `+0x04` and raises the count `+0x00`; `0x001B26D0` clears the list.

`ZBufferObj`, the render command with vtable `0x00903290`, runs `0x001F3A00` as its execute slot: after
its scene-begin calls it runs `0x001B26F0`, which, when any of the eight entries has a handle, queues
`0x001B2A30` on the render context (`0x005FEB30`) with a copy of the `0xE0`-byte list.

`0x001B2A30` runs on the render side with the primitive renderer of the context (`0x00624660`). On first
use it creates eight occlusion queries and keeps them at `+0x1D0` (`+0x1C8` points there). For each
entry:

- with no handle it clears the slot's pending byte `+0x210 + i`;
- it asks the slot's query for its 64-bit sample count. When the count is ready, the visibility is the
  count divided by the rectangle's area in back-buffer pixels (width `0x00182EB0`, height `0x00182E80`),
  0 when the area is 10 pixels or less, clamped to 0 to 1. A rectangle outside the screen or a depth
  outside 0 to 1 gives 0 and no new query;
- when the count is not ready it keeps last frame's value and issues a new query only if none is
  pending;
- to issue, it begins the query, draws the rectangle as a six-vertex quad at depth `z × 0.5 + 0.5`,
  ends the query and sets the pending byte.

Last it copies the eight entries, with their visibility, to `+0xE4` under the lock. `0x001B27E0`, through
`0x00184AA0`, copies them out under the lock and clamps each visibility again.

## Layouts

`FlareSlot` (`0x90` bytes, offsets from the start of the 0x02ADBB40+0x90*slot):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | serial << 8 \| slot; 0 = free |
| `+0x04` | `u32` | depth | 24-bit screen depth (`0x003770D0`) |
| `+0x08` | `f32` | visibility | 0 to 1, eased toward the query result |
| `+0x0C` | `f32` | visibilityFrozen | copy of +`0x08` (`0x00376D80`) |
| `+0x10` | `f32` | fadeA | eased, radius +`0x34` |
| `+0x14` | `f32` | fadeAFrozen | copy (`0x00376D80`) |
| `+0x18` | `f32` | fadeB | eased, radius +`0x38` |
| `+0x1C` | `f32` | fadeBFrozen | copy (`0x00376D80`) |
| `+0x20` | `f32` | fadeC | eased, radius +`0x3C` |
| `+0x24` | `f32` | fadeCFrozen | copy (`0x00376D80`) |
| `+0x28` | `f32` | fadeAOut | read by `0x00376A50` |
| `+0x2C` | `f32` | fadeBOut | read by `0x00376A20` |
| `+0x30` | `f32` | fadeCOut | read by `0x00376AC0` |
| `+0x34` | `f32` | radiusA | definition +`0x1F0` |
| `+0x38` | `f32` | radiusB | definition +`0x1F4` |
| `+0x3C` | `f32` | radiusC | definition +`0x1F8` |
| `+0x40` | `f32` | dimStrength | definition +`0x1DC` |
| `+0x44` | `f32[3]` | lightColour | definition +`0x1E0` to +`0x1E8` |
| `+0x50` | `u32` | light | light handle, 0 = none |
| `+0x54` | `u16` | flags | bit 0 dimming and light, bit 1 fades A and B, bit 2 set at creation and while unprojected, bit 3 frozen |
| `+0x60` | `f32[4]` | lightDirection | request +`0x20` (`0x00377160`) |
| `+0x70` | `i32[4]` | testSquare | y0, y1, x1, x0 in GS pixels (`0x00377100`) |
| `+0x80` | `f32[4]` | floatSquare | x0, x1, y0, y1 in GS coordinates; the query corners (`0x00377130`) |

`OcclusionEntry` (`0x1C` bytes, offsets from the start of the 0x01F811F0+0x04+0x1C*i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | flare slot handle; 0 = unused |
| `+0x04` | `f32` | y0 | first corner, normalised device coordinates |
| `+0x08` | `f32` | x0 |  |
| `+0x0C` | `f32` | x1 | opposite corner |
| `+0x10` | `f32` | y1 |  |
| `+0x14` | `f32` | depth | accepted from 0 to 1 |
| `+0x18` | `f32` | visibility | in: the slot's current value; out: the measured fraction |

`OcclusionManager` (`0x240` bytes, offsets from the start of the 0x01F811F0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` | count | entries appended this frame |
| `+0x004` | `u8[224]` | pending | eight OcclusionEntry, filled by `0x001B2680` |
| `+0x0E4` | `u8[224]` | results | eight OcclusionEntry, written by `0x001B2A30` under the lock |
| `+0x1C8` | `u64` | queries | pointer to +`0x1D0` once the queries exist |
| `+0x1D0` | `u64[8]` | query | pointers, one occlusion query per entry |
| `+0x210` | `u8[8]` | issued | a query is in flight |
| `+0x218` | `u8[40]` | lock | initialised by `0x005CC8A0` |

## State

| Address | What |
|---|---|
| `0x02ADBB30` | live flare slots |
| `0x02ADBB34` | handle serial, 1 to `0xFFFFFF` |
| `0x02ADBB40` | the eight flare slots |
| `0x01F811F0` | the occlusion query manager |
| `0x01F7F550` | the product matrix `0x0017ED50` returns |
| `0x020926C0` | the scene colour the dimming scales |

## Modding notes

- Only eight flares can exist at once; a ninth element of type `0xA1` with bit 2 of `+0x1B4` gets
  handle 0, so its visibility and fades read 0 and it draws with intensity 0.
- The test square's half size is definition `+0x1B6` in GS pixels; a rectangle that covers 10
  back-buffer pixels or less always reads as hidden.
- Visibility and the fades move 40% of the way a frame, so a hidden light's flare drops below 1% of
  its brightness after nine frames.
- The dimming strength `+0x1DC` of 0 keeps the scene colour unchanged while the flare light still
  shines.

## Related

- [How a character is lit](character-lighting-and-shadows.md): the light pool and the light scale.
- [Post-processing](post-processing.md): the render-parameter block and the post-process command.
- [The frame](../PhyreEngine/the-frame.md): where the field frame runs the per-frame pass.
- [Position to scalar](position-to-scalar.md): the projection matrix `0x02AEECB0`.
