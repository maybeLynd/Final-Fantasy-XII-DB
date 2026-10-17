---
title: "Action availability: the shared table that keeps menus and buttons shut during scenes, movies and battle moments, who holds each row and what each bit blocks"
kind: "system"
category: "Controls and input"
addresses: "0215F1C0, 002E1C20, 002E1CA0, 002E1CD0, 002E0FA0, 00254500, 01E0C2C0, 00313A00"
---

## What the player sees

- During a scene, a movie or a screen fade, the main menu, the battle command menu and the map do not open.
- Changing the party leader and cycling targets in the field stop working at the same moments.
- Event skip with Start is offered only while a scene allows it, and never while a movie plays.
- Escape Mode switches itself off while availability bit 6, 9 or 10 is held (the table below; [Escape Mode](escape.md)).

## How it works

### The table

The table is 16 rows of 32-bit masks at `0215F1C0`. Each row belongs to one part of the game, and a set bit in any
row blocks that bit's actions.

| Writer | What it does |
|---|---|
| `002E1C20(row, bit)` | sets one bit (`002E1C20`-`002E1C23` tests the row) |
| `002E1CA0(row, bit)` | clears one bit, with the same test |
| `002E1CD0(clear, row)` | sets the mask `0x139203`, bits 0, 1, 9, 12, 15, 16, 17 and 20, or clears it (`002E1CE3`) |
| `002E1BE0(index, on)` | sets or clears row 1 bit `index` for indexes 0-18 (`002E1BFE`, `002E1C0B`) |
| direct `or` and `and` | row 4 (`002E245F`, `002E2417`, `002E06C3`) and row 7 (`002E2248`, `002E2265`, `002E0D2A`), with the mask `0x100203` |

The row test in the first three is signed, so only rows 16 and up are refused. The slot-0 unload, the `param_1 == 0`
block of `002628B0`, clears all 16 rows through `002E0670` (`00262CCA`); other slots' unloads leave the table. Field
start `00266D10` clears them through `002E1450` (`00267155`).

### The combined mask

`002E0FA0` returns the OR of the 16 rows (`002E0FA9`-`002E1005`). While bit 16 of the busy word `022CB720` is set,
it clears bit 19 from the answer (`002E1009`, `00360360(0x10)`). The movie verb `moviestandby` sets that busy bit (`0035B840`)
and `movieend` clears it (`0035B8D0`), so event skip is refused for the whole movie. 29 call sites in 25 functions
read the combined mask, and `002E1020(row)` reads one row for three of them.

### Who holds each row

| Row | Holder | Bits |
|---:|---|---|
| `0` | the movie verbs `moviestandby` `0x368` (its handler `00356460` is a jump to `0035B840` at `00356467`; `0035B861`, `0035B86D`), `movieplay` `0x36A` and `movieend` `0x36D` (mask, `0035B816`, `0035B967`); the event-skip arm `00360980`, from verb `skipstart` `0x51A` (`0034D3BB`; `003609A7`, `003609B3`), and its release `00360A50`, from `003603F0` and `00360A20` (`00360B06`, `00360B12`); the title screen (`00394112`, `003940CB`); actor and field loads (`002678EB`, `0025D41A`, `0025D5A9`) | `0`, `1`, `9`, `12`, `13`, `15`-`17`, `19`, `20`, `21` |
| `1` | verb `setmenudisablestatus` `0x3A5` through `002E1BE0` (`0035276D`); bit 21 for the movie player (`001B82E4`, `001B76C8`, `001B80A4`, `001B84BE`), saving and loading (`0058252C`, `005823F8`, `005828B4`, `00582F1B`), the title screen (`00393A29`, `00393E07`), a Config screen widget (`0023FC78`, `0024024B`) and the callback `002CEB40` that `002CEFA0` installs (`002CEDE5`, `002CEBB6`) | `0`-`18`, `21` |
| `2` | battle selection, `00313A00`, below | `0`-`8`, `10`-`12`, `20` |
| `3` | verbs `questresultwindow` `0x37C` and `queststartwindow` `0x386` (`00344C84`, `00345704`, `0034515F`, `003464E8`) and `00268D10`/`00263050` | the mask |
| `4` | the screen-mask verbs `maskopen` `0x08A`, `maskopenfast` `0x3B5`, `mesvmaskopen` `0x446`, `mesvmaskopenfast` `0x447`, `maskclose` `0x08B`, `maskclosefast` `0x3B6` | `0`, `1`, `9`, `20` |
| `6` | user control, verbs `ucon` and `ucon_4a5` (`0026C70C`, `0026C80C`, `0026C82C`) and `00263660`, `0026C3E0` | the mask |
| `7` | the full-screen frame modes: set by `00228930` and `002E09A0`, cleared by the main loop (`0022BBA1`-`0022BBC5`) | `0`, `1`, `9`, `20` |
| `8` | the menu-request family, below | `0`-`2`, `4`-`9`, `11`, `12`, `20` |
| `9` | verb `crossfade` `0x16F` (`002F1AD4`, `002F1AE1`) and its completion (`002F19D3`, `002F19E0`) | `0`, `20` |
| `10` | a timed hold after a menu request (`002F1C8B`, `002F18AC`) | `1` |
| `12` | user control (`0026C738`) and a spawn group's last member dying (`00306F9A`), through `00307140` | `0`, `3`-`8`, `11`, `12`, `20` |
| `13` | cleared only: `0025B500` jumps to `002E1CD0` with clear 1 and row 13 (`0025B567`-`0025B573`) | - |
| `15` | the pause menu, `00229590` (`002299BB`-`002299DB`, `00229785`-`002297A9`) | `0`, `1`, `9`, `20` |

Rows 5, 11 and 14 have no writer.

### Row 8

Five helpers write most of row 8, each setting or clearing a fixed group of bits:

| Helper | Writes |
|---|---|
| `00254850` | ten sets when its argument is non-zero (`00254861`-`002548DA`) |
| `002547D0` | seven sets or clears (`002547F2`-`00254836`) |
| `002548F0` | four (`00254911`-`00254937`) |
| `00254940` | one (`00254964`), then `002547D0` |
| `00254980` | seven (`002549A2`-`002549E2`) |

They are called from `0035BC50` (`0035BEB7`), `0035C770` (`0035C778`), `0035C7B0` (`0035C844`-`0035C870`),
`0035C8A0` (`0035C8B5`-`0035C8D7`), `0035C8E0` (`0035C8F3`), `0035C920` (`0035C938`), `0035C940` (`0035C955`), the
party-down window `0035D6B0` (`0035D858`), `0035D8D0` (`0035D90A`-`0035D96A`), `0035D980` (`0035DA3E`), `0035DA80`
(`0035DAB3`) and game over `003EF830` (`003EF8A0`, `003EF8A7`).

The other row-8 writers are the battle command menu (`00276715`, `00279FE9`), the party-down window itself
(`0035D73B`-`0035D84C`), the chocobo dismount and ride (`0035C990`-`0035CA2D`, `0035CF30`-`0035CF79`), and the
target cursor: `003C8990` and `003C8A50` (`003C8A0A`, `003C8AF2`) and the callback `003C8B70` that `003C8A20`
installs, which clears bit 0 five times (`003C8C97`-`003C9085`).

### Battle selection

`00313A00` rewrites row 2 every field frame (`00313A68`-`00313AF5`). Bits 0, 2-8, 11, 12 and 20 are set while a
battle unit is selected (`02089350`). Bit 1 is set then, or while Escape Mode is on (`00253B90`). Bit 10 follows the
area's bit 15 (`00377C20`). It is called from the field frame (`00234624`) and from `00313DB0`.

### The Start button

When the Start screen opens, `00228930` copies all 16 rows to `01FD4700` (the `002E1020` loop at `00228972`) and
sets row 7 through `002E2240(1)` (`002E2248`). On close, `00229510` clears row 7 through `002E2240(0)` (`00229526`,
`002E2265`) and writes back rows 2 and 8 only, clearing and re-setting each of bits 0-21 from the copy (`00229554`,
`00229562`).

### What each bit blocks

| Bit | Blocks |
|---:|---|
| `0` | the main menu with Triangle (`00253D6E`) and its requests (`002E1AB9`, `002E1B31`, `002E25C7`) |
| `4` | the Circle or Cross interact press (`0025413F`) and force fight (`002736F0`, `0027399F`, `002C6580`) |
| `6`, `9` | Escape Mode, forced off (`00252B8C`, `00252B92`) |
| `10` | the battle command menu with Square or the confirm button (`00253F83`, `002541A4`, `0035D66D`), changing the leader (`0035D98D`), Escape Mode (`00252BA2`, `00252BE6`), the battle display and the map screens (`0028333C`, `00400F6F`, `00400FAD`, `004017B0`) |
| `11` | the Select and L3 presses (`00253E00`, `00253F0A`, `00253ECD`) |
| `12`, `16`, `17` | Start's arms (`002288C8`, `0022887E`, `00228893`) |
| `18` | the target cursor (`003C9176`, `003C919F`) |
| `21` | opening the pause menu (`002283DA`, `002283E7`) and the audio hold (`00229B03`) |

No reader tests bits 7, 14, 15 or 20.

Bits 13 and 19 do not block anything: they steer Start's event-skip arm. Bit 19 must be set for that arm to run
at all (`002288F6`), which is why the movie busy bit clears it. Inside the Start handler `002287D0`, with bit 19 set, the arm it passes to `00228700` is 1 only when bit 13 is set and
`003606B0` finds a non-zero word among `022CB9C4`, `022CB9C8` and `022CB9CC`, and 2 otherwise
(`002288F6`-`00228911`). `00360880` walks the same three words, takes the lowest set bit of each and runs that skip
through `00360710`.

`00228380`, which holds the bit-21 test, first starts the task `00228490` when `0017E4C0` answers 0
(`0022839B`-`002283AE`). `0017E4C0` reads the application's byte `+0x27`, the window-active byte: application slot 14
(`007A0B40`) stores it, called by the window procedure with 1 when a new window is in front (`0079914C`) and by
`007A4150`, which also posts message `0x8001` to show or hide the cursor. The task's pointer `01FD4948` is the cell
`00228480` tests.

### Menu requests

`00254500` turns the combined mask into a set of refused menu requests: for each of bits 0-21 that is set, it ORs in
that bit's word of `01E0C2C0` (`00254500`-`0025453C`). The menu router refuses those requests (`00254B80`-`00254BC5`).

| Bit | Requests refused |
|---:|---|
| `0`, `3` | 2, the main menu |
| `1` | 1, the battle command menu; 3, choosing the leader; 5, cycling targets |
| `2`, `10` | 3 |
| `5` | 5 |
| `6` | 14 |
| `8` | 1, and 21 |
| `9` | 5, and 14 |

## Modding notes

- To keep a menu shut from a script, `setmenudisablestatus` owns row 1 bits 0-18; the other rows are rewritten by
  their holders.
- A row number below 0 passes the signed test and writes below the table at `0215F1C0`.
- In row 0 the movie verbs and the actor and field loads all write the mask `0x139203`, so one holder's clear also
  removes the bits another holder set there.

## Related

- [Escape Mode](escape.md) - the toggle bits 6, 9 and 10 force off.
- [Keymap file](keymap-file.md) - the buttons the arbiter reads.
- [Menu requests](../Menus-And-HUD/menus.md) - the request ids and the router.
