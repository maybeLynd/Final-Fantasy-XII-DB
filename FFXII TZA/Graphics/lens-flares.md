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
| `0x00377010(handle, settings)` | copies flag bits `0x1` and `0x2`, the three fade radii `+0x34` to `+0x3C`, the dimming strength `+0x40` and the light colour `+0x44` to `+0x4C` |
| `0x00377100(handle, rect)` | the test square in GS pixels, `+0x70` |
| `0x00377130(handle, rect)` | the same square as floats, `+0x80` |
| `0x003770D0(handle, depth)` | the 24-bit depth `+0x04` |
| `0x00377160(handle, vector)` | the light direction `+0x60` |
| `0x00377090(handle, on)` | flag bit `0x4` |
| `0x003769F0(handle)` | the visibility `+0x08` |
| `0x00376A50(handle)`, `0x00376A20(handle)` | the fades `+0x28` and `+0x2C` |

### The flare element

Effect element type `0xA1`, named `TsElementType_VLENSFLARE` by `0x002FBA60`, owns a slot when its definition's byte `+0x1B4` has bit `0x4` set. Its birth
`0x00461090` takes a slot (`0x00376350`, with the light when bit `0x20` of the definition word `+0x1CE` is
set) and keeps the handle at element `+0x294`. With bit `0x20` it also calls `0x001827B0(1)`, which sets byte
`+0xED` of the render-parameter block (`0x0018D640`). It then fills the settings from the definition
with `0x00377010`:

- flag bit `0x1` from bit `0x20` of `+0x1CE` and flag bit `0x2` from bit `0x10`;
- radii from `+0x1F0`, `+0x1F4` and `+0x1F8`;
- the dimming strength from `+0x1DC` and the light colour from `+0x1E0` to `+0x1E8`.

Then it projects the element's position `+0x230` through `0x02AEECB0` (`0x0039B550`, `0x00399600`) and
stores the test square, the GS screen position `x / 16 − 0x700` and `y / 16 − 0x720` plus and minus
the half size `+0x1B6` (`0x00377100`), and the depth (`0x003770D0`). The release `0x00461250` frees the slot.

Each draw `0x00461270` repeats the projection, stores the square again in both forms (`0x00377130`,
`0x00377100`) and the depth, and for a bit `0x20` flare sets the light direction from `0x02AEEAD0` with w 1.0
(`0x00377160`) and clears flag bit 2. When the projection fails, a bit `0x20` flare sets flag bit 2 instead.
A bit `0x20` flare also passes its screen position, `(x − 1792) / 512` and `(y − 1824) / 448`, to
`0x00182830`, which stores it at render-parameter block `+0x36C` and `+0x370` (`0x00194470`);
`0x0018EEE0` copies the pair into the post-process command at `+0x44` and `+0x48` (`0x0018F3F5`).

### How the parts use the slot

`0x00461270` takes the slot's visibility (`0x003769F0`) as the element's intensity `0x02AEA3D8` (1.0 for an
element without a slot), scaled by the alpha byte of the element's colour over 128 unless that byte is
`0x80`, and reads the two fades (`0x00376A50`, `0x00376A20`). The parts it draws come from the model at definition `+0x208`: the count
`+0x1B2` of parts at the light, then up to `+0x1B3` further parts, each with an offset from the table
at `+0x170`. With bit `0x8` of `+0x1B4` each part also carries the angle of the light about the screen
centre, `atan2(y − 2048, x − 2048)`.

With bit 4 of `+0x1CE` set each part gets a scale from the fades, chosen by the part's bits in
`+0x1CE` (the parts at the light) or in `+0x1CC` and `+0x1CA` (the others):

- `fade A × +0x1D0 + 1` when its first bit is clear;
- `fade A × +0x1D4` when its second bit is clear;
- `fade B × +0x1D8` otherwise.

Without bit 4 every part has scale 1.

### The flare packet

The draw hands its parts to the lens-flare microprogram `0x004C0EA0` in a boot template, as the draws in
[effect element types](effect-element-types.md) do. `0x004C2040`, which `0x0037E0F0` calls at start-up (`0x0037E0FB`),
builds the `0xC20`-byte template `0x02AEA3A0`. Its VIF codes unpack `0xBC` cells to VU cells 0 to `0xBB` (`+0x1C` =
`0x6CBC0000`, `0x004C206D`), so the word at `0x02AEA3C0 + 16 × cell + 4 × lane` lands in that cell and lane. Each draw
writes its values into the template and passes `0x02AEA3B8`, `0xC08` bytes, with the program to `0x003A34D0`
(`0x004620CF`-`0x004620FC`).

| Cell | What the draw or the builder puts there |
|---|---|
| 0 | x and y: the light's GS screen position; z and w: the vector track at definition `+0x110` at the element's frame |
| 1 | z: the intensity `0x02AEA3D8` |
| 2 | x: the number of further parts; y: the number of parts at the light; w: `0x8000` (`0x004C20A5`) |
| 3 to `0x32` | the further parts, three cells each, from `0x02AEA3F0` |
| `0x33` on | the parts at the light, three cells each, from `0x02AEA6F0` |
| `0x39` to `0xB8` | four cells for each of the flare model's first 32 rows (`0x00461720`-`0x00461A88`) |
| `0xB9` | a GIF tag for one `A+D` register (`0x004C20AC`, `0x004C20B7`, `0x004C20C1`) |
| `0xBA` | the `TEX0_1` value: x and y its two words, z the register number 6 (`0x004C20CB`) |
| `0xBB` | the GIF tag of the parts (`0x004C20D5`-`0x004C20F3`), whose count the program fills in |

The program starts its first pass with the count in cell 2 lane y (`0x004C1006`) and its second with lane x
(`0x004C17A0`). For the second pass it subtracts cell 0's z and w from its x and y (`0x004C176E`-`0x004C177F`).

The draw skips the hand-over when a part's row and count reach 32 (`0x00461B3A`, `0x00461C84`, both to `0x00462101`).

### The per-frame pass

The field frame runs `0x00376470` between its two draws ([the frame](../PhyreEngine/the-frame.md)).
It reads back last frame's query results (`0x00184AA0`), resets the light scale (`0x003AC870`), clears the
query list (`0x00184A70`), and for each slot with a handle and flag bit `0x8` clear:

1. When flag bit `0x2` or `0x1` is set it measures `d`, the distance of the test square's centre from the
   centre of the 512 by 448 GS screen (`0x022D8EAC`, `0x022D8EB4`).
2. For each fade it computes `t = 1 − d / radius`, passes a positive `t` through the easing curve
   `0x0046FAE0(t, 1, 2)` (0 otherwise), takes `min(1.5 × value, 1)` as the target and moves the fade 40%
   of the way to it. Flag bit `0x2` runs fade A (`+0x10`, radius `+0x34`, copied to `+0x28`) and fade B
   (`+0x18`, radius `+0x38`, copied to `+0x2C`); flag bit `0x1` runs fade C (`+0x20`, radius `+0x3C`,
   copied to `+0x30`).
3. The visibility target is 0 when the test square leaves the GS screen: `y0` beyond the height,
   `y1` below 1, `x1` beyond the width or `x0` below 1. Otherwise it is the query
   result whose handle matches the slot's, or the result at the slot's own position when none does.
   The visibility `+0x08` moves 40% of the way to the target.
4. Flag bit `0x1` runs the dimming `0x00376AC0` (below).
5. The four corners of the float square, at the slot's depth, are transformed by the matrix
   `0x02AEEB20` and then by the render manager's matrix `+0x6C8` (`0x0017ED50`, which applies it with
   the row transform `0x0017E7E0` and keeps the product at `0x01F7F550`), each divided by its w. The first and
   last corners, the depth and the current visibility go into the query list (`0x001849E0`).

A slot without a handle still adds an empty entry. The pass ends with `0x00182530`. The two
screen-capture states run `0x00376D80` instead, which sets flag bit `0x8` on every live slot, freezing its
fades, and copies `+0x08`, `+0x10`, `+0x18` and `+0x20` into the word after each.

### Ending the freeze

`0x00376BE0` undoes the freeze when play returns to the field. The full menu frame `0x0022B8C0` runs it after
`CLOSE FULLMENU` (`0x0022BBDE`), and the capture-backed frame `0x0022BC20` after it goes back to state 2
(`0x0022BDCC`). For each slot with a handle (`0x00376C30`) it:

1. clears flag bit `0x8` (`0x00376C3D`);
2. copies the four kept words back: `+0x0C` to `+0x08`, `+0x14` to `+0x10`, `+0x1C` to `+0x18` and `+0x24` to
   `+0x20` (`0x00376C3A`-`0x00376C57`);
3. when flag bit `0x1` is set (`0x00376C40`), dims the scene colour and the light scale and rewrites the flare light's
   request as `0x00376AC0` does (`0x00376C62`-`0x00376D43`).

### Dimming and the flare light

`0x00376AC0(slot)` computes `f = 1 − strength +0x40 × fade C +0x30 × visibility +0x08`. It multiplies the
scene colour `0x020926C0` to `0x020926C8` by `f` and the light scale `0x02B3F51C` by `f` (`0x003AC900`, which
also sets `0x02B3F503`).

When the slot has a light, it writes into the light's request (`0x003ABD00`): the direction `+0x60` to `+0x68` at request `+0x20`, the words `0x01F004E0` and `0x01F084E0` at `+0x40` and
`+0x44`, and with `s = min(1.5 × visibility, 1) × fade C` the colour `s × +0x44`, `s × +0x48`,
`s × +0x4C` with alpha 1.0. When `s` is 0.0001 or less it sets the skip bit `0x2` of request byte `+7`
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
| `+0x0C` | `f32` | visibilityFrozen | copy of `+0x08` (`0x00376D80`) |
| `+0x10` | `f32` | fadeA | eased, radius `+0x34` |
| `+0x14` | `f32` | fadeAFrozen | copy (`0x00376D80`) |
| `+0x18` | `f32` | fadeB | eased, radius `+0x38` |
| `+0x1C` | `f32` | fadeBFrozen | copy (`0x00376D80`) |
| `+0x20` | `f32` | fadeC | eased, radius `+0x3C` |
| `+0x24` | `f32` | fadeCFrozen | copy (`0x00376D80`) |
| `+0x28` | `f32` | fadeAOut | read by `0x00376A50` |
| `+0x2C` | `f32` | fadeBOut | read by `0x00376A20` |
| `+0x30` | `f32` | fadeCOut | read by `0x00376AC0` |
| `+0x34` | `f32` | radiusA | definition `+0x1F0` |
| `+0x38` | `f32` | radiusB | definition `+0x1F4` |
| `+0x3C` | `f32` | radiusC | definition `+0x1F8` |
| `+0x40` | `f32` | dimStrength | definition `+0x1DC` |
| `+0x44` | `f32[3]` | lightColour | definition `+0x1E0` to `+0x1E8` |
| `+0x50` | `u32` | light | light handle, 0 = none |
| `+0x54` | `u16` | flags | bit `0x1` dimming and light, bit `0x2` fades A and B, bit `0x4` set at creation and while unprojected, bit `0x8` frozen |
| `+0x60` | `f32[4]` | lightDirection | request `+0x20` (`0x00377160`) |
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
| `+0x1C8` | `u64` | queries | pointer to `+0x1D0` once the queries exist |
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

### The flare packet's words

These words of the template `0x02AEA3A0` are written by the draw `0x00461270`. The command reads each one from the
template when it runs: `0x0022BFF0` copies it into its VU cell at the lane site given.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AEA3C0` | `f32` | 0 (zero-filled tail of `.data`) | cell 0 lane x: the light's x on the GS screen, the projected x / 16 (2048 is the centre); 2000.0 after boot | `0x004C2040` (`memset` at `0x004C2051`, `0x004C207B`); `0x00461270` (`0x00461502`) | `0x00461270` (`0x0046162D`, the part angle); `0x0022BFF0` (`0x0022C650`) |
| `0x02AEA3C4` | `f32` | 0 (zero-filled tail of `.data`) | cell 0 lane y: the light's y on the GS screen, the projected y / 16; 2000.0 after boot | `0x004C2040` (`memset` at `0x004C2051`, `0x004C2074`); `0x00461270` (`0x0046150A`) | `0x00461270` (`0x00461625`, the part angle); `0x0022BFF0` (`0x0022C658`) |
| `0x02AEA3C8` | `f32` | 0 (zero-filled tail of `.data`) | cell 0 lane z: x of the vector track at definition `+0x110` at the element's frame (`0x00430B90`, `0x00461562`); 2048.0 after boot | `0x004C2040` (`memset` at `0x004C2051`, `0x004C2089`); `0x00461270` (`0x0046156A`) | `0x0022BFF0` (`0x0022C65E`) |
| `0x02AEA3CC` | `f32` | 0 (zero-filled tail of `.data`) | cell 0 lane w: y of the same track (`0x00461572`); 2048.0 after boot | `0x004C2040` (`memset` at `0x004C2051`, `0x004C2082`); `0x00461270` (`0x00461576`) | `0x0022BFF0` (`0x0022C666`) |
| `0x02AEA3E0` | `u32` | 0 (zero-filled tail of `.data`) | cell 2 lane x: the number of further parts. It is `+0x1B3` (`0x00461C2C`), or with a part list at definition `+0x20C` the list's count `+0x10` less the parts at the light, at most `+0x1B3` (`0x00461F3E`); each part the draw skips lowers it by one | `0x004C2040` (`memset` at `0x004C2051`); `0x00461270` (`0x00461C2C`, `0x00461C74`, `0x00461F3E`, `0x00461F75`, `0x00461FA6`) | `0x00461270` (`0x00461C74`, `0x00461F75`, `0x00461FA6`); `0x0022BFF0` (`0x0022C650`) |
| `0x02AEA3E4` | `u32` | 0 (zero-filled tail of `.data`) | cell 2 lane y: the number of parts at the light: `+0x1B2` (`0x00461D9F`) or the parts the draw placed (`0x00461C1E`, `0x00461F27`); the draw numbers the further parts after them | `0x004C2040` (`memset` at `0x004C2051`); `0x00461270` (`0x00461C1E`, `0x00461D9F`, `0x00461F27`) | `0x00461270` (`0x00461D89`, `0x00461F16`); `0x0022BFF0` (`0x0022C658`) |
| `0x02AEAF60` | `u32` | 0 (zero-filled tail of `.data`) | cell `0xBA` lane x: the low word of `TEX0_1`, the first word of the texture register pair `0x005030F0` copies for the flare model's row (`0x00461AA1`) | `0x004C2040` (`memset` at `0x004C2051`); `0x00461270` (`0x00461ABF`) | `0x0022BFF0` (`0x0022C650`) |
| `0x02AEAF64` | `u32` | 0 (zero-filled tail of `.data`) | cell `0xBA` lane y: the high word of `TEX0_1`. When the palette operation at definition `+0x150` has a kind, its high 27 bits come from the high word of the result of `0x00431B10` (`0x004616A8`, `0x00461AB2`-`0x00461AB9`) | `0x004C2040` (`memset` at `0x004C2051`); `0x00461270` (`0x00461AC5`) | `0x0022BFF0` (`0x0022C666`) |

### The product matrix's cells

`0x0017ED50` stores the matrix row by row and returns `0x01F7F550` (`0x0017EE3A`). The per-frame pass
`0x00376470` calls it (`0x0037683E`) and passes that pointer (`0x00376848`) to `0x00202D70`, which jumps to the multiply `0x00217150`. The multiply
reads the cells through its second argument at the sites below.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F7F554` | `f32` | 0 (zero-filled tail of `.data`) | row 0, column 1 | `0x0017ED50` (`0x0017EE6A`) | `0x00217150` (`0x002171A5`, `0x002173D5`) |
| `0x01F7F558` | `f32` | 0 (zero-filled tail of `.data`) | row 0, column 2 | `0x0017ED50` (`0x0017EE5F`) | `0x00217150` (`0x00217187`) |
| `0x01F7F55C` | `f32` | 0 (zero-filled tail of `.data`) | row 0, column 3 | `0x0017ED50` (`0x0017EEE1`) | `0x00217150` (`0x00217257`) |
| `0x01F7F560` | `f32` | 0 (zero-filled tail of `.data`) | row 1, column 0 | `0x0017ED50` (`0x0017EE41`) | `0x00217150` (`0x0021716D`, `0x002172A1`, `0x00217312`, `0x002173DE`) |
| `0x01F7F564` | `f32` | 0 (zero-filled tail of `.data`) | row 1, column 1 | `0x0017ED50` (`0x0017EE88`) | `0x00217150` (`0x002171C6`, `0x002173FD`) |
| `0x01F7F568` | `f32` | 0 (zero-filled tail of `.data`) | row 1, column 2 | `0x0017ED50` (`0x0017EE7D`) | `0x00217150` (`0x002171B0`, `0x00217417`) |
| `0x01F7F56C` | `f32` | 0 (zero-filled tail of `.data`) | row 1, column 3 | `0x0017ED50` (`0x0017EEE9`) | `0x00217150` (`0x00217190`) |
| `0x01F7F570` | `f32` | 0 (zero-filled tail of `.data`) | row 2, column 0 | `0x0017ED50` (`0x0017EE4C`) | `0x00217150` (`0x00217182`, `0x0021728F`, `0x00217329`, `0x002173E6`) |
| `0x01F7F574` | `f32` | 0 (zero-filled tail of `.data`) | row 2, column 1 | `0x0017ED50` (`0x0017EEA6`) | `0x00217150` (`0x002171E3`, `0x0021737B`, `0x0021740A`) |
| `0x01F7F578` | `f32` | 0 (zero-filled tail of `.data`) | row 2, column 2 | `0x0017ED50` (`0x0017EE9B`) | `0x00217150` (`0x002171BB`, `0x00217428`) |
| `0x01F7F57C` | `f32` | 0 (zero-filled tail of `.data`) | row 2, column 3 | `0x0017ED50` (`0x0017EEF1`) | `0x00217150` (`0x0021719A`, `0x00217432`) |
| `0x01F7F580` | `f32` | 0 (zero-filled tail of `.data`) | row 3, column 0 | `0x0017ED50` (`0x0017EEC1`) | `0x00217150` (`0x0021744C`) |
| `0x01F7F584` | `f32` | 0 (zero-filled tail of `.data`) | row 3, column 1 | `0x0017ED50` (`0x0017EEF9`) | `0x00217150` (`0x00217454`) |
| `0x01F7F588` | `f32` | 0 (zero-filled tail of `.data`) | row 3, column 2 | `0x0017ED50` (`0x0017EF01`) | `0x00217150` (`0x00217459`) |
| `0x01F7F58C` | `f32` | 0 (zero-filled tail of `.data`) | row 3, column 3 | `0x0017ED50` (`0x0017EED9`) | `0x00217150` (`0x0021745E`) |

### The scene colour's green channel

The scene colour is four floats, red, green, blue and alpha. `0x003769E0`, from the draw `0x0022B0B0` (`0x0022B278`),
copies it to `0x0209A380`, the scene colour of the map ambient
([how a character is lit](character-lighting-and-shadows.md)).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x020926C4` | `f32` | 0 (zero-filled tail of `.data`) | green: 1.0 from each frame's draw set-up, then scaled by type `0xD0` elements and by the flare dimming | `0x0024D540` (`0x0024D721`) and `0x0024DA40` (`0x0024DA52`), which it calls: 1.0 with the whole colour; `0x00465690` (`0x0046578F`): the whole colour scaled; `0x00376AC0` (`0x00376B1B`) and `0x00376BE0` (`0x00376CA6`): times `f` | `0x003769E0` (`0x003769E0`), with the whole colour; `0x00465690` (`0x00465784`); `0x00376AC0` (`0x00376ADB`); `0x00376BE0` (`0x00376C6F`) |

### The slots' fields

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [lens-flares-state.tsv](lens-flares-state.tsv): the handle of slots 1 to 7, and the four frozen copies and the flags of all eight slots | the row's `type` | 0 (zero-filled tail of `.data`) | the row's `meaning`, for the slot and field it names | the row's `set_by`: `0x00376350`, `0x00376990` and `0x00376A80` for a handle, `0x00376D80` for a frozen copy | the row's `read_by`: the handle checks of every accessor, and `0x00376BE0` for a frozen copy |

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
