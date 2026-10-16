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

The main menu's Gambits entry (`menu_command.bin` `0x4B9`, `0028224D`-`00282264`) and the script menu request `0x40`
([Menus](menus.md), host `002D70F0`, `002D726B`) both call `00568B30`. It creates three editors `005691E0`
(`00568B80`), one for each pane: the centre pane and the two off-screen panes that slide in when the set changes. Each
pane shows the member's selected set (`00327C40`, set index at `[02EBF190] + 0x7370 + member x 4`).

### Rows

`00567B60` fills the rows:

| Row | Shows |
|---|---|
| `0` | the character's name; its switch is bit 2 of the party record (`00309B40`) |
| 1 to the slot count | one gambit line: condition and action names, "-" (`0x3EB`) when empty, and ON or OFF from the set's mask |

The slot count is the set's byte `+0x32` ([Gambits](../Enemy-AI-And-Gambits/gambits.md)); the script verb
`setgambit_slotmax` adds to it for all three sets, between 0 and 12 (`00327930`). A line is coloured one way for a Foe
condition and another for Ally or Self (`0031D0D2`, `01EED270`), or greyed when it is off (`00568BB0`).

### Columns and help

Left and right move between the switch, the condition and the action on a line row (`00569C4B`-`00569C96`). The help
line follows the column (`00569E6D`):

| Where | Help (`help_menu.bin`) |
|---|---|
| header row | "Toggle gambits ON/OFF." (`0xCF2`) |
| switch | "Toggle slot ON/OFF. (Can be cleared using ...)" (`0xCF1`) |
| condition | "Change the conditions under which an action is performed. ..." (`0xCEE`) |
| action | "Change which action is performed. ..." (`0xCEF`) |

### Changing set and character

Bit 9 of the pressed or repeat word (`02F97392`, `02F97394`; R2 in the [Controls](../Controls-And-Input/controls.md) order) moves to the next of the
three sets and bit 8 (L2) to the previous one (`00569AF1`, `005699F0`). The three panes slide by `0x780` (`002468A0`),
the pane pointers rotate and the new centre reloads (`0056A010`), with sound `0x51`. Held R1 and L1 step to the next or
previous party member (`00568280`, `00567990`). Each member's cursor row and column are kept (`00569938`-`00569953`).

### Confirming a row

The line list posts confirm (`0x8001`), cancel (`0x8002`), clear (`0x8003`) and end-of-move (`0x8004`) to the editor,
in the convention of [Dialogs](dialogs.md). Confirm runs `00567D80`:

1. On the header row it flips the character's gambits on or off (`00311AF0`, `00567DDD`), sound `0x12` or `0x13`.
2. On a condition or action it opens the condition or action list (`0056B350`).
3. On a switch it picks the line up for moving (`005687F0`).
4. On the same switch again it turns the line on or off and saves; an empty line cannot be turned on (sound 5,
   `00567ECC`).
5. On another row's switch it moves the line there (`00567F90`) and saves.

A move is an insertion: the lines between the old and new row shift one place, and the moved line takes the new row.
Cancel while a line is picked up returns it; cancel otherwise saves and closes all three editors (`005679D0`).

### Clearing a line

Clear (`0x8003`, `00569E06`) runs `0056A1D0(editor, -1, row)`: it empties both the condition and the action, turns the
line off and saves, with sound `0x19`. The header row cannot be cleared.

### The condition and action lists

`0056B350` opens the list `0056B4D0` and slides the editor aside by `GambitTargetListMoveX` or `GambitActionListMoveX`
(`01F2CB10`, `01F2CB14`). The help line shows the highlighted entry's own help text (the list's `0x8000` arm,
`00291D80`).

| List | Built from | Pages |
|---|---|---|
| conditions | `0031EB20` kind `0x23`, grid from condition row `+0x16`/`+0x17` (`00238880`) | 15 of up to 17 |
| actions | `0031EB20` kind `0x22`, grid from action row `+0x38`/`+0x39` (`00237FC0`) | 11 of up to 17; page 0 holds only Attack |

L1 and R1, or left and right, turn the page (`0056AAC0`, `0056AD50`), and the tabs are coloured by target or command
class (`0056ADA0`). An entry not yet owned is listed as the placeholder `0x4C7`, with "Select conditions for an
action." (`0xCD8`) or "Select action to be performed." (`0xCD7`) as its help, and cannot be picked (`0056BC70`,
`0056A890`).

### Refusals

Confirming an entry runs `0056AC50`. An entry whose state is not 0 is refused, and its message shows for 180 frames:

| State | List | Message (`help_menu.bin`) |
|---|---|---|
| `0x10` | actions | "You do not have the license for this action." (`0xCF0`, licence test `00323EC0`) |
| `0x21`-`0x23` | actions | "This action cannot be performed on a foe." / "...on an ally." / "...on the user." (`0xC75`-`0xC77`) |
| `0x1D`-`0x1F` | conditions | "The selected action cannot target a foe." / "...an ally." / "...the user." (`0xC78`-`0xC7A`) |

The target states come from `00327A10(action, condition)`: the condition's target, Foe, Ally or Self, must be allowed
by the action row's `+0x0C` (`8` for Foe, `4` for Ally, `1` or `4` for Self). An accepted entry is written into the
line (`0056A1D0`) and saved, and the list closes after 32 frames.

### The save

Every edit saves at once. `00569F90` copies the rows into the editor's copy of the set and jumps to `003282C0`; a move
ends in the same jump (`005680D7`). `003282D0(member, set)`:

1. picks the member's selected set at `[02EBF190] + 0x5B10 + (member x 3 + selected) x 0x34` (`0032830A`-`00328324`);
2. copies the 0x34-byte set into it (`00328327`-`00328347`);
3. calls `00328140`, which rebuilds the member's gambit orders at `02089378`, one 24-byte order per line that is on and
   filled ([Gambits](../Enemy-AI-And-Gambits/gambits.md)).

These are the only calls to `003282C0`, `003282D0` and `00328140` in the image (a scan of every function for direct
calls).

### Script restore and steering

When the editor finishes loading it keeps a copy of the set (`0056955F`). On close it writes that copy back only when
`[0209AC30] + 0xDEB` is set (`00569242`-`00569259`), which the script verb `fsmenu_registrestore` sets (`00511AA0`,
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
- Which targets an action accepts is its row's byte `+0x0C`; widening it lets more conditions pair with it.
- `setgambit_slotmax` adds its argument to the slot count of all three sets, clamped to 0-12.

## Related

- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the sets, presets and how the orders are walked in battle.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the condition table.
- [Menus](menus.md) - the menu entry and the script request.
- [Dialogs](dialogs.md) - the list widget's sub-commands.
