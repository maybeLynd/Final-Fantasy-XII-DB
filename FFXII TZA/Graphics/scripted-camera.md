[Home](../../README.md) / [Graphics](README.md) / Scripted camera

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Scripted camera: the shot channels, the camera record stack, and how a camera reaches the renderer | system | Graphics | Cameras | The camera a script or cutscene drives, from the shot channels to the matrices the renderer reads: the per-frame channel tick, how a playing shot is published into camera record 5, the eight camera records and the active mask whose highest bit wins, the eased return to the behind camera, the eight one-frame submissions and the priority arbitration in the camera update, where the shake offsets land, the matrices it builds, and the Screen Shake option's gate. | 0x003DA050, 0x002555D0, 0x0025A3B0, 0x0025A2C0, 0x0025A500, 0x0025A520, 0x02097300, 0x02098DEC, 0x00259820, 0x00257830, 0x00257520, 0x00256650, 0x003829D0, 0x02AED630, 0x003820C0, 0x02AED560, 0x00382B70, 0x0037D4C0, 0x0037D970, 0x02AEDEF0 |

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

| Step | What happens | Where in the code |
|---|---|---|
| 1 | For frames 0 (main) and 1 (sub), when the channel named in `+0x18[frame]` is not idle, it tells that channel's player its frame (`0x002563C0`, player `+0x184`). |   |
| 2 | For each non-idle channel that has not finished, the step is `0x02B4E4B0 × rate × 0x01DFE0BC`; the clock grows by it once the channel's run byte is set, and the first positive step sets that byte. |   |
| 3 | It evaluates the shot at the clock (`0x002555A0` → `0x00258350`), or, when the manager's skip byte `+0x201` is set, runs it to its end. | `0x00267300`<br>`0x00257A00` |
| 4 | A player at its end marker (`0x002567B0` returns 2) marks the channel finished, state 2. |   |

A finished channel skips only step 2: steps 3 and 4 still run for it every frame, at a clock that no
longer grows¹. Step 3 passes the manager's dword `+0x28`, the
channel's dword `+0x110 + 0x18 × channel` and the channel number².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DA0E9`-`0x003DA0ED`, `0x003DA11E` |
| ² | `0x003DA11E`-`0x003DA13A` |

</details>

`0x01DFE0BC` is 1.0 at 30 fps and 0.5 at 60 fps
([game settings](../Saving-Loading-And-Settings/game-settings.md)), so a shot plays at the same speed at
either frame rate.

The shake tick `0x003DCFB0(slot)` keeps one shake table per manager, `0x3D0` bytes from `0x02ADDA78` for the manager
`+0x28`, with a `0xF0`-byte row per channel:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | For each of the two frames whose channel `+0x1C[frame]` is set and running, it stores `0x003DA190` of the channel's `+0x174` word through `0x0037DB40(manager, channel, value)`, the dword at `0x02ADDA7C + manager × 0x3D0 + channel × 0xF0`. | `0x003DD026` |
| 2 | For each of the four running channels, it reads the dword at `0x02ADDA78 + manager × 0x3D0 + channel × 0xF0` through `0x0037DCC0(manager, channel)`; a value of 2 marks the channel finished. | `0x003DD075` |

### Publishing a shot

`0x002555D0` runs once per frame over the 20 players (5 managers × 4 channels), manager 4 first and
manager 0 last, so the lowest manager wins a conflict. For each player with a frame (its frame
`+0x184` is not −1, `0x0025561A`) it calls `0x0025A3B0(frame, 5, view)`:

- frame 0 copies the player's 0xD0-byte view (`+0x210`) into camera record 5¹;
- frame 1, or any other non-zero frame, copies it into the sub view `0x02097B80`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025A2C0` |
| ² | `0x0025A3D0`, `0x0025A3B4` |

</details>

After either copy `0x002555D0` itself sets record 5's mode to 3¹ and notes that it
wrote², so a player on frame 1 alone also gives record 5 mode 3 and, below, bit `0x20`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025A500`, `0x00255638` |
| ² | `0x0025563D` |

</details>

Once the field is loaded (`[0x02ADD0D8]` through `0x00377DB0`), both copies then replace the view's floats `+0x00`
and `+0x04`: with `0x02098DE0` / `0x02098DE4` while byte `0x02098DE8` is set, else with `0x0209A6EC` / `0x0209A6F0`,
dwords 2 and 3 of the map pack's section 11 (`0x0025A359`-`0x0025A3A0`, `0x0025A45F`-`0x0025A47A`;
[MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

Then the two transition cameras: when `0x00257520` is blending it writes record 5 from `0x02096410`
with mode 3, and when `0x00255850` is moving it writes record 5 from `0x02096290`, also with mode 3¹. Last,
`0x0025A520(5, any)` sets bit `0x20` of the active mask `0x02098DEC` when any of these wrote, and clears it
otherwise.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002556AC`, `0x002556B9` |

</details>

### The camera records and the active view

Eight camera records of 0x110 bytes sit at `0x02097300`. `0x00259820` takes the highest set bit of
`0x02098DEC` (bit `0x80` down to 0) and its record:

| Record mode `+0xF0` | View published |
|---|---|
| 1 | built by `0x00259990` from the record's `+0xF4` |
| 2 | the previous frame's view, unchanged |
| 3 | the record's view `+0x20` as written |
| other | rebuilt by `0x003CC000` from the eye `+0x00` and target `+0x10`, up `(0, 1, 0)` |

It keeps the result at `0x020972F0` and submits it at priority `0x14` (below). With no bit set it
submits nothing. So record 5 outranks records 0-4 and yields to 6 and 7.

`0x00259820` first stores the record's view address, record `+0x20`, at `0x020972F0`¹, which is
`0x20` when no bit is set. On every call it also asks `0x001825C0(0, −1.0, 0)`², the
depth-of-field request of [field camera](field-camera.md), with mode 0, distance −1.0 and a null point.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00259893` |
| ² | `0x0025989C` |

</details>

Mode 1 passes `0x00259820`'s own argument first, `0x00259990(arg, +0xF4, view)`¹. The
rebuild of the other modes ends in `0x00259A90`², which, once the field is loaded, replaces the
view's `+0x00` and `+0x04` as the copies into record 5 do³. After the submission
`0x020972F0` is copied to `0x020972F8`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00259916`-`0x00259921` |
| ² | `0x002598F6` |
| ³ | `0x00259A99`-`0x00259ADE` |
| ⁴ | `0x0025993E` |

</details>

### Resetting the records

`0x00259E90`, from the boot `0x00266D10`, runs the follow-camera set-up `0x00259B30`, clears the active
mask `0x02098DEC`, the bytes `0x02098DE9` to `0x02098DEB` and the words `0x02098DE0`, `0x02098DE4`, `0x02098DE8`
and `0x020972F0`, and resets every record: eye `(−3, 4, −8, 1)`, target `(0, 0, 0, 1)`, the view
zeroed and rebuilt¹, mode and parameter 0. It zeroes and rebuilds the sub view `0x02097B80`
and the behind camera's view `0x02097C50` the same way.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CBFF0` |

</details>

`0x0025A890`, from the render manager's target rebuild `0x00188B10`, sets the field of view of the eight
record views, `0x02097B80` and `0x02097C50` back to π/4 at `+0x08` and `+0x0C`, with `+0x10` =
`1 / tan(π/8)`¹. `0x00258130`, from the same rebuild², runs `0x003CBAD0` on twenty more
views from `0x02092A40`: five groups `0xBB0` apart, four views `0x2E0` apart in each.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CBAD0` |
| ² | `0x00188B27` |

</details>

The debug verbs `debug_camerasrc` (`0x2013`, `0x0050E5B0`) and `debug_cameradst` (`0x2012`, `0x0050E530`)
pop three floats each and write them, with w 1.0, as record 1's eye¹ or target²; the third float popped is x. `debug_cameraescape` (`0x2077`, `0x0050CD30`) pops three ints
and stores the first popped as a byte at `+0x188` of the shot player chosen by the third (manager) and
the second (channel) (`0x00257AA0`; players at `0x02092830 + manager × 0xBB0 + channel × 0x2E0`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025A4A0` |
| ² | `0x0025A4D0` |

</details>

### Returning to the behind camera

`resumebehindcamera(frames, a, b)` (`0x01E4`, `0x003442D0`) and its four-argument form (`0x0289`,
`0x00343DB0`, with a pose index last) clear the current manager's shot channels and frame owners and
call `0x00257830`, which arms a blend:

- duration `frames × 0x01DFE0B8`, the counter at 0;
- the start pose, entry `index` of the poses at `0x02096370` (0x40 apart) that the shot player
  writes, turned into polar form about its target¹ and stored back into the entry: the
  yaw at `+0x28`, the pitch at `+0x2C` and the distance at `+0x30`²;

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC130` |
| ² | `0x00257881`-`0x0025789D`, `0x003CC1C4`-`0x003CC23A` |

</details>

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
is 0 or the counter has reached it¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00255C20`, `0x00257800` |

</details>

- `behindtoeventcamerasync` (`0x0350`, `0x0034A530`) and `resumebehindcamerasync` (`0x01E5`,
  `0x003445E0`) hold the script until their transition is done.
- When the manager is skipping¹, they instead set the counter to the duration less one
  and run the step once (`0x00255CB0` with `0x00255850`, `0x002578B0` with `0x00257520`), so the camera lands on
  its final pose, and release the script.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00267310` |

</details>

### The behind camera's field of view and roll

`behindcamerafovyroll` (`0x023A`, `0x00349D00`) pops a float, a float, an int and a float. `0x002564D0`
keeps them as the roll target `0x020964F4`, the field-of-view target `0x020964F0`, the ease `0x02096500` and
the duration, the last value times `0x01DFE0B8`, at `0x020964F8`, and zeroes the counter `0x020964FC`.

Each frame the shake gather `0x0037D4C0` asks `0x002563F0` for the two offsets. With a duration of 0 they are
the targets; otherwise each target is multiplied by `0x00256650(ease, counter / duration)`. The counter
then grows by 1 until it passes the duration. The gather adds the offsets to the shake's roll and
field-of-view scalars, which reach `0x02AEDF98` and `0x02AEDF9C` through `0x00382B70`.

`behindcamerafovyrollsync` (`0x023B`, `0x0034A600`) holds the script while the counter has not passed
the duration¹; a skip sets the counter one past it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002564B0` |
| ² | `0x00256500` |

</details>

At each field start `0x00259B30` clears the ramp through `0x003DA2C0`, which calls `0x002564D0(0, 0, 0, 0)`:
both targets, the ease, the duration and the counter become 0, so the offsets are 0 until a script
sets them again.

`getbehindcameradir` (`0x0343`, `0x00347070`) returns the behind camera's direction in eighths¹: from the view `0x002593A0` returns it takes `atan2` of the eye minus the target in x and z
(`+0x90`, `+0x98` minus `+0xA0`, `+0xA8`), adds π/8, wraps it into 0 to 2π and divides by π/4, giving
0 to 7. When the eye and the target share x and z it returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002565C0` |

</details>

### The summon camera's subject

`setsummoncameratarget(id, on)` (`0x0271`, `0x00341410`) makes the actor `id` names (`0x00264010`, the
party focus for a negative id) the subject `0x02096508` through `0x002578F0`, or clears the subject when
`on` is 0. Clearing it also keeps only the low byte, the fade level, of every other live actor's fade word
(`and` with `0xFF`, `0x00257987`), which drops the mark bit `0x8000`, and keeps the fade running
while any actor was marked.

The fade word is a `u16` of the actor's `+0xC0` context: `0x00263EB0(actor, i)` and
`0x0026A3B0(actor, i, v)` read and write `+0x20 + 2i`, `i` clamped to 1 and taken as 0 when negative,
and `0x00263E80` reads `+0x20`. Bit `0x8000` marks the actor; the low byte is its fade level.

Each field frame `0x00256F60` (from `0x0022A770`) boxes the subject and every other live actor of the
five managers on screen with `0x00255CF0`. That function places the points `(−r, 0, 0)` and `(r, h, 0)`
in the camera's orientation at the actor's position, `r` and `h` from `0x00265090` and `0x00263940`,
projects both through `0x02AEDDB0`, divides x and y by the fourth value of each projected point, the float at
`+0x0C`¹, and subtracts 1792 and 1824,
giving the corners of a 512 × 448 frame. Then for each other actor:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00255E17` |

</details>

- the mark is cleared when the actor's depth value `+0x08` is not above the subject's or the two boxes
  do not overlap;
- the mark is set when the actor's box reaches more than 16 into the subject's box on all four sides;
- otherwise the word stays as it was.

While a mark changed or a fade runs¹, `0x00255FF0(step)` moves every other live actor's
level by the step `0x02096514` (`0x20`, set by `0x002556F0`): up toward 255 when marked, down toward 0
when not. It writes the word back, sets the actor's render record colour `+0x220` to `+0x228` to
1.0 and its alpha `+0x22C` to `(255 − level) / 255`, and returns 1 once every level has arrived,
which ends the fade. So the marked actors, those that cover the subject, fade out over eight frames.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02096510` |

</details>

### Running a shot to its end

The skip path `0x00257A00` reads two things from a shot player through small getters: `0x00258AF0(manager,
channel)` returns from the current row's first byte (player `+0x178`): 1 for kind 1, the word `+0x22`
for kind 2, 0 for kind −1 and 1 for any other kind; `0x00258B50` returns the player's `+0x0C`. A negative
channel selects the transition player at `0x02096520` instead.

The transition player is a `0x2E0`-byte shot player like the twenty in the groups. The actor-system reset
`0x002556F0` clears it (`0x00861EC0` at `0x002557C9`), stores −1 in its frame `+0x184`¹, resets
its view `+0x210` through `0x003CBFF0`² and then stores 0 in the frame³, so it starts on frame
0, the main view.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x020966A4`, `0x002557D5` |
| ² | `0x002557DF` |
| ³ | `0x002557F3` |

</details>

The shot evaluation `0x00258350` reads that frame when it is given a negative channel¹ and writes the evaluated pose into entry `frame` of the poses at `0x02096370`, `0x40` apart².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002583CB`, `0x002583D2` |
| ² | `0x00258687`-`0x002586D2` |

</details>

The clear of the frames, `0x00255810` (from the tick `0x00314020` at `0x003140F0` and from `0x003143D0` at `0x003143EB`), walks the twenty group players
(`0x00255820`-`0x0025584D`, from `0x020929B4` in steps of `0xBB0`).

### Submissions

`0x003829D0(camera, priority)` files a 0xD0-byte camera into the first free of eight 0xE0-byte
slots at `0x02AED630`, with the priority at `+0xD4` and the submitted flag at `+0xD0`; with all
eight taken it drops the camera. When `0x00181DD0` reports an override it first applies three vectors
from `0x00181CD0`, `0x00181C50` and `0x00181CB0` to the camera¹. It rebuilds the caller's camera
in place from the eye `0x00181C50()` with x and y negated, the target `0x00181CB0()` and the up vector
`0x00181CD0()` with y negated².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC000` |
| ² | `0x003829F7`-`0x00382A57` |

</details>

Last, filed or dropped, it tells the render manager which view the camera is: `0x001821F0` when the
camera is the sub view `0x02097B80`¹, else `0x00182340`²; they reach
`0x00185A10` and `0x001860E0`, which set the manager's view byte `+0x1C` to 1 and to 0 (`0x00185A1D`,
`0x001860E6`; [map art](../World-Areas-And-Travel/map-art.md)). There are three submitters:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00259FA0` |
| ² | `0x00382B15`-`0x00382B28` |

</details>

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
submission wins a tie, and every submission lasts one frame. With no submission, the update returns and
the previous frame's matrices stand. The winner is copied into the working camera at `0x02AED560`.

### Shake and the build

The shake gather `0x0037D4C0` hands two offset vectors and two scalars to `0x00382B70`, which stores
them at `0x02AEDF70` (eye), `0x02AEDF80` (target), `0x02AEDF98` (roll) and `0x02AEDF9C` (field of view).
The update then:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | adds `0x02AEDF9C` to the field of view `+0x08` and recomputes `+0x10 = 1 / tan(fov / 2)`; |   |
| 2 | adds `0x02AEDF98` to the roll `+0xC4`; |   |
| 3 | turns both offsets by the camera's matrix `+0x60` and adds them to the eye `+0x90` and the target `+0xA0`, so a shake moves in the camera's own frame; | `0x02AED5C0` |
| 4 | rebuilds the matrices from eye, target and roll; | `0x003CBD60` |
| 5 | does the same to a stack copy whose field of view is `+0x0C`, replaced by π/4 when above 1.0, plus the shake. |   |

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
| `0x02B40470` | `0x02AED500` × the working camera's projection (`0x003CBB30`), copied there by `0x003B4150`; the update `0x003820C0` does it on one of its paths, and only while `0x00182570` returns 0; `0x00474710` stores `0x02AED4A0` × the working camera's projection there instead (`0x003CBB30` with the aspect `0x02AED4E0`, `0x004748A1`-`0x004748D1`); `0x002F5550` also calls `0x003B4150` |

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
computes the row's values from the camera's eye and target¹ every time, and writes the
row only when the pointer `0x02089350` is set or both `0x02EBF3C4` and `0x02EBF3C0` are set.
`0x02EBF3C4` is the Screen Shake option, stored by `0x0037DDC0`
([config screen](../Menus-And-HUD/config-screen.md)). With the option off the row is not refreshed and
keeps its last values; the scripted shakes are not gated.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003D83A0` |

</details>

### Handing the camera to the renderer

After the build the camera update calls `0x00182640` with the camera matrix `0x02AEDEB0`, the aspect, the
field of view `+0x08`, the frame-mode zoom¹, the camera's `+0x00` and `+0x04` (the near and
far distances `0x003CBB30` uses) and a flag that is set while the bound map `[0x0209A670]` has a non-zero
`+0x120`. `0x00182640` runs `0x001897C0` on the render manager².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00229D60` |
| ² | `0x00189120` |

</details>

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

<details>
<summary>Show the memory layouts</summary>

Camera record [8] at `0x02097300`, stride `0x110`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | eye | source eye for the rebuild |
| `+0x10` | `f32[4]` | target | source target for the rebuild |
| `+0x20` | `u8[208]` | view | the camera below |
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
| `+0x60` | `f32[16]` | world | camera matrix; `+0x90` is its fourth row, the eye |
| `+0xA0` | `f32[4]` | target |  |
| `+0xC4` | `f32` | roll |  |

Submission slot [8] at `0x02AED630`, stride `0xE0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[208]` | camera |  |
| `+0xD0` | `u32` | submitted | 1 until the next update |
| `+0xD4` | `i32` | priority |  |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

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

</details>

## State

<details>
<summary>Show the state it keeps</summary>

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

`0x003CBD60` runs on the camera from `0x00382486`¹, and `0x003CBFA0`, the vector from the eye to the target,
runs on it from `0x0029BC80`, `0x002DF2C0`, `0x002DF560` and `0x003F1A60`. The 16-byte copy `0x00202C90` takes the eye
`0x02AED5F0` from `0x002C7660`, `0x002C7B10`, `0x003F2CF0`, `0x003F3010`, `0x003F5100`, `0x003F5260`, `0x003F5430` and `0x003FB3E0`; the
vector difference `0x00203080` takes it from `0x0028A090`, `0x003F1A60`, `0x003F35C0`, `0x003F7200`, `0x00505570` and `0x00505E00`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00382406` |

</details>

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
priority `+0xD4`¹ before the flag. A slot wins with a signed compare of its priority against the best
so far (`0x0038212B`, `0x0038214D` and on).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00382B01` |

</details>

### The view's override elements

`0x003820C0` copies the working camera's view `+0x20`¹ to `0x02AEDE70` with `0x00202C70`². When
`0x00181DD0` reports an override it then replaces eight elements from the matrix `m` that `0x00181CF0` returns³; the element `+0x00`, `0x02AEDE70`, takes `-m[+0x0C]`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02AED580` |
| ² | `0x0038267A` |
| ³ | `0x00382694`-`0x00382712` |

</details>

| Global | Element | Type | Start | Override value |
|---|---|---|---|---|
| `0x02AEDE74` | `+0x04` | `f32` | 0 | `-m[+0x1C]` (`0x003826B9`) |
| `0x02AEDE78` | `+0x08` | `f32` | 0 | `-m[+0x2C]` (`0x003826C9`) |
| `0x02AEDE80` | `+0x10` | `f32` | 0 | `-m[+0x00]` (`0x003826D8`) |
| `0x02AEDE84` | `+0x14` | `f32` | 0 | `-m[+0x04]` (`0x003826E8`) |
| `0x02AEDE88` | `+0x18` | `f32` | 0 | `-m[+0x08]` (`0x003826F8`) |
| `0x02AEDEA0` | `+0x30` | `f32` | 0 | `m[+0x20]` (`0x00382705`) |
| `0x02AEDEA4` | `+0x34` | `f32` | 0 | `m[+0x24]` (`0x00382712`) |

The view is read as whole 16-byte rows by `0x0024C060`¹, `0x004FDDA0`² and
`0x0051CDE0`³, and as a matrix through `0x00202C70`, `0x00202D70` and `0x00202D50` by `0x0028DC00`,
`0x002F4520`, `0x002F5550`, `0x003820C0`⁴, `0x003F0170`, `0x003F0610`, `0x003F3710`,
`0x003F5430` and `0x003F7930`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024C10D`-`0x0024C130` |
| ² | `0x004FDDB2`-`0x004FDDEE` |
| ³ | `0x0051CF17`-`0x0051CF8E` |
| ⁴ | `0x00382752`, `0x0038276C`, `0x003827D5` |

</details>

### The Screen Shake rows

The accumulator `0x02EBF380 + draw × 0x20` of the Screen Shake option holds two rows of `0x20` bytes,
`0x02EBF380`-`0x02EBF3BF`, indexed by the same draw number in both functions. `0x0037D970` writes a row's `+0x00`-`+0x08`
and, with one 16-byte store, `+0x0C`-`+0x1B`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037DA23`-`0x0037DA45` |

</details>

The gather `0x0037D4C0` adds `+0x00`-`+0x08` to
the eye offset, `+0x0C`-`+0x14` to the target offset and `+0x18` to the roll it hands to `0x00382B70`¹; it does not read `+0x1C`. `0x0037D890`, which `0x00314020`² and `0x003143D0`³ run, zeroes both rows with eight 8-byte stores⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037D769`-`0x0037D7C4` |
| ² | `0x003140F5` |
| ³ | `0x003143F0` |
| ⁴ | `0x0037D917`-`0x0037D948` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBF388` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 0 `+0x08` (the eye offset's z) and `+0x0C` (the target offset's x) | `0x0037D970` (`0x0037DA3A`; `0x0037DA45`, 16 bytes); `0x0037D890`, 0 (`0x0037D91E`) | `0x0037D4C0` (`0x0037D77B`, `0x0037D781`) |
| `0x02EBF390` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 0 `+0x10` and `+0x14`, the target offset's y and z | `0x0037D970` (`0x0037DA45`); `0x0037D890`, 0 (`0x0037D925`) | `0x0037D4C0` (`0x0037D787`, `0x0037D78D`) |
| `0x02EBF398` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 0 `+0x18`, the roll offset, and `+0x1C`, which only `0x0037D890` writes and no instruction reads | `0x0037D970` (`0x0037DA45`, `+0x18` only: its 16-byte store covers `+0x0C`-`+0x1B`); `0x0037D890`, 0 (`0x0037D92C`, both) | `0x0037D4C0` (`0x0037D793`, `+0x18` only) |
| `0x02EBF3A0` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 1 `+0x00` and `+0x04`, the eye offset's x and y | `0x0037D970` (`0x0037DA23`, `0x0037DA2E`); `0x0037D890`, 0 (`0x0037D933`) | `0x0037D4C0` (`0x0037D770`, `0x0037D775`) |
| `0x02EBF3A8` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 1 `+0x08` and `+0x0C` | `0x0037D970` (`0x0037DA3A`; `0x0037DA45`); `0x0037D890`, 0 (`0x0037D93A`) | `0x0037D4C0` (`0x0037D77B`, `0x0037D781`) |
| `0x02EBF3B0` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 1 `+0x10` and `+0x14` | `0x0037D970` (`0x0037DA45`); `0x0037D890`, 0 (`0x0037D941`) | `0x0037D4C0` (`0x0037D787`, `0x0037D78D`) |
| `0x02EBF3B8` | `f32[2]` | 0 (zero-filled tail of `.data`) | row 1 `+0x18` and `+0x1C`; only `0x0037D890` writes `+0x1C` | `0x0037D970` (`0x0037DA45`, `+0x18` only: its 16-byte store covers `+0x0C`-`+0x1B`); `0x0037D890`, 0 (`0x0037D948`, both) | `0x0037D4C0` (`0x0037D793`, `+0x18` only) |

### The two transitions' state

The move to the event camera is armed by `0x00255C50` and stepped by `0x00255850`; the swing back is armed by `0x00257830`
and stepped by `0x00257520`. Besides their durations and counters they keep the values below. `behindtoeventcamera`¹ pops four values: the ease kind², a
second integer³, the frame count⁴ and the shot row⁵; `0x003DA300` turns the row into
the CML1 row's word `+0x14`⁶ and passes the manager's dword `+0x28`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00349FA0` |
| ² | `0x00349FC7` |
| ³ | `0x00349FD1` |
| ⁴ | `0x00349FDB` |
| ⁵ | `0x00349FEE` |
| ⁶ | `0x003DA31F` |
| ⁷ | `0x003DA316` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02096278` | `i32` | 0 | the second integer `behindtoeventcamera` pops | `0x00255C50` (`0x00255C87`) | no instruction names it apart from that store |
| `0x0209627C` | `i32` | 0 | the move's ease kind, passed to `0x00256650(kind, t)` | `0x00255C50` (`0x00255C5B`) | `0x00255850` (`0x002558E2`) |
| `0x02096280` | `i32` | 0 | the move's shot row; when it is 0 or more (a signed test, `0x00255908`), the transition player `0x02096520` takes as its stream the qword `+0x18` of that row of the shot list of manager `0x02096284` (`0x0025590C`-`0x0025592A`), otherwise its stream is 0 (`0x00255933`) | `0x00255C50` (`0x00255C8E`) | `0x00255850` (`0x002558ED`) |
| `0x02096284` | `i32` | 0 | the move's manager: the stride `0xBB0` into the groups at `0x02092810` (`0x0025590C`) and the manager argument of the shot walk `0x00258350` (`0x0025594B`) | `0x00255C50` (`0x00255C63`) | `0x00255850` (`0x002558FB`) |
| `0x02096298` | `f32` | 0 | the move's view `0x02096290`, field of view `+0x08` in radians: the behind camera's field of view eased toward the start pose's `+0x24` (`0x00255B4F`-`0x00255B64`) | `0x003CBBE0`, π/4 (`0x003CBBF1`), through `0x003CBFF0` when `0x00255C50` arms (`0x00255C94`); `0x00255850` (`0x00255B77`) | `0x0025A2C0` (`0x0025A2C6`, a 16-byte load of `+0x00` to `+0x0F`), when `0x002555D0` copies the view into camera record 5 (`0x002556A0`) |
| `0x020962A0` | `f32` | 0 | the move's view `+0x10`, `1 / tan(fov / 2)`, or 0 when the tangent is 0 | `0x003CBBE0` (`0x003CBC1E`, `0x003CBC35`) through `0x00255C94`; `0x00255850` (`0x00255BB2`, `0x00255BCA`) | `0x0025A2C0` (`0x0025A2E8`, 16 bytes `+0x10` to `+0x1F`) from `0x002556A0` |
| `0x02096360` | `u16` | 0 | 1 once the move has fixed its turn choice | `0x00255C50`, 0 (`0x00255C70`); `0x00255850`, 1 (`0x00255A7D`, `0x00255A97`) | `0x00255850` (`0x00255A44`) |
| `0x02096362` | `u16` | 0 | the move's turn choice, fixed on its first step from the heading difference `d` (`0x00255A67`): 1 when `d` is 0 or more and above π, or below 0 and not below −π (`0x00255A6D`-`0x00255AA1`). Each step then adds −2π to the heading when the choice is 1 and `d` is 0 or more, and 2π when the choice is 0 and `d` is below 0 (`0x00255AB1`-`0x00255AD2`) | `0x00255850` (`0x00255A87`, `0x00255AA1`) | `0x00255850` (`0x00255AAA`) |
| `0x020963F0` | `void*` | 0 | the start pose: an entry of the poses at `0x02096370` | `0x00255C50`, entry 0 (`0x00255CA0`); `0x00257830`, entry `index` (`0x0025784C`-`0x00257868`) | `0x00255850` (`0x00255886`, `0x002559A4`, `0x00255B2F`); `0x00257520` (`0x002575A6`, `0x00257644`, `0x00257715`); `0x00257830` (`0x00257881`) |
| `0x02096418` | `f32` | 0 | the swing-back view `0x02096410`, field of view `+0x08` in radians: interpolated from the start pose's `+0x24` toward the behind camera's (`0x00257742`-`0x00257756`) | `0x003CBBE0`, π/4 (`0x003CBBF1`), through `0x003CBFF0` when `0x00257830` arms (`0x0025787C`); `0x00257520` (`0x00257760`) | `0x0025A2C0` (`0x0025A2C6`), when `0x002555D0` copies the view into camera record 5 (`0x00255673`) |
| `0x02096420` | `f32` | 0 | the swing-back view `+0x10`, `1 / tan(fov / 2)`, or 0 when the tangent is 0 | `0x003CBBE0` (`0x003CBC1E`, `0x003CBC35`) through `0x0025787C`; `0x00257520` (`0x00257798`, `0x002577B0`) | `0x0025A2C0` (`0x0025A2E8`) from `0x00255673` |
| `0x020964E0` | `u16` | 0 | 1 once the swing back has fixed its turn choice | `0x00257830`, 0 (`0x0025783E`); `0x00257520`, 1 (`0x0025766D`, `0x00257687`) | `0x00257520` (`0x00257637`) |
| `0x020964E2` | `u16` | 0 | the swing back's turn choice, set as `0x02096362` from the difference of the heading and the start pose's `+0x28` (`0x00257654`-`0x00257691`); the heading gets −2π or 2π under the same rule (`0x002576A1`-`0x002576BA`) | `0x00257520` (`0x00257677`, `0x00257691`) | `0x00257520` (`0x0025769A`) |

### The transition player

The transition player at `0x02096520` is a `0x2E0`-byte shot player. `0x002556F0` clears all of it¹. It is
set up by the move's first step², by `camerahitcheck`'s run `0x002567E0`, which uses it as its scratch
player, and by the shot start `0x00257230` for a negative channel³. The shot walk `0x00258350` uses it when
it is given a negative channel⁴, and through it the path offsets `0x002554E0`, `0x00256960` and `0x00256CA0`
write its two offset vectors (`+0xF0` eye, `+0x100` target), the evaluator `0x003CC740` storing x, y and z.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002557C9` |
| ² | `0x00255850` |
| ³ | `0x00257258` |
| ⁴ | `0x002583CB` |

</details>

| Global | Field | Type | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02096528` | `+0x08` | `f32` | the segment clock: grows by `+0x10` each step (`0x00258711`-`0x0025871C`) and loses the segment length, the row's `u16` `+0x22`, when it passes it (`0x00258901`-`0x0025891E`) | `0x00255850`, 0 (`0x00255956`, 8 bytes over `+0x08` to `+0x0F`); `0x002567E0` (`0x00256893`, 8 bytes); `0x00257230` (`0x0025728D`, 8 bytes); `0x00258350` (`0x0025871C`, `0x0025891E`) | `0x00258350` (`0x00258711`, `0x00258901`) |
| `0x02096530` | `+0x10` | `f32` | the step: the channel time less the time at `+0x0C` (`0x00258403`-`0x00258439`) | `0x00255850` (`0x0025595D`); `0x002567E0` (`0x0025689A`); `0x00257230` (`0x00257291`); `0x00258350` (`0x00258439`) | `0x00258350` (`0x00258705`) |
| `0x02096610` | `+0xF0` | `f32` | the eye offset's x | `0x00255850` (`0x0025597D`); `0x002567E0` (`0x002568BE`); `0x00257230` (`0x002572B2`); `0x002554E0` (`0x00255532`, and through `0x003CC740`); `0x00256960` (`0x00256A55`, `0x00256AA6`); `0x00256CA0` (`0x00256D90`, `0x00256DE1`) | `0x00258350` (`0x00258592`); `0x00256960` (`0x00256C07`); `0x00256CA0` (`0x00256EDB`) |
| `0x02096614` | `+0xF4` | `f32` | the eye offset's y | `0x00255850` (`0x00255976`, 8 bytes over `+0xF4` and `+0xF8`); `0x002567E0` (`0x002568B7`, 8 bytes); `0x00257230` (`0x002572AB`, 8 bytes); `0x002554E0` (`0x0025552F`, 8 bytes, and through `0x003CC740`); `0x00256960` (`0x00256A4E`, 8 bytes; `0x00256AAE`); `0x00256CA0` (`0x00256D89`, 8 bytes; `0x00256DE9`) | `0x00258350` (`0x0025859A`); `0x00256960` (`0x00256C24`); `0x00256CA0` (`0x00256EF8`) |
| `0x0209661C` | `+0xFC` | `f32` | the eye offset's w, 1.0 | `0x00255850` (`0x00255983`, 8 bytes: 1.0 and `+0x100` = 0); `0x002567E0` (`0x002568C5`, the same); `0x00257230` (`0x002572B9`, the same); `0x002554E0` (`0x00255565`); `0x00256960` (`0x00256A58`); `0x00256CA0` (`0x00256D93`) | no instruction names it apart from these stores |
| `0x02096624` | `+0x104` | `f32` | the target offset's y | `0x00255850` (`0x0025598E`, 8 bytes over `+0x104` and `+0x108`); `0x002567E0` (`0x002568D0`, 8 bytes); `0x00257230` (`0x002572C4`, 8 bytes); `0x002554E0` (`0x0025552F` on its second vector, 8 bytes, and through `0x003CC740`); `0x00256960` (`0x00256C35`); `0x00256CA0` (`0x00256F09`) | `0x00258350` (`0x002585B2`) |
| `0x0209662C` | `+0x10C` | `f32` | the target offset's w, 1.0 | `0x00255850` (`0x00255995`); `0x002567E0` (`0x002568D7`); `0x00257230` (`0x002572CB`); `0x002554E0` (`0x00255565` on its second vector) | no instruction names it apart from these stores |
| `0x02096644` | `+0x124` | `i32` | the current row's byte `+0x25` (`0x00258721`-`0x00258725`); while it is 0 the walk adds the offsets to the pose's eye and target (`0x002585FE`-`0x0025860F`) | `0x00255850` (`0x00255969`); `0x002567E0` (`0x002568A8`); `0x00257230` (`0x0025729C`); `0x00258350` (`0x00258725`) | `0x00258350` (`0x002585FE`) |
| `0x02096698` | `+0x178` | `void*` | the stream position: advanced by `0x2C` past a segment (`0x00258912`) and `0x40` past a key (`0x002589AE`) | `0x00255850` (`0x0025592A`, or 0 at `0x00255933`); `0x002567E0` (`0x00256856`, `0x0025685F`); `0x00257230` (`0x0025727D`, `0x00257286`); `0x00258350` (`0x00258912`, `0x002589AE`) | `0x00258350` (`0x00258560`, `0x00258735`); `0x00258AF0` (`0x00258B1E`) |
| `0x020966A0` | `+0x180` | `i32` | the player state: 1 while a segment runs (`0x002589B6`), 2 at the end (`0x002583E9`, `0x00258588`) | `0x00255850` (`0x00255963`); `0x002567E0` (`0x002568A1`); `0x00257230` (`0x00257295`); `0x00258350` (`0x002583E9`, `0x00258588`, `0x002589B6`) | `0x002567B0` (`0x002567D7`); `0x00258350` (`0x00258ACF`) |
| `0x020966A9` | `+0x189` | `u8` | 1 once the eye side is attached ([EBP camera tables](../EBP-Script-Files/ebp-camera-tables.md)) | `0x00255850` (`0x0025596F`, 2 bytes over `+0x189` and `+0x18A`); `0x002567E0` (`0x002568AF`, 2 bytes); `0x00257230` (`0x002572A3`, 2 bytes); `0x00258350` (`0x002584BC`) | `0x00258350` (`0x00258491`) |

### The previous view, the sub view and the shake vectors

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x020972F8` | `void*` | 0 | the view `0x00259820` published last frame, which a record of mode 2 publishes again | `0x00259820` (`0x0025993E`, a copy of `0x020972F0` after the submission) | `0x00259820` (`0x00259906`) |
| `0x02097B84` | `f32` | 0 | the sub view `0x02097B80`'s `+0x04`: 1000.0 after a rebuild, then the second of the two words `0x0025A3D0` takes once the field is loaded (`0x0209A6F0`, or `0x02098DE4` while `0x02098DE8` is set) | `0x00259E90` (`0x00259F53`, its `0xD0`-byte clear of `0x02097B80`; `0x003CBBE0`, 1000.0, at `0x003CBC05` through `0x00259F5F`); `0x0025A3D0` (`0x0025A3DE`, the 16-byte copy over `0x02097B80`-`0x02097B8F`; `0x0025A48A`) | `0x003829D0` (`0x00382A8A`, a 16-byte load of `+0x00` to `+0x0F`), when `0x00259970` submits the sub view (`0x00259975`) |
| `0x02AEDF74` | `f32` | 0 | the eye shake offset's y | `0x00382910` (`0x0038295A`, 8 bytes over `0x02AEDF74`-`0x02AEDF7B`); `0x00382B70` (`0x00382B81`) | `0x00202B90` (`0x00202B94`), turning the vector by the camera matrix for `0x003820C0` (`0x003823B7`, `0x003824D6`) |
| `0x02AEDF78` | `f32` | 0 | the eye shake offset's z | `0x00382910` (`0x0038295A`); `0x00382B70` (`0x00382B8E`) | `0x00202B90` (`0x00202B9A`) from `0x003823B7` and `0x003824D6` |
| `0x02AEDF7C` | `f32` | 0 | the eye shake offset's w: 1.0 at boot, then the gather's fourth float | `0x00382910`, 1.0 (`0x00382980`, 8 bytes: 1.0 and `0x02AEDF80` = 0); `0x00382B70` (`0x00382B9B`) | no instruction names it apart from these stores; `0x00202B90` reads x, y and z only |
| `0x02AEDF84` | `f32` | 0 | the target shake offset's y | `0x00382910` (`0x00382967`, 8 bytes over `0x02AEDF84`-`0x02AEDF8B`); `0x00382B70` (`0x00382BB4`) | `0x00202B90` (`0x00202B94`) from `0x003823E7` and `0x003824FC` |
| `0x02AEDF88` | `f32` | 0 | the target shake offset's z | `0x00382910` (`0x00382967`); `0x00382B70` (`0x00382BC1`) | `0x00202B90` (`0x00202B9A`) from `0x003823E7` and `0x003824FC` |
| `0x02AEDF8C` | `f32` | 0 | the target shake offset's w: 1.0 at boot, then the gather's fourth float | `0x00382910`, 1.0 (`0x00382975`, 8 bytes: 1.0 and `0x02AEDF90` = 0); `0x00382B70` (`0x00382BCE`) | no instruction names it apart from these stores |

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Gameplay** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203080`](../Battle-Actions/action-range.md) (on action range) | is called by | [`0x00339630`](../Battle-Actions/action-phases.md) (on action phases) |

</details>
