[Home](../../README.md) / [Graphics](README.md) / CharacterRenderObject

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| CharacterRenderObject: the per-character draw object, its model instances, shader bindings and the transform publish | system | Graphics | Character models / Character Rendering | The object that draws one character: how a render record gets one and gives it back, its 0x668-byte layout and 31-slot vtable, the ready byte that gates it, the 0x318-byte shader binding record kept per mesh, the double-buffered publish of the PS2 z-bias values, matrices and fog colour, the bone palette copy, and the 0x260-byte render model instances and their draw list. | 0x00903B68, 0x001F4DA0, 0x001F52F0, 0x001F51E0, 0x001F6E70, 0x001F6D60, 0x001F89E0, 0x001F7790, 0x0018D240, 0x001FB120, 0x001FAD50, 0x001F9A80, 0x001FA3D0, 0x001F9B20, 0x001FA1A0, 0x001FAA10, 0x001FA820, 0x001F6E50, 0x001F86D0, 0x001BD4A0, 0x001BD840, 0x001BDAB0, 0x01F81248, 0x0017F0D0, 0x0017F100, 0x0017EFC0, 0x003703A0, 0x0053AB50, 0x0053D780, 0x00504700, 0x00477F20, 0x004780C0, 0x005049E0, 0x003E55B0, 0x00189120, 0x01F7F598, 0x001F5D70 |

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
`[0x01F81248]`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BDAB0` |

</details>

- `0x0017F0D0(key)` asks the manager for an object through `0x001BD4A0`, once `0x0017EFC0(key)` reports the
  key's model as registered. Its callers are `0x003703A0` (the skeleton-entry update) and `0x0053AB50`
  (the record's draw), each storing the result in the record's `+0x6B8`.

- `0x0017EFC0(key)` asks the model asset cache¹ through `0x001BB040(cache, key)`: the key
  must have a model in the cache's map at `+0xB8` whose asset list is ready (`0x001BB120`, which then
  binds the model's palette textures). For a model with byte `+0x98` set, the companion `-2 - key`, when
  the map holds it, must first pass the asset-list test too; a companion the map does not hold is not
  required².
- `0x0017EFC0` answers 0 when `0x001BC000` gives no cache, and otherwise 1 when the low byte of `0x001BB040`'s
  answer is non-zero³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BC000` |
| ² | `0x001BB0B6`-`0x001BB0FD` |
| ³ | `0x0017EFC8`-`0x0017EFE8` |

</details>

- `0x001BD4A0(manager, key)` looks the model description up¹ and checks a cache of parked
  objects keyed by the description's `+0x2A0`. With no parked object it allocates `0x668` bytes,
  constructs² and runs setup (vtable slot 2). With one it takes it out of the cache and
  resets it³. Either way the object is appended to the manager's live list.
- `0x001BD4A0` takes the object parked last under that key (the back of its list, `0x001BD566`), resets it with the new
  key before it unlinks it, and erases the key's map entry when the list is left empty⁴. A
  new object is counted in manager `+0xFC`⁵, and its setup gets the key and the description.
- The live list is the vector of object pointers at manager `+0x00`, grown by `0x001AB570` when it is full;
  `0x001BD4A0` returns the object⁶.
- `0x0017F100(object)` returns it: `0x001BD840` removes it from the live list and parks it in the cache under
  its model key (`0x001F6E60`, the description's `+0x2A0`). The record's teardown `0x004200A0` calls it and
  clears `+0x6B8`.
- `0x0017F100` does nothing when the manager `0x001BDAB0()` or the object is null⁷.
  `0x001BD840` parks an object only when it finds it in the live vector: it appends `{object, 3}` to its key's list
  and moves the vector's last element into the freed place⁸. It ends with a jump to the
  bare `ret` `0x0016D6A0` with the text `Can't find character object when try to remove it!`⁹.
- `0x001BDAC0(manager)`, the manager's update, is called on every pass of the pump `0x0017D6E0`¹⁰. It ages
  the parked objects only on the pump's first pass, while `0x0017D980()` is 0 (the dword `0x01F7F4B8`, stored 0 at
  `0x0017D706` and 1 at `0x0017D846` before each further pass), and while the dword `0x01FD4A68` is 0
 ¹¹.
- Each such walk lowers a non-zero count of the `{object, 3}` entries by 1¹²; at 0 it calls the object's
  teardown, slot 3¹³, which returns non-zero, since every parked object is ready (see the ready byte).
  `0x001BDAC0` then clears the entry's object pointer and frees the 0x20-byte entry¹⁴; the
  object's own block is not freed.
- A key whose list is left empty loses its map entry, and the manager's key count `+0x48` falls by 1
 ¹⁵.
- `0x001BDAC0` then sets byte `+0x4B5` to 1 on every non-null object in the live list¹⁶, when
  the list is non-empty and either the dword at `0x001C1990()` (`[0x01F81268]`) is 1 or byte `+0xDCC` of the
  `[0x01F7F598]` object is set¹⁷; the two gates of the parked walk do not apply to it
 ¹⁸.
- When the record has a parent with an object, `0x0053AB50` attaches the two through `0x0017EF60` →
  `0x001BD630`, with a per-bone map at record `+0x6D0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BAFF0` |
| ² | `0x001F4DA0` |
| ³ | `0x001F89E0` |
| ⁴ | `0x001BD57E`-`0x001BD5CE` |
| ⁵ | `0x001BD54F` |
| ⁶ | `0x001BD5D3`-`0x001BD5FF` |
| ⁷ | `0x0017F109`-`0x0017F116` |
| ⁸ | `0x001BD870`-`0x001BD902` |
| ⁹ | `0x001BD907`-`0x001BD92F` |
| ¹⁰ | `0x0017D783` |
| ¹¹ | `0x001BDACB`-`0x001BDAE0` |
| ¹² | `0x001BDB67` |
| ¹³ | `0x001BDB2E` |
| ¹⁴ | `0x001BDB35`-`0x001BDB62` |
| ¹⁵ | `0x001BDB77`-`0x001BDB9B` |
| ¹⁶ | `0x001BDC10`-`0x001BDC34` |
| ¹⁷ | `0x00189120`, `0x00187530` |
| ¹⁸ | `0x001BDBCA`-`0x001BDC04` |

</details>

- `0x001BD630` reads, for the bone names of both objects, each name's number with `0x001F6E00` (the
  decimal digits before the first `_`, 0 for a name that starts with `_`) and the text after that
  `_` (`strstr`), and compares the texts character by character.

### The ready byte

The constructor clears `+0x4B4`; setup sets it to 1 at its end¹ and nothing clears it
again. Slots 3, 8, 9, 13, 24 and 30, the bank copy `0x001FAD50` and the draw `0x001F5D70` do nothing while it
is 0, except that slot 24 still sets the cache byte `+0x230` for a non-zero `enable`²; slot 16
reads it per part. `0x001F89E0(object, key)`, the reset used on reuse, writes the key to
`+0x480` and, only for a ready object, restores the per-frame defaults (`+0x4A8` and `+0x4AC` at 1.0,
`+0x4B5`/`+0x4B6` at 1, the output vectors at `+0x3C0` and `+0x3D0`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F7729` |
| ² | `0x001FA1C2` |

</details>

For a ready object `0x001F89E0` also empties the `+0x390` vector, zeroes the byte `+0x498`, `+0x49C`-`+0x4A7` and
`mSpecialShadowFlag` `+0x4B0`, and sets every lane of `+0x3C0` to 0 and of `+0x3D0` to 4¹.
The constructor calls it with key -1 while the object is not ready, so there it only writes the key².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F89F1`-`0x001F8A5E` |
| ² | `0x001F4F86` |

</details>

### Setup

Slot 2, `0x001F6E70(object, key, description)`:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | stores the key at `+0x480`, creates the companion at `+0x28` (`0x001F5B80(0x01F82F10)`, which points back at the object), and sets `+0x499` when the key is one of six in the table at `0x01DFE1B0`; |   |
| 2 | stores the description at `+0x488`, and for a key of 0 or more the character's shadow model at `+0x490`: the record filed under `-2 - key`, which holds the model's `chr_shadow` list ([Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)); | `0x001F6EF7`-`0x001F6F15` |
| 3 | makes the shadow model's mesh instance, keeps it at `+0x50` and binds its material into the template record embedded at `+0x78` through the binder `0x001F7790`; every shipped shadow model has one mesh with one instance (588 of 588 in the [shadow meshes table](../PhyreEngine/phyre-asset-files-meshes-chr_shadow.tsv)); | `0x001F7066`-`0x001F7076`<br>`0x001F70F3` |
| 4 | makes one mesh instance per mesh of the model at `+0x488` into the vector at `+0x30` and appends one `0x318` record per mesh to the vector at `+0x58`, binding it by name or copying an existing record for the same parameter set; | `0x001F7305`-`0x001F732F` |
| 5 | sets `+0x4B4` and calls `0x001BD7D0` on the manager. |   |

### The shader binding record

`0x001F7790(…, shader, block, record, template)` fills a `0x318`-byte record. Without a template it
looks up 98 parameter names in the shader¹ and stores 92 of the results as descriptor
pointers from `+0x30`; with one it copies the template.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0018D240` |

</details>

It then writes defaults into the parameter block: `sunIndex` -1, `fresnelRefEnabled` and `eCameraLightEnabled` 1, `PS2ZBiasEnabled`,
`PS2ZBiasOriginal`, `PS2ZBiasInstance` and `paletteEnabled` 0, among others. A descriptor's word
`+0x10` is the byte offset into the block and `+0x12 & 0x1FFF` its size; every default written here checks it fits.
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
object at `[0x01F7F598]`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00189120` |

</details>

| | Bank A (byte 0) | Bank B (byte non-zero) |
|---|---|---|
| `a`, `b` | part record `+0x08`, `+0x10` | part record `+0x0C`, `+0x14` |
| three 64-byte matrices | object `+0x4C4`..`+0x583` | object `+0x584`..`+0x643` |
| fog colour (slot 9) | object `+0x644`..`+0x653` | object `+0x654`..`+0x663` |

`0x001FAD50(object, part)`, called per part by the draw `0x001F5D70`, reads the bank chosen by byte `+0x1D`
of the same object and writes `PS2ZBiasOriginal` = `a`, `PS2ZBiasInstance` = `b`, the three matrices to
`PS2WHMatrix`, `PS2HSMatrix` and `InvPS2WHSMatrix`, and the fog colour to `PS2FogVec`. Each of the six stores is
skipped when its descriptor in the part record is null¹; none tests the size at `+0x12`.
Slot 9² takes the fog colour as 0..255 values and stores each channel divided by 255, alpha
clamped to 0..1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001FAD9C`-`0x001FAF80` |
| ² | `0x001F9A80` |

</details>

### The draw

`0x0053AB50` draws a record's model. It runs the object's methods through one-line wrappers: slot 1¹, slot 8 with the light block `0x02CA8110`², slot 9³, slot 21 with
record `+0x284` bit `0x1000`⁴, slots 22, 23, 24, 15, slot 26 with the record's matrices at
`+0x6C0`⁵, slot 12, slot 17, slot 6, and slot 16⁶. Slot 8 is described on
[character lighting and shadows](character-lighting-and-shadows.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0017F0B0` |
| ² | `0x0017F1C0` |
| ³ | `0x0017F180` |
| ⁴ | `0x0017F220` |
| ⁵ | `0x0017F260` |
| ⁶ | `0x0017F210` |

</details>

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
object with a key draws the character's shadow. When the key's resource entry¹ has byte
`+0x16` = `'h'` or the key is `0x6E006D`, it returns with nothing drawn². Otherwise it files
block `0x25` with 1³, publishes two shadow values with `0x001FB310` and runs slot 30 on its part records:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E98F0`, `0x002DF980` |
| ² | `0x001F5E69`-`0x001F5E7D` |
| ³ | `0x0060E810` |

</details>

- `0x001FB310` writes `+0x4B8` to the shadow object's `+0x4C` and `+0x50` = 2.3¹ ×
  `+0x4BC`², the values slot 30 hands to `m_chrObjHeight` and
  `m_chrObjFlyingHeight`, and copies `+0x4C0` to `0x02CB83B0`.
- With the shadow model's mesh instance at `+0x50`, the template record `+0x78` is copied into a one-record vector
 ³, slot 30 runs on it, that one mesh is drawn with the `ShadowRender` pass (`0x01F82FA0`, built from the
  name at `0x0015CE17`-`0x0015CE25`; `0x001F5EF0`-`0x001F5F38`) and the render manager's counter goes up by 1⁴.
  In this pass the character's own meshes are not drawn: the draw jumps to the pass's end⁵.
- Without one, slot 30 runs on the vector `+0x58` and each mesh instance of `+0x30` is drawn. The pass is
  `ShadowRenderWithRef`⁶ for a record whose `+0x2C0` is set while `+0x4B7` is set
  and the key is not `0x730004`, and `ShadowRender` for every other record⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01DFE408` |
| ² | `0x001F0850` |
| ³ | `0x001F87B0` |
| ⁴ | `0x00185A80` |
| ⁵ | `0x001F5F97` |
| ⁶ | `0x01F82FC0`, `0x0015CDE7`-`0x0015CDEE` |
| ⁷ | `0x001F615D`-`0x001F61CC` |

</details>

At the end of the mesh walk, while byte `+0xF8` of the manager `0x001BDAB0()` is set, `0x001F68E0`
draws the skeleton: for each mesh instance it builds one line per bone, from the bone's position
(row `+0x30` of its `0x40`-byte matrix) to its parent's, the parent index read from the mesh's
`+0x58` table. It reserves a render-thread callback¹ for `0x001F5C20`, which draws the
lines 512 at a time (`0x006215A0`, mode 1) between `0x00628570(ctx, 0, 1)` and `0x00628570(ctx, 1)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005FEB30` |

</details>

The teardown, slot 3¹, empties the mesh instances through `0x001F86F0`: each instance of
`+0x30` and the single one at `+0x50` goes through `0x001EEEF0` and leaves the object's cluster
`+0x3E0` through `0x001EEC30`, a null-safe `0x0063ABF0(cluster, instance)`. Its twin `0x001EEC50(record)`, reached
only by a tail-jump from the deferred call `0x001B6C30` ([Render command list](render-command-list.md)), returns on a
null record and otherwise calls `0x0063ABF0([0x01F82E50], record +0x00)`, or `0x0063ABF0([0x01F82E50], 0)` when byte
`+0x08` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F6D60` |
| ² | `0x001EEC50`-`0x001EEC73` |

</details>

### The bone palette

Slot 26, `0x001FAA10(object, palette)`, reads each mesh's bone names: the decimal digits before the
first `_` give the palette index. It copies that 64-byte matrix into the mesh's bone matrix with the
first two components of every row negated (`xorps` with `0x80000000`). Rows 0 to 2 keep their fourth component,
and in row 3 the fourth is forced to 1.0¹. It does the same for the single mesh at
`+0x50`, and does not test `+0x4B4`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001FAADE`-`0x001FAB99` |

</details>

### Refraction and shadow parameters

- Slot 24, `0x001FA1A0(object, enable, power, alpha, mode)`, sets `refractionEnabled` (1.0 or 0),
  `refractionPower`, `refractionAlpha` and `RefractionSampler` in every part record, and keeps `mode` at
  `+0x664`.
- A non-zero `enable` first sets byte `+0x230` of the model asset cache `0x001BC000()`, also on an object that is not
  ready¹. A part record is written only when all four descriptors are present. It gets 1.0,
  `power`, `alpha` and the sampler record {`0xFF`, 0, `v`}² when `enable` and the value `v` are
  non-zero, and `refractionEnabled` 0 otherwise³; these stores do not check the size.
- `v` is the first word of a record from the render manager `0x00189120()`, 0 when the record's byte `+0x08` is
  set: `0x00186A80` (its `+0xB78`) for a non-zero `mode`; for `mode` 0, `0x00186840`, or `0x00186A00` while `+0x664`
  still holds a non-zero mode. `+0x664` is stored at each part, so only the first part after a change to mode 0
  gets `0x00186A00`'s record⁴.
- Slot 30, `0x001FA820`, writes `iDebugMode`, `mSpecialShadowFlag` (from `+0x4B0`, set by slot 25),
  `m_chrObjHeight`, `m_chrObjFlyingHeight`, `g_txShadow` and `g_txChrAlpha` from the shadow object
  `0x001F0850` ([graphics settings](../Engine-Core/graphics-settings.md)).
- `0x001FA820(object, parts)` works on the vector of part records it is given. For each, `iDebugMode` is the
  shadow object's `+0x48`, or when that is 0, 1 while `[0x02CB8404]` is above 0.99⁵ and 0 otherwise.
  `m_chrObjHeight` and `m_chrObjFlyingHeight` are its `+0x4C` and `+0x50`, and `g_txShadow` and `g_txChrAlpha`
  its records at `+0x18` and `+0x30`, through `0x001945B0`⁶.
- Each of those writes is skipped when its descriptor is null. While the setting `[0x01F82D20]` `+0x3C` is 0,
  each part also stores `-|[0x02CB8404]|` into `0x02CB8404`, after reading it for `iDebugMode`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001FA1B9`-`0x001FA1C2` |
| ² | `0x001945B0` |
| ³ | `0x001FA2CC`-`0x001FA369` |
| ⁴ | `0x001FA274`-`0x001FA2C5` |
| ⁵ | `0x008F3110`, `0x001FA8EA`-`0x001FA8EE` |
| ⁶ | `0x001FA8D3`-`0x001FA998` |
| ⁷ | `0x001FA8F2`-`0x001FA90C` |

</details>

### Render model instances

The root's `+0xDA0` bank holds the `0x260`-byte render model instances, 160 slots, taken by
`0x004780C0` and reset by `0x005049E0`. A record's `+0x64` names its instance¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E55B0` |

</details>

`0x004780C0` takes a slot from `0x0051FBB0` and returns null when it gives -1. Otherwise it resets the slot's
instance¹, initialises it with `0x00504F00` and its own arguments, stores the slot in the word `+0x00`
and returns it². `0x003E55B0(record)` returns null when the word `+0x64` is -1, and otherwise
the instance in slot `+0x64` of the `+0xDA0` bank of `0x0020E600(record +0x10)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005049E0` |
| ² | `0x004780E0`-`0x00478178` |
| ³ | `0x003E55B6`-`0x003E55E0` |

</details>

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
`0x02AEDE70`¹, and go to `+0x50`-`+0x8F`². Rows `0x02CA7FC0`,
`0x02CA7FD0`, `0x02CA7FE0` and `0x02CA7FF0` hold the second, from `0x02AEDD30`³, and go to
`+0x10`-`+0x4F`⁴. The render update `0x0053AB50` also takes the second's address⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004FDDD7`-`0x004FDE03` |
| ² | `0x004FE192`-`0x004FE1B3` |
| ³ | `0x004FDE11`-`0x004FDE34` |
| ⁴ | `0x004FE1C1`-`0x004FE1E2` |
| ⁵ | `0x0053C1C7`, `0x0053C869`, `0x0053CE39`, `0x0053CF71` |

</details>

At boot `0x00475310`¹ fills part of that block: `+0xC4` 10.0, `+0xC8` 150.0, `+0xCC` 1.5, `+0xE0` 16.0,
`+0xE4` and `+0xE8` 4.0, `+0xD4` 5, `+0xD8` `0x40`, and 0 in `+0xC0` and `+0xD0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036F4FC` |

</details>

Those words from `+0xC0` are the focus pass's settings, a record at `0x02EBA4C0`. The focus verbs set four of them:
`setfocusstatus` (`0x135`, `0x003542E0`) sets `+0xC0` through `0x003799C0`, `setfocuslength` (`0x130`, `0x00352DE0`)
sets `+0xC4` through `0x003799D0`, `setfocusrange` (`0x131`, `0x00353240`) sets `+0xC8` through `0x003799F0`, and
`setfocusshift` (`0x133`, `0x00353AA0`) sets `+0xCC` through `0x00379A00`.

The area unload `0x002628B0` turns the pass off
(`0x003799C0(0)`, `0x00262C16`). Each frame `0x00475390` (through the jump at `0x0036F440`) passes the record to the GS sprite
builder `0x00474710` while `+0xC0` is non-zero and `+0xD0` is 0; `0x00474710` reads it through `r14`.

The copy of the
whole block in `0x004FDDA0`¹ carries every word into the GS buffer, and then overwrites
`+0xE0`-`+0xE8` of the copy with the vector `0x02AEDF10`². So the boot values there reach no
consumer.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004FE100`-`0x004FE175` |
| ² | `0x004FE1F5`-`0x004FE215` |

</details>

The only instructions that name `0x02EBA4E0`-`0x02EBA4EB` by `rip` or through the image base are the boot
stores¹. `0x00474710` reads only `+0x4`, `+0x8`, `+0xC`, `+0x14`, `+0x18` and
`+0x1C` of the record through `r14` and never copies `r14`. The array readers `0x00537AA0` and `0x00537AF0` index
`0x02EBA460` in 4-byte steps and read `+0` and `+8` of the element their callers name with index 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0047534A`, `0x00475373`, `0x0047537D` |

</details>

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

First `0x00477F20` calls `0x00537B10(0, 0)`, `0x00537B10(0, 1)` and `0x00521320()`¹. It sorts while
the bank's byte `+0x62` is 0; 1 takes the `0x004781A0` walk below and any other value draws nothing². In the sorted walk each listed instance takes the bank's byte `+0x66` into `+0xB2`³, and its skeleton entry is slot `+0x40` of the bank at `+0x38`, null for -1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00477F2D`-`0x00477F3E` |
| ² | `0x00477F43`-`0x00477F4E` |
| ³ | `0x00477FB5` |

</details>

The test: while `0x00229EA0` (the byte `0x02064AD3`) is 3, an instance is drawn when `0x002EF010` gives 1 for its
entry's `+0xA8`, and otherwise when it gives 0¹. `0x00504700` makes the extra call as
`0x0053D780(instance, 1, 1)` and always ends with a jump to `0x0053D780(instance, 1, 0)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00477FD0`-`0x00478006` |
| ² | `0x00504706`-`0x0050472E` |

</details>

The record teardown `0x0041E860` returns up to eight instances listed from record `+0x90` through
`0x00478070(bank, index)`, which releases the instance with `0x00504C40` and frees its slot¹. `0x00504C40` frees the sixteen palette resources at `+0x140`²
and marks their pairs in the map `+0x180` free (`0xFF`), releases the `@FDM` binding when `+0x08`
bit `0x4` is set³, releases the 32 texture slot words at `+0x100`⁴ and resets
the instance⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0051FCF0` |
| ² | `0x003CD590`, `0x003CD5D0` |
| ³ | `0x00409CA0` |
| ⁴ | `0x00521250` |
| ⁵ | `0x005049E0` |

</details>

- `0x00504BC0(record, value)` sets bit `0x80` of byte `+1` of each of the record's instance palette
  resources to `value`¹; its caller is `0x004213E0`.
- When the bank's byte `+0x62` is 1, `0x00477F20` walks the instances with `0x004781A0` instead of
  sorting them: an instance with `+0x08` bit `0x1` takes the bank's byte `+0x66` into `+0xB2` and
  `0x003A2C80` copies its `0x260` bytes into the draw list's packet arena as an entry keyed by its
  `+0x04` shifted right by 4. The entry's function is the bare `ret` `0x0016D6A0`, so the drain
  draws nothing for it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CD7F0` |
| ² | `0x004781AA`-`0x004781D1` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

`0x001F4DA0` runs the base constructor `0x00212C70`, sets the vtable and gives each of the vectors `+0x08`, `+0x30`,
`+0x58` and `+0x390` null pointers and an allocator through `0x001EDF00` (which stores the vtable `0x00902720`), and
constructs `+0x3E0` with `0x00633040`. It writes the values listed below and zero in `+0x28`, `+0x50`, `+0x488`,
`+0x490`, `+0x498`-`+0x4A7`, `+0x4B0`, `+0x4B4`, `+0x4B7` and `+0x4B8`-`+0x4BF`, zero-fills the template `+0x78`¹, calls `0x001F89E0(object, -1)` and returns the object².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F4E88`-`0x001F4F7C` |
| ² | `0x001F4F80`-`0x001F4F8C` |

</details>

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
| `+0x4B5` | `u8` |  | 1; set to 1 on the live objects by `0x001BDAC0` (`0x001BDC1B`) while [[`0x01F81268`]] is 1 or [`0x01F7F598`]`+0xDCC` is set |
| `+0x4B6` | `u8` |  | 1 (slot 21) |
| `+0x4B7` | `u8` |  | 0 at construction; the ordered draw's ShadowRenderWithRef test |
| `+0x4B8` | `f32` |  | slot 22 (`0x001F9FE0`): the shadow height, copied to the shadow object's `+0x4C` for m_chrObjHeight (`0x001FB31E`) |
| `+0x4BC` | `f32` |  | slot 23 (`0x001F9A70`): times 2.3 into the shadow object's `+0x50` for m_chrObjFlyingHeight (`0x001FB32F`) |
| `+0x4C0` | `f32` |  | value 20.0 |
| `+0x4C4` | `f32[48]` |  | matrix bank A |
| `+0x584` | `f32[48]` |  | matrix bank B |
| `+0x644` | `f32[4]` |  | fog colour bank A |
| `+0x654` | `f32[4]` |  | fog colour bank B |
| `+0x664` | `u32` |  | refraction mode (slot 24) |

The part record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `void*` |  | the mesh's parameter set; its `+0x08` is the parameter block |
| `+0x008` | `f32` |  | z-bias a, bank A |
| `+0x00C` | `f32` |  | z-bias a, bank B |
| `+0x010` | `f32` |  | z-bias b, bank A |
| `+0x014` | `f32` |  | z-bias b, bank B |
| `+0x030` | `void*[65]` |  | parameter descriptors 0-64, sunIndex first |
| `+0x238` | `void*` |  | position 65: not among the stored descriptors (the record's slot table, below) |
| `+0x240` | `void*[27]` |  | parameter descriptors 66-92, g_txChrAlpha at `+0x310`; 92 stored descriptors in all |

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
| `+0x244` | `u32` |  | bit `0x1` blend override, bit `0x10` draw twice; a reset clears the bits under mask `0x1B` and sets bit `0x4` |
| `+0x248` | `f32` |  | blend override value, 1.0 |

`0x005049E0` keeps every other bit of `+0x244`: `and eax, 0xFFFFFFE4` then `or eax, 4`¹. It
also sets the word `+0xE0` and the dwords `+0x40`, `+0x1E4`, `+0x208`-`+0x220` and `+0x240` to -1, the 32 words
`+0x100`-`+0x13F` to `0xFFFF`, `+0x140`-`+0x17F` to -1, the 20 bytes `+0x180`-`+0x193` to `0xFF` and the 20 dwords
`+0x194`-`+0x1E3` to -1. It zeroes `+0x04`-`+0x2B`, `+0x30`-`+0x3F`, `+0xB2`, `+0xB6`, `+0xB7`, `+0xB9`-`+0xBB`,
`+0xE8`, `+0x1E8` and `+0x24C`, and sets byte `+0xB8` to `0xFF` and `+0x250` to 0.03².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00504AE7`-`0x00504AF3` |
| ² | `0x00504A05`-`0x00504B9A` |

</details>

The vtable has 31 slots (`0x00903B68`, read from the image):

| Slot | Body | What it does |
|---:|---|---|
| 0 | `0x001F52F0` | destructor (`0x001F51E0`), then frees the `0x668` bytes (`0x00809950`) when bit `0x1` of its argument is set; returns the object |
| 1 | `0x001F89B0` | adds the companion `+0x28` to the list from `0x0018B4E0` |
| 2 | `0x001F6E70` | setup |
| 3 | `0x001F6D60` | teardown, only on a ready object (else it returns 0): the mesh instances through `0x001F86F0`, `+0x490` 0, removes the companion `+0x28` from the list of `0x0018B4E0` (`0x0018B0B0`) and hands it to `0x001F8B30(0x01F82F10)`, empties the vectors `+0x58`, `+0x390` and `+0x08`, `+0x488` 0, key -1, `+0x498` 0; returns 1 (`0x001F6D7A`-`0x001F6DE8`) |
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

The destructor `0x001F51E0` sets the vtable `0x00903B68` again, zeroes `+0x28` without removing the companion, destroys
`+0x3E0`¹ and hands the storage of the vectors `+0x390`, `+0x58`, `+0x30` and `+0x08`, where it has
any, back to their allocators (slot 3, with the capacity in bytes). It ends with a jump to the base destructor
`0x00212C80`²; the mesh instance at `+0x50` is not released there.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006336E0` |
| ² | `0x001F51F2`-`0x001F52E5` |

</details>

Slots 6, 7, 10, 12, 14, 19 and 20 are `0x001F9FF0`, `0x001FB080`, `0x001F8C00`, `0x001F8C70`, `0x001FA0A0`,
`0x001F8D10` and `0x001FA0E0`. Every access found is in [the object](character-render-object-character-render-object-accesses.tsv),
[instance](character-render-object-render-model-instance-accesses.tsv) and
[instance bank](character-render-object-render-model-instance-container-accesses.tsv) tables.

</details>

## State

<details>
<summary>Show the state it keeps</summary>

- A returned object is parked under its model and handed to the next record that asks for the same model, after
  `0x001F89E0` resets its per-frame values. One left parked is emptied by its teardown (slot 3) once its count of 3
  has run out and drops out of the cache; its 0x668-byte block is not freed and no destructor runs, so objects are
  never destroyed in play (see Getting and returning an object).
- Bank selection is two bytes of the `[0x01F7F598]` object: `+0x1C` for writing, `+0x1D` for reading.

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 26 calls with 9 other topics</summary>

**Sound and music** (explained on [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00229EA0`](effect-drawing.md) (on effect drawing) | is called by | [`0x003638B0`](../Sound-And-Music/map-sounds.md) (on map sounds) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00360B50`](../Sound-And-Music/music.md) (on music)<br>[`0x00360DD0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003636A0`](../Sound-And-Music/map-sounds.md) (on map sounds) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00263560`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x0026A1D0`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata)<br>[`0x00379070`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x003791C0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003792D0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003DAA20`](../Engine-Core/frame-update-order.md) (on frame update order) |

**Party** (explained on [player movement](../Movement-And-Pathfinding/player-movement.md), [actor managers](../Characters-And-Objects/actor-managers.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00358B40`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00359200`](../Party/party-leader.md) (on party leader) |

**Platform** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x006336E0`](character-render-object.md) | is called by | [`0x0019CC50`](../Engine-Core/debug-menu.md) (on debug menu) |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |

**Scripts and script commands** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00229EA0`](effect-drawing.md) (on effect drawing) | is called by | [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) |
| [`0x00352DE0`](character-render-object.md) | calls | [`0x00267DB0`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00353240`](character-render-object.md) | calls | [`0x00267DB0`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00353AA0`](character-render-object.md) | calls | [`0x00267DB0`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003542E0`](character-render-object.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003799C0`](character-render-object.md) | is called by | [`0x003542E0`](character-render-object.md) |
| [`0x003799D0`](character-render-object.md) | is called by | [`0x00352DE0`](character-render-object.md) |
| [`0x003799F0`](character-render-object.md) | is called by | [`0x00353240`](character-render-object.md) |
| [`0x00379A00`](character-render-object.md) | is called by | [`0x00353AA0`](character-render-object.md) |

**Menus and HUD** (explained on [clan primer](../Menus-And-HUD/clan-primer.md), [widget messages](../Menus-And-HUD/widget-messages.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00229EA0`](effect-drawing.md) (on effect drawing) | is called by | [`0x002468A0`](../Menus-And-HUD/menu-lists.md) (on menu lists)<br>[`0x00246C20`](../Menus-And-HUD/widgets.md) (on widgets) |

**Developer** (explained on [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0017D6E0`](../Engine-Core/game-application.md) (on game application) | calls | [`0x001C2F50`](../Game-Files-And-Data-Tables/standard-file-formats.md) (on standard file formats) |

</details>

---

[← Character render records](character-render-records.md)
