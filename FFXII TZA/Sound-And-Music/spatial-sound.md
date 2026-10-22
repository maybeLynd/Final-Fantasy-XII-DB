---
title: "Spatial sound: the listener, the shapes a sound source can take, and how distance and shape set its volume and direction"
kind: "system"
category: "Sound and music"
addresses: "0x007BBFB0, 0x02EADE08, 0x007EF630, 0x00362850, 0x007F0320, 0x007F25E0, 0x002DE800, 0x007A5E50"
---

## What the player sees

- A waterfall or machine gets louder as the party approaches and sounds from its side of the screen.
- Ambient loops play the same everywhere in an area.
- Sounds are heard from a point near the party leader, pulled a little toward the camera, facing where the camera looks.

## How it works

### The source classes

Every placed sound is a source object of the driver's `SQEX::Sd::Lay` layer. The factory `0x007BBFB0` builds one by the
record's type word:

| Type | Class | Built by the game |
|---:|---|---|
| 1 | `DynamicSound` | yes: a moving source |
| 2 | `AmbientSound` | yes: no position |
| 3 | `DirectionSound` | no |
| 4 | `PointSound` | no |
| 5 | `PolygonSound` | yes: an outline of points |

The only record builder `0x00221940` handles types 1, 2, 4 and 5 (`0x002219BF`-`0x002219E0`), and the only writer of the type,
`0x002DE800`, never stores 3 or 4, so `PointSound` and `DirectionSound` are never built. Each class overrides two
computations of the base `SoundSourceObject`: slot 34 finds where the source is and whether it is in range, and slot 35
works out how it sounds from the listener.

### The listener

The listener is one `0xA0`-byte object whose pointer is at `0x02EADE08` (`0x007BB610`), built once by `0x007BB620`:

1. `0x00362850` places it each update: at the party's focus character, moved 0.3 of the way toward the camera in the
   horizontal plane only; the factor is `0x022CBB28`, set by `0x00362F70` from `0x0215EFD0` = 0.3 (`0x002DE360`) clamped to 0-1.
2. Its front is the camera's target minus its eye (`0x003CBFA0`), and its up is fixed at (0, 1, 0) (`0x00211340`).
3. Lay action 2, `0x007EF630`, stores them and builds the world-to-listener matrix with `0x007EF3B0`, the right-handed
   builder the game selects (`0x002108CA`).

`0x007EF100` builds the listener with identity axes. Lay action 1 sets it from a position and two direction vectors,
which `0x007EF790` normalises; actions 3 and 4 set it from a 4 x 4 matrix, inverted first by `0x007A5780` when the
action's byte `+0x08` is 0, and `0x007EF580` stores it. Each pass, `0x007EF8F0` (from `0x007BB670`) stores the listener's
movement since the last pass and keeps the new position.

### Range and nearest point

| Class | Slot 34 |
|---|---|
| `AmbientSound` | always in range, at the listener (`0x007F1D10`) |
| `DynamicSound` | out of range and stopped when its range is 0 or less (`0x007F144E`-`0x007F1457`); otherwise in range while its distance is below the range |
| `PolygonSound` | finds the nearest point of its outline, below; out when the range is 0 or there are no points (`0x007F260E`, `0x007F261C`) |

`DynamicSound` reads its range and settings once from the sound's bank record: range `+0x1C`, 30.0 in every shipped
sound (`0x007F13EC`).

A `PolygonSound` outline is drawn by its mode byte `+0x104` (`0x007F25E0`):

| Mode | Shape |
|---:|---|
| `0` | the nearest point |
| `1` | line segments |
| `2` | a triangle strip |
| `3` | a triangle fan |
| `4` | a triangle list |

For a triangle it drops the listener onto the triangle's plane; when that point is inside, the plane distance counts,
and otherwise the three edges are tried (`0x007F7440`, `0x007F7570`). Distances are full 3-D, through the lane mask
`(1, 1, 1, 0)` at `0x00D11570`. When the listener stands inside the nearest triangle, the sound has no direction
(`0x007F20E0`).

### Volume and direction

`0x007F0320(rel, range, inner, k, curve)` turns the source's position in listener space into a gain and a pan:

1. With `d` the distance, the gain is 1 inside `inner`, and otherwise `(range - d) / (range - inner)`, floored at 0
   (`0x007F03AA`-`0x007F03E8`).
2. The gain then goes through curve `curve` of the configuration file's `curv` chunk (`0x007ADC40`, `0x007AE260`). The
   curve number is byte `+0x21` of the sound's bank record.
3. The pan is `atan2(x, -z) / pi`: 0 straight ahead, +0.5 to the right (`0x007F0482`-`0x007F0487`).
4. The directionality is `1 - (1 - t) * k`, with `t` the horizontal distance past `inner` as a share of the rest of the
   range, capped at the horizontal distance over 1.0 (`0x02EAD3F0`) and clamped to 0-1. The vertical pan is always 0.

`AmbientSound` gets gain 1 and no direction (`0x007F1CE0`). Each pass the tick `0x007F0820` sends the sound its own volume
ramp times the gain (`0x007F0C49`-`0x007F0CA5`) and the pan and directionality (`0x007F0D4E`). It also sends three distance
values the sound's parameters can read: the distance, `distance / range` and the share past `inner`
(`zeroone_distance` and `zeroone_distance_rate` read the first two, `0x007E7090`). With directionality 0 every speaker
gets the same level, and with 1 the sound is fully directional ([Sound effects](sound-effects.md)).

### From a request to a source

`0x002DE800(position, source record)` fills the descriptor block at `0x0215E710` from the record's shape byte `+9`:

| Shape | Source | Outline |
|---:|---|---|
| `0` | `PolygonSound` | an ellipse of 13 triangles with half-sizes `+0x30`, `+0x34`, turned by `+0x50` |
| `1` | `PolygonSound` | a rectangle of half-sizes `+0x30`, `+0x34` |
| `2` | `PolygonSound` | a line through the record's points |
| `3` | `AmbientSound` | none |
| `4` | `DynamicSound` | none; its range comes from the bank |

`0x002DE420` writes the outline for shapes 0 and 2, the ellipse, and 1, the rectangle; it writes nothing for any other
shape. The ellipse is the centre and 14 points round it, 15 in all, and the rectangle the centre and its four corners with the first repeated, 6 in all (`0x002DEA9A`-`0x002DEB00`). It takes the range from
record `+0x38`, or 200.0 with the outline lowered by 100 when that is 0 or less (`0x0215EF40`).

The starting volume is byte `+0x19` over 127 times the weather slot's percentage over 100 (`0x00221C11`-`0x00221C42`).
The sources come from three places:

- **Map emitters** (`0x003638B0`, [Map sounds](map-sounds.md)): the 456 map packs' emitters use shape 0 1,364 times,
  1 108 times, 2 400 times and 3 454 times, and shape 4 never.
- **Character sounds** (`0x0046C8F0`, `0x0046CC70`, [Animation sounds](animation-sounds.md)): an ellipse of half-size 0.1
  from the template at `0x022CBAB0` (`0x00362F70`), in effect a point.
- **Moving sounds**: `0x00332C40` and `0x003B99D0` force shape 4 (`0x00332E30`-`0x00332E38`, `0x003B9B6C`-`0x003B9B74`).

The template copy `0x003617B0` fills a request from the character template at `0x022CBAB0` for `0x00332C40`, `0x003B99D0`
and `0x0046C8F0`, with the map's sound volume `0x022CBA94` as byte `+0x19`; `0x00332C40` and `0x003B99D0` clamp their
volumes to 0-127 with `0x0046C8D0`. `0x00361BF0` and `0x00361CF0` work out a pan byte and a volume for a point seen from the listener at
`0x022CBB00` (`0x00361810`), and scale the volume by `0x022CBA94 / 127`. `0x00332FA0` stops every sound of an effect
element's list that still plays, through a 16-frame delayed stop (`0x003B3EA0`), and empties the list.

`0x00361750` is the same template copy except for two floats: `0x003617B0` stores its fifth argument at
`+0x10` and its sixth at `+0x1C`, while `0x00361750` stores the float `0x022CBB24` at `+0x10` and its
reciprocal at `+0x1C`. The character sounds call it, `0x0046C8F0` at `0x0046CA4F` and `0x0046CC70` at
`0x0046CF71`; `0x0046C8F0` also calls `0x003617B0` (`0x0046CB1D`).

### The layer's pools

`0x007A5B50` starts the layer from the block `0x00210760` fills (`0x002108AD`-`0x002108BD`): one page, 128 sources and 512
actions.

| Pool | Built by | Holds |
|---|---|---|
| actions | `0x007BAC80` | 512 `0x50`-byte `Lay` actions at `0x02EADE00`, in two queues (`0x007BAB30`) |
| pages | `0x007BB6B0` | one `0x60`-byte `Lay::Page` (`0x007BB7E0`; `0x007BB830` destroys it) with a 128-handle list (`0x007BBD40`, `0x007BBC30`) |
| sources | `0x007BC400` | 128 blocks of `0x230` bytes, their list (`0x007BC2F0`) and two per-pass arrays at `0x02EADED8` and `0x02EADEE0` |

`0x007A5A00(page, out, ...)`, from the game's `0x00221940`, takes the page (`0x007BB690`) and calls `0x007BBAB0`, which builds a
source through the factory `0x007BBFB0` and appends its handle to the page (`0x007BB9A0`); when the page is full it stops
the new sound over 0.1 s (`0x007BBB45`). Lay action 0 runs slot 11 with 0 on every source of a page (`0x007BBB70`).

The source classes are built over the shared base `0x007EF910` (`0x007EFA30` destroys it), which sits on the
`Lay::SoundObject` base `0x007F7360` (`0x007F7380`): `DynamicSound` `0x007F0FD0`, `PointSound` `0x007F1760`, `AmbientSound`
`0x007F1C50` and `DirectionSound` `0x007F1D40`. `0x007EFEF0` gives a source's ramped volume times its `+0x78`, which
`0x007F0610` sets.

### The update pass

The `Lay` thread `0x007A5E50` runs every 32 milliseconds:

1. It applies the queued actions (`0x007BAEC0`) and the listener's movement (`0x007BB670`).
2. It runs every source's slot 34; a source out of range for good is stopped (`0x007EFB60`).
3. It runs every source's tick (`0x007F0820`), which starts, stops and updates its sound.

Steps 2 and 3 are the source pass `0x007BC4F0`. Between them it collects every source whose slot 6 answers true, whose
`+0xE0` is set and `+0xE1` clear and that is not in state 2 or 3, into a 32-byte record each (`0x02EADEE0`); it hands
them to the layer's callback (`0x02EADE28`, a `SoundObjectManagerCallback` that `0x007A5AA0` forwards to the object at
`0x02EACFA0`) and stores each answer back in its source (`0x007EFB20`, `+0xD0`-`+0xF8`).

After the ticks it frees the sources in state 5. The thread then runs `0x007BB780`, which runs `0x007BBD60` on every
page, which drops the handles of sources that have ended.

Only `DynamicSound` moves: action 8 from `0x00332C40` sets its new position each call while its sound plays (`0x007F1310`).
Its Doppler step (speed of sound 340.29, `0x01CB9B30`) needs bank record `+0x48`, which is 0 in every shipped sound, and its
low-pass stays at 1.0.

## Shipped data

| | |
|---|---|
| distance curve | `sead.win.config` holds one curve, linear from (0, 0) to (1, 1); every sound's curve number is 0 |
| so the distance gain | `(range - d) / (range - inner)` |
| `DynamicSound` | range 30.0, inner 0, directionality factor 0, no Doppler, in all 13,150 sound records |

## Modding notes

- A map emitter's range and shape decide where its sound is heard; a range of 0 or less is never heard.
- `0x002DE800` remaps only shapes 0-4; a shape byte of 5 or more reaches the factory as that type number.
- A non-linear distance curve needs a new `curv` element and a curve number in the sound's bank record.
- The listener's pull toward the camera is the float at `0x0215EFD0`.

## Related

- [Sound effects](sound-effects.md) - the play call and the pan mapping.
- [Map sounds](map-sounds.md) - the map emitters.
- [Animation sounds](animation-sounds.md) - character sounds.
- [Sound engine configuration](sound-engine-config.md) - the `curv` chunk.
