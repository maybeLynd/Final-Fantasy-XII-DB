---
title: "Menu lists: the scroll list every menu uses, its rows and columns, cursor moves, scrolling and their timing, and the cursor sounds"
kind: "system"
category: "Menus and HUD"
addresses: "0x002D14E0, 0x002D2DB0, 0x002D1420, 0x002D3BA0, 0x002D4B70, 0x002D4A40, 0x002D1870, 0x002D2D40"
---

## What the player sees

- Menu lists move their cursor one row at a time with Up and Down, and one column at a time with Left and Right in
  lists of several columns.
- Pressing a direction again at the end of a list wraps round to the other end; holding it stops at the end.
- When the cursor reaches the edge of the shown rows, the list scrolls smoothly; holding a direction for a while
  makes it scroll faster.
- Some lists have no cursor and only scroll; Triangle with Up or Down turns a whole page.

## How it works

### Building a list

`0x002D14E0(record)` builds a list: a `0x150`-byte widget with procedure `0x002D2DB0` and, at `+0xC0`, a `0xC0`-byte
content widget with procedure `0x002D1420` that holds the rows (`0x002D14FC`, `0x002D1513`). From the record it takes:

| Record | List | Meaning |
|---|---|---|
| `+0x00` bit 0 | `+0xE0` bit 23 | a scroll-only list, with no cursor (`0x002D165D`) |
| `+0x08` | `+0xD8` | the rows' data |
| `+0x10` | `+0xE8` | the item count, a `u16`, which also sizes the content widget (`0x002D14E0`) |
| `+0x14` | `+0xEC` | columns |
| `+0x18` | `+0xEA` | column width |
| `+0x1C` | `+0x100` | row height |
| `+0x20` | `+0x120` | the row painter, called for each shown row |
| `+0x28` | `+0xC8` | the owner, who gets the list's notices |

It also copies the confirm and cancel masks `0x01E0C2A0` and `0x01E0C2A4` to `+0x110` and `+0x112`. The message window's
choice list, for example, is such a list with the painter `0x002A1B00` ([Message windows](message-windows.md)).

### The grid

A list of `+0xE8` items lays them out row by row in `+0xEC` columns:

```python
rows = ceil(items / columns)                         (0x002D48C0, kept at +0xF0)
shown = ceil((height - top margin +0x13C) / row height), ceil(width / column width)   (0x002D1820)
item = (top row +0xF2 + cursor row +0xF4) x columns + left column +0xED + cursor column +0xEE
```

`0x002D48C0(list, items)` sets the count and sizes the content widget to the rows and columns. The cursor position on
screen is the pair `+0xF4`, `+0xEE`; the view's first row and column are `+0xF2`, `+0xED`.

### Moving the cursor

- `0x002D4B70(list, item)` puts the cursor on an item and moves the view only as far as needed to show it: to the item's
  row when it is above or left of the view, so that it is the last shown row when it is below. It answers 1 when the
  view moved, and resets the view for an empty list.
- `0x002D4D60(list, first, last)` makes the view start at `first`'s row and column, moves it back only as far as needed
  to keep `last` shown, and puts the cursor on `last`'s row, or on the last shown row when the view is held at the end
  of the list.
- `0x002D46F0(list, item)` runs `0x002D4B70` and, when the view moved, places the content at once at
  `(-left x column width, -top x row height)`; it then posts `0x8000` with the item to the owner.
- `0x002D4840(list, first, last, notify)` runs `0x002D4D60`, scrolls there with animation 4 (`0x002D4A40`) and posts `0x8000`
  when `notify` is set.

The notices are listed on [widget messages](widget-messages.md).

### Scrolling

`0x002D4A40(list, kind, rows, columns)` moves the content widget to the view's position with the position tween
`0x002468A0` ([Widgets](widgets.md)). It does nothing when the content is already there. Kind 1 places it at once;
otherwise the run lasts the frames `0x002D1870` gives, as `frames x 1000 / 60` ms, with curve 1, curve 5 for kind 7
(which also sets `+0xE0` bit 24) and curve 0 for kinds 3, 9 and 10 (`0x002D4AE4`-`0x002D4B2B`).

`0x002D1870(list, kind, rows, columns)` gives the frames, with `n` the rows moved and `h` the row height:

| Kind | Frames |
|---:|---|
| `2` | byte `+4` of input channel 0 (`0x0035F0F0`) |
| `3` | byte `+5` of input channel 0 (`0x0035F110`) |
| `4`, `6` | `h x n / 24 + 6`, at most 12 |
| `5` | `h x (n - 1) / 24 + 6`, at most 8 |
| `7` | a wrap: `h x n / 24 + 12`, at most 20, when the content is taller than the list; else `h x rows / 24 + 2`, at most 12; the same across columns, taking the larger |
| `8` | byte `+4` plus byte `+5` x (n - 1) |
| `9`, `10` | byte `+5` x n, halved for 10 |

The channel record `0x022CAE90` is described on [Controls](../Controls-And-Input/controls.md).

### The step

`0x002D3BA0` steps the list from the pad each turn. It uses `0x002D1B10` for a scroll-only list and `0x002D1DB0` for a list
with a cursor, then animates the move and plays its sound. Holding Up or Down (`0x50`) counts at `+0x10B`, one per tick
with no gap of 3 ticks or more, and at 80 it sets `+0xE4` bit 13 and steps again in the same turn
(`0x002D3CDF`-`0x002D3D4D`).

`0x002D1B10(list, pressed, repeat, held)` moves a scroll-only list's view and answers how:

| Input | View | Answer |
|---|---|---|
| Triangle held with Up or Down | a page up or down, unless `+0xE4` bit 13 is set | `4` |
| Up, Down | one row | `2` |
| Up at the top, Down at the bottom, on a fresh press | wraps round, unless `+0xE4` bit 24 is set | `3` |
| Left, Right | one column, wrapping the same way | 2 or 3 |

Bits `0x1000`, `0x2000`, `0x4000` and `0x8000` of the answer say up, down, left or right.

When its fifth argument is non-zero, `0x002D3BA0` uses `0x002D0A20(list, pressed, repeat, held)` instead (`0x002D3CAE`),
a cursor move that keeps margins: the cursor stays `+0x109` rows from the top and `+0x10A` from the bottom of
the view while the view can still scroll, and a page stops `+0x107` rows from the start or `+0x108` from the end.

| Input | Move | Answer |
|---|---|---|
| Triangle held with Up or Down | the view by one page less a row, the cursor too when the view is held at its margin; at the margin, the cursor to the first or last shown row unless `+0xE4` bit 24 is set; nothing when bit 13 is set | `4`, `5`, `6` |
| Up, Down, with at least two rows | the cursor row, or the view once the cursor is at its margin | `1`, `2` |
| Up at the top, Down at the bottom, on a fresh press | wraps to the other end and one column on, unless `+0xE4` bit 24 is set | `3` |
| Left, Right | the cursor column, or the view's column, wrapping the same way into the next row | `1`, `2`, `3` |

After a move the cursor is pulled back onto the last item, and the direction bit is set only when something moved.

### Cursor sounds

`0x002D2D40(list, answer)` plays the step's sound:

- answers 1-3, a move: the list's sound `+0xFF`, 1 when it is 0 and none when it is -1; nothing while `+0xE0` bit 22
  is set; with `+0xE4` bit 29 the block-bank sound `0x003A11F0` gives, played through `0x002DF220(id, 0x40, 0x7F)` while
  `0x02091098` is 0 ([Sound effects](../Sound-And-Music/sound-effects.md));
- answers 4-6, a jump: sound `0x17` through `0x00249C60`, or `0x00249CA0` with `+0xE4` bit 29.

### Other switches

- `0x002D45C0(list, on)` sets `+0xE0` bit 16 and, when the focus widget is the list or one of its ancestors and every
  one of them is active, can take the focus and is not mid-run, calls `0x003689E0(on)`.
- `0x002D49C0(list, on)` sets `+0xE4` bit 21 and clears `+0x118` when it is turned off; the gambit editor and its
  condition list use it (`0x00569812`, `0x0056AB7F`).
- `0x002D49F0(list, kind)`, used by the Clan Primer's family index, scrolls with `0x002D4A40` and, when it scrolled, `+0xE4`
  bit 27 is set and the kind is 8-10, passes the frames to `0x00368860`.

### The hand cursor

The menus share one hand cursor, a `0x70`-byte state block at `0x022CBE30`: the mode `0x022CBE30` (0 off, 1 resting,
2 sliding), the flags `0x022CBE32`, positions with `0x8000` for none, the bounce at `0x022CBE3D`-`0x022CBE43`, the
holder `0x022CBE68`, a four-point trail from `0x022CBE76`, and the fade `0x022CBE87` (0 shown, 1 fading in, 2 fading
out, 3 hidden) with its count `0x022CBE8A` out of `0x022CBE88`. `0x00368360` moves it ([Battle menu](battle-menu.md)).

- `0x00368270()` resets the block: every position to none, mode 1 and flags `0x115`.
- `0x00368010(pos, widget, plain)`, from `0x00368360`, adds up a widget's position and its ancestors' (next at
  `+0x10`, `0x00246480`): with flag bit 5 through each widget's rotation and scale (`0x00398910`, `0x003985B0`,
  `0x00398C50`) about its centre, with flag bit 9 from a widget's `+0x84`/`+0x8C` while its `+0x80` bit 0 is set,
  and with flag bit 6 it scales the alpha byte `+0x0E` by each widget's `+0x24` / 128. `plain` skips all three.
- `0x00367820(widget, pos)`, from `0x00368360`, answers whether a request starts a slide. A widget other than the
  holder clears flag bit 7 and gets 1; while the fade is 2 or 3 it answers 1; an unchanged target answers 0, and
  a held target (`pos` flag bit 8) is recorded without a slide.
- `0x00367200(frames)`, the step, slides in mode 2 (`0x00367ED0`) and fills the trail, returning to mode 1 at the
  end; in mode 1 it ages the trail and counts down the hold `0x022CBE34`, then starts the fade out. It runs the
  bounce while flag bit 4 is set and steps the fade.
- `0x003676D0()`, from the step (`0x00367340`), moves the cursor in mode 2. With flag bit 2 it takes the progress
  `0x00248F40(0x022CBE5C, 0x022CBE60, 0x022CBE5E)`, shifts both the start `0x022CBE48`/`0x022CBE4A` and the target
  `0x022CBE4C`/`0x022CBE4E` by `0x022CBE58`/`0x022CBE5A` when either is non-zero, and sets the position `0x022CBE38`/`0x022CBE3A`
  to start + (target - start) x progress.
- Without flag bit 2, `0x003676D0` jumps to the target (`0x00368940`) and clears `0x022CBE5E` and `0x022CBE70`.
- `0x003676B0()` sets flag bit 11 and calls the step; the widget draw passes `0x00250540`, `0x002506D0` and `0x002508E0`
  run it.
- `0x00368300()` answers whether the hand is drawn: a mode, flag bit 1 or a fade other than hidden, a position,
  and flag bit 2 or a target.
- `0x00368830(on)` sets or clears flag bit 4, which allows the bounce (`0x005641F0`, `0x00564650`, `0x005680E0`,
  `0x005687F0`). `0x003688A0(n)`, from `0x002D3BA0`, and `0x003687C0(flags, n)`, from `0x00368360`, start a bounce whose
  first phase lasts n frames (2 for -1) while bit 4 is set; `0x003687C0` stops it when the request's bit 1 is set.
- `0x003688E0(frames)`, from `0x00368360` and `0x003689E0`, starts a fade in over `frames`: from a fade out (`0x022CBE87` = 2)
  it keeps the progress, `0x022CBE8A = 0x022CBE8A * frames / 0x022CBE88` (`0x0036890E`-`0x00368923`); from hidden (3) it
  starts at the full count, `0x022CBE8A = 0x022CBE88 = frames` (`0x003688F6`-`0x003688FE`).

## Layouts

`MenuList`, the list widget, `0x150` bytes, after the widget header ([Widgets](widgets.md)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C0` | `void*` | content | the content widget that holds the rows |
| `+0x0C8` | `void*` | owner | gets `0x8000` and the other notices |
| `+0x0D8` | `void*` | data | the rows' data |
| `+0x0E0` | `u32` | flags | bit 16 from `0x002D45C0`, 22 silent, 23 scroll-only, 24 a wrap is running |
| `+0x0E4` | `u32` | flags2 | bit 13 fast or no paging, 21 from `0x002D49C0`, 24 no wrap, 27 Clan Primer hook, 29 block-bank sounds |
| `+0x0E8` | `u16` | items | item count |
| `+0x0EA` | `u16` | colWidth | column width |
| `+0x0EC` | `u8` | columns | columns |
| `+0x0ED` | `i8` | left | first shown column |
| `+0x0EE` | `i8` | cursorCol | cursor column on screen |
| `+0x0F0` | `u16` | rows | rows of items |
| `+0x0F2` | `i16` | top | first shown row |
| `+0x0F4` | `i16` | cursorRow | cursor row on screen |
| `+0x0FF` | `i8` | sound | cursor sound, 0 for 1, -1 for none |
| `+0x100` | `u16` | rowHeight | row height |
| `+0x10B` | `u8` | hold | hold counter |
| `+0x10C` | `u32` | holdTime | frame of the last held tick (`0x0208F574`) |
| `+0x110` | `u16[2]` | masks | confirm and cancel masks |
| `+0x120` | `fn*` | painter | the row painter |
| `+0x13C` | `i32` | margin | top margin |

## Modding notes

- A row painter is any function the record's `+0x20` names; the list calls it for each shown row.
- Setting `+0xE4` bit 24 stops a list from wrapping round.

## Related

- [Widgets](widgets.md) - the widget object, tweens and focus.
- [Widget messages](widget-messages.md) - the notices a list posts.
- [Config screen](config-screen.md) - a list whose cursor skips rows.
- [Controls](../Controls-And-Input/controls.md) - the pad words and the mouse wheel in lists.
