---
title: "Menu sprites: the shared picture atlases, how a sprite is found and drawn, the hand cursor, arrows and marks, and the pulsing selection bar"
kind: "system"
category: "Menus and HUD"
addresses: "002467A0, 00280750, 0024B0C0, 002D8BB0, 002DB080, 002426F0, 00242C90, 00244500, 002445A0, 002445C0"
---

## What the player sees

- A pointing hand marks the chosen row in the battle party list and the Gambits screen; it can also be drawn as an
  open hand.
- Scrolling lists and message windows show small up and down triangles, the battle menu shows left and right arrows,
  and message windows carry wing ornaments on both sides.
- The highlighted row of a list sits on a bar that fades out to the right and slowly dims and brightens.
- The Gambits row of the battle menu shows ON or OFF.

## How it works

### The atlases

`002467A0` (from `00253780`, `002538DE`) registers five atlas names with `0024A4E0` and requests kind 7 `D6`<sub>h</sub> through
`00249180`. Its completion `00246A10` binds entries 0 to 4 of `texpack_ys.bin` to them
([PS2 data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md)):

| Cell | Atlas | Entry |
|---|---|---:|
| `0208EAA8` | `buttonicon` | `0` |
| `0208EA98` | `bt_win_0_c` | `1` |
| `0208EAA0` | `cm_win_c` | `2` |
| `0208EA90` | `cursol_4_p` | `3` |
| `0208EAB8` | `keyboard` | `4` |

`00280750` (reached from `002808D0`) registers ten more at `[0209AC30] + 338h` to `+380`<sub>h</sub>, in this order:
`battle_4_c`, `targetline_p`, `s_font_c`, `battle_4_p`, `mini_face_c`, `partytop_4_c`, `partytop_8_c`, `party_grd_2`,
`icons_c` and `extra_c`, and requests kind 7 `D7`<sub>h</sub> (`00280861`). The getters `0035D460` and `0035D3D0` return
`battle_4_c` and `battle_4_p`; `0039BB00(n)` returns `cursol_4_p` for 1, `battle_4_c` for 2 and `buttonicon` otherwise
(`002441F0`).

### Finding a sprite

A sprite is named by its atlas, a set, a group within the set and a frame within the group. The records sit in the
`eXt` block of the atlas's picture ([TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md)). With `T` the
picture header plus `30`<sub>h</sub>:

```python
groups = T + 0x14 + u16[T + 0x14 + set x 2] x 2
record = T + u16[T + 0x10] + (u16[groups + group x 2] + frame) x 8
palette = u8[T + u16[T + 0x12] + (record byte 7 >> 4)] + (record byte 7 & 0xF)
```

`0024B0C0(atlas, set << 8 | group, frame)` returns the record. Every helper below repeats the same arithmetic with its
set and group fixed, and writes the palette byte to the widget's `+5C`<sub>h</sub>. For an 8-bit atlas the draw adds that byte
to the texture descriptor as the palette number (`002DB8C5`-`002DB8D3`).

### Drawing

`002D8BB0(widget, open)` brackets a group of draws: the first open sets the clip to the whole screen through `00249FD0(0)`, and
the last close sets it to the widget's clip box `+48`<sub>h</sub> when `+5C`<sub>h</sub> bit 17 is set. Three forwarders reach the sprite draw
`002DB080(widget, atlas, source, destination, record, 0, scale)`:

| Forwarder | Destination | Record |
|---|---|---|
| `002D8CB0(widget, atlas, source, x, y)` | the source's own size at `x`, `y` | the default `00917250` |
| `002D8C80(widget, atlas, source, box)` | `box`, stretched | the default |
| `002D8D10(widget, atlas, source, box, record, scale)` | `box` | the caller's |

The draw pass gives each widget a fresh `A0`<sub>h</sub>-byte draw record from `002D8C00` (`00245EA7`): clip on (`+5C`<sub>h</sub> bit 17),
alpha `80`<sub>h</sub> at `+5A`<sub>h</sub>, colour `80808080`<sub>h</sub> at `+90`<sub>h</sub> and `+94`<sub>h</sub>, and 1.0 at `+60`<sub>h</sub>, `+68`<sub>h</sub> and `+6C`<sub>h</sub>.

`002D8530` applies its clip box `+48`<sub>h</sub>, or none when bit 17 is clear, through `00249FD0`; `002DD2F0(record, box)` clips
to `box` moved by the record's `+50`<sub>h</sub>/`+52`<sub>h</sub> and cut to its clip box (`00249EE0`), or to an empty box when they do not
meet. For the sprite draw (`002DBD81`), `002DD910` maps the four corners of a quad from the menu's space, centred on 2048, onto the render target, using
the target's width and height (`00182EB0`, `00182E80`, 1920 and 1080 without a display) and the aspect `00182EE0`.

The record's first word flips the source left to right (bit 0, `002DB1B8`) and top to bottom (bit 1, `002DB1D0`); a
non-zero float at `+04`<sub>h</sub> rotates the sprite (`002DB22F`), about `+10`<sub>h</sub>/`+12`<sub>h</sub> when bit 2 is set and about the
centre otherwise; a pointer at `+08`<sub>h</sub> supplies four corner colours.

### The hand cursor

`002426F0(widget, x, y, kind)` draws the hand from `cursol_4_p` set 0 group 0: the pointing hand, or the next record,
an open hand, for kind 4 (`00242719`-`00242738`). The kind's row in `01E0C150` gives the offset from two layout keys and the flip
word for the record:

| Kind | Offset keys | Flip |
|---:|---|---:|
| `0` | `mCursorRightX`, `mCursorRightY` (`01E0C120`, `01E0C124`) | 0 |
| `1` | `mCursorDownX`, `mCursorDownY` | 0 |
| `2` | `mCursorLeftX`, `mCursorLeftY` | 1 |
| `3` | `mCursorUpX`, `mCursorUpY` | 3 |
| `4` | `mCursorOpenX`, `mCursorOpenY` (`01E0C140`, `01E0C144`) | 0 |

It is called by the battle party slot `0029A0A0` (`0029A1AF`), the Gambits screen `005691E0` (`00569775`), `00367940`
and `00367AA0`. The keys are in [Screen layouts](screen-layouts.md).

### Arrows, triangles and marks

Each of these helpers draws one group, the frame argument picking the record:

| Helper | Atlas, set, group | Pictures | Placed | Called by |
|---|---|---|---|---|
| `00242F30(w, x, y, frame)` | `cursol_4_p` 0, 2 | left and right arrows, outlined (frames 0, 1) and filled (2, 3) | centred | the battle menu panel `00276D30` |
| `00244070(w, x, y, frame)` | `cursol_4_p` 0, 6 | up (0) and down (1) triangles | centred | the scroll list `002D1750`, message windows `002A4430`, `002A86A0` |
| `00243F70(w, x, y, frame)` | `cursol_4_p` 0, 12 | an outlined down triangle, two frames | centred | the second confirm `00241D40`, `002A4430` |
| `00243030(w, x, y, open)` | `cursol_4_p` 0, 1 | a spinning disc, eight frames | centred | the menu list window `002CD170`, `002D1750` |
| `00243160(w, x, y)` | `cursol_4_p` 0, 9 | a round `!` mark | centred | `002CD170` |
| `00242A80(w, x, y, width, height)` | `cursol_4_p` 0, 8 | a rectangular frame in colour `65`<sub>h</sub> of `002DD7E0` | stretched to the box | `002CABF0` |
| `00242970(w, x, h, frame)` | `buttonicon` 0, 6 | wing ornaments, left (0) and right (1) | the left ends at `x`, the right starts at `x`, centred in height `h` | the message window `002A4170` |
| `00242870(w, x, y, frame)` | `battle_4_p` 0, 1 | bubbles: a smiley, a burst, a magnifier, a sign; returns the width | at `x`, `y` | `002A4170` |
| `00242600(w, x, y, unused, frame)` | `battle_4_c` 14, 2 | OFF (0) and ON (1) | left edge at `x`, centred on `y` | the battle menu's Gambits row `00276BE0`, `0027AD70` |

The disc turns through its eight frames, four frames each, during the first 32 of every 64 frames of the counter
`0208F570`, and rests on frame 0 for the other 32 (`00243042`-`00243068`). Its `open` argument set means the caller has
already opened the draw.

### The selection bar

`00242C90(widget, x, y, width, height, colour)` draws a list's highlighted row from `battle_4_c` set 3 group 1. It is
called by the scroll list `002D2DB0` (`002D378F`) and the member-list row `00284450` (`0028450C`), and draws nothing
while `002DD4B0` is 0.

1. The head is `max(width x 0.3, w0)` long, `w0` being the first record's width.
2. The first record is drawn at `x`, `w0` wide and `height` high (`002D9DB0`).
3. When the head is longer, the second record is stretched over the rest of it.
4. A colour quad covers the remaining width, with the alpha of its two right corners cleared, so the bar fades out to
   the right (`002DA2D0`).

The colour is the caller's, or `40507275`<sub>h</sub> when none is given; its alpha byte `+93`<sub>h</sub> goes through the pulse
`00244500` first.

### The pulse

`002445A0(on)` switches the pulse (`0208ED50`) and restarts it; `002445C0()` restarts it alone, from 33 call sites in menu code. Restarting stores the frame counter in `0208ED54`. With the pulse on, `00244500(a)` returns, for
`e` frames since the restart:

| Frames `e` | Alpha |
|---|---|
| 0 to 7 | `a` |
| 8 to 79 | `a/2 + a/2 x curve2(72, 80 - e)`, falling to half |
| 80 to 83 | `a/2` |
| 84 to 155 | `a/2 + a/2 x curve1(72, e - 84)`, rising to full |
| 156 | `a`, and the cycle restarts |

The curves are those of [Widgets](widgets.md). With the pulse off the alpha stays `a`. The Party Menu (`00281ED0`)
and its member lists (`00284EC0`, `00285B20`) switch it.

## Layouts

A sprite record, 8 bytes, in the record table of an atlas's `eXt` block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | x | left edge in the picture |
| `02`<sub>h</sub> | `u16` | y | top edge |
| `04`<sub>h</sub> | `u32` | size | bits 0-11 width, 12-23 height, 24-27 palette added, 28-31 palette group |

The draw record that `002D8D10` passes on:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | flags | bit 0 flip left to right, bit 1 flip top to bottom, bit 2 rotate about `+10`<sub>h</sub> |
| `04`<sub>h</sub> | `f32` | angle | 0 for no rotation |
| `08`<sub>h</sub> | `u8*` | corners | four RGBA corner colours, or null for the widget's colour `+90`<sub>h</sub> |
| `10`<sub>h</sub> | `i16[2]` | pivot | rotation centre when bit 2 is set |

## Shipped data

Measured in `us/packfiles/texpack_ys.bin`; the record count runs from the record table to the end of the picture
header.

| Entry | Atlas | Picture | Sprite records |
|---:|---|---|---:|
| `0` | `buttonicon` | 512 x 256, 8-bit | 40 |
| `1` | `bt_win_0_c` | 256 x 256, 8-bit | 42 |
| `2` | `cm_win_c` | 128 x 128, 8-bit | 10 |
| `3` | `cursol_4_p` | 512 x 256, 8-bit | 50 |
| `4` | `keyboard` | 1024 x 1024, 8-bit | 1,142 |

`cursol_4_p` has one set. Each of the five entries is byte-identical in at least eight of the ten
language folders.

## Modding notes

- The hand, arrows, triangles and marks are the records of `cursol_4_p`, entry 3 of `texpack_ys.bin`. The code adds a
  frame number to a group's first record, so a group must keep its records together and in order.
- The hand's offset for each direction comes from the `mCursor` keys of `UISize.json`.
- The pulse's timing is fixed in `00244500`; only the bar's colour comes from the caller.

## Related

- [Widgets](widgets.md) - the widget that owns `+5C`<sub>h</sub> and `+90`<sub>h</sub>, and the curves.
- [Screen layouts](screen-layouts.md) - the `mCursor` keys.
- [TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md) - the picture format and the atlas registry.
- [UI typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md) - the same sprite lookup from authored lists.
- [Battle menu](battle-menu.md) - the ON and OFF mark and the party slot hand.
- [Dialogs](dialogs.md) - the second confirm window.
