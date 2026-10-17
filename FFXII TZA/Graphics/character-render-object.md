---
title: "CharacterRenderObject: the per-character draw object, its model instances, shader bindings and the transform publish"
kind: "system"
category: "Graphics"
addresses: "00903B68, 001F4DA0, 001F52F0, 001F51E0, 001F6E70, 001F6D60, 001F89E0, 001F7790, 0018D240, 001FB120, 001FAD50, 001F9A80, 001FA3D0, 001F9B20, 001FA1A0, 001FAA10, 001FA820, 001F6E50, 001F86D0, 001BD4A0, 001BD840, 001BDAB0, 01F81248, 0017F0D0, 0017F100, 0017EFC0, 003703A0, 0053AB50, 0053D780, 00504700, 00477F20, 004780C0, 005049E0, 003E55B0, 00189120, 01F7F598, 001F5D70"
---

## What the player sees

A character on screen is two things: a render record that decides what it looks like this frame
([character render records](character-render-records.md)), and a CharacterRenderObject that turns
that into draw calls. The object holds the character's shader parameters: its six lights and ambient,
its fog colour, its refraction, its shadow settings, its bone matrices and the PS2-style z-bias and
projection matrices the shaders were written around. A model can exist before its object is ready;
until setup ends the object draws nothing.

## How it works

### Getting and returning an object

A record keeps its object key at `+0x6B0` and the object at `+0x6B8`. The manager is the object at
`[01F81248]` (`001BDAB0`).

- `0017F0D0(key)` asks the manager for an object through `001BD4A0`, once `0017EFC0(key)` reports the
  key's model as registered. Its callers are `003703A0` (the skeleton-entry update) and `0053AB50`
  (the record's draw), each storing the result in the record's `+0x6B8`.

- `0017EFC0(key)` asks the model asset cache (`001BC000`) through `001BB040(cache, key)`: the key
  must have a model in the cache's map at `+0xB8` whose asset list is ready (`001BB120`, which then
  binds the model's palette textures), and a model with byte `+0x98` set also needs its companion
  `-2 - key` to pass the same test.

- `001BD4A0(manager, key)` looks the model description up (`001BAFF0`) and checks a cache of parked
  objects keyed by the description's `+0x2A0`. With no parked object it allocates `0x668` bytes,
  constructs (`001F4DA0`) and runs setup (vtable slot 2). With one it takes it out of the cache and
  resets it (`001F89E0`). Either way the object is appended to the manager's live list.
- `0017F100(object)` returns it: `001BD840` removes it from the live list and parks it in the cache under
  its model key (`001F6E60`, the description's `+0x2A0`). The record's teardown `004200A0` calls it and
  clears `+0x6B8`.
- When the record has a parent with an object, `0053AB50` attaches the two through `0017EF60` →
  `001BD630`, with a per-bone map at record `+0x6D0`.

- `001BD630` reads, for the bone names of both objects, each name's number with `001F6E00` (the
  decimal digits before the first `_`, 0 for a name that starts with `_`) and the text after that
  `_` (`strstr`), and compares the texts character by character.

### The ready byte

The constructor clears `+0x4B4`; setup sets it to 1 at its end (`001F7729`) and nothing clears it
again. Slots 3, 8, 9, 13, 24 and 30, the bank copy `001FAD50` and the draw `001F5D70` do nothing while it
is 0; slot 16 reads it per part. `001F89E0(object, key)`, the reset used on reuse, writes the key to
`+0x480` and, only for a ready object, restores the per-frame defaults (`+0x4A8` and `+0x4AC` at 1.0,
`+0x4B5`/`+0x4B6` at 1, the output vectors at `+0x3C0` and `+0x3D0`).

### Setup

Slot 2, `001F6E70(object, key, description)`:

1. stores the key at `+0x480`, creates the companion at `+0x28` (`001F5B80(01F82F10)`, which points
   back at the object), and sets `+0x499` when the key is one of six in the table at `01DFE1B0`;
2. stores the description at `+0x488`, and for a key of 0 or more the companion model `-2 - key` at
   `+0x490`;
3. binds the companion model's meshes into the template record embedded at `+0x78` through the binder
   `001F7790`, then appends one `0x318` record per mesh of the model to the vector at `+0x58`, binding
   it by name or copying an existing record for the same parameter set;
4. sets `+0x4B4` and calls `001BD7D0` on the manager.

### The shader binding record

`001F7790(…, shader, block, record, template)` fills a `0x318`-byte record. Without a template it
looks up 98 parameter names in the shader (`0018D240`) and stores 92 of the results as descriptor
pointers from `+0x30`; with one it copies the template.

It then writes defaults into the parameter block: `sunIndex` -1, `fresnelRefEnabled` and `eCameraLightEnabled` 1, `PS2ZBiasEnabled`,
`PS2ZBiasOriginal`, `PS2ZBiasInstance` and `paletteEnabled` 0, among others. A descriptor's word
`+0x10` is the byte offset into the block and `+0x12 & 0x1FFF` its size; every write checks it fits.
The offset of each name is in [the binding table](character-render-object-shader-binding-record-0x318-slots.tsv).

### The z-bias and matrix publish

Slot 13, `001FB120(object, part, flag, a, b, m1, m2, m3)`, is called by slot 16 for every part with
`flag` 1. It writes two parameters at once: `PS2ZBiasEnabled` = 1 unless `a` and `b` are both 0, and
`PS2ZBiasNoGS` = (`flag` == 0). The rest goes into one of two banks, chosen by byte `+0x1C` of the
object at `[01F7F598]` (`00189120`):

| | Bank A (byte 0) | Bank B (byte non-zero) |
|---|---|---|
| `a`, `b` | part record `+0x08`, `+0x10` | part record `+0x0C`, `+0x14` |
| three 64-byte matrices | object `+0x4C4`..`+0x583` | object `+0x584`..`+0x643` |
| fog colour (slot 9) | object `+0x644`..`+0x653` | object `+0x654`..`+0x663` |

`001FAD50(object, part)`, called per part by the draw `001F5D70`, reads the bank chosen by byte `+0x1D`
of the same object and writes `PS2ZBiasOriginal` = `a`, `PS2ZBiasInstance` = `b`, the three matrices to
`PS2WHMatrix`, `PS2HSMatrix` and `InvPS2WHSMatrix`, and the fog colour to `PS2FogVec`. Slot 9
(`001F9A80`) takes the fog colour as 0..255 values and stores each channel divided by 255, alpha
clamped to 0..1.

### The draw

`0053AB50` draws a record's model. It runs the object's methods through one-line wrappers: slot 1
(`0017F0B0`), slot 8 with the light block `02CA8110` (`0017F1C0`), slot 9 (`0017F180`), slot 21 with
record `+0x284` bit 12 (`0017F220`), slots 22, 23, 24, 15, slot 26 with the record's matrices at
`+0x6C0` (`0017F260`), slot 12, slot 17, slot 6, and slot 16 (`0017F210`). Slot 8 is described on
[character lighting and shadows](character-lighting-and-shadows.md).

Slot 16, `001FA3D0`, builds the draw list. For each mesh instance in the vector at `+0x30` and each
part descriptor (32 bytes) whose two id bytes and `+0x49C` match a mesh, it picks a technique table by
the part's kind byte (`01DFE1D0`, `01DFE2F0`, or `ChrOpaque` for kinds above `0x10`), switches to the
`01F83020` / `01F83040` set while `+0x4A8` is below 0.75, then calls slots 19, 20 (kinds 2, 5, 10, 13),
10 and 13 for the part, and hands the list to `0060E960`.

The slot-24 call in `0053AB50` goes through the null-safe wrapper `0017F200`, and `0017F250` calls
slot 18, `001FAFB0`, the same way for the texture-rectangle copy `00477B10`. Slot 18 appends a `0x24`-byte element (two bytes and four 8-byte values) to the vector
at `+0x390`.

### The ordered draw

`CharacterOrderedObject`'s execute reaches `001F5D70(object, …)`. For an object with a key, unless
the key's resource entry (`002E98F0`, `002DF980`) has byte `+0x16` = `'h'` or the key is
`0x6E006D`, it files block `0x25` with 1 (`0060E810`), publishes two shadow values with
`001FB310` and runs slot 30 on its part records:

- `001FB310` writes `+0x4B8` to the shadow object's `+0x4C` and `+0x50` = 2.3 (`01DFE408`) ×
  `+0x4BC` (`001F0850`), the values slot 30 hands to `m_chrObjHeight` and
  `m_chrObjFlyingHeight`, and copies `+0x4C0` to `02CB83B0`.
- With no single mesh at `+0x50` slot 30 runs on the vector `+0x58`. With one, the template record
  `+0x78` is copied into a one-record vector (`001F87B0`), slot 30 runs on it, the mesh is drawn
  (`0060B980`) and the render manager's counter goes up by 1 (`00185A80`).

At the end of the mesh walk, while byte `+0xF8` of the manager `001BDAB0()` is set, `001F68E0`
draws the skeleton: for each mesh instance it builds one line per bone, from the bone's position
(row `+0x30` of its `0x40`-byte matrix) to its parent's, the parent index read from the mesh's
`+0x58` table. It reserves a render-thread callback (`005FEB30`) for `001F5C20`, which draws the
lines 512 at a time (`006215A0`, mode 1) between `00628570(ctx, 0, 1)` and `00628570(ctx, 1)`.

The teardown, slot 3 (`001F6D60`), empties the mesh instances through `001F86F0`: each instance of
`+0x30` and the single one at `+0x50` goes through `001EEEF0` and leaves the object's cluster
`+0x3E0` through `001EEC30`, a null-safe `0063ABF0(cluster, instance)`. Its twin `001EEC50(record)`, reached
only by a tail-jump from the deferred call `001B6C30` ([Render command list](render-command-list.md)), returns on a
null record and otherwise calls `0063ABF0([01F82E50], record +0x00)`, or `0063ABF0([01F82E50], 0)` when byte
`+0x08` is set (`001EEC50`-`001EEC73`).

### The bone palette

Slot 26, `001FAA10(object, palette)`, reads each mesh's bone names: the decimal digits before the
first `_` give the palette index. It copies that 64-byte matrix into the mesh's bone matrix with the
first two components of every row negated and the last component forced to 1.0. It does the same for
the single mesh at `+0x50`, and does not test `+0x4B4`.

### Refraction and shadow parameters

- Slot 24, `001FA1A0(object, enable, power, alpha, mode)`, sets `refractionEnabled` (1.0 or 0),
  `refractionPower`, `refractionAlpha` and `RefractionSampler` in every part record, and keeps `mode` at
  `+0x664`.
- Slot 30, `001FA820`, writes `iDebugMode`, `mSpecialShadowFlag` (from `+0x4B0`, set by slot 25),
  `m_chrObjHeight`, `m_chrObjFlyingHeight`, `g_txShadow` and `g_txChrAlpha` from the shadow object
  `001F0850` ([graphics settings](../Engine-Core/graphics-settings.md)).

### Render model instances

The root's `+0xDA0` bank holds the `0x260`-byte render model instances, 160 slots, taken by
`004780C0` and reset by `005049E0`. A record's `+0x64` names its instance (`003E55B0`).

Before the instances, `0041E4D0` runs `004FDD90`, which calls `004FDDA0`. That function copies
the camera matrices `02AEDE70`-`02AEDEAF` and `02AEDD30`-`02AEDD6F` to `02CA7F80` and writes three records into the
current GS command buffer (`005044B0`, closing a full block with `00504450`):

1. a header holding `[02EBA404]`;
2. an A+D GIF tag of 19 register writes, among them XYOFFSET_1 and _2 (`0x18`, `0x19`) = `(0x1000 - w) x 8`,
   `(0x1000 - h) x 8` and SCISSOR_1 and _2 (`0x40`, `0x41`) = 0 to `w - 1`, 0 to `h - 1`, for the GS frame `w`
   `022D8EAC` and `h` `022D8EB4`;
3. a copy of the 0x150-byte block `02EBA400` with the matrices at `+0x10` and `+0x50`, the vector `02AEDF10` at
   `+0xE0` (kept at `02EBA4B0`), and 1791.97 and 1823.97 at `+0xA0` and `+0xA4`.

At boot `00475310` (`0036F4FC`) fills part of that block: `+0xC4` 10.0, `+0xC8` 150.0, `+0xCC` 1.5, `+0xE0` 16.0,
`+0xE4` and `+0xE8` 4.0, `+0xD4` 5, `+0xD8` `0x40`, and 0 in `+0xC0` and `+0xD0`.

`0041E4D0` draws them through `00477F20`: it sorts the instances with `+0x08` bit 0 set into a list by
the sort key `+0x04` (head at bank `+0x60`, link `+0x02`, `004781E0`), then calls `00504700` for each
whose skeleton entry passes the frame-state test. `00504700` calls `0053D780` once, or twice when
instance `+0x244` bit 4 is set, and `0053D780` reaches `0053AB50`.

The record teardown `0041E860` returns up to eight instances listed from record `+0x90` through
`00478070(bank, index)`, which releases the instance with `00504C40` and frees its slot
(`0051FCF0`). `00504C40` frees the sixteen palette resources at `+0x140` (`003CD590`, `003CD5D0`)
and marks their pairs in the map `+0x180` free (`0xFF`), releases the `@FDM` binding when `+0x08`
bit 2 is set (`00409CA0`), releases the 32 texture slot words at `+0x100` (`00521250`) and resets
the instance (`005049E0`).

- `00504BC0(record, value)` sets bit 7 of byte `+1` of each of the record's instance palette
  resources to `value` (`003CD7F0`); its caller is `004213E0`.
- When the bank's byte `+0x62` is 1, `00477F20` walks the instances with `004781A0` instead of
  sorting them: an instance with `+0x08` bit 0 takes the bank's byte `+0x66` into `+0xB2` and
  `003A2C80` copies its `0x260` bytes into the display list's data arena as an entry keyed by its
  `+0x04` shifted right by 4. The entry's function is the bare `ret` `0016D6A0`, so the drain
  draws nothing for it (`004781AA`–`004781D1`).

## Layouts

The object, as its constructor `001F4DA0` and the methods above use it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `void*` | vtable 00903B68 |  |
| `+0x008` | `vec` | 16-byte elements (begin, end, capacity), allocator at +0x020 |  |
| `+0x028` | `void*` | companion object (slots 1 and 3 add it to and remove it from a list) |  |
| `+0x030` | `vec` | mesh instances, 8-byte pointers, allocator at +0x048 |  |
| `+0x050` | `void*` | the single extra mesh instance |  |
| `+0x058` | `vec` | part records, 0x318 bytes each, allocator at +0x070 |  |
| `+0x078` | `0x318 B` | template part record |  |
| `+0x390` | `vec` | 0x24-byte elements, allocator at +0x3A8 (slot 17 empties it) |  |
| `+0x3C0` | `f32[4]` | output vector, 0 after a reset |  |
| `+0x3D0` | `i32[4]` | output vector, 4 after a reset |  |
| `+0x3E0` | `object` | constructed by 00633040 |  |
| `+0x480` | `i32` | key, -1 at construction |  |
| `+0x488` | `void*` | model description |  |
| `+0x490` | `void*` | companion model description |  |
| `+0x498` | `u8` | slot 4 sets, slot 5 returns |  |
| `+0x499` | `u8` | key is in the table at 01DFE1B0 |  |
| `+0x49C` | `u32` | part id matched by slot 16 (slot 15 sets) |  |
| `+0x4A0` | `f32` | slot 11 stores its argument / 128 |  |
| `+0x4A4` | `u32` | slot 11 sets 1 |  |
| `+0x4A8` | `f32` | 1.0; slot 8 stores its float argument |  |
| `+0x4AC` | `f32` | 1.0; slot 8 stores the light block's ambient alpha |  |
| `+0x4B0` | `u32` | mSpecialShadowFlag (slot 25) |  |
| `+0x4B4` | `u8` | ready |  |
| `+0x4B5` | `u8` | 1 |  |
| `+0x4B6` | `u8` | 1 (slot 21) |  |
| `+0x4B8` | `u32` | slot 22 |  |
| `+0x4BC` | `u32` | slot 23 |  |
| `+0x4C0` | `f32` | 20.0 |  |
| `+0x4C4` | `f32[48]` | matrix bank A |  |
| `+0x584` | `f32[48]` | matrix bank B |  |
| `+0x644` | `f32[4]` | fog colour bank A |  |
| `+0x654` | `f32[4]` | fog colour bank B |  |
| `+0x664` | `u32` | refraction mode (slot 24) |  |

The part record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | the mesh's parameter set; its +0x08 is the parameter block |  |
| `+0x08` | `f32` | z-bias a, bank A |  |
| `+0x0C` | `f32` | z-bias a, bank B |  |
| `+0x10` | `f32` | z-bias b, bank A |  |
| `+0x14` | `f32` | z-bias b, bank B |  |
| `+0x30` | `void*[92]` | parameter descriptors, sunIndex first, g_txChrAlpha at +0x310 |  |

The render model instance, as `005049E0` resets it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i16` | own index, -1 when free |  |
| `+0x002` | `i16` | next in the draw list |  |
| `+0x004` | `i32` | sort key |  |
| `+0x008` | `u32` | bit 0 drawn |  |
| `+0x050` | `f32[16]` | matrix, identity |  |
| `+0x090` | `f32[4]` | colour, 1.0 |  |
| `+0x0A0` | `f32[4]` | colour times the script colour, 1.0 |  |
| `+0x0B0` | `i16` | composite fade, Q12, 0x1000 |  |
| `+0x0D0` | `f32[4]` | 255.0 |  |
| `+0x0F8` | `void*` | render record |  |
| `+0x244` | `u32` | bit 0 blend override, bit 4 draw twice; 4 after a reset |  |
| `+0x248` | `f32` | blend override value, 1.0 |  |

The vtable has 31 slots (`00903B68`, read from the image):

| Slot | Body | What it does |
|---:|---|---|
| 0 | `001F52F0` | destructor (`001F51E0`), frees when asked |
| 1 | `001F89B0` | adds the companion `+0x28` to the list from `0018B4E0` |
| 2 | `001F6E70` | setup |
| 3 | `001F6D60` | teardown: removes the companion, empties the vectors, key -1 |
| 4, 5 | `001FB070`, `001F86E0` | set and get `+0x498` |
| 8 | `001F9B20` | lights and ambient into every part record |
| 9 | `001F9A80` | fog colour into the bank |
| 11 | `001F8BE0` | `+0x4A0` = argument / 128, `+0x4A4` = 1 |
| 13 | `001FB120` | z-bias and matrix publish |
| 15 | `001F9A60` | set `+0x49C` |
| 16 | `001FA3D0` | build and submit the draw list |
| 17 | `001F5C10` | empty the `+0x390` vector |
| 21, 22, 23, 25 | `001FA810`, `001F9FE0`, `001F9A70`, `001FAD40` | set `+0x4B6`, `+0x4B8`, `+0x4BC`, `+0x4B0` |
| 24 | `001FA1A0` | refraction parameters |
| 26 | `001FAA10` | bone palette copy |
| 27 | `001F86D0` | return `+0x4B4` |
| 28 | `001F6E50` | return part record `n` |
| 29 | `00848340` | return `this + 8` |
| 30 | `001FA820` | shadow parameters |

Slots 6, 7, 10, 12, 14, 19 and 20 are `001F9FF0`, `001FB080`, `001F8C00`, `001F8C70`, `001FA0A0`,
`001F8D10` and `001FA0E0`. Every access found is in [the object](character-render-object-character-render-object-accesses.tsv),
[instance](character-render-object-render-model-instance-accesses.tsv) and
[instance bank](character-render-object-render-model-instance-container-accesses.tsv) tables.

## State

- Objects are never destroyed in play: a returned object is parked under its model and handed to
  the next record that asks for the same model, after `001F89E0` resets its per-frame values.
- Bank selection is two bytes of the `[01F7F598]` object: `+0x1C` for writing, `+0x1D` for reading.

## Modding notes

- A model whose meshes lack one of the shader parameters still binds: the descriptor is null and every
  write to it is skipped.
- Bone palette indices come from the digits in the bone names; a renamed bone moves to another palette
  entry.

## Related

- [Character render records](character-render-records.md): the record that owns the object, and the banks.
- [Character lighting and shadows](character-lighting-and-shadows.md): slot 8 and the light block.
- [Character fades](character-fades.md): the instance's colour and fade fields.
- [Graphics settings](../Engine-Core/graphics-settings.md): the shadow object and the character light settings.
