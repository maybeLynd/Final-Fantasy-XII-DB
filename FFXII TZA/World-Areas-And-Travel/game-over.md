---
title: "Game over: what a party wipe does, the GAME OVER screen, and the return to the title map"
kind: "system"
category: "World, areas and travel"
summary: "What happens after the last party member falls: the request the field frame posts and the second route a menu death takes, the executor that opens the game-over screen, the task tree that fades the field out, shows the GAME OVER image and the press-to-continue prompt, and fades to black, the request for the title map and the byte it really sets, the main-loop check that tears the field down and returns to the title screen, what is not reloaded, and where a load afterwards puts the party, including the save-crystal entrance alias."
addresses: ["00234590", "0035C7A0", "0035C7B0", "00227370", "002E1B10", "00254850", "00254E50", "002805D0", "0027EFA0", "002E09A0", "00254B50", "0028F970", "00280A00", "00252B40", "0027FB70", "00280140", "003EF750", "003EF830", "003EFAA0", "003EF2E0", "003EEEC0", "003EF4A0", "003EF050", "003EF680", "003EF770", "003EF290", "00361630", "00360C20", "003611F0", "00360D70", "002DDCA0", "002EFA70", "00285EC0", "00285EA0", "003603E0", "003603D0", "0034EB20", "00360120", "003601D0", "003321E0", "0022A770", "0022BC20", "00228C70", "0027F2E0", "00264B90", "00377AB0", "00377A90", "0037B4D0", "00356500", "00359C60", "0030F4B0", "00237CA0", "0034AAB0", "002FEAC0", "00314DC0", "00314D80", "0034AC10"]
---

# Game over: what a party wipe does, the GAME OVER screen, and the return to the title map

## What the player sees

When the last standing party member falls, everyone on the field stops where they are, the
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

The field frame `00234590` checks the party every frame and, when it is wiped, posts mode `0x0B`
through `0035C7A0(0x0B)` and `0035C7B0(0x0B, 1)`; the four wipe predicates and the post are on
[when the game is over](../Status-Effects-And-KO/ko-and-game-over.md).
`0035C7B0` refuses while a request is already pending: `022C83E8` bit 8, a mode `02092730` of
`0x0B` or `0x18`, or the request byte `0215F1A0`. Otherwise it runs five steps:

1. sets `022C83E8` bit 8;
2. halts every actor record with class `0x16` through `00227370` (skipped when `01FD46D4` bit 22 is
   set);
3. writes the request `0215F1A0 = 1`, `0215F1A4 = 0x0B`, `0215F1A8 = 0` through `002E1B10(0x0B, 0)`,
   unless the latch `0215F1A1` is set;
4. sets `022C83E8` bit 1;
5. locks the input group with `00254850(1)`.

A second route needs no field frame. The main loop (`0022A770`) calls `00254E50` once per tick,
which asks `002805D0`: when `0035C740()` is non-zero, a mode-screen task is up and the current mode
`02092730` is one of 6, `0x0A`, `0x0F`, `0x11`, `0x12`, `0x13`, or 2 with a sub-id outside
`0x40` to `0x42`, it runs `0027EFA0`. That body fades (`002EFA70(3, 0, 1, 0)` when `002EFD20(3)` is
non-zero), calls `0035C7B0(0x0B, 0)` and `00252B40(0x0B, 1)`, clears `[0209AC30] + 0xDEE`, runs
`00251E80`, sets `+0xDEF = 1` and starts the game-over task directly with `003EF750` (`0027F02A`).

### From the request to the screen

The UI request consumer `002E09A0` reads `0215F1A0` in its closing block and calls
`00254B50([0215F1A4], [0215F1A8], 0)`, then clears the byte. `00254B50(id, p2, p3)` indexes the byte
table at `00254C70` with `id - 1`: entry 10 is 5, and the jump table at `00254C58` sends 5 to the
default arm `00254C2D`, which runs `0028F970()` (clears bits 4 and 10 of the menu state dword at
`[0209BE80] + 0x10F68`) and then `00280A00(0x0B, 0, 0)`.

`00280A00(mode, p2, p3)` opens a mode screen only when the root block's `+0xC0` and `+0xB8` are
both null. It stores the mode with `00252B40(mode, 1)` (`02092730 = mode & 0x7FFF`, `02092734 = p2`,
`020927D8 = mode`), spawns the mode-screen task `0027FB70` and the area controller `00280140`
(`0xD8` bytes each) and runs `0028CA30`. The create arm of `0027FB70` for mode `0x0B` sets
`[0209AC30] + 0xDEF = 1` and calls `003EF750` (`0027FFC3`), which is
`00244F50(0x108, 003EF830, 0)`: the game-over task. Those are the only two callers of `003EF750`.

### The game-over task and its helpers

`003EF830` is a task of `0x108` bytes. Its create arm:

1. stores itself at `02B5F1C8`;
2. registers the `gameover_c` texture through the two descriptors at `00D11C88` and `00D11CA0`
   (`00393460` and `003933F0`; the descriptor names the string at `00D11CD0`, the file is
   `Tm2_Menu\gameover_c.tm2` in each language folder);
3. attaches itself to the list `0208EA28` with priority 100 and runs `003678F0`;
4. spawns two helpers of `0xD0` bytes: the image task `003EF2E0` at `+0xD0` and the timing task
   `003EEEC0` at `+0xD8`.

Its tick (`001EDEC0` on `+0xB4`) runs the state machine `003EFAA0`. Message `0x10` sets `+0xF0 = 1`;
message `0x8001` kills the prompt task at `+0xE8`; message `0x12` with payload 1, 2 or 3 clears the
helper pointer `+0xD8`, `+0xE0` or `+0xE8`.

The image task `003EF2E0` fades the music with `002DEE50(002DEC00(), 30)`, fades the loaded images
over 30 frames (`003611F0(0x1E)`) and sets the fade rate `003634B0(0x3C)`. Its states:

- state 0 counts down 15 frames, runs `00363560` and `0024D050`, and once `002F1A30(1)` is 0 loads
  image 7 with `00361630(7)`: a slot of the four-entry image table at `022CB9F0` (Layouts); when
  no slot is free (`-1`) it releases every slot with `00360D70` and retries from state 1;
- state 2 waits until the slot's state byte is 5 (`00360C20(7)`); state 3 is "ready";
- state 4 counts down and then sets its end flag `+0xC4` bit 0;
- state 6 waits for `002F1A30(1)` to be 0 and becomes 7.

The timing task `003EEEC0` starts the screen fade `00251D90(1, 0x3C, 0x78)`, waits until
`00251D20()` is above 2, then 18 frames, plays `002C99A0(1000, 8)` and sends the parent message
`0x13` with payload 1; 60 frames later it reaches its end state. It forwards messages `0x0F` and
`0x12` to the parent with payload 1.

### The state machine

`003EFAA0` runs when the countdown `+0xC4` is 0 or has just reached 0. Message `0x13` from the
helpers (`003EF770`) moves it: payload 1 puts it in state 1, payload 2 spawns the prompt task
`003EF050` (`0xD8` bytes) at `+0xE8` and goes to state 3, payload 3 goes to state 4.

1. State 1 waits until the image slot is ready (image task state 3) and message `0x10` has
   arrived (`+0xF0`). It then spawns the logo task `003EF4A0` (`0xD0` bytes, widget `002432B0` from
   the descriptor at `00D11CA8`) at `+0xE0`, shows image 7 with `002DECE0(7)` and goes to state 2.
2. At the same moment the image task enters state 4 with a display count of `0x564`, `0x3DE` or
   `0x3A2` frames when `002DDCA0()` returns 1, 2 or anything else; that is the word at
   `[0215E6E0] + 0x0E`, a 2 downgraded to 1 when `0017E490()` has bit 0 clear.
3. The logo task waits 18 frames, then, once `+0xF0` is set, attaches to the parent's list; when it
   ends it sends `0x13` with payload 2, which spawns the prompt task.
4. The prompt task `003EF050` ends the screen on message 10 when the image task's end flag is set
   or a button in the mask `0xFF09` of `02F9736A` is pressed: it sends `0x8001` to the parent, which
   kills it.
5. Message `0x0F` with payload 3 runs `003EF680`: the logo task is killed, `00250C50(100)` and
   `00251EA0(0.8, 0x78)` run, the timing task is set to state 4 for 180 frames and, unless the image
   task has already ended, the music fades over 120 frames and the images over 240
   (`003611F0(0xF0, 1)`, `003634B0(0xF0, 0)`, image state 6). The parent waits 60 frames and goes to
   state 5.
6. State 5 fades layer 2 to black over 60 frames (`002EFA70(2, 0x3C, 0)`), waits 120 frames and goes
   to 6. State 6 runs `003EF290(image, 1)` when the image task's end flag is set (a one-frame music
   fade and a two-frame image fade), then 7. State 7 waits for image task state 7 and destroys it
   (`00244F00`), then 8.
7. State 8, once `+0xD8`, `+0xE0` and `+0xE8` are all null, destroys the task itself and calls
   `00285EC0(0x0C)` (`003EFB32`).

The teardown message `0x12` unregisters the two textures (`00393900`, `003938B0`), releases the
input locks `00254850(0)` and `00254940(0)` and runs `0027F2E0`, which rewrites the low byte of
`[0209AC30] + 0x400` from its bits 9 and 10 (2 when bit 9 is clear, 1 when bit 9 is set and bit 10
clear, 2 when both are set) and clears bit 11.

### The request for the title map, and what it really does

`00285EC0(field)` sets `[0209AC30] + 0x400` bit 8 and writes `+0x3FC = field`. Its callers are the
game-over task (`003EFB32`, field `0x0C`) and the pause task `00228C70` (`002291B1`, field `0x0C`).

The pause task shows "This will return you to the title screen. Are you sure?" (menu text `0x85F`,
key `0x114`) or "This will close FINAL FANTASY XII THE ZODIAC AGE" (text `0x890`, key `0x115`). A
confirmed return fades (`002EFA70(2, 0x18, 0)`), waits for `002EFD20(2)` to report 2 and calls
`00285EC0(0x0C)`; a confirmed quit calls `001E0FB0(0)`. The same task's skip path calls
`00285EA0(1)`, which sets bit 13 of `+0x400`
([the native command lifecycle](../Scripts-And-Script-Commands/native-commands.md)).

The consumer is the area controller `00280140`, in its message `0x12` arm (`00280248` to
`0028027C`): with bit 8 set it clears the bit and tests `+0x3FC` against `0x0C`. For `0x0C` it
calls `003603E0`, which sets the byte `022CB72B = 1`; for any other field it runs `002CFD10(-1)`
and `00314440(+0x3FC, 0, 0, 0)`, a real field transition
([zone changes](zone-changes-and-mapjump.md)). Then `00251E80`, `00252D90`,
`[0209AC30] + 0xDEF = 0` and `+0xC0 = 0`. So the title map, field `0x0C` (`ttl_a01`), is never
requested as a zone change after a game over; a title-return byte is set instead.

### The main loop tears the field down

`00360120` runs every main-loop iteration (`0022A977` and `0022AE00` in `0022A770`, and `0022BDDB` in
the re-initialisation `0022BC20`). It refreshes the busy mask's bit 7 with `003321E0`, writes
`022CB724 = 0x5A` and `022CB727 = 0`, and when the busy mask `022CB720` is 0 and either title byte
`022CB72A` or `022CB72B` is set, it runs the resume routine `003601D0` and then `0017F740(0)`,
`001EC4B0(1)`, `001EC4B0(2)`, `001830A0(1)`, `00382B50(-1, 0, 0)`, `00182810(1)` and `00357B00`
(`022C7F80 = 0`).

`003601D0` is the field teardown, in this order:

1. both speed scales to 1.0 (`00229EF0`, `00229EE0`), `00368AC0(0)`, `0032E520(0)`, `0035EA30(0)`,
   `0053DD10(1)`;
2. for managers 0 to 2 with `+0x10` bit 0, the jump lock `+0x200` bit 0 is cleared;
3. `002DEE90(-1)`, `003634A0(0)`, `003633B0(0)`, `00362850`, `002DF0F0(0, -1)`, `002DF060`,
   `001DC330(-1)`, `002DEB90(1)`, `005C5230`;
4. the layer mask bits 2 to 4 are cleared through `002DF370(0x1C, 0, 1)` and every image slot is
   released (`00360D70`);
5. `022CB726 = 1`; `022CB727`, `022CB72A` and `022CB72B` are cleared;
6. `002EF840(0)` to `002EF840(6)`, `002F1A70`, `003DE210`, `003DE0A0`, `002EFE40(6)`,
   `002EFE50(0xFF)`, `002EFA70(2, 0, 0, 0)`, `002EFA70(3, 0, 1)`;
7. `002E06B0`, `003636A0`, `00363750`, `00363E40(0)`, `0036DF30`, `0024E910`, `0024D9C0`,
   `00331920(1)`, `002EF5F0`, `002DDE60`.

The other title byte has one writer: the script verb `softwarereset` (`0x3E2`, handler `0034EB20`,
a jump to `003603D0`, which sets `022CB72A = 1`). `00360370` clears every byte of the block at boot
(`0022A39E` in `0022A0B0`). The title screen's own start-up after the teardown belongs to the boot path, outside this page.

### Nothing is reloaded, and where a load puts the party

No step of the chain loads a save, revives a party member or jumps to another field. The save
payload's transition record is untouched: `+0x1044` is the field the party was in and `+0x1048`
the entrance it arrived by (`003148B0`; written only by `setnowjumpindex`, `0034AC10` to
`00314D80`). A load restores that record, and the field start places the party through
`0037B4D0`, which calls `00377A90` (`0037BF67`), reads `+0x1048` and resolves it with
`00377AB0` and `00264B90(0, 0, entrance)`; the position and angle go to `0031BAC0` (`0037BFA6`).

`00264B90(list, manager, entrance, out)` turns an alias into an entry of the field header's
entrance list: `-1` becomes the header's short `+0x52`, `-2` the short `+0x78` (the save-crystal
entrance), `-3` the short `+0x7A`, any other negative `+0x52`. The entry is 0x20 bytes from the
list at `+0x54` (list 0) or `+0x84` (list 1), with `x`, `y`, `z` at `+4`, `+8`, `+0x0C` and the
angle at `+0x10`. When the entrance does not exist `00377AB0` falls back to
`[[0209A678]] + 0x28` and `+0x2C` when `02ADD0D8` is set, else to zero.

The crystal script sets `setnowjumpindex(-2)` around the save screen and restores the real
entrance afterwards ([save and teleport crystals](save-and-teleport-crystals.md)). Slot 0 is the
field-transition autosave and a manual save cannot choose it
([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).

KO is cleared by the crystal, never by the game over. `healall(n)` (`0x3AF`, `00356500`) maps its
argument with `00359C60` (1 to 7, 2 to `0x0F`, 3 to 4, 4 to `0x0C`, 5 to `0x10`, anything else to
7) and runs `0030F4B0(-1, mask)`: bit 0 restores HP, bit 1 restores MP, bit 2 removes the statuses
in `0208D320`, bit 3 those in `0208D324`, and `0x10` also removes `0x544`.

`00237CA0` builds the two groups at start-up: status `i` goes to `0208D320` when its status-table
row has bit 13 of the word at `+6`, else to `0208D324`; KO's row carries `0xA0DF`, so `healall(0)`
revives ([the thirty-two statuses](../Status-Effects-And-KO/statuses.md)). The
crystal also calls `btladjustsystem(1)` (`0x517`, `0034AAB0` to `002FEAC0`), which with bit 0 set
clears `022C3178` bit 0, zeroes `022C3170`, `022C3160` and `022C3158` and sets `022C3168` to -1.

## Layouts

```
root block [0209AC30]
+0x0B8  ptr   mode-screen task             +0x0C0  ptr   area controller (00280A00 refuses while set)
+0x0D0  ptr   pause task 00228C70
+0x3FC  i32   requested field (00285EC0)
+0x400  u32   bit 8 field request pending; bits 9/10 restore pending/verified; bit 11 cleared by 0027F2E0;
              bit 13 set by 00285EA0; low byte rewritten by 0027F2E0
+0xDEE  u8    cleared by 0027EFA0          +0xDEF  u8    1 while a mode screen opens, 0 after the controller's message
```

```
struct GameOverTask size=0x108   (00244F50(0x108, 003EF830, 0); 02B5F1C8 points at it)
+0x0B4  u32   tick handle (001EDEC0)
+0x0C0  i32   state 0..8                   +0x0C4  i32   countdown frames
+0x0D0  ptr   image task 003EF2E0          +0x0D8  ptr   timing task 003EEEC0
+0x0E0  ptr   logo task 003EF4A0           +0x0E8  ptr   prompt task 003EF050
+0x0F0  i32   1 once message 0x10 arrived
+0x0F8  reg   texture registration (00393460)   +0x100  reg   texture registration (003933F0)
```

```
struct ImageSlot base=022CB9F0 count=4 size=0x18   (00361630 loads, 00360C20 reads, 00360D70 releases)
+0x00  u8   state: 0 free, 3 loading, 4 loaded, 5 ready; 00360D70 releases state 5 and flags the rest
+0x01  u8   image id (7 = gameover_c)
+0x02  u8   flags: bit 0 release requested, bit 1 fading (00361200)
+0x03  u8   result byte returned by 00361630
+0x08  ptr  payload                        +0x14  u32  handle from 001DBB80(id)
```

```
title-return bytes
022CB720  u8   busy mask (0 = idle; 003321E0 refreshes bit 7; 00360100 sets, 003601B0/003601C0 modify, 00360370 clears)
022CB724  u32  written 0x5A by 00360120      022CB726  u8   1 after the teardown
022CB727  u8   cleared by 00360120           022CB72A  u8   softwarereset request (003603D0)
022CB72B  u8   title-map request (003603E0, from the area controller when +0x3FC is 0x0C)

request and mode
0215F1A0  u8   request pending     0215F1A1  u8  latch that refuses 002E1B10
0215F1A4  u32  request id          0215F1A8  u32  request parameter
02092730  u32  current mode        02092734  u32  mode parameter     020927D8  u32  raw mode
022C83E8  u32  bit 8 game over posted, bit 1 armed, bit 0 and bit 4 the 0x18 and 0x17 posts
00254C70  u8[]  mode-request arm table (id - 1 → arm)   00254C58  u32[6]  arm jump table
```

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
| display count before the prompt | `0x564`, `0x3DE` or `0x3A2` frames by `002DDCA0()` = 1, 2 or other |

## Operations

A wipe, in order: the field frame posts `0x0B`; `0035C7B0` halts the actors, writes the request and
locks input; the UI consumer runs the executor; the executor opens the mode screen, which spawns
the game-over task; the task fades the music and the field, loads and shows the GAME OVER image,
runs the logo, waits for the display count or a button, fades to black and calls `00285EC0(0x0C)`;
the area controller sets `022CB72B`; the main loop's `00360120` tears the field down and hands over
to the title screen.

A menu death takes the second route: `00254E50` to `002805D0` to `0027EFA0`, which posts `0x0B`
without the field frame and starts the task itself.

The pause screen's return takes the short route: `00228C70` fades and calls `00285EC0(0x0C)`; the
rest is the same.

## State

The root block's `+0x3FC`, `+0x400`, `+0xDEE` and `+0xDEF`; the request bytes `0215F1A0` to
`0215F1A8`; `022C83E8` bits 1 and 8; the mode words `02092730`, `02092734` and `020927D8`; the
game-over task, its four helpers and `02B5F1C8`; the image slot table; the title bytes `022CB720`
to `022CB72B`; the layer mask `0215EFD8`; the input groups locked by `00254850` and `00254940`; the
actors' halt class `0x16`; `022C3158` to `022C3178` after a crystal touch.

## Modding notes

- A respawn has to intercept before `0035C7B0(0x0B, …)`: once the request byte is written the chain
  runs to the title screen with no hook that reloads or revives. `002E1B10` refuses while
  `0215F1A1` is set, which is the one latch on the post.
- Field `0x0C` is never a zone change on this path. A detour that watches `00314440` for the return
  to the title screen sees nothing; watch `003603E0` or `022CB72B` instead.
- "Respawn at the last crystal" has no native field: the crystal-touch point is the verb handler
  `0034AAB0`, run once per crystal confirm and only from the crystal actor; record
  `(+0x1044, -2)` there and request `mapjump(field, -2, mode)` through the zone-change funnel. No
  shipped script passes a negative entrance to `mapjump`, so that path is unexercised.
- "Entrance of the last zone entered" is `(+0x1044, +0x1048)` read at death; scripts rewrite
  `+0x1048` freely and it may hold an alias.
- Whether a party can get back to a crystal has no native answer: exits are authored scripts,
  collision and story flags. Native facts that can stand in: the persistence group of the
  crystal's field against `+0x1044`, the teleport-off bit, the jump lock.
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
- The screen-fade layers: `002EFA70`.
