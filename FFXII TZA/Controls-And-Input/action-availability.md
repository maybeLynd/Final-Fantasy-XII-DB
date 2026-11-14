---
title: "Action availability: the shared table that keeps menus and buttons shut during scenes, movies and battle moments, who holds each row and what each bit blocks"
kind: "system"
category: "Controls and input"
addresses: "0x0215F1C0, 0x002E1C20, 0x002E1CA0, 0x002E1CD0, 0x002E0FA0, 0x00254500, 0x01E0C2C0, 0x00313A00"
---

## What the player sees

- During a scene, a movie or a screen fade, the main menu, the battle command menu and the map do not open.
- Changing the party leader and cycling targets in the field stop working at the same moments.
- Event skip with Start is offered only while a scene allows it, and Start's event skip never runs while a movie plays. Story movies have a skip of their own, run by the scene's script: Start shows or hides a "[confirm button] Skip" prompt, and the confirm button while the prompt shows ends the movie with a half-second fade. The title screen's opening movie ends on Start or the confirm button, with no prompt.
- Escape Mode switches itself off at several of these moments, among them movies, screen fades, full-screen menus and the pause menu (the table below; [Escape Mode](escape.md)).

Scene commands such as the movie, screen-mask and user-control commands each switch on bits in their own row of one
shared table of 16 rows. Before a menu opens or a button acts, the game combines all the rows, and anything whose bit
is on in any row is refused.

## How it works

### The table

The table is 16 rows of 32-bit masks at `0x0215F1C0`. Each row belongs to one part of the game, and a set bit in any
row blocks that bit's actions.

| Writer | What it does |
|---|---|
| `0x002E1C20(row, bit)` | sets one bit (`0x002E1C20`-`0x002E1C23` tests the row) |
| `0x002E1CA0(row, bit)` | clears one bit, with the same test |
| `0x002E1CD0(clear, row)` | sets the mask `0x139203`, bits `0x1`, `0x2`, `0x200`, `0x1000`, `0x8000`, `0x10000`, `0x20000` and `0x100000`, or clears it (`0x002E1CE3`) |
| `0x002E1BE0(index, on)` | sets or clears row 1 bit value `1 << index` for indexes 0-18 (`0x002E1BF7`-`0x002E1BFE`, `0x002E1C0B`) |
| direct `or` and `and` | row 4 (`0x002E245F`, `0x002E2417`, `0x002E06C3`) and row 7 (`0x002E2248`, `0x002E2265`, `0x002E0D2A`), with the mask `0x100203` |

The row test in the first three is signed, so only rows 16 and up are refused. The slot-0 unload, the `param_1 == 0`
block of `0x002628B0`, clears all 16 rows through `0x002E0670` (`0x00262CCA`); other slots' unloads leave the table. Field
start `0x00266D10` clears them through `0x002E1450` (`0x00267155`).

### The combined mask

`0x002E0FA0` returns the OR of the 16 rows (`0x002E0FA9`-`0x002E1005`). While bit `0x10000` of the busy word `0x022CB720` is set,
it clears bit `0x80000` from the answer (`0x002E1009`, `0x00360360(0x10)`). The movie verb `moviestandby` sets that busy bit (`0x0035B840`)
and `movieend` clears it (`0x0035B8D0`), so event skip is refused for the whole movie. 29 call sites in 25 functions
read the combined mask, and `0x002E1020(row)` reads one row for three of them.

### Who holds each row

| Row | Holder | Bits (mask) |
|---:|---|---|
| `0` | the movie verbs `moviestandby` `0x368` (its handler `0x00356460` is a jump to `0x0035B840` at `0x00356467`; `0x0035B861`, `0x0035B86D`), `movieplay` `0x36A` and `movieend` `0x36D` (mask, `0x0035B816`, `0x0035B967`); the event-skip arm `0x00360980`, from verb `skipstart` `0x51A` (`0x0034D3BB`; `0x003609A7`, `0x003609B3`), and its release `0x00360A50`, from `0x003603F0` and `0x00360A20` (`0x00360B06`, `0x00360B12`); the title screen (`0x00394112`, `0x003940CB`); actor and field loads (`0x002678EB`, `0x0025D5A9`) | `0x3BB203` |
| `1` | verb `setmenudisablestatus` `0x3A5` through `0x002E1BE0` (`0x0035276D`); bit `0x200000` for the movie player (`0x001B82E4`, `0x001B76C8`, `0x001B80A4`, `0x001B84BE`), saving and loading (`0x0058252C`, `0x005823F8`, `0x005828B4`, `0x00582F1B`), the title screen (`0x00393A29`, `0x00393E07`), a Config screen widget (`0x0023FC78`, `0x0024024B`) and the callback `0x002CEB40` that `0x002CEFA0` installs (`0x002CEDE5`, `0x002CEBB6`) | `0x27FFFF` |
| `2` | battle selection, `0x00313A00`, below | `0x101DFF` |
| `3` | verbs `questresultwindow` `0x37C` and `queststartwindow` `0x386` (`0x00344C84`, `0x00345704`, `0x0034515F`, `0x003464E8`), `0x00268D10`/`0x00263050`, and `0x0026C5D0`, which clears it with `0x002E1CD0(1, 3)` for each of the four slot actors that is not null while `0x02099DB4` is above 0 (`0x0026C61A`-`0x0026C621`, `0x0026C678`-`0x0026C6B0`, `0x0026C70C`) | the mask |
| `4` | the screen-mask verbs `maskopen` `0x08A`, `maskopenfast` `0x3B5`, `mesvmaskopen` `0x446`, `mesvmaskopenfast` `0x447`, `maskclose` `0x08B`, `maskclosefast` `0x3B6` | `0x100203` |
| `6` | user control, verbs `ucon` and `ucon_4a5` (`0x0026C80C`, `0x0026C82C`) and `0x00263660`, `0x0026C3E0` | the mask |
| `7` | the full-screen frame modes: set by `0x00228930` and `0x002E09A0`, cleared by the main loop (`0x0022BBA1`-`0x0022BBC5`) | `0x100203` |
| `8` | the menu-request family, below | `0x101BF7` |
| `9` | verb `crossfade` `0x16F` (`0x002F1AD4`, `0x002F1AE1`) and its completion (`0x002F19D3`, `0x002F19E0`) | `0x100001` |
| `10` | a timed hold after a menu request (`0x002F1C8B`, `0x002F18AC`) | `0x2` |
| `12` | user control (`0x0026C738`) and a spawn group's last member dying (`0x00306F9A`), through `0x00307140` | `0x1019F9` |
| `13` | the trigger test `0x0025C830`, which sets the mask with `0x002E1CD0(0, 13)` after its time-stop take `0x00227420`, when `0x00377C20()` answers 0 (`0x0025D407`-`0x0025D41A`); `0x0025B500` jumps to `0x002E1CD0` with clear 1 and row 13 (`0x0025B567`-`0x0025B573`) | the mask |
| `15` | the pause menu, `0x00229590` (`0x002299BB`-`0x002299DB`, `0x00229785`-`0x002297A9`) | `0x100203` |

No holder sets a bit in rows 5, 11 and 14; only the two clears `0x002E0670` and `0x002E1450` write them (`0x002E0680`/`0x002E1572`, `0x002E0695`/`0x002E1587`, `0x002E06A3`/`0x002E1595`).

### Row 8

Five helpers write most of row 8, each setting or clearing a fixed group of bits:

| Helper | Writes |
|---|---|
| `0x00254850` | ten sets when its argument is non-zero (`0x00254861`-`0x002548DA`) |
| `0x002547D0` | seven sets or clears (`0x002547F2`-`0x00254836`) |
| `0x002548F0` | four (`0x00254911`-`0x00254937`) |
| `0x00254940` | one (`0x00254964`), then `0x002547D0` |
| `0x00254980` | seven (`0x002549A2`-`0x002549E2`) |

They are called from `0x0035BC50` (`0x0035BEB7`), `0x0035C770` (`0x0035C778`), `0x0035C7B0` (`0x0035C844`-`0x0035C870`),
`0x0035C8A0` (`0x0035C8B5`-`0x0035C8D7`), `0x0035C8E0` (`0x0035C8F3`), `0x0035C920` (`0x0035C938`), `0x0035C940` (`0x0035C955`), the
party-down window `0x0035D6B0` (`0x0035D858`), `0x0035D8D0` (`0x0035D90A`-`0x0035D96A`), `0x0035D980` (`0x0035DA3E`), `0x0035DA80`
(`0x0035DAB3`) and game over `0x003EF830` (`0x003EF8A0`, `0x003EF8A7`).

The other row-8 writers are the battle command menu (`0x00276715`, `0x00279FE9`), the party-down window itself
(`0x0035D73B`-`0x0035D84C`), the chocobo dismount and ride (`0x0035C990`-`0x0035CA2D`, `0x0035CF30`-`0x0035CF79`), and the
target cursor: `0x003C8990` and `0x003C8A50` (`0x003C8A0A`, `0x003C8AF2`) and the callback `0x003C8B70` that `0x003C8A20`
installs, which clears bit `0x1` five times (`0x003C8C97`-`0x003C9085`).

### Battle selection

`0x00313A00` rewrites row 2 every field frame (`0x00313A68`-`0x00313AF5`). The bits under mask `0x1019FD` are set while a
battle unit is selected (`0x02089350`). Bit `0x2` is set then, or while Escape Mode is on (`0x00253B90`). Bit `0x400`
follows the area's bit `0x8000` (`0x00377C20`).

It ends with a jump to `0x002E1C40(v, 5)` (`0x00313AF7`-`0x00313B1C`), a fourteenth bit outside the rows: it clears bit
`0x20` of the HUD hide word `0x0215F1AC` when v is 1, which is when no battle unit is selected and bit `0x40` of
`0x02089340` is clear (`0x00313A3C`-`0x00313A49`), sets it otherwise, and clears bit `0x20` of `0x0215F1B4`
([HUD](../Menus-And-HUD/hud.md)). It is called from the field frame (`0x00234624`) and from `0x00313DB0`.

### The Start button

When the Start screen opens, `0x00228930` copies all 16 rows to `0x01FD4700` (the `0x002E1020` loop at `0x00228972`) and
sets row 7 through `0x002E2240(1)` (`0x002E2248`). On close, `0x00229510` clears row 7 through `0x002E2240(0)` (`0x00229526`,
`0x002E2265`) and writes back rows 2 and 8 only, clearing and re-setting each bit of the mask `0x3FFFFF` from the copy (`0x00229554`,
`0x00229562`).

### What each bit blocks

| Bit | Blocks |
|---:|---|
| `0x1` | the main menu with Triangle (`0x00253D6E`) and its requests (`0x002E1AB9`, `0x002E1B31`, `0x002E25C7`) |
| `0x10` | the Circle or Cross interact press (`0x0025413F`) and force fight (`0x002736F0`, `0x0027399F`, `0x002C6580`) |
| `0x40`, `0x200` | Escape Mode, forced off (`0x00252B8C`, `0x00252B92`) |
| `0x400` | the battle command menu with Square or the confirm button (`0x00253F83`, `0x002541A4`, `0x0035D66D`), changing the leader (`0x0035D98D`), Escape Mode (`0x00252BA2`, `0x00252BE6`), the battle display and the map screens (`0x0028333C`, `0x00400F6F`, `0x00400FAD`, `0x004017B0`) |
| `0x800` | the Select and L3 presses (`0x00253E00`, `0x00253F0A`, `0x00253ECD`) |
| `0x1000`, `0x10000`, `0x20000` | Start's arms (`0x002288C8`, `0x0022887E`, `0x00228893`) |
| `0x40000` | the target cursor (`0x003C9176`, `0x003C919F`) |
| `0x200000` | opening the pause menu (`0x002283DA`, `0x002283E7`) and the audio hold (`0x00229B03`) |

No reader tests bits `0x80`, `0x4000`, `0x8000` or `0x100000`.

Bits `0x2000` and `0x80000` do not block anything: they steer Start's event-skip arm. Bit `0x80000` must be set for that arm to run
at all (`0x002288F6`), which is why the movie busy bit clears it. Inside the Start handler `0x002287D0`, with bit `0x80000` set, the arm it passes to `0x00228700` is 1 only when bit `0x2000` is set and
`0x003606B0` finds a non-zero word among `0x022CB9C4`, `0x022CB9C8` and `0x022CB9CC`, and 2 otherwise
(`0x002288F6`-`0x00228911`). `0x00360880` walks the same three words, takes the lowest set bit of each and runs that skip
through `0x00360710`.

`0x00228380`, which holds the bit `0x200000` test, first starts the task `0x00228490` when `0x0017E4C0` answers 0
(`0x0022839B`-`0x002283AE`). `0x0017E4C0` reads the application's byte `+0x27`, the window-active byte: application slot 14
(`0x007A0B40`) stores it, called by the window procedure with 1 when a new window is in front (`0x0079914C`) and by
`0x007A4150`, which also posts message `0x8001` to show or hide the cursor. The task's pointer `0x01FD4948` is the cell
`0x00228480` tests.

### The movie skip

Story movies are skipped by the scene's script, not by Start's event-skip arm. The offsets below are in the script
section of `us/event/bhm_d/bhm_d0101/bhm_d0101.ebp`; the 35 `movieSkip監督` actors of the `us` scripts decode to the
same verb sequence.

- The director starts the movie with `movieplay` (`6178`), files function 1 of actor 4, the skip actor's `Skip監視`,
  with `REQ` (`618A`), and parks on it with `REQWAIT` (`6191`) before `movieplaysync` (`6192`) and `movieend`
  (`6195`).
- The skip function runs once a frame (`wait(1)`, `700D`). It reads the newly pressed buttons with `padt` (`6ED5`;
  `0x00355440` returns the mapped word `0x02AD9E0C` through `0x0036FFD0`) and the player's state with `getmoviestatus`
  (`6EDB`), and returns, closing window 3, as soon as the state is not 3, playing (`6EE1`-`6EE8`, `7016`).
- Start, bit `0x8` of that word ([Controls](controls.md)), toggles a prompt (`6EEB`-`6EF2`, `6F45`-`6F4B`). To show it,
  `amest` (`6F2A`) opens message window 3 with the image's text entry 1, the confirm-button icon (escape `0F 60`)
  and "Skip", at x 120, y 817. To hide it, `mesclose(3)` (`6F39`).
- `0x002E1F80` stores the position at `+0x10` and `+0x12` of window slot 3 of `0x0215F200` (`0x68` bytes a slot). The
  x would be 60 if `getscreenaspect` answered 0, but its source `0x0053DD10` always answers 1.
- The confirm button while the prompt shows (`6F51`-`6F60`) skips; `get_pad_ok` gives Circle `0x2000` or Cross
  `0x4000` by `0x01FD4A64` (`0x002E12B0`).
- The skip plays a sound (`6F69`), runs `straightpcmtrans(0x1D, 0)` (`6F72`), fades the screen out and waits for
  it (`6F75`-`6F87`), cancels every effect (`6F8A`) and, while the state is still 3, calls `moviecancel` (`6F9D`);
  then `movieend` (`6FA0`). It sets file variable 3 to 1 (`6FBB`-`6FBE`), closes windows 0-7 and returns.
- `moviecancel`'s begin `0x0033FEC0` reaches `0x001B83B0(player, 1)` through `0x0035B720`: it sets `+0xBAC` and, unless
  the state is 0, 5 or 6, sets state 6 with half a second at `+0x10` (`0x001B83B7`-`0x001B83D1`), the fade the
  player's update runs down to state 5 ([Movies](../Graphics/movies.md)).
- Its poll `0x00357300` waits only while `0x0035B740` answers 1 to 3, which state 6 does not, and its result
  `0x0033FA20` runs `movieend`'s `0x0035B8D0`.
- The director sees the skip as the end of its wait: the skip function's return ends `REQWAIT`, and
  `movieplaysync` polls the same `0x00357300`, so it ends at once. The director then tests file variable 3, which it
  cleared before the movie (`615D`).
- When it is set, bhm_d0101 fades the music out and stops it (`61A1`-`61C3`) and, after `skipstart(0)` (`6201`),
  runs `skipexec(0)` (`6204`-`6211`), the scene's event skip
  ([Event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- The title map `ttl_a01`'s `ムービースキップ` actor ends its movie on Start or the confirm button, with no prompt,
  while the state is 3 (`216B4`-`216C7`; `moviecancel` at `21739`), and `ttl_c01`'s `movie_skip_ctrl` cancels a
  playing movie when it is requested (`214D5`). Of the 37 `us` scripts that call `moviestandby`, the staff roll
  `men_z0005` is the one that calls no `moviecancel`.

### Menu requests

`0x00254500` turns the combined mask into a set of refused menu requests: for each bit of the mask `0x3FFFFF` that
is set, it ORs in that bit's word of `0x01E0C2C0` (`0x00254500`-`0x0025453C`). The menu router refuses those requests
(`0x00254B80`-`0x00254BC5`). It reads the combined mask itself, `0x002E0FA0()` (`0x00254504`), and tests two bits per step
for 11 steps (`0x0025451D`-`0x0025453C`), the word of bit value `1 << n` being `0x01E0C2C0 + 4n`. Each word holds bit
`1 << r` for each request *r* it refuses; bits `0x10` and `0x80` and bits `0x800` to `0x200000` have word 0 and
refuse nothing:

| Bit | Word | Requests refused |
|---:|---:|---|
| `0x1`, `0x8` | `0x4` | 2, the main menu |
| `0x2` | `0x2A` | 1, the battle command menu; 3, choosing the leader; 5, cycling targets |
| `0x4`, `0x400` | `0x8` | 3 |
| `0x20` | `0x20` | 5 |
| `0x40` | `0x4000` | 14 |
| `0x100` | `0x200002` | 1, and 21 |
| `0x200` | `0x4020` | 5, and 14 |

## State

The 16 rows, each a `u32` that is 0 in the file. `0x002E0670` and `0x002E1450` clear them two at a time with 8-byte
stores (`0x002E0672`-`0x002E06A3`, `0x002E1564`-`0x002E1595`). Every row is read by `0x002E0FA0` (`0x002E0FC0`, `0x002E0FCD`)
and by the drain `0x002E09A0` (`0x002E0C00`, `0x002E0C0D`), which OR the 16 together, and by `0x002E1020` from `0x00228972`,
which copies each one; the table names these three the readers above.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0215F1C0` | `u32` | 0 | row 0, the movie and event-skip row | the row 0 holders above; 0 (`0x002E0672`, `0x002E1564`) | the readers above |
| `0x0215F1C4` | `u32` | 0 | row 1, the menu-disable row | `0x002E1BE0` (`0x002E1BFE`, `0x002E1C0B`); 0 (`0x002E0672`, `0x002E1564`) | the readers above; `0x002E1020` from `0x002283E2` and `0x00229B12` (bit `0x200000`); `0x002E1BE0` |
| `0x0215F1C8` | `u32` | 0 | row 2, battle selection | `0x00313A00` through `0x002E1C20` and `0x002E1CA0`; `0x00229510` as the Start screen closes (`0x00229554`, `0x00229562`); 0 (`0x002E0679`, `0x002E156B`) | the readers above |
| `0x0215F1CC` | `u32` | 0 | row 3, the quest windows | the row 3 holders above; 0 (`0x002E0679`, `0x002E156B`) | the readers above |
| `0x0215F1D0` | `u32` | 0 | row 4, the screen mask | `0x002E2400` (`0x002E2417`), `0x002E2440` (`0x002E245F`), `0x002E06B0` (`0x002E06C3`); 0 (`0x002E0680`, `0x002E1572`) | the readers above |
| `0x0215F1D4` | `u32` | 0 | row 5; no holder sets a bit | 0 (`0x002E0680`, `0x002E1572`) | the readers above |
| `0x0215F1D8` | `u32` | 0 | row 6, user control | the row 6 holders above; 0 (`0x002E0687`, `0x002E1579`) | the readers above |
| `0x0215F1DC` | `u32` | 0 | row 7, set to `0x100203` while a full-screen menu or the Start screen is up | `0x002E09A0` (`0x002E0D2A`); `0x002E2240` (`0x002E2248`, `0x002E2265`); the main loop through `0x002E1CA0` (`0x0022BBA1`-`0x0022BBC5`); 0 (`0x002E0687`, `0x002E1579`) | the readers above |
| `0x0215F1E0` | `u32` | 0 | row 8, the menu-request family | the row 8 writers below; `0x00229510` as the Start screen closes (`0x00229554`, `0x00229562`); 0 (`0x002E068E`, `0x002E1580`) | the readers above |
| `0x0215F1E4` | `u32` | 0 | row 9, the crossfade | the row 9 holders above; 0 (`0x002E068E`, `0x002E1580`) | the readers above |
| `0x0215F1E8` | `u32` | 0 | row 10, the timed hold after a menu request | `0x002F1C8B`, `0x002F18AC`; 0 (`0x002E0695`, `0x002E1587`) | the readers above |
| `0x0215F1EC` | `u32` | 0 | row 11; no holder sets a bit | 0 (`0x002E0695`, `0x002E1587`) | the readers above |
| `0x0215F1F0` | `u32` | 0 | row 12, user control and a spawn group's last death | `0x00307140`, called at `0x0026C738` and `0x00306F9A`; 0 (`0x002E069C`, `0x002E158E`) | the readers above |
| `0x0215F1F4` | `u32` | 0 | row 13 | `0x0025C830` through `0x002E1CD0(0, 13)` (`0x0025D41A`); `0x0025B500` through `0x002E1CD0` (`0x0025B567`-`0x0025B573`); 0 (`0x002E069C`, `0x002E158E`) | the readers above |
| `0x0215F1F8` | `u32` | 0 | row 14; no holder sets a bit | 0 (`0x002E06A3`, `0x002E1595`) | the readers above |
| `0x0215F1FC` | `u32` | 0 | row 15, the pause menu | `0x00229590` (`0x002299BB`-`0x002299DB`, `0x00229785`-`0x002297A9`); 0 (`0x002E06A3`, `0x002E1595`) | the readers above |

No other instruction reaches the table. The table's address is taken by `0x002E1020`, `0x002E1C20`, `0x002E1CA0` and
`0x002E1CD0`, and `0x0215F1D0` by `0x002E09A0` and `0x002E0FA0`.

### The Start handler's gate

The Start handler `0x002287D0` goes on to its arms when Start is newly pressed (pressed set 0 bit `0x8`,
`0x0022889A`-`0x002288AB`), when `0x003641F0` or `0x00227D70` asks for an arm, or when the global below is not 0
(`0x002288AE`-`0x002288BD`). After it calls `0x00228700`, which answers 1 when it builds the event-skip task, it stores 0
there on a non-zero answer and keeps the old value otherwise (`0x00228916`-`0x00228922`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01FD46F8` | `u32` | 0 | stays 0: it lies in the zero-initialised tail of `.data` (past the section's `0x18E400` file bytes), and its one store writes 0 or the value already there, so the test at `0x002288AE` never opens the arms by it; the arms open on a new Start press or an arm request | `0x002287D0`, 0 or its own value (`0x00228922`) | `0x002287D0` (`0x002288AE`, `0x00228916`) |

No other instruction reaches `0x01FD46F8`; only `0x00228922` stores to it.

## Modding notes

- To keep a menu shut from a script, `setmenudisablestatus` owns row 1 bits `0x7FFFF`; the other rows are rewritten by
  their holders.
- A row number below 0 passes the signed test and writes below the table at `0x0215F1C0`.
- In row 0 the movie verbs and the actor and field loads all write the mask `0x139203`, so one holder's clear also
  removes the bits another holder set there.

## Related

- [Escape Mode](escape.md) - the toggle bits `0x40`, `0x200` and `0x400` force off.
- [Keymap file](keymap-file.md) - the buttons the arbiter reads.
- [Menu requests](../Menus-And-HUD/menus.md) - the request ids and the router.
