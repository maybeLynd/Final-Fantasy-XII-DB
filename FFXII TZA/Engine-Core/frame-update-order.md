---
title: "Frame update order: what runs each frame for the field, the battle layer and every unit"
kind: "system"
category: "Engine core"
addresses: "0022A490, 0022A580, 00229F00, 00229EA0, 0022B6E0, 0022B7E0, 0022A770, 0022B8C0, 0022AF50, 0022BC20, 0022B000, 0035EB70, 0035EC80, 00314020, 0025BFB0, 0032FC30, 00267310, 00234590, 0025D9E0, 00234520, 003DB1F0, 002623A0, 002EEEB0, 00233F70, 001EBA40, 0022BEB0, 00332590, 0037C2E0, 0035E7A0, 00265A20, 00267240, 002671C0, 00300FC0, 002341C0, 0023B020, 00238A60, 00238AE0, 00238B00, 00238B20, 00238B70, 0032A200, 0050F2E0, 0050F170, 0050F380, 002E09A0, 002E2240, 0035E6F0, 00360080, 0035E9F0, 0035E9B0, 00358510, 00358280, 003586A0, 00358550, 00229ED0, 00233700, 00233640, 002335D0, 0023B200, 0026A5B0, 00360710, 00360A50, 002342F0, 002368D0, 0032A170, 00308610, 003590D0, 0031B770, 0026B730, 0036F460, 0027E9E0, 002507C0, 0022BFB0, 00307FF0, 00322190, 0030C3F0"
---

## What the player sees

Every frame the pad is read, the world is simulated a whole number of steps, the camera follows,
sound is mixed, the picture is drawn and the loop waits for the next tick. At 60 frames per second
the world still advances in 30 frames-per-second steps: on some frames the accumulator carries over
and nothing in the world moves, which is why fast turns can look stepped.

The high-speed mode
doubles or quadruples the number of steps a frame earns, but only after a step in which nothing
held it back: a menu, a load, a cutscene or a dialog drops it to normal speed. Behind the full menu only
the cutscene managers tick; the field, the battle and every unit stand still until the menu
closes. A script skip runs the cutscene slots up to sixteen times a frame.

## How it works

### The main state machine

The application's pump calls `0022A490(dt, flag)` once per pass ([game
application](game-application.md)): it stores the flag at `02064AA0`, runs `0022A580`, and
increments `02064AD0` when that returns non-zero. `0022A580` first checks `00184AD0()` (a load in
progress returns 1 after `0020E4E0()`), counts `01FD4A80`, runs `00183100`, `001829A0`,
`00358640`, `001EC490`, `00214C30`, `00183100` again, `00182810` once when `01FD49E0` was set,
`001831C0` and `00183090`, then sets `01FD4A68` from the state and dispatches on the state byte
`02064AD3`:

| State | Handler | What it is |
|---|---|---|
| 0 | `0022B6E0` | start-up: after `0032E520(1)` reports no load pending and `0209273C` is 5 it moves to state 1 and runs the first-screen set-up (`0035EA30(0)`, `0053DD10(1Ch)`, `00236A40`, `00253A10`, `002EF650`, `003318C0`, `0037CB30`) |
| 1 | `0022B7E0` | title and loading: moves to state 2 when `0032E520(1)` and `0037C2E0()` are both 0, then `00184960(2)` |
| 2 | `0022A770` | the field frame (below); the default for any other value |
| 3 | `0022B8C0` | the full menu frame: pad, UI effects, `00314020(1)` under its `ATEL CONTROL` label, sound, the menu's own update; when `002E05C0()` is 0 it closes (`CLOSE FULLMENU`): `00263560`, state 2, `00182D40`, `002E1BA0`, `0024F980(0)`, four `002E1CA0(7)`, `0037CF00`, `003323D0`, `00332660`, `003323B0`, `00376BE0`, `00226280` |
| 4 | `0022AF50` | the screen capture before a menu (`SCREEN CAPTURE`, `0022B0B0(0, 1)`); moves to state 3 |
| 5 | `0022BC20` | the capture-backed frame: `00314020(1)` under `ATEL CONTROL`, then unless still 5 it returns to state 2 with `00263560`, `00376BE0`, `00226280`, `00375EC0` and `00360120` |
| 6 | `0022B000` | a second capture; moves to state 5 |

States 4 and 6 are entered through the setter `00229F00` (called from the request drain `002E09A0`
and from `002E2240`); `00229EA0` is the getter. `01FD4A68` is 1 in states 4 and 6 and 0 otherwise;
`01FD4A84` is 1 in states 2, 3 and 5, and in those three states `0035E6F0`, `00360080`, `0035E9F0`
and `0035E9B0(-16.0)` run before the dispatch; `02064AD8` toggles in every state but 4 and 6;
states 4 and 6 call `001E0580` first.

`0022BFB0(v)`, the handler of verb `05CA`<sub>h</sub> (through `00340B70`), sets `01FD49E0` and stores `v` at
`01FD49E4`; on the next pass `0022A580` calls `00182810(v)` (`0022A5E3`) and clears the request.
`00182810` writes `v != 0` to byte `+1E9`<sub>h</sub> of the post-process parameter object (`00193D50`,
`00193F70`).

State 1's gate `0037C2E0` walks the entries of the table `[02EBF0A8]` (`003204B0` the count,
`00320B30` an entry) and resolves each to a record (`002EAE20`) at `02ADD948`. A record with bit
`4`<sub>h</sub> of `+19`<sub>h</sub> set (`002E4C70` returns 0) goes to `002EAF70`. Any other holds the gate (it returns
1 and resumes there next frame) until bit `2`<sub>h</sub> of its `+18`<sub>h</sub> is set (`002E4C20`), and then gets bit
`2`<sub>h</sub> of `+19`<sub>h</sub> (`002EBE20(record, 1)`). The gate returns 0 once every entry is through.

After the handler, with `01FD4A84` set and `00184950()` = 2, `0035E9F0` and `0035E9B0(17.0)` run;
`001E0560` arms the pump's second pass when `01F82D31` was set; with `01FD4A68` clear,
`02F974A0` clear and no second pass armed, `001832F0()` runs, then `00375B80(0)`; and a callback
pending at `02064AEC` is called and cleared.

### The menu frame and the monster viewer

The full menu frame `0022B8C0` (state 3) runs a few steps that only matter for the Bestiary's
monster viewer, the object at `01F82E18` (`001EBA40`, `2E0`<sub>h</sub> bytes, constructor `001EB190`;
[Clan Primer](../Menus-And-HUD/clan-primer.md)). `00181DD0` reads its byte `+118`<sub>h</sub>, set while a monster is
shown:

1. without a monster shown it starts with `00182370` (`00186110` on the render manager);
2. after the pad and the UI effects, with `02064AA0` at 0, `00258EB0` pushes arena 2 (`0036C1D0`),
   runs `0024B9B0(0, 4)` and pops it (`0036C140`), and `00374950` follows;
3. it installs `0022BEB0` as the menu draw callback (`002D0570` stores it at `0209E630`);
4. after `OTHER`, with a monster shown, `00181B20` posts a `CopyBufferObj` (`0018B8B0`,
   `001F1810`) between the first entry of `00186910(render manager, 0)` (null when that entry's byte `+8`
   is set) and the viewer's `+278`<sub>h</sub>; `00181E50` then steps the viewer's fade at `+20`<sub>h</sub> (`001EC000`);
5. with a monster shown it sets `02064AE8` and runs `003323D0`, `00314370(0)` and `0036F510`, and
   when `00181DB0()` is 0 and `00358340()` holds, `00258E40`; `00181DB0` is `001EB990`, which holds
   while the viewer's byte `+26D`<sub>h</sub> or `+26E`<sub>h</sub> is set. Without a monster, a set `02064AE8` is
   cleared and `00314370(1)` and `0036F510` run.

The draw callback `0022BEB0` brackets the frame's own draws with `001FBE50` and `001FBD80(1)`.
With a monster shown it posts the same copy for the viewer's `+270`<sub>h</sub> (`00181AB0`) and, when
`002EF030()` is 1, interleaves `00258EE0(1)` to `00258EE0(5)` and `00375500(2)` / `(3)`, each behind
`003583F0(0)` or `00358350(0)`, with the viewer's turn `00184690` (`001EC060`).

It starts the viewer's 80-frame fade (`00181C10`, `001EBCF0`:
halved when `001EDE70()` is 0, from 200 down by 200 / frames) once `00181C70()` (`+284`<sub>h</sub>) is 0,
and steps that fade, the one at `+00`<sub>h</sub>, with `00181E30` (`001EBF90`). Both fades draw through `001EB800`.

The two capture states share their tail. `0022AF50` (state 4) and `0022B000` (state 6) both run
`00332590`, which points `022C6F20` at `022C6F30`, runs `0041E500` and `00426950`, and clears
arena 6's byte `+62`<sub>h</sub> in the table at `022D7FD0` when bit 6 of `022D89B8` is set (`003697C0(6)`).
They also run `00376D80`, which for each of the eight records at `02ADBB40` (stride `90`<sub>h</sub>) with
a non-zero first word sets bit 3 of `+54`<sub>h</sub> and copies `+08`<sub>h</sub>, `+10`<sub>h</sub>, `+18`<sub>h</sub> and `+20`<sub>h</sub> into
the word after each.

State 6 also runs `00375F20`, which sets bit 0 of the first word of the
records at `02EBF9F0` (stride `70`<sub>h</sub>) up to the first whose `+58`<sub>h</sub> is 0.

### The field frame

`0022A770` is state 2. After the pad (`0036F2F0`, `0035FF90`, `0036FDF0`, `002498B0`) and the
draw set-up it runs, when `0017E4E0()` is 0, `001EC760()` passes of the following; each pass ends
in the camera, the end-of-frame list and the pacer. `001EC690` advances the counter `01F832C4`, which `001EC760`
among others reads: once when `001EC760` returns 0, and in the pass loop's first step. The event-slot
pusher `0020AF10` zeroes it (`0020AFAA`).

Before the pad, once per `01E02824` with `00264610(0)` non-null, the deferred `0026B730(01E02808
& FFFFh)` runs. Each pass of the loop then:

- runs the speed-mode pad block (below);
- sets the speed factor `02064AC4` to 1.0 or, with the speed permit `02064AD2` set, the entry of
  the speed table `00908BA8` = {1.0, 2.0, 4.0} selected by the speed index `01FD4A98` (`00229E00` returns that entry);
  `003603C0()` forces 1.0 and runs `002370A0`;
- keeps the accumulator `02064AC0` as it stands at `01E02820`; when the pump's flag `02064AA0` was
  set, sets the accumulator to 1.0 (if `01FD4A8C` was 1, which is then cleared) or 0, and clears
  the flag;
- with bit 27 of `00226B10(0)`, `0036F460(accumulator)`; with the `002878A0` predicate false and
  `0017DE60()`, `0027E9E0`; with the predicate true, `003583A0()` and the accumulator at 0,
  `002507C0(1)` ([subsystem update flags](subsystem-update-flags.md)).
- `0036F460` hands the map animation clock `004678E0`
  ([texture animation lists](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md)) the
  accumulator's growth since its last call divided by `[01DFE0B8]`, keeps the fraction in `02AD9B50`,
  and ends with `00468520`, which runs `003CD820` on `+14`<sub>h</sub> of each record of the table
  `[02CA6010]` (count `[02CA6020]`, stride `40`<sub>h</sub>) whose `+4` is 0.

While the accumulator is at least 1.0, one simulation step runs:

1. `00250180(first)`; the tick `00314020(0, first)` when `001800E0()` is 0 and `001800C0()` is 0 or
   `001EC560()` is 0, else `002F1770(0, first)` with result 2;
2. `0037A450`, `0036D890`, `004668C0`; `003323D0` when `00358290()`; `002507C0(first)` when
   `003583A0()`; `00258B90(0)` when `00358340()`; `00314370(result)`; with the mode saved by
   `00358320`, `00358640(0)`, `0037D4C0`, `00314820`, `0036F510`, `00256F60`, `00358640(saved)`;
   `00258D70` when `00358340()`, and `001808D0` on the last step; `00254E50`; `0035AF20(0)`;
3. the accumulator loses 1.0 (floored at 0); a state other than 2 zeroes it and stops; otherwise
   `003586A0(1, 1)` when `002361A0()`, `(3, 1)` when `00265760()`, `(2, 1)` unless `00226BC0()`,
   `(4, 1)` unless `002F1A20()`;
4. `02064AD2 = 00358550()`, and when it is clear (after `0017F740(1)` when set) and `003583D0(0)`
   or `003583D0(1)` holds the accumulator is zeroed; `003603C0()` zeroes it too; `00358280` resets
   the permit byte; `02064AA8` counts the steps of this pass and is zeroed right after the loop,
   so it is non-zero only while a pass's steps run.

After the steps come three groups:

- the camera block, only on a pass in which no whole step ran (the accumulator carried; a flag
  set at the top of the pass is cleared after every step): `00358640(0)`, `004668C0`,
  `00258B90(1)`, `003143D0`, `00314370(1)`, `0037D4C0`, `00314820`, `0036F510`, `0035AF20(1)`,
  `00358640(saved)`, so the camera and the follow still advance on a carry frame;
- the end of the frame: `0035AE30`, `00360120` (the title-return gate, [game
  over](../World-Areas-And-Travel/game-over.md)), `00377520` and `0036F530` when `00358370()`, the
  accumulator gain, the controlled-character change `00358BC0`, `00226280`, `002E65A0`, `00332660`,
  `003323B0`, `00324510`, `0036F2C0`, `0032E040`, `0035E9A0(0022BFD0)`;
- the pacer `0035EC80([02064ACC], 0)` (an identical copy of `0035EB70`) ([startup constants](startup-constants.md)), then
  `0017F370(1)`, `00375B80(1)`, `00376470` and `00375500(7)` when `003583F0`, `0024B4F0`,
  `00374FD0`, `0037DDD0` and `00316930`.

With `0017E4E0()` non-zero the frame runs `002506D0` and, when `001EC560()`, the camera block
(its `00314370(1)` and `0037D4C0` each only while `02064AA0` is 0) followed by `0035AE30`,
`00360120` and the `00358370()` pair, and nothing else.

### The speed mode

- The permit byte `022C7F9A` is set to 1 at boot (`00358510`) and by `00358280` at the end of
  every step; during the step `003586A0(k, 1)` sets bit 1 when `002361A0()`, bit 3 when
  `00265760()`, bit 2 unless `00226BC0()` and bit 4 unless `002F1A20()`; `00358550()` is
  `byte == 1Fh`: every precondition held this step.
- The speed index `01FD4A98` (0 to 2) is written only by `00229ED0`: `00233700` on a press of pad
  bit 10 (0 to 1, or 0 to 2 when `002DDDA0()` is 1; any other value back to 0), `00233640` while
  held (through `002335D0`), and the resets `002370A0` (from `003603C0`), `00239790`, `00237DF0`,
  `00233C10` and `0023B2E0`.
- When `00233700` or `00233640` raises the index to 1 or 2 it also calls `00182FB0(index)`, as do
  `00239790` and `0023B2E0`. That runs `001D85C0` on the `ExtraUI` object `[01F82CD0]` (`001D8210`,
  built by `001D8150`): `+60`<sub>h</sub> = 255.0, `+64`<sub>h</sub> = 6.0, `+69`<sub>h</sub> = 1, `+6C`<sub>h</sub> = 1.5, and `+40`<sub>h</sub> copied
  from `+58`<sub>h</sub> for index 2, else from `+48`<sub>h</sub>.
- The pad block at the top of each pass clears the latch `01FD4A74` when `00265760()` is 0 or
  `00226BC0()`, `002F1A20()` or `0028F6A0()` holds; otherwise, with `0017DEA0()` 0, bit 10 of
  `0036FF70()` and `0036FFD0()` sets the latch and runs `0023B200` (the edge through `0208E6B8`:
  `00233700` on a press, `00233640` while held), which keeps running every pass while the latch
  is set.

The pacer `0035EB70(n, x)` (and its copy `0035EC80`), on the game thread, folds the frame time into `022CA5C4` and
`022CA5D8`, stores `max(n, 1)` ticks at `022CA5F4`, clears the tick counter `022CA5F0` and returns
its previous value; on any other thread it spins until the tick counter at `022CA5E0` has
advanced by `max(n, 1)`.

Between the fold and the reset (`022CA5C4` = 0) the pacer stores at `022CA5DC` the result of
`0035E7A0`, which adds `022CA5D0` to `022CA5C4` once more and measures that sum a against a period
L of 314, or 264 when `00290180()` is 2: it returns the distance from a up to the next multiple of
L, except that below L, outside frame mode 3 (`00229EA0`), it returns 2L - a.

### The simulation tick

`00314020(mode, arg)` has three callers: the field frame with mode 0 and the two menu frames with
mode 1. It returns `mode == 0`. Every mode runs the prologue:

- the tick-active word `022C2548` = 1 (read back by `00314960`, cleared at the one exit), the
  return stub `0016D6A0(0)`, `003EB9A0`, `003DAA20`, `003DA2F0(1.0)`, `003DD210(1.0)`;
- the manager request queue `0025BFB0` (below);
- the deferred mode request: `01EED060` is reset to -1; a non-negative `01EED064` prints two
  console markers and runs `0032FC30(0, request)`, then is reset to -1. `0032FC30(0, r)` is
  `003EA6E0(r, [022C6D1D])`, then `003319D0(r)` unless `00408B30()` is 1, `00408B10()` is 3 or
  `005C5230(5)` returns 0, then `0032FCA0(0, r)`, `0025D4D0(0)` and `022C6E48 |= 1`;
- the movement masks reset `003DAA40`, `0046AFA0`, the stick in mode 0 only (`00358C60`, [player
  movement](../Movement-And-Pathfinding/player-movement.md)), `00268650`, `0025D650`, `00255810`,
  `0037D890` and `0025D640`.

`0025BFB0` reads the mask `02099ABC` and returns when it is 0. With bit 0 set it runs the manager
runtime init `0026CE60` for each set bit from 4 down to 0, re-reading the mask after each, and
zeroes the four party-roster pointers `0209A1F0`-`0209A20F`; then, with or without that sweep, it
runs the unload `002628B0` for each set bit from 4 down to 0, clearing each bit after its call. A
menu frame therefore never stops queued area preparation or the roster clear.

The slot loops work on the five actor-manager slots at `02098E10`, stride `288`<sub>h</sub>, and their
shape depends on the mode:

- mode 0: `003DF760(0, n, 0, 0, 0)` for n = 1 to 5; then sixteen sub-steps: for each slot, when
  the sub-step is 0 or the slot's byte `+201`<sub>h</sub> (`00267310`) is set, the orchestrator
  `00234590(slot)`, the actor drive pass `0025D9E0(slot)` ([field
  runtime](../Characters-And-Objects/field-runtime.md)) and `00234520(slot)`; after sub-step 0's first
  loop `00253C50` and `00268D10`; then, under the same gate, the post-pass `003DB1F0(slot)`;
- mode 1: slots 3 and 4 only, once: the orchestrator, the drive pass, the post-pass and
  `00234520`, then `00253C50`;
- any other mode: no slot work.

Sub-steps 1 to 15 repeat the same three calls and the post-pass for a slot whose `+201`<sub>h</sub> byte is
non-zero; nothing receives the step number. The byte is a bit set: `0026A5B0(slot, on, bit)` sets
or clears one bit, the script-skip begin `00360710(bit, slot)` sets it for a non-zero slot and the
skip end `00360A50` clears it, and `00267310` returns the whole byte, so any pending skip opts the
slot in.

Slot 0 never gets a bit, so the field never fast-forwards: the repeats exist for the
cutscene managers during `skipexec`. The post-pass `003DB1F0` walks a live slot's records:
for a record whose byte `+63`<sub>h</sub> is set it turns every `1` at `+11`<sub>h</sub> of the `+89`<sub>h</sub> entries of
stride `14`<sub>h</sub> at `[+A0h]` into `2`, then runs `003DB6E0` on every record and shifts `+63`<sub>h</sub> right
by one.

The tail, every mode: `022C252C` and `022C2530` increment; the separation pass
`003DAC70(00314F30)` ([movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md));
`002623A0(slot)` for slots 0 to 4 (mode 0) or 3 to 4 (mode 1), which publishes the slot block to
`02099D70` and the focus record to `02099D78` and runs `002E5180` over a live slot's records.

Then `00358EE0(mode)`; the request drain `002E09A0`; `00359800`; `003DE640`; `002E0940`; `0037C1A0`;
`003E7EC0`; `0036FD90(0)` when no dialog is open (`00228480`); `002F1770(mode, arg)`; `002EF910`;
`0036E1E0`; `003DEB30`; `003DF670`; `003606E0`; the audio listener `00362850`.

Then, when `00362DA0()` is 0, the time-scale block: `x = 00362DB0() + [022C2544]` (after
`00259AF0()` when `00265760()` is 0) and `y = 002DEBA0()`; `00361700(y <= x ? min(x, 1.0) : y, 0)`.
Then `003E7650`, `0025D950`, `00263660`, `002EEEB0` (`002EE430`, `002EF050`), and the
tick-active word is cleared.

### The field frame orchestrator

`00234590(slot)` returns at once for any slot but 0, so it runs once per simulation step and never
behind the menu:

1. bit 13 of the battle-state word `02089340` is cleared;
2. the clock: `0032A150()` before and after `0032A100` ([enemy
   respawning](../Enemy-Spawning/enemy-respawning.md)); bit 2 = the counter did not
   move;
3. unless `0035C700()` or `00306BB0()`: UI request `0B`<sub>h</sub> when `002371B0()` holds, else `18`<sub>h</sub> when
   `00237140()` holds (`0035C7A0`);
4. `00313A00`; then, when the force-fight predicate `00253B90()` differs from the inverse of bit 3,
   the unit reset loop: for every unit `0030A880(buffer, 1)` lists, `00300140(unit, keep)` with `keep` = unit
   bit 24 clear, and (`+714`<sub>h</sub> above `21E`<sub>h</sub> or `+6B4`<sub>h</sub> below 9), and `+714`<sub>h</sub> not `113`<sub>h</sub>, and
   the status words `+3Ch | +64h` clear of `8000020`<sub>h</sub>; then bit 3 is toggled;
5. bit 1 cleared; the lock evaluator `0023B040`; `0032A650`; `003226C0`; `0030CBE0`; `003065D0`;
   `00325060`; `00307E70`; `00319600`; `00313760`; `00304440`; the group completion `00307030`;
6. the `18`<sub>h</sub> latch: when `00237260()` holds, bit 9 is set and request `18`<sub>h</sub> raised once
   (`0035C8A0`) and the rest is skipped; otherwise bit 9 is cleared (`0035C8E0(18h)` when it was
   set);
7. the `17`<sub>h</sub> latch: with no leader, no leader record, or a leader whose status words hold
   `80000003`<sub>h</sub> without `00377C20()`, bit 8 is set and request `17`<sub>h</sub> raised once; otherwise bit 8
   is cleared (`0035C8E0(17h)` when it was set);
8. bit 11: with the party-control level at 1 (`003135C0()`) bit 11 is set unless the unit of
   `003137F0()` exists, has a record, and that record's status words are clear of `80000003`<sub>h</sub> or
   `00377C20()` holds; at any other level it is cleared;
9. the obstacle grid `00392740` ([navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)),
   `0033B6D0`, `003246C0` when a navigation dataset is loaded, and `002F82F0`.

`00234520(slot)` is also slot 0 only: the lock evaluator again, `00313DB0`, `00319090`, a
guarded indirect call, and then the one-shot at `0208E6A8`, called and nulled when the
battle-state word has bit 0 set and bits 1 and 2 clear; otherwise `00313CD0` when a navigation
dataset is loaded.

### The per-unit frame

`00233F70(slot, record)` has no caller: `00265A20(manager)` stores its address at record `+38`<sub>h</sub>
for every record whose byte `+14`<sub>h</sub> is at or above `80`<sub>h</sub>, only while the manager's `+28`<sub>h</sub> is 0,
up to 32 of them (`00234480(0, record)`
first, `00234A00` on the record's `+30`<sub>h</sub>, class-3 flag bits cleared, byte `+0E`<sub>h</sub> low bits set,
`00238FA0` for a party row), clearing bit 4 of `+14`<sub>h</sub> on the 33rd and beyond, and keeps the
count at the manager's `+1E8`<sub>h</sub>. The actor drive pass calls the callback per record ([field
runtime](../Characters-And-Objects/field-runtime.md)).

Inside, the unit (`0031B760(record)`) must exist, `002671C0()` must hold (slot 0 active with
`02098E21` bit 0 and `02098E20` bit 7 clear and `02099DA1` zero), a navigation dataset must be
loaded, unit flag bit 3 must be set and bit 16 clear. Then:

- bit 4 clear: when `00267240(record)` holds (byte `+10`<sub>h</sub> zero and `+14`<sub>h</sub> bit 6 or `+0C`<sub>h</sub> bit 0)
  and the unit's `+698`<sub>h</sub> record exists, bit 4 is set: the unit is simulated from the next frame;
- bit 4 set, with a `+698`<sub>h</sub> record whose status words `+3Ch | +64h` are clear of `80000003`<sub>h</sub>
  or with `00377C20()`: the active frame `00307C70`, `00236300`, `00310DB0`, `003247F0`, `00308610`,
  `0023A070`, `002350C0(unit + 10h)`, then `00312700`;
- bit 4 set, the gate failed, bit 1 set: `00312700` only;
- bit 4 set, the gate failed, bit 1 clear, a spawn-backed unit (record byte `+5` = 1 and
  `[+E68h]+18h & Eh` = 4): `00236300`, `0033A240(unit + 80h)`, `0023A070`, `00312700`;
- otherwise idle: bit 1 of the battle-state word is set when `003070E0()` is 0; `0026A330(actor,
  0)`; `003057D0`; `r = 0030CA50(unit)`; with unit bits 33 and 34 set and not (`00322310(r)` = 0
  and `003228E0(r)` non-zero) the unit is torn down (`00300E40(unit, 0)`); then `00312700`.

### The battle-state word

`02089340` is one dword the frame and the battle layer share. `002341C0`, the area teardown reset
(`0030FE60`, `00383A20`, `00306570(0)`, `00392710`, `002FAEC0`, `0031BD60`, `00325080`, `00319B10`,
`002FA470`), clears bit 4. The area initialisation `002342F0` writes `(word & FFFFC01Eh) | 10h`:
bit 4 set, bits 0 and 5 to 13 cleared at once. The boot's battle work init `002368D0` zeroes the
word.

The area initialisation also runs three resets: `00307FF0` (`00234432`) clears `022C1F48` bits 1 and
2 and zeroes `022C1F40`, as the engagement update does ([force-fight mode](force-fight-mode.md));
`00322190` (`00234437`) zeroes the sixteen `u16` words at `0208D334` that `0031B4F0` reads and
`00328D90` writes; `0030C3F0` (`0023445E`) zeroes the 32 records of 12 bytes at `022C1DB0`, one per
unit slot byte `+EA9`<sub>h</sub>, where `00312FA0` saves a unit's `+DC8`<sub>h</sub> word and `+E58`<sub>h</sub> dword and
`00308270` restores them.

| Bit | Set by | Cleared by | Meaning |
|---|---|---|---|
| 0 | `0023B020(fn, handle)`, which stores the one-shot at `0208E6A8`/`0208E6A4` | `00238A60`, which nulls them | a one-shot callback is armed; `00234520` consumes it |
| 1 | the idle unit frame when `003070E0()` is 0; the unit combat frame `00308610` when `00237670(id)` is 0, or when `0030DA30(unit)` holds with unit bit 24 set | the orchestrator every step | the frame is idle |
| 2 | the orchestrator when the clock counter did not move | the orchestrator | the clock stood still this step |
| 3 | toggled by the orchestrator's reset loop | the same | reset-loop parity against `00253B90` |
| 4 | the area initialisation `002342F0` | `002341C0`; `002368D0` | an area is live; the party and menu resolvers test it |
| 5 | `00238B70(1)`, which also posts message `30B`<sub>h</sub> (`002E7C10`) to every unit with byte bit 4 in the unit table at `[0208E688]` (stride `F50`<sub>h</sub>, count `0208E6A0`); called from `00306F00`, `00359A30`, `0035A6F0` and `0035AB20` | `00238B70(0)`; `002342F0` | |
| 6 | `0032A200`, which also runs `003B0770` when `0208CD1C` is not -1 and sets it to -1 | `0032A170`, the treasure verb's close, when `0208CD18` is 0 (the same `003B0770` tail); `002342F0` | the treasure-open verb's begin |
| 7 | `00238AE0(1)`, from the same four callers as bit 5 | `00238AE0(0)`; `002342F0` | |
| 8 | `00300FC0` when the torn-down unit's id is `003590D0()` (request `17`<sub>h</sub>); the orchestrator's `17`<sub>h</sub> latch | the latch; `002342F0` | the leader is incapacitated |
| 9 | `00300FC0` when `00237260()` (request `18`<sub>h</sub>); the `18`<sub>h</sub> latch | the latch; `002342F0` | every active low-type party member is down |
| 10 | `00300FC0` when `002372E0()` (request `0B`<sub>h</sub>) | `002342F0` | the whole roster is down |
| 11 | `00300FC0` when `002373C0()`; the orchestrator's bit-11 test | the orchestrator; `002342F0` | the summoner of `003137F0()` is out of play |
| 12 | `00238B00(1)`, from `002628B0`, `002678C0`, `0026C8C0` and `0025D580` | `00238B00(0)`; `002342F0` | brackets a definition load or unload |
| 13 | `00238B20(1)`, from `0025B740` only | `00238B20(0)`; the orchestrator at the top of every step; `002342F0` | |
| 23 | the verb `btlAtelSetDebugRotControlMode` (`0050F2E0`) | the same verb with 0 | a script mode flag |
| 26 | the verb `btlSetViewCheckMode` (`0050F170`) | the same verb with 0 | a script mode flag |
| 29 | the verb `btlAtelSetRealBattleMode` (`0050F380`, which also runs `00308DE0`) | the same verb with 0 | a script mode flag |

`00300FC0(unit, mode)` is the unit teardown. For a kind-0 record of type `1B`<sub>h</sub> to `27`<sub>h</sub> in mode
0 it runs `003105D0` and `003138D0(0)` only. Otherwise:

1. `00310780`, `002ED180`, the flag clears (`*unit &= ~(bits 1, 19, 20 and 33)`, `+4 &= ~4`),
   `0026DAC0(actor, -1.0)`, `0026A330(actor, 0)`, `003219D0(type, 0, 0, 1)`;
2. `002372E0()`: bit 10, `003001D0`, request `0B`<sub>h</sub>, the lock evaluator `0023B040`, return;
3. else `00237260()`: bit 9, `003001D0`, request `18`<sub>h</sub>, the evaluator, return;
4. else `002373C0()` sets bit 11 alone; then an id equal to `003590D0()` sets bit 8 and raises
   `17`<sub>h</sub>; and in mode 0 at party-control level 1, when the unit is the one of the summoner's row
   `[02EBF190] + 5AD5h` (`0031B770`), `003138D0(0)` and the evaluator run.

## Layouts

Main loop cells (`02064AA0` ..):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `02064AA0` | `u32` | the pump's flag | `02064AA4`  u32  0 |
| `02064AA8` | `u32` | steps this pass | `02064AC0`  f32  time accumulator |
| `02064AC4` | `f32` | speed factor | `02064AC8`  f32  step gain (1.0) |
| `02064ACC` | `u32` | pacer ticks per frame | `02064AD0`  u8   game-step count |
| `02064AD1` | `u8` | 02064AD2 | u8   speed permit (`00358550`: `022C7F9A` == `1F`<sub>h</sub>) |
| `02064AD3` | `u8` | state 0-6 | `02064AD4`  f32  1.0 |
| `01FD4A68` | `u32` | 1 in states 4 and 6 | `01FD4A84`  u32  1 in states 2, 3 and 5 |
| `01FD4A80` | `u32` | frame counter | `01FD4A74`  u32  speed pad latch   `01FD4A8C`  u32  one-shot 1.0 accumulator reload |
| `01FD4A98` | `i32` | speed index 0-2 | `00908BA8`  f32[4]  speed table {1.0, 2.0, 4.0, 0.0} |
| `022C7F9A` | `u8` | step permit byte (bits 1-4 = the four preconditions; 1 at boot and after every step) |  |
| `01E02820` | `f32` | accumulator at the top of the pass | `02064AEC`  ptr  end-of-step callback (called once, then cleared) |

Tick globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `022C2548` | `u32` | tick in progress | `022C252C` / `022C2530`  u32 tick counters |
| `01EED060` | `/ 01EED064` | i32 | the deferred mode request (-1 none) |
| `02099ABC` | `u32` | manager request mask (bits 0-4) |  |
| `02098E10` | `actor-manager` | slots, | 5 x `288`<sub>h</sub>: +`201`<sub>h</sub> u8 sub-step opt-in |
| `02089340` | `u32` | the battle-state word | `0208E6A8` / `0208E6A4`  the one-shot callback and its handle |

## Shipped data

| Fact | Value |
|---|---|
| slots, sub-steps | 5 and 16, both immediates at every loop |
| state handlers | 7, states 0 to 6 |
| accumulator gain | `02064AC8` 1.0 at boot; `02064AC4` 1.0 or the `00908BA8` entry {1.0, 2.0, 4.0} at speed index 0 to 2 |
| speed permit | `022C7F9A` must read `1F`<sub>h</sub> after the step |
| console markers | two strings at `00D103E0` and `00D10420` printed before a deferred mode request |
| unit callbacks | at most 32 per manager (`00265A20`) |

## Operations

Per frame: the state handler; in state 2, zero or more whole simulation steps, each one tick with
its slot loops, orchestrator, drive pass, post-pass and tail; then camera, end-of-frame list and
the pacer wait. Per step: the orchestrator's nine groups for slot 0, the drive pass per slot, the
unit frame per bound record.

## State

The state byte and the main-loop cells; the tick-active word, the two tick counters, the
deferred request and the manager request mask; the battle-state word, its one-shot callback, the
slots' `+201`<sub>h</sub> bytes.

## Modding notes

- The simulation is a fixed-step accumulator: a hook that runs per frame runs zero, one or more
  times per simulation step, and a port must keep the step gain at 1.0 to match.
- The camera block is the carry frame's substitute for a step: a port that runs it after every
  step moves the camera twice on stepped frames and not at all on carry frames.
- High speed is a permit, not a multiplier: the speed index only takes effect after a step in
  which all four preconditions held, and `00358280` re-arms the byte each step.
- The manager request queue is drained before the mode is consulted; a menu frame still prepares
  areas and clears the roster.
- Five and sixteen are compiled-in immediates; nothing reads a count from the slot array.
- Sub-steps 1 to 15 are repeats; only a cutscene manager under `skipexec` opts in, never slot 0.
- The orchestrator and `00234520` are slot-0 only; the menu modes never run them, so the battle
  layer does not advance behind the full menu.

## Related

- [Game application](game-application.md): the pump that calls the game step.
- [Startup constants](startup-constants.md): the state-machine cells and the pacer constant.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the actor drive pass and the per-record
  callback.
- [Enemy respawning](../Enemy-Spawning/enemy-respawning.md): the clock advance and
  the group completion.
