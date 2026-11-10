---
title: "MPK map pack: the sections of a map file, the two packs a field loads, how the loader splits and binds them, and what each section holds"
kind: "format"
category: "World, areas and travel"
addresses: "0x00331990, 0x00378A60, 0x00378030, 0x0036B980, 0x00378BC0, 0x003775D0, 0x00378120, 0x00378230, 0x002F6AB0, 0x003E8940, 0x003E8230, 0x00363B40, 0x003631B0, 0x00379870, 0x003C63A0, 0x0037AA90"
---

## What the player sees

Walking into a new area loads its map pack: the area's sound bank and positional sounds, its world
data (the models, their placement, the lighting and the weather-dependent look), its navigation
mesh, its lights, the switch-driven objects a script controls, and the picture and coordinates the
minimap uses to show where you are. An area that shares a sound bank with its neighbours loads that
bank once from a second, sound-only pack. A section a pack does not carry simply supplies nothing.

## Where it comes from

Each pack is `ps2data/plan_master/map_ctrl/<area>/<zone>/bin/<zone>.mpk`, 550 files. A zone's own
pack is `<zone>.mpk`; the block pack of an area is the one named `<area>00.mpk`, and all 89 of them
carry only the sound sections (slots 0, 1 and 10) or nothing at all.

The packs are namespace-4 resources. `map_ref.bin` names both packs of a field: the field row's
first word is the field's own pack index (`0x00264F10`), and the first word of the row's 16-byte block
record is the block pack index (`0x00264F40`); the block record's second word plus 500 is the sound
map number stored at `0x02ADD078` (`0x00264FD0`, `0x00378030`). The row and block layouts are on the
weather page, which reads the same two tables.

## Layouts

All multi-byte fields are little-endian.

### The pack

`MpkHeader` (`0xC0` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | 32 in all 550 packs; `0x0036B980` rejects a count above 32 |
| `+0x04` | `u32[32]` | size | section size per slot in slot order; 0 means the slot is absent |
| `+0x84` | `u8[60]` | pad | the header is padded to a multiple of `0x40` |

The header length is `((count + 1) * 4 + 0x3F) & ~0x3F`, 0xC0 for 32 slots. After it, for each slot
whose size is non-zero and in slot order, come a 0x40-byte slot (zero in the file; the loader
overwrites it with an arena block header) and the section's bytes. There are no offsets: a section's
position is the running sum, and `0x0036B980` refuses the pack when the sum does not equal the loaded
block's size (`0x0036BA30`-`0x0036BA45`).

| slot | magic | section | kept by | consumer |
|---|---|---|---|---|
| 0 | `SeSe` | the `SeSep` sound-effect bank | mode 0 (`0x02ADD080`) | `0x003635E0` walks it with `0x002DF070` and frees it |
| 1 | `WD` | a wave bank | neither mode | freed unread (`0x00378BC0`) |
| 4 | u32 1 | the navigation dataset | mode 1 (`0x02ADCFE8`, copied) | `0x00384160` binds it (the navigation mesh page) |
| 8 | `YM00` | world data | mode 1 (`0x02ADCFE0`), mode 0 (`0x02ADCFF0`) | `0x0026E760`, `0x0026E7D0` build the 0x240-byte world object through `0x002F6AB0` |
| 9 | `ACTL` | the actor-control table | both (`0x02ADD0B8`) | `0x003E8940` publishes it at `0x02B5D080` |
| 10 | `SPP1` | the map sound list | mode 0 (`0x02ADD068`) | `0x003635E0` keeps it at `0x022CBAF8` (the map sound list page) |
| 13 | `EFB0` | a map effect bank | neither mode | freed; the loose `PS2Data\efb\<zone>.efb` is loaded instead (`0x00377DC0`) |
| 15 | `MRP` | a menu resource package | both (`0x02ADD058`) | `0x00377B90` returns it to `initgauge` (`0x0034DC70`) |
| 16 | `SP1` | the sound-emitter block | both (`0x02ADD060`) | `0x003635C0` keeps it at `0x022CBAF0` |
| 17 | `LGT2` | the light set | both (`0x02ADD090`) | `0x0037AA90(block, 0)` |
| 24 to 27 | `TIM2` | map pictures, one per sub-location | both (`0x02ADD010` + 8i) | `0x003C63A0` uploads picture 0 |
| 28 to 31 | `NPS2` | each picture's placement | both (`0x02ADD030` + 8i) | `0x00379870` applies placement 0 |

Slots 2, 3, 5 to 7, 11, 12, 14 and 18 to 23 are never read by `0x00378BC0` (slot 12 is freed), and no
shipped pack fills them.

### Slot 4, the navigation dataset

The dataset's use is on the [navigation mesh page](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md).
Every offset is from the section start: `0x00384160` adds the dataset's address to `+0x0C` to `+0x20`, `+0x28` and the
grid's `+0x08` and `+0x0C` (`0x00384174`-`0x003842CC`). The readers named below are all the code that loads the
dataset pointer `0x02AEDFB0` or calls its getter `0x00383840` (`0x00335180`, `0x0033D3E0`, `0x00391410`, `0x00392740`).

`NavHeader` (`0x30` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | one | 1 in all 461; read by none of `0x00384160`, `0x00382D10`, `0x00382FF0`, `0x00383740`, `0x00383850`, `0x00383A30`, `0x00383C90`, `0x00383F10`, `0x00335180`, `0x0033D3E0`, `0x00391410` and `0x00392740` |
| `+0x04` | `u16` | vertexCount | read by none of the same readers |
| `+0x06` | `u16` | triangleCount | the whole-mesh loops' bound (`0x00383AAD`, `0x00335293`) |
| `+0x08` | `u16` | portalCount | read by none of the same readers; it counts the padding record 0 |
| `+0x0A` | `u16` | regionCount | the adjacency row length (`0x00383883`, `0x0033D4DA`) and the search's bound (`0x003830F4`, `0x003832AA`) |
| `+0x0C` | `u32` | vertices | `0x00382D6B`, `0x00383B0B`, `0x003352FA`, `0x0033D53F` |
| `+0x10` | `u32` | triangles | `0x00383AC0`, `0x003352A5`, `0x003840B5` |
| `+0x14` | `u32` | portals | `0x00383385`, `0x003838A4`, `0x00383D11`, `0x0033D4F3` |
| `+0x18` | `u32` | regions | `0x0038406D` |
| `+0x1C` | `u32` | adjacency | `0x00383372`, `0x00383874`, `0x0033D4D2` |
| `+0x20` | `u32` | grid | `0x00383F23`, `0x00383771` |
| `+0x24` | `u32` | trailerCount | `0x00392909`, used as min(count, 32) (`0x0039290C`) |
| `+0x28` | `u32` | trailer | `0x00392920`, `0x00391597` |
| `+0x2C` | `u32` | pad | 0 in all; read by none of the same readers |

`NavVertex` (`0x8` bytes, offsets from the start of the vertices):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | x | `0x00382D91`, `0x00383B31`, `0x0033531F`, `0x0033D54B` |
| `+0x04` | `f32` | z | `0x00382DCF`, `0x00383B6F`, `0x0033534A`, `0x0033D566` |

`NavTriangle` (`0x8` bytes, offsets from the start of the triangles):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[3]` | vertex | through the edge table {0, 1, 2, 0} at `0x00D112B0` (`0x00382D7A`, `0x00382D97`, `0x00382DB8`) |
| `+0x06` | `u16` | region | `0x00383AC8`, `0x003352BB` |

`NavPortal` (`0x8` bytes, offsets from the start of the portals):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | vertexA | `0x0038339B`, `0x0038390D`, `0x00383D26`, `0x0033D542` |
| `+0x02` | `u16` | vertexB | `0x003833C6`, `0x00383936`, `0x00383D50`, `0x0033D585` |
| `+0x04` | `u8` | gate | only compared with `0xFF` (`0x003838CC`); `0xFF` or 0 in the shipped records |
| `+0x05` | `u8` | mapId | passed to `0x0032A780` when the gate is not `0xFF` (`0x003838D3`); `0x0033D3E0` passes it with no gate test (`0x0033D4FE`) |
| `+0x06` | `u8` | classMask | bit moverClass (`0x003838C4`, `0x0033D520`) |
| `+0x07` | `u8` | pad | 0 in all; read by none of `0x00382FF0`, `0x00383850`, `0x00383C90` and `0x0033D3E0` |

Record 0 is padding (`00 00 00 00 FF 00 00 00` in all 461), since an adjacency entry of 0 means no portal.

`NavRegion` (`0x22` bytes, offsets from the start of the regions):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | vertexCount | 3 to 8; read by none of `0x00383F10`, the only reader of the region array |
| `+0x02` | `u16` | triangleCount | vertexCount - 2 in all 31,672 (`0x0038407C`, `0x003840E9`) |
| `+0x04` | `u16[8]` | vertex | the polygon, the first vertexCount used; read by none of `0x00383F10` |
| `+0x14` | `u16[6]` | triangle | the first triangleCount used (`0x003840A9`, with no bound but triangleCount) |
| `+0x20` | `u16` | word20 | 0 to 5; reached by `0x003840A9` only for a seventh triangle, which no region has |

The adjacency table is `regionCount * regionCount` u16 portal indices, `[from * regionCount + to]` (0x00383892,
0x00383392, 0x00383D1D, 0x0033D4E7).

`NavGrid` (`0x20` bytes, offsets from the start of the grid):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | cellW | the x divisor (`0x00384016`) and `0x00383740`'s extent (`0x003837CD`) |
| `+0x01` | `u8` | cellH | the z divisor (`0x00383FEC`), `0x00383805` |
| `+0x02` | `u8` | cols | `0x00383F99`, `0x00384003`, `0x003837BA` |
| `+0x03` | `u8` | rows | `0x00383FB5`, `0x003837F2` |
| `+0x04` | `i16` | originX | `0x00383F64`, `0x0038400E`, `0x0038377E` |
| `+0x06` | `i16` | originZ | `0x00383F7D`, `0x00383FDB`, `0x0038379C` |
| `+0x08` | `u32` | cellTable | cols * rows u16 pool offsets (`0x00383FD3`, `0x0038402C`); `0xFFFF` is an empty cell (`0x00384031`) |
| `+0x0C` | `u32` | listPool | `0xFF`-terminated u8 region lists (`0x00383F2E`, `0x0038404F`, `0x00384075`) |
| `+0x10` | `u8[16]` | pad | 0 in all; read by none of `0x00383F10` and `0x00383740`; the cell table follows at `+0x20` in all |

`NavTrailer` (`0x20` bytes, offsets from the start of the trailer):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | kind | zero-extended (`0x00392929`, `0x003915A3`); 0 a circle, 1 an ellipse, others skipped (`0x00392931`-`0x00392938`) |
| `+0x02` | `u16` | word02 | 0 in all; read by none of `0x00392740` and `0x00391410` |
| `+0x04` | `f32` | x | `0x00392950`, `0x003915B3`, `0x003915F9` |
| `+0x08` | `f32` | z | `0x0039294B`, `0x003915C6`, `0x00391616` |
| `+0x0C` | `f32` | radius | `0x00392946`, `0x003915D9`, `0x00391629` |
| `+0x10` | `f32` | radius2 | kind 1 only (`0x0039293F`, `0x003915E4`) |
| `+0x14` | `f32` | angle | kind 1 only, radians (`0x003915EF`; `0x00468580` divides it by -2 pi at `0x00468590`) |
| `+0x18` | `u8[8]` | tail | read by none of `0x00392740` and `0x00391410` |

A kind 0 record is tested as a circle of radius `+0x0C` (`0x00468D50` reads the centre and the radius `+0x10` of the
shape it is handed, `0x00468D87`-`0x00468D9F`); a kind 1 record as an ellipse of radii `+0x0C` and `+0x10` turned by
`+0x14` (`0x00468E50` through `0x00468580`).

In all 461 sections the arrays follow in the order header, vertices, triangles, portals, regions, adjacency, grid,
cell table, list pool, trailer; each starts on a multiple of 0x10, the gaps between them (2 to 16 bytes) are zero,
and the section ends zero-filled to a multiple of 0x40.

### YM00, the world data

`Ym00Header` (`0x14` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "YM00" |
| `+0x04` | `u8[4]` | stamp | an export value; read by none of `0x002F6AB0` (which starts at `+0x10`), the world-object builders `0x0026E760` and `0x0026E7D0` that hand it the section, or the pack walker `0x00378BC0`; nothing fixes its width |
| `+0x08` | `u8[8]` | author | an export tag; read by none of `0x002F6AB0` (which starts at `+0x10`), the world-object builders `0x0026E760` and `0x0026E7D0` that hand it the section, or the pack walker `0x00378BC0`; nothing fixes its width |
| `+0x10` | `u32` | count | 17 in all 461 sections; `0x002F6AB0` reads it at [base + `0x10`] |
| `+0x14` | `u32[]` | index | count + 1 entries of {u24 offset in 16-byte units from `+0x10`, u8 tag}; the last is the end sentinel with tag `0xFF` |

Before the walk `0x002F6AB0` sets `+0x120` to 1 and `+0x110` to 0, and clears the first 0x48 bytes of
the two 0x68-byte sub-records at `+0x40` and `+0xA8` with `0x00231F50`, nine qword stores of 0
(`0x002F6AEA`-`0x002F6B14`).

`0x002F6AB0(object, kind)` walks the index: an entry whose offset equals the next entry's is skipped,
otherwise its tag selects an arm (`cmp eax, 0x21`, a 34-case jump table). The arms that store or
parse a chunk:

| tag | what 0x002F6AB0 does with the chunk |
|---|---|
| 0 | `[+0x16C]` = first dword (a count), `[+0x188]` = chunk + 0x10: the 0x40-byte placement rows `0x002F5550` composes |
| 1 | `[+0x170]` = count, `[+0x190]` = chunk + 0x10, `[+0x1C8]` = an allocation of `count * 4` |
| 9 | `0x003ED3F0(chunk)`: the three 0x180-byte environment records at `0x02B5ED94` |
| 11 | `0x0026E8C0` stores it at `0x0209A660`; dword 0 to `0x022D8ED8` unless 0xFFFFFFFF; dword 1 unpacked by `0x00466140` into the colour `0x0209A3A0`-`0x0209A3AC` (scaled by 1/128); dwords 2 and 3 to `0x0209A6EC` and `0x0209A6F0` |
| 12 | `0x00468160(chunk, [+0x150], [+0x1B8])` |
| 14, 26 | `0x003EC910(6, 0x20, 0x00467D00)` then `0x00467D20(buffer, chunk)`; `[+0x150]` = buffer, `0x00467BF0(buffer, 0)` appends it to the buffer list at `0x02EBB6A0`; tag 26 also sets `[+0x230]` = 1 |
| 17, 31 | `0x00232380(object + 0xA8 or + 0x40, chunk)`: a six-tag sub-container into the two 0x68-byte sub-records, the collision parts (below) |
| 22 | `[+0x180]` = chunk |
| 23 | `0x00466E70(chunk)`: the map animation slots at `[0x02EBB6F0]` (below) |
| 24 | `[+0x220]` = count, `[+0x198]` = chunk + 0x10, `[+0x1D0]` = an allocation of `count * 0xE0` |
| 25 | `0x003ED190(chunk)`: field-dependent environment setup |
| 27 | `0x003ED840(chunk)` |
| 28, 29, 32 | `[+0x1A8]`, `[+0x1B0]`, `[+0x1B8]` = chunk (`0x002F6F09`, `0x002F6CF2`, `0x002F6F12`); arm 32 never runs on the shipped data, so `[+0x1B8]` keeps the 0 stored at `0x002F6BB9` |
| 30 | `[+0x174]` = count, `0x001806F0(count)`, `[+0x178]` = chunk + 0x10: the 0x30-byte instance records |
| 33 | `0x002F6740(object, chunk)`: the background NPC list, a count dword at chunk `+0` and 16-byte entries from chunk `+0x10`, kept at `[+0x1A0]` with the count at `[+0x22C]` (`0x002F6749`-`0x002F675C`); each entry's signed word `+0x00` is group × 100 + n, which `setbgnpcstatus` matches through `0x00379C50` and `0x00379BD0` (`0x00379C77`-`0x00379C9E`) |

Every shipped section carries exactly the 17 tags 0, 1, 11, 12, 17, 22 to 33 and the sentinel, so the
skipped tags 2 to 8, 10, 13, 15, 16 and 18 to 21 never occur. Five tags share their offset with the next
entry in some sections, and the walk skips them there (`0x002F6CAA`-`0x002F6CB7`): tag 32 in all 461 (it shares
tag 31's offset), tag 27 in 358 (tag 23's), tag 17 in 29 (tag 27's), tag 26 in 2 (tag 32's) and tag 31 in one,
`tst0108` (tag 17's).

The `chunk_bytes` column of
[`mpk-map-pack-ym00-chunks.tsv`](mpk-map-pack-ym00-chunks.tsv) counts to the next different offset, so the
rows of these entries show the next chunk's bytes; the parser gives them no bytes.

After the walk the constructor
allocates `count30 * 0x70` at `[+0x1C0]`, fills each entry from the tag-30 records (with bit `0x2000`
of the record's `+0xC`, the colour from its `+0x18` or, when that word is 0, from the tag-0 row through
the `+0x40` sub-record's transform, `0x00231A90`) and links the records that carry bit `0x40000000` of
their `+0xC` word to their tag-24 entry (`word +0x14`).

### The record arrays

Four chunks are arrays of fixed records after a 16-byte head whose first dword is the count; in every
shipped section the chunk is exactly 0x10 + count × the record size.

`Ym00TransformRow` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | row0 | first matrix row; `+0x0C` is 0.0 in all 390,136 rows |
| `+0x10` | `f32[3]` | row1 | second matrix row; `+0x1C` is 0.0 in all |
| `+0x20` | `f32[3]` | row2 | third matrix row; `+0x2C` is 0.0 in all |
| `+0x30` | `f32[3]` | position | read for the instance's distance at `0x002F6962`-`0x002F6979` and for its facing at `0x002F60D7`-`0x002F60FB`; `+0x3C` is 1.0 in all |

`0x002F5550` multiplies the row selected by an instance's `+0x02` into the instance's transform
(`0x002F5EEF`-`0x002F6022`, through `0x00202D70`).

`Ym00Switch` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | id | 1 to 692 in the shipped sections |
| `+0x04` | `u32[3]` | words04 | 0 in 659 of the 1,060 records |
| `+0x10` | `i32` | shownValue | copied into the per-frame cache [`+0x1C8`] (`0x002F6056`), which `0x002F5550` resets to -1 each frame unless [`+0x114`] is 1 (`0x002F5800`-`0x002F5832`) |
| `+0x14` | `i32` | word14 | the shown value + 1 in 118 records |
| `+0x18` | `i32` | word18 | -1 in 1,052 records, 48 or 51 in the others |
| `+0x1C` | `i32` | word1C | -1 in all |
| `+0x20` | `f32` | float20 | 30.0 in 767 records, 3.5 to 100.0 in the others |
| `+0x24` | `f32[3]` | floats24 | -1.0 in all three in 1,052 records; 7.0, -1.0, -1.0 in 8 |

`Ym00ClipGroup` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | kind | 1: the default near and far (`0x002F59AC`); 3: near and far from `+0x04` and `+0x08` (`0x002F5946`, `0x002F594B`); 0: the previous group's pair; stored at the group entry's `+0xC8` and `+0xCC` (`0x002F59BA`, `0x002F59CA`); kind 1 is also tested at `0x002F5219` and `0x002F6670` |
| `+0x04` | `f32` | near | 0.1 in 834 records, -1.0 in 1,150 |
| `+0x08` | `f32` | far | -1.0 in 927 records, 60.0 in 469 |
| `+0x0C` | `f32` | value | copied to the group entry's `+0xD0` (`0x002F6FB1`-`0x002F6FB6`); -1.0 in 4,182 records |

In every section group 0 is of kind 0 and group 1 of kind 1; the other 4,361 groups are of kind 3.

`Ym00Instance` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | piece | entry piece + 1 of the tag-22 chunk's offset table locates the geometry (`0x002F494B`-`0x002F4967`) |
| `+0x02` | `i16` | row | the tag-0 transform row (`0x002F5EEF`, `0x002F70C2`) and the tag-29 entry of that row ([`+0x1B0`]): its word `+0x00` files the instance as an attachment slot (`0x002F6527`-`0x002F6554`) and, with bit `0x40000000` of flags, its word `+0x02` names the background NPC whose fade entry gives the alpha (`0x002F4BD1`-`0x002F4BE0`, `0x002F5E8C`-`0x002F5E9B`); compared with a clip track's `+0x46` (`0x00466D4C`) |
| `+0x04` | `i16` | paletteId | the paletted texture pair bound to the instance (`0x002F5DDB`, `0x001807A0`); 0 to `0x3FFF` also index the texture-frame list [`+0x150`] (`0x002F49A6`, `0x002F74C0`) |
| `+0x06` | `i16` | switch | -1, or the tag-1 switch whose shown value decides the draw (`0x002F602C`-`0x002F6067`) |
| `+0x08` | `u16` | switchValue | the instance is drawn while it equals the switch's value (`0x002F605E`-`0x002F6067`); compared with a clip track's `+0x44` (`0x00466D90`) |
| `+0x0A` | `u16` | facing | 0 keeps the row's matrix; 1 to 4 select how the matrix is turned toward the view each frame (`0x002F5F07`, `0x002F6092`-`0x002F64F1`) |
| `+0x0C` | `u32` | flags | bits `0x2`, `0x4`, `0x8` draw mode (`0x002F4A95`-`0x002F4A9C`); `0x10`, `0x20` (`0x002F4B71`-`0x002F4B87`); `0x80` (`0x002F497D`); `0x100` (`0x002F4A82`); `0x200` (`0x002F4E03`); `0x400` (`0x002F4D43`); `0x1000` (`0x002F4A88`); `0x2000` colour (`0x002F703F`, `0x002F4ED1`); `0x4000` the draw list (`0x002F6FFE`, `0x002F606D`); `0x8000` (`0x002F4993`); `0x10000`, `0x20000` (`0x002F4971`); `0x10000000` sky piece (`0x002F4D3C`); `0x20000000` (`0x002F4A9F`); `0x40000000` fade slot and clip-group link (`0x002F4BC7`, `0x002F701D`) |
| `+0x10` | `u32` | word10 | 0 in all 764,018 records |
| `+0x14` | `u16` | clipGroup | the tag-24 group (`0x002F49B2`, `0x002F5E16`, `0x002F520A`, `0x002F6661`, `0x002F7025`) |
| `+0x16` | `u8` | byte16 | 20 in 725,633 records; 19 values from 3 to 120 |
| `+0x17` | `u8` | alpha | read at `0x002F49BD` for the draw's alpha (`0x002F4D93`-`0x002F4DC4`); 96 in 742,199 records, 128 in 14,472 |
| `+0x18` | `u32` | colour | with flags bit `0x2000`, a non-zero word unpacked by `0x00466140` into the instance colour (`0x002F7049`-`0x002F70A8`) |
| `+0x1C` | `u8` | maskBit | 1 to 254: drawn only while that bit of the active map-part mask (`0x0026E5F0`) is set (`0x002F4B8F`-`0x002F4BB5`), and the alpha is scaled from the table `0x02EBF278` (`0x002F4FD4`); 255 in 762,837 records |
| `+0x1D` | `u8` | byte1D | compared with the texture-slot argument at `0x002F74C5` and `0x002F74E0`; 0 in all |
| `+0x1E` | `u8` | biasA | the negated product of `+0x1E` and `+0x1F` goes to `0x00180890` (`0x002F4AA9`-`0x002F4AC5`) |
| `+0x1F` | `u8` | biasB |  |
| `+0x20` | `u64` | animGroups | bit n puts the instance in the clips of group n (`0x00466D07`-`0x00466D14`, from `0x002F57AC` and `0x002F7160`) |
| `+0x28` | `u64` | qword28 | 0 in all |

The tables beside this page list every record, each with the pack, the record's index and its offset in the
section:

- transforms, 390,136 rows: [part 1](mpk-map-pack-ym00-transforms-part1.tsv) and
  [part 2](mpk-map-pack-ym00-transforms-part2.tsv);
- [switches](mpk-map-pack-ym00-switches.tsv), 1,060 rows;
- [clip groups](mpk-map-pack-ym00-clip-groups.tsv), 5,283 rows;
- instances, 764,018 rows: [part 1](mpk-map-pack-ym00-instances-part1.tsv) and
  [part 2](mpk-map-pack-ym00-instances-part2.tsv).

`0x003ED190` (tag 25) also sends a light direction to the shadow object through `0x001F1590`, which
creates the 0xB08-byte shadow object kept at `0x01F82EA8` on first use (`0x001EF2D0`) and stores the direction
with `0x001F08A0`. The direction is (0.0001, 1, 0) in field `0x11A` (`0x003148F0`); otherwise the
vector at `+0x10` of the tag-11 chunk (`0x0209A660`) when it is non-zero; otherwise the three angles at
`+0x90` to `+0x98` of the tag-25 chunk, light 0 of its first weather record (`0x003ED269`), turned into a
direction, or x 0.0001 and y 1.0 when all three are 0.

`0x003ED3F0` (tag 9) also passes a direction to `0x001F1590`, the same (0.0001, 1, 0) in field `0x11A`.

The tag-28 chunk is published when a map binds: `0x003ED870`, called by `0x0026E960`, stores the world
object's `[+0x1A8]` at `0x02B5F1A8` when the chunk's first word is positive, and `0x003ED820` (from
`0x0026E640` and `0x0036F4D0`) clears `0x02B5F1A0`, `0x02B5F1A8` and `0x02B5F1B0`.

### Tag 23, the map animation slots

Tag 23 holds the map's animation clips: moving and turning map parts, colour pulses, texture frames
and the area's ambient colour. `0x00466E70(chunk)` builds one 0x50-byte slot per clip into an array at
`[0x02EBB6F0]` (count `0x02EBB6E0`, chunk `0x02EBB6F8`). The chunk is a count at `+0x10` and an offset
table from `+0x14` in 16-byte units from `+0x10`; slot `i` has a clip when entries `i` and `i + 1`
differ.

`MapAnimClip` (`0x30` bytes, offsets from the start of the clip):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[32]` | name | "ambient" makes the slot's `+0x34` = 0 |
| `+0x20` | `f32` | start | first frame (`0x00466C40`) |
| `+0x24` | `f32` | end | last frame (`0x00466BB0`) |
| `+0x28` | `i16` | count | with `+0x2C` 0, the target count (`0x00466F81`); otherwise the number of 16-byte map entries from `+0x30` (`0x00467374`, `0x004673AE`, `0x00467842`, `0x00466D26`) |
| `+0x2A` | `u16` | group | model group the clip belongs to (`0x004669F1`, `0x00466CF9`) |
| `+0x2C` | `i16` | mapTargets | 0, or the target count of a clip with map entries (`0x00466FBC`-`0x00466FC5`) |
| `+0x2E` | `u8` | flags | bit `0x1`: `0x02EBB6E4` = this slot (`0x00466F8E`) |
| `+0x2F` | `u8` | byte2F | 0 in all 3,344 shipped clips; read by none of `0x00466E70`, `0x004677A0`, `0x004668C0` and `0x00466CB0` |

After the clip header (and its map entries) comes a track list: a count and one offset per track,
again in 16-byte units. A track starts with its own header and then its keys:

`MapAnimTrack` (`0x20` bytes, offsets from the start of the track):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | keyCount |  |
| `+0x04` | `u32` | channel | the target field the track drives, read as a dword (`0x00467172`, `0x00467827`); `0x00466420` binds nothing for a value above 20 (`0x00466420`-`0x00466423`, unsigned), and `0xFFFFFFFF` is the value of 15,786 tracks of clips with map entries, whose map entry names the channel, and of 60 others |
| `+0x08` | `i16` | targetId | stored at the target's `+0x46` |
| `+0x0A` | `i16` | targetId2 | stored at the target's `+0x44` |
| `+0x0C` | `i32` | target | the target's index in the slot |
| `+0x10` | `f32[4]` | key0 | time, value, in-slope, out-slope; keyCount keys of 16 bytes from here |

`0x00466E70` allocates the slot's track records (0x18 bytes each: key data, time `+0x08`, value
`+0x0C`, key index `+0x10`) and its 0x130-byte targets, and sets bit `channel` of each target's
`+0x40`. It then binds the tracks (`0x004677A0`), resets the slots (`0x00467420`) and runs one update
(`0x004668C0`).

`MapAnimSlot` (`0x50` bytes, offsets from the start of the [0x02EBB6F0]+i*0x50):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | clip |  |
| `+0x08` | `void*` | clipActive | non-null for a live slot; every accessor tests it |
| `+0x10` | `void*` | mapEntries | when clip `+0x2C` is non-zero |
| `+0x18` | `void*` | trackList |  |
| `+0x20` | `void*` | tracks | `0x18` bytes each |
| `+0x28` | `void*` | targets | `0x130` bytes each |
| `+0x30` | `i16` | trackCount |  |
| `+0x32` | `i16` | targetCount |  |
| `+0x34` | `i16` | ambient | 0 for the clip named "ambient", else -1 |
| `+0x38` | `f32` | rate | 1.0 after a reset (`0x00467700` sets it, `0x004735D0` too) |
| `+0x3C` | `f32` | rangeStart | clamped to the clip's start (`0x00467660`) |
| `+0x40` | `f32` | rangeEnd | clamped to the clip's end |
| `+0x44` | `f32` | time |  |
| `+0x48` | `f32` | step | dt * rate, added each frame by `0x004678E0`, zeroed after the update |
| `+0x4C` | `u32` | flags | bit `0x1` playing, bit `0x2` loop, bit `0x4` finished, bit `0x8` update once, bit `0x10` relink |

`0x00466E70` gives every slot the loop bit and, when it has a clip, bits `0x1` and `0x10`. `0x00467420` resets
each live slot: the range becomes the clip's start and end, bit `0x4` is cleared and bit `0x8` set, the time
and every track's time become the start, the rate 1.0, and every target gets an identity matrix
(`0x00203170`), colour 1.0 at `+0x50` to `+0x5C`, rotation and translation 0 and scale 1.0.

`0x004677A0` binds each track's value to its target through `0x00466420(target, channel, &value)`;
with map entries, entry `+0x02` names the track, `+0x04` the channel and `+0x06` the target. The
channels are:

| Channel | Target field |
|---|---|
| 0 to 2 | translation `+0xE8`, `+0xF0`, `+0xF8` |
| 3 to 5 | rotation in degrees `+0xD0`, `+0xD8`, `+0xE0` |
| 6 to 8 | scale `+0x100`, `+0x108`, `+0x110` |
| 9 | `+0x90`, the texture frame the draw pass reads |
| 10, 11 | `+0x98`, `+0xA0` |
| 12, 13, 14 | colour red, green, blue `+0xB0`, `+0xB8`, `+0xC0`; 15 sets all three |
| 16 | `+0xA8`, which the draw pass scales by 0.01 |
| 17 | colour alpha `+0xC8` |
| 18 to 20 | rotation in radians `+0x118`, `+0x120`, `+0x128` |

Each world step `0x004668C0` (reached through the thunk at `0x0036F400`) advances every slot with bit `0x1` whose bit `0x8` is set or
whose step's absolute value exceeds 0.001 (`|+0x48| > 0.001`, `0x00466969`-`0x0046697B`):

1. bits `0x4` and `0x8` are cleared and the time moves by the step;
2. with `lo` = `+0x3C`, `hi` = `+0x40` and `span = hi - lo`, the loop bit and `span >= 1.0` the
   time `t` becomes `t - span` when `t >= hi` and `t + span` when `t < lo` (`0x004669A7`-`0x004669CA`);
   otherwise `t >= hi` stores `hi`, `t < lo` stores `lo`, and either sets bit `0x4` (finished)
   (`0x004669D1`-`0x004669EA`);
3. unless the clip's group is above 0x100 with its bit in the hidden-model set (`0x0026E5F0`),
   `0x00466240` advances each track and `0x00466550` rebuilds each target;
4. the step is zeroed.

`0x00466240(slot, track)` sets the track's time `t = t + step` for the slot's step, and with
`lo = max(+0x3C, first key time)`, `hi = min(+0x40, last key time)` and `span = hi - lo`
(`0x00466251`-`0x0046629E`) checks only the side it moves toward: for a step above 0, `t >= hi` stores
`t - span` (loop bit and `span >= 1.0`, key index 0) or `hi`; for a step of 0 or less, `t < lo`
stores `t + span` (key index the last) or `lo` (`0x004662A2`-`0x004662F6`).

`0x00466240` then finds the key pair around the time and interpolates with a cubic Hermite curve (each key's value, the first key's out-slope and the second
key's in-slope) into the track's value. The slopes are per unit of time: with u = (t - t0) / (t1 - t0),
the value is h00(u) v0 + h01(u) v1 + (t1 - t0) (h10(u) out0 + h11(u) in1).

`0x00466550(slot, target)` reads the bound channels: translation into `+0x70` to `+0x78`, degrees
turned into radians and wrapped into `+0x60` to `+0x68` (the radian channels overwrite them), scale
into `+0x80` to `+0x88`. It rebuilds the target's matrix at `+0x00` from the three rotations, each
applied only when it is not 0 (`0x00202E90`, `0x00202F00`, `0x00202F70`), and the translation, scales its four rows by `+0x80` to `+0x8C`
(`0x00202FE0`) and, for the `ambient` slot, copies the colour `+0x50` to `+0x5C` to `0x0209A370` to
`0x0209A37C`, the ambient colour of the map's lights.

The slot accessors take a slot number and test it against `0x02EBB6E0` and `+0x08`:

- `0x00466C80(slot)` returns the time `+0x44` (0 for a bad slot) and `0x00466AD0(slot)` the finished bit `0x4` (1 for a bad
  slot, the test `0x004735E0` of the actor-control table uses);
- `0x00473490(slot)` returns the time less the clip's start (`0x00466C40`), the verb `getbganimeframe` (`0x0AD`,
  `0x0034FEE3`); `0x004734C0(slot)` returns the clip's end (`0x00466BB0`) less its start, `getbganimelastframe` (`0x0AE`,
  `0x00350393`);
- `0x00467730(slot, t)` seeks: it clears bit `0x4`, sets bit `0x8`, stores `t` as the time of the slot and of every track and
  zeroes the step and each track's `+0x10`; the rewind `0x00473500`, called by `bganimeplay` (`0x09D`, `0x003477B0`),
  `bganimeplay_9e` (`0x09E`, `0x00347CD0`) ([verb table](../Scripts-And-Script-Commands/verb-table.md)), `0x003E8440`,
  `0x003E8690` and `0x003E8990`, and `0x00466DD0` use it;
- `0x00466DD0()` sends every playing slot that does not loop and has a non-zero rate to its range end and marks it
  finished; it runs from the script skip's start `0x00360710` and end `0x00360A50`, and from `0x003486A0` and `0x00355300`.

The draw code reaches targets through the tag-30 instances. `0x00466CB0(slot, idB, idA, mask)`
returns the slot's first target when the clip's group is below 0x100 and its bit is in the
instance's group mask, else the target whose `+0x46` (or map entry `+0x00`) equals `idB`, else the
one whose `+0x44` equals `idA`. `0x002F6AB0` and `0x002F5550` call it with the instance record's `+0x02`
and `+0x08` words and its group mask `+0x20`.

When a slot's bit `0x10` is set, `0x002F5550` clears it and
stores the target in each matching instance's 0x70-byte entry at `+0x50` while the slot plays
(`0x00466B80`, bit `0x1`), or 0 when it does not.

### Tag 23 in the shipped data

`MapAnimChunk` (`0x14` bytes, offsets from the start of the chunk):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | word00 | non-zero in all 461; read by none of `0x00466E70`, which starts at `+0x10`, or of `0x004668C0`, `0x00466DD0` and `0x004678E0`, which only test the chunk pointer `0x02EBB6F8` |
| `+0x04` | `u8[12]` | pad | 0 in all 461; read by none of the same |
| `+0x10` | `u32` | count | the slot count (`0x00466EA9`); 0 in 26 sections |
| `+0x14` | `u32[]` | index | count + 1 entries of {u24 offset in 16-byte units from `+0x10`, u8 `0xFF`} (`0x00466F45`-`0x00466F75`); the last is the chunk's end in all 435 sections with slots |

`MapAnimMap` (`0x10` bytes, offsets from the start of the clip+0x30+i*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | idB | compared with the instance's row word by `0x00466CB0` (`0x00466D58`) |
| `+0x02` | `i16` | track | the track the entry binds (`0x00467854`) |
| `+0x04` | `i16` | channel | the target field (`0x00467392`, `0x00467868`) |
| `+0x06` | `i16` | target | the target index (`0x0046738C`, `0x0046785E`) |
| `+0x08` | `u8[8]` | tail | `0xFF` in all 80,317 entries; read by none of `0x00466E70`, `0x004677A0` and `0x00466CB0` |

The track list follows the map entries: a dword count (`0x00466FE5`) and one `{u24 offset, u8 0xFF}` per track in
16-byte units from the list's start (`0x00467110`-`0x00467123`). Each clip's last key ends where the next index entry
starts, in all 3,344 clips. Key times rise within every track.

A key is `{f32 time, f32 value, f32 inSlope,
f32 outSlope}`: `0x00466240` reads the time (`0x00466383`), the value (`0x00466369`, `0x004663A4`), the second key's in-slope
(`0x004663D4`) and the first key's out-slope (`0x004663EB`). No shipped clip is named `ambient`, so `0x00466550` never
copies a colour to `0x0209A370` from this chunk.

### Tag 11, the view settings

`0x0026E8C0` keeps the chunk at `0x0209A660`; `0x002F6AB0` copies its first four dwords (`0x002F6DE9`-`0x002F6E6F`).

`Ym00ViewSettings` (`0x80` bytes, offsets from the start of the chunk):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | colourWord | stored at `0x022D8ED8` unless it is `0xFFFFFFFF` (`0x002F6DF1`-`0x002F6E03`); while it is `0xFFFFFFFF`, `0x003ECE60` stores the blended fog colour there each frame (`0x003ECF31`-`0x003ECF4E`); `0xFFFFFFFF` in 63 sections |
| `+0x04` | `u32` | colour | unpacked by `0x00466140` into `0x0209A3A0` to `0x0209A3A8`, each byte / 128 (`0x002F6E09`-`0x002F6E53`) |
| `+0x08` | `f32` | viewNear | stored at `0x0209A6EC` (`0x002F6E5B`), which the camera views `0x00259990`, `0x00259A90`, `0x0025A2C0` and `0x0025A3D0` return with the far value (`0x00259A63`-`0x00259A77`) and `0x002F5550` reads (`0x002F55EA`); `0x0026E1D0` resets it to 0.1; 0.1 in 448 sections, 0.3 in 12, 0.2 in 1 |
| `+0x0C` | `f32` | viewFar | stored at `0x0209A6F0` (`0x002F6E69`), read by the same views, `0x002F5550` (`0x002F55D9`) and `0x0026E0F0`; `0x0026E1D0` resets it to 1000.0; 43 values, 1000.0 in 252 |
| `+0x10` | `f32[3]` | direction | handed to the shadow object when any is non-zero by `0x003ED190` (`0x003ED217`-`0x003ED24A`, `0x003ED371`) and `0x003ED3F0` (`0x003ED4E6`-`0x003ED51D`); with `+0x1C`, stored at `0x02B3F560` by `0x00378120` (`0x003781E6`, `0x003AFD40`) |
| `+0x1C` | `f32` | flag | tested non-zero by `0x00378120` (`0x003781E0`); 1.0 in the 102 sections with a direction, 0 in the other 359 |
| `+0x20` | `u8[96]` | pad | 0 in all 461; read by none of `0x002F6AB0`, `0x00378120`, `0x003ECCA0`, `0x003ECE60`, `0x003ED190` and `0x003ED3F0`, the readers of `0x0209A660` |

### Tag 12, the palette animations

`0x00468160(chunk, [+0x150], [+0x1B8])` walks the chunk (the map art page has its palette buffer). The third argument
is the tag-32 pointer, never set on the shipped data (above); only a kind-4 record would read it (`0x00468360`-`0x004683A3`),
and no shipped record is of kind 4.

`PalAnimChunk` (`0x4` bytes, offsets from the start of the chunk):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | count | group count (`0x0046818F`); 0 in 373 sections, 1 to 4 in the other 88 |
| `+0x04` | `u32[]` | index | count + 1 entries of {u24 offset in 16-byte units from the chunk start, u8}; the byte is 0, and `0xFF` for the last entry, which is the chunk's end (`0x004681C0`-`0x004681CE`, `0x00468260`-`0x00468272`); `0xFF` bytes pad the table to 16 bytes |

`PalAnimGroup` (`0x10` bytes, offsets from the start of the chunk+offset*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | recordCount | the `0x30`-byte records from `+0x10` (`0x00468279`; `0x004681CE` adds them up); 1, 3 or 5 |
| `+0x04` | `i32` | texture | the texture of the tag-14 buffer [`+0x150`], `0x60` bytes each (`0x00468275`, `0x0046829A`) |
| `+0x08` | `i32` | slot | the texture's palette slot that takes the new palette handle (`0x0046827D`, `0x004682EB`); 0 in all 134 groups |
| `+0x0C` | `u32` | pad | 0 in all; read by none of `0x00468160` |

Each record is copied to `+0x10` of a `0x40`-byte entry of `[0x02CA6010]` (`0x00468345`-`0x00468357`) and filed by `0x003CCC20`,
which copies its 0x30 bytes into a palette operation (`0x003CCC7E`-`0x003CCC93`) that `0x003CCF20` runs each step (the
model-files page has the operation record).

`PalAnimRecord` (`0x30` bytes, offsets from the start of the group+0x10+i*0x30):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | kind | the operation `0x003CCF20` runs (`0x003CD0E6`-`0x003CD101`): 1 `0x0050AC20`, 2 `0x00506B40`, 7 `0x00508C90`; 4 makes `0x00468160` build a second palette (`0x0046835B`); 1 in 92 records, 2 in 45, 7 in 5 |
| `+0x01` | `u8` | byte01 | 0 in all; read by none of `0x00468160`, `0x003CCC20`, `0x003CCF20`, `0x0050AC20`, `0x00506B40` and `0x00508C90` |
| `+0x02` | `u8` | priority | the operation's place in the palette's list (`0x003CCE94`-`0x003CCEA0`) |
| `+0x03` | `u8` | flags | read by `0x0050AC20` (`0x0050AC71`), `0x00506B40` (`0x00506B98`) and `0x00508C90` (`0x00508EA6`); 15 in 131 records |
| `+0x04` | `u32` | palette | 0 in the file; `0x00468160` stores the palette handle `0x003CCB60` returned (`0x004683CA`), and `0x003CCC20` files the operation on that palette (`0x003CCE42`-`0x003CCE59`) |
| `+0x08` | `u16` | length | steps until the operation ends, 0 for no length (`0x003CCFFA`-`0x003CD007`); 0 in all |
| `+0x0A` | `i16` | delay | counted down before the operation runs (`0x003CCFD0`-`0x003CCFEE`); `0x003CCC20` adds a random part (`0x003CCE2E`); 10 in 2 records |
| `+0x0C` | `i16` | delaySpread | the random part's size (`0x003CCC97`, `0x003CCD74`); 10 in 1 record |
| `+0x0E` | `u16` | rateDivisor | the phase is divided by it when non-zero (`0x0050AC51`, `0x00506B4F`, `0x00508CA9`) |
| `+0x10` | `u16` | period | `0x003CD07A`, `0x003CD0B9` |
| `+0x12` | `u16` | word12 | `0x0050ACFD`, `0x00506C0D`, `0x00508EFF` |
| `+0x14` | `u8` | byte14 | `0x0050AD14`, `0x00506C01`, `0x00508F12` |
| `+0x15` | `u8` | mode | 0 wrap, 1 back and forth (`0x003CD085`-`0x003CD08D`); 1 in 51 records |
| `+0x16` | `u8[10]` | pad16 | 0 in all; read by none of the readers above |
| `+0x20` | `u8[11]` | params | kind 1: i16 `+0x20` (`0x0050AC75`), u8 `+0x22` (`0x0050ACD5`); kind 2: i16 `+0x20`, `+0x22`, `+0x24`, `+0x26` (`0x00506BF5`-`0x00506C25`), u16 `+0x28` (`0x00506B80`), u8 `+0x2A` (`0x00506BDA`); kind 7: i32 `+0x20` (`0x00508CEA`), i16 `+0x24` (`0x00508CD2`), u8 `+0x26` (`0x00508EAB`); kind 4: `+0x20` indexes the third argument's table (`0x00468360`) |
| `+0x2B` | `u8[5]` | pad2B | 0 in all; read by none of the readers above |

### Tag 25, the environment of each weather slot

`0x003ED190(chunk)` keeps the chunk at `0x02EBB7F0` and sets `0x02EBB808` (`0x003ED1CE`, `0x003ED1D5`). The chunk is three
0x180-byte records, record `n` for weather slot `n + 1`: the readers index it by `[0x0209A6E8] - 1`
(`0x003ECD0F`-`0x003ECD36`, `0x003ECFDC`-`0x003ECFEB`, `0x003ED034`-`0x003ED051`, `0x003ED0BC`-`0x003ED0CB`, `0x003ED14C`-`0x003ED15B`), and
`0x003ED7B0` by `slot - 1` from `0x0026E8D0`.

`Ym00Environment` (`0x180` bytes, offsets from the start of the chunk+n*0x180):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i32` | fogCount | fog entries from `+0x10` (`0x003ECD39`); `0x003ED190` copies entry 0 of record 0 only when it is positive (`0x003ED3A3`); 0 to 4 |
| `+0x004` | `i32` | lightCount | stored at `0x0209A2D0` (`0x003ED0CF`, `0x0026E8F6`), the lights `0x00379630` files |
| `+0x008` | `f32` | scale | returned by `0x003ED140` (`0x003ED15F`) and stored at `0x01EFE314` by `0x003B6BA0`, which `0x003B62D0` reads (`0x003B6504`); 1.0 in 1,336 records |
| `+0x00C` | `u32` | word0C | 0 in all 1,383; read by none of `0x003ECCA0`, `0x003ECFD0`, `0x003ED020`, `0x003ED0B0`, `0x003ED140`, `0x003ED190`, `0x003ED3F0` and `0x003ED7B0`, the readers of `0x02EBB7F0` |
| `+0x010` | `u8[128]` | fog | four Ym00Fog entries of `0x20` bytes, below |
| `+0x090` | `u8[96]` | lights | three entries of `0x20` bytes, each an f32[4] of angles and then an f32[4] vector, copied to light i's `+0x10` and `+0x20` at `0x0209A2E0` (`0x003ED054`-`0x003ED0A5`, the weather page); record 0's light 0 angles also turn into the shadow direction (`0x003ED269`) |
| `+0x0F0` | `f32[4]` | ambient | copied to `0x0209A370` to `0x0209A37C` (`0x003ECFEF`-`0x003ED017`) |
| `+0x100` | `u8[128]` | tail | 0 in all 1,383; read by none of the readers of `0x02EBB7F0` |

`Ym00Fog` (`0x20` bytes, offsets from the start of the record+0x10+i*0x20):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | near | `0x003ECAC0` blends it into `0x02EBB7C4` (`0x003ECAF0`, `0x003ECB18`); entry 0 is the base, copied to `0x02EBB7F8` (`0x003ED7C7`, `0x003ED3B5`) |
| `+0x04` | `i32` | far | blended into `0x02EBB7C8` (`0x003ECAF5`, `0x003ECB1C`); entry 0 to `0x02EBB7FC` (`0x003ED7D1`); `0x003ED0E0` turns the published pair into 255 / (far - near) and far (`0x003ED0E0`-`0x003ED12B`) |
| `+0x08` | `i32` | enable | an entry from 1 on blends by direction only when it is not negative (`0x003ECD98`); -1 in 1,286 of the 1,359 counted entries |
| `+0x0C` | `u32` | colour | blended byte by byte through `0x00466140` (`0x003ECBAA`); entry 0 to `0x02EBB804` (`0x003ED7DB`) |
| `+0x10` | `f32[3]` | dir | the blend weight is (1 - dir . [`0x02AEDF10`]) x 0.5 (`0x003ECDA6`-`0x003ECDDF`) |
| `+0x1C` | `u32` | mask | the float 1.0 or a low byte of `0xFF` blends by direction (`0x003ECD70`-`0x003ECD82`); another low byte is a bit of `0x0026E5F0`'s set: set skips the entry, clear makes it the entry blended last with the weight `0x02EBF278`[byte] (`0x003ECD84`-`0x003ECE37`); `0xFF` in 1,329 of the 1,359 counted entries |

`0x003ECCA0`, each frame from `0x0036F530`, starts from entry 0 of the current slot and blends entries 1 on; `0x003ECAC0`
copies an entry whose weight is above 0.996 and blends one whose weight is above 1/256 (`0x003ECAE4`-`0x003ECB0D`).

### Tag 27

`0x003ED840(chunk, length)` is handed the chunk and its length in 16-byte units (`edx`, set at `0x002F6CB5`). It keeps the
chunk at `0x02B5F1A0` and, when the length passes the last index entry, the bytes from there at `0x02B5F1B0`
(`0x003ED840`-`0x003ED865`); `0x003ED820` clears both (`0x003ED823`, `0x003ED82E`). No RIP-relative reference reads
`0x02B5F1A0` or `0x02B5F1B0`, and no 8-byte data pointer holds either address.

`Ym00Tag27` (`0x4` bytes, offsets from the start of the chunk):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | read by `0x003ED840` (`0x003ED840`); 1 to 27 in the 103 sections that apply the tag, 529 entries in all |
| `+0x04` | `u32[]` | index | count + 1 entries of {u24 offset in 16-byte units from the chunk start, u8 `0xFF`}; `0x003ED840` reads the last (`0x003ED844`) |

### Tag 28

`Ym00Tag28` (`0x10` bytes, offsets from the start of the chunk):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | count | 0 in all 461. With a positive count `0x002F6AB0` would allocate ((count + 7) / 8) x 2 bytes at [`+0x210`] (`0x002F727E`-`0x002F72A9`) and `0x003ED870` would publish the chunk at `0x02B5F1A8` (`0x003ED881`-`0x003ED88F`) |
| `+0x04` | `u8[12]` | pad | `0xFF` in all 461 |

### Tag 29, a word pair per transform row

The chunk holds one 16-byte entry per tag-0 transform row, from its first byte (in all 461 sections the chunk is
16 × the tag-0 count), and the readers index it by the instance's row word.

`Ym00RowLink` (`0x10` bytes, offsets from the start of the chunk+row*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | attachSlot | 0 to 31: `0x002F5550` stores the instance's number at `0x0209A71C` + 2 x slot (`0x002F6527`-`0x002F6554`), which `0x003A6FC0` reads (`0x003A6FDA`) to hand `0x003A4290` and `0x003A56F0` the instance; -1 no slot; set in 710 entries of 126 sections |
| `+0x02` | `i16` | bgNpc | with instance flag `0x40000000`, the tag-33 entry whose fade entry [`+0x1D8`] gives the alpha (`0x002F4BE0`, `0x002F4C0D`; `0x002F5E9B`, `0x002F5EC6`); -1 no entry; set in 36,463 entries of 43 sections, each below its section's tag-33 count |
| `+0x04` | `u8[12]` | pad | 0 in all 390,136; read by none of `0x002F4520` and `0x002F5550`, the readers of [`+0x1B0`] |

### Tag 33, the background NPCs

`Ym00BgNpc` (`0x10` bytes, offsets from the start of the chunk+0x10+i*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` | id | group x 100 + n, matched by `0x00379C50` (`0x00379C77`) and `0x00379BD0` (`0x00379BF7`) |
| `+0x02` | `i16` | row | the tag-0 transform row placing it (`0x002307C8`, `0x0032A6FE`); below the section's row count in all |
| `+0x04` | `i16` | sizeA | / 4096 (`0x00908E30`): the first radius of the obstacle-grid shape (`0x0032A70E`, `0x0032A752`) and a body extent (`0x002307F2`) |
| `+0x06` | `i16` | sizeB | / 4096: the second radius (`0x0032A717`, `0x0032A757`) and a body extent (`0x002307FB`) |
| `+0x08` | `i16` | sizeC | / 4096: stored with the others at `0x022D91B0` (`0x0032A720`, `0x00230804`) |
| `+0x0A` | `u8[6]` | tail | read by none of `0x00230790`, `0x0032A6E0`, `0x00379BD0` and `0x00379C50`; the last two bytes are `0xFF` in all 1,506 |

The chunk head is the count (`0x002F6749`) and 12 zero bytes. `0x002F6740` gives each entry a 12-byte state at
`[+0x1D8]` (`0x002F6773`-`0x002F67A6`): `+0x00` shown, 1 at the start, set to 1 by `0x00379C50` (`0x00379CA7`) and to 0 by
`0x00379BD0` (`0x00379C27`), read by `0x0022D7E0` (`0x0022D8DE`) and `0x0032A6C0` (`0x0032A6D5`); `+0x08` the alpha, 1.0 at the
start, read by `0x002F4520` (`0x002F4C0D`) and `0x002F5550` (`0x002F5ECD`). `0x0022D7E0` passes a shown entry to `0x00230790`
(`0x0022D8F1`-`0x0022D8FB`), and the obstacle grid's registry reads the list through `0x0032A6B0`, `0x0032A6C0` and `0x0032A6E0`.

### Tags 31 and 17, the two collision parts

Tag 31 is the map's collision part, the one bodies walk on and are swept against ([collision-mesh
movement](../Movement-And-Pathfinding/collision-mesh-movement.md)); tag 17 is a second part with the same
layout. `0x00232380(part, chunk)` fills the 0x68-byte part at `+0x40` (tag 31, `0x002F6DB7`) or `+0xA8` (tag 17,
`0x002F6DC8`).

`0x0026E960` keeps each part whose grid pointer is set at `0x0209A678` and `0x0209A680`, and copies the
grid's two sets of the `+0x40` part only (`0x0026E9D3`-`0x0026E9EA`). `0x0026E500(0)` returns the `+0x40` part and any
other argument the `+0xA8` part (`0x0026E50A`-`0x0026E520`). `0x00322220` keeps the `+0xA8` part, or the `+0x40` part when
there is no `+0xA8` part, at `0x02EC1378` (`0x0032222B`-`0x00322265`), and the ray casts `0x00318CA0` and `0x0032A4D0` cast
through it (`0x002315E0`, the walker `0x0022F430` with the callback `0x0022D4B0`).

Tag 32 shares tag 31's offset and comes before it in the index of all 461 sections, so `0x002F6AB0` skips it
(`0x002F6CB5`-`0x002F6CB7`) and its arm, `[+0x1B8]` = chunk (`0x002F6F12`), never runs. Tag 17 is skipped the same way in
29 sections, where it shares tag 27's offset, and tag 31 in one, `tst0108`, where 31, 17 and 27 share one offset: in
that section neither part is filled, and both keep the zeroes `0x002F6AB0` cleared them to (`0x002F6AFB`-`0x002F6B14`).

`CollChunk` (`0x20` bytes, offsets from the start of the chunk):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | 6 in all 892 parsed chunks; `0x00232380` walks count entries (`0x00232391`, `0x0023244B`) |
| `+0x04` | `u32[6]` | index | {u24 offset in 16-byte units from the chunk start, u8 sub-tag}: `0x00232380` masks the offset (`0x002323B3`-`0x002323C4`) and switches on the sub-tag (`0x002323C7`-`0x002323D9`, 0 to 5, a table at `0x00232470`); the order is 0, 1, 2, 5, 3, 4 in all |
| `+0x1C` | `u32` | end | {the chunk's length in 16-byte units, `0xFF`}; read by none of `0x00232380`, which stops at count; the grid follows at `+0x20` in all |

`0x00232380` does not skip equal offsets: an empty sub-chunk still stores its pointer.

`CollGrid` (`0x40` bytes, offsets from the start of the chunk+0x20):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | x0 | originX = cols * cellW / 2 - x0, a signed halving (`0x002323DE`-`0x00232400`) |
| `+0x04` | `i32` | z0 | originZ = rows * cellH / 2 - z0 (`0x002323EC`-`0x0023240F`) |
| `+0x08` | `i32` | cols | the column bound of the cell lookup `0x00233050` (`0x002330A7`) and of `0x0022E340` (`0x0022E4F5` for rows); `0x00232380` multiplies it (`0x002323E2`) |
| `+0x0C` | `i32` | rows | the row bound (`0x002330B0`, `0x0022E4F5`) |
| `+0x10` | `i32` | cellW | the column divide (`0x00233086`, `0x0022E4C6`) and the cell rectangle (`0x00231E51`) |
| `+0x14` | `i32` | cellH | the row divide and the half-row stagger of odd columns (`0x00233091`, `0x002330A1`, `0x00231E71`) |
| `+0x18` | `i32` | cells | cols * rows in all 892; stored at the part's `+0x40` (`0x00232413`), the bank stride minus one |
| `+0x1C` | `u32` | word1C | 0 in all |
| `+0x20` | `u32` | poolSlots | the id pool's length rounded up to 8 entries in all; read by none of `0x00232380`, `0x00233050`, `0x0022E340`, `0x00231E40`, `0x0022F430`, `0x0022FFE0`, `0x00230C10`, `0x002327D0` and `0x0026E960` |
| `+0x24` | `u32` | polygonCount | the polygon count in all 892; read by none of the same |
| `+0x28` | `f32` | float28 | read by none of the same |
| `+0x2C` | `f32` | float2C | read by none of the same |
| `+0x30` | `u64` | hiddenModels | the part's hidden model set, copied to `0x0209A690` for the `+0x40` part (`0x0026E9D8`); non-zero in 116 tag-31 grids, 0 in every tag-17 grid |
| `+0x38` | `u64` | hiddenEffects | the hidden effect set, copied to `0x0209A6A8` (`0x0026E9E6`); non-zero in 41 tag-31 grids |

Sub-tag 1 is four banks of `cells + 1` `u16` list starts into the id pool, sub-tag 2 (`[part + 0x28]`). A cell's
list in bank `k` runs from entry `k (cells + 1) + cell` to the next (`0x0022F855`-`0x0022F890`); each bank's last entry is
the next bank's first, and the first is 0, in all 892. In the shipped parts bank 0 lists the type-0 polygons (floors),
bank 1 the type-1 polygons, the wall records (`0x4000` + index) and, in 43 tag-31 parts, background NPC shapes (`0x5000` +
index, each below its section's tag-33 count), bank 2 nothing, and bank 3 the polygons of types 2, 3 and 4 (tag 31 only).

`CollVertex` (`0x10` bytes, offsets from the start of the [part+0x08]+i*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | position | x, y, z: the plane height `0x00231890` (`0x002318CD`, `0x002318E7`, `0x002318C2`) and the inside test `0x002324F0` |
| `+0x0C` | `u8[3]` | colour | red, green, blue, blended by the barycentric weights over 128 into the body colour (`0x00231A90`, `0x00231CBA`-`0x00231DD6`) |
| `+0x0F` | `u8` | fade | the camera region's fade weight over 255 (`0x0022FF10`, `0x0022FF59`); 255 in 462,896 vertices, 0 in 2,364 |

`CollPolygon` (`0x20` bytes, offsets from the start of the [part+0x10]+i*0x20):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | normal | the plane normal (`0x00231890`, `0x002318AC`-`0x002318DB`; `0x0022D7E0`, `0x0022DABF`-`0x0022DADB`) |
| `+0x0C` | `u32` | attr | the attribute word ([doors, gates and map changes](doors-gates-and-map-changes.md)); type bits `0x7` tested by `0x00230A40` (`0x00230A61`), `0x0022D7E0` (`0x0022DA70`-`0x0022DA79`) and `0x00231900` (`0x002319E5`) |
| `+0x10` | `i16[3]` | vertex | vertex indices, sign-extended (`0x00231890` at `0x002318A7`, `0x00231A90` at `0x00231CAE`, `0x00231D19`, `0x00231D86`, `0x0022E7D0` at `0x0022E848`) |
| `+0x16` | `i16[3]` | neighbour | the polygon across each edge, -1 for no neighbour (`0x0022F9B0` from `0x0022FB00`, `0x0022EAC0` at `0x0022ECFD`); -1 for all three in every tag-17 polygon |
| `+0x1C` | `u32` | flags | bit `0x400` is tested by `0x0022E7D0` (`0x0022E93B`) and `0x0022EAC0` (`0x0022ECA2`): past the third edge there is no contact; set in 16,458 polygons; bits `0x3FF` carry values 0 to `0x3FF` that neither reads, and bits above `0x400` are 0 in all 754,558 |

`CollWallChunk` (`0x10` bytes, offsets from the start of the chunk+[sub-tag):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | stored at the part's `+0x44` (`0x0023242F`-`0x0023243A`) |
| `+0x04` | `u8[12]` | pad | 0 in all; the records start at `+0x10`, stored at the part's `+0x18` (`0x00232432`, `0x00232436`) |

`CollWall` (`0x90` bytes, offsets from the start of the [part+0x18]+i*0x90):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | type | 0 sphere, 1 cylinder, 2 box (`0x00380FA0` at `0x00380FE5`); id `0x4000` + i (`0x0022D907`-`0x0022D914`) |
| `+0x04` | `u32` | attr | the attribute word (`0x0022D91E`, `0x0022CCF8`, `0x0022F936`); type 1 in all 89,330 |
| `+0x08` | `u32[2]` | words08 | export bytes (pointers and text in some); read by none of `0x00380FA0`, `0x00381D90`, `0x003810B0`, `0x0022D7E0`, `0x0022DE60`, `0x0022CC50`, `0x0022D4B0` and `0x0022F8B0` |
| `+0x10` | `f32[16]` | forward | unit frame to world (`0x00380FA0` from `0x0038103E`, `0x00381D90` from `0x00381E7E`) |
| `+0x50` | `f32[16]` | inverse | world to unit frame (`0x00380FA0` from `0x00380FD7`, `0x00381D90` from `0x00381DAD`, `0x003810B0` from `0x003810F3`) |

`CollisionPart` (`0x68` bytes, offsets from the start of the object+0x40):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | grid | sub-tag 0 (`0x002323DB`); a null grid leaves the part unbound (`0x0026E9CE`) |
| `+0x08` | `void*` | vertices | sub-tag 5 (`0x00232440`) |
| `+0x10` | `void*` | polygons | sub-tag 3 (`0x00232429`) |
| `+0x18` | `void*` | walls | sub-tag 4 + `0x10` (`0x00232436`) |
| `+0x20` | `void*` | listIndex | sub-tag 1 (`0x0023241D`) |
| `+0x28` | `void*` | idPool | sub-tag 2 (`0x00232423`) |
| `+0x30` | `i32` | spanX | cols * cellW (`0x002323E7`); read by none of `0x00233050`, `0x0022E340`, `0x00231E40`, `0x0022F830`, `0x002327D0`, `0x0022FFE0`, `0x00230C10`, `0x0022D7E0`, `0x0022DE60`, `0x0022CC50`, `0x0022D4B0`, `0x0022F8B0`, `0x00233230`, `0x00233110`, `0x00231900`, `0x00231A90` and `0x0022F430` |
| `+0x34` | `i32` | spanZ | rows * cellH (`0x002323F9`); read by none of the same |
| `+0x38` | `i32` | originX | (`0x00232400`); added to x by `0x00233050` (`0x00233050`) |
| `+0x3C` | `i32` | originZ | (`0x0023240F`); added to z by `0x00233050` (`0x00233059`) |
| `+0x40` | `i32` | cells | (`0x00232417`); read as the i16 bank stride minus one by `0x0022F830` (`0x0022F855`) |
| `+0x44` | `i32` | wallCount | (`0x0023243A`); read by none of the same |
| `+0x48` | `u64[4]` | frameSets | zeroed by `0x00232380` (`0x0023245E`-`0x0023246A`); the shown and hidden sets of the frame (doors page) |

### ACTL, the actor-control table

`ActlHeader` (`0x10` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "ACTL" |
| `+0x04` | `u16` | version | must be 1: `0x003E8940` clears the pointer otherwise |
| `+0x06` | `u16` | recordSize | `0x16` in all 270 sections; `0x003E8230` and the two walkers advance by it |
| `+0x08` | `u16` | idBound | `0x003E8230` refuses an id at or above it |
| `+0x0A` | `u8[2]` | reserved | 0; read by none of `0x003E8230`, `0x003E7EC0`, `0x003E8D50` and `0x003E8940`; nothing fixes its width |
| `+0x0C` | `u16` | indexOffset | `0x10`: the bucket index {u16 bucketCount; {u16 bound, u16 recordOffset}[bucketCount]} |
| `+0x0E` | `u16` | auxOffset | the aux table `0x003E7EC0` and `0x003E8D50` pass to the record handlers |

`0x003E8230(id)` returns the record of an id:

- bucket = `id / 100`, slot = `id % 100`;
- a miss when the id reaches `idBound`, the bucket reaches `bucketCount` or the slot reaches the
  bucket's bound;
- a hit is `section + recordOffset[bucket] + slot * recordSize`;
- the three bounds are signed compares (`0x003E8246`, `0x003E826D`, `0x003E827E`) and the division `id / 100` truncates
  toward zero: `b = hi32(id × 0x51EB851F) >> 5`, plus 1 when that is negative (`imul r9d`, `sar edx, 5`,
  `shr eax, 0x1f`, `add edx, eax`), and `slot = id - 100 × b` (`0x003E8252`-`0x003E8260`, `0x003E8262`-`0x003E8265`);
- a negative id is therefore not a miss: ids -1 to -99 give bucket 0 and a
  negative slot, addressing records before the bucket's first, and lower ids a negative bucket, reading
  `recordOffset` before its table.

`0x003E8230` answers 0 while no table is published (`[0x02B5D080]` null, `0x003E823D`). Its comparisons are signed: the id
is compared as a signed integer (`0x003E8244`) and `bucketCount` and the bucket's bound are read as `i16` (`0x003E8268`,
`0x003E8276`), so a negative id is not refused. An id of -1 to -99 gives bucket 0 and a negative slot, and the answer
lies that many records before the bucket's first record (`0x003E824D`-`0x003E8291`).

`0x003E7EC0` and `0x003E8D50(mode)` walk every bucket's records in the same arithmetic and hand each to
`0x003E8020` or `0x003E8C50` with the aux table and the weather slot (`0x00265920`); `0x003E8D50` skips
records whose byte `+0x15` differs from a non-negative mode.

`0x003E8940(section)` first runs `0x003E8D50(-1)` (`0x003E894C`), which walks the table still published at `0x02B5D080`
(`0x003E8D5F`) and hands every record to `0x003E8C50`, as a negative mode skips no record. It then stores the new section
(`0x003E8951`) and, when that is non-null with a version other than 1, stores 0 instead (`0x003E895D`-`0x003E8968`). The
teardown's `0x003E8940(0)` therefore runs that walk over the outgoing table and leaves the pointer 0.

`0x003E8020` keeps the record's state in its first word: bit `0x1` processed (set on first touch, when the
low nibbles of bytes `+0x13` and `+0x14` are copied into their high nibbles and the high nibble of
`+0x12` becomes 3), bit `0x2` the alternator, bits `0x4` and `0x8` an override, bit `0x10` "was active". A first word
of 0xFFFF is a tombstone that every walker skips.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | state | the state bits above |
| `+0x02` | `i16` | animation | map animation slot, -1 for no slot (`0x004735D0` sets its rate) |
| `+0x08` | `i16` | light | `LGT2` light id, -1 for no light; bit `0x4000` routes it through the aux table (`0x003E8190`) |
| `+0x0E` | `i16` | effect | map effect channel, -1 for no channel |
| `+0x10` | `i16` | sound | map sound emitter below 1000 |
| `+0x12` | `u8` | mode | high nibble 0 runs `0x003E8440`, 1 runs the test `0x003E8350` |
| `+0x13` | `u8` | gate | a non-zero high nibble skips the mode step |
| `+0x14` | `u8` | soundMode | the high nibble feeds `0x00363A90` |
| `+0x15` | `i8` | effectArg | third argument of `0x0026FAD0`, negatives as 0; the walker's mode filter |

On first touch `0x003E8020` runs `0x003E8990`, which clears state bits `0x8` and `0x10`, rewinds the animation
slot (`0x00473500(slot, -1.0, -1.0)`), sets its rate to 0 (`0x004735D0`) and sets the sound emitter's
flags with `0x00363A90`. A toggle with bit `0x2` clear runs `0x003E85B0` and sets the bit; with bit `0x2` set it
runs `0x003E8690` and clears it:

- `0x003E85B0` sets the animation slot's rate to 0, turns the light's loop off and stops its animation
  (`0x0037A310`, `0x0037A130`, or `0x003E8A10` and `0x003E8A40` through the aux table), starts the effect
  channel (`0x0026FAD0`) and clears its flag (`0x002700F0(channel, 0)`), and sets bit `0x4` of the sound
  emitter's flag byte (`0x00363AD0(id, 1)`);
- `0x003E8690` sets the rate to 1.0, resets, turns on and restarts the light (`0x0037A270`, `0x0037B190`,
  `0x0037A1D0`, `0x0037A310`), sets the channel's flags (`0x002700F0`, `0x00270130`) and starts it, and
  clears the emitter's bit `0x4`.

In mode 1 `0x003E8020` sets state bit `0x10` when `0x003E8350` finds that `0x004735E0` (the animation slot), `0x0037B030` (the light,
or the callback `0x003E82A0` through the aux table) and `0x00362E30` (the emitter's bit `0x1`) all return 0
and `0x0026FDB0` does not return 2 for the channel.

`0x003E8350` answers 1 at once, before any of those tests, while state bit `0x10` is already set
(`0x003E8368`-`0x003E83AA`). Otherwise it answers for the first source still running: 2 for the animation slot, 8 for
the light, 4 for the channel and `0x10` for the emitter (`0x003E83A5`, `0x003E83DA`, `0x003E83FA`, `0x003E8419`), and 0
when no source is.

### SP1, the sound emitters

`Sp1Header` (`0x20` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "SP1" |
| `+0x04` | `u32` | listOffset | `0x20` in all 456 sections: `0x00363B40` reads the weather-slot list here when the SPP1 list is absent |
| `+0x08` | `u32` | areasOffset | the listener grid `0x00362E50` searches |
| `+0x0C` | `u32` | indexOffset | {u16 bound; u16 recordOffset[]}: the emitter index `0x00362850` passes to `0x003631B0` |
| `+0x10` | `u32` | emittersOffset | a u16 prefix list terminated by bit `0x8000`, then the emitter records |
| `+0x14` | `u32` | reserved14 | 0 |
| `+0x18` | `u16` | reserved18 | 0 |
| `+0x1A` | `u16` | reserved1A | 0 |
| `+0x1C` | `u32` | reserved1C | 0 |

`0x003631B0(listener, list, index, current)` walks a list of index entries, resolves each through the
index into a record at `0x022CBAF0 + recordOffset`, dispatches on the record's shape byte `+9`
(`& 0x7F`: 0, 1, 2, other), evaluates the volume through `0x00361810` and starts or updates the voice
through `0x003638B0`. The emitter record itself is on the map sound list page.

A null list returns `current` at once (`0x003631CA`). An entry's low 15 bits are its index; an index at or above the
index table's `u16` bound is skipped (`0x00363244`-`0x00363251`), and the entry with bit `0x8000` set is the last one
walked (`0x00363352`-`0x0036335C`).

With `shape = record[+9] & 0x7F` (`0x0036326A`-`0x0036326E`), shapes 0 and 1 clamp the
listener's position with `0x00361DE0` and `0x003623C0`, shape 2 with `0x00362230`, whose return value also goes to
`0x00361810`, and any other shape uses the position as it is (`0x0036326A`-`0x003632CC`). The ellipse, the rectangle and
the segment chain are written out as expressions in
[Geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md#the-volume-clamps).

`0x00361810` gets, with `[0x022CBA8C]`, the record's `+0x38`, `+0x54` and `+0x58` for shapes 0 and 1, `+0x38`, 0 and
4.1415930 for shape 2, and -1.0, 0 and 4.1415930 for the other shapes (`0x003632D1`-`0x00363320`).
`0x003638B0(record, the two values 0x00361810 wrote, current, &position)` runs for every walked entry (`0x00363344`).
`current` takes its return only when the distance `0x00361810` returned is exactly 0.0 (`0x00361B9A`,
`0x00363349`-`0x00363350`), and the
walk returns `current` (`0x00363367`).

`0x00363B40` builds the per-weather-slot ambient list from the `SPP1` section's `u16 +0x1A` offset
when it is non-zero, which it is in all 545 shipped lists, else from this header's `+4` list; the
current slot (`0x00265920`) picks the entry.

### LGT2, the light set

`0x0037AA90(block, group)` accepts the block when its first dword is `LGT2` (`0x3254474C`) and stores
it in group `group` (0 to 4) of the `0x50`-byte group table at `0x02EBF420`. It walks the chunk chain
at `block + u16[+4]` (`{u16 size, u16 kind}` chunks, kinds 0 to 3 and 5 to 7 stored to the group's
slots) and remaps a byte of each of the `u16[+0xA]` 0x70-byte records through `0x01EF94E4`. The
section's own format is on the section-014 page.

The group is compared unsigned, so a negative group returns at once like one above 4 (`0x0037AA9E`-`0x0037AAA2`), and
the block is read with no null test (`0x0037AABF`). A block with another magic stores nothing but still sets the
group's ready byte `+0x4C` (`0x0037AAC5`, `0x0037AC69`). The remapped byte is record `+0x21`, and only its values below 6
change (`0x0037AC16`-`0x0037AC29`); in group 0 each record's `+0x27` also gets bit `0x20` (`0x0037AC3A`-`0x0037AC62`).

### TIM2 pictures and NPS2 placements

`0x003C63A0(picture)` registers picture 0 as a texture (`0x0024A480(picture, "navi_Load", 2, …, 0x200)`)
and keeps its width and height (`u16 +0x14` and `+0x16` of the texture header) at `0x02B457F8` and
`0x02B457FC`.

It first releases the texture it holds at `0x02B457F0` with `0x0024A680(texture, 0)` and zeroes the pointer
(`0x003C63A9`-`0x003C63BC`); a null picture stops there (`0x003C63CA`), which is how `0x003C63A0(0)` drops the minimap
texture. The fourth argument of the registration is `0x0035D530()` (`0x003C63CC`-`0x003C63EC`); the new texture goes to
`0x02B457F0` (`0x003C63F1`) and its header `[texture + 0x20]` is read with no null test (`0x003C63F8`-`0x003C640E`).

`0x00379870(i)` applies placement `i`:

`Nps2Placement` (`0x40` bytes, offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[3]` | magic | "NPS" |
| `+0x03` | `u8` |  | version "2" in all 577 shipped records; `0x00379870` treats "1" as a 256 x 256 picture |
| `+0x04` | `u8[12]` | pad | zero |
| `+0x10` | `f32` | x | world position of the picture (`0x00379870` -> `0x003C6360`) |
| `+0x14` | `f32` | y |  |
| `+0x18` | `f32` | width | picture extent (`0x00379870` -> `0x003C6380`), read for every version byte other than "1" (`0x003798AE`) |
| `+0x1C` | `f32` | height |  |
| `+0x20` | `u8[32]` | pad2 | zero |

`0x00379870` hands `0x003C6380` the placement's width and height cut to whole numbers (`0x003798DA`, `0x003798DE`), and
`0x003C6380` keeps them as floats at `0x02B45808` and `0x02B4580C` (`0x003C638E`, `0x003C6396`), beside the position
`0x02B45800` and `0x02B45804` that `0x003C6360` stores.

`0x00379870` reads `0x02ADD030 + 8i` with no bound on `i` (`0x00379874`-`0x00379888`). A null placement gives the position
(0, 0) and 256 x 256 (`0x003798C4`-`0x003798D2`). The version byte `0x31` ("1") keeps the position and uses 256 x 256
(`0x00379891`-`0x003798A7`); any other version byte takes the width and height at `+0x18` and `+0x1C`
(`0x003798AE`-`0x003798B3`). The position goes to `0x003C6360` (`0x003798D5`) and the size to `0x003C6380` by a tail jump
(`0x003798F0`).

### WD and MRP, carried but unread

Slot 1 is a wave bank: a `WD` magic, `u16 +2` bank id (46 distinct values, 0x1FA to 0x251), `u32 +4`
trailing data size (its start is 0x40-aligned), `u32 +8` and `+0xC` record counts (equal in all 46),
`u32 +0x14` flags (0, 0x8000 or 0x10000), an offset table of `count` dwords at `+0x20` with a record
stride of 0x20. `0x00378BC0` frees the slot in both modes (`0x00378DBA`, `0x00378E19`), so nothing reads it.

Slot 15 is an `MRP` relocated-pointer package (the menu resource package page). The pointer
`0x02ADD058` has four references: the store (`0x00378F04`), the teardown (`0x003782EB`, `0x003782FC`) and the
getter `0x00377B90`, whose only caller is `initgauge` (`0x0034DC70`). That verb passes it to `0x003E9020`,
which passes it as a 32-bit integer to `0x00408300`, where it becomes the second create parameter of
the gauge task `0x00406E80`. Only two packs, `rwg0201` and `rwg0202`, carry the slot, with identical
bytes.

## Shipped data

| quantity | value |
|---|---|
| packs | 550; count 32 and a 0xC0 header in every one; the sizes sum to the file length in every one |
| packs a field names | all 550. The 1,315 `map_ref.bin` rows name 531 distinct indices as a field's own pack (the row's first word, `0x00264F10`) and 93 as a block pack (the first word of the row's 16-byte block record, `0x00264F40`). 461 of the 531 and 89 of the 93 are pack files, 550 in all with no pack serving both; the other 70 and 4 indices name no file ([`mpk-map-pack-map-ref-field-packs.tsv`](mpk-map-pack-map-ref-field-packs.tsv)). Each pack is kind 4's entry for its id, and all twelve size tables give that entry the file's size |
| slots used | 0 (545), 1 (46), 4 (461), 8 (461), 9 (270), 10 (545), 13 (387), 15 (2), 16 (456), 17 (212), 24 to 27 (421, 136, 32, 17), 28 to 31 (396, 133, 31, 17) |
| navigation headers | 461 sections, word `+0x00` 1 and `+0x2C` 0 in all; 116 distinct region counts, the largest 128. [`mpk-map-pack-nav-header-rows.tsv`](mpk-map-pack-nav-header-rows.tsv) has each header's counts and offsets, the zero gap bytes and the zero bytes after the last array |
| navigation vertices | 94,143. [`mpk-map-pack-nav-vertices-rows.tsv`](mpk-map-pack-nav-vertices-rows.tsv) has each x and z |
| navigation triangles | 115,719, every one listed back by its region. [`mpk-map-pack-nav-triangles-rows.tsv`](mpk-map-pack-nav-triangles-rows.tsv) has the three vertices and the region |
| navigation portals | 52,635 records: the padding record 0 of each section and 52,174 portals; gate 0xFF in 51,248 and 0 in 926, under 30 map ids; the ungated ones carry map id 0, except 4 with 12 and 1 with 1; class masks `0x2F` 32,467, `0x08` 19,374, `0x00` 324, `0x0C` 8, `0x2B` 1; byte `+7` 0 in all. [`mpk-map-pack-nav-portals-rows.tsv`](mpk-map-pack-nav-portals-rows.tsv) has each record and how many adjacency entries name it (51,540 two, 634 one) |
| navigation regions | 31,672 polygons of 3 to 8 vertices (392, 6,567, 7,981, 8,672, 4,798, 3,262), each split into vertex count - 2 triangles whose vertices are exactly the polygon's; `+0x20` is 0 in 24,790, 5 in 5,596, 2 in 638, 1 in 589, 3 in 45 and 4 in 14. [`mpk-map-pack-nav-regions-rows.tsv`](mpk-map-pack-nav-regions-rows.tsv) has each region's vertices, triangles and `+0x20` word |
| navigation adjacency | 103,714 non-zero entries, 0 on the diagonal; 103,080 have the same portal back, and 317 region pairs in 15 packs name a different record each way over the same edge, which differ in class mask, gate or map id (305 of them `0x00` one way and `0x08` the other). [`mpk-map-pack-nav-adjacency-rows.tsv`](mpk-map-pack-nav-adjacency-rows.tsv) has each entry with the portal back |
| navigation grids | cells 5 x 5 in all 461; bytes `+0x10` to `+0x1F` zero and the cell table at `+0x20` in all. [`mpk-map-pack-nav-grid-rows.tsv`](mpk-map-pack-nav-grid-rows.tsv) has each grid header |
| navigation grid cells | 270,341 cells, no cell holding 0xFFFF; 124,432 point at an empty list, the others at 1 to 14 regions. [`mpk-map-pack-nav-grid-cells-rows.tsv`](mpk-map-pack-nav-grid-cells-rows.tsv) has each cell's column, row, pool offset and regions |
| navigation obstacles | 240 trailer records in 28 sections, at most 32 per section (32 in `rbl0128`): 130 circles (kind 0) and 110 ellipses (kind 1, the second radius differing from the first in all, the angle 0 in 91). [`mpk-map-pack-nav-trailer-rows.tsv`](mpk-map-pack-nav-trailer-rows.tsv) has each record, with the unread bytes `+0x10` to `+0x17` of the circles and `+0x18` to `+0x1F` of all |
| commonest slot sets | {0, 4, 8, 10, 13, 16, 24, 28} 113 packs; with 9 added 48; with 9 and 17 48; with 9, 17, 25, 29 47; {0, 1, 10} 46; {0, 10} 41 |
| block packs | the 89 `<area>00` packs: 46 carry {0, 1, 10}, 41 {0, 10}, 2 nothing; no other pack is sound-only |
| YM00 | 461 sections, median 2.9 MB; count 17 and the same 17 tags, in the same index order, in every one; 441 stamps are float-shaped values between 1 and 1000. [`mpk-map-pack-ym00-chunks.tsv`](mpk-map-pack-ym00-chunks.tsv) has the 8,298 index entries: pack, the section's file offset, entry, tag, the chunk's offset in the section and its bytes (to the next chunk start), its first dword and its SHA-256; the sentinel's row has no bytes. The records of tags 0, 1, 24 and 30 are listed in [`mpk-map-pack-ym00-transforms-part1.tsv`](mpk-map-pack-ym00-transforms-part1.tsv) and [part 2](mpk-map-pack-ym00-transforms-part2.tsv), [`mpk-map-pack-ym00-switches.tsv`](mpk-map-pack-ym00-switches.tsv), [`mpk-map-pack-ym00-clip-groups.tsv`](mpk-map-pack-ym00-clip-groups.tsv), and [`mpk-map-pack-ym00-instances-part1.tsv`](mpk-map-pack-ym00-instances-part1.tsv) and [part 2](mpk-map-pack-ym00-instances-part2.tsv) |
| YM00 tag 11 | 461 chunks of 0x80 bytes; view near 0.1 in 448, far 43 values (1000.0 in 252); the colour word 0xFFFFFFFF in 63; a direction in 102; bytes `+0x20` to `+0x7F` zero in all. [`mpk-map-pack-ym00-tag11-rows.tsv`](mpk-map-pack-ym00-tag11-rows.tsv) has each chunk's fields by the layout above, with the pack and the section's file offset first in this and the following tables |
| YM00 tag 12 | 142 palette-animation records in 134 groups of 88 sections (373 sections have no record): kind 1 in 92, 2 in 45, 7 in 5; palette slot 0 in all groups. [`mpk-map-pack-ym00-tag12-rows.tsv`](mpk-map-pack-ym00-tag12-rows.tsv) has each record with its group's texture and slot |
| YM00 tag 23 clips | 4,356 slots in 435 sections (26 have no slot): 3,344 clips with 2,583 names, not one `ambient`, and 1,012 empty slots; 321 clips with map entries; flag bit `0x1` in 12. [`mpk-map-pack-ym00-tag23-clips-rows.tsv`](mpk-map-pack-ym00-tag23-clips-rows.tsv) has each slot's clip header, target, map-entry and track counts |
| YM00 tag 23 map entries | 80,317 in 321 clips, bytes `+0x08` to `+0x0F` 0xFF in all. [`mpk-map-pack-ym00-tag23-maps-rows.tsv`](mpk-map-pack-ym00-tag23-maps-rows.tsv) has each entry |
| YM00 tag 23 tracks | 49,016; channel 0xFFFFFFFF in 15,846, then 11 (6,553), 10 (6,150), 16 (3,988), 17 (3,648) and 1 (3,118); every target index below the clip's target count. [`mpk-map-pack-ym00-tag23-tracks-rows.tsv`](mpk-map-pack-ym00-tag23-tracks-rows.tsv) has each track's header and its first and last key times |
| YM00 tag 23 keys | 411,419, in rising time within every track. [`mpk-map-pack-ym00-tag23-keys-rows.tsv`](mpk-map-pack-ym00-tag23-keys-rows.tsv) has each key's time, value and two slopes |
| YM00 tag 25 | 1,383 records, three per section; fog counts 0 (118), 1 (1,193), 2 (57), 3 (8), 4 (7); light counts 0 (579), 1 (499), 2 (275), 3 (30); `+0x0C` and `+0x100` to `+0x17F` zero in all. [`mpk-map-pack-ym00-tag25-rows.tsv`](mpk-map-pack-ym00-tag25-rows.tsv) has each record's counts, scale and ambient colour |
| YM00 tag 25 fog | 5,532 entries, four per record, 1,359 of them counted. [`mpk-map-pack-ym00-tag25-fog-rows.tsv`](mpk-map-pack-ym00-tag25-fog-rows.tsv) has each entry, counted or not |
| YM00 tag 25 lights | 4,149 entries, three per record, 1,139 of them counted; the uncounted ones are zero. [`mpk-map-pack-ym00-tag25-lights-rows.tsv`](mpk-map-pack-ym00-tag25-lights-rows.tsv) has each light's angles and vector |
| YM00 tag 27 | applied in 103 sections (skipped in 358): 529 entries, 1,555,904 bytes, and 16 to 64 bytes after the last entry in all 103. [`mpk-map-pack-ym00-tag27-rows.tsv`](mpk-map-pack-ym00-tag27-rows.tsv) has each entry and that tail with its size, first dword and SHA-256 prefix |
| YM00 tag 28 | 461 chunks of 16 bytes, count 0 and twelve 0xFF bytes in all. [`mpk-map-pack-ym00-tag28-rows.tsv`](mpk-map-pack-ym00-tag28-rows.tsv) has each chunk |
| YM00 tag 29 | 390,136 entries, one per transform row in every section; attachment slots 0 to 31 in 710 entries of 126 sections; a background NPC in 36,463 entries of 43 sections; bytes `+0x04` to `+0x0F` zero in all. [`mpk-map-pack-ym00-tag29-rows.tsv`](mpk-map-pack-ym00-tag29-rows.tsv) has each entry |
| YM00 tag 33 | 1,506 background NPCs in 43 sections (418 have no background NPC), in groups 1 to 49. [`mpk-map-pack-ym00-tag33-rows.tsv`](mpk-map-pack-ym00-tag33-rows.tsv) has each entry's id, group and number, row, the three sizes raw and / 4096, and its unread bytes |
| collision parts (YM00 tags 17, 31, 32) | 1,383 index entries: tag 31 parsed in 460 sections and skipped in 1 (`tst0108`), tag 17 parsed in 432 and skipped in 29, tag 32 skipped in all 461; the 432 sections with both parts parse different bytes for them. [`mpk-map-pack-ym00-coll-rows.tsv`](mpk-map-pack-ym00-coll-rows.tsv) has every entry: pack, section offset, tag, entry, chunk offset, whether it is parsed, the part it fills, the six sub-chunk offsets and the grid fields; cell sizes are 8 × 8 in 808 parts, 2 × 2 in 58, 4 × 4 in 18, 12 × 12 in 4, 3 × 3 in 2 and 4 × 2 in 2 |
| collision cells | 666,892 cells (391,364 in tag 31, 275,528 in tag 17), listing 5,283,962 ids: bank 0 3,199,306 polygons of type 0, bank 1 467,325 type-1 polygons, 540,679 wall records and 4,713 background NPC shapes, bank 2 empty, bank 3 1,071,939 polygons of types 2 (338,709), 3 (692,843) and 4 (40,387). [part 1](mpk-map-pack-ym00-coll-cells-rows-part1.tsv) and [part 2](mpk-map-pack-ym00-coll-cells-rows-part2.tsv) have every cell: pack, section offset, tag, cell, column, row, and for each bank its list start, count and ids |
| collision vertices | 468,899 (416,863 in tag 31). [`mpk-map-pack-ym00-coll-vertices-rows.tsv`](mpk-map-pack-ym00-coll-vertices-rows.tsv) has each vertex's position, colour bytes and fade byte |
| collision polygons | 754,558: tag 31 678,091 of types 0 (560,139), 1 (70,612), 2 (33,194), 3 (10,623) and 4 (3,523); tag 17 76,467 of types 0 (75,962) and 1 (505), not one with a neighbour. Flag bit `0x400` is set in 16,458. [Part 1](mpk-map-pack-ym00-coll-polygons-rows-part1.tsv) and [part 2](mpk-map-pack-ym00-coll-polygons-rows-part2.tsv) have each polygon's normal, attribute word and type, vertices, neighbours and flag word |
| collision wall records | 89,330 (60,145 in tag 31: 2,657 spheres, 6,034 cylinders, 51,454 boxes; 29,185 in tag 17: 3,356, 3,608 and 22,221). [`mpk-map-pack-ym00-coll-walls-rows.tsv`](mpk-map-pack-ym00-coll-walls-rows.tsv) has each record's type, attribute word, the two words at `+0x08`, and both transforms |
| ACTL | 270 sections, 64 to 1,792 bytes; version 1 and record size 0x16 in all; the index ends where the first record begins and the records end at the aux offset in all 270; 1,822 records, 101 of them tombstones. [`mpk-map-pack-actl-rows.tsv`](mpk-map-pack-actl-rows.tsv) has every record: pack, section offset, id (bucket × 100 + slot), bucket, slot, record offset, tombstone, then the record's fields by the layout above |
| SP1 | 456 sections, 704 to 9,792 bytes; `listOffset` (`+0x04`) 0x20 in all; the three regions tile areas, emitters, index in 454 (two sections have no emitter index). [`mpk-map-pack-sp1-rows.tsv`](mpk-map-pack-sp1-rows.tsv) has each section's header offsets, its weather-slot list, the `u16` prefix list up to the bit `0x8000` word, the index bound and its distinct records; [`mpk-map-pack-sp1-index.tsv`](mpk-map-pack-sp1-index.tsv) every index entry (14,272, of which 11,946 are 0); [`mpk-map-pack-sp1-emitters.tsv`](mpk-map-pack-sp1-emitters.tsv) every distinct non-zero record offset (2,326) with its bytes up to the next record or the index, its list index (`+0x00`), flag byte (`+0x08`), shape byte (`+0x09`) and position (`+0x20` to `+0x28`) as the map sound list page reads them |
| SPP1 | 545 lists of 1 to 48 ids, 624 distinct; the weather-table offset `+0x1A` is non-zero in all 545, with 1, 2 or 3 entries in 189, 130 and 226 tables. [`mpk-map-pack-spp1-rows.tsv`](mpk-map-pack-spp1-rows.tsv) has each list's header and weather table; [`mpk-map-pack-spp1-ids.tsv`](mpk-map-pack-spp1-ids.tsv) its 6,512 id entries, each with its bank |
| TIM2 and NPS2 | one picture per section (`u16 +6` = 1); 577 placements, all version "2". [`mpk-map-pack-tim2-rows.tsv`](mpk-map-pack-tim2-rows.tsv) has each picture's header fields and the SHA-256 of its data; [`mpk-map-pack-nps2-rows.tsv`](mpk-map-pack-nps2-rows.tsv) each placement's position and extent |
| WD | 46 sections, all in `<area>00` packs; record stride 0x20 in the 27 with more than one record. [`mpk-map-pack-wd-rows.tsv`](mpk-map-pack-wd-rows.tsv) has each header and where its trailing data starts; [`mpk-map-pack-wd-records.tsv`](mpk-map-pack-wd-records.tsv) the 225 records' 0x20 bytes |
| LGT2 | 212 sections; `+0x08` is 0 in all 212 and the chunk chain carries types 3 and 5 in all, 6 in 211, 0 in 198, 2 in 123 and 7 in 20. [`mpk-map-pack-lgt2-rows.tsv`](mpk-map-pack-lgt2-rows.tsv) has each header and its chunk types; [`mpk-map-pack-lgt2-lights.tsv`](mpk-map-pack-lgt2-lights.tsv) the 5,860 light records by the section-014 layout, with their bytes; [`mpk-map-pack-lgt2-chunks.tsv`](mpk-map-pack-lgt2-chunks.tsv) the 976 chunks with their entries |
| lights per weather | which lamps and fill lights each map shows in each weather. [`mpk-map-pack-lgt2-lit-by-slot.tsv`](mpk-map-pack-lgt2-lit-by-slot.tsv) has 957 rows, one per weather slot for each of the 319 maps of [`weather-maps.tsv`](weather-maps.tsv) whose own pack carries a section: how the slot occurs (`by the roll` on 327 rows, `only when set by the script` on 35, and `no: chance 0 and no setup script sets it` on 595), the records light group 0 lists on entry, their light kinds and script ids, and the cut lit on entry. The other 389 maps carry no section. The listed records differ between slots in 13 maps, 3 of them between slots that occur, all by the roll. In 16 of the 20 sections with type-7 sets a type-0 range is present too, and that range is listed in every slot |
| layers per field | What each map shows, collides with, walks on, triggers, lights and plays, and which of its two packs supplies it. The 89 block packs carry only slots 0, 1 and 10 (above), so in the 1,315 fields the own pack supplies the models drawn (`YM00` tag 30), the collision part (tag 31, which `0x002F6AB0` puts at `+0x40` of the mode-1 world object; [Doors, gates and map changes](doors-gates-and-map-changes.md)), the navigation dataset, the `ACTL` records, the `LGT2` lights and the `SP1` sound emitters, and the block pack supplies the sound-effect bank and the map sound list (slots 0 and 10, kept in mode 0). [`mpk-map-pack-field-layers.tsv`](mpk-map-pack-field-layers.tsv) has one row per field, 0 to 1,314: its zone script, its own and block pack, and for each layer the pack with its count (tag-30 instances, the tag-31 chunk's bytes, the navigation section's bytes, `ACTL` records that are not tombstones, `LGT2` light records, `SP1` emitter records, `SPP1` ids); `-` marks a field without that script, pack or layer. The pack names follow the path the read takes for each kind-4 index ([Asset paths](../Game-Files-And-Data-Tables/asset-paths.md)), one file per index; 1,194 fields have an own pack file and 1,281 a block pack file, and an index without a file is sized -1 and not requested (`0x00378062`). The 708 fields with a zone script all have world data and navigation; 389 of them have no `LGT2` section, 206 no `ACTL` section, 6 no `SP1` section and 4 no map sound list. When both packs carry one of slots 9, 15, 16 and 17, the own pack's section is the one bound: the block pack is requested first and the read queue completes requests in order ([File requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md)), and each completion stores the four slots without a test (`0x00378E9D`, `0x00378EC1`, `0x00378EE2`, `0x00378F04`) and then runs the binder (`0x00378F39`) |
| every section | one row each in [`mpk-map-pack-slots-rows.tsv`](mpk-map-pack-slots-rows.tsv), 4,568 rows for the 550 packs: pack, folder, slot, the section's file offset and size, its first bytes, SHA-256 prefix, and whether the 0x40-byte slot before it is zero (it is in all 4,568) |

## Loader behaviour

### Two requests per field

`0x00331990(field)` requests the block pack in mode 0 and the field's own pack in mode 1 through
`0x00378A60(field, index, mode)`:

1. Mode 0 returns at once when `0x02ADD0E0` is non-negative and equals `0x02ADD0DC`
   (`0x00378AD6`-`0x00378AE6`); its own index is not compared. Otherwise `0x00378230(1)` tears the
   previous packs down (when no load is pending, `0x0032F3D0(0)`) and `0x003784A0` releases the sound
   sections. So the bound block pack is kept only while one is bound and the last mode-1 index
   was 0:
   - `0x02ADD0E0` only ever holds -1 or 0: -1 from the loader reset (`0x00377D29`) and from `0x003784A0`
     when it releases a bound block pack (`0x003784C9`), otherwise the copy of `0x02ADD0E4` that
     `0x00378120` makes when it binds the pending block pack (`0x00378175`-`0x0037817B`), and nothing
     writes `0x02ADD0E4`.
   - `0x02ADD0DC` is written only by mode 1 (`0x00378AC9`).
   - `0x0032F3D0(0)` always answers 0: it answers 0 when `[0x02B62DAB]` is 1 or `[0x02B62DA8]` is 3 (`0x00408B30`,
     `0x00408B10`), and otherwise 1 only when `0x005C5230(4)` is non-zero, which it never is (`0x0032F3D8`-`0x0032F41F`).
     So `0x00378230(1)` runs on every mode-0 call that gets past the first test (`0x00378AE8`-`0x00378AF5`).
2. Mode 1 drops the minimap texture (`0x003C63A0(0)`, `0x00378AA4`), stores the index at `0x02ADD0DC` and tears down
   with `0x00378230(releaseWorld)` (`0x00378AC9`, `0x00378ACF`). The argument is 0, keeping the mode-1 world object, only
   when `0x0032F3D0(0)` answers non-zero, the index equals the previous `0x02ADD0DC` and `0x02ADD0EA` is clear
   (`0x00378AA9`-`0x00378AC3`). `0x0032F3D0(0)` always answers 0, so mode 1 always passes 1 and the world object is
   released.
3. When no load is pending, `0x00377DC0` requests the loose effect bank `PS2Data\efb\<zone>.efb`
   (completions `0x003788F0` in mode 1 to `0x02ADD050`, `0x003789A0` in mode 0 to `0x02ADD098`, bind bits
   `0x20` and `0x40`) and `0x00378030` requests the pack: `0x0032E400(4, index)` sizes it, `0x0036A190` allocates an
   arena block tagged `MapNo`, and `0x0032E620` submits the load with the completion `0x00378BC0` and
   the argument `block | mode`.
4. Mode 1 names the scene from the pack's path (`0x00379A10(4, index)`, with five alias pairs at
   `0x01EF9490`), which `0x001805D0` receives.

Every call of `0x00378A60` first zeroes `0x02EBF9C8` and `0x02ADD0F4` and sets `0x02ADD118` to 1 (`0x00378A82`-`0x00378A95`),
so the early return of step 1 still makes those stores. Any non-zero mode takes the mode-1 steps (`0x00378A9D`). Step 3
tests `0x0032F3D0(0)` again (`0x00378B01`); a non-zero answer, which it never gives, skips both requests through the
return stub `0x0016D6A0` (`0x00378B0A`-`0x00378B14`). Step 4 runs either way, and `0x00377DC0` gets the argument
step 2 passed to `0x00378230` as its last argument, 1 in mode 0 (`0x00378B16`-`0x00378B2B`).

The debug verb `mapload` (0x2001, `0x0050D4D0`) requests one pack in mode 1 with field 0. Around
the pack's allocation `0x0036C1A0` and `0x0036C110` push and pop the current arena number (`0x022D8E1C`,
stack at `0x022D8DD0`).

`0x00378030(mode, field, index, 4, index)` sizes the pack with its fifth argument (`0x0037804B`-`0x00378059`) and returns
at once, storing nothing, when the size is 0 or less (`0x00378062`). Otherwise it pushes arena 6 (`0x0036C1D0(6, 5)`,
`0x00378075`), sets the arena number `0x022D8E1C` to 3 (`0x0036C1A0(3)`, `0x0037807F`), allocates, labels the block `MapNo`
(`0x0036C660`, `0x0037809B`), pops both (`0x0036C110`, `0x0036C140`, `0x003780A0`-`0x003780A5`) and submits the load.

The completion argument is a 32-bit dword, the low 32 bits of the block ORed with the mode (`0x003780D0`-`0x003780DD`),
and `0x00378BC0` takes the block back as `arg & 0xFFFFFFFC` and the mode as `arg & 3` (`0x00378BE2`-`0x00378BF0`). After
the submit `0x00378030` stores `0x00264FD0(field) + 500` at `0x02ADD078` in either mode (`0x003780E8`-`0x003780FA`).

### The split

`0x00378BC0` takes the mode from the argument's low two bits (`0x00378BF0`) and the block from the argument
masked with `0xFFFFFFFC` as a zero-extended 32-bit mask (`0x00378BE2`-`0x00378BED`), which also drops the top
32 bits, so the walk reads the right block only while it lies below 4 GB. It first calls `0x0036B970(block, slots, 32)`,
which is `0x0036B980`:

1. A count above 32 returns 0 (`0x0036B9BB`).
2. The header length plus the sum of every non-zero size plus 0x40 must equal the arena block's own
   size, and the arena must have a free handle per extra section (`0x0036BA78`-`0x0036BAA2`); otherwise
   0 is returned and nothing is split.
3. Each non-zero section's 0x40 slot is overwritten with a copy of the arena block header (owner
   bytes, size `+0x18`, tag) and registered as a block of its own; a zero size yields a null slot.

### The dispatch

With the 32 slot pointers, `0x00378BC0` keeps or frees each section and marks the kept ones in the
pending word `0x02ADD0EC` and the bind word `0x02ADD0F0`:

| slots | mode 1 (the field's own pack) | mode 0 (the block pack) |
|---|---|---|
| 24 to 27, 28 to 31 | stored at `0x02ADD010 + 8i` and `0x02ADD030 + 8i`, bits `0x200` << i and `0x2000` << i | the same |
| 4 | copied into a block of the same size (`0x0036C100` reads it from the block header) tagged `IdMapNo` at `0x02ADCFE8`, the original freed | neither stored nor freed |
| 8 | `0x02ADCFE0`, bit `0x8` | `0x02ADCFF0`, bit `0x8` |
| 0, 10 | freed | `0x02ADD080` and `0x02ADD068`, bit `0x1` |
| 1 | freed | stored at `0x02ADD070` and freed at once |
| 12, 13 | freed | freed |
| 16 | `0x02ADD060`, bit `0x80` | the same |
| 17 | `0x02ADD090`, bit `0x100` | the same |
| 9 | `0x02ADD0B8`, bit `0x10` | the same |
| 15 | `0x02ADD058`, bit `0x40000` | the same |

The slot 4 copy does not test its new block. `0x00378CF6` allocates it, top-down on the first try (`0x0036A190`), and when the arena
cannot make room the allocation's pressure path, retrying bottom-up, gives up and returns 0 (`0x0036C0B2`-`0x0036C0BF`). The labeller
`0x0036C660` skips a null block, but the copy at `0x00378D27` (`memcpy`) then writes the dataset to address 0, and the
game faults there.

`0x00378BC0` then clears pending bits under mask `0x7FFFF` one by one and, when the pending word is empty, calls the binder
`0x003775D0`; `0x00214B70` ends the completion.

### The bind

`0x003775D0` consumes the bind word: bit `0x80` stores the `SP1` block at `0x022CBAF0` (`0x003635C0`); bit `0x1`
walks the `SeSep` bank with `0x002DF070`, frees it and keeps the `SPP1` list at `0x022CBAF8` with the
sound map number (`0x003635E0`); bit `0x10` publishes the `ACTL` block (`0x003E8940`, cleared again when its
version is not 1); bit `0x100` binds the lights (`0x0037AA90(block, 0)`) and refreshes with `0x003DE920(0, 1)`;
bit `0x8` runs `0x00378120`, which:

1. makes the mode-1 `YM00` current (`0x02ADCFF8`) and uploads picture 0 (`0x003C63A0`) and placement 0
   (`0x00379870`);
2. hands the mode-0 `YM00` to `0x0026E7D0` (its object at `0x0209A668`, the pack pointer kept at
   `0x02ADD000`) and the mode-1 one to `0x0026E760` (its object at `0x0209A670`), both built by
   `0x002F6AB0` from a 0x240-byte allocation;
3. binds the navigation copy (`0x02ADD008`, `0x00384160`) and copies the current environment record to
   `0x02ADD10C`-`0x02ADD114`; the verb `seteventfogcolor` (`0x0120`, `0x00351AA0`) later replaces the four bytes at
   `0x02ADD114` with its four arguments, each clamped to 0 to 255, `v < 0 ? 0 : v > 255 ? 255 : v`
   (`0x00351ADD`-`0x00351B18`, then `0x00379950`);
4. stores the tag-11 chunk's vector `+0x10` at `0x02B3F560` (`0x003AFD40`) when its `+0x1C` is non-zero, else
   (0, 100.0, 0) and a fourth float from a stack dword nothing in `0x00378120` sets (`0x003781CF`-`0x0037821A`), and
   calls `0x00332130(0)`.

In `0x003775D0` bit `0x1` calls `0x002DEE90(-1)` twice, with `0x005C5230()` between them, then `0x003635E0` with the list
`0x02ADD068`, the bank `0x02ADD080` and the map number `0x02ADD078`, and zeroes `0x02ADD080` (`0x0037760E`-`0x00377651`). With
bit `0x1` clear it runs `0x003634B0(0, 0x7F)`, the map sound volume fade, instead (`0x00377659`-`0x00377660`).

Bits `0x2`, `0x20000` and `0x40000` are cleared with no other action (`0x003775DA`-`0x003775E4`, `0x0037766B`-`0x00377672`,
`0x003776C9`-`0x003776D3`). The other bits, among them `0x20`, `0x40` and the picture and placement bits `0x200` to
`0x10000`, are left as they are. The bind ends by setting the ready word `0x02ADD0D8` to 1 (`0x003776E9`).

`0x00378120` copies `0x02ADCFE0` to `0x02ADCFF8` (`0x00378132`) and zeroes `0x0209A704` and the byte `0x02ADD0E8` (`0x0037814C`,
`0x00378156`). The mode-0 hand-over of step 2 runs only while `0x02ADCFF0` is non-null, and then also copies `0x02ADD0E4`
to `0x02ADD0E0` and zeroes `0x02ADCFF0` (`0x0037815D`-`0x00378181`); the mode-1 call has no null test (`0x00378193`).

In step 3 the environment record is the dwords `0x02EBB7F8`, `0x02EBB7FC` and `0x02EBB804` (`0x003781AB`-`0x003781C9`), and
`0x02ADD108` is set to 0xA (`0x003781D6`). In step 4 the stored vector is the four dwords `+0x10` to `+0x1C`
(`0x003781E6`), the chunk pointer `[0x0209A660]` is read with no null test (`0x003781E0`), and `0x00332130(0)` is a tail jump
(`0x00378225`).

The teardown `0x00378230(releaseWorld)` frees the stored sections listed below, unbinds the lights
(`0x0037AA50(0)`) and the `ACTL` (`0x003E8940(0)`), frees the navigation copy and zeroes `0x02ADD008`
(`0x003782BB`, `0x003782C2`). Its call `0x00384160(0)` returns at once (`0x00384164`) and leaves `0x02AEDFB0` as it
was. It also drops the
pictures and placements and resets the ambient colour; `0x003784A0` frees the block pack's world
object, the loose effect bank and the two sound sections.

`0x00378230` first zeroes `0x02EBA4DC` and `0x0209A704` (`0x0037824B`, `0x00378253`). With `releaseWorld` set it frees the
pending mode-1 `YM00` `0x02ADCFE0`, zeroes it and calls `0x001808A0`, which only fetches the map-art context and returns
(`0x00378259`-`0x00378275`). While `0x02ADCFF8` is set it runs `0x0026EAC0`, then frees that block when `releaseWorld` is set
or moves it to `0x02ADCFE0` when it is 0, and zeroes `0x02ADCFF8` (`0x0037827A`-`0x003782A8`).

It frees and zeroes the `SP1` block `0x02ADD060`, the `MRP` block `0x02ADD058` and, after `0x003E8940(0)`, the `ACTL` block
`0x02ADD0B8`, each only when set (`0x003782D3`-`0x0037831F`). It zeroes `0x02EBF9C8` and `0x02ADD0F4`, sets `0x02ADD118` to 1 and
drops the minimap texture with `0x003C63A0(0)` (`0x00378326`-`0x0037833E`).

It sets the colour `0x0209A390` to four 1.0 (`0x00378354`) and the colour of each of the five light groups to (1.0, 1.0,
1.0) through `0x002ECE40` (`0x00378360`-`0x00378375`); while `0x02ADD0E9` is 0 it refreshes group 0 with
`0x003DE920(0, 0x003DE700(0), 0)` (`0x00378377`-`0x0037838E`). The four pictures and four placements are freed when set and
all eight pointers zeroed (`0x00378393`-`0x003783DE`).

The loose effect bank `0x02ADD088` is freed after `0x0026FF50` and `0x0026F420` (`0x003783E0`-`0x003783FF`) and the lights
`0x02ADD090` after `0x0037AA50(0)` (`0x00378406`-`0x00378422`). The light handles `0x02ADD120` to `0x02ADD128` and `0x02ADD11C`
are released through `0x003ABCA0` when non-zero and zeroed (`0x00378429`-`0x0037847E`), and the ready word `0x02ADD0D8` is
set to 0 (`0x00378484`). It leaves `0x02ADCFF0`, `0x02ADD080`, `0x02ADD068` and `0x02ADCFE8` as they are.

The navigation copy it frees through `0x02ADD008` (`0x003782AF`-`0x003782C9`) is still named by `0x02ADCFE8`, but it is
never bound a second time. `0x00384160` adds the block's address to each offset in place (`0x0020E600`, then
`0x0020E620`), so a second bind of one block would move its offsets twice. `0x00378120` is the only reader of
`0x02ADCFE8` that binds (`0x00378198`-`0x003781A6`), and it runs only for bind bit `0x8` (`0x003776D9`-`0x003776E2`), which
the same bind clears.

Every pack completion ends in the bind: `0x02ADD0EC` only ever holds bits under `0x7FFFF`, so clearing those
empties it and `0x003775D0` is called (`0x00378F20`-`0x00378F39`). A completion sets bit `0x8` only for a non-null
slot 8 (`0x00378D5B`-`0x00378D6D` in mode 1, `0x00378DDD`-`0x00378DEF` in mode 0). No block pack carries slot 8 (the
shipped data above), so the bind of `0x02ADCFE8` follows only a mode-1 completion, which has written `0x02ADCFE8`
first (`0x00378CB6`, then `0x00378D4C`).

The effect bank `0x003784A0` frees is the block at `0x02ADD0A0`. When the pointer is non-zero it disposes of the type-2
effect contexts (`0x0026FF50`), frees the block (`0x003697F0`) and zeroes the pointer. The loose bank's two completions
publish at `0x02ADD088`, not at `0x02ADD0A0`. The only two stores to `0x02ADD0A0` write 0: the clear in `0x00377CC0`
(`0x00377D48`, `rbx` zeroed at `0x00377CCC`) and this free (`0x003784ED`). No instruction takes its address, by `rip`
or through the image base, so the pointer is always 0 and the free branch (`0x003784DC`-`0x003784ED`) never runs.

The split also zeroes the dword after the map number `0x02ADD078`:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02ADD07C` | `u32` | 0 (zero-filled tail of `.data`) | the dword after the map number `0x02ADD078`, zeroed when the block pack is split | `0x00378BC0`, 0 (`0x00378E2A`, `ebp` cleared at `0x00378C2C`) | no RIP-relative, image-base-relative or disp32 reference reads it, and the dword read of `0x02ADD078` (`0x00377623`) stops before it |
| `0x02ADD0A0` | `void*` | 0 (zero-filled tail of `.data`) | the effect-bank block `0x003784A0` frees | the loader reset `0x00377CC0`, 0 (`0x00377D48`); `0x003784A0`, 0 after the free (`0x003784ED`); no store of a block: no other RIP-relative, image-base-relative or address-forming reference names it, the indexed section stores from `0x02ADD010` and `0x02ADD030` cover four slots each (`0x00378C48`, `0x00378C74`), and no 8-byte pointer or 4-byte RVA in the image holds its address | `0x003784A0` (`0x003784D3`, the test; `0x003784E1`, the block passed to `0x003697F0`) |

The world objects go through two helpers. `0x0026EAC0`, called by `0x00378230` while a mode-1 `YM00` is
current, releases the mode-1 object `0x0209A670`, runs `0x003ECF70` and clears the model block
(`0x0026E640`); `0x0026EAF0`, called by `0x003784A0`, does the same and then releases the mode-0 object
`0x0209A668`. Each release is `0x003EC860(slot, 0x0026EDB0)`: when the slot holds an object, `0x0026EDB0`
runs the object's callback at `+0x128`, the block is freed (`0x003697F0`) and the slot zeroed. The
teardown also runs `0x00363730`, which zeroes `0x022CBA90`, the `SP1` pointer `0x022CBAF0` and `0x022CBA9A`.

`0x002F6AB0` sets that callback to `0x002F5450`. It frees the object's own tables (`[+0x1C0]` to
`[+0x218]` and the tag-24 entries' `+0xC0`), removes the tag-14 buffer from the buffer list
(`0x00468060`), frees the animation slots of tag 23 (`0x00466B10`: both arrays of every slot, then the
slot array; `0x02EBB6E0` and `0x02EBB6F8` become 0) and releases the paletted textures of tag 12
(`0x004680D0`).

The buffer list at `0x02EBB6A0` is set up at boot by `0x00467BB0` (from `0x0036F4D0`, through `0x00536120`)
with 0x28-byte entries: the last path component of a name, at most 31 characters, then the buffer
at `+0x20`. `0x00467BF0` appends an entry (`0x005360C0`, which allocates the node and counts it at
`+0x14`). `0x00468060` unlinks every entry of a buffer with `0x00536140`, whose release callback
`0x00467B20` runs `0x00467B30` on the buffer (its callback at `+0x10`, then its 0x60-byte entry array at
`+0x08` is freed) and frees the buffer.

The start-up initialiser `0x00266D10` resets the loader once through `0x00377CC0`: every section pointer
and world object pointer is zeroed, `0x02ADD0E0` becomes -1, `0x02ADD118` 1 and `0x02ADD130` the text
`none`, the start-up tables are requested again (`0x00378540`), and the pending and bind words
(`0x02ADD0EC`, `0x02ADD0F0`) and `0x02ADD0EA` are cleared.

The text is five bytes, `none` and its terminator, copied from `0x008C5928` as a dword to `0x02ADD130` and a byte to
`0x02ADD134` (`0x00377CCE`, `0x00377CDB`); the teardown `0x00378230` writes it the same way (`0x00378471`, `0x0037848F`).

### The map colour and the buffer list's header

The section-11 colour `0x0209A3A0`-`0x0209A3AC` is reset to (1.0, 1.0, 1.0, 1.0) by `0x0026E1D0` (`0x0026E23F`, one 16-byte
store) and set by the map set-up `0x002F6AB0` from the three integers `0x00466140` unpacks from dword 1,
each scaled by 1/128, `n * [0x008C5B34]` with the constant 0.0078125 (`0x002F6C42`, `0x002F6E0D`-`0x002F6E53`), with
alpha 1.0 (`0x002F6E27`). The body-colour reader `0x00231A90` returns it
when the body's polygon index is negative (a signed test, `0x00231C52`-`0x00231C55`), and the polygon's vertex colour
otherwise.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A3A4` | `f32` | 0 (zero-filled tail) | the colour's second float: mask `0xFF00` of dword 1 (`0x00466147`-`0x0046614D`) / 128 | `0x0026E1D0`, 1.0 (`0x0026E23F`); `0x002F6AB0` (`0x002F6E3C`) | `0x00231A90` (`0x00231DEE`) |
| `0x0209A3A8` | `f32` | 0 (zero-filled tail) | the third float: mask `0xFF0000` (`0x00466152`-`0x0046615B`) / 128 | `0x0026E1D0`, 1.0 (`0x0026E23F`); `0x002F6AB0` (`0x002F6E47`) | `0x00231A90` (`0x00231DFB`) |
| `0x02EBB6B0` | `i32` | 0 (zero-filled tail) | the buffer list's entry size: -1 from the list set-up `0x00536120`, then `0x28`; the append `0x005360C0` allocates it plus `0x10` (`0x005360D0`-`0x005360D8`) and copies that many bytes, a sign-extended count (`0x005360FD`) | `0x00536120` (`0x00536130`, as `+0x10` of the list at `0x02EBB6A0`); `0x00467BB0` (`0x00467BC7`) | `0x005360C0` (`0x005360D0`, `0x005360FD`), from `0x00467BF0` (`0x00467C87`) |
| `0x02EBB6B8` | `void*` | 0 (zero-filled tail) | the list's release callback, `0x00467B20`; the unlink `0x00536140` calls it on the entry's data (`0x0053615B`-`0x0053616D`) | `0x00536120`, 0 (`0x0053612C`); `0x00467BB0` (`0x00467BD1`) | `0x00536140` (`0x0053615B`), from `0x00467CB0` |

## Modding notes

- A pack is valid when its 32 sizes plus the 0xC0 header and one 0x40 slot per present section add
  up to the file length; the loader checks nothing else about the container.
- A section placed in an unused slot (2, 3, 5 to 7, 11, 14, 18 to 23) stays allocated with no owner;
  slot 13 is always freed, so an edited embedded effect bank changes nothing and the loose `.efb` is
  the file to edit.
- A field's `YM00`, navigation, pictures and lights come from its own pack; its sound bank and map
  sound list come from the block pack, so two fields of one block share them.
- `YM00` must carry its 17 chunks in the tag order the index gives; the parser accepts any order but
  skips a chunk whose offset equals the next one's.
- An `ACTL` with a version other than 1 is dropped silently at bind.

## Related

- [Weather: the three weather slots of an area, the change roll on entering, the setweatherslot verb, the MWeather table, what the slot does to the sky, the map and combat, and the environment variant it selects](weather.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them](doors-gates-and-map-changes.md)
- [How a unit finds its way across the navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)
- [The map sound list](../Sound-And-Music/map-sounds.md)
- [The menu-map container](../Game-Files-And-Data-Tables/menu-map-files.md)
- [section_014, the LGT2 light set](../EBP-Script-Files/ebp-lighting-lgt2.md)
- [The EFX and EFB effect containers](../Graphics/effect-files-efx-efb.md)
- [MRP menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md)
- [`shadow-settings-01f82ea8-accesses.tsv`](shadow-settings-01f82ea8-accesses.tsv): every access to the
  shadow object through its pointer `[0x01F82EA8]`, all in the direction setter `0x001F08A0` (18 rows).
- [`mpk-map-pack-actl-census.tsv`](mpk-map-pack-actl-census.tsv): one row per `ACTL` section: its header, the shape
  of its id index, its record count and its tombstones (270 rows).
- [`mpk-map-pack-map-ref-field-packs.tsv`](mpk-map-pack-map-ref-field-packs.tsv): `map_ref.bin` row by row, one per
  field: the field's own pack and its block's pack, each by index, name and non-empty slots (1,315 rows).
- [`mpk-map-pack-mrp-census.tsv`](mpk-map-pack-mrp-census.tsv): the `MRP` sections of `rwg0201` and `rwg0202`, which
  hold the same bytes (2 rows).
- [`mpk-map-pack-sp1-census.tsv`](mpk-map-pack-sp1-census.tsv): one row per `SP1` section: its header offsets, the
  extent of its emitter index and four layout checks (456 rows).
- [`mpk-map-pack-wd-census.tsv`](mpk-map-pack-wd-census.tsv): one row per `WD` section: its header fields and each
  record's two words and hash (46 rows).
- [`mpk-map-pack-ym00-census.tsv`](mpk-map-pack-ym00-census.tsv): one row per `YM00` index entry, with the extent of
  its chunk (8,298 rows).
- [`mpk-map-pack-ym00-tag2226-census.tsv`](mpk-map-pack-ym00-tag2226-census.tsv): one row per tag-22 and tag-26
  chunk of each `YM00`: its nested index and its records (920 rows).

The columns of these tables, after `pack` and the section's size:

- `actl-census`: `ver`, `stride`, `idbound` and `buckets` from the header and the index, `records`, the index and
  aux offsets `idxoff` and `auxoff` and the aux length `auxlen`, `recfit` and `idxfit` (`OK` in all 270: the records
  end at the aux table, and the index ends where the first record begins), and `tombstones`, 101 in all, as in
  [`mpk-map-pack-actl-rows.tsv`](mpk-map-pack-actl-rows.tsv), which has the records themselves;
- `map-ref-field-packs` (no `pack` column): `field`, the own pack's index, name and non-empty slots (`own_idx`,
  `own_pack`, `own_sections`), `block` and its pack's `block_idx`, `block_pack` and `block_sections`, and the row's
  words `w2` and `w3`;
- in `map-ref-field-packs` a pack's name comes from matching its size in `FileSizeTable_US.fst`: `ambiguous:` lists
  the packs of one size (286 cells, where [`mpk-map-pack-field-layers.tsv`](mpk-map-pack-field-layers.tsv) names one
  of them), and `-` marks a field without that pack;
- `mrp-census`: `sha16` the first 16 hex digits of the section's SHA-256, `magic`, the counts and offsets of the
  name tail (`tail`), the five rectangle descriptors (`desc`) and table B (`tblB`), `tblBSpans` table B's two spans
  (a 16-byte name and a TIM2 picture each) and `descs` the descriptor rows;
- `sp1-census`: `dword04` (`+0x04`), `offB`, `offC` and `offD` (the areas, index and emitters offsets of
  [`mpk-map-pack-sp1-rows.tsv`](mpk-map-pack-sp1-rows.tsv)), `offW` (`+0x1A`) and `w_count` (-1 when `+0x1A` is 0),
  the index's bound and its non-zero entries with their lowest and highest values (`c_bound`, `c_offn`, `c_min`,
  `c_max`), and `d_term`, where the `u16` list at `offD` ends (-1 when `offD` is 0);
- `flags` in `sp1-census`, one letter per check: `T` the table of `+0x04` dwords at `+0x20` fits the section, `C`
  every non-zero index entry lies inside it, `D` the list at `offD` ends inside it (`-` when `offD` is 0), and `0`
  for `+0x1A` = 0: `TCD0` in 454 sections and `TC-0` in 2;
- `wd-census`: `field02` the bank id, `dataSize` the trailing data's size and `dataStart` its start, `count`,
  `flags14` (`+0x14`), `firstOff` the first offset-table entry, `tableSpill` 1 where the record table runs past
  `dataStart`, `records` each record's table entry with its X, Y and hash words, and three checks: X never falls
  (`Xmonotonic`), X and Y lie below `dataSize` (`XYunderDsz`), and the records with X equal to Y (`XeqY`);
- `ym00-census`: `inner_name` the name at `+0x08`, `idx_count`, then `entry`, `tag`, `chunk_off` and `chunk_bytes`,
  `order` (`OK` in all: the offsets never fall), `last_end` where the closing entry points and `tail_pad` the bytes
  after it;
- the entries of `ym00-census` are those of [`mpk-map-pack-ym00-chunks.tsv`](mpk-map-pack-ym00-chunks.tsv); here
  `chunk_bytes` runs to the next entry, so it is 0 for the closing entries and for the 851 entries that share their
  offset with the next;
- `ym00-tag2226-census`: `tag` 22 (461 chunks) or 26 (459), `chunkSize`, `count`, `sentinelOK` (the closing entry
  lands at the chunk's end) and `ascending` (the offsets never fall), 1 in all 920, `tagsSeen` the tags of its
  entries, `records` how many records parse (for tag 22 with a count per `+0x30` mode), `picTotal` the pictures of a
  tag-26 chunk and `sampleNames` its first two record names.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat AI: `0x002315E0` is called by `0x0032A4D0`; `0x0032A4D0` is called by `0x003247F0`; those functions are documented on
  [geometry primitives](../Movement-And-Pathfinding/geometry-primitives.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat formula: `0x0046AB10` calls `0x0031B860`; `0x0046AB10` is called by `0x00469EC0`; those functions are documented on
  [save and teleport crystals](save-and-teleport-crystals.md),
  [action definition row](../Battle-Actions/action-definition-row.md).
