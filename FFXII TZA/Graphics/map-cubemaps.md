---
title: "Map cubemaps: the reflection probes, cubeMapConfigs.txt and how map models pick four of them"
kind: "system"
category: "Graphics"
addresses: "01F811C8, 001AD440, 001A5B30, 001ABC80, 001ABCE0, 001AC810, 001AA840, 001AC480, 001AD130, 001ACF80, 001AC4B0, 001ABF50, 001AA3D0, 001AD470, 001AC670, 001AC720, 001AC6F0, 001E4000, 001AD670, 001E6480, 001E6040"
---

## What the player sees

Shiny map surfaces such as polished floors, metal and water reflect a picture of their surroundings, and
lit surfaces pick up ambient colour from them. The pictures are cubemaps captured at a few points in each
map, one set per weather slot. A surface blends the probes nearest to it, so the reflection changes as one
walks from one part of a map to another.

## How it works

### The probe manager

`001AD440` returns the probe manager `[01F811C8]`. Its probes are a vector of pointers at `+F0`<sub>h</sub>. When a
probe index is asked for that does not exist yet, `001AC810(manager, index)` appends probes up to it, each
built by `001AA840(probe, index, 80.0, 2.0, 60.0, 1, 0)`: position (80, 2, 60) at `+20`<sub>h</sub>, radius 0 at
`+2C`<sub>h</sub>, weight 1 at `+30`<sub>h</sub>, its index at `+38`<sub>h</sub>, enabled byte `+40`<sub>h</sub> = 1 and variant 0 at `+44`<sub>h</sub>.
A probe owns a vector of `30`<sub>h</sub>-byte variants (`001AD0C0`), each with a vector of six texture pointers.

`001AD3E0`, from the start-up burst `0017D4C0`, builds the manager on first use: `258`<sub>h</sub> bytes,
constructed by `001AA9E0`, which:

- empties the map at `+08`<sub>h</sub> and the vectors at `+F0`<sub>h</sub>, `+110`<sub>h</sub> and `+140`<sub>h</sub>, and clears the bytes
  `+130`<sub>h</sub>, `+244`<sub>h</sub> and `+250`<sub>h</sub>;
- lays down the developer capture settings: step `+A8`<sub>h</sub> = −2, `+B8`<sub>h</sub> = 12, `+BC`<sub>h</sub> = 1, `+1E0`<sub>h</sub> =
  180, `+1E4`<sub>h</sub> = 3, `+1E8`<sub>h</sub> = 0.785 and `+24C`<sub>h</sub> = `400`<sub>h</sub>, with five status strings at `+44`<sub>h</sub>,
  `+64`<sub>h</sub>, `+84`<sub>h</sub>, `+204`<sub>h</sub> and `+224`<sub>h</sub> (`"None"`, `"Original"`, `"Final"`, `"Current status"`);
- ends with `001AD510(manager, manager + F0h)`, which keeps the probe vector at `+E8`<sub>h</sub> and sets each
  probe's variant `+44`<sub>h</sub> to the manager's `+C0`<sub>h</sub>, or 0 when that is negative or not below the
  probe's variant count.

While the step `+A8`<sub>h</sub> stays negative the capture code does nothing to the picture. The render pass
`00187950` runs `001AC7C0` each frame, which, when byte `+A4`<sub>h</sub> is set and the step is −2, sets the
step to −1 and calls `001EF540(1)` on the shadow object (`001F0850`). `001ACF10(manager, format)`, from
`00186CD0`, keeps the format at `+248`<sub>h</sub> and creates two 512 × 512 targets at `+D0`<sub>h</sub> and `+C8`<sub>h</sub>
(`001EE040`).

### Registering the textures

When a map's art loads, `001A5B30` walks the textures of the map's asset list (context `+78`<sub>h</sub>) and looks
for `cubemap_` in each name (`001A5D3E`). The name is matched against four forms:

| Name | Registered by | Slot |
|---|---|---|
| `cubemap_<p>_<w>.dds.phyre` | `001ABC80(manager, texture, p, w)` | `2w − 2` of variant 0 |
| `cubemap_irr_<p>_<w>.dds.phyre` | `001ABCE0` | `2w − 1` of variant 0 |
| `cubemap_<p>_<w>_e<v>.dds.phyre` | `001ABC80` with variant `v` | `2w − 2` of variant `v` |
| `cubemap_irr_<p>_<w>_e<v>.dds.phyre` | `001ABCE0` with variant `v` | `2w − 1` of variant `v` |

`p` is the probe index and `w` the weather slot, 1 to 3. `001AD7B0` and `001AD6E0` store the texture,
adding variants as needed. Both registrars also set byte `2w − 2` or `2w − 1` of the probe's first
variant record. The irradiance map is the texture the shader reads as `IrrCubeMap`.

### cubeMapConfigs.txt

After the scan, `001A5B30` runs `001AC480` on the manager, which calls `001AD130(manager, manager +
16Ch)` with the map name kept there and sets the manager's byte `+250`<sub>h</sub>; `01DFE191` then records whether
any probe exists. `001AD130`
files a whole-file read of `/GameData/D3D11/ArtData/map/<map>/cubeMapConfigs.txt` (`008F6D08`, through
`001A1220` and `001A0BB0`) with the completion `001AD450`, which runs `001ACF80`. That finds the pending
request whose name matches the map name at context `+241`<sub>h</sub>, parses the text with `001AC4B0`, sets the
manager's byte `+130`<sub>h</sub> and frees the text.

`001AC4B0(manager, text)` reads with `%d` and `%f` (`008F6D3C`, `008F6D40`), skipping the CR and LF
after each value:

1. the probe count; when it exceeds the probes already registered, nothing is read;
2. per probe, in index order: x, y, z (`+20`<sub>h</sub>), the weight (`%d`, `+30`<sub>h</sub>, raised to 1 when below 1)
   and the radius (`%f`, `+2C`<sub>h</sub>). A failed read stops the parse.

### Picking probes for a point

`001ABF50(manager, indices[4], weights[4], point)` returns indices and weights of 0 while the manager's
byte `+244`<sub>h</sub> is set or its `+A8`<sub>h</sub> is −1 or above. Otherwise the indices start at 4 (none) and the
weights at 0, and every enabled probe is weighed, with `d` the distance from the point in the horizontal
plane (x and z):

- a probe with radius 0 gets `weight / d` (1 when `d` is 0);
- a probe with a radius gets `1 − min(d, radius) / radius`.

When the radius probes sum above 1 they are scaled to sum to 1. The radius-0 probes then share what is
left, `1 − sum`, in proportion to their values. The probe pointers are copied to the vector `+110`<sub>h</sub> (sized by
`001AB0F0`) and sorted by weight, highest first (quicksort `001AA3D0` with the comparator `001AD470`), and the first four are returned with their
indices `+38`<sub>h</sub> and weights `+34`<sub>h</sub>. A probe whose byte `+40`<sub>h</sub> is clear is returned with weight 0.

`001AC670(manager, i)` and `001AC720(manager, i)` return probe `i`'s environment and irradiance texture
for the current weather slot (`00265920`, [weather](../World-Areas-And-Travel/weather.md)) in its variant
`+44`<sub>h</sub>. `001AC6F0` returns its radius.

### Binding to map materials

`001E4000`, called from the map-art load, builds a `220`<sub>h</sub>-byte record of shader parameter handles for
every material of every mesh of a map model: 67 lookups by name through `0018D240`, among them
`EnableCubeMap`, `CubeMap0`-`CubeMap3`, `CubeMapWeight0`-`CubeMapWeight3`, `IrrCubeMap0`-`IrrCubeMap3`,
`cubemapIntensity` and `cubemapFactor`. It marks the model ready (`+250`<sub>h</sub>).

`001AD670(manager, off)` stores `off` in the manager's byte `+244`<sub>h</sub> and runs `001E6480` on every map model
of the map-art context (`001A7600`). For each mesh of a ready model, `001E6480`:

1. takes the centre of the mesh's bounds (`006045E0`) and asks `001ABF50` for four probes, kept at the
   model's `+220`<sub>h</sub> (weights) and `+230`<sub>h</sub> (indices);
2. adds up the weights of the four probes that have both textures, and remembers the last of them whose
   doubled radius is below 0.01, so a radius-0 probe;
3. when it found one and every probe with both textures has a doubled radius of at most 0.01, or not above
   the mesh object's `+18`<sub>h</sub> or `+20`<sub>h</sub>, or the object has `+18`<sub>h</sub>, `+1C`<sub>h</sub> or `+20`<sub>h</sub> above 30, that
   probe gets weight 1 and the other three 0;
4. otherwise divides each weight by the total, or sets it to 0 when the total is 0.01 or less;
5. binds `CubeMapN` and `IrrCubeMapN` for each material through `001E6040` and writes `CubeMapWeightN`
   into the material's parameter buffer at the handle's offset (`u16 +10h`), or 0 while `+244`<sub>h</sub> is set.

`001E6040(model, buffer, handle)` binds a texture with a sampler state built by `001E3EB0`, or, when the
model's byte `+218`<sub>h</sub> is set, one of four presets of `[01F7E340]` (`0018AA00`) chosen by the filter
mode.

## Layouts

Probe (`001AA840`), pointed to from manager +`F0`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `vec` | variants | `30`<sub>h</sub> bytes each; +`08`<sub>h</sub> vector of six texture pointers |
| `20`<sub>h</sub> | `f32` | x | cubeMapConfigs.txt; default 80 |
| `24`<sub>h</sub> | `f32` | y | default 2 |
| `28`<sub>h</sub> | `f32` | z | default 60 |
| `2C`<sub>h</sub> | `f32` | radius | 0 = inverse-distance probe |
| `30`<sub>h</sub> | `i32` | weight | at least 1 |
| `34`<sub>h</sub> | `f32` | current weight | `001ABF50` |
| `38`<sub>h</sub> | `u32` | index |  |
| `40`<sub>h</sub> | `u8` | enabled | 1 |
| `44`<sub>h</sub> | `u32` | variant | the _e<v> set in use |

```python
cubeMapConfigs.txt, CRLF text
<count>
then per probe: <x> <y> <z> <weight> <radius>, one value per line
```

## Shipped data

Measured over the archive:

| Fact | Value |
|---|---|
| `cubeMapConfigs.txt` files | 451, one per map folder under `gamedata/d3d11/artdata/map/`, 31 to 271 bytes, all CRLF |
| probes per map | 1 (267 maps), 2 (108), 3 (44), 4 (18), 5 (6), 6 (4), 7 (3), 8 (1) |
| probe count against textures | matches the highest texture probe index + 1 in all 451 maps |
| weight field | 1 in 767 probes; 2, 25 and 30 once each |
| radius field | 0 in 736 of the 770 probes; the other 34 range from 0.2 to 103.3 |
| cubemap textures | 4,610 in the maps' `tex` folders: 2,296 `cubemap_<p>_<w>`, 2,296 `cubemap_irr_<p>_<w>`, 9 of each with `_e1` |
| weather slots | 1 to 3 |
| maps with `_e1` variants | `bhm0201`, `glf0104`, `rbn0108` |

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
