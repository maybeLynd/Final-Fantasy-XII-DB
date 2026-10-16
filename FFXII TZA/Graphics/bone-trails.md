---
title: "Bone trails: the ribbon trails drawn behind weapon bones, from the model descriptor to the triangle strip"
kind: "system"
category: "Graphics"
addresses: "00520160, 00425E70, 003E6770, 0042F250, 02CA8420, 0051C270, 0051CC30, 0051CC10, 0051BC10, 0051CDC0, 0051C380, 0051C3C0, 0051BC70, 00422170, 003711D0, 005409C0, 0053F490, 003A35E0, 01F2A220"
---

## What the player sees

A swung weapon leaves a short coloured ribbon that follows the blade and fades toward its tail. A few summons and one
monster have trails on other bones. A trail fades in over two frames when a scene's command turns it on and fades
out over five when it turns off, and it fades with its character.

## How it works

### The descriptor

A model asks for trails in its model block, the block a render record holds at `+400`<sub>h</sub>. `003E6770` finds the trail
section through the block's offset word `+8`, reads a `u32` count, caps it at four, and walks `50`<sub>h</sub>-byte descriptors
from section `+10`<sub>h</sub>. The descriptor is copied whole into the trail entry at `+370`<sub>h</sub>:

| Descriptor | Entry | Use |
|---|---|---|
| `+00`<sub>h</sub> u8 | `+370`<sub>h</sub> | non-zero binds an image stored after the descriptors (`003E6D80`) instead of the engine's own |
| `+02`<sub>h</sub> u16 | `+372`<sub>h</sub> | the bone sampled |
| `+04`<sub>h</sub> u32 | `+374`<sub>h</sub> | written by `003E6770`: the owning render-record index |
| `+08`<sub>h</sub> f32 | `+378`<sub>h</sub> | uploaded to the program |
| `+0C`<sub>h</sub> f32 | `+37C`<sub>h</sub> | copied to entry `+14`<sub>h</sub> each update and uploaded |
| `+10`<sub>h</sub> u32[16] | `+380`<sub>h</sub> | four colours of four components, uploaded |

### Switching trails on and off

- Authored presentation command `11`<sub>h</sub> of the bank `0041D6C0` registers (`00520160`) stores the command's byte `+2` in
  render record `+3D0`<sub>h</sub> and sets bit 24 of `+294`<sub>h</sub> ([Authored presentation commands](authored-presentation-commands.md)).
- The record pass `00427DE0` sees bit 24 (`0042858C`) and calls `00425E70(record, byte +3D0h)`, which runs `003E6770`
  on the record, its first child and the child's two subtrees. A command addressed to a character reaches the weapon in
  its hand this way.
- On: when the record's first trail handle `+438`<sub>h</sub> is `FFFF`<sub>h</sub>, `003E6770` creates one entry per descriptor
  (`0051CC30`) and stores the handles at `+438`<sub>h</sub>-`+444`<sub>h</sub>. Otherwise it creates nothing.
- Off: it calls `0051CC10` for each handle that is not `FFFF`<sub>h</sub> and stores nothing, so the handles stay in place. A
  stale handle is harmless: every pool routine compares it with the entry's own `+0`.
- `0042F250(record index)` is a second off path: it clears bits 18 and 19 of `+290`<sub>h</sub>, sets bit 20 and calls
  `003E6770(record, 0)`.

`0051CC10` only clears the entry's on byte `+4`; the entry keeps updating and drawing while it fades and frees itself at
zero. `0051BC10` frees an entry at once. `0051CDC0` stores the character's opacity in `+8`, and `0051C380`, called from
`004213E0`, writes the two flag bits of byte `+5`.

`003E70F0(record, v)`, from `0042CBF0` and `0042D050`, passes the opacity to each of the record's
four handles that is not `FFFF`<sub>h</sub> (`0051CDC0`). `003E74C0(record)` frees each such entry at once
(`0051BC10`) and sets its handle to `FFFF`<sub>h</sub>; `003E6890` broadcasts it over the record tree
(`00425F40` with 0).

### The pool

`0051C270` allocates `3C00`<sub>h</sub> bytes, sixteen entries of `3C0`<sub>h</sub>, at `[02CA8420]`, clears every handle and zeroes the
header: live count `02CA8400`, flag byte `02CA8402`, serial `02CA8404`, list head `02CA8408` and tail `02CA8410`. It
builds the parameter template at `02CA8A90` (`005409C0`) and binds the engine's trail image from `01F2A220`.

`0051CC30` takes the first entry whose handle is 0; with none free it returns 0 and the trail is not made. It sets the
handle to `serial << 8 | slot` (the serial wraps to 1 above `FFFFFF`<sub>h</sub>), on = 1, opacity 1.0, `+C`<sub>h</sub> = 20.0, fade 0,
copies the descriptor, clears the histories, takes the first sample and appends the entry to the list.

### Sampling a bone

`00422170(record, bone, base out, tip out)` resolves the record's model instance and calls `003711D0`, or `003712C0`
when the instance's first byte has bit 7. `003711D0` refuses a bone at or past the skeleton's count, copies the bone's
world position (`+B0`<sub>h</sub> of its `290`<sub>h</sub>-byte runtime record) as the base, and builds the tip by putting `(length, 0, 0, 1)`
through the bone's matrix at `+80`<sub>h</sub>, with `length` the float `+74`<sub>h</sub> of the bone's `4C`<sub>h</sub>-byte definition. A trail runs
along the bone's x axis for the bone's authored length.

### The update

`0051C3C0` walks the list once a frame. For each entry:

1. It skips the entry when bit 0 of `entry +5 | 02CA8402` is set.
2. When the alternator `+7` is set or `001EDDA0` returns 1, the sample count rises to at most 16 and the three
   histories shift down one slot. `001EDDA0` returns 0 only while the 60 fps flag `01F82E38` is set and `01DFE0C0` is 0,
   so at 30 fps the histories shift every frame and at 60 fps every second frame. The alternator flips every update.
3. It samples slot 0 again when the owner record is live.
4. It measures how far the tip and the base moved since the last sample, and the angle between the blade directions
   now and one sample ago (`0046F460`, an arccosine table), stored at `+330`<sub>h</sub>.
5. It stores a unit direction in direction slot 0: from the tip toward half-way back along its last step, displaced by
   that step turned a quarter turn about the swing axis (`00202E10`) and scaled to `0.2 × tip distance × angle`.
6. Tip `w` = `max(tip distance, 0.8 × angle × tip distance)`, and the same for the base. When the count is exactly 2
   these are copied into slot 1.
7. While on, the fade `+10`<sub>h</sub> rises by `0.5 × [01DFE0BC]` to 1.0. While off it falls by `0.2 × [01DFE0BC]`, and at zero
   the entry frees itself.

### The draw

The render root's model pass `0041E4D0` ends by calling `0051BC70`. It first draws effect layer 3, the one the effect
system names `TsEffMan_Layer_AfterOBJ` (`00258EE0(3)`, [Effect element runtime](effect-element-runtime.md)), binds the
trail image and palette, and copies the `4A0`<sub>h</sub>-byte template. For each listed entry it:

- skips it when bit 1 of `entry +5 | 02CA8402` is set, when it holds fewer than two samples, or when its opacity `+8` is
  not above 0;
- binds the model's own image when descriptor byte `+0` is set;
- copies the three histories and a parameter block into the template: `20`<sub>h</sub>, the sample count, `+14`<sub>h</sub>,
  fade × opacity, descriptor float `+8`, the four colours and the four rows of the matrix at `02AEDDB0`;
- registers a render command with a `488`<sub>h</sub>-byte payload, the template from `+18`<sub>h</sub>, and the VU1 program `0053F490`
  through `003A35E0` ([PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md)).

### The strip

`005409C0` writes the template as a VIF1 packet: BASE and OFFSET at `+08`<sub>h</sub> and `+0C`<sub>h</sub>, STCYCL at `+18`<sub>h</sub>, an UNPACK
of `45`<sub>h</sub> quadwords to VU address 0 at `+1C`<sub>h</sub>, MSCALF at `+470`<sub>h</sub> that calls the program, and a DIRECT at `+47C`<sub>h</sub>. The
first quadword it uploads, at template `+20`<sub>h</sub>, is a GIF tag: `00008000`<sub>h</sub>, `602E4000`<sub>h</sub>, `00412412`<sub>h</sub>, `00008000`<sub>h</sub>.

| Field | Value |
|---|---|
| EOP | 1 |
| PRE, PRIM | 1, `05C`<sub>h</sub>: triangle strip, Gouraud, textured, alpha-blended |
| FLG | 0, packed |
| NREG | 6 |
| REGS | ST, RGBAQ, XYZF2, ST, RGBAQ, XYZF2 |

The program reads VU cell 0 through the bank cell `02064B0C`, which the image only reads, and after its main loop
writes the tag back with NLOOP set to the number of samples it emitted (`00540905`-`00540955`). Each sample is two
vertices, the base and the tip, each as ST, RGBAQ and XYZF2. The loop's trip count is the sample count in the
uploaded parameter block (`0053F995`).

## Layouts

Trail entry, [`02CA8420`] + slot × `3C0`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u32` | handle | serial << 8 \| slot, 0 = free |
| `004`<sub>h</sub> | `u8` | on |  |
| `005`<sub>h</sub> | `u8` | flags | bit 0 do not update, bit 1 do not draw |
| `006`<sub>h</sub> | `u8` | samples | 1 to 16 |
| `007`<sub>h</sub> | `u8` | alternator |  |
| `008`<sub>h</sub> | `f32` | opacity | the character's |
| `00C`<sub>h</sub> | `f32` | init20 | 20.0 at create |
| `010`<sub>h</sub> | `f32` | fade |  |
| `014`<sub>h</sub> | `f32` | param14 | descriptor +`0C`<sub>h</sub> |
| `018`<sub>h</sub> | `void*` | prev |  |
| `020`<sub>h</sub> | `void*` | next |  |
| `030`<sub>h</sub> | `f32[16][4]` | tip | w = tip speed figure |
| `130`<sub>h</sub> | `f32[16][4]` | base | w = base speed figure |
| `230`<sub>h</sub> | `f32[20][4]` | direction |  |
| `330`<sub>h</sub> | `f32` | angle |  |
| `334`<sub>h</sub> | `f32` | angle2 | the angle when the second sample arrived |
| `370`<sub>h</sub> | `50`<sub>h</sub> | descriptor |  |

Trail image, `01F2A220`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `02`<sub>h</sub> | `u16` | pixels | offset of the 64 × 64 eight-bit pixels |
| `04`<sub>h</sub> | `u16` | palette | offset of the 256-entry palette after the pixels |
| `0B`<sub>h</sub> | `u8` | logW | 6 |
| `0C`<sub>h</sub> | `u8` | logH | 6 |

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
| float `+C`<sub>h</sub> | 2.0 in 235; 2.4, 2.6 and 3.0 once each |
| colours | values 0 to 255; 14 distinct sets of four colours; the first two `(96, 96, 96, 32)`, `(192, 254, 255, 70)` in 179 and 180 trails |
| colour alpha | the third and fourth colours have alpha 0 in 236 trails |
| pool | 16 entries; the image 64 × 64 with a 256-entry palette |

## State

- `[02CA8420]`: the sixteen entries; `02CA8400`-`02CA8410` the header.
- `02CA8A90`: the parameter template.
- Render record `+438`<sub>h</sub>-`+444`<sub>h</sub>: the owner's four handles; `+3D0`<sub>h</sub> the commanded state.

## Modding notes

- `003E6770` finds the trail section with a 32-bit sum of the model block and its offset, so a model
  block must sit below 4 GB.

- A trail's length and direction come from the bone's definition and x axis; the descriptor only picks the bone.
- At most sixteen trails exist at once; a request beyond that makes nothing.
- The trail's alpha is fade × the character's opacity, so a fading character takes its trail with it.
- The four colour groups are integers on the 0-255 scale, uploaded as they are.

## Related

- [Authored presentation commands](authored-presentation-commands.md): command `11`<sub>h</sub>.
- [Model files](model-files-cm-ca.md): the model block that carries the trail section.
- [Character fades](character-fades.md): the opacity `0051CDC0` stores.
- [Effect element runtime](effect-element-runtime.md): display layer 3, drawn just before the trails.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the packet interpreter and the
  recompiled programs.
