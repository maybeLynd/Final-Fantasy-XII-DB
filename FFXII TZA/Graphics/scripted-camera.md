---
title: "Scripted camera: the shot channels, the camera record stack, and how a camera reaches the renderer"
kind: "system"
category: "Graphics"
addresses: "003DA050, 002555D0, 0025A3B0, 0025A2C0, 0025A500, 0025A520, 02097300, 02098DEC, 00259820, 00257830, 00257520, 00256650, 003829D0, 02AED630, 003820C0, 02AED560, 00382B70, 0037D4C0, 0037D970, 02AEDEF0"
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

The per-frame caller `00314370` visits the five manager slots and, for each live one, runs the
shot tick `003DA050` and then the shake tick `003DCFB0`. `003DA050(slot)` does nothing without a
shot list at `+0xD8`; otherwise:

1. For frames 0 (main) and 1 (sub), when the channel named in `+0x18[frame]` is not idle, it
   tells that channel's player its frame (`002563C0`, player `+0x184`).
2. For each non-idle channel that has not finished, the step is `02B4E4B0 × rate × 01DFE0BC`; the
   clock grows by it once the channel's run byte is set, and the first positive step sets that
   byte.
3. It evaluates the shot at the clock (`002555A0` → `00258350`), or, when the manager's skip byte
   `+0x201` is set (`00267300`), runs it to its end (`00257A00`).
4. A player at its end marker (`002567B0` returns 2) marks the channel finished, state 2.

`01DFE0BC` is 1.0 at 30 fps and 0.5 at 60 fps
([game settings](../Saving-Loading-And-Settings/game-settings.md)), so a shot plays at the same speed at
either frame rate.

The shake tick `003DCFB0(slot)` keeps one shake table per manager, `0x3D0` bytes from `02ADDA78` for the manager
`+0x28`, with a `0xF0`-byte row per channel:

1. For each of the two frames whose channel `+0x1C[frame]` is set and running, it stores `003DA190` of the channel's
   `+0x174` word through `0037DB40(manager, channel, value)`, the dword at `02ADDA7C + manager × 0x3D0 + channel ×
   0xF0` (`003DD026`).
2. For each of the four running channels, it reads the dword at `02ADDA78 + manager × 0x3D0 + channel × 0xF0`
   through `0037DCC0(manager, channel)` (`003DD075`); a value of 2 marks the channel finished.

### Publishing a shot

`002555D0` runs once per frame over the 20 players (5 managers × 4 channels), manager 4 first and
manager 0 last, so the lowest manager wins a conflict. For each player with a frame it calls
`0025A3B0(frame, 5, view)`:

- frame 0 copies the player's 0xD0-byte view (`+0x210`) into camera record 5 (`0025A2C0`) and
  sets its mode to 3 (`0025A500`);
- frame 1 copies it into the sub view `02097B80` (`0025A3D0`).

Once the field is loaded (`[02ADD0D8]` through `00377DB0`), both copies then replace the view's floats `+0x00`
and `+0x04`: with `02098DE0` / `02098DE4` while byte `02098DE8` is set, else with `0209A6EC` / `0209A6F0`,
dwords 2 and 3 of the map pack's section 11 (`0025A359`-`0025A3A0`, `0025A45F`-`0025A47A`;
[MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

Then the two transition cameras: when `00257520` is blending it writes record 5 from `02096410`
with mode 3, and when `00255850` is moving it writes record 5 from `02096290`. Last,
`0025A520(5, any)` sets bit 5 of the active mask `02098DEC` when any of these wrote, and clears it
otherwise.

### The camera records and the active view

Eight camera records of 0x110 bytes sit at `02097300`. `00259820` takes the highest set bit of
`02098DEC` (bit 7 down to 0) and its record:

| Record mode `+0xF0` | View published |
|---|---|
| 1 | built by `00259990` from the record's `+0xF4` |
| 2 | the previous frame's view, unchanged |
| 3 | the record's view `+0x20` as written |
| other | rebuilt by `003CC000` from the eye `+0x00` and target `+0x10`, up `(0, 1, 0)` |

It keeps the result at `020972F0` and submits it at priority `0x14` (below). With no bit set it
submits nothing. So record 5 outranks records 0-4 and yields to 6 and 7.

### Resetting the records

`00259E90`, from the boot `00266D10`, runs the follow-camera set-up `00259B30`, clears the active
mask `02098DEC`, the bytes `02098DE9` to `02098DEB` and the words `02098DE0`, `02098DE4`, `02098DE8`
and `020972F0`, and resets every record: eye `(−3, 4, −8, 1)`, target `(0, 0, 0, 1)`, the view
zeroed and rebuilt (`003CBFF0`), mode and parameter 0. It zeroes and rebuilds the sub view `02097B80`
and the behind camera's view `02097C50` the same way.

`0025A890`, from the render manager's target rebuild `00188B10`, sets the field of view of the eight
record views, `02097B80` and `02097C50` back to π/4 at `+0x08` and `+0x0C`, with `+0x10` =
`1 / tan(π/8)` (`003CBAD0`). `00258130`, from the same rebuild (`00188B27`), runs `003CBAD0` on twenty more
views from `02092A40`: five groups `0xBB0` apart, four views `0x2E0` apart in each.

The debug verbs `debug_camerasrc` (`0x2013`, `0050E5B0`) and `debug_cameradst` (`0x2012`, `0050E530`)
pop three floats each and write them, with w 1.0, as record 1's eye (`0025A4A0`) or target
(`0025A4D0`); the third float popped is x. `debug_cameraescape` (`0x2077`, `0050CD30`) pops three ints
and stores the first popped as a byte at `+0x188` of the shot player chosen by the third (manager) and
the second (channel) (`00257AA0`; players at `02092830 + manager × 0xBB0 + channel × 0x2E0`).

### Returning to the behind camera

`resumebehindcamera(frames, a, b)` (`0x01E4`, `003442D0`) and its four-argument form (`0x0289`,
`00343DB0`, with a pose index last) clear the current manager's shot channels and frame owners and
call `00257830`, which arms a blend:

- duration `frames × 01DFE0B8`, the counter at 0;
- the start pose, entry `index` of the poses at `02096370` (0x40 apart) that the shot player
  writes, turned into polar form about its target (`003CC130`);

- the polar form is the distance, the yaw `atan2(dx, dz)`, and the pitch read after turning the
  offset back by the yaw about the up axis with `005068C0(matrix, axis, angle)`, which builds the
  axis-angle rotation matrix from `sinf` and `cosf`;

- `a` at `02096400` and `b`, the ease, at `02096404`.

Each frame `00257520` takes the behind camera's view (`002593A0`, built into `02097C50`), eases
`t = counter / duration` with `00256650(b, t)`, and interpolates target, heading, pitch, distance
and field of view from the start pose toward it, and the roll toward 0. The heading goes the
shorter way round, decided on the first frame. It writes record 5 and counts up until the duration ends; a duration
of 0 blends nothing.

| `00256650(kind, t)` | Ease |
|---|---|
| 0 | `(sin(πt − π/2) + 1) / 2`, slow at both ends |
| 1 | `sin(πt/2 − π/2) + 1`, slow start |
| 2 | `sin(πt/2)`, slow end |
| other | `t` |

`behindtoeventcamera` (`0x034F`, `00349FA0`) is the other transition: through `003DA300` it takes
a shot row and arms `00255C50`, whose move `00255850` writes record 5 from `02096290`.

### Waiting on a transition

Each transition keeps a duration and a counter: `02096270`/`02096274` for the move to the event camera,
`020963F8`/`020963FC` for the swing back to the behind camera. A transition is done when the duration
is 0 or the counter has reached it (`00255C20`, `00257800`).

- `behindtoeventcamerasync` (`0x0350`, `0034A530`) and `resumebehindcamerasync` (`0x01E5`,
  `003445E0`) hold the script until their transition is done.
- When the manager is skipping (`00267310`), they instead set the counter to the duration less one
  and run the step once (`00255CB0` with `00255850`, `002578B0` with `00257520`), so the camera lands on
  its final pose, and release the script.

### The behind camera's field of view and roll

`behindcamerafovyroll` (`0x023A`, `00349D00`) pops a float, a float, an int and a float. `002564D0`
keeps them as the roll target `020964F4`, the field-of-view target `020964F0`, the ease `02096500` and
the duration, the last value times `01DFE0B8`, at `020964F8`, and zeroes the counter `020964FC`.

Each frame the shake gather `0037D4C0` asks `002563F0` for the two offsets. With a duration of 0 they are
the targets; otherwise each target is multiplied by `00256650(ease, counter / duration)`. The counter
then grows by 1 until it passes the duration. The gather adds the offsets to the shake's roll and
field-of-view scalars, which reach `02AEDF98` and `02AEDF9C` through `00382B70`.

`behindcamerafovyrollsync` (`0x023B`, `0034A600`) holds the script while the counter has not passed
the duration (`002564B0`); a skip sets the counter one past it (`00256500`).

At each field start `00259B30` clears the ramp through `003DA2C0`, which calls `002564D0(0, 0, 0, 0)`:
both targets, the ease, the duration and the counter become 0, so the offsets are 0 until a script
sets them again.

`getbehindcameradir` (`0x0343`, `00347070`) returns the behind camera's direction in eighths
(`002565C0`): from the view `002593A0` returns it takes `atan2` of the eye minus the target in x and z
(`+0x90`, `+0x98` minus `+0xA0`, `+0xA8`), adds π/8, wraps it into 0 to 2π and divides by π/4, giving
0 to 7. When the eye and the target share x and z it returns 0.

### The summon camera's subject

`setsummoncameratarget(id, on)` (`0x0271`, `00341410`) makes the actor `id` names (`00264010`, the
party focus for a negative id) the subject `02096508` through `002578F0`, or clears the subject when
`on` is 0. Clearing it also drops the mark bit `0x8000` from every other live actor's fade word and
keeps the fade running while any actor was marked.

The fade word is a `u16` of the actor's `+0xC0` context: `00263EB0(actor, i)` and
`0026A3B0(actor, i, v)` read and write `+0x20 + 2i`, `i` clamped to 1 and taken as 0 when negative,
and `00263E80` reads `+0x20`. Bit `0x8000` marks the actor; the low byte is its fade level.

Each field frame `00256F60` (from `0022A770`) boxes the subject and every other live actor of the
five managers on screen with `00255CF0`. That function places the points `(−r, 0, 0)` and `(r, h, 0)`
in the camera's orientation at the actor's position, `r` and `h` from `00265090` and `00263940`,
projects both through `02AEDDB0`, divides x and y by the third value and subtracts 1792 and 1824,
giving the corners of a 512 × 448 frame. Then for each other actor:

- the mark is cleared when the actor's depth value `+0x08` is not above the subject's or the two boxes
  do not overlap;
- the mark is set when the actor's box reaches more than 16 into the subject's box on all four sides;
- otherwise the word stays as it was.

While a mark changed or a fade runs (`02096510`), `00255FF0(step)` moves every other live actor's
level by the step `02096514` (`0x20`, set by `002556F0`): up toward 255 when marked, down toward 0
when not. It writes the word back, sets the actor's render record colour `+0x220` to `+0x228` to
1.0 and its alpha `+0x22C` to `(255 − level) / 255`, and returns 1 once every level has arrived,
which ends the fade. So the marked actors, those that cover the subject, fade out over eight frames.

### Running a shot to its end

The skip path `00257A00` reads two things from a shot player through small getters: `00258AF0(manager,
channel)` returns from the current row's first byte (player `+0x178`): 1 for kind 1, the word `+0x22`
for kind 2, 0 for kind −1 and 1 for any other kind; `00258B50` returns the player's `+0x0C`. A negative
channel selects the transition player at `02096520` instead.

### Submissions

`003829D0(camera, priority)` files a 0xD0-byte camera into the first free of eight 0xE0-byte
slots at `02AED630`, with the priority at `+0xD4` and the submitted flag at `+0xD0`; with all
eight taken it drops the camera. When `00181DD0` reports an override it first applies three vectors
from `00181CD0`, `00181C50` and `00181CB0` to the camera (`003CC000`). There are three submitters:

| Caller | Camera | Priority |
|---|---|---|
| `00259820` | the active record's view | `0x14` |
| `00259970`, from the field frame before draw 1 | the sub view `02097B80` | `0x14` |
| `003ED8A0`, the effect-file camera | `02096D30` (`003ED9A2`) | `0x64` |

### Choosing the camera

The camera update `003820C0` (called through `0036F510`) stores the aspect `00229D20()` at
`02AED4E0` and `02AED540` ([screen mode and aspect](screen-mode-and-aspect.md)) and walks the
eight slots in order. Each submitted slot has its flag cleared and wins when its priority is
strictly above the best so far, which starts at −1. So the highest priority wins, the earliest
submission wins a tie, and every submission lasts one frame. With none, the update returns and
the previous frame's matrices stand. The winner is copied into the working camera at `02AED560`.

### Shake and the build

The shake gather `0037D4C0` hands two offset vectors and two scalars to `00382B70`, which stores
them at `02AEDF70` (eye), `02AEDF80` (target), `02AEDF98` (roll) and `02AEDF9C` (field of view).
The update then:

1. adds `02AEDF9C` to the field of view `+0x08` and recomputes `+0x10 = 1 / tan(fov / 2)`;
2. adds `02AEDF98` to the roll `+0xC4`;
3. turns both offsets by the camera's matrix `+0x60` (`02AED5C0`) and adds them to the eye `+0x90`
   and the target `+0xA0`, so a shake moves in the camera's own frame;
4. rebuilds the matrices from eye, target and roll (`003CBD60`);
5. does the same to a stack copy whose field of view is `+0x0C`, replaced by π/4 when above 1.0,
   plus the shake.

### The matrices

| Matrix | Built from |
|---|---|
| `02AEDD70` | the head matrix of `02AED4A0` × a projection of the copy with aspect 16/9 and scale 1.1547 (`003CBA50`) |
| `02AEDD30` | the head matrix × the working camera's projection (`003CBB30`); handed to `0024E180` |
| `02AEDE70` | the view: a copy of `+0x20` (`02AED580`), eight elements replaced under the override |
| `02AEDEB0` | a copy of the camera matrix `+0x60`; handed to the device (`00182640`) |
| `02AEDEF0` | the copy's camera matrix; its fourth row `02AEDF20` is the camera position |
| `02AEDDF0` | view × projection, world to clip |
| `02AEDDB0` | view × `02AEDD30` |
| `02AEDE30` | view × a projection with near 1.0 and far 1000 (`003CBC40`) |
| `02AEDF94` | the heading, `atan2f` of the view's `02AEDE90` and `02AEDE98` |

| `02B40470` | `02AED500` × the working camera's projection (`003CBB30`), copied there by `003B4150`; the update `003820C0` does it on one of its paths, and only while `00182570` returns 0; and `002F5550` and `00474710` also call `003B4150` |

`003B40B0(z)` and `003B40F0(z)` turn a depth into `(m[+0x38] − z × m[+0x28]) / (m[+0x3C] − z × m[+0x2C])`
with the elements of `02B40470`; `002F5550`, `00474710` and `0024FF60` call them.

The camera code's small helpers: `003CBCA0` writes the first three rows of an identity matrix (for
`003CBD60` and `0054C6B0`); `003CC480(a, b, c, out)` builds a rotation matrix from three angles with
`sinf` and `cosf`; `003CC270(from, to, heading, distance)` returns the distance in the x–z plane and
the heading `atan2(dx, dz)`, for the shot builders `00255E80` and `00256CA0`; and
`003CC3C0(origin, heading, distance, out)` places a point at that distance along the heading
(`003CC480` with only the heading), for `00257D10` and `00257F60`.

### The Screen Shake option

Besides the scripted shakes, `0037D4C0` adds an accumulator row `02EBF380 + draw × 0x20` while
`02EBF3C0` is set. `deny_camerashake_without_event(n)` (`0x04B6`, `003560D0`) stores `n == 0` in
`02EBF3C0`; the area unload `002628B0` and the manager bind `0026CE60` also write it.

`0037D970`
computes the row's values from the camera's eye and target (`003D83A0`) every time, and writes the
row only when the pointer `02089350` is set or both `02EBF3C4` and `02EBF3C0` are set.
`02EBF3C4` is the Screen Shake option, stored by `0037DDC0`
([config screen](../Menus-And-HUD/config-screen.md)). With the option off the row is not refreshed and
keeps its last values; the scripted shakes are not gated.

### Handing the camera to the renderer

After the build the camera update calls `00182640` with the camera matrix `02AEDEB0`, the aspect, the
field of view `+0x08`, the frame-mode zoom (`00229D60`), the camera's `+0x00` and `+0x04` (the near and
far distances `003CBB30` uses) and a flag that is set while the bound map `[0209A670]` has a non-zero
`+0x120`. `00182640` runs `001897C0` on the render manager (`00189120`).

`001897C0` stores the near and far distances, the field of view, the aspect and the zoom at manager
`+0xCBC`, `+0xCC0`, `+0xCC4`, `+0xCC8` and `+0xCCC`; with the flag set and `+0xCD0` greater than the
near distance, the far distance becomes `+0xCD0`. It then fills the two camera objects of the copy
chosen by the manager's byte `+0x1C` (`0x338` bytes apart):

- the scene camera at `+0x20`, with the matrix at `+0xF8` converted from `02AEDEB0` with its x and y
  terms negated, or a fixed default when any row of the source is all zero;
- a second camera at `+0x1B0`, matrix `+0x288`, the same rotation without the translation and with the
  far distance raised to at least 1000.

Each value it sets on a camera (aspect `+0xC8`, field of view `+0xD0`, zoom `+0xD4`, near `+0xC0`,
far `+0xC4`) is followed by the camera's slot `+0x08`, and `0018A120` rebuilds the camera last.

`0018A680(holder, camera)` copies a camera object into the holder's camera at `+0xE0` the same way: the
first eight words of the matrix `[camera + 0xB8]` into `+0x1B8` (with its word 11 at `+0x1E4`), the aspect,
field of view, zoom and near distance, and the far distance raised to at least 1000, each followed by slot
`+0x08`, then `0018A120(+0xE8)`. `00186670`, `00187950` and `00189570` call it.

## Layouts

Camera record [8] at `02097300`, stride `0x110`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | eye | source eye for the rebuild |
| `+0x10` | `f32[4]` | target | source target for the rebuild |
| `+0x20` | `u8[208] view` | the camera below |  |
| `+0xF0` | `u32` | mode | 1, 2, 3 or other (`00259820`) |
| `+0xF4` | `u32` | param | for mode 1 |

Camera (`0xD0`), as the update reads it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | value0 | 0.1 after a rebuild (`003CBBE0`); replaced by the copies `0025A2C0` / `0025A3D0` |
| `+0x04` | `f32` | value1 | 1000.0 after a rebuild; replaced by the same copies |
| `+0x08` | `f32` | fov | radians |
| `+0x0C` | `f32` | fovCopy | the second copy's field of view |
| `+0x10` | `f32` | projScale | 1 / tan(fov / 2) |
| `+0x20` | `f32[16]` | view | copied to `02AEDE70` |
| `+0x60` | `f32[16]` | world | camera matrix; +`0x90` is its fourth row, the eye |
| `+0xA0` | `f32[4]` | target |  |
| `+0xC4` | `f32` | roll |  |

Submission slot [8] at `02AED630`, stride `0xE0`:

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

The shake census by verb, channel and id is `scripted-camera-camerashake-census.tsv` beside this
page.

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
  oscillators behind `00382B70`.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the shot and shake channels.
- [Frame update order](../Engine-Core/frame-update-order.md): where `00314370`,
  `00259970` and the camera update run.
- [Screen mode and aspect](screen-mode-and-aspect.md): the aspect the projection uses.
- [Config screen](../Menus-And-HUD/config-screen.md): the Screen Shake row.
