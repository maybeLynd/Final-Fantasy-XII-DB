[Home](../../README.md) / [Menus and HUD](README.md) / Staff roll

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Staff roll: the ending credits, every line in order, and how the roll script lays them out | system | Menus and HUD | Menu screens | The staff roll after the ending: the script men_z0005 that plays it over movie 42, the recorder that turns its fsroll calls into lines, how a line's value picks a role from menu03.bin or a name from menu04.bin, the two line modes and the logo pictures, every one of the 950 lines in order with its text in the three text sets, and the credit rows no line shows. | 0x0053F0D0, 0x0053DD20, 0x0053E380, 0x00511980, 0x005119A0, 0x005119F0, 0x00511890, 0x00511830 |

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

The `fsroll` calls of the actor `staffroll_script`, function `create`, hold 950 lines on 600 rows
([staff-roll.tsv](staff-roll.tsv)). Its `for` loops over a counter show runs of consecutive rows, two per pass in
the two-column parts.

No code runs `create`: the entry-slot footer of every actor of `men_z0005` names only `main` (slot 1), the script's
start list and request lists are empty, and no request in any shipped script names it. `staffroll_main.main` resets
the roll with `fsroll_refresh` (`0x0053EDB0` frees the line block and builds an empty one), sets the speed and the
double mode, and records a fade, a movie mark at frame `0x3CFF`, cell 3 of `sf_logo_c`, a second fade and the end
mode. The roll the game draws over movie 42 is that logo.

### The recorder

Each `fsroll` verb pops its arguments and calls the recorder `0x0053F0D0(kind, a, b)`, which works on the roll object
`[0x02CA8A80]` (the `0x1498`-byte widget with procedure `0x0053E380` that `0x0053ED10` builds for `fsroll_initialize`)
and returns at once when the object is missing, running (`+0xFC`) or holds
`0x800` lines (`+0xC8`). It dispatches on the kind through the table `0x0053F3B0`:

| Verb | Begin | Kind | Effect |
|---|---|---|---|
| `fsroll_speed(n)` | `0x00511810` | 1 | the speed `+0xFF` = n (`0x0053F138`); the roll object starts at 1 (`0x0053E4D9`). Each frame of the roll moves the scroll `+0xEC` on by n (`0x0053E94F`-`0x0053E960`) |
| `fsroll_linedisp(n)` | `0x00511830` | 2 | the line mode `+0x102` = n, at least 1 and at most 3; the slot `+0x103` = 0 (`0x0053F14B`-`0x0053F16D`) |
| `fsroll_layout(a, b)` | `0x00511890` | 3 | the begin pops b, then a (`0x005118A0`, `0x005118AA`); the alignment byte `+0x100` = a and the offset word `+0xF4` = the low 16 bits of b, and the cursor `+0xF0` gets the 0 in r9d added (`0x0053F181`-`0x0053F18E`) |
| `fsroll_blank(n)` | `0x00511900` | 4 | moves the cursor `+0xF0` down n times `0x01DFE0B4`; slot 0 (`0x0053F19C`-`0x0053F1AA`) |
| `fsroll_nameA(v)`, `fsroll_nameB(v)`, `fsroll_nameC(v)` | `0x00511980`, `0x005119A0`, `0x005119F0` | 5, with font 0, 1 or 2 | adds a text line through `0x0053DD20` (below) and moves the cursor by its height (`0x0053F1B9`-`0x0053F1DE`) |
| `fsroll_data(n)` | `0x00511A40` | 6 | adds cell n of the picture `sf_logo_c`, centred on the screen width `0x01E0C1D8`, and moves the cursor by its height; slot 0 (`0x0053F1EA`-`0x0053F2AB`) |
| `fsroll_stop(a, b)` | `0x00511A60` | 7 | a stop: stop n's place `+0x110 + 4n` = the cursor `+0xF0` + a and its hold `+0x210 + 2n` = b times `0x01DFE0B4` frames, n the stop count `+0x106`, then raised by 1; the cursor moves on by a (`0x0053F2B8`-`0x0053F2F1`) |
| `fsroll_fontA(a, b)`, `fsroll_fontB(a, b)`, `fsroll_fontC(a, b)` | `0x00511AC0`, `0x00511B30`, `0x00511BD0` | 8, 9, 10 | the settings of font 0, 1 or 2, eight bytes at `+0xCC` + 8 x font: a at `+0xCC` and b at `+0xCD` (`0x0053F34A`-`0x0053F358`). a is added to the height `+0x16` of each later line in that font, in all three line modes (`0x0053DD59`; `0x0053DE2E`, `0x0053DF6C`, `0x0053DFB2`, `0x0053E094`); b goes to the line's byte `+0x1B` (`0x0053DD74`), and a line with it not 0 is drawn twice, first with the font's bytes `+0xCE` and `+0xCF` added to its x and y (2 and 2 for every font: `0x0053E527`, `0x0053E53D`, `0x0053E550`), then in place (`0x0053E1C1`-`0x0053E262`) |
| `fsroll_setend(m, a, b)` | `0x00511610` | 11 + m (`0x00511643`) | the end mode `+0x104` = m (`0x0053F36D`-`0x0053F38A`); for m 1 or 2 also the end line's value `+0x10C` = a and the offset `+0x10E` = b (`0x0053F391`-`0x0053F399`). At `fsroll_start` (`0x0053F460` calls `0x0053E580`), mode 1 takes the first text line (font 0 to 2) whose value `+0x0C` is a and mode 2 the first picture line (byte `+0x18` = 3) whose cell `+0x0C` is a, and sets the cursor `+0xF0` to its place `+0x10` + b − (the screen height `0x01E0C1DC` − its height `+0x16`) / 2 (`0x0053E5AF`-`0x0053E62F`). The scroll stops there (`0x0053E96D`, `0x0053EB04`). Mode 0, or no such line, leaves the cursor where the last line left it. m 3 gives kind 14, a movie mark at frame a, and a larger m a kind the recorder ignores. The roll's two calls, `fsroll_setend(2, 3, 0)`, end on picture cell 3, "The End" |
| `fsroll_moviewait(n)` | `0x00511DE0` | 14 | a movie mark: mark m's place `+0x290 + 4m` = the cursor `+0xF0` and its frame `+0x690 + 4m` = n, m the mark count `+0x10A`, then raised by 1 and held at most 255 (`0x0053F2FD`-`0x0053F336`). When the scroll `+0xEC` reaches a mark's place less the screen height `0x01E0C1DC` (`0x0053E976`-`0x0053E9A8`), the roll waits (state `+0xFC` = 5, n at `+0xF8`; `0x0053EA5E`-`0x0053EA70`) until the movie's frame (`0x0035B730`, a jump to `0x00184810`; [Movies](../Graphics/movies.md)) is at least n, or the read-out is -1, which `0x00184810` returns outside state 3 (`0x0053E7CA`-`0x0053E7DD`) |
| `fsroll_setparam(k, a, b)` | `0x00511760` | k | passes its first argument k to the recorder as the kind and the other two as a and b (`0x0051178E`-`0x00511793`); no shipped script calls it |

A kind outside 1 to 14 does nothing (`0x0053F113` to `0x0053F3A0`). Kinds 1 and 8 to 14 do not move the cursor: their
closing `add [rbx+0xF0], r9d` adds the 0 that `0x0053F10A` put in r9d.

The roll object starts in line mode 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053E4EE` |

</details>

`0x0053ED10`, the begin of `fsroll_initialize`¹, builds the `0xC8`-byte loader `0x0053EB90` while
`[0x02CA8A78]` is 0 and then the roll while `[0x02CA8A80]` is 0, each with a zero record². On
message 1 the roll stores itself at `[0x02CA8A80]`, puts the screen size `0x01E0C1D8` and `0x01E0C1DC` at `+0x9C` and
`+0x9E` and 0 at `+0x98`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00511540` |
| ² | `0x0053ED14`-`0x0053ED4F` |
| ³ | `0x0053E4A6`-`0x0053E4CD` |

</details>

The word store that sets the speed to 1 also sets the alignment `+0x100` to 0¹. Message 1 then sets
`+0x1494` to `0x80`, the cursor `+0xF0` to the screen height and `+0xC0` to the block `0x00249810(2, 0x10000)`, cleared
to zero². Each font's bytes `+0xCE` and `+0xCF` become 2 and 2, and its float at
`+0xD0` + 8 x font becomes 1.0³; it ends with `0x00247930(roll, 0x69)`⁴. The
roll's other messages:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053E4D9` |
| ² | `0x0053E4E2`-`0x0053E51D` |
| ³ | `0x0053E527`-`0x0053E559` |
| ⁴ | `0x0053E563` |

</details>

- Message 2: when `0x001EDEC0(+0xB4)` answers non-zero it runs `0x0053E640(roll)`¹.
- Message 4: when `0x002DDC50()` answers non-zero it calls `0x002D8BB0(+0x38, 1)` and `0x00249FD0` with the box x 0, y
  `0xC`, the screen width and the screen height less `0x18`². It then calls `0x0053E0B0(roll)`
 ³, and `0x002D8BB0(+0x38, 0)` when `0x002DDC50()` again answers non-zero⁴.
- Message 18: with `+0xC0` set it passes the block to `0x003697F0` and sets `+0xC0` and the line count `+0xC8` to 0;
  `[0x02CA8A80]` becomes 0 either way⁵.
- Any other message goes to the default `0x005C5230`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053E479`-`0x0053E48F` |
| ² | `0x0053E400`-`0x0053E443` |
| ³ | `0x0053E44B` |
| ⁴ | `0x0053E450`-`0x0053E462` |
| ⁵ | `0x0053E3C7`-`0x0053E3E7` |
| ⁶ | `0x0053E3B0`-`0x0053E3C2` |

</details>

### A text line

`0x0053DD20(line, roll, font, v)` fills the line's 32-byte record:

- **The text.** When bit `0x8000` of v is set, the text is id 25000 + (v & `0x7FFF`), else id 26000 + v
 ¹, looked up by `0x002F9860`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053DD90`-`0x0053DDA5` |

</details>

  Text group 25 is `menu03.bin` (loader id 65) and group 26 is
  `menu04.bin` (loader id 66), so a value with bit `0x8000` shows row v & `0x7FFF` of `menu03.bin`, the roles, and any
  other value shows row v of `menu04.bin`, the names. Both files are lists of `ex00` rows in UTF-16
  ([Text codes](text-codes.md)).
- **Line mode 1**¹: the line takes a row of its own at the cursor. Alignment 0 puts its left
  edge at the offset, 1 puts its right edge the offset from the right edge of the roll's width `+0x9C`, 2
  centres it; any other value puts it at the left edge.
- **Line mode 2**²: lines go two to a row. The first ends the offset left of the centre, at
  the cursor; the second starts the offset right of the centre on the same row, and the cursor then moves by the
  difference between the two lines' heights³.
- Mode 3 puts three lines to a row⁴; the roll does not use it.
- The slot then advances, (slot + 1) mod the mode⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053DFFB`-`0x0053E0A3` |
| ² | `0x0053DF17`-`0x0053DFE4` |
| ³ | `0x0053DFD0`-`0x0053DFE1` |
| ⁴ | `0x0053DDFE`-`0x0053DEBA` |
| ⁵ | `0x0053DECE`-`0x0053DEE8` |

</details>

The faces are the staff-roll fonts of [Staff-roll font bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md).

### The logos

`sf_logo_c.tm2` (`ps2data/image/ff12/myoshiok/<lang>/tm2_menu/`, the same bytes in every language) is one 1024 x
1024 picture with four pictures on it: the Dolby Pro Logic II logo, the S-Force logo with "ATRAC Decoding
Middleware / "S-FORCE" is a trademark of Sony Corporation.", the THX pm3 Certified Studio logo with its trademark
line, and "The End".

The roll shows cells 0, 2 and 3 as its last three pictures (order 945, 946 and 950). The picture record's `+0x20` is the file's TIM2 picture header¹, and the recorder reads cell n from the
eight-byte records of the header's eXt block at file offset `0x70` + 8 x n: u16 u, u16 v, then the width and height
in the bits under mask `0xFFFFFF` of the next dword².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024A238` |
| ² | `0x0053F26E`-`0x0053F28A` |

</details>

| Cell | Place on the sheet | Picture |
|---|---|---|
| 0 | 0, 288, 256 x 256 | the THX pm3 Certified Studio logo with its trademark lines |
| 1 | 2, 2, 2 x 2 | a dot the roll does not show |
| 2 | 0, 80, 1024 x 176 | the strip holding the Dolby Pro Logic II logo and the S-Force logo with its lines, one picture |
| 3 | 312, 290, 262 x 74 | "The End" |

### The fades

`fsroll_fade(a, b, c, d)`¹ does not go through the recorder: it jumps to `0x0053EFC0`, which appends a
20-byte fade record to the roll object's 128 at `+0xA90` (count `+0x1492`) unless the object is missing or running
(`+0xFC`, `0x0053EFD7`), and moves the cursor `+0xF0` on by a + 3². b, c and d are 30 fps frame
counts, multiplied by `0x01DFE0B4`, `b > -1 ? b × [0x01DFE0B4] : b` and the same for d (`cmp dx, -1` at `0x0053F04C`,
`cmp r9w, -1` at `0x0053F07E`; `c × [0x01DFE0B4]` at `0x0053F000`); a b or d of -1 or less is kept as it is.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00511E00` |
| ² | `0x0053F0B6`-`0x0053F0B9` |

</details>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | place | the cursor at the append (`0x0053EFF8`) |
| `+0x04` | `i16` | totalFrames | c x `[0x01DFE0B4]` + 3, plus b and d when they are not negative (`0x0053F000`, `0x0053F035`-`0x0053F093`) |
| `+0x06` | `i16` | hold | c x `[0x01DFE0B4]` (`0x0053F000`, `0x0053F02C`) |
| `08`, `0C` | `i16` | fadeInLeft, fadeInLength | b (`0x0053F008`, `0x0053F011`, `0x0053F05F`, `0x0053F068`) |
| `0A`, `0E` | `i16` | fadeOutLeft, fadeOutLength | d (`0x0053F01A`, `0x0053F023`, `0x0053F09C`, `0x0053F0A5`) |
| `+0x10` | `i16` | jump | a (`0x0053F043`) |

The runner `0x0053E640` starts a fade when the scroll `+0xEC` reaches its place less the screen height `0x01E0C1DC`,
`+0xEC >= place - [0x01E0C1DC]`¹: the scroll becomes the place less the screen height plus a,
at most the roll's end, the cursor `+0xF0`: `+0xEC = min(place - [0x01E0C1DC] + a, +0xF0)`².
The countdown `+0xF8` becomes the total³, and the roll stops scrolling in state 6, phase 1⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053E9B9`-`0x0053E9E9` |
| ² | `0x0053EA87`-`0x0053EA9F` |
| ³ | `0x0053EAA5`-`0x0053EAAA` |
| ⁴ | `0x0053EAB2`-`0x0053EAB9` |

</details>

Phase 1 raises the text level `+0x1494`, the alpha of the roll's text colour¹, from 0 to `0x80` over b
frames; phase 3 holds it for c frames; phase 2 lowers it to 0 over d frames, and a negative d skips it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053E101` |
| ² | `0x0053E6A6`-`0x0053E78F` |

</details>

When the countdown reaches 0 the runner takes the next fade (`+0x1490`) and scrolls again, state 1¹; while the level is 0 it keeps scrolling within the same frame². While
the roll waits for the movie (state 5) each pending fade's place moves with the lines still below the screen³. The roll script calls `fsroll_fade` 67 times.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0053E796`-`0x0053E7AA` |
| ² | `0x0053EA3E`-`0x0053EA46` |
| ³ | `0x0053E7E3`-`0x0053E868` |

</details>

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

<details>
<summary>Show the shipped data</summary>

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

Both tables are read from the decompiled `us` listing of `men_z0005` and the credit files `menu03.bin` and
`menu04.bin` of each text set.

</details>

## Modding notes

- A line's text is a row number, so a roll can be re-credited by editing `menu03.bin` and `menu04.bin` alone;
  re-ordering needs the script.
- The recorder refuses lines past `0x800`.

## Related

- [Staff-roll font bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md) - the roll's typefaces.
- [Action availability](../Controls-And-Input/action-availability.md) - the movie skip, which `men_z0005` does not offer.
- [Movies](../Graphics/movies.md) - movie playback.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md) - the `fsroll` verbs.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 53 calls with 10 other topics</summary>

**Engine core** (explained on [global state accessors](../Engine-Core/global-state-accessors.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0053E380`](staff-roll.md) | calls | [`0x001EDEC0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |

**Controls and input** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00249810`](staff-roll.md) | is called by | [`0x00291C80`](../Graphics/effect-file-list.md) (on effect file list) |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md), [menu lists](menu-lists.md), [escape](../Controls-And-Input/escape.md), [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [btm exfont bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md), [call signatures](../Engine-Core/call-signatures.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDEC0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x002B7B80`](map-screens.md) (on map screens)<br>[`0x002BAF80`](widgets.md) (on widgets)<br>[`0x002BC3E0`](widgets.md) (on widgets)<br>[`0x002D2DB0`](widgets.md) (on widgets)<br>[`0x00366B80`](../Controls-And-Input/escape.md) (on escape) |
| [`0x00249FD0`](../Game-Files-And-Data-Tables/ui-typed-lists.md) (on ui typed lists) | calls | [`0x003A1DB0`](../PhyreEngine/the-frame.md) Render command: submit current buffer and swap (on the frame) |
| [`0x00249FD0`](../Game-Files-And-Data-Tables/ui-typed-lists.md) (on ui typed lists) | is called by | [`0x002B8EE0`](map-screens.md) (on map screens) |
| [`0x002D8BB0`](staff-roll.md) | is called by | [`0x0053E0B0`](staff-roll.md) |
| [`0x002DDC50`](battle-numbers.md) (on battle numbers) | is called by | [`0x003649A0`](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md) (on btm exfont bitmaps)<br>[`0x00366110`](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md) (on btm exfont bitmaps)<br>[`0x003F0170`](hud.md) (on hud)<br>[`0x00505570`](battle-numbers.md) (on battle numbers)<br>[`0x00505E00`](battle-numbers.md) (on battle numbers) |
| [`0x0053E0B0`](staff-roll.md) | calls | [`0x003649A0`](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md) (on btm exfont bitmaps) |
| [`0x0053E380`](staff-roll.md) | calls | [`0x0053E0B0`](staff-roll.md) |

**Game files and data tables** (explained on [verb table](../Scripts-And-Script-Commands/verb-table.md), [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0053EB90`](staff-roll.md) | calls | [`0x002493D0`](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md) (on mrp menu resource packages)<br>[`0x00249580`](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md) (on mrp menu resource packages) |

**Saving, loading and settings** (explained on [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDEC0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x00582860`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |

**Scripts and script commands** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [btm exfont bitmaps](../Game-Files-And-Data-Tables/btm-exfont-bitmaps.md), [verb table](../Scripts-And-Script-Commands/verb-table.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00511610`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511760`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511810`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511830`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511890`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511900`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511980`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x005119A0`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x005119F0`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511A40`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511A60`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511AC0`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511B30`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511BD0`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511DE0`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00511E00`](staff-roll.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0053ED10`](staff-roll.md) | is called by | [`0x00511540`](staff-roll.md) |
| [`0x0053EFC0`](staff-roll.md) | is called by | [`0x00511E00`](staff-roll.md) |
| [`0x0053F0D0`](staff-roll.md) | is called by | [`0x00511610`](staff-roll.md)<br>[`0x00511760`](staff-roll.md)<br>[`0x00511810`](staff-roll.md)<br>[`0x00511830`](staff-roll.md)<br>[`0x00511890`](staff-roll.md)<br>[`0x00511900`](staff-roll.md)<br>[`0x00511980`](staff-roll.md)<br>[`0x005119A0`](staff-roll.md)<br>[`0x005119F0`](staff-roll.md)<br>[`0x00511A40`](staff-roll.md)<br>[`0x00511A60`](staff-roll.md)<br>[`0x00511AC0`](staff-roll.md) |
| [`0x0053F0D0`](staff-roll.md) | is also called by | [`0x00511B30`](staff-roll.md)<br>[`0x00511BD0`](staff-roll.md)<br>[`0x00511DE0`](staff-roll.md) |

</details>
