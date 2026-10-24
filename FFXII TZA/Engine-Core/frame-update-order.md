---
title: "Frame update order: what runs each frame for the field, the battle layer and every unit"
kind: "system"
category: "Engine core"
addresses: "0x0022A490, 0x0022A580, 0x00229F00, 0x00229EA0, 0x0022B6E0, 0x0022B7E0, 0x0022A770, 0x0022B8C0, 0x0022AF50, 0x0022BC20, 0x0022B000, 0x0035EB70, 0x0035EC80, 0x00314020, 0x0025BFB0, 0x0032FC30, 0x00267310, 0x00234590, 0x0025D9E0, 0x00234520, 0x003DB1F0, 0x002623A0, 0x002EEEB0, 0x00233F70, 0x001EBA40, 0x0022BEB0, 0x00332590, 0x0037C2E0, 0x0035E7A0, 0x00265A20, 0x00267240, 0x002671C0, 0x00300FC0, 0x002341C0, 0x0023B020, 0x00238A60, 0x00238AE0, 0x00238B00, 0x00238B20, 0x00238B70, 0x0032A200, 0x0050F2E0, 0x0050F170, 0x0050F380, 0x002E09A0, 0x002E2240, 0x0035E6F0, 0x00360080, 0x0035E9F0, 0x0035E9B0, 0x00358510, 0x00358280, 0x003586A0, 0x00358550, 0x00229ED0, 0x00233700, 0x00233640, 0x002335D0, 0x0023B200, 0x0026A5B0, 0x00360710, 0x00360A50, 0x002342F0, 0x002368D0, 0x0032A170, 0x00308610, 0x003590D0, 0x0031B770, 0x0026B730, 0x0036F460, 0x0027E9E0, 0x002507C0, 0x0022BFB0, 0x00307FF0, 0x00322190, 0x0030C3F0, 0x00229E00, 0x00229DF0, 0x00250130, 0x002501A0, 0x00250200, 0x00250180, 0x00250540, 0x020927DC, 0x0022B0B0, 0x00183030"
---

## What the player sees

Every frame the pad is read, the world is simulated a whole number of steps, the camera follows,
sound is mixed, the picture is drawn and the loop waits for the next tick. In ordinary field play every frame runs
exactly one step, at 30 and at 60 frames per second alike; at 60 the frame waits one tick instead of two.

A frame in
which the world does not move comes from special paths only: the frame after the step budget is cleared, a script that
slows the game, and a few frames of particular cutscenes at 60 frames per second, which are skipped or run twice to keep
their timing. The camera still moves on such a frame. At 60 frames per second some subsystems run only on alternate
frames.

The high-speed mode
doubles or quadruples the number of steps a frame earns, but only after a step in which nothing
held it back: a menu, a load, a cutscene or a dialog drops it to normal speed. Behind the full menu only
the cutscene managers tick; the field, the battle and every unit stand still until the menu
closes. A script skip runs the cutscene slots up to sixteen times a frame.

At double and quadruple speed a frame runs two or four world steps, but the two map buttons, Map
Transparency and Display Map, still act once per frame: the press is taken on the frame's first step
and ignored on the others (Display Map is read on every step while the location map is open), so a press is
not counted two or four times. The water in the fields follows the chosen speed, not the game's own pace: it
flows two or four times as fast, and keeps that pace while the game itself is held at normal speed without
leaving the speed mode.

## How it works

### The main state machine

The application's pump calls `0x0022A490(dt, flag)` once per pass ([game
application](game-application.md)): it stores the flag at `0x02064AA0`, runs `0x0022A580`, and
increments `0x02064AD0` when that returns non-zero. `0x0022A580` first checks `0x00184AD0()` (a load in
progress returns 1 after `0x0020E4E0()`), counts `0x01FD4A80`, runs `0x00183100`, `0x001829A0`,
`0x00358640`, `0x001EC490`, `0x00214C30`, `0x00183100` again, `0x00182810` once when `0x01FD49E0` was set,
`0x001831C0` and `0x00183090`, then sets `0x01FD4A68` from the state and dispatches on the state byte
`0x02064AD3`:

| State | Handler | What it is |
|---|---|---|
| 0 | `0x0022B6E0` | start-up: after `0x0032E520(1)` reports no load pending and `0x0209273C` is 5 it moves to state 1 and runs the first-screen set-up (`0x0035EA30(0)`, `0x0053DD10(0x1C)`, `0x00236A40`, `0x00253A10`, `0x002EF650` (the new-game payload reset `0x002EF2D0` and the save-image binding `0x00253A80`, [save data fields](../Saving-Loading-And-Settings/save-data-fields.md)), `0x003318C0`, `0x0037CB30`) |
| 1 | `0x0022B7E0` | title and loading: moves to state 2 when `0x0032E520(1)` and `0x0037C2E0()` are both 0, then `0x00184960(2)` |
| 2 | `0x0022A770` | the field frame (below); the default for any other value |
| 3 | `0x0022B8C0` | the full menu frame: pad, UI effects, `0x00314020(1)` under its `ATEL CONTROL` label, sound, the menu's own update; when `0x002E05C0()` is 0 it closes (`CLOSE FULLMENU`): `0x00263560`, state 2, `0x00182D40`, `0x002E1BA0`, `0x0024F980(0)`, four `0x002E1CA0(7)`, `0x0037CF00`, `0x003323D0`, `0x00332660`, `0x003323B0`, `0x00376BE0`, `0x00226280` |
| 4 | `0x0022AF50` | the screen capture before a menu (`SCREEN CAPTURE`, `0x0022B0B0(0, 1)`); moves to state 3 |
| 5 | `0x0022BC20` | the capture-backed frame: `0x00314020(1)` under `ATEL CONTROL`, then unless still 5 it returns to state 2 with `0x00263560`, `0x00376BE0`, `0x00226280`, `0x00375EC0` and `0x00360120` |
| 6 | `0x0022B000` | a second capture; moves to state 5 |

States 4 and 6 are entered through the setter `0x00229F00` (called from the request drain `0x002E09A0`
and from `0x002E2240`); `0x00229EA0` is the getter. `0x01FD4A68` is 1 in states 4 and 6 and 0 otherwise;
`0x01FD4A84` is 1 in states 2, 3 and 5, and in those three states `0x0035E6F0`, `0x00360080`, `0x0035E9F0`
and `0x0035E9B0(-16.0)` run before the dispatch; `0x02064AD8` toggles in every state but 4 and 6;
states 4 and 6 call `0x001E0580` first.

`0x0022BFB0(v)`, the handler of verb `0x05CA` (through `0x00340B70`), sets `0x01FD49E0` and stores `v` at
`0x01FD49E4`; on the next pass `0x0022A580` calls `0x00182810(v)` (`0x0022A5E3`) and clears the request.
`0x00182810` writes `v != 0` to byte `+0x1E9` of the post-process parameter object (`0x00193D50`,
`0x00193F70`).

State 1's gate `0x0037C2E0` walks the entries of the table `[0x02EBF0A8]` (`0x003204B0` the count,
`0x00320B30` an entry) and resolves each to a record (`0x002EAE20`) at `0x02ADD948`. A record with bit
`0x4` of `+0x19` set (`0x002E4C70` returns 0) goes to `0x002EAF70`. Any other holds the gate (it returns
1 and resumes there next frame) until bit `0x2` of its `+0x18` is set (`0x002E4C20`), and then gets bit
`0x2` of `+0x19` (`0x002EBE20(record, 1)`). The gate returns 0 once every entry is through.

After the handler, with `0x01FD4A84` set and `0x00184950()` = 2, `0x0035E9F0` and `0x0035E9B0(17.0)` run;
`0x001E0560` arms the pump's second pass when `0x01F82D31` was set; with `0x01FD4A68` clear,
`0x02F974A0` clear and no second pass armed, `0x001832F0()` runs, then `0x00375B80(0)`; and a callback
pending at `0x02064AEC` is called and cleared.

### The menu frame and the monster viewer

The full menu frame `0x0022B8C0` (state 3) runs a few steps that only matter for the Bestiary's
monster viewer, the object at `0x01F82E18` (`0x001EBA40`, `0x2E0` bytes, constructor `0x001EB190`;
[Clan Primer](../Menus-And-HUD/clan-primer.md)). `0x00181DD0` reads its byte `+0x118`, set while a monster is
shown:

1. without a monster shown it starts with `0x00182370` (`0x00186110` on the render manager);
2. after the pad and the UI effects, with `0x02064AA0` at 0, `0x00258EB0` pushes arena 2 (`0x0036C1D0`),
   runs `0x0024B9B0(0, 4)` and pops it (`0x0036C140`), and `0x00374950` follows;
3. it installs `0x0022BEB0` as the menu draw callback (`0x002D0570` stores it at `0x0209E630`);
4. after `OTHER`, with a monster shown, `0x00181B20` posts a `CopyBufferObj` (`0x0018B8B0`,
   `0x001F1810`) between the first entry of `0x00186910(render manager, 0)` (null when that entry's byte `+8`
   is set) and the viewer's `+0x278`; `0x00181E50` then steps the viewer's fade at `+0x20` (`0x001EC000`);
5. with a monster shown it sets `0x02064AE8` and runs `0x003323D0`, `0x00314370(0)` and `0x0036F510`, and
   when `0x00181DB0()` is 0 and `0x00358340()` holds, `0x00258E40`; `0x00181DB0` is `0x001EB990`, which holds
   while the viewer's byte `+0x26D` or `+0x26E` is set. Without a monster, a set `0x02064AE8` is
   cleared and `0x00314370(1)` and `0x0036F510` run.

The draw callback `0x0022BEB0` brackets the frame's own draws with `0x001FBE50` and `0x001FBD80(1)`.
With a monster shown it posts the same copy for the viewer's `+0x270` (`0x00181AB0`) and, when
`0x002EF030()` is 1, interleaves `0x00258EE0(1)` to `0x00258EE0(5)` and `0x00375500(2)` / `(3)`, each behind
`0x003583F0(0)` or `0x00358350(0)`, with the viewer's turn `0x00184690` (`0x001EC060`).

It starts the viewer's 80-frame fade (`0x00181C10`, `0x001EBCF0`:
halved when `0x001EDE70()` is 0, from 200 down by 200 / frames) once `0x00181C70()` (`+0x284`) is 0,
and steps that fade, the one at `+0x00`, with `0x00181E30` (`0x001EBF90`). Both fades draw through `0x001EB800`.

The two capture states share their tail. `0x0022AF50` (state 4) and `0x0022B000` (state 6) both run
`0x00332590`, which points `0x022C6F20` at `0x022C6F30`, runs `0x0041E500` and `0x00426950`, and clears
arena 6's byte `+0x62` in the table at `0x022D7FD0` when bit `0x40` of `0x022D89B8` is set (`0x003697C0(6)`).
They also run `0x00376D80`, which for each of the eight records at `0x02ADBB40` (stride `0x90`) with
a non-zero first word sets bit `0x8` of `+0x54` and copies `+0x08`, `+0x10`, `+0x18` and `+0x20` into
the word after each.

State 6 also runs `0x00375F20`, which sets bit `0x1` of the first word of the
records at `0x02EBF9F0` (stride `0x70`) up to the first whose `+0x58` is 0.

### The field frame

`0x0022A770` is state 2. After the pad (`0x0036F2F0`, `0x0035FF90`, `0x0036FDF0`, `0x002498B0`, which rebuilds the pad words at `0x02F97360`, [controls](../Controls-And-Input/controls.md)) and the
draw set-up it runs, when `0x0017E4E0()` is 0, `0x001EC760()` passes of the following; each pass ends
in the camera, the end-of-frame list and the pacer. `0x001EC690` advances the counter `0x01F832C4`, which `0x001EC760`
among others reads: once when `0x001EC760` returns 0, and in the pass loop's first step. The event-slot
pusher `0x0020AF10` zeroes it (`0x0020AFAA`).

`0x001EC760` returns 1 at 30 fps (`0x01F82E38` clear, `0x001EC776`). At 60 fps it returns 0 or 2 at listed frames of
particular scenes, picked during an event (`0x001EC560`) by the cut-scene name (`0x001C50C0`), the scene word `0x01EF9218` or
story progress (`0x00265270`) and the frame counter `0x01F832C4`, and outside one by the values `0x0024DE30` reports; it
returns 1 otherwise.

Before the pad, once per `0x01E02824` with `0x00264610(0)` non-null, the deferred `0x0026B730(0x01E02808
& 0xFFFF)` runs. Each pass of the loop then:

- runs the speed-mode pad block (below);
- sets the speed factor `0x02064AC4` to 1.0 or, with the speed permit `0x02064AD2` set, the entry of
  the speed table `0x00908BA8` = {1.0, 2.0, 4.0} selected by the speed index `0x01FD4A98` (`0x00229E00` returns that entry,
  which is also the divisor of the pad gate below);
  `0x003603C0()` forces 1.0 and runs `0x002370A0`;
- keeps the accumulator `0x02064AC0` as it stands at `0x01E02820`; when the pump's flag `0x02064AA0` was
  set, sets the accumulator to 1.0 (if `0x01FD4A8C` was 1, which is then cleared) or 0, and clears
  the flag;
- with bit `0x8000000` of `0x00226B10(0)`, `0x0036F460(accumulator)`; with the `0x002878A0` predicate false and
  `0x0017DE60()`, `0x0027E9E0`; with the predicate true, `0x003583A0()` and the accumulator at 0,
  `0x002507C0(1)` ([subsystem update flags](subsystem-update-flags.md)).
- `0x0036F460` hands the map animation clock `0x004678E0`
  ([texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md)) the
  value `(acc - [0x02AD9B50]) * 30 / ([0x01DFE0B8] * 30)` for the accumulator `acc` (`0x0036F472`,
  `0x0036F4A1`-`0x0036F4B9`), and stores in `0x02AD9B50` `acc`, less 1.0 repeatedly while it is 1.0 or more
  (`0x0036F47A`-`0x0036F499`);
- `0x0036F460` ends with `0x00468520`, which runs `0x003CD820` on `+0x14` of each record of the table
  `[0x02CA6010]` (count `[0x02CA6020]`, stride `0x40`) whose `+4` is 0.

While the accumulator is at least 1.0, one simulation step runs:

1. `0x00250180(first)`; the tick `0x00314020(0, first)` when `0x001800E0()` is 0 and `0x001800C0()` is 0 or
   `0x001EC560()` is 0, else `0x002F1770(0, first)` with result 2;
2. `0x0037A450`, `0x0036D890`, `0x004668C0`; `0x003323D0` when `0x00358290()`; `0x002507C0(first)` when
   `0x003583A0()`; `0x00258B90(0)` when `0x00358340()`; `0x00314370(result)`; with the mode saved by
   `0x00358320`, `0x00358640(0)`, `0x0037D4C0`, `0x00314820`, `0x0036F510`, `0x00256F60`, `0x00358640(saved)`;
   `0x00258D70` when `0x00358340()`, and `0x001808D0` on the last step; `0x00254E50` (the per-tick game-over check, [game over](../World-Areas-And-Travel/game-over.md)); `0x0035AF20(0)`;
3. the accumulator loses 1.0 (floored at 0); a state other than 2 zeroes it and stops; otherwise
   `0x003586A0(1, 1)` when `0x002361A0()`, `(3, 1)` when `0x00265760()`, `(2, 1)` unless `0x00226BC0()`,
   `(4, 1)` unless `0x002F1A20()`;
4. `0x02064AD2 = 0x00358550()`, and when it is clear (after `0x0017F740(1)` when set) and `0x003583D0(0)`
   or `0x003583D0(1)` holds the accumulator is zeroed; `0x003603C0()` zeroes it too; `0x00358280` resets
   the permit byte; `0x02064AA8` counts the steps of this pass and is zeroed right after the loop,
   so it is non-zero only while a pass's steps run.

After the steps come three groups:

- the camera block, only on a pass in which no whole step ran (the accumulator carried; a flag
  set at the top of the pass is cleared after every step): `0x00358640(0)`, `0x004668C0`,
  `0x00258B90(1)`, `0x003143D0`, `0x00314370(1)`, `0x0037D4C0`, `0x00314820`, `0x0036F510`, `0x0035AF20(1)`,
  `0x00358640(saved)`, so the camera and the follow still advance on a carry frame;
- the end of the frame: `0x0035AE30` (the pad vibration output, [vibration](../Controls-And-Input/vibration.md)), `0x00360120` (the title-return gate, [game
  over](../World-Areas-And-Travel/game-over.md)), `0x00377520` and `0x0036F530` when `0x00358370()`, the
  accumulator gain, the controlled-character change `0x00358BC0`, `0x00226280`, `0x002E65A0`, `0x00332660`,
  `0x003323B0`, `0x00324510`, `0x0036F2C0`, `0x0032E040`, `0x0035E9A0(0x0022BFD0)`;
- the pacer `0x0035EC80([0x02064ACC], 0)` (an identical copy of `0x0035EB70`) ([startup constants](startup-constants.md)), then
  `0x0017F370(1)`, `0x00375B80(1)`, `0x00376470` and `0x00375500(7)` when `0x003583F0`, `0x0024B4F0`,
  `0x00374FD0`, `0x0037DDD0` and `0x00316930`, the end-of-frame achievement pass ([achievements](../Steam-And-Achievements/achievements.md)).

With `0x0017E4E0()` non-zero the frame runs `0x002506D0` and, when `0x001EC560()`, the camera block
(its `0x00314370(1)` and `0x0037D4C0` each only while `0x02064AA0` is 0) followed by `0x0035AE30`,
`0x00360120` and the `0x00358370()` pair, and nothing else.

At the end of every pass the accumulator gains `[0x02064AC8] × [0x02064AC4]` (`0x0022AE18`-`0x0022AE34`). The step gain
`0x02064AC8` is 1.0 at boot (`0x0022A1C8`) and after `0x002628B0` and `0x003601D0`; the verb `gameratio` (`0x14F`, `0x00343EE0`)
sets it to its float argument when that is at least 0.05. With the gain and the speed factor at 1.0 every pass runs one
step and leaves the accumulator at 1.0, so a pass runs no step only after the accumulator is zeroed (above), with a gain
below 1.0, or when `0x001EC760` returns 0; a speed factor of 2.0 or 4.0 runs two or four steps a pass.

At 60 fps, while the suppressor `0x01DFE0C0` is clear, the predicate `0x001EDE80` answers the frame parity `0x02064AD8` plus the
steps already run this pass instead of 1 (`0x001EDE9B`-`0x001EDEA7`), so its callers (`0x002507C0`, `0x0025DF00`, `0x0028E290`,
`0x0032E040`, `0x003E00C0`, `0x003FA790`, `0x00477480`) run on alternate frames; `0x00184960` sets the suppressor.

### The speed mode

- The permit byte `0x022C7F9A` is set to 1 at boot (`0x00358510`) and by `0x00358280` at the end of
  every step; during the step `0x003586A0(k, 1)` sets bit `0x2` when `0x002361A0()`, bit `0x8` when
  `0x00265760()`, bit `0x4` unless `0x00226BC0()` and bit `0x10` unless `0x002F1A20()`; `0x00358550()` is
  `byte == 0x1F`: every precondition held this step.
- The speed index `0x01FD4A98` (0 to 2) is written only by `0x00229ED0`: `0x00233700` on a press of pad
  bit `0x400` (0 to 1, or 0 to 2 when `0x002DDDA0()` is 1; any other value back to 0), `0x00233640` while
  held (through `0x002335D0`), and the resets `0x002370A0` (from `0x003603C0`), `0x00239790`, `0x00237DF0`,
  `0x00233C10` and `0x0023B2E0`.
- When `0x00233700` or `0x00233640` raises the index to 1 or 2 it also calls `0x00182FB0(index)`, as do
  `0x00239790` and `0x0023B2E0`. That runs `0x001D85C0` on the `ExtraUI` object `[0x01F82CD0]` (`0x001D8210`,
  built by `0x001D8150`): `+0x60` = 255.0, `+0x64` = 6.0, `+0x69` = 1, `+0x6C` = 1.5, and `+0x40` copied
  from `+0x58` for index 2, else from `+0x48`.
- The pad block at the top of each pass clears the latch `0x01FD4A74` when `0x00265760()` is 0 or
  `0x00226BC0()`, `0x002F1A20()` or `0x0028F6A0()` holds; otherwise, with `0x0017DEA0()` 0, bit `0x400` of
  `0x0036FF70()` and `0x0036FFD0()` sets the latch and runs `0x0023B200` (the edge through `0x0208E6B8`:
  `0x00233700` on a press, `0x00233640` while held), which keeps running every pass while the latch
  is set.

Three pad readers take a press on only some of a pass's steps while the speed permit is up. They are the field's
map controls ([map screens](../Menus-And-HUD/map-screens.md#opening-from-the-field)):

- `0x002501A0`, Map Transparency: bit `0x2` of the pressed word `0x02F97362`, called by the input arbiter at `0x00253E26`;
- `0x00250130`, Display Map: bit `0x1` of the filtered pressed word `0x02F97392`, called at `0x00253E7A` and by the
  location map `0x002BAF80` at `0x002BB9C7`;
- `0x00250200`, either of the two, called at `0x00253E07` and by the overlay page `0x002B7B80` at `0x002B8306`.

Each first asks `0x00229DF0`, which returns the permit byte `0x02064AD2`. With the permit up it truncates the entry
`0x00229E00` returns (`cvttss2si`), divides the step index `0x020927DC` by it (`cdq`, `idiv`) and, on a non-zero
remainder, skips that pad read (`0x00250130` and `0x002501A0` then answer 0, `0x00250200` goes on to its second half;
`0x00250146`-`0x0025015C`, `0x002501AD`-`0x002501C3`, `0x0025020D`-`0x00250221` and `0x0025023E`-`0x00250252`).

`0x00250130` and the
Display Map half of `0x00250200` read the pad without the gate while the location-map container `0x0209E5F0` exists
(`0x002B9FC0`, called at `0x0025013D` and `0x00250235`).

The step index numbers the steps of a pass. `0x00250180(first)` is the first call of every step (`0x0022ABB4`, its only
caller): it stores 0 when `first` is set and the old value plus one otherwise (`0x00250186`-`0x0025018F`). `first` is 1
on the pass's first step (`0x0022AA10`) and 0 after it (`0x0022ACA7`). The UI tick `0x00250540`, run by the full-menu and
capture-backed frames (`0x0022BA45`, `0x0022BD08`), stores 0 (`0x002505D0`). These are the only stores to `0x020927DC`;
its other loads are the gate's four (`0x0025014B`, `0x002501B2`, `0x00250212`, `0x00250243`).

A pass adds `0x02064AC8 × 0x02064AC4` to the accumulator (`0x0022AE18`-`0x0022AE34`) and runs a step for each whole 1.0
(`0x0022AB90`), so with the step gain at 1.0 and a factor of 2.0 or 4.0 it runs two or four steps, indices 0 to 1 or
0 to 3, and only index 0 divides: the press counts once per pass. The divisor is the table entry at the speed
index, not the factor `0x02064AC4`. An entry below 1.0 truncates to 0, and the `idiv` then raises a divide error; the
index the writers above store is 0 to 2, so the table's fourth entry, 0.0, is never the divisor.

The draw `0x0022B0B0` (from `0x0022A82D` and `0x0022A8B8` in the field frame, and from `0x0022AF50`) also reads the table at
the speed index (`0x0022B0F2`-`0x0022B103`) and passes the entry to `0x00183030`, which stores it at `+0x330` of the
map-art context `[0x01F81168]` (`0x00183041`).

`0x001AA2C0` multiplies the two water scroll steps by that value
(`0x001AA30D`, `0x001AA333`), the U and V scroll speeds `mDebugWaterUFactor` and `mDebugWaterVFactor` ([JSON configs](../Game-Files-And-Data-Tables/json-configs.md); [render command list](../Graphics/render-command-list.md)). The draw does
not read the permit, so the water keeps the chosen speed for as long as the speed index is raised.

The pacer `0x0035EB70(n, x)` (and its copy `0x0035EC80`), on the game thread, folds the frame time into `0x022CA5C4` and
`0x022CA5D8`, stores `max(n, 1)` ticks at `0x022CA5F4`, clears the tick counter `0x022CA5F0` and returns
its previous value; on any other thread it spins until the tick counter at `0x022CA5E0` has
advanced by `max(n, 1)`.

Between the fold and the reset (`0x022CA5C4` = 0) the pacer stores at `0x022CA5DC` the result of
`0x0035E7A0`, which adds `0x022CA5D0` to `0x022CA5C4` once more and measures that sum a against a period
L of 314, or 264 when `0x00290180()` is 2: it returns the distance from a up to the next multiple of
L, except that below L, outside frame mode 3 (`0x00229EA0`), it returns 2L - a.

### The ExtraUI overlay

The `ExtraUI` object `[0x01F82CD0]` (`0x90` bytes, built once by `0x001D8150`) draws two pictures through the sprite
batcher, each as a four-vertex quad on a screen of 1920 x 1080, or 512 x 448 when `0x001B1620` answers 0 or the
batcher's byte `+0x3A98` is set (`0x001D7110` and `0x001D70D0` return the width and height):

- the speed mark (picture `+0x30`/`+0x38`, cell `+0x40`), whose alpha `+0x60` `0x001D8520` swings between 63 and
  255 by 1.0 a frame (0.5 when `0x00184950` is not 2); after a speed change it starts at 1.5 times its size
  (`0x001D82D0`, scale `+0x6C`) and shrinks by 0.1 a frame (0.05 when `0x00184950` is 1) until it reaches 1;
- a second picture (`+0x70`, `+0x78`, `+0x80`) whose alpha `+0x88` `0x001D8240` swings the same way at
  `+0x8C` per 1/60 second (`0x0017D270`).

`0x001D7280` draws the second picture when `0x001C18E0()`'s byte `+0x40` is set or `0x00583920` answers non-zero
(`0x001D72F0`), and the speed mark while `0x00229DF0` answers non-zero and `+0x68` is set (`0x001D7DD0`).
`0x001829C0(x, y)`, from `0x00474100`, draws the second picture at a given place (`0x001D76A0`), and `0x00182A40`
restarts its swing at 255 (`0x001D85A0`).

### The simulation tick

`0x00314020(mode, arg)` has three callers: the field frame with mode 0 and the two menu frames with
mode 1. It returns `mode == 0`. Every mode runs the prologue:

- the tick-active word `0x022C2548` = 1 (read back by `0x00314960`, cleared at the one exit), the
  return stub `0x0016D6A0(0)`, `0x003EB9A0`, `0x003DAA20`, `0x003DA2F0(1.0)`, `0x003DD210(1.0)`;
- the manager request queue `0x0025BFB0` (below);
- the deferred mode request: `0x01EED060` is reset to -1; a non-negative `0x01EED064` prints two
  console markers and runs `0x0032FC30(0, request)`, then is reset to -1. `0x0032FC30(0, r)` is
  `0x003EA6E0(r, [0x022C6D1D])`, then `0x003319D0(r)` unless `0x00408B30()` is 1, `0x00408B10()` is 3 or
  `0x005C5230(5)` returns 0, then `0x0032FCA0(0, r)`, `0x0025D4D0(0)` and `0x022C6E48 |= 1`;
- the movement masks reset `0x003DAA40`, `0x0046AFA0`, the stick in mode 0 only (`0x00358C60`, [player
  movement](../Movement-And-Pathfinding/player-movement.md)), `0x00268650`, `0x0025D650`, `0x00255810`,
  `0x0037D890` and `0x0025D640`.

`0x0025BFB0` reads the mask `0x02099ABC` and returns when it is 0. With bit `0x1` set it runs the manager
runtime init `0x0026CE60` for each set bit from 4 down to 0, re-reading the mask after each, and
zeroes the four party-roster pointers `0x0209A1F0`-`0x0209A20F`; then, with or without that sweep, it
runs the unload `0x002628B0` for each set bit from 4 down to 0, clearing each bit after its call. A
menu frame therefore never stops queued area preparation or the roster clear.

The slot loops work on the five actor-manager slots at `0x02098E10`, stride `0x288`, and their
shape depends on the mode:

- mode 0: `0x003DF760(0, n, 0, 0, 0)` for n = 1 to 5; then sixteen sub-steps: for each slot, when
  the sub-step is 0 or the slot's byte `+0x201` (`0x00267310`) is set, the orchestrator
  `0x00234590(slot)`, the actor drive pass `0x0025D9E0(slot)` ([field
  runtime](../Characters-And-Objects/field-runtime.md)) and `0x00234520(slot)`; after sub-step 0's first
  loop `0x00253C50` and `0x00268D10`; then, under the same gate, the post-pass `0x003DB1F0(slot)`;
- mode 1: slots 3 and 4 only, once: the orchestrator, the drive pass, the post-pass and
  `0x00234520`, then `0x00253C50`;
- any other mode: no slot work.

Sub-steps 1 to 15 repeat the same three calls and the post-pass for a slot whose `+0x201` byte is
non-zero; nothing receives the step number. The byte is a bit set: `0x0026A5B0(slot, on, bit)` sets
or clears one bit, the script-skip begin `0x00360710(bit, slot)` sets it for a non-zero slot and the
skip end `0x00360A50` clears it, and `0x00267310` returns the whole byte, so any pending skip opts the
slot in.

Slot 0 never gets a bit, so the field slot is never repeated inside a step (the high-speed mode speeds the field up by
earning two or four steps a frame, see the speed mode below): the repeats exist for the
cutscene managers during `skipexec`. The post-pass `0x003DB1F0` walks a live slot's records:
for a record whose byte `+0x63` is set it turns every `1` at `+0x11` of the `+0x89` entries of
stride `0x14` at `[+0xA0]` into `2`, then runs `0x003DB6E0` on every record and shifts `+0x63` right
by one.

The tail, every mode: `0x022C252C` and `0x022C2530` increment; the separation pass
`0x003DAC70(0x00314F30)` ([movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md));
`0x002623A0(slot)` for slots 0 to 4 (mode 0) or 3 to 4 (mode 1), which publishes the slot block to
`0x02099D70` and the focus record to `0x02099D78` and runs `0x002E5180` over a live slot's records.

Then `0x00358EE0(mode)`; the request drain `0x002E09A0`; `0x00359800`; `0x003DE640`; `0x002E0940`; `0x0037C1A0`;
`0x003E7EC0`; `0x0036FD90(0)` when no dialog is open (`0x00228480`); `0x002F1770(mode, arg)`; `0x002EF910`;
`0x0036E1E0`; `0x003DEB30`; `0x003DF670`; `0x003606E0`; the audio listener `0x00362850`.

Then, when `0x00362DA0()` (the byte `0x022CBA9B`) is 0, the spatial-sound behind factor `0x022CBB28`
is recomputed ([spatial sound](../Sound-And-Music/spatial-sound.md)): `x = 0x00362DB0() + [0x022C2544]`, where
`0x00362DB0` reads the factor itself (after `0x00259AF0()` when `0x00265760()` is 0), and
`y = 0x002DEBA0()`, the configured ratio at `0x0215EFD0`; `0x00361700(y <= x ? min(x, 1.0) : y, 0)`
stores the result, floored at 0, back into `0x022CBB28`.

Then `0x003E7650`, `0x0025D950`, `0x00263660`, `0x002EEEB0` (`0x002EE430`, `0x002EF050`), and the
tick-active word is cleared.

### The scheduled tasks

Several things the player watches play out over a set number of frames are scheduled tasks: the crossfade from a
still of the picture into the live scene, the motion blur fading in or out, a music change and the end of a fading
track, a party member's model being read in, the walk that loads the models an area's battle data names, the extra
files some models load, and the short hold after a message window closes. Behind the full menu the crossfade, the
blur fade and that hold wait while the others go on.

At double and quadruple speed every task advances once per world step except the end of a fading music track, which
advances only on the frame's first step, so a music fade keeps its length in frames.

The table `0x022BDEC0` holds 32 tasks of `0x48` bytes, and bit i of the mask `0x022BE7C0` marks task i as taken.
`0x002F16B0()` takes the lowest free task (`0x002F16C3`, `0x002F16D3`) and sets its bit (`0x002F16DE`). It zeroes the
counter `+0x00` and the length `+0x04` (`0x002F16F4`), the end routine `+0x08` (`0x002F16F7`), the step routine `+0x10`
(`0x002F16FB`) and `+0x28` (`0x002F1702`), and stores the task's index at `+0x18` (`0x002F16FF`).

The take sets the step `+0x1C` to 1 and the tag `+0x1E` to 0 with one dword store (`0x002F1706`), and the menu byte
`+0x20` to 1 (`0x002F170A`). With all 32 tasks taken it returns 0 (`0x002F16D5`).

The runner `0x002F1780(kind, invert, force)` is reached only through `0x002F1770(kind, force)`, which passes invert as 0
(`0x002F1773`, `0x002F1775`). It visits the taken tasks in index order. A kind-1 pass skips a task whose menu byte is 0
(`0x002F17E2`, `0x002F17E8`, `0x002F17EC`), and a pass without force skips a task tagged 1 (`0x002F17FC`, `0x002F1801`).

For each task it runs, the runner calls the step routine with the task (`0x002F1814`). Once the counter has reached
the length (`0x002F1826`) it calls the end routine (`0x002F1840`), sets the step to 1 (`0x002F184F`) and clears the task's
bit (`0x002F1859`). Last it adds the step to the counter (`0x002F1860`, `0x002F1864`), so a task with step 0 never reaches
its length by counting.

`0x002F1770` runs from six sites:

- the simulation tick `0x00314020` (`0x003142C1`), with the tick's own mode and argument: kind 0 with the frame's
  first-step flag from the field frame (`0x0022ABD8`), kind 1 with force 1 from the full menu frame and the
  capture-backed frame (`0x0022BA23`, `0x0022BCCF`);
- the field frame when it skips the tick, kind 0 with the first-step flag (`0x0022ABE5`);
- the start-up and title states, kind 0 with force 1 (`0x0022B701`, `0x0022B803`);
- the area unload `0x002628B0`, kind 0 with force 1, twice (`0x00262AD7`, `0x00262B2C`).

| Taker | The task | Step routine | End routine | Length, step | Menu byte |
|---|---|---|---|---|---|
| `0x002EA6E0` (`0x002EA70B`) | a model's extra files ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)) | `0x002E60F0` | none | `+0x04` = `0x30009`, step 0 | 1 |
| `0x002F1A90` (`0x002F1AE6`) | the crossfade ([script screen effects](../Graphics/script-screen-effects.md)) | `0x002F18D0` | `0x002F1950` | frames × `[0x01DFE0B4]`, step 1 | 0 (`0x002F1B30`) |
| `0x002F1C50` (`0x002F1C66`) | the hold after a message window closes ([controls](../Controls-And-Input/controls.md)) | none | `0x002F18A0` | n × `[0x01DFE0B4]`, step 1 (`0x002F1CAF`) | 0 (`0x002F1C7D`) |
| `0x00361170` (`0x0036119B`), `0x00361200` (`0x00361276`) | the end of a fading music track ([music](../Sound-And-Music/music.md)) | none | `0x00361080` | the length / `0x00184950()` + 1, step 1 and tag 1 (`0x003611AC`, `0x00361296`) | 1 |
| `0x003614E0` (`0x0036153B`, `0x00361585`) | a music change ([music](../Sound-And-Music/music.md)) | `0x00361340` or `0x00360EE0` | `0x00361460` | 8 or 5, step 0 (`0x003615CE`) | 1 |
| `0x0037C910` (`0x0037C938`) | the walk over an area's battle data ([ARD](../Game-Files-And-Data-Tables/ard-area-battle-data.md)) | `0x0037C3F0` | none | 10, step 0 | 1 |
| `0x0037C980`, `0x0037CA00`, `0x0037CA80` (`0x0037C984`, `0x0037CA04`, `0x0037CA84`) | the party read-in ([party control modes](party-control-modes.md)) | `0x0037C730` | none | 4, step 0 | 1 |
| `0x003DE240`, `0x003DE2A0` (`0x003DE265`, `0x003DE2CC`) | the motion blur fade ([script screen effects](../Graphics/script-screen-effects.md)) | `0x003DE160` | `0x003DE1F0` | frames, step 1 | 0 (`0x003DE291`, `0x003DE2F8`) |

Two tasks are also kept by address. `0x022BE7C8` is the crossfade: `0x002F1A90` stores it (`0x002F1AF2`) and its end
routine `0x002F1950` clears it (`0x002F19E7`). `0x002F1A20` returns its low 32 bits to `0x001CC600` (`0x001CC7B9`), `0x0022A770`
(`0x0022AA47`, `0x0022ACEE`) and `0x00353700` (`0x00353704`). `0x002F1A70` copies its length into its counter, so the next
pass that runs it ends it; the unload (`0x00262B76`), `0x003600D0` (`0x003600E6`) and `0x003601D0` (`0x003602CE`) call it.

`0x022BE7D0` is the message-window hold: `0x002F1C50(n)` takes it when none is kept (`0x002F1C5A`, `0x002F1C66`,
`0x002F1C72`), and its end routine `0x002F18A0` clears it (`0x002F18B1`). `0x002F1710()` ends it at once: the counter becomes
the length (`0x002F1739`), the end routine runs (`0x002F1749`), the step becomes 1 (`0x002F174B`) and the bit is cleared
(`0x002F1756`). Square (`0x00253F93`), `0x0025AAD0` (`0x0025AB10`) and the unload (`0x00262A82`) call it.

`0x002F1A30(tag)` answers 1 while a taken task carries that tag (`0x002F1A41`, `0x002F1A4E`, `0x002F1A54`). Of the thirteen
takers only the two music track ends set tag 1, so `0x002F1A30(1)` asks whether a track end is still pending. The
drive pass asks it (`0x0025DD6E`, [field runtime](../Characters-And-Objects/field-runtime.md)), and so do the game-over
states (`0x003EF349`, `0x003EF423`), the chocobo state machine `0x0035CA70` (`0x0035CBC4`), `0x003466F0` (`0x003466F9`) and
`0x00347310` (`0x0034732B`); `0x0034DB30` passes a value of its own (`0x0034DBCE`).

The boot `0x00266D10` clears the mask and both kept tasks through `0x002F1A00` (`0x00266E2E`; `0x002F1A02`, `0x002F1A08`,
`0x002F1A0F`).

### The field frame orchestrator

`0x00234590(slot)` returns at once for any slot but 0, so it runs once per simulation step and never
behind the menu:

1. bit `0x2000` of the battle-state word `0x02089340` is cleared;
2. the clock: `0x0032A150()` before and after `0x0032A100`, which adds 1 to `0x0208D45C` when timer 0 moved; bit `0x4` = the counter
   did not move. The area-return window compares that counter with `(int)(30 × [0x01DFE0B8]) × 300` and expires when the
   difference is greater (9,000 steps at 30 fps, 18,000 at 60: 300 seconds at normal speed) ([enemy
   respawning](../Enemy-Spawning/enemy-respawning.md));
3. unless `0x0035C700()` or `0x00306BB0()`: UI request `0x0B` when `0x002371B0()` holds, else `0x18` when
   `0x00237140()` holds (`0x0035C7A0`);
4. `0x00313A00` (row 2 of [action availability](../Controls-And-Input/action-availability.md)); then, when the force-fight predicate `0x00253B90()` differs from the inverse of bit `0x8`,
   the unit reset loop below runs and then bit `0x8` is toggled;
   - the unit reset loop: for every unit `0x0030A880(buffer, 1)` lists, `0x00300140(unit, keep)` with `keep` = unit
   bit `0x1000000` clear, and (`+0x714` above `0x21E` or `+0x6B4` below 9), and `+0x714` not `0x113`, and
   the status words `+0x3C | +0x64` clear of `0x8000020`;
5. bit `0x2` cleared; the lock evaluator `0x0023B040`; `0x0032A650`; `0x003226C0`; `0x0030CBE0`, which walks the action chain ([action phases](../Battle-Actions/action-phases.md)); `0x003065D0`;
   `0x00325060`, which steps the generation `0x022C2578` that the per-unit `0x003247F0` compares ([enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)); `0x00307E70`; `0x00319600`; `0x00313760`; `0x00304440`; the group completion `0x00307030`;
6. the `0x18` latch: when `0x00237260()` holds, bit `0x200` is set and request `0x18` raised once
   (`0x0035C8A0`) and the rest is skipped; otherwise bit `0x200` is cleared (`0x0035C8E0(0x18)` when it was
   set);
7. the `0x17` latch: with no leader, no leader record, or a leader whose status words hold
   `0x80000003` without `0x00377C20()`, bit `0x100` is set and request `0x17` raised once; otherwise bit `0x100`
   is cleared (`0x0035C8E0(0x17)` when it was set);
8. bit `0x800`: with the party-control level at 1 (`0x003135C0()`) bit `0x800` is set unless the unit of
   `0x003137F0()` exists, has a record, and that record's status words are clear of `0x80000003` or
   `0x00377C20()` holds; at any other level it is cleared;
9. the obstacle grid `0x00392740` ([navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)),
   `0x0033B6D0`, `0x003246C0` when a navigation dataset is loaded, and `0x002F82F0`.

`0x00234520(slot)` is also slot 0 only: the lock evaluator again, `0x00313DB0`, `0x00319090`, a
guarded indirect call, and then the one-shot at `0x0208E6A8`, called and nulled when the
battle-state word has bit `0x1` set and bits `0x2` and `0x4` clear; otherwise `0x00313CD0` when a navigation
dataset is loaded.

### The per-unit frame

`0x00233F70(slot, record)` has no caller: `0x00265A20(manager)` stores its address at record `+0x38`
for every record whose byte `+0x14` is at or above `0x80`, only while the manager's `+0x28` is 0,
up to 32 of them (`0x00234480(0, record)`
first, `0x00234A00` on the record's `+0x30`, class-3 flag bits cleared, byte `+0x0E` low bits set,
`0x00238FA0` for a party row), clearing bit `0x10` of `+0x14` on the 33rd and beyond, and keeps the
count at the manager's `+0x1E8`. The actor drive pass calls the callback per record ([field
runtime](../Characters-And-Objects/field-runtime.md)).

Inside, the unit (`0x0031B760(record)`) must exist, `0x002671C0()` must hold (slot 0 active with
`0x02098E21` bit `0x1` and `0x02098E20` bit `0x80` clear and `0x02099DA1` zero), a navigation dataset must be
loaded, unit flag bit `0x8` must be set and bit `0x10000` clear. Then:

- bit `0x10` clear: when `0x00267240(record)` holds (byte `+0x10` zero and `+0x14` bit `0x40` or `+0x0C` bit `0x1`)
  and the unit's `+0x698` record exists, bit `0x10` is set: the unit is simulated from the next frame;
- bit `0x10` set, with a `+0x698` record whose status words `+0x3C | +0x64` are clear of `0x80000003`
  or with `0x00377C20()`: the active frame `0x00307C70`, `0x00236300`, `0x00310DB0` (the periodic status step, [status timers](../Status-Effects-And-KO/status-timers.md)), `0x003247F0`, `0x00308610`,
  `0x0023A070`, `0x002350C0(unit + 0x10)`, then `0x00312700`;
- bit `0x10` set, the gate failed, bit `0x2` set: `0x00312700` only;
- bit `0x10` set, the gate failed, bit `0x2` clear, a spawn-backed unit (record byte `+5` = 1 and
  `[+0xE68]+0x18 & 0xE` = 4): `0x00236300`, `0x0033A240(unit + 0x80)`, `0x0023A070`, `0x00312700`;
- otherwise idle: bit `0x2` of the battle-state word is set when `0x003070E0()` is 0; `0x0026A330(actor,
  0)`; `0x003057D0`; `r = 0x0030CA50(unit)`; with unit bits `0x200000000` and `0x400000000` set and not (`0x00322310(r)` = 0
  and `0x003228E0(r)` non-zero) the unit is torn down (`0x00300E40(unit, 0)`); then `0x00312700`.

### The battle-state word

`0x02089340` is one dword the frame and the battle layer share. `0x002341C0`, the area teardown reset
(`0x0030FE60`, `0x00383A20`, `0x00306570(0)`, `0x00392710`, `0x002FAEC0`, `0x0031BD60`, `0x00325080`, `0x00319B10` (resets the loot pickup pool, [loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)),
`0x002FA470`), clears bit `0x10`. The area initialisation `0x002342F0` writes `(word & 0xFFFFC01E) | 0x10`:
bit `0x10` set, bits 0 and 5 to 13 cleared at once. The boot's battle work init `0x002368D0` zeroes the
word.

The area initialisation also runs three resets:

- `0x00307FF0` (`0x00234432`) clears `0x022C1F48` bits `0x2` and `0x4` and zeroes `0x022C1F40`, as the engagement
  update does ([force-fight mode](force-fight-mode.md)).
- `0x00322190` (`0x00234437`) zeroes the sixteen `u16` words at `0x0208D334`. The script verbs write and
  read them through `0x00328D90` (`0x00328D9F`) and `0x0031B4F0` (`0x0031B4FF`), and the order code through
  `0x00329E60` (`0x00329F0C`) and `0x00321190` (`0x0032125C`), each for an index of at most 15.
- `0x0030C3F0` (`0x0023445E`) zeroes the 32 records of 12 bytes at `0x022C1DB0`, one per unit slot byte
  `+0xEA9`, where `0x00312FA0` saves a unit's `+0xDC8` word and `+0xE58` dword and `0x00308270`
  restores them.

| Bit | Set by | Cleared by | Meaning |
|---|---|---|---|
| 0 | `0x0023B020(fn, handle)`, which stores the one-shot at `0x0208E6A8`/`0x0208E6A4` | `0x00238A60`, which nulls them | a one-shot callback is armed; `0x00234520` consumes it |
| 1 | the idle unit frame when `0x003070E0()` is 0; the unit combat frame `0x00308610` when `0x00237670(id)` is 0, or when `0x0030DA30(unit)` holds with unit bit `0x1000000` set | the orchestrator every step | the frame is idle |
| 2 | the orchestrator when the clock counter did not move | the orchestrator | the clock stood still this step |
| 3 | toggled by the orchestrator's reset loop | the same | reset-loop parity against `0x00253B90` |
| 4 | the area initialisation `0x002342F0` | `0x002341C0`; `0x002368D0` | an area is live; the party and menu resolvers test it |
| 5 | `0x00238B70(1)`, which also posts message `0x30B` (`0x002E7C10`) to every unit with byte bit `0x10` in the unit table at `[0x0208E688]` (stride `0xF50`, count `0x0208E6A0`); called from `0x00306F00`, `0x00359A30`, `0x0035A6F0` and `0x0035AB20` | `0x00238B70(0)`; `0x002342F0` | |
| 6 | `0x0032A200`, which also runs `0x003B0770` when `0x0208CD1C` is not -1 and sets it to -1 | `0x0032A170`, the treasure verb's close, when `0x0208CD18` is 0 (the same `0x003B0770` tail); `0x002342F0` | the treasure-open verb's begin |
| 7 | `0x00238AE0(1)`, from the same four callers as bit `0x20` | `0x00238AE0(0)`; `0x002342F0` | |
| 8 | `0x00300FC0` when the torn-down unit's id is `0x003590D0()` (request `0x17`); the orchestrator's `0x17` latch | the latch; `0x002342F0` | the leader is incapacitated |
| 9 | `0x00300FC0` when `0x00237260()` (request `0x18`); the `0x18` latch | the latch; `0x002342F0` | every active low-type party member is down |
| 10 | `0x00300FC0` when `0x002372E0()` (request `0x0B`) | `0x002342F0` | the whole roster is down |
| 11 | `0x00300FC0` when `0x002373C0()`; the orchestrator's bit `0x800` test | the orchestrator; `0x002342F0` | the summoner of `0x003137F0()` is out of play |
| 12 | `0x00238B00(1)`, from `0x002628B0`, `0x002678C0`, `0x0026C8C0` and `0x0025D580` | `0x00238B00(0)`; `0x002342F0` | brackets a definition load or unload |
| 13 | `0x00238B20(1)`, from `0x0025B740` only | `0x00238B20(0)`; the orchestrator at the top of every step; `0x002342F0` | |
| 23 | the verb `btlAtelSetDebugRotControlMode` (`0x0050F2E0`) | the same verb with 0 | a script mode flag |
| 26 | the verb `btlSetViewCheckMode` (`0x0050F170`) | the same verb with 0 | a script mode flag |
| 29 | the verb `btlAtelSetRealBattleMode` (`0x0050F380`, which also runs `0x00308DE0`) | the same verb with 0 | a script mode flag |

`0x00300FC0(unit, mode)` is the unit teardown. For a kind-0 record of type `0x1B` to `0x27` in mode
0 it runs `0x003105D0` and `0x003138D0(0)` only. Otherwise:

1. `0x00310780`, `0x002ED180`, the flag clears (`*unit &= ~(bits 0x2, 0x80000, 0x100000 and 0x200000000)`, `+4 &= ~4`),
   `0x0026DAC0(actor, -1.0)`, `0x0026A330(actor, 0)`, `0x003219D0(type, 0, 0, 1)`;
2. `0x002372E0()`: bit `0x400`, `0x003001D0`, request `0x0B`, the lock evaluator `0x0023B040`, return;
3. else `0x00237260()`: bit `0x200`, `0x003001D0`, request `0x18`, the evaluator, return;
4. else `0x002373C0()` sets bit `0x800` alone; then an id equal to `0x003590D0()` sets bit `0x100` and raises
   `0x17`; and in mode 0 at party-control level 1, when the unit is the one of the summoner's row
   `[0x02EBF190] + 0x5AD5` (`0x0031B770`), `0x003138D0(0)` and the evaluator run.

## Layouts

### The notice window

The notice window is the `0x1D8`-byte widget with procedure `0x00474100` that `0x00474070` builds and that keeps itself at `0x02CA6C80`.

`NoticeWindow` (`0x1D8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00474100` |
| `+0x0C0` | `void*` | window | the message window the construct message opens for the copied text with `0x002A3090` (`0x00474271`, stored at `0x00474276`); message 18 closes it with `0x002A27C0` (`0x0047412C`) |
| `+0x0C8` | `char[256]` | text | the construct message's text a, copied with its terminator (`0x004741D4`-`0x004741E0`) and measured by `0x002B3050` (`0x004741FC`) |
| `+0x1C8` | `u32[4]` | box | the four dwords of the construct message's b (`0x00474210`-`0x0047422B`); the draw message passes `+0x1D0` and `+0x1D4` to `0x001829C0` (`0x00474160`-`0x0047416C`) |

### The main loop cells

The main loop's cells and records are laid out as follows.

Main loop cells (`0x02064AA0` ..):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02064AA0` | `u32` | the pump's flag |  |
| `0x02064AA4` | `u32` | 0 |  |
| `0x02064AA8` | `u32` | steps this pass |  |
| `0x02064AC0` | `f32` | time accumulator |  |
| `0x02064AC4` | `f32` | speed factor |  |
| `0x02064AC8` | `f32` | step gain (1.0) |  |
| `0x02064ACC` | `u32` | pacer ticks per frame |  |
| `0x02064AD0` | `u8` | game-step count |  |
| `0x02064AD1` | `u8` |  |  |
| `0x02064AD2` | `u8` | speed permit (0x00358550: 0x022C7F9A == 0x1F) |  |
| `0x02064AD3` | `u8` | state 0-6 |  |
| `0x02064AD4` | `f32` | 1.0 |  |
| `0x01FD4A68` | `u32` | 1 in states 4 and 6 |  |
| `0x01FD4A84` | `u32` | 1 in states 2, 3 and 5 |  |
| `0x01FD4A80` | `u32` | frame counter |  |
| `0x01FD4A74` | `u32` | speed pad latch |  |
| `0x01FD4A8C` | `u32` | one-shot 1.0 accumulator reload |  |
| `0x01FD4A98` | `i32` | speed index 0-2 |  |
| `0x00908BA8` | `f32[4]` | speed table {1.0, 2.0, 4.0, 0.0} |  |
| `0x022C7F9A` | `u8` | step permit byte (bits 1-4 = the four preconditions; 1 at boot and after every step) |  |
| `0x01E02820` | `f32` | accumulator at the top of the pass |  |
| `0x02064AEC` | `void*` | end-of-step callback (called once, then cleared) |  |

Tick globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022C2548` | `u32` | tick in progress |  |
| `0x022C252C` | `u32` | tick counters | with `0x022C2530` |
| `0x022C2530` | `u32` | tick counters | with `0x022C252C` |
| `0x01EED060` | `i32` | the deferred mode request (-1 none) | with `0x01EED064` |
| `0x01EED064` | `i32` | the deferred mode request (-1 none) | with `0x01EED060` |
| `0x02099ABC` | `u32` | manager request mask (bits 0-4) |  |
| `0x02098E10` | `...` | actor-manager slots, 5 x 0x288: +0x201 u8 sub-step opt-in |  |
| `0x02089340` | `u32` | the battle-state word |  |
| `0x0208E6A8` | `void*` | the one-shot callback |  |
| `0x0208E6A4` | `u32` | its handle |  |

## Shipped data

| Fact | Value |
|---|---|
| slots, sub-steps | 5 and 16, both immediates at every loop |
| state handlers | 7, states 0 to 6 |
| accumulator gain | `0x02064AC8` 1.0 at boot; `0x02064AC4` 1.0 or the `0x00908BA8` entry {1.0, 2.0, 4.0} at speed index 0 to 2 |
| speed permit | `0x022C7F9A` must read `0x1F` after the step |
| console markers | two strings at `0x00D103E0` and `0x00D10420` printed before a deferred mode request |
| unit callbacks | at most 32 per manager (`0x00265A20`) |

## Operations

Per frame: the state handler; in state 2, zero or more whole simulation steps, each one tick with
its slot loops, orchestrator, drive pass, post-pass and tail; then camera, end-of-frame list and
the pacer wait. Per step: the orchestrator's nine groups for slot 0, the drive pass per slot, the
unit frame per bound record.

## State

The state byte and the main-loop cells; the tick-active word, the two tick counters, the
deferred request and the manager request mask; the battle-state word, its one-shot callback, the
slots' `+0x201` bytes.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F7F4E9` | `u8` | 0 (zero-filled tail of `.data`) | the speed keys' latch, byte `+0x59` of the static block `0x01F7F490` ([game application](game-application.md)). `0x0017DEA0`, which the field frame calls at `0x0022AA59`, tests the keys Speed1, Speed2 and Speed3 in turn (group 2 slots 0 to 2, through `0x00197710` and `0x0079E6A0`). For the first key held it returns 1, and when bit `0x1` of the latch is clear it first sets the latch and calls `0x00239790` with 1, 2 or 4. With no key held it clears the latch and returns 0, so a held key changes the speed once | `0x0017DEA0`, 1 (`0x0017DEEB`, `0x0017DF3A`, `0x0017DF8E`) and 0 (`0x0017DFA5`) | `0x0017DEA0` (`0x0017DED8`, `0x0017DF28`, `0x0017DF78`) |
| `0x01F82D32` | `u8` | 0 (zero-filled tail of `.data`) | the byte after the second-pass latch pair `0x01F82D30` / `0x01F82D31` ([game application](game-application.md)). `0x001E0580` clears it with `0x01F82D31`; states 4 and 6 run `0x001E0580` (`0x0022A6C1`, `0x0022A6CD`), as do `0x001846B0`, `0x001846F0`, `0x003749F0`, `0x00376050` and `0x003BA020` | `0x001E0580`, 0 (`0x001E0587`) | no instruction names it |
| `0x0208D33C` | `u16[4]` | 0 (zero-filled tail of `.data`) | words 4 to 7 of the sixteen `u16` words at `0x0208D334`. `0x00329E60` stores word `n` and `0x00321190` reads it, each only for `n` from 0 to 15 (an unsigned bound: `cmp` with 15 and `ja` at `0x00329F03` and at `0x00321253`) | `0x00322190`, 0 (`0x00322199`, one 8-byte store); `0x00329E60` (`0x00329F0C`, the word `n`) | `0x00321190` (`0x0032125C`, the word `n`) |
| `0x0208D344` | `u16[4]` | 0 (zero-filled tail of `.data`) | words 8 to 11 of the sixteen `u16` words at `0x0208D334`. `0x00329E60` stores word `n` and `0x00321190` reads it, each only for `n` from 0 to 15 (an unsigned bound: `cmp` with 15 and `ja` at `0x00329F03` and at `0x00321253`) | `0x00322190`, 0 (`0x003221A0`, one 8-byte store); `0x00329E60` (`0x00329F0C`, the word `n`) | `0x00321190` (`0x0032125C`, the word `n`) |
| `0x0208D34C` | `u16[4]` | 0 (zero-filled tail of `.data`) | words 12 to 15 of the sixteen `u16` words at `0x0208D334`. `0x00329E60` stores word `n` and `0x00321190` reads it, each only for `n` from 0 to 15 (an unsigned bound: `cmp` with 15 and `ja` at `0x00329F03` and at `0x00321253`) | `0x00322190`, 0 (`0x003221A7`, one 8-byte store); `0x00329E60` (`0x00329F0C`, the word `n`) | `0x00321190` (`0x0032125C`, the word `n`) |
| `0x022BDEC0` | `task[32]` | 0 (zero-filled tail of `.data`) | the 32 scheduled tasks of `0x48` bytes: counter `+0x00`, length `+0x04`, end routine `+0x08`, step routine `+0x10`, index `+0x18`, step `+0x1C`, tag `+0x1E`, menu byte `+0x20`, the taker's own words from `+0x28` | `0x002F16B0`, which clears a task as it takes it; the takers fill the routines and the length | the runner `0x002F1780`, `0x002F1710`, `0x002F1A30`, `0x002F1A70` |
| `0x022BE7C0` | `u32` | 0 (zero-filled tail of `.data`) | the taken mask: bit i set while task i is taken | `0x002F16B0` (`0x002F16DE`), the runner (`0x002F1859`), `0x002F1710` (`0x002F1756`), `0x002F1A00` (`0x002F1A02`) | `0x002F16B0`, the runner (`0x002F178A`, `0x002F1816`, `0x002F1842`), `0x002F1A30` |
| `0x022BE7C8` | `void*` | 0 (zero-filled tail of `.data`) | the running crossfade's task | `0x002F1A90` (`0x002F1AF2`), `0x002F1950` (`0x002F19E7`), `0x002F1A00` (`0x002F1A08`) | `0x002F1A20`, `0x002F1A70`, `0x002F1A90` (`0x002F1AB5`, `0x002F1B18`, `0x002F1BBE`, `0x002F1BE6`, `0x002F1C2F`) |
| `0x022BE7D0` | `void*` | 0 (zero-filled tail of `.data`) | the message-window hold's task | `0x002F1C50` (`0x002F1C72`), `0x002F18A0` (`0x002F18B1`), `0x002F1A00` (`0x002F1A0F`) | `0x002F1710` (`0x002F1716`), `0x002F1C50` (`0x002F1C5A`, `0x002F1C9D`) |
| `0x022CA620` | `u32` | 0 (zero-filled tail of `.data`) | a copy of `0x022CA60C` that the pacer `0x0035EB70` takes on the game thread (`0x0035EC4D`-`0x0035EC53`) | `0x0035EB70` (`0x0035EC53`) | no instruction names it |
| `0x022CA638` | `u32` | 0 (zero-filled tail of `.data`) | the write index of the 256 frame deadlines (`f64`) at `0x022CA640` that the pacer's worker `0x0035EA40` waits on. `0x0035E9B0(t)`, which `0x0022A580` calls with -16.0 and 17.0 (`0x0022A670`, `0x0022A700`), stores `t` at `0x022CA640 + 8 × index` (`0x0035E9C1`), releases the semaphore `[0x022CA610]` (`0x0035E9CD`) and stores `(index + 1) & 0xFF` (`0x0035E9D2`-`0x0035E9DD`); the worker reads the deadlines with its own index (`0x0035EADC`) | `0x0035E9B0` (`0x0035E9DD`) | `0x0035E9B0` (`0x0035E9B4`, `0x0035E9D2`) |
| `0x02EBF3DC` | `u8` | 0 (zero-filled tail of `.data`) | the step of state 1's gate `0x0037C2E0`: 0 and 1 fetch the next entry, 2 holds on the current record `0x02ADD948`, 3 goes back to 1, 4 is done. The gate stores the step when it holds (2, `0x0037C3AF`, returning 1) and when it finishes (4, `0x0037C39C`, returning 0), and resumes from it on its next call | `0x0037C2E0` (`0x0037C39C`, `0x0037C3AF`); `0x0037CB30`, 0 (`0x0037CB37`), from the start-up's first-screen set-up (`0x0022B795`) | `0x0037C2E0` (`0x0037C2E6`) |
| `0x02EBF3DD` | `u8` | 0 (zero-filled tail of `.data`) | the gate's entry index: `0x0037C2E0` fetches entry `[0x02EBF3DD]` of the table `[0x02EBF0A8]` (`0x00320B30`) while the index is below the count `0x003204B0()` (a signed compare, `jl` at `0x0037C327`), increments it (`0x0037C337`) and skips an entry whose id is 0 or less (`jle`, signed, `0x0037C33F`) | `0x0037C2E0` (`0x0037C337`); `0x0037CB30`, 0 (`0x0037CB30`) | `0x0037C2E0` (`0x0037C319`, `0x0037C337`) |

## Modding notes

- The simulation is a fixed-step accumulator: a frame runs zero, one or more simulation steps, so a hook that runs per
  frame and one that runs per step see different counts; a port must keep the step gain at 1.0 to match.
- The camera block is the carry frame's substitute for a step: a port that runs it after every
  step moves the camera twice on stepped frames and not at all on carry frames.
- High speed is a permit, not a multiplier: the speed index only takes effect after a step in
  which all four preconditions held, and `0x00358280` re-arms the byte each step.
- The manager request queue is drained before the mode is consulted; a menu frame still prepares
  areas and clears the roster.
- Five and sixteen are compiled-in immediates; nothing reads a count from the slot array.
- Sub-steps 1 to 15 are repeats; only a cutscene manager under `skipexec` opts in, never slot 0.
- The orchestrator and `0x00234520` are slot-0 only; the menu modes never run them, so the battle
  layer does not advance behind the full menu.

## Related

- [Game application](game-application.md): the pump that calls the game step.
- [Startup constants](startup-constants.md): the state-machine cells and the pacer constant.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the actor drive pass and the per-record
  callback.
- [Enemy respawning](../Enemy-Spawning/enemy-respawning.md): the clock advance and
  the group completion.
