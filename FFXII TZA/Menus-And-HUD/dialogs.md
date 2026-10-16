---
title: "Dialogs: the confirm window behind every yes-or-no question, notice and the item sort, and three single-screen boxes"
kind: "system"
category: "Menus and HUD"
summary: "The shared confirm window and the boxes that sit beside it: who creates the confirm window and with which flags, what each flag bit changes (cancelling, notice mode, timed dismiss, any-button confirm, the header label, the backdrop and the confirm sound), its stages and the answers it posts back, the item screen's sort bar, the Clan Primer's category list with its four records, and the license board's description box."
addresses: ["0057C480", "0057C380", "002CDF20", "002CE370", "00566680", "0056F810", "00556F90", "00D23688"]
---

# Dialogs: the confirm window behind every yes-or-no question, notice and the item sort, and three single-screen boxes

## What the player sees

- A yes-or-no question, such as buying a license, opens a small window with Yes and No.
- Notices, such as an error or a newly obtained license, open the same window without a choice and close themselves
  after a few seconds or at any button.
- The item screen's Sort command opens it with the sort options.
- The Clan Primer opens on a list of Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips.

## How it works

### The confirm window

`0057C480` is the window's procedure. It is a single instance: building it stores it at the root's `+0x328`
(`0057C4D9`), and message 18 clears that (`0057CC79`). Its create record comes from `0057C380`, whose three callers
pass fixed flags as the record's `+0x20`, kept at `+0x630` (`0057C4E4`-`0057C4E8`):

| Creator | Installed by | Flags | Used for |
|---|---|---|---|
| `002CDF20` | `002CDEA0` | `0xC812` (`002CE086`) | the yes-or-no question: Yes posts `0x8100`, No `0x8101`, No is the default row |
| `002CE370` | `002CE2F0` | `0x411A`; `0x511A`, `0x1411A`, `0x1511A` for errors; `0x611A` for tutorials and license announcements | the notice: 22 caption cases of a 28-slot switch |
| `00566680` | `005665B0` | `0x8036` (`00566939`) | the item screen's sort picker |

Message 1 copies the caption into a `0x400`-byte buffer at `+0x1B0`, measures it, keeps the window at least `0x60`
wide, and clears eight option rows at `+0x5B0`-`+0x62C` (`0057C4BF`-`0057C682`).

### The flag bits

| Bit | Effect |
|---|---|
| `0x2` | cancellable: cancel posts `0x8102` to the owner (`0057CAD1`); without it, cancel moves the cursor to the default row |
| `0x8` | notice: no list is built (`0057C6F3`), the pad is read directly, and confirm posts `0x8100` |
| `0x10`, `0x2000` | frame variants 1 and 4 (`0057C7EE`-`0057C802`) |
| `0x20` | a one-line caption (`0057C506`, `0057C90F`) |
| `0x800` | the hand cursor stays on the chosen row while the window closes (`0057C7CC`) |
| `0x1000` | the window closes itself after `+0x63A` frames; the notice sets 180 (`0057C9E1`) |
| `0x4000` | a dimmed backdrop at `+0xD8` (`0057CD77`), released on close (`0057C34A`) |
| `0x8000` | the header label is `0x4B42` instead of `0x4B48` (`0057C93E`) |
| `0x10000` | any button confirms, and the timed close counts as confirm (`0057CA09`-`0057CA1C`) |
| `0x4`, `0x40`, `0x80`, `0x100`, `0x200`, `0x400` | the confirm sound: the list's sound id becomes `0x37`, `0x19`, `0x18`, 3, 4 or `0x45` (`0057CB8F`-`0057CBD7`); No plays 3 (`0057CB85`) |

### Stages and answers

1. Sub-command `0x8000` moves the window through its stages, counted at `+0x637` up to 2, and tells the owner the
   cursor row with `0x8103` (`0057CC09`).
2. `0x8001` is a pick: in notice mode it posts `0x8100`; otherwise it reads the list's row and its option's flags and
   sets the confirm sound (`0057CB16`).
3. `0x8002` is cancel: with bit `0x2` it posts `0x8102`, otherwise it moves the list back (`002D4650`, `0057CACB`).
4. Message 10 forwards input to the list unless the window is in notice mode (`0057C9A3`).

`00241D40`, installed by `00241BF0` and `00241C90`, is a second confirm procedure that reads the same layout keys.

### The item sort bar

`00566680` is the sort strip in the item screen, installed by `005665B0`. Its message 12 (`00566794`) takes these
sub-commands:

| Sub-command | Does |
|---|---|
| `0x8102` | closes the bar (`00244F00`) |
| `0x8103` | shows the row's help: "Sort items in default order by category." (`0xCC1`), "Sort by item strength." (`0xCC2`), "Sort by amount." (`0xCC3`) |
| `0x8104`-`0x8106` | the three sorts, Auto-sort (`0x4A8`), By Strength (`0x4A9`) and By Quantity (`0x4AA`), passed as 0-2 to `002527B0(7, ...)` and `00565CD0` |

Auto-sort is always offered; the other two rows depend on `00564380`. Message 18 clears the row highlights, sets the parent's sort-changed bit
`+0x180 |= 0x40000000` and clears the root's `+0x2F0` (`005666D4`). Message 15 frees its backdrop through `0057C340`
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

A record is `{u16 label; u16 help; u8 kind; u8 flag}`. A pick posts its kind to the parent with `0x8001`
(`0056F96A`-`0056F9B5`). Records 4-11 hold the page titles of the eight Clan Primer page kinds: 4-7 point at
labels `0x1B58`-`0x1B5B`, which are empty, and 8-11 reuse the four labels above.

### The license board's description box

`00556F90` shows text only and answers messages 1 and 2; its message-18 arm returns 0, as its default does. Its one installer `00556EC0` is called only from the
license board chooser `00557DB0` (`00557E76`, `00557EE5`). The chooser writes the board number to `+0x3D1` on each
cursor step (`00558549`). Message 2 writes the board's name, `menu_command.bin` `0x3ED` plus the board ("White Mage"
for board 0), as the header, and its description, `menu_message.bin` `0x838` plus the board, split into three lines
at `+0xD0` by `002B5730`.

## Modding notes

- A new yes-or-no question goes through `002CDF20`'s flags `0xC812`; a notice through `002CE370`.
- Removing `0x2` makes a question impossible to cancel; adding `0x10000` lets any button confirm.
- The Clan Primer menu's labels, help lines and the page kind each option opens are the four records at `00D23688`.

## Related

- [Menus](menus.md) - how the screens that raise these dialogs open.
- [License board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board the question and the description box serve.
