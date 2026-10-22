---
title: "Field camera: the follow camera, its stick and mouse control, wall avoidance and target framing"
kind: "system"
category: "Graphics"
addresses: "0x00259990, 0x003D9930, 0x02097D30, 0x0032AEC0, 0x0032B1C0, 0x0032B390, 0x0032B4D0, 0x0032DF40, 0x0032C910, 0x0032D3D0, 0x0032D620, 0x0032DC00, 0x0032C650, 0x0032B9C0, 0x0032CF50, 0x0032C3E0, 0x0032C180, 0x0032C2B0, 0x0032BCC0, 0x0032BB00, 0x0032BEB0, 0x0032CD20, 0x0032B900, 0x0032CA70, 0x0032D250, 0x0032D000, 0x001825C0, 0x001894D0, 0x0032B600, 0x0032B790"
---

## What the player sees

Outside cutscenes the camera trails the party leader. The right stick or the mouse swings it round and
raises or lowers it, a button swings it back behind the leader, and with Camera Auto-Rotation on it
drifts behind the leader while the leader runs. It slides along walls, rises over floors and props, pulls
in when something comes between it and the leader, and when the target cursor picks an actor it swings
over the leader's shoulder to look at that actor.

## How it works

### Where it runs

A camera record whose mode `+0xF0` is 1 is built by `0x00259990` ([scripted camera](scripted-camera.md)).
Its `+0xF4` picks one of the 0x860-byte camera controllers at `0x02097D30`. Each frame `0x003D9E20` reads the
target cursor, and `0x003D9930(controller, view, controller + 0x630)` runs `0x0032AEC0` on the follow camera
at controller `+0x2B0`; while the byte `0x02098DE9` is set, `0x003D9950` only republishes the last eye and
look point. `0x003D99B0` sets a controller up (`0x0032B600`) and `0x003D9B80` resets it (`0x0032B790`).

The followed transform at controller `+0x630` gives the position and the leader's facing, taken as
`atan2(+0x18, +0x10)` (`0x0032CE40`). The look point is that position raised by `+0x11C`, 1.3
(`0x0032B1C0`). When the position moves more than `0.1 × [0x01DFE0BC]` in a frame, `0x0032CE40` sets bit
`0x8000000` of the state word `+0xC0`.

### The followed transform

Each controller keeps two poses of `0xB0` bytes, a start at `+0x6E0` and a target at `+0x790`, and a
weight at `+0x840`. A pose holds a position at `+0x00` and the heading as `(cos, 0, sin, 1)` at
`+0x10`. `0x00259510(out, from, to, t)` blends them: the position linearly, the heading from `from` by
`t` times the shorter difference (`0x003A1C50`), written back as cosine and sine.

Each frame `0x0025A180(actor, slot)` copies the leader's transform (the block at `+0x30` of its
`+0xC0` → `+0x138` object) into the target pose and blends start to target by the weight into the
followed transform `+0x630` ([player movement](../Movement-And-Pathfinding/player-movement.md)).

### Resetting the follow camera

`resetbehindcamera` (`0x0288`, `0x00343340`) pops two floats and passes the first popped to `0x00259620`
and the second to `0x0025A0C0`.

- `0x00259620(level)` clamps the value to −1 to 1. On both controllers it copies the target pose's
  position and heading into the start pose, sets the weight `+0x840` to 1.0 and `+0x844` to 0, resets
  the controller (`0x003D9B80`) and sets the follow camera's level (`0x0032B8B0`). It keeps the value at
  `0x02098DFC`.
- `0x0032B8B0(camera, v)` writes `clamp(0.5 × v + 0.483, 0, 1)` to the three level copies `+0x3C`,
  `+0x7C` and `+0xBC` and clears the bytes `+0x00`, `+0x40` and `+0x80`, so 0 gives the starting
  level.
- `0x0025A0C0(heading)` wraps the heading into −π to π, keeps it at `0x02098E00`, and on both follow
  cameras sets the three heading copies `+0x30`, `+0x70` and `+0xB0` to the heading plus π
  (`0x0032B880`).

`0x00259FB0`, from the field-settled sequence ([field runtime](../Characters-And-Objects/field-runtime.md)),
applies `0x02098DFC` and `0x02098E00` again the same way.

### The camera types

At start-up `0x0022A0B0` runs `0x00259DF0`, which files a read of file kind 9 (`0x0032E400`, `0x0032E620`); its completion
`0x00259370(table)` keeps the table at `0x02098DF0`, or 0 when the file is empty, and when the table's count `+0x04` is
above 0 sets `0x02098DF8` to type 0 and copies it with `0x00259FE0` (`0x00259370`-`0x0025938D`).

`setbehindcameratype` (`0x01CB`, `0x00356CB0`), `0x00304060` and `0x00304140` call `0x0025A160(type)`: for a type below the table's count `+0x04` it sets
`0x02098DF8` and `0x00259FE0` copies the type's 64-byte entry (from table `+0x10`) into both controllers:
its first word to `+0x64` and seven pairs of floats to `+0x10 + 12k` and `+0x14 + 12k`. `0x003D9C40`
then stores at `+0x18 + 12k` each segment's length between consecutive pairs as a share of their
total.

The same walk keeps running totals of those shares, the profile's position at the start of a
segment, in three controller fields: `+0x1D0` the start of segment 3; `+0x1D4` the start of segment 2,
or of segment 1 when `+0x2A0` is non-zero; and `+0x1D8` the start of segment 4, or of segment 5 when
`+0x2A0` is non-zero. `0x003D99B0` and `0x003D9B80` run it too, on the default pairs `0x01EFE998` to
`0x01EFE9CC`, from (−0.7, 2.8) to (7.6, 8.8), the end points of the orbit curve below with the height
first.

### Other controller settings

- `0x0025A540(flag, vector)`, from `0x002628B0`, writes the vector to `+0x00` of both
  controllers and the flag to `0x02098DE9`, the byte that limits the follow camera to republishing.
- `tutorial_set_behindcameraenable` (`0x03A1`, `0x003503B0`) stores whether its int is non-zero at
  `0x02098354` (`0x0025A880`), and `tutorial_get_behindcameraenable` (`0x03A0`, `0x0034FFA0`) returns it
  (`0x0025A850`). Opening the pause menu (`0x00229590`) saves the value and clears it.

### The orbit

The camera is a heading `+0x70` (radians, wrapped to 0 to 2π) and a height level `+0x7C` (0 to 1).
`0x0032DF40(heading, level, look, out)` turns the level into a pitch and a distance:

```python
x = 2.8 + 6 × level
y = 0.205 x² − 0.995 x + 0.4788
pitch = −atan2(y, x)        distance = √(x² + y²)
```

At level 0 the eye is 2.8 out and 0.7 below the look point; at level 1, 8.8 out and 7.6 above
(`0x01EED478`: −0.7, 2.8, 7.6, 8.8). The starting level is 0.483 (`0x0032B600`). `0x0032CD20` places the eye
from the look point `+0x20`, heading `h` `+0x30`, pitch `p` `+0x34` and distance `+0x38` of its slot, times
a scale argument `k`: `eye = look + k x [+0x38] x (sin h cos p, -sin p, cos h cos p)` (`0x003CC2F0`,
`0x003CC480`). It then sets `eye.y = min(eye.y + lift, look.y - [camera +0x11C] + 9.0)`, at most 9.0 above
the followed position.

Each frame `0x0032B9C0` adds the input rates to heading and level, divided by `+0x100`: 1.0 when idle, the
frame-rate float `0x00229E70()` while input moves the camera (`0x0032C910`). It also adds the wall turn
`+0x104`, the wall lift `+0x108` and the auto-rotation `+0x10C`. `0x0032BA70` is the same without the
wall and auto terms.

### Stick, mouse and recentre

`0x0032C910` reads the dead zone `+0xF4` (`0x0046DB20`: 50) and the two camera axes `0x0046DB10(0)` and
`0x0046DB10(1)`, centred at `0x80`:

- `0x0032D3D0` turns the horizontal axis into the heading rate `+0xF8`. Past the dead zone the rate is
  `0.4 × 2π / (30 × [0x01DFE0B4])` per frame times the deflection beyond it, over `128 − 50`, eased
  as `(2 × old + new) / 3`.
- A deflection toward a side whose wall probe is hit counts as zero.
- With no stick input and the mouse enabled (`+0x374`, 1 after `0x0032B790`), a mouse movement of 7 or
  more (`0x001E0CE0`, negated by Camera X-Axis Inverted) drives the same rate, times Mouse Sensitivity
  Left/Right (`0x0017E420`) and 0.2.
- `0x0032D620` does the same for the level rate `+0xFC` from the vertical axis, `0x001E0D30` and
  `0x0017E430`, at `0.8 / (30 × [0x01DFE0B4])` per frame.
- With no input, both rates are multiplied by `[0x022C3180]` each frame: 0.5, or √0.5 when `0x001EDE70` is
  set (`0x0032AE70`). They stop at once when Camera Auto-Rotation (`0x0017E260`) is off and no recentre is
  running.
- Bit `0x4` of the pad word `0x0036FF80()` starts a recentre (`0x0032DC00`) toward the heading
  `3π/2 − facing`, behind the leader. The swing is converted into a stick deflection `+0x370`;
  `0x0032D820` feeds it through `0x0032D3D0` each frame until the heading arrives.
- During a recentre `0x0032DB10` eases the level to 0.483 over `30 × [0x01DFE0B4]` frames.

### Camera Auto-Rotation

`0x0032C650` turns the heading toward `3π/2 − facing` once the leader has been moving (state
`0x8000000` without `0x4000000`) for `15 × [0x01DFE0B4]` frames. The turn is proportional to the
angle and falls as the camera rises. It is capped at `0.2 × 2π / (30 × [0x01DFE0B4])` per frame,
and none is made when the camera would have to swing more than 150°, as when the leader runs toward it. With Camera Auto-Rotation
off (`0x0017E260`, CameraRevise) the term is 0; on, it is eased as `(3 × old + new) / 4` into `+0x10C`.

### Walls around the camera

`0x0032D2E0` places four test segments (`0x0032C3E0`) in the frame of the current camera matrix
`0x02AEDEF0`: from beside the followed position to beside the eye on the left and right, from above the
followed position to 2.0 above the eye, and from low on it to 0.3 below the eye. The side offsets and
heights come from the followed transform's `+0x64` and `+0x6C`. `0x0032CF50` casts each against the
field's collision part (`0x0026E500(0)`, kept at `+0x2C8`) through `0x003D97E0` and sets bit `0x1`, `0x2`,
`0x4` or `0x8` of `+0xC0` (`0x01EED488`) for each hit.

- `0x0032C180` turns the heading when one side is hit (state bits `0x11` one way, `0x44` the other) at
  `0.12 × 2π / (30 × [0x01DFE0B4])` per frame, eased into `+0x104`; otherwise `+0x104` decays by 0.9
  a frame.
- `0x0032C2B0` lowers the level for a hit above (`0x22`) and raises it for a hit below (`0x88`) at
  `1.2 / (30 × [0x01DFE0B4])` per frame, eased into `+0x108`; otherwise `+0x108` halves each frame.
- Both act only while Camera Auto-Rotation is on, the leader has moved since the last camera input
  (bit `0x10000000` set, `0x20000000` clear) and the camera is not pulled in.

### Floors and props under the eye

`0x0032BB00(camera, eye, look)` returns how far to lift the eye, the largest of: the value the body-record
query `0x0046DB50` returns for the eye; within 1.2 of the look point, `√(1.44 − d²)` for the horizontal
distance `d`; and the amount that puts the eye 0.27 above the floor triangle under it (`0x002321D0`,
`0x00231890`). A lift at least as large as the
current one `+0x128` replaces it and holds for `20 × [0x01DFE0B4]` frames; then `0x0032DDE0` eases it back
to 0.

### Pulling in

`0x0032BCC0` tests the full-distance eye with the wall contact `0x00232490` and a ray (`0x00231690`); a contact,
or a ray shorter than 0.27, widens the next sweep's polygon mask from 4 to `0xFFFF`. It then sweeps a 0.27
sphere from the look point to the lifted eye (`0x00230C00`). With no hit the eye stands; a hit puts the eye
at the hit point and sets `0x4040000`.

Next frame `0x0032B4D0` takes the pulled-in branch: `0x0032BEB0` sweeps again and, on a hit, shrinks the
distance scale `+0x120` to the hit's share of the full distance, up to two retries. The scale holds for
`60 × [0x01DFE0B4]` frames, then `0x0032DE90` eases it back toward 1. When a sweep is clear, bit
`0x4000000` is cleared and the normal branch `0x0032B390` runs again.

### Framing a target

`0x003D9E20` copies the target cursor's actor (`[0x02B47730] + 0xC8`, while its `+0xC0` bit `0x4` is set)
into `0x02B4E4A0` and raises `0x02B4E4A5`. `0x0032B900` then fetches the point of interest (`0x0032D250`):

1. the point `0x00290A90` returns from the UI manager `[0x0209BE80]`;
2. otherwise the actor's position (`0x003588B0`, `0x002E7F70`).

`0x0032CA70` frames it when the pitch from the point to the leader's look point is at most 80° (1.396). The
eye goes 3.0 out from the leader on the line away from the point, turned by 0.25 rad, and passes the same
wall, ray and sweep tests; the look point is the point of interest. When it declines, bit `0x80000` stops
further tries until the cursor closes (`0x0032B900`).

`0x0032AEC0` counts `+0x320` up while framing and down otherwise, capped at `15 × [0x01DFE0B4]`. `0x0032D000`
blends the follow eye and look (`+0x2E0`, `+0x2F0`) toward the framing pair (`+0x300`, `+0x310`) by
`(1 + cos(π t + π)) / 2`, with `t` the count over its cap, going round the shorter way (`0x0032CC90`).
`0x0032C5E0` records which way round when framing starts or ends.

### Publishing

`0x0032AEC0` writes the blended eye `+0x330` and look point `+0x340` into the view (`0x003CC080`). It then
requests depth-of-field mode 1 with the focus distance `max(1 + 2p, −(1 − 0.8 p) z)`, where `z` is the
look point's depth in view space and `p` is `t` raised to 0.16 (`0x001825C0`). It adds the eye's movement
to the travelled distance `+0x368`.

`0x001825C0(mode, distance, point)` stores the request in the render manager (`0x00189120`) through
`0x001894D0`, at `+0x340` (mode), `+0x344` (distance) and `+0x348` (a vector; the camera passes the
normalised eye-to-look direction), in one of two copies chosen by
its byte `+0x1C`. `0x00189CE0` hands the request to the render parameters (`0x00194490` at `0x0018A0E5`), where
mode 1 sets the focus ([post-processing](post-processing.md)). `0x00259820` clears the request to mode 0
each frame before the camera runs.

## Layouts

Follow camera (controller + `0x2B0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x060` | `f32[4] look point` | followed position + 0x11C up |  |
| `+0x070` | `f32` | heading | 0 to 2π |
| `+0x07C` | `f32` | height level | 0 to 1 |
| `+0x080` | `...` | orbit block | look +`0xA0`, heading +`0xB0`, pitch +`0xB4`, distance +`0xB8` (`0x0032DF40`) |
| `+0x0C0` | `u32` | state | probe hits `0x1`-`0x8`, `0x4000000` pulled in, `0x8000000` leader moving |
| `+0x0F4` | `i32` | stick dead zone 50 |  |
| `+0x0F8` | `f32` | heading rate | +`0x0FC` level rate |
| `+0x100` | `f32` | rate divisor | 1.0 idle, `0x00229E70`() under input |
| `+0x104` | `f32` | wall turn | +`0x108` wall lift, +`0x10C` auto-rotation |
| `+0x11C` | `f32` | look height | 1.3 |
| `+0x120` | `f32` | distance scale | +`0x124` its hold count |
| `+0x128` | `f32` | floor lift | +`0x12C` its hold count |
| `+0x140` | `...` | four test segments, 0x60 apart |  |
| `+0x2C0` | `void*` | followed transform |  |
| `+0x2C8` | `void*` | collision part | `0x0026E500`(0) |
| `+0x2E0` | `f32[4] follow eye` | +0x2F0 follow look |  |
| `+0x300` | `f32[4] framing eye` | +0x310 framing look |  |
| `+0x320` | `i32` | framing count | 0 to 15 x [`0x01DFE0B4`] |
| `+0x330` | `f32[4] published eye` | +0x340 published look |  |
| `+0x350` | `f32[4]` | point | of interest |
| `+0x360` | `u32` | framed actor |  |
| `+0x368` | `f32` | travelled distance |  |
| `+0x370` | `i32` | recentre deflection |  |
| `+0x374` | `u32` | mouse enabled | 1 |

## State

| Address | What |
|---|---|
| `0x02097D30` | the camera controllers, 0x860 bytes each |
| `0x02B4E4A0`, `0x02B4E4A5` | the framed actor and its flag (`0x003D9E20`) |
| `0x022C3184`, `0x022C3188` | the curve's highest and lowest `y`, 7.6 and −0.7 (`0x0032B600`) |
| `0x01EED478` | the curve's end points |
| `0x01EED488` | the four probe bits |

## Modding notes

- Distance and height come only from the curve in `0x0032DF40`; changing its constants (2.8, 6, 0.205,
  0.995, 0.4788) changes the whole range, and `0x022C3184`/`0x022C3188` must follow for the auto-rotation
  scaling.
- Turn rates scale with `[0x01DFE0B4]`, so they hold the same speed at 30 and 60 fps.
- The 0.27 floor margin and sweep radius appear in `0x0032BB00`, `0x0032BCC0`, `0x0032BEB0` and `0x0032CA70`;
  change them together.
- Camera Auto-Rotation off also turns off the wall turn and wall lift, not only the drift behind the
  leader.

## Related

- [Scripted camera](scripted-camera.md): the camera records, submission and the matrices.
- [Post-processing](post-processing.md): the depth-of-field focus the camera requests.
- [Config screen](../Menus-And-HUD/config-screen.md): Camera Auto-Rotation, mouse sensitivity and axis options.
- [Geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md): the body-top query `0x0046DB50`.
- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): the collision
  part and the wall test.
- [Player movement](../Movement-And-Pathfinding/player-movement.md): the stick dead zone.
