[Home](../../README.md) / [Menus and HUD](README.md) / Menu screen reference

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Menu screens: every menu widget procedure, the screen it belongs to, what installs it and the resources it loads | reference | Menus and HUD | How menus work | All 267 menu widget procedures in the game, found from every construction site: for each one its size, installer and install site, parent, the screen it belongs to with that screen's shipped name, the layout records and files it loads, and the final page that documents it; how the Party Menu entries and the request router reach each screen; the 123 procedures no single screen claims, listed in menu-screens.tsv; and the menu state block [0x0209AC30] field by field. | 0x00280DE0, 0x00281ED0, 0x0027FB70, 0x0027F5D0, 0x00254B50, 0x00280980, 0x00244F50, 0x00245000, 0x002800F0, 0x00283270, 0x0027F210 |

## What it lists

[`menu-screens.tsv`](menu-screens.tsv) has one row per widget procedure, 267 in all. They are every procedure the image passes to the
widget constructors `0x00244F50`, `0x00245000` and `0x002465F0` ([Widgets](widgets.md)): 299 construction sites, of which
296 load the procedure with a `lea` and three are the constructors' own calls and the forwarder `0x00564AC0`. Six of
the 296 calls are reached from two or four `lea` sites, so the `install site` column lists 306 `lea` sites. Each
procedure is tied to a screen by walking its installers up to a Party Menu entry or a menu request.

Of the rip-relative `lea` instructions in `.text`, 312 load one of the 267 procedures. The six that are not install
sites all load `0x005C5230` (`xor eax, eax; ret`), and none of them builds a widget:

- the constructor `0x002465F0` puts it in place of a null procedure¹;
- `0x002778C0` stores it at `+0x2D50` and `+0x2D90` of its object²;
- `0x005C51A0`, whose address is at `0x00D314D0`, returns it;
- `0x007A0180` registers it with `0x007A0090` as the handler of the console commands `MinFramerate` and `Expect`
 ³;
- `0x00808C90` passes it to `0x00862010`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024662E` |
| ² | `0x00277945` |
| ³ | `0x007A01D2`, `0x007A02AE` |
| ⁴ | `0x00808CF8` |

</details>

### The Party Menu and its entries

The Party Menu is `0x00280DE0` ("Party Menu", `menu_command.bin` `0x554`, the control label at `0x00915DD0`), built by
`0x00280D20` for menu request 2 ([Menus](menus.md)). Its entry dispatcher `0x00281ED0`¹ opens each entry by
its `menu_command.bin` id:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002811DC` |

</details>

| Entry | Opener (site in `0x00281ED0`) | Screen procedure | Page |
|---|---|---|---|
| Party `0x4B3` | posts `0x8001` to its member list | `0x00280DE0`, list `0x00285290` | |
| Status `0x4B4`, Equip `0x4B6` | `0x002C2280` (`0x002822A9`) | `0x002C2320` | |
| Licenses `0x4B5` | `0x005601B0` (`0x002823C5`) | `0x00560910` | [License Board screen](license-board-screen.md) |
| World Map `0x4B7` | `0x0028E790` (`0x002823B8`) | `0x00552250` | [Map screens](map-screens.md) |
| Inventory `0x4B8` | `0x00565DD0` (`0x00282127`) | `0x00565E00` | [Inventory screen](inventory-screen.md) |
| Gambits `0x4B9` | `0x00568B30` (`0x00282264`) | `0x005691E0` | [Gambits screen](gambit-screen.md) |
| Clan Primer `0x4BC` | `0x00574CB0` (`0x0028239B`) | `0x00574E80` | [Clan Primer](clan-primer.md) |
| Config `0x4BE` | `0x00240680` (`0x0028217D`) | `0x0023FBE0` | [Config screen](config-screen.md) |
| Graphics Settings `0x503` | `0x0023BCC0` (`0x00282186`) | `0x0023BD40` | [Config screen](config-screen.md) |
| Controls `0x504` | `0x0023CC90` (`0x0028218F`) | `0x0023CE10` | [Config screen](config-screen.md) |
| Quit `0x505` | `0x0027EBC0` (`0x00282196`) | `0x0027EA70` | |
| Parameter Settings `0x53A` | `0x00240D60` (`0x002821B8`) | `0x00240AD0` | |

Status and Equip share one screen procedure, `0x002C2320`. On Equip only¹ it hosts the
equipment pane `0x003FF360`, its list `0x003FDFE0` ("Change equipment.", `0xCC9`) and the slot names Weapon,
Off-hand, Helm, Armor and Accessory (`menu_expansion.bin` `0x4A99`, `0x4A9A`, `0x4A9C`-`0x4A9E`, `0x003FEE40`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002C25E9`-`0x002C267F` |

</details>

### Command rows and first visits

The Party Menu¹, the Status and Equip screen² and the Inventory³ keep their
command rows in a set, at `+0xD0` on the Party Menu and `+0xC0` on the other two: an `i16` count and, at `+0x08`, a
pointer to `0x20`-byte rows that start with the row's id and hold its widget at `+0x08`. The rows follow the set in
the screen.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00281AE0` |
| ² | `0x002C2320` |
| ³ | `0x00565E00` |

</details>

- `0x002CD440(set, id)` returns the row with the id, or null.
- `0x002C9F30(set, id, colour)` writes a colour to the widget's `+0xE4` for the row with the id, or row 0
  when no row has it; `0x002C9F80` does the same but changes nothing then, and `0x002C9FD0(set, colour)`
  colours every row. `0x002C9F20(row, colour)` and `0x002C9E60(row)` write and read one row's colour, grey
  `0x80808080` when it has no widget.
- `0x002CA010(set, id, on)` sets bit `0x2` of the widget's `+0xF0` when `on & 1` is set and clears it otherwise, for
  the row with the id (row 0 when no row has it), or for every row with id -1, and skips a row with no widget
 ¹; `0x002CA0C0(row, on)` does the same for one row with bit `0x4`².
  `0x002CA0E0(row, dx, dy)` moves a row's widget by (dx, dy) and keeps the offset at `+0xEC`, `+0xEE`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CA03C`, `0x002CA09E` |
| ² | `0x002CA0C7` |

</details>

Entries and Inventory categories remember a first visit in a save-wide flag:

- `0x002CD920(id)` gives the flag of an entry id, `0x002CDE20(id)` answers whether it is set (`0x00252D10`; 1
  for an id without one) and `0x002CDE50(id, v)` writes it¹.
- The entry dispatcher sets the flag when it opens an entry and then sets the row's bit `0x4` from it
  (`0x00282310`, `0x002CA0C0` at `0x00282329`); the Inventory does the same for its categories².
- When the Party Menu meets an entry whose flag is clear³, it shows the notice whose caption case
  `0x002CD8A0(id)` gives (`0x002CE2F0`, `0x0028113C`; [Dialogs](dialogs.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00252D40` |
| ² | `0x0056633C`, `0x00566354` |
| ³ | `0x00281127` |

</details>

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
`+0xDE0`, skipping empty slots (`+0x60` below 0) and, while `+0xD3C` bit `0x10` is set, slots with flag bit `0x2`
or `+0x60` of 6 or more. On a move they play sound `0x51`¹ and refresh the screen².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00249C60` |
| ² | `0x002C2C50` |

</details>

The menu state block `[0x0209AC30]` is set up by `0x002800F0`, from `0x00253970`, which points it at `0x0209AC60` and
clears its `0xE00` bytes once. `0x00282EA0(slot)` gives the index, 0 to 8, of the `0xC0`-byte party record from
`+0x408` that member slot `slot` (`+0xAC8`) points at, or 0; fifteen description and row builders call it.

`0x002845E0(row, record)`, from `0x00283E40`, lays out a member-list row for a party record:

- it places the row by the panel's `+0xFC` bit `0x8`, at alpha `0x80` with the bit and `0x58` without, and hides it
  for a record whose position `+0x60` is negative;
- it orders it by `(0x2F - position) x 2`¹ and takes its frame from the position clamped to 0-15
  by `0x002C9BD0`, which the license screens `0x00558CE0` and `0x005618E0` also use;
- it shows its marks from the record's flags `+0x00` bits `0x2` and `0x20000` and `+0x44` bits `0x1`, `0x2` and `0x80000000` (colour 4 when
  any is set) and from the panel's `+0xFC` bits `0x10` and `0x20`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00247930` |

</details>

`0x002847C0(row)`, from `0x002C1FF0`, narrows nodes 0, 1, 2, 3 and 5 of a row to 0.75 of their authored widths
(`0x00254A00` returns 0.75, and its `0x002DDC50` test always holds), node 5 by 2 more, and moves nodes 1 and 2 left by
the width the nodes before them gave up.

`0x002C98F0(i, frames)` closes slot i's two widgets (`+0x2C8`, `+0x2B8`), first giving them a closing run of
`frames` when that is above 0, and also the widget `[0x0209C318]`; `0x002C98C0(frames)` runs it for slot 0 and
closes `+0x280`. `0x0027F1A0(row, id)` fills a 32-byte slot row for an equipment id: the name¹, the
icon byte `+0x2C` and the class `+0x38`, all zero for `0xFFFF`; the equipment pane's `0x003FEE40` uses it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002B58B0` |

</details>

### The member-record panel

The panel `0x002CBF80`, built by `0x002CBED0` under Status and Equip, `0x002CBE40` under the gambit screen and
`0x002CBDA0` under the shop, shows a party member against a chosen piece or ability. It is a `0x170`-byte widget
kept at `[0x0209AC30] + 0x2E0`¹, and on message 1 it builds its parts²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CBF34`-`0x002CBF48` |
| ² | `0x002CC0A8`-`0x002CC20E` |

</details>

| Offset | Part | Size | Procedure |
|---|---|---:|---|
| `+0xC0` | the arrow strip | `0xF8` | `0x002CABF0` |
| `+0xC8` | the stat labels, made only when bit `0x1` of the build word is set (`0x002CC09D`) | `0xD0` | `0x002CB150` |
| `+0xD0`-`+0x117` | nine 8-byte pointers to the rows, row i at `+0xD0` + 8 x i | `0x110` | `0x002CA6C0` |
| `+0x118`-`+0x15F` | nine 8-byte pointers to the rows' difference widgets, row i's at `+0x118` + 8 x i, made only when bit `0x1` of the build word is set (`0x002CC10A`) | `0xE8` | `0x002CB4B0` |

The build word is `+0x10` of the parameter block that the construct message carries at `+8`¹, not a
word of the panel. Only the shop's builder sets its bit `0x1` (`0x002CBDC8` stores 7); the Status and Equip builder
stores `(screen == Status) << 3`² and the gambit editor stores 8³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CBFE7` |
| ² | `0x002C24BF`-`0x002C24CE`, `0x002CBF00`-`0x002CBF09` |
| ³ | `0x0056958E` |

</details>

So the stat labels, the nine difference widgets and `0x002CC4F0`, whose callers `0x0056D370`, `0x0056E5D0` and
`0x0057B1A0` are shop functions, belong to the shop's panel; under Status, Equip and the gambit screen the panel has
the rows and the arrow strip only.

- `0x002CA7C0(..., row, diff, id)`, run by `0x002CC4F0` for each of the nine rows with the row at `+0xD0 + 8 x i`
  and its difference widget at `+0x118 + 8 x i`¹, handles an equipment id:
  - it does nothing when the member record `0x00282DF0` returns for the row's `+0xD4` has a negative word `+0x60`
   ²;
  - it builds the member's stats as they are and with the piece in its slot³;
  - it marks the difference widget when the piece is the one worn (its `+0xE0`, `0x002CAA86`);
  - it passes whether the piece can be worn⁴ to `0x002CB360` with the difference widget and to
    `0x002CA5D0` with the row⁵;
  - it shows the differences with `0x002CC780`.
- It shows one difference for a weapon (group 1) and two for a shield or armour (groups 2 and 3), and 0 for
  ammunition or classes 21 and 22. For a magick, technick or gambit (classes 8, 9, 11, 12) it fades both toward
  `0x20` instead: the difference widget's node 11 through `0x002CB360` (`0x002CA994`-`0x002CA99B`; the target at
  `0x002CB424`, the start at `0x002CB43A`) and the row's node 0 by writing the row's fade record itself
 ⁶.
- `0x002CC780(nodes, delta, ...)` writes a difference: the number's absolute value in colour 4 when it is above
  0, 5 when it is below 0 and 0 when it is 0⁷, and for a non-zero difference a second
  node (`0x0029CCF0`, given the sign) placed by the number of digits.
- `0x002CB1F0(..., labels, id)`, given the stat labels at `+0xC8`⁸, shows them for an equipment id:
  text `0x4A90` for a weapon other than ammunition, `0x4A93` and `0x4A94` for a shield, `0x4A91` and `0x4A92`
  for armour other than classes 21 and 22.
- `0x002CAFE0(strip, n, step, mode, keep)` takes the arrow strip at `+0xC0` and, as n, the panel's byte
  `+0x168`⁹:
  - it hides the strip's four arrow nodes, the list at the strip's `+0x60`;
  - when the strip is shown (its `+0x40` bit `0x1`), n is above 1 and the strip's `+0xF0` bit `0x2` is clear, it shows
    one pair, chosen by `+0xF0` bit `0x1`, in colour 2 for mode 1 and 0 otherwise;
  - without `keep` it places the list's node 2 (n - 1) x step to the left of its base¹⁰
    and stores that offset, negated, in the strip's `+0xEE`¹¹.
- `0x002CA3B0(widget, node, target, curve, ms)` starts a fade of a node's brightness `+0x3B` toward `target`,
  with the start time from `0x0208F570`, and keeps the fade in the widget it is given (`+0xC0`-`+0xD0`): the
  difference widget at `0x002CA8F6` and `0x002CB43A`.
- The rows' fades use the same record, written in place without `0x002CA3B0`: past the member check¹²
  `0x002CA7C0` starts node 0 toward `0x80`¹³ and toward `0x20` as above, and `0x002CA5D0` starts
  node 0 toward `0x80`, or toward `0x20` when its flag is set or, with a non-zero mode, the member is not the current
  one¹⁴.
- Past the same check `0x002CA7C0` also starts the difference widget's node 11 toward `0x80`¹⁵.
- `0x002CA2E0(widget)`, the message-2 step of both the rows¹⁶ and the difference widgets
 ¹⁷, advances a widget's fade through `0x00248F40` and writes the brightness into the node's four
  vertex colours.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CC537`-`0x002CC565` |
| ² | `0x002CA7FA`-`0x002CA7FF` |
| ³ | `0x0030A4E0` |
| ⁴ | `0x00317B70` |
| ⁵ | `0x002CAA9C`-`0x002CAAB5` |
| ⁶ | `0x002CA9A0`-`0x002CA9F4` |
| ⁷ | `0x002CC7A4`-`0x002CC7CD` |
| ⁸ | `0x002CC51E` |
| ⁹ | `0x002CB831`-`0x002CB83F`, `0x002CB97B`-`0x002CB998`, `0x002CBA0F`-`0x002CBA1D`, `0x002CC460`-`0x002CC47A` |
| ¹⁰ | `0x002CB0FE`-`0x002CB111` |
| ¹¹ | `0x002CB0F7` |
| ¹² | `0x002CA7FF` |
| ¹³ | `0x002CA869`-`0x002CA8B2` |
| ¹⁴ | `0x002CA620`-`0x002CA6AC` |
| ¹⁵ | `0x002CA8E8`-`0x002CA8F6` |
| ¹⁶ | `0x002CA6FA` |
| ¹⁷ | `0x002CB4EE` |

</details>

The comparison `0x0030A4E0` also returns a warning code, which the Equip screen turns into its help-window warnings
("Equipping a shield will remove your two-handed weapon." and the others); every code, its condition and its line
are on [Stats](../Damage-And-Battle-Formulas/stats.md#the-equipment-comparisons-warnings).

The four objects' own fields, beyond the widget header ([Widgets](widgets.md)) and the parts listed above, are in
[`menu-screens-member-record-panel-accesses.tsv`](menu-screens-member-record-panel-accesses.tsv) beside this page, every access with the object it reaches (its
`object` column). The record is the `0x170` widget at `[0x0209AC30] + 0x2E0`:

`MemberRecordPanel` (`0x170` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header: the build takes its rect `+0x98`-`+0x9E` from the layout `0x002432B0` returns for the creation record's two words, with the header's `+0x50` passed by address (`0x002CBFD1`-`0x002CC02F`), and installs the animation descriptor `0x00916FA8` through `0x00247570` (`0x002CC036`-`0x002CC040`, the header's `+0x48`); a builder that finds a record already kept at [`0x0209AC30`] + `0x2E0` builds no panel and goes on only when that record's `+0x7C` bit `0x20` is set (`0x002CBE1A`, `0x002CBE9F`, `0x002CBF51`); message 18 clears the block's `+0x2E0` (`0x002CBFB3`-`0x002CBFBD`) |
| `+0x0C0` | `void*` | strip | the arrow strip (above); with bit `0x10000` of `+0x168` the build adds 8 to the strip's `+0x98` and 4 to its `+0x9A` and runs `0x00247870` on it (`0x002CC21D`-`0x002CC25C`) |
| `+0x0C8` | `void*` | labels | the stat labels (above), 0 outside the shop's panel; `0x002CC2A0` reads it at `0x002CC47F` |
| `+0x0D0` | `void*[9]` | rows | the nine rows (above); `0x002CB8D0` (`0x002CB901`-`0x002CB922`), `0x002CBA50` (`0x002CBA79`-`0x002CBAB0`), `0x002CBC50` (`0x002CBCC0`) and `0x002CC660` (`0x002CC6E0`) walk them |
| `+0x118` | `void*[9]` | differences | the nine difference widgets (above), 0 outside the shop's panel |
| `+0x160` | `i16` | rowX | row 0's `+0x98` and `+0x9C`, its x and width, copied at the build (`0x002CC185`-`0x002CC1E0`) |
| `+0x162` | `i16` | rowW |  |
| `+0x164` | `i16` | diffX | the same of difference widget 0, or of row 0 when there is no such widget (`0x002CC1A2`-`0x002CC1F0`); `0x002CC2A0` places the rows from `+0x164`/`+0x166` when bits `0xF0000` of `+0x168` are set, else from `+0x160`/`+0x162` (`0x002CC2BF`-`0x002CC300`) |
| `+0x166` | `i16` | diffW |  |
| `+0x168` | `u32` | flags | byte 0: the rows shown, zeroed and counted by `0x002CC2A0` (`0x002CC33E`, `0x002CC431`), the n `0x002CAFE0` takes (above), read by `0x002CBC50` and `0x002CC660` before they walk the rows (`0x002CBC7B`, `0x002CC68D`); bit `0x100`: the build counted at most one party slot whose stats record (`0x00282DF0`) has a non-negative `+0x60` word and, when the menu block's `+0xD3C` bit `0x10` is set, passes `0x00282FA0` (written as byte `+0x169`, `0x002CC12B`-`0x002CC155` and `0x002CC261`-`0x002CC26C`; tested at `0x002CC379` and by the strip at `0x002CAC3D`); bit `0x200`: a copy of bit `0x10000` (`0x002CC272`-`0x002CC280`); bits `0xF0000`: the creation block's byte `+0x0C`, the mode (`0x002CC045`-`0x002CC059`), also read as the word `+0x16A` by `0x002CC4F0` (`0x002CC513`, `0x002CC550`); bit `0x10000` also moves the strip (above); bit `0x20000` set by `0x002CB850` at `0x002CB86D` and cleared at `0x002CB87E`; bit `0x100000`: the block's `+0x10` bit `0x4` (`0x002CC065`-`0x002CC078`); bits `0x300000` tested by `0x002CBA50`, `0x002CC2A0` and `0x002CC4F0` (`0x002CBAA8`, `0x002CC37F`, `0x002CC574`); bits `0xC00000`: `0x002CC4F0` sets bit `0x400000` and clears bit `0x800000` when the item's class (the first dword of `0x0035D330`(1, id << 16)) is 8, 9, 11 or 12 and clears both otherwise (`0x002CC59E`-`0x002CC5D6`), only with bits `0x300000` set and an id other than `0xFFFF` (`0x002CC574`-`0x002CC592`); `0x002CC2A0` tests both at `0x002CC36D` |
| `+0x16C` | `u8[4]` | gap16C | reached by no instruction in the table |

The strip's own fields, from its procedure `0x002CABF0` (message 1 the build at `0x002CAEBC`, message 2 the tick at
`0x002CAD79`, message 3 the colour pulse at `0x002CAC95`, message 4 the draw at `0x002CAC2D`) and from `0x002CAFE0` (above):
`+0xEE` is written by `0x002CAFE0`¹ and read by the strip's tick², and `+0xF0` is read at
`0x002CB069`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CB0F7` |
| ² | `0x002CAE74` |

</details>

`MemberRecordStrip` (`0xF8` bytes, offsets from the start of the strip):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header; the build takes its rect `+0x98`-`+0x9E` from `0x002432B0` with 7 (`0x002CAEC3`-`0x002CAF19`) and gives nodes 2 and 3 the texts `0x466D` and `0x4670`, hidden (`0x002CAF29`-`0x002CAF70`); the record's build then moves the rect (above) |
| `+0xC0` | `u8[20]` | tween | a record of the WidgetFade shape below, stepped by the tick (`0x002CADEA`-`0x002CAE5A`) into `+0xE4`; the tick clears its bits `0x1`-`0x2` when the tween ends (`0x002CAE2D`); no other writer in the table |
| `+0xD8` | `void*` | panel | the record, from the creation message's `+0x10` (`0x002CAF7D`); the draw reads it and draws nothing while its `+0x168` bit `0x100` or `0x200` is set (`0x002CAC2D`-`0x002CAC47`) |
| `+0xE0` | `u32` | buildTick | the frame counter `0x0208F570` at the build (`0x002CAF8A`); the colour pulse feeds it to `0x002CC8D0` and paints nodes 0 to 3 with the result (`0x002CAC95`-`0x002CAD69`) |
| `+0xE4` | `i16` | x | row 0's `+0x98`, or difference widget 0's when the record's `+0x168` bits `0xF0000` are set (`0x002CAF90`-`0x002CAFB8`); the tween's result each tick (`0x002CAE5E`); the draw's x (`0x002CAC5E`) |
| `+0xE6` | `i16` | y | their `+0x9A` (`0x002CAFBF`-`0x002CAFC3`); the draw's y, plus one (`0x002CAC56`-`0x002CAC65`) |
| `+0xE8` | `i16` | push1 | 4 when the menu block's byte `+0xDE9` bit `0x2` is set, then one less each tick to 0 (`0x002CAD79`-`0x002CAD88`, `0x002CADD0`-`0x002CADD5`); subtracted from node 1's x (`0x002CAE7B`) |
| `+0xEA` | `i16` | push0 | the same for bit `0x1` (`0x002CAD8F`-`0x002CAD9E`, `0x002CADBD`-`0x002CADC2`); added to node 0's x (`0x002CAE9C`); the block's two bits are cleared once read (`0x002CADE3`) |
| `+0xEC` | `i16` | minus1 | -1 at the build (`0x002CAF73`-`0x002CAF76`); no read in the table |
| `+0xEE` | `i16` | offset | the list's node 2 offset, negated, stored by `0x002CAFE0` (`0x002CB0F7`) and added to node 1's x by the tick (`0x002CAE74`) |
| `+0xF0` | `u32` | arrowFlags | bit `0x1` which pair, bit `0x2` hides (above); read at `0x002CB069` |
| `+0xF4` | `u8[4]` | gapF4 | reached by no instruction in the table |

The tick also places the arrows: node 1 at its layout x (`[+0x60] + 8`, layout `+4`) plus `+0xEE` minus `+0xE8`, node 0
at its layout x plus `+0xEA`, both at their layout y¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CAE65`-`0x002CAEAB` |

</details>

A row and a difference widget keep their fade in one record at `+0xC0`, written by `0x002CA3B0` for the difference
widget and in place for the row (above):

`WidgetFade` (`0x14` bytes, offsets from the start of the row):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | fadeFlags | bit `0x1`: running, set by every starter and cleared with bit `0x2` when the fade ends (`0x002CA34B`); bits `0x4`-`0x20`: the curve `0x00248F40` takes ((flags >> 2) & `0xF`, `0x002CA310`-`0x002CA31E`), `0x002CA3B0`'s curve argument (`0x002CA3C7`-`0x002CA3E3`) or 1 from the rows' starters (`0x45` at `0x002CA87E`, `0x002CA9C0`, `0x002CA635`, `0x002CA664`); bit `0x40`: set by every starter; bits `0x2` and `0x80`: cleared by every starter (`0x002CA3B0` ANDs with `0xFFFFFF41` at `0x002CA3C7`, the rows' starters with `0xFFFFFF45` at `0x002CA876`, `0x002CA9B8`, `0x002CA62D` and `0x002CA65C`); bits `0x100` and above: kept by those masks, no write in the table |
| `+0x04` | `i16` | fadeFrom | the node's brightness `+0x3B` when the fade started (`0x002CA3EA`-`0x002CA3F2`, `0x002CA889`-`0x002CA890`) |
| `+0x06` | `i16` | fadeNode | the node's index in the widget's list `+0x60`: `0x002CA3B0`'s argument (`0x002CA3FA`), 11 for the difference widget (`0x002CA8CC`, `0x002CB3FA`); 0 for the row (`0x002CA89E`, `0x002CA9E0`, `0x002CA641`, `0x002CA670`) |
| `+0x08` | `i16` | fadeDelta | target minus fadeFrom (`0x002CA3EE`-`0x002CA402`, `0x002CA884`-`0x002CA897`) |
| `+0x0C` | `u32` | fadeFrames | the length in frames: `0x002CA3B0`'s ms argument times 60 over 1000 (`0x002CA3D6`, `0x002CA417`-`0x002CA428`); the rows' starters write 6 (`0x002CA8B2`, `0x002CA9F4`, `0x002CA6A2`) |
| `+0x10` | `u32` | fadeStart | the frame counter `0x0208F570` when the fade started (`0x002CA40A`-`0x002CA410`, `0x002CA8A6`-`0x002CA8AC`) |

`0x002CA2E0` runs while bit `0x1` or `0x2` is set: it asks `0x00248F40` for the progress of the frames since fadeStart over
fadeFrames with the curve¹; at 1.0² it writes fadeFrom + fadeDelta and clears bits
`0x1`-`0x2`³, otherwise fadeFrom + fadeDelta x progress⁴; the brightness
`b` goes to the node's `+0x3B` and to its four vertex colours `+0x28`-`+0x34` as the grey `b | b << 8 | b << 16` with
bit `0x80000000` set⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CA302`-`0x002CA32B` |
| ² | `0x01CEBBA8` |
| ³ | `0x002CA33B`-`0x002CA34B` |
| ⁴ | `0x002CA354`-`0x002CA37C` |
| ⁵ | `0x002CA37F`-`0x002CA39C` |

</details>

A row's fields beyond the header and the fade record:

`MemberRecordRow` (`0x110` bytes, offsets from the start of the row):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0D4` | `u32` | slot | the party slot, from the creation block's +8 (`0x002CA789`-`0x002CA78C`); `0x00282DF0`(slot) is the member's stats record (`0x002CA5EA`, `0x002CA7E2`, `0x002CA84D`, `0x002CA9A0`, `0x002CB913`, `0x002CBA93`, `0x002CBCC3`, `0x002CC359`, `0x002CC3C4`, `0x002CC6E3`) |
| `+0x0D8` | `char[16]` | numText1 | the first difference's number as text, which `0x002CC780` writes through `0x0029FF60` and the number node's `+0x18` points at (`0x002CAB31`, `0x002CAB90`; `0x002A0030`) |
| `+0x0E8` | `char[16]` | numText2 | the second's (`0x002CAB5E`) |
| `+0x0F8` | `char[8]` | signText1 | the first difference's sign text, "ex00" and "+" or "-" (`0x00365668`-`0x00365690` through `0x0029CCF0`), which the sign node's `+0x18` points at (`0x002CAB1D`, `0x002CAB85`; `0x002CC864`-`0x002CC86B`) |
| `+0x100` | `char[8]` | signText2 | the second's (`0x002CAB4A`) |
| `+0x108` | `void*` | panel | the record, from the creation block's `+0x10` (`0x002CA792`-`0x002CA796`); on message 2 the row clears its `+0x50` bit `0x1` when the record's `+0x168` bit `0x10000` is set and sets it otherwise (`0x002CA6FF`-`0x002CA723`) |

The row's build (message 1, `0x002CA734`-`0x002CA7A9`) takes its rect from `0x002432B0` with 6, like the record's, and clears
`+0x50` bit `0x1` when the record's bit `0x10000` is set.

A difference widget's fields beyond the header and the fade record:

`MemberRecordDifference` (`0xE8` bytes, offsets from the start of the difference):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xD4` | `u32` | slot | the party slot, from the creation block's +8 (`0x002CB660`-`0x002CB663`; read at `0x002CA8BC`, `0x002CB37A`, `0x002CBAD2`) |
| `+0xD8` | `void*` | panel | the record, from the block's `+0x10` (`0x002CB669`-`0x002CB66D`; read at `0x002CB4F3`) |
| `+0xE0` | `u32` | worn | 1 when the piece is the one worn, else 0 (above; `0x002CA824`, `0x002CAA86`, `0x002CAA93`); its bit `0x1` is copied into the shown bit of nodes 16 and 10 (`0x002CA8FF`-`0x002CA92F`, `0x002CB443`-`0x002CB46F`) and tested at `0x002CB3C9` |
| `+0xE4` | `u32` | bright | 1 when node 11 fades toward `0x80` (`0x002CA8EB`, `0x002CB42A`), 0 toward `0x20` (`0x002CB41D`); on message 2 its bit `0x1` is copied into the shown bit of nodes 0 to 8 (`0x002CB52B`-`0x002CB5FB`) |

On message 1¹ the difference widget takes its rect from `0x002432B0` with 9, stores slot and panel,
and when the record's `+0x168` bits `0xF0000` are set sets its `+0x50` bit `0x1`, shows node 11 and nodes 0 to 8 and hides
node 16; with the bits clear it clears `+0x50` bit `0x1`. On message 2 it steps its fade² and then does the
same `+0x50` choice³, shows node 11 and copies `+0xE4` into nodes 0 to 8.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CB60B`-`0x002CB70F` |
| ² | `0x002CB4EE` |
| ³ | `0x002CB4F3`-`0x002CB517` |

</details>

### The Equip screen's stat panel

The Equip screen's stat panel lists Attack Power, Defense, Magick Resist, Evade, Magick Evade, Strength, Magick
Power, Vitality and Speed, each as worn and, when it changes, with the highlighted piece. `0x003FE410(opener)` builds
it once as a `0x118`-byte widget with procedure `0x003FE5D0` and keeps it at `[0x0209AC30] + 0x138`¹;
Status and Equip passes 1² and the shop 0³. Message 18 clears the pointer⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FE44B`-`0x003FE466` |
| ² | `0x002C24BA` |
| ³ | `0x0057AD55` |
| ⁴ | `0x003FE60E` |

</details>

`EquipStatPanel` (`0x118` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header (widgets.md) |
| `+0x0C0` | `void*` | rows | the row list; message 1 gives it the row painter `0x003FE490` at its `+0x120` and this panel at its `+0xD8` (`0x003FE690`-`0x003FE6B8`) |
| `+0x0C8` | `i32[9]` | current | the nine values as worn, in row order |
| `+0x0EC` | `i32[9]` | preview | the nine values with the highlighted piece |
| `+0x110` | `u16` | opener | `0x003FE410`'s argument, stored by message 1 (`0x003FE689`) |
| `+0x112` | `u8[2]` | gap112 | read and written by none of the panel's functions |
| `+0x114` | `u32` | flags | bit `0x1`: the current numbers in colour 2, otherwise colour 0 (`0x003FE521`) |

The refreshers fill both rows from two comparisons, as worn and with the candidate set¹. Row i takes stats byte `+0x0A`, `+0x0B`, `+0x0C`, `+0x11`, `+0x12`, `+0x06`, `+0x07`, `+0x08`
or `+0x09` of the comparison's block ([Stats](../Damage-And-Battle-Formulas/stats.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FE8C0`-`0x003FE9D6`, `0x003FEB90`-`0x003FECA6` |

</details>

`0x003FEAD0(candidate)` refreshes for
a candidate set, or with no candidate shows the worn set in both rows; `0x003FE720(mode, slot)` builds the candidate for
mode `0x401` (every slot empty), `0x402` (the Optimise set, `0x002F9F20`) and `0x404` (the worn set, the five
words at the menu block's `+0xD48` 32 bytes apart, with `slot` emptied)¹. Any other mode,
`0x403` included, refreshes with no candidate, the worn set in both rows². The callers pass
their message id as the mode³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FE73C`-`0x003FE852` |
| ² | `0x003FE751`, `0x003FE7E6` |
| ³ | `0x002C2917`, `0x002C2D4F` |

</details>

The row painter `0x003FE490(panel, nodes, ..., i)` draws row i:

- the name, text `0x4A90 + i`¹;
- the current value with number format `0x4B33` for rows 0-4 and `0x4B32` for rows 5-8²;
- the preview only when it differs, in colour 5 when it is at least the current value and 4 when lower
 ³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FE4D2` |
| ² | `0x003FE4AE`-`0x003FE4C4` |
| ³ | `0x003FE53C`-`0x003FE576` |

</details>

The same refreshers write max HP and max MP, as `i16` values, to the widget at `[[0x0209AC30] + 0x130] + 0xC0`:
the previewed and current max HP at `+0xF0` and `+0xF2`, the previewed and current max MP at `+0xF4` and `+0xF6`,
each pair 0 when the two are equal¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FEA26`-`0x003FEAAA` |

</details>

### Screens opened by menu requests

The generic request host `0x0027FB70` (built by `0x00280A00` for the router `0x00254B50`, `0x00254C39`) and its dispatcher
`0x0027F5D0` open the rest. The field's input arbiter `0x00253C70` hands a button's menu request to that router
(`0x002540D2`, `0x002541C7`; [Controls](../Controls-And-Input/controls.md)), and `0x002E09A0` does too¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E0D0B` |

</details>

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

`0x0035D6B0` keeps itself in `0x022CA428` and sets `+0xC0` to `0x18` when it opens (message 1); message 18 clears
`0x022CA428`¹. Each step message (2) on which
`0x001EDEC0(+0xB4)` answers nonzero counts `+0xC0` down; at 0 it calls `0x0035C660` once, which opens the question
box (`0x00241C90`, flags `0x4FB`, root `[0x0208EA28]`) with text `0x86E` "Select a new party leader." in mode 3 of
`0x02092730` and `0x86F` "All members of the party have fallen. ..." in any other. A `0x8100` answer closes the
window².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035D703` |
| ² | `0x00244F00` |

</details>

### The special-attack window

The special-attack window `0x002D5EB0` lists up to four party members, each in a row widget (procedure `0x002D5C80`;
`+0x748` of them, `0x158` bytes each from `+0x180`) that shows the member's entry (status record
`0x0035BB20(row word +0x140)`, the member the row was created for) from a table of 24-byte entries:

- `0x002D5280(window, entries, n, step)` finds the member's entry by its handle, keeps it at `+0x150`, picks the current
  choice among its `+0x12` choices (`+0x06` words), sets `+0x142` bit `0x4` from bit `0x1` of the entry's `+0x14`, or
  clears it when `step` is given, and shows the choice's action name (class `0x14`, `0x002B58B0`) in node 1;
  `0x002D54B0(window, action)` shows a given action's name there.
- `0x002D5170(window, kind, plain)` builds the title at `+0xC0`: text `0x4669`, `0x466A` or `0x466C` by kind, or
  `0x46B4` with `+0x142` bit `0x4` or `plain`, followed by the member's name¹.
- `0x002D53F0(window, value, max)` writes value x 100 into node 1 (`0x0029F6E0`, grey `0x80808080`) and gives node
  0's gauge value x 100 / max², 0 for a max of 0.
- On opening the time `+0x740` and its maximum `+0x744` both take the value `0x00309E40` stores:
  `0x022C2188 = min(4.0, 0x022C2184 + (0x022C2188 - 0x022C2184) x 0.5)`³. `0x0030D720` sets both globals to 4.0, and
  `0x0030DB70` writes `0x022C2184`⁴. The procedure below counts the time down.
- `0x002D5500(window, n)` shows the first n of three marks in the child list of node 2, and `0x002D5C30(window)`
  runs it with the entry's count `+0x13`.
- The child `0x0028B860`, built by `0x002899A0` under the window, takes its box from the HUD sprite set
  (`0x0035D460()`) on message 1. On message 2, 90 frames after the time `+0xC0` that message 6 stamps, it
  closes (`0x00244DD0`, or `0x00245020` with `+0xC4` bit `0x2`), unless message 15 has set `+0xC4` bit `0x1`.
- Its draw (message 4) takes `t = min(frame - +0xC0, 90) x 256 / 90` and reads the four-key track `0x00915E10` at
  `t` with `0x00271AB0` ([Party list](party-list.md)): the widget's `+0x5A` takes the key byte `+7`, `+0x58` the byte
  `+6` `>> 1`, and the key field `+10` is the `s` with which `0x0028B700` draws the set's piece `+0x88` at
  `(+0x9C >> 1, +0x9E >> 1)`⁵.
- While `t >= 16` the draw draws the piece again with `s` from the track at `t - 16`⁶.
- `0x0028B700(draw, set, piece, x, y, s)` draws a piece one source row at a time, centred on `x` and starting
  half the piece's height above `y`. Each row is one pixel high and its half width alternates between
  `w - (w x s >> 8)` and `w + (w x s >> 8)`, with `w` half the piece's width; `0x002D8C80` draws each row.
  It first sets the draw's palette byte `+0x5C` from the set's table and the piece's byte `+7`.
- `0x002D50B0(window, keep)` calls `0x00244DD0(row)`, which closes a row widget, for every row (`0x158` bytes from
  `+0x180`, `+0x748` of them, a signed count) except row `keep`. It then ends with a jump to
  `0x00244DD0(window + 0xC0)`, which closes the gauge child, not the window⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00296600` |
| ² | `0x00225580` |
| ³ | `0x002F8B90` |
| ⁴ | `0x0030DC8B` |
| ⁵ | `0x0028B9A3`-`0x0028BA59` |
| ⁶ | `0x0028BA5E`-`0x0028BAB9` |
| ⁷ | `0x002D50E2`-`0x002D5167` |

</details>

On row `keep` `0x002D50B0` sets bits `0x3` of byte `+0x142`, copies its word `+0x98` to word `+0x144`, stores `0x10` at
byte `+0x143`, and stores the window's word `+0x15A` plus the word `+0x0E` at `[[window + 0x120]]` at word `+0x146`¹; it reads that pointer after testing `window + 0xC0` against null, a test that is never met².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D50DB`-`0x002D514A` |
| ² | `0x002D50C3`-`0x002D50D5` |

</details>

`0x002D5EB0(window, message)` (1,821 bytes) is the window's procedure. It dispatches on the message's dword `+0` through
a table of 20¹: 1 opens, 2 ticks, 10 takes input, and 14, 15 and 18 are told below; 4 and 20
return 0, and any other goes to `0x005C5230(window, message)`, whose answer it returns². Every
way out passes the stack-cookie check `0x00808C40(cookie)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D5ED1`-`0x002D5EF5` |
| ² | `0x002D65A2`-`0x002D65A9` |
| ³ | `0x002D65AE`-`0x002D65B6` |

</details>

Message 1 calls `0x003678F0()`, sets the window's dword `+0x98` to 0 and its words `+0x9C` and `+0x9E` to `[0x01E0C1D8]`
and `[0x01E0C1DC]` when the window is not null, sets the time and its maximum from `0x00309E40()`, creates the gauge child
with `0x00245000(window + 0xC0, 0xC0, 0x002D5E00, 0)` and adds it with `0x00244960(window, window + 0xC0)`¹. It then fills the entry table with `0x00309C40(window + 0x6E0, 4)` and zeroes the word `+0x752`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D5EF7`-`0x002D5F69` |
| ² | `0x002D5F6E`-`0x002D5F82` |

</details>

For each of the four 24-byte entries whose dword `+0` is not 0, it looks for the first party member `i` below
`0x0035BB60()` whose status record `0x0035BB20(i)` has that dword at `+4`, and lists `i`; the count goes to byte `+0x748`¹. Each listed member `k` gets a row at `+0x180 + k x 0x158`:
`0x00245000(row, 0x158, 0x002D5C80, params)`, with the params' qwords `+0x08` and `+0x10` holding `count - 1 - k` and the
member, then `0x002D5280(row, window + 0x6E0, 4, 0)`, `0x002D5170(row, k, 0)` and `0x00244960(window, row)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D5F89`-`0x002D5FEA` |
| ² | `0x002D5FF1`-`0x002D6065` |

</details>

The answer of that `0x00245000` call has its words `+0x98` and `+0x9A` raised by the gauge child's `+0x98` and `+0x9A`,
the window's `+0x158` and `+0x15A`¹. The window then clears byte `+0x74B`, clears bit `0x2` of
each row's byte `+0x142` and sets it on row 0², draws the gauge with
`0x002D53F0(window + 0xC0, time, maximum)`, and calls `0x0029E0E0()`, `0x0029E770([0x0209E664], [0x01E0C1DC] - [0x0209E668])`,
`0x0029E330(0xE)` and `0x0029E6D0(0)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D606A`-`0x002D609B` |
| ² | `0x002D60A8`-`0x002D60F2` |
| ³ | `0x002D60F4`-`0x002D6134` |

</details>

Last it sets byte `+0x74A` to 25, calls `0x00247570(window, 0x002735E0(5))`, sets the sound handle `+0x74C` to -1 and
returns 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D6139`-`0x002D6166` |

</details>

Message 2 returns 0 unless `0x001EDEC0(window dword +0xB4)` answers non-zero and bit `0x1` of byte `+0x749` is clear¹. While byte `+0x74A` is above 0 it counts it down; when it reaches 0 it keeps `0x00271500(0x5A)`
at `+0x74C`, calls `0x0029E6D0(1)` and returns 0². With the byte at 0, a word `+0x752` of 1
returns 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D636C`-`0x002D6386` |
| ² | `0x002D638C`-`0x002D63C3` |
| ³ | `0x002D63C8`-`0x002D63D2` |

</details>

With the word at 2, word `+0x750` counts up. Below 8, each row steps its choice index, word `+0x148`, back to 0 at the
entry's choice count byte `+0x12`, clears bit `0x4` of its byte `+0x142` and shows the entry's word
`+0x06 + 2 x index` with `0x002D54B0(row, action)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D63D8`-`0x002D63F2`, `0x002D6472`-`0x002D64CE` |

</details>

At 8 it calls `0x0029E6D0(1)`, zeroes the word `+0x752`, and for each row shows the entry's action, word `+0x04`, with
`0x002D54B0`, copies bit `0x1` of the entry's byte `+0x14` to bit `0x4` of the row's byte `+0x142` and calls
`0x002D5170(row, k, 0)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D63F4`-`0x002D6470` |

</details>

Then, for any word `+0x752` but 1, it takes `[0x009171D0]`, 1/30, off the time `+0x740`, not below 0, and redraws the
gauge with `0x002D53F0(window + 0xC0, time, maximum)`¹. At 0 it stops the sound with
`0x002716F0(+0x74C)`, sets the handle to -1, plays sound `0x5B` (`0x00249C60(0x5B)`), calls `0x0030DB70(0, 0.0)`, closes
with `0x00244DD0(window)`, calls `0x00290740()` and returns 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D64D0`-`0x002D650D` |
| ² | `0x002D6512`-`0x002D6557` |

</details>

Message 10 returns 0 when bit `0x1` of byte `+0x749` is set, word `+0x752` is not 0, byte `+0x74A` is above 0 or the
time is 0¹. It tests the word `[0x02F9736A]` against three masks, `0x1000`, `0x8000`, and
`0x4000` when `0x001E0C10()` answers non-zero, else the word `[0x01E0C2A4]`, one per row while the row exists, and the
first mask with a bit set in that word picks its row².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D6193`-`0x002D61CB` |
| ² | `0x002D61D1`-`0x002D622B` |

</details>

For a picked row, when bit `0x1` of its entry's byte `+0x14` is set it returns 0; otherwise it calls
`0x0030DB70(entry, time)`¹. An answer of 0 plays sound 2 (`0x00249C60(2)`), stops the sound with
`0x002716F0(+0x74C)` and sets the handle to -1, sets word `+0x752` to 1, and calls `0x0029DF90()`, `0x002470C0(window)` and
`0x002D50B0(window, row)`, and returns 0². Any other answer plays sound `0x5C` (`0x00249C60(0x5C)`)
and shuffles as below without sound `0x53`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D62E1`-`0x002D630D` |
| ² | `0x002D6312`-`0x002D6367` |
| ³ | `0x002D6319`-`0x002D6323` |

</details>

With no match, the window shuffles when `0x0029DBE0(0x112)` has a bit in the word `[0x02F9736C]`, else returns 0¹. The shuffle plays sound `0x53` (`0x00249C60(0x53)`), sets word `+0x750` to 0 and word `+0x752`
to 2 (one dword store of `0x20000`), calls `0x0029E6D0(0)`, refills the entries with `0x00309C40(window + 0x6E0, 4)`, and
for each row calls `0x002D5280(row, window + 0x6E0, 4, 8)` and `0x002D5170(row, k, 1)`, then returns 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D622D`-`0x002D6240` |
| ² | `0x002D6246`-`0x002D62DC` |

</details>

Message 14 calls `0x00309C00(&a, &b)` with two locals, `0x0035D060(5)` and `0x002470D0(window)`, and returns 0¹. Message 15 sets bit `0x1` of byte `+0x749`, stops the sound with `0x002716F0(+0x74C)` and sets
the handle to -1, calls `0x0029DF90()` and returns 0². Message 18 stops the sound with
`0x002716F0(+0x74C)`, sets the handle to -1, calls `0x0035D060(1)` and `0x00182DA0()` and returns 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D616B`-`0x002D618E` |
| ² | `0x002D6559`-`0x002D657C` |
| ³ | `0x002D657E`-`0x002D65A4` |

</details>

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

144 procedures belong to a screen. The other 123 belong to no screen: the field HUD and its children (root `0x00253780`),
the party HP and MP list, the help line and target window, the message windows, the shared dialogs, list rows, the
title screen, the logos, the screen mask, the NG signal and the shared backgrounds and captions. Several are shared by
many screens, for example the list item `0x00292390` (11 owners) and the layout item `0x0029E7D0`, which the layout decoder
`0x002432B0` installs for every screen.

### Resources

A procedure's layout comes from `mrppack_ys.bin`: `0x00280980` relocates its 23 units into `[0x0209AC30] + 8 x unit`¹, and `0x002432B0` reads a record of a unit. It fills and relocates only a unit whose slot is
still null², fills nothing while `layoutPack` (`+0x3D0`) is null³, and on both paths ends by
jumping to `0x00280AD0`⁴. The table gives layouts as unit and record. Files are
named from the resource path table `0x01EC73A0`, and images by the label the code passes to `0x0024A5A0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00280980`-`0x002809DE` |
| ² | `0x002809A8` |
| ³ | `0x00280993` |
| ⁴ | `0x002809EE` |

</details>

Some screens also load text groups ([Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).
`0x002F8040(g)` answers whether group g is resident¹. The gambit editor's `0x00292210` adds groups 10 and 16
to its resource batch when they are not², and `0x002922F0`, run by the gambit editor³, the Inventory⁴, the
shop⁵ and `0x00560910`⁶, releases each resident group through `0x002F83E0`: 17 unless `[0x02CA8F94]` is set, 10, 20 and 14
unless `[0x02CA96D4]` is set, and 16.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EC3D80` |
| ² | `0x002491B0` |
| ³ | `0x00569236` |
| ⁴ | `0x00566217` |
| ⁵ | `0x0057BC88` |
| ⁶ | `0x0056098E` |

</details>

### The Quit and Parameter Settings pointers

Each opener creates its screen through `0x00244F50` only while its global is 0 and keeps the widget there; the screen
clears it when it is destroyed (message 18), and on leaving returns to the Party Menu on its entry¹,
plays sound 3 and closes². Both globals are 0 in the file. The Config, Graphics Settings and Controls
pointers are on [Config screen](config-screen.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002814E0` |
| ² | `0x00244F00` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209AC20` | `void*` | 0 | the open Quit screen, the `0xC0`-byte widget with procedure `0x0027EA70` | `0x0027EBC0` (`0x0027EC0B`); `0x0027EA70`, 0 on message 18 (`0x0027EA9E`) | `0x0027EBC0`, which creates it only while it is 0 (`0x0027EBD3`) and opens it (`0x00246AC0`, `0x0027EC1A`); `0x0027EA70`, which closes it after `0x002814E0(0x505)` (`0x0027EB4A`) |
| `0x0208E6C8` | `void*` | 0 | the open Parameter Settings screen, the `0xC8`-byte widget with procedure `0x00240AD0` | `0x00240D60` (`0x00240DAB`); `0x00240AD0`, 0 on message 18 (`0x00240B00`) | `0x00240D60`, which creates it only while it is 0 (`0x00240D73`) and opens it under the menu root `[0x0208EA28]` (`0x00246AD0`, `0x00240DBA`); `0x00240AD0`, which closes it after `0x002814E0(0x53A)` (`0x00240B5C`) |

No other instruction reaches either.

### The Parameter Settings screen

The Parameter Settings screen is the `0xC8`-byte widget kept at `0x0208E6C8` with procedure `0x00240AD0` (above). On
message 1
it decodes record `0x10` of the layout file at `[0x0209AC30] + 0x60` into its `+0x50`¹; its two rows are painted by `0x00240A60` ([Config screen](config-screen.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002432B0`, `0x00240C41`-`0x00240C59` |

</details>

`ParameterSettingsScreen` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00240AD0` |
| `+0xC0` | `void*` | commandList | the two-row list (Max. LP, Max. Gil): the list widget node 0 of the screen's layout holds at its `+0x18`, taken on message 1 (`0x00240C9D`-`0x00240CA8`). Message 1 sizes it to 2 rows (`0x002D48C0`, `0x00240CAF`), makes this screen its `+0xD8` (`0x00240D2A`), installs the row painter `0x00240A60` at its `+0x120` (`0x00240D38`) and puts the cursor on row 0 (`0x002D46F0`, `0x00240D46`); message 10 runs it (`0x002D3900`, `0x00240C34`). The list's notices read the cursor row from its `+0xF2`, `+0xF4`, `+0xEC`, `+0xEE` and `+0xED` (`0x00240B70`-`0x00240BA1`, `0x00240BD7`-`0x00240C08`): `0x8000` shows the row's help text from the pairs at `0x00914C60` (`0x00240C0A`-`0x00240C20`), `0x8001` on row 0 sets 99,999 LP (`0x00305A00`, `0x00240BBB`) and on row 1 99,999,999 gil (`0x003058B0`, `0x00240BAE`) |

### The leader choice window

The party leader choice is the `0xC8`-byte widget kept at `0x022CA428` with procedure `0x0035D6B0`.

`LeaderChoiceWindow` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0035D6B0` |
| `+0xC0` | `i32` | delay | the steps left before the question opens: the construct message sets `0x18` (`0x0035D89C`); each step message 2 on which `0x001EDEC0`(`+0xB4`) answers non-zero lowers it while it is above 0 (`0x0035D7D2`-`0x0035D7DE`), and at 0 the question opens (`0x0035D7E4`) |
| `+0xC4` | `u32` | flags | bit `0x1`: the question box is open, set after `0x0035C660` opens it (`0x0035D7F1`, `0x0035D808`) so it opens once, cleared by the construct message (`0x0035D895`); bit `0x2`: `0x0035BB70`, run at the field set-up and teardown, is closing the window (`0x0035BBB1`), and then message 18 skips its own restore of the menu state (`0x0035D6FC`) |

### The menu state block

The menu state block is the static `0x0209AC60`, `0xE00` bytes. `0x002800F0`, from `0x00253970`¹, points
`[0x0209AC30]` at it and clears it once²; every reader reaches it through `[0x0209AC30]`. It holds
the open screens and panes, the menu pictures and layouts, the nine party records the menus show, and the state the
menu screens share.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002539C0` |
| ² | `0x002800FA`-`0x00280110` |

</details>

`MenuStateBlock` (`0xE00` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `void*[23]` | layoutUnits | the 23 layout units of mrppack_ys.bin, unit u at +8 x u: `0x00280980` fills each empty one with the pack's address plus the pack's u32 at 4 x u (`0x002809A3`-`0x002809B7`) and relocates it (`0x002A00F0`); the screens read their layout records from it through `0x002432B0` (the unit table below) |
| `+0x0B8` | `void*` | modeScreenTask | the open mode-screen task, the `0xD8`-byte widget `0x0027FB70` that `0x00280A00` builds for a menu request (`0x00280A6F`-`0x00280A76`): it stores itself when it opens (`0x0027FE02`) and clears this on message `0x12` (`0x0027FBAB`); `0x00280A00` opens nothing while this or areaController is set (`0x00280A1A`-`0x00280A30`) (Game over) |
| `+0x0C0` | `void*` | areaController | the open area controller, the `0xD8`-byte widget `0x00280140` that `0x00280A00` builds beside the mode-screen task (`0x00280A85`-`0x00280A8C`): set when it opens (`0x00280429`) and cleared on its message `0x12` (`0x002802A0`); `0x00280120` answers 1 while this is 0 (`0x00280129`), and `0x0027EFA0` writes 2 to its `+0xC8` before a game over (`0x0027EFDA`-`0x0027EFE8`) |
| `+0x0C8` | `void*` | eventSkipTask | the event-skip task, the `0xD8`-byte widget `0x00228130` that `0x00228700` builds for Start's skip arm (`0x0022875F`-`0x00228777`) and that clears this when it ends (`0x002281E9`); `0x00228700` builds no task while it is set (`0x0022871A`); it builds the pause task `0x00228C70` at `+0xD0` first, through `0x002289D0` (`0x00228755`) (Action availability) |
| `+0x0D0` | `void*` | pauseTask | the pause task, the `0xF8`-byte widget `0x00228C70` that `0x002289D0` builds (`0x00228A01`-`0x00228A09`), where the player closes it, skips the event, returns to the title or quits (Game over); `0x002289D0` builds none while this is set (`0x002289EA`); set when it opens (`0x00228DC6`) and cleared when it ends (`0x0022946D`) |
| `+0x0D8` | `void*` | partyMenu | the open Party Menu `0x00280DE0`, stored by its menu task `0x00281AE0` (`0x00281B23`, called from `0x00280E4E`) and cleared by `0x00281E00` (`0x00281EB4`); the script menu host `0x002D70F0` stores itself here when a script opens a menu (`0x002D735A`); `0x00280B70` closes it (`0x00280C6A`-`0x00280C71`) |
| `+0x0E0` | `void*` | scriptResourceTask | the `0xC0`-byte task `0x002D6EE0` that the script verb fsmenu_loadresource builds through `0x002D7840` (`0x002D7862`-`0x002D786E`): it requests the picture tuto_win_c into tutoWinPicture (`0x002D6F39`-`0x002D6F65`), stores itself (`0x002D6F80`) and clears this on message `0x12` (`0x002D6F0F`); `0x002D7840` builds no task while it or tutoWinPicture is set (`0x002D784B`-`0x002D785D`) |
| `+0x0E8` | `void*` | autoWindow | the auto window `0x002D66D0` that the script verbs fsmenu_showauto and fsmenu_showautofast build through `0x002D7B40` (`0x002D7B7C`-`0x002D7B9C`): it stores itself (`0x002D673A`) and clears this (`0x002D6708`); `0x002D7B40` builds no window while it is set (`0x002D7B5F`) |
| `+0x0F0` | `void*` | highlightRectWindow | the `0x188`-byte highlight-rectangle window `0x002D6CA0` that fsmenu_loadresource builds through `0x002D7840` (`0x002D7887`-`0x002D7897`): it stores itself (`0x002D6D82`) and clears this when it closes (`0x002D6CE2`); the verbs fsmenu_registrect, fsmenu_showrect, fsmenu_hiderect and fsmenu_registiconrect drive it (`0x002D78B0`, `0x002D7CB0`, `0x002D7800`, `0x002D7710`), as do the gambit editor (`0x0056A3D0`, `0x0056BE40`) and the location map (`0x003C6B70`) |
| `+0x0F8` | `void*` | memberList | the Party Menu's member list `0x00285290`: set when it opens (`0x002852F0`) and cleared when it closes (`0x0028562C`); its row widgets sit at its `+0xC0` + 8 x slot, which `0x002830A0`, `0x00280B70` and `0x00282FC0` walk beside memberSlots (`0x002830F3`, `0x00280BC3`, `0x00282FF3`) |
| `+0x100` | `void*` | requestDispatcher | the request-screen dispatcher `0x0027F5D0` under the mode-screen task: set when it opens (`0x0027F738`) and cleared when it leaves (`0x0027F84F`) |
| `+0x108` | `void*` | equipPane | the equipment pane `0x003FF360` of Status and Equip, built once by `0x003FF160` (`0x003FF192`-`0x003FF1BC`) and cleared by the pane (`0x003FF8E4`) |
| `+0x110` | `void*` | statusPane | the Status pane `0x002C59D0` (mrppack unit 7 record 2), built once by the screen `0x002C2320` on Status only (`0x002C25E9`, `0x002C2692`-`0x002C26BE`) and cleared by the pane (`0x002C5E4B`) |
| `+0x118` | `void*` | namePanel | the Party Menu's current-member name panel `0x002C13C0` (mrppack unit 7 record 10): set when it opens (`0x002C150B`), cleared when it closes (`0x002C1770`) |
| `+0x120` | `void*` | listPanel | the Party Menu's list panel `0x002C3560` (mrppack unit 7 record 12): set when it opens (`0x002C386F`), cleared when it closes (`0x002C35B1`) |
| `+0x128` | `void*` | fourPanePanel | the Party Menu's four-pane panel `0x002C4460` (mrppack unit 7 record 11): set when it opens (`0x002C46DB`), cleared when it closes (`0x002C44B0`) |
| `+0x130` | `void*` | statusBottomPane | the Status and Equip pane `0x002C1E20` (mrppack unit 6 record 2), built by `0x002C1DA0` (`0x002C1DF7`) and cleared by the pane (`0x002C1E55`) |
| `+0x138` | `void*` | equipStatPanel | the Equip screen's stat panel, EquipStatPanel above: built by `0x003FE410` (`0x003FE466`), cleared on its message 18 (`0x003FE60E`) |
| `+0x140` | `void*` | statusEquipScreen | the Status and Equip screen `0x002C2320`: set when it opens (`0x002C2363`), cleared when it returns to the Party Menu (`0x002C25DB`) |
| `+0x148` | `void*` | slotNames | the slot-name widget `0x003FEE40` (Weapon, Off-hand, Helm, Armor, Accessory), built by `0x003FEDC0` (`0x003FEE17`) and released and cleared by `0x003FD2C0` (`0x003FD335`-`0x003FD341`) |
| `+0x150` | `void*` | equipList | the equipment list `0x003FDFE0` ("Change equipment."), built by `0x003FDA20` (`0x003FDA69`) and cleared by the list (`0x003FE072`) |
| `+0x158` | `void*` | licenseMemberPick | the License Board's member pick `0x00560910`: set when it opens (`0x00560A40`), with partyFlags bit `0x10` set (`0x00560A4E`); cleared when it leaves (`0x005609BD`), with bit `0x10` cleared (`0x005609CB`) |
| `+0x160` | `void*` | gambitPane | the gambit editor's pane in entry 4 of its table `0x02CA96E0` (the cell `0x02CA9700`): the editor `0x005691E0` copies it here when it opens (`0x00569507`-`0x0056951A`) and clears this when it leaves through `0x002814E0`(`0x4B9`) (`0x0056927A`) |
| `+0x168` | `void*` | inventory | the Inventory screen `0x00565E00`: set when it opens (`0x00565E50`), cleared on its message 18 (`0x0056622F`) (Inventory screen) |
| `+0x170` | `void*[33]` | tabPanes | the tab panes of the Inventory and the shops, the pane of slot s at +8 x s: the table `0x00D233A0` gives categories `0x405`-`0x409` and `0x40D`-`0x40F` slots 0-7 and the shop tab keys `0x597`-`0x5AF` slots 8-32 (the 33-entry search `0x00563FD0`-`0x00563FE1`); `0x00564B90` stores a built pane (`0x00564C40`), the pane procedure `0x005651E0` clears its slot (`0x005655CA`), and `0x00563FC0`, `0x00564A60`, `0x00565190` and `0x005659B0` look a pane up (Inventory screen) |
| `+0x278` | `void*` | infoPanel | the Party Menu panel `0x002CF940` (mrppack unit 6 record 6) that `0x002CF8B0` builds for the Party Menu and the shop list: set when it opens (`0x002CFC3B`), cleared when it closes (`0x002CF978`) |
| `+0x280` | `void*` | gradient | the menu background gradient `0x002CE7E0` (picture party_grd_2), built by `0x002CD800` (`0x002CD85C`) and cleared by the gradient (`0x002CE841`); `0x002C98C0` closes it (`0x002C98D4`) |
| `+0x288` | `void*` | summonNameRow | the name row `0x002CF740` (mrppack unit 6 record 10) that `0x002CF710` builds only while an Esper is summoned (partyFlags bit `0x8`) and this is 0 (`0x002CF717`-`0x002CF728`): set at `0x002CF7E8`, cleared on its message `0x12` (`0x002CF77E`) |
| `+0x290` | `void*` | screenLayer0 | screen layer kind 0: `0x002CCD40` builds the `0xF0`-byte fade layer `0x002CCE70` of kind k at `+0x290` + 8 x k (`0x002CCD62`-`0x002CCDA6`) under that kind's root (`0x002CCDB5`-`0x002CCDEA`), and `0x002CCBC0`(k, frames) closes it; kind 0 comes from `0x002CCCF0` (`0x002CCD21`) and goes under the menu root `0x0208EA28`; `0x002CCBA0` closes it (`0x002CCBA7`) |
| `+0x298` | `void*` | screenLayer1 | screen layer kind 1, from `0x002CCCA0` (`0x002CCCD6`), under `0x0208EA28`; `0x002CCB10`, `0x002CCB30` and `0x002CCC30` close it through `0x00244F00`, each only when it is not 0 and its `+0x7C` bit `0x20` is clear (`0x002CCB17`-`0x002CCB27`, `0x002CCB37`-`0x002CCB4B`, `0x002CCC37`-`0x002CCC48`); `0x002CCB30`(value) first, for a value of 1 to `0xFFF`, puts its low 10 bits in bits 22-31 of `+0x7C` and sets bit `0x800`, and for `0x1000` or more clears bit `0x800` and sets `+0x40` bit `0x10000` (`0x002CCB4D`-`0x002CCB7F`); `0x002CCC30` first sets its `+0x7C` bit `0x800` and puts 1 in bits 22-31 (`0x002CCC4A`-`0x002CCC54`), so that a closing run `0x00244DD0` starts from state 0 or 3 lasts 1 ms, which is 0 frames (`0x00244EB0`-`0x00244ED4`); `0x002CD150` reads it (`0x002CD159`) |
| `+0x2A0` | `void*` | screenLayer2 | screen layer kind 2, from the pause task `0x00228C70` (`0x00229109`-`0x00229127`), under `0x0208EA38`; the event-skip task closes it (`0x002CCBC0`(2, `0x1000`) at `0x00228192`-`0x002281A2`) |
| `+0x2A8` | `void*` | screenLayer3 | screen layer kind 3, from the pause screen `0x00229590` (`0x0022993C`, `0x00229A98`), under `0x0208EA48`, which also closes it (`0x0022983E`); `0x00229590` waits for it to be gone (`0x00229776`) (Pause screen) |
| `+0x2B0` | `void*` | screenLayer4 | screen layer kind 4, which `0x002CCD40` would put under `0x0208EA50` (`0x002CCDE6`-`0x002CCDEA`); stays 0, because the five calls of `0x002CCD40` pass kinds 0, 1, 2, 3 and 3 (`0x002CCD21`, `0x002CCCD6`, `0x00229127`, `0x0022993C`, `0x00229A98`) |
| `+0x2B8` | `void*` | topBand | the top black band `0x002C9120` of the screen openers: `0x002C99E0` builds it for slot 0 (`0x002C9A62`-`0x002C9A77`) under `0x0208EA28`, and the band clears its slot when it closes (`0x002C9176`); read by `0x002C9060`, `0x002C9400`, `0x002C9430` and the request dispatcher (`0x0027F78E`) |
| `+0x2C0` | `void*` | topBandSlot1 | slot 1 of the top band, which `0x002C99E0` would build under `0x0208EA38` (`0x002C9A8D`); stays 0, because `0x002C99E0` is reached only from `0x002C99A0`, which passes slot 0 (`0x002C99AF`) |
| `+0x2C8` | `void*` | bottomBand | the bottom black band `0x002C9570`, built with topBand (`0x002C9A2F`-`0x002C9A5A`) and cleared when it closes (`0x002C95C7`); `0x002C98F0` closes both bands and the side mask `0x0209C318` (`0x002C98FF`-`0x002C998F`); read by `0x002C9430`, `0x002C9490`, `0x002C9890` and the request dispatcher (`0x0027F7A3`) |
| `+0x2D0` | `void*` | bottomBandSlot1 | slot 1 of the bottom band; stays 0 for the same reason as topBandSlot1 |
| `+0x2D8` | `void*` | titleCaption | the screen title caption `0x002CA1F0` (mrppack unit 6 record 4), rebuilt by `0x002CA150` after releasing the old one (`0x002CA182`-`0x002CA1C5`) and released by `0x002CA110` (`0x002CA11B`-`0x002CA133`) |
| `+0x2E0` | `void*` | memberRecordPanel | the member-record panel `0x002CBF80` (The member-record panel above), built by `0x002CBED0`, `0x002CBE40` or `0x002CBDA0` (`0x002CBF48`, `0x002CBE96`, `0x002CBE11`) and cleared on its message `0x12` (`0x002CBFBD`) |
| `+0x2E8` | `void*` | questionOrNotice | the open yes-or-no question `0x002CDF20` (set `0x002CDF6C`, cleared `0x002CE1F7`) or notice `0x002CE370` (set `0x002CE48A`, cleared `0x002CE3D4`) (Dialogs) |
| `+0x2F0` | `void*` | sortBar | the item sort bar `0x00566680` ("Sort", menu_command.bin `0x415`), built by `0x005665B0` (`0x00566661`) and cleared by the bar (`0x00566765`) |
| `+0x2F8` | `void*` | descriptionWindow | the description window, MenuDescriptionWindow below: built by `0x00292FA0` only while this is 0 (`0x00292FBA`-`0x00292FF4`); the window also stores itself (`0x00293042`), and `0x00292B10` releases it and its box and clears this (`0x00292B5C`) |
| `+0x300` | `void*` | itemPictureLoader | the item-picture loader `0x00291D90` (itemgra_c pictures for the ten entries at `0x0209BEA0`): set when it opens (`0x00291F96`), cleared when it closes (`0x00291DD2`); the area controller waits while this or pictureLoader is set (`0x002802F2`-`0x00280308`) |
| `+0x308` | `void*` | pictureLoader | the picture loader `0x002CEB40` for the entries at `0x0209E638` that `0x002CEFA0` installs: set at `0x002CEDB7`, cleared when it closes (`0x002CEB87`); the pause screen takes the focus only while this is 0 (`0x002470ED`) (Pause screen) |
| `+0x310` | `void*` | silhouette | the gambit editor's character silhouette `0x002CF440`: set when it opens (`0x002CF620`), cleared when it closes (`0x002CF489`) |
| `+0x318` | `void*` | memberOrderWatch | the `0xF0`-byte widget `0x00283A10` that `0x002839B0` builds once (`0x002839BB`-`0x002839E0`; also from the shop list and `0x0035CA70`): when created it copies the nine records' member ids `+0x60` to its `+0xC0`-`+0xE0` (`0x00283A51`-`0x00283AF9`). Each step runs `0x00283B30`: after the member order changes it waits for the party read-in (`0x00324360`, done when `0x0037CB50` reports it), then re-records the fighting units and reloads their models (`0x00324380`), goes round once more if `+0xE8` bit `0x1` flags a further change, then stops (state 0). `0x00283940` releases it and clears this (`0x00283963`) |
| `+0x320` | `void*` | licenseBoardView | the License Board's open board chooser `0x00557DB0` (built by `0x00557AE0`, `0x00557B4D`) or grid view `0x0055CD40` (built by `0x0055C690`, `0x0055C6FD`); each clears it when it closes (`0x005582CE`, `0x0055CDC4`) (License Board screen) |
| `+0x328` | `void*` | confirmWindow | the confirm window `0x0057C480` (Dialogs): set when it opens (`0x0057C4D9`), cleared when it ends (`0x0057CC83`) |
| `+0x330` | `void*` | commandRowSet | the command-row set being filled (Command rows and first visits above): `0x002CD4D0`(set, rows, n) clears n 32-byte rows and points this at the set (`0x002CD4E5`-`0x002CD4FD`); `0x002CD3C0` appends a row with its id and two texts (`0x002CD3D3`-`0x002CD403`), `0x002CD420` returns row i and `0x002CD4B0` the count |
| `+0x338` | `void*` | picBattle4c | the picture battle_4_c, registered by `0x00280750` (`0x00280807`-`0x00280823`, label `0x01E0C1E8`) and bound by `0x00280670` (`0x002806A0`-`0x002806B6`); `0x0035D460` returns it (`0x0035D467`) (Menu sprites) |
| `+0x340` | `void*` | picTargetlineP | the picture targetline_p, the second of the ten pictures `0x00280750` registers in its loop (`0x0028080E`-`0x00280823`, label `0x01E0C1E0`) and `0x00280670` binds (`0x002806A0`-`0x002806B6`) |
| `+0x348` | `void*` | picSFontC | the picture s_font_c, the third of the ten (label `0x01E0C230`), registered and bound by the same loops |
| `+0x350` | `void*` | picBattle4p | the picture battle_4_p, the fourth (label `0x01E0C1F0`); `0x0035D3D0` returns it (`0x0035D3D7`) |
| `+0x358` | `void*` | picMiniFaceC | the picture mini_face_c, the fifth (label `0x01E0C278`); `0x0035C430` copies a guest's small face into it (`0x0035C440`, `0x0035C51F`) (Binmenu images) |
| `+0x360` | `void*` | picPartytop4c | the picture partytop_4_c, the sixth (label `0x01E0C200`); `0x0035D470` returns it (`0x0035D477`) |
| `+0x368` | `void*` | picPartytop8c | the picture partytop_8_c, the seventh (label `0x01E0C208`); `0x0035D480` returns it (`0x0035D487`) |
| `+0x370` | `void*` | picPartyGrd2 | the picture party_grd_2, the eighth (label `0x01E0C238`), registered and bound by the same loops |
| `+0x378` | `void*` | picIconsC | the picture icons_c, the ninth (label `0x01E0C1F8`); read by `0x00242B90` (`0x00242BA9`) and `0x002C33F0` (`0x002C343F`) |
| `+0x380` | `void*` | picExtraC | the picture extra_c, the tenth (label `0x01E0C280`), registered and bound by the same loops; the loops end at `+0x388` (`0x00280832`, `0x002806CA`) |
| `+0x388` | `void*` | effectPicture | the TIM2 picture at the picture pack's u32 `+0x28` offset, set once by `0x00280670` (`0x002806D3`-`0x002806F4`); `0x002509D0` reads it (`0x00250B01`, `0x00250B6E`) (Script screen effects) |
| `+0x390` | `void*` | colourTable0 | colour table 0: `0x00280AD0` points it at the colour-table file plus the file's u32 `+0x00` (`0x00280AE7`-`0x00280AF6`); read by `0x002509D0`, `0x00250E90`, `0x002C8EE0` and `0x002CEFD0` (CL2 menu colour tables) |
| `+0x398` | `void*` | colourTable1 | colour table 1, the file plus its u32 `+0x04` (`0x00280B04`-`0x00280B1B`); `0x0035D530` returns it plus `0x40` (`0x0035D537`-`0x0035D53E`) |
| `+0x3A0` | `void*` | colourTable2 | colour table 2, the file plus its u32 `+0x08` (`0x00280B29`-`0x00280B40`); `0x0035D520` returns it (`0x0035D527`) |
| `+0x3A8` | `void*` | colourTable3 | colour table 3, the file plus its u32 `+0x0C` (`0x00280B4E`-`0x00280B65`); read by `0x002509D0` (`0x00250B40`) |
| `+0x3B0` | `void*` | shopPicture | the shop picture shop_8_c, requested by `0x002CBD50` as kind 7, id `0x63` (`0x002CBD5B`-`0x002CBD91`) and released by `0x002CC5F0` (`0x002CC5FB`-`0x002CC618`) |
| `+0x3B8` | `void*` | tutoWinPicture | the picture tuto_win_c, requested by scriptResourceTask as kind 7, id `0xD8` (`0x002D6F39`-`0x002D6F65`) and released by `0x002D7960` (`0x002D796B`-`0x002D7988`) |
| `+0x3C0` | `void*` | guestPortrait | the guest portrait face_guest, requested by `0x002CEAE0` when a guest is in the party (`0x002CEAEB`-`0x002CEB26`) and freed by `0x002CE980` after it copies it into partytop_8_c (`0x002CEA9F`-`0x002CEAC1`) (Binmenu images) |
| `+0x3C8` | `void*` | colourTableFile | the menu colour-table file, kind 7, id `0xD4`, requested by `0x002808D0` (`0x00280924`-`0x0028095D`); `0x00280AD0` takes the four colour tables from it |
| `+0x3D0` | `void*` | layoutPack | mrppack_ys.bin, kind 7, id `0xD3`, requested by `0x002808D0` (`0x002808E0`-`0x00280916`); `0x00280980` takes layoutUnits from it (`0x0028098B`-`0x002809AA`) |
| `+0x3D8` | `void*` | picturePack | tex2pack_ys.bin, kind 7, id `0xD7`, requested by `0x00280750` with `0x00280670` as its completion (`0x00280840`-`0x0028086D`); `0x00280670` binds its pictures to the ten picture names (`0x002806A0`-`0x002806D1`) |
| `+0x3E0` | `i16` | mapReturnAction | word +0 of the 6-byte record the location map or its overlay hands back through `0x00285F00` (`0x00285F09`) (Map screens): `0x002814E0` passes the record to `0x0028E690` (`0x00281572`-`0x00281579`), which does nothing for 0 and 3, reopens the location map (`0x002B9D30`) for 1 and the World Map host `0x00550400` for any other value (`0x0028E6A5`-`0x0028E712`); `0x002814E0` then branches on it (`0x00281585`) |
| `+0x3E2` | `u16` | mapReturnPage | word +2 of that record, written with +0 (`0x00285F09`): the page, bit `0x8000` set; `0x0028E690` hands it to the map it reopens (`0x0028E6C4`, `0x0028E72F`) |
| `+0x3E4` | `i16` | mapReturnPosition | word +4 of that record (`0x00285F13`); `0x0028E690` passes it to the World Map (`0x0028E75A`) |
| `+0x3E6` | `u8[2]` | gap3E6 | read and written by no function; nothing fixes its width |
| `+0x3E8` | `u8[16]` | mapViewResume | the 16-byte record copied whole by `0x00285EE0` (`0x00285EEA`) from the notice board list (`0x0037E481`-`0x0037E488`) or the Clan Primer's hunt list (`0x00579B86`-`0x00579B8D`): `0x002804E0` opens the World Map (`0x0028E790`) when bit `0x100` of its dword `+0x08` is set and the location map (`0x0028E630`) when it is clear, for the area in its dword `+0x00` (`0x002804EB`-`0x002805C3`); `0x00575580` reopens the Clan Primer straight into Hunts from it (Clan Primer) |
| `+0x3F8` | `u32` | areaWait | the dword the area controller hands to `0x0032E4D0` in state 1 (`0x00280357`); no instruction writes it, so it keeps the 0 of the first clear (`0x00280110`), and `0x0032E4D0` answers 0 for 0 (`0x0032E4DB`, `0x0032E50B`) |
| `+0x3FC` | `i32` | requestedField | the field the next teardown of the area controller travels to: `0x00285EC0` writes it (`0x00285ED8`) with bit `0x100` of areaFlags (Game over), and the controller reads it through its `+0xC0`, which points at `+0x3F8` (`0x0028044C`, `0x00280252`, `0x00280279`) |
| `+0x400` | `u32` | areaFlags | the area controller's state (low byte) and requests (the table below), reached through the controller's or the event-skip task's `+0xC0` (`0x0028044C`, `0x0022828E`) |
| `+0x404` | `u8[4]` | gap404 | read and written by no function; nothing fixes its width |
| `+0x408` | `u8[192]` | record0 | party record 0, a Party member status record (the layout on the Party member status record page) that `0x00283270` builds through `0x00320040`(3, 0, record) (`0x00283350`-`0x00283368`) for slot 0 of the gameplay roster, map 3 (Party slots); slots 0-3 are the active party |
| `+0x4C8` | `u8[192]` | record1 | party record 1, built the same way for roster slot 1 (the loop adds `0xC0` per slot, `0x0028342C`) |
| `+0x588` | `u8[192]` | record2 | party record 2, for roster slot 2 |
| `+0x648` | `u8[192]` | record3 | party record 3, for roster slot 3, the last of the active party |
| `+0x708` | `u8[192]` | record4 | party record 4, for roster slot 4, the first reserve slot |
| `+0x7C8` | `u8[192]` | record5 | party record 5, for roster slot 5 |
| `+0x888` | `u8[192]` | record6 | party record 6, for roster slot 6 |
| `+0x948` | `u8[192]` | record7 | party record 7, for roster slot 7 |
| `+0xA08` | `u8[192]` | record8 | party record 8, for roster slot 8; the loop ends at 9 (`0x00283433`) |
| `+0xAC8` | `void*[9]` | memberSlots | the nine records in menu order: for each member id of the 16-entry order table `0x00915CE0` (0, 3, 2, 4, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 0) `0x00283270` points the next slot at the first unused record with that id (`0x00283473`-`0x002834D2`), then appends the unused records in record order (`0x002834D4`-`0x002835E5`); `0x00282EA0`(slot) gives a slot's record index, and the member steps walk the slots from currentMember |
| `+0xB10` | `u8[26]` | activeMember | one byte per member id (record `+0x60`): 1 when the member's record is one of the first four (the active party), 0 for the reserve; written by `0x00283270` when its argument is non-zero (`0x0028337D`-`0x00283393`) and by `0x00284C90` (`0x00284E43`); read by `0x002858A0`, `0x002C1FF0` and `0x0035CA70` (`0x00285963`, `0x002C2124`, `0x0035CD9C`) (Chocobos and airships) |
| `+0xB2A` | `u8` | activeCount | the number of records 0-3 with a member (`+0x60` not negative): cleared and counted by `0x00283270` (`0x002832B9`, `0x002833A7`); read by `0x002CC2A0`, `0x005691E0` and `0x0056AB00` (`0x002CC307`, `0x005694B0`, `0x0056AC13`) |
| `+0xB2B` | `u8` | reserveCount | the number of records 4-8 with a member: cleared and counted by `0x00283270` (`0x002832AB`, `0x002833AF`); read with activeCount (`0x002CC30F`, `0x005694A9`, `0x0056AC0B`) |
| `+0xB2C` | `u8` | mainCount | the number of members with an id of 5 or less and record flag bit `0x2` clear, the six main characters: cleared and counted by `0x00283270` (`0x0028329D`, `0x002833C5`-`0x002833D2`); read by `0x002CC2A0`, `0x002CDAE0`, `0x003FD6B0`, `0x003FD860`, `0x0055F780`, `0x0055F830`, `0x005636F0` and `0x00563B10` |
| `+0xB2D` | `u8` | guestId | the member id of a guest in the party (record flag bit `0x2`), or `0xFF`: `0x00283270` (`0x002832C7`, `0x002833FB`-`0x00283400`); `0x002CEAE0` loads the guest's portrait face_guest id + `0x10` into guestPortrait (`0x002CEAF4`) |
| `+0xB2E` | `u8[526]` | partyMarks | the party-mark bitmap of Party marks: one byte per equipment, technick or magick id, bit value 1 << n for member n; `0x002826F0` and `0x00282A40` build it and `0x00282F10` reads it (`0x00282868`-`0x002829B5`, `0x00282BA7`-`0x00282CF9`, `0x00282F66`); the highest index, `0x20D` for magick `0x3051`, ends at `+0xD3C` |
| `+0xD3C` | `u32` | partyFlags | the party's menu conditions, rebuilt by `0x00283270` (the table below) |
| `+0xD40` | `u8[32]` | weaponSlot | the Weapon slot row of the current member, a MenuEquipSlotRow below: `0x0027F210` fills the five rows from the member's equipment words at record `+0x9A` + 4 x k, k 0-4 (the loop offset runs from `+0x98` to `+0xA8`), each time currentMember changes (`0x0027F240`-`0x0027F2BA`, through `0x00285F20` and the member steps); the member is [`+0xAC8` + 8 x currentMember] (`0x0027F247`-`0x0027F24F`). It clears each row, stores the id, and for an id other than `0xFFFF` fills name, icon and class from the query record `0x0035D330`(1, id << 16) (`0x0027F25E`-`0x0027F2A6`), so an empty slot's row is 0 apart from its id |
| `+0xD60` | `u8[32]` | offHandSlot | the Off-hand slot row; its id `+0xD68` and class `+0xD6B` decide whether a weapon needs ammunition (`0x0027F086`, `0x0027F0B0`) (Equipment) |
| `+0xD80` | `u8[32]` | helmSlot | the Helm slot row |
| `+0xDA0` | `u8[32]` | armorSlot | the Armor slot row |
| `+0xDC0` | `u8[32]` | accessorySlot | the Accessory slot row; the fill stops after it (`0x0027F2B3`) |
| `+0xDE0` | `i16` | currentMember | the slot, 0-8 in memberSlots, of the member the menus show: `0x00285F20` sets it and refreshes the slot rows (`0x00285F27`); the member steps `0x0027ED10`, `0x0027EDA0`, `0x0027F360` and `0x0027F430` move it (`0x0027ED80`, `0x0027EE3F`, `0x0027F40E`, `0x0027F503`) and the member list sets it on a pick (`0x00285B08`) |
| `+0xDE2` | `u8` | equipWarning | the Equip screen's warning code (Stats): written by the refreshers and the equipment list (`0x003FE9E7`, `0x003FECBB`, `0x003FE04C`, `0x003FE304`, `0x003FF722`, `0x00291D65`) and shown by `0x002CA490` (`0x002CA4A8`, `0x002CA557`) |
| `+0xDE3` | `u8` | shownWarning | the warning code last shown, so codes 1-9, `0xE` and `0xF` are shown once each (`0x002CA55E`, `0x002CA5C7`; cleared at `0x003FE03E`, `0x003FE2F6`, `0x003FF714`, `0x00291D57`) |
| `+0xDE4` | `u16` | warningItem | the item id the refreshers store with the code (`0x003FE9F8`, `0x003FECD0`); no instruction reads it (Stats) |
| `+0xDE6` | `u8` | licenseZoom | the License Board's zoom: the grid view's scale `+0x8C` is 2.0 while this is 0 and 1.0 while it is 1 (table `0x00D23080`, `0x0055D0D7`-`0x0055D0FD`); the button `0x110` flips it and runs the scale change over 150 (`0x0055C9FC`-`0x0055CA69`); 0 again when menu request 16 runs (`0x0027FCF2`), from `0x00394460` (`0x00394470`) and when a script opens the License Board (`0x002D73A2`) |
| `+0xDE7` | `u8` | partyMenuPage | the Party Menu's member page in `0x002C1A80`: 1 after it opens the list panel (`0x002C1C4C`-`0x002C1C58`), 2 after the four-pane panel (`0x002C1B2E`-`0x002C1B3A`), 0 when it closes them (`0x002C1C0C`); `0x002C1A80` answers non-zero while it is not 0 (`0x002C1C97`-`0x002C1CA0`) |
| `+0xDE8` | `u8` | visitsMarked | set to 1 by `0x002CD510` (`0x002CD641`) after it marks as visited Config, Status and Inventory, also World Map, Clan Primer and Licenses while the byte `0x0209A2A9` is set (`0x00264150`), and the categories `0x38`, `0x39`, `0x3A`, `0x3A`, `0x34`, `0x35`, `0x36` and `0x37` while the flags 1, 3, 2, 8, 5, 4, 7 and 6 of the bit array read by `0x00252D10` are set (`0x002CD56A`-`0x002CD635`), `0x002CD650` having set those flags first (`0x002CD514`); Party, Equip and Gambits are never marked. Called from the Party Menu (`0x00281CB5`) and the Inventory (`0x00565E57`); read by no function |
| `+0xDE9` | `u8` | stepFlash | which step arrow flashes (the table below); `0x002CABF0` and `0x00566C10` take their bits and clear them |
| `+0xDEA` | `u8` | panelsHidden | 1 while the License Board or the Clan Primer covers the Party Menu: `0x00561DC0` (from the License Board member pick `0x00560910`) and `0x005738D0` (Clan Primer, `0x00572F31` with 1, `0x00573A36` with 0) store it (`0x00561DCF`, `0x005738E1`), store it in the second-pass switch `0x0208F568` (`0x00247920`, `0x00561DD5`, `0x005738E7`) and write it to bit `0x1000000` of widget `+0x40`, the second-draw-pass bit. `0x00561DC0` does so through `0x00247730`, which also walks the children, on the Party Menu's name, list and four-pane panels and on the widgets `0x00295CF0` and `0x0028F570` answer (`0x00561DE9`-`0x00561E50`). `0x005738D0` does so through `0x00247730` on pane `+0xE8` of the Clan Primer's back panel [`0x02CA9718`] and on the widget `0x0028F570` answers (`0x0057391F`, `0x00573969`), and inline, on the one widget, on the help window `+0x110` and on the widget at `+0xE0` of the mid pane `+0xF8` (`0x005738FF`-`0x0057390E`, `0x00573943`-`0x00573952`); the Party Menu's panels then stay in the first pass. A widget is drawn in the pass its bit names, and the second pass runs only while `0x0208F568` is not 0 (`0x0024623A`-`0x0024624B`, `0x0025299E`-`0x002529CE`); `0x0057A040` returns 0 at once while this byte is 0 (`0x0057A073`) |
| `+0xDEB` | `u8` | commitGambits | set to 1 by the script verb fsmenu_registrestore while an area controller is open (`0x00511AA0`-`0x00511AB4`, `0x002D7D47`) and cleared by `0x002D6F90` (`0x002D6FE5`); while it is set, the gambit editor writes the copy of the set it kept at load (`+0x128`, `0x005695CE`-`0x005695F7`) back to the member when it closes (`0x00569242`-`0x00569259`) (Gambits screen) |
| `+0xDEC` | `u8` | blinkOff | non-zero stops the menu's pulsing marks: `0x002CC8D0` then returns the base value instead of base + amplitude x sin (`0x002CC8E5`-`0x002CC8F9`); the script verb fsmenu_blinkanchor writes its argument xor 1 (`0x00511B15`-`0x00511B24`, `0x002D7D37`); the auto window and the highlight window clear it around their own pulse and restore it (`0x002D684E`-`0x002D687D`, `0x002D6E2C`-`0x002D6E4D`) |
| `+0xDED` | `u8` | startHold | the Start presses still to swallow after an event skip: the event-skip task sets 3 when it ends (`0x00228210`), and the Start handler `0x002287D0`, with no event-skip task and no area controller, takes one off and does nothing else while it is above 0 (`0x0022884B`-`0x0022885E`) |
| `+0xDEE` | `u8` | savedMusicVolume | the music volume to bring back when the menu closes: the mode-screen task stores the volume `0x002DE350` reports when it opens a menu and, when it is above 50, fades the music to 50 over 60 frames (`0x002DEE50`; `0x0027FEC8`-`0x0027FEF6`, `0x0027FF1C`-`0x0027FF4A`), otherwise stores 0; the Party Menu (`0x00281206`-`0x0028122D`) and the return to the menu (`0x002815A2`-`0x002815C1`) fade it back and clear this; `0x0027EFA0` clears it for a game over (`0x0027F00C`) |
| `+0xDEF` | `u8` | modeScreenOpening | 1 while a mode screen is opening: set by the mode-screen task (`0x0027FDC0`, `0x0027FFBC`) and `0x0027EFA0` (`0x0027F01F`), cleared by the area controller (`0x00280292`); `0x00254A70` returns it (`0x00254A77`) (Screen fades) |
| `+0xDF0` | `i32` | openLength | the length of the screen's opening run: the mode-screen task stores 1 when the request word has bit `0x8000` and 200 otherwise (`0x0027FD83`-`0x0027FDAB`, through `0x002CC9F0`); `0x002CC9B0` returns it for the location map, the World Map, `0x005542D0` and `0x00581310` (`0x002BB194`, `0x005529F2`, `0x0055491D`, `0x00581333`), which hand it to `0x002CC960` or `0x002CC9C0` |
| `+0xDF4` | `i32` | shopArenaPending | 1 after the mode-screen task opens a shop (`0x0027FCCE`): the area controller's message `0x12` then puts arena 11 back to mode 0 through `0x0024AB60` and clears this (`0x0028018B`-`0x002801A4`) (Resource arena) |
| `+0xDF8` | `i32` | chosenEntry | the Party Menu entry chosen last, its menu_command.bin id: the Party Menu writes it (`0x00280E30`, `0x002810FC`); the Equip comparisons test it for Equip, `0x4B6` (`0x00293791`, `0x002943CA`, `0x00294F3E`, `0x00295554`, `0x00295ACB`) (Menus) |
| `+0xDFC` | `u8[4]` | tail | read and written by no function; nothing fixes its width |

The layout units of `layoutUnits` and the functions that read them:

| Unit | Offset | Read by |
|---:|---|---|
| 0 | `+0x00` | `0x0029CB50` (`0x0029CB57`) |
| 1 | `+0x08` | the Battle Menu (`0x00279E20`, `0x0027C870`), the party list and its children (`0x00298250`, `0x00299090`, `0x00299AC0`, `0x0029A0A0`, `0x0029B700`, `0x0029BE50`, `0x0029C530`), `0x002BE0A0`, `0x002BEFB0`, `0x002BF3D0`, the escape widget `0x00366B80` and the kill-chain widget `0x003FAF10` |
| 2 | `+0x10` | the minimap `0x003C5910` and the HUD widget `0x003C9A30` with its child `0x003C95C0` |
| 3 | `+0x18` | the special-attack window's panes (`0x002D5590`, `0x002D5690`, `0x002D5830`, `0x002D5C80`, `0x002D5E00`) |
| 4 | `+0x20` | `0x0035D3F0` |
| 5 | `+0x28` | `0x003CA530`, `0x003CAE00`, `0x003CB150` |
| 6 | `+0x30` | the Quit screen `0x0027EA70`, the member list and its rows (`0x00285290`, `0x00283BB0`, `0x00284450`, `0x002858A0`), `0x002C1000`, `0x002C1E20`, `0x002C9BF0`, `0x002CA1F0`, `0x002CE7A0`, `0x002CF740`, `0x002CF940`, the location map pane `0x00403380` |
| 7 | `+0x38` | the Party Menu panels (`0x002C13C0`, `0x002C3560`, `0x002C4460`), Status and Equip (`0x002C59D0`, `0x003FE5D0`, `0x003FF360`), the member-record panel and its children (`0x002CBED0`, `0x002CA6C0`, `0x002CABF0`, `0x002CB150`, `0x002CB4B0`) |
| 8 | `+0x40` | the list item `0x00292390` and the equipment rows (`0x003FD1D0`, `0x003FD6B0`, `0x003FD860`, `0x003FEE40`) |
| 9 | `+0x48` | the Inventory panes and rows (`0x003FCD20`, `0x005636F0`, `0x00563B10`, `0x00564010`, `0x00566A70`, `0x00567200`, `0x0056DD50`) |
| 10 | `+0x50` | the gambit editor (`0x005677A0`, `0x005691E0`, `0x0056AB00`, `0x0056ADA0`, `0x0056B4D0`, `0x0056C060`, `0x0056C170`) |
| 11 | `+0x58` | the License Board grid view (`0x005595E0`, `0x005599D0`, `0x0055CD40`, `0x00560910`, `0x005618E0`) |
| 12 | `+0x60` | Config, Graphics Settings, Controls and Parameter Settings (`0x0023B330`, `0x0023B6F0`, `0x0023BD40`, `0x0023C5C0`, `0x0023CE10`, `0x0023D4F0`, `0x0023D890`, `0x0023DD10`, `0x0023EA10`, `0x00240AD0`) |
| 13-16 | `+0x68`-`+0x80` | `0x0051EDC0(n)`, which returns unit 13 + n (`0x0051EDC0`-`0x0051EDF0`), called from `0x00406A60` and `0x00406E80` |
| 17 | `+0x88` | `0x0029CB70` (`0x0029CB77`) |
| 18 | `+0x90` | the gil window `0x002A1FB0` |
| 19 | `+0x98` | the License Board chooser (`0x00556DB0`, `0x00556F90`, `0x00558CE0`) |
| 20 | `+0xA0` | `0x0027E9D0`, called from `0x001D7150` |
| 21 | `+0xA8` | the on-screen keyboard `0x002878E0` ([On-screen keyboard](../Controls-And-Input/on-screen-keyboard.md)) |
| 22 | `+0xB0` | `0x0029CB60` (`0x0029CB67`) |

`areaFlags` (`+0x400`), the area controller's word ([Game over](../World-Areas-And-Travel/game-over.md)):

| Bits | Meaning |
|---|---|
| `0xFF` | the controller's state: 0 when it opens (`0x00280453`); its step runs state 1 (`0x00280357`), which ends in 2 (`0x002803CC`), and state 2 (`0x002802C8`); `0x0027F2E0` writes 2, or 1 when bit `0x200` is set and bit `0x400` clear (`0x0027F31E`-`0x0027F33B`) |
| `0x100` | a field change is requested: set with `requestedField` by `0x00285EC0` (`0x00285EC7`), and with field 0 by the controller's state 1 (`0x002803A3`-`0x002803B3`); cleared by the controller when it closes (`0x0028024E`), and by the event-skip task's message 18 when bit `0x2000` is clear, which then calls `0x003603E0` (`0x002281CC`-`0x002281D9`) |
| `0x200`, `0x400` | set together by `0x00285E60` (`0x00285E6B`, `0x00285E7C`); cleared by the controller's state 1 after it resets the save image (`0x00280380`-`0x00280395`), and bit `0x200` makes the controller's close restore the world (`0x002801E4`-`0x00280246`) |
| `0x800` | bit `0x8000` of the request that opened the controller (`0x00280481`-`0x0028049B`); `0x0027F2E0` closes slot 0 over 1 frame instead of 200 while it is set, then clears it (`0x0027F2F2`-`0x0027F301`, `0x0027F349`) |
| `0x1000` | set by the event-skip task when it opens (`0x00228295`) |
| `0x2000` | set or cleared by `0x00285EA0(on)` (`0x00285EAA`-`0x00285EB6`), cleared by the event-skip task when it opens (`0x002282A3`) and, after `0x00360880()`, by its message 18 when it is set (`0x002281B1`-`0x002281C3`); the pause task's state 4, the skip, calls it with 1 (`0x0022917A`) |
| `0x4000` | passed to `0x00244630` when the event-skip task ends (`0x002281FB`-`0x00228204`); none of the writers above sets it |

The pause task `0x00228C70` steps on its word `+0xE6` through the table at `0x002294EC`¹: 1
`0x00228E96`, 2 `0x00229073`, 3 `0x002290D9`, 4 `0x00229159`, 5 `0x00229196`, 6 `0x00229093`, 7 `0x002291CD`. State 2 closes the
task: it clears `+0xE6` and calls `0x00244F00(task)` and `0x00227DD0(100)`². State 4, the skip:
when `0x002CCC70(2)` answers non-zero it clears `+0xE6` and calls `0x00285EA0(1)`, `0x00244F00(task)` and `0x00227DD0(1)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00228E76`-`0x00228E94` |
| ² | `0x00229073`-`0x00229087` |
| ³ | `0x00229159`-`0x0022918A` |

</details>

State 5, once `0x002EFD20(2)` answers 2, clears `+0xE6` and calls `0x00285EC0(0x0C)`, which requests field `0x0C`, the
title map, then `0x00244F00(task)` and `0x00227DD0(1)`¹. State 7 clears `+0xE6`, calls
`0x00244F00(task)` and `0x00227DD0(1)`, then `0x002EFA70(0, 0, 0, 0)` and `0x00227E20`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00229196`-`0x002291C1` |
| ² | `0x002291CD`-`0x00229215` |

</details>

When the confirmation box of menu text `0x85F` or `0x890` answers `0x8100` (message 12), state 6 leads on to states 3
and 5 or to state 7¹: returning to the title and quitting. Its answers
`0x8101` and `0x8102` store 6 in `+0xE6` and 1 in `+0xE8`², and state 6 then leads back to
state 1³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002293E4`-`0x0022940A`, `0x0022921A`-`0x002292B4` |
| ² | `0x00229226`-`0x00229243` |
| ³ | `0x002290A2`-`0x002290CB` |

</details>

`0x00227DD0(n)` passes `n * 60 / 1000` to `0x00251EE0`, which writes it to word `+0x122` of the object at `[0x020927F0]`
when there is one, and calls `0x00250F30`¹; then, when `[0x0209AC30] + 0xC8` holds the event-skip
task, it writes 2 to that task's `+0xCC`². The pause task's closing states 2, 4, 5 and 7 all
call it, so the event-skip task's `+0xCC` becomes 2 whichever was chosen; of them state 4 alone sets bit `0x2000`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00227DD4`-`0x00227DED` |
| ² | `0x00227DF2`-`0x00227E05` |

</details>

The event-skip task zeroes its `+0xCC` when it opens, on message 1¹. On message 2, when its `+0xCC` is 2,
`0x00251D50()` answers non-zero and `[0x0209AC30] + 0xD0` is null, it releases itself through `0x00245020` and zeroes
`+0xCC`². Its message 18 calls `0x00360880()` and clears bit `0x2000` when that bit is set, else,
when bit `0x100` is set, clears it and calls `0x003603E0()`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00228277` |
| ² | `0x0022821F`-`0x00228258` |
| ³ | `0x002281A7`-`0x002281D9` |

</details>

`partyFlags` (`+0xD3C`), rebuilt by `0x00283270` each time it rebuilds the party records:

| Bit | Set when | Read by |
|---:|---|---|
| `0x1` | some member's gambit set has more than 10 slots (byte `+0x32` of the copy `0x00327BE0` makes, `0x00283406`-`0x00283423`; [Gambits screen](gambit-screen.md)) | the gambit editor (`0x00569482`) |
| `0x2` | a guest is in the party (record flag bit `0x2`, `0x002833E0`-`0x002833ED`) | the guest portrait (`0x002CE998`, `0x002CEAEB`) |
| `0x4` | the party is riding a chocobo (`0x00303EE0`, `0x002832DC`-`0x002832F8`) | the member list, which refuses party changes with "You cannot change party members while mounted" (`0x0BE1`, `0x00285DEB`-`0x00285DF5`; `0x00284CD4`) |
| `0x8` | an Esper is summoned (`0x003135E0`, `0x002832FE`-`0x0028331A`) | the member list ("You cannot remove a summoner with an active Esper from the party", `0x0BE2`, `0x00285DFC`-`0x00285E06`; `0x00284CDC`), `0x002830A0` (`0x002830AB`) and `0x002CF710` (`0x002CF717`) |
| `0x10` | a member pick shows only the six main characters: the License Board pick sets it when it opens and clears it when it leaves (`0x00560A4E`, `0x005609CB`), the member-record panel writes it as the inverse of bit `0x8` of its creation record's `+0x10` word (`0x002CC07E`-`0x002CC097`), and the name panel saves, clears and restores it (`0x002C153A`-`0x002C1581`) | the member steps (`0x0027ED47`, `0x0027EDEA`, `0x0027F3A2`-`0x0027F3C7`, `0x0027F486`) and the panels `0x002CBC50`, `0x002CC2A0`, `0x002CC660` (`0x002CBCDF`, `0x002CC31F`, `0x002CC392`, `0x002CC6FF`), which skip guests and members past id 5 |
| `0x20` | bit `0x400` of the combined action availability mask `0x002E0FA0()`, set in towns ([Action availability](../Controls-And-Input/action-availability.md); `0x0028332E`-`0x00283348`) | no instruction tests it |

`stepFlash` (`+0xDE9`), which step arrow flashes for 4 frames:

| Bit | Set by | Taken by |
|---:|---|---|
| `0x1` | a step to the next member (`0x0027F3FF`, `0x0027F4F1`) | the member-record panel's child `0x002CABF0`, its `+0xEA` (`0x002CADAC`-`0x002CADE3`) |
| `0x2` | a step to the previous member (`0x0027ED71`, `0x0027EE2C`) | `0x002CABF0`, its `+0xE8` |
| `0x4` | a step to the next tab (`0x00564300`: `0x00564344`, `0x00564366`) or gambit page (`0x0056AD50`: `0x0056AD80`) | the gambit icon `0x00566C10`, its `+0xE4` (`0x00566D72`-`0x00566DA9`) |
| `0x8` | a step to the previous tab (`0x00563EC0`: `0x00563EFD`) or gambit page (`0x0056AAC0`: `0x0056AAE1`) | `0x00566C10`, its `+0xE2` |

The equipment rows that `0x0027F210` fills, five from `+0xD40` 32 bytes apart (Weapon, Off-hand, Helm, Armor,
Accessory), and the description window at `+0x2F8`:

`MenuEquipSlotRow` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name | the piece's name, `0x002B58B0` of the item's text (`0x0027F28C`-`0x0027F295`); read by no function |
| `+0x08` | `u16` | id | the piece's item id, `0xFFFF` for an empty slot (`0x0027F259`-`0x0027F271`); read by the equipment screens (`0x003FD3CC`, `0x003FDFE0`, `0x003FE720`, `0x003FEF01`, `0x003FF0C7`, `0x003FF8AA`, `0x003FF94C`) and `0x0027F030` |
| `+0x0A` | `u8` | icon | the item's icon, its query record's `+0x2C` (`0x0027F299`-`0x0027F29D`); read by no function |
| `+0x0B` | `u8` | class | the item's class, the query record's `+0x38` (`0x0027F2A2`-`0x0027F2A6`); read by `0x003FD360` for the weapon (`0x003FD48B`) and `0x0027F030` for the off hand (`0x0027F0B0`) |
| `+0x0C` | `u8[20]` | zero | cleared by the fill (`0x0027F262`-`0x0027F26C`) and read by no function |

`MenuDescriptionWindow` (`0xD8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets); procedure `0x00293010` |
| `+0xC0` | `void*` | box | the description box, the `0x102D0`-byte list item `0x00292390` that `0x00293170` creates and keeps here (Inventory screen); 0 when the window opens (`0x00293049`) |
| `+0xC8` | `i8` | iconShown | the icon picture the box shows last: -1 when the window opens (`0x00293050`), and the box copies icon r into its picture only when r differs, then stores r (`0x0029277B`-`0x002927A5`); `0x0029289C` passes it to `0x01E0C480` |
| `+0xC9` | `u8` | iconHalf | which half of the icon picture the box writes next: 0 when the window opens (`0x00293050`); the box uploads at row offset this x 64 (`0x002925BD`-`0x002925C4`, `0x002927F0`-`0x002927FC`, `0x002929A1`-`0x002929A8`) and flips it after each upload (`0x00292634`, `0x0029290B`, `0x00292A28`) |
| `+0xCA` | `u8[2]` | gap0CA | read and written by no function; nothing fixes its width |
| `+0xCC` | `i32` | width | 0 when the window opens (`0x00293059`); `0x002932F0`(n) writes n (`0x00293303`), which the Inventory uses to size the line to its widest category name (Inventory screen); read by no function |
| `+0xD0` | `i32` | mode | the window's mode from the opening message's argument: 1 gives 6, 2 gives 4, 3 gives 5, 4 gives 7 and any other 1 (`0x0029305F`-`0x002930A3`); read by no function |
| `+0xD4` | `u8[4]` | tail | read and written by no function; nothing fixes its width |

### Static values of three screens

The Party Menu's name panel `0x002C13C0` copies its layout record's fields into six globals on message 1¹. On message 4 it clips the current member's name to a rectangle at the panel's position plus
these offsets and draws it, scrolling it while bit `0x10000` of the name entry's `+0x18` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002C1448`-`0x002C148C` |
| ² | `0x002C1649`-`0x002C1756` |

</details>

The language test `0x00254A10`, true for the `kr`, `ch`, `jp` and `cn` settings, picks one of two left offsets and one
of two widths. `0x002C38B0` and `0x002C4720`, which build the name entries of the list and four-pane panels, set bit `0x10000` of an
entry when the name is wider than the width the same test picks, a signed 32-bit compare¹.
The rectangle takes each value's low 16 bits; the text position takes the whole `i32`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002C3A32`; `0x002C48B2`, `0x002C4A53`, `0x002C4CBD`, `0x002C4F2B` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01E0CEBC` | `i32` | 128 | the name's left offset when the language test is true: the record's `+0x0C` (`i16`) | `0x002C13C0` (`0x002C1457`) | `0x002C13C0` (`0x002C1682`) |
| `0x01E0CEC0` | `i32` | 116 | the left offset otherwise: the same `+0x0C` | `0x002C13C0` (`0x002C1461`) | `0x002C13C0` (`0x002C1675`) |
| `0x01E0CEC4` | `i32` | 33 | the top offset, `+0x0E` (`i16`), also the text's y | `0x002C13C0` (`0x002C146B`) | `0x002C13C0` (`0x002C1697`, `0x002C1708`, `0x002C173D`) |
| `0x01E0CEC8` | `i32` | 340 | the clip width when the language test is true: `+0x10` (`u16`) | `0x002C13C0` (`0x002C1475`) | `0x002C13C0` (`0x002C16B8`); `0x002C38B0` (`0x002C39B0`); `0x002C4720` (`0x002C483F`) |
| `0x01E0CECC` | `i32` | 352 | the clip width otherwise: `+0x10` less 12 | `0x002C13C0` (`0x002C1482`) | `0x002C13C0` (`0x002C16A8`); `0x002C38B0` (`0x002C399D`); `0x002C4720` (`0x002C4828`) |
| `0x01E0CED0` | `i32` | 55 | the clip height, `+0x12` (`u16`) | `0x002C13C0` (`0x002C148C`) | `0x002C13C0` (`0x002C16B1`) |

The record is `[[panel + 0x60] + 0x100]`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002C1448`-`0x002C144C` |

</details>

For the Equip screen's Optimise preview, `0x003FE720` with mode `0x402` stores the set `0x002F9F20` builds: slots 0-3 as
eight bytes at `0x02B5F210`¹ and slot 4 in the global below. The equipment row painter `0x003FF1F0` reads the
word of slot *i* of `0x02B5F210` for row *i* while its pane's `+0x178` is `0x402`, and shows that item in place of the
worn one when they differ².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003FE82E` |
| ² | `0x003FF25A`-`0x003FF2BB` |

</details>

The menu background gradient `0x002CE7E0`, on message 18, tests the global `0x02CA972C`. When it is not 0 it clears it
and has `0x00577BD0` send message 16 to the Clan Primer widget at `[0x02CA9730]`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CE848`-`0x002CE85A` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B5F218` | `u16` | 0 | the Optimise set's accessory, slot 4; `0xFFFF` for no accessory | `0x003FE720` (`0x003FE839`) | `0x003FF1F0`, row 4 (`0x003FF280`, through `0x02B5F210` + 2 × row) |
| `0x02CA972C` | `u32` | 0 | stays 0: the one store, `0x002CE854`, writes 0, so the gradient never sends the message | `0x002CE7E0`, 0 (`0x002CE854`) | `0x002CE7E0` (`0x002CE848`) |

## Columns

| Column | Meaning |
|---|---|
| `procedure` | the widget procedure |
| `size` | the procedure's code size in bytes |
| `installer` | the functions that construct it |
| `install site` | the `lea` of the procedure and the constructor call |
| `parent` | the widget procedures above the installer, `shared: n parents` for more than three, or `top (no parent)` |
| `screen` | the screen it belongs to, or `no screen` |
| `screen text id` | the shipped text that names that screen |
| `resources` | layout records (`mrppack_ys` unit and record), files and image labels it loads |
| `page` | the final page that documents it, if any |
| `role (from the body or a page)` | what the procedure does |

## Related

- [Menus](menus.md) - the requests and the router.
- [Widgets](widgets.md) - how the procedures are constructed.
- [Widget messages](widget-messages.md) - the messages they answer.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 77 calls with 10 other topics</summary>

**Enemy AI and gambits** (explained on [gambits](../Enemy-AI-And-Gambits/gambits.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00283270`](menu-screens.md) | calls | [`0x00327BE0`](menu-screens.md) Gambit config: copy base pair set for stats index |

**Steam and achievements** (explained on [achievements](../Steam-And-Achievements/achievements.md), [gil](../Rewards-EXP-Gil-And-Loot/gil.md), [frame update order](../Engine-Core/frame-update-order.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00282FA0`](menu-screens.md) | is called by | [`0x003162E0`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316760`](../Steam-And-Achievements/achievements.md) (on achievements) |
| [`0x00283270`](menu-screens.md) | is called by | [`0x00316930`](../Steam-And-Achievements/achievements.md) (on achievements) |
| [`0x00305A00`](menu-screens.md) | calls | [`0x00316C60`](menu-screens.md) |
| [`0x0056D370`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) | calls | [`0x00316A50`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Rewards: EXP, LP, gil and loot** (explained on [item and ability ids](../Engine-Core/item-and-ability-ids.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002A1FB0`](message-windows.md) (on message windows) | calls | [`0x00253690`](party-list.md) Game state: get gil (on party list) |
| [`0x002CE7A0`](menu-screens.md) | calls | [`0x00253690`](party-list.md) Game state: get gil (on party list) |
| [`0x003058B0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) | calls | [`0x00254EE0`](../Engine-Core/debug-menu.md) Game state: set gil (on debug menu) |
| [`0x0056D370`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) | calls | [`0x00253690`](party-list.md) Game state: get gil (on party list) |

**Scripts and script commands** (explained on [gambit screen](gambit-screen.md), [generated function families](../Compiler-And-C-Runtime/generated-function-families.md), [license board screen](license-board-screen.md), [music table](../Sound-And-Music/music-table.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [starting inventory](../Party/starting-inventory.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00280120`](menu-screens.md) | is called by | [`0x00510950`](menu-screens.md)<br>[`0x00510990`](menu-screens.md)<br>[`0x005109B0`](menu-screens.md)<br>[`0x00510A40`](menu-screens.md)<br>[`0x00510AA0`](menu-screens.md)<br>[`0x00510AE0`](menu-screens.md)<br>[`0x00510B40`](menu-screens.md)<br>[`0x00510B80`](gambit-screen.md) (on gambit screen)<br>[`0x00510C80`](menu-screens.md)<br>[`0x00510E40`](menu-screens.md)<br>[`0x00510F30`](menu-screens.md)<br>[`0x00511010`](menu-screens.md) |
| [`0x00280120`](menu-screens.md) | is also called by | [`0x00511200`](menu-screens.md)<br>[`0x00511360`](menu-screens.md)<br>[`0x005113A0`](../Compiler-And-C-Runtime/generated-function-families.md) (on generated function families)<br>[`0x005113D0`](menu-screens.md)<br>[`0x00511400`](menu-screens.md)<br>[`0x00511430`](menu-screens.md)<br>[`0x00511460`](menu-screens.md)<br>[`0x00511490`](menu-screens.md)<br>[`0x005114C0`](menu-screens.md)<br>[`0x00511510`](../Compiler-And-C-Runtime/generated-function-families.md) (on generated function families)<br>[`0x00511550`](menu-screens.md)<br>[`0x005115B0`](menu-screens.md) |
| [`0x00280120`](menu-screens.md) | is also called by | [`0x005115E0`](menu-screens.md)<br>[`0x00511660`](menu-screens.md)<br>[`0x005116E0`](menu-screens.md)<br>[`0x00511730`](menu-screens.md)<br>[`0x005117B0`](menu-screens.md)<br>[`0x00511850`](menu-screens.md)<br>[`0x005118D0`](menu-screens.md)<br>[`0x00511920`](menu-screens.md)<br>[`0x005119C0`](menu-screens.md)<br>[`0x00511A10`](menu-screens.md)<br>[`0x00511AA0`](menu-screens.md)<br>[`0x00511B00`](menu-screens.md) |
| [`0x00280120`](menu-screens.md) | is also called by | [`0x00511B70`](gambit-screen.md) (on gambit screen)<br>[`0x00511C30`](menu-screens.md)<br>[`0x00511C80`](menu-screens.md)<br>[`0x00511CD0`](menu-screens.md)<br>[`0x00511D30`](menu-screens.md)<br>[`0x00511D60`](menu-screens.md)<br>[`0x00511DA0`](menu-screens.md)<br>[`0x00511E60`](menu-screens.md)<br>[`0x00511EE0`](menu-screens.md)<br>[`0x00511F50`](license-board-screen.md) (on license board screen)<br>[`0x00511FE0`](license-board-screen.md) (on license board screen)<br>[`0x00512030`](menu-screens.md) |
| [`0x00280120`](menu-screens.md) | is also called by | [`0x00512080`](menu-screens.md)<br>[`0x005120C0`](menu-screens.md)<br>[`0x00512100`](menu-screens.md)<br>[`0x00512140`](menu-screens.md)<br>[`0x00512180`](menu-screens.md) |
| [`0x002D7710`](menu-screens.md) | is called by | [`0x00511200`](menu-screens.md) |
| [`0x002D7800`](menu-screens.md) | is called by | [`0x00510AA0`](menu-screens.md)<br>[`0x00510B40`](menu-screens.md) |
| [`0x002D7840`](menu-screens.md) | is called by | [`0x005120C0`](menu-screens.md) |
| [`0x002D78B0`](menu-screens.md) | is called by | [`0x005109B0`](menu-screens.md) |
| [`0x002D7B40`](menu-screens.md) | is called by | [`0x005117B0`](menu-screens.md)<br>[`0x00511920`](menu-screens.md) |
| [`0x002D7CB0`](menu-screens.md) | is called by | [`0x00510A40`](menu-screens.md)<br>[`0x00510AE0`](menu-screens.md) |
| [`0x002DEE50`](../Sound-And-Music/music-table.md) (on music table) | is called by | [`0x00340260`](../Sound-And-Music/music-table.md) (on music table)<br>[`0x00345B60`](../Sound-And-Music/music-table.md) (on music table) |
| [`0x0037CB50`](menu-screens.md) | is called by | [`0x0034E3E0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) |
| [`0x00394460`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x00511EA0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |

**World, areas and travel** (explained on [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0035D530`](menu-screens.md) | is called by | [`0x003C63A0`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |

</details>
