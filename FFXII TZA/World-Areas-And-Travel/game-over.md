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
`0x0035C7B0` refuses while a request is already pending: `0x022C83E8` bit 8, a mode `0x02092730` of
`0x0B` or `0x18`, or the request byte `0x0215F1A0`. Otherwise it runs five steps:

1. sets `0x022C83E8` bit 8;
2. halts every actor record with class `0x16` through `0x00227370` (skipped when `0x01FD46D4` bit 22 is
   set);
3. writes the request `0x0215F1A0 = 1`, `0x0215F1A4 = 0x0B`, `0x0215F1A8 = 0` through `0x002E1B10(0x0B, 0)`,
   unless the latch `0x0215F1A1` is set;
4. sets `0x022C83E8` bit 1;
5. locks the input group with `0x00254850(1)`.

A second route needs no field frame. The main loop (`0x0022A770`) calls `0x00254E50` once per tick,
which asks `0x002805D0`: when `0x0035C740()` is non-zero, a mode-screen task is up and the current mode
`0x02092730` is one of 6, `0x0A`, `0x0F`, `0x11`, `0x12`, `0x13`, or 2 with a sub-id outside
`0x40` to `0x42`, it runs `0x0027EFA0`. That body fades (`0x002EFA70(3, 0, 1, 0)` when `0x002EFD20(3)` is
non-zero), calls `0x0035C7B0(0x0B, 0)` and `0x00252B40(0x0B, 1)`, clears `[0x0209AC30] + 0xDEE`, runs
`0x00251E80`, sets `+0xDEF = 1` and starts the game-over task directly with `0x003EF750` (`0x0027F02A`).

### From the request to the screen

The UI request consumer `0x002E09A0` reads `0x0215F1A0` in its closing block and calls
`0x00254B50([0x0215F1A4], [0x0215F1A8], 0)`, then clears the byte. `0x00254B50(id, p2, p3)` indexes the byte
table at `0x00254C70` with `id - 1`: entry 10 is 5, and the jump table at `0x00254C58` sends 5 to the
default arm `0x00254C2D`, which runs `0x0028F970()` (clears bits 4 and 10 of the menu state dword at
`[0x0209BE80] + 0x10F68`) and then `0x00280A00(0x0B, 0, 0)`.

`0x00280A00(mode, p2, p3)` opens a mode screen only when the root block's `+0xC0` and `+0xB8` are
both null. It stores the mode with `0x00252B40(mode, 1)` (`0x02092730 = mode & 0x7FFF`, `0x02092734 = p2`,
`0x020927D8 = mode`), spawns the mode-screen task `0x0027FB70` and the area controller `0x00280140`
(`0xD8` bytes each) and runs `0x0028CA30`. The create arm of `0x0027FB70` for mode `0x0B` sets
`[0x0209AC30] + 0xDEF = 1` and calls `0x003EF750` (`0x0027FFC3`), which is
`0x00244F50(0x108, 0x003EF830, 0)`: the game-over task. Those are the only two callers of `0x003EF750`.

### The game-over task and its helpers

`0x003EF830` is a task of `0x108` bytes. Its create arm:

1. stores itself at `0x02B5F1C8`;
2. registers the `gameover_c` texture through the two descriptors at `0x00D11C88` and `0x00D11CA0`
   (`0x00393460` and `0x003933F0`; the descriptor names the string at `0x00D11CD0`, the file is
   `Tm2_Menu\gameover_c.tm2` in each language folder);
3. attaches itself to the list `0x0208EA28` with priority 100 and runs `0x003678F0`;
4. spawns two helpers of `0xD0` bytes: the image task `0x003EF2E0` at `+0xD0` and the timing task
   `0x003EEEC0` at `+0xD8`.

Its tick (`0x001EDEC0` on `+0xB4`) runs the state machine `0x003EFAA0`. Message `0x10` sets `+0xF0 = 1`;
message `0x8001` kills the prompt task at `+0xE8`; message `0x12` with payload 1, 2 or 3 clears the
helper pointer `+0xD8`, `+0xE0` or `+0xE8`.

The image task `0x003EF2E0` fades the music with `0x002DEE50(0x002DEC00(), 30)`, fades the loaded images
over 30 frames (`0x003611F0(0x1E)`) and sets the fade rate `0x003634B0(0x3C)`. Its states:

- state 0 counts down 15 frames, runs `0x00363560` and `0x0024D050`, and once `0x002F1A30(1)` is 0 loads
  image 7 with `0x00361630(7)`: a slot of the four-entry image table at `0x022CB9F0` (Layouts); when
  no slot is free (`-1`) it releases every slot with `0x00360D70` and retries from state 1;
- state 2 waits until the slot's state byte is 5 (`0x00360C20(7)`); state 3 is "ready";
- state 4 counts down and then sets its end flag `+0xC4` bit 0;
- state 6 waits for `0x002F1A30(1)` to be 0 and becomes 7.

The timing task `0x003EEEC0` starts the screen fade `0x00251D90(1, 0x3C, 0x78)`, waits until
`0x00251D20()` is above 2, then 18 frames, plays `0x002C99A0(1000, 8)` and sends the parent message
`0x13` with payload 1; 60 frames later it reaches its end state. It forwards messages `0x0F` and
`0x12` to the parent with payload 1.

### The state machine

`0x003EFAA0` runs when the countdown `+0xC4` is 0 or has just reached 0. Message `0x13` from the
helpers (`0x003EF770`) moves it: payload 1 puts it in state 1, payload 2 spawns the prompt task
`0x003EF050` (`0xD8` bytes) at `+0xE8` and goes to state 3, payload 3 goes to state 4.

1. State 1 waits until the image slot is ready (image task state 3) and message `0x10` has
   arrived (`+0xF0`). It then spawns the logo task `0x003EF4A0` (`0xD0` bytes, widget `0x002432B0` from
   the descriptor at `0x00D11CA8`) at `+0xE0`, shows image 7 with `0x002DECE0(7)` and goes to state 2.
2. At the same moment the image task enters state 4 with a display count of `0x564`, `0x3DE` or
   `0x3A2` frames when `0x002DDCA0()` returns 1, 2 or anything else; that is the word at
   `[0x0215E6E0] + 0x0E`, a 2 downgraded to 1 when `0x0017E490()` has bit 0 clear.
3. The logo task waits 18 frames, then, once `+0xF0` is set, attaches to the parent's list; when it
   ends it sends `0x13` with payload 2, which spawns the prompt task.
4. The prompt task `0x003EF050` ends the screen on message 10 when the image task's end flag is set
   or a button in the mask `0xFF09` of `0x02F9736A` is pressed: it sends `0x8001` to the parent, which
   kills it.
5. Message `0x0F` with payload 3 runs `0x003EF680`: the logo task is killed, `0x00250C50(100)` and
   `0x00251EA0(0.8, 0x78)` run, the timing task is set to state 4 for 180 frames and, unless the image
   task has already ended, the music fades over 120 frames and the images over 240
   (`0x003611F0(0xF0, 1)`, `0x003634B0(0xF0, 0)`, image state 6). The parent waits 60 frames and goes to
   state 5.
6. State 5 fades layer 2 to black over 60 frames (`0x002EFA70(2, 0x3C, 0)`), waits 120 frames and goes
   to 6. State 6 runs `0x003EF290(image, 1)` when the image task's end flag is set (a one-frame music
   fade and a two-frame image fade), then 7. State 7 waits for image task state 7 and destroys it
   (`0x00244F00`), then 8.
7. State 8, once `+0xD8`, `+0xE0` and `+0xE8` are all null, destroys the task itself and calls
   `0x00285EC0(0x0C)` (`0x003EFB32`).

The teardown message `0x12` unregisters the two textures (`0x00393900`, `0x003938B0`), releases the
input locks `0x00254850(0)` and `0x00254940(0)` and runs `0x0027F2E0`.

`0x0027F2E0` takes a length of 1 when bit 11 of `[0x0209AC30] + 0x400` is set and 200
otherwise (`0x0027F2ED`-`0x0027F301`), closes menu slot 0 over it (`0x002C98C0` at `0x0027F306`), steps the
mode-screen backdrop `0x020927F0` toward its fade (`0x00250F30` at `0x0027F30B`), fades fade slot 3 in over length × 60 / 1000 frames when the
length is above 1 and slot 3 is active (`0x002CC960` at `0x0027F312`; `0x002EFD20(3)`, `0x002EFA70(3, n, 1)`).

It then rewrites the low byte of `[0x0209AC30] + 0x400` from its bits 9 and 10 (2 when bit 9 is clear, 1 when bit 9 is set and bit 10
clear, 2 when both are set) and clears bit 11.

### The request for the title map, and what it really does

`0x00285EC0(field)` sets `[0x0209AC30] + 0x400` bit 8 and writes `+0x3FC = field`. Its callers are the
game-over task (`0x003EFB32`, field `0x0C`) and the pause task `0x00228C70` (`0x002291B1`, field `0x0C`).

The pause task shows "This will return you to the title screen. Are you sure?" (menu text `0x85F`,
key `0x114`) or "This will close FINAL FANTASY XII THE ZODIAC AGE" (text `0x890`, key `0x115`). A
confirmed return fades (`0x002EFA70(2, 0x18, 0)`), waits for `0x002EFD20(2)` to report 2 and calls
`0x00285EC0(0x0C)`; a confirmed quit calls `0x001E0FB0(0)`. The same task's skip path calls
`0x00285EA0(1)`, which sets bit 13 of `+0x400`
([the native command lifecycle](../Scripts-And-Script-Commands/native-commands.md)).

The consumer is the area controller `0x00280140`, in its message `0x12` arm (`0x00280248` to
`0x0028027C`): with bit 8 set it clears the bit and tests `+0x3FC` against `0x0C`. For `0x0C` it
calls `0x003603E0`, which sets the byte `0x022CB72B = 1`; for any other field it runs `0x002CFD10(-1)`
and `0x00314440(+0x3FC, 0, 0, 0)`, a real field transition
([zone changes](zone-changes-and-mapjump.md)). Then `0x00251E80`, `0x00252D90`,
`[0x0209AC30] + 0xDEF = 0` and `+0xC0 = 0`. So the title map, field `0x0C` (`ttl_a01`), is never
requested as a zone change after a game over; a title-return byte is set instead.

### The main loop tears the field down

`0x00360120` runs every main-loop iteration (`0x0022A977` and `0x0022AE00` in `0x0022A770`, and `0x0022BDDB` in
the re-initialisation `0x0022BC20`). It refreshes the busy mask's bit 7 with `0x003321E0`, writes
`0x022CB724 = 0x5A` and `0x022CB727 = 0`, and when the busy mask `0x022CB720` is 0 and either title byte
`0x022CB72A` or `0x022CB72B` is set, it runs the resume routine `0x003601D0` and then `0x0017F740(0)`,
`0x001EC4B0(1)`, `0x001EC4B0(2)`, `0x001830A0(1)`, `0x00382B50(-1, 0, 0)`, `0x00182810(1)` and `0x00357B00`
(`0x022C7F80 = 0`).

`0x003601D0` is the field teardown, in this order:

1. both speed scales to 1.0 (`0x00229EF0`, `0x00229EE0`), `0x00368AC0(0)`, `0x0032E520(0)`, `0x0035EA30(0)`,
   `0x0053DD10(1)`;
2. for managers 0 to 2 with `+0x10` bit 0, the jump lock `+0x200` bit 0 is cleared;
3. `0x002DEE90(-1)`, `0x003634A0(0)`, `0x003633B0(0)`, `0x00362850`, `0x002DF0F0(0, -1)`, `0x002DF060`,
   `0x001DC330(-1)`, `0x002DEB90(1)`, `0x005C5230`: the sound teardown, in which `0x002DF0F0(0, -1)` and
   `0x001DC330(-1)` are the audio manager's stop calls for sounds and for voices, and `0x002DEE90(-1)` calls
   `0x0035EA30(0)` until `0x001DBD00` returns 0 ([audio manager](../Sound-And-Music/audio-manager.md));
4. the layer mask bits 2 to 4 are cleared through `0x002DF370(0x1C, 0, 1)` and every image slot is
   released (`0x00360D70`);
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

`0x00264B90(list, manager, entrance, out)` turns an alias into an entry of the field header's
entrance list: `-1` becomes the header's short `+0x52`, `-2` the short `+0x78` (the save-crystal
entrance), `-3` the short `+0x7A`, any other negative `+0x52`. The entry is 0x20 bytes from the
list at `+0x54` (list 0) or `+0x84` (list 1), with `x`, `y`, `z` at `+4`, `+8`, `+0x0C` and the
angle at `+0x10`. When the entrance does not exist `0x00377AB0` falls back to
`[[0x0209A678]] + 0x28` and `+0x2C` when `0x02ADD0D8` is set, else to zero.

The crystal script sets `setnowjumpindex(-2)` around the save screen and restores the real
entrance afterwards ([save and teleport crystals](save-and-teleport-crystals.md)). Slot 0 is the
field-transition autosave and a manual save cannot choose it
([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).

KO is cleared by the crystal, never by the game over. `healall(n)` (`0x3AF`, `0x00356500`) maps its
argument with `0x00359C60` (1 to 7, 2 to `0x0F`, 3 to 4, 4 to `0x0C`, 5 to `0x10`, anything else to
7) and runs `0x0030F4B0(-1, mask)`: bit 0 restores HP, bit 1 restores MP, bit 2 removes the statuses
in `0x0208D320`, bit 3 those in `0x0208D324`, and `0x10` also removes `0x544`.

`0x00237CA0` builds the two groups at start-up: status `i` goes to `0x0208D320` when its status-table
row has bit 13 of the word at `+6`, else to `0x0208D324`; KO's row carries `0xA0DF`, so `healall(0)`
revives ([the thirty-two statuses](../Status-Effects-And-KO/statuses.md)). The
crystal also calls `btladjustsystem(1)` (`0x517`, `0x0034AAB0` to `0x002FEAC0`), which with bit 0 set
clears `0x022C3178` bit 0, zeroes `0x022C3170`, `0x022C3160` and `0x022C3158` and sets `0x022C3168` to -1.

## Layouts

Root block [`0x0209AC30`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0B8` | `void*` | mode-screen task | +`0x0C0`  ptr   area controller (`0x00280A00` refuses while set) |
| `+0x0D0` | `void*` | pause task 0x00228C70 |  |
| `+0x3FC` | `i32` | requested field (0x00285EC0) |  |
| `+0x400` | `u32` | bit 8 field request pending; bits 9/10 restore pending/verified; bit 11 cleared by 0x0027F2E0; | bit 13 set by `0x00285EA0`; low byte rewritten by `0x0027F2E0` |
| `+0xDEE` | `u8` | cleared by 0x0027EFA0 | +`0xDEF`  u8    1 while a mode screen opens, 0 after the controller's message |

Struct GameOverTask size=`0x108`   (`0x00244F50`(`0x108`, `0x003EF830`, 0); `0x02B5F1C8` points at it):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xB4` | `u32` | tick handle (0x001EDEC0) |  |
| `+0xC0` | `i32` | state 0..8 | +`0x0C4`  i32   countdown frames |
| `+0xD0` | `void*` | image task 0x003EF2E0 | +`0x0D8`  ptr   timing task `0x003EEEC0` |
| `+0xE0` | `void*` | logo task 0x003EF4A0 | +`0x0E8`  ptr   prompt task `0x003EF050` |
| `+0xF0` | `i32` | 1 once message 0x10 arrived |  |
| `+0xF8` | `reg` | texture registration (0x00393460) | +`0x100`  reg   texture registration (`0x003933F0`) |

Struct ImageSlot base=`0x022CB9F0` count=4 size=`0x18`   (`0x00361630` loads, `0x00360C20` reads, `0x00360D70` releases):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | state: 0 free, 3 loading, 4 loaded, 5 ready; 0x00360D70 releases state 5 and flags the rest |  |
| `+0x01` | `u8` | image id (7 = gameover_c) |  |
| `+0x02` | `u8` | flags: bit 0 release requested, bit 1 fading (0x00361200) |  |
| `+0x03` | `u8` | result byte returned by 0x00361630 |  |
| `+0x08` | `void*` | payload | +`0x14`  u32  handle from `0x001DBB80`(id) |

Title-return bytes:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022CB720` | `u8` | busy mask (0 = idle; 0x003321E0 refreshes bit 7; 0x00360100 sets, 0x003601B0/0x003601C0 modify, 0x00360370 clears) |  |
| `0x022CB724` | `u32` | written 0x5A by 0x00360120 | `0x022CB726`  u8   1 after the teardown |
| `0x022CB727` | `u8` | cleared by 0x00360120 | `0x022CB72A`  u8   softwarereset request (`0x003603D0`) |
| `0x022CB72B` | `u8` | title-map request (0x003603E0, from the area controller when +0x3FC is 0x0C) |  |

Request and mode:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x0215F1A0` | `u8` | request pending | `0x0215F1A1`  u8  latch that refuses `0x002E1B10` |
| `0x0215F1A4` | `u32` | request id | `0x0215F1A8`  u32  request parameter |
| `0x02092730` | `u32` | current mode | `0x02092734`  u32  mode parameter     `0x020927D8`  u32  raw mode |
| `0x022C83E8` | `u32` | bit 8 game over posted, bit 1 armed, bit 0 and bit 4 the 0x18 and 0x17 posts |  |
| `0x00254C70` | `u8[]` | mode-request arm table (id - 1 → arm) | `0x00254C58`  u32[6]  arm jump table |

## Shipped data

| Fact | Value |
|---|---|
| `healall` calls in the 1,114 us zone scripts | `healall(0)` 1,228 in 184 scripts; `healall(5)` 903 in 103; `healall(2)` 20 in 18 |
| `setnowjumpindex(-2)` | 1,146 calls in 183 scripts: the 81 crystal scripts and 102 others, each around a save screen |
| save screens opened (`openfullscreenmenu_48d(0x8005, …)`) | 1,148 calls |
| `mapjump` calls | 8,881; none passes a negative entrance, so the `-2` alias is only ever set through `setnowjumpindex` |
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
`0x0215F1A8`; `0x022C83E8` bits 1 and 8; the mode words `0x02092730`, `0x02092734` and `0x020927D8`; the
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
  `(+0x1044, -2)` there and request `mapjump(field, -2, mode)` through the zone-change funnel. No
  shipped script passes a negative entrance to `mapjump`, so that path is unexercised.
- "Entrance of the last zone entered" is `(+0x1044, +0x1048)` read at death; scripts rewrite
  `+0x1048` freely and it may hold an alias.
- Whether a party can get back to a crystal has no native answer: exits are authored scripts,
  collision and story flags. Native facts that can stand in: the persistence group of the
  crystal's field against `+0x1044`, the teleport-off bit, the jump lock.
- `healall` and the crystal are zone-script rows: on a mirror they run untouched; supply the missing
  counterpart rather than suppressing them.
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
- [The screen-fade layers](../17-Presentation-Rendering/screen-fades.md
): `0x002EFA70`.
