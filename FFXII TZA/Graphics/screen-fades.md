---
title: "Screen fades: the seven fade layers, the fade verbs and the per-movie fade schedule"
kind: "system"
category: "Graphics"
addresses: "0x022BDD60, 0x002EFA70, 0x002EF910, 0x00375900, 0x00375A20, 0x00375AE0, 0x00375470, 0x00374950, 0x00375500, 0x003740B0, 0x01EFAC20, 0x002EFE10, 0x002EFE40, 0x002EFE50, 0x002EFE60, 0x0037DDD0, 0x0037DEA0, 0x02EBF008, 0x00360710, 0x002EFD80, 0x002EFDC0"
---

## What the player sees

The screen going to black or white between areas, around a cutscene and around a pre-rendered
movie, and coming back. A fade to the colour stays on screen until something fades back in. A
skipped cutscene cuts to black at once. Every pre-rendered movie that ships with a schedule row
opens and closes with its own authored fade, some of them to white.

## How it works

### The seven fade layers

There are seven fade records of 0x30 bytes at `0x022BDD60`, one per layer 0 to 6. Every accessor
clamps the layer into 0..6 (for example `0x002EFA90`). A record holds the handle of the screen effect
that draws it, a state (0 free, 1 running, 2 finished), the direction and a 0x28-byte effect
descriptor (see Layouts). Layers are independent: fades on different layers run and draw at the
same time.

### Starting a fade

`0x002EFA70(layer, frames, direction, white)` starts every fade. Direction 0 fades out, to the
colour; direction 1 fades in, back to the scene.

1. It keeps the old descriptor's colour and bytes `+1` and `+3`, then clears the descriptor.
2. A running or finished record releases its old effect through `0x0024CFF0` and is freed.
3. It picks the colour (next section), stores the direction in record `+0x05`, and builds the
   descriptor: kind 1, stage `0x022BDEB4` in the low nibble of `+1`, blend `0x022BDD5D` in the high
   nibble, class 1 in `+2`, priority `0x022BDEB0` in `+3`, bit `0x1` of `+0x1C` set for a fade-in, and
   the duration `2 × frames` at `+0x24` (`0x002EFAF3`).
4. `0x00375900` files the descriptor and returns its handle; `0x003B0F80(handle, 1)` registers it, and
   a non-zero handle marks the record running (`0x002EFCE7`).
5. It resets the three selectors: blend 3, priority 0, stage 6 (`0x002EFCF4`-`0x002EFD05`).

`0x002EFE40(stage)`, `0x002EFE50(priority)` and `0x002EFE60(blend)` set the selectors for the next start
only. `0x002EFA20` resets them with all seven handles and the one-shot colour.

### The colour

In order (`0x002EFBD5`-`0x002EFC6F`):

- When the one-shot byte `0x022BDD5C` is set, the four bytes `0x022BDD58`-`0x022BDD5B` are the colour and
  the byte is cleared. `0x002EFE10(r, g, b, a)` arms it.
- Otherwise a fade-in on a layer that was running or finished keeps the previous colour, and also
  takes the previous fade's stage, blend and priority.
- Otherwise the colour is `0x80000000` (black) or, with `white` = 1, `0x80FFFFFF` (white). Alpha
  `0x80` is full strength.

### The screen-effect descriptor pool

Fades are one kind of screen effect. The pool holds 32 records of 0x70 bytes at `0x02EBF9E0`: the
0x68-byte descriptor, the handle at `+0x68` and an elapsed counter at `+0x6C`.

- `0x00375900(descriptor)` returns 0 when all 32 hold a handle. Otherwise `0x00375A20(stage, priority)`
  finds the insertion point, before the first record of a higher stage or of the same stage and a
  higher priority, and moves the later records down one slot. The handle is
  `0x80000000 | (++counter & 0x0FFFFFFF)` (counter `0x02EC07E8`), the counter starts at 0, and 0x68
  bytes are copied from the descriptor (`0x003759C9`-`0x00375A01`).
- The filed record's elapsed counter `+0x6C` starts at 0 (`0x003759C2`). After the copy `0x00375900`
  clears bit `0x1` of `+0x10` (`0x00375A06`), so the tick and the draw take the record, and writes
  `[rsp + 4] - 0xD` over the qword `+0x08`, with `rsp` as at its entry (`0x0037590A`-`0x00375912`,
  `0x00375A0A`). It returns the handle (`0x00375A0E`).
- The pool is kept packed and in draw order. `0x00375470(handle)` removes a record by moving every
  later record up one slot and clearing the last handle. It walks the records up to the first free
  one (`0x00375490`-`0x003754A3`), and a handle it does not meet there leaves the pool as it is.
- A handle's top nibble is its class; class 8 is this pool. `0x0024DE70` (state) and `0x0024CFF0`
  (release) dispatch on it and reach `0x00375AE0` and `0x00375470`.

- `0x00374930` clears the handle `+0x68` of all 32 records, which empties the pool. It runs when
  effect group 8 is emptied (`0x0024C550(8)`).

`0x00375500(stage)` draws, in pool order, every record of that stage whose class byte is enabled in
`0x02EC07E0` and whose `+0x10` bit `0x1` is clear; kind 1 goes to `0x003740B0`. The frame bodies call it
for stages 2, 3, 5 and 6 in the scene draw `0x0022B0B0` and stage 7 after `0x00376470`, so the stage,
then the priority, sets the order in which fades and other screen effects cover each other.

The draw runs between `0x00862C10(1, stage)` (`0x00375523`) and a tail jump to `0x00862C30` (`0x00375671`),
and calls `0x0039D570(0)` and `0x0039D3F0` before the walk (`0x00375539`, `0x0037553E`). It waits on bit
`0x100` of `0x02EAF6D8` before the walk, before each record and after the walk (`0x00375535`, `0x003755B2`,
`0x00375655`); that word is 0, so each wait falls through. The walk stops at the first record with no
handle (`0x0037556E`).

Its jump table at `0x00375678` sends kinds 2 to 7 to `0x003745C0`, `0x003749F0`, `0x00375B90`, `0x00375D90`,
`0x00374280` and `0x00374E30`, and kinds `0x0B` to `0x0D` to `0x00376220`, `0x00376050` and `0x00375280`; kind
0, kinds 8 to `0x0A` and kinds above `0x0D` draw nothing (`0x003755B4`-`0x003755CB`). A record whose
handler returns 0 is removed (`0x00375470`, `0x00375636`), and the walk takes the next record from the
same slot (`0x0037563B`). The draw does not test the result of `0x003740B0` (`0x003755D5`).

The kind `0x0C` draw `0x00376050` points `r14` at record `+0x30` only when byte `+0x1E` is 2, 3 or 4
(`0x003760A9`-`0x003760DC`); for any other value `r14` stays 0 and the word read at `0x003760F5` would come from
address 0. No kind `0x0C` record holds another value. A record gets its bytes only from the descriptor that
`0x00375900` copies into it (`0x003759CC`-`0x00375A01`). `0x00375A20`, `0x00375470` and `0x00375F80` move whole records,
and the pool's other stores touch bit `0x1` of `+0x10`, the qword `+0x08`, the handle `+0x68` and the counter
`+0x6C`; the draw handlers write their own packets, not the record.

Of the 47 calls to `0x00375900`, one files kind `0x0C`. `0x0024B7B0`, which the per-frame driver `0x0024D540` calls
(`0x0024D6C4`) and which acts only in draw 0 with bit `0x40` of `0x020926E4` set (`0x0024B7CD`-`0x0024B7DC`), builds
it with kind `0x0C` (`0x0024B92A`), the word `0x200` at `+0x1D`, which makes `+0x1D` 0 and `+0x1E` 2
(`0x0024B936`), `+0x1F` = 1 (`0x0024B93C`) and the qword `0x1C00` at `+0x30` (`0x0024B90D`-`0x0024B918`,
`0x0024B940`), and files it at `0x0024B949`.

The other calls store kinds 1 to 7, `0x0B` and `0x0D`, and the blur descriptors that `0x003DDF90` files from
`0x02B58A90` get kind stores of 2 only (`0x003DDCC9`, `0x003DDD6A`, `0x003DE01C`). So in the draw that matches
`+0x1D` (`0x0037609A`), `0x00376050` always reads the word `+0x30` (`0x003760D4`, `0x003760DC`), `0x1C00`. With
`+0x1F` = 1 it then returns 0 at `0x00376139`, after `0x002D7FA0(0x1C00)` and `0x00182AD0`, without a capture, and
the draw removes the record (`0x00375636`).

The class enables are bytes at `0x02EC07E0`, just past the pool, indexed by the record's class byte `+2`. The reset
`0x00375120` (called from `0x00259180` at `0x002591CD`) sets classes 0 to 3 to 1 with one 4-byte store (`0x0037514F`) and
classes 4 and 5 with one 2-byte store at `0x02EC07E4` (`0x0037515C`). Three walks of the pool test the byte of each
live record's class: the pool tick `0x00374950` (`0x0037497A`), `0x00374FD0` (`0x0037502B`) and the draw `0x00375500`
(`0x00375578`), each as `[0x02EBF9E0 + 0xE00 + class]`.

### Drawing a fade

`0x003740B0` draws one full-screen quad (corners at ±1.0) in the descriptor's colour with alpha
`colourAlpha × f`, where `f = counter / duration` clamped to 0..1, and `1 − f` for a fade-in. With a
duration of 0 or a counter past it, a fade-out draws the full colour and a fade-in draws nothing.

The alpha `colourAlpha × f` is truncated to an integer (`0x00374186`). The full colour is the dword
`+0x20` (`0x00374121`); the fade-in past its duration draws its quad with all four colour bytes 0
(`0x00374196`), which leaves the screen as it is under blends 0 to 5 of the table below. At a counter
of 0 a fade-in draws the full colour and a fade-out the four zero bytes (`0x00374117`-`0x0037411F`).

It returns without drawing in two cases. One is the first test of `0x00374060` (below, `0x00374069`-`0x0037408D`),
made again here: `0x00254A70` returns 0, bit `0x800` of `0x020926E4` is set and the record's handle is not
`0x002EF9F0(3)`, layer 3's (`0x003740B9`-`0x003740DD`). The other is bit `0x10` of draw 1's pass mask set (`0x003583F0(1)`,
`0x003740E8`) while the draw byte `0x022C7F98` is 0 (`0x00358320`, `0x003740F1`).

It writes the four corners, the colour as four floats (`+0x40`-`+0x4C`) and the blend word (`+0x50`)
into the buffer `0x00863B40` returns, and submits it with `0x00863B90(2)` and `0x0039D3F0`
(`0x0037419A`-`0x00374266`).
The blend is entry `blend` of eight 8-byte words at `0x01EFAC20`, read as the PS2 GS `ALPHA`
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

The pool tick `0x00374950` (run by `0x00258D70` in the field frame's simulation step, and by the menu
frames `0x0022B8C0` and `0x0022BC20`) adds to the counter of every enabled record: 2 on its first tick,
and 2 per tick while `0x001EDDA0` reports the 30 fps time base, else 1. The duration is twice the
frame count, so a fade lasts `frames` thirtieths of a second at either frame rate. A record whose
`+0x10` bit `0x1` is set is passed over like a disabled one, and the walk stops at the first record
with no handle (`0x00374970`-`0x00374988`).

The state query `0x00375AE0` answers 3 for a kind-1
record while the counter is below the duration and 5 once it reaches it. It answers 3 for kinds 2,
3, 5, 6 and `0x0D` and 0 for kind 0 (jump table `0x00375B3C`). For the other kinds it goes on to the
later records, and it answers 0 when no record holds the handle (`0x00375B0F`-`0x00375B1A`).

The tick also asks `0x00374060(record)` about every kind-1 record it counted and removes the record
(`0x00375470`) when it answers 0, then takes the next record from the same slot (`0x003749C1`).
It answers 1 while byte `+0xDEF` of `[0x0209AC30]` is 0 (`0x00254A70`),
bit `0x800` of `0x020926E4` is set and the record is not layer 3's, whose handle `0x002EF9F0(3)`
returns (`0x002EF9F0(layer)` reads a fade record's first dword, the layer clamped into 0..6).
Otherwise it answers 0 once the record has `+0x1C` bit `0x2` set and its counter `+0x6C` above
`+0x24`, and 1 before that.

`0x0022A040` answers 1 when a fade layer other than 3 is running (`0x002EFD20(layer)` = 1 for one of
layers 0–2 and 4–6). The render thread's block `0x19` arm `0x006234A0` asks it.

### The per-tick poll

`0x002EF910`, from the world tick `0x00314020`, asks for the state of every layer with a handle
(`0x0024DE70`):

- 3: the record is running; its state byte `+0x04` is set to 1 (`0x002EF9BC`).
- 5, fade-out: the record becomes finished, state 2 (`0x002EF977`), and its effect stays in the pool,
  so the screen stays black or white.
- 5, fade-in: the effect is released and the record freed. For layers 0, 2, 4, 5 and 6
  (`bt 0x75`, `0x002EF9AF`) it then calls `0x001D6C80`, which runs the map prefetch step `0x001DA290`
  ([prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md)).
- Any other answer leaves the record as it is (`0x002EF96F`).

`0x002EF840(layer)` frees one layer and `0x002EF890()` all seven; the `mapjump` verb (`0x008D`, poll
`0x00355350`) calls `0x002EF890`.

### The script verbs

| Verb | Id | Handler | Start |
|---|---|---|---|
| `fadeout(frames)` | `0x00B6` | `0x00356650` | `0x002EFA70(0, frames, 0, 0)` |
| `whiteout(frames)` | `0x00B7` | `0x00356FE0` | `0x002EFA70(0, frames, 0, 1)` |
| `fadein(frames)` | `0x00B8` | `0x00355EB0` | `0x002EFA70(0, frames, 1, 0)` |
| `fadeout_d0(layer, frames)` | `0x00D0` | `0x00356270` | `0x002EFA70(layer, frames, 0, 0)` |
| `whiteout_d1(layer, frames)` | `0x00D1` | `0x00356A50` | `0x002EFA70(layer, frames, 0, 1)` |
| `fadein_d2(layer, frames)` | `0x00D2` | `0x003559B0` | `0x002EFA70(layer, frames, 1, 0)` |
| `fadetrans(blend)` | `0x00BC` | `0x00340580` | `0x002EFE60(blend)` for the next start |

The one-argument forms push 0 under the popped frame count and pop it back as the layer, so they
always use layer 0. The two fade-in handlers first call `0x00183070` and `0x001D6C20`, which clears byte
`+0x88` of the prefetch manager, the cache backfill gate of
[file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md). A `fadein` after
a `whiteout` on the same layer fades back from white, because a fade-in keeps the colour.

### The engine's own fades

Read from the arguments at each call of `0x002EFA70`:

| Layer | Caller | Fade |
|---|---|---|
| 0 | `0x0037DEA0` | the movie schedule (below) |
| 0 | `0x0035CA70` | out over 30 frames (`0x0035CABB`), in over 30 (`0x0035CAE9`) |
| 0 | `0x00280140` | in over 1 frame |
| 2 | `0x00314530`, `0x003601D0` | out at once |
| 2 | `0x0025D9E0` | in over 8 frames |
| 2 | `0x00394130`, `0x003EFAA0` | out over 15 and 60 frames |
| 3 | `0x003145E0`, `0x003601D0`, `0x0027EFA0` | in at once |
| 3 | `0x003939B0` | out over its argument's frame count |
| 3 | `0x002CC960`, `0x002CC9C0` | in and out over lengths computed from their argument |
| 4 | `0x00360710` | the skip: out at once |
| 4 | `0x003603F0`, `0x00360480` | in over 8 frames |

The field transition `0x00314440` (also reached from `mapjump`) fades layer 2 out over 8 frames or at
once, black or white by its flags, after `0x002EFE50(0xFF)` (`0x003144C2`-`0x003144E5`).

### The cutscene skip

`skipexec` reaches `0x00360710`, which after its teardown calls, when `0x00267310` reports 0,
`0x002EFE40(6)`, `0x002EFE50(0xFF)` and `0x002EFA70(4, 0, 0, 0)` (`0x00360832`-`0x0036084F`): layer 4 goes to
black in zero frames, at priority 255 so it covers every other stage-6 effect. The skip itself is
on [event scenes](../Scripts-And-Script-Commands/event-scenes.md).

### The movie fade schedule

`0x0037DDD0` runs at the end of the field frame. It reads the movie player's state (`0x00184860`, the
player object `0x01F81218` `+4`):

- In state 1 or 2 (opening, ready) it clears the two issued bits (`0x02ADEDC0` bits `0x8` and `0x10`), stores
  the movie's end mark and elapsed frames, and selects row `id` of the table behind registry slot
  `0x02EBF008` (`+0x0C` the data, `+0x08` the stride) into `0x02ADED98`; with no table the row is null.
- In state 3 (playing) it updates the elapsed frames and calls `0x0037DEA0(0x02ADECD0)`.

The elapsed frames are the player's counter `+0x18` times 0.033366665 (`0x001B77B0`). The end mark
is its counter `+0x20` times the same, less 30, or less 8 for movie id 43 (`0x001B77E0`).
`0x0037DEA0` issues each fade once, both on layer 0 after `0x002EFE40(5)`, so movie fades draw in stage 5:

```
fade-in : when bit 0x8 clear, inLength != 0 and elapsed >= inStart:
          0x002EFA70(0, inLength - elapsed + inStart, 1, flags & 1); set bit 0x8
fade-out: when bit 0x10 clear, outLength != 0 and elapsed >= end - outLength - outLead:
          0x002EFA70(0, end - outLead - elapsed, 0, (flags & 2) != 0); set bit 0x10
```

A late first check shortens the fade by the frames already passed, so the fade still ends on time.
With a null row `0x0037DEA0` returns at once (`0x0037DEB7`), so that movie gets no scheduled fade.

### The effect fade

`efffadein(n)` (`0x0268`, `0x00354670`) and `efffadeout(n)` (`0x0269`, `0x00354090`) play the effect
that entry `n` of the table at `0x01EF9400` names, through `0x0036E750(0, 0, params, n, 9)` and
`0x003B02A0`. Both first release the handle held at `0x022BDEB8`. `efffadein` (`0x002EFD80`) keeps no
handle, so its effect runs to its own end; `efffadeout` (`0x002EFDC0`) keeps the handle, so its effect
holds until `efffadecancel` (`0x02A6`, `0x002EFD50`) or the next effect fade releases it.

### The screen picture

The verb `0x5A3` (`0x0034EA10`) passes its argument (`0x00267E10`) to `0x00473E60(n)`, which first dismisses the
loading icon (`0x00183070`) and then runs `0x00182F10(n)` on the screen picture `[0x01F82CE0]` (`0x001D8D30`):

1. `0x001D8FC0` sets `+0x08` to `n x [0x01DFE0B4] + [+0x18] + [+0x14]` and the mode `+0x30` to 1, or 2 when `n` is 0;
2. `0x001D8F50` starts the picture when it holds one (`+0x28`): it logs `[ScreenImage]:playDPic`, sets `+0x00` to 1
   and either fades the level `+0x1C` in from 0 by `255 / [+0x14]` per step or, with no fade length, shows it at
   255 and sets `+0x10` to 2.

`0x00473E20()` reads the picture's `+0x10` (`0x00225680`) and answers 1 while it is 0 to 2, 2 when it is 3 and 0
for any other value. The poll `0x0034F570` of the verb `0x5A6` returns 1, which holds the script, while that
answer is 1.

## Layouts

FadeLayer[7] at `0x022BDD60`, stride `0x30`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | class-8 screen-effect handle, 0 when free |
| `+0x04` | `u8` | state | 0 free, 1 running, 2 finished |
| `+0x05` | `u8` | direction | 0 out, 1 in |
| `+0x08` | `...` | descriptor | `0x28` bytes, below |

Kind-1 descriptor (record `+0x08`; pool record `+0x00`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | kind | 1 |
| `+0x01` | `u8` | stage/blend | low nibble stage (default 6), high nibble blend (default 3) |
| `+0x02` | `u8` | class | 1 |
| `+0x03` | `u8` | priority | default 0 |
| `+0x04` | `u8[24]` | zero | zero for this kind (the start's qword clears); copied with the descriptor; in the pool record `0x00375900` then writes the qword `+0x08` (`0x00375A0A`) |
| `+0x1C` | `u8` | flags | bit `0x1` fade-in |
| `+0x1D` | `u8[3]` | zero | zero for this kind; copied with the descriptor |
| `+0x20` | `u32` | colour | RGBA bytes, alpha `0x80` full |
| `+0x24` | `u32` | duration | 2 x frames |

Pool record only:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x68` | `u32` | handle |  |
| `+0x6C` | `u32` | counter |  |

The pool copies 0x68 bytes from the record's `+0x08`, more than the 0x28 of its descriptor. The 0x40 bytes
past the descriptor are the next layer's whole record and the first 0x10 bytes of the one after; for
layers 5 and 6 they run past the array's end at `0x022BDEB0`, into the selectors `0x022BDEB0` and `0x022BDEB4`
and the handle `0x022BDEB8`. The kind-1 code reads none of them.

Movie fade row (registry slot `0x02EBF008`, stride 8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | id | equals the row index |
| `+0x01` | `u8` | inStart | frame the fade-in starts |
| `+0x02` | `u8` | inLength | fade-in frames, 0 for no fade-in |
| `+0x03` | `u8` | outLead | frames between the fade-out's end and the end mark |
| `+0x04` | `u8` | outLength | fade-out frames, 0 for no fade-out |
| `+0x05` | `u8` | unused | 0 in every row |
| `+0x06` | `u8` | unused | 0 in every row |
| `+0x07` | `u8` | flags | bit `0x1` white fade-in, bit `0x2` white fade-out |

## Shipped data

The schedule is `battle_pack.bin` directory entry `+0x118`, an `st2e` section whose header
declares 49 rows of 8 bytes; each row's id is a movie code of path kind `0x1C` (`0x01ECB4D0`, entry
`2 × id`), the name the player opens as `<code>.webm`. The per-row listing is
[`screen-fades-movie-fade-schedule-names.tsv`](screen-fades-movie-fade-schedule-names.tsv) beside this page.

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

Every row whose movie is missing has its seven fade bytes zero (its first byte is still the row's id); ids 0 (`OPN`) and 32 (`WAR`) ship and take no
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

### Columns of screen-fades-movie-fade-schedule-names.tsv

One row per schedule row, 49 rows; `id` is the row's index, equal to its byte `+0`, and `movie` the name
between the path's last `\` and its `.`.

| Column | Holds |
|---|---|
| `path_kind_0x1C_entry` | the string of path kind `0x1C` entry `2 × id` in the array at `0x01ECB4D0`; `NULL` for ids 38, 39, 40 and 46, whose entry is 0 |
| `webm_ships` | `yes` when `<movie>.webm` is in `gamedata/d3d11/artdata/video` (40 rows), `no` when it is not (9 rows: the four `NULL` ids and 37, 41, 44, 45, 47) |
| `row_bytes` | the row's 8 bytes from the `us` `battle_pack.bin` section, in hex, in the order of the layout above |
| `note` | `all-zero` when bytes `+1` to `+7` are all 0 (11 rows); empty otherwise |

## State

The movie fade schedule is the object at `0x02ADECD0`, which `0x0037DDD0` passes to `0x0037DEA0` (`0x0037DDF4`). Besides the
issued bits `+0xF0` (`0x02ADEDC0`) and the row `+0xC8` (`0x02ADED98`), it holds:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02ADECE4` | `u32` | 0 (zero-filled tail) | `+0x14`, the movie's elapsed frames: the player's counter `+0x18` times 0.033366665, truncated (`0x001B77B0`) | `0x0037DDD0`: 0, then the value, in states 1 and 2 (`0x0037DE22`, `0x0037DE3F`); the value in state 3 (`0x0037DDFB`) | `0x0037DEA0` (`0x0037DEDC`, `0x0037DF33`), through the object |
| `0x02ADED90` | `void*` | 0 | `+0xC0`, a pointer to `0x02ADEDC8`, so the end mark is read at its `+0x10` | `0x0037DDD0` (`0x0037DE28`) | `0x0037DEA0` (`0x0037DF27`) |
| `0x02ADEDD8` | `i32` | 0 | the movie's end mark: the player's counter `+0x20` times 0.033366665, less 30 (less 8 for movie id 43), truncated and raised to 0 when negative (`0x001B77E0`) | `0x0037DDD0`, in states 1 and 2 (`0x0037DE34`) | `0x0037DEA0` (`0x0037DF37`, through `+0xC0`) |

Both schedule tests in `0x0037DEA0` are unsigned: the fade-in fires once the elapsed frames are not below the row's
start byte `+0x01` (`0x0037DEDF`), and the fade-out once they are not below `end - outLength - outLead` (`0x0037DF44`), so a
difference below 0 compares as a large unsigned value.

`fadecolor(r, g, b, a)` (`0x00BA`, `0x00340080`) pops its four arguments and jumps to `0x002EFE10(r, g, b, a)`. That
stores them in the one-shot colour `0x022BDD58`-`0x022BDD5B` and sets `0x022BDD5C` (`0x002EFE10`-`0x002EFE2A`). The next
`0x002EFA70` copies the four bytes into the record's `+0x28`-`+0x2B`, the descriptor's colour `+0x20`, and
clears `0x022BDD5C` (`0x002EFBDE`-`0x002EFC0A`).

The pool's handle words lie `0x70` apart from `0x02EBFA48`, and the last record's is `0x02EC07D8`. Each walk of the
pool but the state query stops at the first record with no handle, so it reads this word only after the 31 records
before it. The state query `0x00375AE0` compares the handle of all 32 records (`0x00375AF5`-`0x00375B16`), so it reads
this word whenever no record before it matched with a kind that answers.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022BDD59` | `u8` | 0 (zero-filled tail of `.data`) | the one-shot colour's green | `0x002EFE10` (`0x002EFE1D`, from `fadecolor`'s second argument) | `0x002EFA70` (`0x002EFBE9`, into the record's `+0x29`, the descriptor's `+0x21`) |
| `0x022BDD5A` | `u8` | 0 (zero-filled tail of `.data`) | the one-shot colour's blue | `0x002EFE10` (`0x002EFE23`, from the third argument) | `0x002EFA70` (`0x002EFBF4`, into the record's `+0x2A`, the descriptor's `+0x22`) |
| `0x022BDD90` | `u32` | 0 (zero-filled tail of `.data`) | layer 1's handle `+0x00`, 0 when the layer is free; the next five rows are layers 2 to 6, each reached as `0x022BDD60` + layer × `0x30` | `0x002EFA20`, 0 (`0x002EFA2F`); `0x002EFA70` (`0x002EFCD7`, the handle `0x00375900` returns); 0 from `0x002EF840` (`0x002EF878`, one layer), `0x002EF890` (`0x002EF8DD`, all seven) and `0x002EF910` (`0x002EF9A2`, a finished fade-in) | `0x002EF840` (`0x002EF86D`); `0x002EF890` (`0x002EF8D0`); `0x002EF910` (`0x002EF95C`, `0x002EF995`); `0x002EF9F0` (`0x002EFA13`, which returns it); `0x002EFA70` (`0x002EFB4C`, `0x002EFCE1`) |
| `0x022BDDC0` | `u32` | 0 (zero-filled tail of `.data`) | layer 2's handle | `0x002EFA20`, 0 (`0x002EFA35`); the others as for `0x022BDD90` | as for `0x022BDD90` |
| `0x022BDDF0` | `u32` | 0 (zero-filled tail of `.data`) | layer 3's handle | `0x002EFA20`, 0 (`0x002EFA3B`); the others as for `0x022BDD90` | as for `0x022BDD90` |
| `0x022BDE20` | `u32` | 0 (zero-filled tail of `.data`) | layer 4's handle | `0x002EFA20`, 0 (`0x002EFA41`); the others as for `0x022BDD90` | as for `0x022BDD90` |
| `0x022BDE50` | `u32` | 0 (zero-filled tail of `.data`) | layer 5's handle | `0x002EFA20`, 0 (`0x002EFA47`); the others as for `0x022BDD90` | as for `0x022BDD90` |
| `0x022BDE80` | `u32` | 0 (zero-filled tail of `.data`) | layer 6's handle | `0x002EFA20`, 0 (`0x002EFA4D`); the others as for `0x022BDD90` | as for `0x022BDD90` |
| `0x02EC07D8` | `u32` | 0 (zero-filled tail of `.data`) | the handle `+0x68` of record 31, the pool's last; 0 when that record is free | 0 from `0x00374930` (`0x00374940`) and `0x00375120` (`0x00375133`), the loops over all 32; `0x00375900` (`0x003759BB`, the new handle when the record goes in last); `0x00375A20` (`0x00375AC3`, record 30 moved down to make room); 0 from `0x00375470` (`0x003754E2`) and `0x00375F80` (`0x00376020`) after a removal | `0x00375900` (`0x00375937`); `0x00374950` (`0x00374970`, `0x003749B9`); `0x00374FD0` (`0x0037501A`); `0x00375500` (`0x0037556A`, `0x00375633`); `0x00375AE0` (`0x00375AF5`); `0x00375470` (`0x00375490`; the move at `0x003754DF`); `0x00375F80` (`0x00375FE0`; the move at `0x0037601D`) |

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
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md):
  the movie verbs, the player states and `skipexec`.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the fade verbs.
- [Frame update order](../Engine-Core/frame-update-order.md): where the pool tick, the
  schedule and the draw stages run.
- [Prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md): the map prefetch a
  finished fade-in runs.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): FrameLimit and the time base.
