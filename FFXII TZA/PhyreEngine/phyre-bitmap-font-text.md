---
title: "Phyre bitmap-font text: how PBitmapFontText lays out a string from a bitmap font, builds its quads and draws it, and the debug-information overlay that uses it"
kind: "system"
category: "PhyreEngine"
addresses: "0067B180, 0067B3A0, 0067B530, 0067B4C0, 0067BF70, 0067C4F0, 0067C5A0, 0067C310, 0067C260, 0067C440, 0067BB30, 0067BD50, 0067BE10, 0067BEC0, 0059A600, 001EA3C0, 001EA830, 001EAE10, 01DFDE00"
---

## What the player sees

PhyreEngine's bitmap-font text has one user in the executable: the debug-information overlay, a
block of white text with a black copy behind it that starts with `Debug Info:`. Menus, dialogue and
battle messages are drawn by the game's own text code. The overlay draws only while its enable byte
is set.

## How it works

### The objects

A text is a `270`<sub>h</sub>-byte object built by `0067B180(text, material)`; the constructor's unwind path
`0067B470` releases the index block (`+C0`<sub>h</sub>), `+B0`<sub>h</sub> and the array at `+88`<sub>h</sub> again. It holds:

- the string, as a byte array at `+240`<sub>h</sub> (count) and `+248`<sub>h</sub> (pointer) with room for one
  terminator more than its capacity;
- two vertex data blocks reached through `+B8`<sub>h</sub> (positions at `+00`<sub>h</sub>, texture coordinates at
  `+88`<sub>h</sub>), each 8 bytes (two floats) per vertex and four vertices per glyph;
- an index data block at `+C0`<sub>h</sub>, 16-bit, six indices per glyph;
- the material object at `+238`<sub>h</sub> and layout values at `+258`<sub>h</sub>–`+268`<sub>h</sub>, with the line scale `+260`<sub>h</sub>
  starting at 0.65.

The material object (`58`<sub>h</sub> bytes) keeps the bitmap font at `+40`<sub>h</sub>. `0067BD50(material, cluster,
mode)` finds the first `PMaterial` (descriptor `02CB6B80`) among the cluster's instance lists and
passes it to `0067BB30`, which sets the object up:

1. it stores `006CCCE0(mode)` at `+48`<sub>h</sub> (7 when that is null) and, unless bit 7 of `+34`<sub>h</sub> is set,
   presets the five bytes at `+18`<sub>h</sub> to 5, 1, 2, 2, 2 before passing them to `0061D9C0`;
2. it creates a parameter buffer for the found material's effect variant (`00600120`, `E`<sub>h</sub> on
   failure) and copies the material's parameter buffer into it;
3. it binds the font's texture (`+30`<sub>h</sub> of the font) to the parameter `BitmapFontTexture` and the
   object at `+18`<sub>h</sub> to `LinearClampSampler`, sets the colour to white, and stores the new buffer
   as the only entry of the array at `+08`<sub>h</sub>.

### Setting the text

`0067C4F0(text, string)` returns 1 for a null string. When the buffer is missing or too short it
grows it through `0067BF70`; otherwise it returns at once when the buffer already holds the same
string. It then copies the string in and rebuilds the geometry (`0067B530`).

`0067BF70(text, n)` sizes everything for `n` glyphs: the string buffer to `n + 1` bytes (keeping
the old text, zeroing the rest), both vertex blocks to `4n` vertices and the index block to `6n`
indices with maximum index `4n − 1`. It fills the index block once, two triangles per glyph as
`v, v+1, v+2, v, v+2, v+3`, through `0067BEC0` and the index map `00671D80`, and commits it (`006747D0`). `0067C5A0` calls it and then rebuilds for the current
string.

`0067C310(text, n)` sets the number of buffers in each of the three blocks to `2n` (at least 1) and
logs `Altering buffer count of PDataBlock whilst bound.  Rebind needed.` (or the `PIndexDataBlock`
form) when a block is bound at the time.

### Building the quads

`0067B530(text, length)` is `PBitmapFontText::createMeshGeometry`. It takes the next free buffer of
each vertex block (`0067BE10`, which sleeps 1 ms at a time while that buffer is still in use) and
decodes the string as UTF-8 (`0059A600`). For each character it searches the font's character table
(`30`<sub>h</sub>-byte `PBitmapFontCharInfo` records, `+10`<sub>h</sub> count and `+18`<sub>h</sub> pointer of the font) for a
matching `m_characterCode`, clearing a scratch record first (`0067CBD0`):

- A line feed starts a new line: the pen's x goes back to 0 and its y drops by the line scale times
  the font's `m_lineSpacing`.
- A code with no record logs `PBitmapFontText::createMeshGeometry: Warning - skipping unrenderable
  character with code '%d'` and moves the pen's x on by half the scaled line spacing.
- Any other character writes four positions from the pen, the record's offsets and its
  `m_width` and `m_height`, and four texture coordinates from its texel position divided by the
  texture's size, swapped for a record with `m_rotated` set. The pen then advances by the record's
  advance values and by the kerning to the next character.

Kerning comes from `0067B4C0`: the record's `m_kernPairs` entries starting at `m_kernOffset` in the
font's kerning table are triples of 32-bit integers; the first whose first value is the next
character's code gives its second value divided by 64. At the end the index count becomes six per
glyph drawn and both vertex buffers are committed.

### Colour and drawing

`0067C440(material, rgb)` writes `(r, g, b, 1.0)` into the material's `textColor` parameter; it
returns 9 when the material has no such parameter and 3 when the parameter lies outside the buffer.

`0067C260(text, renderer)` keeps the renderer at `+250`<sub>h</sub> and draws the text's mesh instance at
`+140`<sub>h</sub> through `0060B980`, with a `PMaterialSelectorMaterialSet` holding `+160`<sub>h</sub>. A text whose buffer exists but starts with
a zero byte is not drawn; the first such call logs `Attempting to render text but no text string has
not been set. Did you forget to call PBitmapFontText::setText()?` (byte `02E3F804`).

### The debug-information overlay

The game's overlay object builds its text in `001EA3C0`:

1. it loads the two clusters named at `01DFDE00`, `PhyreText.fx.phyre` and `tuffysdf.fgen.phyre`;
2. it finds the first `PBitmapFont` (descriptor `02E3FA60`) in the font cluster (`13`<sub>h</sub> when there is
   none), builds the material object around it and sets it up from the shader cluster with mode 3;
3. it copies its `softEdges` value into that material's parameters and creates the text
   (`0067B180`), with the string `Debug Info:`, 128 for `0067C310` and a capacity for `0067C5A0`.

Its draw, `001EA830`, runs only while its byte `+EA`<sub>h</sub> is set: it sets the current string, colours
the text black and draws it with the transform at `+98`<sub>h</sub>, then white with the one at `+58`<sub>h</sub>, so the
white text has a black shadow. `001EAE10` destroys the text (`0067B3A0`) and the material object and
passes both clusters to `0019CC50`.

## Layouts

PBitmapFontText (`270`<sub>h</sub>), fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0B8`<sub>h</sub> | `void*` | vertex blocks: positions at `+00`<sub>h</sub>, texture coordinates at `+88`<sub>h</sub> |  |
| `0C0`<sub>h</sub> | `PIndexDataBlock` | index data block (min index `+00`<sub>h</sub>, max index `+04`<sub>h</sub>, count `+08`<sub>h</sub>, type `+0C`<sub>h</sub> = `0C`<sub>h</sub>) |  |
| `238`<sub>h</sub> | `void*` | material object |  |
| `240`<sub>h</sub> | `u32` | string buffer size (bit 31: not owned) |  |
| `248`<sub>h</sub> | `void*` | string bytes |  |
| `250`<sub>h</sub> | `void*` | renderer of the last draw |  |
| `258`<sub>h</sub> | `f32` | widest line |  |
| `25C`<sub>h</sub> | `f32` | total height |  |
| `260`<sub>h</sub> | `f32` | line scale, 0.65 at construction |  |
| `264`<sub>h</sub> | `f32` | highest glyph top |  |
| `268`<sub>h</sub> | `f32` | lowest glyph bottom |  |

PBitmapFontCharInfo (`30`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | m_characterCode |  |
| `04`<sub>h</sub> | `i32` | m_kernPairs | number of kerning triples |
| `08`<sub>h</sub> | `i32` | m_kernOffset | first triple, in 32-bit units |
| `0C`<sub>h</sub> | `f32` | texel x |  |
| `10`<sub>h</sub> | `f32` | texel y |  |
| `14`<sub>h</sub> | `f32` | m_width |  |
| `18`<sub>h</sub> | `f32` | m_height |  |
| `1C`<sub>h</sub> | `f32` | x offset |  |
| `20`<sub>h</sub> | `f32` | y offset |  |
| `24`<sub>h</sub> | `f32` | x advance |  |
| `28`<sub>h</sub> | `f32` | y advance |  |
| `2C`<sub>h</sub> | `bool` | m_rotated |  |

## Shipped data

| Fact | Value |
|---|---|
| `gamedata/d3d11/artdata/shaders/phyretext.fx.phyre` | 44,634 bytes |
| `gamedata/d3d11/artdata/font/tuffysdf.fgen.phyre` | 269,961 bytes |
| `gamedata/d3d11/artdata/font/tuffy.fgen.phyre` | 269,961 bytes, not named by the overlay |

## Modding notes

- Only characters present in the font's table are drawn; anything else is skipped with a log line
  and half a line of space, so a replacement font must cover every code the text uses.
- The text is decoded as UTF-8, so a multi-byte character is looked up by its code point.
- Each rebuild writes the next buffer of a ring of `2n` buffers (256 for the overlay);
  `0067BE10` waits only when that buffer is still in use.

## Related

- [Phyre modules](phyre-modules.md): the `PText` module and its registration.
- [Phyre field schema](phyre-field-schema.md): the `PBitmapFont` and `PBitmapFontCharInfo` members.
