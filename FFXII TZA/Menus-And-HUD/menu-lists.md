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
| `+0x00` bit `0x1` | `+0xE0` bit `0x800000` | a scroll-only list, with no cursor (`0x002D165D`); the same bit clears `+0xE0` bit `0x10000` (`0x002D1659`) |
| `+0x00` bit `0x4` | `+0xE0` bit `0x200000` | set when the record bit is clear (`0x002D1578`-`0x002D1589`) |
| `+0x00` bit `0x8` | `+0xE0` bit `0x10000` | set when the record bit is clear (`0x002D158F`-`0x002D15A0`) |
| `+0x00` bit `0x10` | `+0xE0` bit `0x4000000` | copied (`0x002D15A6`-`0x002D15B4`) |
| `+0x00` bit `0x20` | `+0xE0` bit `0x2000000` | copied (`0x002D15BA`-`0x002D15C9`) |
| `+0x00` bit `0x40` | `+0xE0` bit `0x8000000` | copied (`0x002D15CF`-`0x002D15DD`) |
| `+0x00` bit `0x80` | `+0xE0` bit `0x10000000` | copied (`0x002D15E3`-`0x002D15F2`) |
| `+0x00` bit `0x100` | `+0xE0` bit `0x20000000` | set when the record bit is clear (`0x002D15F8`-`0x002D1608`) |
| `+0x00` bit `0x200` | `+0xE0` bit `0x40000000` | copied (`0x002D160E`-`0x002D1636`) |
| `+0x08` | `+0xD8` | the rows' data |
| `+0x10` | `+0xE8` | the item count, a `u16`, which also sizes the content widget (`0x002D14E0`) |
| `+0x14` | `+0xEC` | columns |
| `+0x18` | `+0xEA` | column width |
| `+0x1C` | `+0x100` | row height |
| `+0x20` | `+0x120` | the row painter, called for each shown row |
| `+0x28` | `+0xC8` | the owner, who gets the list's notices |

It also copies the confirm and cancel masks `0x01E0C2A0` and `0x01E0C2A4` to `+0x110` and `+0x112`. The message window's
choice list, for example, is such a list with the painter `0x002A1B00` ([Message windows](message-windows.md)).

Before the record bits it zeroes `+0xE0`-`+0xE7` and sets the low 16 bits of `+0xE0` (`0x002D1552`-`0x002D1559`), and
`+0xE4` then gets bits `0x10`, `0x40` and `0x2000000` (`0x002D1643`). It sets `+0x103` to `0x5D`, `+0x106` to `0xFF`
and `+0x109` and `+0x10A` to 1, and zeroes `+0xF8`, `+0x104`, `+0x107`, `+0x108`, `+0x10B`, `+0x10C`, `+0x130`,
`+0x13C`-`+0x143`, `+0x148` and the view and cursor `+0xED`, `+0xEE`, `+0xF2` and `+0xF4` (`0x002D1569`-`0x002D16D7`).

`+0x144` takes bit `0x800` of the list's `+0x40` (`0x002D16B7`-`0x002D16C6`), which also gets bits `0x2` and `0x1000`
(`0x002D1518`-`0x002D1532`). The rows `+0xF0` are `ceil(items / columns)` (`0x002D16E9`-`0x002D16F0`); a column count of 0
faults on the `idiv`. The content widget, when it was created, is sized to columns x column width by rows x row
height, at least one row (`+0x9C`, `+0x9E`, `0x002D16F7`-`0x002D1729`).

The content widget is then attached to the list (`0x00244960`, `0x002D1737`), the mouse wheel is cleared (`0x001E0F20`,
`0x002D173C`) and the list is returned.

The content procedure `0x002D1420(content, message)` answers 0 to message 1 (`0x002D142D`). On message 4 it draws the
rows with the content's draw record `+0x38`: `0x002D2600(draw, content)`, or `0x002D28E0` when the list
`[content + 0x10]` has `+0xE0` bit `0x2000000`, and then stores 0 in `0x02CA8F30` (`0x002D1489`-`0x002D14C6`). On message
17 whose value `+0x08` is 1 it clears the list's `+0xE4` bit `0x8000000` (`0x002D1453`-`0x002D1477`); message 17 with
another value only answers 0. Any other message stores 1 in `0x02CA8F30` and goes on to `0x005C5230`, which answers 0
(`0x002D143F`-`0x002D144E`).

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
  view moved, and resets the view for an empty list: with no items it stores 0 in the dword at `+0xF2`, the top row
  and the cursor row, and answers 1 (`0x002D4BB9`-`0x002D4BCC`).
- An item past the last becomes the last (`0x002D4BE4`). Its rows, with `s` the shown rows and `r` the item's row
  (`0x002D4B76`-`0x002D4C8E`): when the top row plus `s` passes the row count `+0xF0`, the view goes back to row 0 with
  the cursor on row `r`; an item above the view with `r` below `s` does the same.
- An item above the view with `r` of `s` or more makes `r` the top row and the cursor row the word `+0xF6`; one
  below makes `r - (s - 1)` the top row and `s - 1` the cursor row; else the cursor row is `r` less the top row.
- Its columns, with `t` the shown columns and `c` the item's column (`0x002D4C96`-`0x002D4D5A`): when the left column
  `+0xED` plus the column count `+0xEC` passes `t`, the view goes back to column 0 with the cursor column `+0xEE` on
  `c`; the other cases follow the rows, except that an item left of the view with `c` of `t` or more puts the cursor
  column on 0. A column move answers 1; with no column move it answers whether the rows moved.
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
(which also sets `+0xE0` bit `0x1000000`) and curve 0 for kinds 3, 9 and 10 (`0x002D4AE4`-`0x002D4B2B`).

It answers 0 when the content is already there (`0x002D4A92`-`0x002D4AA1`, `0x002D4ACD`). Kind 1 is compared before the
direction bits are masked off, so only a bare 1 places at once (`0x002D4AA3`); it clears the content's tween bit `0x1`
of `+0x80` and answers 0 (`0x002D4AA8`-`0x002D4ACD`). When `0x002D1870` gives 0 frames no tween starts and it answers 0
(`0x002D4AE0`-`0x002D4AE2`). After `0x002468A0` it takes 1 off the content's `+0x94`, the frame counter value the tween
started at, and answers the frames (`0x002D4B30`-`0x002D4B36`).

### The content position

The content widget `[list+0xC0]` keeps its position as two `i16` words, x at `+0x98` and y at `+0x9A`. The target
is x = -(first column `+0xED`, `i8`, x column width `+0xEA`, `u16`) and y = -(first row `+0xF2`, `i16`, x row
height `+0x100`, `u16`), computed in 32 bits (`0x002D4A53`-`0x002D4A8F`). Both ways of moving work in 16 bits:

- kind 1 stores the low words of the targets (`0x002D4AB6`, `0x002D4AC5`);
- the tween `0x002468A0` stores the start words at `+0x84`/`+0x86` and the 16-bit differences at `+0x8C`/`+0x8E`
  (`0x00246940`-`0x00246981`).

The y target fits the word while first row x row height is at most 32,768, so a list with row height `h` reaches
row `32768 / h` (rounded down) exactly, the largest row with `-(row × h) >= -32768` (`imul r14d, eax`, `neg r14d`,
`0x002D4A81`-`0x002D4A8F`, stored as a word at `0x002D4AC5`); with `h` = 48 that is row 682.

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

`0x002D1870` reads the kind without its direction bits `0xF000` (`0x002D188E`) and takes `n` and the columns moved as
absolute values (`0x002D1886`-`0x002D18A6`); any other kind gives 0 (`0x002D18A8`, `0x002D1A85`). Kind 7 counts the rows only
when the kind has an up or down bit, `0x3000` (`0x002D194B`), and the columns only with a left or right bit, `0xC000`
(`0x002D19C3`); a side it does not count gives 0. Across columns it compares the widths `+0x9C` and uses the column
width `+0xEA` times the columns moved, or times the column count `+0xEC` (`0x002D19CB`-`0x002D1A50`).

The channel record `0x022CAE90` is described on [Controls](../Controls-And-Input/controls.md).

### The step

`0x002D3BA0` steps the list from the pad each turn. It uses `0x002D1B10` for a scroll-only list and `0x002D1DB0` for a list
with a cursor, then animates the move and plays its sound. Holding Up or Down (`0x50`) counts at `+0x10B`, one per tick
with no gap of 3 ticks or more, and at 80 it sets `+0xE4` bit `0x2000` and steps again in the same turn
(`0x002D3CDF`-`0x002D3D4D`).

`0x002D1B10(list, pressed, repeat, held)` moves a scroll-only list's view and answers how:

| Input | View | Answer |
|---|---|---|
| Triangle held with Up or Down | a page up or down, unless `+0xE4` bit `0x2000` is set | `4` |
| Up, Down | one row | `2` |
| Up at the top, Down at the bottom, on a fresh press | wraps round, unless `+0xE4` bit `0x1000000` is set | `3` |
| Left, Right | one column, wrapping the same way | 2 or 3 |

Bits `0x1000`, `0x2000`, `0x4000` and `0x8000` of the answer say up, down, left or right.

When its fifth argument is non-zero, `0x002D3BA0` uses `0x002D0A20(list, pressed, repeat, held)` instead (`0x002D3CAE`),
a cursor move that keeps margins: the cursor stays `+0x109` rows from the top and `+0x10A` from the bottom of
the view while the view can still scroll, and a page stops `+0x107` rows from the start or `+0x108` from the end.

| Input | Move | Answer |
|---|---|---|
| Triangle held with Up or Down | the view by one page less a row, the cursor too when the view is held at its margin; at the margin, the cursor to the first or last shown row unless `+0xE4` bit `0x1000000` is set; nothing when bit `0x2000` is set | `4`, `5`, `6` |
| Up, Down, with at least two rows | the cursor row, or the view once the cursor is at its margin | `1`, `2` |
| Up at the top, Down at the bottom, on a fresh press | wraps to the other end and one column on, unless `+0xE4` bit `0x1000000` is set | `3` |
| Left, Right | the cursor column, or the view's column, wrapping the same way into the next row | `1`, `2`, `3` |

After a move the cursor is pulled back onto the last item, and the direction bit is set only when something moved.

### Cursor sounds

`0x002D2D40(list, answer)` plays the step's sound:

- answers 1-3, a move: the list's sound `+0xFF`, 1 when it is 0 and no sound when it is -1; nothing while `+0xE0` bit
  `0x400000` is set; with `+0xE4` bit `0x20000000` the block-bank sound `0x003A11F0` gives, played through `0x002DF220(id,
  0x40, 0x7F)` while `0x02091098` is 0 ([Sound effects](../Sound-And-Music/sound-effects.md));
- without that bit the move's sound goes through `0x00249C60`, which takes the handle from `0x003A1180` and plays it the
  same way; both play nothing when the handle is -1 (`0x002D2D64`-`0x002D2D9C`, `0x00249C60`-`0x00249C86`,
  `0x00249CA0`-`0x00249CC6`);
- answers 4-6, a jump: sound `0x17` through `0x00249C60`, or `0x00249CA0` with `+0xE4` bit `0x20000000`;
- any other answer plays nothing (`0x002D2D42`, `0x002D2D4C`).

### Other switches

- `0x002D45C0(list, on)` sets `+0xE0` bit `0x10000` and, when the focus widget is the list or one of its ancestors and every
  one of them is active, can take the focus and is not mid-run, calls `0x003689E0(on)`.
- `0x002D49C0(list, on)` sets `+0xE4` bit `0x200000` and clears `+0x118` when it is turned off; the gambit editor and its
  condition list use it (`0x00569812`, `0x0056AB7F`).
- `0x002D49F0(list, kind)`, used by the Clan Primer's family index, scrolls with `0x002D4A40` and, when it scrolled, `+0xE4`
  bit `0x8000000` is set and the kind is 8-10, passes the frames to `0x00368860`.

### The hand cursor

The menus share one hand cursor, a `0x70`-byte state block at `0x022CBE30`: the mode `0x022CBE30` (0 off, 1 resting,
2 sliding), the flags `0x022CBE32`, positions with `0x8000` for no position, the bounce at `0x022CBE3D`-`0x022CBE43`, the
holder `0x022CBE68`, a four-point trail from `0x022CBE76`, and the fade `0x022CBE87` (0 shown, 1 fading in, 2 fading
out, 3 hidden) with its count `0x022CBE8A` out of `0x022CBE88`. `0x00368360` moves it ([Battle menu](battle-menu.md)).

- `0x00368270()` resets the block: every position to `0x8000`, mode 1 and flags `0x115`.
- `0x00368010(pos, widget, plain)`, from `0x00368360`, adds up a widget's position and its ancestors' (next at
  `+0x10`, `0x00246480`), and `plain` skips all three of these flag steps:
  - with flag bit `0x20` through each widget's rotation and scale (`0x00398910`, `0x003985B0`, `0x00398C50`) about its
    centre;
  - with flag bit `0x200` from a widget's `+0x84`/`+0x8C` while its `+0x80` bit `0x1` is set;
  - with flag bit `0x40` it scales `+0x0E` by each widget's alpha, `+0x0E = (+0x0E × [widget + 0xA0]) >> 7`
    (`0x003681AB`-`0x003681B7`): the alpha byte `+0x0E` times the widget's alpha `+0xA0` / 128, which `0x00246480` copies
    to `+0x24` of its position record (`0x002464ED`-`0x002464F5`), where the `imul` at `0x003681AF` reads it.
- `0x00367820(widget, pos)`, from `0x00368360`, answers whether a request starts a slide. A widget other than the
  holder clears flag bit `0x80` and gets 1; while the fade is 2 or 3 it answers 1; an unchanged target answers 0, and
  a held target (`pos` flag bit `0x100`) is recorded without a slide.
- `0x00367200(frames)`, the step, slides in mode 2 (`0x00367ED0`) and fills the trail, returning to mode 1 at the
  end; in mode 1 it ages the trail and counts down the hold `0x022CBE34`, then starts the fade out. It runs the
  bounce while flag bit `0x10` is set and steps the fade.
- `0x003676D0()`, from the step (`0x00367340`), moves the cursor in mode 2. With flag bit `0x4` it takes the progress
  `0x00248F40(0x022CBE5C, 0x022CBE60, 0x022CBE5E)`, shifts both the start `0x022CBE48`/`0x022CBE4A` and the target
  `0x022CBE4C`/`0x022CBE4E` by `0x022CBE58`/`0x022CBE5A` when either is non-zero, and sets the position `0x022CBE38`/`0x022CBE3A`
  to start + (target - start) x progress.
- Without flag bit `0x4`, `0x003676D0` jumps to the target (`0x00368940`) and clears `0x022CBE5E` and `0x022CBE70`.
- `0x003676B0()` sets flag bit `0x800` and calls the step; the widget draw passes `0x00250540`, `0x002506D0` and `0x002508E0`
  run it.
- `0x00368300()` answers whether the hand is drawn: a mode, flag bit `0x2` or a fade other than hidden, a position,
  and flag bit `0x4` or a target.
- `0x00368830(on)` sets or clears flag bit `0x10`, which allows the bounce (`0x005641F0`, `0x00564650`, `0x005680E0`,
  `0x005687F0`). `0x003688A0(n)`, from `0x002D3BA0`, and `0x003687C0(flags, n)`, from `0x00368360`, start a bounce whose
  first phase lasts n frames while bit `0x10` is set; `0x003688A0` takes -1 as 2, and `0x003687C0` does nothing for -1
  (`0x003687C8`); `0x003687C0` stops it when the request's bit `0x2` is set.
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
| `+0x0E0` | `u32` | flags | bit `0x10000` from `0x002D45C0`, `0x400000` silent, `0x800000` scroll-only, `0x1000000` a wrap is running |
| `+0x0E4` | `u32` | flags2 | bit `0x2000` fast or no paging, `0x200000` from `0x002D49C0`, `0x1000000` no wrap, `0x8000000` Clan Primer hook, `0x20000000` block-bank sounds |
| `+0x0E8` | `u16` | items | item count |
| `+0x0EA` | `u16` | colWidth | column width |
| `+0x0EC` | `u8` | columns | columns |
| `+0x0ED` | `i8` | left | first shown column |
| `+0x0EE` | `i8` | cursorCol | cursor column on screen |
| `+0x0F0` | `u16` | rows | rows of items |
| `+0x0F2` | `i16` | top | first shown row |
| `+0x0F4` | `i16` | cursorRow | cursor row on screen |
| `+0x0FF` | `i8` | sound | cursor sound, 0 for 1, -1 for no sound |
| `+0x100` | `u16` | rowHeight | row height |
| `+0x10B` | `u8` | hold | hold counter |
| `+0x10C` | `u32` | holdTime | frame of the last held tick (`0x0208F574`) |
| `+0x110` | `u16[2]` | masks | confirm and cancel masks |
| `+0x120` | `fn*` | painter | the row painter |
| `+0x13C` | `i32` | margin | top margin |

## State

The globals in the first three tables belong to the hand cursor's block `0x022CBE30`. All are 0 in the file, and
`0x00368270` also sets every one of them to 0 when it clears the block's `0x70` bytes with `memset` (`0x00368281`).

### The bounce

The bounce runs while flag bit `0x10` of `0x022CBE32` is set and the phase `0x022CBE3D` is 1 to 4. The step `0x00367200` adds
its frames to `0x022CBE3E`; once that passes the phase's length, the byte at `0x022CBE40` + phase - 1 (`0x0036759E`), it
moves to the next phase with the count at 0. After phase 4 it starts again at phase 1 with the lengths 2, 6, 4 and
30 (`0x003675AB`-`0x003675CE`). `0x00367ED0` shifts the hand by:

```python
phase 2:     offset = trunc(4 x 0x00248F40(2, [0x022CBE41], [0x022CBE3E]))       (0x00367F36-0x00367F57)
phase 3:     offset = 4 - trunc(4 x 0x00248F40(1, [0x022CBE42], [0x022CBE3E]))   (0x00367F08-0x00367F32)
phase 1, 4:  offset = 0
```

The offset is negated when `0x022CBE36` is 2 and added to x when `0x022CBE3C` is 0, to y when it is 1 (`0x00367F5B`-`0x00367F83`).

These start a bounce, each only while flag bit `0x10` is set:

- `0x003687C0(flags, n)` sets the lengths n, 6, 4, 30 and phase 1, does nothing when n is -1, and sets phase 0, whatever
  flag bit `0x10`, when `flags` bit `0x2` is set; `0x00368360` passes the slide's frames + 2 (`0x00368675`).
- `0x003688A0(n)` sets n (2 for -1), 6, 4, 30 and phase 1; `0x00368860(n)` the same with n + 2 (2 when n is -3).
- `0x00368360` sets 0, 6, 4, 30 for a request whose byte `+0x08` is 2 (`0x00368702`), and 2, 6, 4, 30 when it places the
  hand at once without the request's `+0x0A` bit `0x2` (`0x00368767`).
- `0x00367200` sets 2, 6, 4, 30 when a slide ends, unless flag bit `0x400` is set (`0x003673BB`-`0x003673CC`).

The Clan Primer's list step `0x00570CE0` copies the eight bytes `0x022CBE3C`-`0x022CBE43` out with `0x00367EC0` before it
steps the list (`0x00570D6F`) and puts them back with `0x00368820` on the path that puts the list's view and cursor back where they were with `0x002D47C0`
(`0x00571222`-`0x0057126A`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBE3C` | `u8` | 0 | the bounce's axis: 0 along x, 1 along y, any other value no shift; only its own copy is ever stored back, so it stays 0 and the hand bounces sideways | `0x00368820` (`0x00368828`) | `0x00367EC0` (`0x00367EC5`); `0x00367ED0` (`0x00367F67`) |
| `0x022CBE3E` | `u16` | 0 | frames into the current bounce phase | `0x00367200` (0: `0x003673BB`, `0x003675BB`, `0x003675D7`, `0x00367662`; the count: `0x00367594`); `0x003678F0`, 0 (`0x00367908`); `0x00368270`, 0 (`0x003682B7`); `0x00368360`, 0 (`0x00368702`, `0x00368767`); `0x003687C0`, 0 (`0x003687DB`); `0x00368820` (`0x00368828`); `0x00368860`, 0 (`0x00368896`); `0x003688A0`, 0 (`0x003688D3`); `0x00368940`, 0 (`0x0036899D`) | `0x00367200` (`0x00367584`); `0x00367EC0` (`0x00367EC5`); `0x00367ED0` (`0x00367F08`, `0x00367F36`) |
| `0x022CBE40` | `u8` | 0 | phase 1's length in frames, the pause before the hand moves out | `0x00367200`, 2 (`0x003673BB`, `0x003675BB`); `0x00368360`, 0 (`0x00368702`) or 2 (`0x00368767`); `0x003687C0`, n (`0x003687D5`); `0x00368820` (`0x00368828`); `0x00368860` (`0x00368890`); `0x003688A0` (`0x003688CD`) | `0x00367200` (`0x0036759E`); `0x00367EC0` (`0x00367EC5`) |
| `0x022CBE41` | `u8` | 0 | phase 2's length, the move out of 4 pixels: always 6 | `0x00367200` (`0x003673BB`, `0x003675BB`); `0x00368360` (`0x00368702`, `0x00368767`); `0x003687C0` (`0x003687E2`); `0x00368820` (`0x00368828`); `0x00368860` (`0x0036886F`); `0x003688A0` (`0x003688AC`) | `0x00367200` (`0x0036759E`); `0x00367EC0` (`0x00367EC5`); `0x00367ED0` (`0x00367F43`) |
| `0x022CBE42` | `u8` | 0 | phase 3's length, the move back: always 4 | `0x00367200` (`0x003673CC`, `0x003675C5`); `0x00368360` (`0x00368771`); `0x003687C0` (`0x003687E2`); `0x00368820` (`0x00368828`); `0x00368860` (`0x0036886F`); `0x003688A0` (`0x003688AC`) | `0x00367200` (`0x0036759E`); `0x00367EC0` (`0x00367EC5`); `0x00367ED0` (`0x00367F15`) |
| `0x022CBE43` | `u8` | 0 | phase 4's length, the rest before the next bounce: always 30 | `0x00367200` (`0x003673CC`, `0x003675C5`); `0x00368360` (`0x00368771`); `0x003687C0` (`0x003687EB`); `0x00368820` (`0x00368828`); `0x00368860` (`0x0036887D`); `0x003688A0` (`0x003688BA`) | `0x00367200` (`0x0036759E`); `0x00367EC0` (`0x00367EC5`) |

### The trail

While the hand slides, `0x00367200` keeps where it is drawn each frame (`0x00367ED0`) as point 0 and moves the older
points one place on (`0x00367292`-`0x003672F7`), up to the four that `0x022CBE70` counts. Each point's alpha comes from the
four bytes at `0x01EF9248`: `0x30`, `0x20`, `0x10` and `0x08` (`0x0036732A`).

At rest each step sets the oldest point's x to `0x8000`, gives each point the alpha of the point after it and counts
one point fewer (`0x003673EE`-`0x00367433`). The last point steps through the four alphas before it goes
(`0x0036743B`-`0x00367487`).

`0x00367940` draws the points from the oldest to point 0 at their y + 4, each at its alpha times the hand's over 128.
It reads them through the block's address (`0x00367A30`, `0x00367A47`, `0x00367A4D`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBE71` | `u8` | 0 | point 0's alpha | `0x00367200` (`0x0036732A`, `0x003673F5`, `0x00367487`) | `0x00367200` (`0x0036743B`); `0x00367940` (`0x00367A30`) |
| `0x022CBE72` | `u8` | 0 | point 1's alpha | `0x00367200` (`0x0036732A`, `0x00367402`) | `0x00367200` (`0x003673EE`); `0x00367940` (`0x00367A30`) |
| `0x022CBE73` | `u8` | 0 | point 2's alpha | `0x00367200` (`0x0036732A`, `0x0036740F`) | `0x00367200` (`0x003673FB`); `0x00367940` (`0x00367A30`) |
| `0x022CBE74` | `u8` | 0 | point 3's alpha | `0x00367200` (`0x0036732A`) | `0x00367200` (`0x00367408`); `0x00367940` (`0x00367A30`) |
| `0x022CBE76` | `i16` | 0 | point 0's x, `0x8000` for no point | `0x00367200` (`0x003672EB`; `0x8000`: `0x0036741D`, `0x00367669`); `0x003678F0`, `0x8000` (`0x00367901`); `0x00368270`, `0x8000` (`0x003682D0`); `0x00368940`, `0x8000` (`0x00368996`) | `0x00367200` (`0x003672CA`); `0x00367940` (`0x00367A4D`) |
| `0x022CBE78` | `i16` | 0 | point 0's y | `0x00367200` (`0x003672F7`) | `0x00367200` (`0x003672D8`); `0x00367940` (`0x00367A47`) |
| `0x022CBE7A` | `i16` | 0 | point 1's x, `0x8000` for no point | `0x00367200` (`0x003672D1`; `0x8000`: `0x0036741D`, `0x00367671`); `0x003678F0` (`0x0036790F`); `0x00368270` (`0x003682D7`); `0x00368940` (`0x003689A4`) | `0x00367200` (`0x003672AE`); `0x00367940` (`0x00367A4D`) |
| `0x022CBE7C` | `i16` | 0 | point 1's y | `0x00367200` (`0x003672DF`) | `0x00367200` (`0x003672BC`); `0x00367940` (`0x00367A47`) |
| `0x022CBE7E` | `i16` | 0 | point 2's x, `0x8000` for no point | `0x00367200` (`0x003672B5`; `0x8000`: `0x0036741D`, `0x00367679`); `0x003678F0` (`0x00367916`); `0x00368270` (`0x003682DE`); `0x00368940` (`0x003689AB`) | `0x00367200` (`0x00367292`); `0x00367940` (`0x00367A4D`) |
| `0x022CBE80` | `i16` | 0 | point 2's y | `0x00367200` (`0x003672C3`) | `0x00367200` (`0x003672A0`); `0x00367940` (`0x00367A47`) |
| `0x022CBE82` | `i16` | 0 | point 3's x, `0x8000` for no point | `0x00367200` (`0x00367299`; `0x8000`: `0x0036741D`, `0x00367681`); `0x003678F0` (`0x0036791D`); `0x00368270` (`0x003682E5`); `0x00368940` (`0x003689B2`) | `0x00367940` (`0x00367A4D`) |
| `0x022CBE84` | `i16` | 0 | point 3's y | `0x00367200` (`0x003672A7`) | `0x00367940` (`0x00367A47`) |

### The request

`0x00368360` turns a request's position into a screen position (`0x00368010`) and adds the request's offset `+0x04`/`+0x06`
when its `+0x0A` bit `0x100` is set, giving the target. `0x00367820` starts a slide only when the target changed and the
position before the offset differs from `0x022CBE50`/`0x022CBE52`. With the same position and a new offset it retargets a
sliding hand, or moves a resting one there at once, without a slide (`0x0036787B`-`0x003678D9`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBE50` | `i16` | 0 | x of the last request's position before its offset; the target itself when the hand is placed at once; `0x8000` for no request | `0x00367200`, `0x8000` when a fade out ends with flag bit `0x80` (`0x00367658`); `0x00367820` (`0x003678CE`); `0x003678F0`, `0x8000` (`0x00367934`); `0x00368270`, `0x8000` (`0x003682AD`); `0x00368360` (`0x003686DD`; the target: `0x00368723`); `0x00368940`, `0x8000` without a position (`0x003689C9`) | `0x00367820` (`0x0036787B`) |
| `0x022CBE52` | `i16` | 0 | y of the same | `0x00367200` (`0x00367658`); `0x00367820` (`0x003678D9`); `0x003678F0` (`0x00367934`); `0x00368270` (`0x003682AD`); `0x00368360` (`0x003686E9`; the target: `0x00368744`); `0x00368940` (`0x003689C9`) | `0x00367820` (`0x00367887`) |
| `0x022CBE54` | `i16` | 0 | x of the last request's offset, 0 when it had no offset; the next request's offset minus this is the shift `0x022CBE58` | `0x00368360` (`0x003684D6`) | `0x00368360` (`0x003684AA`) |
| `0x022CBE56` | `i16` | 0 | y of the same, for `0x022CBE5A` | `0x00368360` (`0x003684DD`) | `0x00368360` (`0x003684BC`) |
| `0x022CBE86` | `u8` | 0 | the hand's alpha while flag bit `0x40` is set, in place of the fade's: every request that sets the flags stores `0x80`, full, first | `0x00368360`, `0x80` (`0x0036854F`) | `0x00367940` (`0x003679D6`) |

Nothing else reads or writes these globals. The block's address is taken only by `0x00367940` and `0x00368270`, with `0x022CBE4C` handed to
`0x00368940` by `0x003676D0`, which reads only the target there.

### The content widget

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA8F30` | `i32` | 0 | 0 after the content widget draws its rows on message 4 (`0x002D2600`, or `0x002D28E0` with list `+0xE0` bit `0x2000000`), 1 after any message other than 1, 4 and 17, which it passes to `0x005C5230` | `0x002D1420` (1: `0x002D143F`; 0: `0x002D14B5`, `0x002D14C6`) | no instruction |

## Modding notes

- A row painter is any function the record's `+0x20` names; the list calls it for each shown row.
- Setting `+0xE4` bit `0x1000000` stops a list from wrapping round.

## Related

- [Widgets](widgets.md) - the widget object, tweens and focus.
- [Widget messages](widget-messages.md) - the notices a list posts.
- [Config screen](config-screen.md) - a list whose cursor skips rows.
- [Controls](../Controls-And-Input/controls.md) - the pad words and the mouse wheel in lists.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Save load settings: `0x00244960` is called by `0x0057E4D0`, `0x005819F0`, `0x005823B0`, `0x00582860`; `0x003678F0` is called by
  `0x00582860`; those functions are documented on [changing areas](../World-Areas-And-Travel/changing-areas.md),
  [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md),
  [game application](../Engine-Core/game-application.md).
