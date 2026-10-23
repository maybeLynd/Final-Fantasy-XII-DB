---
title: "Scripted camera: the shot channels, the camera record stack, and how a camera reaches the renderer"
kind: "system"
category: "Graphics"
addresses: "0x003DA050, 0x002555D0, 0x0025A3B0, 0x0025A2C0, 0x0025A500, 0x0025A520, 0x02097300, 0x02098DEC, 0x00259820, 0x00257830, 0x00257520, 0x00256650, 0x003829D0, 0x02AED630, 0x003820C0, 0x02AED560, 0x00382B70, 0x0037D4C0, 0x0037D970, 0x02AEDEF0"
---

## What the player sees

The directed camera of a cutscene, or of a field moment such as a door opening, flies authored
shots and then hands control back to the ordinary behind camera, either at once or with an eased
swing back. While a shot plays it outranks the follow camera; when the last shot stops, the camera
below it takes over. A skipped scene lands each running shot on its final pose. An effect file can
carry its own camera, which wins for exactly the frames on which the effect submits it. The Screen
Shake option silences one shake source outside scripted events; scripted shakes still play.

## How it works

The shot data, its key and segment stream, the ease curves and paths, and the per-frame
interpolation are on [EBP camera tables](../EBP-Script-Files/ebp-camera-tables.md); the
shake curves and oscillators on [EBP camera shake](../EBP-Script-Files/ebp-camera-shake.md).
The four shot channels per actor manager, their binds and the verbs that start, stop, switch and
re-rate them are on [actor managers](../Characters-And-Objects/actor-managers.md). This page covers the
path from a running channel to the picture.

### The channel tick

The per-frame caller `0x00314370` visits the five manager slots and, for each live one, runs the
shot tick `0x003DA050` and then the shake tick `0x003DCFB0`. `0x003DA050(slot)` does nothing without a
shot list at `+0xD8`; otherwise:

1. For frames 0 (main) and 1 (sub), when the channel named in `+0x18[frame]` is not idle, it
   tells that channel's player its frame (`0x002563C0`, player `+0x184`).
2. For each non-idle channel that has not finished, the step is `0x02B4E4B0 × rate × 0x01DFE0BC`; the
   clock grows by it once the channel's run byte is set, and the first positive step sets that
   byte.
3. It evaluates the shot at the clock (`0x002555A0` → `0x00258350`), or, when the manager's skip byte
   `+0x201` is set (`0x00267300`), runs it to its end (`0x00257A00`).
4. A player at its end marker (`0x002567B0` returns 2) marks the channel finished, state 2.

`0x01DFE0BC` is 1.0 at 30 fps and 0.5 at 60 fps
([game settings](../Saving-Loading-And-Settings/game-settings.md)), so a shot plays at the same speed at
either frame rate.

The shake tick `0x003DCFB0(slot)` keeps one shake table per manager, `0x3D0` bytes from `0x02ADDA78` for the manager
`+0x28`, with a `0xF0`-byte row per channel:

1. For each of the two frames whose channel `+0x1C[frame]` is set and running, it stores `0x003DA190` of the channel's
   `+0x174` word through `0x0037DB40(manager, channel, value)`, the dword at `0x02ADDA7C + manager × 0x3D0 + channel ×
   0xF0` (`0x003DD026`).
2. For each of the four running channels, it reads the dword at `0x02ADDA78 + manager × 0x3D0 + channel × 0xF0`
   through `0x0037DCC0(manager, channel)` (`0x003DD075`); a value of 2 marks the channel finished.

### Publishing a shot

`0x002555D0` runs once per frame over the 20 players (5 managers × 4 channels), manager 4 first and
manager 0 last, so the lowest manager wins a conflict. For each player with a frame it calls
`0x0025A3B0(frame, 5, view)`:

- frame 0 copies the player's 0xD0-byte view (`+0x210`) into camera record 5 (`0x0025A2C0`) and
  sets its mode to 3 (`0x0025A500`);
- frame 1 copies it into the sub view `0x02097B80` (`0x0025A3D0`).

Once the field is loaded (`[0x02ADD0D8]` through `0x00377DB0`), both copies then replace the view's floats `+0x00`
and `+0x04`: with `0x02098DE0` / `0x02098DE4` while byte `0x02098DE8` is set, else with `0x0209A6EC` / `0x0209A6F0`,
dwords 2 and 3 of the map pack's section 11 (`0x0025A359`-`0x0025A3A0`, `0x0025A45F`-`0x0025A47A`;
[MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

Then the two transition cameras: when `0x00257520` is blending it writes record 5 from `0x02096410`
with mode 3, and when `0x00255850` is moving it writes record 5 from `0x02096290`. Last,
`0x0025A520(5, any)` sets bit 5 of the active mask `0x02098DEC` when any of these wrote, and clears it
otherwise.

### The camera records and the active view

Eight camera records of 0x110 bytes sit at `0x02097300`. `0x00259820` takes the highest set bit of
`0x02098DEC` (bit 7 down to 0) and its record:

| Record mode `+0xF0` | View published |
|---|---|
| 1 | built by `0x00259990` from the record's `+0xF4` |
| 2 | the previous frame's view, unchanged |
| 3 | the record's view `+0x20` as written |
| other | rebuilt by `0x003CC000` from the eye `+0x00` and target `+0x10`, up `(0, 1, 0)` |

It keeps the result at `0x020972F0` and submits it at priority `0x14` (below). With no bit set it
submits nothing. So record 5 outranks records 0-4 and yields to 6 and 7.

### Resetting the records

`0x00259E90`, from the boot `0x00266D10`, runs the follow-camera set-up `0x00259B30`, clears the active
mask `0x02098DEC`, the bytes `0x02098DE9` to `0x02098DEB` and the words `0x02098DE0`, `0x02098DE4`, `0x02098DE8`
and `0x020972F0`, and resets every record: eye `(−3, 4, −8, 1)`, target `(0, 0, 0, 1)`, the view
zeroed and rebuilt (`0x003CBFF0`), mode and parameter 0. It zeroes and rebuilds the sub view `0x02097B80`
and the behind camera's view `0x02097C50` the same way.

`0x0025A890`, from the render manager's target rebuild `0x00188B10`, sets the field of view of the eight
record views, `0x02097B80` and `0x02097C50` back to π/4 at `+0x08` and `+0x0C`, with `+0x10` =
`1 / tan(π/8)` (`0x003CBAD0`). `0x00258130`, from the same rebuild (`0x00188B27`), runs `0x003CBAD0` on twenty more
views from `0x02092A40`: five groups `0xBB0` apart, four views `0x2E0` apart in each.

The debug verbs `debug_camerasrc` (`0x2013`, `0x0050E5B0`) and `debug_cameradst` (`0x2012`, `0x0050E530`)
pop three floats each and write them, with w 1.0, as record 1's eye (`0x0025A4A0`) or target
(`0x0025A4D0`); the third float popped is x. `debug_cameraescape` (`0x2077`, `0x0050CD30`) pops three ints
and stores the first popped as a byte at `+0x188` of the shot player chosen by the third (manager) and
the second (channel) (`0x00257AA0`; players at `0x02092830 + manager × 0xBB0 + channel × 0x2E0`).

### Returning to the behind camera

`resumebehindcamera(frames, a, b)` (`0x01E4`, `0x003442D0`) and its four-argument form (`0x0289`,
`0x00343DB0`, with a pose index last) clear the current manager's shot channels and frame owners and
call `0x00257830`, which arms a blend:

- duration `frames × 0x01DFE0B8`, the counter at 0;
- the start pose, entry `index` of the poses at `0x02096370` (0x40 apart) that the shot player
  writes, turned into polar form about its target (`0x003CC130`);

- the polar form is the distance, the yaw `atan2(dx, dz)`, and the pitch read after turning the
  offset back by the yaw about the up axis with `0x005068C0(matrix, axis, angle)`, which builds the
  axis-angle rotation matrix from `sinf` and `cosf`;

- `a` at `0x02096400` and `b`, the ease, at `0x02096404`.

Each frame `0x00257520` takes the behind camera's view (`0x002593A0`, built into `0x02097C50`), eases
`t = counter / duration` with `0x00256650(b, t)`, and interpolates target, heading, pitch, distance
and field of view from the start pose toward it, and the roll toward 0. The heading goes the
shorter way round, decided on the first frame. It writes record 5 and counts up until the duration ends; a duration
of 0 blends nothing.

| `0x00256650(kind, t)` | Ease |
|---|---|
| 0 | `(sin(πt − π/2) + 1) / 2`, slow at both ends |
| 1 | `sin(πt/2 − π/2) + 1`, slow start |
| 2 | `sin(πt/2)`, slow end |
| other | `t` |

`behindtoeventcamera` (`0x034F`, `0x00349FA0`) is the other transition: through `0x003DA300` it takes
a shot row and arms `0x00255C50`, whose move `0x00255850` writes record 5 from `0x02096290`.

### Waiting on a transition

Each transition keeps a duration and a counter: `0x02096270`/`0x02096274` for the move to the event camera,
`0x020963F8`/`0x020963FC` for the swing back to the behind camera. A transition is done when the duration
is 0 or the counter has reached it (`0x00255C20`, `0x00257800`).

- `behindtoeventcamerasync` (`0x0350`, `0x0034A530`) and `resumebehindcamerasync` (`0x01E5`,
  `0x003445E0`) hold the script until their transition is done.
- When the manager is skipping (`0x00267310`), they instead set the counter to the duration less one
  and run the step once (`0x00255CB0` with `0x00255850`, `0x002578B0` with `0x00257520`), so the camera lands on
  its final pose, and release the script.

### The behind camera's field of view and roll

`behindcamerafovyroll` (`0x023A`, `0x00349D00`) pops a float, a float, an int and a float. `0x002564D0`
keeps them as the roll target `0x020964F4`, the field-of-view target `0x020964F0`, the ease `0x02096500` and
the duration, the last value times `0x01DFE0B8`, at `0x020964F8`, and zeroes the counter `0x020964FC`.

Each frame the shake gather `0x0037D4C0` asks `0x002563F0` for the two offsets. With a duration of 0 they are
the targets; otherwise each target is multiplied by `0x00256650(ease, counter / duration)`. The counter
then grows by 1 until it passes the duration. The gather adds the offsets to the shake's roll and
field-of-view scalars, which reach `0x02AEDF98` and `0x02AEDF9C` through `0x00382B70`.

`behindcamerafovyrollsync` (`0x023B`, `0x0034A600`) holds the script while the counter has not passed
the duration (`0x002564B0`); a skip sets the counter one past it (`0x00256500`).

At each field start `0x00259B30` clears the ramp through `0x003DA2C0`, which calls `0x002564D0(0, 0, 0, 0)`:
both targets, the ease, the duration and the counter become 0, so the offsets are 0 until a script
sets them again.

`getbehindcameradir` (`0x0343`, `0x00347070`) returns the behind camera's direction in eighths
(`0x002565C0`): from the view `0x002593A0` returns it takes `atan2` of the eye minus the target in x and z
(`+0x90`, `+0x98` minus `+0xA0`, `+0xA8`), adds π/8, wraps it into 0 to 2π and divides by π/4, giving
0 to 7. When the eye and the target share x and z it returns 0.

### The summon camera's subject

`setsummoncameratarget(id, on)` (`0x0271`, `0x00341410`) makes the actor `id` names (`0x00264010`, the
party focus for a negative id) the subject `0x02096508` through `0x002578F0`, or clears the subject when
`on` is 0. Clearing it also drops the mark bit `0x8000` from every other live actor's fade word and
keeps the fade running while any actor was marked.

The fade word is a `u16` of the actor's `+0xC0` context: `0x00263EB0(actor, i)` and
`0x0026A3B0(actor, i, v)` read and write `+0x20 + 2i`, `i` clamped to 1 and taken as 0 when negative,
and `0x00263E80` reads `+0x20`. Bit `0x8000` marks the actor; the low byte is its fade level.

Each field frame `0x00256F60` (from `0x0022A770`) boxes the subject and every other live actor of the
five managers on screen with `0x00255CF0`. That function places the points `(−r, 0, 0)` and `(r, h, 0)`
in the camera's orientation at the actor's position, `r` and `h` from `0x00265090` and `0x00263940`,
projects both through `0x02AEDDB0`, divides x and y by the third value and subtracts 1792 and 1824,
giving the corners of a 512 × 448 frame. Then for each other actor:

- the mark is cleared when the actor's depth value `+0x08` is not above the subject's or the two boxes
  do not overlap;
- the mark is set when the actor's box reaches more than 16 into the subject's box on all four sides;
- otherwise the word stays as it was.

While a mark changed or a fade runs (`0x02096510`), `0x00255FF0(step)` moves every other live actor's
level by the step `0x02096514` (`0x20`, set by `0x002556F0`): up toward 255 when marked, down toward 0
when not. It writes the word back, sets the actor's render record colour `+0x220` to `+0x228` to
1.0 and its alpha `+0x22C` to `(255 − level) / 255`, and returns 1 once every level has arrived,
which ends the fade. So the marked actors, those that cover the subject, fade out over eight frames.

### Running a shot to its end

The skip path `0x00257A00` reads two things from a shot player through small getters: `0x00258AF0(manager,
channel)` returns from the current row's first byte (player `+0x178`): 1 for kind 1, the word `+0x22`
for kind 2, 0 for kind −1 and 1 for any other kind; `0x00258B50` returns the player's `+0x0C`. A negative
channel selects the transition player at `0x02096520` instead.

The transition player is a `0x2E0`-byte shot player like the twenty in the groups. The actor-system reset
`0x002556F0` clears it (`0x00861EC0` at `0x002557C9`), stores −1 in its frame `+0x184` (`0x020966A4`, `0x002557D5`), resets
its view `+0x210` through `0x003CBFF0` (`0x002557DF`) and then stores 0 in the frame (`0x002557F3`), so it starts on frame
0, the main view.

The shot evaluation `0x00258350` reads that frame when it is given a negative channel
(`0x002583CB`, `0x002583D2`) and writes the evaluated pose into entry `frame` of the poses at `0x02096370`, `0x40` apart
(`0x00258687`-`0x002586D2`).

The clear of the frames, `0x00255810` (from the tick `0x00314020` at `0x003140F0` and from `0x003143D0` at `0x003143EB`), walks the twenty group players
(`0x00255820`-`0x0025584D`, from `0x020929B4` in steps of `0xBB0`).

### Submissions

`0x003829D0(camera, priority)` files a 0xD0-byte camera into the first free of eight 0xE0-byte
slots at `0x02AED630`, with the priority at `+0xD4` and the submitted flag at `+0xD0`; with all
eight taken it drops the camera. When `0x00181DD0` reports an override it first applies three vectors
from `0x00181CD0`, `0x00181C50` and `0x00181CB0` to the camera (`0x003CC000`). There are three submitters:

| Caller | Camera | Priority |
|---|---|---|
| `0x00259820` | the active record's view | `0x14` |
| `0x00259970`, from the field frame before draw 1 | the sub view `0x02097B80` | `0x14` |
| `0x003ED8A0`, the effect-file camera | `0x02096D30` (`0x003ED9A2`) | `0x64` |

### Choosing the camera

The camera update `0x003820C0` (called through `0x0036F510`) stores the aspect `0x00229D20()` at
`0x02AED4E0` and `0x02AED540` ([screen mode and aspect](screen-mode-and-aspect.md)) and walks the
eight slots in order. Each submitted slot has its flag cleared and wins when its priority is
strictly above the best so far, which starts at −1. So the highest priority wins, the earliest
submission wins a tie, and every submission lasts one frame. With none, the update returns and
the previous frame's matrices stand. The winner is copied into the working camera at `0x02AED560`.

### Shake and the build

The shake gather `0x0037D4C0` hands two offset vectors and two scalars to `0x00382B70`, which stores
them at `0x02AEDF70` (eye), `0x02AEDF80` (target), `0x02AEDF98` (roll) and `0x02AEDF9C` (field of view).
The update then:

1. adds `0x02AEDF9C` to the field of view `+0x08` and recomputes `+0x10 = 1 / tan(fov / 2)`;
2. adds `0x02AEDF98` to the roll `+0xC4`;
3. turns both offsets by the camera's matrix `+0x60` (`0x02AED5C0`) and adds them to the eye `+0x90`
   and the target `+0xA0`, so a shake moves in the camera's own frame;
4. rebuilds the matrices from eye, target and roll (`0x003CBD60`);
5. does the same to a stack copy whose field of view is `+0x0C`, replaced by π/4 when above 1.0,
   plus the shake.

### The matrices

| Matrix | Built from |
|---|---|
| `0x02AEDD70` | the head matrix of `0x02AED4A0` × a projection of the copy with aspect 16/9 and scale 1.1547 (`0x003CBA50`) |
| `0x02AEDD30` | the head matrix × the working camera's projection (`0x003CBB30`); handed to `0x0024E180` |
| `0x02AEDE70` | the view: a copy of `+0x20` (`0x02AED580`), eight elements replaced under the override |
| `0x02AEDEB0` | a copy of the camera matrix `+0x60`; handed to the device (`0x00182640`) |
| `0x02AEDEF0` | the copy's camera matrix; its fourth row `0x02AEDF20` is the camera position |
| `0x02AEDDF0` | view × projection, world to clip |
| `0x02AEDDB0` | view × `0x02AEDD30` |
| `0x02AEDE30` | view × a projection with near 1.0 and far 1000 (`0x003CBC40`) |
| `0x02AEDF94` | the heading, `atan2f` of the view's `0x02AEDE90` and `0x02AEDE98` |

| `0x02B40470` | `0x02AED500` × the working camera's projection (`0x003CBB30`), copied there by `0x003B4150`; the update `0x003820C0` does it on one of its paths, and only while `0x00182570` returns 0; and `0x002F5550` and `0x00474710` also call `0x003B4150` |

`0x003B40B0(z)` and `0x003B40F0(z)` turn a depth into `(m[+0x38] − z × m[+0x28]) / (m[+0x3C] − z × m[+0x2C])`
with the elements of `0x02B40470`; `0x002F5550`, `0x00474710` and `0x0024FF60` call them.

The camera code's small helpers: `0x003CBCA0` writes the first three rows of an identity matrix (for
`0x003CBD60` and `0x0054C6B0`); `0x003CC480(a, b, c, out)` builds a rotation matrix from three angles with
`sinf` and `cosf`; `0x003CC270(from, to, heading, distance)` returns the distance in the x–z plane and
the heading `atan2(dx, dz)`, for the shot builders `0x00255E80` and `0x00256CA0`; and
`0x003CC3C0(origin, heading, distance, out)` places a point at that distance along the heading
(`0x003CC480` with only the heading), for `0x00257D10` and `0x00257F60`.

### The Screen Shake option

Besides the scripted shakes, `0x0037D4C0` adds an accumulator row `0x02EBF380 + draw × 0x20` while
`0x02EBF3C0` is set. `deny_camerashake_without_event(n)` (`0x04B6`, `0x003560D0`) stores `n == 0` in
`0x02EBF3C0`; the area unload `0x002628B0` and the manager bind `0x0026CE60` also write it.

`0x0037D970`
computes the row's values from the camera's eye and target (`0x003D83A0`) every time, and writes the
row only when the pointer `0x02089350` is set or both `0x02EBF3C4` and `0x02EBF3C0` are set.
`0x02EBF3C4` is the Screen Shake option, stored by `0x0037DDC0`
([config screen](../Menus-And-HUD/config-screen.md)). With the option off the row is not refreshed and
keeps its last values; the scripted shakes are not gated.

### Handing the camera to the renderer

After the build the camera update calls `0x00182640` with the camera matrix `0x02AEDEB0`, the aspect, the
field of view `+0x08`, the frame-mode zoom (`0x00229D60`), the camera's `+0x00` and `+0x04` (the near and
far distances `0x003CBB30` uses) and a flag that is set while the bound map `[0x0209A670]` has a non-zero
`+0x120`. `0x00182640` runs `0x001897C0` on the render manager (`0x00189120`).

`0x001897C0` stores the near and far distances, the field of view, the aspect and the zoom at manager
`+0xCBC`, `+0xCC0`, `+0xCC4`, `+0xCC8` and `+0xCCC`; with the flag set and `+0xCD0` greater than the
near distance, the far distance becomes `+0xCD0`. It then fills the two camera objects of the copy
chosen by the manager's byte `+0x1C` (`0x338` bytes apart):

- the scene camera at `+0x20`, with the matrix at `+0xF8` converted from `0x02AEDEB0` with its x and y
  terms negated, or a fixed default when any row of the source is all zero;
- a second camera at `+0x1B0`, matrix `+0x288`, the same rotation without the translation and with the
  far distance raised to at least 1000.

Each value it sets on a camera (aspect `+0xC8`, field of view `+0xD0`, zoom `+0xD4`, near `+0xC0`,
far `+0xC4`) is followed by the camera's slot `+0x08`, and `0x0018A120` rebuilds the camera last.

`0x0018A680(holder, camera)` copies a camera object into the holder's camera at `+0xE0` the same way: the
first eight words of the matrix `[camera + 0xB8]` into `+0x1B8` (with its word 11 at `+0x1E4`), the aspect,
field of view, zoom and near distance, and the far distance raised to at least 1000, each followed by slot
`+0x08`, then `0x0018A120(+0xE8)`. `0x00186670`, `0x00187950` and `0x00189570` call it.

## Layouts

Camera record [8] at `0x02097300`, stride `0x110`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | eye | source eye for the rebuild |
| `+0x10` | `f32[4]` | target | source target for the rebuild |
| `+0x20` | `u8[208] view` | the camera below |  |
| `+0xF0` | `u32` | mode | 1, 2, 3 or other (`0x00259820`) |
| `+0xF4` | `u32` | param | for mode 1 |

Camera (`0xD0`), as the update reads it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | value0 | 0.1 after a rebuild (`0x003CBBE0`); replaced by the copies `0x0025A2C0` / `0x0025A3D0` |
| `+0x04` | `f32` | value1 | 1000.0 after a rebuild; replaced by the same copies |
| `+0x08` | `f32` | fov | radians |
| `+0x0C` | `f32` | fovCopy | the second copy's field of view |
| `+0x10` | `f32` | projScale | 1 / tan(fov / 2) |
| `+0x20` | `f32[16]` | view | copied to `0x02AEDE70` |
| `+0x60` | `f32[16]` | world | camera matrix; +`0x90` is its fourth row, the eye |
| `+0xA0` | `f32[4]` | target |  |
| `+0xC4` | `f32` | roll |  |

Submission slot [8] at `0x02AED630`, stride `0xE0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[208]` | camera |  |
| `+0xD0` | `u32` | submitted | 1 until the next update |
| `+0xD4` | `i32` | priority |  |

## Shipped data

Counted in the decompiled `us` scripts (1,114 files):

| Fact | Value |
|---|---|
| `camerastart` (all forms) | 4,322 calls in 430 scripts |
| `cameraclear` | 873 calls in 433 scripts |
| `camerasync` (both forms) | 617 calls in 135 scripts |
| `camerastop_54` | 113 calls in 30 scripts |
| `camerachange` | 88 calls in 30 scripts |
| `cameraratio` (both forms) | 92 calls in 33 scripts |
| `resumebehindcamera` | 43 calls in 30 scripts; 38 of them `(0, 0, 2)`, an immediate return |
| `camerahitcheck` | 8 calls in 2 scripts |
| `behindtoeventcamera` | 2 calls |
| shake verbs | `camerashakestart` 328, `camerashakeclear` 315, `camerashakestop` 180 |

[`scripted-camera-camerashake-census.tsv`](scripted-camera-camerashake-census.tsv) counts the shake calls by verb, and
[`scripted-camera-camerashake-channels.tsv`](scripted-camera-camerashake-channels.tsv) by start channel and bank index, with
the scripts that make them.

## State

Every global below is 0 at load (the zero-filled tail of `.data`).

### The working camera's eye and roll

The working camera at `0x02AED560` keeps its eye in the fourth row `+0x90` of its camera matrix, so `0x02AED5F0` is the
eye's x, and its roll at `+0xC4`. The update `0x003820C0` copies the winning slot over the camera with 16-byte stores,
then adds the shake to the eye and the roll:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AED5F4` | `f32` | 0 | the eye's y, `+0x94` | `0x003820C0`: the winner's copy (`0x003822B5`, 16 bytes over `0x02AED5F0`-`0x02AED5FF`), plus the turned eye offset (`0x00382476`) | `0x003820C0` (`0x0038233D` in its 16-byte copy to the stack, `0x00382452`, `0x00382541`); `0x003CBD60` (`0x003CBDB5`); `0x003CBFA0` (`0x003CBFBC`); `0x0037D970` (`0x0037D9A2`); `0x00202C90` and `0x00203080` as part of the vector `0x02AED5F0`; `0x002F1F40` (`0x002F1FDC`, `0x002F2018`), `0x0043F2B0` (`0x0043F2FE`, `0x0043F368`) and `0x005002E0` (`0x00500324`, `0x0050038A`), each a 16-byte load of the row `0x02AED5F0` |
| `0x02AED5F8` | `f32` | 0 | the eye's z, `+0x98` | `0x003820C0`: the winner's copy (`0x003822B5`), plus the turned eye offset (`0x0038247E`) | `0x003820C0` (`0x0038233D`, `0x00382468`, `0x0038256A`); `0x003CBD60` (`0x003CBDC3`); `0x003CBFA0` (`0x003CBFD1`); `0x0037D970` (`0x0037D9B5`); `0x00202C90` and `0x00203080` as part of the vector `0x02AED5F0`; `0x002F1F40` (`0x002F1FDC`, `0x002F2018`), `0x0043F2B0` (`0x0043F2FE`, `0x0043F368`) and `0x005002E0` (`0x00500324`, `0x0050038A`), each a 16-byte load of the row `0x02AED5F0` |
| `0x02AED624` | `f32` | 0 | the roll, `+0xC4` | `0x003820C0`: the winner's copy (`0x003822D6`, 16 bytes over `0x02AED620`-`0x02AED62F`), plus the shake roll `0x02AEDF98` (`0x003823DA`) | `0x003820C0` (`0x0038235D` in its copy to the stack, `0x003823BE`); `0x003CBD60` (`0x003CBE05`) |

`0x003CBD60` runs on the camera from `0x00382486` (`0x00382406`), and `0x003CBFA0`, the vector from the eye to the target,
runs on it from `0x0029BC80`, `0x002DF2C0`, `0x002DF560` and `0x003F1A60`. The 16-byte copy `0x00202C90` takes the eye
`0x02AED5F0` from `0x002C7660`, `0x002C7B10`, `0x003F2CF0`, `0x003F3010`, `0x003F5100`, `0x003F5260`, `0x003F5430` and `0x003FB3E0`; the
vector difference `0x00203080` takes it from `0x0028A090`, `0x003F1A60`, `0x003F35C0`, `0x003F7200`, `0x00505570` and `0x00505E00`.

### The submitted flags

Slot n's submitted flag is the `u32` at `0x02AED630` + n × `0xE0` + `0xD0`. Slot 0's is `0x02AED700`; slots 1 to 7 are:

| Global | Slot | Set by | Read by |
|---|---|---|---|
| `0x02AED7E0` | 1 | `0x00382910`, 0 at boot (`0x00382930`); `0x003820C0`, 0 when it reads the slot (`0x00382147`); `0x003829D0`, 1 (`0x00382B07`) | `0x003820C0` (`0x00382138`); `0x003829D0` (`0x00382A70`) |
| `0x02AED8C0` | 2 | `0x00382910` (`0x00382936`); `0x003820C0` (`0x00382169`); `0x003829D0` | `0x003820C0` (`0x0038215A`); `0x003829D0` |
| `0x02AED9A0` | 3 | `0x00382910` (`0x0038293C`); `0x003820C0` (`0x0038218B`); `0x003829D0` | `0x003820C0` (`0x0038217C`); `0x003829D0` |
| `0x02AEDA80` | 4 | `0x00382910` (`0x00382942`); `0x003820C0` (`0x003821AD`); `0x003829D0` | `0x003820C0` (`0x0038219E`); `0x003829D0` |
| `0x02AEDB60` | 5 | `0x00382910` (`0x00382948`); `0x003820C0` (`0x003821CF`); `0x003829D0` | `0x003820C0` (`0x003821C0`); `0x003829D0` |
| `0x02AEDC40` | 6 | `0x00382910` (`0x0038294E`); `0x003820C0` (`0x003821F1`); `0x003829D0` | `0x003820C0` (`0x003821E2`); `0x003829D0` |
| `0x02AEDD20` | 7 | `0x00382910` (`0x00382954`); `0x003820C0` (`0x00382213`); `0x003829D0` | `0x003820C0` (`0x00382204`); `0x003829D0` |

`0x003820C0` takes a slot whose flag equals 1 and `0x003829D0` files into the first slot whose flag is 0, setting the
priority `+0xD4` (`0x00382B01`) before the flag. A slot wins with a signed compare of its priority against the best
so far (`0x0038212B`, `0x0038214D` and on).

### The view's override elements

`0x003820C0` copies the working camera's view `+0x20` (`0x02AED580`) to `0x02AEDE70` with `0x00202C70` (`0x0038267A`). When
`0x00181DD0` reports an override it then replaces eight elements from the matrix `m` that `0x00181CF0` returns
(`0x00382694`-`0x00382712`); the element `+0x00`, `0x02AEDE70`, takes `-m[+0x0C]`:

| Global | Element | Type | Start | Override value |
|---|---|---|---|---|
| `0x02AEDE74` | `+0x04` | `f32` | 0 | `-m[+0x1C]` (`0x003826B9`) |
| `0x02AEDE78` | `+0x08` | `f32` | 0 | `-m[+0x2C]` (`0x003826C9`) |
| `0x02AEDE80` | `+0x10` | `f32` | 0 | `-m[+0x00]` (`0x003826D8`) |
| `0x02AEDE84` | `+0x14` | `f32` | 0 | `-m[+0x04]` (`0x003826E8`) |
| `0x02AEDE88` | `+0x18` | `f32` | 0 | `-m[+0x08]` (`0x003826F8`) |
| `0x02AEDEA0` | `+0x30` | `f32` | 0 | `m[+0x20]` (`0x00382705`) |
| `0x02AEDEA4` | `+0x34` | `f32` | 0 | `m[+0x24]` (`0x00382712`) |

The view is read as whole 16-byte rows by `0x0024C060` (`0x0024C10D`-`0x0024C130`), `0x004FDDA0` (`0x004FDDB2`-`0x004FDDEE`) and
`0x0051CDE0` (`0x0051CF17`-`0x0051CF8E`), and as a matrix through `0x00202C70`, `0x00202D70` and `0x00202D50` by `0x0028DC00`,
`0x002F4520`, `0x002F5550`, `0x003820C0` (`0x00382752`, `0x0038276C`, `0x003827D5`), `0x003F0170`, `0x003F0610`, `0x003F3710`,
`0x003F5430` and `0x003F7930`.

## Modding notes

- A camera submitted at a priority above `0x64` from a hook beats every camera in the game for that
  frame; it must be submitted every frame to stay.
- Shot speed follows `cameraratio` and the frame rate factor, not the frame count.
- `resumebehindcamera` with a non-zero frame count gives an eased swing back to the behind camera;
  0 frames cuts.
- The Screen Shake option does not stop scripted camera shakes.

## Related

- [EBP camera tables](../EBP-Script-Files/ebp-camera-tables.md): the shots and how a shot is
  played.
- [EBP camera shake](../EBP-Script-Files/ebp-camera-shake.md): the shake curves and
  oscillators behind `0x00382B70`.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the shot and shake channels.
- [Frame update order](../Engine-Core/frame-update-order.md): where `0x00314370`,
  `0x00259970` and the camera update run.
- [Screen mode and aspect](screen-mode-and-aspect.md): the aspect the projection uses.
- [Config screen](../Menus-And-HUD/config-screen.md): the Screen Shake row.
