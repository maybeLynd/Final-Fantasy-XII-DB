---
title: "Dialogs: the confirm window behind every yes-or-no question, notice and the item sort, and three single-screen boxes"
kind: "system"
category: "Menus and HUD"
addresses: "0057C480, 0057C380, 002CDF20, 002CE370, 00566680, 0056F810, 00556F90, 00D23688"
---

## What the player sees

- A yes-or-no question, such as buying a license, opens a small window with Yes and No.
- Notices, such as an error or a newly obtained license, open the same window without a choice and close themselves
  after a few seconds or at any button.
- The item screen's Sort command opens it with the sort options.
- The Clan Primer opens on a list of Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips.

## How it works

### The confirm window

`0057C480` is the window's procedure. It is a single instance: building it stores it at the root's `+328`<sub>h</sub>
(`0057C4D9`), and message 18 clears that (`0057CC79`). Its create record comes from `0057C380`, whose three callers
pass fixed flags as the record's `+20`<sub>h</sub>, kept at `+630`<sub>h</sub> (`0057C4E4`-`0057C4E8`):

| Creator | Installed by | Flags | Used for |
|---|---|---|---|
| `002CDF20` | `002CDEA0` | `C812`<sub>h</sub> (`002CE086`) | the yes-or-no question: Yes posts `8100`<sub>h</sub>, No `8101`<sub>h</sub>, No is the default row |
| `002CE370` | `002CE2F0` | `411A`<sub>h</sub>; `511A`<sub>h</sub>, `1411A`<sub>h</sub>, `1511A`<sub>h</sub> for errors; `611A`<sub>h</sub> for tutorials and license announcements | the notice: 22 caption cases of a 28-slot switch |
| `00566680` | `005665B0` | `8036`<sub>h</sub> (`00566939`) | the item screen's sort picker |

Message 1 copies the caption into a `400`<sub>h</sub>-byte buffer at `+1B0`<sub>h</sub>, measures it, keeps the window at least `60`<sub>h</sub>
wide, and clears eight option rows at `+5B0`<sub>h</sub>-`+62C`<sub>h</sub> (`0057C4BF`-`0057C682`).

### The flag bits

| Bit | Effect |
|---|---|
| `2`<sub>h</sub> | cancellable: cancel posts `8102`<sub>h</sub> to the owner (`0057CAD1`); without it, cancel moves the cursor to the default row |
| `8`<sub>h</sub> | notice: no list is built (`0057C6F3`), the pad is read directly, and confirm posts `8100`<sub>h</sub> |
| `10`<sub>h</sub>, `2000`<sub>h</sub> | frame variants 1 and 4 (`0057C7EE`-`0057C802`) |
| `20`<sub>h</sub> | a one-line caption (`0057C506`, `0057C90F`) |
| `800`<sub>h</sub> | the hand cursor stays on the chosen row while the window closes (`0057C7CC`) |
| `1000`<sub>h</sub> | the window closes itself after `+63A`<sub>h</sub> frames; the notice sets 180 (`0057C9E1`) |
| `4000`<sub>h</sub> | a dimmed backdrop at `+D8`<sub>h</sub> (`0057CD77`), released on close (`0057C34A`) |
| `8000`<sub>h</sub> | the header label is `4B42`<sub>h</sub> instead of `4B48`<sub>h</sub> (`0057C93E`) |
| `10000`<sub>h</sub> | any button confirms, and the timed close counts as confirm (`0057CA09`-`0057CA1C`) |
| `4`<sub>h</sub>, `40`<sub>h</sub>, `80`<sub>h</sub>, `100`<sub>h</sub>, `200`<sub>h</sub>, `400`<sub>h</sub> | the confirm sound: the list's sound id becomes `37`<sub>h</sub>, `19`<sub>h</sub>, `18`<sub>h</sub>, 3, 4 or `45`<sub>h</sub> (`0057CB8F`-`0057CBD7`); No plays 3 (`0057CB85`) |

### Stages and answers

1. Sub-command `8000`<sub>h</sub> moves the window through its stages, counted at `+637`<sub>h</sub> up to 2, and tells the owner the
   cursor row with `8103`<sub>h</sub> (`0057CC09`).
2. `8001`<sub>h</sub> is a pick: in notice mode it posts `8100`<sub>h</sub>; otherwise it reads the list's row and its option's flags and
   sets the confirm sound (`0057CB16`).
3. `8002`<sub>h</sub> is cancel: with bit `2`<sub>h</sub> it posts `8102`<sub>h</sub>, otherwise it moves the list back (`002D4650`, `0057CACB`).
4. Message 10 forwards input to the list unless the window is in notice mode (`0057C9A3`).

`00241D40`, installed by `00241BF0` and `00241C90`, is a second confirm procedure that reads the same layout keys.
Its row callback `00241D00` draws Yes (`menu_command.bin` `3E8`<sub>h</sub>) on row 0 and No (`3E9`<sub>h</sub>) on the other.

The procedure registers itself in the table `0208EA60` under slot 2 when its creator's root is `[0208EA38]`, 4 for `[0208EA50]`
and 1 otherwise (`00241E11`-`00241E48`), and clears the slot when it closes (`0024257E`). `00241A50(slot)` answers
whether one is open; the battle menu asks with 1 (`0027C4D2`) and `00228C70` with 2 (`00228E65`). Its other
callers are `0027A353`, also in the battle menu, and `00229095`.

### The item sort bar

`00566680` is the sort strip in the item screen, installed by `005665B0`. Its message 12 (`00566794`) takes these
sub-commands:

| Sub-command | Does |
|---|---|
| `8102`<sub>h</sub> | closes the bar (`00244F00`) |
| `8103`<sub>h</sub> | shows the row's help: "Sort items in default order by category." (`CC1`<sub>h</sub>), "Sort by item strength." (`CC2`<sub>h</sub>), "Sort by amount." (`CC3`<sub>h</sub>) |
| `8104`<sub>h</sub>-`8106`<sub>h</sub> | the three sorts, Auto-sort (`4A8`<sub>h</sub>), By Strength (`4A9`<sub>h</sub>) and By Quantity (`4AA`<sub>h</sub>), passed as 0-2 to `002527B0(7, ...)` and `00565CD0` |

`00565CD0(screen, tab, sort)` sorts the tab's list (`00252F40` of the list id at `00D23960 + 4 x tab`) through
`00249CE0` with one of six comparators, and does nothing for a list of fewer than two items. Each comparator reads the
two items' query records (`0035D330(1, id << 16)`,
[item and ability ids](../Engine-Core/item-and-ability-ids.md)) and falls back to the next rule on a tie:

| Sort | Tab | Comparator | Order |
|---|---|---|---|
| Auto-sort | any | `002CFFE0` | class 6 items by `002CFDA0`; others by `+30`<sub>h</sub>, then the id |
| By Strength | `0`, `3` | `002CFD30` | `+58`<sub>h</sub> highest first, then `002CFDA0` |
| By Strength | `1` | `002CFEE0` | `+50`<sub>h</sub>; then for `+50`<sub>h</sub> = 2 `+58`<sub>h</sub> and `+5C`<sub>h</sub>, otherwise `+5C`<sub>h</sub> and `+60`<sub>h</sub>, highest first; then `002D01A0` |
| By Strength | `2` | `002D0100` | `+5C`<sub>h</sub>, then `+60`<sub>h</sub>, highest first, then `002CFDA0` |
| By Quantity | any | `002D0200` | the count `+24`<sub>h</sub> highest first, then `002CFFE0` |

`002CFDA0` orders by `+38`<sub>h</sub>, then `+30`<sub>h</sub>, then the id, and `002D01A0` by `+30`<sub>h</sub>, then the id, all lowest first.

Auto-sort is always offered; the other two rows depend on `00564380`. Message 18 clears the row highlights, sets the parent's sort-changed bit
`+180h |= 40000000h` and clears the root's `+2F0`<sub>h</sub> (`005666D4`). Message 15 frees its backdrop through `0057C340`
(`00566771`).

### The Clan Primer's category list

`0056F810` is installed only by `00574D00`, from the Clan Primer's back panel `00574E80`. It lists four records of the
table at `00D23688`, filtered by unlock (`0056F750`). Its message table at `0056FA80` serves ids 1, 10, 12, 14, 15 and 18,
and every other id goes to the default `0056FA73`.

| Record | Label | Help | Opens kind |
|---:|---|---|---:|
| 0 | Hunts | "Hunt information and progress." | 6 |
| 1 | Bestiary | "Insights on foes you have defeated." | 5 |
| 2 | Sky Pirate's Den | "What will it take to fill the den?" | 7 |
| 3 | Traveler's Tips | "Hints for the wary adventurer." | 4 |

A record is 6 bytes (below). A pick posts its kind to the parent with `8001`<sub>h</sub>
(`0056F96A`-`0056F9B5`). Records 4-11 hold the page titles of the eight Clan Primer page kinds: 4-7 point at
labels `1B58`<sub>h</sub>-`1B5B`<sub>h</sub>, which are empty, and 8-11 reuse the four labels above.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | label | label text |
| `02`<sub>h</sub> | `u16` | help | help text |
| `04`<sub>h</sub> | `u8` | kind | posted to the parent on a pick |
| `05`<sub>h</sub> | `u8` | flag | - |

### The license board's description box

`00556F90` shows text only and answers messages 1 and 2; its message-18 arm returns 0, as its default does. Its one installer `00556EC0` is called only from the
license board chooser `00557DB0` (`00557E76`, `00557EE5`). The chooser writes the board number to `+3D1`<sub>h</sub> on each
cursor step (`00558549`). Message 2 writes the board's name, `menu_command.bin` `3ED`<sub>h</sub> plus the board ("White Mage"
for board 0), as the header, and its description, `menu_message.bin` `838`<sub>h</sub> plus the board, split into three lines
at `+D0`<sub>h</sub> by `002B5730`.

## Modding notes

- A new yes-or-no question goes through `002CDF20`'s flags `C812`<sub>h</sub>; a notice through `002CE370`.
- Removing `2`<sub>h</sub> makes a question impossible to cancel; adding `10000`<sub>h</sub> lets any button confirm.
- The Clan Primer menu's labels, help lines and the page kind each option opens are the four records at `00D23688`.

## Related

- [Menus](menus.md) - how the screens that raise these dialogs open.
- [License board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board the question and the description box serve.
