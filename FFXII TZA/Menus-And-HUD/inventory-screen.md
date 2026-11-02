---
title: "Inventory screen: the category rows, the item tabs and their rows, the help line, moving an item to a new place, and the tab strip"
kind: "system"
category: "Menus and HUD"
addresses: "0x00565E00, 0x005651E0, 0x00564C80, 0x00564E10, 0x005641F0, 0x00564D30, 0x00565BD0, 0x00564650, 0x005674B0"
---

## What the player sees

The Inventory lists Items, Weapons, Armor, Accessories, Ammunition, Abilities, Loot and Key Items, each once the
party has owned something of that kind. Choosing a category shows its items with their counts and a help line
for the item under the cursor. Confirming an item picks it up; moving the cursor and confirming again drops it
there, and the new order is kept. The sort bar offers Auto-sort, By Strength and By Quantity. Returning to a
category puts the cursor back on the item last looked at.

## How it works

### The category rows

`0x00565E00` is the screen's procedure; `0x00565DD0` builds it once ([Widgets](widgets.md)). On message 1 it stores
itself at `[0x0209AC30] + 0x168` and adds one row per category whose save-wide flag is set (`0x00252D10`), with its
help text:

| Category (`menu_command.bin`) | Flag | Help |
|---|---:|---|
| Weapons `0x405` | 1 | `0xBE9` |
| Armor `0x406` | 2 | `0xBEA` |
| Accessories `0x407` | 8 | `0xBEB` |
| Ammunition `0x408` | 3 | `0xBEC` |
| Items `0x409` | 4 | `0xBED` |
| Abilities `0x40D` | 5 | `0xBF1` |
| Loot `0x40E` | 6 | `0xBF2` |
| Key Items `0x40F` | 7 | `0xBF3` |

The rows form three groups, Key Items and Loot, then Abilities and Items, then Weapons, Ammunition, Armor and
Accessories; each group is moved down by the gap `0x01E0C3B4` for every earlier group that has a row (`0x002CA0E0`). A
row whose category `0x002CDAE0` reports is drawn in colour 2, and a category not yet visited carries the mark of
`0x002CDE20` ([Menu screens](menu-screens.md)).

Message 12 takes three sub-commands:

- `0x8000`, the cursor moved: it closes the previous category's pane (`0x00563FC0`), opens the new one (`0x00564B90`)
  and sizes the help line to the category's widest name (`0x00564430`, kept per category at `+0x1E8`; `0x002932F0`);
- `0x8001`, confirm on a row in colour 0: it marks the category visited (`0x002CDE50`), gives its pane the focus
  (`0x005659B0`) and stores the category (`0x002527B0(6, 1, id)`);
- `0x8002`, cancel: it closes the screen's list and the open pane (`0x00563FC0`).

`0x00563FC0(id)` closes a category's pane: it sets the pane's `+0x40` bit `0x40` and either hides it (`0x00244DD0`, when
bits `0x1` and `0x20` are set) or sends it message `0x00915058` and releases it (`0x00245020`). Message 18 returns to the menu
(`0x002814E0(0x4B8)`) and clears `[0x0209AC30] + 0x168`.

### The tab panes

The tab panes that `0x00564B90` builds (procedures `0x005636F0`, `0x00563930`, `0x00563B10`, `0x00563D20`) hand their messages
to the shared procedure `0x005651E0`. The pane of a category lives at `[0x0209AC30] + 0x170 + 8 x slot`, where the table
`0x00D233A0` gives the slot: categories `0x405`-`0x409` and `0x40D`-`0x40F` take slots 0 to 7, and the keys
`0x597`-`0x5AF` take 8 to 32 (the tab sets of the [Shop screens](shop-screens.md)). `0x00564A60`, `0x00565190` and `0x005659B0` look a category's pane up there:

- `0x00564A60(id)` answers whether the pane has rows (`+0xE0`);
- `0x00565190(id)` runs the pane's input step `0x00564E10(pane, 1)`;
- `0x005659B0(id)` gives the pane focus (`0x00244640`, `0x00244830`), or hands it to `0x002286B0` when `0x00228480` returns non-zero and
  `[0x0209AC30] + 0x308` is empty.

`0x005639D0` and `0x00563C00` are the row callbacks the create records of `0x00563B10` and `0x00563D20` carry (`0x00563B59`,
`0x00563D5B`), called as `(pane, element, _, n)`; both return 1:

- without a row table `+0xE0`, they clear the element list (`0x00243580`) and show the text node (`[[element + 0x10] +
  8]`, bit `0x1` of `+0x08`) with the string `0x002F9860(0x7D8)`, the colour `0x0020E620(0)`, x = the template's `+0x04` -
  20 and y = its `+0x06`;
- with rows (`0x20` bytes from `+0xE0`), the icon node (`[[element + 0x10]]`) is shown when the row's byte `+0x0A` is
  not `0xFF`, with that cell and `+0x39` from the palette table, else hidden; the text node takes the row's string
  `+0x00`, `0x0020E620(0)`, the template position and, at `+0x24`, `0x002DD7E0(6)` when the pane's `+0x180` has bit
  `0x100` and its word `+0x17C` equals `n`, else `0x002DD7E0(0)`;
- `0x005639D0` also runs `0x003FCAD0(element, row, 2, 7)`.

`0x005651E0` answers:

| Message | Does |
|---|---|
| 8, focus | `0x00563DC0` |
| 9, blur | hides the list's cursor |
| 10, tick | `0x00564C80` |
| 12 `0x8000` | the cursor moved: `0x00563F10` shows its help |
| 12 `0x8001` | picks the item up: `0x005641F0` |
| 12 `0x8002` | cancel: clears the help (`0x00293110(0, 0)`) and gives the focus back |
| 12 `0x8004` | `0x00564650` ends a move |
| 18 | frees the rows and clears its slot |
| `0x11E` | `0x00565720` rebuilds the rows |
| `0x1A` | slides a row aside while an item is held |

### A pane's tabs

`0x00564780(pane, kind, ...)` fills a pane's tab slots:

- it stores the kind at `+0x17E` and `+0x17F`, keeps the kind's tab list from `0x01F2CB90` at `+0xE8`, sets `+0x17C`
  to -1 and clears the tab count, mask `0x1F0000` of `+0x180` (`0x005647AD`-`0x005647F4`);
- for each tab in the list that passes its check (`0x00252D10` for kinds 0 to 7, then `0x0057D610`), it fills the slot at
  `+0xF0` + 8 x count and adds 1 to the count (`0x0056486D`-`0x00564898`, `0x0056493F`-`0x00564966`);
- a slot holds at `+0` the value `0x002526F0(8, ...)` keeps for the tab, or `0xFFFF` when that is 0, for kinds 0 to 7
  (`0x005648D9`-`0x005648E9`), and `0xFFFF` for the others (`0x00564992`); `0xFFFF` at `+2` and `+4`; the tab's place in the
  list at `+6`; and the tab's id at `+7` (`0x005648B8`-`0x005648D1`, `0x00564971`-`0x00564989`);
- after the last tab it writes `0xFF` to the next slot's `+6` as the end mark (`0x005649D4`), clears the selected tab,
  mask `0x3E00000` of `+0x180`, and for kinds 0 to 7 selects the tab whose id is the one `0x002526F0(8, kind + 0x40)` keeps
  (`0x005649DC`-`0x00564A4C`).

The count and the selection are read as signed 5-bit numbers (`0x00564875`-`0x00564882`, `0x005649CA`-`0x005649D0`), so a slot
index runs from 0 to 15 (`+0xF0`-`+0x16F`), and with the end mark the strip holds 15 tabs. The lists at `0x01F2CB90`
for kinds 0 to 37 hold at most 9 tabs (kind 32, `0x00D23C70`).

### Rows

`0x00565720(pane, id)` frees the old rows and builds the tab's rows with `0x0057CF20`, the builder of the shop lists
([Shop screens](shop-screens.md)). It then puts the cursor back on the remembered item: the row whose id is the one
kept for the tab, scrolled into view (`0x002D1820`, `0x002D47C0`). `0x00565A00` does the same inside `0x005655F0`, the row
builder that the shop tabs and the Inventory's tab switch share.

The row painters `0x00563560` and `0x005637D0` draw a row: the icon frame `+0x0A` (no icon for `-1`), the name `+0x00`, and
numbers through `0x0029FF60`: `0x00563560` writes `+0x0E` less `+0x0C` and `+0x0E`, `0x005637D0` only `+0x0E`. The held row
is drawn in colour 6. An empty tab shows text `0x7D8`.

`0x00564430(id)` returns the widest name of a category's items (`0x00292B70`, `0x002B3050`): one list for each category,
two for Abilities.

| Category | Lists (`0x00252F40`) and kind |
|---|---|
| Weapons | 1, kind 1 |
| Armor | 2, kind 3 |
| Accessories | 3, kind 5 |
| Ammunition | 4, kind 3 |
| Items | 0, kind 8 |
| Abilities | 9 kind 6, 8 kind 7 |
| Loot | 11, kind 9 |
| Key Items | 10, kind 10 |

### The help line

`0x00563F10(pane, row)` shows the help of the item under the cursor, `0x00293110(0x00D23962[tab], id << 16)`, unless the
pane holds an item (`+0x180` bit `0x100`) or bits `0x4000000` or `0x20000000` are set; `0x00563DC0` does the same on focus and then shows the
cursor. The tab of a pane is `0x00564380`.

### The description box

`0x00293170(kind, id, a, b)` fills the description box. It works through the window at `[0x0209AC30] + 0x2F8` and the box
at that window's `+0xC0`:

1. While the window is 0 it does nothing (`0x002931AE`).
2. When the box exists, it closes the box (`0x00244DD0`). First it installs the animation descriptor `0x00916058` when
   `a` is set and `0x00916030` when `b` is set (`0x00247570`).
3. Kind 0 stops there.
4. Otherwise `0x00292B70` composes the line ([Text codes](text-codes.md)). When there is no line, it stops with the box
   closed.
5. With no box yet, it creates one through `0x00244F50`: a `0x102D0`-byte list item with procedure `0x00292390`
   ([AS7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md)), kept at the window's `+0xC0`. An
   existing box is sent the line and the entry as message 12 (`0x00247510`, [Widget messages](widget-messages.md)). If
   bit `0x20` of the box's `+0x7C` is clear, it stops instead.
6. It installs `0x00916058` again when `a` is set, then opens the box under the window (`0x00246AD0`).

`0x00293110(kind, id)` calls it with `b` = 0. `a` is bit `0x1` of the box's `+0x40`, or 0 when there is no box. The one
exception is `0x00293110(0, 0)`, which passes `b` = 1, so it only closes the box. `0x00293100(kind, id, a)` passes `b` = 0.

Every caller, and the kind it passes. The id is in the high word unless the row says otherwise:

| Caller (call site) | Where | Kind |
|---|---|---|
| `0x00563F10` (`0x00563F7D`), `0x00563DC0` (`0x00563E42`) | Inventory, the item under the cursor | word `+2` of the tab's 4-byte record at `0x00D23960`: Weapons 1, Armor 3, Accessories 5, Ammunition 2 (the kind `0x00292B70` narrows ammunition to; `0x00564430` passes 3), Items 8, Loot 9, Key Items 10; Abilities 6, or 7 when byte `+0xF7` of the pane's current entry is 15 (`0x005643E2`-`0x00564407`) |
| `0x0056E5D0` (`0x0056E6C9`, through `0x00293100`) | shops | `0x00D235D8[help kind]`: help kinds 0 to 11 give 1, 3, 5, 2, 8, 7, 6, 9, 11, 12, 13 and 15 |
| `0x003FDFE0` (`0x003FE2D5`) | Equip, the slot list | word `+2` of the slot's 4-byte record at `0x00D23988`: Weapon 1, Off-hand 3, Helm 4, Armor 4, Accessory 5 |
| `0x003FF920` (`0x003FF973`) | Equip | `0x00292F60(slot)` |
| `0x002C59D0` (`0x002C5E39`) | the Status pane | 14, with the status number (the entry's byte `+0xC8`) as the whole id rather than in the high word, the form every status lookup takes (`0x0031E137`); 0 and 0 when the entry fails `0x002D02A0` |
| `0x002C59D0` (`0x002C5D84`), `0x003FF360` (`0x003FF732`), `0x005651E0` (`0x0056531A`), `0x0056C850` (`0x0056C913`), `0x0056E140` (`0x0056E283`), `0x0057B6A0` (`0x0057B6C7`) | | 0 and 0, which closes the box |

The shops' help kinds 8 and 10 (categories 12, 31 and 14) give kinds 11 and 13. Neither has a handler, so for those
goods the box closes and stays empty.

### The input step

`0x00564C80(pane)` runs every frame: while an item is held, `0x00564D30`; otherwise `0x00564E10(pane, 0)`.

- `0x00564E10` switches tabs on the buttons of `0x02F97368 & 0xCA0` (`0x00563EC0` one way, `0x00564300` the other), keeps the new tab's cursor (`0x002527B0(8, ...)`), rebuilds its rows (`0x005655F0`, `0x005674B0`) and
  plays sound 10. The extra button (bit `0x8000` of `0x02F9736A`) opens the sort bar (`0x005665B0`, sound 4), or plays sound 5
  on an empty tab ([Dialogs](dialogs.md)).
- `0x005641F0(pane, row)` picks the row's item up: it stores the row at `+0x17C` and `+0x17A`, turns the list into move
  mode (`+0xE4` bits `0x4`, `0x20000` and `0x40000`) and hides the tab arrows (`0x005670F0`).

### Moving an item

`0x00564D30(pane)` handles the held item:

1. with no held row it ends the move;
2. cancel (`0x01E0C2A4`) plays sound 3, and `0x00564C80` puts the cursor back on the held row (`0x002D4840`);
3. confirm (`0x01E0C2A0`) plays sound `0x37`, calls `0x00565BD0(pane, from, to)` when the cursor is on another row, and
   ends the move;
4. any other frame runs the list (`0x002D3900`).

`0x00565BD0` stores the new place in the tab's list (`0x002530E0(list 0x00D23960[tab], item, item at the target)`), shifts
the rows between the two places by one and puts the held row at the target, then redraws (`0x002D1AC0`). While an item
is held, message `0x1A` slides each row between the two places by 4 a frame.

`0x00564650` ends the move: it clears the
row offsets, leaves move mode, restores the tab strip (`0x00567690`), shows the key-guide entries again
(`0x00295D50(1)`, `0x00564741`), resets `+0x17C` to `-1` and clears `+0x178` and `+0x181`, zeroes `0x022CBE36`
(`0x00368A60`) and re-allows the list bounce (`0x00368830(1)`, `0x00564773`; [Menu lists](menu-lists.md)).

### The tab strip

The tab strip at `+0xC8` of a screen is shared with the shop, equipment and gambit lists (callers `0x00564159`,
`0x003FD7C8`, `0x0056AE5F`):

- `0x005674B0(strip, current)` lays the tab buttons (`+0xC8`, count byte `+0x150`) out from `+0x148`, brightens the
  current one to `0x80` and the others to `0x40` (`0x002D04F0`), and moves the marker to it (`0x00566B70`, 100 ms);
- `0x00567690(strip, current)` only recolours them; `0x005670F0` and `0x00566FE0` show the two arrows when there are at least
  two tabs, the latter also offsetting the strip by its width;
- `0x00566B70(marker, tab, x, curve, ms)` starts the marker's move to `x` over `ms x 60 / 1000` frames.

## State

The description box `0x00292390` shows an item picture by id: on message 12 it keeps the id at `+0x102C8`, and on its
next message 2 it decodes picture `id & 63` of sheet `id >> 6` and copies its `ListItemIconW` × `ListItemIconH`
pixels, 64 × 96 (`0x01E0C470`, `0x01E0C474`), into the `itemgra_c` atlas
([AS7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md)).

After the copy it stores where that picture lies in an eight-column grid of such cells (`0x002928A9`-`0x002928FE`). The id is a signed `i16`; a negative id
skips the update (`0x0029269D`), so the remainders below are taken of a non-negative id.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01E0C478` | `i32` | -1 | the last decoded picture's x in the grid: (`id` mod 64) mod 8 × `ListItemIconW` | `0x00292390` (`0x002928D3`) | no instruction names it |
| `0x01E0C47C` | `i32` | -1 | its y: (`id` mod 64) / 8 × `ListItemIconH` | `0x00292390` (`0x002928FE`) | no instruction names it |

## Modding notes

- A category appears only once its save-wide flag is set; clearing the flag hides the row.
- Moving an item writes the stored order (`0x002530E0`), so the new order survives saving.
- The shop keys `0x597`-`0x5AF` share the slot table `0x00D233A0` (slots 8 to 32).
- A pane's tab strip holds 15 tabs: the count at the bits under mask `0x1F0000` of `+0x180` is a signed 5-bit number, and a sixteenth
  tab would put the end mark below `+0xF0` (A pane's tabs, above).

## Related

- [Menu screens](menu-screens.md): the command rows and first visits.
- [Dialogs](dialogs.md): the sort bar.
- [Shop screens](shop-screens.md): the shared row builder.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md): the item counts the rows show.
- [Widgets](widgets.md): the screen widget and focus.
