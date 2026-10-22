---
title: "Gambits screen: the three gambit sets, switching lines on and off, moving them, choosing conditions and actions, and the save to the character"
kind: "system"
category: "Menus and HUD"
addresses: "0x00568B30, 0x005691E0, 0x00567D80, 0x00567F90, 0x0056B4D0, 0x0056AC50, 0x00569F90, 0x003282D0"
---

## What the player sees

- Gambits shows one character's gambit set: a header row that turns the character's gambits on or off, and one row per
  gambit slot with an ON/OFF switch, a condition and an action.
- The set and the character can be changed without leaving the screen; the sets slide in from the side.
- Choosing a condition or action opens a paged list; locked entries show as a placeholder, and a choice that does not
  fit is refused with a message such as "You do not have the license for this action."
- Every change is kept at once; there is no confirm on leaving.

## How it works

### Opening

The main menu's Gambits entry (`menu_command.bin` `0x4B9`, `0x0028224D`-`0x00282264`) and the script menu request `0x40`
([Menus](menus.md), host `0x002D70F0`, `0x002D726B`) both call `0x00568B30`. It creates three editors `0x005691E0`
(`0x00568B80`), one for each pane: the centre pane and the two off-screen panes that slide in when the set changes. Each
pane shows the member's selected set (`0x00327C40`, set index at `[0x02EBF190] + 0x7370 + member x 4`).

### Rows

`0x00567B60` fills the rows:

| Row | Shows |
|---|---|
| `0` | the character's name; its switch is bit 2 of the party record (`0x00309B40`) |
| 1 to the slot count | one gambit line: condition and action names, "-" (`0x3EB`) when empty, and ON or OFF from the set's mask |

The slot count is the set's byte `+0x32` ([Gambits](../Enemy-AI-And-Gambits/gambits.md)); the script verb
`setgambit_slotmax` adds to it for all three sets, between 0 and 12 (`0x00327930`). A line is coloured one way for a Foe
condition and another for Ally or Self (`0x0031D0D2`, `0x01EED270`), or greyed when it is off (`0x00568BB0`).

### Columns and help

Left and right move between the switch, the condition and the action on a line row (`0x00569C4B`-`0x00569C96`). The help
line follows the column (`0x00569E6D`):

| Where | Help (`help_menu.bin`) |
|---|---|
| header row | "Toggle gambits ON/OFF." (`0xCF2`) |
| switch | "Toggle slot ON/OFF. (Can be cleared using ...)" (`0xCF1`) |
| condition | "Change the conditions under which an action is performed. ..." (`0xCEE`) |
| action | "Change which action is performed. ..." (`0xCEF`) |

`0x005678C0(column)` gives the help kind of a column from `0x00D234F8`: none, 4 and 5 for columns 0 to 2, and 8 or 9 for
column 3, by the language test `0x00254A10` (`0x00569CB8`, `0x00569D87`, `0x00569DA8`). `0x00568AA0` paints a line's number in
two digits (`0x0029F6E0`), nudging the second label for numbers below 10 unless `0x00254A10` is true.

### Changing set and character

Bit 9 of the pressed or repeat word (`0x02F97392`, `0x02F97394`; R2 in the [Controls](../Controls-And-Input/controls.md) order) moves to the next of the
three sets and bit 8 (L2) to the previous one (`0x00569AF1`, `0x005699F0`). The three panes slide by `0x780` (`0x002468A0`),
the pane pointers rotate and the new centre reloads (`0x0056A010`), with sound `0x51`. Held R1 and L1 step to the next or
previous party member (`0x00568280`, `0x00567990`). Each member's cursor row and column are kept (`0x00569938`-`0x00569953`).

### Confirming a row

The line list posts confirm (`0x8001`), cancel (`0x8002`), clear (`0x8003`) and end-of-move (`0x8004`) to the editor,
in the convention of [Dialogs](dialogs.md). Confirm runs `0x00567D80`:

1. On the header row it flips the character's gambits on or off (`0x00311AF0`, `0x00567DDD`), sound `0x12` or `0x13`.
2. On a condition or action it opens the condition or action list (`0x0056B350`).
3. On a switch it picks the line up for moving (`0x005687F0`).
4. On the same switch again it turns the line on or off and saves; an empty line cannot be turned on (sound 5,
   `0x00567ECC`).
5. On another row's switch it moves the line there (`0x00567F90`) and saves.

A move is an insertion: the lines between the old and new row shift one place, and the moved line takes the new row.
While a line is held, `0x00568FE0` slides each line between the two rows by 4 a frame, and the editor's tick `0x005678F0`
eases the scroll `+0x343` (`0x00248F40`) and pulses the held line through `0x005682C0`: its level `+0x350` swings between
`0x80` and `0xFF` by `0x20` a frame, and fades by 16 a frame once nothing is held.
Cancel while a line is picked up returns it; cancel otherwise saves and closes all three editors (`0x005679D0`).

### Clearing a line

Clear (`0x8003`, `0x00569E06`) runs `0x0056A1D0(editor, -1, row)`: it empties both the condition and the action, turns the
line off and saves, with sound `0x19`. The header row cannot be cleared.

### The condition and action lists

`0x0056B350` opens the list `0x0056B4D0` and slides the editor aside by `GambitTargetListMoveX` or `GambitActionListMoveX`
(`0x01F2CB10`, `0x01F2CB14`). The help line shows the highlighted entry's own help text (the list's `0x8000` arm,
`0x00291D80`).

| List | Built from | Pages |
|---|---|---|
| conditions | `0x0031EB20` kind `0x23`, grid from condition row `+0x16`/`+0x17` (`0x00238880`) | 15 of up to 17 |
| actions | `0x0031EB20` kind `0x22`, grid from action row `+0x38`/`+0x39` (`0x00237FC0`) | 11 of up to 17; page 0 holds only Attack |

L1 and R1, or left and right, turn the page (`0x0056AAC0`, `0x0056AD50`), and the tabs are coloured by target or command
class (`0x0056ADA0`). An entry not yet owned is listed as the placeholder `0x4C7`, with "Select conditions for an
action." (`0xCD8`) or "Select action to be performed." (`0xCD7`) as its help, and cannot be picked (`0x0056BC70`,
`0x0056A890`).

The pages are built by `0x0056B100` (conditions, the page count from `0x00327BD0`) and `0x0056AE80` (actions, `0x00327BB0`),
eight bytes a page from `+0x300`, from the run state of `0x0056A3D0` and the tab colouring of `0x0056ADA0`:

- each page's entries come from `0x0031EB20`; a page with none, or whose entries all have state `0x0F`, gets colour
  `0x87` and is disabled (state 2 for conditions, 3 for actions);
- a condition page is coloured by the target class `+0x38` of its entries' class `0xB` record: 1 `0x85`, 2 `0x86`,
  3 `0x84`; an action page by the class 1 record its item names (`0x0035D330(0x14)` `+0x2C`): 5 `0x8B`, 8 `0x89`,
  9 `0x8A`, else `0x88`;
- the page and row of the line's current entry go to `+0x595` and `+0x599`/`+0x59A` (page 0, row 0 when absent), and an
  entry equal to the argument with state 0 returns 1 and stores its page and row at the editor's `+0x334`/`+0x335`.

The rows use painters at `+0x120`: `0x0056BBD0` for a condition (the name, in colour 2 when its state byte is not 0)
and `0x0056A780` for an action, which adds the icon frame and, when its byte `+0x11` is set, the number `+0x0C` with text
`0x465F` (`0x0029FF60`); the frame is hidden for an empty entry, id `0x96`, or state `0x0F`.

`0x005678A0` re-attaches the member-scoped pane `[0x02CA96D8]` (`0x005677A0`) to the root `[0x0208EA28]` (`0x00246AD0`) for the
two openers (`0x00282286`, `0x002D7270`).

### Refusals

Confirming an entry runs `0x0056AC50`. An entry whose state is not 0 is refused, and its message shows for 180 frames:

| State | List | Message (`help_menu.bin`) |
|---|---|---|
| `0x10` | actions | "You do not have the license for this action." (`0xCF0`, licence test `0x00323EC0`) |
| `0x21`-`0x23` | actions | "This action cannot be performed on a foe." / "...on an ally." / "...on the user." (`0xC75`-`0xC77`) |
| `0x1D`-`0x1F` | conditions | "The selected action cannot target a foe." / "...an ally." / "...the user." (`0xC78`-`0xC7A`) |

The target states come from `0x00327A10(action, condition)`: the condition's target, Foe, Ally or Self, must be allowed
by the action row's `+0x0C` (`8` for Foe, `4` for Ally, `1` or `4` for Self). An accepted entry is written into the
line (`0x0056A1D0`) and saved, and the list closes after 32 frames.

### The save

Every edit saves at once. `0x00569F90` copies the rows into the editor's copy of the set and jumps to `0x003282C0`; a move
ends in the same jump (`0x005680D7`). `0x003282D0(member, set)`:

1. picks the member's selected set at `[0x02EBF190] + 0x5B10 + (member x 3 + selected) x 0x34` (`0x0032830A`-`0x00328324`);
2. copies the 0x34-byte set into it (`0x00328327`-`0x00328347`);
3. calls `0x00328140`, which rebuilds the member's gambit orders at `0x02089378`, one 24-byte order per line that is on and
   filled ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

These are the only calls to `0x003282C0`, `0x003282D0` and `0x00328140` in the image (a scan of every function for direct
calls).

### Script restore and steering

When the editor finishes loading it keeps a copy of the set (`0x0056955F`). On close it writes that copy back only when
`[0x0209AC30] + 0xDEB` is set (`0x00569242`-`0x00569259`), which the script verb `fsmenu_registrestore` sets (`0x00511AA0`,
`0x002D7D40`) and `0x002D6F90` clears. So a scripted lesson can put the set back as it was, while ordinary use keeps every
edit.

The verbs `fsmenu_changechip`, `fsmenu_movechip`, `fsmenu_movelist` and `fsmenu_registopenchip` steer the cursor for a
lesson: the editor's state machine `0x0056A3D0` and the list's `0x0056BE40` allow only the input that moves toward the
target row, page and entry, then only confirm (`0x002D66A0`).

## Shipped data

| | |
|---|---|
| condition list | 15 pages of up to 17, 255 conditions placed |
| action list | 11 pages: 1, 17, 17, 17, 17, 13, 17, 17, 17, 17 and 7 actions |

## Modding notes

- A condition's or action's place in the lists is its grid column and row in the condition or action table.
- Which targets an action accepts is its row's byte `+0x0C`; widening it lets more conditions pair with it.
- `setgambit_slotmax` adds its argument to the slot count of all three sets, clamped to 0-12.

## Related

- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the sets, presets and how the orders are walked in battle.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the condition table.
- [Menus](menus.md) - the menu entry and the script request.
- [Dialogs](dialogs.md) - the list widget's sub-commands.
