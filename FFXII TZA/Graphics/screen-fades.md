---
title: "Screen fades: the seven fade layers, the fade verbs and the per-movie fade schedule"
kind: "system"
category: "Graphics"
addresses: "022BDD60, 002EFA70, 002EF910, 00375900, 00375A20, 00375AE0, 00375470, 00374950, 00375500, 003740B0, 01EFAC20, 002EFE10, 002EFE40, 002EFE50, 002EFE60, 0037DDD0, 0037DEA0, 02EBF008, 00360710, 002EFD80, 002EFDC0"
---

## What the player sees

The screen going to black or white between areas, around a cutscene and around a pre-rendered
movie, and coming back. A fade to the colour stays on screen until something fades back in. A
skipped cutscene cuts to black at once. Every pre-rendered movie that ships with a schedule row
opens and closes with its own authored fade, some of them to white.

## How it works

### The seven fade layers

There are seven fade records of 0x30 bytes at `022BDD60`, one per layer 0 to 6. Every accessor
clamps the layer into 0..6 (for example `002EFA90`). A record holds the handle of the screen effect
that draws it, a state (0 free, 1 running, 2 finished), the direction and a 0x28-byte effect
descriptor (see Layouts). Layers are independent: fades on different layers run and draw at the
same time.

### Starting a fade

`002EFA70(layer, frames, direction, white)` starts every fade. Direction 0 fades out, to the
colour; direction 1 fades in, back to the scene.

1. It keeps the old descriptor's colour and bytes `+1` and `+3`, then clears the descriptor.
2. A running or finished record releases its old effect through `0024CFF0` and is freed.
3. It picks the colour (next section), stores the direction in record `+0x05`, and builds the
   descriptor: kind 1, stage `022BDEB4` in the low nibble of `+1`, blend `022BDD5D` in the high
   nibble, class 1 in `+2`, priority `022BDEB0` in `+3`, bit 0 of `+0x1C` set for a fade-in, and
   the duration `2 × frames` at `+0x24` (`002EFAF3`).
4. `00375900` files the descriptor and returns its handle; `003B0F80(handle, 1)` registers it, and
   a non-zero handle marks the record running (`002EFCE7`).
5. It resets the three selectors: blend 3, priority 0, stage 6 (`002EFCF4`-`002EFD05`).

`002EFE40(stage)`, `002EFE50(priority)` and `002EFE60(blend)` set the selectors for the next start
only. `002EFA20` resets them with all seven handles and the one-shot colour.

### The colour

In order (`002EFBD5`-`002EFC6F`):

- When the one-shot byte `022BDD5C` is set, the four bytes `022BDD58`-`022BDD5B` are the colour and
  the byte is cleared. `002EFE10(r, g, b, a)` arms it.
- Otherwise a fade-in on a layer that was running or finished keeps the previous colour, and also
  takes the previous fade's stage, blend and priority.
- Otherwise the colour is `0x80000000` (black) or, with `white` = 1, `0x80FFFFFF` (white). Alpha
  `0x80` is full strength.

### The screen-effect descriptor pool

Fades are one kind of screen effect. The pool holds 32 records of 0x70 bytes at `02EBF9E0`: the
0x68-byte descriptor, the handle at `+0x68` and an elapsed counter at `+0x6C`.

- `00375900(descriptor)` returns 0 when all 32 hold a handle. Otherwise `00375A20(stage, priority)`
  finds the insertion point, before the first record of a higher stage or of the same stage and a
  higher priority, and moves the later records down one slot. The handle is
  `0x80000000 | (++counter & 0x0FFFFFFF)` (counter `02EC07E8`), the counter starts at 0, and 0x68
  bytes are copied from the descriptor (`003759C9`-`00375A01`).
- The pool is kept packed and in draw order. `00375470(handle)` removes a record by moving every
  later record up one slot and clearing the last handle.
- A handle's top nibble is its class; class 8 is this pool. `0024DE70` (state) and `0024CFF0`
  (release) dispatch on it and reach `00375AE0` and `00375470`.

- `00374930` clears the handle `+0x68` of all 32 records, which empties the pool. It runs when
  effect group 8 is emptied (`0024C550(8)`).

`00375500(stage)` draws, in pool order, every record of that stage whose class byte is enabled in
`02EC07E0` and whose `+0x10` bit 0 is clear; kind 1 goes to `003740B0`. The frame bodies call it
for stages 2, 3, 5 and 6 in the scene draw `0022B0B0` and stage 7 after `00376470`, so the stage,
then the priority, sets the order in which fades and other screen effects cover each other.

### Drawing a fade

`003740B0` draws one full-screen quad (corners at ±1.0) in the descriptor's colour with alpha
`colourAlpha × f`, where `f = counter / duration` clamped to 0..1, and `1 − f` for a fade-in. With a
duration of 0 or a counter past it, a fade-out draws the full colour and a fade-in draws nothing.
The blend is entry `blend` of eight 8-byte words at `01EFAC20`, read as the PS2 GS `ALPHA`
register:

| Blend | Word | Result |
|---|---|---|
| 0, 3 | `0x44` | `(Cs − Cd) × As + Cd`, ordinary alpha blend (the default) |
| 1 | `0x48` | `Cs × As + Cd`, additive |
| 2 | `0x42` | `Cd − Cs × As`, subtractive |
| 4 | `0x49` | `Cd × As + Cd` |
| 5 | `0x46` | `Cd − Cd × As` |
| 6 | `0xA8`, fix `0x80` | `Cs`, opaque |
| 7 | `0x04` | `(Cs − Cd) × As + Cs` |

### Timing

The pool tick `00374950` (run by `00258D70` in the field frame's simulation step, and by the menu
frames `0022B8C0` and `0022BC20`) adds to the counter of every enabled record: 2 on its first tick, and 2 per tick while `001EDDA0` reports the
30 fps time base, else 1. The duration is twice the frame count, so a fade lasts `frames`
thirtieths of a second at either frame rate. The state query `00375AE0` answers 3 for a kind-1
record while the counter is below the duration and 5 once it reaches it.

The tick also asks `00374060(record)` about every kind-1 record and removes the record
(`00375470`) when it answers 0. It answers 1 while byte `+0xDEF` of `[0209AC30]` is 0 (`00254A70`),
bit `0x800` of `020926E4` is set and the record is not layer 3's, whose handle `002EF9F0(3)`
returns (`002EF9F0(layer)` reads a fade record's first dword, the layer clamped into 0..6).
Otherwise it answers 0 once the record has `+0x1C` bit 1 set and its counter `+0x6C` above
`+0x24`, and 1 before that.

`0022A040` answers 1 when a fade layer other than 3 is running (`002EFD20(layer)` = 1 for one of
layers 0–2 and 4–6). The render thread's block `0x19` arm `006234A0` asks it.

### The per-tick poll

`002EF910`, from the world tick `00314020`, asks for the state of every layer with a handle
(`0024DE70`):

- 3: the record is running.
- 5, fade-out: the record becomes finished and its effect stays in the pool, so the screen stays
  black or white.
- 5, fade-in: the effect is released and the record freed. For layers 0, 2, 4, 5 and 6
  (`bt 0x75`, `002EF9AF`) it then calls `001D6C80`, which runs the map prefetch step `001DA290`
  ([prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).

`002EF840(layer)` frees one layer and `002EF890()` all seven; the `mapjump` verb (`0x008D`, poll
`00355350`) calls `002EF890`.

### The script verbs

| Verb | Id | Handler | Start |
|---|---|---|---|
| `fadeout(frames)` | `0x00B6` | `00356650` | `002EFA70(0, frames, 0, 0)` |
| `whiteout(frames)` | `0x00B7` | `00356FE0` | `002EFA70(0, frames, 0, 1)` |
| `fadein(frames)` | `0x00B8` | `00355EB0` | `002EFA70(0, frames, 1, 0)` |
| `fadeout_d0(layer, frames)` | `0x00D0` | `00356270` | `002EFA70(layer, frames, 0, 0)` |
| `whiteout_d1(layer, frames)` | `0x00D1` | `00356A50` | `002EFA70(layer, frames, 0, 1)` |
| `fadein_d2(layer, frames)` | `0x00D2` | `003559B0` | `002EFA70(layer, frames, 1, 0)` |
| `fadetrans(blend)` | `0x00BC` | `00340580` | `002EFE60(blend)` for the next start |

The one-argument forms push 0 under the popped frame count and pop it back as the layer, so they
always use layer 0. The two fade-in handlers first call `00183070` and `001D6C20`, which clears byte
`+0x88` of the prefetch manager, the cache backfill gate of
[file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md). A `fadein` after
a `whiteout` on the same layer fades back from white, because a fade-in keeps the colour.

### The engine's own fades

Read from the arguments at each call of `002EFA70`:

| Layer | Caller | Fade |
|---|---|---|
| 0 | `0037DEA0` | the movie schedule (below) |
| 0 | `0035CA70` | out over 30 frames (`0035CABB`), in over 30 (`0035CAE9`) |
| 0 | `00280140` | in over 1 frame |
| 2 | `00314530`, `003601D0` | out at once |
| 2 | `0025D9E0` | in over 8 frames |
| 2 | `00394130`, `003EFAA0` | out over 15 and 60 frames |
| 3 | `003145E0`, `003601D0`, `0027EFA0` | in at once |
| 3 | `003939B0` | out over its argument's frame count |
| 3 | `002CC960`, `002CC9C0` | in and out over lengths computed from their argument |
| 4 | `00360710` | the skip: out at once |
| 4 | `003603F0`, `00360480` | in over 8 frames |

The field transition `00314440` (also reached from `mapjump`) fades layer 2 out over 8 frames or at
once, black or white by its flags, after `002EFE50(0xFF)` (`003144C2`-`003144E5`).

### The cutscene skip

`skipexec` reaches `00360710`, which after its teardown calls, when `00267310` reports 0,
`002EFE40(6)`, `002EFE50(0xFF)` and `002EFA70(4, 0, 0, 0)` (`00360832`-`0036084F`): layer 4 goes to
black in zero frames, at priority 255 so it covers every other stage-6 effect. The skip itself is
on [cutscenes and the world lock](../Scripts-And-Script-Commands/cutscenes-and-the-world-lock.md).

### The movie fade schedule

`0037DDD0` runs at the end of the field frame. It reads the movie player's state (`00184860`, the
player object `01F81218` `+4`):

- In state 1 or 2 (opening, ready) it clears the two issued bits (`02ADEDC0` bits 3 and 4), stores
  the movie's end mark and elapsed frames, and selects row `id` of the table behind registry slot
  `02EBF008` (`+0x0C` the data, `+0x08` the stride) into `02ADED98`; with no table the row is null.
- In state 3 (playing) it updates the elapsed frames and calls `0037DEA0(02ADECD0)`.

The elapsed frames are the player's counter `+0x18` times 0.033366665 (`001B77B0`). The end mark
is its counter `+0x20` times the same, less 30, or less 8 for movie id 43 (`001B77E0`).
`0037DEA0` issues each fade once, both on layer 0 after `002EFE40(5)`, so movie fades draw in stage 5:

```
fade-in : when bit 3 clear, inLength != 0 and elapsed >= inStart:
          002EFA70(0, inLength - elapsed + inStart, 1, flags & 1); set bit 3
fade-out: when bit 4 clear, outLength != 0 and elapsed >= end - outLength - outLead:
          002EFA70(0, end - outLead - elapsed, 0, (flags & 2) != 0); set bit 4
```

A late first check shortens the fade by the frames already passed, so the fade still ends on time.

### The effect fade

`efffadein(n)` (`0x0268`, `00354670`) and `efffadeout(n)` (`0x0269`, `00354090`) play the effect
that entry `n` of the table at `01EF9400` names, through `0036E750(0, 0, params, n, 9)` and
`003B02A0`. Both first release the handle held at `022BDEB8`. `efffadein` (`002EFD80`) keeps no
handle, so its effect runs to its own end; `efffadeout` (`002EFDC0`) keeps the handle, so its effect
holds until `efffadecancel` (`0x02A6`, `002EFD50`) or the next effect fade releases it.

## Layouts

FadeLayer[7] at `022BDD60`, stride `0x30`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | handle | class-8 screen-effect handle, 0 when free |
| `04` | `u8` | state | 0 free, 1 running, 2 finished |
| `05` | `u8` | direction | 0 out, 1 in |
| `08` | `...` | descriptor | `0x28` bytes, below |

```
Kind-1 descriptor (record +0x08; pool record +0x00)
+0x00  u8    kind        1
+0x01  u8    stage/blend  low nibble stage (default 6), high nibble blend (default 3)
+0x02  u8    class       1
+0x03  u8    priority    default 0
+0x1C  u8    flags       bit 0 fade-in
+0x20  u32   colour      RGBA bytes, alpha 0x80 full
+0x24  u32   duration    2 x frames
pool record only:
+0x68  u32   handle
+0x6C  u32   counter
```

The pool copies 0x68 bytes, more than the 0x28 a fade record has; the bytes past `+0x28` come
from the next layer's record and the kind-1 code reads none of them.

Movie fade row (registry slot `02EBF008`, stride 8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | id | equals the row index |
| `01` | `u8` | inStart | frame the fade-in starts |
| `02` | `u8` | inLength | fade-in frames, 0 for none |
| `03` | `u8` | outLead | frames between the fade-out's end and the end mark |
| `04` | `u8` | outLength | fade-out frames, 0 for none |
| `05` | `u8` | unused | 0 in every row |
| `06` | `u8` | unused | 0 in every row |
| `07` | `u8` | flags | bit 0 white fade-in, bit 1 white fade-out |

## Shipped data

The schedule is `battle_pack.bin` directory entry `+0x118`, an `st2e` section whose header
declares 49 rows of 8 bytes; each row's id is a movie code of path kind `0x1C` (`01ECB4D0`, entry
`2 × id`), the name the player opens as `<code>.webm`. The per-row listing is
`screen-fades-movie-fade-schedule-names.tsv` beside this page.

| Fact | Value |
|---|---|
| section | `us` copy at `0x443E8`-`0x44598`, 432 bytes; identical in all nine language copies |
| rows | 49; 32 fade in, 37 fade out, 11 do neither (ids 0, 32, 37-41, 44-47) |
| commonest row | in at frame 30 over 30, out over 60 ending 60 before the end mark: 11 rows |
| fade-in starts | frame 30 in 20 rows, frame 0 in 12 |
| fade-in lengths | 30 frames 26, 15 frames 2, 60 frames 2, 10 and 6 frames 1 each |
| fade-out lengths | 60 frames 20, 30 frames 10, 15 frames 4, 90, 150 and 6 frames 1 each |
| fade-out leads | 60 frames 31, 0 frames 5, 205 frames 1 |
| white fade-in | ids 17, 19, 21, 26, 35, 43 |
| white fade-out | ids 26, 35, 43 (always with a white fade-in) |
| id 25, `EPL` | in over 15 from frame 30; out over 150 ending 205 before the end mark |
| id 43, `IVT` | 6-frame white fade-in at frame 0, 6-frame white fade-out at the end mark |
| movies | 40 `.webm` files; ids 38, 39, 40, 46 have no path, ids 37, 41, 44, 45, 47 have no `.webm` |

Every row whose movie is missing is all zero; ids 0 (`OPN`) and 32 (`WAR`) ship and take no
scheduled fade.

In the decompiled `us` scripts (1,114 files), counting every call:

| Fact | Value |
|---|---|
| `fadeout` | 4,391 calls in 818 scripts |
| `fadeout_d0` | 5,168 calls in 920 scripts |
| `fadein` | 4,621 calls in 712 scripts |
| `fadein_d2` | 1,698 calls in 391 scripts |
| `whiteout` / `whiteout_d1` | 221 in 158 / 408 in 202 |
| `efffadein` / `efffadeout` | 42 in 41 (`n` 5 or 10) / 28 in 28 (`n` 6) |
| `fadetrans`, `efffadecancel` | no calls |

## Modding notes

- A fade-out stays on screen until a fade-in on the same layer; leaving one out of a script leaves
  the screen black. `mapjump` frees all seven layers.
- Fade lengths are thirtieths of a second at both frame rates.
- A movie's fades are its schedule row; edit `inStart`, `inLength`, `outLead` and `outLength` there.
  Rows are matched by position; byte `+0` is the row index and the code ignores it.
- Use `fadetrans` before a fade to change its blend; values above 7 index past the blend table.
- Draw order between overlapping fades follows the stage and priority, not the layer number.

## Related

- [Script screen effects](script-screen-effects.md): the cut-in, motion blur, soft focus and
  screen blur effects that share the descriptor pool.
- [Movies](movies.md): the movie files the schedule's ids name.
- [Cutscenes and the world lock](../Scripts-And-Script-Commands/cutscenes-and-the-world-lock.md):
  the movie verbs, the player states and `skipexec`.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the fade verbs.
- [Frame update order](../Engine-Core/frame-update-order.md): where the pool tick, the
  schedule and the draw stages run.
- [Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md): the map prefetch a
  finished fade-in runs.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): FrameLimit and the time base.
