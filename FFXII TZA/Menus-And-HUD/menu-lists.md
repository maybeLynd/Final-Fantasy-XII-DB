---
title: "Menu lists: the scroll list every menu uses, its rows and columns, cursor moves, scrolling and their timing, and the cursor sounds"
kind: "system"
category: "Menus and HUD"
addresses: "002D14E0, 002D2DB0, 002D1420, 002D3BA0, 002D4B70, 002D4A40, 002D1870, 002D2D40"
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

`002D14E0(record)` builds a list: a `150`<sub>h</sub>-byte widget with procedure `002D2DB0` and, at `+C0`<sub>h</sub>, a `C0`<sub>h</sub>-byte
content widget with procedure `002D1420` that holds the rows (`002D14FC`, `002D1513`). From the record it takes:

| Record | List | Meaning |
|---|---|---|
| `+00`<sub>h</sub> bit 0 | `+E0`<sub>h</sub> bit 23 | a scroll-only list, with no cursor (`002D165D`) |
| `+08`<sub>h</sub> | `+D8`<sub>h</sub> | the rows' data |
| `+10`<sub>h</sub> | `+E8`<sub>h</sub> | the item count, a `u16`, which also sizes the content widget (`002D14E0`) |
| `+14`<sub>h</sub> | `+EC`<sub>h</sub> | columns |
| `+18`<sub>h</sub> | `+EA`<sub>h</sub> | column width |
| `+1C`<sub>h</sub> | `+100`<sub>h</sub> | row height |
| `+20`<sub>h</sub> | `+120`<sub>h</sub> | the row painter, called for each shown row |
| `+28`<sub>h</sub> | `+C8`<sub>h</sub> | the owner, who gets the list's notices |

It also copies the confirm and cancel masks `01E0C2A0` and `01E0C2A4` to `+110`<sub>h</sub> and `+112`<sub>h</sub>. The message window's
choice list, for example, is such a list with the painter `002A1B00` ([Message windows](message-windows.md)).

### The grid

A list of `+E8`<sub>h</sub> items lays them out row by row in `+EC`<sub>h</sub> columns:

```python
rows = ceil(items / columns)                         (002D48C0, kept at +0xF0)
shown = ceil((height - top margin +0x13C) / row height), ceil(width / column width)   (002D1820)
item = (top row +0xF2 + cursor row +0xF4) x columns + left column +0xED + cursor column +0xEE
```

`002D48C0(list, items)` sets the count and sizes the content widget to the rows and columns. The cursor position on
screen is the pair `+F4`<sub>h</sub>, `+EE`<sub>h</sub>; the view's first row and column are `+F2`<sub>h</sub>, `+ED`<sub>h</sub>.

### Moving the cursor

- `002D4B70(list, item)` puts the cursor on an item and moves the view only as far as needed to show it: to the item's
  row when it is above or left of the view, so that it is the last shown row when it is below. It answers 1 when the
  view moved, and resets the view for an empty list.
- `002D4D60(list, first, last)` makes the view start at `first`'s row and column, moves it back only as far as needed
  to keep `last` shown, and puts the cursor on `last`'s row, or on the last shown row when the view is held at the end
  of the list.
- `002D46F0(list, item)` runs `002D4B70` and, when the view moved, places the content at once at
  `(-left x column width, -top x row height)`; it then posts `8000`<sub>h</sub> with the item to the owner.
- `002D4840(list, first, last, notify)` runs `002D4D60`, scrolls there with animation 4 (`002D4A40`) and posts `8000`<sub>h</sub>
  when `notify` is set.

The notices are listed on [widget messages](widget-messages.md).

### Scrolling

`002D4A40(list, kind, rows, columns)` moves the content widget to the view's position with the position tween
`002468A0` ([Widgets](widgets.md)). It does nothing when the content is already there. Kind 1 places it at once;
otherwise the run lasts the frames `002D1870` gives, as `frames x 1000 / 60` ms, with curve 1, curve 5 for kind 7
(which also sets `+E0`<sub>h</sub> bit 24) and curve 0 for kinds 3, 9 and 10 (`002D4AE4`-`002D4B2B`).

`002D1870(list, kind, rows, columns)` gives the frames, with `n` the rows moved and `h` the row height:

| Kind | Frames |
|---:|---|
| `2` | byte `+4` of input channel 0 (`0035F0F0`) |
| `3` | byte `+5` of input channel 0 (`0035F110`) |
| `4`, `6` | `h x n / 24 + 6`, at most 12 |
| `5` | `h x (n - 1) / 24 + 6`, at most 8 |
| `7` | a wrap: `h x n / 24 + 12`, at most 20, when the content is taller than the list; else `h x rows / 24 + 2`, at most 12; the same across columns, taking the larger |
| `8` | byte `+4` plus byte `+5` x (n - 1) |
| `9`, `10` | byte `+5` x n, halved for 10 |

The channel record `022CAE90` is described on [Controls](../Controls-And-Input/controls.md).

### The step

`002D3BA0` steps the list from the pad each turn. It uses `002D1B10` for a scroll-only list and `002D1DB0` for a list
with a cursor, then animates the move and plays its sound. Holding Up or Down (`50`<sub>h</sub>) counts at `+10B`<sub>h</sub>, one per tick
with no gap of 3 ticks or more, and at 80 it sets `+E4`<sub>h</sub> bit 13 and steps again in the same turn
(`002D3CDF`-`002D3D4D`).

`002D1B10(list, pressed, repeat, held)` moves a scroll-only list's view and answers how:

| Input | View | Answer |
|---|---|---|
| Triangle held with Up or Down | a page up or down, unless `+E4`<sub>h</sub> bit 13 is set | `4` |
| Up, Down | one row | `2` |
| Up at the top, Down at the bottom, on a fresh press | wraps round, unless `+E4`<sub>h</sub> bit 24 is set | `3` |
| Left, Right | one column, wrapping the same way | 2 or 3 |

Bits `1000`<sub>h</sub>, `2000`<sub>h</sub>, `4000`<sub>h</sub> and `8000`<sub>h</sub> of the answer say up, down, left or right.

### Cursor sounds

`002D2D40(list, answer)` plays the step's sound:

- answers 1-3, a move: the list's sound `+FF`<sub>h</sub>, 1 when it is 0 and none when it is -1; nothing while `+E0`<sub>h</sub> bit 22
  is set; with `+E4`<sub>h</sub> bit 29 the block-bank sound `003A11F0` gives, played through `002DF220(id, 40h, 7Fh)` while
  `02091098` is 0 ([Sound effects](../Sound-And-Music/sound-effects.md));
- answers 4-6, a jump: sound `17`<sub>h</sub> through `00249C60`, or `00249CA0` with `+E4`<sub>h</sub> bit 29.

### Other switches

- `002D45C0(list, on)` sets `+E0`<sub>h</sub> bit 16 and, when the focus widget is the list or one of its ancestors and every
  one of them is active, can take the focus and is not mid-run, calls `003689E0(on)`.
- `002D49C0(list, on)` sets `+E4`<sub>h</sub> bit 21 and clears `+118`<sub>h</sub> when it is turned off; the gambit editor and its
  condition list use it (`00569812`, `0056AB7F`).
- `002D49F0(list, kind)`, used by the Clan Primer's family index, scrolls with `002D4A40` and, when it scrolled, `+E4`<sub>h</sub>
  bit 27 is set and the kind is 8-10, passes the frames to `00368860`.

### The hand cursor

The menus share one hand cursor, a `70`<sub>h</sub>-byte state block at `022CBE30`: the mode `022CBE30` (0 off, 1 resting,
2 sliding), the flags `022CBE32`, positions with `8000`<sub>h</sub> for none, the bounce at `022CBE3D`-`022CBE43`, the
holder `022CBE68`, a four-point trail from `022CBE76`, and the fade `022CBE87` (0 shown, 1 fading in, 2 fading
out, 3 hidden) with its count `022CBE8A` out of `022CBE88`. `00368360` moves it ([Battle menu](battle-menu.md)).

- `00368270()` resets the block: every position to none, mode 1 and flags `115`<sub>h</sub>.
- `00368010(pos, widget, plain)`, from `00368360`, adds up a widget's position and its ancestors' (next at
  `+10`<sub>h</sub>, `00246480`): with flag bit 5 through each widget's rotation and scale (`00398910`, `003985B0`,
  `00398C50`) about its centre, with flag bit 9 from a widget's `+84`<sub>h</sub>/`+8C`<sub>h</sub> while its `+80`<sub>h</sub> bit 0 is set,
  and with flag bit 6 it scales the alpha byte `+0E`<sub>h</sub> by each widget's `+24`<sub>h</sub> / 128. `plain` skips all three.
- `00367820(widget, pos)`, from `00368360`, answers whether a request starts a slide. A widget other than the
  holder clears flag bit 7 and gets 1; while the fade is 2 or 3 it answers 1; an unchanged target answers 0, and
  a held target (`pos` flag bit 8) is recorded without a slide.
- `00367200(frames)`, the step, slides in mode 2 (`00367ED0`) and fills the trail, returning to mode 1 at the
  end; in mode 1 it ages the trail and counts down the hold `022CBE34`, then starts the fade out. It runs the
  bounce while flag bit 4 is set and steps the fade.
- `003676B0()` sets flag bit 11 and calls the step; the widget draw passes `00250540`, `002506D0` and `002508E0`
  run it.
- `00368300()` answers whether the hand is drawn: a mode, flag bit 1 or a fade other than hidden, a position,
  and flag bit 2 or a target.
- `00368830(on)` sets or clears flag bit 4, which allows the bounce (`005641F0`, `00564650`, `005680E0`,
  `005687F0`). `003688A0(n)`, from `002D3BA0`, and `003687C0(flags, n)`, from `00368360`, start a bounce whose
  first phase lasts n frames (2 for -1) while bit 4 is set; `003687C0` stops it when the request's bit 1 is set.
- `003688E0(frames)`, from `00368360` and `003689E0`, starts a fade in over `frames`: from a fade out it keeps
  the progress, scaled; from hidden it starts at the full count.

## Layouts

`MenuList`, the list widget, `150`<sub>h</sub> bytes, after the widget header ([Widgets](widgets.md)):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0C0`<sub>h</sub> | `void*` | content | the content widget that holds the rows |
| `0C8`<sub>h</sub> | `void*` | owner | gets `8000`<sub>h</sub> and the other notices |
| `0D8`<sub>h</sub> | `void*` | data | the rows' data |
| `0E0`<sub>h</sub> | `u32` | flags | bit 16 from `002D45C0`, 22 silent, 23 scroll-only, 24 a wrap is running |
| `0E4`<sub>h</sub> | `u32` | flags2 | bit 13 fast or no paging, 21 from `002D49C0`, 24 no wrap, 27 Clan Primer hook, 29 block-bank sounds |
| `0E8`<sub>h</sub> | `u16` | items | item count |
| `0EA`<sub>h</sub> | `u16` | colWidth | column width |
| `0EC`<sub>h</sub> | `u8` | columns | columns |
| `0ED`<sub>h</sub> | `i8` | left | first shown column |
| `0EE`<sub>h</sub> | `i8` | cursorCol | cursor column on screen |
| `0F0`<sub>h</sub> | `u16` | rows | rows of items |
| `0F2`<sub>h</sub> | `i16` | top | first shown row |
| `0F4`<sub>h</sub> | `i16` | cursorRow | cursor row on screen |
| `0FF`<sub>h</sub> | `i8` | sound | cursor sound, 0 for 1, -1 for none |
| `100`<sub>h</sub> | `u16` | rowHeight | row height |
| `10B`<sub>h</sub> | `u8` | hold | hold counter |
| `10C`<sub>h</sub> | `u32` | holdTime | frame of the last held tick (`0208F574`) |
| `110`<sub>h</sub> | `u16[2]` | masks | confirm and cancel masks |
| `120`<sub>h</sub> | `fn*` | painter | the row painter |
| `13C`<sub>h</sub> | `i32` | margin | top margin |

## Modding notes

- A row painter is any function the record's `+20`<sub>h</sub> names; the list calls it for each shown row.
- Setting `+E4`<sub>h</sub> bit 24 stops a list from wrapping round.

## Related

- [Widgets](widgets.md) - the widget object, tweens and focus.
- [Widget messages](widget-messages.md) - the notices a list posts.
- [Config screen](config-screen.md) - a list whose cursor skips rows.
- [Controls](../Controls-And-Input/controls.md) - the pad words and the mouse wheel in lists.
