---
title: "Bone trails: the ribbon trails drawn behind weapon bones, from the model descriptor to the triangle strip"
kind: "system"
category: "Graphics"
addresses: "0x00520160, 0x00425E70, 0x003E6770, 0x0042F250, 0x02CA8420, 0x0051C270, 0x0051CC30, 0x0051CC10, 0x0051BC10, 0x0051CDC0, 0x0051C380, 0x0051C3C0, 0x0051BC70, 0x00422170, 0x003711D0, 0x005409C0, 0x0053F490, 0x003A35E0, 0x01F2A220"
---

## What the player sees

A swung weapon leaves a short coloured ribbon that follows the blade and fades toward its tail. A few summons and one
monster have trails on other bones. A trail fades in over two frames when a scene's command turns it on and fades
out over five when it turns off, and it fades with its character.

## How it works

### The descriptor

A model asks for trails in its model block, the block a render record holds at `+0x400`. `0x003E6770` finds the trail
section through the block's offset word `+8`, reads a `u32` count, caps it at four, and walks `0x50`-byte descriptors
from section `+0x10`. The descriptor is copied whole into the trail entry at `+0x370`:

| Descriptor | Entry | Use |
|---|---|---|
| `+0x00` u8 | `+0x370` | non-zero binds an image stored after the descriptors (`0x003E6D80`) instead of the engine's own |
| `+0x02` u16 | `+0x372` | the bone sampled |
| `+0x04` u32 | `+0x374` | written by `0x003E6770`: the owning render-record index |
| `+0x08` f32 | `+0x378` | uploaded to the program |
| `+0x0C` f32 | `+0x37C` | copied to entry `+0x14` each update and uploaded |
| `+0x10` u32[16] | `+0x380` | four colours of four components, uploaded |

### Switching trails on and off

- Authored presentation command `0x11` of the bank `0x0041D6C0` registers (`0x00520160`) stores the command's byte `+2` in
  render record `+0x3D0` and sets bit 24 of `+0x294` ([Authored presentation commands](authored-presentation-commands.md)).
- The record pass `0x00427DE0` sees bit 24 (`0x0042858C`) and calls `0x00425E70(record, byte +0x3D0)`, which runs `0x003E6770`
  on the record, its first child and the child's two subtrees. A command addressed to a character reaches the weapon in
  its hand this way.
- On: when the record's first trail handle `+0x438` is `0xFFFF`, `0x003E6770` creates one entry per descriptor
  (`0x0051CC30`) and stores the handles at `+0x438`-`+0x444`. Otherwise it creates nothing.
- Off: it calls `0x0051CC10` for each handle that is not `0xFFFF` and stores nothing, so the handles stay in place. A
  stale handle is harmless: every pool routine compares it with the entry's own `+0`.
- `0x0042F250(record index)` is a second off path: it clears bits 18 and 19 of `+0x290`, sets bit 20 and calls
  `0x003E6770(record, 0)`.

`0x0051CC10` only clears the entry's on byte `+4`; the entry keeps updating and drawing while it fades and frees itself at
zero. `0x0051BC10` frees an entry at once. `0x0051CDC0` stores the character's opacity in `+8`, and `0x0051C380`, called from
`0x004213E0`, writes the two flag bits of byte `+5`.

`0x003E70F0(record, v)`, from `0x0042CBF0` and `0x0042D050`, passes the opacity to each of the record's
four handles that is not `0xFFFF` (`0x0051CDC0`). `0x003E74C0(record)` frees each such entry at once
(`0x0051BC10`) and sets its handle to `0xFFFF`; `0x003E6890` broadcasts it over the record tree
(`0x00425F40` with 0).

### The pool

`0x0051C270` allocates `0x3C00` bytes, sixteen entries of `0x3C0`, at `[0x02CA8420]`, clears every handle and zeroes the
header: live count `0x02CA8400`, flag byte `0x02CA8402`, serial `0x02CA8404`, list head `0x02CA8408` and tail `0x02CA8410`. It
builds the parameter template at `0x02CA8A90` (`0x005409C0`) and binds the engine's trail image from `0x01F2A220`.

`0x0051CC30` takes the first entry whose handle is 0; with none free it returns 0 and the trail is not made. It sets the
handle to `serial << 8 | slot` (the serial wraps to 1 above `0xFFFFFF`), on = 1, opacity 1.0, `+0xC` = 20.0, fade 0,
copies the descriptor, clears the histories, takes the first sample and appends the entry to the list.

### Sampling a bone

`0x00422170(record, bone, base out, tip out)` resolves the record's model instance and calls `0x003711D0`, or `0x003712C0`
when the instance's first byte has bit 7. `0x003711D0` refuses a bone at or past the skeleton's count, copies the bone's
world position (`+0xB0` of its `0x290`-byte runtime record) as the base, and builds the tip by putting `(length, 0, 0, 1)`
through the bone's matrix at `+0x80`.

The runtime records are the block the instance handle `+0x84` resolves to
(`0x00371227`-`0x00371239`); `length` is the float at `+0x74 + 0x4C × n` of the other block, the one handle `+0xA0` resolves to
(`0x003711EB`-`0x00371215`), with `n` the word `+0x27E` of the bone's runtime record (`0x0037123C`-`0x00371276`). A trail runs
along the bone's x axis for that length.

### The update

`0x0051C3C0` walks the list once a frame. For each entry:

1. It skips the entry when bit 0 of `entry +5 | 0x02CA8402` is set.
2. When the alternator `+7` is set or `0x001EDDA0` returns 1, the sample count rises to at most 16 and the three
   histories shift down one slot. `0x001EDDA0` returns 0 only while the 60 fps flag `0x01F82E38` is set and `0x01DFE0C0` is 0,
   so at 30 fps the histories shift every frame and at 60 fps every second frame. The alternator flips every update.
3. It samples slot 0 again when the owner record is live.
4. It measures how far the tip and the base moved since the last sample, and the angle between the blade directions
   now and one sample ago (`0x0046F460`, an arccosine table), stored at `+0x330`.
5. It stores a unit direction in direction slot 0: from the tip toward half-way back along its last step, displaced by
   that step turned a quarter turn about the swing axis (`0x00202E10`) and scaled to `0.2 × tip distance × angle`.
6. Tip `w` = `max(tip distance, 0.8 × angle × tip distance)`, and the same for the base. When the count is exactly 2
   these are copied into slot 1.
7. While on, the fade `+0x10` rises by `0.5 × [0x01DFE0BC]` to 1.0. While off it falls by `0.2 × [0x01DFE0BC]`, and at zero
   the entry frees itself.

### The draw

The render root's model pass `0x0041E4D0` ends by calling `0x0051BC70`. It first draws effect layer 3, the one the effect
system names `TsEffMan_Layer_AfterOBJ` (`0x00258EE0(3)`, [Effect element runtime](effect-element-runtime.md)), binds the
trail image and palette, and copies the `0x4A0`-byte template. For each listed entry it:

- skips it when bit 1 of `entry +5 | 0x02CA8402` is set, when it holds fewer than two samples, or when its opacity `+8` is
  not above 0;
- binds the model's own image when descriptor byte `+0` is set;
- copies the three histories and a parameter block into the template: `0x20`, the sample count, `+0x14`,
  fade × opacity, descriptor float `+8`, the four colours and the four rows of the matrix at `0x02AEDDB0`;
- registers a render command with a `0x488`-byte payload, the template from `+0x18`, and the VU1 program `0x0053F490`
  through `0x003A35E0` ([PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md)).

### The strip

`0x005409C0` writes the template as a VIF1 packet: BASE and OFFSET at `+0x08` and `+0x0C`, STCYCL at `+0x18`, an UNPACK
of `0x45` quadwords to VU address 0 at `+0x1C`, MSCALF at `+0x470` that calls the program, and a DIRECT at `+0x47C`. The
first quadword it uploads, at template `+0x20`, is a GIF tag: `0x00008000`, `0x602E4000`, `0x00412412`, `0x00008000`.

| Field | Value |
|---|---|
| EOP | 1 |
| PRE, PRIM | 1, `0x05C`: triangle strip, Gouraud, textured, alpha-blended |
| FLG | 0, packed |
| NREG | 6 |
| REGS | ST, RGBAQ, XYZF2, ST, RGBAQ, XYZF2 |

The program reads VU cell 0 through the bank cell `0x02064B0C`, which the image only reads, and after its main loop
writes the tag back with NLOOP set to the number of samples it emitted (`0x00540905`-`0x00540955`). Each sample is two
vertices, the base and the tip, each as ST, RGBAQ and XYZF2. The loop's trip count is the sample count in the
uploaded parameter block (`0x0053F995`).

## Layouts

Trail entry, [`0x02CA8420`] + slot × `0x3C0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` | handle | serial << 8 \| slot, 0 = free |
| `+0x004` | `u8` | on |  |
| `+0x005` | `u8` | flags | bit 0 do not update, bit 1 do not draw |
| `+0x006` | `u8` | samples | 1 to 16 |
| `+0x007` | `u8` | alternator |  |
| `+0x008` | `f32` | opacity | the character's |
| `+0x00C` | `f32` | init20 | 20.0 at create |
| `+0x010` | `f32` | fade |  |
| `+0x014` | `f32` | param14 | descriptor +`0x0C` |
| `+0x018` | `void*` | prev |  |
| `+0x020` | `void*` | next |  |
| `+0x030` | `f32[16][4]` | tip | w = tip speed figure |
| `+0x130` | `f32[16][4]` | base | w = base speed figure |
| `+0x230` | `f32[20][4]` | direction |  |
| `+0x330` | `f32` | angle |  |
| `+0x334` | `f32` | angle2 | the angle when the second sample arrived |
| `+0x370` | `0x50` | descriptor |  |

Trail image, `0x01F2A220`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x02` | `u16` | pixels | offset of the 64 × 64 eight-bit pixels |
| `+0x04` | `u16` | palette | offset of the 256-entry palette after the pixels |
| `+0x0B` | `u8` | logW | 6 |
| `+0x0C` | `u8` | logH | 6 |

## Shipped data

Measured over the 1,066 `.cm` models in the archive; the model block is the `@FCP` chunk's payload.

| Fact | Value |
|---|---|
| models with a trail section | 216 of 1,066 |
| trails per model | 1 in 199, 2 in 14, 3 in 1, 4 in 2; 238 in all, none over four |
| by folder | weapon 202 models (218 trails), gadget 9, summon 4 (10), monster 1 |
| bones | 2 in 202 trails, 3 in 20, 4 in 3, 0 and 20 in 2 each, 41-44 in 2 each, 54 in 1 |
| own-image byte, word `+4` | 0 in all 238 |
| float `+8` | 1.0 in all 238 |
| float `+0xC` | 2.0 in 235; 2.4, 2.6 and 3.0 once each |
| colours | values 0 to 255; 14 distinct sets of four colours; the first two `(96, 96, 96, 32)`, `(192, 254, 255, 70)` in 179 and 180 trails |
| colour alpha | the third and fourth colours have alpha 0 in 236 trails |
| pool | 16 entries; the image 64 × 64 with a 256-entry palette |

## State

- `[0x02CA8420]`: the sixteen entries; `0x02CA8400`-`0x02CA8410` the header.
- `0x02CA8A90`: the parameter template.
- Render record `+0x438`-`+0x444`: the owner's four handles; `+0x3D0` the commanded state.

## Modding notes

- `0x003E6770` finds the trail section with a 32-bit sum of the model block and its offset, so a model
  block must sit below 4 GB.

- A trail's length and direction come from the bone's length entry and x axis; the descriptor only picks the bone.
- At most sixteen trails exist at once; a request beyond that makes nothing.
- The trail's alpha is fade × the character's opacity, so a fading character takes its trail with it.
- The four colour groups are integers on the 0-255 scale, uploaded as they are.

## Related

- [Authored presentation commands](authored-presentation-commands.md): command `0x11`.
- [Model files](model-files-cm-ca.md): the model block that carries the trail section.
- [Character fades](character-fades.md): the opacity `0x0051CDC0` stores.
- [Effect element runtime](effect-element-runtime.md): display layer 3, drawn just before the trails.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the packet interpreter and the
  recompiled programs.
