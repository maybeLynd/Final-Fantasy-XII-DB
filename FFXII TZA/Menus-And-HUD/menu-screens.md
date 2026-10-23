---
title: "Menu screens: every menu widget procedure, the screen it belongs to, what installs it and the resources it loads"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00280DE0, 0x00281ED0, 0x0027FB70, 0x0027F5D0, 0x00254B50, 0x00280980, 0x00244F50, 0x00245000"
---

## What it lists

`menu-screens.tsv` has one row per widget procedure, 267 in all. They are every procedure the image passes to the
widget constructors `0x00244F50`, `0x00245000` and `0x002465F0` ([Widgets](widgets.md)): 299 construction sites, of which
296 load the procedure with a `lea` and three are the constructors' own calls and the forwarder `0x00564AC0`. Each
procedure is tied to a screen by walking its installers up to a Party Menu entry or a menu request.

### The Party Menu and its entries

The Party Menu is `0x00280DE0` ("Party Menu", `menu_command.bin` `0x554`, the control label at `0x00915DD0`), built by
`0x00280D20` for menu request 2 ([Menus](menus.md)). Its entry dispatcher `0x00281ED0` (`0x002811DC`) opens each entry by
its `menu_command.bin` id:

| Entry | Opener (site in `0x00281ED0`) | Screen procedure | Page |
|---|---|---|---|
| Party `0x4B3` | posts `0x8001` to its member list | `0x00280DE0`, list `0x00285290` | |
| Status `0x4B4`, Equip `0x4B6` | `0x002C2280` (`0x002822A9`) | `0x002C2320` | |
| Licenses `0x4B5` | `0x005601B0` (`0x002823C5`) | `0x00560910` | [License Board screen](license-board-screen.md) |
| World Map `0x4B7` | `0x0028E790` (`0x002823B8`) | `0x00552250` | [Map screens](map-screens.md) |
| Inventory `0x4B8` | `0x00565DD0` (`0x00282127`) | `0x00565E00` | [Widgets](widgets.md) |
| Gambits `0x4B9` | `0x00568B30` (`0x00282264`) | `0x005691E0` | [Gambits screen](gambit-screen.md) |
| Clan Primer `0x4BC` | `0x00574CB0` (`0x0028239B`) | `0x00574E80` | [Clan Primer](clan-primer.md) |
| Config `0x4BE` | `0x00240680` (`0x0028217D`) | `0x0023FBE0` | [Config screen](config-screen.md) |
| Graphics Settings `0x503` | `0x0023BCC0` (`0x00282186`) | `0x0023BD40` | [Config screen](config-screen.md) |
| Controls `0x504` | `0x0023CC90` (`0x0028218F`) | `0x0023CE10` | [Config screen](config-screen.md) |
| Quit `0x505` | `0x0027EBC0` (`0x00282196`) | `0x0027EA70` | |
| Parameter Settings `0x53A` | `0x00240D60` (`0x002821B8`) | `0x00240AD0` | |

Status and Equip share one screen procedure, `0x002C2320`, which hosts the equipment pane `0x003FF360`, its list
`0x003FDFE0` ("Change equipment.", `0xCC9`) and the slot names Weapon, Off-hand, Helm, Armor and Accessory
(`menu_expansion.bin` `0x4A99`, `0x4A9A`, `0x4A9C`-`0x4A9E`, `0x003FEE40`).

### Command rows and first visits

The Party Menu, the Status and Equip screen and the Inventory (`0x00565E00`) keep their command rows in a set
at `+0xD0`: an `i16` count and, at `+0x08`, `0x20`-byte rows that start with the row's id and hold its
widget at `+0x08`.

- `0x002CD440(set, id)` returns the row with the id, or null.
- `0x002C9F30(set, id, colour)` writes a colour to the widget's `+0xE4` for the row with the id, or row 0
  when none has it; `0x002C9F80` does the same but changes nothing then, and `0x002C9FD0(set, colour)`
  colours every row. `0x002C9F20(row, colour)` and `0x002C9E60(row)` write and read one row's colour, grey
  `0x80808080` when it has no widget.
- `0x002CA010(set, id, on)` sets or clears bit 1 of the widget's `+0xF0` for the row with the id, or for
  every row with id -1; `0x002CA0C0(row, on)` does the same with bit 2. `0x002CA0E0(row, dx, dy)` moves a
  row's widget by (dx, dy) and keeps the offset at `+0xEC`, `+0xEE`.

Entries and Inventory categories remember a first visit in a save-wide flag:

- `0x002CD920(id)` gives the flag of an entry id, `0x002CDE20(id)` answers whether it is set (`0x00252D10`; 1
  for an id without one) and `0x002CDE50(id, v)` writes it (`0x00252D40`).
- The entry dispatcher sets the flag when it opens an entry and then sets the row's bit 2 from it
  (`0x00282310`, `0x002CA0C0` at `0x00282329`); the Inventory does the same for its categories (`0x0056633C`,
  `0x00566354`).
- When the Party Menu meets an entry whose flag is clear (`0x00281127`), it shows the notice whose caption case
  `0x002CD8A0(id)` gives (`0x002CE2F0`, `0x0028113C`; [Dialogs](dialogs.md)).

| Entry (`menu_command.bin`) | Flag | Notice case |
|---|---|---|
| Party `0x4B3` | `0x29` | `0x10` |
| Status `0x4B4` | `0x2A` | `0x11` |
| Licenses `0x4B5` | `0x2C` | `0x13` |
| Equip `0x4B6` | `0x2B` | `0x12` |
| World Map `0x4B7` | `0x2E` | `0x15` |
| Inventory `0x4B8` | `0x2F` | `0x16` |
| Gambits `0x4B9` | `0x2D` | `0x14` |
| Clan Primer `0x4BC` | `0x31` | `0x17` |
| Config `0x4BE` | `0x33` | `0x10` |
| Weapons `0x405` | `0x38` | - |
| Armor `0x406`, Accessories `0x407` | `0x3A` | - |
| Ammunition `0x408` | `0x39` | - |
| Items `0x409` | `0x35` | - |
| Abilities `0x40D` | `0x34` | - |
| Loot `0x40E` | `0x37` | - |
| Key Items `0x40F` | `0x36` | - |

On the Status and Equip screen, `0x002C2200(member)` and `0x002C2240(member)` step to the previous or next
member: `0x0027ED10` and `0x0027F360` walk the nine member slots at `[0x0209AC30] + 0xAC8` from the current one
`+0xDE0`, skipping empty slots (`+0x60` below 0) and, while `+0xD3C` bit `0x10` is set, slots with flag bit 1
or `+0x60` of 6 or more. On a move they play sound `0x51` (`0x00249C60`) and refresh the screen (`0x002C2C50`).

The menu state block `[0x0209AC30]` is set up by `0x002800F0`, from `0x00253970`, which points it at `0x0209AC60` and
clears its `0xE00` bytes once. `0x00282EA0(slot)` gives the index, 0 to 8, of the `0xC0`-byte party record from
`+0x408` that member slot `slot` (`+0xAC8`) points at, or 0; fifteen description and row builders call it.

`0x002845E0(row, record)`, from `0x00283E40`, lays out a member-list row for a party record:

- it places the row by the panel's `+0xFC` bit 3, at alpha `0x80` with the bit and `0x58` without, and hides it
  for a record whose position `+0x60` is negative;
- it orders it by `(0x2F - position) x 2` (`0x00247930`) and takes its frame from the position clamped to 0-15
  by `0x002C9BD0`, which the license screens `0x00558CE0` and `0x005618E0` also use;
- it shows its marks from the record's flags `+0x00` bits 1 and 17 and `+0x44` bits 0, 1 and 31 (colour 4 when
  any is set) and from the panel's `+0xFC` bits 4 and 5.

`0x002847C0(row)`, from `0x002C1FF0`, narrows nodes 0, 1, 2, 3 and 5 of a row to 0.75 of their authored widths
(`0x00254A00` returns 0.75, and its `0x002DDC50` test always holds), node 5 by 2 more, and moves nodes 1 and 2 left by
the width the nodes before them gave up.

`0x002C98F0(i, frames)` closes slot i's two widgets (`+0x2C8`, `+0x2B8`), first giving them a closing run of
`frames` when that is above 0, and also the widget `[0x0209C318]`; `0x002C98C0(frames)` runs it for slot 0 and
closes `+0x280`. `0x0027F1A0(row, id)` fills a 32-byte slot row for an equipment id: the name (`0x002B58B0`), the
icon byte `+0x2C` and the class `+0x38`, all zero for `0xFFFF`; the equipment pane's `0x003FEE40` uses it.

### The member-record panel

The panel `0x002CBF80`, built by `0x002CBED0` under Status and Equip, `0x002CBE40` under the gambit screen and
`0x002CBDA0` under the shop, shows a party member against a chosen piece or ability:

- `0x002CA7C0(..., row, panel, id)`, run by `0x002CC4F0`, handles an equipment id: it builds the member's stats as
  they are and with the piece in its slot (`0x0030A4E0`), marks the panel when the piece is the one worn
  (`+0xE0`), passes whether it can be worn (`0x00317B70`) to `0x002CB360` and `0x002CA5D0`, and shows the differences
  with `0x002CC780`.
- It shows one difference for a weapon (group 1) and two for a shield or armour (groups 2 and 3), and none for
  ammunition or classes 21 and 22. For a magick, technick or gambit (classes 8, 9, 11, 12) it fades the row
  toward `0x20` instead.
- `0x002CC780(nodes, delta, ...)` writes a difference: the number's absolute value in colour 4 when it is above
  0 and 5 otherwise, and for a non-zero difference a second node (`0x0029CCF0`, given the sign) placed by the
  number of digits.
- `0x002CB1F0(..., panel, id)` shows the stat labels for an equipment id: text `0x4A90` for a weapon other than
  ammunition, `0x4A93` and `0x4A94` for a shield, `0x4A91` and `0x4A92` for armour other than classes 21 and 22.
- `0x002CAFE0(panel, n, step, mode, keep)` hides the panel's four arrow nodes; when the panel is shown (`+0x40`
  bit 0), n is above 1 and `+0xF0` bit 1 is clear, it shows one pair, chosen by `+0xF0` bit 0, in colour 2 for
  mode 1 and 0 otherwise. Without `keep` it places them (n - 1) x step to the left.
- `0x002CA3B0(panel, node, target, curve, ms)` starts a fade of a node's brightness `+0x3B` toward `target`,
  with the start time from `0x0208F570`; `0x002CA2E0(panel)`, the step that `0x002CA6C0` and `0x002CB4B0` run, advances
  it through `0x00248F40` and writes the brightness into the node's four vertex colours.

The comparison `0x0030A4E0` also returns a warning code, which the Equip screen turns into its help-window warnings
("Equipping a shield will remove your two-handed weapon." and the others); every code, its condition and its line
are on [Stats](../Damage-And-Battle-Formulas/stats.md#the-equipment-comparisons-warnings).

### The Equip screen's stat panel

The Equip screen's stat panel lists Attack Power, Defense, Magick Resist, Evade, Magick Evade, Strength, Magick
Power, Vitality and Speed, each as worn and, when it changes, with the highlighted piece. `0x003FE410(opener)` builds
it once as a `0x118`-byte widget with procedure `0x003FE5D0` and keeps it at `[0x0209AC30] + 0x138` (`0x003FE44B`-`0x003FE466`);
Status and Equip passes 1 (`0x002C24BA`) and the shop 0 (`0x0057AD55`). Message 18 clears the pointer (`0x003FE60E`).

`EquipStatPanel` (`0x118` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header (widgets.md) |
| `+0x0C0` | `void*` | rows | the row list; message 1 gives it the row painter `0x003FE490` at its +`0x120` and this panel at its +`0xD8` (`0x003FE690`-`0x003FE6B8`) |
| `+0x0C8` | `i32[9]` | current | the nine values as worn, in row order |
| `+0x0EC` | `i32[9]` | preview | the nine values with the highlighted piece |
| `+0x110` | `u16` | opener | `0x003FE410`'s argument, stored by message 1 (`0x003FE689`) |
| `+0x112` | `u8[2]` | gap112 | read and written by none of the panel's functions |
| `+0x114` | `u32` | flags | bit 0: the current numbers in colour 2, otherwise colour 0 (`0x003FE521`) |

The refreshers fill both rows from two comparisons, as worn and with the candidate set (`0x003FE8C0`-`0x003FE9D6`,
`0x003FEB90`-`0x003FECA6`). Row i takes stats byte `+0x0A`, `+0x0B`, `+0x0C`, `+0x11`, `+0x12`, `+0x06`, `+0x07`, `+0x08`
or `+0x09` of the comparison's block ([Stats](../Damage-And-Battle-Formulas/stats.md)).

`0x003FEAD0(candidate)` refreshes for
a candidate set, or with none shows the worn set in both rows; `0x003FE720(mode, slot)` builds the candidate for
mode `0x401` (every slot empty), `0x402` (the Optimise set, `0x002F9F20`) and `0x404` (the worn set, the five
words at the menu block's `+0xD48` 32 bytes apart, with `slot` emptied) (`0x003FE73C`-`0x003FE852`). Any other mode,
`0x403` included, refreshes with no candidate, the worn set in both rows (`0x003FE751`, `0x003FE7E6`). The callers pass
their message id as the mode (`0x002C2917`, `0x002C2D4F`).

The row painter `0x003FE490(panel, nodes, ..., i)` draws row i:

- the name, text `0x4A90 + i` (`0x003FE4D2`);
- the current value with number format `0x4B33` for rows 0-4 and `0x4B32` for rows 5-8 (`0x003FE4AE`-`0x003FE4C4`);
- the preview only when it differs, in colour 5 when it is at least the current value and 4 when lower
  (`0x003FE53C`-`0x003FE576`).

The same refreshers write max HP and max MP, as `i16` values, to the widget at `[[0x0209AC30] + 0x130] + 0xC0`:
the previewed and current max HP at `+0xF0` and `+0xF2`, the previewed and current max MP at `+0xF4` and `+0xF6`,
each pair 0 when the two are equal (`0x003FEA26`-`0x003FEAAA`).

### Screens opened by menu requests

The generic request host `0x0027FB70` (built by `0x00280A00` for the router `0x00254B50`, `0x00254C39`) and its dispatcher
`0x0027F5D0` open the rest. The field's input arbiter `0x00253C70` hands a button's menu request to that router
(`0x002540D2`, `0x002541C7`; [Controls](../Controls-And-Input/controls.md)), and `0x002E09A0` does too (`0x002E0D0B`):

| Screen | Procedure | Opened through |
|---|---|---|
| Party Menu | `0x00280DE0` | `0x00280D20` (`0x0027FCAE`) |
| shop: Buy, Sell, Bazaar | `0x0057B890` | `0x0057B800` (`0x0027FCDA`); [Shop screens](shop-screens.md) |
| game over | `0x003EF830` | `0x003EF750` (`0x0027FFC3`) |
| the script menu host | `0x002D70F0` | `0x002D7070` (`0x0027FE8C`) |
| Save, Load (`menu_message.bin` `0x870`, `0x871`) | `0x00582860` | `0x00583930` (`0x0027F984`) |
| the notice board list | `0x0037E350` | `0x0037FF80` (`0x0027F9AF`) |
| World Map | `0x00552250` | `0x0028E790` (`0x0027FA2C`) |
| location map | `0x002BA700` | `0x0028E660` (`0x0027F6AF`, `0x0027F9EC`) |
| Battle Menu (`0x553`) | `0x00279E20` | `0x00276650`, from the HUD frame (`0x00290DC0`); [Battle menu](battle-menu.md) |
| the special-attack window | `0x002D5EB0` | `0x002D5030`, from `0x0028E970` (`0x00254C18`) |
| party leader choice, "Select a new party leader." (`0x86E`) | `0x0035D6B0` | `0x0035D080` (`0x00254C26`) |

`0x0035D6B0` keeps itself in `0x022CA428` and sets `+0xC0` to `0x18` when it opens. Each step message (2) on which
`0x001EDEC0(+0xB4)` answers nonzero counts `+0xC0` down; at 0 it calls `0x0035C660` once, which opens the question
box (`0x00241C90`, flags `0x4FB`, root `[0x0208EA28]`) with text `0x86E` "Select a new party leader." in mode 3 of
`0x02092730` and `0x86F` "All members of the party have fallen. ..." in any other. A `0x8100` answer closes the
window (`0x00244F00`).

### The special-attack window

The special-attack window `0x002D5EB0` shows one party member's entry (status record `0x0035BB20(+0x140)`) from a
table of 24-byte entries:

- `0x002D5280(window, entries, n, step)` finds the member's entry by its handle, keeps it at `+0x150`, picks the
  current choice among its `+0x12` choices (`+0x06` words), sets `+0x142` bit 2 from the entry's `+0x14` unless
  `step` is given, and shows the choice's action name (class `0x14`, `0x002B58B0`) in node 1; `0x002D54B0(window,
  action)` shows a given action's name there.
- `0x002D5170(window, kind, plain)` builds the title at `+0xC0`: text `0x4669`, `0x466A` or `0x466C` by kind, or
  `0x46B4` with `+0x142` bit 2 or `plain`, followed by the member's name (`0x00296600`).
- `0x002D53F0(window, value, max)` writes value x 100 into node 1 (`0x0029F6E0`, grey `0x80808080`) and gives node
  0's gauge value x 100 / max (`0x00225580`), 0 for a max of 0.
- On opening (message 1, `0x002D5F30`) the time `+0x740` and its maximum `+0x744` both take the value `0x00309E40`
  stores: `0x022C2188 = min(4.0, 0x022C2184 + (0x022C2188 - 0x022C2184) x 0.5)` (`0x002F8B90`). `0x0030D720` sets both
  globals to 4.0, and `0x0030DB70` writes `0x022C2184` (`0x0030DC8B`). Each message 2 takes 1/30 off `+0x740`; at 0 the
  window plays sound `0x5B`, calls `0x0030DB70(0, 0)` and closes (`0x00244DD0`).
- `0x002D5500(window, n)` shows the first n of three marks in the child list of node 2, and `0x002D5C30(window)`
  runs it with the entry's count `+0x13`.
- The child `0x0028B860`, built by `0x002899A0` under the window, takes its box from the HUD sprite set
  (`0x0035D460()`) on message 1. On message 2, 90 frames after the time `+0xC0` that message 6 stamps, it
  closes (`0x00244DD0`, or `0x00245020` with `+0xC4` bit 1), unless message 15 has set `+0xC4` bit 0.
- Its draw (message 4) takes `t = min(frame - +0xC0, 90) x 256 / 90` and reads the four-key track `0x00915E10` at
  `t` with `0x00271AB0` ([Party list](party-list.md)): the widget's `+0x5A` takes the key byte `+7`, `+0x58` the byte
  `+6` `>> 1`, and the key field `+10` is the `s` with which `0x0028B700` draws the set's piece `+0x88` at
  `(+0x9C >> 1, +0x9E >> 1)` (`0x0028B9A3`-`0x0028BA59`).
- While `t >= 16` the draw draws the piece again with `s` from the track at `t - 16` (`0x0028BA5E`-`0x0028BAB9`).
- `0x0028B700(draw, set, piece, x, y, s)` draws a piece one source row at a time, centred on `x` and starting
  half the piece's height above `y`. Each row is one pixel high and its half width alternates between
  `w - (w x s >> 8)` and `w + (w x s >> 8)`, with `w` half the piece's width; `0x002D8C80` draws each row.
  It first sets the draw's palette byte `+0x5C` from the set's table and the piece's byte `+7`.
- `0x002D50B0(window, keep)` closes every row widget (`0x158` bytes from `+0x180`, `+0x748` of them) except row
  `keep`, which is marked to stay, and then the window (`0x00244DD0`).

### Screens and their procedures

| Screen | Procedures |
|---:|---:|
| Party Menu | 11 |
| Status and Equip | 10 |
| Licenses | 17 |
| World Map | 7 |
| Inventory | 5 |
| Gambits | 5 |
| Clan Primer, with its Hunts and Sky Pirate's Den pages | 19, 5 and 3 |
| Config, Graphics Settings, Controls | 10, 3 and 3 |
| Quit, Parameter Settings | 1 each |
| Battle Menu | 6 |
| Save and Load | 11 |
| shop | 6 |
| location map, map overlay | 7 and 3 |
| party leader choice | 1 |
| game over, special-attack window, notice board list | 5, 4 and 1 |

144 procedures belong to a screen. The other 123 belong to none: the field HUD and its children (root `0x00253780`),
the party HP and MP list, the help line and target window, the message windows, the shared dialogs, list rows, the
title screen, the logos, the screen mask, the NG signal and the shared backgrounds and captions. Several are shared by
many screens, for example the list item `0x00292390` (11 owners) and the layout item `0x0029E7D0`, which the layout decoder
`0x002432B0` installs for every screen.

### Resources

A procedure's layout comes from `mrppack_ys.bin`: `0x00280980` relocates its 23 units into `[0x0209AC30] + 8 x unit`
(`0x00280980`-`0x002809DE`), and `0x002432B0` reads a record of a unit. The table gives layouts as unit and record. Files are
named from the resource path table `0x01EC73A0`, and images by the label the code passes to `0x0024A5A0`.

Some screens also load text groups ([Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).
`0x002F8040(g)` answers whether group g is resident (`0x02EC3D80`). The gambit editor's `0x00292210` adds groups 10 and 16
to its resource batch when they are not (`0x002491B0`), and `0x002922F0`, run by the gambit editor (`0x00569236`), the Inventory (`0x00566217`), the
shop (`0x0057BC88`) and `0x00560910` (`0x0056098E`), releases each resident group through `0x002F83E0`: 17 unless `[0x02CA8F94]` is set, 10, 20 and 14
unless `[0x02CA96D4]` is set, and 16.

### The Quit and Parameter Settings pointers

Each opener creates its screen through `0x00244F50` only while its global is 0 and keeps the widget there; the screen
clears it when it is destroyed (message 18), and on leaving returns to the Party Menu on its entry (`0x002814E0`),
plays sound 3 and closes (`0x00244F00`). Both globals are 0 in the file. The Config, Graphics Settings and Controls
pointers are on [Config screen](config-screen.md).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209AC20` | `void*` | 0 | the open Quit screen, the `0xC0`-byte widget with procedure `0x0027EA70` | `0x0027EBC0` (`0x0027EC0B`); `0x0027EA70`, 0 on message 18 (`0x0027EA9E`) | `0x0027EBC0`, which creates it only while it is 0 (`0x0027EBD3`) and opens it (`0x00246AC0`, `0x0027EC1A`); `0x0027EA70`, which closes it after `0x002814E0(0x505)` (`0x0027EB4A`) |
| `0x0208E6C8` | `void*` | 0 | the open Parameter Settings screen, the `0xC8`-byte widget with procedure `0x00240AD0` | `0x00240D60` (`0x00240DAB`); `0x00240AD0`, 0 on message 18 (`0x00240B00`) | `0x00240D60`, which creates it only while it is 0 (`0x00240D73`) and opens it under the menu root `[0x0208EA28]` (`0x00246AD0`, `0x00240DBA`); `0x00240AD0`, which closes it after `0x002814E0(0x53A)` (`0x00240B5C`) |

No other instruction reaches either: no other RIP-relative, image-base-relative or 32-bit offset reference names them.

### The leader choice window

The party leader choice is the `0xC8`-byte widget at `0x022CA428` with procedure `0x0035D6B0`.

```struct LeaderChoiceWindow base=record size=0xC8
+0x00    u8[192]         header                 the widget header, written by the constructor 0x002465F0 (Widgets, The
                                                header); procedure 0x0035D6B0
+0xC0    i32             delay                  the steps left before the question opens: the construct message sets
                                                0x18 (0x0035D89C); each step message 2 on which 0x001EDEC0(+0xB4) answers
                                                non-zero lowers it while it is above 0 (0x0035D7D2-0x0035D7DE), and at 0
                                                the question opens (0x0035D7E4)
+0xC4    u32             flags                  bit 0: the question box is open, set after 0x0035C660 opens it
                                                (0x0035D7F1, 0x0035D808) so it opens once, cleared by the construct
                                                message (0x0035D895); bit 1: the field teardown 0x0035BB70 is closing the
                                                window (0x0035BBB1), and then message 18 skips its own restore of the
                                                menu state (0x0035D6FC)
```

## Columns

| Column | Meaning |
|---|---|
| `procedure` | the widget procedure |
| `size` | the procedure's code size in bytes |
| `installer` | the functions that construct it |
| `install site` | the `lea` of the procedure and the constructor call |
| `parent` | the widget procedures above the installer, `shared: n parents` for more than three, or `none (top)` |
| `screen` | the screen it belongs to, or `no screen` |
| `screen text id` | the shipped text that names that screen |
| `resources` | layout records (`mrppack_ys` unit and record), files and image labels it loads |
| `page` | the final page that documents it, if any |
| `role (from the body or a page)` | what the procedure does |

## Related

- [Menus](menus.md) - the requests and the router.
- [Widgets](widgets.md) - how the procedures are constructed.
- [Widget messages](widget-messages.md) - the messages they answer.
