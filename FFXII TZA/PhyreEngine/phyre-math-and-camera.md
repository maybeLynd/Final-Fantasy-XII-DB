---
title: "Phyre math and camera: the matrix helpers, the renderer's camera matrices, node and bounds transforms, and the light and shadow terms"
kind: "system"
category: "PhyreEngine"
addresses: "0x005DFCD0, 0x005DFDE0, 0x005EB670, 0x006107F0, 0x00185AF0, 0x001871B0, 0x0060CE50, 0x006A0E10, 0x006045E0, 0x005FD810, 0x005DC040, 0x0060E410, 0x0067F280, 0x005FF5A0, 0x006C18D0, 0x00606BE0, 0x006073D0, 0x0018A4A0, 0x01F2ED48, 0x01F2EDA8"
---

## What the player sees

The camera position, the culling boxes of models, the fall-off of point and spot lights and the
distances at which shadow cascades change all come from the helpers on this page. A spot light's
edge softness is the gap between its inner and outer cone angles; a point light fades from full
strength at its inner range to nothing at its outer range.

## How it works

### Vector and matrix helpers

Matrices are 16 floats, row-major, with the translation in the last row.

| Function | What it does |
|---|---|
| `0x005DFCD0(m, out, p)` | transforms the point `p` (w = 1): `out = p.x·row0 + p.y·row1 + p.z·row2 + row3`, three floats |
| `0x005DFDE0(m, out, v)` | transforms the 4-vector `v` through the first three columns and copies `v.w` |
| `0x005EB670(out, m)`, `0x006107F0(out, m)` | transpose a 4×4 matrix |
| `0x001871B0(out, m)` | affine inverse: inverts the upper 3×3 through its cofactors and determinant and negates the translation through it. It writes only the three float lanes of each row; the w lanes (`+0x0C`, `+0x1C`, `+0x2C`, `+0x3C`) are copied from stack slots it never sets (`0x00187417`–`0x00187448`), so its output must not be used as a full 4×4 |
| `0x00185AF0(out, m)` | that inverse as a 4×4 matrix with the last column `(0, 0, 0, 1)` |
| `0x0018A4A0(out, camera)` | copies the `0xC0` bytes of a `PCamera`; the script getter `0x00678140` uses it |

### The renderer's camera

`0x0060CE50(renderer, camera)` stores the camera at `+0xA8` and builds two matrices. Its callers hand it the
camera's `PCamera` part, 8 bytes into a `PCameraPerspective` (`0x001880CD` `lea rdx, [rax + 8]`), so the offsets
here are offsets in that part:

1. The camera-to-world matrix at `+0xB0`: the camera's `m_localToWorldMatrix` (`+0xB0` of the
   camera) when it has one, expanded from 4×3 to 4×4; otherwise the affine inverse (`0x00185AF0`) of its
   `m_viewMatrix` (`+0x00`).
2. The view matrix at `+0xF0`: the affine inverse of the first (`0x00187460`).

It then clears `+0xA0`. Six game functions call it, among them `0x00187950`, `0x001E2AF0` and
`0x001F06D0`.

### The perspective projection

`0x00189C20`, slot 1 of the `PCameraPerspective` vtable (`0x008C5D68`), rebuilds the camera's projection matrix
from its near and far planes, aspect ratio and field of view.

Its seven callers include the render manager's
camera set-up `0x00184CE0`, which stores the vtable (`0x00184D1F`), sets the field of view to pi/4 (45 degrees) and
the scale `+0xD4` to 1.0, then calls it, and `0x006AD750`. With `n` = `+0xC0`, `f` = `+0xC4`, `a` = `+0xC8`, `fov` = `+0xD0` (radians)
and `k` = `+0xD4`, and `c = tan(pi/2 - fov * 0.5)`, the cotangent of half the field of view (`tanf`, the import at
`0x008C2BC0`, through `0x00861F1A`):

```python
x scale   +0x38 = c * k / a
y scale   +0x4C = c * k
z         +0x60 = (n + f) / (n - f)      +0x64 = -1.0
w         +0x70 = 2 * n * f / (n - f)    +0x74 = 0
every other cell of +0x38..+0x77 = 0
```

The matrix is column-major (four columns of four floats from `+0x38`): a right-handed projection that looks
down the camera's -z, with clip-space depth from -1 at the near plane to +1 at the far plane and +y up.

### Node world matrices

`0x006A0E10(node, out)` copies the node's `m_localMatrix` (`+0x20`) and multiplies it by the local
matrix of each parent in turn (`m_parent` at `+0x08`, `0x00185100`), so the result is the node's
matrix in world space.

### Mesh-instance bounds

A `PMeshInstanceBounds` keeps a minimum corner at `+0x00`, a size at `+0x18`, the world matrix at
`+0x10` (`m_worldMatrix`) and its mesh instance at `+0x28`.

- `0x005DC040(bounds, meshInstance)` attaches new bounds: it takes the instance's world matrix
  (`+0x08`) and the instance, copies corner and size from the bounds the instance already has
  (`m_bounds`, `+0x38`) or zeroes them, and becomes the instance's `m_bounds`.
- `0x0060E410(bounds, corner, size)` sets the corner and size.
- `0x006045E0(bounds, &min, &max)` gives the world-space box: it expands the 4×3 world matrix to 4×4
  (identity when there is none) and transforms the box with `0x005FD810`, which puts all eight corners
  through the matrix and keeps the smallest and largest of each axis.

### Look-at

`0x0067F280(matrix, target)` is a `PWorldMatrix` script method registered by `0x0067E6C0`. It rebuilds
the 4×3 matrix with the look-at builder `0x001EB4B0`, aimed at the point at `+0x20` of its second
argument. `0x001EB4B0(out, eye, target, up)` normalises the direction from eye to target, takes the
side axis as the normalised cross product of that direction and `up`, the new up axis as the cross
product of side and direction, and writes side, up, the negated direction and the eye as the four
rows.

### Light attenuation

`0x005FF5A0(&a, &b, &c, &d, light)` computes the four terms a shader uses to fade a light:

- Range: for a point light (type object `0x01F2ED48`, `PointLight`) or a spot light (`0x01F2EDA8`,
  `SpotLight`), `a = −1 / (outer² − inner²)` and `b = 1 + inner² / (outer² − inner²)`, from
  `m_innerRange` (`+0x34`) and `m_outerRange` (`+0x38`), so `a·d² + b` is 1 at the inner range and 0
  at the outer. Other lights get `a = 0`, `b = 1`.
- Cone: for a spot light, with `ci = cos(m_innerConeAngle − 1e-6)` (`+0x28`) and
  `co = cos(m_outerConeAngle + 1e-6)` (`+0x2C`), `c = −1 / (co − ci)` and `d = co / (co − ci)`, so
  `c·cosθ + d` is 1 at the inner angle and 0 at the outer. Other lights get `c = 0`, `d = 1`.

### Lights and shadow types

`0x006C18D0(lightType, shadowType)` returns true for the pairs the renderer supports: a spot light
(`0x01F2EDA8`) with `PCFShadowMap` (`0x01F2EDE8`), and a directional light (`0x01F2ED68`) with `CascadedShadowMap`
(`0x01F2EE08`) or `CombinedCascadedShadowMap` (`0x01F2EE28`). Point lights take no shadow type.
`0x006B9CF0` calls it.

### Shadow-split distances

`0x00606BE0(shadowCaster, out)` writes the far planes of up to four shadow splits as one 4-vector:
the splits are the caster's `PShadowSplit` records (`+0x10` count, `+0x18` data, `0xE8` bytes each)
and `m_farPlane` is the split's `+0xC8`. A split the caster does not have gives 100000.0. The
shader-parameter evaluator `0x00600F30` uses it for parameter type `0xD8`, passing the light's
`m_shadowCaster` (`+0x18`).

### LOD blend weight

`0x006073D0(lod, i)` returns the address of element `i` of the array of 12-byte elements at
`+0x20`/`+0x28` (the inline slot when there is one element). The shader-parameter evaluator
`0x00600F30` reads its first float as the LOD blend weight, the value the `LOD_BLEND` context switch
tests.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PCameraProjection` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xC8` | `f32` | m_aspect | m_aspect (f32), registered by `0x006788C0` (`0x00632960` at `0x0067895A`); the cluster loader binds it by name (`0x0059B430`) in the 247 shipped .phyre files that declare PCameraProjection |
| `+0xCC` | `u8[4]` | bytesCC | the bytes after m_aspect (+`0xC8`) up to the end of the `0xD0`-byte class, where m_FOV of PCameraPerspective starts; no registered member covers it (`0x00678420` registers the `0xD0`-byte class at `0x0067846A`) |

### Camera and bounds records

The structures below are the ones the mechanisms above use.

`RendererCamera` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xA0` | `u64` | cleared | zeroed by `0x0060CE50` |
| `+0xA8` | `void*` | camera | the PCamera |
| `+0xB0` | `f32[16]` | cameraToWorld | camera space to world |
| `+0xF0` | `f32[16]` | view | world to camera space |

A `PCameraPerspective` as `0x00189C20` uses it. Its `PCamera` part starts 8 bytes in, after the vtable, so the
`PCamera` members' offsets in the [field schema](phyre-field-schema.md) are 8 lower than here:

`PCameraPerspective` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x008C5D68` |
| `+0x08` | `f32[12]` | m_viewMatrix | 4 x 3 |
| `+0x38` | `f32[16]` | m_projectionMatrix | written by `0x00189C20` |
| `+0x78` | `f32[16]` | m_viewProjectionMatrix |  |
| `+0xB8` | `void*` | m_localToWorldMatrix |  |
| `+0xC0` | `f32` | m_nearPlane |  |
| `+0xC4` | `f32` | m_farPlane |  |
| `+0xC8` | `f32` | m_aspect | PCameraProjection |
| `+0xD0` | `f32` | m_FOV | radians, the full vertical angle |
| `+0xD4` | `f32` | scale | a factor on both axes' scales |

`PMeshInstanceBounds` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | corner | minimum corner, object space |
| `+0x10` | `void*` | m_worldMatrix | the instance's world matrix |
| `+0x18` | `f32[3]` | size | extent along each axis |
| `+0x28` | `void*` | m_meshInstance | owning PMeshInstance |

## State

| Address | What |
|---|---|
| `0x01F2ED48` | `PointLight` light-type object |
| `0x01F2ED68` | `DirectionalLight` light-type object |
| `0x01F2EDA8` | `SpotLight` light-type object |
| `0x01F2EDE8` | `PCFShadowMap` shadow-type object |
| `0x01F2EE08` | `CascadedShadowMap` shadow-type object |
| `0x01F2EE28` | `CombinedCascadedShadowMap` shadow-type object |

### A static orthographic camera

The C++ initialiser `0x00169580` builds a `PCameraOrthographic` in place at `0x02EA5760`: it constructs the part at
`+0x08` (`0x00184E60`), installs the vtable `0x00902ED8`, sets `+0xC8` and `+0xD0` to 1.0, runs `0x001F0A00` on the object
and registers the exit stub `0x008B7C90`, which only puts back the `PCameraProjection` vtable `0x008C5D50`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA5760` | `void*` | 0 (zero-filled tail of `.data`) | the object's vtable: `0x00902ED8` (`PCameraOrthographic`), then `0x008C5D50` at exit | `0x00169580` (`0x001695A8`); `0x008B7C90` (`0x008B7C97`) | no instruction names it; `0x00169580` passes the object's address to `0x001F0A00` (`0x001695A1`) |
| `0x02EA5828` | `f32` | 0 (zero-filled tail of `.data`) | `+0xC8`, `m_aspect`: 1.0 | `0x00169580` (`0x00169597`) | no instruction names it |
| `0x02EA5830` | `f32` | 0 (zero-filled tail of `.data`) | `+0xD0`, the first member after the `0xD0` bytes of `PCameraProjection`: 1.0 | `0x00169580` (`0x001695AF`) | no instruction names it |

## Modding notes

- A light whose inner and outer ranges are equal divides by zero in `0x005FF5A0`; keep the outer range
  larger. The cone angles are nudged by 1e-6, so equal cone angles give a very steep but finite edge.
- Shadow casters are only accepted on spot and directional lights, and only with the matching shadow
  type.
- A shadow caster with fewer than four splits reports 100000.0 for the missing far planes, so every
  distance falls into an existing split.

## Related

- [Shader variant selection](shader-variant-selection.md): the light code and the `LOD_BLEND` switch these values feed.
- [Phyre frame](the-frame.md): the camera snapshot a frame copies.
- [Phyre field schema](phyre-field-schema.md): the `PCamera`, `PLight`, `PNode` and `PMeshInstanceBounds` members named here.
- [Phyre entities and components](phyre-entities-and-components.md): the world-matrix registry.
