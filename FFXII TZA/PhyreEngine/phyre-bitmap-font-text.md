[Home](../../README.md) / [PhyreEngine](README.md) / Phyre bitmap-font text

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre bitmap-font text: how PBitmapFontText lays out a string from a bitmap font, builds its quads and draws it, and the debug-information overlay that uses it | system | PhyreEngine | Drawing and shaders | PhyreEngine's PText layer in the executable: the 0x270-byte PBitmapFontText object, its text buffer and ring-buffered vertex and index blocks, how a UTF-8 string becomes one quad per glyph with line feeds, kerning and a fallback for characters the font lacks, the text material with its texture, sampler and colour parameter, the draw, and the game's one user, the debug-information overlay built from PhyreText.fx.phyre and tuffysdf.fgen.phyre. | 0x0067B180, 0x0067B3A0, 0x0067B530, 0x0067B4C0, 0x0067BF70, 0x0067C4F0, 0x0067C5A0, 0x0067C310, 0x0067C260, 0x0067C440, 0x0067BB30, 0x0067BD50, 0x0067BE10, 0x0067BEC0, 0x0059A600, 0x001EA3C0, 0x001EA830, 0x001EAE10, 0x01DFDE00 |

## What the player sees

PhyreEngine's bitmap-font text has one user in the executable: the debug-information overlay, a
block of white text with a black copy behind it that starts with `Debug Info:`. Menus, dialogue and
battle messages are drawn by the game's own text code. The overlay draws only while its enable byte
is set.

The overlay joins two files: `tuffysdf.fgen.phyre` holds the font, a picture of the characters with a table giving
each one's place and size in it, and `PhyreText.fx.phyre` holds the shader that draws it. For each character of the
string the game takes its table entry and draws one small rectangle cut from the font picture.

## How it works

### The objects

A text is a `0x270`-byte object built by `0x0067B180(text, material)`; the constructor's unwind path
`0x0067B470` releases the index block (`+0xC0`), `+0xB0` and the array at `+0x88` again. It holds:

- the string, as a byte array at `+0x240` (count) and `+0x248` (pointer) with room for one
  terminator more than its capacity;
- two vertex data blocks reached through `+0xB8` (positions at `+0x00`, texture coordinates at
  `+0x88`), each 8 bytes (two floats) per vertex and four vertices per glyph;
- an index data block at `+0xC0`, 16-bit, six indices per glyph;
- the material object at `+0x238` and layout values at `+0x258`–`+0x268`, with the line scale `+0x260`
  starting at 0.65.

`0x0067B180` zeroes the count dword and the pointer 8 bytes after it in each 16 bytes of `+0x00` to `+0x7F`, and
sets up a record at `+0x80`: `+0x80`, `+0x88`, `+0x90`, `+0xA8`, `+0xB0` and `+0xB8` zero, `+0x84` and `+0x9C`
to `+0xA7` set to `0xFFFFFFFF`, `+0x98` to 2 (`0x0067B1E7`-`0x0067B213`, `0x0067B2CF`).

After handing the first pair's old null pointer to `0x001B7170` (`0x0067B2C0`), the constructor makes that record
the one entry of the array `+0x00`/`+0x08`, not owned (count `0x80000001`, `0x0067B2C9`). It builds the index
block at `+0xC0` (`0x00662A80`) and the mesh instance at `+0x140` (`0x001B6CE0`), stores the material at
`+0x238` and 0.65 at `+0x260` (`0x0067B295`), and zeroes `+0x240`, `+0x248` to `+0x25C`, `+0x264` and `+0x268`.

The 12 floats at `+0x208` to `+0x234` are zero except 1.0 at `+0x20C`, `+0x214` and `+0x220`
(`0x0067B238`-`0x0067B26F`), and the mesh instance's `+0x148` points at them (`0x0067B378`). The constructor
allocates `0x110` bytes (`0x0017D260(0x110, 8)`, `0x0067B2EC`), builds two `0x88`-byte vertex blocks in them
(`0x006629F0`) and hands them to the array `+0xB0` with count 2 (`0x001B8100`, `0x0067B347`); a null allocation
leaves that array empty (`0x0067B2FF`). The test at `0x0067B2D9` skips this only when `+0xB0` is already 2, and
the constructor has just zeroed it (`0x0067B210`).

It then runs `0x0060DF70(+0x140, text)` (`0x0067B356`) and stores `material + 8`, the material object's buffer
array, at `+0x160` (`0x0067B371`; `0x0067B36D` takes `[+0x140] + 0x60` instead only when that sum is zero), and
returns the text.

`0x0067B3A0` first runs `0x00673860(text)` (`0x0067B3B7`) and calls slot `+0x10` of the object at `+0x250` when it is
set (`0x0067B3CC`). It frees the string bytes `+0x248` with `0x00584730` when bit `0x80000000` of `+0x240` is clear
and the pointer is set (`0x0067B3EB`), then zeroes both. It passes the mesh instance `+0x140` to `0x005DD890`, the
index block `+0xC0` to `0x00663170` and the array `+0xB0` to `0x001B6EF0`. It frees `+0x90` the same way under bit
`0x80000000` of `+0x88` (`0x0067B442`), zeroes `+0x88` and `+0x90`, and ends in `0x006467E0(text)` (`0x0067B462`).

The material object (`0x58` bytes) keeps the bitmap font at `+0x40`. `0x0067BD50(material, cluster,
mode)` finds the first `PMaterial` (descriptor `0x02CB6B80`) among the cluster's instance lists: the first
list on the cluster's chain `+0x38` whose class, or a parent along `+0x78`, is that descriptor and whose
count `+0x74` is above 0. It returns 7 when there is no such list (`0x0067BE03`).

It passes the list's first object, `[list + 0x60] + [class + 0xF8]`, to `0x0067BB30` with the same cluster
and mode (`0x0067BDFE`), first stepping the storage `[list + 0x60]` on by the instance size `[class + 0x38]`
while it equals the link chain at `[list + 0x10]` (`0x0067BDDC`-`0x0067BDEA`). `0x0067BB30` sets the object up
and returns 0 (`0x0067BD15`, `0x0067BD2C`), or the first non-zero result named below:

1. it stores `0x006CCCE0(mode)` at `+0x48` (7 when that is null) and, unless bit `0x80` of `+0x34` is set,
   presets the five bytes at `+0x18` to 5, 1, 2, 2, 2 before passing them to `0x0061D9C0`, whose non-zero
   result it returns (`0x0067BBC8`);
2. it stores the cluster at `+0x50` (`0x0067BBE0`), creates a parameter buffer for the found material's
   effect variant (`0x00600120` on the material's `+0x00` and the cluster, `0xE` on failure) and stores it at
   `+0x00`;
3. it copies the material's parameter buffer `+0x08` into that buffer's data, as many bytes as the
   source's first dword gives (`memcpy`, `0x0067BC08`);
4. it binds the font's texture (`+0x30` of the font) to the parameter `BitmapFontTexture` and the
   object at `+0x18` to `LinearClampSampler`, sets the colour to white, and stores the new buffer
   as the only entry of the array at `+0x08`;
5. the texture goes through `0x001B81B0` in a record of `0x42`, the `+0x18` object and the texture
   (`0x0067BC49`), the sampler through `0x00194540` (`0x0067BC73`) and the colour through
   `0x0067C440(object, {1, 1, 1})` (`0x0067BCA0`), each non-zero result returned; a parameter the effect lacks
   is skipped (`0x0067BC3C`, `0x0067BC68`);
6. the array entry sits inline at `+0x10` with count 1 (`0x0067BCF6`, `0x0067BD29`); an older owned pointer in
   that array is freed with `0x00584730` first (`0x0067BCF1`).

### Setting the text

`0x0067C4F0(text, string)` returns 1 for a null string. When the buffer is missing or too short it
grows it through `0x0067BF70`; otherwise it returns at once when the buffer already holds the same
string. It then copies the string in and rebuilds the geometry (`0x0067B530`).

Too short means `len > size - 1`, the size being `+0x240` without bit `0x80000000` (`0x0067C539`-`0x0067C547`).
The same string is a `strncmp` of `len + 1` bytes and returns 0 (`0x0067C54C`, `0x0067C55B`). A non-zero result
of `0x0067BF70` is returned (`0x0067C56B`); otherwise `memcpy` copies `len + 1` bytes (`0x0067C57A`) and the result
of `0x0067B530(text, len)` is returned (`0x0067C584`).

`0x0067BF70(text, n)` sizes everything for `n` glyphs: the string buffer to `n + 1` bytes (keeping
the old text, zeroing the rest), both vertex blocks to `4n` vertices and the index block to `6n`
indices with maximum index `4n − 1`. It fills the index block once, two triangles per glyph as
`v, v+1, v+2, v, v+2, v+3`, through `0x0067BEC0` and the index map `0x00671D80`, and commits it
(`0x006747D0`). `0x0067C5A0` calls it and then rebuilds for the current
string.

`0x0067C5A0` returns a non-zero result of `0x0067BF70` without the rebuild (`0x0067C5B0`); otherwise it measures
the string at `+0x248` and ends in `0x0067B530(text, length)` (`0x0067C5D3`), whose result it returns.

`0x0067C310(text, n)` sets the number of buffers in each of the three blocks to `2n` (at least 1) and
logs `Altering buffer count of PDataBlock whilst bound.  Rebind needed.` (or the `PIndexDataBlock`
form) when a block is bound at the time.

The blocks are `[+0xB8]`, `[+0xB8] + 0x88` and the index block `+0xC0`; bound is bit `0x1` of a vertex
block's `+0x74` (`0x00671B10`) or of the index block's `+0x6C` (`0x00671B20`). A block that already has that
count is left alone (`0x0067C359`, `0x0067C3A1`, `0x0067C3E4`). A resize (`0x00672B80`, `0x00672C70` for the index
block) that returns non-zero ends the function with that result (`0x0067C385`); a successful one sets the
block's current buffer to 0 (`0x0067C38B`, `0x0067C3CE`, `0x0067C411`). It returns 0 otherwise (`0x0067C414`).

`0x0067BE10(block, arg)` binds a vertex block that is not bound yet (`0x0066F970`, whose non-zero result it
returns, `0x0067BE33`). It takes the buffer after the current one `+0x18`, wrapping to 0 at the count `+0x20`
(`0x0067BE46`-`0x0067BE52`), calls `Sleep(1)` (`0x0067BE85`) while the dword `+0x20` of that buffer's `0x48`-byte
entry is above 0, maps it with `0x00671B30(block, index, arg)` (`0x0067BE99`) and on success sets byte `+0x1C`
to 2 (`0x0067BEAC`); it returns the map's result.

`0x0067BEC0` does the same for the index block with its bound bit (`0x0066FAB0`), the current buffer `+0x10`,
the count `+0x18`, the map `0x00671D80` (`0x0067BF49`) and byte `+0x0E` (`0x0067BF5C`).

### Building the quads

`0x0067B530(text, length)` is `PBitmapFontText::createMeshGeometry`. It takes the next free buffer of
each vertex block (`0x0067BE10`, which sleeps 1 ms at a time while that buffer is still in use) and
decodes the string as UTF-8 (`0x0059A600`). For each character it searches the font's character table
(`0x30`-byte `PBitmapFontCharInfo` records, `+0x10` count and `+0x18` pointer of the font) for a
matching `m_characterCode`, clearing a scratch record first (`0x0067CBD0`):

- A line feed starts a new line: the pen's x goes back to 0 and its y drops by the line scale times
  the font's `m_lineSpacing`.
- A code with no record logs `PBitmapFontText::createMeshGeometry: Warning - skipping unrenderable
  character with code '%d'` and moves the pen's x on by half the scaled line spacing.
- Any other character writes four positions from the pen, the record's offsets and its
  `m_width` and `m_height`, and four texture coordinates from its texel position divided by the
  texture's size, swapped for a record with `m_rotated` set. The pen then advances by the record's
  advance values and by the kerning to the next character.

Kerning comes from `0x0067B4C0`: the record's `m_kernPairs` entries starting at `m_kernOffset` in the
font's kerning table are triples of 32-bit integers; the first whose first value is the next
character's code gives its second value divided by 64. At the end the index count becomes six per
glyph drawn and both vertex buffers are committed.

The kerning table is the pointer at `+0x28` of the font (`0x0067B4E6`), reached through the material object
`+0x238` and its font `+0x40`; the division is `n * 0.015625` with the float at `0x00D22698` (`0x0067B520`). An
`m_kernPairs` of 0 or below, or no matching triple, gives 0.0 (`0x0067B4CC`, `0x0067B50A`).

`0x0059A600(&p)` reads the lead byte at `p`. From `0xC0` up it takes the number `n` of following bytes from
it (1 for `0xC0`-`0xDF`, 2 for `0xE0`-`0xEF`, 3 for `0xF0`-`0xF7`, 4 for `0xF8`-`0xFB`, 5 for `0xFC`-`0xFF`)
and keeps its low `6 - n` bits (`0x0059A60D`-`0x0059A655`). It then takes six bits from each following byte,
`code = code * 64 + (byte & 0x3F)`, without checking them, and leaves `p` after the last byte read
(`0x0059A676`-`0x0059A6E0`). A lead byte below `0xC0` is returned as the code (`0x0059A6E4`).

### Colour and drawing

`0x0067C440(material, rgb)` writes `(r, g, b, 1.0)` into the material's `textColor` parameter; it
returns 9 when the material has no such parameter and 3 when the parameter lies outside the buffer.

The parameter buffer is the material object's `+0x00`, and 9 also comes back when that is null
(`0x0067C47A`). The parameter is found by name (`0x0018D240`, `0x0067C486`); its offset is the word `+0x10` and its
size the word `+0x12` under mask `0x1FFF`. The 3 comes back when `offset + size` exceeds the data's first
dword or `offset < 4` (`0x0067C4AF`, `0x0067C4C0`). Otherwise `memcpy` copies `size` bytes of the colour to the
data at `offset` (`0x0067C4D1`) and 0 is returned.

`0x0067C260(text, renderer)` keeps the renderer at `+0x250` and draws the text's mesh instance at
`+0x140` through `0x0060B980`, with a `PMaterialSelectorMaterialSet` holding `+0x160`. A text whose
buffer exists but starts with
a zero byte is not drawn; the first such call logs `Attempting to render text but no text string has
not been set. Did you forget to call PBitmapFontText::setText()?` (byte `0x02E3F804`).

That skip returns 0 (`0x0067C2AC`); a buffer size `+0x240` of 0, bit `0x80000000` aside, skips the check
(`0x0067C27D`). The draw copies the material object's `+0x48` to the renderer's `+0x80` (`0x0067C2C2`) and passes
`0x0060B980` the renderer, the mesh instance, the selector (vtable `0x008C6C98`), 0, the renderer's dword `+0x220`
and a zero byte (`0x0067C300`); it returns that call's result.

### The debug-information overlay

The game's overlay object builds its text in `0x001EA3C0`:

1. it loads the two clusters named at `0x01DFDE00`, `PhyreText.fx.phyre` and `tuffysdf.fgen.phyre`;
2. it finds the first `PBitmapFont` (descriptor `0x02E3FA60`) in the font cluster (`0x13` when there is
   no such font), builds the material object around it and sets it up from the shader cluster with mode 3;
3. it copies its `softEdges` value into that material's parameters and creates the text
   (`0x0067B180`), with the string `Debug Info:`, 128 for `0x0067C310` and a capacity for `0x0067C5A0`.

Its draw, `0x001EA830`, runs only while its byte `+0xEA` is set and its text `+0x20` exists (`0x001EA83F`, `0x001EA856`): it
sets the current string (`0x0067C4F0`, the pointer at `+0x48`, or a null pointer while the dword `+0x50` is 0), posts
the render queue's block (`0x00185A50`), and writes the `+0x58` transform's position `+0x88` to `+0x90` plus the offset
`+0x100` to `+0x108` into `+0xC8` to `+0xD0`, the position of the transform at `+0x98` (`0x001EA8E1`).

It colours the text black (`0x0067C440` on the material `+0x18`) and draws it with the transform at `+0x98`, then white
with the one at `+0x58`, so the white text has a black shadow. `0x001EAC60` hands each transform to the text's `+0x208`
to `+0x234`: rows 1 to 3's first three values, with row 0's x, y and z as each row's fourth value.

The draw returns 0 when it has drawn both, and 0 when the byte or the text is missing (`0x001EA979`). A non-zero
result of a call it checks (`0x005FEFD0`, `0x0067C4F0`, either `0x0067C260` draw, `0x00600A60`) ends it at once and is
returned, so with `+0x50` at 0 (`0x0067C4F0` returns 1 for the null string) nothing is drawn. With its third
argument set it also opens the context's bit `0x1` bracket first (`0x005FEFD0(context, 0)`, `0x001EA86B`) and closes
it after the white draw (`0x00600A60(context, 3)`, `0x001EA970`); the overlay's three calls (`0x001C2DB0`) give it 0.

`0x001EAE10` destroys the text (`0x0067B3A0`) and the material object and
passes both clusters to `0x0019CC50`. The material `+0x18` goes through `0x001EA050` and the text `+0x20` through
`0x0067B3A0`; each, when present, is then freed with `0x00584730` and its pointer set to 0 (`0x001EAE42`,
`0x001EAE65`). The clusters are the pointers at `+0x00` and `+0x08`, each passed with the loaded-asset registry
`0x0019CE20()`.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PBitmapFont` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | m_isSDF | m_isSDF (u8), registered by `0x0067CFE0` (`0x00632960` at `0x0067D0E1`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFont |
| `+0x01` | `u8[3]` | pad01 | alignment bytes after m_isSDF (u8 at `+0x00`) up to m_fontSize (u32 at `+0x04`); no registered member covers it (`0x0067CA70` registers the `0x38`-byte class at `0x0067CAC0`) |
| `+0x04` | `u32` | m_fontSize | m_fontSize (u32), registered by `0x0067CFE0` (`0x00632960` at `0x0067D072`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFont |
| `+0x08` | `f32` | m_lineSpacing | the font's line spacing: a line feed drops the pen's y by the line scale times it (`0x0067B530` reads it at `0x0067B75B`); m_lineSpacing (f32), registered by `0x0067CFE0` (`0x00632960` at `0x0067D154`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFont |
| `+0x0C` | `f32` | m_baselineOffset | m_baselineOffset (f32), registered by `0x0067CFE0` (`0x00632960` at `0x0067D1C7`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFont |

`PBitmapFontCharInfo` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | m_characterCode | the character code the text builder `0x0067B530` searches the table for (`0x0067B739`); m_characterCode (i32), registered by `0x0067D3B0` (`0x00632960` at `0x0067D43E`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo; the placement constructor `0x0067C660` clears `+0x00` to `+0x07` (`0x0067C667`) |
| `+0x04` | `i32` | m_kernPairs | number of kerning triples: the kerning lookup `0x0067B4C0` reads it (`0x0067B4C5`); m_kernPairs (i32), registered by `0x0067D3B0` (`0x00632960` at `0x0067D4B1`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo; cleared by the placement constructor `0x0067C660` (`0x0067C667`) |
| `+0x08` | `i32` | m_kernOffset | first triple, in 32-bit units: the kerning lookup `0x0067B4C0` reads it (`0x0067B4DA`); m_kernOffset (i32), registered by `0x0067D3B0` (`0x00632960` at `0x0067D524`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo; cleared by the placement constructor `0x0067C660` (`0x0067C66A`) |
| `+0x0C` | `f32[2]` | m_uv | m_uv (f32[2], a fixed-size array), registered by `0x0067D3B0` (`0x00632A70` at `0x0067D592`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo |
| `+0x14` | `f32` | m_width | the glyph's width in the quad `0x0067B530` builds (`0x0067B7DA`); m_width (f32), registered by `0x0067D3B0` (`0x00632960` at `0x0067D60C`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo; cleared by the placement constructor `0x0067C660` (`0x0067C66E`) |
| `+0x18` | `f32` | m_height | the glyph's height in the quad `0x0067B530` builds (`0x0067B7C3`); m_height (f32), registered by `0x0067D3B0` (`0x00632960` at `0x0067D67F`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo; cleared by the placement constructor `0x0067C660` (`0x0067C66E`) |
| `+0x1C` | `f32[2]` | m_offset | m_offset (f32[2], a fixed-size array), registered by `0x0067D3B0` (`0x00632A70` at `0x0067D6ED`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo |
| `+0x24` | `f32[2]` | m_advance | m_advance (f32[2], a fixed-size array), registered by `0x0067D3B0` (`0x00632A70` at `0x0067D762`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo |
| `+0x2C` | `u8` | m_rotated | when set, `0x0067B530` swaps the glyph's texture coordinates (`0x0067B818`); m_rotated (u8), registered by `0x0067D3B0` (`0x00632960` at `0x0067D7DC`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PBitmapFontCharInfo; cleared by the placement constructor `0x0067C660` (`0x0067C672`) |
| `+0x2D` | `u8[3]` | pad2D | the bytes after m_rotated (u8 at `+0x2C`) up to the end of the `0x30`-byte record; no registered member covers it (`0x0067CB20` registers the `0x30`-byte class at `0x0067CB70`) |

### Text objects and character records

The structures below are the ones the mechanisms above use.

PBitmapFontText (`0x270`), fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0B8` | `void*` |  | vertex blocks: positions at `+0x00`, texture coordinates at `+0x88` |
| `+0x0C0` | `PIndexDataBlock` |  | index data block (min index `+0x00`, max index `+0x04`, count `+0x08`, type `+0x0C` = `0x0C`) |
| `+0x238` | `void*` |  | material object |
| `+0x240` | `u32` |  | string buffer size (bit `0x80000000`: not owned) |
| `+0x248` | `void*` |  | string bytes |
| `+0x250` | `void*` |  | renderer of the last draw |
| `+0x258` | `f32` |  | widest line |
| `+0x25C` | `f32` |  | total height |
| `+0x260` | `f32` |  | line scale, 0.65 at construction |
| `+0x264` | `f32` |  | highest glyph top |
| `+0x268` | `f32` |  | lowest glyph bottom |

PBitmapFontCharInfo (`0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | m_characterCode |  |
| `+0x04` | `i32` | m_kernPairs | number of kerning triples |
| `+0x08` | `i32` | m_kernOffset | first triple, in 32-bit units |
| `+0x0C` | `f32` |  | texel x |
| `+0x10` | `f32` |  | texel y |
| `+0x14` | `f32` | m_width |  |
| `+0x18` | `f32` | m_height |  |
| `+0x1C` | `f32` |  | x offset |
| `+0x20` | `f32` |  | y offset |
| `+0x24` | `f32` |  | x advance |
| `+0x28` | `f32` |  | y advance |
| `+0x2C` | `bool` | m_rotated |  |

## Shipped data

| Fact | Value |
|---|---|
| `gamedata/d3d11/artdata/shaders/phyretext.fx.phyre` | 44,634 bytes |
| `gamedata/d3d11/artdata/font/tuffysdf.fgen.phyre` | 269,961 bytes |
| `gamedata/d3d11/artdata/font/tuffy.fgen.phyre` | 269,961 bytes; no string in the executable and no other shipped file names it, so the game never loads it |

## Modding notes

- Only characters present in the font's table are drawn; anything else is skipped with a log line
  and half a line of space, so a replacement font must cover every code the text uses.
- The text is decoded as UTF-8, so a multi-byte character is looked up by its code point.
- Each rebuild writes the next buffer of a ring of `2n` buffers (256 for the overlay);
  `0x0067BE10` waits only when that buffer is still in use.

## Related

- [Phyre modules](phyre-modules.md): the `PText` module and its registration.
- [Phyre field schema](phyre-field-schema.md): the `PBitmapFont` and `PBitmapFontCharInfo` members.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 2 calls with 1 other topic</summary>

**Menus and HUD** (explained on [graphics settings](../Engine-Core/graphics-settings.md))

| Function | | Functions |
|---|---|---|
| `0x005FEFD0` | is called by | `0x0018EEE0` |
| `0x00600A60` | is called by | `0x0018EEE0` |

</details>
