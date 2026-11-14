---
title: "Menu sprites: the shared picture atlases, how a sprite is found and drawn, the hand cursor, arrows and marks, and the pulsing selection bar"
kind: "system"
category: "Menus and HUD"
addresses: "0x002467A0, 0x00280750, 0x0024B0C0, 0x002D8BB0, 0x002DB080, 0x002426F0, 0x00242C90, 0x00244500, 0x002445A0, 0x002445C0"
---

## What the player sees

- A pointing hand marks the chosen row in the battle party list and the Gambits screen; it can also be drawn as an
  open hand.
- Scrolling lists and message windows show small up and down triangles, the battle menu shows left and right arrows,
  and message windows carry wing ornaments on both sides.
- The highlighted row of a list sits on a bar that fades out to the right and slowly dims and brightens.
- The Gambits row of the battle menu shows ON or OFF.

Each of the five shared atlases is one TIM2 picture in `texpack_ys.bin`, and its `eXt` block holds a table of sprite
records, each giving a rectangle of the picture and its palette. A menu names a sprite by atlas, set, group and frame,
and the game draws that rectangle where the menu asks.

## How it works

### The atlases

`0x002467A0` (from `0x00253780`, `0x002538DE`) registers five atlas names with `0x0024A4E0` and requests kind 7 `0xD6` through
`0x00249180`. It returns at once while the pack pointer `0x0208EA88` is set (`0x002467B1`) and registers only the cells
that are still null, each with `0x0024A4E0(name, 2)` (`0x002467B7`-`0x0024685A`). The request passes its argument on with
kind 7, id `0xD6`, 3, 1 and the completion `0x00246A10` (`0x00246887`), and the pack buffer `0x00249180` returns goes to
`0x0208EA88` (`0x0024688C`).

Its completion `0x00246A10` binds entries 0 to 4 of `texpack_ys.bin` to them, each through `0x0024A1D0` at the pack
start plus the entry's directory offset. It does nothing while `0x0208EA88` is null (`0x00246A1E`) and skips a null
cell (`0x00246A2E`-`0x00246AA5`)
([PS2 data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md)):

| Cell | Atlas | Entry |
|---|---|---:|
| `0x0208EAA8` | `buttonicon` | `0` |
| `0x0208EA98` | `bt_win_0_c` | `1` |
| `0x0208EAA0` | `cm_win_c` | `2` |
| `0x0208EA90` | `cursol_4_p` | `3` |
| `0x0208EAB8` | `keyboard` | `4` |

`0x00280750` (reached from `0x002808D0`) registers ten more at `[0x0209AC30] + 0x338` to `+0x380`, in this order:
`battle_4_c`, `targetline_p`, `s_font_c`, `battle_4_p`, `mini_face_c`, `partytop_4_c`, `partytop_8_c`, `party_grd_2`,
`icons_c` and `extra_c`, and requests kind 7 `0xD7` (`0x00280861`). It returns at once while the pack buffer
`+0x3D8` is set (`0x0028077F`), registers only the slots that are still null (`0x00280807`), and clears bit `0x80`
of `+0x38` in the entries of `party_grd_2` and `icons_c` (`0x00280895`, `0x002808AD`).

The getters `0x0035D460` and `0x0035D3D0` return
`battle_4_c` and `battle_4_p`; `0x0039BB00(n)` returns `cursol_4_p` for 1, `battle_4_c` for 2 and `buttonicon` otherwise
(`0x002441F0`).

### Finding a sprite

A sprite is named by its atlas, a set, a group within the set and a frame within the group. The records sit in the
`eXt` block of the atlas's picture ([TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md)). With `T` the
picture header plus `0x30`:

```python
groups = T + 0x14 + u16[T + 0x14 + set x 2] x 2
record = T + u16[T + 0x10] + (u16[groups + group x 2] + frame) x 8
palette = u8[T + u16[T + 0x12] + (record byte 7 >> 4)] + (record byte 7 & 0xF)
```

Every record, with its rectangle and palette, is in the sprite table of
[TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md), and each item's selection is joined to it on
[Typed UI lists](../Game-Files-And-Data-Tables/ui-typed-lists.md).

`0x0024B0C0(atlas, set << 8 | group, frame)` returns the record. Every helper below repeats the same arithmetic with its
set and group fixed, and writes the palette byte to the widget's `+0x5C`. For an 8-bit atlas the draw adds that byte
to the texture descriptor as the palette number (`0x002DB8C5`-`0x002DB8D3`).

### Drawing

`0x002D8BB0(widget, open)` brackets a group of draws: the first open sets the clip to the whole screen through
`0x00249FD0(0)`, and the last close sets it to the widget's clip box `+0x48` when `+0x5C` bit `0x20000` is set.
The depth is the byte `+0x5D`: `open` 1 adds 1 and only a count that was 0 sets the clip (`0x002D8BB0`-`0x002D8BC5`);
any other `open` takes 1 off and only a count that reaches 0 sets the clip, to `0x00249FD0(0)`, the whole screen, when
bit `0x20000` is clear (`0x002D8BCA`-`0x002D8BF9`). The other opens and closes do nothing more.

Three forwarders reach the sprite draw `0x002DB080(widget, atlas, source, destination, record, 0, scale)`:

| Forwarder | Destination | Record |
|---|---|---|
| `0x002D8CB0(widget, atlas, source, x, y)` | the source's own size at `x`, `y` | the default `0x00917250` |
| `0x002D8C80(widget, atlas, source, box)` | `box`, stretched | the default |
| `0x002D8D10(widget, atlas, source, box, record, scale)` | `box` | the caller's |

The draw pass gives each widget a fresh `0xA0`-byte draw record from `0x002D8C00` (`0x00245EA7`): clip on (`+0x5C` bit `0x20000`),
brightness (RGB scale) `0x80` at `+0x5A` (`0x002D8C22`), colour `0x80808080` at `+0x90` and `+0x94`, and 1.0
at `+0x60`, `+0x68` and `+0x6C`.

`0x002D8530` applies its clip box `+0x48`, or no clip box when bit `0x20000` is clear, through `0x00249FD0`;
`0x002DD2F0(record, box)` clips to `box` moved by the record's `+0x50`/`+0x52` and cut to its clip box (`0x00249EE0`), or
to an empty box when they do not meet. For the sprite draw (`0x002DBD81`), `0x002DD910` maps the four corners of a quad
from the menu's space, centred on 2048, onto the render target, using the target's width and height (`0x00182EB0`,
`0x00182E80`, 1920 and 1080 without a display) and the aspect `0x00182EE0`.

The sprite draw `0x002DB080` calls `0x002DD910` only for an atlas with no pointer at `+0x20` whose name holds
the text
`screenCapture` (`0x002DB9E6`, `0x002DBA01`, `0x002DBC93`-`0x002DBC96`, `0x002DBD4A`-`0x002DBD4D`).

The record's first word flips the source left to right (bit `0x1`, `0x002DB1B8`) and top to bottom (bit `0x2`, `0x002DB1D0`); a
non-zero float at `+0x04` rotates the sprite (`0x002DB22F`), about `+0x10`/`+0x12` when bit `0x4` is set and about the
centre otherwise; a pointer at `+0x08` supplies four corner colours.

In order, `0x002DB080` does this, the draw record being its first argument, the widget:

1. It returns at once when the dword `0x0215E6D0` is 0 (`0x002DB0B0`, `0x002DB170`).
2. From the source box words x, y, w, h it takes u0 = max(x, 0), v0 = max(y, 0),
   u1 = x + w and v1 = y + h. For the vertices it swaps the u pair for record bit `0x1` and the v pair
   for bit `0x2` (`0x002DB1B8`-`0x002DB1E5`); steps 10 and 12 take u0, u1, v0 and v1 unswapped, and step 13
   the swapped pairs.
3. It takes the packet cursor `0x02EBEFC0 + 0x18 × [0x02EBEFF0] + 8` and calls `0x00181560`
   (`0x002DB1EA`-`0x002DB218`).
4. With the record's float `+0x04` equal to 0 it copies the `0x40` bytes at the draw
   record's start to `0x022D8F30` and to the packet's `+0x20` (`0x002DB24F`-`0x002DB2CB`). The
   corners are the destination box (x, y, x + w, y + h), each put through `0x00202B70`; its
   x and y then become `x / v[3]` and `y / v[3]`, over its fourth component
   (`0x002DB22F`-`0x002DB36A`).
5. On that path the mode is the sixth argument when the source width and height equal the
   destination's, and 2 otherwise (`0x002DB2CF`-`0x002DB2F0`).
6. With a non-zero float the pivot is the record's words `+0x10` and `+0x12` for bit `0x4`
   and the destination's `width / 2` and `height / 2` otherwise (`0x002DB371`-`0x002DB398`); the
   matrix is built by `0x00203170`, `0x00398C50` with the angle, a second `0x00203170` whose
   elements 0 and 5 take the seventh argument, and `0x00397910` twice; the mode is 2
   (`0x002DB3D5`-`0x002DB467`).
   - With the pivot px, py and the destination's width w and height h, the corners are -px, -py and
     w - px, h - py for bit `0x4`, and -(w >> 1), -(h >> 1) and w >> 1, h >> 1 otherwise
     (`0x002DB37D`-`0x002DB3D2`).
   - Before the second `0x00397910`, row 3 of the matrix takes x + px and y + py of the destination
     (`0x002DB415`-`0x002DB452`); the finished matrix goes to `0x022D8F30` and to the packet's `+0x20`
     (`0x002DB45C`-`0x002DB4B2`).
7. The four corner colours come from the record's pointer `+0x08`; when that pointer is
   null or bit `0x40000` of the draw record's `+0x5C` is set, all four take the draw
   record's bytes `+0x90`-`+0x93` (`0x002DB532`-`0x002DB546`, `0x002DB657`). Every vertex takes
   the draw record's dword `+0x70` as its depth.
8. The packet takes the draw record's `+0x88` for register `0x14`, its signed word `+0x5A`
   three times and its signed word `+0x58` as four dwords, then the qword 0, the dwords
   `0x10000000` and `0x6C088100` and the qwords `0x1000000000000006` and `0xE`
   (`0x002DB7A0`-`0x002DB7FB`). `0x001816F0` is called with the same four signed words
   (`0x002DB7C6`-`0x002DB7D4`).
9. The atlas qword `+0x30` goes to register 6, changed in one of three ways by bit
   `0x10000` of `+0x5C` and by the bits under `0x3F00` of the atlas dword `+0x38` being
   `0x1400` or `0x1300` (`0x002DB803`-`0x002DB908`). For `0x1400` an entry for register `0x16`
   follows, the atlas qword with the low four bits of `+0x5C` in its top byte
   (`0x002DB86F`-`0x002DB892`); on every other way, 0 for register `0x7F`.
10. It sends 0 to register `0x14` and packs v1 - 1, v0, u1 - 1 and u0 into 10-bit fields
    of one word for register 8, above a low nibble of `0xA` (`0x002DB914`-`0x002DB95B`). It
    sends the draw record's `+0x80` to register `0x47` and `+0x78` to register `0x42`
    (`0x002DB95F`-`0x002DB97A`).
11. One of two fixed words follows with `0x431`: `0x30AA400000008004` on the condition of
    step 7 and `0x30AE400000008004` otherwise (`0x002DB982`-`0x002DB9B1`). It calls
    `0x00181910(+0x80)`, `0x001816B0(+0x78)` and `0x00181870(3)` (`0x002DB9B5`-`0x002DB9CF`).
12. It looks for the text `screenCapture` in the atlas name with `strstr` (`0x002DB9D4`-
    `0x002DB9E6`): found, it calls `0x00181890(1, 1, 0, 0, 0, 0)`; not found,
    `0x00181890(1, 2, u0, u1 - 1, v0, v1 - 1)` (`0x002DB9EC`-`0x002DBA2F`).
    - It closes the packet and calls `0x0016D6A0`, a bare `ret`, and then adds 0 to the cursor
      (`0x002DBA7A`-`0x002DBA96`): the amount added is a stack dword less the packet's start, with its low
      four bits cleared, and that dword holds the packet's start (`0x002DBA56`).
    - `0x003A1DB0` then hands the buffer up to the cursor, which leaves this packet out, to `0x0036F360` and
      starts the other buffer (`0x002DBA9B`; `0x003A1DD4`-`0x003A1DFA`).
13. It builds four `0x30`-byte vertices (position, depth as a float, 1.0, colours, mode).
    With a pointer at atlas `+0x20` it calls `0x001819A0` with the words `+0x14` and `+0x16`
    of the object that pointer names, the atlas, the draw record's byte `+0x5C` and a fifth argument
    (`0x002DBC93`-`0x002DBCDF`), and sets the texture coordinates from the swapped pairs of step 2
    (`0x002DBCE4`-`0x002DBD48`).
    - The fifth argument is bit `0x200000` of `+0x5C` as 1 or 0 when the atlas dword `+0x38` has
      `0x1300` under `0x3F00` and `+0x5C` has bit `0x100000`, and 0 otherwise (`0x002DBC9C`-`0x002DBCCC`).
14. Otherwise, when the name was found, it calls `0x00181A10(0x00182EB0(), h, atlas)` with
    `h = 0x00182E80() × 512 / 448`, then `0x002DD910` on the quad and `0x001816D0(2)`
    (`0x002DBD4A`-`0x002DBD8B`). On every path it ends with `0x00181460(quad, 4)` and
    `0x00181330()` (`0x002DBD90`-`0x002DBDA1`).

### The hand cursor

`0x002426F0(widget, x, y, kind)` draws the hand from `cursol_4_p` set 0 group 0: the pointing hand, or the next record,
an open hand, for kind 4 (`0x00242719`-`0x00242738`). The kind's row in `0x01E0C150` gives the offset from two layout keys and the flip
word for the record:

| Kind | Offset keys | Flip |
|---:|---|---:|
| `0` | `mCursorRightX`, `mCursorRightY` (`0x01E0C120`, `0x01E0C124`) | 0 |
| `1` | `mCursorDownX`, `mCursorDownY` | 0 |
| `2` | `mCursorLeftX`, `mCursorLeftY` | 1 |
| `3` | `mCursorUpX`, `mCursorUpY` | 3 |
| `4` | `mCursorOpenX`, `mCursorOpenY` (`0x01E0C140`, `0x01E0C144`) | 0 |

It is called by the battle party slot `0x0029A0A0` (`0x0029A1AF`), the Gambits screen `0x005691E0` (`0x00569775`), `0x00367940`
and `0x00367AA0`. The keys are in [Screen layouts](screen-layouts.md).

How it draws:

- The atlas is `[0x0208EA90]` (`0x00242702`). The source box is the sprite record's x, y and the two 12-bit sizes of its
  dword `+0x04` (`0x00242748`-`0x00242780`); the destination is `x` and `y` plus the two keys' words, at the same size
  (`0x00242785`-`0x002427CA`), and it writes the palette byte to `+0x5C` (`0x002427E3`-`0x00242809`).
- Each `0x18`-byte row holds a float at `+0x00`, which goes to the draw record's rotation `+0x04` and is 0 in all
  five rows, the flip at `+0x04` and the two key pointers at `+0x08` and `+0x10`; the record's corner colours are 0
  (`0x0024274E`, `0x002427C4`-`0x002427DE`). The kind indexes the table with no range check (`0x0024273B`).
- It opens the draw with `0x002D8BB0(widget, 1)`, draws through `0x002D8D10` with scale 1.0 and closes with
  `0x002D8BB0(widget, 0)` (`0x0024280C`-`0x00242847`).

### Arrows, triangles and marks

Each of these helpers draws one group, the frame argument picking the record:

| Helper | Atlas, set, group | Pictures | Placed | Called by |
|---|---|---|---|---|
| `0x00242F30(w, x, y, frame)` | `cursol_4_p` 0, 2 | left and right arrows, outlined (frames 0, 1) and filled (2, 3) | centred | the battle menu panel `0x00276D30` |
| `0x00244070(w, x, y, frame)` | `cursol_4_p` 0, 6 | up (0) and down (1) triangles | centred | the scroll list `0x002D1750`, message windows `0x002A4430`, `0x002A86A0` |
| `0x00243F70(w, x, y, frame)` | `cursol_4_p` 0, 12 | an outlined down triangle, two frames | centred | the second confirm `0x00241D40`, `0x002A4430` |
| `0x00243030(w, x, y, open)` | `cursol_4_p` 0, 1 | a spinning disc, eight frames | centred | the menu list window `0x002CD170`, `0x002D1750` |
| `0x00243160(w, x, y)` | `cursol_4_p` 0, 9 | a round `!` mark | centred | `0x002CD170` |
| `0x00242A80(w, x, y, width, height)` | `cursol_4_p` 0, 8 | a rectangular frame in colour `0x65` of `0x002DD7E0` | stretched to the box | `0x002CABF0` |
| `0x00242970(w, x, h, frame)` | `buttonicon` 0, 6 | wing ornaments, left (0) and right (1) | the left ends at `x`, the right starts at `x`, centred in height `h` | the message window `0x002A4170` |
| `0x00242870(w, x, y, frame)` | `battle_4_p` 0, 1 | bubbles: a smiley, a burst, a magnifier, a sign; returns the width | at `x`, `y` | `0x002A4170` |
| `0x00242600(w, x, y, unused, frame)` | `battle_4_c` 14, 2 | OFF (0) and ON (1) | left edge at `x`, centred on `y` | the battle menu's Gambits row `0x00276BE0`, `0x0027AD70` |

The disc turns through its eight frames, four frames each, during the first 32 of every 64 frames of the counter
`0x0208F570`, and rests on frame 0 for the other 32 (`0x00243042`-`0x00243068`). Its `open` argument set means the caller has
already opened the draw.

### The selection bar

`0x00242C90(widget, x, y, width, height, colour)` draws a list's highlighted row from `battle_4_c` set 3 group 1. It is
called by the scroll list `0x002D2DB0` (`0x002D378F`) and the member-list row `0x00284450` (`0x0028450C`), and draws nothing
while `0x002DD4B0` is 0.

1. The head is `max(width x 0.3, w0)` long, `w0` being the first record's width.
2. The first record is drawn at `x`, `w0` wide and `height` high (`0x002D9DB0`).
3. When the head is longer, the second record is stretched over the rest of it.
4. A colour quad covers the remaining width, with the alpha of its two right corners cleared, so the bar fades out to
   the right (`0x002DA2D0`).

The colour is the caller's, or `0x40507275` when the caller gives no colour; its alpha byte `+0x93` goes through the
pulse `0x00244500` first.

### The pulse

`0x002445A0(on)` switches the pulse (`0x0208ED50`) and restarts it; `0x002445C0()` restarts it alone, from 33 call sites in menu code. Restarting stores the frame counter in `0x0208ED54`. With the pulse on, `0x00244500(a)` returns, for
`e` frames since the restart:

| Frames `e` | Alpha |
|---|---|
| 0 to 7 | `a` |
| 8 to 79 | `a/2 + a/2 x curve2(72, 80 - e)`, falling to half |
| 80 to 83 | `a/2` |
| 84 to 155 | `a/2 + a/2 x curve1(72, e - 84)`, rising to full |
| 156 or more | `a`, and the cycle restarts: the first call at 156 frames or later stores the frame counter in `0x0208ED54` (`0x0024456C`-`0x00244583`) |

The curves are those of [Widgets](widgets.md). With the pulse off the alpha stays `a`. The Party Menu (`0x00281ED0`)
and its member lists (`0x00284EC0`, `0x00285B20`) switch it.
`a` is the low byte of the argument, `e` an unsigned difference, and `a/2` rounds down; the curve's share is
truncated: `h = (a & 0xFF) >> 1` and `alpha = h + (int)(curve * h)`, with `e = [0x0208F570] - [0x0208ED54]`
(`0x00244506`-`0x00244554`).

## Layouts

A sprite record, 8 bytes, in the record table of an atlas's `eXt` block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | x | left edge in the picture |
| `+0x02` | `u16` | y | top edge |
| `+0x04` | `u32` | size | mask `0xFFF` width, `0xFFF000` height, `0xF000000` palette added, `0xF0000000` palette group |

The draw record that `0x002D8D10` passes on:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | flags | bit `0x1` flip left to right, bit `0x2` flip top to bottom, bit `0x4` rotate about `+0x10` |
| `+0x04` | `f32` | angle | 0 for no rotation |
| `+0x08` | `u8*` | corners | four RGBA corner colours, or null for the widget's colour `+0x90` |
| `+0x10` | `i16[2]` | pivot | rotation centre when bit `0x4` is set |

The widget draw record, `0xA0` bytes, that `0x002D8C00` fills for each widget in the draw pass (kept at the widget's
`+0x38`, `0x00245EB0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x5C` | `u32` | flags | byte 0 is the text palette, handed to the text context by `0x002DD680` (`0x002DD69E`-`0x002DD6A5`) and `0x002DD5D0` (`0x002DD5F1`); bit `0x20000` turns the clip on: set by the fill (`0x002D8C16`), kept for a child only when the parent's record has it (`0x0024614D`-`0x0024616F`), and `0x002D8530` clips to `+0x48` only while it is set (`0x002D8530`-`0x002D8544`); bit `0x40000` makes the sprite draw ignore the corner colours and draw flat in the record's colour (`0x002DB53F`, `0x002DB988`-`0x002DB99B`, `0x002DBAB5`) |
| `+0x60` | `f32` | textSize | the text size, 1.0 from the fill (`0x002D8C58`): `0x002DD680` hands it to the text context's `+0x34` (`0x002DD6AF`-`0x002DD6B4`) and `0x002DD5D0` to the UTF-16 one (`0x002DD5EC`); the help line sets it to 1.0 before it draws (`0x002BF909`) |
| `+0x68` | `f32` | f68 | 1.0 from the fill (`0x002D8C5F`); the draw pass saves the whole record before a node's draw message and copies it back after (`0x0024625B`-`0x002462BA`, `0x002462E5`-`0x00246344`) |
| `+0x6C` | `f32` | f6C | 1.0 from the fill (`0x002D8C66`); saved and restored with the record in the same way |
| `+0x88` | `u64` | gsTex1 | `0x60` from the fill (`0x002D8C26`): the value the sprite draw `0x002DB080` sends to GS register `0x14`, TEX1_1 (`0x002DB7A0`-`0x002DB7AA`), as `0x002D9C40` does (`0x002D9CE5`-`0x002D9CF3`); `0x60` sets MMAG and MMIN to 1, linear filtering |

## Shipped data

The counts are those of `us/packfiles/texpack_ys.bin`; the record count runs from the record table to the end of the
picture
header.

| Entry | Atlas | Picture | Sprite records |
|---:|---|---|---:|
| `0` | `buttonicon` | 512 x 256, 8-bit | 40 |
| `1` | `bt_win_0_c` | 256 x 256, 8-bit | 42 |
| `2` | `cm_win_c` | 128 x 128, 8-bit | 10 |
| `3` | `cursol_4_p` | 512 x 256, 8-bit | 50 |
| `4` | `keyboard` | 1024 x 1024, 8-bit | 1,142 |

`cursol_4_p` has one set. Each of the five entries has the same bytes in at least eight of the ten language
folders.

## Modding notes

- The hand, arrows, triangles and marks are the records of `cursol_4_p`, entry 3 of `texpack_ys.bin`. The code adds a
  frame number to a group's first record, so a group must keep its records together and in order.
- The hand's offset for each direction comes from the `mCursor` keys of `UISize.json`.
- The pulse's timing is fixed in `0x00244500`; only the bar's colour comes from the caller.

## Related

- [Widgets](widgets.md) - the widget that owns `+0x5C` and `+0x90`, and the curves.
- [Screen layouts](screen-layouts.md) - the `mCursor` keys.
- [TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md) - the picture format and the atlas registry.
- [UI typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md) - the same sprite lookup from authored lists.
- [Battle menu](battle-menu.md) - the ON and OFF mark and the party slot hand.
- [Dialogs](dialogs.md) - the second confirm window.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00203170` is called by `0x003F1E90`; those functions are documented on [hud](hud.md).
- Gameplay: `0x00203170` is called by `0x00339630`; those functions are documented on
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md).
- Movement: `0x00203170` is called by `0x0022EF20`, `0x00230790`, `0x0026EB30`, `0x00334220`, `0x00334AB0`, `0x00334E00`,
  `0x00335B60`, `0x00336E40`, `0x00338490`, `0x00339F00`, `0x0033A3D0`, `0x0033BAA0`; `0x00203170` is also called by `0x0033C310`,
  `0x0033CBF0`, `0x0033CC80`, `0x0033D890`, `0x0033DB60`, `0x0033DFD0`, `0x003ED190`, `0x003ED3F0`.
- Movement: those functions are documented on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md).
- Movement: and on [bestiary](../Enemy-Spawning/bestiary.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [traps](../World-Areas-And-Travel/traps.md).
- Script VM: `0x00203170` is called by `0x00356160`.
