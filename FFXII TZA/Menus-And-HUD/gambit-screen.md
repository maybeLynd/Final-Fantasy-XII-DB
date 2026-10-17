---
title: "Gambits screen: the three gambit sets, switching lines on and off, moving them, choosing conditions and actions, and the save to the character"
kind: "system"
category: "Menus and HUD"
addresses: "00568B30, 005691E0, 00567D80, 00567F90, 0056B4D0, 0056AC50, 00569F90, 003282D0"
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

The main menu's Gambits entry (`menu_command.bin` `4B9`<sub>h</sub>, `0028224D`-`00282264`) and the script menu request `40`<sub>h</sub>
([Menus](menus.md), host `002D70F0`, `002D726B`) both call `00568B30`. It creates three editors `005691E0`
(`00568B80`), one for each pane: the centre pane and the two off-screen panes that slide in when the set changes. Each
pane shows the member's selected set (`00327C40`, set index at `[02EBF190] + 7370h + member x 4`).

### Rows

`00567B60` fills the rows:

| Row | Shows |
|---|---|
| `0` | the character's name; its switch is bit 2 of the party record (`00309B40`) |
| 1 to the slot count | one gambit line: condition and action names, "-" (`3EB`<sub>h</sub>) when empty, and ON or OFF from the set's mask |

The slot count is the set's byte `+32`<sub>h</sub> ([Gambits](../Enemy-AI-And-Gambits/gambits.md)); the script verb
`setgambit_slotmax` adds to it for all three sets, between 0 and 12 (`00327930`). A line is coloured one way for a Foe
condition and another for Ally or Self (`0031D0D2`, `01EED270`), or greyed when it is off (`00568BB0`).

### Columns and help

Left and right move between the switch, the condition and the action on a line row (`00569C4B`-`00569C96`). The help
line follows the column (`00569E6D`):

| Where | Help (`help_menu.bin`) |
|---|---|
| header row | "Toggle gambits ON/OFF." (`CF2`<sub>h</sub>) |
| switch | "Toggle slot ON/OFF. (Can be cleared using ...)" (`CF1`<sub>h</sub>) |
| condition | "Change the conditions under which an action is performed. ..." (`CEE`<sub>h</sub>) |
| action | "Change which action is performed. ..." (`CEF`<sub>h</sub>) |

`005678C0(column)` gives the help kind of a column from `00D234F8`: none, 4 and 5 for columns 0 to 2, and 8 or 9 for
column 3, by the language test `00254A10` (`00569CB8`, `00569D87`, `00569DA8`). `00568AA0` paints a line's number in
two digits (`0029F6E0`), nudging the second label for numbers below 10 unless `00254A10` is true.

### Changing set and character

Bit 9 of the pressed or repeat word (`02F97392`, `02F97394`; R2 in the [Controls](../Controls-And-Input/controls.md) order) moves to the next of the
three sets and bit 8 (L2) to the previous one (`00569AF1`, `005699F0`). The three panes slide by `780`<sub>h</sub> (`002468A0`),
the pane pointers rotate and the new centre reloads (`0056A010`), with sound `51`<sub>h</sub>. Held R1 and L1 step to the next or
previous party member (`00568280`, `00567990`). Each member's cursor row and column are kept (`00569938`-`00569953`).

### Confirming a row

The line list posts confirm (`8001`<sub>h</sub>), cancel (`8002`<sub>h</sub>), clear (`8003`<sub>h</sub>) and end-of-move (`8004`<sub>h</sub>) to the editor,
in the convention of [Dialogs](dialogs.md). Confirm runs `00567D80`:

1. On the header row it flips the character's gambits on or off (`00311AF0`, `00567DDD`), sound `12`<sub>h</sub> or `13`<sub>h</sub>.
2. On a condition or action it opens the condition or action list (`0056B350`).
3. On a switch it picks the line up for moving (`005687F0`).
4. On the same switch again it turns the line on or off and saves; an empty line cannot be turned on (sound 5,
   `00567ECC`).
5. On another row's switch it moves the line there (`00567F90`) and saves.

A move is an insertion: the lines between the old and new row shift one place, and the moved line takes the new row.
While a line is held, `00568FE0` slides each line between the two rows by 4 a frame, and the editor's tick `005678F0`
eases the scroll `+343`<sub>h</sub> (`00248F40`) and pulses the held line through `005682C0`: its level `+350`<sub>h</sub> swings between
`80`<sub>h</sub> and `FF`<sub>h</sub> by `20`<sub>h</sub> a frame, and fades by 16 a frame once nothing is held.
Cancel while a line is picked up returns it; cancel otherwise saves and closes all three editors (`005679D0`).

### Clearing a line

Clear (`8003`<sub>h</sub>, `00569E06`) runs `0056A1D0(editor, -1, row)`: it empties both the condition and the action, turns the
line off and saves, with sound `19`<sub>h</sub>. The header row cannot be cleared.

### The condition and action lists

`0056B350` opens the list `0056B4D0` and slides the editor aside by `GambitTargetListMoveX` or `GambitActionListMoveX`
(`01F2CB10`, `01F2CB14`). The help line shows the highlighted entry's own help text (the list's `8000`<sub>h</sub> arm,
`00291D80`).

| List | Built from | Pages |
|---|---|---|
| conditions | `0031EB20` kind `23`<sub>h</sub>, grid from condition row `+16`<sub>h</sub>/`+17`<sub>h</sub> (`00238880`) | 15 of up to 17 |
| actions | `0031EB20` kind `22`<sub>h</sub>, grid from action row `+38`<sub>h</sub>/`+39`<sub>h</sub> (`00237FC0`) | 11 of up to 17; page 0 holds only Attack |

L1 and R1, or left and right, turn the page (`0056AAC0`, `0056AD50`), and the tabs are coloured by target or command
class (`0056ADA0`). An entry not yet owned is listed as the placeholder `4C7`<sub>h</sub>, with "Select conditions for an
action." (`CD8`<sub>h</sub>) or "Select action to be performed." (`CD7`<sub>h</sub>) as its help, and cannot be picked (`0056BC70`,
`0056A890`).

The pages are built by `0056B100` (conditions, the page count from `00327BD0`) and `0056AE80` (actions, `00327BB0`),
eight bytes a page from `+300`<sub>h</sub>, from the run state of `0056A3D0` and the tab colouring of `0056ADA0`:

- each page's entries come from `0031EB20`; a page with none, or whose entries all have state `0F`<sub>h</sub>, gets colour
  `87`<sub>h</sub> and is disabled (state 2 for conditions, 3 for actions);
- a condition page is coloured by the target class `+38`<sub>h</sub> of its entries' class `B`<sub>h</sub> record: 1 `85`<sub>h</sub>, 2 `86`<sub>h</sub>,
  3 `84`<sub>h</sub>; an action page by the class 1 record its item names (`0035D330(14h)` `+2C`<sub>h</sub>): 5 `8B`<sub>h</sub>, 8 `89`<sub>h</sub>,
  9 `8A`<sub>h</sub>, else `88`<sub>h</sub>;
- the page and row of the line's current entry go to `+595`<sub>h</sub> and `+599`<sub>h</sub>/`+59A`<sub>h</sub> (page 0, row 0 when absent), and an
  entry equal to the argument with state 0 returns 1 and stores its page and row at the editor's `+334`<sub>h</sub>/`+335`<sub>h</sub>.

The rows use painters at `+120`<sub>h</sub>: `0056BBD0` for a condition (the name, in colour 2 when its state byte is not 0)
and `0056A780` for an action, which adds the icon frame and, when its byte `+11`<sub>h</sub> is set, the number `+0C`<sub>h</sub> with text
`465F`<sub>h</sub> (`0029FF60`); the frame is hidden for an empty entry, id `96`<sub>h</sub>, or state `0F`<sub>h</sub>.

`005678A0` re-attaches the member-scoped pane `[02CA96D8]` (`005677A0`) to the root `[0208EA28]` (`00246AD0`) for the
two openers (`00282286`, `002D7270`).

### Refusals

Confirming an entry runs `0056AC50`. An entry whose state is not 0 is refused, and its message shows for 180 frames:

| State | List | Message (`help_menu.bin`) |
|---|---|---|
| `10`<sub>h</sub> | actions | "You do not have the license for this action." (`CF0`<sub>h</sub>, licence test `00323EC0`) |
| `21`<sub>h</sub>-`23`<sub>h</sub> | actions | "This action cannot be performed on a foe." / "...on an ally." / "...on the user." (`C75`<sub>h</sub>-`C77`<sub>h</sub>) |
| `1D`<sub>h</sub>-`1F`<sub>h</sub> | conditions | "The selected action cannot target a foe." / "...an ally." / "...the user." (`C78`<sub>h</sub>-`C7A`<sub>h</sub>) |

The target states come from `00327A10(action, condition)`: the condition's target, Foe, Ally or Self, must be allowed
by the action row's `+0C`<sub>h</sub> (`8` for Foe, `4` for Ally, `1` or `4` for Self). An accepted entry is written into the
line (`0056A1D0`) and saved, and the list closes after 32 frames.

### The save

Every edit saves at once. `00569F90` copies the rows into the editor's copy of the set and jumps to `003282C0`; a move
ends in the same jump (`005680D7`). `003282D0(member, set)`:

1. picks the member's selected set at `[02EBF190] + 5B10h + (member x 3 + selected) x 34h` (`0032830A`-`00328324`);
2. copies the `34`<sub>h</sub>-byte set into it (`00328327`-`00328347`);
3. calls `00328140`, which rebuilds the member's gambit orders at `02089378`, one 24-byte order per line that is on and
   filled ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

These are the only calls to `003282C0`, `003282D0` and `00328140` in the image (a scan of every function for direct
calls).

### Script restore and steering

When the editor finishes loading it keeps a copy of the set (`0056955F`). On close it writes that copy back only when
`[0209AC30] + DEBh` is set (`00569242`-`00569259`), which the script verb `fsmenu_registrestore` sets (`00511AA0`,
`002D7D40`) and `002D6F90` clears. So a scripted lesson can put the set back as it was, while ordinary use keeps every
edit.

The verbs `fsmenu_changechip`, `fsmenu_movechip`, `fsmenu_movelist` and `fsmenu_registopenchip` steer the cursor for a
lesson: the editor's state machine `0056A3D0` and the list's `0056BE40` allow only the input that moves toward the
target row, page and entry, then only confirm (`002D66A0`).

## Shipped data

| | |
|---|---|
| condition list | 15 pages of up to 17, 255 conditions placed |
| action list | 11 pages: 1, 17, 17, 17, 17, 13, 17, 17, 17, 17 and 7 actions |

## Modding notes

- A condition's or action's place in the lists is its grid column and row in the condition or action table.
- Which targets an action accepts is its row's byte `+0C`<sub>h</sub>; widening it lets more conditions pair with it.
- `setgambit_slotmax` adds its argument to the slot count of all three sets, clamped to 0-12.

## Related

- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the sets, presets and how the orders are walked in battle.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the condition table.
- [Menus](menus.md) - the menu entry and the script request.
- [Dialogs](dialogs.md) - the list widget's sub-commands.
