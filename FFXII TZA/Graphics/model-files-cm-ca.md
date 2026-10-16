---
title: "Model files (.cm, .ca): the @FRP container and its FCP, FDM, FOR, FTE, FCT and FTR entries"
kind: "format"
category: "Graphics"
addresses: "00504F00, 00504E70, 00504940, 004780C0, 0041FCF0, 0041F340, 00420480, 002EDBD0, 003E55F0, 004FE270, 004FE2F0, 01F265B0, 01F266B0, 003E6150, 003E5AD0, 0041E5B0, 004292B0, 003712E0, 00372820, 003713C0, 00409300, 004094D0, 00409250, 0046D560, 004201F0, 00504840, 005048A0, 0053AB50, 00504D30, 005044D0, 00504D20"
---

## What the player sees

Every character, monster, NPC, summon, weapon, treasure chest and map object on screen is drawn from
a `.cm` file: its skeleton, its textures and palettes, which parts it draws, how far away it switches
to a simpler look, and the radii, heights and turn rates the battle code reads for it. Its motions
come from `.ca` files. The grey look of a model under a status effect is not a shader: almost every
palette carries a grey fourth page, and the game switches the model to it.

## Where it comes from

The files are in the archive at `ps2data/obj_finish/in/<folder>/.../<name>.cm` and `.ca`; the folders
are `weapon`, `monster`, `npc`, `high`, `gadget`, `summon`, `chara`, `treasure` and `bg_obj`.

A loaded file is registered in the render resource bank like any other source (see
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)), and its
entries are found by tag and name in the `@FRP` container (see
[resource sections](../Game-Files-And-Data-Tables/resource-sections.md), which covers the container
header, its version 0 and version 1 offset tables and the section search).

A character render record is bound to its model by `0041FCF0`, which passes the model's bank index
(record `+0x408`) to `0041F340`. That routine:

1. finds the `@FTR` entry by tag and the record's name (`00409660`), sizes the skeleton
   (`003712E0`) and builds it in a new row of the table at root `+0xD98` (`0046E4D0` → `00372820`);
2. makes a model row in the table at root `+0xDA0` with `004780C0`, which calls `00504F00`, and keeps
   the row's index in the record's word `+0x90`;
3. when the model's bank entry has an effect ticket, makes the record's effect context from it
   (`003B3550`, kept at record `+0x288` and row `+0x240`).

`00420480` then points record `+0x400` at the `@FCP` payload (`004205E6`) and stores the `@FOR` scale
at record `+0x26C` (`0042061B`).

## Layouts

### The container

```
@FRP header (0x30 bytes)   see resource sections; name = the file name without extension
version 0                  every .cm (1,066) and 1,969 .ca: u32 offset table at +0x30, offsets from +0x30
version 1                  1,195 .ca: +0x30 u32 columns (80), +0x34 u32 rows, offsets from +0x40, 0 = empty slot
+0x08                      u32 content length; the rest of the file is zero padding
```

### The entry header

Every entry starts with the same `0x30`-byte header the section search compares.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | tag | @FCP, @FTR, @FDM, @FOR, @FTE, @FCT, @FEF, @FMC, @FMN, @FMW, @FRM |
| `04` | `u32` | kind | @FTR 2; @FCP, @FDM, @FOR, @FTE, @FCT, @FEF 0 |
| `08` | `u32` | length | bytes of the entry, header included |
| `0C` | `u32` | count | @FCP 1, @FTR nodes, @FTE textures, @FCT palettes, @FDM and @FOR 0 |
| `10` | `char[32]` | name | the container's name for the model entries |

### The model row

`00504F00` fills a `0x260`-byte row of the root's `+0xDA0` table. It copies the 32-byte model name to
`+0x0C`, binds the container section at `+0x1F0` and the `@FEF` section at `+0x228` (`00504E70`), and
stores each entry's offset from the container, or −1 when the entry is absent (`00409A30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `1F8` | `void*` | the @FRP container (00504940) |  |
| `208` | `u32` | @FOR offset | +`0x214`  u32   @FEF offset |
| `20C` | `u32` | @FDM offset | +`0x218`  u32   @FTE offset |
| `210` | `u32` | @FTR offset | +`0x21C`  u32   @FCT offset |
| `220` | `u32` | @FCP offset | +`0x230`  ptr   the @FEF section (`00504940`) |
| `0B8` | `i8` | the @FOR record key | +`0xB9`  s8    the option number |
| `0B3` | `u8` | LOD levels (+0x3A + 1) | +`0xBA`  s8    the palette page (`00504D20`) |

### @FCP, the parameter block

Entry 0 of every `.cm`. The payload starts at entry `+0x30`; offsets are from the payload.

```
+0x00  u8        4
+0x01  u8        non-zero: 0041F340 allocates a second per-node block and sets record +0x284 bit 0x10000;
                 id 0x40000000 returns it
+0x02  u16[17]   offset of sections 1 to 17, 0 = absent (section n at +2n)
+0x24  u32       length of section 2, copied after the skeleton
+0x2C  u8[6]     event map (0041E5B0), 0x7F ends it
+0x32  u8        version, 0x0A
+0x3A  u16       bone for special id 0x104 (003E5AD0)
+0x3C  u16       bone for special id 0x105
+0x3E  u16       bone for special id 0x106
section 1 +0x14C u16[32]  bone for special ids 0 to 31 (003E5AD0)
section 2        copied verbatim after the skeleton core (00372820)
section 7        the pose sequencer's events (model-oscillators-and-pose-sequencer.md)
section 8        a 0x10-byte head starting with a u16 count, then count x 0x1D0 bytes (003E6D10);
                 copied into the record's block by 0041F340
section 9        f32 / u32 slots read through property ids
```

A property id is `SS VV DD FF`: `SS & 0x1F` is the section, `SS >> 5` the mode, `VV` the lowest
payload version that may answer, `DD` the slot in the default table and `FF` the slot in the section.

- `004FE270(payload, id)` reads a float. With no payload or `VV` above the version byte it returns
  default float `DD` from `01F265B0`. Otherwise an id of `0x20000000` or more returns −1.0, and any
  other id reads section slot `FF`, or the default when the section is absent.
- `004FE2F0(payload, id)` reads an integer. Mode 1 (`0x2…`) reads dword `FF` with the same fallbacks,
  defaults from `01F266B0`. Mode 3 (`0x6…`) reads byte `SS & 3` of dword `FF` of section 9. The id
  `0x40000000` returns payload byte `+0x01`. Any other mode returns −1.
- `003E6150(record, id)` returns 0 for a model without `@FCP`; otherwise it calls the float getter and multiplies the result by the record's scale `+0x26C`
  for a fixed list of section 1 and section 9 ids, or divides by it for `0x9001E1F`.

Small readers take values straight from the record's `@FCP` payload `+0x400`, scaling sizes by the
record's per-axis scale (`+0x260`–`+0x268` × `+0x160`–`+0x168` × `+0x26C`):

- `003E5CD0` returns section 3, or null; `003E4700` section 1's float `+0x144` (1.0 without).
- `003E4DD0(record, axis)` section 1's `+0x114`, `+0x118` or `+0x11C` times that axis's scale (1.0
  without); `003E5130` the six floats `+0xBC`–`+0xD0` of section 1, two each times the z, x and y
  scales; `003E4B50` a box from section 1's `+0x114`–`+0x11C`, or from `004234B0`'s `+0x54` when it
  returns a block. `0042E850` calls `003E4700`, `003E4DD0` and `003E4B50`; the effect target
  queries `003A4290` and `003A56F0` call `003E5130` and `003E4F50`.
- `003E5C90` returns section 9's float `+0xA8` (0.10472 without), `003E5EA0` its `+0xA4` (0 without),
  and `003E4F50` places section 9's point `+0xD0`–`+0xD8` by the record's matrix `+0x180` and adds the
  focus point `+0x670`. `003E56E0` reads property `0x62060A2D` (`004FE2F0`).
- `003E6D40(record)` returns the arena address of the block at `+0x2FC` plus the offset `+0x300`, or 0
  when the offset is 0 (`003AB7F0`).

### @FTR, the skeleton

```
+0x30  u32       node count again
+0x34  u32       offset of the value pool, from the entry
+0x38  u16       extra u16 slots after the node list (equal to the @FDM key count)
+0x40  u32[n]    per node: (record offset from the entry << 12) | node number
record +0x00  u32  bits 0-11 the node's key, bits 12-23 its parent (0xFFF = none), bits 24-31 0xFF
record +0x04  u32  flags; the u16 pool indices follow at +0x08 (+0x0A when bit 30 is set)
```

With flag bits `0x200100` both set, `00409300` takes one pool dword for each of bits 23, 24 and 25 as
the node's translation x, y and z, and one pool float for each of bits 26, 27 and 28 as three angles
in radians that `0046D560` turns into the rotation; otherwise the node starts at the identity. Bit 21
makes `004094D0` copy sixteen pool dwords as a 4×4 matrix to node `+0x150`. Bits 31 and 22 each skip
one index. `00409250` returns the key from bits 0–11, or the u16 at `+0x08` when bit 30 is set.

`00409240(entry)` gives the node count (word `+0x30` for a kind-2 entry, dword `+0x0C` otherwise),
`00409270(entry, n)` the address of node `n`'s record (`+0x40` table entry `>> 12`, 0 past the count
or for another kind), and `004095A0` the address of the `+0x40` table. With flag bit 22 set,
`004092A0(entry, record)` returns the pool dword named by the node's first pool index, skipping one
index for bit 31 and sixteen more when bits `0x200100` are both set, and 0 otherwise.

### @FOR, variants and distance LOD

```
+0x30  u8     record count
+0x32  u8     table B stride per option number
+0x33  u8     option numbers allowed (row +0xB9 is clamped below it)
+0x34  u16    table A offset (0x40)
+0x36  u16    table B offset
+0x38  u16    offset of the records, 0xE0 bytes each
+0x3A  u8     LOD distance count (0, 1 or 2)
+0x3B  u8     highest LOD level
+0x3C  u16    first LOD distance, centimetres
+0x3E  u16    second LOD distance, centimetres
record +0x00   u8    key
record +0x05   u8[]  selector count per part
record +0x18   f32   the model's scale
record +(i+1) x 0x20   part i's selector bytes
```

### @FDM, the key table

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `30` | `u16` | 1, 2 or 3 |  |
| `32` | `u16` | offset of {u32 count, u32 keys[count]} (0x50) |  |

### @FTE, textures

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `30` | `u8` | count, then u8 texture slots uploaded with every draw |  |
| `40` | `records,` | 0x20 | bytes each, +`0x0C` of the header many |
| `00` | `u32` | VRAM bytes, a multiple of 0x2000 |  |
| `04` | `u16` | width | +`0x06`  u16  height |
| `08` | `u16` | GS pixel format: 0x13 8-bit indexed, 0x14 4-bit indexed |  |
| `0A` | `u16` | upload width | +`0x0C`  u16  upload height |
| `14` | `u32` | upload bytes = upload width x height x 4 |  |
| `18` | `u32` | pixel data offset, from the entry |  |

### @FCT, palettes

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `30` | `records,` | 0x10 | bytes each, +`0x0C` of the header many |
| `00` | `u16` | VRAM bytes (0x2000) |  |
| `02` | `u16` | palette bytes (colours = bytes / 4) |  |
| `04` | `u8` | upload width | +`0x05`  u8   pages (4) |
| `06` | `u16` | upload height |  |
| `0C` | `u32` | data offset, from the entry: four pages of palette-bytes each |  |

## Shipped data

| Fact | Value |
|---|---|
| `.cm` files | 1,066, all version 0: weapon 326, monster 254, npc 174, high 132, gadget 103, summon 26, chara 17, treasure 17, bg_obj 17 |
| `.ca` files | 3,164: 1,969 version 0, 1,195 version 1 (80 columns in all; 1 row in 1,150, 3 in 45) |
| container name | equals the file name in all 4,230; bytes `+0x20`–`+0x2F` zero in all |
| padding | every byte past `+0x08` is zero; `.ca` version 0 files are unpadded |
| sizes | `.cm` 7,168 to 1,310,720 bytes, median 131,072; `.ca` 1,408 to 2,752,512, median 15,552 |
| `.cm` entry sets | the six model entries in 855; the same plus `@FEF` in 144; plus `@FMC`, `@FMN`, `@FMW` in 45 (29 weapons, 16 treasures); `@FCP @FTR @FOR` in 21 weapons; `@FCP @FTR @FDM @FOR` in 1 |
| `@FCP` | entry 0 in all 1,066; version byte `0x0A` in all; 976 to 42,960 bytes |
| `@FCP` sections | 1, 2, 6 and 7 in all; 9 in 723 (absent in every weapon and bg_obj); 3 in 603; 10 in 613; 4 in 216; 8 in 28; 5 in 7 |
| `@FCP` byte `+0x01` | 1 in 127 (81 monsters, 26 summons, 20 NPCs), 0 elsewhere |
| `@FCP` event map | all zero in 723; `7F`×6 in 298; `3D 36 35 01 81 7F` in 29 weapons; `08 01 05 00 7F 7F` in 16 treasures |
| `@FTR` | kind 2 in all; 27,561 nodes; one root per file, always node 0; every other parent below its child |
| `@FTR` flags | bit 8 set and top byte `0xFF` in all 27,561 nodes |
| `@FTR` `+0x38` | equals the `@FDM` key count in all 1,045; up to 1,188 (`m1208`) |
| `@FOR` | in all 1,066; one record in 1,000, up to 12; keys 1 to n in 1,062 |
| `@FOR` LOD | no distance in 751, one in 179, two in 136; 32,767 cm (no switch) in 59: the only distance in 54 one-distance files, the second in 5 two-distance files |
| `@FDM` | in 1,045 (all but 21 weapons); 30,023 keys, all below `0x10000` |
| `@FTE` | in 1,044; 2,127 textures, 1 to 17 per file; 2,081 8-bit and 46 4-bit; pixel data packed in record order up to the entry's end in all |
| `@FCT` | in 1,044; 1,972 palettes of 256 colours (1,618), 128 (318) or 16 (36); four pages in all |
| palette page 3 | mean colourfulness (max − min channel) 30.6, 30.5, 21.4 and 1.6 on pages 0 to 3; grey on page 3 only in 1,818 of the 1,970 palettes whose pages fit |

## Loader behaviour

### Binding a model row

- `00504E70(sub, bank, root, tag, name)` looks the tag up in the given bank entry and, when that fails,
  searches the bank for an entry with the tag and name (`00409FA0`).
- `00504940` stores the container pointer at `+0x1F8` and the `@FEF` section at `+0x230`.
- `00504F00` walks the `@FOR` records for the requested key: a match is stored at `+0xB8`; otherwise
  the first record's key, or 0. The option number is kept at `+0xB9` when it is below `@FOR +0x33`,
  else 0. `+0xB3` gets the LOD distance count plus one, and the row's flags `|= 3`.

### @FCP

- `002EDBD0(record)` looks `@FCP` up by tag and the record's 32-byte name at `+0x3C` and stores the
  payload (`+0x30`) at record `+0x400`, or 0 when absent; `003E55F0` returns it. Nothing is checked
  or converted on load, and every later read goes through the getters.
- `003E5AD0(record, id)` returns the bone for a special id: ids below `0x20` from section 1's table,
  `0x104`–`0x106` from `+0x3A`–`+0x3E`, `0xFFFF` otherwise.
- `0041E5B0(record, state, event)` scans the six-byte event map, stopping at a byte whose low seven
  bits are `0x7F`, and returns the index of the byte whose low seven bits equal the event, or −1.
  Bytes with the high bit set match only when state is 0, and are tried first.
- `004292B0` plays a motion id of `0x1000` or more through it when the record has its own motion
  entries (`+0x2F8` set): the index picks `@FMC` entry `[+0x2FA] + index` of the model's own
  container, keeping the id's top four bits. An id with no match plays nothing and returns −1.

- `0041F340` copies section 8 (head plus `count × 0x1D0` bytes, `003E6D10`, `003E6CF0`) into the
  record's block at `+0x2FC`, offset `+0x300`, writes the record index at the copy's `+0x08` and
  calls `0051D220` on it. The first call ever builds a 64 × 64 8-bit texture and a 256-colour
  palette from the image embedded at `01F2B340` (`00184140`, `001837A0`); every call clears the
  copy's byte `+0x06` and `02CA8428`.
- The record-system reset `00425DC0` runs `0051D1D0` first: it zeroes the 16 KiB of emulated VU
  memory at `02064E30`, calls `00258EE0(3)`, and binds the embedded texture and palette to GS
  addresses `0x2A00` and `0x2E00` (`002D7E00`).
- Authored command `0x1F` reaches `003E6710(record, on)`: on runs `0051DB60` on the copy, which sets
  its word `+0x06` to 1 and resets each entry (`+0x14` = 1.0, `+0x00` and `+0x10` cleared, `+0x1C4`
  = 1, `0x100` bytes at `+0xA0` zeroed); off runs `00519720`.
- `0051D2F0(copy, value)` keeps the low two bits of `value` in byte `+0x07` and masks the byte's
  other bits with `value >> 2`; `00421280` passes 4 or 6.

### @FTR

`003712E0` sizes the skeleton as `(count × 0x149 + [+0x38]) × 2` rounded up to 16 bytes, plus the
section 2 length: `count` nodes of `0x290` bytes, then `count + [+0x38]` u16 slots. `00372820`:

- matches the model name against `skeletonmapping.bin` (see [add-motion tables](add-motion-tables.md))
  and keeps the last match at skeleton `+0xB0`;
- builds every node. Each parent gets its first child at node `+0x274` and siblings chain through
  `+0x272`; a node without a parent joins node 0's sibling chain. A node with flag bit 8 is built from
  its pool values and its number is appended to the u16 list after the nodes; any other node starts
  at the identity;
- fills the `[+0x38]` extra slots with `0x7FFF`;
- copies section 2 after the core (`003729BD`) and runs `003713C0`, which hands it to `003E1C50`.

The binder also accepts kind 0, records of `0x4C` bytes from `+0x30` with the parent at `+0x20`; no
shipped file uses it.

### @FOR

- `00504840(entry, key)` returns float `+0x18` of the record with that key, or 1.0. `00420480` calls it
  with record byte `+0x5C`, and the result is the record scale that `003E6150` applies.
- `004201F0(record, view)` runs only when the entry starts with `@FOR`. With a non-zero distance count
  it builds the windows `{0, d0 × 0.01, d1 × 0.01, 1.0e8}` in metres, or uses the record's float array
  `+0xA0` when record byte `+0xC0` bit 0 is set.
- The level is the first window that holds the view depth (float `+0x208`; a negative depth gives
  level 0), capped at `+0x3B`. It stores `(count + 1 − level) / (count + 1)` at record `+0x2A4`, so 1.0
  is nearest, then calls `00421280`.

### @FDM

`005048A0(record, key)` returns the position of the key in the key table, or −1.

### The draw builder

`0053AB50` resolves table A, table B and the records from `+0x34`, `+0x36` and `+0x38`
(`0053B33A`–`0053B35A`) and takes the record whose key equals row `+0xB8`. For each part and each of
its selector bytes `s` it reads `A = tableA[3s + part] + [+0x32] × option` and the pair
`tableB[2A]`, `tableB[2A + 1]` (`0053B4B6`–`0053B4EC`): the first is an `@FTE` texture slot, the second
an `@FCT` palette. The texture slots listed at `@FTE +0x30` are added to every draw (`0053B45A`). The
VRAM bytes `+0x00` of the selected textures are summed before upload (`0053B5B0`).

### The texture slot cache

Uploaded model textures are tracked in a cache of 256 entries of `0x30` bytes at `[02CA8450]`,
which the root-bank builder `0041E3A0` allocates through `005211F0` (every entry's index and key set
to `0xFFFF`) and forgets through `00521300`. The live count is `02CA8458` and the next search start
`02CA845C`.

- `005210F0(key)` returns the entry already holding the key and adds a reference (`+0x24`), or takes
  the next free entry from the search start, clears its word `+0x24` through `00540FC0` and then
  sets it to 1; it returns `0xFFFF` when 256 are in use.
- `00521250(index)` drops a reference and frees the entry at 0. `00521290(key)` finds an entry by
  key; `005212E0(index)` returns entry `index & 0xFF` when its first word still equals `index`.
- `00504520(instance, slot, texture)` binds an `@FTE` texture to the instance's slot word
  `+0x100 + 2 × slot`: it releases the old entry, takes one for the texture's key (`+0x1C`), and
  copies the texture's size and register words with the base-2 logarithms of width and height.
- `00504800(instance, slot)` returns the slot's width and height as one dword once the entry is
  marked uploaded (bit 0 of `+0x1C`), else 0. `00521320` clears that mark and the word `+0x14` in
  all 256 entries.

### The upload area

The draw places the selected textures in GS memory through two windows over the addresses from
`12 × width × height` of the GS frame (`022D8EAC`, `022D8EB4`) up to `0x3C0000`. Window `i` has a
low cursor `02EBA460[i]` and a high cursor `02EBA468[i]`.

- `00537AA0(window, size, end)` takes `size` bytes from the low end (0) or the high end (1) and
  returns their start, or 0 when they do not fit; `00537AF0(window, size)` only tests the fit.
- `00537B10(0, end)` puts window 0's end back to its start value and copies it into window 1;
  `00537B10(1, end)` copies window 0's current end into window 1. `00477F20` calls `00537B10(0, 0)`
  and `00537B10(0, 1)` before it draws the instances (`00477F2D`, `00477F39`).
- When a model's textures and palettes do not fit window 1, `0053AB50` resets window 1 from window
  0 and clears every cache mark (`0053B67E`–`0053B699`). It then takes textures from the low end
  and palette pages from the high end (`0053B761`, `0053BB73`).

The draw writes its transfers and state into the current GS command buffer (`005044B0` returns
`02EBEFC0 + 0x18 × [02EBEFF0]`), and when fewer than a block's bytes remain it closes the buffer
with `00504450`: a `{0x10000000, 0}` record, then the flip `003A1DB0`. `00504490` only flips.

- `0053D4B0` writes a part's alpha and depth test: registers `0x47` and `0x48` with the reference
  `alpha × [02CA81DC]`, capped at `0x80` and raised to `[01F2CA90]` for an instance with `+0xF8` set
  whose `003E56A0` entry has bit 3 of `+0x134`; the alpha is the part's bits 1–7, or the
  instance's byte `+0xBC`. With instance `+0x08` bit 3 it writes `0x34000` instead.
- `0053D140` writes a material block: a tag (`0x10000008`, `0x50000005`), two register words per
  mode (`0x44` and `0x42`/`0x43`, or `0x4A`), per-texture pairs from the material when its flag byte
  has bit 0 or bit 2, and the two texture handles.

### Palettes

- `00504D30(row, index, sub, out)` makes a palette resource of `bytes / 4` colours for palette
  `index` (below `+0x0C` and 16), keeps it in the row's 16 slots at `+0x140`, and records the pair
  `(index << 4) | sub` in the row's 20-byte map at `+0x180`.
- `005044D0(row, index)` returns the page in use: data offset + `row[+0xBA]` × palette bytes.
- `00504D20(row, page)` sets `+0xBA`. `00428CD0` sets it on a render record, its partner and their
  children; the status step `00470780` passes 3 (`0047082A`, `0047091B`, `00470A43`), other callers 0
  or 2.

### Palette animation

A palette resource is also registered for animation in one of 32 records of `0x40` bytes at
`[02B47790]` (`003CCB60(source, destination, colours)`, from `00504D30` and the map's palette parser
`00468160`): the handle is `serial << 8 | slot` (serial `02B47774`, wrapping to 1 past `0xFFFFFF`),
and the record joins a list (head `02B47778`, tail `02B47780`, count byte `02B47770`).

`PaletteRecord` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | opCount | operation count |
| `01` | `u8` | flags | any of bits `0x3F` set: +`0x08` and +`0x10` are handles (`0036B130`); `0x40` keep running; `0x80` run |
| `02` | `u16` | colourCount | colour count, at most `0x20` |
| `04` | `u32` | handle | serial << 8 \| slot |
| `08` | `void*` | source | source palette |
| `10` | `void*` | destination | destination palette |
| `18` | `void*` | previous | previous record |
| `20` | `void*` | next | next record |
| `28` | `void*` | firstOp | first operation |
| `30` | `void*` | lastOp | last operation |
| `38` | `u32` | overrideOnly | when non-zero, runs only while `00181DD0` reports an override |

`PaletteOperation` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | kind | 1-8 |
| `04` | `u8` | paletteSlot | palette slot |
| `08` | `u16` | length | length in steps (0 = no end) |
| `0A` | `i16` | delay | start delay |
| `10` | `u16` | period | 0 = none |
| `15` | `u8` | mode | 0 wrap, 1 back and forth |
| `20` | `u32` | secondPalette | second palette handle (kinds 4 and 8) |
| `30` | `u32` | handle | operation handle |
| `34` | `u16` | time | time |
| `36` | `u16` | phase | phase |
| `38` | `void*` | next | next operation |
| `40` | `void*` | previous | previous operation |

The 128 operation records are at `[02B47798]`.

`003CCF20(step)`, each simulation step from `00258D70` and `00258E40`, walks the records with bit 7
set (clearing it unless bit 6 is set): it copies the source colours into `02B477A0` (`003CD840`),
counts each operation's delay down or its time up by `step`, takes the phase (the time modulo the
period, or reflected on odd periods in mode 1), applies the operation, and writes the result to the
destination (`003D2B60`). An operation past its length is removed.

The kinds call `0050AC20`,
`00506B40`, `005080A0`, `0050A100` (with the second palette), `00509BB0`, `00507490`, `00508C90` and
`00507120` (with the second palette).

`003CD2C0(handle)`, from the draw builder `0053AB50`, does the same once into `02B4A7A0` without
moving time. `003CD6C0(handle)` returns the record; `003CD7C0` and `003CD7F0` set its bits 6 and 7;
`003CD590` detaches its operations and clears its count; `003CD5D0` unregisters it; `003CD650(handle)`
removes one operation from its record.

## Modding notes

- Keep every entry's name equal to the container's: the model row finds each entry by tag and name.
- `@FCP` must be entry 0 and keep version `0x0A`; a lower version byte makes ids with a higher minimum
  version return the built-in defaults.
- A model without section 9 gets the built-in defaults for every battle radius and turn rate.
- In `@FTR`, list a parent before its children, keep node 0 the root, and set flag bits 8 and 21
  together with the pool values each bit reads.
- `@FTR +0x38` must equal the `@FDM` key count; the skeleton reserves exactly that many slots.
- The `@FOR` record's float `+0x18` scales the model's battle radii and heights with it.
- LOD distances are centimetres; with no distance the model never switches.
- Give every palette four pages; page 3 is shown by the status step that passes 3.

## Related

- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` header and the section search.
- [Resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): how a loaded file is registered and released.
- [Model effects and motion commands](model-effects-and-motion-commands.md): `@FEF` and the motion entries.
- [Add-motion tables](add-motion-tables.md): the skeleton mapping matched against a model's name.
- [Model oscillators and the pose sequencer](model-oscillators-and-pose-sequencer.md): `@FCP` section 7 and the sway section.
