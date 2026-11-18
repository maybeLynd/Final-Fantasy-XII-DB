[Home](../../README.md) / [Game files and data tables](README.md) / Location-map colour tables (.cl2)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Location-map colour tables (.cl2): the CLT2 palettes some location maps draw with | format | Game files and data tables | Image files | The loca_*.cl2 files: a one-picture TIM2-shaped container holding only a palette, how the map-data widget's pane loader picks one per map entry from menumap_common.bin, how the reader hands its palette and colour count to every picture of the entry's menumap_sub file, how the upload turns it into an RGBA8 texture with PS2 alpha rescaled, the 20 shipped files, and the rules an edited table must keep. | 0x003C1F00, 0x003C26C0, 0x003C2190, 0x02B457E0, 0x0024A9E0, 0x0024A480, 0x0024A1D0, 0x00181000, 0x00180E70, 0x0017F3B0, 0x008C5B34, 0x02CF7480, 0x00163D00, 0x003BC2D0 |

## What the player sees

The colours of the pictures on a location map. No location-map picture uses its own palette: every map takes the
third colour table of `clutpack_ys.bin`, except the Great Crystal and Sky Fortress Bahamut maps, whose two map
entries name a `.cl2` and take that file's table instead, so the same pixel data can be recoloured without being
reshipped.

## Where it comes from

The files are resource kind 7: `ps2data/image/ff12/myoshiok/<locale>/bin_menu/loca_<name>.cl2`. In the US kind-7
path array¹ id `0xE2` is `Loca_gil.cl2`, `0xE3` `Loca_bhm.cl2` and `0xE4` `Loca_rbl.cl2`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01EC73A0` |

</details>

The map-data widget `0x02B457E0` loads `menumap_common.bin` (kind 7 `0xA4`) into its `+0xE8`¹. The pane
loader `0x003C1F00(widget, owner, descriptor, n)`, reached through `0x003C2190` from `0x002B7B80`, `0x002BAF80` and
`0x003CB4F0`, takes a free pane (two, `0xA8` bytes apart from `+0x120`), requests `menumap_sub<n>.bin` (kind 7
`0x142 + n`) through `0x00249180`, and then picks the colour table:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BC2D0` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It releases the table already at widget `+0x118` and clears the pointer. | `0x003697F0` |
| 2 | It finds the entry table in `menumap_common.bin` (the u16 at file `+8` is its offset: a u32 count, then 8-byte entries) and, when `n` is below the count and byte `+1` of entry `n` is not 0, requests kind 7 id `0xE1 + byte` through `0x00249210` into heap 3, keeping the buffer at `+0x118`. | `0x003C2068`-`0x003C208D` |

The pane loader returns 0 and requests nothing when both panes are in use, or when one is in use and
exactly one of the first 50 entries of `menumap_common.bin` has entry `n`'s group byte (an index at or past
the count reads as group 0; `0x003C1F4D`, `0x003C1FC6`-`0x003C1FD3`). Otherwise it stores `n` at pane `+0x10` and
the descriptor's byte `+0x10` at pane `+0x12`, passes the descriptor's dword `+0` to `0x00249180`¹, and returns 1².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003C1FFD` |
| ² | `0x003C20A4` |

</details>

All three callers build a descriptor with 2 in its dword `+0` and 2 at `+0x10`¹, so every pane passes 2 to `0x00249180` and stores 2 at pane
`+0x12`. The entry table and `+0x118` are read through `0x02B457E0`, the widget `0x003C2190` passes.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002B7CEF` and `0x002B7D00`, `0x002BB0F7` and `0x002BB108`, `0x003CB5CB` and `0x003CB5DF` |

</details>

## Layouts

All multi-byte fields are little-endian.

The file is a TIM2 file with the magic changed, one picture and no pixel data.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` |  | value "CLT2": read by no function: the table pointer, widget `+0x118`, is loaded by the draw `0x003C26C0` (`0x003C2794`), which hands it to `0x0024A9E0` (`+0x06` and the picture header from `+0x10`), and by the releases `0x003C1F00` (`0x003C2024`) and `0x003BC4E0` (`0x003BC55A`); nothing fixes its width |
| `+0x04` | `u8` | version | 4 |
| `+0x05` | `u8` | format | 0 |
| `+0x06` | `u16` | pictures | 1; read by `0x0024A9E0` as the bound of the picture index, which is 0 here |
| `+0x08` | `u8[8]` | zero |  |

Picture header (`+0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `u32` | totalSize | file size - `0x10`; not read |
| `+0x14` | `u32` | clutSize | colours x 4; not read |
| `+0x18` | `u32` | imageSize | 0; read |
| `+0x1C` | `u16` | headerSize | `0x30`; read |
| `+0x1E` | `u16` | colours | read |
| `+0x20` | `u8` | pictFormat | 0 |
| `+0x21` | `u8` | mipmaps | 0 |
| `+0x22` | `u8` | clutType | 3 (32-bit colours); not read |
| `+0x23` | `u8` | imageType | 5 or 4; not read |
| `+0x24` | `u8[28]` | zero |  |
| `+0x40` | `u8[4][colours]` |  | palette: R, G, B, A |

The palette starts at `+0x10 + headerSize + imageSize`. The alpha byte is on the PS2 scale, where `0x80` is
opaque.

The file stays as loaded in its buffer at widget `+0x118`, and nothing writes to it. The atlas slot keeps a
pointer to its palette (`+0x28`), and the upload copies the colours into the texture¹ and rescales
the alpha there ([the upload](#the-upload)). The next pane load frees the buffer (step 1 of the pane loader).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0017F503` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

Measured over every `.cl2` in the archive and every `menumap_common.bin`.

| Fact | Value |
|---|---|
| files | 20: `loca_bhm` and `loca_gil` in nine locales, `loca_rbl` in `ch` and `in`; 3 distinct contents, every same-name copy identical |
| sizes | 2,112 bytes (`bhm`, `gil`), 192 bytes (`rbl`) |
| colours | 512 (`bhm`, `gil`, image type 5); 32 (`rbl`, image type 4) |
| header | version 4, format 0, one picture, image size 0, header size `0x30`, clut type 3, total size = file size - `0x10`, clut size = colours x 4, all other header bytes zero, in all 20 |
| alpha bytes | `0xFF` in 239 of 512 colours of `bhm` and `gil`; every other alpha is at most `0x6F`; no alpha is `0x80` |
| `menumap_common.bin` | nine copies, 1,760 bytes; entry table at `0x0C` with 48 entries; byte `+1` is 1 in entry 40 and 2 in entry 46, 0 elsewhere |
| selected | entry 40 requests `0xE2` (`Loca_gil`), entry 46 requests `0xE3` (`Loca_bhm`); no entry selects `0xE4` |

[`cl2-menu-colour-tables-cl2-rows.tsv`](cl2-menu-colour-tables-cl2-rows.tsv) lists the 20 files, with size,
SHA-256, kind-7 id, the locale ids whose path array names each copy with their size-table entries, and
every header field, then all 1,056 colours of the three distinct contents: the raw RGBA, the alpha the
upload makes of it, the palette and pixel value the colour serves, and how many pixels of the selecting map
entry's pictures carry that value.

- `Loca_gil.cl2` recolours the two pictures of map entry 40, the Great Crystal maps `gil_i01` and `gil_i02`,
  and `Loca_bhm.cl2` the four of entry 46, the Sky Fortress Bahamut maps `bhm_a01`, `bhm_a02`, `bhm_a03` and
  `bhm_b01`. Those pictures have the same pixel counts in all nine languages.
- Locale ids 0, 6, 9 and 10 read the `in` copies; ids 1 to 5, 7, 8 and 11 read their own folder's (`us`,
  `fr`, `de`, `it`, `es`, `kr`, `ch`, `cn`). Every size table gives `0xE2` and `0xE3` their 2,112 bytes.
- For an 8-bit picture `0x00181000` makes one 256-colour palette per 256 colours¹, so the 512
  colours are palettes 0 and 1. Within a palette, pixel value `v` takes colour `v` with its bits `0x8` and
  `0x10` exchanged²: colour 8 serves pixel value 16. Every pixel value from 0 to 255
  occurs in the pictures.
- The exchange runs only for a picture whose `clutType << 8 | imageType` is `0x105`, `0x205`, `0x305`,
  `0x4104`, `0x4204` or `0x4304`³; any other pair keeps the file's order⁴.
  Every sloc picture in every folder (385 distinct pictures, 3,502 copies) has clut type 3 and image type 5, `0x305`.
- Each palette becomes a 256 x 1 texture⁵, registered under the picture's name with
  its palette number⁶.
- 239 colours of each 512-colour table have alpha `0xFF`, above the PS2 opaque `0x80`; the TSV marks them
  out of range, and the upload draws them at 255 like `0x80`. Every other alpha is at most `0x6F`.
- `Loca_rbl.cl2` (`0xE4`, 32 colours, `ch` and `in`) is selected by no map entry: byte `+1` is 0 in the 46
  other entries of all nine `menumap_common.bin` copies, so the pane loader never asks for `0xE1 + 3`. The
  US, FR, DE, IT, ES, KR and CN size tables hold -1 for it.
- A replacement keeps its palette at `0x10 + headerSize + imageSize`, `colours x 4` bytes long, and a count
  below `0x4000`, or `0x0024A480` keeps no palette for the picture⁷. Colours past the last
  multiple of 256 serve no 8-bit picture. The read is sized by the size table, so a file of another size
  needs its entries changed.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00181039` |
| ² | `0x00181064`-`0x00181108` |
| ³ | `0x00181064`-`0x00181095` |
| ⁴ | `0x00181111` |
| ⁵ | `0x0017F3B0`, `0x00181122` |
| ⁶ | `0x001B20B0`, `0x00181140` |
| ⁷ | `0x0024A4AA` |

</details>

</details>

## Loader behaviour

### The reader

`0x003C26C0(widget, n)` finds the pane holding `menumap_sub<n>` and walks the sub file's picture table. For each
picture whose atlas slot is still empty and whose offset is not -1, it:

1. takes the colour table at `+0x118`, or the buffer at `+0x110` when that is empty, and gets its picture header
   through `0x0024A9E0(buffer, 0)` (buffer `+0x10`). `+0x110` is the default: `0x003C2100` fills it, when it is
   empty, with `0x0035D520()` = `[0x0209AC30 + 0x3A0]`, which `0x00280AD0` sets to the third table of
   `clutpack_ys.bin` (kind 7 id `0xD4`, requested by `0x002808D0`);
2. reads the image size (`+8`), header size (`+0xC`) and colour count (`+0xE`) of that header and computes the
   palette address;
3. names the picture `loca_<a>_<b>` (`sprintf "loca_%d_%d"`) from the sub file's tables and registers it through
   `0x0024A480(picture, name, flags, palette, colours)`.

`0x003C26C0` returns 0 when neither pane holds a file for `n`¹. Otherwise it stores the picture count, the
low byte of the table's first word, at pane `+0x13` and the key array at pane `+0x08`²,
walks that many entries and returns 1³. The flags it registers with are the pane's byte `+0x12`⁴, and the handle goes into the atlas slot⁵. It also asks `0x0024A9E0` for the picture's
own header and drops the answer⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003C2704` |
| ² | `0x003C2730`-`0x003C273F` |
| ³ | `0x003C2864` |
| ⁴ | `0x003C2815` |
| ⁵ | `0x003C2829` |
| ⁶ | `0x003C27C7` |

</details>

`0x0024A480` registers the atlas¹ and, for a colour count below `0x4000`, stores the count in bits
`0x40000` and up of the slot's flags and the palette at slot `+0x28`, then builds the texture² and
returns the slot. The count compare is signed³; a larger count leaves `+0x28` at the 0 that
`0x0024A4E0` stored. The slot is not tested: with all 64 slots busy `0x0024A4E0` returns null, and the flag write
at `0x0024A4B1` faults, or with a larger count `0x0024A1D0` is handed the null slot.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024A4E0` |
| ² | `0x0024A1D0` |
| ³ | `0x0024A4AA` |

</details>

### The upload

With a slot palette present, `0x0024A1D0` passes the stored count, the palette and the picture's own clut and image
type bytes (picture header `+0x12`, `+0x13`) to `0x00181000` for an 8-bit picture or `0x00180E70` for a 4-bit one, so
the file's `clutType` and `imageType` never matter.

Both reach `0x0017F3B0(colours, n, 1, 1)`, n 256 or 16, which creates an n x 1 texture of the format object
`0x02CF7480`¹, named `RGBA8` by `0x00163D00`. That initialiser builds the object through
`0x00616210` with the name, `0xB`, `0x1F8`, 0 and four `0x1C`, and registers its teardown `0x008AF060` with
`atexit`². `0x0017F3B0` maps the texture³, copies the colours⁴, and rescales byte 3 of each to `min(255, trunc(a × 255 / 128))` (`0x0017F517`-`0x0017F54A`,
factor 1/128 at `0x008C5B34`), then commits it⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0060DD70`, `0x0017F433` |
| ² | `0x00808B90` |
| ³ | `0x0017EBD0` |
| ⁴ | `0x00679570`, `0x0017F503` |
| ⁵ | `0x0062C360`, `0x0017F572` |

</details>

A failed map skips the copy, the rescale and the commit¹. A null mapped pointer skips only the
copy, and the rescale then reads address 3 and faults². A null colour pointer
returns the texture unfilled³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0017F4D8` |
| ² | `0x0017F4E6`, `0x0017F520` |
| ³ | `0x0017F4B9` |

</details>

The texture object is `0x188` bytes from `0x0085E730(0x188, 0, -1)`, cleared and built by
`0x006160B0`¹. After `0x0060DD70` the buffer count asked for, the
fourth argument and at least 1, is compared with the texture's buffer count
`+0x30 & 0x7FFFFFFF`, taken as 1 when 0; when they differ
`0x00628100(texture, count asked for)` runs, after the log line "Altering buffer count of
PTexture2D whilst bound" when `0x00625F00` answers non-zero, and a 0 answer from `0x00628100`
clears `+0x0C`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0017F3E4`-`0x0017F40C` |
| ² | `0x0017F438`-`0x0017F480` |

</details>

Bit `0x2` of the flag dword `+0x18` is cleared before `0x00610990` and bit `0x200` set
after it¹. `0x0061E200` runs when the object's first qword is not
`0x02CF7A30` and `0x00625F00` answers 0². When the commit `0x0062C360`
answers 0 the dword `+0x0C` takes `[0x01F7F5A0] % count`, the buffer count, and the byte
`+0x08` becomes 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0017F483`-`0x0017F48F` |
| ² | `0x0017F496`-`0x0017F4B1` |
| ³ | `0x0017F553`-`0x0017F57E` |

</details>

The teardown `0x008AF060` frees nothing: it loads the address `0x02CF7480` and jumps to `0x0016D6A0`,
which only returns¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008AF060`-`0x008AF067` |

</details>

An alpha of `0x80` or more draws fully opaque; `0x6F` draws as
221 of 255.

## Modding notes

- To recolour every map without a `.cl2`, edit the third table of `clutpack_ys.bin`, which uses the
  same layout.
- The game never checks `CLT2`, the version, the picture count, the sizes or the clut and image types. It reads
  `+0x18`, `+0x1C` and `+0x1E` and the palette they locate, and the picture count only as the bound of the
  picture index¹, which the reader passes as 0, so the header is at `+0x10` for any count.
- Keep the image size 0 and the header size `0x30`, or move the palette to match `0x10 + headerSize + imageSize`.
- Write alpha on the PS2 scale: `0x80` is opaque, and values above it saturate.
- To recolour another map, set byte `+1` of its `menumap_common.bin` entry to `k`; the game then requests kind 7
  id `0xE1 + k`, which must be a shipped path with a size in the file-size tables.
- `Loca_rbl.cl2` (`0xE4`) ships only in `ch` and `in`, so a byte of 3 would request a file missing in the other
  locales.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024A9E4` |

</details>

## Related

- [Map screens](../Menus-And-HUD/map-screens.md): the map-data widget and the menumap files it loads.
- [UI typed lists](ui-typed-lists.md): the atlas registry `0x0024A480` registers each picture in.
- [File size tables (.fst)](file-size-tables-fst.md): the kind 7 path arrays and request sizes.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the request entries.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Platform** (explained on [gi render commands](../Graphics/gi-render-commands.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0060DD70`](cl2-menu-colour-tables.md) | is called by | [`0x00625830`](../Graphics/gi-render-commands.md) (on gi render commands) |

</details>
