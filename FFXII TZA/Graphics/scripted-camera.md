---
title: "Scripted camera: the shot channels, the camera record stack, and how a camera reaches the renderer"
kind: "system"
category: "Graphics"
summary: "The camera a script or cutscene drives, from the shot channels to the matrices the renderer reads: the per-frame channel tick, how a playing shot is published into camera record 5, the eight camera records and the active mask whose highest bit wins, the eased return to the behind camera, the eight one-frame submissions and the priority arbitration in the camera update, where the shake offsets land, the matrices it builds, and the Screen Shake option's gate."
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

### Publishing a shot

`002555D0` runs once per frame over the 20 players (5 managers × 4 channels), manager 4 first and
manager 0 last, so the lowest manager wins a conflict. For each player with a frame it calls
`0025A3B0(frame, 5, view)`:

- frame 0 copies the player's 0xD0-byte view (`+0x210`) into camera record 5 (`0025A2C0`) and
  sets its mode to 3 (`0025A500`);
- frame 1 copies it into the sub view `02097B80` (`0025A3D0`).

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

### Returning to the behind camera

`resumebehindcamera(frames, a, b)` (`0x01E4`, `003442D0`) and its four-argument form (`0x0289`,
`00343DB0`, with a pose index last) clear the current manager's shot channels and frame owners and
call `00257830`, which arms a blend:

- duration `frames × 01DFE0B8`, the counter at 0;
- the start pose, entry `index` of the poses at `02096370` (0x40 apart) that the shot player
  writes, turned into polar form about its target (`003CC130`);
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

## Layouts

Camera record [8] at `02097300`, stride `0x110`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `f32[4]` | eye | source eye for the rebuild |
| `10` | `f32[4]` | target | source target for the rebuild |
| `20` | `u8[208] view` | the camera below |  |
| `F0` | `u32` | mode | 1, 2, 3 or other (`00259820`) |
| `F4` | `u32` | param | for mode 1 |

Camera (`0xD0`), as the update reads it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08` | `f32` | fov | radians |
| `0C` | `f32` | fovCopy | the second copy's field of view |
| `10` | `f32` | projScale | 1 / tan(fov / 2) |
| `20` | `f32[16]` | view | copied to `02AEDE70` |
| `60` | `f32[16]` | world | camera matrix; +`0x90` is its fourth row, the eye |
| `A0` | `f32[4]` | target |  |
| `C4` | `f32` | roll |  |

Submission slot [8] at `02AED630`, stride `0xE0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[208]` | camera |  |
| `D0` | `u32` | submitted | 1 until the next update |
| `D4` | `i32` | priority |  |

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
