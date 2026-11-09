---
title: "Game over: what a party wipe does, the GAME OVER screen, and the return to the title map"
kind: "system"
category: "World, areas and travel"
addresses: "0x00234590, 0x0035C7A0, 0x0035C7B0, 0x00227370, 0x002E1B10, 0x00254850, 0x00254E50, 0x002805D0, 0x0027EFA0, 0x002E09A0, 0x00254B50, 0x0028F970, 0x00280A00, 0x00252B40, 0x0027FB70, 0x00280140, 0x003EF750, 0x003EF830, 0x003EFAA0, 0x003EF2E0, 0x003EEEC0, 0x003EF4A0, 0x003EF050, 0x003EF680, 0x003EF770, 0x003EF290, 0x00361630, 0x00360C20, 0x003611F0, 0x00360D70, 0x002DDCA0, 0x002EFA70, 0x00285EC0, 0x00285EA0, 0x003603E0, 0x003603D0, 0x0034EB20, 0x00360120, 0x003601D0, 0x003321E0, 0x0022A770, 0x0022BC20, 0x00228C70, 0x0027F2E0, 0x00264B90, 0x00377AB0, 0x00377A90, 0x0037B4D0, 0x00356500, 0x00359C60, 0x0030F4B0, 0x00237CA0, 0x0034AAB0, 0x002FEAC0, 0x00314DC0, 0x00314D80, 0x0034AC10"
---

## What the player sees

When the last main character still standing falls (guests do not count, and a standing reserve member
opens the party screen instead), everyone on the field stops where they are, the
screen dims, the music fades and the GAME OVER image appears. After a while, or as soon as a
button is pressed once the image has settled, the screen fades to black and the title screen
comes up. Nothing is reloaded along the way: the field, the party and everything that happened
since the last save are gone, and play resumes only when the player loads a save from the title
screen.

The same return happens from the pause screen's "This will return you to the title screen"
confirmation, and a zone script can ask for it too. Where a load afterwards puts the party is
the save's business: a save written at a crystal puts the party beside that crystal, an autosave
puts it at the entrance the party came in by.

## How it works

### The wipe becomes a request

The field frame `0x00234590` checks the party every frame and, when it is wiped, posts mode `0x0B`
through `0x0035C7A0(0x0B)` and `0x0035C7B0(0x0B, 1)`; the four wipe predicates and the post are on
[when the game is over](../Status-Effects-And-KO/ko-and-game-over.md).
`0x0035C7B0(kind, post)` refuses while a request is already pending: `0x022C83E8` bit `0x100`, a mode `0x02092730` of
`0x0B` or `0x18`, or the request byte `0x0215F1A0` (`0x002E12D0`; `0x0035C7BA`-`0x0035C7ED`). Otherwise, for kind `0x0B`, it
runs five steps:

1. sets `0x022C83E8` bit `0x100` (`0x0035C806`);
2. halts every actor through stop request 22 (`0x16`) of the
   [time stop registry](../Engine-Core/time-stop-and-freeze.md): `0x00227370` (`0x0035C810`) calls
   `0x00226BE0(0x16, 0, 0, 0, -1, -1)`, no actor, no handles, fade -1 and flag -1 (`0x0022739B`), and tail-jumps to
   the apply `0x00226280` (`0x002273A4`); both are skipped when `0x01FD46D4` bit `0x400000`, request 22's active bit,
   is set (`0x00227374`);
3. when `post` is non-zero (`0x0035C815`), writes the request `0x0215F1A0 = 1`, `0x0215F1A4 = 0x0B`, `0x0215F1A8 = 0`
   through `0x002E1B10(0x0B, 0)`, unless the latch `0x0215F1A1` is set; `0x0035C7A0` gives 1 and `0x0027EFA0` 0;
   `0x002E1B10` answers 1 when it writes (`0x002E1B35`-`0x002E1B47`) and 0 when the latch refuses (`0x002E1B58`), and
   only for id 2 does it also ask `0x002E0FA0` (`0x002E1B27`-`0x002E1B33`);
4. sets `0x022C83E8` bit `0x2` (`0x0035C864`);
5. locks the input group with `0x00254850(1)` (`0x0035C870`): ten `0x002E1C20(8, bit)` calls set bits `0x1`, `0x2`,
   `0x4`, `0x10`, `0x20`, `0x40`, `0x80`, `0x200`, `0x800` and `0x100000` of action availability row 8
   (`0x00254861`-`0x002548DA`, [action availability](../Controls-And-Input/action-availability.md)).

For kind `0x18` it opens the mode-`0x18` screen with `0x00254B40(0x18)` (`0x0035C7FF`), then sets `0x022C83E8` bit `0x1`
and tail-jumps to `0x00254940(1)` (`0x0035C832`-`0x0035C844`). For kind `0x17` it sets bit `0x10` and tail-jumps to
`0x002548F0(1)` (`0x0035C849`-`0x0035C85F`). Any other kind returns after the refusal tests (`0x0035C830`).

A second route needs no field frame. The main loop (`0x0022A770`) calls `0x00254E50` once per tick,
which asks `0x002805D0`: when `0x0035C740()` is non-zero, a mode-screen task is up and the current mode
`0x02092730` is one of 6, `0x0A`, `0x0F`, `0x11`, `0x12`, `0x13`, or 2 with a sub-id outside
`0x40` to `0x42`, it runs `0x0027EFA0`.

`0x002805D0` answers 1 only when the area controller `[0x0209AC30] + 0xC0` is also set and the mode-screen task
`[0x0209AC30] + 0xB8` has 0 in its dword `+0xD4` (`0x002805E4`-`0x00280601`). The mode goes through the byte table
`0x0028065C` (index mode − 2, `0x00280609`-`0x0028062E`), and the sub-id is the task's dword `+0xC4` (`0x00280630`); every
other case answers 0 (`0x00280648`).

The sub-id test subtracts `0x40` and compares unsigned with 2 (`0x00280636`-`0x0028063C`), so a sub-id below `0x40`
passes it as one above `0x42` does. The task takes the sub-id from the screen request's second dword
(`0x0027FDE1`). `openfullscreenmenu_48d(2, n)` opens mode `0x0A`, not mode 2 (`0x002E0DA0`, `0x002E0DD8`), and that mode
answers 1 with no sub-id test. The ids the scripts pass are 2, 4, 6, `0x8000` and `0x8004` to `0x8006`, and none
maps to mode 2.

Mode 2 comes from the input arbiter, with sub-id 0 on Triangle (`0x00253D78`) and on Select or L3 with `0x21`
(`0x00253EE6`, `0x00253F53`) or, once story flag `0x5E` is set, `0x00264640(2)`, 1 when that is 0 (`0x00253F44`). `0x0035D750`
also posts it with sub-id 0 from mode `0x18`.

Arming sets availability bit `0x1` through `0x00254850(1)` (`0x0035C870`, `0x0035C8D7`). The arbiter returns while Game
Over is armed (`0x00253C97`), and the drain drops a pending id 2 when that bit is set (`0x002E0C5E`-`0x002E0C65`).

The one order left is the screen opening first and the arming landing later in the same step. Opening mode 2
sets the main-loop state to 4 (`0x002E0D39`), and `0x00254E50` runs only in state 2, so only the check later in that step
(`0x0022AC73`) can see the new screen. The new task's `+0xD4` is then still 0 (`0x00246626`): only its second update can
raise it (`0x0027FC09`), and its first only moves `+0xD0` from 0 to 1 (`0x0027FD47`).

The open shuts the route through a queued hit. `0x00280A60` calls `0x00252B40`, whose tail `0x00254740` raises freeze
request 13 for mode 2 (`0x002552E0`, `0x0025479D`) and applies it at once (`0x002547A2`). Its A record clears bit
`0x2000000` ([time stop](../Engine-Core/time-stop-and-freeze.md)), so the apply starts the effect mask at 0
(`0x00226334`-`0x00226339`), and what it adds later, `0x76`, `0x2`, `0x108` or the `0x10C` case, leaves bit `0x1` clear.
That mask goes to `0x0209215E` (`0x00226474`).

Between the drain (`0x0031427D`) and the check, `0x00258D70` (`0x0022AC65`, when `0x00358340()` is non-zero; that value
depends on bit `0x4` of `0x022C7F92`, which the `movieend` body writes through `0x00358650`, `0x0035B953`) runs the effect
passes. With bit `0x1` clear, the kind 1 pass (`0x00258DF8`, `0x0024BA07`) skips every instance outside state 1
(`0x0024BB54`-`0x0024BB64`), and an instance in state 1 takes its paused step and leaves (`0x0024BB9D`,
`0x0024BD05`-`0x0024BD17`).
The state 3 arm that calls `0x002FC010` (`0x0024BD80`) does not run, so a queued value does not reach the applier
`0x00307300` that way.

The other caller of `0x002FC010`, the deferred list at `0x02092170` (`0x0024B5EC`), reads no kind mask. On this step
`0x0024B4F0` reaches it at `0x0022AED7`, after the loop that holds the check (`0x0022AD69`), too late for that check. In
the effect passes only kind 1 reaches `0x002FC010`: the state 3 table at `0x0024BD5B` sends every other kind elsewhere.

Effect programs send timeline codes to `0x00319F50` through `0x002EB740`, and only codes 0 (`0x00319FD8`) and 2
(`0x0031A042`) have a direct-call path to `0x0030E360`. The 347 shipped commands that send them, `0x03` and `0x22`, are
all in magic files, and those play as kind 1 (`0x002FCCC0`). A held kind 1 instance runs only `0x003A7EE0` and
`0x003A93F0`, which have no direct-call path to `0x003B8670`, and no shipped command uses `0x11`, the signal to a kind 1
instance (`0x003B8CB2`).

Two direct-call chains from the field frame after the drain still reach `0x00300FC0` through `0x00300E40`. `0x00359800`
goes through `0x00359A30`, `0x0035A590`, `0x00233F50` and `0x00233EA0` only in dispose state 1, which the `disposeentry`
begin sets (`0x0035A64F`) and the same tick ends (`0x00359B01`). `0x0037C1A0` goes through `0x0037B4D0`, `0x00233AD0`,
`0x00324450` and `0x003243F0` only for a slot of the mask that `partystdmotionrecover` fills (`0x0037CFD0`).

Each chain tears down a unit whose record is already down or that has none (`0x00233ED7`-`0x00233EF7`, `0x00324420`), so
neither changes what `0x002372E0` reads. Either arms Game Over only when that test is already true while bit `0x2` of
`0x022C83E8` is clear. A KO with a unit arms at the KO (`0x0030E877`), so that state needs another cause, such as a KO
on a record with no unit (`0x0030E729`). This rules out the hit route and, over direct calls and for magic files their
action requesters play, the effect programs; no route with every gate true is located yet, and the sub-id test stays
as written above.

The body of `0x0027EFA0` fades (`0x002EFA70(3, 0, 1, 0)` when `0x002EFD20(3)` is
non-zero), calls `0x0035C7B0(0x0B, 0)` and `0x00252B40(0x0B, 1)`, writes 2 to the area controller's `+0xC8`
(`[[0x0209AC30] + 0xC0] + 0xC8`, `0x0027EFE8`, read with no null test, so a null controller faults there), releases
the mode-screen task `[0x0209AC30] + 0xB8` through `0x00245020` (`0x0027F000`; it returns at once for a null task),
clears `[0x0209AC30] + 0xDEE`, runs
`0x00251E80`, sets `+0xDEF = 1` and starts the game-over task directly with `0x003EF750` (`0x0027F02A`).

### From the request to the screen

The UI request consumer `0x002E09A0` reads `0x0215F1A0` in its closing block and calls
`0x00254B50([0x0215F1A4], [0x0215F1A8], 0)`, then clears the byte. `0x00254B50(id, p2, p3)` indexes the byte
table at `0x00254C70` with `id - 1`: entry 10 is 5, and the jump table at `0x00254C58` sends 5 to the
default arm `0x00254C2D`, which runs `0x0028F970()` (clears bits `0x10` and `0x400` of the menu state dword at
`[0x0209BE80] + 0x10F68`) and then `0x00280A00(0x0B, 0, 0)`.

Around that dispatch `0x00254B50` does more:

- It first returns 0 without opening anything while `0x02092734` is 1 (`0x00254B71`) or when the combined action
  availability mask holds bit `1 << (id & 31)` (`0x00254B80`-`0x00254BC5`). No word of that mask's table `0x01E0C2C0`
  holds bit `0x800`, so id 11 is refused only by the latch.
- Before it reads the byte table it calls `0x0017E7D0`, `0x0035DA80` and `0x003C8990` (`0x00254BC7`-`0x00254BD1`).
- `0x0028F970` changes nothing while `[0x0209BE80]` is null or bit `0x2000` of that dword is set; otherwise it also
  clears the word `+0x10FA0` (`0x0028F97B`-`0x0028F9AF`), and when `0x00273A20([0x0209BE80] + 0xAB30)` answers non-zero it
  sets bit `0x40` of `+0x10CFC` (`0x0028F9B6`-`0x0028F9D4`).

`0x00280A00(mode, p2, p3)` opens a mode screen only when the root block's `+0xC0` and `+0xB8` are
both null. It stores the mode with `0x00252B40(mode, 1)` (`0x02092730 = mode & 0x7FFF`, `0x02092734 = 1`,
`0x020927D8 = mode & 0x7FFF`), spawns the mode-screen task `0x0027FB70` and the area controller `0x00280140`
(`0xD8` bytes each) and runs `0x0028CA30`. The create arm of `0x0027FB70` for mode `0x0B` sets
`[0x0209AC30] + 0xDEF = 1` and calls `0x003EF750` (`0x0027FFC3`), which is
`0x00244F50(0x108, 0x003EF830, 0)`: the game-over task. Those are the only two callers of `0x003EF750`.

`0x00280A00` in full (`0x00280A00`-`0x00280AC0`):

- With the root block's `+0xC0` or `+0xB8` set it returns 0 and builds nothing (`0x00280A1A`-`0x00280A30`,
  `0x00280AAD`).
- `0x00252B40` stores its second argument, which `0x00280A00` gives as 1, in `0x02092734`, and `mode & 0x7FFF` in both
  `0x02092730` and `0x020927D8` (`0x00252B40`-`0x00252B52`); it then jumps to `0x00254740`.
- Both tasks get one create record whose `+0x08` points at `{mode, p2, p3, 0}` (`0x00280A32`-`0x00280A8C`).
- `0x0028CA30` runs through `0x0028E860` (`0x00280A91`), and the call returns 1 (`0x00280A96`).

### The game-over task and its helpers

`0x003EF830` is a task of `0x108` bytes. Its create arm:

1. zeroes `+0xC0` (the state), `+0xE0`, `+0xE8` and `+0xF0` (`0x003EF985`-`0x003EF99A`) and stores itself at
   `0x02B5F1C8`;
2. takes a request group for itself (`0x00249580`, `0x003EF9A7`) and in it registers the `gameover_c` texture,
   kind 7 id `0x39`, through the descriptor at `0x00D11C88` into `+0xF8` (`0x00393460`, `0x003EF9C4`; the
   descriptor names the string at `0x00D11CD0`, the file is `Tm2_Menu\gameover_c.tm2` in each language folder);
3. requests `gameover.mrp`, kind 7 id `0x38`, through the id table at `0x00D11CA0` into `+0x100` (`0x003933F0`,
   `0x003EF9DE`), and closes the group (`0x00249410`, `0x003EF9E6`), whose message `0x10` arrives once both files
   have landed;
4. sets its rect to `0x01E0C1D8` x `0x01E0C1DC` at 0, 0 (`0x003EF9EB`-`0x003EFA0A`), attaches itself to the list
   `0x0208EA28` with priority 100 and runs `0x003678F0`;
5. spawns two helpers of `0xD0` bytes: the image task `0x003EF2E0` at `+0xD0` and the timing task
   `0x003EEEC0` at `+0xD8`, whose create record names the game-over task as its parent (`0x003EFA45`-`0x003EFA67`),
   and returns 0.

Its tick (`0x001EDEC0` on `+0xB4`) runs the state machine `0x003EFAA0` when `0x001EDEC0` answers non-zero
(`0x003EF966`). Message `0x10` sets `+0xF0 = 1`. Messages `0x0F`, `0x12`, `0x13` and `0x8001` reach it as
message `0x0C` with that id at `+0x08` and the payload byte at `+0x10` (`0x003EF8C5`-`0x003EF8DB`); it ignores
other ids there.

Message `0x8001` kills the prompt task at `+0xE8` (`0x00244F00`, `0x003EF8EE`); message `0x12` with payload 1, 2
or 3 clears the helper pointer `+0xD8`, `+0xE0` or `+0xE8`, and other payloads change nothing. Message `0x0F`
runs `0x003EF680` and message `0x13` `0x003EF770`, each with the payload byte (`0x003EF951`, `0x003EF8FF`). Messages
other than 1, 2, `0x0C`, `0x10` and `0x12` go to `0x005C5230(task)`, whose answer it returns (`0x003EF872`); every
other path returns 0.

The image task `0x003EF2E0` fades the music with `0x002DEE50(0x002DEC00(), 30)`, fades the loaded images
over 30 frames (`0x003611F0(0x1E)`) and sets the fade rate `0x003634B0(0x3C)`. Its create arm also sets state 0
with a count of 15 at `+0xC8` and calls `0x00246AD0(game-over task, self)` (`0x003EF476`-`0x003EF491`). Its tick
(message 2) runs only when `0x001EDEC0` on `+0xB4` answers non-zero, and messages other than 1 and 2 go to
`0x005C5230` (`0x003EF301`). Its states:

- state 0 counts down 15 frames, runs `0x00363560` and `0x0024D050`, and once `0x002F1A30(1)` is 0 loads
  image 7 with `0x00361630(7)`: a slot of the four-entry image table at `0x022CB9F0` (Layouts); when
  no slot is free (`-1`) it releases every slot with `0x00360D70` and retries from state 1;
- `0x00361630` also answers -1 when the first free slot is slot 2 or 3 (Layouts); state 1 calls `0x00361630(7)` on
  every tick until it answers 0 or more, and either state then goes to state 2 with a count of 0
  (`0x003EF3D0`-`0x003EF3EB`);
- state 2 waits until the slot's state byte is 5 (`0x00360C20(7)`); state 3 is "ready"; states 3, 5 and 7 do
  nothing on a tick;
- state 4 counts down and then sets its end flag `+0xC4` bit `0x1`;
- state 6 waits for `0x002F1A30(1)` to be 0 and becomes 7.

The timing task `0x003EEEC0` starts the screen fade `0x00251D90(1, 0x3C, 0x78)`, waits until
`0x00251D20()` is above 2, then 18 frames, plays `0x002C99A0(1000, 8)` and sends the parent message
`0x13` with payload 1; 60 frames later it reaches its end state. It forwards messages `0x0F` and
`0x12` to the parent with payload 1.

Its create arm takes the parent from the create record's `+0x08`, zeroes its state byte `+0xC8` and count
`+0xCC`, and calls `0x00247930(self, 100)` and `0x00246AD0(game-over task, self)` (`0x003EEFEE`-`0x003EF032`). The
`0x002C99A0` call passes 0 as a third argument (`0x003EEF9A`-`0x003EEFA6`). Its tick runs while `0x001EDEC0` on `+0xB4`
answers non-zero, and its state step only when the count `+0xCC` is 0 or has just reached 0 (`0x003EEF27`-`0x003EEF4D`).

The end state is state 3, which waits; state 2 becomes 3 when its 60 frames are over (`0x003EEF86`). In state 4,
which `0x003EF680` sets, it destroys itself with `0x00244F00` once its count has run out (`0x003EEF71`-`0x003EEF74`).
Messages other than 1, 2, `0x0F` and `0x12` go to `0x005C5230` (`0x003EEEF7`).

### The state machine

`0x003EFAA0` runs when the countdown `+0xC4` is 0 or has just reached 0. Message `0x13` from the
helpers (`0x003EF770`) moves it: payload 1 puts it in state 1, payload 2 spawns the prompt task
`0x003EF050` (`0xD8` bytes) at `+0xE8` and goes to state 3, payload 3 goes to state 4. Other payloads change
nothing (`0x003EF79C`).

The prompt task's create record, like the logo task's below, is {0, the game-over task, the dword at `+0x100`},
the last two sign-extended from 32 bits (`0x003EF7BB`-`0x003EF7E8`, `0x003EFC16`-`0x003EFC48`). States 0, 2, 3 and 4 do
nothing in `0x003EFAA0` (`0x003EFAFA`); `0x003EF770` and `0x003EF680` move the task out of them.

1. State 1 waits until the image slot is ready (image task state 3) and message `0x10` has
   arrived (`+0xF0`). It then spawns the logo task `0x003EF4A0` (`0xD0` bytes) at `+0xE0`, starts music track 7
   at full volume with `0x002DECE0(7)` (`0x003EFC69`; [Music](../Sound-And-Music/music.md)) and goes to state 2.
   - The music and step 2 below run only when the image task's state byte reads 3 again after the spawn
     (`0x003EFC5B`-`0x003EFC62`); otherwise the task goes to state 2 without them (`0x003EFCA9`, `0x003EFCAE`).
   - The logo task's widget is entry 0 of the `gameover.mrp` file its create record names
     (`0x002432B0(self + 0x50, file, 0, self)`, `0x003EF4E2`); the animation descriptor at `0x00D11CA8` goes to
     `0x00247570` (`0x003EF539`).
2. At the same moment the image task enters state 4 with a display count of `0x564`, `0x3DE` or
   `0x3A2` frames when `0x002DDCA0()` returns 1, 2 or anything else; that is the word at
   `[0x0215E6E0] + 0x0E`, a 2 downgraded to 1 when `0x0017E490()` has bit `0x1` clear. The downgrade is stored
   back into the word (`0x002DDCC7`).
3. The logo task waits 18 frames, then, once `+0xF0` is set, attaches to the parent's list; when it
   ends it sends `0x13` with payload 2, which spawns the prompt task.
   - Its create arm copies the widget's rectangle to `+0x98`-`+0x9E`, takes the parent from the record's
     `+0x08`, calls `0x00247930(self, 99)` and `0x00244960(game-over task, self)`, sets the count `+0xCC` to 18 and
     calls `0x00247870(self, 0)` (`0x003EF4F9`-`0x003EF569`).
   - From then on every tick, while `+0xC8` bit `0x1` is clear, counts `+0xCC` down and, once it is 0 and
     `+0xF0` is set, calls `0x00246AD0(game-over task, self)` (`0x003EF58A`-`0x003EF5BB`).
   - It forwards messages `0x0F`, `0x12` and `0x13` to the parent with payload 2 (`0x003EF5E1`-`0x003EF601`);
     message `0x0E` sets its `+0xC8` bit `0x1` (`0x003EF5CD`), and other messages go to `0x005C5230`.
4. The prompt task `0x003EF050` ends the screen on message 10 when the image task's end flag is set
   or a button in the mask `0xFF09` of `0x02F9736A` is pressed: it sends `0x8001` to the parent, which
   kills it.
   - Its widget is entry 1 of the same file (`0x002432B0(self + 0x50, file, 1, self)`, `0x003EF095`). Like the
     logo task it copies the rectangle, calls `0x00247930(self, 99)` and `0x00244960(game-over task, self)` and
     `0x00247870(self, 0)`, with an 18-frame count at `+0xC8` (`0x003EF0AC`-`0x003EF10A`).
   - Its tick, while `+0xCC` bit `0x1` is clear, counts `+0xC8` down and then calls
     `0x00246AD0(game-over task, self)` on every tick (`0x003EF12F`-`0x003EF15F`).
   - Message `0x0C` is passed on to the parent with its own id and payload (`0x003EF1DA`-`0x003EF1E9`). Message
     `0x0E` sets `+0xCC` bit `0x1` and calls `0x002470D0(self)` (`0x003EF171`-`0x003EF17B`).
   - Messages `0x0F`, `0x12` and `0x13` go to the parent with payload 3 (`0x003EF18D`, `0x003EF1FB`-`0x003EF214`),
     and other messages go to `0x005C5230` (`0x003EF233`).
5. Message `0x0F` with payload 3 runs `0x003EF680`: the logo task is killed, `0x00250C50(100)` and
   `0x00251EA0(0.8, 0x78)` run, the timing task is set to state 4 for 180 frames and, unless the image
   task has already ended, the music fades over 120 frames and the images over 240
   (`0x003611F0(0xF0, 1)`, `0x003634B0(0xF0, 0)`, image state 6). The parent waits 60 frames and goes to
   state 5.
   - `0x003EF680` returns at once for any other payload (`0x003EF683`). The full calls are `0x00250C50(100, 180)` and
     `0x00251EA0(0.8, 0x78, 0)` (`0x003EF6A9`-`0x003EF6C5`), and the image task's count `+0xC8` becomes 240
     (`0x003EF720`).
   - It reads the timing task `+0xD8` with no null test (`0x003EF6A2`-`0x003EF6D1`).
6. State 5 fades layer 2 to black over 60 frames (`0x002EFA70(2, 0x3C, 0)`), waits 120 frames and goes
   to 6. State 6 runs `0x003EF290(image, 1)` when the image task's end flag is set (a one-frame music
   fade and a two-frame image fade), then 7. State 7 waits for image task state 7 and destroys it
   (`0x00244F00`), then 8.
   - `0x003EF290(image, n)` runs `0x002DEE50(0x002DEC00(), n, 0)`, `0x003611F0(2n, 1)` and `0x003634B0(2n, 0)` and puts
     the image task in state 6 with a count of `2n` (`0x003EF29F`-`0x003EF2D2`).
7. State 8, once `+0xD8`, `+0xE0` and `+0xE8` are all null, destroys the task itself and calls
   `0x00285EC0(0x0C)` (`0x003EFB32`).

The teardown message `0x12` releases the `gameover_c` texture entry at `+0xF8` (`0x00393900`, `0x003EF888`) and
frees the `gameover.mrp` buffer at `+0x100` (`0x003938B0`, `0x003EF899`), calls `0x00254850(0)` and `0x00254940(0)`
and runs `0x0027F2E0`. `0x00254850(0)` returns at once with no write (`0x00254856`, `0x002548DF`), so it releases
nothing; `0x00254940(0)` calls `0x002E1CA0(8, 0xB)` and jumps to `0x002547D0(0)` (`0x00254948`-`0x0025496D`).

Of the ten row-8 bits that `0x00254850(1)` set, the teardown therefore clears `0x800` (`0x00254964`) and, through
`0x002547D0(0)`, `0x2`, `0x4`, `0x10`, `0x20`, `0x40`, `0x80` and `0x200` (`0x002547F2`-`0x00254836`). Bits `0x1` and
`0x100000` stay set. `0x00254980(0)` clears both among its seven bits (`0x002549A2`-`0x002549E2`); it is called with 0 at
`0x0035D90A` and `0x0035DAB3`. The party-down window clears both when the current mode `0x02092730` is `0x18`, through
`0x002E1CA0(8, 0)` and `0x002E1CA0(8, 0x14)` (`0x0035D728`-`0x0035D746`).

`0x002E1CA0(8, 0)` also clears bit `0x1` alone at `0x0027A8AA`, in the chocobo dismount and ride (`0x0035C9A5`,
`0x0035CF6C`) and in the target cursor (`0x003C8A0A`, `0x003C8AF2`, `0x003C8C97`-`0x003C9085`). `0x00229510` rewrites row 8
from the copy taken when the Start screen opened (`0x00229554`, `0x00229562`). The area unload clears every row through
`0x002E0670` (`0x00262CCA`), and the field start through `0x002E1450` (`0x00267155`). No `0x002E1CD0` call names row 8.

`0x0027F2E0` takes a length of 1 when bit `0x800` of `[0x0209AC30] + 0x400` is set and 200
otherwise (`0x0027F2ED`-`0x0027F301`), closes menu slot 0 over it (`0x002C98C0` at `0x0027F306`), steps the
mode-screen backdrop kept at `0x020927F0` toward its fade (`0x00250F30` at `0x0027F30B`), fades fade slot 3 in over
length × 60 / 1000 frames when the length is above 1 and slot 3 is active (`0x002CC960` at `0x0027F312`;
`0x002EFD20(3)`, `0x002EFA70(3, n, 1)`).

It then rewrites the low byte of `[0x0209AC30] + 0x400` from its bits `0x200` and `0x400` (2 when bit `0x200` is clear, 1 when bit `0x200` is set and bit `0x400`
clear, 2 when both are set) and clears bit `0x800`.

### The request for the title map, and what it really does

`0x00285EC0(field)` sets `[0x0209AC30] + 0x400` bit `0x100` and writes `+0x3FC = field`. Its callers are the
game-over task (`0x003EFB32`, field `0x0C`) and the pause task `0x00228C70` (`0x002291B1`, field `0x0C`).

The pause task shows "This will return you to the title screen. Are you sure?" (menu text `0x85F`,
key `0x114`) or "This will close FINAL FANTASY XII THE ZODIAC AGE" (text `0x890`, key `0x115`). A
confirmed return fades (`0x002EFA70(2, 0x18, 0)`), waits for `0x002EFD20(2)` to report 2 and calls
`0x00285EC0(0x0C)`; a confirmed quit calls `0x001E0FB0(0)`. The same task's skip path calls
`0x00285EA0(1)`, which sets bit `0x2000` of `+0x400`
([the native command lifecycle](../Scripts-And-Script-Commands/native-commands.md)).

The consumer is the area controller `0x00280140`, in its message `0x12` arm (`0x00280248` to
`0x0028027C`): with bit `0x100` set it clears the bit and tests `+0x3FC` against `0x0C`. For `0x0C` it
calls `0x003603E0`, which sets the byte `0x022CB72B = 1`; for any other field it runs `0x002CFD10(-1)`
and `0x00314440(+0x3FC, 0, 0, 0)`, a real field transition
([zone changes](zone-changes-and-mapjump.md)). Then `0x00251E80`, `0x00252D90`,
`[0x0209AC30] + 0xDEF = 0` and `+0xC0 = 0`. So the title map, field `0x0C` (`ttl_a01`), is never
requested as a zone change after a game over; a title-return byte is set instead.

### The main loop tears the field down

`0x00360120` runs every main-loop iteration (`0x0022A977` and `0x0022AE00` in `0x0022A770`), and at `0x0022BDDB` in the
capture-backed frame `0x0022BC20` (the re-initialisation) only on the frame whose state byte `0x02064AD3` is no longer 5,
when that frame returns to state 2 (`0x0022BDB2`-`0x0022BDDB`).

It refreshes the busy mask's bit `0x80` with `0x003321E0`, writes `0x022CB724 = 0x5A` and `0x022CB727 = 0`, and when the
busy mask `0x022CB720` is 0 and either title byte `0x022CB72A` or `0x022CB72B` is set, it runs the resume routine `0x003601D0`
and then `0x0017F740(0)`, `0x001EC4B0(1)`, `0x001EC4B0(2)`, `0x001830A0(1)`, `0x00382B50(-1, 0, 0)`, `0x00182810(1)` and
`0x00357B00` (`0x022C7F80 = 0`).

`0x003321E0` tests the low dwords of the five pending masks `0x022C6E48` to `0x022C6E68` (8 bytes apart) without
bit `0x1`: when all five are 0 it clears bit `0x80` through `0x003601C0(7)`, otherwise it sets it through
`0x003601B0(7)` (`0x003321E0`-`0x00332244`).

`0x003601D0` is the field teardown, in this order:

1. both speed scales to 1.0 (`0x00229EF0`, `0x00229EE0`), `0x00368AC0(0)`, `0x0032E520(0)`, `0x0035EA30(0)`,
   `0x0053DD10(1)`;
2. for managers 0 to 2 with `+0x10` bit `0x1`, the jump lock `+0x200` bit `0x1` is cleared;
3. `0x002DEE90(-1)`, `0x003634A0(0)`, `0x003633B0(0)`, `0x00362850`, `0x002DF0F0(0, -1)`, `0x002DF060`,
   `0x001DC330(-1)`, `0x002DEB90(1)`, `0x005C5230`: the sound teardown, in which `0x002DF0F0(0, -1)` and
   `0x001DC330(-1)` are the audio manager's stop calls for sounds and for voices, and `0x002DEE90(-1)` calls
   `0x0035EA30(0)` until `0x001DBD00` returns 0 ([audio manager](../Sound-And-Music/audio-manager.md));
   - `0x001DC330(-1)` is reached through the jump `0x002DF690` (`0x0036025F`), and `0x002DEE90(-1)` runs twice more,
     before `0x002DEB90(1)` and after `0x005C5230` (`0x00360267`, `0x0036027E`);
4. the bits `0x1C` of the layer mask are cleared through `0x002DF370(0x1C, 0, 1)` and every image slot is
   released (`0x00360D70`), with `0x0035EA30(0)` before and after the release (`0x00360293`, `0x0036029F`);
5. `0x022CB726 = 1`; `0x022CB727`, `0x022CB72A` and `0x022CB72B` are cleared;
6. `0x002EF840(0)` to `0x002EF840(6)`, `0x002F1A70`, `0x003DE210`, `0x003DE0A0`, `0x002EFE40(6)`,
   `0x002EFE50(0xFF)`, `0x002EFA70(2, 0, 0, 0)`, `0x002EFA70(3, 0, 1)`;
7. `0x002E06B0`, `0x003636A0`, `0x00363750`, `0x00363E40(0)`, `0x0036DF30`, `0x0024E910`, `0x0024D9C0`,
   `0x00331920(1)`, `0x002EF5F0`, `0x002DDE60`; `0x003636A0`, `0x00363750` (which unbinds the map sound list) and
   `0x00363E40(0)` are map-sound calls ([map sounds](../Sound-And-Music/map-sounds.md)).

The other title byte has one writer: the script verb `softwarereset` (`0x3E2`, handler `0x0034EB20`,
a jump to `0x003603D0`, which sets `0x022CB72A = 1`). `0x00360370` clears every byte of the block at boot
(`0x0022A39E` in `0x0022A0B0`). The title screen's own start-up after the teardown belongs to the boot path, outside this page.

### Nothing is reloaded, and where a load puts the party

No step of the chain loads a save, revives a party member or jumps to another field. The save
payload's transition record is untouched: `+0x1044` is the field the party was in and `+0x1048`
the entrance it arrived by (`0x003148B0`; written only by `setnowjumpindex`, `0x0034AC10` to
`0x00314D80`). A load restores that record, and the field start places the party through
`0x0037B4D0`, which calls `0x00377A90` (`0x0037BF67`), reads `+0x1048` and resolves it with
`0x00377AB0` and `0x00264B90(0, 0, entrance)`; the position and angle go to `0x0031BAC0` (`0x0037BFA6`).

`0x00264B90(list, manager, entrance, x, y, z, angle)` turns an alias into an entry of the field header's
entrance list: `-1` becomes the header's short `+0x52`, `-2` the short `+0x78` (the save-crystal
entrance), `-3` the short `+0x7A`, any other negative `+0x52`. The entry is 0x20 bytes from the
list at `+0x54` (list 0) or `+0x84` (list 1), with `x`, `y`, `z` at `+4`, `+8`, `+0x0C` and the
angle at `+0x10`. When the entrance does not exist `0x00377AB0` falls back to
`[[0x0209A678]] + 0x28` and `+0x2C` when `0x02ADD0D8` is set, else to zero.

In full, `0x00264B90` first zeroes its four outputs (`0x00264BBE`-`0x00264BD8`). The header is
`[0x02098E10 + 0x288 × manager]`, and a null header answers 0 (`0x00264BE3`). The alias tests run in that order
on the replaced value, so a `+0x52` of -2 goes on to `+0x78`, and an entrance still negative after the
last `+0x52` read becomes 0 (`0x00264BEE`-`0x00264C1F`).

A header whose first word is 2 or less answers 0 (`0x00264C23`), and so do a list offset that decodes to 0 and
an entrance not below the list's first dword, its count (`0x00264C3D`-`0x00264C49`). Any non-zero `list` takes
`+0x84`; the list is the header plus the low 32 bits of the decoded offset (`0x00264C42`-`0x00264C44`). Success
answers 1.

`0x00377AB0(entrance, out)` resolves through `0x00264B50`, which is `0x00264B90(0, 0, entrance, ...)`, into
`out + 0` to `out + 0x0C` (`0x00377AC5`-`0x00377AE5`). Its fallback writes `+0x28` to `x` and `+0x2C` to `z`
only while a map is bound (`0x0209A670`) and `[[0x0209A678]]` is non-null, and 0 otherwise; `y` and the angle
are 0 (`0x00377AEE`-`0x00377B35`). On every path the angle goes through `0x003A1C50` (`0x00377B37`-`0x00377B4A`).

The crystal script sets `setnowjumpindex(-2)` around the save screen and restores the real
entrance afterwards. On field 403, Valley of the Dead, while the story counter is below 1,345, it heals the party
again instead and keeps the entrance ([save and teleport crystals](save-and-teleport-crystals.md)). Slot 0 is the
field-transition autosave and a manual save cannot choose it
([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).

KO is cleared by the crystal, never by the game over. `healall(n)` (`0x3AF`, `0x00356500`) maps its
argument with `0x00359C60` (1 to 7, 2 to `0x0F`, 3 to 4, 4 to `0x0C`, 5 to `0x10`, anything else to
7) and runs `0x0030F4B0(-1, mask)`: bit `0x1` restores HP, bit `0x2` restores MP, bit `0x4` removes the statuses
in `0x0208D320`, bit `0x8` those in `0x0208D324`, and `0x10` also removes `0x544`.

`0x00237CA0` builds the two groups at start-up: status `i` goes to `0x0208D320` when its status-table
row has bit `0x2000` of the word at `+6`, else to `0x0208D324`. It zeroes both groups first (`0x00237CCA`) and walks
statuses 0 to 31, setting bit `1 << i` (`0x00237D36`). The row is the decoded `[0x02EBF118] + 0x0C` plus `i` times
the word `+0x08`, added in 32 bits (`0x00237D09`-`0x00237D22`); with the table or its decoded rows missing it reads
`+6` of address 0 and faults (`0x00237D26`-`0x00237D28`).

KO's row carries `0xA0DF`, so `healall(0)`
revives ([the thirty-two statuses](../Status-Effects-And-KO/statuses.md)). The
crystal also calls `btladjustsystem(1)` (`0x517`, `0x0034AAB0` to `0x002FEAC0`), which with bit `0x1` set
clears `0x022C3178` bit `0x1`, zeroes `0x022C3170`, `0x022C3160` and `0x022C3158` and sets `0x022C3168` to -1.

## Layouts

Root block [`0x0209AC30`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0B8` | `void*` |  | mode-screen task |
| `+0x0C0` | `void*` |  | area controller (`0x00280A00` refuses while set) |
| `+0x0D0` | `void*` |  | pause task `0x00228C70` |
| `+0x3FC` | `i32` |  | requested field (`0x00285EC0`) |
| `+0x400` | `u32` |  | bit `0x100` field request pending; bits `0x200`/`0x400` restore pending/verified; bit `0x800` cleared by `0x0027F2E0`; bit `0x2000` set by `0x00285EA0`; low byte rewritten by `0x0027F2E0` |
| `+0xDEE` | `u8` |  | cleared by `0x0027EFA0` |
| `+0xDEF` | `u8` |  | 1 while a mode screen opens, 0 after the controller's message |

Struct GameOverTask size=`0x108`   (`0x00244F50`(`0x108`, `0x003EF830`, 0); `0x02B5F1C8` points at it):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0B4` | `u32` |  | tick handle (`0x001EDEC0`) |
| `+0x0C0` | `i32` |  | state 0..8 |
| `+0x0C4` | `i32` |  | countdown frames |
| `+0x0D0` | `void*` |  | image task `0x003EF2E0` |
| `+0x0D8` | `void*` |  | timing task `0x003EEEC0` |
| `+0x0E0` | `void*` |  | logo task `0x003EF4A0` |
| `+0x0E8` | `void*` |  | prompt task `0x003EF050` |
| `+0x0F0` | `i32` |  | 1 once message `0x10` arrived |
| `+0x0F8` | `reg` |  | texture registration (`0x00393460`) |
| `+0x100` | `void*` |  | gameover.mrp buffer (`0x003933F0`) |

Struct ImageSlot base=`0x022CB9F0` count=4 size=`0x18`   (`0x00361630` loads, `0x00360C20` reads, `0x00360D70` releases):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | state: 0 free, 3 loading, 4 loaded, 5 ready; `0x00360D70` releases state 5 and flags the rest (a state-5 slot gets `0x002DEDE0`(id), `0x002DEC20`(id) and state 0; other used slots get flags bit `0x1`) `0x00361630`(id): -1 for a negative id; a used slot with the id gets flags bits `0x1` and `0x2` cleared and returns `+0x03`; else the first free slot, only when it is slot 0 or 1 (`0x0036169A`), gets state 3, the id, `+0x08` = 0, `+0x10` = 0, `+0x14` = `0x002DEC70`(id), cleared flags and state 4, and returns `+0x03`; otherwise -1. `0x00360C20`(id): the state of the used slot holding the id, or -1 |
| `+0x01` | `u8` |  | image id (7 = gameover_c) |
| `+0x02` | `u8` |  | flags: bit `0x1` release requested, bit `0x2` fading (`0x00361200`) |
| `+0x03` | `u8` |  | result byte returned by `0x00361630` |
| `+0x08` | `void*` | payload |  |
| `+0x14` | `u32` |  | handle from `0x001DBB80`(id) |

Title-return bytes:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022CB720` | `u32` |  | busy mask (0 = idle; `0x003321E0` refreshes bit `0x80`; `0x00360100` and `0x00360370` clear it, `0x003601B0`/`0x003601C0` modify) |
| `0x022CB724` | `u16` |  | written `0x5A` by `0x00360120` |
| `0x022CB726` | `u8` |  | 1 after the teardown |
| `0x022CB727` | `u8` |  | cleared by `0x00360120` |
| `0x022CB72A` | `u8` |  | softwarereset request (`0x003603D0`) |
| `0x022CB728` | `u16` |  | cleared by `0x00360370` (`0x0036037E`), read by `0x003603B0` |
| `0x022CB72B` | `u8` |  | title-map request (`0x003603E0`, from the area controller when `+0x3FC` is `0x0C`) |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022CB724` | `u16` |  | 90 (`0x5A`), stored as a word every main-loop pass by `0x00360120` (`0x00360135`) and at boot by `0x00360370` (`0x0036039C`); read by no instruction |
| `0x022CB727` | `u8` |  | 0, stored by `0x00360120` (`0x0036013C`), `0x003601D0` (`0x003602AB`) and `0x00360370` (`0x00360385`); read by no instruction |

Request and mode:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x0215F1A0` | `u8` |  | request pending |
| `0x0215F1A1` | `u8` |  | latch that refuses `0x002E1B10` |
| `0x0215F1A4` | `u32` |  | request id |
| `0x0215F1A8` | `u32` |  | request parameter |
| `0x02092730` | `u32` |  | current mode |
| `0x02092734` | `u32` |  | mode parameter |
| `0x020927D8` | `u32` |  | raw mode |
| `0x022C83E8` | `u32` |  | bit `0x100` game over posted, bit `0x2` armed, bit `0x1` and bit `0x10` the `0x18` and `0x17` posts |
| `0x00254C70` | `u8[]` |  | mode-request arm table (id - 1 → arm) |
| `0x00254C58` | `u32[6]` |  | arm jump table |

## Shipped data

| Fact | Value |
|---|---|
| `healall` calls in the 1,114 us zone scripts | `healall(0)` 1,228 in 184 scripts; `healall(5)` 903 in 103; `healall(2)` 20 in 18 |
| `setnowjumpindex(-2)` | 1,146 calls in 183 scripts: the 81 crystal scripts and 102 others, each around a save screen |
| save screens opened (`openfullscreenmenu_48d(0x8005, …)`) | 1,148 calls |
| `mapjump` calls | 7,356; no call passes a negative entrance, so the `-2` alias is only ever set through `setnowjumpindex` |
| GAME OVER image | `gameover_c.tm2` under each language's `Tm2_Menu` folder; image id 7 in the slot table |
| pause texts | `0x85F` "This will return you to the title screen. Are you sure?", `0x890` "This will close FINAL FANTASY XII THE ZODIAC AGE. Are you sure?" |
| title map | field `0x0C` is `ttl_a01` ([zone changes](zone-changes-and-mapjump.md)) |
| display count before the prompt | `0x564`, `0x3DE` or `0x3A2` frames by `0x002DDCA0()` = 1, 2 or other |

## Operations

A wipe, in order: the field frame posts `0x0B`; `0x0035C7B0` halts the actors, writes the request and
locks input; the UI consumer runs the executor; the executor opens the mode screen, which spawns
the game-over task; the task fades the music and the field, loads and shows the GAME OVER image,
runs the logo, waits for the display count or a button, fades to black and calls `0x00285EC0(0x0C)`;
the area controller sets `0x022CB72B`; the main loop's `0x00360120` tears the field down and hands over
to the title screen.

A menu death takes the second route: `0x00254E50` to `0x002805D0` to `0x0027EFA0`, which posts `0x0B`
without the field frame and starts the task itself.

The pause screen's return takes the short route: `0x00228C70` fades and calls `0x00285EC0(0x0C)`; the
rest is the same.

## State

The root block's `+0x3FC`, `+0x400`, `+0xDEE` and `+0xDEF`; the request bytes `0x0215F1A0` to
`0x0215F1A8`; `0x022C83E8` bits `0x2` and `0x100`; the mode words `0x02092730`, `0x02092734` and `0x020927D8`; the
game-over task, its four helpers and `0x02B5F1C8`; the image slot table; the title bytes `0x022CB720`
to `0x022CB72B`; the layer mask `0x0215EFD8`; the input groups locked by `0x00254850` and `0x00254940`; the
actors' halt class `0x16`; `0x022C3158` to `0x022C3178` after a crystal touch.

## Modding notes

- A respawn has to intercept before `0x0035C7B0(0x0B, …)`: once the request byte is written the chain
  runs to the title screen with no hook that reloads or revives. `0x002E1B10` refuses while
  `0x0215F1A1` is set, which is the one latch on the post.
- Field `0x0C` is never a zone change on this path. A detour that watches `0x00314440` for the return
  to the title screen sees nothing; watch `0x003603E0` or `0x022CB72B` instead.
- "Respawn at the last crystal" has no native field: the crystal-touch point is the verb handler
  `0x0034AAB0`, run once per crystal confirm and only from the crystal actor; record
  `(+0x1044, -2)` there and request `mapjump(field, -2, mode)` through the zone-change funnel.
- No shipped script passes a literal negative entrance to `mapjump`: the 59,674 literal entrances in the
  10,036 listings (every language tree, the developer events and the developer menus) are 0 to 34, and the
  other 6,640 calls pass a variable or `nowjumpindex()`.
- "Entrance of the last zone entered" is `(+0x1044, +0x1048)` read at death; scripts rewrite
  `+0x1048` freely and it may hold an alias.
- Whether a party can get back to a crystal has no native answer: exits are authored scripts,
  collision and story flags. Native facts that can stand in: the persistence group of the
  crystal's field against `+0x1044`, the teleport-off bit, the jump lock.
- The pause task's quit (`0x001E0FB0(0)`) and `softwarereset` share nothing with the game over except
  the title bytes; a hook on `0x00360120` catches all three returns.

## Related

- [When the game is over](../Status-Effects-And-KO/ko-and-game-over.md): the four wipe predicates and the post.
- [Zone changes](zone-changes-and-mapjump.md): the transition record, `0x00314440`, the busy mask and the file table.
- [Save and teleport crystals](save-and-teleport-crystals.md): the heal, the save screen and the `-2` alias.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): slot 0 and the autosave.
- [UI request router](../Menus-And-HUD/menus.md): the area controller's messages.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md): KO's row and the status groups.
- [Boss fights](../Battle-Actions/boss-fights.md): the jump lock that keeps a party in a fight.
- [The screen-fade layers](../Graphics/screen-fades.md): `0x002EFA70`.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat formula: `0x00307300` calls `0x002FEE20`, `0x00300CE0`, `0x0030DAE0`, `0x003112F0`, `0x00320A40`, `0x00385F60`; `0x00319F50`
  calls `0x00300520`, `0x00385F60`; those functions are documented on
  [area of effect](../Battle-Actions/area-of-effect.md),
  [save and teleport crystals](save-and-teleport-crystals.md), [traps](traps.md),
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md).
