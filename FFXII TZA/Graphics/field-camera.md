---
title: "Field camera: the follow camera, its stick and mouse control, wall avoidance and target framing"
kind: "system"
category: "Graphics"
addresses: "00259990, 003D9930, 02097D30, 0032AEC0, 0032B1C0, 0032B390, 0032B4D0, 0032DF40, 0032C910, 0032D3D0, 0032D620, 0032DC00, 0032C650, 0032B9C0, 0032CF50, 0032C3E0, 0032C180, 0032C2B0, 0032BCC0, 0032BB00, 0032BEB0, 0032CD20, 0032B900, 0032CA70, 0032D250, 0032D000, 001825C0, 001894D0, 0032B600, 0032B790"
---

## What the player sees

Outside cutscenes the camera trails the party leader. The right stick or the mouse swings it round and
raises or lowers it, a button swings it back behind the leader, and with Camera Auto-Rotation on it
drifts behind the leader while the leader runs. It slides along walls, rises over floors and props, pulls
in when something comes between it and the leader, and when the target cursor picks an actor it swings
over the leader's shoulder to look at that actor.

## How it works

### Where it runs

A camera record whose mode `+F0`<sub>h</sub> is 1 is built by `00259990` ([scripted camera](scripted-camera.md)).
Its `+F4`<sub>h</sub> picks one of the `860`<sub>h</sub>-byte camera controllers at `02097D30`. Each frame `003D9E20` reads the
target cursor, and `003D9930(controller, view, controller + 630h)` runs `0032AEC0` on the follow camera
at controller `+2B0`<sub>h</sub>; while the byte `02098DE9` is set, `003D9950` only republishes the last eye and
look point. `003D99B0` sets a controller up (`0032B600`) and `003D9B80` resets it (`0032B790`).

The followed transform at controller `+630`<sub>h</sub> gives the position and the leader's facing, taken as
`atan2(+18h, +10h)` (`0032CE40`). The look point is that position raised by `+11C`<sub>h</sub>, 1.3
(`0032B1C0`). When the position moves more than `0.1 × [01DFE0BC]` in a frame, `0032CE40` sets bit
`8000000`<sub>h</sub> of the state word `+C0`<sub>h</sub>.

### The followed transform

Each controller keeps two poses of `B0`<sub>h</sub> bytes, a start at `+6E0`<sub>h</sub> and a target at `+790`<sub>h</sub>, and a
weight at `+840`<sub>h</sub>. A pose holds a position at `+00`<sub>h</sub> and the heading as `(cos, 0, sin, 1)` at
`+10`<sub>h</sub>. `00259510(out, from, to, t)` blends them: the position linearly, the heading from `from` by
`t` times the shorter difference (`003A1C50`), written back as cosine and sine.

Each frame `0025A180(actor, slot)` copies the leader's transform (the block at `+30`<sub>h</sub> of its
`+C0`<sub>h</sub> → `+138`<sub>h</sub> object) into the target pose and blends start to target by the weight into the
followed transform `+630`<sub>h</sub> ([player movement](../Movement-And-Pathfinding/player-movement.md)).

### Resetting the follow camera

`resetbehindcamera` (`0288`<sub>h</sub>, `00343340`) pops two floats and passes the first popped to `00259620`
and the second to `0025A0C0`.

- `00259620(level)` clamps the value to −1 to 1. On both controllers it copies the target pose's
  position and heading into the start pose, sets the weight `+840`<sub>h</sub> to 1.0 and `+844`<sub>h</sub> to 0, resets
  the controller (`003D9B80`) and sets the follow camera's level (`0032B8B0`). It keeps the value at
  `02098DFC`.
- `0032B8B0(camera, v)` writes `clamp(0.5 × v + 0.483, 0, 1)` to the three level copies `+3C`<sub>h</sub>,
  `+7C`<sub>h</sub> and `+BC`<sub>h</sub> and clears the bytes `+00`<sub>h</sub>, `+40`<sub>h</sub> and `+80`<sub>h</sub>, so 0 gives the starting
  level.
- `0025A0C0(heading)` wraps the heading into −π to π, keeps it at `02098E00`, and on both follow
  cameras sets the three heading copies `+30`<sub>h</sub>, `+70`<sub>h</sub> and `+B0`<sub>h</sub> to the heading plus π
  (`0032B880`).

`00259FB0`, from the field-settled sequence ([field runtime](../Characters-And-Objects/field-runtime.md)),
applies `02098DFC` and `02098E00` again the same way.

### The camera types

At start-up `0022A0B0` runs `00259DF0`, which files a read of file kind 9 (`0032E400`, `0032E620`); its completion
`00259370(table)` keeps the table at `02098DF0`, or 0 when the file is empty, and when the table's count `+04`<sub>h</sub> is
above 0 sets `02098DF8` to type 0 and copies it with `00259FE0` (`00259370`-`0025938D`).

`setbehindcameratype` (`01CB`<sub>h</sub>, `00356CB0`), `00304060` and `00304140` call `0025A160(type)`: for a type below the table's count `+04`<sub>h</sub> it sets
`02098DF8` and `00259FE0` copies the type's 64-byte entry (from table `+10`<sub>h</sub>) into both controllers:
its first word to `+64`<sub>h</sub> and seven pairs of floats to `+10h + 12k` and `+14h + 12k`. `003D9C40`
then stores at `+18h + 12k` each segment's length between consecutive pairs as a share of their
total.

The same walk keeps running totals of those shares, the profile's position at the start of a
segment, in three controller fields: `+1D0`<sub>h</sub> the start of segment 3; `+1D4`<sub>h</sub> the start of segment 2,
or of segment 1 when `+2A0`<sub>h</sub> is non-zero; and `+1D8`<sub>h</sub> the start of segment 4, or of segment 5 when
`+2A0`<sub>h</sub> is non-zero. `003D99B0` and `003D9B80` run it too, on the default pairs `01EFE998` to
`01EFE9CC`, from (−0.7, 2.8) to (7.6, 8.8), the end points of the orbit curve below with the height
first.

### Other controller settings

- `0025A540(flag, vector)`, from `002628B0`, writes the vector to `+00`<sub>h</sub> of both
  controllers and the flag to `02098DE9`, the byte that limits the follow camera to republishing.
- `tutorial_set_behindcameraenable` (`03A1`<sub>h</sub>, `003503B0`) stores whether its int is non-zero at
  `02098354` (`0025A880`), and `tutorial_get_behindcameraenable` (`03A0`<sub>h</sub>, `0034FFA0`) returns it
  (`0025A850`). Opening the pause menu (`00229590`) saves the value and clears it.

### The orbit

The camera is a heading `+70`<sub>h</sub> (radians, wrapped to 0 to 2π) and a height level `+7C`<sub>h</sub> (0 to 1).
`0032DF40(heading, level, look, out)` turns the level into a pitch and a distance:

```python
x = 2.8 + 6 × level
y = 0.205 x² − 0.995 x + 0.4788
pitch = −atan2(y, x)        distance = √(x² + y²)
```

At level 0 the eye is 2.8 out and 0.7 below the look point; at level 1, 8.8 out and 7.6 above
(`01EED478`: −0.7, 2.8, 7.6, 8.8). The starting level is 0.483 (`0032B600`). `0032CD20` places the eye
from the look point, heading, pitch and a distance scale (`003CC2F0`), raises it by the floor lift, and
keeps it at most 9.0 above the followed position.

Each frame `0032B9C0` adds the input rates to heading and level, divided by `+100`<sub>h</sub>: 1.0 when idle, the
frame-rate float `00229E70()` while input moves the camera (`0032C910`). It also adds the wall turn
`+104`<sub>h</sub>, the wall lift `+108`<sub>h</sub> and the auto-rotation `+10C`<sub>h</sub>. `0032BA70` is the same without the
wall and auto terms.

### Stick, mouse and recentre

`0032C910` reads the dead zone `+F4`<sub>h</sub> (`0046DB20`: 50) and the two camera axes `0046DB10(0)` and
`0046DB10(1)`, centred at `80`<sub>h</sub>:

- `0032D3D0` turns the horizontal axis into the heading rate `+F8`<sub>h</sub>. Past the dead zone the rate is
  `0.4 × 2π / (30 × [01DFE0B4])` per frame times the deflection beyond it, over `128 − 50`, eased
  as `(2 × old + new) / 3`.
- A deflection toward a side whose wall probe is hit counts as zero.
- With no stick input and the mouse enabled (`+374`<sub>h</sub>, 1 after `0032B790`), a mouse movement of 7 or
  more (`001E0CE0`, negated by Camera X-Axis Inverted) drives the same rate, times Mouse Sensitivity
  Left/Right (`0017E420`) and 0.2.
- `0032D620` does the same for the level rate `+FC`<sub>h</sub> from the vertical axis, `001E0D30` and
  `0017E430`, at `0.8 / (30 × [01DFE0B4])` per frame.
- With no input, both rates are multiplied by `[022C3180]` each frame: 0.5, or √0.5 when `001EDE70` is
  set (`0032AE70`). They stop at once when Camera Auto-Rotation (`0017E260`) is off and no recentre is
  running.
- Bit `4`<sub>h</sub> of the pad word `0036FF80()` starts a recentre (`0032DC00`) toward the heading
  `3π/2 − facing`, behind the leader. The swing is converted into a stick deflection `+370`<sub>h</sub>;
  `0032D820` feeds it through `0032D3D0` each frame until the heading arrives.
- During a recentre `0032DB10` eases the level to 0.483 over `30 × [01DFE0B4]` frames.

### Camera Auto-Rotation

`0032C650` turns the heading toward `3π/2 − facing` once the leader has been moving (state
`8000000`<sub>h</sub> without `4000000`<sub>h</sub>) for `15 × [01DFE0B4]` frames. The turn is proportional to the
angle and falls as the camera rises. It is capped at `0.2 × 2π / (30 × [01DFE0B4])` per frame,
and none is made when the camera would have to swing more than 150°, as when the leader runs toward it. With Camera Auto-Rotation
off (`0017E260`, CameraRevise) the term is 0; on, it is eased as `(3 × old + new) / 4` into `+10C`<sub>h</sub>.

### Walls around the camera

`0032D2E0` places four test segments (`0032C3E0`) in the frame of the current camera matrix
`02AEDEF0`: from beside the followed position to beside the eye on the left and right, from above the
followed position to 2.0 above the eye, and from low on it to 0.3 below the eye. The side offsets and
heights come from the followed transform's `+64`<sub>h</sub> and `+6C`<sub>h</sub>. `0032CF50` casts each against the
field's collision part (`0026E500(0)`, kept at `+2C8`<sub>h</sub>) through `003D97E0` and sets bit `1`<sub>h</sub>, `2`<sub>h</sub>,
`4`<sub>h</sub> or `8`<sub>h</sub> of `+C0`<sub>h</sub> (`01EED488`) for each hit.

- `0032C180` turns the heading when one side is hit (state bits `11`<sub>h</sub> one way, `44`<sub>h</sub> the other) at
  `0.12 × 2π / (30 × [01DFE0B4])` per frame, eased into `+104`<sub>h</sub>; otherwise `+104`<sub>h</sub> decays by 0.9
  a frame.
- `0032C2B0` lowers the level for a hit above (`22`<sub>h</sub>) and raises it for a hit below (`88`<sub>h</sub>) at
  `1.2 / (30 × [01DFE0B4])` per frame, eased into `+108`<sub>h</sub>; otherwise `+108`<sub>h</sub> halves each frame.
- Both act only while Camera Auto-Rotation is on, the leader has moved since the last camera input
  (bit `10000000`<sub>h</sub> set, `20000000`<sub>h</sub> clear) and the camera is not pulled in.

### Floors and props under the eye

`0032BB00(camera, eye, look)` returns how far to lift the eye, the largest of: the value the body-record
query `0046DB50` returns for the eye; within 1.2 of the look point, `√(1.44 − d²)` for the horizontal
distance `d`; and the amount that puts the eye 0.27 above the floor triangle under it (`002321D0`,
`00231890`). A lift at least as large as the
current one `+128`<sub>h</sub> replaces it and holds for `20 × [01DFE0B4]` frames; then `0032DDE0` eases it back
to 0.

### Pulling in

`0032BCC0` tests the full-distance eye with the wall contact `00232490` and a ray (`00231690`); a contact,
or a ray shorter than 0.27, widens the next sweep's polygon mask from 4 to `FFFF`<sub>h</sub>. It then sweeps a 0.27
sphere from the look point to the lifted eye (`00230C00`). With no hit the eye stands; a hit puts the eye
at the hit point and sets `4040000`<sub>h</sub>.

Next frame `0032B4D0` takes the pulled-in branch: `0032BEB0` sweeps again and, on a hit, shrinks the
distance scale `+120`<sub>h</sub> to the hit's share of the full distance, up to two retries. The scale holds for
`60 × [01DFE0B4]` frames, then `0032DE90` eases it back toward 1. When a sweep is clear, bit
`4000000`<sub>h</sub> is cleared and the normal branch `0032B390` runs again.

### Framing a target

`003D9E20` copies the target cursor's actor (`[02B47730] + C8h`, while its `+C0`<sub>h</sub> bit `4`<sub>h</sub> is set)
into `02B4E4A0` and raises `02B4E4A5`. `0032B900` then fetches the point of interest (`0032D250`):

1. the point `00290A90` returns from the UI manager `[0209BE80]`;
2. otherwise the actor's position (`003588B0`, `002E7F70`).

`0032CA70` frames it when the pitch from the point to the leader's look point is at most 80° (1.396). The
eye goes 3.0 out from the leader on the line away from the point, turned by 0.25 rad, and passes the same
wall, ray and sweep tests; the look point is the point of interest. When it declines, bit `80000`<sub>h</sub> stops
further tries until the cursor closes (`0032B900`).

`0032AEC0` counts `+320`<sub>h</sub> up while framing and down otherwise, capped at `15 × [01DFE0B4]`. `0032D000`
blends the follow eye and look (`+2E0`<sub>h</sub>, `+2F0`<sub>h</sub>) toward the framing pair (`+300`<sub>h</sub>, `+310`<sub>h</sub>) by
`(1 + cos(π t + π)) / 2`, with `t` the count over its cap, going round the shorter way (`0032CC90`).
`0032C5E0` records which way round when framing starts or ends.

### Publishing

`0032AEC0` writes the blended eye `+330`<sub>h</sub> and look point `+340`<sub>h</sub> into the view (`003CC080`). It then
requests depth-of-field mode 1 with the focus distance `max(1 + 2p, −(1 − 0.8 p) z)`, where `z` is the
look point's depth in view space and `p` is `t` raised to 0.16 (`001825C0`). It adds the eye's movement
to the travelled distance `+368`<sub>h</sub>.

`001825C0(mode, distance, point)` stores the request in the render manager (`00189120`) through
`001894D0`, at `+340`<sub>h</sub> (mode), `+344`<sub>h</sub> (distance) and `+348`<sub>h</sub> (a vector; the camera passes the
normalised eye-to-look direction), in one of two copies chosen by
its byte `+1C`<sub>h</sub>. `00189CE0` hands the request to the render parameters (`00194490` at `0018A0E5`), where
mode 1 sets the focus ([post-processing](post-processing.md)). `00259820` clears the request to mode 0
each frame before the camera runs.

## Layouts

Follow camera (controller + `2B0`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `060`<sub>h</sub> | `f32[4] look point` | followed position + `11C`<sub>h</sub> up |  |
| `070`<sub>h</sub> | `f32` | heading | 0 to 2π |
| `07C`<sub>h</sub> | `f32` | height level | 0 to 1 |
| `080`<sub>h</sub> | `...` | orbit block | look +`A0`<sub>h</sub>, heading +`B0`<sub>h</sub>, pitch +`B4`<sub>h</sub>, distance +`B8`<sub>h</sub> (`0032DF40`) |
| `0C0`<sub>h</sub> | `u32` | state | probe hits `1`<sub>h</sub>-`8`<sub>h</sub>, `4000000`<sub>h</sub> pulled in, `8000000`<sub>h</sub> leader moving |
| `0F4`<sub>h</sub> | `i32` | stick dead zone 50 |  |
| `0F8`<sub>h</sub> | `f32` | heading rate | +`0FC`<sub>h</sub> level rate |
| `100`<sub>h</sub> | `f32` | rate divisor | 1.0 idle, `00229E70`() under input |
| `104`<sub>h</sub> | `f32` | wall turn | +`108`<sub>h</sub> wall lift, +`10C`<sub>h</sub> auto-rotation |
| `11C`<sub>h</sub> | `f32` | look height | 1.3 |
| `120`<sub>h</sub> | `f32` | distance scale | +`124`<sub>h</sub> its hold count |
| `128`<sub>h</sub> | `f32` | floor lift | +`12C`<sub>h</sub> its hold count |
| `140`<sub>h</sub> | `...` | four test segments, `60`<sub>h</sub> apart |  |
| `2C0`<sub>h</sub> | `void*` | followed transform |  |
| `2C8`<sub>h</sub> | `void*` | collision part | `0026E500`(0) |
| `2E0`<sub>h</sub> | `f32[4] follow eye` | `+2F0`<sub>h</sub> follow look |  |
| `300`<sub>h</sub> | `f32[4] framing eye` | `+310`<sub>h</sub> framing look |  |
| `320`<sub>h</sub> | `i32` | framing count | 0 to 15 x [`01DFE0B4`] |
| `330`<sub>h</sub> | `f32[4] published eye` | `+340`<sub>h</sub> published look |  |
| `350`<sub>h</sub> | `f32[4]` | point | of interest |
| `360`<sub>h</sub> | `u32` | framed actor |  |
| `368`<sub>h</sub> | `f32` | travelled distance |  |
| `370`<sub>h</sub> | `i32` | recentre deflection |  |
| `374`<sub>h</sub> | `u32` | mouse enabled | 1 |

## State

| Address | What |
|---|---|
| `02097D30` | the camera controllers, `860`<sub>h</sub> bytes each |
| `02B4E4A0`, `02B4E4A5` | the framed actor and its flag (`003D9E20`) |
| `022C3184`, `022C3188` | the curve's highest and lowest `y`, 7.6 and −0.7 (`0032B600`) |
| `01EED478` | the curve's end points |
| `01EED488` | the four probe bits |

## Modding notes

- Distance and height come only from the curve in `0032DF40`; changing its constants (2.8, 6, 0.205,
  0.995, 0.4788) changes the whole range, and `022C3184`/`022C3188` must follow for the auto-rotation
  scaling.
- Turn rates scale with `[01DFE0B4]`, so they hold the same speed at 30 and 60 fps.
- The 0.27 floor margin and sweep radius appear in `0032BB00`, `0032BCC0`, `0032BEB0` and `0032CA70`;
  change them together.
- Camera Auto-Rotation off also turns off the wall turn and wall lift, not only the drift behind the
  leader.

## Related

- [Scripted camera](scripted-camera.md): the camera records, submission and the matrices.
- [Post-processing](post-processing.md): the depth-of-field focus the camera requests.
- [Config screen](../Menus-And-HUD/config-screen.md): Camera Auto-Rotation, mouse sensitivity and axis options.
- [Geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md): the body-top query `0046DB50`.
- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): the collision
  part and the wall test.
- [Player movement](../Movement-And-Pathfinding/player-movement.md): the stick dead zone.
