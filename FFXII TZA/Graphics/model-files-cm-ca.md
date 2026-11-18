[Home](../../README.md) / [Graphics](README.md) / Model files (.cm, .ca)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Model files (.cm, .ca): the @FRP container and its FCP, FDM, FOR, FTE, FCT and FTR entries | format | Graphics | Character models / Model Files | The model and animation containers: the .cm and .ca files under obj_finish, the seven entries a model row binds from a .cm, the @FCP parameter block with its section table, property ids and default tables, the @FTR skeleton and how it is built, the @FOR variant records and distance LOD, the @FDM key table, the @FTE textures and @FCT four-page palettes, the draw builder's texture and palette pick, and counts over all 4,230 shipped files. | 0x00504F00, 0x00504E70, 0x00504940, 0x004780C0, 0x0041FCF0, 0x0041F340, 0x00420480, 0x002EDBD0, 0x003E55F0, 0x004FE270, 0x004FE2F0, 0x01F265B0, 0x01F266B0, 0x003E6150, 0x003E5AD0, 0x0041E5B0, 0x004292B0, 0x003712E0, 0x00372820, 0x003713C0, 0x00409300, 0x004094D0, 0x00409250, 0x0046D560, 0x004201F0, 0x00504840, 0x005048A0, 0x0053AB50, 0x00504D30, 0x005044D0, 0x00504D20 |

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

A character render record is bound to its model by `0x0041FCF0`, which passes the model's bank index
(record `+0x408`) to `0x0041F340`. That routine:

1. finds the `@FTR` entry by tag and the record's name (`0x00409660`), sizes the skeleton
   (`0x003712E0`) and builds it in a new [skeleton entry](skeleton-entries-and-bones.md) at root `+0xD98` (`0x0046E4D0` → `0x00372820`);
2. makes a render model instance in the table at root `+0xDA0` with `0x004780C0`, which calls `0x00504F00`, and keeps
   the row's index in the record's word `+0x90`;
3. when the model's bank entry has an effect ticket, makes the record's effect context from it
   (`0x003B3550`, kept at record `+0x288` and row `+0x240`).

`0x00420480` then points record `+0x400` at the `@FCP` payload (`0x004205E6`) and stores the `@FOR` scale
at record `+0x26C` (`0x0042061B`).

Binding a character to its model takes three things from the `.cm`: the `@FTR` entry becomes the character's skeleton,
a draw instance is made for the model, and when the model carries an effect, an effect context is made for it. The
character then keeps a link to the model's `@FCP` parameter block.

## Layouts

All multi-byte fields are little-endian.

### The container

```python
@FRP header (0x30 bytes)   see resource sections; name = the file name without extension
version 0                  every .cm (1,066) and 1,969 .ca: u32 offset table at +0x30, offsets from +0x30
version 1                  1,195 .ca: +0x30 u32 columns (80), +0x34 u32 rows, offsets from +0x40, 0 = empty slot
+0x08                      u32 content length; the rest of the file is zero padding
```

### The entry header

Every entry starts with the same `0x30`-byte header the section search compares.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | tag | @FCP, @FTR, @FDM, @FOR, @FTE, @FCT, @FEF, @FMC, @FMN, @FMW, @FRM |
| `+0x04` | `u32` | kind | @FTR 2; @FCP, @FDM, @FOR, @FTE, @FCT, @FEF 0 |
| `+0x08` | `u32` | length | bytes of the entry, header included |
| `+0x0C` | `u32` | count | @FCP 1, @FTR nodes, @FTE textures, @FCT palettes, @FDM and @FOR 0 |
| `+0x10` | `char[32]` | name | the container's name for the model entries |

### The model row

`0x00504F00` fills a `0x260`-byte render model instance of the root's `+0xDA0` table. It stores the container at
`+0x30`, the skeleton entry `0x0041F340` passes (root `+0xD98`) at `+0x38`, the render record's `+0x18` at `+0x40`
(`0x00504F2D`-`0x00504F41`) and the low byte of its tenth argument at `+0xBB` (`0x00505052`). It finds the model's bank
entry with `0x00409F50(container, id)` (`0x00504F47`), runs `0x00504940` after the offsets (`0x00505026`) and sets bits
`0x3` of the flags `+0x08` (`0x0050512D`).

It copies the 32-byte model name to
`+0x0C`, binds the container section at `+0x1F0` and the `@FEF` section at `+0x228` (`0x00504E70`), and
stores each entry's offset from the container, or −1 when the entry is absent (`0x00409A30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x1F8` | `void*` |  | the @FRP container (`0x00504940`) |
| `+0x208` | `u32` |  | @FOR offset |
| `+0x214` | `u32` |  | @FEF offset |
| `+0x20C` | `u32` |  | @FDM offset |
| `+0x218` | `u32` |  | @FTE offset |
| `+0x210` | `u32` |  | @FTR offset |
| `+0x21C` | `u32` |  | @FCT offset |
| `+0x220` | `u32` |  | @FCP offset |
| `+0x230` | `void*` |  | the @FEF section (`0x00504940`) |
| `+0x0B8` | `i8` |  | the @FOR record key |
| `+0x0B9` | `i8` |  | the option number |
| `+0x0B3` | `u8` |  | LOD levels (`+0x3A` + 1) |
| `+0x0BA` | `i8` |  | the palette page (`0x00504D20`) |

### @FCP, the parameter block

Entry 0 of every `.cm`. The payload starts at entry `+0x30`; offsets are from the payload.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | value 4 |
| `+0x01` | `u8` |  | non-zero: `0x0041F340` allocates a second per-node block and sets record `+0x284` bit `0x10000`; id `0x40000000` returns it |
| `+0x02` | `u16[17]` |  | offset of sections 1 to 17, 0 = absent (section n at +2n) |
| `+0x24` | `u32` |  | length of section 2, copied after the skeleton |
| `+0x2C` | `u8[6]` |  | event map (`0x0041E5B0`), `0x7F` ends it |
| `+0x32` | `u8` |  | version, `0x0A` |
| `+0x3A` | `u16` |  | bone for special id `0x104` (`0x003E5AD0`) |
| `+0x3C` | `u16` |  | bone for special id `0x105` |
| `+0x3E` | `u16` |  | bone for special id `0x106` |

```
section 1 +0x14C u16[32]  bone for special ids 0 to 31 (0x003E5AD0)
section 2        copied verbatim after the skeleton core (0x00372820)
section 5        per palette a u16 offset of a list; each list is u16 offsets ending at 0, each naming a 0x30-byte
                 animation entry; every offset is from the section (0x003E7210)
section 6        16-byte points, for ids 0x300 up: u16 bone, a u16 that is 0 in every model, three f32 (0x003E5B30)
section 7        the pose sequencer's events (model-oscillators-and-pose-sequencer.md)
section 8        a 0x10-byte head starting with a u16 count, then count x 0x1D0 bytes (0x003E6D10);
                 copied into the record's block by 0x0041F340
section 9        f32 / u32 slots read through property ids
section 10       a block taken by 0x003AF340: f32 +0x08 and byte +0x10 are read; see the values below
```

A property id is `SS VV DD FF`: `SS & 0x1F` is the section, `SS >> 5` the mode, `VV` the lowest
payload version that may answer, `DD` the slot in the default table and `FF` the slot in the section.

- `0x004FE270(payload, id)` reads a float. With no payload or `VV` above the version byte it returns
  default float `DD` from `0x01F265B0`. Otherwise an id of `0x20000000` or more returns −1.0, and any
  other id reads section slot `FF`, or the default when the section is absent.
- `0x004FE2F0(payload, id)` reads an integer. Mode 1 (`0x2…`) reads dword `FF` with the same fallbacks,
  defaults from `0x01F266B0`. Mode 3 (`0x6…`) reads byte `SS & 3` of dword `FF` of section 9. The id
  `0x40000000` returns payload byte `+0x01`. Any other mode returns −1.
- Mode 3 also returns default dword `DD` of `0x01F266B0` for no payload (`0x004FE37E`), for `VV` above the
  version byte (`0x004FE38D`) and for an absent section 9 (`0x004FE397`). The id `0x40000000` is tested
  before the mode (`0x004FE2F6`), and its byte is read with no test for a null payload (`0x004FE2FE`).
- `0x003E6150(id, property)` takes a render id and a property id. It returns 0 for a model without `@FCP`
  (`0x002EDBD0` of the id gives no payload, `0x003E616A`).
- Otherwise it calls the float getter (`0x003E61AA`) and multiplies the result, `v * [record + 0x26C]` (`0x003E62E1`),
  by the scale `+0x26C` of the id's render record for a fixed list of section 1 and section 9 ids, or
  divides by it for `0x9001E1F`, `v / [record + 0x26C]` (`0x003E62F4`), with `v = 0x004FE270(payload, property)`.
  The render record is `[0x022C6F28] + 0x740 * id` (`0x003E618A`-`0x003E6191`).
- The ids it multiplies (`0x003E61AF`-`0x003E62E1`): `0x1002143` and `0x1002244` of section 1; of section 9
  `0x9000000`, `0x9000101`, `0x9000202`, `0x9000505`, `0x9000606`, `0x9000707`, `0x9000808`, `0x9000B0C`,
  `0x9000C0D`, `0x9000D0E`, `0x9000E0F`, `0x9000F10` and `0x9042A2E`.
- Also of section 9: `0x9001011`, `0x9001112`, `0x9001213`, `0x9001314`, `0x9001415`, `0x9001516`, `0x9001617`,
  `0x9001718`, `0x9001819`, `0x900191A`, `0x9001A1B`, `0x9001B1C`, `0x9001C1D` and `0x9001D1E`. Every other id
  is returned as the getter gives it.

Small readers take values straight from the record's `@FCP` payload `+0x400`, scaling sizes by the
record's per-axis scale (`+0x260`–`+0x268` × `+0x160`–`+0x168` × `+0x26C`):

- `0x003E5CD0` returns section 3, or null; `0x003E4700` section 1's float `+0x144` (1.0 without).
- `0x003E4DD0(record, axis)` section 1's `+0x114`, `+0x118` or `+0x11C` times that axis's scale (1.0
  without); `0x003E5130` the six floats `+0xBC`–`+0xD0` of section 1, two each times the z, x and y
  scales; `0x003E4B50` a box from section 1's `+0x114`–`+0x11C`, or from `0x004234B0`'s `+0x54` when it
  returns a block. `0x0042E850` calls `0x003E4700`, `0x003E4DD0` and `0x003E4B50`; the effect target
  queries `0x003A4290` and `0x003A56F0` call `0x003E5130` and `0x003E4F50`.
- `0x003E5C90` returns section 9's float `+0xA8` (0.10472 without), `0x003E5EA0` its `+0xA4` (0 without),
  and `0x003E4F50` places section 9's point `+0xD0`–`+0xD8` by the record's matrix `+0x180` and adds the
  focus point `+0x670`. `0x003E56E0` reads property `0x62060A2D` (`0x004FE2F0`).
- `0x003E6D40(record)` returns the arena address of the block at `+0x2FC` plus the offset `+0x300`, or 0
  when the offset is 0 (`0x003AB7F0`).

### @FCP values per model

Each model's value for a property is what the getters above return for it. The block is at payload
version `0x0A` in all 1,066 models, so a stored value is used whenever the section is present, and the
default otherwise. No property slot reads past its section in shipped data.

`0x003E6150` scales at run time, so the tables keep the stored value and the `scale` column says what the
site does to it. The same property read through `0x004FE270` is not scaled: `0x09001D1E` is scaled at
`0x002E2EC9` and not at `0x0046C7EE`.

`0x003204E0(unit, index, out)` reads a property chosen by index, 0 to `0x21`. The id comes from the table at
`0x01EED320` and the handling from the byte table at `0x003205F0`: a float through `0x002ECE50`, the same float
multiplied or divided by the third output of `0x00265240`, or an integer through `0x002ECE80`. Index `0x1C` holds
`0x40000000`, the one id `0x004FE2F0` answers with payload byte `+0x01` (`0x004FE2F6`-`0x004FE2FE`). `0x003045CA` calls
it with index 1, and `0x00320DC8` with an index from the table at `0x01EED288`.

Town selections are made in code. Where `0x00377C20` is non-zero, `0x002E2E9D`-`0x002E2EA7` read `0x01002D4F` and
`0x01002E50`; elsewhere `0x002E2EAE`-`0x002E2EB8` read `0x01002143` and `0x01002244`. `0x002E9681`-`0x002E968D` makes
the same choice between `0x01002D4F` and `0x01002143`. The town pair's default is −1.0, and all 1,066 models
store a value of 0 or more for both, so the default is not used by a shipped model.

Section 5 is in 7 models. `0x003E7210(record, palette, sub)` takes list `palette` and passes each named entry to
`0x00504D30`, or only entry `sub` when `sub` is not `0xFFFF` (`0x003E7235`). Presentation command `0x16` sets the
palette, the choice between this call and `0x003E69E0`, and `sub`, then calls `0x0042B550`.

Section 6 holds 16 points in every model; 5,837 of the 17,056 name a bone and the rest hold `0xFFFF`. `0x003E5B30`
takes id `0x30B` from the active presentation entry or the rig and not from this section (`0x003E5B43`), as
[skeleton entries and bones](skeleton-entries-and-bones.md) describes. The stored point `0x0B` names a bone in 719
models.

Section 10 is 48 bytes in all 613 models that have it. `0x003E6E40` is the path to it, called at `0x003AF3B0`:
`0x003AF340` stores float `+0x08` divided by byte `+0x10` in the second-pool entry's `+0x18`
([character lighting and shadows](character-lighting-and-shadows.md)). The other 43 bytes are kept as stored. Float
`+0x08` is 75 in 578 models, 60 in 22, 50 in 11 and 120 in 2; byte
`+0x10` is 8 in 609 and 16 in 4.

`Database/Tools/catalogues/fcp_tables.py` writes the `fcp-` tables named in the table list below.

### @FTR, the skeleton

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `u16` |  | node count again, read as a word by `0x00409240` (`0x0040924A`) |
| `+0x34` | `u32` |  | offset of the value pool, from the entry |
| `+0x38` | `u16` |  | extra u16 slots after the node list (equal to the @FDM key count) |
| `+0x40` | `u32[n]` |  | per node: (record offset from the entry << 12) \| node number |

```
record +0x00  u32  mask 0xFFF the node's key, mask 0xFFF000 its parent (0xFFF = no parent), mask 0xFF000000 0xFF
record +0x04  u32  flags; the u16 pool indices follow at +0x08 (+0x0A when bit 0x40000000 is set)
```

With flag bits `0x200100` both set, `0x00409300(entry, record, out)` sets `out` `+0x30`-`+0x38` to 0 and `+0x3C` to
1.0 (`0x0040936A`-`0x0040938F`), steps past one index for bit `0x80000000`, the sixteen matrix indices and one index
for bit `0x400000`, then takes one pool dword for each of bits `0x800000`, `0x1000000` and `0x2000000` as the
node's translation x, y and z (`0x00409392`-`0x004093D4`).

It takes one pool float for each of bits `0x4000000`, `0x8000000` and `0x10000000` as three angles in radians, 0.0
for a clear bit, that `0x0046D560` turns into the rotation (`0x004093D7`-`0x0040941B`); otherwise the node starts at the
identity (`0x00409428`).

The pool is the entry plus its `+0x34`, added in 32 bits (`0x00409347`), and the indices start at record `+0x08`, or
`+0x0A` with bit `0x40000000` (`0x00409340`-`0x00409352`). All of this is for a kind-2 entry. For kind 0 `0x00409300`
builds the rotation from the record floats `+0x34`, `+0x38` and `+0x3C` (`0x0046D380`) and the translation from
`+0x28`-`+0x30` (`0x0046D920`), for kind 1 from `+0x94`-`+0x9C` and `+0x88`-`+0x90` (`0x0046D380`, `0x0046D8E0`), and
for any other kind it writes nothing (`0x0040931F`-`0x00409336`, `0x0040942F`-`0x004094A6`).

For kind 1 the three translation floats are copied to the stack first (`0x00409452`-`0x0040946E`), and `0x0046D8E0`
also stores `out` `+0x3C`: the product of the 1.0 that `0x0046D380` left there (`0x0046D550`) and the stack dword
after those three floats (`0x0046D90B`-`0x0046D910`), which `0x00409300` never writes. `0x0046D920`, the kind-0 call,
leaves `+0x3C` at 1.0.

Bit `0x200000` makes `0x004094D0` copy sixteen pool dwords as a 4×4 matrix to node `+0x150`, starting after the
index for bit `0x80000000` (`0x004094F5`-`0x0040958D`), and the identity goes there without it (`0x0046D110`,
`0x00409593`). Bits `0x80000000` and `0x400000` each skip one index. `0x00409250` returns the key from bits `0xFFF`,
or the u16 at `+0x08` when bit `0x40000000` is set.

`0x0046D560(m, x, y, z)` takes each sine from the 32,768-entry table `0x01F004E0` at
`trunc(a / 2π × 32768) & 0x7FFF` (2π the float `0x01CEBC78`, 32768 the float `0x00D10820`) and each cosine at
`(0x2000 − trunc(a / 2π × −32768)) & 0x7FFF` (`0x00D10828`), a quarter turn on (`0x0046D57E`-`0x0046D665`). It writes
the rows `+0x00`, `+0x10` and `+0x20`, each with a fourth float of 0 (`0x0046D699`, `0x0046D6D1`, `0x0046D728`), and
leaves `+0x30` to `+0x3F` as they are.

With s and c the sine and cosine of x, y and z, row 0 is `(cy·cz, cy·sz, −sy)`, row 1
`(sx·sy·cz − cx·sz, sx·sy·sz + cx·cz, sx·cy)` and row 2 `(cx·sy·cz + sx·sz, cx·sy·sz − sx·cz, cx·cy)`
(`0x0046D67F`-`0x0046D71C`).

`0x00409240(entry)` gives the node count (word `+0x30` for a kind-2 entry, dword `+0x0C` otherwise), `0x00409270(entry,
n)` the address of node `n`'s record (`+0x40` table entry `>> 12`, 0 past the count or for another kind), and
`0x004095A0` the address of the `+0x40` table. With flag bit `0x400000` set, `0x004092A0(entry, record)` returns, as a
float, the dword of the pool at `entry + [entry + 0x34]` named by the node's first pool index, skipping one index each
for bits `0x40000000` and `0x80000000` and sixteen more when bits `0x200100` are both set, and 0.0 otherwise.

### @FOR, variants and distance LOD

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `u8` |  | record count |
| `+0x32` | `u8` |  | table B stride per option number |
| `+0x33` | `u8` |  | option numbers allowed (row `+0xB9` is clamped below it) |
| `+0x34` | `u16` |  | table A offset (`0x40`) |
| `+0x36` | `u16` |  | table B offset |
| `+0x38` | `u16` |  | offset of the records, `0xE0` bytes each |
| `+0x3A` | `u8` |  | LOD distance count (0, 1 or 2) |
| `+0x3B` | `u8` |  | highest LOD level |
| `+0x3C` | `u16` |  | first LOD distance, centimetres |
| `+0x3E` | `u16` |  | second LOD distance, centimetres |

```
record +0x00   u8    key
record +0x05   u8[]  selector count per part
record +0x18   f32   the model's scale
record +(i+1) x 0x20   part i's selector bytes
```

### @FDM, the key table

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `u16` |  | 1, 2 or 3 |
| `+0x32` | `u16` |  | offset of {u32 count, u32 keys[count]} (`0x50`) |

### @FTE, textures

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `u8` |  | count, then u8 texture slots uploaded with every draw |
| `+0x40` | `...` |  | records, `0x20` bytes each, `+0x0C` of the header many |
| `+0x00` | `u32` |  | VRAM bytes, a multiple of `0x2000` |
| `+0x04` | `u16` | width |  |
| `+0x06` | `u16` | height |  |
| `+0x08` | `u16` |  | GS pixel format: `0x13` 8-bit indexed, `0x14` 4-bit indexed |
| `+0x0A` | `u16` |  | upload width |
| `+0x0C` | `u16` |  | upload height |
| `+0x14` | `u32` |  | upload bytes = upload width x height x 4 |
| `+0x18` | `u32` |  | pixel data offset, from the entry |

### @FCT, palettes

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `...` |  | records, `0x10` bytes each, `+0x0C` of the header many |
| `+0x00` | `u16` |  | VRAM bytes (`0x2000`) |
| `+0x02` | `u16` |  | palette bytes (colours = bytes / 4) |
| `+0x04` | `u8` |  | upload width |
| `+0x05` | `u8` |  | pages (4) |
| `+0x06` | `u16` |  | upload height |
| `+0x0C` | `u32` |  | data offset, from the entry: four pages of palette-bytes each |

[`model-files-cm-ca-fct-palette-colours.tsv`](model-files-cm-ca-fct-palette-colours.tsv) lists every colour of every
page, one row each. The 1,972 palettes share 1,512 contents, and each content is written once;
[`model-files-cm-ca-fct-palette-contents.tsv`](model-files-cm-ca-fct-palette-contents.tsv) gives its `sha256`, the
same column as the palette table.

`0x005044D0` returns a page's address (data offset + page × palette bytes), and `0x0053BE13` copies that many bytes
unchanged. The fourth byte of a colour is its alpha. The alpha reference of a draw stops at `0x80` (`0x0053D4B0`), and
959,330 of the 1,377,728 colours hold `0x80` there, 58,026 hold 0 and 26,496 hold more than `0x80`.

Two palettes hold fewer than four pages: `high/c10/c1005/hc1005_01.cm` palette 1 and `high/n11/n1164/hn1164_01.cm`
palette 2 stop after 64 colours of page 0, where their entry ends. `0x005044D0` does not test the size.

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
| `@FTR` nodes | byte `+0x03` is `0xFF` and flags word `+0x04` has bit `0x100` set in all 27,561 nodes |
| `@FTR` `+0x38` | equals the `@FDM` key count in all 1,045; up to 1,188 (`m1208`) |
| `@FOR` | in all 1,066; one record in 1,000, up to 12; keys 1 to n in 1,062 |
| `@FOR` LOD | no distance in 751, one in 179, two in 136; 32,767 cm (no switch) in 59: the only distance in 54 one-distance files, the second in 5 two-distance files |
| `@FDM` | in 1,045 (all but 21 weapons); 30,023 keys, all below `0x10000` |
| `@FTE` | in 1,044; 2,127 textures, 1 to 17 per file; 2,081 8-bit and 46 4-bit; pixel data packed in record order up to the entry's end in all |
| `@FCT` | in 1,044; 1,972 palettes of 256 colours (1,618), 128 (318) or 16 (36); four pages in all |
| palette page 3 | mean colourfulness (max − min channel) 30.6, 30.5, 21.4 and 1.6 on pages 0 to 3; page 3 is near-grey (no colour's red, green and blue differ by more than 13) in 1,962 of the 1,970 palettes whose pages fit, and the only near-grey page in 1,856 of them; equal red, green and blue in every colour of page 3 in one; the other 8 are second and third palettes of `hc1005_02`, `hc1005_03` and `hc1006_01` to `hc1006_03`, spread 37 to 88 |

Every file, entry and record of the 4,230 files, decoded with the layouts above. The tables join by `path`, the
file's path under `ps2data/obj_finish/in/`. `bound_id` joins [model-asset-list.tsv](model-asset-list.tsv), and the
weapons' special-id bones and node keys per model are in [weapon-bones.tsv](weapon-bones.tsv). A field the layouts do
not name is given by its offsets, as hex bytes.

| table | rows | one row per |
|---|---:|---|
| [`model-files-cm-ca-files.tsv`](model-files-cm-ca-files.tsv) | 4,230 | `.cm` or `.ca` file: folder, container version, size, content length, entry count, SHA-256, the entries' tags in order and the bound id that names it |
| [`model-files-cm-ca-entries.tsv`](model-files-cm-ca-entries.tsv) | 78,618 | container entry: index, file offset, tag, kind, length, count and name |
| [`model-files-cm-ca-ca-slots.tsv`](model-files-cm-ca-ca-slots.tsv) | 63,836 | non-empty slot of a version-1 `.ca`: its row and column and the entry's tag |
| [`model-files-cm-ca-heads.tsv`](model-files-cm-ca-heads.tsv) | 1,066 | `.cm`: the header fields of its `@FCP`, `@FTR`, `@FOR`, `@FDM` and `@FTE` entries |
| [`model-files-cm-ca-fcp-sections.tsv`](model-files-cm-ca-fcp-sections.tsv) | 6,454 | present `@FCP` section: offset, span and length |
| [`model-files-cm-ca-fcp-attachment-slots.tsv`](model-files-cm-ca-fcp-attachment-slots.tsv) | 19,296 | one slot of `@FCP` section 3: bone, position, angles and scale ([character render records](character-render-records.md)) |
| [`model-files-cm-ca-fcp-section-bytes.tsv`](model-files-cm-ca-fcp-section-bytes.tsv) | 6,454 | present `@FCP` section: every byte as hex |
| [`model-files-cm-ca-fcp-slots.tsv`](model-files-cm-ca-fcp-slots.tsv) | 176,008 | dword of section 1 or 9 of a model |
| [`model-files-cm-ca-fcp-property-values.tsv`](model-files-cm-ca-fcp-property-values.tsv) | 60,762 | model and property id: the value the getter returns |
| [`model-files-cm-ca-fcp-property-sites.tsv`](model-files-cm-ca-fcp-property-sites.tsv) | 46 | code site passing a property id |
| [`model-files-cm-ca-fcp-property-selector.tsv`](model-files-cm-ca-fcp-property-selector.tsv) | 34 | index of `0x003204E0` and the property it reads |
| [`model-files-cm-ca-fcp-direct-readers.tsv`](model-files-cm-ca-fcp-direct-readers.tsv) | 30 | code site reading a section's offset through the record's payload |
| [`model-files-cm-ca-fcp-points.tsv`](model-files-cm-ca-fcp-points.tsv) | 17,056 | section 6 point of a model |
| [`model-files-cm-ca-fcp-block10.tsv`](model-files-cm-ca-fcp-block10.tsv) | 613 | section 10 block of a model |
| [`model-files-cm-ca-fcp-palette-variants.tsv`](model-files-cm-ca-fcp-palette-variants.tsv) | 60 | section 5 animation entry of a model |
| [`model-files-cm-ca-special-bones.tsv`](model-files-cm-ca-special-bones.tsv) | 740 | `.cm` outside `weapon`: its special-id bones |
| [`model-files-cm-ca-ftr-nodes.tsv`](model-files-cm-ca-ftr-nodes.tsv) | 27,561 | `@FTR` node: key, parent, flags and pool indices |
| [`model-files-cm-ca-for-records.tsv`](model-files-cm-ca-for-records.tsv) | 1,275 | `@FOR` record: key, selectors per part and scale |
| [`model-files-cm-ca-fdm-keys.tsv`](model-files-cm-ca-fdm-keys.tsv) | 30,023 | `@FDM` key: its position in the key table |
| [`model-files-cm-ca-fte-textures.tsv`](model-files-cm-ca-fte-textures.tsv) | 2,127 | `@FTE` texture: sizes, format and pixel data offset |
| [`model-files-cm-ca-ftr-values.tsv`](model-files-cm-ca-ftr-values.tsv) | 27,561 | `@FTR` node of every `.cm`: the stored pool values of its bind matrix, translation and angles |
| [`model-files-cm-ca-fct-palettes.tsv`](model-files-cm-ca-fct-palettes.tsv) | 1,972 | `@FCT` palette: sizes, data offset, grey pages, the largest channel spread of each page and the SHA-256 of its colours |
| [`model-files-cm-ca-fct-palette-colours.tsv`](model-files-cm-ca-fct-palette-colours.tsv) | 1,377,728 | one colour of one page of one distinct palette content |
| [`model-files-cm-ca-fct-palette-contents.tsv`](model-files-cm-ca-fct-palette-contents.tsv) | 1,512 | one distinct palette content: its SHA-256, sizes and how many palettes use it |

| Column | Table | Meaning |
|---|---|---|
| `folder`, `version`, `size`, `content_length`, `entries` | files | the kind folder, the container version, the file's bytes, `+0x08` and the container's count `+0x0C` |
| `sha256` | files | the SHA-256 of the whole file |
| `entry_set` | files | the entries' tags in index order; a run of one tag is written `tag xN` |
| `bound_id` | files | the bound id whose `cm` names the `.cm`, or whose `lane_files` name the `.ca`; `-` for a `.ca` no lane names |
| `index`, `offset` | entries | the entry's index in the offset table (the slot in a version-1 `.ca`) and its offset in the file |
| `tag`, `kind`, `length`, `count`, `name` | entries | the entry header's `+0x00`, `+0x04`, `+0x08`, `+0x0C` and `+0x10` |
| `slot`, `row`, `column` | ca-slots | the slot, and for a slot below 80 × rows its row and column (slot = row × 80 + column); `-` for the slots after them |
| `fcp_byte00`, `fcp_byte01`, `fcp_sections` | heads | `@FCP` payload bytes `+0x00` and `+0x01`, and the sections whose offset is not 0 |
| `fcp_section2_length`, `fcp_event_map`, `fcp_version` | heads | payload `+0x24`, the six bytes at `+0x2C` and the version byte `+0x32` |
| `fcp_26_2b`, `fcp_33_39` | heads | payload bytes `+0x26`–`+0x2B` and `+0x33`–`+0x39` |
| `ftr_nodes`, `ftr_pool_offset`, `ftr_extra_slots` | heads | `@FTR` `+0x30`, `+0x34` and `+0x38` |
| `for_records`, `for_31`, `for_table_b_stride`, `for_options` | heads | `@FOR` bytes `+0x30` to `+0x33` |
| `for_table_a`, `for_table_b`, `for_records_offset` | heads | `@FOR` `+0x34`, `+0x36` and `+0x38` |
| `for_lod_distances`, `for_lod_highest`, `for_lod_d0_cm`, `for_lod_d1_cm` | heads | `@FOR` `+0x3A`, `+0x3B`, `+0x3C` and `+0x3E` |
| `for_table_a_bytes`, `for_table_b_bytes` | heads | the bytes of table A and of table B, up to the next table |
| `fdm_30`, `fdm_keys_offset`, `fdm_keys`, `fdm_34_4f` | heads | `@FDM` `+0x30`, `+0x32`, the key count, and the bytes from `+0x34` to the key table |
| `fte_always_slots` | heads | the texture slots listed after the count at `@FTE` `+0x30` |
| `path`, `section`, `offset`, `bytes`, `hex` | fcp-section-bytes | the model, the section, its offset in the payload, its span, and its bytes |
| `slot`, `offset`, `bits`, `float` | fcp-slots | the dword's number in the section, its offset in the payload, its bits, and the same bits as a float. A slot holding words or an integer keeps its bits here |
| `property`, `origin`, `bits`, `value` | fcp-property-values | the id; `stored` or `default`; the dword used; the value as a float, an integer, or the byte the id selects, before any run-time scale |
| `site`, `call`, `getter` | fcp-property-sites | where the id is loaded, the call that takes it, and the getter or wrapper called |
| `mode`, `section`, `byte`, `min_version`, `default_slot`, `slot` | fcp-property-sites | the id's fields as above; `byte` is the byte of a mode 3 id |
| `default_bits`, `default_value` | fcp-property-sites | the default table's entry for the id |
| `index`, `after` | fcp-property-selector | the index of `0x003204E0` and what it does to the float it reads; the other columns are as in fcp-property-sites |
| `scale`, `use` | fcp-property-sites | what `0x003E6150` does with the value (`-` for a getter that does not scale), and what the value is for, with the page that says so; `-` where no page names a use |
| `site`, `section`, `fields` | fcp-direct-readers | where the section's offset word is read, the section, and the field offsets taken from it in the same run of code; `-` where the code passes the address on |
| `point`, `id`, `bone`, `word_02`, `position_bits`, `position` | fcp-points | the point, its id, its bone, the word `+0x02`, and the three floats as stored and in decimal |
| `bits_08`, `float_08`, `byte_10`, `ratio`, `raw` | fcp-block10 | float `+0x08`, byte `+0x10`, their quotient as `0x003AF44A` stores it, and the whole block |
| `palette`, `variant`, `list_slot`, `entry_offset`, `entry_in_section`, `entry` | fcp-palette-variants | the palette, the position in its list, both payload offsets, whether all `0x30` bytes lie in the section, and the entry's bytes |
| `section`, `offset`, `span`, `length` | fcp-sections | the section, its offset in the payload, the bytes to the next section or the payload's end, and the length for section 2 (`+0x24`) and section 8 (`0x10` + count × `0x1D0`) |
| `section_offset`, `slot`, `bone` | fcp-attachment-slots | section 3's offset in the payload, the slot from 0 to 31, and the stored `u16` bone |
| `bone_state`, `ftr_nodes` | fcp-attachment-slots | `none` for `0xFFFF`, `node` below the model's `@FTR` node count, `past_nodes` at or past it, and that count |
| `bone_key`, `bone_parent` | fcp-attachment-slots | the node's key and parent as in ftr-nodes; `-` when `bone_state` is not `node` |
| `position`, `position_bits` | fcp-attachment-slots | section `+0x40` for the slot: three floats, then their stored bits in hex |
| `angles`, `angles_bits` | fcp-attachment-slots | section `+0x240` for the slot: three floats, then their stored bits in hex |
| `scale`, `scale_bits` | fcp-attachment-slots | section `+0x1C0` for the slot: the float, then its stored bits in hex |
| `special_bones_0_31`, `special_bones_104_106` | special-bones | as in [`weapon-bones.tsv`](weapon-bones.tsv): the set entries of section 1's table at `+0x14C` and of `+0x3A`–`+0x3E`, as "id: bone", or `-` when every entry is `0xFFFF` |
| `node`, `number`, `record` | ftr-nodes | the node's position, the node number of its `+0x40` table word, and its record offset in the entry |
| `key`, `parent`, `byte_03`, `flags` | ftr-nodes | the key as `0x00409250` reads it, the parent (`-` for no parent), record byte `+0x03` and the flags `+0x04` |
| `pool_indices`, `pool_index_list` | ftr-nodes | the record's u16 pool indices in stored order: one for each of flag bits `0x80000000`, `0x400000` and `0x20000000`, sixteen for `0x200000`, and one for each translation and angle bit; the list fills every record |
| `key`, `parent`, `flags`, `inline_id` | ftr-values | as in ftr-nodes; `key` is the inline id when flag bit `0x40000000` is set, `inline_id` that word, `-` without the bit |
| `bind_matrix` | ftr-values | the sixteen pool dwords for flag bit `0x200000` (`0x004094D0`), in stored order, as hex; `-` without the bit. They are the stored values, not a matrix rebuilt from the other columns. The matrix is the node's inverse bind matrix, equal to the skeleton matrix of the mesh's bone [`s<N>_`](../PhyreEngine/phyre-asset-files.md) |
| `translation`, `angles` | ftr-values | for nodes with flag bits `0x200100` both set: the pool dwords that `0x00409300` reads for x, y and z (bits `0x800000` to `0x2000000`) and for the three angles (bits `0x4000000` to `0x10000000`), hex, `-` for a clear bit |
| `index_400000`, `index_20000000` | ftr-values | the pool dword named by the index for that flag bit, hex. `0x004092A0` returns the first; the second is the value as stored |
| `index_80000000` | ftr-values | the u16 stored for flag bit `0x80000000`, as hex. `0x00409300` and `0x004094D0` step past it, and it can exceed the pool, so neither routine uses it as a pool index |
| `record`, `key`, `selectors_0`, `selectors_1`, `selectors_2` | for-records | the record's position, its key, and the selector counts of parts 0, 1 and 2 at `+0x05`, `+0x06` and `+0x07` |
| `scale`, `part_0`, `part_1`, `part_2` | for-records | float `+0x18`, and the selector bytes of parts 0, 1 and 2 at `+0x20`, `+0x40` and `+0x60`, as many as the part's selector count, separated by spaces; `-` when the count is 0 (815 rows for part 1) |
| `bytes_01_04`, `bytes_08_17`, `bytes_1c_1f`, `bytes_80_df` | for-records | record bytes `+0x01`–`+0x04`, `+0x08`–`+0x17`, `+0x1C`–`+0x1F` and `+0x80`–`+0xDF` (`-` when all zero) |
| `position`, `key` | fdm-keys | the key's position in the table and the key |
| `vram_bytes`, `width`, `height`, `format` | fte-textures | record `+0x00`, `+0x04`, `+0x06` and `+0x08` |
| `upload_width`, `upload_height`, `upload_bytes`, `pixel_offset` | fte-textures | record `+0x0A`, `+0x0C`, `+0x14` and `+0x18`; each texture's pixel data is its upload bytes long, and the next starts where it ends |
| `dword_1c` | fte-textures | record `+0x1C` |
| `vram_bytes`, `palette_bytes`, `colours`, `upload_width`, `pages`, `upload_height` | fct-palettes | record `+0x00`, `+0x02`, palette bytes / 4, `+0x04`, `+0x05` and `+0x06` |
| `dword_08`, `data_offset`, `data_bytes` | fct-palettes | record `+0x08`, `+0x0C`, and the bytes of the four pages inside the entry |
| `grey_pages`, `page_spreads`, `sha256` | fct-palettes | the pages on which every colour has equal red, green and blue, the largest max − min channel difference over each page's colours, pages 0 to 3 (both `-` when the pages do not fit), and the SHA-256 of the data bytes |
| `content`, `page`, `colour` | fct-palette-colours | the content's number from fct-palette-contents, page 0 to 3, and the colour's place in the page |
| `byte0`, `byte1`, `byte2`, `byte3` | fct-palette-colours | the colour's four stored bytes, in decimal: red, green, blue, as the `grey_pages` column reads them, and alpha |
| `content`, `sha256` | fct-palette-contents | the number the colour rows use, and the `sha256` of the palette table |
| `palette_bytes`, `colours`, `data_bytes`, `palettes` | fct-palette-contents | the record's palette bytes, palette bytes / 4, the bytes present in the entry, and how many of the 1,972 palettes hold this content |

## Loader behaviour

### Binding a model row

- `0x00504E70(sub, bank, root, tag, name)` looks the tag up in the given bank entry and, when that fails,
  searches the bank for an entry with the tag and name (`0x00409FA0`).
- The first lookup matches the name too: `sub +0x10` gets the offset `0x00409A30(entry, tag, name)` and
  word `sub +0x00` the entry's id word (`0x00504EA3`, `0x00504EAE`); a null entry gives the offset −1
  (`0x00504E90`). On −1 the index `0x00409FA0(root, tag, name)` goes to word `+0x00` (`0x00504EC9`), and the
  offset is looked up again in the entry `0x00409F50(root, index)` gives (`0x00504EDE`).
- `0x00504940` stores the container pointer at `+0x1F8` and the `@FEF` section at `+0x230`.
- The container is `0x004096C0` of the bank entry for word `+0x1F0` with the offset `+0x200`
  (`0x0050496E`), and it is copied to `+0x48` (`0x005049C9`). The `@FEF` section is `0x004096C0` of the same
  entry when its first word equals word `+0x228`, else of the entry `0x00409F50` gives for `+0x228`
  (`0x00504981`, `0x00504991`), with the offset `+0x238` (`0x005049A7`).
- `0x00504F00` walks the `@FOR` records for the requested key: a match is stored at `+0xB8`; otherwise
  the first record's key, or 0. The option number is kept at `+0xB9` when it is below `@FOR +0x33`,
  else 0. `+0xB3` gets the LOD distance count plus one, and the row's flags `|= 3`.
- The `@FOR` entry is the low 32 bits of the container pointer `+0x1F8` plus the offset `+0x208`, summed in 32
  bits, and absent for an offset of -1 (`0x00505036`-`0x00505063`). A key of `0xFF` counts as no match, and a first
  record's key of `0xFF` gives 0 (`0x005050A2`-`0x005050C8`).
- A negative option number also gives 0 (`0x005050EA`), and without a `@FOR` entry `+0xB3` is 1 and `+0xB9` 0
  (`0x005050D6`, `0x0050510F`-`0x00505127`).

### @FCP

- `0x002EDBD0(id)` takes a render id: -1 returns 0 (`0x002EDBD4`-`0x002EDBE0`), and the record is
  `[0x022C6F28]` + id × `0x740` (`0x002EDBE6`-`0x002EDBF1`). A null record, a record whose `+0x284` is 0 and a record whose
  word `+0x408` is `0xFFFF` return 0 and store nothing (`0x002EDBF8`-`0x002EDC1F`).
- Otherwise it takes the container `0x00409F50` returns for word `+0x408` (`0x002EDC21`-`0x002EDC33`), looks
  `@FCP` up in it by tag and the record's 32-byte name at `+0x3C` (`0x002EDC44`), and stores the
  payload (`+0x30`) at record `+0x400`, or 0 when absent; it then jumps to `0x003E55F0`, which returns
  it (`0x002EDC71`). Nothing is checked or converted on load, and every later read goes through the getters.
- The bank is the descriptor at `+0xD90` of the root that record `+0x10` names (`0x0020E600`,
  `0x002EDC21`-`0x002EDC2C`), and the lookup gives `0x00409660` the tag `0x50434640`, `@FCP` (`0x002EDC3C`).
- `0x003E5AD0(record, id)` returns the bone for a special id: ids below `0x20` from section 1's table,
  `0x104`–`0x106` from `+0x3A`–`+0x3E`, `0xFFFF` otherwise.
  It also gives `0xFFFF` for a record with no `@FCP` (`+0x400` = 0, `0x003E5AD7`-`0x003E5ADA`).
- `0x003E5AD0`'s id compare is signed (`0x003E5AEA jge`), so a negative id reads below section 1's table, and section
  1's offset is not tested for 0, so an absent section 1 reads the table at payload `+0x14C`. The section address
  is formed in 32 bits (`0x003E5AE1 add eax, r8d`, then `movsxd`), so it is right only for a payload address below
  `0x80000000`.
- `0x0041E5B0(record, state, event)` scans the six-byte event map, stopping at a byte whose low seven
  bits are `0x7F`, and returns the index of the byte whose low seven bits equal the event, or −1.
  Bytes with the high bit set match only when state is 0, and are tried first.
- A record without `@FCP` returns −1 at once (`0x003E55F0` gives 0, `0x0041E5CF`). The event compared is
  `event & 0xFFF` (`0x0041E5D4`), so only an event whose low 12 bits are below `0x7F` can match.
- `0x004292B0` plays a motion id of `0x1000` or more through it when the record has its own motion
  entries (`+0x2F8` set): the index picks `@FMC` entry `[+0x2FA] + index` of the model's own
  container, keeping the id's top four bits. An id with no match plays nothing and returns −1.
- Its arguments are `(record, source, direct)`: the id is word `+0x3B4` of `source`, the record itself
  from `0x0042AC65` and `[arg + 8]` from `0x0042E215`. "Set" means word `+0x2F8` is not `0xFFFF`
  (`0x004292C4`). An id of `0x104A` is first rewritten to `0x103D` in `source` (`0x004292F7`-`0x004292FC`),
  and the state is the signed low two bits of `source` byte `+0x40B` (`0x00429315`-`0x0042931B`).
- A match calls `0x00423B10(record, data, (id & 0xF000) | ([+0x2FA] + index))`, with the data
  `0x004096F0` gives for the entry of word `+0x2F8` in the root's descriptor `+0xD90`
  (`0x0042933A`-`0x0042936E`), and returns its result.
- No match runs `0x00422C20(record)` (`0x00429378`), which releases the presentation entries `+0xC4` and
  `+0xC8` (`0x00422C50`, `0x00422C7E`), setting each to -1 (`0x00422C55`, `0x00422C83`) and, after `+0xC4`, word `+0xCC`
  to `0xFFFF` (`0x00422C5B`); it then clears `+0x68`, `+0xD8`, `+0xE0`, `+0xF0`, `+0xF8` and `+0x23C` and bit
  `0x40` of byte `+0xC0`, and stores `0x0020E620(0)` at `+0x69C` (`0x00422C8D`-`0x00422CC1`).
- Without own entries, or for an id below `0x1000`, a `direct` of 0 returns −1 (`0x00429398`); otherwise
  it calls `0x00423B10(record, address, id)` with the address `0x0020E600` decodes from `source` `+0x390`
  and returns its result (`0x004293B5`).

- `0x0041F340` copies section 8 (head plus `count × 0x1D0` bytes, `0x003E6D10`, `0x003E6CF0`) into the
  record's block at `+0x2FC`, offset `+0x300`, writes the record index at the copy's `+0x08` and
  calls `0x0051D220` on it. The first call ever builds a 64 × 64 8-bit texture and a 256-colour
  palette from the image embedded at `0x01F2B340` (`0x00184140`, `0x001837A0`); every call clears the
  copy's byte `+0x06` and `0x02CA8428`.
- The section 8 draw stage `0x00425DC0` runs `0x0051D1D0` first: it zeroes the 16 KiB of emulated VU
  memory at `0x02064E30`, calls `0x00258EE0(3)`, and binds the embedded texture and palette to GS
  addresses `0x2A00` and `0x2E00` (`0x002D7E00`).
- The image's three statics: `0x02CA842C` is 1 once it is made, which `0x0051D220` tests (`0x0051D226`) and
  sets (`0x0051D27A`); `0x02CA8430` keeps the 64 × 64 texture's handle from `0x00184140` (`0x0051D295`) and
  `0x02CA8438` the palette's from `0x001837A0` with 256 entries (`0x0051D2B9`). `0x0051D1D0` binds the two
  (`0x0051D1F2`, `0x0051D206`).
- Authored command `0x1F` reaches `0x003E6710(record, on)`: on runs `0x0051DB60` on the copy, which sets
  its word `+0x06` to 1 and resets each entry (`+0x14` = 1.0, `+0x00` and `+0x10` cleared, `+0x1C4`
  = 1, `0x100` bytes at `+0xA0` zeroed); off runs `0x00519720`.
- `0x0051D2F0(copy, value)` keeps the low two bits of `value` in byte `+0x07` and masks the byte's
  other bits with `value >> 2`; `0x00421280` passes 4 or 6.

### Section 8: sprites along a bone point's path

Section 8 is in 28 models. A record draws a chain of textured sprites that follow the recent path of a point on one
bone. The bind turns the copy on for every model that has one (`0x0042001D`). Command `0x1F` can also switch it, and no
shipped command does: none of the 1,583,764 has that id.

[`fcp-section8-records.tsv`](fcp-section8-records.tsv) has the 53 records, and
[`fcp-section8-fields.tsv`](fcp-section8-fields.tsv) has each field with its readers and writers, and
[`fcp-section8-models.tsv`](fcp-section8-models.tsv) has the 28 models.

Head, `0x10` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` |  | record count |
| `+0x02` | `u16` |  | first record, `0x10` in all 28 |
| `+0x04` | `u16` |  | `0x12` in all 28; the seven routines that take the copy do not read it |
| `+0x06` | `u8` |  | on; the authored byte is cleared at bind (`0x0051D2C0`) |
| `+0x07` | `u8` |  | bit `0x1` no update, bit `0x2` no draw |
| `+0x08` | `u32` |  | render record index (`0x0041F5F3`) |
| `+0x0C` | `f32` |  | alpha factor, from render record `+0x49C` (`0x0051DBE0`) |

Record, `0x1D0` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` |  | sample count, 0 to 16 at run time |
| `+0x004` | `u16` |  | sprite steps (`0x002F08A2`) |
| `+0x008` | `u16` |  | phase B steps (`0x002F08A8`) |
| `+0x00C` | `u32` |  | bone key, matched on nodes with flag `0x100` (`0x00372800`) |
| `+0x010` | `f32` |  | sprite spacing at run time (`0x0051DAFA`) |
| `+0x014` | `f32` |  | alpha multiplier, 1.0 at switch-on (`0x0051DB97`) |
| `+0x018` | `f32` |  | phase A colour step |
| `+0x01C` | `f32` |  | phase B colour step |
| `+0x020` | `f32[3]` |  | phase A first corner S, T, Q |
| `+0x02C` | `f32` |  | phase A half size |
| `+0x030` | `f32[3]` |  | phase A second corner S, T, Q |
| `+0x03C` | `f32` |  | spacing decay per update (`0x0051DABA`) |
| `+0x040` | `f32[3]` |  | phase B first corner S, T, Q |
| `+0x04C` | `f32` |  | phase B half size |
| `+0x050` | `f32[3]` |  | phase B second corner S, T, Q |
| `+0x05C` | `f32` |  | spacing cap (`0x0051DAD3`) |
| `+0x060` | `u32[4]x2` |  | phase A colour, start and end |
| `+0x080` | `u32[4]x2` |  | phase B colour, start and end |
| `+0x0A0` | `f32[16][4]` |  | history at run time: world point, w the distance moved |
| `+0x1A0` | `f32[3]` |  | the point, in the bone's space |
| `+0x1B0` | `f32[3]` |  | vector of the spacing test (`0x0051D689`) |
| `+0x1C0` | `f32` |  | spacing scale (`0x0051D131`) |
| `+0x1C4` | `u32` |  | update alternator at run time |
| `+0x1C8` | `u8[8]` |  | zero in all 53; moved by the load copy (`0x0041F5E7`); no routine reads them |

Each update shifts the sixteen history rows and adds the bone point, and the sample count rises to at most 16. The
spacing grows by the newest distance when the test on `+0x1B0` passes. It is then multiplied by the decay and capped
at `+0x5C` and at the path's total length (`0x0051DA60`-`0x0051DAFA`).

The draw sends the record's first `0x1A0` bytes to VU program `0x002F0280`. The program places `+0x04` sprites at equal
spacing along a curve through the samples. The first `+0x04 - +0x08` use phase A and the rest phase B, and in each
the colour moves from start to end by its step per sprite. In all 53 records each step is 1 / (phase steps - 1), or
0 for a phase of one sprite. Sizes are scaled by the render record (`0x003E5770`), and the spacing by `+0x1C0`.

`+0x1BC` is zero in all 53 and loaded with `+0x1B0` without being used. Which texels of the embedded image a sprite
shows follows from its S, T and Q and is outside these tables.

The rows `+0x1B0` is tested against are read from `0x022D9360`-`0x022D938B` (`0x0051D6E7`-`0x0051D73F`), which `0x0051D310`,
`0x00421D70`, `0x004220F0` and `0x003710E0` do not write. They hold what other routines left (`0x0040BD35`, `0x00535767` and
`0x0054290E` among the stores), so the test is given as code. The distance the update subtracts comes from `0x022D904C`,
whose only reference is that read (`0x0051D930`) and which lies in zero-filled `.data`.

### @FTR

`0x003712E0` sizes the skeleton as `(count × 0x149 + [+0x38]) × 2` rounded up to 16 bytes, plus the
section 2 length: `count` nodes of `0x290` bytes, then `count + [+0x38]` u16 slots. `0x00372820`:

- matches the model name against `skeletonmapping.bin` (see [add-motion tables](add-motion-tables.md))
  and keeps the last match at skeleton `+0xB0`;
- builds every node. Each parent gets its first child at node `+0x274` and siblings chain through
  `+0x272`; a node without a parent joins node 0's sibling chain. A node with flag bit `0x100` is built from
  its pool values and its number is appended to the u16 list after the nodes; any other node starts
  at the identity;
- fills the `[+0x38]` extra slots with `0x7FFF`;
- copies section 2 after the core (`0x003729BD`) and runs `0x003713C0`, which hands it to `0x003E1C50`.
- `0x003713C0` first re-encodes the bone array `+0x84` from the block handle `+0x80` (`0x003AB7F0`,
  `0x003713EC`). With a resource word `+0x16` of `0xFFFF` it stops there (`0x003713F6`). Otherwise it
  re-resolves the skeleton resource `+0xA0` (`0x004096C0` of the entry `0x00409F50` gives for `+0x16` in the
  descriptor `+0x18`, offset `+0x1C`, `0x00371424`) and clears `+0x94` (`0x00371435`).
- When `+0xA0` is not null and the section 2 offset `+0x90` is above 0 (`0x00371443`, `0x0037144C`), it
  points `+0x94` at the copy, `[+0x84] + [+0x90]` (`0x00371469`), and calls `0x003E1C50` on it
  (`0x00371487`).

The binder also accepts kind 0, records of `0x4C` bytes from `+0x30` with the parent at `+0x20`; no
shipped file uses it.

### @FOR

- `0x00504840(entry, key)` returns float `+0x18` of the record with that key, or 1.0. `0x00420480` calls it
  with record byte `+0x5C`, and the result is the record scale that `0x003E6150` applies.
- `0x004201F0(record, view)` runs only when the entry starts with `@FOR`. With a non-zero distance count it builds the
  windows `{0, d0 × 0.01, d1 × 0.01, 1.0e8}` in metres, or uses the float array `+0xA0` of the view (of the record
  when `view` is null) when byte `+0xC0` of that same object has bit `0x1` set.
- The level is the first window that holds the view depth (float `+0x208`; a negative depth gives
  level 0), capped at `+0x3B`. It stores `(count + 1 − level) / (count + 1)` at record `+0x2A4`, so 1.0
  is nearest, then calls `0x00421280`.

### @FDM

`0x005048A0(record, key)` returns the position of the key in the key table, or −1.

It returns −1 for a null record (`0x005048AB`), a row index word `+0x64` of `0xFFFF` (`0x005048C7`), no model
row (`0x004780B0` of the root's `+0xDA0` table, `0x005048E3`), no `@FDM` (offset `+0x20C` of −1, `0x005048EE`)
and a key table offset `+0x32` of 0 (`0x00504901`). The entry is `low32([+0x1F8] + [+0x20C])` of the row
(`0x005048F6`). Otherwise it compares the key with the table's keys in order
and returns the first match's position (`0x00504916`-`0x00504922`); a count of 0 or less gives −1 (`0x00504914`).

### The draw builder

`0x0053AB50` resolves table A, table B and the records from `+0x34`, `+0x36` and `+0x38`
(`0x0053B33A`–`0x0053B35A`) and takes the record whose key equals row `+0xB8`. For each part and each of
its selector bytes `s` it reads `A = tableA[3s + part] + [+0x32] × option` and the pair
`tableB[2A]`, `tableB[2A + 1]` (`0x0053B4B6`–`0x0053B4EC`): the first is an `@FTE` texture slot, the second
an `@FCT` palette. The texture slots listed at `@FTE +0x30` are added to every draw (`0x0053B45A`). The
VRAM bytes `+0x00` of the selected textures are summed before upload (`0x0053B5B0`).

### The texture slot cache

Uploaded model textures are tracked in a cache of 256 entries of `0x30` bytes at `[0x02CA8450]`,
which the root-bank builder `0x0041E3A0` allocates through `0x005211F0` (every entry's index and key set
to `0xFFFF`) and forgets through `0x00521300`. The live count is `0x02CA8458` and the next search start
`0x02CA845C`.

- `0x005210F0(key)` returns the entry already holding the key and adds a reference (`+0x24`), or takes
  the next free entry from the search start, clears its word `+0x24` through `0x00540FC0` and then
  sets it to 1; it returns `0xFFFF` when 256 are in use.
- `0x00521250(index)` drops a reference and frees the entry at 0. `0x00521290(key)` finds an entry by
  key; `0x005212E0(index)` returns entry `index & 0xFF` when its first word still equals `index`.
- `0x00504520(instance, slot, texture)` binds an `@FTE` texture to the instance's slot word
  `+0x100 + 2 × slot`: it releases the old entry, takes one for the texture's key (`+0x1C`), and
  copies the texture's size and register words with the base-2 logarithms of width and height.
- `0x00504800(instance, slot)` returns the slot's width and height as one dword once the entry is
  marked uploaded (bit `0x1` of `+0x1C`), else 0. `0x00521320` clears that mark and the dword `+0x14`
  (`0x00521344`) in all 256 entries.

### The upload area

The draw places the selected textures in GS memory through two windows over the addresses from
`12 × width × height` of the GS frame (`0x022D8EAC`, `0x022D8EB4`) up to `0x3C0000`. Window `i` has a
low cursor `0x02EBA460[i]` and a high cursor `0x02EBA468[i]`: window 0's are `0x02EBA460` and `0x02EBA468`,
window 1's `0x02EBA464` and `0x02EBA46C` (`0x00537AA0` indexes them by window). `0x00537B10` sets window 1's
(`0x00537B77`, `0x00537B84`-`0x00537B91`).

- `0x00537AA0(window, size, end)` takes `size` bytes from the low end (0) or the high end (1) and
  returns their start, or 0 when they do not fit; `0x00537AF0(window, size)` only tests the fit.
- `0x00537B10(0, end)` puts window 0's end back to its start value and copies it into window 1;
  `0x00537B10(1, end)` copies window 0's current end into window 1. `0x00477F20` calls `0x00537B10(0, 0)`
  and `0x00537B10(0, 1)` before it draws the instances (`0x00477F2D`, `0x00477F39`).
- When a model's textures and palettes do not fit window 1, `0x0053AB50` resets window 1 from window
  0 and clears every cache mark (`0x0053B67E`–`0x0053B699`). It then takes textures from the low end
  and palette pages from the high end (`0x0053B761`, `0x0053BB73`).

The draw writes its transfers and state into the current GS command buffer (`0x005044B0` returns
`0x02EBEFC0 + 0x18 × [0x02EBEFF0]`), and when fewer than a block's bytes remain it closes the buffer
with `0x00504450`: a `{0x10000000, 0}` record, then the flip `0x003A1DB0`. `0x00504490` only flips.

- `0x0053D4B0` writes a part's alpha and depth test: registers `0x47` and `0x48` with the reference `alpha ×
  [0x02CA81DC]`, at most `0x80` and raised to `[0x01F2CA90]` for an instance with `+0xF8` set whose `0x003E56A0` entry has
  bit `0x8` of `+0x134`.
- In `0x0053D4B0` the alpha is the instance's byte `+0xBC` when the draw's `+0x8700` is non-zero and the instance's
  `+0x244` bit `0x20` is clear, and otherwise the part's bits under mask `0xFE`. With instance `+0x08` bit `0x8` it
  writes `0x34000` instead.
- `0x0053D140` writes a material block: a tag (`0x10000008`, `0x50000005`), two register words per mode (`0x44` and
  `0x42`/`0x43`, or `0x4A`), per-texture pairs from the material when its flag byte has bit `0x4` and, in the `0x44`
  mode only, bit `0x1`, and the two texture handles.

### Palettes

- `0x00504D30(row, index, sub, out)` makes a palette resource of `bytes / 4` colours for palette
  `index` (below `+0x0C` and 16), keeps it in the row's 16 slots at `+0x140`, and, when the pair
  `(index << 4) | sub` is not yet in the row's 20-byte map at `+0x180` and the map has a free byte, records it
  there.
  - For such a new pair it also files the caller's `0x30`-byte animation entry on that palette through `0x003CCC20` (`0x00504E3C`; one of
  128 slots at `[0x02B47798]`, linked into the palette's record by its priority byte `+2`) and keeps the returned
  handle at `+0x194 + 4n` (`0x00504E41`).
  - It returns at once for a row without `@FCT` (offset `+0x21C` of −1, `0x00504D5A`) or a `sub` of 16 or
    more (`0x00504D80`). The palette resource is made only while slot `index` is −1:
    `0x003CCB60(0, 0, colours)`, with a null source and destination (`0x00504DB3`), then
    `0x003CD7C0(handle, 1)`, which sets the record's bit `0x40` (`0x00504DC5`).
  - A handle of 0 is kept as −1 and ends the call (`0x00504DD3`, `0x00504DEB`). A free map byte is one of
    `0xFF` (`0x00504E16`), and the handle goes into the entry's `+0x04` before `0x003CCC20` (`0x00504E38`).
- `0x005044D0(row, index)` returns the page in use: data offset + `row[+0xBA]` × palette bytes, added to the `@FCT`
  section (the low 32 bits of `+0x1F8` plus `+0x21C`, summed in 32 bits), with the page byte signed
  (`0x005044E1`-`0x0050450D`). It returns 0 for a row without `@FCT` (`+0x21C` of −1) or an index not below the
  palette count `+0x0C` (`0x005044D9`, `0x005044ED`).
- `0x00504D20(row, page)` sets `+0xBA`. `0x00428CD0` sets it on a render record, its first child `+0x08` and the
  rest of that child's tree (`0x0042EF90`). The status step `0x00470780` passes 3 (`0x0047082A`, `0x004708CE`,
  `0x0047091B`, `0x00470A43`), as do the Stone install in `0x0046FD00` (`0x0046FDD4`) and Stone's step `0x00470AA0`
  (`0x00470AFE`); `0x00470230` and `0x00470B70` give it 2 in their flash frames (`0x00470330`, `0x00470CEB`).
- The type `0xD0` effect body `0x00465CD0` passes its byte `+0x235` while its flag word `+0x232` has bit `0x400`
  (`0x00465F0C`-`0x00465F4A`); the other callers give it 0.

### Palette animation

A palette resource is also registered for animation in one of 32 records of `0x40` bytes at
`[0x02B47790]` (`0x003CCB60(source, destination, colours)`, from `0x00504D30` and the map's palette parser
`0x00468160`): the handle is `serial << 8 | slot` (serial `0x02B47774`, wrapping to 1 past `0xFFFFFF`),
and the record joins a list (head `0x02B47778`, tail `0x02B47780`, count byte `0x02B47770`).

`PaletteRecord` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | opCount | operation count |
| `+0x01` | `u8` | flags | any of bits `0x3F` set: `+0x08` and `+0x10` are handles (`0x0036B130`); `0x40` keep running; `0x80` run |
| `+0x02` | `u16` | colourCount | colour count; `0x003CD840` and `0x003D2B60` copy only 1, `0x10` or `0x100` colours |
| `+0x04` | `u32` | handle | serial << 8 \| slot |
| `+0x08` | `void*` | source | source palette |
| `+0x10` | `void*` | destination | destination palette |
| `+0x18` | `void*` | previous | previous record |
| `+0x20` | `void*` | next | next record |
| `+0x28` | `void*` | firstOp | first operation |
| `+0x30` | `void*` | lastOp | last operation |
| `+0x38` | `u32` | overrideStamp | `0x00181DD0`() when `0x003CCC20` last added an operation; 0 skips the record during an override |

`PaletteOperation` (`0x50` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | kind | 1-8 |
| `+0x04` | `u8` | paletteSlot | palette slot |
| `+0x08` | `u16` | length | length in steps (0 = no end) |
| `+0x0A` | `i16` | delay | start delay |
| `+0x10` | `u16` | period | 0 = no period |
| `+0x15` | `u8` | mode | 0 wrap, 1 back and forth |
| `+0x20` | `u32` | secondPalette | second palette handle (kinds 4 and 8) |
| `+0x30` | `u32` | handle | operation handle |
| `+0x34` | `u16` | time | time |
| `+0x36` | `u16` | phase | phase |
| `+0x38` | `void*` | next | next operation |
| `+0x40` | `void*` | previous | previous operation |

The 128 operation records are at `[0x02B47798]`.

`0x003CCF20(step)`, each simulation step from `0x00258D70` and `0x00258E40`, walks the records with bit `0x80`
set (clearing it unless bit `0x40` is set): it copies the source colours into `0x02B477A0` (`0x003CD840`),
counts each operation's delay down or its time up by `step`, takes the phase (the time modulo the
period, or reflected on odd periods in mode 1), applies the operation, and writes the result to the
destination (`0x003D2B60`). An operation past its length is removed.

The kinds call `0x0050AC20`,
`0x00506B40`, `0x005080A0`, `0x0050A100` (with the second palette), `0x00509BB0`, `0x00507490`, `0x00508C90` and
`0x00507120` (with the second palette).

`0x003CD2C0(handle)`, from the draw builder `0x0053AB50`, does the same once into `0x02B4A7A0` without
moving time. `0x003CD6C0(handle)` returns the record; `0x003CD7C0` and `0x003CD7F0` set its bits `0x40` and `0x80`;
`0x003CD590` detaches its operations and clears its count; `0x003CD5D0` unregisters it; `0x003CD650(handle)`
removes one operation from its record.

Both walks skip a record whose `+0x38` is 0 while `0x00181DD0()` is non-zero (`0x003CCF6A`-`0x003CCF77`,
`0x003CD2DD`-`0x003CD2EA`); a record with `+0x38` non-zero runs either way, still only with bit `0x80` of `+0x01`
(`0x003CCF60`-`0x003CCF64`). `0x003CCC20` stores `0x00181DD0()` in `+0x38` each time it adds an operation
(`0x003CCE6B`-`0x003CCE76`).

## Modding notes

- Keep every entry's name equal to the container's: the model row finds each entry by tag and name.
- `@FCP` must be entry 0 and keep version `0x0A`; a lower version byte makes ids with a higher minimum
  version return the built-in defaults.
- A model without section 9 gets the built-in defaults for every battle radius and turn rate.
- In `@FTR`, list a parent before its children, keep node 0 the root, and set flag bits `0x100` and `0x200000`
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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 35 calls with 12 other topics</summary>

**Enemy AI and gambits** (explained on [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [glossary](../Engine-Core/glossary.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x003014C0`, `0x00301AD0`, `0x00305AB0` |

**Battle actions**

| Function | | Functions |
|---|---|---|
| `0x003204E0` | is called by | `0x00320D70` |
| `0x00377C20` | is called by | `0x002FFA60`, `0x002FFCF0`, `0x002FFF50`, `0x00305110`, `0x00305230`, `0x00305430`, `0x00307300`, `0x0030C010`, `0x0030D160`, `0x0030D600`, `0x0030DA30`, `0x0030F760` |
| `0x00377C20` | is also called by | `0x00311B20`, `0x00311CF0`, `0x00312FA0`, `0x00313CD0`, `0x00313DB0` |

**Battle actions** (explained on [action definition row](../Battle-Actions/action-definition-row.md), [quickenings and summons](../Battle-Actions/quickenings-and-summons.md), [force fight mode](../Engine-Core/force-fight-mode.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md))

**Battle actions** (explained on [action phases](../Battle-Actions/action-phases.md), [game over](../World-Areas-And-Travel/game-over.md), [frame update order](../Engine-Core/frame-update-order.md), [identifier spaces](../Engine-Core/identifier-spaces.md))

**Battle actions** (explained on [call signatures](../Engine-Core/call-signatures.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

**Gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [enmity](../Enemy-AI-And-Gambits/enmity.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00307D10`, `0x0030A8A0`, `0x0030C210`, `0x0030D9A0` |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00253C70` |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00313A00` |

**Items, equipment, shops and licenses** (explained on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00309FB0`, `0x0030FD10` |

**Rewards: EXP, LP, gil and loot** (explained on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00312280` |

**Status effects and KO** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x0030E360`, `0x0030F690`, `0x00310DB0` |

**World, areas and travel** (explained on [party control modes](../Engine-Core/party-control-modes.md), [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | calls | `0x003148F0` |
| `0x00377C20` | is called by | `0x002342F0` |

</details>

---

[Model lifecycle →](model-lifecycle.md)
