---
title: "Battle menu: the command lists, the party HP and MP list, the help line, the boss and overhead gauges, and how a chosen command is issued"
kind: "system"
category: "Menus and HUD"
addresses: "00279E20, 00276D30, 002778C0, 0027E050, 0027C3D0, 00311B20, 0029BE50, 002C8310"
---

## What the player sees

- The battle menu lists Attack, Magicks & Technicks, Mist (or Dismiss while an Esper is out), Gambits and Items.
- Choosing a list opens the next one, such as the five magick schools, and choosing an action asks for a target.
- Greyed commands explain themselves on the help line, for example "Silenced: Cannot use magicks."
- The party list shows each member's name, HP and MP; a boss shows a gauge at the top, and units carry HP gauges
  above their heads.

## How it works

### The widgets

| Object | Size | Procedure | Built by |
|---|---|---|---|
| manager | `61F0`<sub>h</sub> | `00279E20` | `00276650` (`002766D1`), from `00290CF0` into `[0209BE80] + AB30h` |
| panel, two slots | `3010`<sub>h</sub> | `00276D30` | manager message 2 (`0027A402`) |
| list widget | `2DC0`<sub>h</sub> | `002778C0` | panel message 1 (`00276DD3`) |
| list page, two | `1620`<sub>h</sub> | `0027AD70` | list widget message 1 (`002779DB`, `00277A08`) |
| target category tabs | `D0`<sub>h</sub> | `0027C870` | manager message 2 (`0027A12F`) |
| Dismiss confirmation | `4A0`<sub>h</sub> | `0027AA70` | manager message 2 (`0027A369`) |

The menu is requested through router ids 1 and 4 ([Menus](menus.md)): `0035D660` calls `0028FD50`, and the HUD frame
`0028E290` builds the manager through `00290CF0` (`0028E480`). The manager starts with list kind 1, the top commands,
and keeps a stack of the lists opened in the cursor block at `[0209BE80] + AA60h` (`00290D88`).

Each widget dispatches through its own tables: the manager answers 21 messages (`0027AA38`, `0027A9E0`), the panel 10
(`00277880`, `00277854`) and the list widget 14 (`00279D98`, `00279D60`).

`00290CF0` builds the manager only when the request bit 4 of `[0209BE80] + 10F68h` is set and, unless bit 10 is also
set, router id 1 is not refused (`00254500`, `00254550(set, 1)`, a bit test); the HUD itself is on [HUD](hud.md).
The list widget keeps a chain of callback records `{fn*, argument, previous, next}`: `00274BA0` appends one
(`002779C8`), and `00274BD0(head, first, n)` runs up to `n` of them and unlinks each that answers 1 (`00278390`,
`00278592`, `00278A7A`, `00278A91`).

### Lists

`0027E050` turns a menu kind into a list code for the list builder `0031EB20` and installs the row painter, and
`0027D480` writes the title:

| Kind | List | Title |
|---:|---|---|
| `1` | top commands, list 6 | none |
| `2` | Magicks & Technicks, list 8 | "Magicks & Technicks" |
| `3` | Mist, list 9 | "Mist" |
| `4` | items, list `B`<sub>h</sub> | "Items" |
| `6`, `7` | Summon and Quickening actions, list `B`<sub>h</sub> | "Summon", "Quickening" |
| `10`-`14` | the magicks of one school, list `B`<sub>h</sub> | "White Magicks" to "Arcane Magicks" |
| `15` | technicks, list `B`<sub>h</sub> | "Technicks" |
| `16`-`19` | a target list, codes `10`<sub>h</sub>, `D`<sub>h</sub>, `F`<sub>h</sub>, `1C`<sub>h</sub> (`01E0C398`) | the action's name |

The command lists are `{flag, id}` pairs (`0031EB88`-`0031EBEC`):

| List | Table | Rows |
|---:|---|---|
| `6` | `00D10650` | Attack, Magicks & Technicks, Mist, Dismiss, Gambits, Items |
| `8` | `00D10680` | White, Black, Time, Green and Arcane Magicks, Technicks |
| `9` | `00D1065C` | Summon, Quickening |

Mist is listed only while `003135C0` is 0, and Dismiss only while it is 1 ([Command availability](../Battle-Actions/command-availability.md)),
so the top list shows one of the two. Each row is checked with `00318CD0`, which leaves it out, greys it with a reason,
or lists it (`0031ECA3`-`0031ED3D`). An action list keeps the actions of the list's kind byte `+1E`<sub>h</sub> (and school
`+2Ch & 7`) that the member owns and has left (`00317BC0`), with their MP, Mist charge or item count.

### Row painters

`0027E050` installs one painter per list (`0027E2F0`):

| Painter | Lists | Draws |
|---|---|---|
| `00276BE0` | top commands, Mist | the command labels |
| `0027D240` | the magick schools, kind 2 | the label word of the school row (class `18`<sub>h</sub>) when flag bit 2 is set, of the command row (class `15`<sub>h</sub>) otherwise |
| `0027CE70` | the action lists, kinds 4-8, 10-15 and 20 | the action rows |
| `0027BC10` | kind 9, list `18`<sub>h</sub> | the name of a class 1 row, or Remove (`menu_command.bin` `404`<sub>h</sub>) for the id -1, with byte `+15EF`<sub>h</sub> set to 6 for the row equal to `+1538`<sub>h</sub> |
| `0027D5C0` | target list `F`<sub>h</sub> | the name of the row's id through `0031C5D0` |
| `0027E530` | the other target lists | the unit's name (`00272CB0`) and, when `00272C80` gives a number, that number after it |

A row whose greyed flag is set is drawn at alpha `40`<sub>h</sub>. An empty list draws one row with alpha `96 + 32 x sin(t x pi / 30)`
of the frame counter: "No Available Targets" (`menu_message.bin` `7D1`<sub>h</sub>) for a target list, and `7D2`<sub>h</sub>, empty in the
shipped text, for the others (`0027D24A`-`0027D25E`, `0027BC1A`-`0027BC29`).

### Names and help

The labels and help come from the battle command table, class `15`<sub>h</sub> (21 rows), and the magick schools, class `18`<sub>h</sub>
(5 rows): word `+2` is the label and word `+0` the help line (`0031DC54`-`0031DCEC`).

| Command | Help (`help_menu.bin`) |
|---|---|
| Attack | "Attack with weapon in hand." (`BB8`<sub>h</sub>) |
| Technicks | "Special actions that cost no MP." (`BBA`<sub>h</sub>) |
| Items | "Use items from your inventory." (`BBB`<sub>h</sub>) |
| Summon | "Summon an Esper to fight at your side." (`BBD`<sub>h</sub>) |
| Quickening | "Perform powerful attacks." (`BBE`<sub>h</sub>) |
| Gambits | "Toggle character gambits ON/OFF." (`BBF`<sub>h</sub>) |
| Dismiss | "Release a summoned Esper." (`BC1`<sub>h</sub>) |
| Magicks & Technicks | "Use magicks and technicks." (`BC4`<sub>h</sub>) |
| Mist | "Perform an action expending Mist Charges." (`BC5`<sub>h</sub>) |
| the five schools | `BC7`<sub>h</sub>-`BCB`<sub>h</sub>, for example "Offensive magicks for dealing damage." |

### Input

The list widget reads the pressed word ([Controls](../Controls-And-Input/controls.md), `00277ACD`):

- Square closes the menu in every state (`00277ADE`-`00277B15`).
- Outside a target list, left and right step to the previous or next party member when more than one is in the party
  (`00277BFF`, `0027C280`). `0027C280(handle, step)` keeps the members whose record has flag bits 0 and 3 clear, puts
  them in party order (`00273600`, an insertion sort of `{key, value}` pairs) and steps round them.
- In a target list, L1 and R1 step the target category (`0027B430`, `0027C730`) among the tabs the manager allows.
- The row cursor, confirm and cancel come from the page's list, which posts `8000`<sub>h</sub>, `8001`<sub>h</sub> and `8002`<sub>h</sub> to the list
  widget in the convention of [Dialogs](dialogs.md).

### Target tabs

The tab strip `0027C870` shows one tab per target list the action allows.
`00276960(tabs, actor, action, kind, show, mask, ...)` sets it up from the mask:

1. Mask bits 1, 2, 8 and 4 enable tabs 0 to 3, the strip's child nodes 2 to 5 (tables `00915BE0` and `00915BF0`,
   `00276A19`-`00276A60`).
2. Bit 8 is dropped when target list `F`<sub>h</sub> has no row (`0027B090`), and bit 4 when list `1C`<sub>h</sub> has none left after
   filtering (`0027AF80`).
3. A disabled tab's four corner alphas are set to 0; an enabled tab is placed at `0027B290(tabs, mask, i)` and fades
   in by `18`<sub>h</sub> per call.
4. The strip is centred from its total width `0027B120`, and its side nodes 6 and 7 are shown only when two or more
   tabs are enabled (mask not 1, 2, 4 or 8).

The filter skips, for filter 1, rows with flag bit 1 and units whose status words hold KO, Stone or bit 31
(`00273710`, mask `80000003`<sub>h</sub>), and for every filter units whose byte `+0A`<sub>h</sub> (`002647E0`) has bit 2 (filter 0) or bit 0
(otherwise). `0027B5A0` and `0027B6C0` make the same two checks from a saved request when L1 or R1 is pressed
(`0027C730`), and `0027BB70` applies the filter to a page's rows in place, keeping the count at `+40`<sub>h</sub>.

`0027DCA0` moves the strip half way towards its centred position, snapping when it is within 1. `00276830(tabs,
kind)` marks the tab of list kind `10`<sub>h</sub>-`13`<sub>h</sub>: the other tabs draw one palette further on.

### The first target row

`0027BED0(page, handles)` picks the row a target list opens on (`002798E8`), the first rule that finds one:

1. the first row not greyed (flag bit 1) whose unit is one of the four handles given;
2. the first row with flag bit 0;
3. the row of the acting unit, page `+08`<sub>h</sub>;
4. the nearest row that is not greyed and not the actor and whose unit is on screen, else the nearest such row;
5. the saved row `+44`<sub>h</sub>, or the first row not greyed, or row 0.

Distances are from the actor's position (`002E9D10`, `00203080`, `002703F0`). A unit is on screen when its position
projects in front of the camera `02AEDDB0` (`00272250`) inside the 1920 x 1080 frame (`00273850`). `00272180(out,
matrix, point)` projects a point and divides by its depth; `00272250` turns the result into frame coordinates,
`(x - 8000h) / 16 + 01E0C1D8 / 2` and the same for y, and `002722A0` does the same with the width divided by
`00183280()`.

### Refreshing an open list

`0027D740(page)` rebuilds an open page while its `+1528`<sub>h</sub> bit 10 is set:

1. A command or action list is rebuilt with `0031EB20`; an action list (page kind 11) keeps the cursor on the row
   with the same id, and the cursor is clamped to the last row.
2. A target list (bit 13) is rebuilt from a copy of the page (`00272400`, which copies the `50`<sub>h</sub>-byte header and the
   eight-byte rows) and filtered (`0027BB70`). Once bit 14 is set it keeps its old order (`002727F0`: rows still
   present first, in their old order, then the new ones); before that, with bit 12 it is sorted by distance from the
   camera `02AEDDB0` (`002729A0`), and bit 14 is then set.
3. The cursor stays on the same unit, or is clamped to the last row; bits `80800`<sub>h</sub> are set when the row count or the
   cursor changed.

`0035BC50` sorts its list `1A`<sub>h</sub> at `022C83F0` by distance in the same way (`00272B40`, `0035BD19`).

Both sorts end in `002748E0(n, rows, ascending)` (`00272AC5`, `00272C0F`, each passing 1). It orders `n`
eight-byte rows by their signed dword `+0`: a quicksort with its own stack of ranges leaves ranges of 11
rows or fewer, and one insertion pass over the whole array finishes; a zero third argument sorts in
descending order.

### The target cursor

`0027CD00(cursor, widget)` draws the hand over the target unit (`002780DC`): it projects the unit's position
(`002713E0`, `002722A0`), hides the hand while the unit is behind the camera (`003678F0`), and otherwise slides it
from its last place towards the unit by the blend at `+0A`<sub>h</sub> (`002752E0`), jumping straight there after it was
hidden; `00368360` draws it, and `00368940` also runs once the blend is full.

The list's row hook `0027E4E0(page, widget, unit)` (`00279C26`) pulses a row while `0027B770` finds its unit within
the radius `+1540`<sub>h</sub> of the cursor's unit (`0027B3B0`), neither row greyed: `0027AF00` sets the draw's `+58`<sub>h</sub> to half
of the page's `+A0`<sub>h</sub> and swings its `+5A`<sub>h</sub> by `sin(frame x pi / 7)` times half its value. `0027BD80(actor, action)` returns the value `0031AB80`
reports for a kind 1 answer, or 0 (`00279ABF`).

The grid list draw `00367AA0` pulses its cells the same way through a hook. `00368A50(widget, hook)`
keeps the two at `022CBE90` and `022CBE98`; for each visible cell the draw calls
`hook(widget +D8h, sprite, cell, first)` and draws the sprite over the cell when it answers non-zero
(`00367DC5`). The list widget `002778C0` installs one of two hooks, both ending in the `0027B770` test
for the cell's row id `+510h + 8 x cell`:

- `0027D700` (`002794DF`, while `+1528`<sub>h</sub> bit 21 is set) first runs `0027B200` for cell 0;
- `0027E7B0` (`00279AEC`) answers 0 while `+1528`<sub>h</sub> bit 15 is set and runs `0027B200` on a draw's
  first call. `0027B200(page, sprite)` passes the sprite's `+3C`<sub>h</sub> x 4 to `002030E0` and calls
  `0027AF00`.

The target lines and marks the list asks for while it is open (`0027DE30`, `0027DC10`) are on [HUD](hud.md).

### From a row to an action

Confirm (`8001`<sub>h</sub>) runs the classifier `0027C3D0` (`0027841E`), which answers with what comes next:

| Row | Next |
|---|---|
| Attack | the foe list for action `96`<sub>h</sub> (`0027C469`) |
| Items, Summon, Quickening, Magicks & Technicks, Mist, a school | that list |
| Gambits | switches the member's gambits on or off at once (`00311AF0`, `0027C512`) and closes |
| Dismiss | the Dismiss confirmation |
| an action | its target list, or the action at once when it needs no target choice |
| a greyed row | refused with sound 5 |

A new list of the same panel is rebuilt in place and pushed on the stack; a target list opens in a new panel. Cancel
pops the stack and closes the menu when it is empty (`002787AF`).

The action is issued through `00311CD0(actor, target, action, 0)` (`00278766`), or `00311B20` for a party-position
target (`0027869B`), which both reach `00311CF0` once ([Action phases](../Battle-Actions/action-phases.md)). The
menu never asks for the whole party (fan-out 0 at all six call sites). Dismiss asks "Dismiss {name}?"
(`menu_message.bin` `7D0`<sub>h</sub>, `0027AA70`) and on Yes issues action `113`<sub>h</sub> on the Esper (`0027AB01`).

### The help line

The help block is `[0209BE80] + 8FA0h`, drawn in two alternating windows `002BF690`. `0027B880` fills it on each
cursor move:

- a command row shows its help;
- an action row shows the action's description;
- a greyed row shows its refusal first, through `0027C150`;
- a target row opens the target information window (`002C0870`) instead of text.

The help block's own calls (`0028FEA0`, `00290C60`, `00290C80`) are listed on [HUD](hud.md). The target information
window `002BFD20` builds its weakness line with `00295D90(size, out, mask)` (`002C02B2`): "Weak: "
(`listhelp_common.bin` `2331`<sub>h</sub>), an optional part from `002AC290`, then one element icon, text `4B27`<sub>h</sub> plus the
element, for each set bit of the mask.

`0027C220(page, row)` picks the refusal: in a command list (page kind 6 to 10) a row with flag bit 1 gives its reason
byte `+4`, in an action list (kind 11) a row with flag bit 0 gives its byte `+6`; a positive reason with a row in
`0027C150` becomes that text (`0027C220`-`0027C27E`).

| Refusal | Text (`help_menu.bin`) |
|---:|---|
| `7`<sub>h</sub> | "Stopped: Cannot take commands." (`C92`<sub>h</sub>) |
| `8`<sub>h</sub> | "Sleeping: Cannot take commands." (`C94`<sub>h</sub>) |
| `9`<sub>h</sub> | "Confused: Cannot take commands." (`C95`<sub>h</sub>) |
| `A`<sub>h</sub> | "Silenced: Cannot use magicks." (`C96`<sub>h</sub>) |
| `B`<sub>h</sub> | "Disabled: Cannot take commands." (`C93`<sub>h</sub>) |
| `C`<sub>h</sub> | "Berserk: Cannot take commands." (`C91`<sub>h</sub>) |
| `E`<sub>h</sub> | "Magicks forbidden: Cannot use magicks." (`C90`<sub>h</sub>) |
| `16`<sub>h</sub> | "You cannot attack here." (`C8A`<sub>h</sub>) |
| `17`<sub>h</sub> | "You cannot use magicks here." (`C8B`<sub>h</sub>) |
| `18`<sub>h</sub> | "You cannot use technicks here." (`C8D`<sub>h</sub>) |
| `19`<sub>h</sub> | "You cannot use items here." (`C8F`<sub>h</sub>) |
| `1A`<sub>h</sub>, `1B`<sub>h</sub> | "You cannot summon here." (`C98`<sub>h</sub>, `C99`<sub>h</sub>) |

The window rises by `HelpMessageMoveY` (`002BF77A`) while the boss gauge is out of its compact state.

The host `002BE490` keeps the two windows `2B8`<sub>h</sub> bytes apart. On its message 2, `002BE290` builds the target
information window (`002C0F30`) when bit 0 of `+57E`<sub>h</sub> asks for it, in the free window that `002BEA40` returns:
`002BEA40` clears `+570`<sub>h</sub>, starts closing each busy window whose `+280`<sub>h</sub> bit 0 is clear, and returns a window with no
procedure. `002BE290` then closes the window at `+570`<sub>h</sub> once its `+280`<sub>h</sub> has bit 2 set and bit 0 clear, and clears
`+570`<sub>h</sub> and bit 1 of `+57E`<sub>h</sub>.

While `002BFD20` lays the target window out, `002C0760` hides six of its child widgets
and seven of its parts and sets its height from part 5, and `002C03A0` hides the child of part 12.

### The party list

The party list `0029BE50` (`B68`<sub>h</sub> bytes, at `[0209BE80] + 10F78h`) draws one slot `0029A0A0` per member from the
`C0`<sub>h</sub>-byte party status records ([Party member status record](../Characters-And-Objects/party-member-status-record.md)):

| Element | Drawn by | From |
|---|---|---|
| name | `00297F60` | `+10`<sub>h</sub> |
| HP | `00297D10` | `+20`<sub>h</sub> |
| HP gauge | `00297E10` | HP against the larger of HP and `+28`<sub>h</sub> |
| max HP | `00297E70` | `+24`<sub>h</sub> |
| MP | `0029A8E0` | `+2C`<sub>h</sub> |
| MP bars | `0029A930` | `+38`<sub>h</sub> over `+87`<sub>h</sub> bars; the first `+86`<sub>h</sub> bars pulse, with sound `48`<sub>h</sub> or `49`<sub>h</sub> when that count changes |

The battle menu highlights the acting member's slot (`00296AF0`) and clears it (`00296B80`). How the rows are built
and animated, the rolling numbers, and the modes in which the rows become the target cursor are on
[Party list](party-list.md).

The menu finds members through the party status records at `0035BB20(i)`, `0C0`<sub>h</sub> bytes each, with the handle at
`+04`<sub>h</sub>:

- `00273320(handle)` returns the member's position, or -1, and `002737B0(handle)` whether it is in the party.
- `00272EE0(handle)` returns the record's type `+60`<sub>h</sub>, or 6 when no record of the first four has the handle.
- `00273460()` returns the handle of the first record with flag bit 2, and `002734B0()` that record.
- `00273800(handle)` returns 1 when the member's record has flag bit 3 clear, that is, when it is in range.

### The boss gauge

The boss gauge `00405310` (manager `00406A60`, `02B62D88`) draws up to two bars from the table at `02EC1380`, which
`0031B690` fills every frame with HP and MP. Only `00328FF0` registers a unit there, always as entry 0
(`0023AA04`), with the class from the spawn row ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
The style is one bar for class 1 or 2 and style 2 for class 3 (`00405100`).

### Boss gauge bars

Each bar is a child `004061F0` of the gauge's window `[02B62D88] + C0h`, at `+C8`<sub>h</sub> and `+D0`<sub>h</sub>
(`00404D40(i)` returns bar `i`, 0 or 1). A bar carries the counter of the
[script gauges](script-gauges.md) (`+C0`<sub>h</sub> mode, `+E0`<sub>h</sub> maximum, `+E4`<sub>h</sub> value, `00408140`, `00407240`).

- `00405770(gauge, style)` sets both bars up for a style from the pairs at `00D12190`: style 0 uses layout child 0
  and hides bar 1, styles 1 and 2 use children 2 and 3, style 3 children 1 and 2. It reads each value with
  `00404F50` (1000 when missing), sets the maximum (`004073B0`) and redraws.
- `00404F50(i, style, cells)` returns entry `i` of the value table `[02B62D88] + E8h` (count `+E3`<sub>h</sub>, `18`<sub>h</sub> bytes
  each). For style 2 it cuts entry 0 into 50 cells: `cells = current x 51 / max`, 51 counted as 50. Bar 0 then
  gets the part inside the current cell, bar 1 the cell count as a width `cells x 6 - 2` of 298.
- `004060B0(bar, open, b)` starts a bar's 25-frame opening (`00246AD0`) or closing; a segmented bar (`+130`<sub>h</sub>
  bit 8) also plans a ramp of 50 cells over 25 frames, and closing marks all 50 cells `+13C`<sub>h</sub> lit (9).
- `004058E0(bar, start)` runs the opening or closing each frame: the value widget grows by the square of the eased
  step (`00248F40`), or a segmented bar widens cell by cell (`004076B0`). When a closing run ends the bar is
  released (`00245020`).
- `004068B0(bar, value)` takes a new value, ends a running ramp at it and sets the flash timer `+178`<sub>h</sub>: 1 frame for a
  rise; 40 for a drop, or 1 once the drops' total `+17C`<sub>h</sub> passes 3,999 (each adds 40 divided by its size).
- `00406770(bar, on)` re-reads the value when shown, and `00406DD0(gauge, on)` records the state in `+C8`<sub>h</sub> bit 5
  and passes it to every shown bar (`+130`<sub>h</sub> bit 4).
- `00405C20` draws a bar: the number (`0029E840`) and, for a segmented bar, up to 49 cell frames in batches of 16
  (`002D9DB0`, `002DAC70`). A lit cell's state counts 1 to 8 while the first sprite fades out, then 9 to 17 while
  the second fades in, wrapping to 9 (`002D8D10`).

A bar does nothing in a frame while the window's `+C8`<sub>h</sub> bit 6 or 7 is set, unless it is closing (`0040639D`-`004063B2`).
The verbs reach the gauge through one-jump stubs:

| Verb or caller | Function | Effect |
|---|---|---|
| `bossgaugeopen` (`00349B60` → `003EC7F0`) | `00405270` | sets `+C8`<sub>h</sub> bit 0, unless bit 1 or 5 is set |
| `bossgaugeclose` (`00349F80` → `003EC7C0`) | `00404E10` | once (`+C2`<sub>h</sub> bit 0): turns the bars off (`00406DD0`), closes the window (`00244F00`) when a value is still above 0, or else releases each bar or marks it closing |
| HUD hide (`0035D0E0`) | `00405150` | closes the window (`00244DD0`) and remembers it in `+C8`<sub>h</sub> bit 2 |
| HUD show (`0035D1B0`) | `004052D0` | reopens it (`00246AD0`) when bit 2 is set |
| pause mask `0215F1B3` | `00404D70`, `00404DC0` | sets or clears `+C8`<sub>h</sub> bit 7 ([Script gauges](script-gauges.md)) |

### Overhead HP gauges

`002C7660` gives each unit a gauge kind, 0 for a party member, 1 or 2 for other units, and `002C8310` draws it when
the unit's byte `+17`<sub>h</sub> bit 1 and the HUD's bit are set. The step is `min(HP, max) x 100 / max >> 2`, 0 to 25
(`002C8398`-`002C83A1`); it picks the frame `00916F08[step]` and a colour between the kind's `Min` and `Max` keys
(`002C5F90`).

| Kind | Layout keys |
|---:|---|
| 0, party | `HpGaugeSide{Min,Max}_{R,G,B,A}` (`01E0CEF8`-`01E0CF14`) |
| `1` | `HpGaugeEnmey{Min,Max}_{R,G,B,A}` (`01E0CED8`-`01E0CEF4`) |
| `2` | `HpGaugeOther{Min,Max}_{R,G,B,A}` (`01E0CF18`-`01E0CF34`) |

### Layout keys

| Part | Keys |
|---|---|
| panel | `BattleMenuLRCursorMoveX` (`002776CB`) |
| list size | `BattleCommandGillTagOffset`, `BattleCommandNumTagWidth`, `BattleCommandScrollTableOffsetX`, `mCommandTitleFontHeight` (`0027DED0`) |
| list page | `mScrollListHeight` (`0027AE79`) |
| command rows | `mGambitPositionOffsetX/Y`, the ON/OFF mark on the Gambits row (`00276BE0`) |
| action rows | `BattleCommandNumPosX`, `BattleCommandMistPosX/Y`, `BattleMistCount0Offset`-`BattleMistCount3Offset`, `BattleMistIconWidth` (`0027CE70`) |
| help line | `HelpMessageMoveY`, `mHelpMessageFontCount` |
| boss gauge | `BossGaugeExColorR/G/B/A` (`0029EA58`-`0029EA6F`) |

The label widths come from a pre-pass, `00273E30`, which scene and action code runs (`00306760`, `00313550`,
`00313840`, `00254A90`) and which writes `022CA408`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | id | class `15`<sub>h</sub> row, or class `18`<sub>h</sub> school when flags bit 2 is set |
| `03`<sub>h</sub> | `u8` | flags | bit 1 greyed, bit 2 school row, bit 3 greyed by `00318CD0` answer 2 |
| `04`<sub>h</sub> | `u8` | reason | refusal shown through `0027C150` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | id | action id (class `14`<sub>h</sub>) |
| `02`<sub>h</sub> | `u16` | cost | MP, Mist charges or item count |
| `04`<sub>h</sub> | `u16` | flags | bit 0 greyed, bits 6-9 the targets the action needs |
| `06`<sub>h</sub> | `u8` | reason | `002FFCF0` code from `00317BC0` |

## Modding notes

- The top command list is the six pairs at `00D10650`; reordering them reorders the menu.
- A command's label and help are words `+2` and `+0` of its battle command row.
- A new refusal reason needs a row in `0027C150` to show text.

## Related

- [Command availability](../Battle-Actions/command-availability.md) - which commands and actions are offered.
- [Target selection](../Battle-Actions/target-selection.md) - the target lists.
- [Action phases](../Battle-Actions/action-phases.md) - what happens after an action is issued.
- [Menus](menus.md) - the router ids that open the menu.
- [Gambits screen](gambit-screen.md) - the same on/off switch for a member's gambits.
