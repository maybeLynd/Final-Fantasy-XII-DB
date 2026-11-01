---
title: "CharacterRenderObject: the per-character draw object, its model instances, shader bindings and the transform publish"
kind: "system"
category: "Graphics"
addresses: "0x00903B68, 0x001F4DA0, 0x001F52F0, 0x001F51E0, 0x001F6E70, 0x001F6D60, 0x001F89E0, 0x001F7790, 0x0018D240, 0x001FB120, 0x001FAD50, 0x001F9A80, 0x001FA3D0, 0x001F9B20, 0x001FA1A0, 0x001FAA10, 0x001FA820, 0x001F6E50, 0x001F86D0, 0x001BD4A0, 0x001BD840, 0x001BDAB0, 0x01F81248, 0x0017F0D0, 0x0017F100, 0x0017EFC0, 0x003703A0, 0x0053AB50, 0x0053D780, 0x00504700, 0x00477F20, 0x004780C0, 0x005049E0, 0x003E55B0, 0x00189120, 0x01F7F598, 0x001F5D70"
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
`[0x01F81248]` (`0x001BDAB0`).

- `0x0017F0D0(key)` asks the manager for an object through `0x001BD4A0`, once `0x0017EFC0(key)` reports the
  key's model as registered. Its callers are `0x003703A0` (the skeleton-entry update) and `0x0053AB50`
  (the record's draw), each storing the result in the record's `+0x6B8`.

- `0x0017EFC0(key)` asks the model asset cache (`0x001BC000`) through `0x001BB040(cache, key)`: the key
  must have a model in the cache's map at `+0xB8` whose asset list is ready (`0x001BB120`, which then
  binds the model's palette textures), and a model with byte `+0x98` set also needs its companion
  `-2 - key` to pass the same test.

- `0x001BD4A0(manager, key)` looks the model description up (`0x001BAFF0`) and checks a cache of parked
  objects keyed by the description's `+0x2A0`. With no parked object it allocates `0x668` bytes,
  constructs (`0x001F4DA0`) and runs setup (vtable slot 2). With one it takes it out of the cache and
  resets it (`0x001F89E0`). Either way the object is appended to the manager's live list.
- `0x0017F100(object)` returns it: `0x001BD840` removes it from the live list and parks it in the cache under
  its model key (`0x001F6E60`, the description's `+0x2A0`). The record's teardown `0x004200A0` calls it and
  clears `+0x6B8`.
- When the record has a parent with an object, `0x0053AB50` attaches the two through `0x0017EF60` →
  `0x001BD630`, with a per-bone map at record `+0x6D0`.

- `0x001BD630` reads, for the bone names of both objects, each name's number with `0x001F6E00` (the
  decimal digits before the first `_`, 0 for a name that starts with `_`) and the text after that
  `_` (`strstr`), and compares the texts character by character.

### The ready byte

The constructor clears `+0x4B4`; setup sets it to 1 at its end (`0x001F7729`) and nothing clears it
again. Slots 3, 8, 9, 13, 24 and 30, the bank copy `0x001FAD50` and the draw `0x001F5D70` do nothing while it
is 0; slot 16 reads it per part. `0x001F89E0(object, key)`, the reset used on reuse, writes the key to
`+0x480` and, only for a ready object, restores the per-frame defaults (`+0x4A8` and `+0x4AC` at 1.0,
`+0x4B5`/`+0x4B6` at 1, the output vectors at `+0x3C0` and `+0x3D0`).

### Setup

Slot 2, `0x001F6E70(object, key, description)`:

1. stores the key at `+0x480`, creates the companion at `+0x28` (`0x001F5B80(0x01F82F10)`, which points
   back at the object), and sets `+0x499` when the key is one of six in the table at `0x01DFE1B0`;
2. stores the description at `+0x488`, and for a key of 0 or more the character's shadow model at `+0x490`: the
   record filed under `-2 - key` (`0x001F6EF7`-`0x001F6F15`), which holds the model's `chr_shadow` list
   ([Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md));
3. makes the shadow model's mesh instance, keeps it at `+0x50` (`0x001F7066`-`0x001F7076`) and binds its material into
   the template record embedded at `+0x78` through the binder `0x001F7790` (`0x001F70F3`); every shipped shadow model
   has one mesh with one instance (588 of 588 in the
   [shadow meshes table](../PhyreEngine/phyre-asset-files-meshes-chr_shadow.tsv));
4. makes one mesh instance per mesh of the model at `+0x488` into the vector at `+0x30` (`0x001F7305`-`0x001F732F`) and
   appends one `0x318` record per mesh to the vector at `+0x58`, binding it by name or copying an existing record
   for the same parameter set;
5. sets `+0x4B4` and calls `0x001BD7D0` on the manager.

### The shader binding record

`0x001F7790(…, shader, block, record, template)` fills a `0x318`-byte record. Without a template it
looks up 98 parameter names in the shader (`0x0018D240`) and stores 92 of the results as descriptor
pointers from `+0x30`; with one it copies the template.

It then writes defaults into the parameter block: `sunIndex` -1, `fresnelRefEnabled` and `eCameraLightEnabled` 1, `PS2ZBiasEnabled`,
`PS2ZBiasOriginal`, `PS2ZBiasInstance` and `paletteEnabled` 0, among others. A descriptor's word
`+0x10` is the byte offset into the block and `+0x12 & 0x1FFF` its size; every write checks it fits.
The offset of each name is in [the shader binding record's table](character-render-object-shader-binding-record-0x318-slots.tsv).

### Columns of character-render-object-shader-binding-record-0x318-slots.tsv

One row per name lookup in `0x001F7790`, 98 rows: 92 stored, then the six `...SamplerSampler` names, which are
bound as samplers and given no slot (`offset` `(unstored)`, `index` and `store_site` empty).

| Column | Holds |
|---|---|
| `lookup_site` | the address of the `call 0x0018D240` that looks the name up; a call to `0x0018D240` on all 98 rows |
| `store_site` | the address of the `mov` that stores the lookup's result (`rax`) at the row's `offset` in the record; on all 92 stored rows that instruction names the offset |

### The z-bias and matrix publish

Slot 13, `0x001FB120(object, part, flag, a, b, m1, m2, m3)`, is called by slot 16 for every part with
`flag` 1. It writes two parameters at once: `PS2ZBiasEnabled` = 1 unless `a` and `b` are both 0, and
`PS2ZBiasNoGS` = (`flag` == 0). The rest goes into one of two banks, chosen by byte `+0x1C` of the
object at `[0x01F7F598]` (`0x00189120`):

| | Bank A (byte 0) | Bank B (byte non-zero) |
|---|---|---|
| `a`, `b` | part record `+0x08`, `+0x10` | part record `+0x0C`, `+0x14` |
| three 64-byte matrices | object `+0x4C4`..`+0x583` | object `+0x584`..`+0x643` |
| fog colour (slot 9) | object `+0x644`..`+0x653` | object `+0x654`..`+0x663` |

`0x001FAD50(object, part)`, called per part by the draw `0x001F5D70`, reads the bank chosen by byte `+0x1D`
of the same object and writes `PS2ZBiasOriginal` = `a`, `PS2ZBiasInstance` = `b`, the three matrices to
`PS2WHMatrix`, `PS2HSMatrix` and `InvPS2WHSMatrix`, and the fog colour to `PS2FogVec`. Slot 9
(`0x001F9A80`) takes the fog colour as 0..255 values and stores each channel divided by 255, alpha
clamped to 0..1.

### The draw

`0x0053AB50` draws a record's model. It runs the object's methods through one-line wrappers: slot 1
(`0x0017F0B0`), slot 8 with the light block `0x02CA8110` (`0x0017F1C0`), slot 9 (`0x0017F180`), slot 21 with
record `+0x284` bit `0x1000` (`0x0017F220`), slots 22, 23, 24, 15, slot 26 with the record's matrices at
`+0x6C0` (`0x0017F260`), slot 12, slot 17, slot 6, and slot 16 (`0x0017F210`). Slot 8 is described on
[character lighting and shadows](character-lighting-and-shadows.md).

Slot 16, `0x001FA3D0`, builds the object's draw list. For each mesh instance in the vector at `+0x30` and each
part descriptor (32 bytes) whose two id bytes and `+0x49C` match a mesh, it picks a technique table by
the part's kind byte (`0x01DFE1D0`, `0x01DFE2F0`, or `ChrOpaque` for kinds above `0x10`), switches to the
`0x01F83020` / `0x01F83040` set while `+0x4A8` is below 0.75, then calls slots 19, 20 (kinds 2, 5, 10, 13),
10 and 13 for the part, and hands the list to `0x0060E960`.

The slot-24 call in `0x0053AB50` goes through the null-safe wrapper `0x0017F200`, and `0x0017F250` calls
slot 18, `0x001FAFB0`, the same way for the texture-rectangle copy `0x00477B10`. Slot 18 appends a `0x24`-byte element (two bytes and four 8-byte values) to the vector
at `+0x390`.

### The ordered draw

`CharacterOrderedObject`'s execute reaches `0x001F5D70(object, …)`. The shadow pass is the walk the frame render
makes with byte `+0xC34` of the render manager `[0x01F7F598]` set to 1 (`0x00187D20`, read at `0x001F5DCA`). In it an
object with a key draws the character's shadow. When the key's resource entry (`0x002E98F0`, `0x002DF980`) has byte
`+0x16` = `'h'` or the key is `0x6E006D`, it returns with nothing drawn (`0x001F5E69`-`0x001F5E7D`). Otherwise it files
block `0x25` with 1 (`0x0060E810`), publishes two shadow values with `0x001FB310` and runs slot 30 on its part records:

- `0x001FB310` writes `+0x4B8` to the shadow object's `+0x4C` and `+0x50` = 2.3 (`0x01DFE408`) ×
  `+0x4BC` (`0x001F0850`), the values slot 30 hands to `m_chrObjHeight` and
  `m_chrObjFlyingHeight`, and copies `+0x4C0` to `0x02CB83B0`.
- With the shadow model's mesh instance at `+0x50`, the template record `+0x78` is copied into a one-record vector
  (`0x001F87B0`), slot 30 runs on it, that one mesh is drawn with the `ShadowRender` pass (`0x01F82FA0`, built from the
  name at `0x0015CE17`-`0x0015CE25`; `0x001F5EF0`-`0x001F5F38`) and the render manager's counter goes up by 1 (`0x00185A80`).
  In this pass the character's own meshes are not drawn: the draw jumps to the pass's end (`0x001F5F97`).
- Without one, slot 30 runs on the vector `+0x58` and each mesh instance of `+0x30` is drawn. The pass is
  `ShadowRenderWithRef` (`0x01F82FC0`, `0x0015CDE7`-`0x0015CDEE`) for a record whose `+0x2C0` is set while `+0x4B7` is set
  and the key is not `0x730004`, and `ShadowRender` for every other record (`0x001F615D`-`0x001F61CC`).

At the end of the mesh walk, while byte `+0xF8` of the manager `0x001BDAB0()` is set, `0x001F68E0`
draws the skeleton: for each mesh instance it builds one line per bone, from the bone's position
(row `+0x30` of its `0x40`-byte matrix) to its parent's, the parent index read from the mesh's
`+0x58` table. It reserves a render-thread callback (`0x005FEB30`) for `0x001F5C20`, which draws the
lines 512 at a time (`0x006215A0`, mode 1) between `0x00628570(ctx, 0, 1)` and `0x00628570(ctx, 1)`.

The teardown, slot 3 (`0x001F6D60`), empties the mesh instances through `0x001F86F0`: each instance of
`+0x30` and the single one at `+0x50` goes through `0x001EEEF0` and leaves the object's cluster
`+0x3E0` through `0x001EEC30`, a null-safe `0x0063ABF0(cluster, instance)`. Its twin `0x001EEC50(record)`, reached
only by a tail-jump from the deferred call `0x001B6C30` ([Render command list](render-command-list.md)), returns on a
null record and otherwise calls `0x0063ABF0([0x01F82E50], record +0x00)`, or `0x0063ABF0([0x01F82E50], 0)` when byte
`+0x08` is set (`0x001EEC50`-`0x001EEC73`).

### The bone palette

Slot 26, `0x001FAA10(object, palette)`, reads each mesh's bone names: the decimal digits before the
first `_` give the palette index. It copies that 64-byte matrix into the mesh's bone matrix with the
first two components of every row negated and the last component forced to 1.0. It does the same for
the single mesh at `+0x50`, and does not test `+0x4B4`.

### Refraction and shadow parameters

- Slot 24, `0x001FA1A0(object, enable, power, alpha, mode)`, sets `refractionEnabled` (1.0 or 0),
  `refractionPower`, `refractionAlpha` and `RefractionSampler` in every part record, and keeps `mode` at
  `+0x664`.
- Slot 30, `0x001FA820`, writes `iDebugMode`, `mSpecialShadowFlag` (from `+0x4B0`, set by slot 25),
  `m_chrObjHeight`, `m_chrObjFlyingHeight`, `g_txShadow` and `g_txChrAlpha` from the shadow object
  `0x001F0850` ([graphics settings](../Engine-Core/graphics-settings.md)).

### Render model instances

The root's `+0xDA0` bank holds the `0x260`-byte render model instances, 160 slots, taken by
`0x004780C0` and reset by `0x005049E0`. A record's `+0x64` names its instance (`0x003E55B0`).

Before the instances, `0x0041E4D0` runs `0x004FDD90`, which calls `0x004FDDA0`. That function copies
the camera matrices `0x02AEDE70`-`0x02AEDEAF` and `0x02AEDD30`-`0x02AEDD6F` to `0x02CA7F80` and writes three records into the
current GS command buffer (`0x005044B0`, closing a full block with `0x00504450`):

1. a header holding `[0x02EBA404]`;
2. an A+D GIF tag of 19 register writes, among them XYOFFSET_1 and _2 (`0x18`, `0x19`) = `(0x1000 - w) x 8`,
   `(0x1000 - h) x 8` and SCISSOR_1 and _2 (`0x40`, `0x41`) = 0 to `w - 1`, 0 to `h - 1`, for the GS frame `w`
   `0x022D8EAC` and `h` `0x022D8EB4`;
3. a copy of the 0x150-byte block `0x02EBA400` with the matrices at `+0x10` and `+0x50`, the vector `0x02AEDF10` at
   `+0xE0` (kept at `0x02EBA4B0`), and 1791.97 and 1823.97 at `+0xA0` and `+0xA4`.

Those matrices are the two copies. Rows `0x02CA7F80`, `0x02CA7F90`, `0x02CA7FA0` and `0x02CA7FB0` hold the first, from
`0x02AEDE70` (`0x004FDDD7`-`0x004FDE03`), and go to `+0x50`-`+0x8F` (`0x004FE192`-`0x004FE1B3`). Rows `0x02CA7FC0`,
`0x02CA7FD0`, `0x02CA7FE0` and `0x02CA7FF0` hold the second, from `0x02AEDD30` (`0x004FDE11`-`0x004FDE34`), and go to
`+0x10`-`+0x4F` (`0x004FE1C1`-`0x004FE1E2`). The render update `0x0053AB50` also takes the second's address
(`0x0053C1C7`, `0x0053C869`, `0x0053CE39`, `0x0053CF71`).

At boot `0x00475310` (`0x0036F4FC`) fills part of that block: `+0xC4` 10.0, `+0xC8` 150.0, `+0xCC` 1.5, `+0xE0` 16.0,
`+0xE4` and `+0xE8` 4.0, `+0xD4` 5, `+0xD8` `0x40`, and 0 in `+0xC0` and `+0xD0`.

Those words from `+0xC0` are the focus pass's settings, a record at `0x02EBA4C0`. The focus verbs set four of them:
`setfocusstatus` (`0x135`, `0x003542E0`) sets `+0xC0` through `0x003799C0`, `setfocuslength` (`0x130`, `0x00352DE0`)
sets `+0xC4` through `0x003799D0`, `setfocusrange` (`0x131`, `0x00353240`) sets `+0xC8` through `0x003799F0`, and
`setfocusshift` (`0x133`, `0x00353AA0`) sets `+0xCC` through `0x00379A00`.

The area unload `0x002628B0` turns the pass off
(`0x003799C0(0)`, `0x00262C16`). Each frame `0x00475390` (through the jump at `0x0036F440`) passes the record to the GS sprite
builder `0x00474710` while `+0xC0` is non-zero and `+0xD0` is 0; `0x00474710` reads it through `r14`.

The copy of the
whole block in `0x004FDDA0` (`0x004FE100`-`0x004FE175`) carries every word into the GS buffer, and then overwrites
`+0xE0`-`+0xE8` of the copy with the vector `0x02AEDF10` (`0x004FE1F5`-`0x004FE215`). So the boot values there reach no
consumer that is located yet.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBA4B8` | `f32` | 0 (zero-filled tail of `.data`) | the third float of the vector `0x02AEDF10` that `0x004FDDA0` keeps, from the copy's `+0xE8` | `0x004FDDA0` (`0x004FE233`) | `0x0053AB50` (`0x0053C94F`), which adds it, times a scale, to the third float of a point; the next frame's block copy in `0x004FDDA0` |
| `0x02EBA4C4` | `f32` | 0 (zero-filled tail of `.data`) | the focus length, 10.0 at boot | `0x00475310` (`0x00475322`); `0x003799D0` (`0x003799D0`), for `setfocuslength` | `0x00474710` (`0x0047486A`, `0x00474AC6`); the block copy in `0x004FDDA0` |
| `0x02EBA4C8` | `f32` | 0 (zero-filled tail of `.data`) | the focus range, 150.0 at boot | `0x00475310` (`0x00475332`); `0x003799F0` (`0x003799F0`), for `setfocusrange` | `0x00474710` (`0x00474862`, `0x00474AC0`); the block copy in `0x004FDDA0` |
| `0x02EBA4CC` | `f32` | 0 (zero-filled tail of `.data`) | the focus shift, 1.5 at boot | `0x00475310` (`0x00475342`); `0x00379A00` (`0x00379A00`), for `setfocusshift` | `0x00474710` (`0x00474857`, `0x0047509F`, `0x004750B6`); the block copy in `0x004FDDA0` |
| `0x02EBA4D0` | `u32` | 0 (zero-filled tail of `.data`) | non-zero holds the focus pass back; only ever set to 0 | `0x00475310`, 0 (`0x00475358`) | `0x00475390` (`0x00475399`); the block copy in `0x004FDDA0` |
| `0x02EBA4E0` | `f32` | 0 (zero-filled tail of `.data`) | 16.0 from boot | `0x00475310` (`0x0047534A`) | the block copy in `0x004FDDA0`, which then overwrites the copied word; the focus pass `0x00474710`, which gets the record from `0x00475390` (`0x004753A2`), reads nothing at its `+0x20`, and no other RIP-relative, image-base-relative or address-forming reference names it |
| `0x02EBA4E4` | `f32` | 0 (zero-filled tail of `.data`) | 4.0 from boot | `0x00475310` (`0x00475373`) | as for `0x02EBA4E0` |
| `0x02EBA4E8` | `f32` | 0 (zero-filled tail of `.data`) | 4.0 from boot; the 8-byte store also zeroes `0x02EBA4EC` | `0x00475310` (`0x0047537D`) | as for `0x02EBA4E0` |

`0x0041E4D0` draws them through `0x00477F20`: it sorts the instances with `+0x08` bit `0x1` set into a list by
the sort key `+0x04` (head at bank `+0x60`, link `+0x02`, `0x004781E0`), then calls `0x00504700` for each
whose skeleton entry passes the frame-state test. `0x00504700` calls `0x0053D780` once, or twice when
instance `+0x244` bit `0x10` is set, and `0x0053D780` reaches `0x0053AB50`.

The record teardown `0x0041E860` returns up to eight instances listed from record `+0x90` through
`0x00478070(bank, index)`, which releases the instance with `0x00504C40` and frees its slot
(`0x0051FCF0`). `0x00504C40` frees the sixteen palette resources at `+0x140` (`0x003CD590`, `0x003CD5D0`)
and marks their pairs in the map `+0x180` free (`0xFF`), releases the `@FDM` binding when `+0x08`
bit `0x4` is set (`0x00409CA0`), releases the 32 texture slot words at `+0x100` (`0x00521250`) and resets
the instance (`0x005049E0`).

- `0x00504BC0(record, value)` sets bit `0x80` of byte `+1` of each of the record's instance palette
  resources to `value` (`0x003CD7F0`); its caller is `0x004213E0`.
- When the bank's byte `+0x62` is 1, `0x00477F20` walks the instances with `0x004781A0` instead of
  sorting them: an instance with `+0x08` bit `0x1` takes the bank's byte `+0x66` into `+0xB2` and
  `0x003A2C80` copies its `0x260` bytes into the draw list's packet arena as an entry keyed by its
  `+0x04` shifted right by 4. The entry's function is the bare `ret` `0x0016D6A0`, so the drain
  draws nothing for it (`0x004781AA`–`0x004781D1`).

## Layouts

The object, as its constructor `0x001F4DA0` and the methods above use it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `void*` |  | vtable `0x00903B68` |
| `+0x008` | `vec` |  | 16-byte elements (begin, end, capacity), allocator at `+0x020` |
| `+0x028` | `void*` |  | companion object (slots 1 and 3 add it to and remove it from a list) |
| `+0x030` | `vec` |  | mesh instances, 8-byte pointers, allocator at `+0x048` |
| `+0x050` | `void*` |  | the shadow model's mesh instance |
| `+0x058` | `vec` |  | part records, `0x318` bytes each, allocator at `+0x070` |
| `+0x078` | `u8[792]` |  | template part record (`0x318` bytes) |
| `+0x390` | `vec` |  | `0x24`-byte elements, allocator at `+0x3A8` (slot 17 empties it) |
| `+0x3C0` | `f32[4]` |  | output vector, 0 after a reset |
| `+0x3D0` | `i32[4]` |  | output vector, 4 after a reset |
| `+0x3E0` | `object` |  | constructed by `0x00633040` |
| `+0x480` | `i32` |  | key, -1 at construction |
| `+0x488` | `void*` |  | model description |
| `+0x490` | `void*` |  | shadow model record (filed under -2 - key) |
| `+0x498` | `u8` |  | slot 4 sets, slot 5 returns |
| `+0x499` | `u8` |  | key is in the table at `0x01DFE1B0` |
| `+0x49C` | `u32` |  | part id matched by slot 16 (slot 15 sets) |
| `+0x4A0` | `f32` |  | slot 11 stores its argument / 128 |
| `+0x4A4` | `u32` |  | slot 11 sets 1 |
| `+0x4A8` | `f32` |  | 1.0; slot 8 stores its float argument |
| `+0x4AC` | `f32` |  | 1.0; slot 8 stores the light block's ambient alpha |
| `+0x4B0` | `u32` | mSpecialShadowFlag | (slot 25) |
| `+0x4B4` | `u8` | ready |  |
| `+0x4B5` | `u8` |  | value 1 |
| `+0x4B6` | `u8` |  | 1 (slot 21) |
| `+0x4B8` | `u32` |  | slot 22 |
| `+0x4BC` | `u32` |  | slot 23 |
| `+0x4C0` | `f32` |  | value 20.0 |
| `+0x4C4` | `f32[48]` |  | matrix bank A |
| `+0x584` | `f32[48]` |  | matrix bank B |
| `+0x644` | `f32[4]` |  | fog colour bank A |
| `+0x654` | `f32[4]` |  | fog colour bank B |
| `+0x664` | `u32` |  | refraction mode (slot 24) |

The part record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` |  | the mesh's parameter set; its `+0x08` is the parameter block |
| `+0x08` | `f32` |  | z-bias a, bank A |
| `+0x0C` | `f32` |  | z-bias a, bank B |
| `+0x10` | `f32` |  | z-bias b, bank A |
| `+0x14` | `f32` |  | z-bias b, bank B |
| `+0x30` | `void*[92]` |  | parameter descriptors, sunIndex first, g_txChrAlpha at `+0x310` |

The render model instance, as `0x005049E0` resets it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i16` |  | own index, -1 when free |
| `+0x002` | `i16` |  | next in the draw list |
| `+0x004` | `i32` |  | sort key |
| `+0x008` | `u32` |  | bit `0x1` drawn |
| `+0x050` | `f32[16]` |  | matrix, identity |
| `+0x090` | `f32[4]` |  | colour, 1.0 |
| `+0x0A0` | `f32[4]` |  | colour times the script colour, 1.0 |
| `+0x0B0` | `i16` |  | composite fade, Q12, `0x1000` |
| `+0x0D0` | `f32[4]` |  | value 255.0 |
| `+0x0F8` | `void*` |  | render record |
| `+0x244` | `u32` |  | bit `0x1` blend override, bit `0x10` draw twice; 4 after a reset |
| `+0x248` | `f32` |  | blend override value, 1.0 |

The vtable has 31 slots (`0x00903B68`, read from the image):

| Slot | Body | What it does |
|---:|---|---|
| 0 | `0x001F52F0` | destructor (`0x001F51E0`), frees when asked |
| 1 | `0x001F89B0` | adds the companion `+0x28` to the list from `0x0018B4E0` |
| 2 | `0x001F6E70` | setup |
| 3 | `0x001F6D60` | teardown: removes the companion, empties the vectors, key -1 |
| 4, 5 | `0x001FB070`, `0x001F86E0` | set and get `+0x498` |
| 8 | `0x001F9B20` | lights and ambient into every part record |
| 9 | `0x001F9A80` | fog colour into the bank |
| 11 | `0x001F8BE0` | `+0x4A0` = argument / 128, `+0x4A4` = 1 |
| 13 | `0x001FB120` | z-bias and matrix publish |
| 15 | `0x001F9A60` | set `+0x49C` |
| 16 | `0x001FA3D0` | build and submit the object's draw list |
| 17 | `0x001F5C10` | empty the `+0x390` vector |
| 21, 22, 23, 25 | `0x001FA810`, `0x001F9FE0`, `0x001F9A70`, `0x001FAD40` | set `+0x4B6`, `+0x4B8`, `+0x4BC`, `+0x4B0` |
| 24 | `0x001FA1A0` | refraction parameters |
| 26 | `0x001FAA10` | bone palette copy |
| 27 | `0x001F86D0` | return `+0x4B4` |
| 28 | `0x001F6E50` | return part record `n` |
| 29 | `0x00848340` | return `this + 8` |
| 30 | `0x001FA820` | shadow parameters |

Slots 6, 7, 10, 12, 14, 19 and 20 are `0x001F9FF0`, `0x001FB080`, `0x001F8C00`, `0x001F8C70`, `0x001FA0A0`,
`0x001F8D10` and `0x001FA0E0`. Every access found is in [the object](character-render-object-character-render-object-accesses.tsv),
[instance](character-render-object-render-model-instance-accesses.tsv) and
[instance bank](character-render-object-render-model-instance-container-accesses.tsv) tables.

## State

- Objects are never destroyed in play: a returned object is parked under its model and handed to
  the next record that asks for the same model, after `0x001F89E0` resets its per-frame values.
- Bank selection is two bytes of the `[0x01F7F598]` object: `+0x1C` for writing, `+0x1D` for reading.

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
