---
title: "Game over: what a party wipe does, the GAME OVER screen, and the return to the title map"
kind: "system"
category: "World, areas and travel"
addresses: "00234590, 0035C7A0, 0035C7B0, 00227370, 002E1B10, 00254850, 00254E50, 002805D0, 0027EFA0, 002E09A0, 00254B50, 0028F970, 00280A00, 00252B40, 0027FB70, 00280140, 003EF750, 003EF830, 003EFAA0, 003EF2E0, 003EEEC0, 003EF4A0, 003EF050, 003EF680, 003EF770, 003EF290, 00361630, 00360C20, 003611F0, 00360D70, 002DDCA0, 002EFA70, 00285EC0, 00285EA0, 003603E0, 003603D0, 0034EB20, 00360120, 003601D0, 003321E0, 0022A770, 0022BC20, 00228C70, 0027F2E0, 00264B90, 00377AB0, 00377A90, 0037B4D0, 00356500, 00359C60, 0030F4B0, 00237CA0, 0034AAB0, 002FEAC0, 00314DC0, 00314D80, 0034AC10"
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

The field frame `00234590` checks the party every frame and, when it is wiped, posts mode `0B`<sub>h</sub>
through `0035C7A0(0Bh)` and `0035C7B0(0Bh, 1)`; the four wipe predicates and the post are on
[when the game is over](../Status-Effects-And-KO/ko-and-game-over.md).
`0035C7B0` refuses while a request is already pending: `022C83E8` bit 8, a mode `02092730` of
`0B`<sub>h</sub> or `18`<sub>h</sub>, or the request byte `0215F1A0`. Otherwise it runs five steps:

1. sets `022C83E8` bit 8;
2. halts every actor record with class `16`<sub>h</sub> through `00227370` (skipped when `01FD46D4` bit 22 is
   set);
3. writes the request `0215F1A0 = 1`, `0215F1A4 = 0Bh`, `0215F1A8 = 0` through `002E1B10(0Bh, 0)`,
   unless the latch `0215F1A1` is set;
4. sets `022C83E8` bit 1;
5. locks the input group with `00254850(1)`.

A second route needs no field frame. The main loop (`0022A770`) calls `00254E50` once per tick,
which asks `002805D0`: when `0035C740()` is non-zero, a mode-screen task is up and the current mode
`02092730` is one of 6, `0A`<sub>h</sub>, `0F`<sub>h</sub>, `11`<sub>h</sub>, `12`<sub>h</sub>, `13`<sub>h</sub>, or 2 with a sub-id outside
`40`<sub>h</sub> to `42`<sub>h</sub>, it runs `0027EFA0`. That body fades (`002EFA70(3, 0, 1, 0)` when `002EFD20(3)` is
non-zero), calls `0035C7B0(0Bh, 0)` and `00252B40(0Bh, 1)`, clears `[0209AC30] + DEEh`, runs
`00251E80`, sets `+DEFh = 1` and starts the game-over task directly with `003EF750` (`0027F02A`).

### From the request to the screen

The UI request consumer `002E09A0` reads `0215F1A0` in its closing block and calls
`00254B50([0215F1A4], [0215F1A8], 0)`, then clears the byte. `00254B50(id, p2, p3)` indexes the byte
table at `00254C70` with `id - 1`: entry 10 is 5, and the jump table at `00254C58` sends 5 to the
default arm `00254C2D`, which runs `0028F970()` (clears bits 4 and 10 of the menu state dword at
`[0209BE80] + 10F68h`) and then `00280A00(0Bh, 0, 0)`.

`00280A00(mode, p2, p3)` opens a mode screen only when the root block's `+C0`<sub>h</sub> and `+B8`<sub>h</sub> are
both null. It stores the mode with `00252B40(mode, 1)` (`02092730 = mode & 7FFFh`, `02092734 = p2`,
`020927D8 = mode`), spawns the mode-screen task `0027FB70` and the area controller `00280140`
(`D8`<sub>h</sub> bytes each) and runs `0028CA30`. The create arm of `0027FB70` for mode `0B`<sub>h</sub> sets
`[0209AC30] + DEFh = 1` and calls `003EF750` (`0027FFC3`), which is
`00244F50(108h, 003EF830, 0)`: the game-over task. Those are the only two callers of `003EF750`.

### The game-over task and its helpers

`003EF830` is a task of `108`<sub>h</sub> bytes. Its create arm:

1. stores itself at `02B5F1C8`;
2. registers the `gameover_c` texture through the two descriptors at `00D11C88` and `00D11CA0`
   (`00393460` and `003933F0`; the descriptor names the string at `00D11CD0`, the file is
   `Tm2_Menu\gameover_c.tm2` in each language folder);
3. attaches itself to the list `0208EA28` with priority 100 and runs `003678F0`;
4. spawns two helpers of `D0`<sub>h</sub> bytes: the image task `003EF2E0` at `+D0`<sub>h</sub> and the timing task
   `003EEEC0` at `+D8`<sub>h</sub>.

Its tick (`001EDEC0` on `+B4`<sub>h</sub>) runs the state machine `003EFAA0`. Message `10`<sub>h</sub> sets `+F0h = 1`;
message `8001`<sub>h</sub> kills the prompt task at `+E8`<sub>h</sub>; message `12`<sub>h</sub> with payload 1, 2 or 3 clears the
helper pointer `+D8`<sub>h</sub>, `+E0`<sub>h</sub> or `+E8`<sub>h</sub>.

The image task `003EF2E0` fades the music with `002DEE50(002DEC00(), 30)`, fades the loaded images
over 30 frames (`003611F0(1Eh)`) and sets the fade rate `003634B0(3Ch)`. Its states:

- state 0 counts down 15 frames, runs `00363560` and `0024D050`, and once `002F1A30(1)` is 0 loads
  image 7 with `00361630(7)`: a slot of the four-entry image table at `022CB9F0` (Layouts); when
  no slot is free (`-1`) it releases every slot with `00360D70` and retries from state 1;
- state 2 waits until the slot's state byte is 5 (`00360C20(7)`); state 3 is "ready";
- state 4 counts down and then sets its end flag `+C4`<sub>h</sub> bit 0;
- state 6 waits for `002F1A30(1)` to be 0 and becomes 7.

The timing task `003EEEC0` starts the screen fade `00251D90(1, 3Ch, 78h)`, waits until
`00251D20()` is above 2, then 18 frames, plays `002C99A0(1000, 8)` and sends the parent message
`13`<sub>h</sub> with payload 1; 60 frames later it reaches its end state. It forwards messages `0F`<sub>h</sub> and
`12`<sub>h</sub> to the parent with payload 1.

### The state machine

`003EFAA0` runs when the countdown `+C4`<sub>h</sub> is 0 or has just reached 0. Message `13`<sub>h</sub> from the
helpers (`003EF770`) moves it: payload 1 puts it in state 1, payload 2 spawns the prompt task
`003EF050` (`D8`<sub>h</sub> bytes) at `+E8`<sub>h</sub> and goes to state 3, payload 3 goes to state 4.

1. State 1 waits until the image slot is ready (image task state 3) and message `10`<sub>h</sub> has
   arrived (`+F0`<sub>h</sub>). It then spawns the logo task `003EF4A0` (`D0`<sub>h</sub> bytes, widget `002432B0` from
   the descriptor at `00D11CA8`) at `+E0`<sub>h</sub>, shows image 7 with `002DECE0(7)` and goes to state 2.
2. At the same moment the image task enters state 4 with a display count of `564`<sub>h</sub>, `3DE`<sub>h</sub> or
   `3A2`<sub>h</sub> frames when `002DDCA0()` returns 1, 2 or anything else; that is the word at
   `[0215E6E0] + 0Eh`, a 2 downgraded to 1 when `0017E490()` has bit 0 clear.
3. The logo task waits 18 frames, then, once `+F0`<sub>h</sub> is set, attaches to the parent's list; when it
   ends it sends `13`<sub>h</sub> with payload 2, which spawns the prompt task.
4. The prompt task `003EF050` ends the screen on message 10 when the image task's end flag is set
   or a button in the mask `FF09`<sub>h</sub> of `02F9736A` is pressed: it sends `8001`<sub>h</sub> to the parent, which
   kills it.
5. Message `0F`<sub>h</sub> with payload 3 runs `003EF680`: the logo task is killed, `00250C50(100)` and
   `00251EA0(0.8, 78h)` run, the timing task is set to state 4 for 180 frames and, unless the image
   task has already ended, the music fades over 120 frames and the images over 240
   (`003611F0(F0h, 1)`, `003634B0(F0h, 0)`, image state 6). The parent waits 60 frames and goes to
   state 5.
6. State 5 fades layer 2 to black over 60 frames (`002EFA70(2, 3Ch, 0)`), waits 120 frames and goes
   to 6. State 6 runs `003EF290(image, 1)` when the image task's end flag is set (a one-frame music
   fade and a two-frame image fade), then 7. State 7 waits for image task state 7 and destroys it
   (`00244F00`), then 8.
7. State 8, once `+D8`<sub>h</sub>, `+E0`<sub>h</sub> and `+E8`<sub>h</sub> are all null, destroys the task itself and calls
   `00285EC0(0Ch)` (`003EFB32`).

The teardown message `12`<sub>h</sub> unregisters the two textures (`00393900`, `003938B0`), releases the
input locks `00254850(0)` and `00254940(0)` and runs `0027F2E0`.

`0027F2E0` takes a length of 1 when bit 11 of `[0209AC30] + 400h` is set and 200
otherwise (`0027F2ED`-`0027F301`), closes menu slot 0 over it (`002C98C0` at `0027F306`), steps the
mode-screen backdrop `020927F0` toward its fade (`00250F30` at `0027F30B`), fades fade slot 3 in over length × 60 / 1000 frames when the
length is above 1 and slot 3 is active (`002CC960` at `0027F312`; `002EFD20(3)`, `002EFA70(3, n, 1)`).

It then rewrites the low byte of `[0209AC30] + 400h` from its bits 9 and 10 (2 when bit 9 is clear, 1 when bit 9 is set and bit 10
clear, 2 when both are set) and clears bit 11.

### The request for the title map, and what it really does

`00285EC0(field)` sets `[0209AC30] + 400h` bit 8 and writes `+3FCh = field`. Its callers are the
game-over task (`003EFB32`, field `0C`<sub>h</sub>) and the pause task `00228C70` (`002291B1`, field `0C`<sub>h</sub>).

The pause task shows "This will return you to the title screen. Are you sure?" (menu text `85F`<sub>h</sub>,
key `114`<sub>h</sub>) or "This will close FINAL FANTASY XII THE ZODIAC AGE" (text `890`<sub>h</sub>, key `115`<sub>h</sub>). A
confirmed return fades (`002EFA70(2, 18h, 0)`), waits for `002EFD20(2)` to report 2 and calls
`00285EC0(0Ch)`; a confirmed quit calls `001E0FB0(0)`. The same task's skip path calls
`00285EA0(1)`, which sets bit 13 of `+400`<sub>h</sub>
([the native command lifecycle](../Scripts-And-Script-Commands/native-commands.md)).

The consumer is the area controller `00280140`, in its message `12`<sub>h</sub> arm (`00280248` to
`0028027C`): with bit 8 set it clears the bit and tests `+3FC`<sub>h</sub> against `0C`<sub>h</sub>. For `0C`<sub>h</sub> it
calls `003603E0`, which sets the byte `022CB72B = 1`; for any other field it runs `002CFD10(-1)`
and `00314440(+3FCh, 0, 0, 0)`, a real field transition
([zone changes](zone-changes-and-mapjump.md)). Then `00251E80`, `00252D90`,
`[0209AC30] + DEFh = 0` and `+C0h = 0`. So the title map, field `0C`<sub>h</sub> (`ttl_a01`), is never
requested as a zone change after a game over; a title-return byte is set instead.

### The main loop tears the field down

`00360120` runs every main-loop iteration (`0022A977` and `0022AE00` in `0022A770`, and `0022BDDB` in
the re-initialisation `0022BC20`). It refreshes the busy mask's bit 7 with `003321E0`, writes
`022CB724 = 5Ah` and `022CB727 = 0`, and when the busy mask `022CB720` is 0 and either title byte
`022CB72A` or `022CB72B` is set, it runs the resume routine `003601D0` and then `0017F740(0)`,
`001EC4B0(1)`, `001EC4B0(2)`, `001830A0(1)`, `00382B50(-1, 0, 0)`, `00182810(1)` and `00357B00`
(`022C7F80 = 0`).

`003601D0` is the field teardown, in this order:

1. both speed scales to 1.0 (`00229EF0`, `00229EE0`), `00368AC0(0)`, `0032E520(0)`, `0035EA30(0)`,
   `0053DD10(1)`;
2. for managers 0 to 2 with `+10`<sub>h</sub> bit 0, the jump lock `+200`<sub>h</sub> bit 0 is cleared;
3. `002DEE90(-1)`, `003634A0(0)`, `003633B0(0)`, `00362850`, `002DF0F0(0, -1)`, `002DF060`,
   `001DC330(-1)`, `002DEB90(1)`, `005C5230`: the sound teardown, in which `002DF0F0(0, -1)` and
   `001DC330(-1)` are the audio manager's stop calls for sounds and for voices, and `002DEE90(-1)` calls
   `0035EA30(0)` until `001DBD00` returns 0 ([audio manager](../Sound-And-Music/audio-manager.md));
4. the layer mask bits 2 to 4 are cleared through `002DF370(1Ch, 0, 1)` and every image slot is
   released (`00360D70`);
5. `022CB726 = 1`; `022CB727`, `022CB72A` and `022CB72B` are cleared;
6. `002EF840(0)` to `002EF840(6)`, `002F1A70`, `003DE210`, `003DE0A0`, `002EFE40(6)`,
   `002EFE50(FFh)`, `002EFA70(2, 0, 0, 0)`, `002EFA70(3, 0, 1)`;
7. `002E06B0`, `003636A0`, `00363750`, `00363E40(0)`, `0036DF30`, `0024E910`, `0024D9C0`,
   `00331920(1)`, `002EF5F0`, `002DDE60`; `003636A0`, `00363750` (which unbinds the map sound list) and
   `00363E40(0)` are map-sound calls ([map sounds](../Sound-And-Music/map-sounds.md)).

The other title byte has one writer: the script verb `softwarereset` (`3E2`<sub>h</sub>, handler `0034EB20`,
a jump to `003603D0`, which sets `022CB72A = 1`). `00360370` clears every byte of the block at boot
(`0022A39E` in `0022A0B0`). The title screen's own start-up after the teardown belongs to the boot path, outside this page.

### Nothing is reloaded, and where a load puts the party

No step of the chain loads a save, revives a party member or jumps to another field. The save
payload's transition record is untouched: `+1044`<sub>h</sub> is the field the party was in and `+1048`<sub>h</sub>
the entrance it arrived by (`003148B0`; written only by `setnowjumpindex`, `0034AC10` to
`00314D80`). A load restores that record, and the field start places the party through
`0037B4D0`, which calls `00377A90` (`0037BF67`), reads `+1048`<sub>h</sub> and resolves it with
`00377AB0` and `00264B90(0, 0, entrance)`; the position and angle go to `0031BAC0` (`0037BFA6`).

`00264B90(list, manager, entrance, out)` turns an alias into an entry of the field header's
entrance list: `-1` becomes the header's short `+52`<sub>h</sub>, `-2` the short `+78`<sub>h</sub> (the save-crystal
entrance), `-3` the short `+7A`<sub>h</sub>, any other negative `+52`<sub>h</sub>. The entry is `20`<sub>h</sub> bytes from the
list at `+54`<sub>h</sub> (list 0) or `+84`<sub>h</sub> (list 1), with `x`, `y`, `z` at `+4`, `+8`, `+0C`<sub>h</sub> and the
angle at `+10`<sub>h</sub>. When the entrance does not exist `00377AB0` falls back to
`[[0209A678]] + 28h` and `+2C`<sub>h</sub> when `02ADD0D8` is set, else to zero.

The crystal script sets `setnowjumpindex(-2)` around the save screen and restores the real
entrance afterwards ([save and teleport crystals](save-and-teleport-crystals.md)). Slot 0 is the
field-transition autosave and a manual save cannot choose it
([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).

KO is cleared by the crystal, never by the game over. `healall(n)` (`3AF`<sub>h</sub>, `00356500`) maps its
argument with `00359C60` (1 to 7, 2 to `0F`<sub>h</sub>, 3 to 4, 4 to `0C`<sub>h</sub>, 5 to `10`<sub>h</sub>, anything else to
7) and runs `0030F4B0(-1, mask)`: bit 0 restores HP, bit 1 restores MP, bit 2 removes the statuses
in `0208D320`, bit 3 those in `0208D324`, and `10`<sub>h</sub> also removes `544`<sub>h</sub>.

`00237CA0` builds the two groups at start-up: status `i` goes to `0208D320` when its status-table
row has bit 13 of the word at `+6`, else to `0208D324`; KO's row carries `A0DF`<sub>h</sub>, so `healall(0)`
revives ([the thirty-two statuses](../Status-Effects-And-KO/statuses.md)). The
crystal also calls `btladjustsystem(1)` (`517`<sub>h</sub>, `0034AAB0` to `002FEAC0`), which with bit 0 set
clears `022C3178` bit 0, zeroes `022C3170`, `022C3160` and `022C3158` and sets `022C3168` to -1.

## Layouts

Root block [`0209AC30`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0B8`<sub>h</sub> | `void*` | mode-screen task | +`0C0`<sub>h</sub>  ptr   area controller (`00280A00` refuses while set) |
| `0D0`<sub>h</sub> | `void*` | pause task 00228C70 |  |
| `3FC`<sub>h</sub> | `i32` | requested field (00285EC0) |  |
| `400`<sub>h</sub> | `u32` | bit 8 field request pending; bits 9/10 restore pending/verified; bit 11 cleared by 0027F2E0; | bit 13 set by `00285EA0`; low byte rewritten by `0027F2E0` |
| `DEE`<sub>h</sub> | `u8` | cleared by 0027EFA0 | +`DEF`<sub>h</sub>  u8    1 while a mode screen opens, 0 after the controller's message |

Struct GameOverTask size=`108`<sub>h</sub>   (`00244F50`(`108`<sub>h</sub>, `003EF830`, 0); `02B5F1C8` points at it):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `B4`<sub>h</sub> | `u32` | tick handle (001EDEC0) |  |
| `C0`<sub>h</sub> | `i32` | state 0..8 | +`0C4`<sub>h</sub>  i32   countdown frames |
| `D0`<sub>h</sub> | `void*` | image task 003EF2E0 | +`0D8`<sub>h</sub>  ptr   timing task `003EEEC0` |
| `E0`<sub>h</sub> | `void*` | logo task 003EF4A0 | +`0E8`<sub>h</sub>  ptr   prompt task `003EF050` |
| `F0`<sub>h</sub> | `i32` | 1 once message `10`<sub>h</sub> arrived |  |
| `F8`<sub>h</sub> | `reg` | texture registration (00393460) | +`100`<sub>h</sub>  reg   texture registration (`003933F0`) |

Struct ImageSlot base=`022CB9F0` count=4 size=`18`<sub>h</sub>   (`00361630` loads, `00360C20` reads, `00360D70` releases):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | state: 0 free, 3 loading, 4 loaded, 5 ready; 00360D70 releases state 5 and flags the rest |  |
| `01`<sub>h</sub> | `u8` | image id (7 = gameover_c) |  |
| `02`<sub>h</sub> | `u8` | flags: bit 0 release requested, bit 1 fading (00361200) |  |
| `03`<sub>h</sub> | `u8` | result byte returned by 00361630 |  |
| `08`<sub>h</sub> | `void*` | payload | +`14`<sub>h</sub>  u32  handle from `001DBB80`(id) |

Title-return bytes:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `022CB720` | `u8` | busy mask (0 = idle; 003321E0 refreshes bit 7; 00360100 sets, 003601B0/003601C0 modify, 00360370 clears) |  |
| `022CB724` | `u32` | written `5A`<sub>h</sub> by 00360120 | `022CB726`  u8   1 after the teardown |
| `022CB727` | `u8` | cleared by 00360120 | `022CB72A`  u8   softwarereset request (`003603D0`) |
| `022CB72B` | `u8` | title-map request (003603E0, from the area controller when `+3FC`<sub>h</sub> is `0C`<sub>h</sub>) |  |

Request and mode:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0215F1A0` | `u8` | request pending | `0215F1A1`  u8  latch that refuses `002E1B10` |
| `0215F1A4` | `u32` | request id | `0215F1A8`  u32  request parameter |
| `02092730` | `u32` | current mode | `02092734`  u32  mode parameter     `020927D8`  u32  raw mode |
| `022C83E8` | `u32` | bit 8 game over posted, bit 1 armed, bit 0 and bit 4 the `18`<sub>h</sub> and `17`<sub>h</sub> posts |  |
| `00254C70` | `u8[]` | mode-request arm table (id - 1 → arm) | `00254C58`  u32[6]  arm jump table |

## Shipped data

| Fact | Value |
|---|---|
| `healall` calls in the 1,114 us zone scripts | `healall(0)` 1,228 in 184 scripts; `healall(5)` 903 in 103; `healall(2)` 20 in 18 |
| `setnowjumpindex(-2)` | 1,146 calls in 183 scripts: the 81 crystal scripts and 102 others, each around a save screen |
| save screens opened (`openfullscreenmenu_48d(8005h, …)`) | 1,148 calls |
| `mapjump` calls | 8,881; none passes a negative entrance, so the `-2` alias is only ever set through `setnowjumpindex` |
| GAME OVER image | `gameover_c.tm2` under each language's `Tm2_Menu` folder; image id 7 in the slot table |
| pause texts | `85F`<sub>h</sub> "This will return you to the title screen. Are you sure?", `890`<sub>h</sub> "This will close FINAL FANTASY XII THE ZODIAC AGE. Are you sure?" |
| title map | field `0C`<sub>h</sub> is `ttl_a01` ([zone changes](zone-changes-and-mapjump.md)) |
| display count before the prompt | `564`<sub>h</sub>, `3DE`<sub>h</sub> or `3A2`<sub>h</sub> frames by `002DDCA0()` = 1, 2 or other |

## Operations

A wipe, in order: the field frame posts `0B`<sub>h</sub>; `0035C7B0` halts the actors, writes the request and
locks input; the UI consumer runs the executor; the executor opens the mode screen, which spawns
the game-over task; the task fades the music and the field, loads and shows the GAME OVER image,
runs the logo, waits for the display count or a button, fades to black and calls `00285EC0(0Ch)`;
the area controller sets `022CB72B`; the main loop's `00360120` tears the field down and hands over
to the title screen.

A menu death takes the second route: `00254E50` to `002805D0` to `0027EFA0`, which posts `0B`<sub>h</sub>
without the field frame and starts the task itself.

The pause screen's return takes the short route: `00228C70` fades and calls `00285EC0(0Ch)`; the
rest is the same.

## State

The root block's `+3FC`<sub>h</sub>, `+400`<sub>h</sub>, `+DEE`<sub>h</sub> and `+DEF`<sub>h</sub>; the request bytes `0215F1A0` to
`0215F1A8`; `022C83E8` bits 1 and 8; the mode words `02092730`, `02092734` and `020927D8`; the
game-over task, its four helpers and `02B5F1C8`; the image slot table; the title bytes `022CB720`
to `022CB72B`; the layer mask `0215EFD8`; the input groups locked by `00254850` and `00254940`; the
actors' halt class `16`<sub>h</sub>; `022C3158` to `022C3178` after a crystal touch.

## Modding notes

- A respawn has to intercept before `0035C7B0(0Bh, …)`: once the request byte is written the chain
  runs to the title screen with no hook that reloads or revives. `002E1B10` refuses while
  `0215F1A1` is set, which is the one latch on the post.
- Field `0C`<sub>h</sub> is never a zone change on this path. A detour that watches `00314440` for the return
  to the title screen sees nothing; watch `003603E0` or `022CB72B` instead.
- "Respawn at the last crystal" has no native field: the crystal-touch point is the verb handler
  `0034AAB0`, run once per crystal confirm and only from the crystal actor; record
  `(+1044h, -2)` there and request `mapjump(field, -2, mode)` through the zone-change funnel. No
  shipped script passes a negative entrance to `mapjump`, so that path is unexercised.
- "Entrance of the last zone entered" is `(+1044h, +1048h)` read at death; scripts rewrite
  `+1048`<sub>h</sub> freely and it may hold an alias.
- Whether a party can get back to a crystal has no native answer: exits are authored scripts,
  collision and story flags. Native facts that can stand in: the persistence group of the
  crystal's field against `+1044`<sub>h</sub>, the teleport-off bit, the jump lock.
- `healall` and the crystal are zone-script rows: on a mirror they run untouched; supply the missing
  counterpart rather than suppressing them.
- The pause task's quit (`001E0FB0(0)`) and `softwarereset` share nothing with the game over except
  the title bytes; a hook on `00360120` catches all three returns.

## Related

- [When the game is over](../Status-Effects-And-KO/ko-and-game-over.md): the four wipe predicates and the post.
- [Zone changes](zone-changes-and-mapjump.md): the transition record, `00314440`, the busy mask and the file table.
- [Save and teleport crystals](save-and-teleport-crystals.md): the heal, the save screen and the `-2` alias.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): slot 0 and the autosave.
- [UI request router](../Menus-And-HUD/menus.md): the area controller's messages.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md): KO's row and the status groups.
- [Boss fights](../Battle-Actions/boss-fights.md): the jump lock that keeps a party in a fight.
- [The screen-fade layers](../17-Presentation-Rendering/screen-fades.md
): `002EFA70`.
