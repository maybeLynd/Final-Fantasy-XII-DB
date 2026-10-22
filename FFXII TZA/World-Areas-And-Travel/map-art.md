---
title: "Map art: the remaster's map models, the map-art context, its per-map files and the calls the map draw makes"
kind: "system"
category: "World, areas and travel"
addresses: "0x01F81168, 0x001A9930, 0x001A98B0, 0x001A2130, 0x001A9ED0, 0x001A7A50, 0x001A3160, 0x001A5B30, 0x001A92C0, 0x001A9050, 0x001A6A20, 0x001A7F10, 0x001E1670, 0x001A7600, 0x001A7A10, 0x001E5080, 0x001A4DB0, 0x001A9BF0, 0x001E59B0, 0x001AA120, 0x001A9B70, 0x001E5790, 0x001AA240, 0x001E69A0, 0x001A9DD0, 0x001809A0, 0x001C0A90, 0x001BF8B0, 0x001A9CD0, 0x001A53F0, 0x001A7E40, 0x001A40B0"
---

## What the player sees

Every area of the remaster is drawn with new, higher-detail models and textures, yet everything the
area does still follows the original map data: gates open, banners sway, palettes cycle, and models
appear and vanish with the story exactly where the PlayStation 2 version had them. Walls and floors
carry normal and specular detail, many surfaces get a tiled detail texture such as sand, concrete or
steel, and a handful of areas change the order in which scenery and characters are drawn.

## How it works

### The context

`0x001A98B0` creates the map-art context once, from the application set-up `0x00186CD0`. It builds a
0xA0-byte pool at `0x01F81170` (`0x00633040`) and the 0x520-byte context at `0x01F81168` (constructor
`0x001A2130`); `0x001A9930` returns the context. The constructor sets the model count `+0x20` to -1,
reads `opt.csv` (`0x001A9050`), copies the water quality (`[0x01F82D20] + 0x40`) to `+0x2F8` and whether
it is non-zero to `+0x2E5`, and registers `0x001A97F0` with the render settings block (`0x0060B720`).
The per-frame update `0x001A9ED0(context, dt)` runs from the frame pump.

### Naming the map

When the zone's own pack is requested, `0x00379A10` cuts `<area>\<map>` out of the pack's path, swaps
five zones for the zone whose art they reuse (table `0x01EF9490`), passes the name to `0x001805D0` and
clears the first-pass byte `0x022BE7E0`. The swaps are `dst0109` to `dst0103`, `dst0110` to `dst0105`,
`frs0109` to `frs0101`, `frs0110` to `frs0106` and `gil0303` to `gil0301`.

`0x001805D0` calls `0x001A7A50(context, name)`:

1. While an asset list is held (`+0x78`), the same name as `+0x241` returns at once; another name
   first unloads the old map with `0x001A92C0`.
2. `0x001A7CB0` files a whole-file read of `.\GameData\D3D11\ArtData\map\NoModelGroupMaps.txt` with the
   completion `0x001A9A30`, but only while the name set `+0x3A0` is empty.
3. The loaded byte `+0x80` is cleared, the name is copied to `+0x241` and to the probe manager's
   `+0x16C` (`0x001AD780`).
4. The map part of the name is hashed (`0x00674A00`) and looked up in the `opt.csv` table `+0x3E0`:
   `+0x418` and `+0x419` get bytes 1 and 3 of the entry, or both 0 without one. The render manager's
   byte `+0xDB9` is cleared and the post-process object's byte `+0x3E8` (`0x00193D50`) set to 1.
5. The asset list `.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_D3D11_srm.ah` is requested when
   `0x0019EAA0` can open it, else `<map>_D3D11.ah`, through `0x0019EB60`; the handle goes to `+0x78`.
6. The texture-animation prefix `.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_anime_` is written
   to `+0x141`.

### The load waits for the instance count

The map's world data (`YM00`) lists the zone's instances in its tag-30 chunk; the parser passes their
count to `0x001806F0`, which stores it at `+0x20`. Each frame `0x001A9ED0` checks the held asset list:
once `0x0019EB00` reports it loaded, the loaded byte `+0x80` and the queued byte `+0x41A` are clear and
the count is 0 or more, it sets `+0x41A` and posts `0x001A3160` to the job manager (`0x0019A180`,
`0x00199F10`, `0x0019A000`). `0x001A3160` runs the load `0x001A5B30`, sets `+0x80` and clears `+0x41A`.

### Matching models to instances

`0x001A5B30` first rebuilds the texture table `+0x448` (`0x001A7F10`), clears the set `+0xB0`
(`0x001A5810`) and the key vector `+0x4C8`, and sets `+0x3D8` when the map part of the name (`+0x247`)
is in the NoModelGroupMaps set. It registers the cube-map textures with the probe manager
(`0x001ABC80`, `0x001ABCE0`, stored by `0x001AD7B0` and `0x001AD6E0`; `0x001AAC50` builds a probe variant
record with six texture slots), then allocates the slot array `+0x88`: 16 bytes per instance, a
pointer for the main view and one for the sub view.

It then walks every `PMeshInstance` (class descriptor `0x02CB6E80`) of every asset in the list. An
instance whose name `m_name` (`+0x80`) has more than eight characters is matched to the YM00
instance whose index is the decimal number starting at its ninth character; a number outside 0 to
count - 1 skips it. For a match:

- `0x001EE1D0` gives the instance a material array of its own, allocated from the pool `[0x01F81170]`
  (`0x0063A990`).
- Every entry of its mesh's matrix-index array (count at mesh `+0x70`, entries at `+0x78`) is added to
  the set `+0xE8`; with bit 10 of `m_extraFlag` (`+0x5C`) set, also to `+0xB0`. An instance without
  the array puts its own index in `+0xB0` when bit 10 is set.
- Bit 14 of `m_extraFlag` gives the index a sway entry in the map `+0x490` with the context's current speed,
  limit and margin (`+0x480` to `+0x48C`).
- The draw key `+0x4C8[index]` is `m_specialRenderOrder` (`+0x78`) times 0x10000 plus the index when
  the order is positive, else the index times 0x10000.
- The first instance of an index gets two `MapRenderObject`s of 0x268 bytes (`0x001E1670`), one per
  view; a later instance with the same index is appended to both (`0x001A7850`). Its destructor `0x001E1C90`
  (from `0x001E1D90`) unregisters it from `0x01F82D60` (`0x001F8B30`), frees its five vectors (`+0x18`, `+0x38`,
  `+0x58`, `+0x78`, `+0x98`) and ends with `0x00212C80`.

### Material extras for each model

`0x001A7F10` pairs textures with their companions. For each texture of the list whose name ends in
`_n.dds.phyre` or `_spec.dds.phyre` (suffix table `0x008F66F0`, 0x20 bytes apart), it takes the base
name, maps it through `phyremaps.txt` (`0x001A9940`), resolves the base texture (`0x001A76D0`) and stores
the companion in the base texture's entry of `+0x448` (`0x001A2F70`): the normal map at `+0x00`, the
specular map at `+0x08` and the base name at `+0x40`. Textures under `/ArtData/shared/map/` are
paired through the `phyremaps.txt` table's values instead.

For every slot `0x001A5B30` then runs, on both objects, `0x001E4000` (the shader parameter handles of
every material, one 0x220-byte record each, and the ready byte `+0x250`) and looks up the entry of the
model's main texture, the `TextureSampler` texture of its first material (`0x001E3F70`):

- `0x001E55C0(object, normal)` writes 1 to `EnableNormalMap` and binds `NormalMap` on every material of
  an instance without bit 9 of `m_extraFlag`, when the entry has a normal map;
- `0x001E6110(object, specular)` does the same with `EnableSpecularMap` and `SpecularMap`;
- the main texture is kept at `+0x260`.

The load ends by restarting the texture-animation chain (`0x001A7D50`), loading the probe placements
(`0x001AC480`, which also sets `0x01DFE191` when a probe exists), requesting the procedural texture
configuration (`0x001C0A90`) and resetting every sway entry (`0x001A7770`).

### Procedural detail textures

`0x001C0A90(procedural context, name)` files a read of
`/GameData/D3D11/ArtData/map/<area>\<map>/proceduralTextureConfigs.txt` into a pending entry of the
procedural-texture context `[0x01F81258]` keyed by the name. Its completion runs `0x001C0960`, which
finds the entry whose name equals the map-art context's `+0x241`, removes it and hands the text to
`0x001BF8B0`.

`0x001BF8B0` reads records of eight CRLF-separated values until the text ends or a value fails to read:
the texture name, the detail kind, five floats, an integer (1 when missing) and an optional float (0
when missing). It resolves the texture through `0x001A6FF0` (the map's `tex` folder, or its
`phyremaps.txt` value) and skips a record whose texture has no `+0x448` entry (`0x001A7990`). The kind
is looked up by name in the procedural context (`+0x78`); `0x001A9CD0` stores the record in the entry.

After the last record `0x001A53F0` applies them: for each slot whose current-view object has a main
texture (`+0x260`) whose entry carries a kind, it stores the kind at the object's `+0x08` and passes
the kind's texture (`+0x20`) and the seven values to `0x001E5C40`.

### Paletted textures from the PS2 data

The YM00 tag-12 chunk carries the map's paletted PS2 textures. Its parser `0x00468160` walks them
(`0x00536080` returns texture `i`, `0x00536060` the pixel block) and calls `0x001801A0` for each, which
runs `0x001A4DB0(context, id, …)`. For an id with no entry yet, `0x001A4DB0` adds one to the map
`+0x268` with two textures:

- the palette at `+0x28`, built by `0x001837C0` from the PS2 palette data, which reorders a 256-colour
  palette in blocks of eight for the formats `0x105`, `0x205`, `0x305`, `0x4104`, `0x4204` and
  `0x4304`;
- the index texture at `+0x30`, built by `0x00184140` from the index data, or by `0x00183EE0` when the
  call's flag is set.

It also appends a 32-byte record (id, palette data pointer, sizes and format) to the vector `+0x2A0`;
when the vector is full (`+0x2A8` at `+0x2B0`), `0x001A40B0` inserts it instead, doubling the capacity
(one record when empty) through the allocator at `+0x2B8`.

Every frame `0x001808D0`, called from `0x0022A770`, runs `0x001AA120`, which rewrites each recorded palette from its PS2 data through
`0x00183320`, scaling alpha from 0-128 to 0-255 with `a = min((int)(a × 255.0 × (1 / 128)), 255)`
(`0x00183440`-`0x0018346A`), so a palette the original code animates in memory
animates on screen. `0x004680D0` releases the PS2 side and calls `0x00180280`, whose `0x001A5980` frees
both textures of every entry (`0x00183720`) and empties the map and the vector.

### The views and the bridge

Byte `+0x1C` of the render manager (`0x00189120`) tells which view is being prepared: `0x00185A10` sets it
when the camera submitted is the sub view `0x02097B80` (`0x003829D0`, `0x00259FA0`, `0x001821F0`), and
`0x00189CE0` clears it. Every bridge call that picks an object passes that byte as the view, so slot
`2i` is the main-view object of instance `i` and slot `2i + 1` its sub-view object.

The map code reaches the context only through bridge functions at `0x001801A0` to `0x00180A60`. Most
fetch the context (`0x001A9930`) and do nothing when it is absent; `0x00180650`, `0x00180730`, `0x00180830`
and `0x00180900` call their target without that test, and the flag readers (`0x001803D0` and its
neighbours) work on the object alone. `0x001809A0` never touches the context: it calls `0x0018CA40`
twice and tail-jumps to `0x0018C3C0`. The calls the map draw makes:

| Bridge | Target | What it does |
|---|---|---|
| `0x00180320(i)` | `0x001A7600` | the object of instance `i` for the current view, or 0 |
| `0x001803A0()` | `+0x3D8` | the map is in NoModelGroupMaps |
| `0x00180430()` | `+0x80` | the load has finished |
| `0x001804F0(i)` | set `+0xE8` | `i` drives a bone of some model |
| `0x001804A0(i)` | set `+0xB0` (`0x001A7940`) | loaded and `i` is in the set |
| `0x001807A0(i, id)` | `0x001A9BF0` | binds the paletted pair of `id` to the object of `i` |
| `0x00180560(i, matrix)` | `0x001A7A10`, `0x001E5080` | whether the model of `i` is in view |
| `0x001802E0(i)` | `0x001A7410` | the sway angle of `i` |
| `0x00180900(o, …)` | `0x001AA240`, `0x001E69A0` | per-instance draw flags and the alpha threshold |
| `0x00180830(o, …, m)` | `0x001A9DD0` | sampler mode |
| `0x00180730(o, mode, …)` | `0x001A9B70`, `0x001E5790` | a mode from 0 to 4 with its vectors and matrices |
| `0x00180650(…, o, …)` | `0x001A94C0`, `0x001A4FE0` | queues the object for drawing |
| `0x001809A0()` | `0x0018C3C0` | posts the map opaque command once |

### Building the draw list

The draw-list build `0x002F5550` asks `0x001803A0` and `0x00180430` once (`0x002F5D4D`, `0x002F5D56`) and then
walks the instances. For each it takes the object (`0x002F5D84`) and asks `0x001804F0` (`0x002F5D95`):

- An instance whose object has bit 4 of `m_extraFlag` set (`0x001803D0`, `0x002F5DBE`) is skipped.
- On the first pass after a load, while `0x022BE7E0` is 0 and the load has finished, `0x001807A0` binds
  the paletted pair of the instance's texture id (its record's `+0x04`) at `0x002F5DE2`; the pass then
  sets `0x022BE7E0` (`0x002F65D1`).
- For an instance with a model, the hidden-model set (`0x0026E5F0`) is skipped when the map is in
  NoModelGroupMaps or the instance has bit 5 (`0x00180410`, `0x002F5E6B`); the script-forced set
  (`0x0026E5D0`) still applies.
- With bit 2 (`0x00180600`, `0x002F5E46`) the instance is left out while its tag-24 entry's `+0xC8`
  exceeds 1.0.
- An instance in `+0xB0` (`0x001804A0`, `0x002F5F6C`) keeps its placement without the extra transform its
  entry carries at `+0x50`. A model whose instance lacks bit 3 (`0x00180460`, `0x002F5F93`) is placed
  with an identity row instead of the YM00 placement row; with bit 14 (`0x00180480`) the row is turned
  by the sway angle (`0x001802E0`, `0x002F5FE4`).

At the end the build fills the two per-list masks the draw pass reads: an entry is marked culled when
`0x00180560` (`0x002F6683`) reports the model of its instance out of view.

`0x001E5080(object, matrix)` decides that test. It answers yes at once when the first instance's mesh
has a matrix-index array, the first instance has bit 6, or any instance of the object has bit 1.
Otherwise it multiplies the instance matrix by the view matrix of the current view (render manager
`+0x98`, or `+0x3D0` for the sub view, `0x001854C0`) and tests each instance's bounds (`+0x38`) with
`0x001E4B80`; any pass answers yes.

`0x001E4B80` takes the eight corners of the bounds into clip space and
`0x001E25F0` ANDs their outcodes, so a box counts as out of view only when all eight corners lie beyond
the same plane.

The probe binding (`0x001E6480`) and `0x001E2AF0` take an instance's world box from `0x006045E0`, which
hands the bounds' origin, extents and matrix (identity without one) to `0x005FD810`; that transforms
the eight corners and returns their minimum and maximum.

`0x001E2AF0` then runs `0x001E4F70(object, bounds)`: with no matrix at the object's `+0x10` it tests the bounds as they
are, otherwise it rebuilds them from that matrix's columns through `0x001854C0` first, and in both cases passes
them to the clip test `0x001E4B80`.

### Drawing an instance

The draw pass `0x002F4520` clears the draw map at the start of a list (`0x00180250`, `0x002F481A`). For
each instance that has an object (`0x00180320`, `0x002F49E3`) it fills the object from the instance's
PS2 state:

- `0x00180900` (`0x002F4DF8`) passes two flags, a mode, an alpha threshold and two more flags.
  `0x001AA240` keeps a mode of 0, 2 or 3 and turns any other value into 1.
- `0x001E69A0` stores the flags at `+0xC1`, `+0xC2`, `+0xC4` and `+0xC3`, the mode per instance in
  `+0x78` (0 for instances whose byte in `+0x58` is set), the threshold at `+0xC8` unless the
  instance's own `m_alphaThreshold` (`+0x74`) is positive, and a per-instance byte in `+0x98`.
- `0x00180830` (`0x002F4E13`) passes a mode built from bits 4 and 5 of the record's flag word `+0x0C`;
  `0x001A9DD0` stores 3, 2, 1 or 0 at `+0xD0` for 1, 2, 3 or 0.
- `0x00180730` (`0x002F5149`) passes a mode from 0 to 4, chosen from bits 7, 8, 15 and 29 of the
  record's flag word, with its vectors and matrices. `0x001A9B70` passes 1 to 4 through and any other
  value as 0; `0x001E5790` stores it at `+0xD8` and copies the data the mode uses (layout below).
- `0x00180650` (`0x002F5225`) draws the object at once (its vtable slot `+0x08`), or stores it in the
  draw map `+0x4E8` under its key from `+0x4C8` (`0x001A94C0`). An object whose `+0xB8` is set and whose
  `+0xBC` is 0 is also appended to the list `+0x90` (`0x001A4FE0`), which `0x00180A30` draws through
  `0x001A8F80` while `+0x2E5` is set.

Before the walk of the first list the pass finds the last drawn instance whose record flag word has
bit 10 or bit 28 set. Instances up to it are drawn at once; at it the pass calls `0x001809A0`
(`0x002F524B`), and every later instance is queued in the draw map. Once per frame (byte `0x01F7F50D`,
cleared by `0x0017F270`) `0x001809A0` posts a `RenderMapOpaqueObj` command (`0x001F1D30`) on the render
command vector `[0x01F7F5E8]`.

The command's draw `0x001F3570` draws the characters' opaque objects first, when `0x0017FE50` returns 0
and `+0x419` is clear, and then the map's opaque objects with `+0x418` as their order flag
(`0x0018B1B0`). The pass ends with `0x001802B0`: `0x001A6CC0` draws the queued objects in key order and
empties the draw map.

### Binding a paletted pair

`0x001A9BF0(context, view, i, id)` finds `id` in `+0x268`; when instance `i` has an object for the view,
`0x001A2EE0` fetches the pair and `0x001E59B0(object, palette, index)` binds it.

On every material of a ready object `0x001E59B0` writes 1 to `EnableIndexedTex`, binds `PalletTexture` and `IndexTexture`
(`0x001E6040`), and, when the material has `PalletTexSamplerState`, writes a sampler preset from
`[0x01F7E340]` (`0x0018AA00`). The preset follows the instance's `m_specialTextureWrapType` (`+0x7C`) when
it is below 4, else the object's `+0xD0`: 1 gives preset 0, 2 gives 2, 3 gives 3, any other value 1.
It sets the object's `+0x218`.

### The weather slot's shadow set

The weather roll `0x0026D910` calls `0x00180620(slot - 1)`, which runs `0x001A7E40(context, slot - 1)`. That
copies the slot's map and character shadow minimums (`+0x338` and `+0x344` plus four times the slot)
to the shadow object's `+0x140` and `+0x144` (`0x001A7E5F`-`0x001A7E7A`), its cascade row (`+0x350` plus 12
times the slot) to
`+0x870` to `+0x878`, and, while `+0x398` is set, its light direction (`+0x374` plus 12 times the
slot) through `0x001F08A0`.

### Leaving a map

`0x001A92C0` unloads, in this order:

1. every instance's material array goes back to the pool (`0x001EEEF0`, `0x0063ABF0`);
2. the set `+0xE8` and the key vector are emptied;
3. `0x001BD7E0` runs `0x001F8860` on every character render object of `[0x01F81248]` (`0x001BDAB0`), which
   writes 0 to each part record's cube-map enable and unbinds its four cube-map samplers;
4. `+0x80` is cleared and the asset list is released through a render command (`0x00185A90`,
   `0x001A97D0`);
5. the texture-animation sets are dropped (`0x001A96B0`) and `+0x140` cleared;
6. `0x001A5890` destroys both objects of every slot, frees the slot array, sets the model count back to
   -1 and empties the texture table `+0x448`, so the next load waits for the next map's count;
7. the probe manager drops its probes (`0x001ABE30`): each probe is freed through a render command
   (`0x001AD490`, which empties its variants with `0x001ABD40`), and its vectors, `+0x130` and `+0x250`
   are reset;
8. `0x001BF230` drops the procedural context's pending reads, and the list `+0x90` and every sway entry
   are emptied.

### The option files

`0x001A9050` reads `./PS2Data/opt.csv` once. It skips the header line, takes each CRLF line with five
comma-separated fields, hashes the first (the map name, `0x00674A00`) and stores a u32 whose bytes 0 to
3 are 1 when fields 2 to 5 begin with `Y` or `y`. The header names the fields `MapName`,
`ForceMSAAOff`, `FlipMapOpaqueOrder`, `SMAA` and `ForceNoOpaqueChrFirst`; `0x001A7A50` copies
`FlipMapOpaqueOrder` to `+0x418` and `ForceNoOpaqueChrFirst` to `+0x419`.

`0x001A9A30` passes the text of `NoModelGroupMaps.txt` to `0x001A6A20` and frees it. `0x001A6A20` inserts the
name `start` into the set `+0x3A0` and then every token it reads with `%s`, stepping by the token's
length plus 2, so the file must separate names with CRLF.

## Layouts

### The context

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x020` | `i32` | modelCount | YM00 instance count; -1 until `0x001806F0` sets it |
| `+0x078` | `void*` | assetList | the map's `.ah` list (`0x001A7A50`) |
| `+0x080` | `u8` | loaded | set by `0x001A3160` after `0x001A5B30` |
| `+0x088` | `MapRenderObject*` | slots | two per instance: `[2i]` main view, `[2i + 1]` sub view |
| `+0x090` | `MapRenderObject**` | extraList | vector begin, end at `+0x98` (`0x001A4FE0`, `0x001A8F80`) |
| `+0x0B0` | `EastlSet` | keepPlacement | instance ids (`0x001804A0`); 0x38 bytes, root at `+0xC8` |
| `+0x0E8` | `EastlSet` | boneInstances | instance ids named by a mesh's matrix-index array (`0x001804F0`) |
| `+0x141` | `char[256]` | animePrefix | the `.ta` prefix |
| `+0x241` | `char[35]` | mapName | `<area>\<map>`; `+0x247` is the map part |
| `+0x268` | `EastlMap` | palettedTextures | texture id to {palette `+0x28`, index `+0x30`} |
| `+0x2A0` | `PaletteRefresh*` | paletteRefresh | vector begin of 32-byte records, end at `+0x2A8` (`0x001AA120`) |
| `+0x2E5` | `u8` | waterOn | water quality is non-zero |
| `+0x2F8` | `i32` | waterQuality | `[0x01F82D20] + 0x40` at construction |
| `+0x3A0` | `EastlSet` | noModelGroupNames | map names from `NoModelGroupMaps.txt`, plus `start`; size at `+0x3C8` |
| `+0x3D8` | `u8` | noModelGroup | the current map is in the set |
| `+0x3E0` | `EastlMap` | optTable | map-name hash to the `opt.csv` flag bytes (entry `+0x24`) |
| `+0x418` | `u8` | flipMapOpaqueOrder | `opt.csv` field 3 |
| `+0x419` | `u8` | noOpaqueChrFirst | `opt.csv` field 5 |
| `+0x41A` | `u8` | loadQueued | the load job is posted |
| `+0x448` | `EastlMap` | textureExtras | main texture to its extras (below) |
| `+0x490` | `EastlMap` | sway | instance id to sway entry |
| `+0x4C8` | `u32*` | drawKeys | vector begin, end at `+0x4D0`; one key per instance id |
| `+0x4E8` | `EastlMap` | drawMap | draw key to object, emptied every list |

### A texture's extras

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | normalMap | `<name>_n` texture (`0x001A7F10`) |
| `+0x08` | `void*` | specularMap | `<name>_spec` texture |
| `+0x18` | `void*` | kind | procedural kind record (`0x001A9CD0`) |
| `+0x20` | `f32` | value1 | first float of the record; 0.5 by default |
| `+0x24` | `f32` | value2 | second float |
| `+0x28` | `f32` | value3 | third float |
| `+0x2C` | `f32` | value4 | fourth float; 1.0 by default |
| `+0x30` | `f32` | value5 | fifth float; 1.0 by default |
| `+0x34` | `f32` | value7 | the optional last float |
| `+0x38` | `i32` | value6 | the integer; 1 by default |
| `+0x40` | `char[32]` | baseName | base texture name |

### The MapRenderObject fields the bridge writes

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x008` | `void*` | proceduralKind | `0x001A53F0` |
| `+0x018` | `void*` | instances | vector of `PMeshInstance` pointers |
| `+0x038` | `void*` | handles | one 0x220-byte record of parameter handles per material (`0x001E4000`) |
| `+0x058` | `u8*` | instanceFlag | per instance |
| `+0x078` | `i32*` | instanceMode | per instance (`0x001E69A0`) |
| `+0x098` | `u8*` | instanceByte | per instance (`0x001E69A0`) |
| `+0x0B8` | `u8` | extraPass | bit 1 of a material's `+0x10` flags (`0x001E4000`) |
| `+0x0C1` | `u8` | flagA | `0x001E69A0` |
| `+0x0C2` | `u8` | flagB | `0x001E69A0` |
| `+0x0C3` | `u8` | flagD | `0x001E69A0` |
| `+0x0C4` | `u8` | flagC | `0x001E69A0` |
| `+0x0C8` | `f32` | alphaThreshold | `0x001E69A0` |
| `+0x0D0` | `i32` | samplerMode | `0x001A9DD0` |
| `+0x0D8` | `i32` | lightingMode | `0x001E5790`, 0 to 4 |
| `+0x0DC` | `f32[4]` | vector | mode 1; x and y sign-flipped |
| `+0x0EC` | `f32[16]` | matrixA | modes 1 and 4 |
| `+0x12C` | `f32[16]` | matrixB | modes 1 to 4 |
| `+0x16C` | `f32[3]` | vector2 | mode 2 |
| `+0x1D8` | `f32[4]` | vector0 | mode 0 |
| `+0x218` | `u8` | indexedBound | `0x001E59B0` |
| `+0x250` | `u8` | ready | `0x001E4000` |
| `+0x260` | `void*` | mainTexture | key into the context's `+0x448` |

### `m_extraFlag` bits the map code reads

| Bit | Read by | Effect |
|---|---|---|
| 1 | `0x001E5080` | the model counts as in view |
| 2 | `0x00180600` (`0x001E5250`) | left out while the tag-24 entry's `+0xC8` exceeds 1.0 |
| 3 | `0x00180460` (`0x001E4B40`) | keep the YM00 placement row |
| 4 | `0x001803D0` (`0x001E4AE0`) | the instance is skipped in the draw list |
| 5 | `0x00180410` (`0x001E4B20`) | exempt from the hidden-model set |
| 6 | `0x001E5080` | the model counts as in view |
| 7 | `0x001803F0` (`0x001E4B00`) | the draw pass uses white instead of the instance colour |
| 9 | `0x001E55C0`, `0x001E6110` | no normal or specular map |
| 10 | `0x001A5B30` | the instance ids go into `+0xB0` |
| 14 | `0x00180480` (`0x001E4B60`), `0x001A5B30` | the instance sways |

## Shipped data

Measured over the archive.

| Fact | Value |
|---|---|
| asset lists | 914 under `gamedata/d3d11/artdata/map/`: 457 `<map>_d3d11.ah` and 457 `<map>_d3d11_srm.ah` |
| `opt.csv` | `ps2data/opt.csv`, 10,182 bytes, CRLF, a header and 459 rows of 5 fields |
| `FlipMapOpaqueOrder` | `Yes` for 7 maps: `ene0102`, `enw0103`, `frs0106`, `rbn0101`, `rbn0201`, `var0101`, `vic0101` |
| `ForceNoOpaqueChrFirst` | `Yes` for 9 maps: `bul0101`, `rbn5001`, `rrp0101` to `rrp0106`, `rsn5001` |
| `ForceMSAAOff`, `SMAA` | `No` and `Yes` in every row |
| `NoModelGroupMaps.txt` | 32 map names, CRLF, each with an asset list |
| `proceduralTextureConfigs.txt` | 451 files, 68 to 6,696 bytes, all CRLF; 10,477 records, every one of 8 values |
| detail kinds used | `Wall_concrete_01` 6,332, `Steel_rough_01` 1,516, `Rock_roughlittle_01` 1,158, `Sand_little_01` 612, `Fabric_flax_01` 543, `Fabric_carpet_01` 169, `Wood_rough_01` 60, `snow_01` 41, `Leather_base_01` 35, `Wall_concrete_04` 11 |

## Operations

Entering a zone, as the map-art context sees it:

1. `0x00379A10` names the map; `0x001A7A50` unloads the previous one and requests the new asset list.
2. The YM00 parser stores the instance count (`0x001806F0`) and builds the paletted pairs
   (`0x001801A0`, `0x001A4DB0`).
3. `0x001A9ED0` sees the list loaded and posts `0x001A3160`; `0x001A5B30` builds the models and requests
   the procedural configuration; `+0x80` is set.
4. The first draw-list build binds the paletted pairs (`0x001807A0`) and sets `0x022BE7E0`.
5. Every frame the build culls with `0x00180560`, the pass fills each object and draws it, and
   `0x001AA120` refreshes the palettes.

## State

| Address | Kind | Role |
|---|---|---|
| `0x01F81168` | `void*` | the map-art context |
| `0x01F81170` | `void*` | the pool for per-instance material arrays |
| `0x01F81180` | `void*` | the pending `NoModelGroupMaps.txt` text |
| `0x022BE7E0` | `i32` | 0 until the first draw-list build after a map change has bound the paletted pairs |
| `0x01F7F50D` | `u8` | the map opaque command is posted this frame |
| `0x01F81258` | `void*` | the procedural-texture context |

## Modding notes

- A model is attached to a YM00 instance only through its `PMeshInstance` name: eight characters,
  then the instance index in decimal. A model with no instance is never drawn.
- A new map without its own art can reuse another map's by adding a pair to the alias table
  `0x01EF9490`; the five shipped pairs reuse one zone's art for another.
- `opt.csv` is read once at start-up; only `FlipMapOpaqueOrder` and `ForceNoOpaqueChrFirst` change
  the draw. A missing row leaves both off.
- Keep `NoModelGroupMaps.txt` and `proceduralTextureConfigs.txt` CRLF-separated with no leading
  spaces. A procedural record whose texture has no entry in the texture table is skipped.
- Normal and specular maps are found by name: `<texture>_n.dds.phyre` and `<texture>_spec.dds.phyre`
  in the same asset list.

## Related

- [MPK map pack](mpk-map-pack.md): the `YM00` tags that give the instance count and the paletted textures.
- [Doors, gates and map changes](doors-gates-and-map-changes.md): the hidden-model sets the draw list applies.
- [Weather](weather.md): the weather slot behind the shadow set.
- [Zone changes](zone-changes-and-mapjump.md): when the pack request that names the map happens.
- [Texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md): the `.ta` chain the load restarts.
- [Phyre field schema](../PhyreEngine/phyre-field-schema.md): the `PMeshInstance` fields.
- [Render parameters and shader assets](../Graphics/render-parameters-and-shader-assets.md): the map texture paths.
