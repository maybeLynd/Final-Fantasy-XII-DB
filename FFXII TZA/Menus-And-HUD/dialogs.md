---
title: "Dialogs: the confirm window behind every yes-or-no question, notice and the item sort, and three single-screen boxes"
kind: "system"
category: "Menus and HUD"
addresses: "0x0057C480, 0x0057C380, 0x002CDF20, 0x002CE370, 0x00566680, 0x0056F810, 0x00556F90, 0x00D23688"
---

## What the player sees

- A yes-or-no question, such as buying a license, opens a small window with Yes and No.
- Notices, such as an error or a newly obtained license, open the same window without a choice and close themselves
  after a few seconds or at any button.
- The item screen's Sort command opens it with the sort options.
- Two more screens have a box of their own: the Clan Primer opens on a list of Hunts, Bestiary, Sky Pirate's Den
  and Traveler's Tips, and the license board chooser shows the name and description of the board under the cursor.

## How it works

### The confirm window

`0x0057C480` is the window's procedure. It is a single instance: building it stores it at the root's `+0x328`
(`0x0057C4D9`), and message 18 clears that (`0x0057CC79`). Its create record comes from `0x0057C380`, whose three callers
pass fixed flags as the record's `+0x20`, kept at `+0x630` (`0x0057C4E4`-`0x0057C4E8`):

| Creator | Installed by | Flags | Used for |
|---|---|---|---|
| `0x002CDF20` | `0x002CDEA0` | `0xC812` (`0x002CE086`) | the yes-or-no question: Yes posts `0x8100`, No `0x8101`, No is the default row |
| `0x002CE370` | `0x002CE2F0` | `0x411A`; `0x511A`, `0x1411A`, `0x1511A` for errors; `0x611A` for tutorials and license announcements | the notice: 22 caption cases of a 28-slot switch |
| `0x00566680` | `0x005665B0` | `0x8036` (`0x00566939`) | the item screen's sort picker |

Message 1 copies the caption into a `0x400`-byte buffer at `+0x1B0`, measures it, keeps the window at least `0x60`
wide, and clears eight option rows at `+0x5B0`-`+0x62C` (`0x0057C4BF`-`0x0057C682`).

### The flag bits

| Bit | Effect |
|---|---|
| `0x2` | cancellable: cancel posts `0x8102` to the owner (`0x0057CAD1`); without it, cancel moves the cursor to the default row |
| `0x8` | notice: no list is built (`0x0057C6F3`), the pad is read directly, and confirm posts `0x8100` |
| `0x10`, `0x2000` | frame variants 1 and 4 (`0x0057C7EE`-`0x0057C802`) |
| `0x20` | a one-line caption (`0x0057C506`, `0x0057C90F`) |
| `0x800` | the hand cursor stays on the chosen row while the window closes (`0x0057C7CC`) |
| `0x1000` | the window closes itself after `+0x63A` frames; the notice sets 180 (`0x0057C9E1`) |
| `0x4000` | a dimmed backdrop at `+0xD8` (`0x0057CD77`), released on close (`0x0057C34A`) |
| `0x8000` | the header label is `0x4B42` instead of `0x4B48` (`0x0057C93E`) |
| `0x10000` | any button confirms, and the timed close counts as confirm (`0x0057CA09`-`0x0057CA1C`) |
| `0x4`, `0x40`, `0x80`, `0x100`, `0x200`, `0x400` | the confirm sound: the list's sound id becomes `0x37`, `0x19`, `0x18`, 3, 4 or `0x45` (`0x0057CB8F`-`0x0057CBD7`); No plays 3 (`0x0057CB85`) |

### Stages and answers

1. Sub-command `0x8000` moves the window through its stages, counted at `+0x637` up to 2, and tells the owner the
   cursor row with `0x8103` (`0x0057CC09`).
2. `0x8001` is a pick: in notice mode it posts `0x8100`; otherwise it reads the list's row and its option's flags and
   sets the confirm sound (`0x0057CB16`).
3. `0x8002` is cancel: with bit `0x2` it posts `0x8102`, otherwise it moves the list back (`0x002D4650`, `0x0057CACB`).
4. Message 10 forwards input to the list unless the window is in notice mode (`0x0057C9A3`).

`0x0057C3E0(window, element, row)` is the list's row callback, given in the create record `0x002D14E0` takes
(`0x0057C722`). While `+0x636` is set it colours the element (`+0x90`) with `0x002DD7E0(6)` when the row's word
`+0x5B8 + 16 x row` equals `+0x638`, else with `0x002DD7E0(2)` unless the row's `+0x5BC` has bit `0x1`, draws
`0x002D8910(element, 0, 0, [window + 16 x (row + 0x5B)], 0)`, and puts the colour back to `0x002DD7E0(0)`.

`0x00241D40`, installed by `0x00241BF0` and `0x00241C90`, is a second confirm procedure that reads the same layout keys.
Its row callback `0x00241D00` draws Yes (`menu_command.bin` `0x3E8`) on row 0 and No (`0x3E9`) on the other.
`0x00241B40(window)` answers a pick: message 12 with `0x8100` to the owner `+0xD0` for row 0 of the list `+0xC8`
and `0x8101` for any other. `0x00241A70(window)` answers a cancel by the mode byte `+0x3BE`: 1 sends `0x8101`, 2
sends `0x8102`, and 0 moves the list back to the row `+0xC0` (`0x002D4650`), first posting `0x8104` to the owner
when `+0x3C4` bit `0x800` is set.

`0x002477A0(window, v)`, which `0x00241D40` calls with 4 (`0x00242101`), stores `v & 7` in bits `0x70000` of `+0x44` and sets
the two bytes `+0xAC` and `+0xAD` from that field: with its bit `0x4` set, `+0xAD` becomes `0xF9` when bit `0x2` is
set and `+0xAC` becomes `0xF9` when bit `0x1` is set; with bit `0x4` clear, each byte becomes `0xF9` or 6 by its bit.

Four builders fill the record `0x00241C90` takes and open the window:

- `0x00394380(text, owner)`, from `0x003939B0`, turns the second draw pass on (`0x00247780(1)`) and opens it with text
  `0x002F9860(text)` under the root `[0x0208EA28]`, flags `0x1002` and mode 2.
- `0x003948B0(text, owner, flags, options)` opens it under `[0x0208EA28]` with the options' bits under mask `0x1F` (`+0x48`) turned
  into window bits `0x8`, else `0x200` (with the default row from `+0x44`), then `0x10`, `0x800` and `0x400`; flags with
  `& 0xFF0` of `0x70` or `0xD0` give style 1 or 2. `0x0023E020`, `0x0023E560`, `0x00252030`, `0x0057AA00`, `0x00583990`
  and `0x00583FD0` call it.
- `0x003949B0(text, owner, options)` and `0x00394A90` do the same from the options' word `+0x14` (bit `0x4` to `0x20`, bit `0x10`
  to `0x8` or else bit `0x8` to `0x200`, bit `0x20` to `0x10`, bit `0x40` to `0x800`, bit `0x80` to `0x100`, bit `0x100` to `0x400`) in
  style 2, under `[0x0208EA28]` or, for `0x00394A90`, the
  root `[0x0208EA50]` (slot 4); `0x00394A90` serves `0x00583FD0`.

The procedure registers itself in the table `0x0208EA60` under slot 2 when its creator's root is `[0x0208EA38]`, 4 for `[0x0208EA50]`
and 1 otherwise (`0x00241E11`-`0x00241E48`), and clears the slot when it closes (`0x0024257E`). `0x00241A50(slot)` answers
whether one is open; the battle menu asks with 1 (`0x0027C4D2`) and `0x00228C70` with 2 (`0x00228E65`). Its other
callers are `0x0027A353`, also in the battle menu, and `0x00229095`.

### The item sort bar

`0x00566680` is the sort strip in the item screen, installed by `0x005665B0`. Its message 12 (`0x00566794`) takes these
sub-commands:

| Sub-command | Does |
|---|---|
| `0x8102` | closes the bar (`0x00244F00`) |
| `0x8103` | shows the row's help: "Sort items in default order by category." (`0xCC1`), "Sort by item strength." (`0xCC2`), "Sort by amount." (`0xCC3`) |
| `0x8104`-`0x8106` | the three sorts, Auto-sort (`0x4A8`), By Strength (`0x4A9`) and By Quantity (`0x4AA`): the code minus `0x8103`, 1-3, is stored as the tab's sort through `0x002527B0(7, tab, ...)` (`0x005667DD`), and the code minus `0x8104`, 0-2, is passed to `0x00565CD0` (`0x005667FD`) |

`0x002527B0(7, tab, v)` stores `v` in the byte `+0x70 + tab` of `[0x020927C0]`, the tab clamped to 0-31 (`0x002527F7`,
`0x0025280A`), and `0x002526F0(7, tab, 1)` reads it back (`0x00252763`, `0x00252777`). When the bar opens, a stored value
other than 0 puts the cursor on the row whose code is `0x8103` plus that value (`0x005668F7`-`0x00566905`, `0x0057CD00` at
`0x005669A5`, `0x002D4650` at `0x005669C1`); with 0, or when that row is not listed, the cursor starts on row 0
(`0x00566900`, `0x0057CD37`).

`0x00565CD0(screen, tab, sort)` sorts the tab's list (`0x00252F40` of the list id at `0x00D23960 + 4 x tab`) through
`0x00249CE0` with one of five comparators (`0x00565D43`-`0x00565D7F`), and does nothing for a list of fewer than two items. Each comparator reads the
two items' query records (`0x0035D330(1, id << 16)`,
[item and ability ids](../Engine-Core/item-and-ability-ids.md)) and falls back to the next rule on a tie:

| Sort | Tab | Comparator | Order |
|---|---|---|---|
| Auto-sort | any | `0x002CFFE0` | class 6 items by `0x002CFDA0`; others by `+0x30`, then the id |
| By Strength | `0`, `3` | `0x002CFD30` | `+0x58` highest first, then `0x002CFDA0` |
| By Strength | `1` | `0x002CFEE0` | `+0x50`; then for `+0x50` = 2 `+0x58` and `+0x5C`, otherwise `+0x5C` and `+0x60`, highest first; then `0x002D01A0` |
| By Strength | `2` | `0x002D0100` | `+0x5C`, then `+0x60`, highest first, then `0x002CFDA0` |
| By Quantity | any | `0x002D0200` | the count `+0x24` highest first, then `0x002CFFE0` |

`0x002CFDA0` orders by `+0x38`, then `+0x30`, then the id, and `0x002D01A0` by `+0x30`, then the id, all lowest first.

`0x002D0070` and `0x002CFE40` are `0x002CFFE0` and `0x002CFDA0` for rows that carry the item id in the word `+8`
instead of `+0`. `0x002C38B0` (`0x002C3AF8`) and `0x002C4720` (`0x002C4947`, `0x002C4AF7`, `0x002C4E4E`, `0x002C4FCB`)
pass `0x002D0070` to `0x00249CE0`.

Auto-sort is always offered; the other two rows depend on `0x00564380`. Message 18 clears the row highlights, sets the parent's sort-changed bit
`+0x180 |= 0x40000000` and clears the root's `+0x2F0` (`0x005666D4`). Message 15 frees its backdrop through `0x0057C340`
(`0x00566771`).

### The Clan Primer's category list

`0x0056F810` is installed only by `0x00574D00`, from the Clan Primer's back panel `0x00574E80`. It lists four records of the
table at `0x00D23688`, filtered by unlock (`0x0056F750`). Its message table at `0x0056FA80` serves ids 1, 10, 12, 14, 15 and 18,
and every other id goes to the default `0x0056FA73`.

| Record | Label | Help | Opens kind |
|---:|---|---|---:|
| 0 | Hunts | "Hunt information and progress." | 6 |
| 1 | Bestiary | "Insights on foes you have defeated." | 5 |
| 2 | Sky Pirate's Den | "What will it take to fill the den?" | 7 |
| 3 | Traveler's Tips | "Hints for the wary adventurer." | 4 |

A record is 6 bytes (below). A pick posts its kind to the parent with `0x8001`
(`0x0056F96A`-`0x0056F9B5`). Records 4-11 hold the page titles of the eight Clan Primer page kinds: 4-7 point at
labels `0x1B58`-`0x1B5B`, which are empty, and 8-11 reuse the four labels above.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | label | label text |
| `+0x02` | `u16` | help | help text |
| `+0x04` | `u8` | kind | posted to the parent on a pick |
| `+0x05` | `u8` | flag | - |

### The license board's description box

`0x00556F90` shows text only and answers messages 1 and 2; its message-18 arm returns 0, as its default does. Its one installer `0x00556EC0` is called only from the
license board chooser `0x00557DB0` (`0x00557E76`, `0x00557EE5`). The chooser writes the board number to `+0x3D1` on each
cursor step (`0x00558549`). Message 2 writes the board's name, `menu_command.bin` `0x3ED` plus the board ("White Mage"
for board 0), as the header, and its description, `menu_message.bin` `0x838` plus the board, split into three lines
at `+0xD0` by `0x002B5730`.

## State

The table `0x0208EA60` holds one 8-byte window pointer per slot. `0x00241D40` stores itself at the slot it picked
(`0x00241E48`) and clears it when it closes (`0x0024257E`), both through the slot index.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0208EA68` | `void*` | 0 (zero-filled tail) | slot 1: the second confirm window opened under a root other than `[0x0208EA38]` and `[0x0208EA50]`, 0 when none is open | `0x00241D40`: the window (`0x00241E48`), 0 when it closes (`0x0024257E`); `0x002419B0`, 0 after it closes the window (`0x00241A04`, `0x00241A31`) | `0x002419B0` (`0x002419B6`); `0x00241A50(slot)` (`0x00241A5C`), with 1 from the battle menu (`0x0027C4D2`) and with a variable slot from `0x0027A353` and `0x00229095` |

`0x002419B0`, run by `0x0035BB70` at the field set-up and teardown (`0x0035BB99`), closes the slot-1 window unless its
`+0x7C` bit `0x20` is set: it hides it (`0x00244DD0`) when bits `0x1` and `0x20` of `+0x40` are set, and otherwise sends it message 15
(`0x00915058`) and releases it (`0x00245020`).

No other instruction reaches `0x0208EA68`. The table's address is taken only by `0x00241A50`.

## Modding notes

- A new yes-or-no question goes through `0x002CDF20`'s flags `0xC812`; a notice through `0x002CE370`.
- Removing `0x2` makes a question impossible to cancel; adding `0x10000` lets any button confirm.
- The Clan Primer menu's labels, help lines and the page kind each option opens are the four records at `0x00D23688`.

## Related

- [Menus](menus.md) - how the screens that raise these dialogs open.
- [License board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board the question and the description box serve.
