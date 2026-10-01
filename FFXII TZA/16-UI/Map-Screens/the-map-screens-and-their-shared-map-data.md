---
system: The map screens — track map, location map, world map, a field-time map container, and the map-data widget they share
category: 16-UI
status: DOCUMENTED — UQ-156 answered 2026-09-26 (the 0xBC08 protocol arm by arm, the four things each page draws, the containers' lifetime); UQ-157 answered 2026-09-15; UQ-158 answered 2026-09-17; MS-1, MS-2 and MS-3 answered 2026-09-29 (FABLE); MS-4 answered 2026-09-30 (SWE2-STRUCT for OPUS, d526b865b); prose residue closed 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 20): the track container's zeroing, the track closer's callers, the marker walkers' substitution, the two drawers' differences and 003BC160's scan read from the image, and 003BC160's test and store corrected (consumer-check) (owner re-status 2026-10-01, OPUS; documented_rule READY)
owner_layer: CodeDomain:UI (map screens)
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: screens identified by the readers of their uisize.json layout keys (key -> global join in ../Layout-Parameter-System/members/layout_key_slots.py,
    readers by rip-relative scan); objects by their constructors; membership of the map-data family by the rip references to
    its singleton 02B457E0 plus the closure of callees called only from members (members/wm_family.py, raw E8/E9 index)
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: falsification-pass-GN161
  crossref_clean: false
  reopened_count: 0
---

# The map screens and their shared map data

> **Three map screens and one field-time container share a single map-data widget.** The **track map** is opened from
> field input, and its code reads the `TrackMap*` layout keys. The **location map** reads `LocaMap*`, and the **world map**
> reads `WorldMap*`. Track map, location map and the field-time container are instances of one `0x179E0`-byte container
> class. Each holds two in-place `0xBC08`-byte pages and flips between them. All of them read area and field data through
> the `0x278`-byte map-data widget at `02B457E0`, which loads `menumap_world`, `menumap_location` and `menumap_common`.
> That widget and the callees only it uses are **108 functions, 104 of them on the frontier**.

**PARTIAL.** Read: which code is which screen, the objects and who creates them, the container's page flip, and the
membership of the map-data family with the screens that reach each member. Not read: what each page draws, who drives the
field-time preloader (§2.6), and the role of most members. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: read since. What each page draws is UQ-156, answered 2026-09-26 (§7); the preloader's driver is MS-4, answered 2026-09-30 (§7); every member's role is in §4.)*

*(2026-09-13, FABLE. It grew out of the `lmap` native reader:
[lmap page §10](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md).)*

## 1. What the player sees

- The **track map**: the map opened from field input (`002B6220`), styled by the TrackMap colour, scale and icon keys.
- The **location map**: the area map with "map jump" icons. Its data is the area's field graph ([lmap §10](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md)).
- The **world map**: the map with a cursor, map names, region text and lines (`WorldMapLineScale`).
  Its mesh geometry is `worldmap/meshdata.mg` (kind 7 `0xA8`, requested by `00562F90` and by the
  license-board-side widget `00561390`) — layout in
  [mg-worldmap-mesh.md](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mg-worldmap-mesh.md).

These descriptions come from the key names and the data the screens read. What each screen draws is not read (§7). *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: read since; UQ-156, answered 2026-09-26, §7.)*

## 2. Native mechanism

### 2.1 How each screen was identified

`001CA600` binds ~~222~~ 226 of `uisize.json`'s keys by one pattern (corrected 2026-09-27; the three float keys go through a
second object, see the layout page). It reads each key and stores the value through a pointer at
UI-object `+0x3B00 + slot`, and `001AF470` fills those pointers with the addresses of fixed globals. Joining the two gives
**key → global** for all ~~222~~ 226 keys ([`layout-key-slots.tsv`](../Layout-Parameter-System/members/layout-key-slots.tsv); the readers of every key: [layout parameters](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md)). The layout
parameter page lists the key names ([ui-layout-parameters](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md)).
A rip-relative scan of the map keys' globals then finds their readers. Apart from `001AF470` itself and the black-band
fades, they are:

| keys | globals | readers | screen |
|---|---|---|---|
| `TrackMapScale`, `TrackMapIconScale` | `01E0CE70`, `01E0CE74` | `002B7B80` | track map page |
| `TrackMapColorR/G/B/A`, `ExtraTrackMapJumpIconOffsetX/Y` | `01E0CE60`–`01E0CE6C`, `0209E5A8` / `0209E5AC` | `002B8EE0` | track map drawer |
| `LocaMapBlackBandH` | `01E0C3E0` | `002BA700` (also the fades `0027EF00`, `002804E0`) | location map container |
| `BaseMapJumpIconScale`, `ExtraLocaMapJumpIconOffsetX/Y` | `01E0CE80`, `0209E5D8` / `0209E5DC` | `002BCB00` | location map drawer |
| `WorldMapWidth`, `WorldMapHeight` | `01F2CAA4`, `01F2CAA8` | `00552250`, `005528C0` | world map widget and page |
| `WorldMapCursorOffsetX/Y` | `01F2CAAC`, `01F2CAB0` | `00550A00` | world map cursor |
| `MapNameOffsetX/Y`, `RegionTextPosX/Y` | `02CA8F34`, `01F2CABC`, … | `00553AE0` | world map name text |

The `WorldMapBlackBand*` keys (`01E0C3C0`, `01E0C3C4`) are read by `0027EF50` and `002804E0`. Those are the fullscreen
transition's black bands, not a map screen.

### 2.2 The objects

| object | size | singleton | procedure | page procedure | created by |
|---|---:|---|---|---|---|
| track map container | `0x179E0` | `0209E5C0` | `002B7590` | `002B7B80` | `002B6350` (`002B6394`–`002B63A8`; page `002B6427`–`002B6474`) |
| location map container | `0x179E0` | `0209E5F0` | `002BA700` | `002BAF80` | `002B9D30` (`002B9D71`–`002B9D85`; page `002B9E0C`–`002B9E59`) |
| field-time map container | `0x179E0` | `02B47760` | `003CB650` | `003CB4F0` (`003CB807`) | `003CB440` (`003CB46A`–`003CB491`) |
| world map widget | `0x188` | `02CA8F38` | `00552250` | `005528C0` (`00552301`) | `00550400` (`00550444`–`00550455`) |
| map-data widget | `0x278` | `02B457E0` | `003BC4E0` | — | `003BC450`, called by `002BA040` (`002BA15C`) and `003CB440` (`003CB4CC`) |

All three containers also install the small child procedure `002BA240`. Its only three references are one `lea` in each
container procedure.

### 2.3 The container class: two page slots and a flip

A container keeps two `0xBC10`-byte page slots at `+0x1B0` and `+0x1B0 + 0xBC10`. Bit 2 of the word at `+0x179D2`
selects the current page: `+0x1B0 + 0xBC10 × bit 2` (`002BA168`–`002BA183`). Opening a page while the container exists
is done in `002B9DB9`–`002B9E59`, and the track map constructor has the same shape:

1. `00273A20` is called on a page slot; a non-zero result skips the open (`002B9DEB`–`002B9DF2`).
2. Bit 2 is flipped in place (`not`, `xor`, `and 4`, `xor`; `002B9E22`–`002B9E35`).
3. The page procedure is constructed with size `0xBC08` in the slot the new bit selects, through `00245000` (`002B9E3C`–`002B9E59`).

The page's `+0xBBF0` is set to the container (`002B9E79`). So each open builds the next page in the other slot, while the
previous page stays in memory for the transition. The word `+0x179DA` holds the first argument (`002B9D96`).

### 2.3a The message protocol of the two pages, parsed

**Both page procedures accept the same 42-id message space and handle the same 17 of it.** Added
2026-09-16 (OPUS) against `UQ-156`, which lists both as *unparsed* in the handler census. The row is
**not** closed: it also asks what each page *draws*, and that is not answered here.

Each procedure opens with the same prologue — the container backpointer `+0xBBF0` read first (§2.3),
then a two-level switch on the message id:

```
002B7BDF  mov   edx, dword ptr [rdx]                   id = the message's first dword
002B7BE1  lea   eax, [rdx - 1]
002B7BE4  cmp   eax, 0x29                              ids 0x01..0x2A are in range
002B7BE7  ja    002B8E21                               out of range -> the default arm
002B7BED  lea   r8,  [rip - 0x197BF4]                  r8 = 00120000, the image base
002B7BF6  movzx eax, byte ptr [r8 + rax + 0x198EB0]    index byte table
002B7BFF  mov   ecx, dword ptr [r8 + rax*4 + 0x198E70] case RVA table
002B7C07  add   rcx, r8
002B7C0A  jmp   rcx
```

**The tables are reached as `image base + displacement`, never as a materialised address**, which is
why neither body shows a reference to them under an `E8`/`E9`/`LEA`/pointer sweep — the same idiom the
absence-claim gate carries an `imagebase` instrument for.

| | `002B7B80` | `002BAF80` |
|---|---|---|
| body | 4,847 B | 4,810 B |
| index table | `002B8EB0` | `002BC28C` |
| case table | `002B8E70` | `002BC24C` |
| default arm | `002B8E21` | `002BC20D` |
| distinct arms | 16 (one is the default) | 16 (one is the default) |
| ids handled | **17** over 15 arms | **17** over 15 arms |

**Handled ids, identical in both:** `0x01`, `0x02`, `0x04`, `0x08`, `0x09`, `0x0A`, `0x0E`, `0x0F`, `0x10`,
`0x13`, `0x14`, `0x21`, `0x25`, `0x26`, `0x27`, `0x28`, `0x2A` — with `0x08`/`0x09` sharing one arm and
`0x13`/`0x14` sharing another, in both procedures.

**The other 25 in-range ids reach the default arm**, the same code an out-of-range id reaches: `0x03`,
`0x05`–`0x07`, `0x0B`–`0x0D`, `0x11`, `0x12`, `0x15`–`0x20`, `0x22`–`0x24`, `0x29`. Being *in range* is
not being *handled*, and a census that counted the range would report 42 where the protocol is 17.

**Why the agreement matters.** Two independently compiled 4.8 KB bodies selecting the same 17 ids, with
the same two pairs sharing arms, is the signature of one widget vocabulary implemented twice — not two
screens that happen to overlap. What differs is what each arm *does*, which is the half of `UQ-156`
that stays open. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: that half is UQ-156, answered 2026-09-26; §7 reads every arm.)*

*Method: the index and case tables were read at the displacements above and every decoded arm checked to
land inside its own body; the `ja` target is present among the arms in both. A first version of the check
also asserted the tables lie outside the body — true of `002B7B80` by accident, false of `002BAF80`, whose
case table sits inside its declared extent, so that assertion was dropped rather than tuned.*

### 2.4 Who opens and closes them

| entry | what it does | reached from |
|---|---|---|
| `002B6220` | if `0209E5C0` is null: track map container `002B6350(arg, 5)`, then `+0x179D2 \|= 0x500` (`002B6249`) | `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` (`00253DE2`) |
| `0028E630(x)` | location map `002B9D30(0, 6)`, `002B9FE0(x)`, then `002BA040` | `002804E0` (`002805C3`) |
| `0028E660(x)` | location map `002B9D30(x, 5)`, `002BA020`, `002BA000`, then `002BA040` | the fullscreen procedure `0027F5D0` (`0027F6AF`, `0027F9EC`) |
| `0028E690(req)` | `req.u16[0]` 0 or 3: nothing (`0028E6AB`–`0028E6B8`); 1: location map `002B9D30(req.u16[2], 5)` + `002BA040` (`0028E6BE`–`0028E6D2`); otherwise **world map**: `0209BE80 +0x10FA2 = 1`, `00550400(1, +0x10FA6)`, `00550510(+0x10F68 bit 12)`, `00550540` with a record `{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}`, `00550610` (`0028E6EA`–`0028E770`) | the close request `002814E0` (`00281579`, `002817CA`, `00281844`) |
| `0028E790` | world map from the saved `0209BE80 +0x10FA2` / `+0x10FA6` / `+0x10FA8`, after destroying the field-time container | `0027F5D0` (`0027FA2C`), `00281ED0` (`002823B8`), `002804E0` (`00280566`) |
| `002BA040` | location map setup. With `+0x179D2` bit 10 set, it copies 32 bytes at `+0x190` from the field-time container (`002BA095`–`002BA0B1`). Otherwise it destroys that container (`003CB410`, `002BA080`) and fills `+0x190` itself through `00404060` (`002BA0BF`–`002BA0E0`). Then, with bit 10 still clear, it creates the map-data widget (`002BA0F8`–`002BA15C`). With bit 10 set it instead sets bits 0–1 and calls the container's own procedure (its qword `+0`) with messages 16 and 32 (`002BA102`–`002BA14E`). It destroys nothing and creates no map-data widget. | the three location-map entries above |
| `003CB440` | creates the field-time container and, in it, the map-data widget | `00253A30` (from `ActorSystem_InitializeManagerRuntime`, `0026D374`), `00251F40` (from `00254A90`, which `ActorManager_RunFieldRuntimePass` calls, and from `00255330`, `00254E70`, `00255020`) |
| `003CB410` | destroys the field-time container (`00245020`, clears `02B47760`) | `00253A30`, `0028E790`, `002BA040`, `00281ED0` |

### 2.5 The map-data widget and its family

The widget itself is documented with its file formats: [lmap page §10](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md).
It covers the loader `003BC2D0`, the release on message 18, the record and point accessors, and the field → area locator
`003C0380`.

**Membership.** There are **77** functions with a rip reference to `02B457E0`, plus **31** callees called only from members:
**108** functions and 26,595 bytes. [`members/wm_members.tsv`](members/wm_members.tsv) lists each with the screens whose
roots reach it within four caller hops:

| screens reaching the member | members |
|---|---:|
| location + track | 30 |
| world only | 23 |
| location + track + world | 17 |
| field + location + track | 14 |
| field + location + track + world | 9 |
| field + location | 3 |
| field + location + world | 2 |
| location only | 2 |
| the containers' child `002BA240` | 2 |
| widget-internal (loader, procedure, helpers reached only through them) | 6 |

**So the family is shared infrastructure rather than one screen's code.** 75 members serve more than one screen; 23 are
reached only from the world map and 2 only from the location map. The closure-only members outside `003BB…`–`003C2…` (`002543F0`, `002550E0`,
`00255200`, `0035D520`, `0037EB90`–`00380170`, `004022F0`, `00473CC0`) are exclusive by caller set only; §4 reads each —
three turn out to be general helpers with one map client (`0035D520`, `004022F0`, `00473CC0`), the rest do compute on the
map tables.

### 2.6 The map image cache and the field-time preloader

The map-data widget keeps **two cache slots** of `0xA8` bytes at `+0x120` and `+0x1C8`, keyed by a sub-location index in
byte `+0x10` (`003C0CF0`, `003C21C0`). `003C1F00(widget, pool, &args, index)` fills a free slot by requesting **kind 7 id
`0x142 + index`** (`003C1FE9`–`003C208D`). The kind-7 path array resolves that id to `menumap_subNN.bin`, the per-sub-location
`sloc` image container ([sloc](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md)).
`003C0CF0(index)` reports 0 for no slot, 1 while the slot's `+8` is still null, and 2 once it is loaded.
`003C21C0(index)` evicts every other slot through `003C22B0`, and `003C2200(index)` tails into `003C26C0`, which
populates the matching slot's `+0x18` child-label array (§4 — §2.6's earlier "releases" was wrong; release is
`003C2210`/`003C22B0`).
Two slots match the generator header's "double buffer" ([lmap §10.6](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md)).

**The field-time container's page `003CB4F0` is that cache's preloader**, not a drawn page. Message 14 stores the
index from `msg[+8]` in `02B47768` and polls `003C0CF0`. At 2 it destroys itself; at 1 it waits. Otherwise it opens a
resource pool scope (`00249580` … `00249410`) and tries `003C2190` (load). If that fails it evicts the other slot
(`003C21C0`) and retries, then calls `003C21B0` (a tail call to `003C2210` on the widget, not read) *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: `003C2210` is read in §4: it releases both cache slots)* and retries once more (`003CB581`–`003CB62F`). Message 16
releases the slot (`003C2200`) and destroys the page. Message 18 sends message 44 through `00275440`. So from actor
init and the field pass onward, the current sub-location's map images are being loaded before any map screen opens.

## 3. Key addresses

| address | role |
|---|---|
| `0209E5C0` / `002B7590` / `002B7B80` / `002B8EE0` | track map container, procedure, page, drawer |
| `0209E5F0` / `002BA700` / `002BAF80` / `002BCB00` | location map container, procedure, page, drawer |
| `02B47760` / `003CB650` / `003CB4F0` | field-time map container, procedure, page |
| `02CA8F38` / `00552250` / `005528C0` | world map widget, procedure, page |
| `02B457E0` / `003BC4E0` | map-data widget and procedure |
| `0028E630`, `0028E660`, `0028E690`, `0028E790`, `002B6220` | openers |
| `001CA600` / `001AF470` | layout key reader / key-slot pointer installer |

## 4. What each member computes

*(2026-09-14, FRONTIER, `FABLE-REQ-SWE2-FRONTIER-MAP-MEMBERS`.)* All 108 members of
[`wm_members.tsv`](members/wm_members.tsv) read whole. Each row gives the role the body computes from
the map-data widget `02B457E0` (or its shared tables `020927C0`/`020927D0`/`02AED490`) and one interior
instruction where the mechanism is visible. Vocabulary follows [lmap §10](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md):
the widget's `+0xD8`/`+0xE0`/`+0xE8` slots hold the three kind-7 resources (`0xA2`/`0xA3`/`0xA4`); inside them,
a `word[+8]`/`word[+0xA]`/`word[+0xC]`/`word[+0x10]` field is a byte offset to a counted sub-table;
a record's `byte[+9]` is its count and `word[+0xA+i*2]` its offset to the `{countA, countB, ...}` point
sub-block; `+0x120`/`+0x1C8` are the two `0xA8`-byte record cache slots. The 24-byte point entry fields used
below: `+0xC` field id, `+0xE`/`+0x12`/`+0x14`/`+0x16` persistent/encoded gate ids, `+0x10` kind+flags
(`>>2 & 0xF` = kind nibble, `&0xFC0` = encoded-id flag), `+0x11`/`+0x14` link-selector bytes.

The dominant pattern: **four gate queries wrap every table entry** — `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`
(`0032A8A0`) on `word[+0x14]`/`+0x12`/`+0xE`, `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`) on `word[+0x16]`,
`002543F0` (u16-list → encoded-id presence) on kind bytes, and `003C08B0` on destination indices — and every
row-builder or enumerator is a filter over one of the widget's counted sub-tables.

*Added 2026-09-18 (FABLE): what the persistent gate ids are called.* The accessor's bank is the one the script verbs `setmapjumpgroupflag`, `releasemapjumpgroupflag` and `ismapjumpgroupflag` reach - 12,900 literal uses over 328 ids in the shipped scripts, 52 of them pre-set on a new game ([the flag banks](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) section 4c and its per-id census). So an entry's persistent gate is, in the game's own vocabulary, a **map-jump-group flag**, and the zone scripts are what open and close it. ~~Whether each gate id in this data appears among the scripts' 328 was not checked.~~ **Checked 2026-09-18 (FABLE): the join holds, and it says what one of the fields is for.** [lmap_gate_join.py](members/lmap_gate_join.py) parses `menumap_location.bin` with the native layout (control: it reproduces the 384 A and 111 B point entries) and intersects the point entries' persistent gate words with the scripts' flag census ([lmap-gate-join.tsv](members/lmap-gate-join.tsv)). **Word `+0x12`: 51 distinct ids, 2 of them threshold-form and 49 inside the bank's `2`..`0x1FF` range, and all 49 are flags a shipped script sets - and not one of the 49 is ever released.** So `+0x12` is a one-way *revealed* flag: a point appears on the map once some zone script has set its flag, and stays. Word `+0xE`: 11 distinct ids - 2 in range (both script-set, never released), 4 in the threshold form with bit 14 set (story-progress gates, not flags) and 5 with bit 15 set, a form this page does not read. Word `+0x14`, by contrast, is **not** a flag id in a point entry: 78 of its 79 distinct values lie outside the bank's range, which agrees with this page's other reading of it as a link-selector byte; the `PersistentFlag(word[+0x14])` rows of section 4 belong to the other tables they name.

### World-map members (23 — reached only from the world map)

| member | what it computes | interior cite |
|---|---|---|
| `003BCAF0` | mode `ecx` → writes `+0xC9`, scans the `+0xD8` `word[+0xC]` 8-byte link table, and ORs each matching entry's two node bytes into the `+0x270` bitset | `003BCB63` `or dword ptr [r9 + 0x270], r8d` |
| `003BCCA0` | `(cx=link index, rdx=8-byte link entry, r8=out)` → resolves the `word[+0xA]` 0x1C-stride destination row, gates it through `003C08B0`, and emits a 16-byte descriptor `{cx, linked byte, table w0/w2, src w4/w6, resolved w0/w2}` | `003BCD84` `mov word ptr [r15], si` |
| `003BD040` | `(cx=node index, rdx=out)` → builds the 0x28-byte world node descriptor: copies the entry's coords/kind bytes, `002543D0` → `byte[+3]`, name via `002543A0`/`002F9860`, and `003BD480`'s flags word at `+0x1C` | `003BD12D` `call 003BD480` |
| `003BD1B0` | the destination-list pass: sets `+0xCA`, iterates the `word[+0xA]` table, keeps entries passing `003C08B0` + `003C0C50`, emits each via `003BD040`; a second pass over the kind-6 script table appends script-driven nodes | `003BD2BB` `call 003BD040` |
| `003BD480` | `(cx=node index)` → the availability flags word: current-field test (`003148F0`→`00264F90`→`00254380`), `003C1680`, `002543F0`, `0032A8A0`/`00309EC0` on the entry's gate ids, `003C0A00`, `003C08B0` | `003BD5C4` `call 0032A8A0` |
| `003BF7C0` | `(rcx=0x18-stride rows, dx=kind, r8=mode)` → enumerates the `+0xE8` kind table's `0x3B` entries filtered by `00254380`-group and `003C12B0`, emitting each via `003BF6C0`; kind 6 additionally ORs `0x20` when `003C0E30` hits | `003BF882` `call 003BF6C0` |
| `003BFB60` | selector-byte chase: seed `[rcx+8+dl]`, hop through the `+0x28`-stride row list matching `dl`, resolving via `003BD040`, until `0xFF` or `[rbp+1]`; returns the row index | `003BFBFB` `call 003BD040` |
| `003BFC70` | directional nearest pick over the `0x28`-stride world rows: projects `rcx`'s `+4/+6` and each row's `+3/+5` to floats, keeps the `003BD6F0` best | `003BFD8C` `call 003BD6F0` |
| `003BFE10` | `(cx)` → the `+0xD8` `word[+8]` group-table header `{index, 002F9920 name ptr, 003BFEA0 flag}` | `003BFE6B` `call 002F9920` |
| `003BFEA0` | is `ecx` the group byte of the `word[+0xA]` entry indexed by the active field's `00254380` kind index | `003BFEFE` `cmp ebx, eax` |
| `003BFFF0` | `(dx=group, rcx=out u16 list)` → enumerates the `word[+0xC]` block's `byte[+2]==0` link entries, `003C08B0`-gated, `003BCCA0`-translated, writing each matched index | `003C0072` `call 003BCCA0` |
| `003C00C0` | same block and filter, but emits full 16-byte `003BCCA0` descriptors at `rbp + r8*16` | `003C0146` `call 003BCCA0` |
| `003C0180` | same block filtered by link-kind `byte[+2]==dx`, `003C08B0`-gated, `003BCCA0`-emitted | `003C0214` `call 003BCCA0` |
| `003C0250` | `+0xD8` `word[+0x10]` table (`{u32 count | 4-byte {key,…,u16 val}[]}`): byte key `cx` → paired u16, −1 on miss | `003C029B` `movzx eax, word ptr [r9 + rax*4 + 4]` |
| `003C0450` | `(edx=kind, rcx=0x18-stride rows)` → every `+0xE8` entry with `byte[+0]==edx` passing `003C12B0`, emitted as `{idx, kind byte, 002F9920 ptr, 003C05F0 flags}`; requires ≥2 instances when `r8b` and `edx`≠current kind | `003C0571` `call 003C12B0` |
| `003C08B0` | **the destination gate**: `(cx)` → `word[+0xA]` entry `cx` must have `byte[+0xA]≠0` and `word[+8]` within `00265270`'s bound, then dispatches on `+0xCA`: mode 0/1 → true, 2 → `+0x270` bitset, 3 → `003C0B70`, 4 → `003C0BE0`, 5 → `003C0A00`; else a `003C0D70` kind scan | `003C09AA` `bt ecx, edx` on the `+0x270` row loaded at `003C09A3` |
| `003C0A00` | mode-5 gate: scans the kind-6 script table (`00473BB0`, count `+0xCB`) for an entry whose `[+0x24]` matches `cx`, then a second scan by `00254380` group | `003C0A70` `call 00473BB0` |
| `003C0B70` | `word[+0xA]` entry `cx` → `PersistentFlag(word[+0x14])` | `003C0BC2` `call 0032A8A0` |
| `003C0BE0` | `word[+0xA]` entry `cx` → `BattleEncodedId_DispatchQueryMode0Value` mode-0 on `word[+0x16]` | `003C0C31` `call 00309EC0` |
| `003C0C50` | the `word[+0xA]` table's trailing 8-byte entries (after the `count`×0x1C rows): entry `cx` → `PersistentFlag(word[+0])` | `003C0CA4` `call 0032A8A0` |
| `003C0D70` | kind `ecx` (<0x3B) → 1 when mode `+0xCA`==0, `ecx`==current field's kind, or `edx`==0; else some `+0xE8` instance `byte[+0]==ecx` must pass `003C12B0` | `003C0DFA` `call 003C12B0` |
| `003C0E30` | field `ecx` → 1 iff a type-1 kind-6 script entry's `00264F90` field equals `ecx` | `003C0EBC` `call 00264F90` |
| `003C1D70` | `word[+0xA]` entry `dx` → `002493D0` loads kind-7 resource `0xE8 + byte[+0xB]` with the args in `r8` | `003C1DD9` `call 002493D0` |

### Location + track members (30)

| member | what it computes | interior cite |
|---|---|---|
| `00255200` | `003779F0` map index → 32-byte entry at `020927C0 + 0x224`; 1 iff any byte is nonzero | `00255230` `cmp byte ptr [rax + rdx], cl` |
| `0037EB90` | gated on `02AED490`'s `+0xE0` bit 0x100: iterates `00473B70`/`00473BB0` script rows until `[rsp+0x34]≠0`, returns `[rsp+0x2C]`; `0046B180` bounds the `+0xEA`-word −0x80 index | `0037EC30` `call 00473BB0` |
| `003BCDE0` | `(record, point, link pair at r8, out r9)` → resolves a link destination: `PersistentFlag` gate on `r8+0x10`, point enabled, `003BCBA0` bit 0xB, pair-words matched against `word[+0xC]`, `003C1180` probes, then finds the destination point (`003C0340` scan, `003BDFF0` kind redirect, `003C1980`) → `{record, point or 0xFF, 3 pair words}` | `003BCF39` `call 003BF430` |
| `003BD9F0` | gated `+0xD0` bits 8|9: counts the `+0xCB` kind-6 entries (`00473BB0`) whose `[+0x2C]` field matches `r14w`, conditioned on `[+0x38]` by `bpl` (0: must be 0, 1: must be nonzero); copies the first hit's 0x1C row to `rbx` | `003BDA7C` `call 00473BB0` |
| `003BDB30` | `003BF920` field → the `r15b`-th matching kind-6 entry; `+0xD0` bit 0x400 adds a `00473CC0` row fetch; emits `{u16, qword}` | `003BDC5F` `call 00473CC0` |
| `003BDCD0` | same enumeration, count-only: kind-6 entries with `[+0x34]≠0`, `[+0x2C]`==`003BF920` field, `[+0x38]≠0` | `003BDD8D` `inc esi` |
| `003BE2D0` | field `ecx` → `003C0380` record → searches both `+0x120`/`+0x1C8` cached records' `word[+8]`-offset u16 lists for `word==ecx` → `base + word[+4]` | `003BE346` `cmp ecx, ebp` on the u16 loaded at `003BE343` |
| `003BE3A0` | the draw-list builder: `(kind esi, record edx, mode r8b, out)` sets `+0xCA`, special `+0xD0` bits for kinds 0xD/0x2F, `003C1A20` collects enabled points, `003C2320` emits each 0x30-byte row relative to the record origin; kind 6 attaches a `003BD9F0`/`00473CC0` name row | `003BE554` `call 003C2320` |
| `003BE680` | record `ecx` → its sub-block's C entry `byte[+2]` → returns `word[+0]`, writes `word[+2]`/`word[+4]` to `r10`/`r8` | `003BE6EB` `movzx ecx, word ptr [rdx + 4]` |
| `003BE700` | record `ecx` → index of the 24-byte A/B sub-entry whose `+0x11` kind byte == `edx`, −1 on miss | `003BE7CC` `cmp ecx, ebp` on the `+0x11` byte loaded at `003BE7C6` |
| `003BE810` | selector-byte chase: seed `[rcx+r8b+8]`, each hop resolves via `003BDDE0` + `003BCBA0` bit-0xB gate, next selector from the entry's `+4..+7` bytes chosen by `bpl`; `0xFF` terminates | `003BE8C1` `call 003BDDE0` |
| `003BE950` | directional nearest pick over a 0x18-stride row list: per row `003BCBA0` bit-0xB gate, position via `003BF5E0` or the `0037EB70`/`002F9920`/`0029CD00` projection, `003BD6F0` directional score | `003BEC15` `call 003BD6F0` |
| `003BEC50` | field `ecx` → `003C0380` record → `003BF5E0` → returns the resolved position qword | `003BEC7C` `call 003BF5E0` |
| `003BECA0` | field `ecx` → same cached-record search as `003BE2D0` but returns `base + word[+2]`, the paired pointer | `003BED52` `movzx eax, word ptr [rdx + 2]` |
| `003BED70` | the record draw pass: iterates all `003C0340` points, kind nibble `[+0x10]>>2&0xF` → `003BE1E0` resolve or direct `003C18A0`/`003C0F70` gate, `003BF5E0` positions each, accumulates a bounding box; re-runs under `+0xD0` bit 0x800 when the record's `+0xE8` entry `byte[+1]` is set | `003BEE16` `call 003BF430` |
| `003BF520` | `(record ebp, field esi, kind edi)` → the cached record's `+0x18+idx*8` object slot whose `word[+0xA]`-offset u16 table entry matches `{field, kind}` | `003BF5D8` `mov rax, qword ptr [r9 + rcx*8 + 0x18]` |
| `003BF920` | `(record, point)` → the enabled point's `word[+0xC]` field id, `0xFFFF` if unavailable | `003BF973` `movzx eax, word ptr [rax + 0xc]` |
| `003BF9A0` | entry `{+0xC field}` → extended flags: `003BCBA0` base, bit 8 when field == `00264790`'s, kind-6 table scans → bits 5/6, `00377A40` → bit 9, `003C17E0` → bit 0xE | `003BFA4C` `call 00473BB0` |
| `003C02B0` | `+0xE8` kind-table index `ecx` → `{u16 idx, u8 kind, 002F9920 name ptr, 003C05F0 flags}` row | `003C030B` `call 002F9920` |
| `003C06E0` | 24-byte point entry → lock-state bits: `word[+0xE]`==0xFFFF → 1; `[+0x10]&0xFC0` → `BattleEncodedId_DispatchQueryMode0Value` mode 8 → {8,0x10}; else `PersistentFlag(word[+0xE])` → {2,4} | `003C070A` `call 0032A8A0` |
| `003C0740` | `(record, point)` → count of the record's 20-byte C entries (count `byte[+2]`) for which `003BCDE0` link resolution succeeds; gated on point availability + `003BCBA0` bit 0xB | `003C083F` `call 003BCDE0` |
| `003C0890` | stores `r9b` → `+0xCA`, tail into `003C0740` | `003C0897` `mov byte ptr [rax + 0xca], r9b` |
| `003C0CC0` | `+0xD0` bit 4 ∧ bit 6 → "page block processed" | `003C0CD8` `test cl, 4` |
| `003C0D30` | `(record, point)` → `003BF430`, then kind dispatch: A → `003C18A0`, B → `003C0F70` | `003C0D5E` `jmp 003C18A0` |
| `003C1070` | `(record, field)` → 1 when `field` is the current field (`00264790` override else `003148F0`) or when the record's C-entry u16 list holds `{field, current}` — the player-node test | `003C1126` `cmp ebp, eax` |
| `003C1180` | `(pair rcx, point entry rdx)` → link viability: `003C06E0`/`002543F0`/`00377A40`/`003C1070` gates, then a `00255150` geometric test of the entry's `003BF520` object against `rsi`'s rect | `003C127E` `call 00255150` |
| `003C1980` | A-entry → writes `003BCBA0` flags to `[r8]`, returns the `003C06E0`-decoded lock bit after `+0xE`/`0xFC0` evaluation | `003C19C7` `call 0032A8A0` |
| `003C1A20` | `(record edx, mode, list r9, origin r10)` → collects the record's enabled points into `{pos, entry*, sel}` triples, tracking the mode-selected coordinate; returns count + extremes | `003C1C26` `call 003BF5E0` |
| `003C2320` | emits one 0x30 draw row: entry coords + four selector bytes (`0xFF`-normalized), `PersistentFlag(word[+0x12])` → `+0x1C` bit 0, kind-0xD remap via `003BE700`, then `003BDDE0`/`003BE810`/`003BE950` fill the directional next-target bytes `+8..+B` | `003C253F` `call 003BDDE0` |
| `004022F0` | general helper, one client (`003BCBA0`): scans `rcx`'s element arrays (kinds 3..9 via `003DFBB0`/`003DFB50`) for an element whose `+8` word == `edx` (or ∈ {0x14, 0x17, 0x18} when `edx` is one) | `00402391` `movsx eax, word ptr [rax + 8]` |

### Location + track + world members (17)

| member | what it computes | interior cite |
|---|---|---|
| `002543F0` | `ecx` → the `020927D0` `[+0xC]`-offset u16 list entry → `BattleEncodedId_DispatchQueryMode0Value` mode-0 ≠ 0 | `00254424` `call 00309EC0` |
| `0037ED70` | tail thunk to `0037EB90` | `0037ED70` `jmp 0037EB90` |
| `003BCBA0` | point entry `rcx` → its state-flags word: `003C0380`+`003C1070` → bit 0 is-current-node; `00255200` → bit 0xA; `003C06E0` bit 3 → bit 4; else `00264F90`+`002543F0` → bit 1; `+0xD0`&0x800 → bit 15; `003BE2D0`+`004022F0` → bit 12/13 composite | `003BCBC3` `call 003C1070` |
| `003BDDE0` | `(record, point, outs r14/rbp/r15)` → walks the record's D-subentries whose `+0x11` kind matches the point's, reports the first `003C0D30`-enabled one (`{flag, index, ptr}`) | `003BDFB1` `call 003C0D30` |
| `003BDFF0` | record's last enabled point of D-kind `edx`: scans `003C0340` points for `([+0x10]>>2)&0xF==edx`, `003C0D30` enabled (or `+0xD0`&0x800 bypass), `003C06E0` bit 0 | `003BE100` `call 003C06E0` |
| `003BE1E0` | `(record, kind, out r8)` → `003BDFF0` then re-resolves the `+0xE0` D-subtable 24-byte entry at that index; index out via `[r8]` | `003BE1FD` `call 003BDFF0` |
| `003BF5E0` | `(widget rcx, record edx, field r8d, kind r9d, out r14)` → the cached record's matching `+0x18+idx*8` object plus the u16-table entry's resolved data pointer | `003BF6A5` `mov ecx, dword ptr [r8 + rcx*4 + 4]` |
| `003BF6C0` | kind `cx` (<0x3B) → 0x18-byte row `{kind, 00254380 byte, match count, last index, 00377870 ptr, flags{0:current,1:002543F0,0xE:003C0F00}}` | `003BF769` `call 00377870` |
| `003C05F0` | kind-table index `ecx` → flags word: bit 0 current-field kind, bit 1 `002543F0`, bit 5 `003C15B0`, bit 11 `!003C12B0`, bit 14 `003C1680`, bit 15 entry `byte[+1]` | `003C0670` `call 003C12B0` |
| `003C0F00` | kind `ecx` → 0 iff some `+0xE8` entry `byte[+0]==ecx` fails `003C1680` | `003C0F3F` `call 003C1680` |
| `003C0F70` | B-entry enablement: `PersistentFlag(word[+0x16])`; `+0xCA`==6 bypass; `byte[+0x14]` link → `003BDDE0` + `003BCBA0` bit 11; `+0xE8` kind → `002543F0`; `PersistentFlag(word[+0x12])` | `003C0FE0` `call 003BDDE0` |
| `003C12B0` | kind-table index `ecx` → enabled: `PersistentFlag(word[+2])`, `002543F0` on `byte[+0]`; else iterates that record's points through `003BE1E0`/`003C18A0`/`003C0F70` with `003BF5E0` positions — "does this kind have a drawable instance" | `003C13CB` `call 003BF430` |
| `003C15B0` | record `ecx` → 1 iff a type-1 kind-6 script entry's `003C0380` record equals `ecx` | `003C163C` `call 003C0380` |
| `003C1680` | record `ecx` → 1 iff none of its `countA+countB` points is ~~a B-entry~~ an **A-entry (zone, kind 0)** whose `word[+0xC]` fails `003C17E0` — `r8d` is 0 below `countA` (`003C1765`) and 1 above (`003C178A`), and `003C179D`/`003C17A0` skips the `+0xC` read for kind 1 *(corrected 2026-09-30, SWE2-CONTRACT's `lmap_readers.py` P5)* | `003C17A6` `call 003C17E0` |
| `003C17E0` | field `ecx` → progress test: `003779F0` index → `+0xE8` `word[+0xA]` entry `byte` threshold vs `003C4AD0`/`00255060` (current node) or `002550E0` level | `003C1850` `call 00255060` |
| `003C18A0` | A-entry enablement: `003BCBA0` flags + `+0xE`/`0xFC0` lock decode (bit 0x10 ∧ flags&0x401 → locked); globals `02B457D4`/`02B457D8`, `0037ED70` field match, or mode 6 + `0037ED80` bypass | `003C1931` `call 0037ED70` |
| `00473CC0` | general helper: `rcx`-indexed entry → two `0x8000`-flagged u16 offsets resolved to `[r8]`/`[r9]` pointers, returns `byte[+1]` count | `00473CDF` `movzx eax, word ptr [rcx + rax*4 + 4]` |

### Field + location + track members (14)

| member | what it computes | interior cite |
|---|---|---|
| `003BC160` | field→record driver: gated on `+0xC8`==1, `+0xD0`&0x100, `0037ED80`()==1; scans kind-6 entries for `[+0x20]`==1 ∧ ~~`[+0x34]`==0, writes `02B457DC`=(index≠0)~~ `[+0x34]`≠0, writes dword `02B457D8`=(index≠0) *(Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 20): `003BC20C` is `jne` to the hit after `cmp dword ptr [rsp + 0x34], ebp` with `ebp` = 0, and `003BC247` stores at `02B457D8`; see the `003BC160` interior citation near the end of the page)*, returns `003C0380([+0x2C])` | `003BC24D` `call 003C0380` |
| `003BC970` | releases the `+0xF8` page block and its `+0x108` processed copy, clearing `+0xD0` bits 2/6; no-op unless `+0xD0`&4 and (releasing-for-load or bit 0x40 clear) | `003BC9CA` `call 003697F0` |
| `003BD890` | `+0xF0` header `word[+6]` index into the `+0xF8` page block → `block + word[+8] + entry[idx*8+0x14]` | `003BD8CE` `movzx edx, word ptr [rcx + r8*8 + 0x14]` |
| `003BD950` | backward scan of `rcx`'s counted 8-byte entries for the first whose `word[+0]` passes `00265270` and `word[+2]` passes `PersistentFlag` — "deepest enabled" | `003BD9A1` `call 0032A8A0` |
| `003C0CF0` | cache-slot state for `ecx`: 0 absent / 1 while `+8` null / 2 loaded (§2.6) | `003C0D23` `cmp qword ptr [rax + 8], r9` |
| `003C1DF0` | rebinds the page block: `+0xE8` `word[+0xA]`-table tail (4-aligned) → `003BD950` deepest entry → `+0xF0`; `003BC970` frees the old block; loads kind-7 `0x496 + byte[+4]` → `+0xF8`; `+0xD0` &= ~0x40, |=4 | `003C1EBC` `call 00249210` |
| `003C1F00` | fills a free `+0x120`/`+0x1C8` cache slot with kind-7 `0x142 + edi` (`00249180`), stamps `+0x10`/`+0x12`, releases the old `+0x118`, optionally loads `0xE1 + byte[+1]` (§2.6) | `003C200D` `call 00249180` |
| `003C2190` | arg-permuting tail into `003C1F00` on the widget | `003C21A0` `jmp 003C1F00` |
| `003C21B0` | tail `003C2210` on the widget — release both cache slots | `003C21B7` `jmp 003C2210` |
| `003C21C0` | evicts the cache slot whose `+0x10` kind ≠ `ecx`, through `003C22B0` | `003C21F4` `jmp 003C22B0` |
| `003C2200` | tail `003C26C0(widget, ecx)` — **populate** the slot holding record-kind `ecx` (see correction below) | `003C2209` `jmp 003C26C0` |
| `003C2210` | releases both `+0x120`/`+0x1C8` slots: each `+0x13`-counted `+0x18+k*8` child via `0024A680`, then the block via `003697F0` | `003C227C` `call 003697F0` |
| `003C22B0` | one slot: same child-array + block release | `003C22DF` `call 0024A680` |
| `003C26C0` | `(widget, record-kind edx)` → the slot whose `+0x10`==edx: walks the record's `word[+0xA]` u32-offset table and **fills** each empty `+0x18+k*8` child — `0024A9E0` resolves two string pointers into `+0x110`/`+0x118`, `0017D2E0` formats (fmt `02185C28`), `0024A480` creates | `003C2824` `call 0024A480` |

### Field + location + track + world members (9)

| member | what it computes | interior cite |
|---|---|---|
| `0037F050` | `02AED490 == 0` — is the field map table absent | `0037F052` `cmp qword ptr [rip + 0x276e437], rax` |
| `00380170` | `ecx-0x80` ≤ 0x2C → `0046B180` map-table lookup, else −1 | `00380179` `call 0046B180` |
| `003BC260` | widget `+0xCC` word → `0046B240`/`00315DC0`/`00380170` probes, else `0046B180` — the id → table index used by every kind-6 scan | `003BC270` `call 0046B240` |
| `003BC3E0` | callback invoker: `call [rcx]` with a `{0x10, 0}` arg block — the widget's `+0xC0` notification hook | `003BC41E` `call rax` |
| `003BC9F0` | `(field cx, cb rdx)` → re-resolves `+0xCC`→`+0xCE` via `0037EDB0` and rebinds via `0037FD50` when the field table is loaded; else `0037F440`, else callback `0x102` | `003BCA95` `call 0037FD50` |
| `003BF430` | the point accessor (lmap §10): `(record, point)` → A or B 24-byte entry + kind tag in `[r8]` (0/1/3) | `003BF4D3` `lea rcx, [r10 + r10*2]` |
| `003BFF20` | `(record, field)` → scans the record's C-entry u16 list for `field`, returns the paired u16, −1 on miss | `003BFFBB` `cmp eax, ebx` |
| `003C0340` | record → `countA + countB` point count | `003C0366` `movzx eax, byte ptr [rcx + 1]` |
| `003C0380` | field → record index: iterates `+0xE8` kind entries `byte[+0]`==`00264F90(field)` group, `003BFF20` alias, then scans record points for `word[+0xC]`==target | `003C040A` `call 003BF430` |

### Field + location members (3)

| member | what it computes | interior cite |
|---|---|---|
| `003BC2C0` | `02B457E0 == 0` — widget-absent probe | `003BC2C2` `cmp qword ptr [rip + 0x2789517], rax` |
| `003BC450` | constructor: `00244F50` builds the `0x278` widget with proc `003BC4E0`, stores `02B457E0`; fails if it already exists | `003BC4A2` `call 00244F50` |
| `003C20D0` | one-shot clear of `+0x110` | `003C20E7` `mov qword ptr [rax + 0x110], 0` |

### Field + location + world members (2)

| member | what it computes | interior cite |
|---|---|---|
| `0037F160` | `02AED490`'s `+0xE0` bit 7 | `0037F173` `shr eax, 7` |
| `003BBFB0` | widget teardown: frees each flag-gated `+0xD8`/`+0xE0`/`+0xE8` resource and the `+0xF8`/`+0x108` page block; when bit 0x80 and the field tables are gone, `0037E4F0` + `00245020` destroy it | `003BC144` `call 00245020` |

### Location-only members (2)

| member | what it computes | interior cite |
|---|---|---|
| `003BD860` | `+0xD0` bit 6 ∧ `+0xF8` → returns `+0x108`, the processed page block | `003BD882` `mov rax, qword ptr [rax + 0x108]` |
| `003BF8E0` | `+0xE8` kind-table index `ecx` → `byte[+0]` kind byte | `003BF90C` `movzx eax, byte ptr [rcx]` |

### Members with no screen label (6 — widget-internal)

| member | what it computes | interior cite |
|---|---|---|
| `002550E0` | `003779F0` index → `020927C0 + 0x224` 32-byte entry → tail `00255060`; the level/resolve path `003C17E0` compares against | `00255112` `jmp 00255060` |
| `0037F140` | `02AED490`'s `+0xE0` bit 9 | `0037F153` `shr eax, 9` |
| `003BC2D0` | the loader: kind-7 `0xA2`/`0xA3`/`0xA4` → `+0xD8`/`+0xE0`/`+0xE8`, preloads script kinds 6/0x17 into `+0xD0` bits 0/1 (lmap §10.1) | `003BC312` `call 00249210` |
| `003BC4E0` | the widget procedure: message 1 init (zeroes `+0xC0..+0x118`, `00861EC0` clears `+0x120` for 0x158, `003BC2D0` load, `00246AD0`/`00247870` register), 0x10 release, 0x11 unload+destroy, else `005C5230` | `003BC936` `call 003BC2D0` |
| `003BCAB0` | `+0xCC` → `0037EDB0` index → `+0xCE`, tail `0037FD50` rebind | `003BCAE4` `jmp 0037FD50` |
| `003BD8F0` | `(page block rcx, idx edx, out r8)` → `block + word[+8] + entry[idx*8+0x14]`; `[r8]` gets `block + word[+0xA]` when ≠ 0xFFFF | `003BD93A` `movzx eax, word ptr [rcx + 8]` |

### Container children (2)

| member | what it computes | interior cite |
|---|---|---|
| `0035D520` | general helper, one client (`003C2100`): `[[0209AC30]+0x3A0]` child-object getter — not a map role | `0035D527` `mov rax, qword ptr [rax + 0x3a0]` |
| `003C2100` | binds the widget's `+0x110` lazily to `0035D520()`, then runs `[[rdi+8]]`'s first virtual | `003C2169` `call rax` |

**Correction to §2.6:** `003C2200(index)` does not release a slot — it tails into `003C26C0`, which
*populates* the matching slot's `+0x18` child-label array. The releasers are `003C21B0`/`003C2210`
(both slots) and `003C21C0`/`003C22B0` (the non-matching slot).

## 6a. The world map's atlas children

*(2026-09-13, FRONTIER, from the menu-screen package.)* The atlas labels five more procedures world-map children by
installer; all five hang off the two world-map procedures above:

- `00551E00` (ids 1, 24) and `00551F00` (ids 1, 14, 24) — installed by `005528C0`; construct/released panes, no input arm.
- `005542D0` (27-member subtree, ids 1, 2, 10, 12, 14, 15) — installed by `005528C0`; the world map's *interactive* pane —
  the only child with directional (10) and sub-command (12) arms, i.e. the destination/cursor list the page drives.
- `00555330` (ids 1, 4, 24) — installed by `00552250`; a help-message pane.
- `0055A8A0` (16-member subtree, ids 1, 4, 18) — installed by `0055A810`; a pane with a draw arm (id 4) and destroy.

## 6b. The world map screen package

*(2026-09-15, FRONTIER — the MENU-SCREENS-WORLDMAP addendum: the world map's own widget subtree read as one
more screen package. What the player sees: the full-screen continent map opened from the field menu's
"World Map" entry — a pannable map, a blinking cursor, a destination list, the map name in the corner and
a help line along the bottom.)*

### The installer and the two procedures

`00550400(kind, arg)` is the field-menu installer (the `0028E690` request-router row in §3): if
`02CA8F38` is still null it runs `002901D0`, `0035C080`, then
`00244F50(0x188, 00552250, {kind, arg})` and stores the widget into `02CA8F38`
(`0055043F`–`00550455`). The world-map screen is therefore a **0x188-byte host widget** whose
procedure is `00552250`; the host's own construct arm (below) builds the **0xA020-byte page widget**
`005528C0` as its `+0x160` child. `005528C0`'s released arm (id 24) reads `02CA8F38` and clears the
host widget's `+0x160` page-child link (`mov rax,[02CA8F38]`; `mov [rax+0x160],0` at
`00553A23`–`00553A2C`) — it unlinks the page from the host; the global itself is never written by
this arm, so ownership of `02CA8F38` stays with the host/installer side.

### `00552250` — the host, 41 ids to 13 arms

The dispatch is a two-level switch (`dec eax; cmp eax,0x28`) at `0055226C`–`00552294`, byte index table
`0055288C`, arm-offset table `00552858`.

| id | arm | what it does | interior cite |
|---|---|---|---|
| 1 (construct) | `00552296` | stores the proc at `[rbx+8]`; copies `msg+8`→`+0x172`, `msg+0x10`→`+0x174`; seeds `+0x98..+0x9E` from `01E0C1D8`/`01E0C1DC` (screen dims); `00247930(0x64)` anim; creates child `005528C0` (`ecx=0xA020`) → `+0x160`, sets `[child+0x110]=self`; `00247570` binds the descriptor | `00552301` `lea rdx,[rip+0x5b8]` = `005528C0` |
| 16 | `0055233F` | `msg+8` bit 8 → `+0x170` bit 2 (set/clear), then `00563110(+0xC0)` — a "show/hide the label layer" toggle | `00552342` `bt rax, 8` |
| 41 | `005523BF` | the build arm — `003BCAF0`, `00550A00`, `00550820`, `002F9860` picks string `0xBFA`/`0xC03`/`0xC04` by `+0x172`, `0035C140`, creates help pane `00555330` (`ecx=0xC0`) → `+0x168`; copies `+0x170`/`+0x178`/`+0x180` flags into the child's `+0x150`/`+0x14A`/`+0x14C`; `00246AD0` registers `+0x160`, `+0x168` and itself on `0208EA20`/`0208EA28`; `002470D0` focus-push; `00249C60(0x4C)` sound | `0055243F` `lea rdx,[rip+0x2eea]` = `00555330` |
| 2 | `0055251B` | if `+0x170` bit7 set and both children already gone → `00244F00(self)`, clears bit7 — the deferred self-destroy | `00552547` `call 00244F00` |
| 15 | `0055255F` | releases both children via `00244F00`, then `0035C080` — pre-destroy | `0055256B` `call 00244F00` |
| 18 | `0055258D` | `00245020` broadcast to each child, `00563080(+0xC0)` free, `003BBFB0`, `00247780(1)` — the destroy-broadcast | `00552599` `call 00245020` |
| 24 (released) | `005525E1` | if `+0x170` bit3 clear: `00285F00` posts `{+0x170 bit4, +0x176, 0}` to `*(0209AC30)+0x3E0` — reports the exit mode back to the system | `00552619` `call 00285F00` |
| 39 | `00552625` | `msg+8 <<4` xored into `+0x170` bit4; `msg+0x10` → `+0x176` — sets the mode flag the release arm reports | `00552634` `and ax, 0x10` |
| 10 | `00552651` | **the pad arm** — `002C9430(0)`/`(1)` read both pads; `02F97368..70` supply the directional step bits (nibbles `>>4` + sign bits 0x10/0x20/0x40/0x80 adjust ±1); adds them to the page child's `+0x100`/`+0x102` (map cursor x/y) and clamps `[0, WorldMapWidth−screen]`/`[−pad0, pad1+WorldMapHeight−screen]`; a confirm bit in `02F97368` & `01F2CAA4` mask → `00550470` | `005526B9` `add word ptr [rax+0x100], cx` |
| 4 (draw) | `0055276D` | `005632B0` (→`00555A10`) on `[+0x38]`; copies child `+0x100`/`+0x102` (or `+0x17C`/`+0x17E`) into ebp/r14, `+0x14E`→`[+0x38]+0x58`; `00562F30(+0xC0, x, y, rsi)` draws at the cursor; stores back `+0x17C`/`+0x17E` | `005527D2` `call 00562F30` |
| 35 | `005527FA` | writes `+0x172` into `*msg+8` — an out-param query ("which map mode is showing") | `00552805` `mov dword ptr [rax], ecx` |
| 40 | `0055280B` | sets `+0x170` bit6 and self-sends id 41 through `[rbx]` — the "rebuild me" trigger | `00552834` `call rax` |
| default (3,5–9,11–14,17,19–38 except above) | `0055283A` | `005C5230` shared tail | `0055283D` `call 005C5230` |

**The kinds, named 2026-09-25 (FABLE, Claude Opus 5.5).** The installer's `kind` is the host's `+0x172`, and the
build arm titles the help line by it. By the text-id method of `UQ-299`, `0xC03` is "Choose your destination."
(kind 2), `0xC04` is "Airship Route" (kind 3), and `0xBFA` (kind 5) is an empty row. The UI request router picks
the kind:
- the field menu's world-map entry sets kind 1;
- request 17, the Strahl boarding menu, sets kind 2;
- request 15 sets kind 3;
- request 18 sets kind 7, which gets no title.

In kind 3 the `arg` (`+0x174`) is a route number. `003BCAF0` marks the two nodes of every `menumap_world.bin` link
whose byte `+2` equals it. The shipped links number routes 1-14, which are seven node pairs, each once per
direction. See [ui-request-router.md](../Request-Router/ui-request-router.md) UQ-162.

### `005528C0` — the page, 42 ids to 17 arms

Two-level switch at `005528EA`–`00552918` (`cmp eax,0x29`), index table `00553AB0`, arm table `00553A6C`.
The widget is `0xA020` bytes — the page itself is the whole map surface.

| id | arm | what it does | interior cite |
|---|---|---|---|
| 1 (construct) | `0055291A` | dims `01E0C1D8`/`01E0C1DC` → `+0x98..+0x9E`; `00247930(0x64)`; `00247570` descriptor; `002C9430` ×2 (both pads) | `0055294E` `lea rdx,[rip+0x7d05cb]` |
| 6 | `005529F2` | **the populate arm** — `002CC9B0`/`002CC960` fetch the map-data record; `00551230` mode query; `00551130` ×2 locate two entries; `002F9860` ×2 fetch the region strings; `00244F50(0x1C0, 00553AE0)` creates the MapName/RegionText pane; `00562120` ×3, `003C0180`, `00202C90`, `00553DD0` (destination-list rebuild); `00246AC0` registers | `00552CA1` `mov ecx, 0x1c0` + `lea rdx` = `00553AE0` |
| 10, 11 | `00552EC7` | **the input arm** — `+0x150` bit7 gate; `00551230` mode → ebx; reads the `02F97368..71` pad/direction bytes and `002C9430` pads, scrolls `+0x100`/`+0x102` clamped to `01F2CAA4−01E0C1D8`/`01F2CAA8−01E0C1DC`; mode 2 with a flag delta installs `00551E00` (`0x4A0`), `005542D0` (`0xDE0`), `00551F00` (`0x4A0`) via `00244F50`+`00244960`+`00246AC0` — the three panes come up lazily on first input; other modes → `00249C60(3)` sound + `002CC9B0`/`002CC9C0` index + `00550470` confirm | `005530DA` `lea rdx,[rip-0x12e1]` = `00551E00`; `0055339A` `lea rdx,[rip+0xf2f]` = `005542D0`; `005534C5` `lea rdx,[rip-0x15cc]` = `00551F00` |
| 4 (draw) | `00553625` | the render arm — `002753F0` indirect entry, `00551230`, `005632B0`, `00562F40`→`00555400`, `005512B0` ×2, `005520F0`, `005551F0`, `00553BB0`, `00554BD0`, `0057E210`, `00554EA0`, `00562920`, `0057E090`, `002C9430` ×4 — map surface, markers, destination names, cursor | `0055369C` `call 005512B0` |
| 2 | `0055354A` | `001EDEC0(+0xB4)` gate; while `+0x150` bit2 and `+0x154` nonzero, `+0x154` counts down toward 0 by quarter-steps (min step 4) — the open-transition timer; then `00554A60([+0x118])`, `00553CB0`, `00551230`; mode 2 → `005620A0(+0xC0)` smooth-scroll step | `005535A5` the `/4` step math |
| 15 | `0055391A` | `00244F00` child destroy — pre-destroy | `0055392D` `call 00244F00` |
| 18 | `00553947` | `00245020` broadcast — destroy notify | `00553958` `call 00245020` |
| 24 (released) | `00553A23` | clears `[02CA8F38]+0x160` — drops the host's page-child link; **at this site** the global is dereferenced and not written: the store lands in the object it points at, not in the pointer. It is written elsewhere — `00244F50(0x188, 00552250, {kind, arg})` above stores the widget into it | `00553A2C` `mov [rax+0x160], rsi` |
| 29 | `00553A02` | clears `+0x130` — drops a record pointer | `00553A04` `mov qword ptr [rdi+0x130], rsi` |
| 30 | `00553A0F` | `00551CD0(+0x160, msg+8)` — relabel the `+0x160` child | `00553A1A` `call 00551CD0` |
| 31 | `005539EF` | sets `+0x150` bit0 + `00247780(0)` — the open-animation start | `005539F9` `call 00247780` |
| 32 | `00553537` | `msg+8` word → `+0x154` — arms the open-transition timer | `0055353C` `mov word ptr [rdi+0x154], ax` |
| 34 | `005539D0` | `msg+8 <<2` xored into `+0x150` bit2 — sets the flag id 2 counts down under | `005539E0` `and ax, 4` |
| 37 | `00553995` | `00550470` — the confirm/activate | `005539A0` `call 00550470` |
| 38 | `005539AC` | `002901D0(byte[[+0x9F40]+0x39])` writes `0209BE80+0x10FA4` (the world-map mode field), then `00550470` — set-mode + confirm | `005539C2` `call 002901D0` |
| 42 | `0055396F` | `msg+8 <<7` xored into `+0x150` bit7 — sets the input gate the id 10/11 arm tests | `00553984` `and ax, bx` (0x80) |
| default (3,5,7–9,12–14,16,17,19–23,25–28,33,35,36,39–41) | `00553A37` | `005C5230` shared tail | `00553A3D` `call 005C5230` |

### The five panes

| pane | size | ids | what it is |
|---|---|---|---|
| `00551E00` | `0x4A0` | 1, 24 | construct builds its `+0xC0` record from `002F9860(0x800)` (a fixed string id) via `00241BF0`; id 24 self-sends 0x1F + 0x25 through `00275440` — a released-stamp pane |
| `00551F00` | `0x4A0` | 1, 14, 24 | construct looks the destination name up (`003BD040` on `msg+0x10`), formats with `002B4090(0x200)`, stores the `+0xC0` record; id 14 returns 0; id 24 sends 0x1F + 0x26 — the **destination-name header pane** |
| `005542D0` | `0xDE0` | 1, 2, 10, 12, 14, 15 | **the interactive pane** — the destination list. Four `0x328`-byte entry records at `+0xF8`, page counter `+0xE0`, sub-indices `+0xE2`/`+0xE3`. id 10: `+0xD0`&4 → `002D3900` on `+0xE8`, else pad test → `00249C60(3)` + `00244F00` (cancel). id 12: `msg+8 − 0x8001` = page left/right — walks the `0x328` slots through `00551B30`/`00551C20`/`00551930`/`00551D80`. id 2: per-slot fade tick (`+0x10C` word ±0x800, clamp [0,0x4000]) |
| `00553AE0` | `0x1C0` | 1, 4 | **MapName/RegionText pane** — id 1 seeds `+0x98`=0, `+0x9C`=0x7800438 and binds the layout keys; id 4 draws the two strings (`002D8910`/`002D8650`) |
| `00555330` | `0xC0` | 1, 4, 24 | the help pane — id 1 copies a 6-field record (`002432B0`), binds, `0029FB50`, `00247930(0x5d)`; id 24 clears the host's `+0x168` link |
| `0055A8A0` | — | 1, 4, 18 | installed by `0055A810` on the `+0xD8` slot — a one-record pane; id 4 draws through `00274780`+`00555A10`+`00555400`, id 18 clears the slot |

### Members

All 185 subtree members of the eight world-map roots (`00550400`, `00552250`, `005528C0`, `00551E00`,
`00551F00`, `005542D0`, `00553AE0`, `00555330`, `0055A8A0`), each with a role line and an interior cite.
The `subtrees` column names the roots that reach the member.

| member | size | subtrees | role | interior cite |
|---|---|---|---|---|
| `0017FA70` | 28 | 2250 | one-call wrapper into `001B5FB0` | `0017FA78` |
| `001B5CC0` | 159 | 2250 | iterates the `rcx+0x278` ring, marks each `[rdx+0x10]=1` — a per-child flag sweep | `001B5D10` |
| `001E0A10` | 42 | 28C0 | engine-ctx pair: `00198790` ctx, `005C3A30`, then `00198790`, `001986D0` | `001E0A16` |
| `001E0E30` | 21 | 28C0 | ctx `00198790` then tail `00225570` | `001E0E34` |
| `001E0E50` | 21 | 28C0 | ctx `00198790` then tail `00197700` | `001E0E54` |
| `00202D80` | 81 | 28C0 | 3-float component-wise multiply `rdx[i]*r8[i]` to a stack out | `00202DAE` |
| `002030E0` | 142 | A8A0 | copies a 0x40-byte record and adds the float delta `r8` into `+0x30..0x38` — a position-offset copy | `00203129` |
| `00241BF0` | 148 | 1E00,1F00 | builds the pane's `+0xC0` child record from a template + flags (`r8d=0x410` seen) | `00241C3B` |
| `00244A20` | 943 | 42D0 | 943 B widget-flag processor — `+0x7C` bits 0x30 gate a long update path | `00244A64` |
| `00245510` | 142 | 28C0 | `00368300` predicate gate, then `002D8C00` init + `00367940`/`00368300` steps — the cursor-anim guarded helper | `00245519` |
| `00246480` | 306 | 42D0 | null-guarded widget helper — `+0xC` word accumulation on `rdx` | `0024651F` |
| `002465F0` | 395 | 1E00,1F00 | the widget constructor (CONTRACT-widget-object) | `002465F8` |
| `00247780` | 22 | 2250,28C0,42D0 | anim kick — `xor eax,edx` flag toggle on the target | `0024778D` |
| `002497B0` | 45 | 1E00,1F00 | `0036C1D0(3)` + `0036A100` — a string intern/lookup | `002497C0` |
| `00254380` | 31 | 28C0,1F00,42D0 | `[tbl]+0xA` word, byte-count bounds check (list length) | `00254390` |
| `002543A0` | 40 | 1F00 | `[tbl]+0xE` word to a record; `ecx` bounds to an element ptr or the `01A97280` fallback | `002543B1` |
| `002543D0` | 31 | 1F00 | `[tbl]+8` word, byte-count bounds check | `002543E0` |
| `002543F0` | 71 | 28C0,1F00 | `[tbl]+0xC` word, count guard then word fetch | `002543F4` |
| `00270260` | 396 | 2250,28C0 | 396 B packet-context prologue — binds the GIF output ctx | `0027026A` |
| `00270420` | 209 | 28C0 | 209 B buffer fill — `r8d` count loop writing `01F44830`-family constants | `00270426` |
| `00270500` | 80 | 28C0 | 80 B float accumulation over a `rcx` array | `0027052A` |
| `00270550` | 55 | 28C0 | vector length-squared `x^2+y^2+z^2` | `0027056E` |
| `002708B0` | 41 | 28C0 | vector scale `rdx[i]*xmm2` plus tail copy | `002708C8` |
| `00271010` | 56 | 2250,28C0,A8A0 | advances the `+0x10` packet cursor past `+0x8`, optional `0016D6A0` flush | `0027102F` |
| `00271050` | 44 | 28C0,A8A0 | writes the `0x50000000|count` DMA-tag quad at `[+0x30]` | `0027106A` |
| `002710C0` | 58 | 28C0,A8A0 | writes the `0x200000000000|(idx<<0xF)|count` qword tag at `[+0x28]` | `002710DF` |
| `00271290` | 70 | 2250,A8A0 | copy loop `rcx` to `rdx`, count `r8` | `002712B4` |
| `00271480` | 17 | 28C0,A8A0 | marks `+0x10` into `+0x30`, bumps `+0x10` by 0x10 (packet tag slot) | `0027148C` |
| `002714C0` | 17 | 28C0,A8A0 | same mark into `+0x28` | `002714CC` |
| `00271870` | 75 | 2250,28C0,A8A0 | writes the `0x10000000` tag pair at `[+0x10]`, `0016D6A0` emit of `r8>>4` dwords | `0027189B` |
| `002718C0` | 18 | 28C0 | bit0 test, returns 2 or `dl&1` — a tiny selector | `002718CA` |
| `00274780` | 10 | 2250,A8A0 | `rcx + dword[rcx+rdx*8]` — a rel32 proc-slot fetch | `00274786` |
| `002747B0` | 137 | 2250 | 137 B rip-ref helper on the widget globals | `002747B7` |
| `002753F0` | 68 | 28C0 | 68 B `call rax` dispatch — the draw arm's indirect entry | `0027540E` |
| `002754E0` | 97 | 28C0 | 97 B float lerp — `dst = src + (dst-src)*t` per component | `00275514` |
| `00285F00` | 27 | 2250 | posts `{dword,word}` into `*(0209AC30)+0x3E0/+0x3E4` — the system notify slot | `00285F02` |
| `0028C4F0` | 101 | 2250 | scans the `+0xD54` five-word array against 4 — a field scan on the world-map state block | `0028C523` |
| `0028C940` | 46 | 2250 | sets `+0x28` bit1, scans the `+0x44` word list on bits 0/1 | `0028C959` |
| `0028E8B0` | 19 | 2250 | tail `002BE020` — a teardown forwarder | `0028E8BE` |
| `0028E900` | 25 | 2250 | `[0209BE80]+0x8FA0` to `002BE050` — the world-map teardown on the global block | `0028E913` |
| `0028FCB0` | 72 | 2250 | 72 B accessor on the `0209BE80`-family globals | `0028FCBA` |
| `002901D0` | 73 | 28C0 | writes `0209BE80+0x10FA4 = cx`; zero also clears `+0x10FAC` — the world-map mode field | `002901D4` |
| `00290990` | 83 | 2250 | `[0209BE80]+0x10F00` to `0028C4F0`, clears `+0x10F68` bit3 — the map close path | `00290994` |
| `002BE020` | 48 | 2250 | 48 B `00244F00` destroy wrapper | `002BE035` |
| `002BE050` | 42 | 2250 | the map teardown chain: `002BEED0`, `00290990`, `0035C070`, `0016D6A0`, `003C53E0`, tail `0028E240` | `002BE054` |
| `002BE110` | 139 | 2250 | rebind guard — `[+0x1048]+0x4F0 == arg` else `002BE0A0` | `002BE145` |
| `002CC960` | 68 | 28C0 | `002EFD20` clamp+index then a map-data record fetch | `002CC971` |
| `002CC9B0` | 14 | 28C0,42D0 | `[[rip]+0xDF0]` — a `0209AC30`-region dword getter | `002CC9BD` |
| `002CC9C0` | 41 | 28C0,42D0 | `r9+3` index helper into the same block | `002CC9D5` |
| `002D1870` | 556 | 42D0 | 556 B — `cdq`/`idiv` row-major math on `+0xEA`/`+0xED`/`+0xF2`/`+0x100` — the destination-grid index | `002D18B1` |
| `002D4650` | 160 | 42D0 | `002D4B70` on `+0xED`/`+0xF2` then compares — a grid hit-test | `002D4670` |
| `002D4A40` | 291 | 42D0 | 291 B — `+0xEA` x `+0xED` plus `+0x100` x `+0xF2` — the grid cell offset | `002D4AD4` |
| `002D4B70` | 492 | 42D0 | 492 B — `(+0x9E - +0x13C + +0x100 - 1)/+0x100` — the visible-row count | `002D4C69` |
| `002D8C00` | 115 | 28C0 | 0xA0-byte draw-record init — ~~alpha 0x80~~ **the RGB scale `+0x5A` = 0x80, and the alpha scale `+0x58` is left 0 by the zero-fill** (the widget pass sets it afterwards; corrected 2026-09-25, OPUS, UQ-351: replay [case A](../../_index/candidates/uq351-opus-replay-widget-alpha-guard/)), colours 0x80808080, 1.0f scale | `002D8C11` |
| `002EFD20` | 40 | 28C0 | clamps `ecx` to [0,6] then `rax*3` — a small enum table indexer | `002EFD35` |
| `00314960` | 7 | 1E00,1F00 | returns the `022C2549` dword — a global getter | `00314966` |
| `0035C080` | 68 | 2250 | 68 B — the shared child-clear helper (sec.3) | `0035C084` |
| `0035C140` | 5 | 2250 | 5 B tail into `0028FCB0` | `-` |
| `00367820` | 200 | 28C0 | `022CBE30`-block guard — clears `022CBE4E` bit7, returns 1 | `00367826` |
| `00367940` | 346 | 28C0 | 346 B — the `022CBE30` cursor/sprite-anim step, `+0x800` flag reset | `00367948` |
| `00367FA0` | 104 | 28C0 | 104 B — reads `022CBE30` word fields | `00367FA5` |
| `00368010` | 559 | 28C0 | 559 B — the `022CBE30` record constructor (xmm fill + cookie) | `0036802E` |
| `00368250` | 5 | 28C0 | tail thunk into `00367FA0` | `-` |
| `00368300` | 84 | 28C0 | 84 B — `022CBE30` predicate: bit1 / byte==3 / word != 0xFFFF8000 | `0036830A` |
| `00368360` | 1116 | 28C0 | 1116 B — the `022CBE30` main step, gated on `+0x1F63ABE` | `0036836A` |
| `003687C0` | 66 | 28C0 | writes `022CBE3D..43` defaults (0x406, 0x1E) when `+0x10` set | `003687CA` |
| `003688E0` | 90 | 28C0 | `022CBE8A` mode switch — cases 2/3 write `022CBE82`/`022CBE8C` | `003688F6` |
| `00377870` | 49 | 28C0 | 49 B flag test/set on `cx` | `0037788D` |
| `0037E4F0` | 190 | 2250 | 190 B — `01F44830`-region accessor | `0037E4F6` |
| `0037EDB0` | 86 | 2250 | reads `[rdx]` index to the `020927C0+0x224` entry (sec.4) | `0037EDE0` |
| `0037F050` | 13 | 2250 | 13 B compare on the `0208EA20` region | `0037F052` |
| `0037F160` | 26 | 2250 | 26 B — `eax>>7` bit-field extract | `0037F173` |
| `0037F440` | 143 | 2250 | 143 B `01F44830`-region helper | `0037F447` |
| `0037F860` | 401 | 2250 | 401 B — `003697F0` heap free + `+0xE0` field walk | `0037F87D` |
| `0037FBA0` | 430 | 2250 | 430 B — `+0xEE` count x `+0xF0` byte-record match loop | `0037FC42` |
| `0037FD50` | 232 | 2250 | 232 B — `02AED490`-region rebind tail | `0037FD5A` |
| `0039BB60` | 492 | 2250 | 492 B — rip-ref string/table helper | `0039BB69` |
| `003BBFB0` | 425 | 2250 | 425 B — `02AED490`-region destructor | `003BBFB6` |
| `003BC260` | 81 | 2250,28C0 | 81 B — `0046B240` call wrapper | `003BC270` |
| `003BC3E0` | 82 | 2250 | 82 B — `01F44830`-region accessor | `003BC3E9` |
| `003BC9F0` | 190 | 2250 | 190 B — `02B457E0`-block entry fetch | `003BC9F6` |
| `003BCAF0` | 174 | 2250 | 174 B — `02B457E0` block + `+0xCC` index | `003BCAF5` |
| `003BCCA0` | 308 | 2250,28C0 | 308 B — `02B457E0` block + `+0x10` field | `003BCCB3` |
| `003BD040` | 364 | 2250,1F00 | 364 B — `02B457E0` entry-by-name lookup | `003BD04A` |
| `003BD1B0` | 718 | 2250 | 718 B — `+0x172`-indexed `02B457E0` record fetch | `003BD1BC` |
| `003BD480` | 618 | 1F00 | 618 B — `003148F0` + record walk | `003BD4AA` |
| `003BE1E0` | 228 | 28C0 | 228 B — `003BDFF0` enum, out=-1 default | `003BE1FD` |
| `003BF430` | 237 | 28C0 | 237 B — the nibble-keyed `02B457E0` fetch (unresolved-158) | `003BF435` |
| `003BF5E0` | 217 | 28C0 | 217 B — `02B457E0` field-sum helper | `003BF64E` |
| `003BF6C0` | 255 | 28C0,42D0 | 255 B — `00254380` bounds + entry fetch | `003BF6ED` |
| `003BF7C0` | 274 | 28C0,42D0 | 274 B — `02B457E0` entry fetch | `003BF7DC` |
| `003BFB60` | 262 | 2250 | 262 B — `01F44830`-region helper | `003BFB6E` |
| `003BFC70` | 370 | 2250 | 370 B — `01F44830`-region helper | `003BFC87` |
| `003BFE10` | 129 | 28C0 | 129 B — `02B457E0` fetch | `003BFE16` |
| `003BFEA0` | 122 | 28C0 | 122 B — `003148F0` call wrapper | `003BFEA8` |
| `003BFFF0` | 202 | 2250 | 202 B — `01F44830`-region helper | `003BFFFA` |
| `003C00C0` | 183 | 2250 | 183 B — `01F44830`-region helper | `003C00CA` |
| `003C0180` | 207 | 28C0 | 207 B — `02B457E0` `+0xD8` table, `+0xC`-word bounds | `003C018A` |
| `003C0250` | 82 | 28C0 | 82 B — `02B457E0` `+0xD8` table, `+0x10`-word bounds | `003C027B` |
| `003C0340` | 51 | 28C0 | 51 B — `02B457E0` `+0xE0` table, byte `+9` count, `+0xA` word index | `003C035B` |
| `003C0450` | 406 | 42D0 | 406 B — `02B457E0` `+0xE8` table, `+8`-word bounds, writes `+0xCA` | `003C0468` |
| `003C05F0` | 232 | 42D0 | 232 B — `02B457E0` `+0xE8` table scan | `003C05FF` |
| `003C08B0` | 333 | 2250,28C0,1F00 | 333 B — `02B457E0` `+0xE8` entry setter | `003C08C4` |
| `003C0A00` | 362 | 28C0,1F00 | 362 B — `01F44830`-region + `+0xD8` walk | `003C0A1A` |
| `003C0B70` | 108 | 28C0 | 108 B — `02B457E0` `+0xD8` `+0xA`-word accessor | `003C0B74` |
| `003C0BE0` | 107 | 28C0 | 107 B — same table, `+0xA`-word variant | `003C0BE4` |
| `003C0C50` | 110 | 2250 | 110 B — `02B457E0` `+0xE8` accessor | `003C0C54` |
| `003C0D70` | 187 | 28C0 | 187 B — `02B457E0` `+0xE8` `+8`-word bounds | `003C0D7F` |
| `003C0E30` | 207 | 28C0,42D0 | 207 B — `02B457E0` `+0xD0` bit8 gate + `+0xE8` walk | `003C0E36` |
| `003C0F00` | 112 | 28C0 | 112 B — `02B457E0` `+0xE8` bounds | `003C0F14` |
| `003C0F70` | 246 | 28C0 | 246 B — `02B457E0` `+0x16`-word record scan | `003C0F8E` |
| `003C12B0` | 755 | 28C0,42D0 | 755 B — `02B457E0` `+0xE8` `+8`-word entry walk | `003C12BB` |
| `003C1680` | 350 | 1F00 | 350 B — `02B457E0`-family entry iterator | `003C1694` |
| `003C18A0` | 220 | 28C0 | 220 B — `003BCBA0` + `+0xE`-word entry walk | `003C18BA` |
| `003C1D70` | 124 | 42D0 | 124 B — `02B457E0` `+0xD8` `+0xA`-word bounds | `003C1D76` |
| `003C53E0` | 18 | 2250 | 18 B — clears `02B45970[ecx]` dword | `003C53E3` |
| `00473BB0` | 213 | 2250,28C0 | 213 B — `[[rip]+idx*4+8]` rel32 table to record fill | `00473BCC` |
| `00473CC0` | 92 | 2250 | 92 B — same table, `+4` word vs 0x8000 mask | `00473CEF` |
| `00550470` | 153 | 2250,28C0,42D0 | the confirm — `002470C0` on the `+0x160` child then self, msg 15, sets `+0x170` bit7 | `00550476` |
| `00550690` | 388 | 2250 | 388 B — `+0x160` child `+0x128` read (pane-install arm helper) | `005506A2` |
| `00550820` | 468 | 2250 | 468 B — `+0x160` `+0x118` read, builds children | `0055082A` |
| `00550A00` | 462 | 2250 | 462 B — `003BD1B0(+0x172)` string fetch + `01F44830` refs | `00550A0B` |
| `00550BD0` | 985 | 28C0 | 985 B — `+0x130`/`+0x54` gated, `01F2CAA4` x float — the map-surface scale/draw | `00550C03` |
| `00550FB0` | 373 | 2250 | 373 B — writes `+0x16`-offset records, `00900358`/`00D22FC0` refs | `00550FC5` |
| `00551130` | 190 | 28C0 | the destination-entry locator — `+0x140` list walk matching `+0x39`, returns `+0x3C/+0x3E` centre minus half dims | `00551190` |
| `00551230` | 117 | 28C0,42D0 | sends msg 0x23 to `02CA8F38`, returns the out-dword — the mode query | `00551234` |
| `005512B0` | 858 | 28C0 | 858 B — `00551230` + `01F44830` — the populate-loop driver | `005512C5` |
| `00551800` | 294 | 42D0 | 294 B — `003BF7C0`/`003C0450` + `01F44830` — entry build | `00551813` |
| `00551930` | 176 | 42D0 | 176 B — `00551230` + `002D48C0`/`002D47C0` — grid-cell write | `00551948` |
| `005519E0` | 334 | 1E00,1F00 | the shared pane tail (ids 2/12/14) — `00244F00`/`00245020`/`00249C60`/`00273A20`/`00275440` | `005519E6` |
| `00551B30` | 232 | 42D0 | 232 B — `+0x10 = msg+2`, `00551230` + `002D47C0`/`002D48C0` — entry set | `00551B5D` |
| `00551C20` | 171 | 42D0 | 171 B — writes the `{computed-byte, r8b, +0x10-word}` record into the slot | `00551C77` |
| `00551CD0` | 162 | 28C0 | 162 B — `(dims - 0x20)/4` position compute on `+0x160` | `00551CE6` |
| `00551D80` | 114 | 42D0 | 114 B — copies a 0x18-byte record, sets `+0x1A` bit0, `+0x10`=3 — slot populate | `00551DB1` |
| `00551E00` | 245 | 1E00 | pane proc (0x4A0, ids 1/24): construct builds the `+0xC0` record (`00241BF0` + `002F9860(0x800)`), id 24 sends 0x1F/0x25 | `00551E0A` |
| `00551F00` | 321 | 1F00 | pane proc (0x4A0, ids 1/14/24): construct does `003BD040` + `002F9860(msg+8)` + `002B4090(0x200)` format, id 14 to 0 | `00551F0D` |
| `005520F0` | 320 | 28C0 | 320 B — `00271450` bind + `002714A0` + emit loop — a packetized line/text draw | `00552115` |
| `00552250` | 1543 | 2250 | the host widget proc (0x188, 41 ids to 13 arms) — installs `005528C0`, drives cursor scroll | `00552258` |
| `005528C0` | 4521 | 28C0 | the page proc (0xA020, 42 ids to 17 arms) — installs the panes, owns `02CA8F38` | `005528DC` |
| `00553AE0` | 202 | 3AE0 | MapName/RegionText pane (0x1C0, ids 1/4): id 1 sets `+0x98`=0 / `+0x9C`=0x7800438 + `00247570` name; id 4 draws via `002D8910`/`002D8650` | `00553B1B` |
| `00553BB0` | 251 | 28C0 | 251 B — scroll-offset compute on `01E0C1D8`/`01E0C1DC` dims | `00553BBC` |
| `00553CB0` | 287 | 28C0 | 287 B — `0x80`-const refresh helper | `00553CC2` |
| `00553DD0` | 353 | 28C0 | 353 B — `+0x9F6C` walk — the destination-list rebuild | `00553E29` |
| `00553F40` | 817 | 42D0 | the `005542D0` shared tail (817 B) — dispatches 0x23 more ids | `00553F4B` |
| `005542D0` | 1861 | 42D0 | the interactive pane (0xDE0, ids 1/2/10/12/14/15) — 4 x 0x328-byte entries at `+0xF8` | `005542E0` |
| `00554A60` | 360 | 28C0 | 360 B — `+0x154`-family countdown (0x4000/0x3666/0x2CCC steps) | `00554AC4` |
| `00554BD0` | 718 | 28C0 | 718 B — `+0x58/+0x5A` position draw — the entry marker | `00554C7C` |
| `00554EA0` | 846 | 28C0 | 846 B — the same-position draw, `0029CD00`/`002D8650` — the other marker layer | `00554EEB` |
| `005551F0` | 165 | 28C0 | 165 B — `005520F0` + `00562A30` — a line-emit wrapper | `005551F7` |
| `005552A0` | 134 | 28C0 | 134 B — `002C9430` pad-read helper | `005552BD` |
| `00555330` | 201 | 5330 | help pane (0xC0, ids 1/4/24): id 1 `002432B0` 6-field copy + `00247570`/`0029FB50`/`00247930(0x5d)` | `0055535B` |
| `00555400` | 667 | 28C0,A8A0 | 667 B — `00271450`/`00271480` packet emit — a sprite quad writer | `00555487` |
| `005556A0` | 873 | 2250 | 873 B — `+0x90` byte x `+0x5A` tile-index math — the map-surface draw | `005556B2` |
| `00555A10` | 61 | 2250,28C0,A8A0 | 61 B — `00271010`/`00271450`/`00271870` — a packet-emit wrapper | `00555A19` |
| `00555A50` | 18 | 2250 | 18 B — `[+0x10] + rcx + rdx*0x20` row indexer | `00555A5B` |
| `00555A70` | 274 | 2250 | 274 B — `01F44830`-region helper | `00555A7C` |
| `00555B90` | 370 | A8A0 | 370 B — `0x3000000000008000|idx` qword tag + 0x412 — a sprite packet emit | `00555BC1` |
| `00555D10` | 619 | 28C0,A8A0 | 619 B — iterates the `+0x140` list calling `00555B90`/`00556240` — the name-list draw | `00555D23` |
| `00555F80` | 700 | 28C0,A8A0 | 700 B — xmm6-9 save + `00271450` — the big packetized draw | `00555FAF` |
| `00556240` | 312 | A8A0 | 312 B — `00271450`/`00271480`/`002714A0`/`002714C0`/`002714E0` + `00271050`/`002710C0` — a positioned sprite packet | `0055625F` |
| `0055A8A0` | 341 | A8A0 | pane proc (ids 1/4/18): id 1 stores `+0xC0`/`+0xC8`/`+0xD0`; id 4 `00274780`+`00555A10`+`00555400` draw | `0055A928` |
| `00561F60` | 43 | 28C0 | 43 B — `+0x24` +=/-= `+0x26` by `+0x28`&1, clamped [0,0x100] — the cursor blink animator | `00561F77` |
| `00561F90` | 227 | 28C0 | 227 B — `+0x24`-word field on `+0x90` — blink state read | `00562002` |
| `00562080` | 31 | 28C0 | 31 B — blink init: `+0x26`=0x10, `+0x1C`=0x808080, `+0x20`=0x80808080 | `00562090` |
| `005620A0` | 127 | 28C0 | 127 B — float lerp toward `+0x30` — the smooth-scroll step | `005620AA` |
| `00562120` | 108 | 28C0 | 108 B — `00202C90` + `+0xC0` field — a layout helper | `00562144` |
| `00562190` | 14 | 28C0 | 14 B — swaps rcx/rdx to `00562850` | `00562199` |
| `005621A0` | 1711 | 28C0 | 1711 B — the `w_line01` text-line draw (rect primitives `00181330`/`00181560`/`001816B0`) | `005621B5` |
| `00562920` | 262 | 28C0 | 262 B — `[+0x80]` to `[+0x60]` to `[0]` entry deref chain | `005629A5` |
| `00562A30` | 1019 | 28C0 | 1019 B — `00563360` + `00271450` packet ctx — the second text draw | `00562A47` |
| `00562E30` | 254 | 28C0 | 254 B — `00271450`/`00271080`/`00271100`/`002714A0`/`002714E0`/`00563430` — the underline/divider emit | `00562E5A` |
| `00562F30` | 8 | 2250 | 8 B — tail `005556A0` on `[rcx]` | `00562F33` |
| `00562F40` | 66 | 28C0 | 66 B — `00555400` wrapper | `00562F65` |
| `00563080` | 143 | 2250 | 143 B — frees the `+0x10` chain (`0024A680`/`003697F0`) | `005630A2` |
| `00563110` | 402 | 2250 | 402 B — the `w_line01`/`00D23270` label setter — writes formatted text into `+0xC0` | `00563133` |
| `005632B0` | 5 | 2250,28C0 | 5 B — tail `00555A10` | `-` |
| `005632C0` | 147 | 42D0 | 147 B — `0024A680` + `003C1D70` on `00D23250` — label teardown | `00563309` |
| `00563360` | 193 | 28C0 | 193 B — `00271450`/`002714A0`/`00271480` — a packet-ctx prologue | `00563369` |
| `00563430` | 227 | 28C0 | 227 B — `00203170` x2 on the `02CA9660` region — the route-line helper | `00563440` |
| `0057E030` | 53 | 2250 | 53 B — linked-list push on `+8`/`+0x10` | `0057E050` |
| `0057E070` | 22 | 2250 | 22 B — 0x28-byte list init | `0057E07D` |
| `0057E090` | 249 | 28C0 | 249 B — `+0x18` bit2 gated list pop | `0057E10D` |
| `0057E190` | 122 | 28C0 | 122 B — `+0x10` list fetch, `r8` flag variant | `0057E1CF` |
| `0057E210` | 212 | 28C0 | 212 B — `+0x10` list walk + `00245510`/`00368250`/`00368360` | `0057E218` |
| `0057E2F0` | 30 | 2250 | 30 B — 0x38-byte record init | `0057E301` |

**Message-id meanings learned here** (posted to the protocol page's open list): **id 10/11** is the
per-frame pad/directional arm — `02F97368..71` carry the direction nibbles and the confirm bit,
`+0x100`/`+0x102` is the map cursor. **Id 6** on a page procedure is the *content populate* (load data,
fetch strings, install the label pane). **Id 41** on the host is *build/register the children*; **id 40**
self-sends 41 (rebuild). **Id 39** loads the exit mode into `+0x176`/`+0x170` bit4, and **id 24**'s arm
reports it through `00285F00`. **Id 35** is an out-param query for `+0x172`. **Ids 29/32/34/42** are the
flag/timer arms — `+0x154` is the open-transition counter, `+0x150` bits 0/2/7 the open/anim/input gates.

## 6c. The layout-key readers

*(2026-09-14, FRONTIER — the LAYOUT-KEY-READERS package.)* Every `uisize.json` key whose reader sits
inside the map screens' call trees, with the use-site instruction. "P" marks a widget procedure. The
shared-band helpers are covered once here: they all feed `height → ecx`, `gradient → edx`,
`anim-ms → r8d` into `002C9060`/`002C9490` (band build) and `002C9890`, and differ only in which key
triple they bind — each screen's instance supplies its own `*BlackBandH`/`*BlackBandGradH`.

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `00552250` P (world map host) | `WorldMapWidth`, `WorldMapHeight` | pan clamp: `edx = WorldMapWidth − screenW` then `[r8+0x100]` held ≤ it (`00552708`/`00552726`); `r9d = WorldMapHeight − screenH + offset` same way (`00552666`) |
| `005528C0` P (world map page) | `WorldMapWidth`, `WorldMapHeight` | same clamp on the page's `+0x100`/`+0x102` scroll pair (`00552B5A` `cmovg`, `00552B75` `sub`+`cmp`) |
| `00553CB0` (→`005528C0`) | `WorldMapWidth`, `WorldMapHeight` | edge-hit flags for the pad arm: `ecx = WorldMapWidth − x` and `ecx = WorldMapHeight − y` compared against the cursor to set direction bits 1/2/8 (`00553D3E`, `00553D55`) |
| `005552A0` (→`00551130`→`005528C0`) | `WorldMapWidth`, `WorldMapHeight` | the smooth-scroll clamp: `[rbx]`/`[rdi]` scroll target held inside map-minus-screen (`005552D3`, `005552EF`) |
| `00550A00` (→`00552250`, the id-41 build arm) | `WorldMapCursorOffsetX`, `WorldMapCursorOffsetY` | cursor init: base word + key stored to `[rbx]`/`[rbx+4]` (`00550AA6`, `00550AB6`) |
| `00555A70` (→`005556A0`→`00562F30` draw) | `WorldMapVRUpperWidth` | `eax = key`, halved, → float `[rbx+0x10]` — the upper viewer rect's half-width for centering (`00555A9C`) |
| `00555F80` (→`00555400`→`0055A8A0` pane) | `WorldMapVRUpperWidth`, `WorldMapVRUpperHeight` | both converted to float → `[rcx+8]`/`[rcx+0xC]` — the viewer rect's dimensions (`0055602F`, `0055603F`) |
| `00563430` (→`00562E30`→`005520F0` draw) | `WorldMapLineScale` | stored to global `02CA96D0` beside two computed floats — the destination-line spacing scale (`005634F1`) |
| `0027EF50` (→`0027F5D0`) | `WorldMapBlackBandH`, `WorldMapBlackBandGradH`, `BlackBandAnimTime` | the world map's fade band: heights to `002C9060`, anim time in `r8d` (`0027EF6B`/`0027EF5E`) — see `002C9060` convention above |
| `002804E0` (→`0027F5D0`, `00579AE0`) | `WorldMapBlackBandH`, `WorldMapBlackBandGradH`, `LocaMapBlackBandH`, `PartyBlackBandGradH`, `BlackBandAnimTime` | second band builder shared by the world and location maps — two band triples in one helper (`00280513`/`00280519`, `0028058D`) |
| `002BA700` P (location map) | `LocaMapBlackBandH`, `NaSPArtSignalOffsetX/Y`, plus the shared `BlackBandAnimTime`/`PartyBlackBandGradH` | band build via `002C9490` (`002BAA14`); then `edx − NaSPArtSignalOffsetY`, `ecx = NaSPArtSignalOffsetX` feed `0029E770` — the "N/A"-class signal sprite's position (`002BAA49`, `002BAA4F`) |
| `0027EF00` (→`0027F5D0`) | `LocaMapBlackBandH`, `PartyBlackBandGradH`, `BlackBandAnimTime` | the location map's own band triple — `ecx`/`edx`/`r8d` into `002C9060` (`0027EF1B`, `0027EF15`, `0027EF0E`) |
| `0039BB60`, `0039BF50` (→`0039BEC0`→`003BC4E0`, the location-map text pane) | `FontBaseHeight` | `imul ecx, FontBaseHeight, 0x3C` then `cmp` against the scroll word — the per-line text-scroll limit (`0039BCDD`, `0039C08E`) |
| `0028FCB0` (→`0035C140`→`00552250` host) | `mHelpMessageFontCount` | `r9d` = the help string's char-count arg on the world map's help-message draw (`0028FCE8`) |

The non-frontier map readers — `002B7B80` P (TrackMap scale/icon), `002B8EE0` (TrackMap color + ExtraTrack
jump-icon), `002BCB00` (BaseMap/ExtraLoca jump-icon), `00553AE0` P (MapName/RegionText offsets) — are
already dispositioned on this page (`002B7B80`/`002BAF80` UQ-156, the `00553AE0` pane at §6b).

## 7. What is not known

- [x] ~~What the field-time container `02B47760` is for.~~ **Answered the same day (§2.6; first recorded as a narrowing):** its page preloads the
  current sub-location's `menumap_subNN.bin` into the map-data cache. *(Split 2026-09-30, SWE2-FRONTIER, on FABLE's
  [`qid-marker-truth-fable-0930`](../../_index/candidates/qid-marker-truth-fable-0930/README.md) (`02d59b826`): this box keeps the answered half; the sender residue is MS-4, the next box.)*
- [x] **MS-4.** Who sends the field-time container `02B47760` message 14 (its opening), and with which index. Static:
  find the senders of message 14 to that container and the index each passes. Registered 2026-09-30 (SWE2-FRONTIER). *(MS-4 answered 2026-09-30 by SWE2-STRUCT for OPUS `d526b865b`, [record](../../_index/candidates/swe2struct-residue3-0930/README.md); register restated 2026-10-01 by OPUS for SWE2-DATA.)*
- [x] **UQ-156.** What each page draws, and the message protocol of the `0xBC08` pages (`002B7B80` and `002BAF80` are "unparsed" in the
  handler census). **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5)**, by the narrowings below: the protocol arm by arm,
  the map picture, lines, icons and labels each page draws, and the containers' lifetime.
      *Narrowed 2026-09-18 (FABLE): the protocol half is read arm by arm; what the four large arms draw is the residue.* Both procedures were decoded through the tables §2.3a located, arm by arm (each arm runs from its case target to the next target). The eleven small arms are the same code in both, up to the page's own record fields: **15** (about to be destroyed) sets bit 2 of the page's flag word `+0x13A` (`002B8B16`; the location map also runs the base handler `002470C0`, `002BBEFA`); **19 / 20** call `002D7580(0, 1)` (`002B8B24`–`002B8B2B`), the transition helper the license-board page names; **8 / 9** call `0027FB30(id == 8)` (`002B8B35`–`002B8B40`), one flag for the pair; **40** (`0x28`) stores the message's word `+8` at page `+0xBBE6` (`002B8B4A`); **37** (`0x25`) latches the 60 Hz tick `0208F570` at `+0xBBE8` and the message bytes `+8` / `+0x10` at `+0xBBE4` / `+0xBBE5` (`002B8DF2`–`002B8E0E`); **38** (`0x26`) clears that pair to `0xFFFF` (`002B8E17`); **42** (`0x2A`) queries the page's map slot `+0x138` through `003C02B0` (§2.6's slot query) and, unless the slot's `+0x10` has bit 15 set, runs `0029E330(0xD)` then `0029E790(0x5D)` and returns 1 (`002B8DAC`–`002B8DF0`); **33** (`0x21`) is the slot load §2.6 reads (`003C2190` three times inside the pool scope `00249580` .. `00249410`, eviction through `003C21C0` / `003C21B0`); **16** (resource batch complete) releases the slot through `003C2200` and rebuilds through `00246AC0` (`002B7D5B`). The four large arms differ between the pages and are read only to their callees: **1** (construct) links the record through `00247570`, `004022D0` and `00247930` and reads `01E0C1D8` / `01E0C1DC` (the location map first sizes two `0x80`-byte buffers through `002C9430`); **2** (generation reconcile) runs `001EDEC0`, `00403330`, `00403180` and `002B66E0` (the location map adds `003C5120`); **14** (opening transition, 1,369 B / 1,483 B) builds the page through `003C02B0` twice and `00402230` twice, then ~~`002B6DB0` / `002B7460` / `003BED70` / `00271CB0` on the track map and `002CC9B0` / `002CC960` / `00249C60` / `002BC3E0` on the location map~~ *(Superseded 2026-09-26 (FABLE): both pages run `002B7460` / `003BED70` / `00271CB0`. The dispatcher is `002B6DB0` on the track map and `002BC3E0` on the location map, and only the location map adds `002CC9B0` / `002CC960` / `00249C60`. See the arm 14 reading.)*, and only the track map reads `TrackMapScale` `01E0CE70`; **10** (directional input, 189 B / 1,407 B) ~~is a cursor step on the track map (`00254560`, `InputGameplay_TestCombinedMask` `00250200`, `002B6260`) and a full list walk on the location map (`00249C60` five times, `002B9B30`, `002BA310`, `003BF8E0`)~~ *(Superseded 2026-09-26 (FABLE): the track arm is a close, a hand-off to its command dispatcher `002B6DB0`, and a rescale. The location arm confirms by marker kind, cancels, toggles the zoom, dispatches and steps the marker. See the arm 10 readings and the consumer check [uq156-arm-readings](../../_index/candidates/uq156-arm-readings/consumer-check.md).)*; **4** (draw after content, 1,787 B / 402 B) is the track map's own drawing (`003C8060`, `003BE2D0`, `003DFBB0`, `003DFB50` each twice, `002B6B50` twice, the 2048-unit origin `00900384`) against the location map's short pass (`002BD590`, `00404230`, `004043B0`, `004044D0`); **39** (`0x27`, 593 B) is shared drawing through `00402250` (the page helper `UQ-158` read), `003C3F90` and `00202B70`. So the vocabulary is one and the bodies differ in four arms; what those four draw on screen is not read. Static: both tables and all thirty-two arms.
      *Narrowed again 2026-09-25 (FABLE, Claude Opus 5.5): arm 4, the draw arm, is read in full on both pages. They share
      one skeleton, and the track map adds a gate, a centring step and a per-frame element rebuild.* Static.
      - **The shared skeleton** (`002B841B`–`002B8B16` track, `002BBD5C`–`002BBEEE` location):
        1. The arm computes the view origin: the scroll words `+0xBBD8`/`+0xBBDA`, scaled by the zoom percentage
           `+0xD4` (divided by 100), plus the base `+0xC8`/`+0xCC`.
        2. It calls the page's drawer. The track map goes through `002B9A20` to `002B8EE0`, and the location map through
           `002BD590` to `002BCB00`. Both pass the marker list `+0xBBC0` (`UQ-158`'s `002B7460`), the current map record
           `+0xBBC8`, the page's `+0x38` object, the map data `+0x130`, the mode word `+0xBBE0`, the zoom, and message
           37's latch (`+0xBBE4`/`+0xBBE5`/`+0xBBE8`).
        3. When the element array `+0xBBD0` exists, it runs ~~`00404230` and `004043B0` over the array~~ `00404230`,
           which draws the map picture, and then `004043B0` over the array, with the `+0x38`
           object's byte `+0x5C` forced to 1 and then restored. *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5):
           `00404230` is not given the array; see the next bullet.)*
        4. It finishes with `004044D0` over the marker list.
      - **The map picture** *(read 2026-09-26, FABLE, Claude Opus 5.5; static)*. `00404230` draws it on both pages, as
        one textured quad. Its texture is the map data's `+0x10` object (`[+0x130]+0x10`, passed as the sixth argument at
        `002B8A8C` and `002BBE93`). The quad sits at the draw record's `+0x50`/`+0x52` plus the view origin and is scaled
        by the zoom. Before the quad emit, the routine pushes four GS register records, which
        [the GS layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) names:
        - `TEX0_1` is the texture's `+0x30` qword plus `4 × byte[record+0x5C]` in the `CBP` (palette base) field
          (`00404284`–`00404297`);
        - `TEX1_1` is `0x60` (`MMAG` = `MMIN` = linear, by the register layout);
        - `CLAMP_1` is a region clamp to the texture's width and height, `[+0x20]+0x14`/`+0x16`;
        - `TEST_1` is `0x3001`, the configuration the GS page finds on every authored `TEST_1`.

        So byte `+0x5C` of the widget's draw record ([the widget contract](../Widget-Object-Model/CONTRACT-widget-object.md)
        `+0x38`) is a palette-bank index, and the picture is always drawn with bank 1: both arms force it to 1 around
        the call. The picture is drawn only while the element array `+0xBBD0` exists (`002B8A28`, `002BBE6A`). Control:
        `_index/candidates/uq156-arm-readings/map_picture.py`, with a known positive (a documented
        packet with the same four tags) and a planted negative (the line pass).
      - **The track map's placement** *(read 2026-09-26, FABLE, Claude Opus 5.5; static)*. The track arm calls
        `002B6B50` twice (`002B88ED`, `002B8A87`) and multiplies the layout width by its result for the picture's
        horizontal centre. The helper reads the ratio `0017FFD0` returns: 16/9 over the display object's width/height.
        - At a ratio of 1 or more (16:9 or narrower) it returns the console-tunable centre x `01E0CE50` (0.67).
        - Below a third (wider than three times 16:9) it returns 1.5.
        - In between, it returns a line in the inverse ratio that meets 1.5 at a third. With the image values of the
          "Super Wide" multiplier and midpoint `01E0CE58`/`01E0CE5C` (1.0 and 21) that is about 0.62 just past 16:9
          and 0.75 at 21:9.

        The four floats are the tuning console's ids 190–193
        ([the console slice](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-F-ids-172-203.md)).
        The helper's arm for ratios at or above midpoint/16 returns `0.67 × multiplier ÷ ratio`, but the first test
        has already returned for every ratio of 1 or more. So that arm runs only if the midpoint is tuned below 16:
        its console bound starts at 15.9.
      - **What only the track map does:**
        - **It draws nothing while system-stop request 10 is active** — the time-stop magick / target-selection cursor
          of [the registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md).
          The test is the registry's is-active check on its active-request bitset (`002B841B`–`002B8427`).
        - **It centres the view on a subject**, chosen by the current record's flag dword `+0x28`:
          - bit 8: the record's kind-5 element at the index `00264770` returns (`002B8617`–`002B86D4`);
          - bit 15: the first marker whose kind-5 element has type `0x14`, `0x17` or `0x18` and passes `003FFF40`
            (`002B86D9`–`002B87EA`);
          - otherwise: the character the battle-menu selection state holds at `022C806C` (written by the battle-menu selection-state builder; the
            controlled character, by inference). Its world position is projected through `00202B70`, and the map's
            layout-cell origin is subtracted (`002B87EF`–`002B88AD`).
        - **The last branch also stores a ~~layer byte~~ palette bank** from the map's cell table into the `+0x38` object's `+0x5C`
          (`002B8872`). ~~So the drawn layer follows where that character stands; that meaning is inferred.~~
          *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the character's position does not choose the entry.* The
          slice `002B882D`–`002B8872` reads only the map data's `+8` atlas, with no float input. The atlas header's
          `word[+0x44]` picks an entry through the index table at `+0x48`. The entry's byte `+7` gives a palette-table
          index (high nibble, table at `+0x42`) plus an offset (low nibble). That is the entry format of the layout
          page's tree-entry decode, which adds the same value into `+0x5C`; this site stores it. The entry's dword `+4`
          anchor is what the arm then subtracts from the projected position. The picture does not use this bank, because
          the arm forces bank 1 around it. The marker drawer `002B8EE0` and the label pass `004044D0` save the byte,
          override it for some draws and restore it, so the stored value is the default bank for their other draws. What
          `word[+0x44]` holds at run time is not read. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: a stated limit. The word sits in the header of the loaded resource the arm reaches through `[[+0x130]+8]+0x20` (`002B882D`-`002B883C`), so its value is that file's data. Which bank each map gets is not claimed, and no claim on this page rests on it.)*
        - **It rebuilds the element array** `+0xBBD0` every frame through `00402A40` (`002B8A19`). The location map's
          arm 4 never builds it.
      - **In player terms (inference from the mechanism):** the track map is a live map centred on the controlled
        character or on a designated point, hidden during target selection. The location map draws the same layers at
        a scroll position the player moves, with no subject to follow.
      - *Still unread:* what the two drawers `002B8EE0` and `002BCB00` put on screen, element by element, and arms 1, 2,
        10 and 14 beyond their callees. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: the arms are read in the narrowings below, 2026-09-26: arms 1 and 2 on both pages, both arm 10s and both arm 14s. The drawers are read below as one pulsing icon per marker, and how the two differ is answered below. A stated limit: no draw-call-by-draw-call account of each icon's passes is claimed.)*
      - *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): the track map's drawer is already read, as an icon drawer.*
        - **One icon per marker.** `002B9A20` walks the marker list: it calls `002B8EE0` with the current node
          (`002B9AE0`), then follows the node's `+0x60` link (`002B9AE5`). One node, the one equal to a stack argument,
          is passed a caller value where every other node gets −1 (`002B9AB0`); it is probably the highlighted marker. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: settled. The stack argument is the page's current marker `+0xBBC8` (loaded at `002B88F2`, passed at `002B89C9`), and the value it receives is message 37's latched byte `+0xBBE4` (`002B899F`). The location walker gets the same pair (`002BBD80`/`002BBE52`, `002BBE2C`). So the current marker is drawn with the latch byte and every other marker with -1. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) D1-D2.)*
        - **What each icon is.** [The blinking icon and its atlas](../../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md)
          reads `002B8EE0` itself, without knowing whose icons it drew. The icon comes from a packed atlas when the
          node's `+0x02` is 1, and from a sized resource otherwise. Optional passes add an outline and the node's
          sub-items. Brightness pulses with a 60-tick period, and the pulse depth is authored at the node's `+0x50`.
        - **The offset it reads.** The "global Y offset" that page reads at `002B9058` is
          `ExtraTrackMapJumpIconOffsetY` (`0209E5AC`, the table in §2.1).
        - **The location map is a twin.** `002BD590` walks the same list the same way: one call per node
          (`002BD63A`), the `+0x60` link (`002BD63F`), and the same single-node substitution (`002BD60B`). Its drawer
          `002BCB00` makes the same atlas test on the node's `+0x02` (`002BCB2F`) and the same 60-tick pulse
          (`002BCE28`, `002BCEBF`). So both maps draw a pulsing icon per marker. How the two drawers differ inside is
          not read. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20, answered by a census of both bodies: the two drawers make the same calls except these. The track drawer sets the scissor directly through `00249FD0` four times, makes one more `002D8530` call, tints with `TrackMapColorR/G/B/A` (`01E0CE60`-`01E0CE6C`, read at `002B93B6` and `002B9502`), places against the 512 x 448 screen through `002B6B50`, `01E0CE54` and the 2048 origin `00900384`, and reads two floats with no layout key, `01E0CE78`/`01E0CE7C`, as integers. The location drawer clips through the offset-apply `002DD2F0` three times (it runs `00249EE0`, then `00249FD0`), calls `00249EE0` once more, and scales its icons by `BaseMapJumpIconScale` (`01E0CE80`, `002BCC0C`). Each reads its own jump-icon offset pair (`0209E5A8`/`0209E5AC` against `0209E5D8`/`0209E5DC`). Both call `003BC160`, `003BDCD0` and `003BDB30`. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) C1-C5.)*
        - *Still unread:* arms 1, 2, 10 and 14 beyond their callees. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: read below, 2026-09-26: arms 1 and 2 on both pages, both arm 10s and both arm 14s.)*
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): the track map's arm 10 (message `0x0A`, `002B82D7`–`002B8394`,
        189 B) is read in full.* The arm is found through the procedure's own index and case tables. It is the
        per-message input step of an open page:
        1. **Gates.** It does nothing while `+0xE0` bit 0 is set (`002B82D7`), and it takes the default arm unless the
           page state `+0x13A & 6` equals 2 (`002B82E1`–`002B82ED`). It calls `00254560(1)`, a seven-case predicate,
           and ignores the result.
        2. **Close.** If the input snapshot's filtered word `02F97392` has bit 1 set, or the combined-mask test
           `00250200` passes, **and** the container's `+0x179D2` bit 11 is set, the arm clears `0209E5B0` and calls
           `002B6260` (`002B82FD`–`002B832A`). That routine acts on the track-map container `0209E5C0` through
           `00244F00`: message 15, then teardown. The page closes.
        3. **Commands.** Otherwise, unless `+0x13A` bit 3 is set, it hands the message to the page's command dispatcher
           `002B6DB0` (`002B832F`–`002B833F`). The dispatcher has a `0x26`-case table and defaults the zoom `+0xD4` to
           100.
        4. **Rescale.** If `+0xE0` bit 0 is now set, the arm clears `+0x13A` bit 0 and rescales the marker list
           `+0xBBC0` by zoom ÷ 100.0 (`008F3134`) through `00403130` (`002B8344`–`002B8376`). If `+0xE0` bit 1 is set,
           it clears `+0x13A` bit 0 as well. It returns 0.
        *Not established:* what `00254560`'s case 1 tests, and what the container's `+0x179D2` bit 11 means (by its
        use here, it is the condition that lets the cancel input close the page). The location map's arm 10
        (1,407 B) and arms 1, 2 and 14 remain. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: all closed below. `00254560(1)` is the constant 1 (the location arm-10 reading, 2026-09-26), bit 11 is MS-1 (answered 2026-09-29), and the remaining arms are read 2026-09-26.)*
      - *Arms 1 and 2 read in full on both pages, 2026-09-26 (FABLE, Claude Opus 5.5).*
        - **Arm 1 (message `0x01`, construct; track `002B7C0C`–`002B7CBA`, location `002BAFF0`–`002BB0C2`):**
          1. It stores the message's `+0x10` pointer as the page's map data `+0x130`, then attaches through `00247570`
             with a static descriptor.
          2. It loads the page's layout size from `01E0C1DC` (`0x1C0` = 448) and `01E0C1D8` (`0x200` = 512) into `+0x9E`
             and `+0x9C`: the PS2 screen size. It zeroes `+0x98` and copies the pair to `+0xBBEC`/`+0xBBEE`.
          3. It takes the map slot `+0x138` from the message's word `+8`; a negative value becomes 0.
          4. It initialises the marker highlight's rectangle tween at `+0x108` (C-13's `RectTween`, OPUS `7b543c07f`)
             through `004022D0`, sends itself message `0x26` (clearing the message-37 latch
             pair) and finishes with `00247930(page, 0xD3)`.
          5. The location map (`002BB00B`–`002BB02C`) lays itself out below the top screen band. It calls
             `002C9430(0x80)` twice, stores the result at `+0x9A` (its top) and subtracts it from 448 for `+0x9E`. It
             finishes with `00247930(page, 0x63)`.
             - `002C9430(0x80)` reads the band record `[0209AC30]+0x2B8`. It returns `+0xDA` + `+0xD6` while the
               record's `+0xD0` bit 0 is set, and `+0xCE` otherwise.
             - An index other than 0 selects `+0x2C8`, and on the bit-7 path it returns 448 minus the sum.
             - The world-map rows above call this function's `(0)`/`(1)` results "pads". They are these band extents,
               not controller reads.
        - **Arm 2 (message `0x02`, generation reconcile; track `002B8394`–`002B841B`, location `002BBCD0`–`002BBD5C`):**
          1. It acts only when `001EDEC0([+0xB4])` is non-zero. It steps the highlight tween at `+0x108` toward its target (`00403330`, an ease-out) and runs the marker
             list `+0xBBC0` against the current map record `+0xBBC8`; in mode 6 no record is passed (`00403180`).
          2. It re-centres through `002B66E0` when `+0x13A` bit 0 is set, a record exists and `+0x13A` bit 3 is clear.
          3. It copies the record's rectangle (`+0x30`..`+0x37`) into the tween's target (`+0x110`) as one qword, without
             resetting the blend, so the highlight glides to the moved marker.
          4. The location map adds one call, `003C5120`, before the refresh.
        - *Still unread:* the location map's arm 10, and arm 14 on both pages. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: both read in the next two narrowings, 2026-09-26.)*
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): the location map's arm 10 (message `0x0A`,
        `002BB751`–`002BBCD0`, 1,407 B) is read in full, and `00254560`'s case 1 is closed.* Static. `r14` is the page
        and `rdi` its container (`+0xBBF0`, `002BAFB8`). The arm is the location map's input step. Its gates are the
        track map's: nothing while `+0xE0` bit 0 is set, and the default arm unless `+0x13A & 6` equals 2.
        - **`00254560(1)` is the constant 1.** Case 1 of the seven-case table lands on the same arm as an index above 6,
          which returns 1 without reading anything. The track map ignores the result. The location map branches on it
          (`002BB781`–`002BB783`), so the path at `002BB785`–`002BB7DC` never runs. That path is a close on
          `02F97392` bit 15, gated on mode ≠ 6 and container `+0x179D2` bit 11.
          - The domain of "never" is this procedure: no direct jump in it targets that range, and no case-table arm
            starts inside it.
        - **Confirm on the current marker** (`002BB7E1`–`002BB96B`). The confirm needs `02F97392` & `01E0C2A0`,
          container bit 11, a current marker `+0xBBC8` and `+0x13A` bit 3 clear. It then branches on the marker's kind
          byte `+2`:
          - **Kind 0:** `002BA310` opens a `0x3E0`-byte child page on the marker. It opens nothing, and returns 0, when
            the global byte `0209A2A9` is set or a count it computes from the marker is not positive. On success the
            arm clears `+0x13A` bit 0 and plays sound 2; otherwise sound 5.
          - **Kind 1, a link** (`+0x1C` bit 0 set; otherwise sound 5). The arm plays sound 2 and saves the zoom
            `+0xD4` to `0209E5E8`, except in mode 6. It sets container `+0x179D2` bit 9 and attaches the marker's
            descriptor (a default when `+0x20` is `0xFF`). It stores the marker's `+0x20`/`+0x22` at container
            `+0x179D9`/`+0x179DC`, sets `+0x179DE` to 1 and evicts the other cached slots (`003C21C0`). It then closes
            the page through `00244F00`, sets container bit 7 and makes the marker's byte `+0x21` the container's slot
            `+0x179D0`. `003BF8E0` is called on the old slot and its result is discarded.
          - Any other kind falls through to the cancel step.
        - **Cancel** (`002BB970`–`002BBA42`). The button in `01E0C2A4` (`0x4000`) closes the page whenever container
          bit 11 is set. The filtered bit-0 input test closes it too, but only when the "keep open" flag is clear.
          - The flag is set when container `+0x179D2` bit 10 is clear and the mode is not 6. With `02B457D8`
            non-zero, the condition is mode not 5.
          - The close attaches the default descriptor and plays sound 3. When the flag is set it broadcasts message
            `0x1F` to the page's children (`00275440`).
          - It then runs `002CC9B0`/`002CC9C0` and the location map's closer `002B9B30`. That closer sends the
            current page slot through `00244F00`, sets container bit 3 and releases the two sibling objects at
            `0209E600`/`0209E5F8`.
          - Finally it stores 3 in `02092750` if `0209E5B0` is non-zero, and 0 otherwise.
        - **Zoom toggle** (`002BBA47`–`002BBAF7`, `+0x13A` bit 3 clear, `+0xE0` bit 0 clear). The trigger is the
          button bound to input id `0x110`, tested against `02F97392`. `003BE680` returns the map slot's default zoom
          and writes its two other levels. The arm sets the first level when the zoom equals the second, and the second otherwise, through the
          page's zoom setter. It saves the new level to `0209E5E8` (except in mode 6) and passes `0xC80` ÷ zoom to a
          marker-list routine.
        - **Commands and rescale.** It passes the message to the page's command dispatcher `002BC3E0` (the location
          map's counterpart of `002B6DB0`). It then rescales the marker list by zoom ÷ 100 through `00403130` when
          `+0xE0` bit 0 is set, exactly as the track map does.
        - **Marker step** (`002BBB47`–`002BBCAF`). With a current marker and `+0x13A` bit 3 clear, the arm feeds the
          directional snapshot words `02F97392`/`02F97390`/`02F97394` to a marker-list routine. The words are zeroed
          when `+0xE0` bit 0 is set, the mode is 6, `02B457D8` is non-zero, or the global byte `0209A2A9` is set. The
          step returns the new current marker. On a change the arm:
          - plays sound 1;
          - clears the old marker's `+0x4E` bit 0 (setting bits 1 and 2 when it is a link);
          - sets bit 0 and clears bits 1 and 2 on the new marker;
          - fills a record from the new marker's `+0x10` and hands it to a list routine. Outside mode 6, with
            `02B457D8` clear and marker `+0x28` bit 8 set, the record's second pointer is instead looked up by the
            active field id;
          - retargets the highlight tween at `+0x108` on the new marker (`00402610`: the current rectangle becomes the
            blended one, the target the marker's, the blend 0), and sets `+0x13A` bit 0.
        - ~~*Not established:* what container `+0x179D2` bits 9, 10 and 11 mean as states.~~ **Answered 2026-09-29 (FABLE,
          Claude Opus 5.5; MS-1; `_index/candidates/ms-map-screens-fable/ms_states.py` C 9 10 11, a census of every write
          to the word with each register source traced):** bit 11 gates every close and the confirm in both arm 10s; bit 10
          selects the copied map data (§2.4, `002BA040`) and here clears the "keep open" flag.
          - **Bit 9 is the reopen request after a link.** The link path above sets it, and nothing else does. Each page's
            per-frame step clears it, and only once both page slots are empty and it has called the reopen.
          - **Bit 10 means "opened in mode 5".** Only the two mode-5 openers set it: the fullscreen procedure's location
            opener, and the track opener that creates its container with bits 8 and 10. Nothing clears it, so it holds for
            the container's life.
          - **Bit 11 is the confirm latch.** It is set once, at the end of the location map's confirm, and never cleared.
            After one confirm, every later close and confirm is refused until the container dies. The track map tests the
            bit but never sets it, so its gate is always open.
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): arm 14 (message `0x0E`, the opening) is read in full on both
        pages* (track `002B7D7E`–`002B82D7`, location `002BB186`–`002BB751`). Static. The two arms run the same sequence
        against their own container, dispatcher and saved-zoom global:
        1. **Map data and slot flags.** The arm copies container `+0x190` to page `+0xC0`. It then queries the map slot
           `+0x138` (`003C02B0`) and sets `+0x13A` bit 3 from the slot's `+0x10` bit 15, the bit arm 42 also tests.
           Arm 10 tests that bit: on the location map it disables the confirm, zoom toggle, dispatcher and marker
           step; on the track map it disables the dispatcher.
        2. **Location map only.** It plays sound `0x4C` after `002CC9B0`/`002CC960`. It also installs a callback on the
           shared `0xD0`-byte object `00402680` returns. The callback acts only once the location container and
           `0209E5F8` are both gone.
        3. **Commands and map.** It passes the message to the page's command dispatcher (`002B6DB0` / `002BC3E0`) and
           builds the map through `003BED70(slot, mode)`.
           - If that returns 0, the track map skips to step 9.
           - The location map does the same, unless `02B457D8` is non-zero, in which case it skips only the layout.
        4. **Layout.** It centres the returned map on the 512×448 screen, writing the view origin `+0x128`/`+0x12A`, the
           centre `+0xD0`/`+0xD2` and the scroll words `+0xBBD8`/`+0xBBDA` (with `00271CB0`). It sends itself message
           `0x1D` and builds the marker list `+0xBBC0` (`002B7460`).
        5. **The arriving marker.**
           - Outside mode 6 (and, on the location map, with `02B457D8` clear), when the container's word `+0x179DE`
             is non-zero, the current marker `+0xBBC8` is the one
             whose id is the container's byte `+0x179DC`. That marker gets `+0x4E` bit 0 set, bits 1 and 2 cleared,
             `+0x4C` = `0x80`, `+0x50` = `0x100` and `+0x38` = 1.0.
           - Otherwise, including when no marker has that id, it is the list's first marker (`00402230`).
           - Mode 6 (and, on the location map, a non-zero `02B457D8`) takes a list default instead.
           - On the location map these are the fields arm 10's link path writes: `+0x179DC` from the link marker's
             `+0x22`, `+0x179DE` = 1, and the new slot in `+0x179D0`. So following a link opens the next map on the
             marker it names.
           - Not traced here: who re-opens the page after the link's close, and who clears `+0x179DE`. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: both found below, 2026-09-26: container bits 7 and 9 drive the re-open, and `+0x179DE` is never cleared.)*
        6. **Zoom restore.** `003BE680` gives the slot's default zoom and two other levels. Mode 6 takes the first
           level. Otherwise the saved zoom (track `0209E5B8`, location `0209E5E8`) is kept when it equals one of the
           three, else the default is used, and the result is saved back. The marker list is given `0xC80` ÷ zoom.
           The page's zoom setter then receives:
           - on the location map, that restored level;
           - on the track map, `TrackMapScale` `01E0CE70` (150).

           Both then clear `+0xE0` bit 0, set `+0xD8` to `0x100` and run `002B6AE0` with the same value.
        7. **Centre on the marker.** With a current marker and `+0x13A` bit 3 clear, it snaps the highlight tween at `+0x108` onto
           the marker (`004026D0`), retargets it there (`00402610`) and marks the marker current. It sets `+0x13A` bit 0 and repeats `002B66E0` until `+0xC8`/`+0xCC` stop changing, at
           most 64 times, then clears bit 0 again.
        8. **Description and elements.** It builds the description record for `00402490` from:
           - the slot's name (`002543A0`, or the slot's alternative through `003BF6C0`) and `002543D0`'s value;
           - a mode-dependent second pointer. Outside mode 6 this is a lookup by the active field id when marker
             `+0x28` bit 8 is set. In mode 6 it is a search through `003BC160` when bit 6 is set, and a hit there also
             runs a map-data routine on `+0x130`'s `+8`.

           It then builds the element array `+0xBBD0` through `00402A40(+0x140, 0x100, slot, mode)`.
        9. **Close-out.** The location map runs `002470D0` on the page. Both broadcast message `0x2B` to the page's
           children (`00275440`) and return 0.
        - *Still open on UQ-156:* the meaning of container `+0x179D2` bits 9–11, the reopen after a link, and what
          each page draws (arm 4's callees). *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: all three answered since: MS-1 (2026-09-29), the re-open in the next narrowing, and UQ-156.)*
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): container flag bits 7, 9, 11 and 13 are read from their
        writers and readers, and the re-open after a link is found.* Static. The location container's procedure
        `002BA700` is itself a message procedure. Its per-frame step is id 2; id 32 sets bit 7, id 41 is a query, and
        id 43 sets bit 13.
        - **Bit 13** is set by container message 43 (`002BAE6A`–`002BAE86`). The first time it is set outside mode 6,
          the arm calls `003C1DF0`.
        - **Bit 11 means the page is up.** The id-2 step sets it (`002BA90B`–`002BAA79`) when these hold:
          - bits 3 and 11 are clear and bit 13 is set;
          - the current page slot reports ready through `00273A20`, and the page's `+0x40` bit 9 is clear;
          - outside mode 6, `003C0CC0` passes.

          It then runs one of two entry sequences and sets bit 11:
          - a band animation through `002C9490` (which clears bit 12); or
          - message `0x2A` to the page after `0035C080`, which sets bit 12.

          Id 41 answers "bit 11 set and `003BD890` non-null". Every close and confirm in both arm 10s waits on this
          bit, so they are ignored until the page is up.
        - **Only the location container ever sets bit 11.** The track container `002B7590` has the same guard
          (`002B776A`–`002B77C2`: bits 3|11 clear, bit 13 set, slot ready, `003C0CC0`), but it discards the result and
          writes nothing. The field-time container `003CB650` only tests the bit.
          - So the track map's arm-10 close never runs. Its closer `002B6260` has four other call sites:
            `00253C70` (twice) and two further routines. Which of those fire is not traced here. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: the two routines are named. `002B6260` has five direct call sites: `00253C70` at `00253C92`, taken on every call while the byte `02092750` is not 3, and at `00253EA4`; the request reset `00252DE0`, whose first call it is (`00252DE4`) and which only the area unload `002628B0` calls (`00262DCE`); `002B6140`, which releases a ready page through `00247870` and then tail-jumps into it (`002B6194`), called from `00251F40`, `00254AC0` and `00255330`; and the dead arm-10 close `002B8325`. Each returns at once when `0209E5C0` is null. Which of them closes a given track map in play is a stated limit, not a question about the code. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) B1-B4.)*
          - Domain of "only": every instruction carrying the displacement `0x179D2`. That is 109 sites, 49 of them
            writes; their register sources are resolved and the three full-word stores checked. Register-base
            accesses without the displacement are outside it.
        - **Bit 7 is an open request, and bit 9 holds it** (`002BAB71`–`002BABE7).
          - When bit 7 is set and bit 9 is clear, the id-2 step opens slot `+0x179D0` in mode `+0x179D8` through
            `002B9D30` (§2.3) and clears bit 7 once that succeeds.
          - When bit 9 is set, it waits until neither page slot's `00273A20` returns 1. It then runs `003C21B0` and
            clears bit 9, and the open follows on a later step.
          - Id 32 also sets bit 7. It first refreshes `+0x179D0`: from `003BC160` in mode 6, otherwise from a slot
            lookup when bit 8 is set.
        - **So a link runs end to end.** Arm 10's link path sets bits 9 and 7 and stores the new slot and the arriving
          marker's id. It then closes the page. The container waits for the old page's slots to settle, re-opens the
          location map on the new slot, and the new page's arm 14 selects the marker by that id.
        - Bits 8 and 10 are set by `002BA020` / `002BA000` on the fullscreen route (`0028E660`, §2.4). Bit 10 is the
          map-data copy flag §2.4 names.
        - *Controls:* `_index/candidates/uq156-arm-readings/uq156_bits.py` (census, with the
          location setter planted as a known positive; FAILS 0) and `uq156_arms.py`.
        - *Still open on UQ-156:* what each page draws (arm 4's callees), what `003C1DF0` and `003BD890` do, and who
          clears container `+0x179DE`. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: answered in the next narrowing: both callees were already documented, and `+0x179DE` is never cleared.)*
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): the two callees were already documented, and
        `+0x179DE` is never cleared.* Static.
        - **`003C1DF0` and `003BD890` were already on record.** The line above listed them as open; that was a miss on
          my part, because the database had them before this section was written.
          - `003C1DF0` is the lazy install of the `menumap_common` sub-location directory into the map-data widget's
            `+0xF0`/`+0xF8` ([cmap page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cmap-menumap-common-sublocation-directory.md);
            the layout-parameter page describes its gates).
          - `003BD890` indexes that block by the `+0xF0` header's word `+6` (this page's widget table).
          - So bit 13 records that container message 43 has arrived. Outside mode 6, the directory install has been
            attempted by then. The "page up" query (id 41) also needs the directory entry to exist.
        - **`+0x179DE` is set by every link and never cleared.** Its only store is the location link path
          (`002BB928`, value 1). The domain is every instruction carrying the displacements `0x179DC`–`0x179DF`: two
          stores and four reads, all on the two map pages.
          - After the first link, every later opening of that container's page takes the last link's marker
            (`+0x179DC`) as the arriving marker, for as long as the container lives.
          - On the track container neither field is ever written. Its arm-14 branch therefore rests on the container's
            initial contents, which this page does not read (the allocation's zeroing is not traced). *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: the zeroing is read. The track container comes from the widget factory `00244F50` (`002B63A0`), which hands the new object to `002465F0`; that clears all `0x179E0` bytes with `memset` (`00246626`; the import slot `008C2A60`) before the procedure is installed. No instruction stores at `+0x179DC`-`+0x179DF` outside the location page, so on the track container that word stays 0 and arm 14 takes the list's first marker outside mode 6. Limit: a displacement census does not see a block copy. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) A1-A5.)*
        - *Still open on UQ-156:* what each page draws (arm 4's callees), and the container's lifetime (who destroys
          `0209E5F0`). *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: answered below, in the containers' lifetime narrowing, 2026-09-26.)*
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): the element nodes are the lines between the location's
        areas.* Static.
        - **Which points.** `00402A40` asks the draw-list builder `003BE3A0` for selector 0. In `003C1A20` the selector
          is a point-kind filter: a point is kept only when `003BF430`'s kind equals it (`003C1BCC`–`003C1BD4`), and
          selector 2 skips the test. The constants beside it are capacities, checked at `003C1CA7`: 20 kind-0 points,
          16 kind-1 points, or 24 of either. So the element pass takes the **field points** (lmap array A), while the
          marker list (selector 2) takes every point.
        - **What each node is.** `003C0890` expands each field point into 16-byte records, and `004023D0(list, rec)`
          returns 1 when a listed node already holds the same **undirected segment**: the two ids at `+0x80`/`+0x82`
          and the two endpoints at `+0x84`/`+0x86` and `+0x8C`/`+0x8E` match in either order (`004023E0`–`0040246F`).
          A record that is not yet listed becomes a `0xB0`-byte node: it is zero-filled, the record is copied to
          `+0x80`, `004027D0` is applied and the node is linked through `+0x98`/`+0xA0`. The nodes sit in place in
          the page's array at `+0x140` (capacity passed as `0x100`), and the head goes to `+0xBBD0`.
          So the elements are the connections between the location's areas, each drawn once. This matches the lmap
          file's array C, whose entries pair two field ids of the same record.
        - **How they are drawn.** `004043B0` walks the list and draws each node through `00274CA0`. A node whose
          `+0xA8` bit 0 is set is modulated by `sinf` first. No instruction in the page procedures or the
          `00402000`–`00405000` helpers writes `+0xA8`, and the node is zero-filled, so within that domain the pulse
          never runs.
        - *Still open:* what the track map's own drawing adds (its arm-4 callees, such as `003C8060`), and the
          location container's lifetime. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: both answered in the next narrowing, 2026-09-26.)*
      - *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): the containers' lifetime, and the rest of arm 4.* Static.
        - **The track map's own drawing** is the map picture and the placement above, plus two setup calls:
          - `003C8060` returns the block at `02B457F0`, and the arm negates its floats `+0x10`/`+0x14`
            (`002B85A9`–`002B85D8`) before its transform call. One setter writes those floats; ~~what they mean is not
            read here.~~ **they are the current sub-location picture's world origin** *(answered 2026-09-29, FABLE; MS-2;
            `ms_states.py` O)*. The setter's only caller is the sub-location transform of
            [the `sloc` container page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md)
            (§4), which passes the `NPS2` record's originX / originZ. So negating them translates a world position into the
            picture's frame, before the 4-pixels-per-unit scale.
          - the arm's first call publishes a fixed render-command packet (the slot publish of
            [drawing one coloured rectangle](../../99-Unresolved-Residual/drawing-one-coloured-rectangle.md)).
          - The label pass `004044D0`, on both pages, walks the marker list (`00404570`–`004046D1`). Each atlas-kind
            marker (byte `+2` = 1) with a non-zero word `+0x4C` gets its `+0x10` string drawn through the text-draw
            entry `002D8670`, at the marker's `+0x18`/`+0x1A` scaled by the zoom plus the origin. The pass uses palette
            bank 0 and scales the record's alpha `+0x58` by `+0x4C`/128. The text is grey (`0x80404040`) unless marker
            `+0x4E` bit 3 or `+0x1C` bit 0 is set. A string equal to text `0x3EC` is dropped unless a shared flag check answers.
            The record's `+0x58`, `+0x5C` and `+0x90` are restored after each marker.
        - **A container lives from its creator's store until its own per-frame step releases it.** Nothing else writes
          the two globals: each has exactly two rip-relative writes, the create store (`002B9D85` location, `002B63A8`
          track) and the clear below.
          1. A closer (`002B9B30` location, `002B6260` track) releases the current page slot through `00244F00` and
             sets container `+0x179D2` bit 3. These two stores are the only bit-3 setters among all 109 sites that
             carry the displacement.
          2. Each later per-frame step (message 2; `002BABFD` location, `002B785C` track) first releases the child at
             `+0xC0` while it is up, unless the container's byte `+0x180` bit 0 holds it. Once the child and both page
             slots are gone (the handler-pointer test `00273A20`), the container calls `00245020` on itself.
          3. That notify tail-jumps to the release `002482E0` unless the widget defers
             ([the widget contract](../Widget-Object-Model/CONTRACT-widget-object.md) §16). The release enters the
             continuation the container's arm 1 stored at `+8` (`002BA6B0` location, `002B7540` track), which clears
             the global (`0209E5F0` / `0209E5C0`).
          4. When the sibling object (`0209E5F8` / `0209E5C8`) and the shared cursor singleton `02B62D78` are also gone,
             the continuation copies the container's saved 6-byte record (`0209E608` / `0209E5D0`) to
             `[0209AC30]+0x3E0` through `00285F00`. That is the cell the world map's exit report also writes. It then
             tail-calls `002814E0` with `0x417` / `0x4EA`.
        - **When that happens.** The location closer has two call sites, both in the location page. `002BB7D7` lies in
          the range shown dead above, so only the cancel close (`002BBA2A`) runs it. A link keeps the container: it
          releases only the page (`002BB941`) and sets the open request. That is why `+0x179DE` carries into later
          openings, until the player cancels out of the location map. An ancestor's release would also end a
          container, since the continuation runs on every release; ~~which ancestors can be released is not read here.~~
          **It has none** *(MS-3, answered 2026-09-29, FABLE, Claude Opus 5.5; `_index/candidates/ms-map-screens-fable/ms3.py` K P N F)*:
          both containers are created parentless and never attached (the constructor only allocates; the creators attach
          only the page under the container; no tree-attach routine is handed a container), so that route is empty.
          Control: `_index/candidates/uq156-arm-readings/container_lifetime.py`, 16 checks, with the two closers as
          planted positives and a `0x400` setter as a planted negative.
- [x] ~~The role of each of the 108 members beyond the accessors read on the lmap page.~~ **Read (§4):** every
  member has a role line with an interior citation, grouped by the screens that reach it.
- [x] **UQ-157 ANSWERED 2026-09-15 (OPUS) — they are the world map's *reopen arguments*, and
      `0028E790` does nothing with them but replay them into the installer this page already
      documents.**
      - **Their widths are settled by the accesses, not assumed.** `+0x10FA2` is a **byte**
        (`cmp byte [rax+0x10FA2], 3` at `0028E7AF`; `movzx ecx, byte` at `0028E7C8`), `+0x10FA6` is
        a **word** (`mov word [rax+0x10FA6], cx` at `0028E7BA`; `movzx edx, word` at `0028E7CF`),
        and `+0x10FA8` is a **dword** (`mov ecx, dword [rax+0x10FA8]` at `0028E806`).
      - **The byte and the word are the installer's two arguments.** `0028E7D6` calls
        **`00550400(kind = byte[+0x10FA2], arg = word[+0x10FA6])`** — the field-menu installer
        §“The installer and the two procedures” already describes, which builds the
        `0x188`-byte host widget with procedure `00552250` and stores it into `02CA8F38`. So the
        saved byte **is** that `kind` and the saved word **is** that `arg`.
      - **The `3` is a validity test on the pair, and this is the behavioural part.** `0028E7AF`
        compares the byte against `3` and, **when it is anything else, zeroes the word first**
        (`0028E7B8`–`0028E7BA`) before reloading the base and reading both back. So **the saved
        `arg` is only carried across when `kind == 3`**; every other kind reopens with `arg = 0`.
      - **The dword is a second request's payload.** `0028E7F3`–`0028E815` clears a 16-byte stack
        request, writes `dword[+0x10FA8]` into its `+0x08`, and passes it to **`00550540`** — the
        same helper this page's §3 request-router row already lists — followed by `00550610`.
      - **Between the two, an unrelated bit is replayed:** `00550510((dword[+0x10F68] >> 12) & 1)`
        (`0028E7E2`–`0028E7EE`), which comes from a different saved field and is named here only
        so the sequence reads completely.
      - **What the values *mean* is one hop further and is not claimed.** `kind`, `arg` and the
        dword are carried verbatim; naming which map or which cursor position they denote needs the
        installer's own consumers (`002901D0`, `00244F50`) and `00550540`'s, none of which this
        reading follows. **UQ-157.** *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: the kinds are named since, on [the request router](../Request-Router/ui-request-router.md) §7 and §7b R5: 1 the field menu's map, 2 the Strahl picker, 3 the airship-route map (the word is the route), 7 the field menu's map opened on its own. A stated limit: kind 6 (`002804E0`) and the dword's meaning are not claimed.)*
- [x] ~~**UQ-158.** The shared page helpers `002B7460`, `00402A40`, `00402250` and `00403970`, and the page sub-widget created by~~
  `00402680` (procedure `00403380`).
  ***ANSWERED 2026-09-17 (FABLE): the four helpers are the pages' marker-list builder, a flag-gated position lookup, a node-list merge and a one-element draw call, and the sub-widget is a lazily built singleton cursor that clears itself on its close message.** `002B7460(page)` clears the page's list pointer `+0xBBC0`, zero-fills a `0x480`-byte scratch of `0x30`-byte entries, asks the map-data block evaluator `003BE3A0(scratch, page +0x138, page +0xBBE0, 2)` to fill it, ORs bit 15 into every entry's dword when `page +0x13A` bit 3 is set (`002B74C3`..`002B74EB`), builds the page's entry list from the scratch through `00402D20(page +0xB140, scratch, n)` into `+0xBBC0`, and, when the page's mode word `+0xBBE0` is 6, runs `00402BF0` over the list (`002B7508`..`002B7519`): the marker list for the page's map. `00402250(outX, outY, field, kind, arg5)` resolves the field's `+0x1C` word through the cached-record search `003BE2D0`, passes the record to `003DFB50(record, kind, arg5)`, the persistent-flag gate, and on a hit returns the entry's words `+4` and `+6` as two ints and 1, otherwise 0 (`00402265`..`004022B1`): a position lookup that only answers for a discovered entry. `00402A40(page, ...)` pulls the page's record through `003BED70`, evaluates the block through `003BE3A0` into a `0x480`-byte buffer, walks its `0x30`-byte entries storing a byte into each node's `+0xCA` through `003C0890`, and ~~where `004023D0` answers 1~~ *where `004023D0` does **not** answer 1 (corrected 2026-09-26, FABLE: a 1 means the segment is already listed, `00402B2A`–`00402B2D` skips it)* applies `004027D0` (the small-record transform) and links the node into the page's doubly linked list through `+0x98` and `+0xA0` (`00402B8F`..`00402B96`): the node-list merge. `00403970(page, x, y, flags, ...)` consults `002551B0` (the field-bits query) and `003C4AE0` under `page +0x28` bit 9, resolves positions through `003BEC50`, `003BECA0` and `003BE2D0`, and hands twenty stack arguments to `00403640` (`00403B0D`..`00403B8A`): one map element's draw. `00402680` builds the `0xD0`-byte widget with procedure `00403380` through the factory `00244F50` only when `02B62D78` is null and stores it there (`00402684`..`004026A4`); the procedure clears `02B62D78` on message 20 (`004033A2`..`004033B4`), and on its build message takes the layout words from `002432B0` into `+0x98`..`+0x9E`, attaches through `00247570` and builds through `00246AC0` (`004034CA`..`00403541`): a singleton cursor sub-widget. The callers place them: `002B7460`, `00402A40` and `00402250` are called only by the two `0xBC08` handlers `002B7B80` and `002BAF80`, `00402680` only by `002BAF80`, and `00403970` by `002B8EE0` and `002BCB00`. Static, bodies read; what each handler draws with them is UQ-156.*

## 8. Evidence

- **Tier 1 disassembly throughout.** Constructors, openers and the flip are read at the cited instructions. Callers come
  from the raw E8/E9 index, and procedure installs from rip-relative `lea` scans.
- **Key → global:** [`layout_key_slots.py`](../Layout-Parameter-System/members/layout_key_slots.py) re-derives all 222 rows from
  `001CA600` and `001AF470`; none is unresolved.
- **Membership:** `members/wm_family.py` and `members/wm_members.py` re-derive the 108 rows. They need the raw call index
  `rawcalls.json` and the frontier lists, and they run from `Database/Tools/work/FABLE/pub140-scratch/`, where those live.
## Falsification pass 1 — 2026-09-14 (OPUS), SURVIVED

**Attacked against the shipping image and this page's own side files, not re-read from its prose.**
Authority `73461d08…`, image base `0x120000`, so every VA below is decoded from the bytes at the
site this page cites.

| # | claim attacked | verdict |
|--:|---|---|
| 1 | the three containers are one `0x179E0`-byte class | **SURVIVED** |
| 2 | each holds two in-place `0xBC08`-byte pages | **SURVIVED**, and the stride is not the size |
| 3 | the map-data widget is `0x278` bytes | **SURVIVED** |
| 4 | the family is 108 functions, 104 on the frontier | **SURVIVED**, reproduced two ways |

**1. The container size.** `mov ecx, 0x179E0` is present at all three cited construction sites —
`002B6394` (track map), `002B9D71` (location map) and `003CB476` (the field-time container, inside
`003CB440`). Three independent call sites carrying the same immediate is what "one class" has to
mean at this level, and it is what the bytes say.

**2. The pages — and the arithmetic closes with 16 bytes to spare.** At `002B9E4A`,
`mov edx, 0xBC08` is the page SIZE, exactly as claimed. Five bytes later at `002B9E4F`,
`imul rax, rax, 0xBC10` is the page **stride**, and `002B9E40` is `lea rcx, [rdx + 0x1B0]`, the
array base. **The stride is 8 bytes larger than the size**, which the page does not say. So the
layout is

    container + 0x1B0 + index * 0xBC10,  each page 0xBC08 bytes
    0x1B0 + 2 * 0xBC10 = 0x179D0   against a container of 0x179E0   — 0x10 left over

**Two pages is the only count that fits.** Three would need `0x235E0`. That is independent
corroboration of the "two in-place pages" claim from the container size alone, and it did not exist
on the page before this pass.

**3. The widget.** `mov ecx, 0x278` at `003BC493`, inside the cited constructor `003BC450`. It is
not in the first `0x40` bytes, which is why a spot check at the function entry would have missed it.

**4. The family count, reproduced twice.** `members/wm_members.tsv` holds **108** member rows of
which **104** carry `frontier = yes` — the page's figures to the digit. `members/wm_family.json`
independently records **77 seed + 31 closure = 108**, and the TSV's `membership` column splits
77 singleton / 31 closure. Two files agreeing on both the total and its decomposition.

### The finding: the figures are checkable, the DERIVATION is not

`members/wm_family.py` is tracked and sits beside this page. It opens `tools/rawcalls.json`,
`arch_frontier.txt` and `c_frontier.txt`. **None of those three is in the repository** — all live
under `Database/Tools/work/`, which `.gitignore` excludes. So a peer can check 108 and 104 against
the committed side files, and cannot re-derive them. That is not a defect in the claim; it is a
limit on who can falsify it, and it now says so here rather than being discovered by the next reader.
Filed as `OPUS-REQ-SWE2-FRONTIER-ATLAS-GENERATOR-INPUTS`.

**Not attacked, and not claimed:** what each page draws, the field-time preloader's driver, and the
role of most members — the page's own PARTIAL list, unchanged by this pass. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: all three are read since: UQ-156 (2026-09-26), MS-4 (2026-09-30) and §4's role lines.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — CLIENT (17 edges through 14 of this page's functions).** The CoreRuntimeScheduling layer reaches this page at `0039BB60`, `0039BF50`, `005542D0`, `00198790` and 10 more. `FUN_001ec760` is the worked example, read in full - it is a 2,232-byte body behind the same `[01F82E38]` gate and the same `001EC560` predicate as the cutscene-override table, and it does nothing at all when either refuses; **1 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT (9 edges through 9 of this page's functions).** The Gameplay layer reaches this page at `00203170`, `002543F0`, `00309EC0`, `00315E90` and 5 more. `BattleEncodedId_DispatchQueryMode0Value` is the worked example, read in full - it is the encoded-id dispatch, and it says how an id is built: `0xFFFF` answers `-1`, the top nibble `id & 0xF000` must be **`0xE000` or below**, and `id >> 12` is the class that selects the arm; **2 of the 3 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Equipment_CheckItemEligibleForSlot`, owned by that layer, calls `00309EC0` on this page. That caller is the slot-eligibility test: the slot index is bounded at 4, the sentinel id `0xFFFF` fails, the item record's `byte[+7] >> 5` must equal the asked-for slot, and when a character record is supplied its `byte[+4]` selects the per-character equip mask that `byte[+9]` is bit-tested against; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT.** `SpawnKeep_RotatePersistenceBanksForAreaTransition`, owned by that layer, calls `003148F0` on this page. That caller is the area-transition bank rotation: it takes a **`0x9428`-byte stack frame** through the stack probe, needs both `[0208E690]` and `[0208E698]`, and compares the current area index against the stored `word[02089372]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**StoryEvent — CLIENT.** `FUN_001ed240`, owned by that layer, calls `00265270` on this page. That caller is a 2,192-byte cutscene-override table: it matches the current area id against hard-coded values such as `0xD70` and `0xD48`, the story-progress word selected by `[01DFE40C]` out of `01F832B0` against a step number, the model's name against string literals such as `g0999` and `c1004`, and the animation time against a window, returning a small override index when all four agree; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 431 edges measured — the seeded row
said 36; the graph has since added the live callers).** The map screens are *drawn by* the render
layer: `Presentation.UI.InputConsumerStateMachine` `002BAF80`/`002B7B80` drive the screen bodies
(58 edges), the `005621A0`/`00555400`/`00562A30`/`005556A0`/`003F0170`/`00556240`/`00401620`/
`00400E80` draw-path bodies call the `002710xx` widget records and `00181330`/`00181560`/`001816B0`
shared helpers, and the icon primitives `002BCB00`/`002B8EE0` plus `caseD_0`/`caseD_1`
(`00505E00`/`00505570`) reach the same family. The crossing is the screens' place inside the render
pass — the pages draw through Presentation, not beside it.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 23 edges).** All 23 edges are Movement bodies
(`003ED190`/`003ED3F0` twice each, `PartyFollow_SolveFormation`,
`BattleLocomotion_TestForwardStepClearance`, `0033xxxx` steering helpers, `00230790`/`0026EB30`/
`0022EF20`, …) sharing the two cited accessors `00203170` and `003148F0`. Pure fan-in.

**PlatformOnlineAchievements — CLIENT (SWE2-CONTRACT 2026-09-15, 11 edges).** `003160C0` — the achievement walk over
the `[022C2550]` table — calls five of this page's helpers (`00255060`/`00264790`/`003148F0`/
`003779F0`/`003C4AD0`); `00316480` calls `0046B180`/`0046B240`; `003161A0`/`003154B0` call
`00265270`; `00315E90` calls `00309EC0`; `00316930` calls `00315DC0`. The achievement layer walks
the same registered-screen/area tables through this page's accessors — the layer consults the
page's functions, not shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Most of these edges are other callers of the shared helpers §4 lists as family members; §2.5 already states that the family is shared infrastructure rather than one screen's code.*

**ActorEntity — CLIENT and SERVICE (12 edges).** `ActorSystem_InitializeManagerRuntime` `0026CE60` calls `00253A30` and `ActorManager_RunFieldRuntimePass` `0025D9E0` calls `00254A90`, the two openers of the field-time container (§2.4); `0025D9E0` also calls `002EFD20` and `WorldTransition_GetActiveOrPendingFieldId` `003148F0`, and `BattleSlotMap_InitializeMappingClasses` `00329CC0` calls `003148F0`; `003F1E90` calls `002030E0` and the route-line helper `00203170`; `ActorResource_BeginPrimaryPayloadLoad` `00330310` and `003306E0` call the string intern/lookup `0036A100`; the track-map body `002B7B80` calls `Actor_GetWorldPosition` `00265020` and `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0`; and the arbiter `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls `0025B4C0`. Actor initialisation and the field pass are what create the field-time container and so start the map-image preload, the track map reads actor positions to place its markers, and the rest is actor code sharing the field-id getter, a vector helper and the string lookup.

**Audio — SERVICE and CLIENT (9 edges).** `001E0E30` tail-jumps into `00225570`, a 5-byte read of byte `+0x14` of the object it is given (here the input manager), and `00222740`, `00222F20`, `00223DA0` and `00224C40` call the same `00225570`; the close request `002814E0` calls `002DEE50`, which stores one audio-side state byte and tail-jumps into the audio layer; the list-input dispatcher `002D3BA0` and `002D2D40` call `00249CA0`, which resolves a sound through the audio layer and plays it unless the resolve returns -1; and `00261F90` calls `003148F0`. The map pages play their cursor sounds through the audio layer, the close path sets one audio state byte, and `00225570` is a tiny byte getter filed to Audio that the input wrapper also uses.

**CombatAI — CLIENT (3 edges).** `AiOrder_EvaluateTargetSelector` `00301AD0` calls `BattleEncodedId_DispatchQueryMode0Value` `00309EC0`, and `AiTargetSelector_ResolveOperandValue` `00321190` calls `0046B180` and `0046B240`. The gambit selector reads the same encoded-id query and the same kind-6 id-to-table-index helpers the map entries use for their gate ids; the AI does not reach the map screens.

**CombatAction — CLIENT (4 edges).** `00317BC0` and `00317C80` call `00309EC0`; `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060` and `002FA740` call `003148F0`. Action code shares the encoded-id query and the current-field-id getter with the map family; no action body opens a map.

**Input — CLIENT and SERVICE (79 edges).** `InputManager_GetSingleton` `00198790` is called by 46 input bodies, among them `InputAPI_PollControlState` `001E09B0`, `InputFeedback_DispatchViaManagerGate` `001E1120`, `0017DE10`, `001E0A10`, `001E0E30` and `001E0E50`, and the member wrappers `001E0A10`, `001E0E30` and `001E0E50` also call `001986D0`, `00197700`, `00225570` and the probe `005C3A30`; the arbiter `00253C70` calls `002B6220` (which opens the track map), `002B6260`, `FieldData_GetVariable0` `00265270`, `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` `0032A8A0` and `InputGameplay_TestCombinedMaskBit1WithTemporalGate` `00250200`, and itself calls `0017DE10`, `001E0D80`, `001E0F20`, `InputGameplay_TestFilteredMask92Bit0WithTemporalGate` `00250130`, `InputGameplay_TestAggregatedMask62Bit1WithTemporalGate` `002501A0`, `00250200` and `00862CF0`; the screen bodies `002B7B80`, `002BAF80`, `0027F5D0`, `002814E0`, `002D1870`, `002D3900`, `002D3A50`, `002D3BA0` and `00368360` call the input layer's wrappers and mask tests (`001E0A10`, `001E0E30`, `001E0E50`, `001E0F20`, `00250130`, `00250200`, `002D66A0`, `0035F0F0`, `0035F110`), and the input body `00291D90` calls the image-slot release `0024A680`. The map pages read the pad through the input layer's manager singleton and mask tests, and the input arbiter is what opens the track map; most of the 79 edges are the singleton getter's other callers.

**Resource — SERVICE and CLIENT (52 edges).** The map members load their images and tables through the resource layer's named-slot request family: `00249210` (called by the wrappers `00249180`, `00249320`, `00249350`, `00249380` and `002493D0`) calls `0032E400` and `0032E620`, `002493D0` and `0024A480` call `0024A4E0` (the only writer of a slot name) and `0024A480` calls `0024A1D0`; members such as the loader `003BC2D0`, `003C1DF0`, `003C1F00`, `003C2210`, `003C22B0`, `003C26C0`, the preloader `003CB4F0`, the creator `003CB440`, `00404060`, and the world-map bodies `00550540`, `00553F40`, `00561390`, `00562F90`, `00563080`, `00563110` and `005632C0` call `00249580` (which supplies the resource pool context), `00249210`, `002493D0`, `0024A480`, `0024A5A0` or the release `0024A680`; `00393460` and `003934F0` call `002493D0`; `00254A90` calls `001D6C20`; `001DA220` and `001DA970` call `00265270`; and `00249210`, `0024EF90` and `0024F240` call the string lookup `0036A100`. The map image cache of §2.6 and the kind-7 table loads are resource requests; the resource layer owns the slots, and the map widget owns only which index it asks for.

**SaveLoad and Save_Load_Settings — DEPENDENCY, CLIENT and SERVICE (27 edges).** `003148F0`, `0032A8A0`, `0046B180` and `0046B240` call `SaveImage_GetPersistentPayloadBase` `002EF2B0` (`003148F0` returns the dword at `+0x1044` of that payload, clamped at 0); `SaveImage_FinalizeHeaderAndChecksum` `00583D60` calls `00254380`, `MapRef_GetPersistenceGroupId` `00264F90`, `003148F0` and `0032A8A0`; the save controllers `SaveWrite_OperationStateCallback` `0057E4D0`, `SaveLoad_FullImageStorageCompletionCallback` `00580840`, `SaveSlotScan_ControllerCallback` `005819F0`, `SaveStorageQueue_ControllerStateHandler` `005823B0` and `SaveLoad_ControllerLifecycleHandler` `00582860` call the widget helpers `00244960`, `00245020` and `00247870`, `00582860` also calls `001EDEC0` and `002814E0`, and `00582790` calls `00249210`, `00249410` and `00249580`; the save screen `00280140` calls `00245020` and `002EFD20`; and the fullscreen procedure `0027F5D0` calls `SaveLoad_OpenController` `00583930` and `SaveTransition_PrepareRuntimeImageForCapture` `005844A0`. The current field id, the persistent flags and the map-entry gates live in the save image's persistent payload, so the map screens depend on that layer's data, while the save screens reuse the same widget and resource-scope helpers and the save header reads the same map state.

**Script_VM_Native_Bridge — CLIENT (12 edges).** `00356160` calls `00203170`; `00510950` and `00510990` call `00247780`; `00357450` and `0050CDE0` call `00264F90`, and `0033F310` and `00357450` call `003148F0`; `0033FD40` calls `002EFD20`; `0034E0B0` (the script query of the primary flag bank) calls `0032A8A0`; `0050D8F0` calls `0036A100`; `00351F90` calls `0046B180` and `0033F6E0` calls `0046B240`. Script verbs read the same current-field id, map-reference group, flag bank and map-data records the screens read; they consult the shared helpers and do not drive the map screens.

**World — CLIENT (2 edges).** `003C63A0` calls `0024A480` and `0024A680`. A World-filed body requests and releases a named image slot through the same resource helpers the map family uses.

**WorldAreaField — SERVICE and CLIENT (64 edges).** The world-map and location members `003BCBA0`, `003BD480`, `003BF6C0`, `003BF7C0`, `003BFEA0`, `003C0380`, `003C0450`, `003C05F0`, `003C08B0`, `003C0A00`, `003C0D70`, `003C0E30`, `003C1070`, `003C1180` and `003BD950` call `MapRef_GetPersistenceGroupId` `00264F90`, `003148F0` or `00265270`, and the arbiter `00253C70` calls `00265270`, `FieldData_GetActiveFieldRecordBit15` `00313F60` and `FieldData_GetActiveFieldRecordBit15` `00377C20`; `002B7B80` and `002BAF80` call `003148F0`. In the other direction `003148F0` is called by the field bodies `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910`, `WorldPersistence_ResetBanksForFieldTransition` `0026DB30`, `0026DE00`, `002FA520`, `00377700`, `00377750`, `00377780`, `00377BA0`, `00377C20`, `00377C70`, `003C0450` and `00576A50`; `00264F90` and `00265270` by `WorldTransition_StageFieldTransition` `003145E0`, `003778B0`, `003C0450`, `0057FB00`, `001EDCD0` and `003EAA70`; `002EFD20` by `WorldTransition_RequestFieldTransition` `00314440`; the string lookup `0036A100` by `00267930`, `003319D0` and `AreaArd_LoadOrUnloadFieldResource` `003EA820`; and the members `001EC560`, `00255060`, `0029FB50`, `002F9920`, `00309EC0`, `003779F0`, `003C05F0`, `003C12B0` and `003C4AD0` by the field bodies `001EDCD0`, `00576A50`, `0057FB00` and `003C0450`, with `00551800`, `00551930` and `00551B30` calling `003C0450`. The map screens are a view of the field layer's own state (current field, map-reference groups, field variables and the map index table), so most of these 64 edges are the field layer calling its own getters that the map family also calls, plus the world-map page bodies that call the field-filed entry scan `003C0450`.

## Interior read — frontier hub `00271450` (2026-09-17, SWE2-EC7) — evidence only

`00271450` — 37 B, 27 frontier callers at census. Read against the shipping image (page is
PARTIAL — no disposition claimed): a current-row getter over a 24-byte-stride table at
`02EBEFC0`. `idx = dword [02EBEFF0]`; writes `{ entry_ptr = table + idx*24, qword = entry[+8] }`
into `[rcx]`/`[rcx+8]`/`[rcx+16]` — the entry pointer plus one shared qword copied twice, a
three-field out-struct with the second/third fields identical.

## Interior read — frontier hub `002D3900` (2026-09-17, SWE2-EC7) — evidence only

`002D3900` — 324 B, 12 A-measured callers at census. Read against the shipping image (page is
PARTIAL — no disposition claimed): the pane tick this page's `005542D0` row routes through.
Loads three word globals `02F9736A`/`02F9736C`/`02F97368` (page/cursor dims), calls `001E0E30`,
bumps the frame counter at `0209E65C` and wraps it at `01E0CF88`; on wrap it takes the sign of `001E0A10`'s result,
gated by `word [rsi+0xE8] <= 0xC` — the `+0xE8` count this page's row keys on —
then tails `002D3BA0(rsi, dim0, dim1, dim2)` to push the recomputed geometry.

> **Correction 2026-09-18 (FABLE), from the bytes.** The three word globals this function loads are `02F9736A`, `02F9736C` and `02F97368` - the input snapshot's **raw newly-pressed, repeat and held words** ([the config screen](../Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) section 6) - and the counter it bumps and wraps is `0209E65C` against `01E0CF88`; the addresses printed above are not in the function. What it hands `002D3BA0` is therefore a frame of **input**, not geometry: that routine is the list-input dispatcher, whose confirm and cancel arms test these words against the masks `01E0C2A0` / `01E0C2A4`. A byte-identical twin, `002D3A50` (also 324 B), loads the **filtered** copies `02F97392` / `02F97394` / `02F97390` instead, which is what lets a press the game synthesises reach a list ([UQ-239](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)). The `+0xE8 <= 0xC` test and the two helper calls are as the section says.

## Interior citation — frontier hub `003BC160` (2026-09-18, SWE2-EC7)

`003BC160` — 244 B, 7 callers (incl. the `003CB650` map-screen body this page lists);
evidence-only — this host is PARTIAL. Decoded for the record: a gated scan over the
`02B457E0` record — requires `byte [+0xC8] == 1`, `[+0xD0] & 0x100`, and `0037ED80() == 1`
(`003BC194`–`003BC1B1`) — then loops `00473BB0(0, ebx, esi, &out)` over the `00473B70`
count looking for `out[0] == 1 && out[0x14] == expected`; a hit stores `out[0xC]` through
`003C0380` and sets ~~byte `02B457D9 = (ebx != 0)`~~ dword `02B457D8 = (ebx != 0)` *(Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 20): the store at `003BC247` is `mov dword ptr [rip + 0x278958b], ebp`, which lands on `02B457D8`; the global the arm-10 and arm-14 tests above read)* ([`003BC247`](../../_index/ADDRESS-INDEX.md)),
everything else returns `-1`. What the predicate scans for stays open with the page's boxes. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20, answered: the hit is the first entry whose kind `out[+0]` is 1 and whose bit `out[+0x14]` is set (`003BC208`: `cmp dword ptr [rsp + 0x34], ebp` with `ebp` = 0, then `jne` to the hit). The entries are row 0 of the chunk at `02CA6C68` (`00473B70`), the `QHD0` chunk of [the quest-menu detail tables](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/menuquest-bin-quest-detail-tables.md). The bit is the one `00473BB0` takes from the entry's first bitfield (`00473C6C`) at `003BC260`'s result divided by 5. The hit's `out[+0xC]`, the entry's word `+4`, goes to `003C0380`. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) E1-E7.)*

## SWE2-EC7-67 update - `00255060`

`00255060` (128 B) is a call-free byte-buffer popcount - sums set bits of `byte[rcx..rcx+edx)`, `0xFF` short-circuits +8, `0x00` skipped; the map-screen visited-node count. Interior anchor `00255075` (the per-byte bit test).

## SWE2-EC7-68 update (2026-09-19) - `00271080` / `00270FF0` draw-list buffer helpers

`00271080` (58 B) is the tag writer the screen draw bodies call to
head a packet: `rax = [rcx+0x18]` is the write cursor,
`dword[rax+8] = 0x11000000` and `dword[rax+0xC] = 0x10000000` stamp
the two tag fields, and `([rcx+0x10] - eax - 0x10) >> 4` derives
the element count handed to `0016D6A0`. Interior anchor `002710B0`
(the `0016D6A0` call).

`00270FF0` (30 B) is the matching consume: when `[rcx+0x10]` and
`[rcx+8]` differ it advances `[rcx][+8]` by the 16-aligned pending
span `((+0x10 - +0x8) & ~0xF)` and tail-jumps `003A1DB0`; equal
cursors return without touching the buffer. Interior anchor
`00271004` (the `[+8]` advance).

## SWE2-EC7-70 update (2026-09-19) - `002D3BA0` list-input dispatcher measured

`002D3BA0` (1,904 B) measured - the map-screen page's "list-input
dispatcher" is exact: it reads the `+0xE0`/`+0xE4` flag words, runs the
`(flags & 0xF000) - 1` six-arm jump table at `02ED4310` (`00120000` +
`0x1B4310`), each arm pairing `002D4A40`/`002D1870`/`00368860` with
escalating `edi` op codes, and carries the `+0x10B`/`+0x10C` repeat
throttle against `0208F574`, the `+0xE4` bit-13 commit, and helpers
`002D0A20`/`002D1B10`/`002D1DB0`/`002D2D40`/`002D4330`/`002445C0`/
`0035F110`.
Interior anchor `002D3E2B` (the `jmp rcx` table dispatch).

## SWE2-EC7-70 update (2026-09-19) - `002B6AE0` paired-field setter measured

`002B6AE0` (99 B) is the two-word setter the map screens share: copies
`word[+0xC8]` and `word[+0xCC]` to the stack, runs `002B69B0(&a, &b, rcx,
edx)` to adjust the pair, writes the signed results back as dwords at
`+0xC8`/`+0xCC`, and stores `edx` at `+0xD4`.
Interior anchor `002B6B17` (the `002B69B0` call).

`00402D20` (138 B) is the row-link builder `002B7460` calls: for each of `r8d` source rows at `rsi + 0x30` stride it runs `00402C30` on the `0x70`-stride destination record and threads the result onto the `+0x60` next / `+0x68` prev chain, returning the list head - the map screen's record-list construction half, paired with `00402DB0`'s mask-filtered walk.

Interior anchor `00402D60` (function `00402D20`).
