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

## State

### The request block

`0x002DE800` builds every placed-sound request in the block at `0x0215E710`, which `0x002DE360` (from `0x003692D0`) resets.
`0x002DEFA0` (`0x002DEFDF`) and `0x002DF460` (`0x002DF49F`) pass the block's address on, through `0x001DBE00` and `0x001DC190`,
to the record builder `0x00221940`, its only reader. Every field is 0 in the file (the zero-filled tail of `.data`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0215E714`, `0x0215E718` | `f32`, `f32` | 0 | `+0x04`, `+0x08`: the position's y and z | `0x002DE360`, 0 (`0x002DE3A2`, `0x002DE3AC`); `0x002DE800`, the caller's position (`0x002DE872`, `0x002DE87F`) | `0x00221940` (`0x00221B45`, `0x00221B37`, `0x00221C03`, `0x00221BFA`) |
| `0x0215E720` | `f32` | 0 | `+0x10`: the range | `0x002DE360`, 20.0 (`0x002DE376`); `0x002DE800`, record `+0x10` (`0x002DE88C`) | `0x00221940` (`0x00221A3F`, `0x00221B0A`) |
| `0x0215E724` | `f32` | 0 | `+0x14`: the value passed beside the range into the source's creation record (`0x00221A68`, `0x00221B3F`) | `0x002DE360`, 0 (`0x002DE38C`); `0x002DE800`, 0 (`0x002DE894`), or for shape 2 the first float of record `+0x30` (`0x002DE90C`) | `0x00221940` (`0x00221A4A`, `0x00221B13`) |
| `0x0215E728` | `i32` | 0 | `+0x18`: the source type (see The source classes): 5 for shapes 0-2, 2 for shape 3, 1 for shape 4, and the shape byte itself for any other shape | `0x002DE800` (`0x002DE85B`, `0x002DE8C7`, `0x002DE8D2`, `0x002DEB14`) | `0x00221940` (`0x002219BF`) |
| `0x0215E72C` | `i32` | 0 | `+0x1C`: the outline mode a `PolygonSound` keeps at `+0x104`: 1, line segments, for shape 2; 3, a triangle fan, for shapes 0 and 1 | `0x002DE360`, 0 (`0x002DE3B3`); `0x002DE800` (`0x002DEA4D`, `0x002DEB0A`) | `0x00221940`, as a byte (`0x00221A5F`) |
| `0x0215E730` | `i32` | 0 | `+0x20`: the outline's point count: 15 for the ellipse, 6 for the rectangle, the record's points plus one for a line | `0x002DE800` (`0x002DEB00`, `0x002DEA9F`, `0x002DEA57`) | `0x00221940` (`0x00221A47`) |
| `0x0215E734`, `0x0215E744`, `0x0215E754`, `0x0215E764`, `0x0215E774`, `0x0215E784` | `f32[4]` each | 0 | `+0x24` on: the outline's points, 16 bytes each (x, y, z, 1.0); these six are the rectangle's | `0x002DE420`: the rectangle (`0x002DE56B`-`0x002DE61B`) and the ellipse, through the address `0x0215E734` (`0x002DE733`); `0x002DE800`: a line's points (`0x002DE940`-`0x002DE9E6`, `0x002DEA18`-`0x002DEA44`) | `0x00221940`, x, y and z of each point (`0x00221A80`-`0x00221A99`) |
| `0x0215EF38` | `i32` | 0 | `+0x828`: the record's percentage byte for the current weather slot, record `+0x0C` plus the slot from `0x00265920` minus 1 | `0x002DE800` (`0x002DE843`) | `0x00221940`, the starting volume (`0x00221C1D`) |
| `0x0215EF3C` | `i32` | 0 | `+0x82C`: the record's volume byte `+0x19` | `0x002DE800` (`0x002DE84E`) | `0x00221940`, the starting volume (`0x00221C11`) |
| `0x0215EF4C` | `u8` | 0 | `+0x83C`: a byte the reset clears; nothing reads it | `0x002DE360`, 0 (`0x002DE3BF`) | no instruction |

### The character-sound template

`0x00362F70` fills the request template at `0x022CBAB0` and the listener-side constants once; the template copies
`0x00361750` (`0x00361750`-`0x00361782`), `0x003617B0` (`0x003617B0`-`0x003617DA`), `0x00361BF0` (`0x00361C0B`-`0x00361C5B`) and
`0x00361CF0` (`0x00361D0B`-`0x00361D3C`) read the whole template, `+0x00`-`+0x3F`, in four 16-byte loads, and nothing else
reads it.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBAB8` | `u8[8]` | 0 | template `+0x08`-`+0x0F`, zeroed (`0x00363078`) and then overwritten by the stores below | `0x00362F70` | the four template copies |
| `0x022CBAB9` | `u8` | 0 | template `+0x09`, the shape: bit 7 cleared, so shape 0, the ellipse | `0x00362F70` (`0x0036307F`) | `0x00362F70` (the same `and`); the four template copies |
| `0x022CBABA` | `u32` | 0 | template `+0x0A`-`+0x0D`: `0x7F`, 0, 100, 100 | `0x00362F70` (`0x003630DD`) | the four template copies |
| `0x022CBABE` | `u8` | 0 | template `+0x0E`: 100 | `0x00362F70` (`0x003630C1`) | the four template copies |
| `0x022CBAC0` | `f32` | 0 | template `+0x10`: the range, 20.0 | `0x00362F70` (`0x0036308D`, `0x003630EE`) | the four template copies |
| `0x022CBAC8` | `u8[8]` | 0 | template `+0x18`-`+0x1F`: zeroed, then `+0x1B` and `+0x1C` stored below | `0x00362F70` (`0x00363086`) | the four template copies |
| `0x022CBACB` | `u8` | 0 | template `+0x1B`: 100, the pan width `0x00361810` scales (`0x00361891`) | `0x00362F70` (`0x003630E7`) | the four template copies |
| `0x022CBACC` | `f32` | 0 | template `+0x1C`: 0.05 | `0x00362F70` (`0x003630C7`) | the four template copies |
| `0x022CBAD0`, `0x022CBAD8`, `0x022CBAE0`, `0x022CBAE8` | `u8[8]` each | 0 | template `+0x20`-`+0x3F`: 0, so the half-sizes `+0x30` and `+0x34` are 0 and `0x002DE800` raises them to 0.1 (`0x002DEAB8`-`0x002DEACA`) | `0x00362F70` (`0x0036309B`, `0x003630A2`, `0x003630A9`, `0x003630B0`) | the four template copies |
| `0x022CBAA4` | `u8` | 0 | 6: the step by which `0x00361810` moves a request's behind-the-listener amount `+0x2C` toward 64 (behind) or 0, in the range 0-64 (`0x00361B45`-`0x00361B78`) | `0x00362F70` (`0x0036315B`) | `0x00361810` (`0x00361B45`) |
| `0x022CBAA8` | `i32` | 0 | 44: the volume factor at full behind, `(4096 + (44 - 64) x amount) / 4096`, so 2816/4096 at 64 (`0x00361B6F`-`0x00361B90`) | `0x00362F70` (`0x00363165`) | `0x00361810` (`0x00361B6F`) |
| `0x022CBB2C` | `u8` | 0 | 150: the percentage applied to a request's pan width `+0x1B` (`0x003618D4`-`0x003618EB`) | `0x00362F70` (`0x00363102`) | `0x00361810` (`0x00361868`) |

`0x00361810` skips both behind-the-listener steps and uses 100 instead of `0x022CBB2C` while `0x002DEBF0` answers 2 (the
word `0x0215EF48`, `0x00361858`-`0x00361866`, `0x00361B3B`-`0x00361B43`).

### The listener's place

`0x00362850` keeps the game-side listener at `0x022CBB00` as four floats, x, y, z and 1.0, and its facing at `0x022CBA8C`.
The microphone mode `0x022CBA9A` (`set_microphone_pos`, `0x00363B00`) picks where they come from (`0x003629DF`-`0x00362A9A`):

| Mode | Place | Facing |
|---|---|---|
| 0 | the party's focus character (`0x003588B0`, `0x00265020`), moved toward the camera in the horizontal plane as The listener describes (`0x003628B2`-`0x003629D7`) | `atan2` of the character's offset from the camera, x over z (`0x00362918`-`0x00362925`); kept when the two are at one point |
| 1 | the position `set_microphone_pos` stored at `0x022CBB10`, copied whole (`0x00362A83`-`0x00362A9A`) | its value `0x022CBAAC` (`0x00362A8A`-`0x00362A92`) |
| 2 | the camera's position, the fourth row of the camera matrix `0x02AEDEF0` (`0x00202C70`, `0x00362A00`-`0x00362A4A`) | the angle of the matrix's third row (`0x00362A54`-`0x00362A79`) |

In mode 1 and mode 2 the mode 0 result is overwritten. `0x00362F70` starts both at (0, 0, 0, 1.0) and 0. The place is
read through its address by `0x003631B0`, which runs the map's emitters from it ([Map sounds](map-sounds.md)), by the
pan and volume step `0x00361810`, and by the two calls that hand it to the driver: `0x002DF560` each update and
`0x002DF2C0` when the map sound starts, through `0x001DC390` and `0x00211340`, and `0x001DC000` and `0x00210F60`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBB04` | `f32` | 0 | the listener's y: the focus character's own y in mode 0, with no offset | `0x00362850`: mode 0 (`0x003629BF`), mode 2 (`0x00362A1A`), mode 1 with the 16-byte copy (`0x00362A9A`); `0x00362F70`, 0 with the 16-byte store (`0x00362FCC`) | through the address `0x022CBB00`: `0x00361810` (`0x00361883`), from `0x00361BF0` (`0x00361CA6`), `0x00361CF0` (`0x00361DA3`) and `0x003631B0` (`0x00363320`); `0x003631B0` (`0x0036327D`, 16 bytes) and its shape tests `0x00362230` (`0x00362390`; `0x00363FD0` at `0x00363FE4`), `0x003623C0` (`0x00362414`, `0x003626B6`) and `0x00361DE0` (`0x00361E1B`, `0x00362138`), each 16 bytes, from `0x00362850` (`0x00362B76`, `0x00362BB7`); `0x00211340` (`0x002113A7`), from `0x00362850` through `0x002DF560` (`0x00362ABB`); `0x00210F60` (`0x00210FC7`), from `0x00362F70` through `0x002DF2C0` (`0x0036314C`) |
| `0x022CBB08` | `f32` | 0 | the listener's z | `0x00362850`: mode 0 (`0x003629D7`), mode 2 (`0x00362A3B`), mode 1 with the 16-byte copy (`0x00362A9A`); `0x00362F70`, 0 with the 16-byte store (`0x00362FCC`) | `0x00362850`, which hands x and z to the emitter lookup `0x00362E50` (`0x00362B4E`); through the address `0x022CBB00`: `0x00361810` (`0x003618BB`), from `0x00361BF0` (`0x00361CA6`), `0x00361CF0` (`0x00361DA3`) and `0x003631B0` (`0x00363320`); `0x003631B0` (`0x0036327D`, 16 bytes) and its shape tests `0x00362230` (`0x00362390`; `0x00363FD0` at `0x00363FE4`), `0x003623C0` (`0x00362414`, `0x003626B6`) and `0x00361DE0` (`0x00361E1B`, `0x00362138`), each 16 bytes, from `0x00362850` (`0x00362B76`, `0x00362BB7`); `0x00211340` (`0x002113A2`), from `0x00362850` through `0x002DF560` (`0x00362ABB`); `0x00210F60` (`0x00210FC2`), from `0x00362F70` through `0x002DF2C0` (`0x0036314C`) |
| `0x022CBB0C` | `f32` | 0 | the listener's fourth float: 1.0, or in mode 1 the fourth float of the stored position | `0x00362850`, 1.0: mode 0 (`0x003629B5`), mode 2 (`0x00362A4A`); mode 1 with the 16-byte copy (`0x00362A9A`); `0x00362F70`, 1.0 with the 16-byte store (`0x00362FCC`) | through the address `0x022CBB00`, only as part of 16-byte loads: `0x003631B0` (`0x0036327D`), `0x00362230` (`0x00362390`), `0x00363FD0` (`0x00363FE4`), `0x003623C0` (`0x00362414`, `0x003626B6`), `0x00361DE0` (`0x00361E1B`, `0x00362138`) |
| `0x022CBA8C` | `f32` | 0 | the listener's facing, in radians: `0x00361810` subtracts it from the direction of a sound to get the sound's pan (`0x003619C6`-`0x00361A25`) | `0x00362850`: mode 0 (`0x00362925`), mode 2 (`0x00362A79`), mode 1 (`0x00362A92`); `0x00362F70`, 0 (`0x00362FC6`) | `0x00361BF0` (`0x00361C76`), `0x00361CF0` (`0x00361D7E`) and `0x003631B0` (`0x003632EB`), which pass it to `0x00361810` (`0x003619D0`); `0x00362850` (`0x00362AAC`) and `0x00362F70` (`0x0036310E`), which pass it to `0x002DF560` and `0x002DF2C0`, where `0x00211340` and `0x00210F60` overwrite that argument unread (`0x002113A2`, `0x00210FC2`) |

No other instruction reaches these four: no other RIP-relative, image-base-relative or 32-bit offset reference names
them. The cutscene skip masks `0x022CB9C0` and `0x022CB9D8`, `u32[6]` each, are the only indexed tables below them
(`0x003604D0`, `0x003605A0`, `0x00360710`, `0x00360980`, `0x00360A50`), and they end at `0x022CB9F0`.
### The layer's pools

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EADDF8` | `i32` | 0 | the `Lay` action count, 512 | `0x007BAC80` (`0x007BAC94`) | no instruction |
| `0x02EADE10` | `i32` | 0 | the page count, 1 | `0x007BB6B0` (`0x007BB6BC`) | `0x007BB690`, which bounds a page number (`0x007BB694`); `0x007BB6B0` (`0x007BB6F5`, `0x007BB760`); `0x007BB780` (`0x007BB78D`, `0x007BB7B9`) |
| `0x02EADE18` | `void*` | 0 | the table of page pointers | `0x007BB6B0` (`0x007BB6EE`) | `0x007BB690` (`0x007BB69C`); `0x007BB6B0` (`0x007BB746`); `0x007BB780` (`0x007BB7A0`) |
| `0x02EADE20` | `i32` | 0 | the source count, 128 | `0x007BC400` (`0x007BC412`) | `0x007BC400` (`0x007BC44D`, `0x007BC467`, `0x007BC47C`, `0x007BC4A2`, `0x007BC4DE`) |
| `0x02EADE24` | `i32` | 0 | the last serial given to a source; each new source's handle takes the next | `0x007BBFB0` (`0x007BC135`) | `0x007BBFB0` (`0x007BC11E`) |

The `Lay` free-action queue `0x02EADD70` and the source list `0x02EADE80` have the layouts `DriverQueue` and
`ObjectList` of [Sound driver objects](sound-driver-objects.md); "through the address" names the helpers a function
hands the object to. `0x007BAC80` puts the 512 actions on the free-action queue, `0x007BAD60` takes one, and the `Lay`
runner `0x007BAEC0` gives each back after running it (`0x007BB4FD`-`0x007BB53F`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EADD78` | `void*` | 0 | Lay free-action queue `+0x08`, the cells, 512 of them | `0x0016A180` (`0x0016A1A4`); `0x008B8F40`, 0 after freeing them (`0x008B8F91`); through the address: `0x007BAB30` (`0x007BAB6C`, `0x007BAC22`), from `0x007BAC80` (`0x007BACC7`) | `0x008B8F40`, which frees them at exit (`0x008B8F44`); through the address: `0x007BAB30`, which frees the old cells and chains the new ones (`0x007BAB45`, `0x007BAC40`) |
| `0x02EADD98` | `i32` | 0 | Lay free-action queue `+0x28`, capacity: 512 cells | `0x0016A180`, 0 with `+0x2C` (`0x0016A19D`); through the address: `0x007BAB30` (`0x007BABA0`), from `0x007BAC80` (`0x007BACC7`) | no instruction |
| `0x02EADD80` | `void*` | 0 | Lay free-action queue `+0x10`, first free cell | `0x0016A180` (`0x0016A1A4`); `0x007BAC80` (`0x007BACFB`); `0x007BAD60` (`0x007BAE28`); `0x007BAEC0` (`0x007BB50D`); `0x008B8F40` (`0x008B8F91`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAC80` (`0x007BACE8`, `0x007BAD34`); `0x007BAD60` (`0x007BAE15`); `0x007BAEC0` (`0x007BB4FD`) |
| `0x02EADD88` | `void*` | 0 | Lay free-action queue `+0x18`, first queued cell | `0x0016A180` (`0x0016A1AC`); `0x007BAC80` (`0x007BAD13`); `0x007BAD60` (`0x007BAE0E`); `0x007BAEC0` (`0x007BB525`); `0x008B8F40` (`0x008B8FA0`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAC80` (`0x007BAD0A`); `0x007BAD60` (`0x007BAD8B`); `0x007BAEC0` (`0x007BB51C`) |
| `0x02EADD90` | `void*` | 0 | Lay free-action queue `+0x20`, last queued cell | `0x0016A180` (`0x0016A1AC`); `0x007BAC80` (`0x007BAD2D`); `0x007BAEC0` (`0x007BB53F`); `0x008B8F40` (`0x008B8FA0`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAC80` (`0x007BAD1C`); `0x007BAEC0` (`0x007BB52E`) |
| `0x02EADD9C` | `i32` | 0 | Lay free-action queue `+0x2C`, cells queued | `0x0016A180` (`0x0016A19D`); `0x007BAC80` (`0x007BAD27`); `0x007BAD60` (`0x007BAE20`); `0x007BAEC0` (`0x007BB539`); `0x008B8F40` (`0x008B8F7D`); through the address: `0x007BAB30` (from `0x007BAC80`) | `0x007BAC80` (`0x007BAD27`); `0x007BAD60` (`0x007BAE20`); `0x007BAEC0` (`0x007BB539`) |
| `0x02EADE88` | `i32` | 0 | source list `+0x08`, capacity: the nodes the list holds | `0x0016A230` (`0x0016A24D`); through the address: `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) | `0x007BBFB0` (`0x007BC1E5`); `0x007BC2B0` (`0x007BC2C1`); `0x007BC4F0` (`0x007BC777`); through the address: `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`); `0x007B2880` (from `0x007BBFB0` at `0x007BC22B`) |
| `0x02EADE8C` | `i32` | 0 | source list `+0x0C`, nodes in use | `0x0016A230` (`0x0016A24D`); `0x007BC4F0` (`0x007BC802`); `0x008B8FD0` (`0x008B900D`); through the address: `0x007B5580` (from `0x007BBFB0`); `0x007B2880` (from `0x007BBFB0`); `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) | `0x007BC4F0` (`0x007BC802`); through the address: `0x007B5580` (from `0x007BBFB0`); `0x007B2880` (from `0x007BBFB0`) |
| `0x02EADE90` | `void*` | 0 | source list `+0x10`, the `DriverListNode` array | `0x0016A230` (`0x0016A254`); `0x008B8FD0` (`0x008B9021`); through the address: `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) | `0x007BBFB0` (`0x007BC1ED`); `0x007BC2B0` (`0x007BC2CD`); `0x007BC4F0` (`0x007BC787`); `0x008B8FD0` (`0x008B8FD4`); through the address: `0x007B2880` (from `0x007BBFB0`); `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) |
| `0x02EADE98` | `void*` | 0 | source list `+0x18`, first free node | `0x0016A230` (`0x0016A254`); `0x007BC4F0` (`0x007BC80B`); `0x008B8FD0` (`0x008B9021`); through the address: `0x007B5580` (from `0x007BBFB0`); `0x007B2880` (from `0x007BBFB0`); `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) | `0x007BC4F0` (`0x007BC7E7`, `0x007BC7F2`); through the address: `0x007B5580` (from `0x007BBFB0`); `0x007B2880` (from `0x007BBFB0`) |
| `0x02EADEA0` | `void*` | 0 | source list `+0x20`, first node in use | `0x0016A230` (`0x0016A25C`); `0x007BC4F0` (`0x007BC7A6`); `0x008B8FD0` (`0x008B9030`); through the address: `0x007B5580` (from `0x007BBFB0`); `0x007B2880` (from `0x007BBFB0`); `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) | `0x007BC4F0` (`0x007BC523`, `0x007BC6F8`); through the address: `0x007B5580` (from `0x007BBFB0`) |
| `0x02EADEA8` | `void*` | 0 | source list `+0x28`, last node in use | `0x0016A230` (`0x0016A25C`); `0x007BC4F0` (`0x007BC7C9`); `0x008B8FD0` (`0x008B9030`); through the address: `0x007B5580` (from `0x007BBFB0`); `0x007B2880` (from `0x007BBFB0`); `0x007BC2F0` with `0x007B6AA0` (from `0x007BC400`) | through the address: `0x007B5580` (from `0x007BBFB0`) |

No other instruction reaches these globals. The search covered the executable's RIP-relative references, its
image-base-relative references, which hold none of them, and a scan of `.text` for each global's 32-bit offset from
the image base, which finds none.

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
