---
title: "Staff roll: the ending credits, every line in order, and how the roll script lays them out"
kind: "system"
category: "Menus and HUD"
addresses: "0x0053F0D0, 0x0053DD20, 0x0053E380, 0x00511980, 0x005119A0, 0x005119F0, 0x00511890, 0x00511830"
---

## What the player sees

- After the ending, the staff roll scrolls up the screen over a movie: roles and the staff under or beside them, in
  three typefaces, then the middleware and studio logos.
- When the movie has ended, the last picture stays until Start, the cancel button or the confirm button is pressed;
  the screen then fades out.

## How it works

### The script

The roll is the event script `men_z0005`. Its actor `staffroll_main`, function `main`, plays it:

1. It calls `sethpmenufast(0)`, `sethpmenu(0)` and `settrapshowstatus(0)`, sets up the roll (`fsroll_initialize`,
   `fsroll_refresh`), its speed 2 (`fsroll_speed`) and `fsroll_setdouble(1)`.
2. It readies movie 42 (`moviestandby(42)`, `moviestandbysync`), fades in, starts the movie (`movieplay(42)`) and the
   roll (`fsroll_start`), and waits for the movie (`movieplaysync`).
3. After 90 frames it waits, a frame at a time, until Start, the cancel button or the confirm button is newly
   pressed (`padt() & (8 | get_pad_cancel() | get_pad_ok())`), fades out (`fadeout_d0(0, 60)`), ends the movie and
   closes the roll (`movieend`, `fsroll_finalize`).

The lines themselves are the `fsroll` calls of the actor `staffroll_script`, function `create`: 950 lines on 600
rows ([staff-roll.tsv](staff-roll.tsv)). Its `for` loops over a counter show runs of consecutive rows, two per pass
in the two-column parts.

### The recorder

Each `fsroll` verb pops its arguments and calls the recorder `0x0053F0D0(kind, a, b)`, which works on the roll object
`[0x02CA8A80]` (created by `0x0053E380`) and returns at once when the object is missing, running (`+0xFC`) or holds
`0x800` lines (`+0xC8`). It dispatches on the kind through the table `0x0053F3B0`:

| Verb | Begin | Kind | Effect |
|---|---|---|---|
| `fsroll_linedisp(n)` | `0x00511830` | 2 | the line mode `+0x102` = n, at least 1 and at most 3; the slot `+0x103` = 0 (`0x0053F14B`-`0x0053F16D`) |
| `fsroll_layout(a, b)` | `0x00511890` | 3 | the alignment `+0x100` = a and the offset `+0xF4` = b (`0x0053F181`-`0x0053F18E`) |
| `fsroll_blank(n)` | `0x00511900` | 4 | moves the cursor `+0xF0` down n times `0x01DFE0B4`; slot 0 (`0x0053F19C`-`0x0053F1AA`) |
| `fsroll_nameA(v)`, `fsroll_nameB(v)`, `fsroll_nameC(v)` | `0x00511980`, `0x005119A0`, `0x005119F0` | 5, with font 0, 1 or 2 | adds a text line through `0x0053DD20` (below) and moves the cursor by its height (`0x0053F1B9`-`0x0053F1DE`) |
| `fsroll_data(n)` | `0x00511A40` | 6 | adds cell n of the picture `sf_logo_c`, centred on the screen width `0x01E0C1D8`, and moves the cursor by its height; slot 0 (`0x0053F1EA`-`0x0053F2AB`) |

The roll object starts in line mode 1 (`0x0053E4EE`).

### A text line

`0x0053DD20(line, roll, font, v)` fills the line's 32-byte record:

- **The text.** When bit 15 of v is set, the text is id 25000 + (v & `0x7FFF`), else id 26000 + v
  (`0x0053DD90`-`0x0053DDA5`), looked up by `0x002F9860`. Text group 25 is `menu03.bin` (loader id 65) and group 26 is
  `menu04.bin` (loader id 66), so a value with bit 15 shows row v & `0x7FFF` of `menu03.bin`, the roles, and any
  other value shows row v of `menu04.bin`, the names. Both files are lists of `ex00` rows in UTF-16
  ([Text codes](text-codes.md)).
- **Line mode 1** (`0x0053DFFB`-`0x0053E0A3`): the line takes a row of its own at the cursor. Alignment 0 puts its left
  edge at the offset, 1 puts its right edge the offset from the right edge of the roll's width `+0x9C`, 2
  centres it; any other value puts it at the left edge.
- **Line mode 2** (`0x0053DF17`-`0x0053DFE4`): lines go two to a row. The first ends the offset left of the centre, at
  the cursor; the second starts the offset right of the centre on the same row, and the cursor then moves by the
  difference between the two lines' heights (`0x0053DFD0`-`0x0053DFE1`).
- Mode 3 puts three lines to a row (`0x0053DDFE`-`0x0053DEBA`); the roll does not use it.
- The slot then advances, (slot + 1) mod the mode (`0x0053DECE`-`0x0053DEE8`).

The faces are the staff-roll fonts of [Staff-roll font bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md).

### The logos

`sf_logo_c.tm2` (`ps2data/image/ff12/myoshiok/<lang>/tm2_menu/`, the same bytes in every language) is one 1024 x
1024 picture with four pictures on it: the Dolby Pro Logic II logo, the S-Force logo with "ATRAC Decoding
Middleware / "S-FORCE" is a trademark of Sony Corporation.", the THX pm3 Certified Studio logo with its trademark
line, and "The End".

The roll shows cells 0, 2 and 3 as its last three pictures (order 945, 946 and 950). The picture record's `+0x20` is the file's TIM2 picture header (`0x0024A238`), and the recorder reads cell n from the
eight-byte records of the header's eXt block at file offset `0x70` + 8 x n: u16 u, u16 v, then the width and height
in bits 0-11 and 12-23 of the next dword (`0x0053F26E`-`0x0053F28A`).

| Cell | Place on the sheet | Picture |
|---|---|---|
| 0 | 0, 288, 256 x 256 | the THX pm3 Certified Studio logo with its trademark lines |
| 1 | 2, 2, 2 x 2 | a dot the roll does not show |
| 2 | 0, 80, 1024 x 176 | the strip holding the Dolby Pro Logic II logo and the S-Force logo with its lines, one picture |
| 3 | 312, 290, 262 x 74 | "The End" |

### The language trees

All nine language trees run the same `create` sequence: every line has the same position, font and row number in
each. Their credit files hold three sets of text:

| Set | Trees | menu03.bin roles filled, shown | menu04.bin names filled, shown | Rows a line shows that are empty |
|---|---|---|---|---|
| `text_in` | in, kr, cn, ch | 233, 229 | 656, 636 | 2 (`menu04.bin` 657 and 1023) |
| `text_us` | us | 247, 229 | 784, 592 | 46 (`menu04.bin` 424-427, 465-470 and others) |
| `text_fr` | fr, de, it, es | 252, 216 | 854, 592 | 59 (13 roles, 46 names) |

- **The `in` set (in, kr, cn, ch) holds the roll the script was written for.** It shows all but 4 roles and 20
  names, only two of its shown rows are empty, and each role sits over its own staff: the first lines put
  "Original Game Design & Int'l Director" over "Hiroyuki Ito" and "Director" over "Hiroshi Minagawa".
- **The `us` set and the European set (fr, de, it, es) hold an older roll.** Their rows are in another order, so
  role row k and name row k no longer pair: the same first line puts "Main System & Event Programmer" over "Hiroyuki
  Ito (Game Design)", rows no line reaches hold 18 roles and 192 names in `us`, and 46 shown rows are empty.
- The English game loads the `us` files: the US size table gives loader ids 65 and 66 the us files' sizes, 15,548
  and 35,532 bytes.

## Shipped data

[staff-roll.tsv](staff-roll.tsv): the 950 lines in the order the roll shows them.

| Column | Meaning |
|---|---|
| `order` | the line's place in the roll, 1-950 |
| `row` | the screen row it is on, 1-600; two lines share a row in line mode 2 |
| `position` | left at the offset, right the offset from the edge, centred (mode 1); left or right of centre by the offset (mode 2) |
| `font` | A, B or C, the verb `fsroll_nameA`, `fsroll_nameB` or `fsroll_nameC`; `-` for a picture |
| `source` | `menu03.bin` (a role), `menu04.bin` (a name) or `sf_logo_c` (a picture) |
| `source_row` | the row of that file, or the picture cell |
| `script_line` | the line of the decompiled `us` listing of `men_z0005` that adds it (a loop's line for each pass) |
| `text_us`, `text_in`, `text_fr` | the row's text in each set (above); `-` where the row is empty, so the line is blank |

[staff-roll-unshown.tsv](staff-roll-unshown.tsv): the filled rows of each set that no line shows (18 roles and 192
names in `us`, 4 and 20 in `in`, 36 and 262 in the European set).

| Column | Meaning |
|---|---|
| `text_set` | `text_us`, `text_in` or `text_fr` |
| `source` | `menu03.bin` or `menu04.bin` |
| `source_row` | the row |
| `text` | its text |

`Database/Tools/catalogues/staff_roll.py` writes both tables from the decompiled scripts and the credit files.

## Modding notes

- A line's text is a row number, so a roll can be re-credited by editing `menu03.bin` and `menu04.bin` alone;
  re-ordering needs the script.
- The recorder refuses lines past `0x800`.

## Related

- [Staff-roll font bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md) - the roll's typefaces.
- [Action availability](../Controls-And-Input/action-availability.md) - the movie skip, which `men_z0005` does not offer.
- [Movies](../Graphics/movies.md) - movie playback.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md) - the `fsroll` verbs.
