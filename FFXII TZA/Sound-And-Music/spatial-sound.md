---
title: "Spatial sound: the listener, the shapes a sound source can take, and how distance and shape set its volume and direction"
kind: "system"
category: "Sound and music"
summary: "How a placed sound is heard: the five sound-source classes and the three the game builds, where the listener stands and faces, how each shape finds its nearest point and whether it is in range, the shared distance-to-volume and direction formula with the shipped linear curve, the distance values a sound can read, how map, character and moving sounds become sources, and the 32-millisecond pass that updates them."
addresses: "007BBFB0, 02EADE08, 007EF630, 00362850, 007F0320, 007F25E0, 002DE800, 007A5E50"
---

## What the player sees

- A waterfall or machine gets louder as the party approaches and sounds from its side of the screen.
- Ambient loops play the same everywhere in an area.
- Sounds are heard from a point near the party leader, pulled a little toward the camera, facing where the camera looks.

## How it works

### The source classes

Every placed sound is a source object of the driver's `SQEX::Sd::Lay` layer. The factory `007BBFB0` builds one by the
record's type word:

| Type | Class | Built by the game |
|---:|---|---|
| 1 | `DynamicSound` | yes: a moving source |
| 2 | `AmbientSound` | yes: no position |
| 3 | `DirectionSound` | no |
| 4 | `PointSound` | no |
| 5 | `PolygonSound` | yes: an outline of points |

The only record builder `00221940` handles types 1, 2, 4 and 5 (`002219BF`-`002219E0`), and the only writer of the type,
`002DE800`, never stores 3 or 4, so `PointSound` and `DirectionSound` are never built. Each class overrides two
computations of the base `SoundSourceObject`: slot 34 finds where the source is and whether it is in range, and slot 35
works out how it sounds from the listener.

### The listener

The listener is one `0xA0`-byte object whose pointer is at `02EADE08` (`007BB610`), built once by `007BB620`:

1. `00362850` places it each update: at the party's focus character, moved 0.3 of the way toward the camera in the
   horizontal plane only; the factor is `022CBB28`, set by `00362F70` from `0215EFD0` = 0.3 (`002DE360`) clamped to 0-1.
2. Its front is the camera's target minus its eye (`003CBFA0`), and its up is fixed at (0, 1, 0) (`00211340`).
3. Lay action 2, `007EF630`, stores them and builds the world-to-listener matrix with `007EF3B0`, the right-handed
   builder the game selects (`002108CA`).

### Range and nearest point

| Class | Slot 34 |
|---|---|
| `AmbientSound` | always in range, at the listener (`007F1D10`) |
| `DynamicSound` | out of range and stopped when its range is 0 or less (`007F144E`-`007F1457`); otherwise in range while its distance is below the range |
| `PolygonSound` | finds the nearest point of its outline, below; out when the range is 0 or there are no points (`007F260E`, `007F261C`) |

`DynamicSound` reads its range and settings once from the sound's bank record: range `+0x1C`, 30.0 in every shipped
sound (`007F13EC`).

A `PolygonSound` outline is drawn by its mode byte `+0x104` (`007F25E0`):

| Mode | Shape |
|---:|---|
| `0` | the nearest point |
| `1` | line segments |
| `2` | a triangle strip |
| `3` | a triangle fan |
| `4` | a triangle list |

For a triangle it drops the listener onto the triangle's plane; when that point is inside, the plane distance counts,
and otherwise the three edges are tried (`007F7440`, `007F7570`). Distances are full 3-D, through the lane mask
`(1, 1, 1, 0)` at `00D11570`. When the listener stands inside the nearest triangle, the sound has no direction
(`007F20E0`).

### Volume and direction

`007F0320(rel, range, inner, k, curve)` turns the source's position in listener space into a gain and a pan:

1. With `d` the distance, the gain is 1 inside `inner`, and otherwise `(range - d) / (range - inner)`, floored at 0
   (`007F03AA`-`007F03E8`).
2. The gain then goes through curve `curve` of the configuration file's `curv` chunk (`007ADC40`, `007AE260`). The
   curve number is byte `+0x21` of the sound's bank record.
3. The pan is `atan2(x, -z) / pi`: 0 straight ahead, +0.5 to the right (`007F0482`-`007F0487`).
4. The directionality is `1 - (1 - t) * k`, with `t` the horizontal distance past `inner` as a share of the rest of the
   range, capped at the horizontal distance over 1.0 (`02EAD3F0`) and clamped to 0-1. The vertical pan is always 0.

`AmbientSound` gets gain 1 and no direction (`007F1CE0`). Each pass the tick `007F0820` sends the sound its own volume
ramp times the gain (`007F0C49`-`007F0CA5`) and the pan and directionality (`007F0D4E`). It also sends three distance
values the sound's parameters can read: the distance, `distance / range` and the share past `inner`
(`zeroone_distance` and `zeroone_distance_rate` read the first two, `007E7090`). With directionality 0 every speaker
gets the same level, and with 1 the sound is fully directional ([Sound effects](sound-effects.md)).

### From a request to a source

`002DE800(position, source record)` fills the descriptor block at `0215E710` from the record's shape byte `+9`:

| Shape | Source | Outline |
|---:|---|---|
| `0` | `PolygonSound` | an ellipse of 13 triangles with half-sizes `+0x30`, `+0x34`, turned by `+0x50` |
| `1` | `PolygonSound` | a rectangle of half-sizes `+0x30`, `+0x34` |
| `2` | `PolygonSound` | a line through the record's points |
| `3` | `AmbientSound` | none |
| `4` | `DynamicSound` | none; its range comes from the bank |

The starting volume is byte `+0x19` over 127 times the weather slot's percentage over 100 (`00221C11`-`00221C42`).
The sources come from three places:

- **Map emitters** (`003638B0`, [Map sounds](map-sounds.md)): the 456 map packs' emitters use shape 0 1,364 times,
  1 108 times, 2 400 times and 3 454 times, and shape 4 never.
- **Character sounds** (`0046C8F0`, `0046CC70`, [Animation sounds](animation-sounds.md)): an ellipse of half-size 0.1
  from the template at `022CBAB0` (`00362F70`), in effect a point.
- **Moving sounds**: `00332C40` and `003B99D0` force shape 4 (`00332E30`-`00332E38`, `003B9B6C`-`003B9B74`).

### The update pass

The `Lay` thread `007A5E50` runs every 32 milliseconds:

1. It applies the queued actions (`007BAEC0`) and the listener's movement (`007BB670`).
2. It runs every source's slot 34; a source out of range for good is stopped (`007EFB60`).
3. It runs every source's tick (`007F0820`), which starts, stops and updates its sound.

Only `DynamicSound` moves: action 8 from `00332C40` sets its new position each call while its sound plays (`007F1310`).
Its Doppler step (speed of sound 340.29, `01CB9B30`) needs bank record `+0x48`, which is 0 in every shipped sound, and its
low-pass stays at 1.0.

## Shipped data

| | |
|---|---|
| distance curve | `sead.win.config` holds one curve, linear from (0, 0) to (1, 1); every sound's curve number is 0 |
| so the distance gain | `(range - d) / (range - inner)` |
| `DynamicSound` | range 30.0, inner 0, directionality factor 0, no Doppler, in all 13,150 sound records |

## Modding notes

- A map emitter's range and shape decide where its sound is heard; a range of 0 or less is never heard.
- `002DE800` remaps only shapes 0-4; a shape byte of 5 or more reaches the factory as that type number.
- A non-linear distance curve needs a new `curv` element and a curve number in the sound's bank record.
- The listener's pull toward the camera is the float at `0215EFD0`.

## Related

- [Sound effects](sound-effects.md) - the play call and the pan mapping.
- [Map sounds](map-sounds.md) - the map emitters.
- [Animation sounds](animation-sounds.md) - character sounds.
- [Sound engine configuration](sound-engine-config.md) - the `curv` chunk.
