---
title: "Inventory screen: the category rows, the item tabs and their rows, the help line, moving an item to a new place, and the tab strip"
kind: "system"
category: "Menus and HUD"
addresses: "00565E00, 005651E0, 00564C80, 00564E10, 005641F0, 00564D30, 00565BD0, 00564650, 005674B0"
---

## What the player sees

The Inventory lists Items, Weapons, Armor, Accessories, Ammunition, Abilities, Loot and Key Items, each once the
party has owned something of that kind. Choosing a category shows its items with their counts and a help line
for the item under the cursor. Confirming an item picks it up; moving the cursor and confirming again drops it
there, and the new order is kept. The sort bar offers Auto-sort, By Strength and By Quantity. Returning to a
category puts the cursor back on the item last looked at.

## How it works

### The category rows

`00565E00` is the screen's procedure; `00565DD0` builds it once ([Widgets](widgets.md)). On message 1 it stores
itself at `[0209AC30] + 168h` and adds one row per category whose save-wide flag is set (`00252D10`), with its
help text:

| Category (`menu_command.bin`) | Flag | Help |
|---|---:|---|
| Weapons `405`<sub>h</sub> | 1 | `BE9`<sub>h</sub> |
| Armor `406`<sub>h</sub> | 2 | `BEA`<sub>h</sub> |
| Accessories `407`<sub>h</sub> | 8 | `BEB`<sub>h</sub> |
| Ammunition `408`<sub>h</sub> | 3 | `BEC`<sub>h</sub> |
| Items `409`<sub>h</sub> | 4 | `BED`<sub>h</sub> |
| Abilities `40D`<sub>h</sub> | 5 | `BF1`<sub>h</sub> |
| Loot `40E`<sub>h</sub> | 6 | `BF2`<sub>h</sub> |
| Key Items `40F`<sub>h</sub> | 7 | `BF3`<sub>h</sub> |

The rows form three groups, Key Items and Loot, then Abilities and Items, then Weapons, Ammunition, Armor and
Accessories; each group is moved down by the gap `01E0C3B4` for every earlier group that has a row (`002CA0E0`). A
row whose category `002CDAE0` reports is drawn in colour 2, and a category not yet visited carries the mark of
`002CDE20` ([Menu screens](menu-screens.md)).

Message 12 takes three sub-commands:

- `8000`<sub>h</sub>, the cursor moved: it closes the previous category's pane (`00563FC0`), opens the new one (`00564B90`)
  and sizes the help line to the category's widest name (`00564430`, kept per category at `+1E8`<sub>h</sub>; `002932F0`);
- `8001`<sub>h</sub>, confirm on a row in colour 0: it marks the category visited (`002CDE50`), gives its pane the focus
  (`005659B0`) and stores the category (`002527B0(6, 1, id)`);
- `8002`<sub>h</sub>, cancel: it closes the screen's list and the open pane (`00563FC0`).

`00563FC0(id)` closes a category's pane: it sets the pane's `+40`<sub>h</sub> bit 6 and either hides it (`00244DD0`, when
bits 0 and 5 are set) or sends it message `00915058` and releases it (`00245020`). Message 18 returns to the menu
(`002814E0(4B8h)`) and clears `[0209AC30] + 168h`.

### The tab panes

The tab panes that `00564B90` builds (procedures `005636F0`, `00563930`, `00563B10`, `00563D20`) hand their messages
to the shared procedure `005651E0`. The pane of a category lives at `[0209AC30] + 170h + 8 x slot`, where the table
`00D233A0` gives the slot: categories `405`<sub>h</sub>-`409`<sub>h</sub> and `40D`<sub>h</sub>-`40F`<sub>h</sub> take slots 0 to 7, and the keys
`597`<sub>h</sub>-`5AF`<sub>h</sub> take 8 to 32 (the tab sets of the [Shop screens](shop-screens.md)). `00564A60`, `00565190` and `005659B0` look a category's pane up there:

- `00564A60(id)` answers whether the pane has rows (`+E0`<sub>h</sub>);
- `00565190(id)` runs the pane's input step `00564E10(pane, 1)`;
- `005659B0(id)` gives the pane focus (`00244640`, `00244830`), or hands it to `002286B0` when `00228480` returns non-zero and
  `[0209AC30] + 308h` is empty.

`005651E0` answers:

| Message | Does |
|---|---|
| 8, focus | `00563DC0` |
| 9, blur | hides the list's cursor |
| 10, tick | `00564C80` |
| 12 `8000`<sub>h</sub> | the cursor moved: `00563F10` shows its help |
| 12 `8001`<sub>h</sub> | picks the item up: `005641F0` |
| 12 `8002`<sub>h</sub> | cancel: clears the help (`00293110(0, 0)`) and gives the focus back |
| 12 `8004`<sub>h</sub> | `00564650` ends a move |
| 18 | frees the rows and clears its slot |
| `11E`<sub>h</sub> | `00565720` rebuilds the rows |
| `1A`<sub>h</sub> | slides a row aside while an item is held |

### Rows

`00565720(pane, id)` frees the old rows and builds the tab's rows with `0057CF20`, the builder of the shop lists
([Shop screens](shop-screens.md)). It then puts the cursor back on the remembered item: the row whose id is the one
kept for the tab, scrolled into view (`002D1820`, `002D47C0`). `00565A00` does the same inside `005655F0`, the row
builder that the shop tabs and the Inventory's tab switch share.

The row painters `00563560` and `005637D0` draw a row: the icon frame `+0A`<sub>h</sub> (none for `-1`), the name `+00`<sub>h</sub>, and
numbers through `0029FF60`: `00563560` writes `+0E`<sub>h</sub> less `+0C`<sub>h</sub> and `+0E`<sub>h</sub>, `005637D0` only `+0E`<sub>h</sub>. The held row
is drawn in colour 6. An empty tab shows text `7D8`<sub>h</sub>.

`00564430(id)` returns the widest name of a category's items (`00292B70`, `002B3050`): one list for each category,
two for Abilities.

| Category | Lists (`00252F40`) and kind |
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

`00563F10(pane, row)` shows the help of the item under the cursor, `00293110(00D23962[tab], id << 16)`, unless the
pane holds an item (`+180`<sub>h</sub> bit 8) or bits 26 or 29 are set; `00563DC0` does the same on focus and then shows the
cursor. The tab of a pane is `00564380`.

### The input step

`00564C80(pane)` runs every frame: while an item is held, `00564D30`; otherwise `00564E10(pane, 0)`.

- `00564E10` switches tabs on the buttons of `02F97368 & CA0h` (`00563EC0` one way, `00564300` the other), keeps the new tab's cursor (`002527B0(8, ...)`), rebuilds its rows (`005655F0`, `005674B0`) and
  plays sound 10. The extra button (bit 15 of `02F9736A`) opens the sort bar (`005665B0`, sound 4), or plays sound 5
  on an empty tab ([Dialogs](dialogs.md)).
- `005641F0(pane, row)` picks the row's item up: it stores the row at `+17C`<sub>h</sub> and `+17A`<sub>h</sub>, turns the list into move
  mode (`+E4`<sub>h</sub> bits 2, 17 and 18) and hides the tab arrows (`005670F0`).

### Moving an item

`00564D30(pane)` handles the held item:

1. with no held row it ends the move;
2. cancel (`01E0C2A4`) plays sound 3, and `00564C80` puts the cursor back on the held row (`002D4840`);
3. confirm (`01E0C2A0`) plays sound `37`<sub>h</sub>, calls `00565BD0(pane, from, to)` when the cursor is on another row, and
   ends the move;
4. any other frame runs the list (`002D3900`).

`00565BD0` stores the new place in the tab's list (`002530E0(list 00D23960[tab], item, item at the target)`), shifts
the rows between the two places by one and puts the held row at the target, then redraws (`002D1AC0`). While an item
is held, message `1A`<sub>h</sub> slides each row between the two places by 4 a frame. `00564650` ends the move: it clears the
row offsets, leaves move mode, restores the tab strip (`00567690`) and resets `+17C`<sub>h</sub> to `-1`.

### The tab strip

The tab strip at `+C8`<sub>h</sub> of a screen is shared with the shop, equipment and gambit lists (callers `00564159`,
`003FD7C8`, `0056AE5F`):

- `005674B0(strip, current)` lays the tab buttons (`+C8`<sub>h</sub>, count byte `+150`<sub>h</sub>) out from `+148`<sub>h</sub>, brightens the
  current one to `80`<sub>h</sub> and the others to `40`<sub>h</sub> (`002D04F0`), and moves the marker to it (`00566B70`, 100 ms);
- `00567690(strip, current)` only recolours them; `005670F0` and `00566FE0` show the two arrows when there are at least
  two tabs, the latter also offsetting the strip by its width;
- `00566B70(marker, tab, x, curve, ms)` starts the marker's move to `x` over `ms x 60 / 1000` frames.

## Modding notes

- A category appears only once its save-wide flag is set; clearing the flag hides the row.
- Moving an item writes the stored order (`002530E0`), so the new order survives saving.
- The shop keys `597`<sub>h</sub>-`5AF`<sub>h</sub> share the slot table `00D233A0` (slots 8 to 32).

## Related

- [Menu screens](menu-screens.md): the command rows and first visits.
- [Dialogs](dialogs.md): the sort bar.
- [Shop screens](shop-screens.md): the shared row builder.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md): the item counts the rows show.
- [Widgets](widgets.md): the screen widget and focus.
