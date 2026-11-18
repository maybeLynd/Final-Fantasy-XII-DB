[Home](../../README.md) / [Graphics](README.md) / Map cubemaps

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Map cubemaps: the reflection probes, cubeMapConfigs.txt and how map models pick four of them | system | Graphics | Screen effects and movies | The per-map reflection probes of the remaster: the cubemap_&lt;probe&gt;_&lt;weather&gt; environment and irradiance textures a map's art carries, the cubeMapConfigs.txt file that places each probe and gives its weight and radius, the probe manager that builds them, the weighting that picks up to four probes for a point, and how map model materials receive the chosen cubemaps and weights. | 0x01F811C8, 0x001AD440, 0x001A5B30, 0x001ABC80, 0x001ABCE0, 0x001AC810, 0x001AA840, 0x001AC480, 0x001AD130, 0x001ACF80, 0x001AC4B0, 0x001ABF50, 0x001AA3D0, 0x001AD470, 0x001AC670, 0x001AC720, 0x001AC6F0, 0x001E4000, 0x001AD670, 0x001E6480, 0x001E6040 |

## What the player sees

Shiny map surfaces such as polished floors, metal and water reflect a picture of their surroundings, and
lit surfaces pick up ambient colour from them. The pictures are cubemaps captured at a few points in each
map, one set per weather slot. A surface blends the probes nearest to it, so the reflection changes as one
walks from one part of a map to another.

Each map's art carries the probe pictures as textures named by probe number and weather slot, and `cubeMapConfigs.txt`
in the map's folder gives each probe its position, weight and radius. For every mesh of a map model the game weighs
the probes by distance from the mesh's centre and hands the best four, in the current weather, to that mesh's
material.

## How it works

### The probe manager

`0x001AD440` returns the probe manager `[0x01F811C8]`. Its probes are a vector of pointers at `+0xF0`. When a
probe index is asked for that does not exist yet, `0x001AC810(manager, index)` appends probes up to it, each
built by `0x001AA840(probe, index, 80.0, 2.0, 60.0, 1, 0)`: position (80, 2, 60) at `+0x20`, radius 0 at
`+0x2C`, weight 1 at `+0x30`, its index at `+0x38`, enabled byte `+0x40` = 1 and variant 0 at `+0x44`.

Each probe is a 0x48-byte block from `0x00210EC0` (`0x001AC885`), appended to the vector as it comes back, a null
block included (`0x001AC8D3`-`0x001AC904`). `0x001AC810` then stores `index` at `+0x38` of probe `index` and returns
that probe, whether or not it appended any (`0x001AC912`-`0x001AC91F`). `0x001AA840` also zeroes the current weight
`+0x34` and sets the dword `+0x3C` to 1 (`0x001AA8A4`-`0x001AA8B4`).

A probe owns a vector of 0x30-byte variants at `+0x00` (`0x001AD0C0`), whose allocator object at `+0x18` holds the
vtable `0x00902720` (`0x001EDF00`). A variant has six flag bytes at `+0x00`, which start at 0 (`0x001AAC9A`,
`0x001AAC9C`), a vector of texture pointers at `+0x08` and a byte at `+0x28`. Variant 0, the one `0x001AA840`
builds, gets twelve null texture pointers: six from the variant template `0x001AAC50` (`0x001AACB0`-`0x001AACE2`) and
six more that `0x001AA840` pushes itself (`0x001AA936`-`0x001AA973`); `0x001AA840` then sets its byte `+0x28` to 1
(`0x001AA975`).

The variants that `0x001ABB30` adds for an `_e<v>` texture get six null pointers each (`0x001ABB9A`-`0x001ABBD5`). The
registrars and the texture getters below use the slots `2w − 2` and `2w − 1`, 0 to 5 for the weather slots 1 to 3.

`0x001AD3E0`, from the start-up burst `0x0017D4C0`, builds the manager on first use: `0x258` bytes,
constructed by `0x001AA9E0`, which:

- empties the map at `+0x08` and the vectors at `+0xF0`, `+0x110` and `+0x140`, and clears the bytes
  `+0x130`, `+0x244` and `+0x250`;
- lays down the developer capture settings: step `+0xA8` = −2, `+0xB8` = 12, `+0xBC` = 1, `+0x1E0` =
  180, `+0x1E4` = 3, `+0x1E8` = 0.785 and `+0x24C` = `0x400`, with five status strings at `+0x44`,
  `+0x64`, `+0x84`, `+0x204` and `+0x224` (`"None"`, `"Original"`, `"Final"`, `"Current status"`);
- ends with `0x001AD510(manager, manager + 0xF0)`, which keeps the probe vector at `+0xE8` and sets each
  probe's variant `+0x44` to the manager's `+0xC0`, or 0 when that is negative or not below the
  probe's variant count.

While the step `+0xA8` stays negative the capture code does nothing to the picture. The render pass
`0x00187950` runs `0x001AC7C0` each frame, which, when byte `+0xA4` is set and the step is −2, sets the
step to −1 and calls `0x001EF540(1)` on the shadow object (`0x001F0850`). `0x001ACF10(manager, samples)`, from
`0x00186CD0` with the multisample count `0x02CB8084` (`0x0018710D`-`0x0018711D`), keeps the count at `+0x248`
(`0x001ACF1A`) and creates two 512 × 512 targets at `+0xD0` and `+0xC8` (`0x001EE040`).

### Registering the textures

When a map's art loads, `0x001A5B30` walks the textures of the map's asset list (context `+0x78`) and looks
for `cubemap_` in each name (`0x001A5D3E`). The name is matched against four forms:

| Name | Registered by | Slot |
|---|---|---|
| `cubemap_<p>_<w>.dds.phyre` | `0x001ABC80(manager, texture, p, w)` | `2w − 2` of variant 0 |
| `cubemap_irr_<p>_<w>.dds.phyre` | `0x001ABCE0` | `2w − 1` of variant 0 |
| `cubemap_<p>_<w>_e<v>.dds.phyre` | `0x001ABC80` with variant `v` | `2w − 2` of variant `v` |
| `cubemap_irr_<p>_<w>_e<v>.dds.phyre` | `0x001ABCE0` with variant `v` | `2w − 1` of variant `v` |

`p` is the probe index and `w` the weather slot, 1 to 3. `0x001AD7B0` and `0x001AD6E0` store the texture,
adding variants as needed. Both registrars also set byte `2w − 2` or `2w − 1` of the probe's first
variant record. The irradiance map is the texture the shader reads as `IrrCubeMap`.

A negative `p` registers nothing: both registrars return at once (`0x001ABC83`, `0x001ABCE3`). Otherwise they take
the probe from `0x001AC810(manager, p)` (`0x001ABC9D`, `0x001ABCFD`), store the texture through
`0x001AD7B0(probe, texture, w, v)` or `0x001AD6E0` with the same arguments (`0x001ABCB3`, `0x001ABD13`) and then set the
byte (`0x001ABCCF`, `0x001ABD2F`).

### cubeMapConfigs.txt

After the scan, `0x001A5B30` runs `0x001AC480` on the manager, which calls `0x001AD130(manager, manager +
0x16C)` with the map name kept there and sets the manager's byte `+0x250`; `0x01DFE191` then records whether
any probe exists.

`0x001AD130` files a whole-file read of `/GameData/D3D11/ArtData/map/<map>/cubeMapConfigs.txt` (`0x008F6D08`,
through `0x001A1220` and `0x001A0BB0`) with the completion `0x001AD450`, which runs `0x001ACF80` while the manager
`[0x01F811C8]` exists (`0x001AD457`). That finds the pending request whose name matches the map name at context
`+0x241`, parses the text with `0x001AC4B0`, sets the manager's byte `+0x130` and frees the text.

`0x001ACF80(manager)` does nothing without a map-art context `0x001A9930()` (`0x001ACFA4`). It walks the pending
entries of the map at `+0x08` in order (`0x0016D6D0`), passes over an entry whose request has no text yet (request
`+0x100`, `0x001ACFBF`) and stops at the first whose name (entry `+0x20`) equals the map name
(`0x001ACFE0`-`0x001ACFF5`). With no such entry, or one without a request, it changes nothing (`0x001ACFB5`,
`0x001AD00E`).

For the entry it finds, it takes the entry out of the map (`0x0016DA60`) and lowers the map's count `+0x30`
(`0x001AD014`). It frees the entry's name when its buffer holds more than one byte, and the 0x48-byte entry,
through the allocators at entry `+0x38` and manager `+0x38` (`0x001AD02C`-`0x001AD064`). It then runs
`0x001AC4B0(manager, request +0x100)` (`0x001AD078`), sets `+0x130` (`0x001AD07D`), frees the text (`0x00210EB0`,
`0x001AD090`) and frees the 0x118-byte request (`0x00809950`, `0x001AD09D`).

`0x001AC4B0(manager, text)` reads with `%d` and `%f` (`0x008F6D3C`, `0x008F6D40`), skipping the CR and LF
after each value:

1. the probe count; when it exceeds the probes already registered, nothing is read;
2. per probe, in index order: x, y, z (`+0x20`), the weight (`%d`, `+0x30`, raised to 1 when below 1)
   and the radius (`%f`, `+0x2C`). A failed read stops the parse.

After each value it moves to the first CR or LF and then past every CR and LF after it (`0x001AC4E0`-`0x001AC509`),
so the rest of a value's line is skipped. The move stops only at a CR or LF, not at the end of the text; all
451 shipped files end with CR LF, so it always stops inside the text. A count that does not read as one `%d`
value reads nothing (`0x001AC4D5`). The count is compared unsigned (`0x001AC523`), so a negative count also reads
nothing, and a count of 0 reads no probe (`0x001AC532`).

Each value goes straight into the probe, so a failed read keeps the values read before it (`0x001AC57D`,
`0x001AC5C9`, `0x001AC61E`), and the weight is raised to 1 only once it has been read (`0x001AC5FB`-`0x001AC601`).

### Picking probes for a point

`0x001ABF50(manager, indices[4], weights[4], point)` returns indices and weights of 0 while the manager's
byte `+0x244` is set or its `+0xA8` is −1 or above. Otherwise the indices start at 4 (no probe) and the
weights at 0, and every enabled probe is weighed, with `d` the distance from the point in the horizontal
plane (x and z):

- a probe with radius 0 gets `weight / d` (1 when `d` is 0);
- a probe with a radius gets `1 − min(d, radius) / radius`.

When the radius probes sum above 1 they are scaled to sum to 1. The radius-0 probes then share what is
left, `1 − sum`, in proportion to their values. The probe pointers are copied to the vector `+0x110` (sized by
`0x001AB0F0`) and sorted by weight, highest first (quicksort `0x001AA3D0` with the comparator `0x001AD470`), and the first four are returned with their
indices `+0x38` and weights `+0x34`. A probe whose byte `+0x40` is clear is returned with weight 0.

`0x001AC670(manager, i)` and `0x001AC720(manager, i)` return probe `i`'s environment and irradiance texture
for the current weather slot (`0x00265920`, [weather](../World-Areas-And-Travel/weather.md)) in its variant
`+0x44`. `0x001AC6F0` returns its radius.

Both return 0 while the manager's `+0xA8` is −1 or above, when `i`, taken unsigned, is not below the size of
the probe vector the manager keeps at `+0xE8`, or when that variant's texture vector is empty
(`0x001AC674`-`0x001AC6CE`, `0x001AC724`-`0x001AC77E`). Otherwise they read its slot `2w − 2` or `2w − 1` for the
weather slot `w` (`0x001AC6D7`, `0x001AC787`); the variant `+0x44` is used without a check.

### Binding to map materials

`0x001E4000`, called from the map-art load, builds a 0x220-byte record of shader parameter handles for
every material of every mesh of a map model: 67 lookups by name through `0x0018D240`, among them
`EnableCubeMap`, `CubeMap0`-`CubeMap3`, `CubeMapWeight0`-`CubeMapWeight3`, `IrrCubeMap0`-`IrrCubeMap3`,
`cubemapIntensity` and `cubemapFactor`. It marks the model ready (`+0x250`).

`0x001AD670(manager, off)` stores `off` in the manager's byte `+0x244` and runs `0x001E6480` on every map model
of the map-art context (`0x001A7600`). For each instance `i` from 0 to the context's count `+0x20` − 1 it takes
the object for the current view, slot `2i` or `2i + 1` by the render manager's view byte `+0x1C` (`0x00189120`,
`0x001AD690`-`0x001AD6AC`), and passes over an instance with no object (`0x001AD6B4`). With a count of 0 it only
stores the byte (`0x001AD686`). For each mesh of a ready model, `0x001E6480`:

1. takes the centre of the mesh's bounds (`0x006045E0`) and asks `0x001ABF50` for four probes, kept at the
   model's `+0x220` (weights) and `+0x230` (indices);
2. adds up the weights of the four probes that have both textures, and remembers the last of them whose
   doubled radius is below 0.01, so a radius-0 probe;
3. when it found one and every probe with both textures has a doubled radius of at most 0.01, or not above
   the mesh object's `+0x18` or `+0x20`, or the object has `+0x18`, `+0x1C` or `+0x20` above 30, that
   probe gets weight 1 and the other three 0;
4. otherwise divides each weight by the total, or sets it to 0 when the total is 0.01 or less;
5. binds `CubeMapN` and `IrrCubeMapN` for each material through `0x001E6040` and writes `CubeMapWeightN`
   into the material's parameter buffer at the handle's offset (`u16 +0x10`), or 0 while `+0x244` is set.

`0x001E6040(model, buffer, handle, texture)` binds `texture` with a sampler preset of `[0x01F7E340]` and does
nothing for a null `handle` (`0x001E6043`). It hands the record `0xFF`, preset, texture to
`0x001945B0(buffer, handle, record)` (`0x001E6060`-`0x001E60F9`).

The preset follows a wrap value: the instance's `m_specialTextureWrapType` (`+0x7C`) when it is below 4, else
the object's `+0xD0`. 1 gives index 0, 2 gives 2, 3 gives 3 and any other value 1. When the model's byte
`+0x218` is set, the preset is the qword at `[0x01F7E340] + 8 × index` (`0x0018AA00`, `0x001E6070`-`0x001E60CD`).

Otherwise `0x001E3EB0(model, +0xD4, +0xD0, 1)` picks it from the same index, with no sampler state built: the
same qword when the object's `+0xD4` is 1, else the qword at `[0x01F7E340] + 0x60 + 8 × index` (`0x0018A9E0` with
1, `0x001E3EC0`-`0x001E3F62`).

## Layouts

Probe (`0x001AA840`), pointed to from manager `+0xF0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `vec` | variants | `0x30` bytes each; `+0x08` vector of texture pointers, slots 0-5 used (12 in variant 0) |
| `+0x20` | `f32` | x | cubeMapConfigs.txt; default 80 |
| `+0x24` | `f32` | y | default 2 |
| `+0x28` | `f32` | z | default 60 |
| `+0x2C` | `f32` | radius | 0 = inverse-distance probe |
| `+0x30` | `i32` | weight | at least 1 |
| `+0x34` | `f32` | current weight | `0x001ABF50` |
| `+0x38` | `u32` | index |  |
| `+0x3C` | `u32` |  | value 1: set by `0x001AA840` |
| `+0x40` | `u8` | enabled | 1 |
| `+0x44` | `u32` | variant | the _e&lt;v&gt; set in use |

```python
cubeMapConfigs.txt, CRLF text
<count>
then per probe: <x> <y> <z> <weight> <radius>, one value per line
```

## Shipped data

Measured over the archive. [`map-cubemaps-rows.tsv`](map-cubemaps-rows.tsv) has one row per probe of every map, 770 rows: the map, its folder, the probe index, x, y, z, weight and radius as the file gives them, the weather slots that ship both the environment and the irradiance texture for that probe, the slots with an `_e1` variant, and the first 16 hex digits of the file's SHA-256 on its first row.

| Fact | Value |
|---|---|
| `cubeMapConfigs.txt` files | 451, one per map folder under `gamedata/d3d11/artdata/map/`, 31 to 271 bytes, all CRLF |
| configs a zone can load | all 451: each sits in a map folder that a zone pack path names (kind 4, after the five swaps of [naming the map](../World-Areas-And-Travel/map-art.md#naming-the-map)). The two map folders no pack path names, `alc02/alc0201` and `frs01/frs0109` (`frs0109` loads `frs0101`'s art), hold no config |
| probes per map | 1 (267 maps), 2 (108), 3 (44), 4 (18), 5 (6), 6 (4), 7 (3), 8 (1) |
| probe count against textures | matches the highest texture probe index + 1 in all 451 maps |
| weight field | 1 in 767 probes; 2, 25 and 30 once each |
| radius field | 0 in 736 of the 770 probes; the other 34 range from 0.2 to 103.3 |
| cubemap textures | 4,610 in the maps' `tex` folders: 2,296 `cubemap_<p>_<w>`, 2,296 `cubemap_irr_<p>_<w>`, 9 of each with `_e1` |
| weather slots | 1 to 3 |
| maps with `_e1` variants | `bhm0201`, `glf0104`, `rbn0108` |

### Columns of map-cubemaps-rows.tsv

| Column | Holds |
|---|---|
| `e1_slots` | the weather slots, separated by spaces, for which the map's `tex` folder holds both `cubemap_<p>_<w>_e1` and `cubemap_irr_<p>_<w>_e1` for the row's probe `p`; `1 2 3` on probe 0 of `bhm0201`, `glf0104` and `rbn0108`, `-` on the other 767 rows |
| `file_sha256_16` | the first 16 hex digits of the SHA-256 of the map folder's `cubeMapConfigs.txt`, on the map's probe-0 row (451 rows); empty on the other 319 |

## Modding notes

- A map's `cubeMapConfigs.txt` must not list more probes than the map has `cubemap_` textures for, or the
  whole file is ignored and every probe stays at (80, 2, 60).
- Provide both the environment and the irradiance texture for each probe and weather slot; a probe
  missing either contributes nothing to a mesh.
- A radius of 0 makes a probe pull by inverse horizontal distance over the whole map; a radius limits it to
  that circle and lets it outrank the radius-0 probes.
- Height plays no part in the weighting.

## Related

- [Texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md): the map-art
  context and load that also register the cubemaps.
- [Weather](../World-Areas-And-Travel/weather.md): the weather slot that picks the cubemap set.
- [Render parameters and shader assets](render-parameters-and-shader-assets.md): the map parameters
  beside the cubemap intensity.
- [Character render object](character-render-object.md): the character side of the shader bindings.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 4 calls with 1 other topic</summary>

**Platform** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x0016D6D0` | is called by | `0x0019CC50`, `0x001B1960` |
| `0x0016DA60` | is called by | `0x0019CC50`, `0x001B1960` |

</details>
