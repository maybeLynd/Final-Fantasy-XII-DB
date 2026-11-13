---
title: "Battle menu: the command lists, the party HP and MP list, the help line, the boss and overhead gauges, and how a chosen command is issued"
kind: "system"
category: "Menus and HUD"
addresses: "0x00279E20, 0x00276D30, 0x002778C0, 0x0027E050, 0x0027C3D0, 0x00311B20, 0x0029BE50, 0x002C8310"
---

## What the player sees

- The battle menu lists Attack, Magicks & Technicks, Mist (or Dismiss while an Esper is out), Gambits and Items.
- Choosing a list opens the next one, such as the five magick schools, and choosing an action asks for a target.
- Greyed commands explain themselves on the help line, for example "Silenced: Cannot use magicks."
- The party list shows each member's name, HP and MP; a boss shows a gauge at the top, and units carry HP gauges
  above their heads.

Each command's name and help line come from the battle command table, which points at texts in `help_menu.bin`.
Choosing a row opens the next list, opens a target list, or hands the action and its target to the battle's action
phases.

## How it works

### The widgets

| Object | Size | Procedure | Built by |
|---|---|---|---|
| manager | `0x61F0` | `0x00279E20` | `0x00276650` (`0x002766D1`), from `0x00290CF0` into `[0x0209BE80] + 0xAB30` |
| panel, two slots | `0x3010` | `0x00276D30` | manager message 2 (`0x0027A402`) |
| list widget | `0x2DC0` | `0x002778C0` | panel message 1 (`0x00276DD3`) |
| list page, two | `0x1620` | `0x0027AD70` | list widget message 1 (`0x002779DB`, `0x00277A08`) |
| target category tabs | `0xD0` | `0x0027C870` | manager message 2 (`0x0027A12F`) |
| Dismiss confirmation | `0x4A0` | `0x0027AA70` | manager message 2 (`0x0027A369`) |

The menu is requested through router ids 1 and 4 ([Menus](menus.md)): `0x0035D660` calls `0x0028FD50`, and the HUD frame
`0x0028E290` builds the manager through `0x00290CF0` (`0x0028E480`). The manager starts with list kind 1, the top commands,
and keeps a stack of the lists opened in the cursor block at `[0x0209BE80] + 0xAA60` (`0x00290D88`).

Each widget dispatches through its own tables: the manager answers 21 messages (`0x0027AA38`, `0x0027A9E0`), the panel 10
(`0x00277880`, `0x00277854`) and the list widget 14 (`0x00279D98`, `0x00279D60`).

`0x00290CF0` builds the manager only when the request bit `0x10` of `[0x0209BE80] + 0x10F68` is set and, unless bit `0x400` is also
set, router id 1 is not refused (`0x00254500`, `0x00254550(set, 1)`, a bit test); the HUD itself is on [HUD](hud.md).
The list widget keeps a chain of callback records `{fn*, argument, previous, next}`: `0x00274BA0` appends one
(`0x002779C8`), and `0x00274BD0(head, first, n)` runs up to `n` of them and unlinks each that answers 1 (`0x00278390`,
`0x00278592`, `0x00278A7A`, `0x00278A91`).

### Lists

`0x0027E050` turns a menu kind into a list code for the list builder `0x0031EB20` and installs the row painter, and
`0x0027D480` writes the title:

| Kind | List | Title |
|---:|---|---|
| `1` | top commands, list 6 | no title |
| `2` | Magicks & Technicks, list 8 | "Magicks & Technicks" |
| `3` | Mist, list 9 | "Mist" |
| `4` | items, list `0xB` | "Items" |
| `6`, `7` | Summon and Quickening actions, list `0xB` | "Summon", "Quickening" |
| `10`-`14` | the magicks of one school, list `0xB` | "White Magicks" to "Arcane Magicks" |
| `15` | technicks, list `0xB` | "Technicks" |
| `16`-`19` | a menu target list ([Target selection](../Battle-Actions/target-selection.md)), codes `0x10`, `0xD`, `0xF`, `0x1C` (`0x01E0C398`) | the action's name |

The command lists are `{flag, id}` pairs; each list's row count is an immediate (`0x0031EBA2`, `0x0031EBBF`,
`0x0031EBEC`; `0x0031EB83`-`0x0031EBEC`):

| List | Table | Rows |
|---:|---|---|
| `6` | `0x00D10650`, or `0x00D10660` while bit `0x800` of `[0x02EBF190] + 4` is set (`0x0031EBCC`-`0x0031EBE8`); the two hold the same six pairs | Attack, Magicks & Technicks, Mist, Dismiss, Gambits, Items |
| `7` | `0x00D10670` | command 14 (shipped name "NOT USED cancellation"), Attack, command 4 ("NOT USED concentration"), Magicks & Technicks, Mist, Dismiss, Gambits, Items |
| `8` | `0x00D10680` | White, Black, Time, Green and Arcane Magicks, Technicks |
| `9` | `0x00D1065C` | Summon, Quickening |

`0x00311B20` sets bit `0x800` of `[0x02EBF190] + 4` when it issues Attack (`0x96`) to every living member in party
slots 0-3, its fifth argument not 0 (`0x00311BC8`-`0x00311BD7`), and clears it when it issues Attack to one target
(`0x00311C8C`); for any other action it leaves the bit as it is (`0x00311BC6`). A living member here is a party-slot
unit with a stats record and without the statuses `0x80000003` (KO, Stone, X-Zone) outside a town
(`0x00311BF5`-`0x00311C3C`). A call that returns -1 at its start (below) leaves the bit as it is.

Mist is listed only while `0x003135C0` is 0, and Dismiss only while it is 1 ([Command availability](../Battle-Actions/command-availability.md)),
so the top list shows one of the two. Each row is checked with `0x00318CD0`, which leaves it out, greys it with a reason,
or lists it (`0x0031ECA3`-`0x0031ED3D`). An action list keeps the actions of the list's kind byte `+0x1E` (and school
`+0x2C & 7`) that the member owns and has left (`0x00317BC0`), with their MP, Mist charge or item count.

### The list codes

`0x0031EB20` reads the list code at the block's `+0x00`. Codes 1 to 35 go through the 35 index bytes at `0x0031FBA4` to
one of eleven arms at `0x0031FB78` (`0x0031EB43`-`0x0031EB6F`); code 0 and codes above 35 return -1 (`0x0031EB4C`). Every
code starts from an empty list: count `+0x40` = 0 and default entry `+0x44` = -1 (`0x0031EB40`, `0x0031EB46`).

| Code | List | Rows from | Stops at |
|---:|---|---|---|
| `1` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `2` | no call in the exe passes this code | no rows: `0x0031FB63` returns -1, as for a code above 35 | - |
| `3` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `4` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `5` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `6` | the top commands, menu kind 1 (`0x0027E0A6`), and the label widths `0x00273E30` (`0x002742AC`) | `0x00D10650`, or `0x00D10660` while bit `0x800` of `[0x02EBF190] + 4` is set (`0x0031EBCC`-`0x0031EBE8`) | 6 rows (`0x0031EBEC`) |
| `7` | eight commands: command 14 (shipped name "NOT USED cancellation"), Attack, command 4 ("NOT USED concentration"), Magicks & Technicks, Mist, Dismiss, Gambits, Items; no call in the exe passes this code | `0x00D10670` (`0x0031EBB8`) | 8 rows (`0x0031EBBF`) |
| `8` | Magicks & Technicks, menu kind 2 (`0x0027E0EE`), and `0x00273E30` (`0x0027438C`) | `0x00D10680` (`0x0031EBAF`) | 6 rows (`0x0031EBEC`) |
| `9` | Mist, menu kind 3 (`0x0027E0CA`), and `0x00273E30` (`0x002742AC`) | `0x00D1065C` (`0x0031EB9B`) | 2 rows (`0x0031EBA2`) |
| `0xA` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0xB` | an action list: menu kinds 4-8, 10-15 and 20, and `0x00273E30` (`0x002744F3`) | the actions whose kind byte `+0x1E` is the block's `+0x14` and, for magicks, whose school `+0x2C & 7` is `+0x18` (`0x0031EF77`-`0x0031EF8D`), ids 0 to `0x115` (`0x0031EF63`); for items, technicks and magicks `0x00250270` then puts the rows in the order of inventory list 0, 8 or 9 ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md); `0x0025029D`-`0x002502C2`) | 512 (`0x0031EE94`) |
| `0xC` | a target list of allies and foes ([Target selection](../Battle-Actions/target-selection.md)); no call in the exe passes this code | the battle unit slots through `0x00322A80` | 512 (`0x0031F370`) |
| `0xD` | the ally target list, menu kind 17, and the tab check at `0x0027C811` | the battle unit slots through `0x00322A80` | 512 (`0x0031F370`) |
| `0xE` | the allies on screen; no call in the exe passes this code | the battle unit slots through `0x00322A80` | 512 (`0x0031F370`) |
| `0xF` | the members at member-map positions 4-8, menu kind 18, and the tab checks `0x0027B090` (`0x0027B0C6`) and `0x0027B6C0` (`0x0027B6FE`) | the bytes at `[0x02EBF190] + 0x5A7E` (`0x0031F473`) | positions 4-8 (`0x0031F435`, `0x0031F522`); 512 (`0x0031F441`) |
| `0x10` | the foe target list, menu kind 16 | the battle unit slots through `0x00322A80` | 512 (`0x0031F370`) |
| `0x11` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x12` | the living enemy-side units (stats `+0x05` not 0), which `0x0031E880` asks for `0x003B8260` (`0x003B82B6`, `0x003B82D7`), the handler of action timeline opcodes 50 and 51 (`0x003B9559`, `0x003B956F`) | the battle unit slots (`0x0031F714`) | 512 (`0x0031F747`) |
| `0x13` | the living enemy-side units on screen (`0x0031F7BB`); no call in the exe passes this code | the battle unit slots | 512 (`0x0031F747`) |
| `0x14` | the living party-side units (stats `+0x05` = 0), for the party list (`0x0035BF4B`, [Party list](party-list.md)) | the battle unit slots | 512 (`0x0031F747`) |
| `0x15` | the living party-side units on screen (`0x0031F7BB`); no call in the exe passes this code | the battle unit slots | 512 (`0x0031F747`) |
| `0x16` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x17` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x18` | the list that action `0x9B` opens, menu kind 9 (`0x0027E2D8`): the builder flags the `0x9B` row with `0x20` (`0x0031F17F`-`0x0031F187`), and the classifier answers 9 for such a row (`0x0027C5AA`); a confirmed row issues action `0x9C`, or `0x9D` for the member's current entry and for Remove (`0x0027C613`-`0x0027C665`) | no rows in the shipped executable: the builder's arm returns the empty list, no instruction stores to the page's row cells or count but the builder's, and the action that opens the list, `0x9B` (with `0x9C` and `0x9D` it issues), is a Reserve row of the action table ([Action list](../Battle-Actions/action-list.md)) | - |
| `0x19` | the actions of one kind that a member owns: the Party Menu's list panel, magicks (`0x002C3960`), and its four-pane panel, technicks, Quickenings and summons (`0x002C47FF`, `0x002C4972`, `0x002C4E79`) | the id list at `0x0208CD20` for the block's `+0x14`, or at `0x0208CE70` for school `+0x18` ([Action definition row](../Battle-Actions/action-definition-row.md); `0x0031F8ED`-`0x0031F920`) | the list's own count (`0x0031F976`); this arm has no 512 test |
| `0x1A` | the actors that `0x0046B4C0` lists, for the party list (`0x0035BCC3`) | actor managers 0-2 (`0x0031F5CB`, `0x0031F6FE`) | 512 (`0x0031F620`) |
| `0x1B` | a party member's foe list: the builder runs it in place of `0xC` and `0x10` (`0x0031F305`) | `0x0046B870`, actor managers 0-2 | 512 (`0x0031F620`) |
| `0x1C` | the target list of menu kind 19, and the tab checks at `0x002769F6`, `0x0027C7D8` and `0x0027C9CE` | `0x0046B690`, actor managers 0-2 | 512 (`0x0031F620`) |
| `0x1D` | the licenses a member owns, for the Party Menu's four-pane panel (`0x002C4B3B`) | bit *n* of the member record's `+0x194` for license node *n* ([Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md); `0x0031F850`-`0x0031F862`) | the node count `[0x02EBF038] + 4` (`0x0031F81F`); 512 (`0x0031F82D`) |
| `0x1E` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x1F` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x20` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x21` | no call in the exe passes this code | no rows: `0x0031F70C` returns the empty list | - |
| `0x22` | a page of the gambit actions ([Gambits screen](gambit-screen.md); `0x0056A930`, `0x0056AF65`) | the grid at `0x0208D308`, page `+0x3C` below `[0x0208D300]` (`0x0031F9AF`-`0x0031F9BF`) | the page width `[0x0208D301]` (`0x0031F9C5`); 512 (`0x0031F9E0`); the first id that `0x00322C50(0x14)` refuses (`0x0031FA10`) |
| `0x23` | a page of the gambit conditions (`0x0056B1D4`, `0x0056BD0F`) | the grid at `0x0208D318`, page `+0x3C` below `[0x0208D310]` (`0x0031FAA6`-`0x0031FAB2`) | the page width `[0x0208D311]` (`0x0031FAB8`); 512 (`0x0031FAD0`); the first id that `0x00322C50(0xB)` refuses (`0x0031FB00`) |

### Row painters

`0x0027E050` installs one painter per list (`0x0027E2F0`):

| Painter | Lists | Draws |
|---|---|---|
| `0x00276BE0` | top commands, Mist | the command labels |
| `0x0027D240` | the magick schools, kind 2 | the label word of the school row (class `0x18`) when flag bit `0x4` is set, of the command row (class `0x15`) otherwise |
| `0x0027CE70` | the action lists, kinds 4-8, 10-15 and 20 | the action rows |
| `0x0027BC10` | kind 9, list `0x18` | the name of a class 1 row, or Remove (`menu_command.bin` `0x404`) for the id -1, with byte `+0x15EF` set to 6 for the row equal to `+0x1538` |
| `0x0027D5C0` | target list `0xF` | the name of the row's id through `0x0031C5D0` |
| `0x0027E530` | the other target lists | nothing while the page's `+0x1528` bit `0x8000` is set (`0x0027E54B`); otherwise the unit's name (`0x00272CB0`) and, when `0x00272C80` gives an ordinal above 0, that ordinal's letter after it, the letter `0x0024ABE0` writes, as over the unit's head (`0x0027E657`-`0x0027E686`, [Enemy names on screen](enemy-names-on-screen.md)). With the language test `0x00254A10` false the letter text starts past its blank `0x06` and stands at the name's width plus half of `0x0039C100()` less `0x0039C120(ordinal)`, plus 4 (`0x0027E693`-`0x0027E6F0`); with it true the letter ends 11 short of the width `+0x9C` of the widget `[page + 0x1510]` (`0x0027E6FA`-`0x0027E750`). Both draw through `0x002D8690` (`0x0027E765`) |

A row whose greyed flag is set is drawn at half brightness: its colour scale `+0x5A` becomes `0x40`
(`0x0027E60C`-`0x0027E61B`, `0x0027D2BA`-`0x0027D2D3`), and `0x0027E530` restores it after the row (`0x0027E782`).

An empty list draws one row whose colour byte `+0x90` is `96 + 32 x sin(t x pi / 30)`, with `+0x91` and `+0x92` at
`0x30` and the alpha `+0x93` at `0x80`, t being the frame counter `0x0208F570`, and the text "No Available Targets"
(`menu_message.bin` `0x7D1`) for a target list, and `0x7D2`, empty in the
shipped text, for the others (`0x0027D24A`-`0x0027D25E`, `0x0027BC1A`-`0x0027BC29`; the colour at `0x0027E566`-`0x0027E5DD`,
`0x0027D263`-`0x0027D2B2`, `0x0027BC33`-`0x0027BC91`).

### Names and help

The labels and help come from the battle command table, class `0x15` (21 rows), and the magick schools, class `0x18`
(5 rows): word `+2` is the label and word `+0` the help line (`0x0031DC54`-`0x0031DCEC`).

| Command | Help (`help_menu.bin`) |
|---|---|
| Attack | "Attack with weapon in hand." (`0xBB8`) |
| Technicks | "Special actions that cost no MP." (`0xBBA`) |
| Items | "Use items from your inventory." (`0xBBB`) |
| Summon | "Summon an Esper to fight at your side." (`0xBBD`) |
| Quickening | "Perform powerful attacks." (`0xBBE`) |
| Gambits | "Toggle character gambits ON/OFF." (`0xBBF`) |
| Dismiss | "Release a summoned Esper." (`0xBC1`) |
| Magicks & Technicks | "Use magicks and technicks." (`0xBC4`) |
| Mist | "Perform an action expending Mist Charges." (`0xBC5`) |
| the five schools | `0xBC7`-`0xBCB`, for example "Offensive magicks for dealing damage." |

### Input

The list widget reads the pressed word ([Controls](../Controls-And-Input/controls.md), `0x00277ACD`):

- Square closes the menu in every state (`0x00277ADE`-`0x00277B15`).
- Outside a target list, left and right step to the previous or next party member when more than one is in the party
  (`0x00277BFF`, `0x0027C280`). `0x0027C280(handle, step)` keeps the members whose record has flag bits `0x1` and `0x8` clear, puts
  them in party order (`0x00273600`, an insertion sort of `{key, value}` pairs) and steps round them.
- In a target list, L1 and R1 step the target category (`0x0027B430`, `0x0027C730`) among the tabs the manager allows.
- The row cursor, confirm and cancel come from the page's list, which posts `0x8000`, `0x8001` and `0x8002` to the list
  widget in the convention of [Dialogs](dialogs.md).

### Target tabs

The tab strip `0x0027C870` shows one tab per target list the action allows.
`0x00276960(tabs, actor, action, kind, show, mask, ...)` sets it up from the mask:

1. Mask bits `0x1`, `0x2`, `0x8` and `0x4` enable tabs 0 to 3, the strip's child nodes 2 to 5 (tables `0x00915BE0` and `0x00915BF0`,
   `0x00276A19`-`0x00276A60`).
2. Bit `0x8` is dropped when target list `0xF` has no row (`0x0027B090`), and bit `0x4` when list `0x1C` has no row left
   after filtering (`0x0027AF80`).
3. A disabled tab's four corner alphas are set to 0; an enabled tab takes its layout alphas at once
   (`0x00276A90`-`0x00276AA0`; the add of `0x18` after it is capped at the same bytes, `0x00276AC0`-`0x00276ADC`) and is
   placed at `0x0027B290(tabs, mask, i)`.
4. The strip is centred from its total width `0x0027B120`, and its side nodes 6 and 7 are hidden when the mask
   is 1, 2, 4 or 8 and shown for every other mask, 0 included (`0x00276B4E`-`0x00276B7A`).

The filter skips, for filter 1, rows with flag bit `0x2` and units whose status words hold KO, Stone or bit
`0x80000000` (`0x00273710`, mask `0x80000003`), and for every filter units whose byte `+0x0A` (`0x002647E0`) has bit `0x4`
(filter 0) or bit `0x1` (otherwise).

`0x0027B5A0` makes the same two checks from a saved request when L1 or R1 is pressed (`0x0027C730`), and `0x0027B6C0` only
answers whether target list `0xF` has a row (`0x0031EB20`). `0x0027BB70` applies the checks to a page's rows in place,
keeping the count at `+0x40`; its callers `0x0027D740` and `0x0027E050` take the filter from page bit `0x8000` and the
mask from page bit `0x1000`, which picks bit `0x1` over bit `0x4`.

`0x0027DCA0` moves the strip half way towards its centred position, snapping when it is within 1. `0x00276830(tabs,
kind)` marks the tab of list kind `0x10`-`0x13`: the other tabs draw one palette further on.

### The first target row

`0x0027BED0(page, handles)` picks the row a target list opens on (`0x002798E8`), the first rule that finds one:

1. the first row not greyed (flag bit `0x2`) whose unit is one of the four handles given;
2. the first row with flag bit `0x1`;
3. the row of the acting unit, page `+0x08`;
4. the nearest row that is not greyed and not the actor and whose unit is on screen, else the nearest such row;
5. the saved row `+0x44`, or the first row not greyed, or row 0.

Distances are from the actor's position (`0x002E9D10`, `0x00203080`, `0x002703F0`). A unit is on screen when its position
projects in front of the camera `0x02AEDDB0` (`0x00272250`) inside the 1920 x 1080 frame (`0x00273850`). `0x00272180(out,
matrix, point)` projects a point and divides by its depth; `0x00272250` turns the result into frame coordinates,
`(x - 0x8000) / 16 + 0x01E0C1D8 / 2` and the same for y, and `0x002722A0` does the same with the width divided by
`0x00183280()`.

### Refreshing an open list

`0x0027D740(page)` rebuilds an open page while its `+0x1528` bit `0x400` is set:

1. A command or action list is rebuilt with `0x0031EB20`; an action list (page kind 11) keeps the cursor on the row
   with the same id, and the cursor is clamped to the last row.
2. A target list (bit `0x2000`) is rebuilt from a copy of the page (`0x00272400`, which copies dwords `+0x00`, `+0x40`
   and `+0x44`, bytes `+0x08`-`+0x3F` and the eight-byte rows, leaving `+0x04` and `+0x48`-`+0x4F` as they were).
   With bit `0x40000` set the rebuilt rows are stored as they are (`0x0027D9FE`).
3. Otherwise the rows are filtered (`0x0027BB70`) and ordered. Once bit `0x4000` is set the list keeps its old order
   (`0x002727F0`: rows still present first, in their old order, then the new ones). The first rebuild sets bit `0x4000`,
   after sorting the rows by where their units stand across the picture, left to right, when bit `0x1000` is
   set (`0x002729A0`).
4. The cursor stays on the same unit, or is clamped to the last row; bits `0x80800` are set when the row count or the
   cursor changed.
5. With bit `0x8000` set, when the cursor had to move and the list is empty, or, on any rebuild but the first
   ordering (rows kept in their old order, or stored as they are under bit `0x40000`: `0x0027DA9F`), the row now under
   the cursor is another unit, the saved copy of the list and the cursor are put back and bit `0x100000` is set
   (`0x0027DB06`-`0x0027DB55`).

The key of each row in `0x002729A0` is the horizontal frame coordinate `0x00249110` gives for the unit's position
under the camera matrix `0x02AEDDB0` (`0x00272A73`-`0x00272AA0`); no distance is computed. `0x0035BC50` sorts its list
`0x1A` at `0x022C83F0` by the same coordinate (`0x00272B40`, key at `0x00272BBB`-`0x00272BDC`; called at `0x0035BD19`).

Both sorts end in `0x002748E0(n, rows, ascending)` (`0x00272AC5`, `0x00272C0F`, each passing 1). It orders `n`
eight-byte rows by their signed dword `+0`: a quicksort with its own stack of ranges leaves ranges of 11
rows or fewer, and one insertion pass over the whole array finishes; a zero third argument sorts in
descending order.

### The target cursor

`0x0027CD00(cursor, widget)` draws the hand over the target unit (`0x002780DC`): it projects the unit's position
(`0x002713E0`, `0x002722A0`), hides the hand while the unit is behind the camera (`0x003678F0`), and otherwise slides it
from its last place towards the unit by the blend at `+0x0A` (`0x002752E0`), jumping straight there after it was
hidden; `0x00368360` draws it, and `0x00368940` also runs once the blend is full.

The list's row hook `0x0027E4E0(page, widget, unit)` (`0x00279C26`) pulses a row while `0x0027B770` finds its unit within
the radius `+0x1540` of the cursor's unit (`0x0027B3B0`), neither row greyed: `0x0027AF00` sets the draw's `+0x58` to half
of the page's `+0xA0` and swings its `+0x5A` by `sin(frame x pi / 7)` times half its value. `0x0027BD80(actor, action)` returns the value `0x0031AB80`
reports for a kind 1 answer, or 0 (`0x00279ABF`).

The grid list draw `0x00367AA0` pulses its cells the same way through a hook. `0x00368A50(widget, hook)`
keeps the two at `0x022CBE90` and `0x022CBE98`; for each visible cell the draw calls
`hook(widget +0xD8, sprite, cell, first)` and draws the sprite over the cell when it answers non-zero
(`0x00367DC5`). The list widget `0x002778C0` installs one of two hooks, both ending in the `0x0027B770` test
for the cell's row id `+0x510 + 8 x cell`:

- `0x0027D700` (`0x002794DF`, while `+0x1528` bit `0x200000` is set) first runs `0x0027B200` for cell 0;
- `0x0027E7B0` (`0x00279AEC`) answers 0 while `+0x1528` bit `0x8000` is set and runs `0x0027B200` on a draw's
  first call. `0x0027B200(page, sprite)` passes the sprite's `+0x3C` x 4 to `0x002030E0` and calls
  `0x0027AF00`.

The target lines and marks the list asks for while it is open (`0x0027DE30`, `0x0027DC10`) are on [HUD](hud.md).

### From a row to an action

Confirm (`0x8001`) runs the classifier `0x0027C3D0` (`0x0027841E`), which answers with what comes next:

| Row | Next |
|---|---|
| Attack | the foe list for action `0x96` (`0x0027C469`) |
| Items, Summon, Quickening, Magicks & Technicks, Mist, a school | that list |
| Gambits | switches the member's gambits on or off at once (`0x00311AF0`, `0x0027C512`); the menu stays open on the same list (below) |
| Dismiss | the Dismiss confirmation |
| an action | its target list, or the action at once when it needs no target choice |
| a greyed row | refused with sound 5 |

The Gambits row is command 13 of list 6; the classifier's command arm, which serves list codes 6 and 9, picks it (`0x0027C457`, table `0x0027C6D0`). The classifier reads the member's
switch (`0x00309B40`), writes the opposite with `0x00311AF0`, and answers `0x17` when it turned the gambits on and `0x19`
when it turned them off (`0x0027C4F3`-`0x0027C529`). The list widget then (`0x00278559`-`0x002785AC`):

1. sets the list's confirm sound `+0xFC` to `0x12` for on or `0x13` for off (`0x00278569`, `0x00278577`), which the
   list's step plays once the widget answers the confirm with 0 (`0x002D4114`-`0x002D4154`);
2. runs its page tasks through `0x00274BD0(head, first, 0xFF)` (`0x00278592`), the rebuild `0x0027D740` of each open page
   whose `+0x1528` bit `0x400` is set (Refreshing an open list, above);
3. sets the countdown `+0x2DB4` to 6 (`0x002785A3`) and answers 0 (`0x002785AA`); this path does not call the close
   `0x00244F00`, which the answer `0x1B` does (`0x00278632`).

The countdown drops by one on each update (messages 10 and 11) that reaches `0x00277F7A`, and stops at 0
(`0x00277F82`-`0x00277F88`). While it is not 0 and the page's `+0x1528` bit `0x20000` is set, the list's `+0xE4` bit `0x20` is set
(`0x00277F3D`-`0x00277F68`), and the list's step then does not pass a confirm press on (`0x002D40AE`). The page build
(message 31) sets bit `0x20000` for menu kind 9, list `0x18`, and clears it for every other kind (`0x00279527`-`0x00279541`,
`0x0027E2D8`), so on the top list the countdown runs without blocking a press.

The answer `0x17` also follows the actions `0x9C` and `0x9D` that the classifier issues at once (`0x0027C5FE`,
`0x0027C642`, `0x0027C665`), and they take the same path.

A new list of the same panel is rebuilt in place and pushed on the stack; a target list opens in a new panel. Cancel
pops the stack and closes the menu when it is empty (`0x002787AF`).

The action is issued through `0x00311CD0(actor, target, action, 0)` (`0x00278766`), or `0x00311B20` for a party-position
target (`0x0027869B`), which both reach `0x00311CF0` once ([Action phases](../Battle-Actions/action-phases.md)).
`0x00311B20` returns -1 without reaching it when the acting handle resolves to no unit, or when a non-zero target
handle resolves to no unit for an action other than `0x414E` (`0x0031B7E0`, `0x00311B3E`-`0x00311B74`).

The menu never asks for the whole party (fan-out 0 at all six call sites). Dismiss asks "Dismiss {name}?"
(`menu_message.bin` `0x7D0`, `0x0027AA70`) and on Yes issues action `0x113` on the Esper (`0x0027AB01`).

### The help line

The help block is `[0x0209BE80] + 0x8FA0`, drawn in two alternating windows `0x002BF690`. `0x0027B880` fills it on each
cursor move:

- a command row shows its help;
- an action row shows the action's description;
- a greyed row shows its refusal first, through `0x0027C150`;
- a target row opens the target information window (`0x002C0870`) instead of text.

The help block's own calls (`0x0028FEA0`, `0x00290C60`, `0x00290C80`) are listed on [HUD](hud.md). The target information
window `0x002BFD20` builds its weakness line with `0x00295D90(size, out, mask)` (`0x002C02B2`): "Weak: "
(`listhelp_common.bin` `0x2331`), an optional part from `0x002AC290`, then one element icon, text `0x4B27` plus the
element, for each set bit of the mask.

Observed in the game, Reks targeting a Cactite: without Libra on Reks the window shows "Lv. ??" and "HP ????/????".
With Libra on Reks it shows "Lv. 2 Cactite A", "HP 84/84" and a blue Libra mark at its top right; with augment 41
(Anti-Libra, the status record's `+0x51` bit `0x2`) on the Cactite it shows "Lv. ??" and "HP ????/????" again and
the mark is crossed by a red X.

`0x0027C220(page, row)` picks the refusal: in a command list (page kind 6 to 10) a row with flag bit `0x2` gives its reason
byte `+4`, in an action list (kind 11) a row with flag bit `0x1` gives its byte `+6`; a positive reason with a row in
`0x0027C150` becomes that text (`0x0027C220`-`0x0027C27E`).

| Refusal | Text (`help_menu.bin`) |
|---:|---|
| `0x7` | "Stopped: Cannot take commands." (`0xC92`) |
| `0x8` | "Sleeping: Cannot take commands." (`0xC94`) |
| `0x9` | "Confused: Cannot take commands." (`0xC95`) |
| `0xA` | "Silenced: Cannot use magicks." (`0xC96`) |
| `0xB` | "Disabled: Cannot take commands." (`0xC93`) |
| `0xC` | "Berserk: Cannot take commands." (`0xC91`) |
| `0xE` | "Magicks forbidden: Cannot use magicks." (`0xC90`) |
| `0x16` | "You cannot attack here." (`0xC8A`) |
| `0x17` | "You cannot use magicks here." (`0xC8B`) |
| `0x18` | "You cannot use technicks here." (`0xC8D`) |
| `0x19` | "You cannot use items here." (`0xC8F`) |
| `0x1A`, `0x1B` | "You cannot summon here." (`0xC98`, `0xC99`) |

The window rises by `HelpMessageMoveY` (`0x002BF77A`) while the boss gauge is out of its compact state.

Each window is a `0x500`-byte widget at the help block's `+0xC0` or `+0x5C0`, the two used in turn by the byte
`+0x10C8` (`0x002BF5C1`-`0x002BF644`). `0x002BF4F0`, run by the block's procedure `0x002BE490` (`0x002BE4C1`), builds a window,
or, while one is up, a new line in it (`0x002BFB40` at `0x002BF577`). A line is a `0x100`-byte widget `0x002BF8C0` in the
next of four slots at the window's `+0xD8`, chosen by the cursor `+0x4E8` (`0x002BFB9A`-`0x002BFBF6`); the new line waits
at `+0x4D8` and becomes the active line `+0x4E0` once that is empty (`0x002BFB58`-`0x002BFB93`).

A line whose text is
wider than its box scrolls: after a hold of 60 frames it moves left by one each frame and wraps, the text drawn
twice, the second copy one text width plus the width of the gap text `0x00916C28` after the first (`0x002BF8C0`).

The help window, `0x500` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C0` | `void*` | block | the help block that built the window: the construct message stores the creation record's first qword (`0x002BF7D1`-`0x002BF7DF`), which `0x002BF4F0` sets to the block (`0x002BF542`) |
| `+0x4EA` | `u16` | flags | bit `0x1`: the picture cell `+0x4E9` is still to be shown. The builder sets it with `+0x4E9` (`0x002BF587`-`0x002BF595`, `0x002BF617`-`0x002BF626`); the next tick (message 2) clears it and gives the window's first node that cell at its `+0x0A` and the cell's byte 7 at its `+0x39` (`0x002BF718`-`0x002BF74E`) |
| `+0x4F0` | `void*` | text | the help text shown, the creation record's `+0x10`, which `0x002BF4F0` copies from the block's `+0x10D0` (`0x002BF53B`): stored by the construct message (`0x002BF880`-`0x002BF887`) and by each new line (`0x002BFCE1`-`0x002BFCED`) |
| `+0x4F8` | `i16` | baseY | the window's y from its layout, kept by the construct message (`0x002BF808`-`0x002BF80F`), which then puts the window at this plus the rise or plus 0 (`0x004051D0`, `0x002BF826`-`0x002BF84E`); each tick moves the window to this plus `0x002BED00(HelpMessageMoveY)` when its y `+0x9A` differs (`0x002BF77A`-`0x002BF7BA`) |

A help line, `0x100` bytes, four at the window's `+0xD8`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xC0` | `void*` | block | the help block, the creation record's first qword, stored by the construct message (`0x002BFA53`-`0x002BFA61`) |
| `+0xD8` | `void*` | text | the line's text, the creation record's `+0x10` (`0x002BFAC3`-`0x002BFAC7`), drawn by `0x002D8910` (`0x002BF93C`, `0x002BF969`, `0x002BF989`) |
| `+0xE0` | `void*` | font | the font the line is measured and drawn with, the creation record's `+0x18` (`0x002BFACE`-`0x002BFAD2`; measured by `0x0029CD90` at `0x002BFC25`); the fifth argument of each draw (`0x002BF933`, `0x002BF959`, `0x002BF97F`) |
| `+0xE8` | `i32` | loopWidth | the scroll's cycle: the text's width plus the width of the gap text `0x00916C28`, both from `0x0029CD90` (`0x002BFC6D`, `0x002BFCB7`), through the creation record's `+0x28` (`0x002BFAF8`-`0x002BFB04`); the offset wraps at it (`0x002BF9E2`) and the second copy is drawn at it less the offset (`0x002BF950`-`0x002BF975`) |
| `+0xEC` | `u32` | holdStart | the frame counter `0x0208F570` when the line was built (`0x002BFAEC`-`0x002BFAF2`): while it is not 0 the line is drawn once at x 0 (`0x002BF921`, `0x002BF97F`-`0x002BF99A`), and the tick sets it to 0 once more than 60 frames have passed (`0x002BFA08`-`0x002BFA15`) |
| `+0xF0` | `i32` | scroll | the scroll offset: 0 when built (`0x002BFB0A`); each tick of a scrolling line adds the frames since `+0xF8`, modulo `+0xE8` (`0x002BF9D8`-`0x002BF9E8`); the draw puts the text at x = -offset and again at `+0xE8` - offset (`0x002BF92A`-`0x002BF975`) |
| `+0xF4` | `u32` | flags | bit `0x1`: the text is wider than its box, the creation record's `+0x30` (`0x002BFC34`-`0x002BFC3D`, copied at `0x002BFAD9`-`0x002BFAE6`), so the line scrolls; bit `0x2`: set once the line has posted message 12 up the chain (`0x00275440`) on its first tick (`0x002BFA1F`-`0x002BFA47`); the window answers message 12 by closing its active line `+0x4E0` (`0x002BF6DA`-`0x002BF6FF`) |
| `+0xF8` | `u32` | lastStep | the frame counter at the last scroll step (`0x002BF9EE`-`0x002BF9F4`), and at every tick of the hold (`0x002BF9FC`-`0x002BFA02`); a counter below it counts as one frame (`0x002BF9C5`-`0x002BF9D6`) |

The host `0x002BE490` keeps the two windows `0x2B8` bytes apart. On its message 2, `0x002BE290` builds the target
information window (`0x002C0F30`) when bit `0x1` of `+0x57E` asks for it, in the free window that `0x002BEA40` returns:
`0x002BEA40` clears `+0x570`, starts closing each busy window whose `+0x280` bit `0x1` is clear, and returns a window with no
procedure. `0x002BE290` then closes the window at `+0x570` once its `+0x280` has bit `0x4` set and bit `0x1` clear, and clears
`+0x570` and bit `0x2` of `+0x57E`.

While `0x002BFD20` lays the target window out, `0x002C0760` hides six of its child widgets
and seven of its parts and sets its height from part 5, and `0x002C03A0` hides the child of part 12.

The window shows its key `+0x288`: a unit handle, or a party member type when `+0x280` bit `0x2` is set
(`0x002BFF3D`-`0x002BFF8F`). Message 1 measures the box `+0x28C`-`+0x292` (x, y, width, height) from a scratch layout
(`0x002C0AD4`-`0x002C0B12`), and message 3 draws it as a soft-edged box (`0x00392A00`, `0x002C08DA`-`0x002C0967`).

The statuses take turns through the status cycle record at `+0x2A0` ([Party list](party-list.md)), stepped by
`0x00272F80(record, 30, 2, +0x29C, key)` on every layout pass (`0x002C019D`-`0x002C01D6`); `+0x29C` is the frame counter
`0x0208F570` less 30, stored on activation, message 6 (`0x002C08C6`-`0x002C08CF`), and the layout shows the status row at
`+0x2B0` (`0x002C01DF`-`0x002C023B`).

The action id and focus handle the help block posts (`0x00290C80`, `0x00290C60`) land at `+0x294` and `+0x298` and set
`+0x280` bit `0x20`; nothing reads them, and every layout pass sets `+0x294` to `0xFFFF` (`0x002C01B1`).

### The party list

The party list `0x0029BE50` (`0xB68` bytes, at `[0x0209BE80] + 0x10F78`) draws one slot `0x0029A0A0` per member from the
0xC0-byte party status records ([Party member status record](../Characters-And-Objects/party-member-status-record.md)):

| Element | Drawn by | From |
|---|---|---|
| name | `0x00297F60` | `+0x10` |
| HP | `0x00297D10` | `+0x20` |
| HP gauge | `0x00297E10` | HP against the larger of HP and `+0x28` |
| max HP | `0x00297E70` | `+0x24` |
| MP | `0x0029A8E0` | `+0x2C` |
| MP bars | `0x0029A930` | `+0x38` over `+0x87` bars; the first `+0x86` bars pulse, with sound `0x48` or `0x49` when that count changes |

The battle menu highlights the acting member's slot (`0x00296AF0`) and clears it (`0x00296B80`). How the rows are built
and animated, the rolling numbers, and the modes in which the rows become the target cursor are on
[Party list](party-list.md).

The menu finds members through the party status records at `0x0035BB20(i)`, `0x0C0` bytes each, with the handle at
`+0x04`:

- `0x00273320(handle)` returns the member's position, or -1, and `0x002737B0(handle)` whether it is in the party.
- `0x00272EE0(handle)` returns the record's type `+0x60`, or 6 when no record of the first four has the handle.
- `0x00273460()` returns the handle of the first record with flag bit `0x4`, and `0x002734B0()` that record.
- `0x00273800(handle)` returns 1 when the member's record has flag bit `0x8` clear, that is, when it is in range.

### The boss gauge

The boss gauge `0x00405310` (manager `0x00406A60`, `0x02B62D88`) draws up to two bars from the table at `0x02EC1380`, which
`0x0031B690` fills every frame with HP and MP. Only `0x00328FF0` registers a unit there, always as entry 0
(`0x0023AA04`), with the class from the spawn row ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
The style is one bar for class 1 or 2 and style 2 for class 3 (`0x00405100`).

### Boss gauge bars

Each bar is a child `0x004061F0` of the gauge's window `[0x02B62D88] + 0xC0`, at `+0xC8` and `+0xD0`
(`0x00404D40(i)` returns bar `i`, 0 or 1). A bar carries the counter of the
[script gauges](script-gauges.md) (`+0xC0` mode, `+0xE0` maximum, `+0xE4` value, `0x00408140`, `0x00407240`).

- `0x00405770(gauge, style)` sets both bars up for a style from the pairs at `0x00D12190`: style 0 uses layout child 0
  and hides bar 1, styles 1 and 2 use children 2 and 3, style 3 children 1 and 2. It reads each value with
  `0x00404F50` (1000 when missing), sets the maximum (`0x004073B0`) and redraws.
- `0x00404F50(i, style, cells)` returns entry `i` of the value table `[0x02B62D88] + 0xE8` (count `+0xE3`, 0x18 bytes
  each). For style 2 it cuts entry 0 into 50 cells: `cells = current x 51 / max`, 51 counted as 50. Bar 0 then
  gets the part inside the current cell, bar 1 the cell count as a width `cells x 6 - 2` of 298.
- `0x004060B0(bar, open, b)` does nothing while the bar's `+0x130` bit `0x1` is set. Otherwise it shows the bar
  (`0x00246AD0`). With `open` it sets that bit, starts the 25-frame count `+0x17A`, keeps `b` at `+0x13A` and zeroes the
  50 cells `+0x13C`; a segmented bar (`+0x130` bit `0x100`) also plans a ramp of 50 cells over 25 frames. Without
  `open` it marks all 50 cells lit (9).
- `0x004058E0(bar, start)` runs the opening or closing each frame: the value widget grows by the square of the eased
  step (`0x00248F40`), or a segmented bar widens cell by cell (`0x004076B0`). When a closing run ends the bar is
  released (`0x00245020`).
- `0x004068B0(bar, value)` takes a new value, ends a running ramp at it and sets the flash timer `+0x178`:
  - with `+0x130` bit `0x40` the timer is 40 when `+0x136` is 0, else 8 with cell `+0x137` of `+0x13C` set to 10;
  - with bit `0x80` it is 1 when `+0x136` is 0, else 8 with the cell before `+0x137` set to 1; bit `0x20` is set in
    both cases;
  - any other bar gets 1 frame for a rise; 40 for a drop, or 1 once the drops' total `+0x17C` passes 3,999 (each adds
    40 divided by its size, at least 1).
- `0x00406770(bar, on)` re-reads the value when shown, and `0x00406DD0(gauge, on)` records the state in `+0xC8` bit `0x20`
  and passes it to every shown bar (`+0x130` bit `0x10`).
- `0x00405C20` draws a bar: the number (`0x0029E840`) and, for a segmented bar, up to 49 cell frames in batches of 16
  (`0x002D9DB0`, `0x002DAC70`). A lit cell's state counts 1 to 8 while the first sprite fades out, then 9 to 17 while
  the second fades in, wrapping to 9 (`0x002D8D10`).

While the manager's `+0xC8` has bit `0x40` or `0x80` set (the manager `[0x02B62D88]` is loaded at `0x0040631A`, its
`+0xC8` read at `0x0040639D`), a bar skips the rest of its frame from `0x004063B8` on, unless it is closing: its
`+0x130` bit `0x8`, set only by `bossgaugeclose` (`0x00404EE2`), is tested at `0x004063AB`.

The pause test comes after these steps, in order (`0x004062A0`-`0x00406397`), so they run during a pause:

1. the frame ends when `0x001EDEC0` returns 0 for the bar's `+0xB4` or the bar's `+0xD8` bit `0x20` is set
   (`0x004062A0`-`0x004062BA`);
2. for style 2 with `+0x136` clear, the style-2 maximum refresh: `0x004073B0` takes `+0x0C` of what `0x00404F50`
   returns for style 2 (below), and is skipped when that is null (`0x004062C0`-`0x004062E9`);
3. with a manager, the `0x00247870` call, told whether the manager's value count `+0xE3` is non-zero; the frame
   ends when it is zero (`0x004062EE`-`0x00406314`);
4. while the delay `+0x13A` is non-zero, it is counted down by one and the frame ends (`0x00406321`-`0x00406340`);
5. the frame ends when there is no manager or the manager has no window at `+0xC0` (`0x00406341`-`0x00406354`);
6. while bit `0x1` of the window's `+0x40` is clear: a non-zero 25-frame count `+0x17A` is copied into the flash
   timer `+0x178` (`0x0040637B`), but the frame ends instead when the bar's `+0x130` bit `0x1` is set
   (`0x00406375`); a zero count ends the frame unless the bar is closing (`0x00406384`-`0x0040638B`);
7. the frame ends when bit `0x1` of the bar's own `+0x40` is clear (`0x00406391`-`0x00406397`).

The verbs reach the gauge through one-jump stubs:

| Verb or caller | Function | Effect |
|---|---|---|
| `bossgaugeopen` (`0x00349B60` → `0x003EC7F0`) | `0x00405270` | sets `+0xC8` bit `0x1`, unless bit `0x2` or `0x20` is set |
| `bossgaugeclose` (`0x00349F80` → `0x003EC7C0`) | `0x00404E10` | once (`+0xC2` bit `0x1`): turns the bars off (`0x00406DD0`), closes the window (`0x00244F00`) when a value is still above 0, or else releases each bar or marks it closing |
| HUD hide (`0x0035D0E0`) | `0x00405150` | closes the window (`0x00244DD0`) and remembers it in `+0xC8` bit `0x4` |
| HUD show (`0x0035D1B0`) | `0x004052D0` | reopens it (`0x00246AD0`) when bit `0x4` is set |
| pause mask `0x0215F1B3` | `0x00404D70`, `0x00404DC0` | sets or clears `+0xC8` bit `0x80` ([Script gauges](script-gauges.md)) |

### Overhead HP gauges

`0x002C7660` gives each unit a gauge kind, 0 for a party member, 1 or 2 for other units, and `0x002C8310` draws it when
the unit's byte `+0x17` bit `0x2` and the HUD's bit are set. The step is `min(HP, max) x 100 / max >> 2`, 0 to 25
(`0x002C8398`-`0x002C83A1`); it picks the frame `0x00916F08[step]` and a colour between the kind's `Min` and `Max` keys
(`0x002C5F90`).

`0x002C8310` itself, from its one call (`0x002C7892`):

- draws nothing when its third argument is 0 or when `0x003F0040` gives it no sprite (`0x002C8310`-`0x002C8314`,
  `0x002C833F`-`0x002C834A`);
- takes the step as 0 when the maximum is 0 and counts an HP below 0 as 0 (`0x002C838C`-`0x002C8394`);
- reads frame `0x00916F08[step]` past the base frame of the sheet `0x0035D3D0` returns (`0x002C83A8`-`0x002C83D8`) and hands
  the sprite, that frame, the third argument and the step's colour `0x002C5F90(kind, step)` to `0x002C69A0`
  (`0x002C83E1`-`0x002C8422`);
- stores the four bytes of `0x002C5F90(kind, 0)` at the sprite's `+0x90`, `+0x94` and `+0x98`, and the fourth times
  the third argument, shifted right 7, at `+0x9C`, with 1 at `+0x80` (`0x002C8427`-`0x002C8488`);
- submits the sprite with `0x003F1290`: to its fifth argument when the eighth is 1, otherwise to its fourth after
  `0x00202B10` moves the position at `+0x10` by the ninth and sets `+0x1C` to 1.0 (`0x002C8480`-`0x002C84BD`).

| Kind | Layout keys |
|---:|---|
| 0, party | `HpGaugeSide{Min,Max}_{R,G,B,A}` (`0x01E0CEF8`-`0x01E0CF14`) |
| `1` | `HpGaugeEnmey{Min,Max}_{R,G,B,A}` (`0x01E0CED8`-`0x01E0CEF4`) |
| `2` | `HpGaugeOther{Min,Max}_{R,G,B,A}` (`0x01E0CF18`-`0x01E0CF34`) |

### Layout keys

| Part | Keys |
|---|---|
| panel | `BattleMenuLRCursorMoveX` (`0x002776CB`) |
| list size | `BattleCommandGillTagOffset`, `BattleCommandNumTagWidth`, `BattleCommandScrollTableOffsetX`, `mCommandTitleFontHeight` (`0x0027DED0`) |
| list page | `mScrollListHeight` (`0x0027AE79`) |
| command rows | `mGambitPositionOffsetX/Y`, the ON/OFF mark on the Gambits row (`0x00276BE0`) |
| action rows | `BattleCommandNumPosX`, `BattleCommandMistPosX/Y`, `BattleMistCount0Offset`-`BattleMistCount3Offset`, `BattleMistIconWidth` (`0x0027CE70`) |
| help line | `HelpMessageMoveY`, `mHelpMessageFontCount` |
| boss gauge | `BossGaugeExColorR/G/B/A` (`0x0029EA58`-`0x0029EA6F`) |

The label widths come from a pre-pass, `0x00273E30`, which scene and action code runs (`0x00306760`, `0x00313550`,
`0x00313840`, `0x00254A90`) and which writes `0x022CA408`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | id | class `0x15` row, or class `0x18` school when flags bit `0x4` is set |
| `+0x03` | `u8` | flags | bit `0x2` greyed, bit `0x4` school row, bit `0x8` greyed by `0x00318CD0` answer 2 |
| `+0x04` | `u8` | reason | refusal shown through `0x0027C150` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | id | action id (class `0x14`) |
| `+0x02` | `u16` | cost | MP, Mist charges or item count |
| `+0x04` | `u16` | flags | bit `0x1` greyed, mask `0x3C0` the targets the action needs |
| `+0x06` | `u8` | reason | `0x002FFCF0` code from `0x00317BC0` |

### The list widget's page tasks

The list widget (`0x2DC0` bytes, procedure `0x002778C0`) keeps four `0x20`-byte page-task records at `+0x2D30`, each `{function, argument, previous, next}`, linked from `+0xE0`; the stepper `0x00274BD0` calls each record's function in turn and unlinks a record whose function answers 1.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2D40` | `void*` | headPrev | the previous link of record 0 of the list widget's four 0x20-byte page-task records at +0x2D30 ({function, argument, previous, next}). Record 0 is the list head (+0xE0 and +0xE8 are set to +0x2D30 at 0x00277999, 0x002779A0), so nothing links before it: 0x00274BA0 sets the previous link of records 1-3 only (0x00274BC8, called for records 1, 2 and 3 at 0x002779C8). The stepper 0x00274BD0 reads it when record 0's function answers 1 and the record is unlinked (0x00274C3C) and sets it to 0 (0x00274C61); it stays 0 |
| `+0x2D48` | `void*` | headNext | the next link of record 0: 0x00274BA0 reads it to find the tail (0x00274BA0) and sets it to record 1 when it appends record 1 (0x00274BC4); the stepper 0x00274BD0 follows it (0x00274C15), relinks it past record 1 when record 1 is unlinked (0x00274C49) and sets it to 0 when record 0 is unlinked (0x00274C65). Record 0's function is the page rebuild 0x0027D740 for the child page at +0xF0 (0x0027795C, argument +0x2D38 at 0x0027795F); record 2's is the same for the page at +0x1710 (0x00277984, 0x00277977); records 1 and 3 hold the stub 0x005C5230 (0x0027796A, 0x0027798B) |

### The boss gauge manager

The manager is the `0xF0`-byte widget kept at `0x02B62D88` with procedure `0x00406A60` (The boss gauge above).

`BossGaugeManager` (`0xF0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00406A60` |
| `+0xC0` | `void*` | window | the boss gauge window, the `0xD8`-byte widget with procedure `0x00405310` that the tick builds (`0x00244F50` at `0x00406C36`) and that stores itself here (`0x00405384`); the tick attaches it hidden (`0x00244960`) while the HUD is hidden and opens it otherwise (`0x00406C3B`-`0x00406C63`); `0x00404D40` returns its bars (`0x00404D4C`), and bossgaugeclose `0x00404E10`, the HUD hide `0x00405150`, the HUD show `0x004052D0`, `0x004060B0`, the bar `0x004061F0` and `0x00406DD0` reach the window through it; 0 at construction (`0x00406C8D`) |
| `+0xC8` | `u32` | flags | bit `0x1`: bossgaugeopen asked for the gauge (`0x00405270`), and the tick builds the window while it is set (`0x00406B52`); bit `0x2`: the window is open, set by the tick with bit `0x1` cleared (`0x00406C68`-`0x00406C74`), after which the tick only refreshes the value table (`0x004050C0`, `0x00406B44`); bit `0x4`: the HUD hid the window (`0x00405150`), taken back by the HUD show (`0x004052EC`, `0x00405301`); bits `0x2` and `0x4` are cleared when the window goes (`0x004056F2`). Bit `0x8`: skip the full-values test once (`0x00406BC2`-`0x00406BCA`). Bit `0x10`: 1 at construction (`0x10`, `0x00406CA5`); passed to the new window as its creation argument (`0x00406B85`-`0x00406B9D`) unless an entry's value is below its maximum (`0x00406BD2`-`0x00406C0E`). Bit `0x20`: the bars' state from `0x00406DD0` (`0x00406DE0`, `0x00406E0D`). Bit `0x80`: the script pause mask, set and cleared by `0x00404D70` and `0x00404DC0` (`0x00404D9C`-`0x00404DAB`, `0x00404DEC`-`0x00404DFB`); while bit `0x40` or `0x80` is set, a bar that is not closing skips its frame from `0x004063B8` on (`0x0040639D`-`0x004063B2`) |
| `+0xCC` | `u8[4]` | pad0CC | read and written by no function; nothing fixes its width |
| `+0xD0` | `void*` | layoutRecord | the gauge's layout record, `0x0051EDC0`(3) (`0x00406CAF`-`0x00406CB4`): its byte `+0x24` is the picture count and its `+0x28` the picture list the construct message loads (`0x00406CC9`-`0x00406CDF`) |
| `+0xD8` | `void*` | pictures | the array of `+0xE0` picture handles the construct message allocates (`0x00393590`, `0x00406CFA`) and fills, one load (`0x0024A440`) for each list entry of type 1 and 0 for the others (`0x00406D17`-`0x00406D54`); message 18 releases each (`0x0024A680`) and frees the array (`0x00406AA6`-`0x00406B04`) |
| `+0xE0` | `u8` | pictureCount | the number of pictures, byte `+0x24` of the layout record (`0x00406CDF`); bounds the load and release loops (`0x00406D01`, `0x00406D58`, `0x00406AB8`, `0x00406AE7`) |
| `+0xE1` | `u8` | style | the bar style `0x00405100` picks from the boss's class, `0xFF` for no gauge (`0x00406BBC`; The boss gauge above); the tick passes it to the window and builds no window for `0xFF` (`0x00406B70`, `0x00406C13`); 0 at construction (`0x00406CC2`) |
| `+0xE2` | `u8` | pad0E2 | read and written by no function; nothing fixes its width |
| `+0xE3` | `u8` | entryCount | the entries in the value table `+0xE8`, the count `0x0031B690` returns on each draw (`0x00406B27`-`0x00406B33`) and on `0x004050C0`'s refresh (`0x004050EA`); 0 at construction (`0x00406C9E`); bossgaugeclose `0x00404E10` (`0x00404E69`), `0x00404F50` (`0x00404F71`, `0x00404FA1`), the window `0x00405310` (`0x004055F3`), the bar `0x004061F0` (`0x004062FC`) and `0x00407D10` (`0x00407D75`) read it |
| `+0xE4` | `u8[4]` | pad0E4 | read and written by no function; nothing fixes its width |
| `+0xE8` | `void*` | valueTable | the boss value table, `0x18` bytes an entry ({..., value `+0x08`, maximum `+0x0C`, ...}), whose address `0x0031B690` stores here through its argument (`0x0031B6B5`, `0x0031B72D`); `0x00404F50` returns its entries (`0x00404F81`, `0x00404FAE`), the tick tests each value against its maximum (`0x00406BE1`), bossgaugeclose (`0x00404E76`) and `0x00407D10` (`0x00407D7D`) read it; 0 at construction (`0x00406C94`) |

## State

For style 2 `0x00404F50` does not return a table entry: it copies value entry 0, the 24 bytes at `[[0x02B62D88] + 0xE8]`,
to `0x02B62D90` (`0x00405007`-`0x00405016`), rewrites its value and maximum for the bar asked, and returns `0x02B62D90`
(`0x004050A7`). The callers read `+0x08`, `+0x0C` and `+0x10` of the entry they get.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B62D90` | `u8[8]` | 0 | bytes `+0x00`-`+0x07` of that copy; no caller reads them | `0x00404F50` (`0x0040500A`) | no instruction |
| `0x02B62D98` | `i32` | 0 | `+0x08`, the value: for bar 0 the part inside the current cell, `(current x 51 - cells x max) / 51` rounded up (`0x00405023`-`0x00405054`); for bar 1 the width `cells x 6 - 2` (`0x0040508D`-`0x004050A1`) | `0x00404F50` (`0x0040500A`, `0x00405047`, `0x00405054`, `0x004050A1`) | through the returned address: `0x00405770` (`0x00405820`), `0x004061F0` (`0x00406479`, `0x004064A9`, `0x004064D9`), `0x00406770` (`0x00406817`), `0x00407D10` (`0x00407D98`) |
| `0x02B62D9C` | `i32` | 0 | `+0x0C`, the maximum: for bar 0 the maximum over 51 rounded up (`0x0040505A`-`0x00405086`), for bar 1 298 (`0x00405090`) | `0x00404F50` (`0x0040500A`, `0x00405072`, `0x00405086`, `0x00405090`) | through the returned address: `0x00405770` (`0x00405829`), `0x004061F0` (`0x004062E3`, `0x00406476`), `0x00407D10` (`0x00407D9C`) |
| `0x02B62DA0` | `u8[8]` | 0 | bytes `+0x10`-`+0x17` of the copy; the dword `+0x10` is read | `0x00404F50` (`0x00405016`) | through the returned address: `0x004061F0` (`0x004064A4`) |

The callers reach these cells only through the address `0x00404F50` returns, from its calls at `0x00405816`, `0x004062D9`,
`0x004063FA`, `0x004067C8` and `0x00407D8E`. No other instruction reaches them. `0x02B62D90` is taken only by `0x00404F50`, at
`0x0040507F` and `0x004050A7`.

The boss value table `0x02EC1380` holds two entries of `0x18` bytes: `+0x00` the unit's slot (`i32`), `+0x04` its
class (`u32`), then HP `+0x08`, max HP `+0x0C`, MP `+0x10` and max MP `+0x14`, each `i32` (`0x0031B690` sign-extends
MP and max MP from the stats record's `i16` words `+0x4C` and `+0x28`, `0x0031B6FD`-`0x0031B70F`).

The area-change step
`0x002342F0` resets both entries through `0x003221B0` (`0x00234428`): slot -1, every other word 0. `0x0031B690` walks the two
entries (`0x0031B6C0`-`0x0031B720`) and skips one whose class is 0. The one call of `0x00328FF0`, at `0x0023AA04`, registers
entry 0, and nothing else forms the table's address but the walker `0x0031B690` and the reset, so entry 1 keeps slot -1
and class 0.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EC1388` | `i32` | 0 (zero-filled tail of `.data`) | entry 0's HP; the reset's 8-byte store also zeroes max HP `0x02EC138C` | `0x003221B0` (`0x003221E0`); `0x0031B690` (`0x0031B6E7`) on its first pass, past the class test | `0x004061F0` (`0x00406479`, `0x004064A9`) through the entry address `0x00404F50` returns |
| `0x02EC1390` | `i32` | 0 (zero-filled tail of `.data`) | entry 0's MP; the reset's 8-byte store also zeroes max MP `0x02EC1394` | `0x003221B0` (`0x003221E7`); `0x0031B690` (`0x0031B701`) on its first pass, past the class test | `0x004061F0` (`0x004064A4`, when the bar's flag `+0x130` bit `0x4` is set) through the entry address `0x00404F50` returns |
| `0x02EC1398` | `i32` | 0 (zero-filled tail of `.data`) | entry 1's unit slot; -1 after each reset | `0x003221B0` (`0x003221B9`, the 8-byte 0 over `0x02EC1398`-`0x02EC139F`; `0x003221D6`, -1) | `0x0031B690` (`0x0031B6C5`) on its second pass, only when entry 1's class `0x02EC139C` is not 0; it passes the slot to `0x00236820` |
| `0x02EC13A0` | `i32` | 0 (zero-filled tail of `.data`) | entry 1's HP; the reset's 8-byte store also zeroes max HP `0x02EC13A4` | `0x003221B0` (`0x003221EE`); `0x0031B690` (`0x0031B6E7`) on its second pass, past the class test | `0x004061F0` (`0x00406479`, `0x004064A9`) through the entry address `0x00404F50` returns |
| `0x02EC13A8` | `i32` | 0 (zero-filled tail of `.data`) | entry 1's MP; the reset's 8-byte store also zeroes max MP `0x02EC13AC` | `0x003221B0` (`0x003221F5`); `0x0031B690` (`0x0031B701`) on its second pass, past the same class test | `0x004061F0` (`0x004064A4`) through the entry address `0x00404F50` returns (`0x00404F88`-`0x00404F8C`), when the bar's flag `+0x130` bit `0x4` is set |

## Modding notes

- The top command list is the six pairs at `0x00D10650`, or at `0x00D10660` while bit `0x800` of `[0x02EBF190] + 4` is
  set; reordering a table reorders the menu, and the two tables hold the same pairs.
- A command's label and help are words `+2` and `+0` of its battle command row.
- A new refusal reason needs a row in `0x0027C150` to show text.

## Related

- [Command availability](../Battle-Actions/command-availability.md) - which commands and actions are offered.
- [Target selection](../Battle-Actions/target-selection.md) - the menu's target lists and their builder.
- [Action phases](../Battle-Actions/action-phases.md) - what happens after an action is issued.
- [Menus](menus.md) - the router ids that open the menu.
- [Gambits screen](gambit-screen.md) - the same on/off switch for a member's gambits.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Items equipment shops license: `0x00236820` is called by `0x0031A300`; `0x00322C50` is called by `0x003096F0`, `0x0030B180`,
  `0x0030B4B0`, `0x0030B510`, `0x0030B570`, `0x0030B630`, `0x00317930`, `0x0031A510`, `0x00323910`, `0x00323C60`, `0x00323D10`,
  `0x00323EC0`; `0x00322C50` is also called by `0x00325F40`.
- Items equipment shops license: those functions are documented on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [stats](../Damage-And-Battle-Formulas/stats.md),
  [bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md).
- Items equipment shops license: and on [party table](../Party/party-table.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [quickening and esper list](../Battle-Actions/quickening-and-esper-list.md),
  [command availability](../Battle-Actions/command-availability.md).
- RNG random selection: `0x002342F0` calls `0x00328D80`; those functions are documented on
  [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md).
- Spawn encounter lifecycle: `0x002342F0` calls `0x00233780`, `0x00307090`; `0x00236820` is called by `0x00308D90`; those
  functions are documented on [enemy respawning](../Enemy-Spawning/enemy-respawning.md),
  [battle units](../Characters-And-Objects/battle-units.md).
- Status periodic terminal: `0x002342F0` calls `0x0030E990`; `0x00322C50` is called by `0x0030E130`, `0x0030FED0`, `0x00310DB0`;
  those functions are documented on [battle units](../Characters-And-Objects/battle-units.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- World area: `0x002342F0` is called by `0x00266D10`; `0x0024A680` is called by `0x003C63A0`; those functions are documented
  on [force fight mode](../Engine-Core/force-fight-mode.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
