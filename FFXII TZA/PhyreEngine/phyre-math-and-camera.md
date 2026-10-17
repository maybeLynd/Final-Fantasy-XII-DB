---
title: "Phyre math and camera: the matrix helpers, the renderer's camera matrices, node and bounds transforms, and the light and shadow terms"
kind: "system"
category: "PhyreEngine"
addresses: "005DFCD0, 005DFDE0, 005EB670, 006107F0, 00185AF0, 001871B0, 0060CE50, 006A0E10, 006045E0, 005FD810, 005DC040, 0060E410, 0067F280, 005FF5A0, 006C18D0, 00606BE0, 006073D0, 0018A4A0, 01F2ED48, 01F2EDA8"
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
| `005DFCD0(m, out, p)` | transforms the point `p` (w = 1): `out = p.x·row0 + p.y·row1 + p.z·row2 + row3`, three floats |
| `005DFDE0(m, out, v)` | transforms the 4-vector `v` through the first three columns and copies `v.w` |
| `005EB670(out, m)`, `006107F0(out, m)` | transpose a 4×4 matrix |
| `001871B0(out, m)` | affine inverse: inverts the upper 3×3 through its cofactors and determinant and negates the translation through it. It writes only the three float lanes of each row; the w lanes (`+0x0C`, `+0x1C`, `+0x2C`, `+0x3C`) are copied from stack slots it never sets (`00187417`–`00187448`), so its output must not be used as a full 4×4 |
| `00185AF0(out, m)` | that inverse as a 4×4 matrix with the last column `(0, 0, 0, 1)` |
| `0018A4A0(out, camera)` | copies the `0xC0` bytes of a `PCamera`; the script getter `00678140` uses it |

### The renderer's camera

`0060CE50(renderer, camera)` stores the camera at `+0xA8` and builds two matrices:

1. The camera-to-world matrix at `+0xB0`: the camera's `m_localToWorldMatrix` (`+0xB0` of the
   camera) when it has one, expanded from 4×3 to 4×4; otherwise the affine inverse (`00185AF0`) of its
   `m_viewMatrix` (`+0x00`).
2. The view matrix at `+0xF0`: the affine inverse of the first (`00187460`).

It then clears `+0xA0`. Six game functions call it, among them `00187950`, `001E2AF0` and
`001F06D0`.

### Node world matrices

`006A0E10(node, out)` copies the node's `m_localMatrix` (`+0x20`) and multiplies it by the local
matrix of each parent in turn (`m_parent` at `+0x08`, `00185100`), so the result is the node's
matrix in world space.

### Mesh-instance bounds

A `PMeshInstanceBounds` keeps a minimum corner at `+0x00`, a size at `+0x18`, the world matrix at
`+0x10` (`m_worldMatrix`) and its mesh instance at `+0x28`.

- `005DC040(bounds, meshInstance)` attaches new bounds: it takes the instance's world matrix
  (`+0x08`) and the instance, copies corner and size from the bounds the instance already has
  (`m_bounds`, `+0x38`) or zeroes them, and becomes the instance's `m_bounds`.
- `0060E410(bounds, corner, size)` sets the corner and size.
- `006045E0(bounds, &min, &max)` gives the world-space box: it expands the 4×3 world matrix to 4×4
  (identity when there is none) and transforms the box with `005FD810`, which puts all eight corners
  through the matrix and keeps the smallest and largest of each axis.

### Look-at

`0067F280(matrix, target)` is a `PWorldMatrix` script method registered by `0067E6C0`. It rebuilds
the 4×3 matrix with the look-at builder `001EB4B0`, aimed at the point at `+0x20` of its second
argument. `001EB4B0(out, eye, target, up)` normalises the direction from eye to target, takes the
side axis as the normalised cross product of that direction and `up`, the new up axis as the cross
product of side and direction, and writes side, up, the negated direction and the eye as the four
rows.

### Light attenuation

`005FF5A0(&a, &b, &c, &d, light)` computes the four terms a shader uses to fade a light:

- Range: for a point light (type object `01F2ED48`, `PointLight`) or a spot light (`01F2EDA8`,
  `SpotLight`), `a = −1 / (outer² − inner²)` and `b = 1 + inner² / (outer² − inner²)`, from
  `m_innerRange` (`+0x34`) and `m_outerRange` (`+0x38`), so `a·d² + b` is 1 at the inner range and 0
  at the outer. Other lights get `a = 0`, `b = 1`.
- Cone: for a spot light, with `ci = cos(m_innerConeAngle − 1e-6)` (`+0x28`) and
  `co = cos(m_outerConeAngle + 1e-6)` (`+0x2C`), `c = −1 / (co − ci)` and `d = co / (co − ci)`, so
  `c·cosθ + d` is 1 at the inner angle and 0 at the outer. Other lights get `c = 0`, `d = 1`.

### Lights and shadow types

`006C18D0(lightType, shadowType)` returns true for the pairs the renderer supports: a spot light
(`01F2EDA8`) with `PCFShadowMap` (`01F2EDE8`), and a directional light (`01F2ED68`) with `CascadedShadowMap`
(`01F2EE08`) or `CombinedCascadedShadowMap` (`01F2EE28`). Point lights take no shadow type.
`006B9CF0` calls it.

### Shadow-split distances

`00606BE0(shadowCaster, out)` writes the far planes of up to four shadow splits as one 4-vector:
the splits are the caster's `PShadowSplit` records (`+0x10` count, `+0x18` data, `0xE8` bytes each)
and `m_farPlane` is the split's `+0xC8`. A split the caster does not have gives 100000.0. The
shader-parameter evaluator `00600F30` uses it for parameter type `0xD8`, passing the light's
`m_shadowCaster` (`+0x18`).

### LOD blend weight

`006073D0(lod, i)` returns the address of element `i` of the array of 12-byte elements at
`+0x20`/`+0x28` (the inline slot when there is one element). The shader-parameter evaluator
`00600F30` reads its first float as the LOD blend weight, the value the `LOD_BLEND` context switch
tests.

## Layouts

`RendererCamera` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xA0` | `u64` | cleared | zeroed by `0060CE50` |
| `+0xA8` | `void*` | camera | the PCamera |
| `+0xB0` | `f32[16]` | cameraToWorld | camera space to world |
| `+0xF0` | `f32[16]` | view | world to camera space |

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
| `01F2ED48` | `PointLight` light-type object |
| `01F2ED68` | `DirectionalLight` light-type object |
| `01F2EDA8` | `SpotLight` light-type object |
| `01F2EDE8` | `PCFShadowMap` shadow-type object |
| `01F2EE08` | `CascadedShadowMap` shadow-type object |
| `01F2EE28` | `CombinedCascadedShadowMap` shadow-type object |

## Modding notes

- A light whose inner and outer ranges are equal divides by zero in `005FF5A0`; keep the outer range
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
