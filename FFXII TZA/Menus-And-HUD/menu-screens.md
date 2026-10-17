---
title: "Menu screens: every menu widget procedure, the screen it belongs to, what installs it and the resources it loads"
kind: "reference"
category: "Menus and HUD"
addresses: "00280DE0, 00281ED0, 0027FB70, 0027F5D0, 00254B50, 00280980, 00244F50, 00245000"
---

## What it lists

`menu-screens.tsv` has one row per widget procedure, 267 in all. They are every procedure the image passes to the
widget constructors `00244F50`, `00245000` and `002465F0` ([Widgets](widgets.md)): 299 construction sites, of which
296 load the procedure with a `lea` and three are the constructors' own calls and the forwarder `00564AC0`. Each
procedure is tied to a screen by walking its installers up to a Party Menu entry or a menu request.

### The Party Menu and its entries

The Party Menu is `00280DE0` ("Party Menu", `menu_command.bin` `554`<sub>h</sub>, the control label at `00915DD0`), built by
`00280D20` for menu request 2 ([Menus](menus.md)). Its entry dispatcher `00281ED0` (`002811DC`) opens each entry by
its `menu_command.bin` id:

| Entry | Opener (site in `00281ED0`) | Screen procedure | Page |
|---|---|---|---|
| Party `4B3`<sub>h</sub> | posts `8001`<sub>h</sub> to its member list | `00280DE0`, list `00285290` | |
| Status `4B4`<sub>h</sub>, Equip `4B6`<sub>h</sub> | `002C2280` (`002822A9`) | `002C2320` | |
| Licenses `4B5`<sub>h</sub> | `005601B0` (`002823C5`) | `00560910` | [License Board screen](license-board-screen.md) |
| World Map `4B7`<sub>h</sub> | `0028E790` (`002823B8`) | `00552250` | [Map screens](map-screens.md) |
| Inventory `4B8`<sub>h</sub> | `00565DD0` (`00282127`) | `00565E00` | [Widgets](widgets.md) |
| Gambits `4B9`<sub>h</sub> | `00568B30` (`00282264`) | `005691E0` | [Gambits screen](gambit-screen.md) |
| Clan Primer `4BC`<sub>h</sub> | `00574CB0` (`0028239B`) | `00574E80` | [Clan Primer](clan-primer.md) |
| Config `4BE`<sub>h</sub> | `00240680` (`0028217D`) | `0023FBE0` | [Config screen](config-screen.md) |
| Graphics Settings `503`<sub>h</sub> | `0023BCC0` (`00282186`) | `0023BD40` | [Config screen](config-screen.md) |
| Controls `504`<sub>h</sub> | `0023CC90` (`0028218F`) | `0023CE10` | [Config screen](config-screen.md) |
| Quit `505`<sub>h</sub> | `0027EBC0` (`00282196`) | `0027EA70` | |
| Parameter Settings `53A`<sub>h</sub> | `00240D60` (`002821B8`) | `00240AD0` | |

Status and Equip share one screen procedure, `002C2320`, which hosts the equipment pane `003FF360`, its list
`003FDFE0` ("Change equipment.", `CC9`<sub>h</sub>) and the slot names Weapon, Off-hand, Helm, Armor and Accessory
(`menu_expansion.bin` `4A99`<sub>h</sub>, `4A9A`<sub>h</sub>, `4A9C`<sub>h</sub>-`4A9E`<sub>h</sub>, `003FEE40`).

### Command rows and first visits

The Party Menu, the Status and Equip screen and the Inventory (`00565E00`) keep their command rows in a set
at `+D0`<sub>h</sub>: an `i16` count and, at `+08`<sub>h</sub>, `20`<sub>h</sub>-byte rows that start with the row's id and hold its
widget at `+08`<sub>h</sub>.

- `002CD440(set, id)` returns the row with the id, or null.
- `002C9F30(set, id, colour)` writes a colour to the widget's `+E4`<sub>h</sub> for the row with the id, or row 0
  when none has it; `002C9F80` does the same but changes nothing then, and `002C9FD0(set, colour)`
  colours every row. `002C9F20(row, colour)` and `002C9E60(row)` write and read one row's colour, grey
  `80808080`<sub>h</sub> when it has no widget.
- `002CA010(set, id, on)` sets or clears bit 1 of the widget's `+F0`<sub>h</sub> for the row with the id, or for
  every row with id -1; `002CA0C0(row, on)` does the same with bit 2. `002CA0E0(row, dx, dy)` moves a
  row's widget by (dx, dy) and keeps the offset at `+EC`<sub>h</sub>, `+EE`<sub>h</sub>.

Entries and Inventory categories remember a first visit in a save-wide flag:

- `002CD920(id)` gives the flag of an entry id, `002CDE20(id)` answers whether it is set (`00252D10`; 1
  for an id without one) and `002CDE50(id, v)` writes it (`00252D40`).
- The entry dispatcher sets the flag when it opens an entry and then sets the row's bit 2 from it
  (`00282310`, `002CA0C0` at `00282329`); the Inventory does the same for its categories (`0056633C`,
  `00566354`).
- When the Party Menu meets an entry whose flag is clear (`00281127`), it shows the notice whose caption case
  `002CD8A0(id)` gives (`002CE2F0`, `0028113C`; [Dialogs](dialogs.md)).

| Entry (`menu_command.bin`) | Flag | Notice case |
|---|---|---|
| Party `4B3`<sub>h</sub> | `29`<sub>h</sub> | `10`<sub>h</sub> |
| Status `4B4`<sub>h</sub> | `2A`<sub>h</sub> | `11`<sub>h</sub> |
| Licenses `4B5`<sub>h</sub> | `2C`<sub>h</sub> | `13`<sub>h</sub> |
| Equip `4B6`<sub>h</sub> | `2B`<sub>h</sub> | `12`<sub>h</sub> |
| World Map `4B7`<sub>h</sub> | `2E`<sub>h</sub> | `15`<sub>h</sub> |
| Inventory `4B8`<sub>h</sub> | `2F`<sub>h</sub> | `16`<sub>h</sub> |
| Gambits `4B9`<sub>h</sub> | `2D`<sub>h</sub> | `14`<sub>h</sub> |
| Clan Primer `4BC`<sub>h</sub> | `31`<sub>h</sub> | `17`<sub>h</sub> |
| Config `4BE`<sub>h</sub> | `33`<sub>h</sub> | `10`<sub>h</sub> |
| Weapons `405`<sub>h</sub> | `38`<sub>h</sub> | - |
| Armor `406`<sub>h</sub>, Accessories `407`<sub>h</sub> | `3A`<sub>h</sub> | - |
| Ammunition `408`<sub>h</sub> | `39`<sub>h</sub> | - |
| Items `409`<sub>h</sub> | `35`<sub>h</sub> | - |
| Abilities `40D`<sub>h</sub> | `34`<sub>h</sub> | - |
| Loot `40E`<sub>h</sub> | `37`<sub>h</sub> | - |
| Key Items `40F`<sub>h</sub> | `36`<sub>h</sub> | - |

On the Status and Equip screen, `002C2200(member)` and `002C2240(member)` step to the previous or next
member: `0027ED10` and `0027F360` walk the nine member slots at `[0209AC30] + AC8h` from the current one
`+DE0`<sub>h</sub>, skipping empty slots (`+60`<sub>h</sub> below 0) and, while `+D3C`<sub>h</sub> bit `10`<sub>h</sub> is set, slots with flag bit 1
or `+60`<sub>h</sub> of 6 or more. On a move they play sound `51`<sub>h</sub> (`00249C60`) and refresh the screen (`002C2C50`).

The menu state block `[0209AC30]` is set up by `002800F0`, from `00253970`, which points it at `0209AC60` and
clears its `E00`<sub>h</sub> bytes once. `00282EA0(slot)` gives the index, 0 to 8, of the `C0`<sub>h</sub>-byte party record from
`+408`<sub>h</sub> that member slot `slot` (`+AC8`<sub>h</sub>) points at, or 0; fifteen description and row builders call it.

`002845E0(row, record)`, from `00283E40`, lays out a member-list row for a party record:

- it places the row by the panel's `+FC`<sub>h</sub> bit 3, at alpha `80`<sub>h</sub> with the bit and `58`<sub>h</sub> without, and hides it
  for a record whose position `+60`<sub>h</sub> is negative;
- it orders it by `(2Fh - position) x 2` (`00247930`) and takes its frame from the position clamped to 0-15
  by `002C9BD0`, which the license screens `00558CE0` and `005618E0` also use;
- it shows its marks from the record's flags `+00`<sub>h</sub> bits 1 and 17 and `+44`<sub>h</sub> bits 0, 1 and 31 (colour 4 when
  any is set) and from the panel's `+FC`<sub>h</sub> bits 4 and 5.

`002847C0(row)`, from `002C1FF0`, narrows nodes 0, 1, 2, 3 and 5 of a row to 0.75 of their authored widths
(`00254A00` returns 0.75, and its `002DDC50` test always holds), node 5 by 2 more, and moves nodes 1 and 2 left by
the width the nodes before them gave up.

`002C98F0(i, frames)` closes slot i's two widgets (`+2C8`<sub>h</sub>, `+2B8`<sub>h</sub>), first giving them a closing run of
`frames` when that is above 0, and also the widget `[0209C318]`; `002C98C0(frames)` runs it for slot 0 and
closes `+280`<sub>h</sub>. `0027F1A0(row, id)` fills a 32-byte slot row for an equipment id: the name (`002B58B0`), the
icon byte `+2C`<sub>h</sub> and the class `+38`<sub>h</sub>, all zero for `FFFF`<sub>h</sub>; the equipment pane's `003FEE40` uses it.

### The member-record panel

The panel `002CBF80`, built by `002CBED0` under Status and Equip, `002CBE40` under the gambit screen and
`002CBDA0` under the shop, shows a party member against a chosen piece or ability:

- `002CA7C0(..., row, panel, id)`, run by `002CC4F0`, handles an equipment id: it builds the member's stats as
  they are and with the piece in its slot (`0030A4E0`), marks the panel when the piece is the one worn
  (`+E0`<sub>h</sub>), passes whether it can be worn (`00317B70`) to `002CB360` and `002CA5D0`, and shows the differences
  with `002CC780`.
- It shows one difference for a weapon (group 1) and two for a shield or armour (groups 2 and 3), and none for
  ammunition or classes 21 and 22. For a magick, technick or gambit (classes 8, 9, 11, 12) it fades the row
  toward `20`<sub>h</sub> instead.
- `002CC780(nodes, delta, ...)` writes a difference: the number's absolute value in colour 4 when it is above
  0 and 5 otherwise, and for a non-zero difference a second node (`0029CCF0`, given the sign) placed by the
  number of digits.
- `002CB1F0(..., panel, id)` shows the stat labels for an equipment id: text `4A90`<sub>h</sub> for a weapon other than
  ammunition, `4A93`<sub>h</sub> and `4A94`<sub>h</sub> for a shield, `4A91`<sub>h</sub> and `4A92`<sub>h</sub> for armour other than classes 21 and 22.
- `002CAFE0(panel, n, step, mode, keep)` hides the panel's four arrow nodes; when the panel is shown (`+40`<sub>h</sub>
  bit 0), n is above 1 and `+F0`<sub>h</sub> bit 1 is clear, it shows one pair, chosen by `+F0`<sub>h</sub> bit 0, in colour 2 for
  mode 1 and 0 otherwise. Without `keep` it places them (n - 1) x step to the left.
- `002CA3B0(panel, node, target, curve, ms)` starts a fade of a node's brightness `+3B`<sub>h</sub> toward `target`,
  with the start time from `0208F570`; `002CA2E0(panel)`, the step that `002CA6C0` and `002CB4B0` run, advances
  it through `00248F40` and writes the brightness into the node's four vertex colours.

### Screens opened by menu requests

The generic request host `0027FB70` (built by `00280A00` for the router `00254B50`, `00254C39`) and its dispatcher
`0027F5D0` open the rest:

| Screen | Procedure | Opened through |
|---|---|---|
| Party Menu | `00280DE0` | `00280D20` (`0027FCAE`) |
| shop: Buy, Sell, Bazaar | `0057B890` | `0057B800` (`0027FCDA`); [Shop screens](shop-screens.md) |
| game over | `003EF830` | `003EF750` (`0027FFC3`) |
| the script menu host | `002D70F0` | `002D7070` (`0027FE8C`) |
| Save, Load (`menu_message.bin` `870`<sub>h</sub>, `871`<sub>h</sub>) | `00582860` | `00583930` (`0027F984`) |
| the notice board list | `0037E350` | `0037FF80` (`0027F9AF`) |
| World Map | `00552250` | `0028E790` (`0027FA2C`) |
| location map | `002BA700` | `0028E660` (`0027F6AF`, `0027F9EC`) |
| Battle Menu (`553`<sub>h</sub>) | `00279E20` | `00276650`, from the HUD frame (`00290DC0`); [Battle menu](battle-menu.md) |
| the special-attack window | `002D5EB0` | `002D5030`, from `0028E970` (`00254C18`) |
| party leader choice, "Select a new party leader." (`86E`<sub>h</sub>) | `0035D6B0` | `0035D080` (`00254C26`) |

`0035D6B0` keeps itself in `022CA428` and sets `+C0`<sub>h</sub> to `18`<sub>h</sub> when it opens. Each step message (2) on which
`001EDEC0(+B4h)` answers nonzero counts `+C0`<sub>h</sub> down; at 0 it calls `0035C660` once, which opens the question
box (`00241C90`, flags `4FB`<sub>h</sub>, root `[0208EA28]`) with text `86E`<sub>h</sub> "Select a new party leader." in mode 3 of
`02092730` and `86F`<sub>h</sub> "All members of the party have fallen. ..." in any other. A `8100`<sub>h</sub> answer closes the
window (`00244F00`).

### The special-attack window

The special-attack window `002D5EB0` shows one party member's entry (status record `0035BB20(+140h)`) from a
table of 24-byte entries:

- `002D5280(window, entries, n, step)` finds the member's entry by its handle, keeps it at `+150`<sub>h</sub>, picks the
  current choice among its `+12`<sub>h</sub> choices (`+06`<sub>h</sub> words), sets `+142`<sub>h</sub> bit 2 from the entry's `+14`<sub>h</sub> unless
  `step` is given, and shows the choice's action name (class `14`<sub>h</sub>, `002B58B0`) in node 1; `002D54B0(window,
  action)` shows a given action's name there.
- `002D5170(window, kind, plain)` builds the title at `+C0`<sub>h</sub>: text `4669`<sub>h</sub>, `466A`<sub>h</sub> or `466C`<sub>h</sub> by kind, or
  `46B4`<sub>h</sub> with `+142`<sub>h</sub> bit 2 or `plain`, followed by the member's name (`00296600`).
- `002D53F0(window, value, max)` writes value x 100 into node 1 (`0029F6E0`, grey `80808080`<sub>h</sub>) and gives node
  0's gauge value x 100 / max (`00225580`), 0 for a max of 0.
- `002D5500(window, n)` shows the first n of three marks in the child list of node 2, and `002D5C30(window)`
  runs it with the entry's count `+13`<sub>h</sub>.
- `002D50B0(window, keep)` closes every row widget (`158`<sub>h</sub> bytes from `+180`<sub>h</sub>, `+748`<sub>h</sub> of them) except row
  `keep`, which is marked to stay, and then the window (`00244DD0`).

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

144 procedures belong to a screen. The other 123 belong to none: the field HUD and its children (root `00253780`),
the party HP and MP list, the help line and target window, the message windows, the shared dialogs, list rows, the
title screen, the logos, the screen mask, the NG signal and the shared backgrounds and captions. Several are shared by
many screens, for example the list item `00292390` (11 owners) and the layout item `0029E7D0`, which the layout decoder
`002432B0` installs for every screen.

### Resources

A procedure's layout comes from `mrppack_ys.bin`: `00280980` relocates its 23 units into `[0209AC30] + 8 x unit`
(`00280980`-`002809DE`), and `002432B0` reads a record of a unit. The table gives layouts as unit and record. Files are
named from the resource path table `01EC73A0`, and images by the label the code passes to `0024A5A0`.

Some screens also load text groups ([Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).
`002F8040(g)` answers whether group g is resident (`02EC3D80`). The gambit editor's `00292210` adds groups 10 and 16
to its resource batch when they are not (`002491B0`), and `002922F0`, run by the gambit editor (`00569236`), the Inventory (`00566217`), the
shop (`0057BC88`) and `00560910` (`0056098E`), releases each resident group through `002F83E0`: 17 unless `[02CA8F94]` is set, 10, 20 and 14
unless `[02CA96D4]` is set, and 16.

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
