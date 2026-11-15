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
Its `+0xF4` picks one of the 0x860-byte camera controllers at `0x02097D30`. `0x00259990(go, n, view)` (from `0x00259820`,
`0x00259921`) does nothing until the field is loaded (`0x00377DB0`) or while `go` is 0 (`0x002599B8`-`0x002599C3`). Otherwise
each frame it calls `0x003D9E20`, which reads the target cursor, and `0x003D9930(controller, view, controller + 0x630)`,
which runs `0x0032AEC0` on the follow camera at controller `+0x2B0` (`0x002599D3`, `0x00259A21`).

Once the field is loaded, also when `go` is 0, it then replaces the view's `+0x00` and `+0x04` with `0x02098DE0` and
`0x02098DE4` while the byte `0x02098DE8` is set, else with `0x0209A6EC` and `0x0209A6F0` (`0x00259A3B`-`0x00259A77`). Two hold
bytes decide whether `0x003D9930` runs (`0x002599D8`-`0x00259A11`):

- `0x02098DEA`: `setnoupdatebehindcamera` (`0x0236`, `0x0025A5B0`) sets it to 2 unless it is 1, and clears it with 0. At 2
  it drops to 1 and the camera runs once more; at 1 the camera does not run unless `0x02098DEB` is above 1.
- `0x02098DEB`: `0x0025A5D0` sets it to 1 and clears it, for `setnoupdatebehindcamera_system` (`0x0506`) and the time stop
  ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)). At 1 the camera does not run; above 1
  it drops by one and the camera runs.

While the byte `0x02098DE9` is set, `0x003D9950` runs instead, and `0x003D9E20` is not called (`0x002599C5`).
It publishes controller `+0x00`, the vector
`0x0025A540` stores in both controllers, as the eye (copied to `+0x90`), and the followed transform's
position at `+0x630`, raised by `+0x64`, as the look point (copied to `+0x70`), through `0x003CC080`
(`0x003D9950`-`0x003D99AA`). `0x003D99B0` sets a controller up (`0x0032B600`) and `0x003D9B80` resets it
(`0x0032B790`). `0x003D99B0` runs `0x0032B790` again after `0x0032B600` (`0x003D9AB5`).

`0x0032B600` sets the three orbit blocks `+0x00`, `+0x40` and `+0x80` to the look point (0, 0, 0, 1), heading 0 and
level 0.483 with that level's pitch and distance (`0x0032B624`-`0x0032B6C1`), runs `0x0032CE40` and `0x0032B790`, and then
zeroes the state `+0xC0` (`0x0032B6DC`-`0x0032B70D`). It stores `atan2(−0.7, 2.8)` and `atan2(7.6, 8.8)` from `0x01EED478`
at `0x022C3190` and `0x022C3194`, and 7.598 (`0x00D108E4`) and −0.7 (`0x00D108F4`) at `0x022C3184` and `0x022C3188`
(`0x0032B713`-`0x0032B776`).

`0x0032B790` sets the state, `[camera + 0xC0] = 0x20000000` (`0x0032B790`), and zeroes the two rates, the wall and
auto terms, the floor lift `[camera + 0x128] = 0`, both hold counts, `+0x364` and the travelled distance
(`0x0032B79C`-`0x0032B7AA`, `0x0032B84F`-`0x0032B861`). It sets the divisor `+0x100` and the scale `+0x120` to 1.0 and
the look height `+0x11C` to 1.3 (`0x3FA66666`; `0x0032B7B1`, `0x0032B7BB`, `0x0032B84F`).

It puts the eye and look pairs `+0x2E0` to `+0x340` and the point `+0x350` at (0, 0, 0, 1), zeroes the framing count
`+0x320` and the framed actor `+0x360`, and sets `+0x374` to 1 (`0x0032B790`-`0x0032B868`). It leaves the recentre
deflection `+0x370` as it was.

The followed transform at controller `+0x630` gives the position and the leader's facing, taken as
`atan2(+0x18, +0x10)` (`0x0032CE40`). The look point is that position raised by `+0x11C`, 1.3
(`0x0032B1C0`). When the position moves more than `0.1 × [0x01DFE0BC]` in a frame, `0x0032CE40` sets bit
`0x8000000` of the state word `+0xC0`.

`0x0032B1C0(camera, position)` is the per-frame body. It keeps only the bits under mask `0xE7FE0000` of the state
`+0xC0` (`0x0032B1CC`), places the block `+0x00` from the orbit block's look `+0xA0`, heading `+0xB0` and level
`+0xBC` (`0x0032DF40` with the camera as its output, `0x0032B1D6`-`0x0032B1FB`), copies
`+0xE0`-`+0xEC` to `+0xD0`-`+0xDC`, keeps `0x0026E500(0)` at `+0x2C8`, copies the position to `+0x60` and raises it by
`+0x11C`, and runs `0x0032CE40` and `0x0032C910` (`0x0032B1FB`-`0x0032B272`).

It then makes one or two passes (`0x0032B280`-`0x0032B302`): the pulled-in branch `0x0032B4D0` while bit `0x4000000` is set,
else the normal branch `0x0032B390`. A second pass runs only when the first changed that bit, and runs the other branch.
When the normal branch pulled the camera in and Camera Auto-Rotation is on (`0x0017E260`), the heading `+0x70` becomes
the heading from the look point to the pulled-in eye `+0x2D0` (`0x003CC130`, `0x0032B2BF`-`0x0032B2F2`). Whenever the
normal branch pulled the camera in, the byte `+0x40` is then set to 0, with Camera Auto-Rotation on or off
(`0x0032B2F7`, `0x0032B2FB`).

Last it eases the floor lift and the distance scale (`0x0032DDE0`, `0x0032DE90`, `f = 1 + cos(π + π/4 × (T - n) / T)`
below), copies the orbit look `+0xA0` to the follow look `+0x2F0` and stores at `+0x130` the horizontal distance
from the follow eye `+0x2E0` to it, `[camera + 0x130] = √((x2F0 - x2E0)² + (z2F0 - z2E0)²)`, with `x` and `z` the
words `+0x0` and `+0x8` of each point (`sqrtf` `0x00861F14`; `0x0032B308`-`0x0032B379`).

Each ease first counts its hold down by 1 while the hold is above 0. While the hold `n` is then below the length
`T`, it moves the value the fraction `f = 1 + cos(π + π/4 × (T - n) / T)` of the way to its rest value
(`cosf` `0x00861F08`):
- the lift: `[camera + 0x128] = lift + (0 - lift) × f`, with `n = [camera + 0x12C]` and
  `T = 20 × [0x01DFE0B4]` (`0x0032DDE6`-`0x0032DE78`);
- the scale: `[camera + 0x120] = scale + (1 - scale) × f`, with `n = [camera + 0x124]` and
  `T = 60 × [0x01DFE0B4]`; it also clears the bytes `+0x40` and `+0x80` (`0x0032DE96`-`0x0032DF31`).

### The followed transform

Each controller keeps two poses of `0xB0` bytes, a start at `+0x6E0` and a target at `+0x790`, and a weight at
`+0x840`. A pose holds a position at `+0x00` and a heading pair `(a, 0, b, 1)` at `+0x10`. The target comes from the
leader's body block, whose pair `0x003DAF20` writes as `a = cos h`, `b = sin h` of the body heading `h` (`+0xF8`).

`0x00259510(out, from, to, t)` blends the position linearly and reads each heading as `atan2f(a, b)`, which for a body
pair is `pi/2 - h`. It adds `t` times the shorter difference (`0x003A1C50`) to `from`'s angle and writes `a = cosf` and
`b = sinf` of the result, so at `t` = 1 a body pair comes out swapped, `(sin h, 0, cos h, 1)`. `0x0032CE40` reads the
output as `atan2(b, a)`, which gives that angle back.

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

The file is kind 9 file 3, `common/behindcamera.bin` (1,040 bytes): a 16-byte header whose `+0x04` is 16, then
16 entries of 64 bytes. Each entry is the float `+0x00` (the look point's raise, 1.3 to 3.5), a word `+0x04` that
the copy skips (0 in all 16), and the seven heights at `+0x08` and seven distances at `+0x24`. Every type is in
[`behindcamera-types-rows.tsv`](behindcamera-types-rows.tsv). Types 0 and 13 hold the default pairs; the others
use three more profiles, with raises 2.0 (types 1, 2, 4, 5 and 7 to 9), 3.5 (3, 6 and 10 to 12) and 2.2 (14
and 15).

### Columns of behindcamera-types-rows.tsv

One row per entry of `common/behindcamera.bin`, 16 rows, `type` 0 to 15; the entry of type t starts at file
`+0x10 + 64 × t`. All 224 height and distance cells equal the file's float rounded to one decimal place.

| Column | Holds |
|---|---|
| `below_count` | `yes` when the type is below the table's count `+0x04` (16), so `0x0025A160` accepts it; `yes` on all 16 rows |
| `word_00` | the entry's `+0x00` as the integer of its bits: the float raise of the look point, 1.3 (`1067869798`, types 0 and 13), 2.0 (`1073741824`), 2.2 (`1074580685`) or 3.5 (`1080033280`) |
| `word_04_not_copied` | the 32-bit word at entry `+0x04` in hex, which `0x00259FE0` does not copy; `0x00000000` on all 16 rows |
| `a0`, `a1`, `a2`, `a3`, `a4`, `a5`, `a6` | the seven heights, the floats at entry `+0x08 + 4k` for `ak`, copied to controller `+0x10 + 12k`; they rise from `a0` to `a6` on all 16 rows, from −1.9 (`a0`, lowest) to 7.6 (`a6`, highest) |
| `b0`, `b1`, `b2`, `b3`, `b4`, `b5`, `b6` | the seven distances, the floats at entry `+0x24 + 4k` for `bk`, copied to controller `+0x14 + 12k`; they rise from `b0` to `b6` on all 16 rows, from 2.8 to 8.8, and `b6` is 8.8 on all 16 |

`setbehindcameratype` (`0x01CB`, `0x00356CB0`), `0x00304060` and `0x00304140` call `0x0025A160(type)`: for a type below the table's count `+0x04` it sets
`0x02098DF8` and `0x00259FE0` copies the type's 64-byte entry (from table `+0x10`) into both controllers:
its first word to `+0x64` and seven pairs of floats to `+0x10 + 12k` and `+0x14 + 12k`. `0x003D9C40`
then stores at `+0x18 + 12k` each segment's length between consecutive pairs as a share of their
total.

The types the game selects: `0x00304060` and `0x00304140` pass `0x0031B950(i)`, the camera type of the party row
in selection slot i (`0x0031B981`), slot 3 for `0x00304060` (`0x003040AB`-`0x003040B7`) and the saved leader's slot
`0x00327200()` for `0x00304140` (`0x00304144`-`0x00304152`). `0x0031B8E0` reads it from the row's byte `+0x07`
(`0x0031B934`): 0 for the 26 main and guest rows, 1 to 13 for the Espers (Belias 1 to Zodiark 13) and 14 for
the Chocobo (row 26) ([party table](../Party/party-table.md)).

No script calls `setbehindcameratype`:
there are 0 calls in the 1,114 us scripts and in the 8,914 containers of the other eight language trees. The
writers of `0x02098DF8` are `0x00259370` and `0x00259E90`, which store 0 (`0x00259383`, `0x00259F8E`), and `0x0025A160`
(`0x0025A171`). `0x00259FE0` is called from `0x00259370` and `0x0025A160` alone (`0x0025938D`, `0x0025A177`). So type 15 is
loaded with the others and selected by nothing in the shipped game.

The same walk keeps running totals of those shares, the profile's position at the start of a
segment, in three controller fields: `+0x1D0` the start of segment 3; `+0x1D4` the start of segment 2,
or of segment 1 when `+0x2A0` is non-zero; and `+0x1D8` the start of segment 4, or of segment 5 when
`+0x2A0` is non-zero.

`0x003D99B0` runs it too, on the default pairs `0x01EFE998` to `0x01EFE9CC`, from
(−0.7, 2.8) to (7.6, 8.8), the end points of the orbit curve below with the height first, which it copies
into the controller first (`0x003D99DF`-`0x003D9AB0`, `0x003D9B3E`). `0x003D9B80` runs it on the pairs the
controller holds at that moment (`0x003D9C1F`).

### Other controller settings

- `0x0025A540(flag, vector)` writes the vector to `+0x00` of both controllers and the flag to `0x02098DE9`,
  the byte that limits the follow camera to republishing. It has three callers:
  - `0x002628B0` (`0x00262D07`);
  - `lockbehindcamera` (`0x01CA`, `0x00356470`), with flag 1 and its three int arguments as floats, w 1.0
    (`0x003564DF`);
  - `unlockbehindcamera` (`0x01CE`, `0x00356920`), with flag 0 and the vector {0, 0, 0, 1.0} (`0x00356959`).
- `tutorial_set_behindcameraenable` (`0x03A1`, `0x003503B0`) stores whether its int is non-zero at
  `0x02098354` (`0x0025A880`), and `tutorial_get_behindcameraenable` (`0x03A0`, `0x0034FFA0`) returns it
  (`0x0025A850`). Opening the pause menu (`0x00229590`) saves the value and clears it.

### The orbit

The camera is a heading `+0x70` (radians, wrapped to 0 to 2π) and a height level `+0x7C` (0 to 1).
`0x0032DF40(heading, level, look, out)` turns the level into a pitch and a distance. It copies the look point to
`out +0x20`, stores the heading at `+0x30`, the level at `+0x3C`, the pitch at `+0x34` and the distance at
`+0x38`, and clears the byte `out +0x00` (`0x0032DF46`-`0x0032DFF1`):

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

The slot is block `n` of the camera, `camera + 64 × n` (`0x0032CD41`-`0x0032CD50`); `0x0032BCC0` passes 2, the orbit block
`+0x80`. The eye is written to slot `+0x10` with w 1.0 (`0x0032CD98`-`0x0032CDD6`) and copied to `0x01EED450`, whose address
`0x0032CD20` returns. A first `0x003CC2F0` call, from the vector at `0x01EED460`, writes only a stack copy that the function
does not read again (`0x0032CD5E`-`0x0032CD74`).

Each frame `0x0032B9C0` adds the input rates to heading and level, divided by `+0x100`: 1.0 when idle, the
frame-rate float `0x00229E70()` while input moves the camera (`0x0032C910`). It also adds the wall turn
`+0x104`, the wall lift `+0x108` and the auto-rotation `+0x10C`. `0x0032BA70` is the same without the
wall and auto terms.

`0x0032B9C0` first forms the heading
`h = [camera + 0x70] + [camera + 0xF8] / [camera + 0x100] + [camera + 0x104] + [camera + 0x10C]`
(`0x0032B9C0`-`0x0032B9E5`). It wraps the heading into 0 to 2π, `h = h - 2π` while `h > 2π` and `h = h + 2π` while
`h < 0`, stores it at `+0x70` and clears the byte `+0x40` (`0x0032B9ED`-`0x0032BA27`).

The level is `l = [camera + 0x7C] + [camera + 0xFC] / [camera + 0x100] + [camera + 0x108]`
(`0x0032BA2B`-`0x0032BA40`). It clamps the level to 0 to 1, `l = l < 0 ? 0 : l > 1 ? 1 : l` (`maxss xmm2, xmm0`,
`minss xmm1, xmm2`, `0x0032BA4C`-`0x0032BA50`), and stores it at `+0x7C` (`0x0032BA54`). While bit `0x200` or `0x800` of
`+0xC0` is set (a vertical stick deflection this frame, `0x0032D620`) it also keeps the new level,
`[camera + 0x114] = l` when `[camera + 0xC0] & 0xA00` is non-zero (`0x0032BA59`-`0x0032BA65`).

### Stick, mouse and recentre

`0x0032C910` reads the dead zone `+0xF4` (`0x0046DB20`: 50) and the two camera axes `0x0046DB10(0)` and
`0x0046DB10(1)`, centred at `0x80`, and the pad word `0x0036FF80()` (through `0x0046DB40`). While `+0x374` is 0 it takes 0 for both axes and the pad word (`0x0032C92C`, `0x0032C939`, `0x0032C95B`-`0x0032C960`), so the stick neither turns the camera nor starts a recentre:

- `0x0032D3D0` turns the horizontal axis into the heading rate `+0xF8`. Past the dead zone the rate is
  `0.4 × 2π / (30 × [0x01DFE0B4])` per frame times the deflection beyond it, over `128 − 50`, eased
  as `(2 × old + new) / 3`; while `0x001EDE70` is set during a recentre (state bits `0x40300000`) it eases as
  `(5 × old + new / 2) / 6` instead (`0x0032D4AA`-`0x0032D4E3`).
- A deflection sets bit `0x100` of `+0xC0` when it stays positive past the dead zone, else bit `0x400`
  (`0x0032D512`-`0x0032D52A`).
- A deflection toward a side whose wall probe is hit counts as zero, but it is still input: the function returns 1
  (`0x0032D454`-`0x0032D46E`, `0x0032D534`).
- With no stick input and camera input enabled (`+0x374`, 1 after `0x0032B790`; `0x02098354` for the first controller,
  which `tutorial_set_behindcameraenable` sets), a mouse movement of 7 or more (`0x001E0CE0`, negated by Camera X-Axis
  Inverted) drives the same rate, times Mouse Sensitivity Left/Right (`0x0017E420`) and 0.2, applied to the eased value;
  the mouse ignores the wall probes (`0x0032D53E`-`0x0032D5A6`).
- `0x0032D620` does the same for the level rate `+0xFC` from the vertical axis, `0x001E0D30` and `0x0017E430`. The stick
  gives `0.8 / (30 × [0x01DFE0B4])` per frame with the sign turned, so a positive deflection lowers the level; it is
  blocked toward a hit above (`0x22`) or below (`0x88`) and sets bit `0x200` or `0x800` (`0x0032D692`-`0x0032D734`).
- The level's mouse term, not negated, uses the heading's `0.4 × 2π / (30 × [0x01DFE0B4])` and the same sensitivity
  factor (`0x0032D73F`-`0x0032D7A5`).
- With no input, both rates are multiplied by `[0x022C3180]` each frame: 0.5, or √0.5 when `0x001EDE70` is
  set (`0x0032AE70`), and a rate whose size is then below 0.00001 is set to 0 (`0x0032D5DD`-`0x0032D5F8`,
  `0x0032D7DC`-`0x0032D7F7`). They stop at once when Camera Auto-Rotation (`0x0017E260`) is off and no recentre is
  running.
- Bit `0x4` of the pad word `0x0036FF80()` starts a recentre (`0x0032DC00`) toward the heading
  `3π/2 − facing`, behind the leader. The swing is converted into a stick deflection `+0x370`;
  `0x0032D820` feeds it through `0x0032D3D0` each frame until the heading arrives. Each press adds 1 to `+0x364`
  (`0x0032C983`).
- `0x0032DC00(camera, heading, again)` turns the current heading `+0x30` and the target into −π to π and keeps the
  target at `+0x36C`. A first call (`again` 0) sets bit `0x200000` and zeroes `+0x118`, and its deflection is a sixth
  of the swing.
- In `0x0032DC00`, with `h` the wrapped heading and `d = target - h`, bit `0x40000000` names the way round. It is set
  when `0 <= d <= π`, `d >= 2π` or `-2π < d < -π`, with `d = d + 2π` when `h > target`, and cleared otherwise,
  with `d = d - 2π` when `target > h` (`0x0032DC79`-`0x0032DD5B`).
- Bit `0x100000` is set while the swing exceeds π/40, `abs(d) > 0.0785398` (`0x0032DD13`-`0x0032DD5B`), and `+0x370`
  holds the size only: `[camera + 0x370] = (int)((128 - z) × a / R + z)`, with `z` the dead zone `+0xF4`,
  `a = abs(d)` (`abs(d) / 6` on a first call) and `R = 0.4 × 2π / (30 × [0x01DFE0B4])`, the heading rate at full
  deflection (`0x0032DD65`-`0x0032DDCA`).
- During a recentre `0x0032DB10` eases the level to 0.483 over `30 × [0x01DFE0B4]` frames: with `n` the step
  count `+0x118` and `D = 30 × [0x01DFE0B4]` it writes `a + (0.483 − a) × (1 + cos(π + π × n / D)) / 2`, `a` the
  level copy `+0x3C`, to `+0x7C` and to the kept level `+0x114`, and clears byte `+0x40`
  (`0x0032DB16`-`0x0032DBA1`).
- While `n` is below `D`, `0x0032DB10` adds 1 to `+0x118` and returns 1; otherwise it returns 0, and its call at
  `0x0032CA23` then clears the recentre bit `0x200000` (`0x0032DBD0`-`0x0032DBDE`, `0x0032CA2A`-`0x0032CA2C`).
- Any stick or mouse input sets the divisor `+0x100` to `0x00229E70()` and bit `0x20000000`, and ends a running recentre
  by clearing `0x100000`, `0x200000` and `0x40000000` (`0x0032C9B8`-`0x0032C9D4`); with no input the divisor is 1.0. The
  recentre steps run only on frames with no input on their axis, and once both are done bit `0x40000000` is cleared
  too (`0x0032C9DA`-`0x0032CA48`).

### Camera Auto-Rotation

`0x0032C650` turns the heading toward `3π/2 − facing` once the leader has been moving (state
`0x8000000` without `0x4000000`) for `15 × [0x01DFE0B4]` frames. The turn is proportional to the
angle and falls as the camera rises. It is capped at `0.2 × 2π / (30 × [0x01DFE0B4])` per frame,
and no turn is made when the camera would have to swing more than 150°, as when the leader runs toward it. With Camera
Auto-Rotation off (`0x0017E260`, CameraRevise) the term is 0; on, it is eased as `(3 × old + new) / 4` into `+0x10C`.

### Walls around the camera

`0x0032D2E0` places four test segments (`0x0032C3E0`) in the frame of the current camera matrix
`0x02AEDEF0`: from beside the followed position to beside the eye on the left and right, from above the
followed position to 2.0 above the eye, and from low on it to 0.3 below the eye. The side offsets and
heights come from the followed transform's `+0x64` and `+0x6C`. `0x0032CF50` casts each against the
field's collision part (`0x0026E500(0)`, kept at `+0x2C8`) through `0x003D97E0` and sets bit `0x1`, `0x2`,
`0x4` or `0x8` of `+0xC0` (`0x01EED488`) for each hit.

`0x0032C3E0(transform, eye, position, matrix, segments, y)` sets the matrix's translation to the position and starts the
segments at local z 0.5: the sides at x `∓s` and height `h / 2`, the upper one at height `h`, the lower one at 0.5,
with `h` the transform's `+0x6C` and `s` = `+0x64 × (1 − 0.5 × (y − [0x022C3188]) / ([0x022C3184] − [0x022C3188]))`
(`0x0032C408`-`0x0032C501`). It then moves the translation to the eye and ends the side segments at x `∓0.5`, z 1.0
(`0x0032C506`-`0x0032C55D`).

In `0x0032CF50` a hit is a non-negative answer, kept as a word at segment `+0x50`, and each cast passes mask 4
(`0x0032CF9B`-`0x0032CFC7`). The bits follow the segment order: `0x1` the `−s` side, `0x2` the upper, `0x4` the `+s` side
and `0x8` the lower segment.

- `0x0032C180` turns the heading when one side is hit (state bits `0x11` one way, `0x44` the other) at
  `0.12 × 2π / (30 × [0x01DFE0B4])` per frame, eased into `+0x104`; otherwise `+0x104` decays by 0.9
  a frame. The turn is eased as `(4 × old + new) / 5` and sets bit `0x4000` (`0x11`) or `0x1000` (`0x44`) of `+0xC0`;
  with both sides hit it turns neither way, and the decay stops at 0 below 0.00001 (`0x0032C1A7`-`0x0032C1F7`,
  `0x0032C207`-`0x0032C2AE`).
- `0x0032C2B0` lowers the level for a hit above (`0x22`) and raises it for a hit below (`0x88`) at
  `1.2 / (30 × [0x01DFE0B4])` per frame, eased into `+0x108`; otherwise `+0x108` halves each frame.
  A hit above wins over one below; the lift is eased as `(4 × old + new) / 5` and sets bit `0x8000` or `0x2000`, and
  the halving stops at 0 below 0.00001, `x = x × 0.5` then `x = 0` when `abs(x) < 0.00001` (`0x0032C2E6`-`0x0032C3D0`).
- Both act only while Camera Auto-Rotation is on, the leader has moved since the last camera input
  (bit `0x10000000` set, `0x20000000` clear) and the camera is not pulled in, with bits `0x4000000` and `0x40000`
  clear. With Auto-Rotation off `0x0032C180` zeroes `+0x104`, and `0x0032C2B0` zeroes the wall turn `+0x104` too, not its
  own `+0x108`, which halves, `[camera + 0x108] = [camera + 0x108] × 0.5` (`0x0032C1BE`, `0x0032C2E0`-`0x0032C2F6`).

### Floors and props under the eye

`0x0032BB00(camera, eye, look)` returns how far to lift the eye, the largest of: the value the body-record
query `0x0046DB50` returns for the eye; within 1.2 of the look point, `√(1.44 − d²)` for the horizontal
distance `d`; and the amount that puts the eye 0.27 above the floor triangle under it (`0x002321D0`,
`0x00231890`). A lift at least as large as the current one `+0x128` replaces it and sets the hold `+0x12C` to
`20 × [0x01DFE0B4]` frames.

The lift is not held flat. From the first call of `0x0032DDE0` after that, the hold counts down and the lift eases
toward 0 by a fraction that grows from near 0 to `1 − √2/2` (0.2929) as the hold runs out, and stays at `1 − √2/2`
each call once the hold is 0.

`0x0032BB00` itself returns the current lift when that is larger, and sets the hold `+0x12C` when it returns the new
one, `[camera + 0x12C] = (int)([0x01DFE0B4] × 60 / 60 × 20)` (`0x0032BC3D`-`0x0032BC83`); its caller `0x0032BCC0` stores the result at `+0x128` (`0x0032BD2D`, `0x0032BE55`). The 1.2 test
uses the full distance to the look point and the root the horizontal one (`0x0032BB8B`-`0x0032BBEE`).

### Pulling in

`0x0032BCC0(camera, out)` places the eye at full distance with no lift and stores the lift `0x0032BB00` gives for it at
`+0x128` (`0x0032BD08`-`0x0032BD2D`). It tests the eye placed with that lift and the distance scale `+0x120` with the wall
contact `0x00232490`, which sets bit `0x20000` on a contact, and the full-distance eye with a ray (`0x00231690`); a
contact, or a ray shorter than 0.27, widens the polygon mask of the sweep that follows from 4 to `0xFFFF`
(`0x0032BD38`-`0x0032BDCA`).

It then sweeps a 0.27 sphere from the look point to the lifted eye (`0x00230C00`). A non-zero return (a ray hit, or the
push moved the point) puts the eye at the sweep's output, sets `0x4040000` and returns 0 (`0x0032BE17`-`0x0032BE2D`). With
a zero return the eye stands where the orbit puts it: the lift `0x0032BB00` gives for the sweep's output block is stored
at `+0x128` and the eye is placed again with it, and `0x0032BCC0` returns 1 (`0x0032BE31`-`0x0032BE7B`).

The normal branch `0x0032B390` runs Camera Auto-Rotation (`0x0032C650`); then, unless pulled in, the probes (`0x0032D2E0`,
`0x0032CF50`), clearing bit `0x40000` when no probe hit (`0x0032B3BE`-`0x0032B3CC`); the wall turn `0x0032C180`; the wall lift
`0x0032C2B0`, or, when the wall turn set bit `0x1000` or `0x4000` (`[camera + 0xC0] & 0x5000`, `0x0032B3DA`), a
halving of `+0x108` that stops at 0 below 0.00001, `x = x × 0.5` and then `x = 0` when `abs(x) < 0.00001`
(`0x0032B3F0`-`0x0032B423`).

It then adds the rates (`0x0032B9C0`), places the orbit (`0x0032DF40`) and runs `0x0032BCC0`. Its eye goes to `+0x2E0`, and
a pulled-in eye also to `+0x2D0`, with byte `+0x80` cleared (`0x0032B42D`-`0x0032B4B6`).

In the same call (see `0x0032B1C0` above) `0x0032B4D0` takes the pulled-in branch. It zeroes the wall turn `+0x104` and
the auto-rotation `+0x10C`, sets the orbit look `+0xA0` to the look point and, when bit `0x10000000` is set and Camera
Auto-Rotation is on, turns the heading toward the pulled-in eye `+0x2D0` (`0x003CC130`; `0x0032B4D8`-`0x0032B553`). It then
adds the rates without the wall and auto terms (`0x0032BA70`) and places the orbit (`0x0032DF40`).

`0x0032BEB0` sweeps again (`0x0032BF38`). On a hit it places the eye with the distance scale `+0x120` and sweeps
again, up to two retries (`0x0032C021`-`0x0032C052`); a hit nearer than the current scale first shrinks `+0x120` to
the hit's share of the full horizontal distance and clears bytes `+0x40` and `+0x80` (`0x0032BFC7`-`0x0032BFDB`).

With a hit its eye is the last sweep's output, the contact or the shortened eye, raised by the lift `0x0032BB00`
gives, which it stores at `+0x128` (`0x0032C084`-`0x0032C0B4`), and at most 9.0 above the followed position
(`0x0032C0D1`-`0x0032C0DE`); it replaces the orbit heading `+0xB0` and distance `+0xB8` with those from the look point
to that output (`0x003CC130`, `0x0032C0EB`, `0x0032C100`), clears byte `+0x80` (`0x0032C0F9`, `0x0032C108`) and returns 0.

With no hit it places the eye with the scale `+0x120` and lift `+0x128` (`0x0032C111`-`0x0032C139`), clears bit
`0x20000` of `+0xC0` (`0x0032C141`) and returns 1. Its eye goes to `+0x2E0`, and a hit eye also to `+0x2D0`
(`0x0032B57D`-`0x0032B5E2`).

That shrink also sets the count `+0x124` to `T = 60 × [0x01DFE0B4]` (`0x0032BFE2`-`0x0032C008`). `0x0032DE90` counts it
down before testing it, so the scale starts easing back toward 1 on the next update, by a fraction that grows as
the count falls. At count 0 each update still moves it the fraction `1 - √2/2` of the way, so it approaches 1 and
no update sets it to exactly 1. When a sweep is clear, bit `0x4000000` is cleared
(`0x0032B59E`) and the normal branch `0x0032B390` runs again, in the same call when the pulled-in branch ran first.

### Framing a target

`0x003D9E20` copies the target cursor's actor (`[0x02B47730] + 0xC8`, while its `+0xC0` bit `0x4` is set)
into `0x02B4E4A0` and raises `0x02B4E4A5`. `0x0032B900` then fetches the point of interest (`0x0032D250`):

1. the point `0x00290A90` returns from the UI manager `[0x0209BE80]`;
2. otherwise the actor's position (`0x003588B0`, `0x002E7F70`); with no actor the point keeps its last value (`0x0032D289`).
   Either way only x, y and z of `+0x350` are written (`0x0032D298`-`0x0032D2BA`).

`0x0032CA70` frames it when the pitch from the point to the leader's look point is at most 80° (1.396). The
eye goes 3.0 out from the leader on the line away from the point, turned by 0.25 rad, and passes the same
wall, ray and sweep tests; the look point is the point of interest. When it declines, bit `0x80000` stops
further tries until the cursor closes (`0x0032B900`). A sweep hit moves the framing eye `+0x300` to the hit point
(`0x0032CC29`); the framing look `+0x310` gets the point of interest and `0x0032CA70` returns 1, or 0 when it declines
(`0x0032CAC0`, `0x0032CC30`-`0x0032CC6D`).

`0x0032B900` keeps the framed actor at `+0x360`: while `0x02B4E4A6` is set it takes `0x02B4E4A0` when the cursor's actor
changed (`0x02B4E4A4`) or `+0x360` is 0, and otherwise keeps it; with `0x02B4E4A6` clear it stores 0
(`0x0032B90F`-`0x0032B936`). It tries only while the cursor is open (`0x02B4E4A5`; closed, it clears bit `0x80000`,
`0x0032B994`), bit `0x80000` is clear and `+0x360` is set; it returns what `0x0032CA70` returned, or 0, and keeps that at
`0x022C318C` (`0x0032B93C`-`0x0032B9A5`).

`0x0032AEC0` counts `+0x320` up while framing and down otherwise, capped at `15 × [0x01DFE0B4]`. `0x0032D000`
blends the follow eye and look (`+0x2E0`, `+0x2F0`) toward the framing pair (`+0x300`, `+0x310`) by
`(1 + cos(π t + π)) / 2`, with `t` the count over its cap, going round the shorter way (`0x0032CC90`).

`0x0032AEC0` keeps what `0x0032C5E0` answers at `+0x324` when framing starts and when it ends (`0x0032AF82`,
`0x0032B01A`).

`0x0032AEC0` passes `0x0032C5E0` the addresses of the follow eye, the follow look, the framing eye and
the framing look; `0x0032C5E0` stores the four in its home slots and gives `0x003CC130` the addresses of those
slots, not the positions (`0x0032C5E3`-`0x0032C60B`, `0x0032C628`-`0x0032C62D`), so the answer does not follow where
the camera or the target is.

`0x0032D000` blends the eye linearly into `+0x330`; for
the look it blends the heading, pitch and distance from eye to look of the two pairs (`0x003CC130`) and places the
published look `+0x340` from the blended eye with them (`0x003CC2F0`, `0x0032D22A`).

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

`0x001825C0` does nothing when `0x00189120` returns null (`0x001825DF`). `0x001894D0` picks the copy `+0x1C ≠ 0` at a stride
of `0x338` (`0x001894D5`-`0x001894DD`) and copies only the vector's x, y and z, and only for a non-null point
(`0x001894F6`-`0x00189515`): the null point of `0x00259820` leaves the last vector in place.

## Layouts

Follow camera (controller + `0x2B0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x060` | `f32[4]` | look point | followed position + `0x11C` up |
| `+0x070` | `f32` | heading | 0 to 2π |
| `+0x07C` | `f32` | height level | 0 to 1 |
| `+0x080` | `...` | orbit block | look `+0xA0`, heading `+0xB0`, pitch `+0xB4`, distance `+0xB8`, level `+0xBC`, byte `+0x80` cleared (`0x0032DF40`) |
| `+0x0C0` | `u32` | state | probe hits `0x1`-`0x8`, `0x4000000` pulled in, `0x8000000` leader moving |
| `+0x0F4` | `i32` |  | stick dead zone 50 |
| `+0x0F8` | `f32` |  | heading rate |
| `+0x0FC` | `...` |  | level rate |
| `+0x100` | `f32` | rate divisor | 1.0 idle, `0x00229E70`() under input |
| `+0x104` | `f32` |  | wall turn |
| `+0x108` | `...` |  | wall lift |
| `+0x10C` | `...` | auto-rotation |  |
| `+0x11C` | `f32` | look height | 1.3 |
| `+0x120` | `f32` |  | distance scale |
| `+0x124` | `...` |  | its hold count |
| `+0x128` | `f32` |  | floor lift |
| `+0x12C` | `...` |  | its hold count |
| `+0x140` | `...` |  | four test segments, `0x60` apart |
| `+0x2C0` | `void*` |  | followed transform |
| `+0x2C8` | `void*` | collision part | `0x0026E500`(0) |
| `+0x2E0` | `f32[4]` |  | follow eye |
| `+0x2F0` | `...` |  | follow look |
| `+0x300` | `f32[4]` |  | framing eye |
| `+0x310` | `...` |  | framing look |
| `+0x320` | `i32` | framing count | 0 to 15 x [`0x01DFE0B4`] |
| `+0x330` | `f32[4]` |  | published eye |
| `+0x340` | `...` |  | published look |
| `+0x350` | `f32[4]` |  | point of interest |
| `+0x360` | `u32` |  | framed actor |
| `+0x368` | `f32` |  | travelled distance |
| `+0x370` | `i32` |  | recentre deflection |
| `+0x374` | `u32` | camera input enabled (stick, pad, mouse) | 1 |

## State

| Address | What |
|---|---|
| `0x02097D30` | the camera controllers, 0x860 bytes each |
| `0x02097D20`, `0x02098580` | the two camera contexts, each 16 bytes before its controller: those 16 bytes and controller `+0x848`-`+0x84F` hold 0 and move only when `setinterventioncamera` copies one context over the other (`0x00359410`: `0x002593D0`, `0x00259470`); controller `+0x844` is only ever stored 0 (`0x00259811`, `0x0025A2B5`) |
| `0x02B4E3F0`, `0x02B4E3F4`, `0x02B4E3F8` | the framed actor's position x, y and z, the first three floats of a `0xB0`-byte copy of its movement body's placement `+0x30` (`0x003D9ED1`): `0x003D9E20` writes them from `0x002E7F70` (`0x003D9F4F`, `0x003D9F65`, `0x003D9F5D`) and raises `0x02B4E4A6` (`0x003D9F6D`); `0x003D9FB0` zeroes the `0xC0` bytes from `0x02B4E3F0` (`0x003D9FB2`) |
| `0x02B4E4A0`, `0x02B4E4A5` | the framed actor and its flag (`0x003D9E20`) |
| `0x022C3184`, `0x022C3188` | the highest and lowest `y` kept for the curve, 7.598 from `0x00D108E4` (the curve's own end point is 7.6) and −0.7 from `0x00D108F4` (`0x0032B74F`-`0x0032B776`) |
| `0x01EED478` | the curve's end points |
| `0x01EED488` | the four probe bits |

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01EED440` | `f32` | 0 (image) | x of the eye `0x0032AEC0` last published, one copy for both controllers. Each call adds the distance from it to the new published eye `+0x330` to the travelled distance `+0x368` (`0x0032B10F`-`0x0032B163`), then copies the new eye's four floats over `0x01EED440`-`0x01EED44C` | `0x0032AEC0` (`0x0032B16F`) | `0x0032AEC0` (`0x0032B10F`) |
| `0x01EED444` | `f32` | 0 (image) | its y | `0x0032AEC0` (`0x0032B17C`) | `0x0032AEC0` (`0x0032B117`) |
| `0x01EED448` | `f32` | 0 (image) | its z | `0x0032AEC0` (`0x0032B189`) | `0x0032AEC0` (`0x0032B128`) |
| `0x01EED44C` | `f32` | 1.0 (image) | its w, copied with the rest | `0x0032AEC0` (`0x0032B19E`) | no instruction names it |
| `0x01EED450` | `f32` | 0 (image) | x of the eye `0x0032CD20` places: it copies the placed eye's four floats to `0x01EED450`-`0x01EED45C` (`0x0032CDE8`-`0x0032CE0F`) and returns their address (`0x0032CDDD`) | `0x0032CD20` (`0x0032CDE8`) | through the returned pointer: `0x0032BCC0` (`0x0032BE65`-`0x0032BE75`), `0x0032BEB0` (`0x0032BF5B`, `0x0032BF60`, `0x0032C126`-`0x0032C136`), and the calls it is handed to: `0x0032BB00` (`0x0032BD1A`), `0x00232490` (`0x0032BD50`), `0x00231690` (`0x0032BD9D`), `0x00230C00` (`0x0032BE12`, `0x0032BF38`, `0x0032C047`) and `0x0032C3E0` (`0x0032D397`) |
| `0x01EED454` | `f32` | 0 (image) | its y | `0x0032CD20` (`0x0032CDF5`) | through the returned pointer: `0x0032BCC0` (`0x0032BE65`-`0x0032BE75`), `0x0032BEB0` (`0x0032BF5B`, `0x0032BF60`, `0x0032C126`-`0x0032C136`), and the calls it is handed to: `0x0032BB00` (`0x0032BD1A`), `0x00232490` (`0x0032BD50`), `0x00231690` (`0x0032BD9D`), `0x00230C00` (`0x0032BE12`, `0x0032BF38`, `0x0032C047`) and `0x0032C3E0` (`0x0032D397`) |
| `0x01EED458` | `f32` | 0 (image) | its z | `0x0032CD20` (`0x0032CE02`) | through the returned pointer: `0x0032BCC0` (`0x0032BE65`-`0x0032BE75`), `0x0032BEB0` (`0x0032BF5B`, `0x0032BF60`, `0x0032C126`-`0x0032C136`), and the calls it is handed to: `0x0032BB00` (`0x0032BD1A`), `0x00232490` (`0x0032BD50`), `0x00231690` (`0x0032BD9D`), `0x00230C00` (`0x0032BE12`, `0x0032BF38`, `0x0032C047`) and `0x0032C3E0` (`0x0032D397`) |
| `0x01EED45C` | `f32` | 1.0 (image) | its w | `0x0032CD20` (`0x0032CE0F`) | through the returned pointer: `0x0032BCC0` (`0x0032BE65`-`0x0032BE75`), `0x0032BEB0` (`0x0032BF5B`, `0x0032BF60`, `0x0032C126`-`0x0032C136`), and the calls it is handed to: `0x0032BB00` (`0x0032BD1A`), `0x00232490` (`0x0032BD50`), `0x00231690` (`0x0032BD9D`), `0x00230C00` (`0x0032BE12`, `0x0032BF38`, `0x0032C047`) and `0x0032C3E0` (`0x0032D397`) |
| `0x01EED474` | `u32` | 1 (image) | 1 while the camera is not framing a target. When framing starts with it set, `0x0032AEC0` records the way round (`0x0032C5E0`, kept at `+0x324`) and clears it; when framing ends with it clear, it records the way round again and sets it | `0x0032AEC0`, 0 (`0x0032AF8F`) and 1 (`0x0032B025`) | `0x0032AEC0` (`0x0032AF5D`, `0x0032AFAF`) |
| `0x01EFE990` | `u32` | 1 (image) | set to 1 by the controller set-up `0x003D99B0` and the reset `0x003D9B80` (with the controller's `+0x190` flags) | `0x003D99B0`, 1 (`0x003D9AC8`); `0x003D9B80`, 1 (`0x003D9BA6`) | no instruction names it |
| `0x02097D34` | `f32` | 0 (zero-filled tail of `.data`) | controller 0 `+0x04`: y of the vector `0x0025A540` writes to `+0x00` of both controllers. While `0x02098DE9` is set, `0x003D9950` copies the four floats to `+0x90` and publishes them as the eye, with the followed transform's position as the look point (`0x003D9950`-`0x003D99AA`) | `0x0025A540` (`0x0025A551`) | `0x003D9950` (`0x003D9968`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x02097D38` | `f32` | 0 (zero-filled tail of `.data`) | controller 0 `+0x08`: its z | `0x0025A540` (`0x0025A55E`) | `0x003D9950` (`0x003D996E`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x02097D3C` | `f32` | 0 (zero-filled tail of `.data`) | controller 0 `+0x0C`: its w | `0x0025A540` (`0x0025A56B`) | `0x003D9950` (`0x003D9974`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x02098590` | `f32` | 0 (zero-filled tail of `.data`) | controller 1 `+0x00`: x of the same vector | `0x0025A540` (`0x0025A577`) | `0x003D9950` (`0x003D9950`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x02098594` | `f32` | 0 (zero-filled tail of `.data`) | controller 1 `+0x04`: its y | `0x0025A540` (`0x0025A584`) | `0x003D9950` (`0x003D9968`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x02098598` | `f32` | 0 (zero-filled tail of `.data`) | controller 1 `+0x08`: its z | `0x0025A540` (`0x0025A591`) | `0x003D9950` (`0x003D996E`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x0209859C` | `f32` | 0 (zero-filled tail of `.data`) | controller 1 `+0x0C`: its w | `0x0025A540` (`0x0025A59E`) | `0x003D9950` (`0x003D9974`), through the controller pointer `0x00259990` passes (`0x00259A32`), when `0x02098DE9` is set |
| `0x022C318C` | `u32` | 0 (zero-filled tail of `.data`) | the result of the last framing attempt: `0x0032B900` stores what `0x0032CA70` returned (0 when it declined, `0x0032B983`) or, on its other paths, 0. It loads the word into `edx` before calling `0x0032D250` (`0x0032B95D`), which replaces `edx` with 3 before using it (`0x0032D268`) | `0x0032B900` (`0x0032B983`, `0x0032B9A5`) | `0x0032B900` (`0x0032B95D`) |
| `0x022C3198` | `f32` | 0 (zero-filled tail of `.data`) | the blended heading of the previous frame. `0x0032D000` blends the follow and framing headings by the framing weight and compares the new value with this one: on a change of more than π/8 either way (`0x00915610`, `0x00D108F0`) it stores the follow heading in a stack slot that it does not read again (`0x0032D13C`), so the test changes nothing. Then it keeps the new value | `0x0032D000` (`0x0032D15F`) | `0x0032D000` (`0x0032D116`) |
| `0x022C319C` | `f32` | 0 (zero-filled tail of `.data`) | the blended pitch of the previous frame, compared and kept the same way (`0x0032D174`-`0x0032D182`) | `0x0032D000` (`0x0032D1C5`) | `0x0032D000` (`0x0032D157`) |

## Modding notes

- Distance and height come only from the curve in `0x0032DF40`; changing its constants (2.8, 6, 0.205,
  0.995, 0.4788) changes the whole range, and `0x022C3184`/`0x022C3188` must follow for the auto-rotation
  scaling.
- Turn rates scale with `[0x01DFE0B4]`, so they hold the same speed at 30 and 60 fps.
- The 0.27 floor margin and sweep radius appear in `0x0032BB00`, `0x0032BCC0`, `0x0032BEB0` and `0x0032CA70`;
  change them together.
- Camera Auto-Rotation off also turns off the wall turn and wall lift, not only the drift behind the
  leader.
- A replacement `common/behindcamera.bin` keeps:
  - the 16-byte header with the type count as the word `+0x04`, and the 64-byte entries from `+0x10` laid out as
    in [The camera types](#the-camera-types);
  - at least 15 types. `0x0025A160` takes a type only when it is below the count (`0x0025A16C`, a signed test), and a
    type at or above it leaves `0x02098DF8` and both controllers as they were. The party table's camera types run
    0 to 14 (the Espers 1 to 13, the Chocobo 14), so with fewer types the members past the count keep the type
    set before them;
  - its length, or the entry for kind 9 file 3 in the
    [file size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md) changed with it, since the file
    is read at that size.
- With a count of 0 the start-up copy of type 0 is skipped (`0x00259370`); an empty file leaves the table pointer 0,
  so `0x0025A160` takes no type (`0x0025A16A`).

## Related

- [Scripted camera](scripted-camera.md): the camera records, submission and the matrices.
- [Post-processing](post-processing.md): the depth-of-field focus the camera requests.
- [Config screen](../Menus-And-HUD/config-screen.md): Camera Auto-Rotation, mouse sensitivity and axis options.
- [Geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md): the body-top query `0x0046DB50`.
- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): the collision
  part and the wall test.
- [Player movement](../Movement-And-Pathfinding/player-movement.md): the stick dead zone.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat action: `0x00327200` is called by `0x00313DB0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Gameplay: `0x0031B8E0` calls `0x00322C50`; `0x0031B950` calls `0x00322C50`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
