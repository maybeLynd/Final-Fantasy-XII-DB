[Home](../../README.md) / [Game files and data tables](README.md) / Standard file formats

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Standard file formats: the TGA, CSV, JSON, WebM, C-header and PS2 icon files the game ships, and which of them it reads | format | Game files and data tables | Data tables and configs | The archive files in public formats: two TGA title images, seventeen CSV tables, 830 JSON documents, forty WebM movies, six C headers, the PS2 memory-card icon pair and the PS2 boot descriptor. For each, its shipped counts and sizes, the function that opens it and what that function does with the bytes, and which files no path in the executable names. | 0x00473E80, 0x01F26568, 0x001D8D60, 0x001EE820, 0x001A9050, 0x001A7A50, 0x00674A00, 0x0024C970, 0x0024F240, 0x0024EF90, 0x001D9A40, 0x00200BF0, 0x001C3760, 0x001C7360, 0x001C7520, 0x00202930, 0x001C61F0, 0x001C53F0, 0x001C5F20, 0x001C76E0, 0x001C5930, 0x001C5750, 0x001C6E20, 0x001C2F50, 0x00582790, 0x00249210, 0x005832B0, 0x002DF9A0, 0x01E461F0, 0x002DF980, 0x001B7F30 |

## What the player sees

The health warning and the Square Enix logo at start-up are TGA images. The full-motion movies are
WebM files. Per-map render choices, which effects get soft particles, the remaster's lighting and
camera tuning for each map and cutscene, the menu font colours and the screen layout come from CSV
and JSON tables. A handful of files are leftovers of the PlayStation 2 disc: a memory-card icon pair,
the disc's boot descriptor and six C headers. The game reads the icon pair, holds a path to the boot
descriptor, and names none of the headers.

## Where it comes from

All of these files are entries in the game's archive (see [Bigfile archive](bigfile-archive.md)). The
TGA files are under `gamedata/titleimage/in/`, the movies under `gamedata/d3d11/artdata/video/`, the
JSON documents under `jsondata/`, the CSV tables under `ps2data/`, `jsondata/` and `prefetchdata/`,
and the PS2 leftovers under `ps2data/cdi/in/` and `ps2data/image/ff12/myoshiok/<lang>/`.

The executable reaches them two ways. Most are opened by a literal path: `./PS2Data/opt.csv`
(`0x008F6560`), the five `.\PS2Data\soft_particle\softparticle_*.csv` names (`0x00915400`–`0x009154D8`),
`/eventList.csv` (`0x00900738`), the `JsonData/...` names (`0x008F9E38`–`0x008F9EE0`), the title-image
directory `/GameData/titleimage/` (`0x00D22660`) and the movie pattern `%s%s.webm` (`0x008F8D70`). The
PS2 icon pair and the boot descriptor are instead entries of the per-kind path arrays that
`0x002DF9A0` installs at boot, and are read by kind and id
(see [File size tables](file-size-tables-fst.md)).

## Layouts

The TGA image and the PS2 icon pair are little-endian; the CSV tables and JSON documents are text.

### TGA title image

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | id length | 0 |
| `+0x01` | `u8` | colour-map type | 0 |
| `+0x02` | `u8` | image type | 2 (uncompressed true colour) |
| `+0x03` | `u8[9]` |  | colour map, origin 0 |
| `+0x0C` | `u16` | width | 1920   <- read |
| `+0x0E` | `u16` | height | 1080   <- read |
| `+0x10` | `u8` | bits per pixel | 24 |
| `+0x11` | `u8` | descriptor | `0x20` (top-left origin) |
| `+0x12` | `u8[width*height*3]` |  | pixels, B G R, first row at the top |

The game reads only the width and height; it assumes the rest (no id field, 24-bit, top-left).

### CSV tables

All seventeen are CRLF text without a byte-order mark. Only one holds quotes: the header line of
`jsondata/parametersmanageruisizestruct.csv` puts its fifth and sixth field names, a tab followed by `min` and a
tab followed by `max`, in double quotes.

```
opt.csv               MapName,ForceMSAAOff,FlipMapOpaqueOrder,SMAA,ForceNoOpaqueChrFirst
                      alc0101,No,No,Yes,No                         one row per map
softparticle_<type>   Name,UseSoftParticle,SoftParticleFactor      <type> = chara, common, event, magic
                      h0000.efx,No,10                              <letter><number>.efx,Yes|No,factor
softparticle_bg.csv   Map,VFXName,GroupId,UseSoftParticle,SoftParticleFactor
                      alc0101,a_sun1,31,No,10
eventlist.csv         274,0,240,0                                  four integers, no header
```

What the readers keep:

Opt.csv entry (tree node `+0x24`, keyed by the map-name hash):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | ForceMSAAOff | starts with Y or y |
| `+0x01` | `u8` | FlipMapOpaqueOrder | starts with Y or y |
| `+0x02` | `u8` |  | SMAA starts with Y or y |
| `+0x03` | `u8` | ForceNoOpaqueChrFirst | starts with Y or y |

Soft-particle entry, 4 bytes, indexed by the effect number (per-type tables) or by row number (softparticle_bg.csv):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | GroupId | (bg only) |
| `+0x00` | `u8` | UseSoftParticle != 'N' | (`+0x00` per type, `+0x01` bg); with `+0x01` |
| `+0x01` | `u8` | UseSoftParticle != 'N' | (`+0x00` per type, `+0x01` bg); with `+0x00` |
| `+0x02` | `u16` | SoftParticleFactor | (per type: 10 when "Yes" has no number) |

Bg map record, 16 bytes at `0x02F93340`, one per run of rows with the same Map:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[14]` |  | map name |
| `+0x0E` | `u16` |  | first row of the run |

EventList.csv record, 8 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` |  | second field |
| `+0x04` | `u32` | third field | the first and fourth fields are read and dropped |

### JSON documents

Each is one object of string keys. `init.json` holds the global render defaults, a
`ModelsToPreload` array of six character names and the four `TrackingMapScreen*` numbers; a map file
holds that map's render overrides; a cutscene file holds a `Common` object and `Cut 1`, `Cut 2` …
objects; a font colour file holds `mClutIndex`, `mClutComment` and eight colour numbers;
`monstergallery.json` holds `Common` and `MonsterId0` … entries; `0.json` is `{}`.

### PS2 memory-card icon pair

Icon.sys (192 bytes; the PS2 icon.sys layout cut at `0xC0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` |  | value "PS2D" |
| `+0x06` | `u16` |  | value 26: title line-break position |
| `+0x0C` | `u32` |  | value 109: background transparency |
| `+0x10` | `u32[4][4]` |  | background corner colours (39,24,6,0 / 186,164,125,0 alternating) |
| `+0x50` | `f32[3][4]` |  | light directions (0.5, 0.5, 0.5, 0) |
| `+0x80` | `f32[3][4]` |  | light colours |
| `+0xB0` | `f32[4]` | ambient | (a full PS2 icon.sys continues with the title at `+0xC0` and three icon names; this one ends here) |

Icon1.ico (33,688 bytes; PS2 icon model, not a Windows icon):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` |  | value `0x00010000`: file id (the same four bytes a Windows .ico starts with) |
| `+0x004` | `u32` |  | value 1: animation shapes |
| `+0x008` | `u32` |  | value 6: texture type |
| `+0x00C` | `f32` |  | value 1.0 |
| `+0x010` | `u32` |  | value 36: vertices |
| `+0x014` | `u8[36][24]` |  | the 36 vertices, 24 bytes each: position, normal, uv, colour |
| `+0x374` | `u8[20]` |  | animation header (one frame) |
| `+0x388` | `u8[16]` |  | frame record |
| `+0x398` | `u16[128*128]` |  | texture (32,768 bytes) |

### PS2 boot descriptor

`system.cnf` is three CRLF lines, 57 bytes: `BOOT2 = cdrom0:\SLPM_667.50;1`, `VER = 0.01`,
`VMODE = NTSC`.

## Shipped data

| Fact | Value |
|---|---|
| archive | 89,414 entries, 48 extensions; eight are public formats |
| `.tga` | 2 files, 6,220,818 bytes each: `warning.tga`, `sqex logo size_ffx.tga`, both in `gamedata/titleimage/in/` |
| TGA header | both type 2, 1920 × 1080, 24 bpp, descriptor `0x20`; 18 + 1920 × 1080 × 3 = the file size; each file has a row in [`standard-file-formats-small-files.tsv`](standard-file-formats-small-files.tsv) with its header fields |
| `.csv` | 17 files, 209,639 bytes |
| `ps2data/opt.csv` | 10,182 bytes, header + 459 rows; SMAA `Yes` in all 459, FlipMapOpaqueOrder in 7, ForceNoOpaqueChrFirst in 9, ForceMSAAOff in no row |
| `ps2data/soft_particle/` | `bg` 65,112 bytes (2,373 rows; 418 maps in 433 runs), `chara` 2,187 (126 rows, ids 0–125), `common` 2,686 (147, ids 1–151), `event` 3,747 (218, ids 0–227), `magic` 6,528 (362, ids 0–396) |
| `prefetchdata/<lang>/eventlist.csv` | 9 identical files (`us fr it es de jp kr cn ch`), 4,912 bytes, 315 records; the records, in file order and numbered from 0, are the rows of [`standard-file-formats-eventlist-rows.tsv`](standard-file-formats-eventlist-rows.tsv) |
| other CSV | `jsondata/parametersmanageruisizestruct.csv` 10,350 bytes; `prefetchdata/ff12mapjump_custom_nocrystal.csv` 64,639 bytes |
| `.json` | 830 files, 3,230,298 bytes; 775 CRLF, 29 on one line, 26 empty; no file with a byte-order mark |
| `jsondata/` root | `0.json` 2 bytes, `init.json` 5,746, `monstergallery.json` 337,640, `monstertoweapon.json` 50,445 |
| `jsondata/maps/` | 459 files, 581,069 bytes; the same 459 map names as `opt.csv` |
| `jsondata/cutscenes/` | 337 files, 2,235,149 bytes; 39 `sum_*`, of which 26 are empty; one `_2ndscreen` file (`slm_z0100_2ndscreen.json`) |
| `jsondata/fontcluts/` | 28 files `fontclut_0` … `fontclut_27`, 8,160 bytes; each file's `mClutIndex` equals its number |
| `jsondata/uisize/` | `uisize.json` 7,478 bytes, `uisize_sd.json` 4,609 |
| not strict JSON | 4: `uisize.json` and `uisize_sd.json` end with a trailing comma; `maps/bhm0201.json` misses the comma before line 44, and `cutscenes/evt_t0005.json` the two before lines 227 and 238, where `"Cut 5"` and `"Cut 6"` follow the block before them |
| `.webm` | 40 files, 10,881,781,239 bytes (21,563,773 to 1,451,123,949) |
| WebM header | all 40 open with EBML `1A 45 DF A3`, doctype `webm`; each declares one `V_VP8` video track of 1920 × 1080. 37 add two 6-channel 48 kHz `A_VORBIS` tracks, `eng` then `jpn`; `anx.webm` and `stf.webm` have one 2-channel Vorbis track with no language element and no frame duration (doctype version 2, muxer `webmmux-1.0.4.1`); `ivt.webm` has no audio track. The other 38 give a frame duration of 33,366,666 ns (29.97 frames per second) |
| every `.webm` | one row each in [`standard-file-formats-webm-rows.tsv`](standard-file-formats-webm-rows.tsv), 40 rows, 3,933.855 seconds in all (`stf.webm` the longest, 523.521): size, duration, muxer, video size and frame duration, every audio track, and the cue points with their first and last times; `-` where a file has no such element |
| `.h` | 6 files, 13,036 bytes: `us/worldmap/menumap_sub.h`, `menumap_world.h`, `menumap_world_debug.h`; `menuquest.h` in `us`, `kr`, `cn` |
| `.h` text | generated `#define` tables (converted from Excel sheets), CRLF, UTF-8; the `kr` and `cn` `menuquest.h` start with a UTF-8 byte-order mark |
| `.sys`, `.ico` | `icon.sys` (192 bytes) and `icon1.ico` (33,688 bytes) in `myoshiok/in/bin_menu/` and `myoshiok/ch/bin_menu/`; the two copies are byte-identical |
| `.cnf` | `ps2data/cdi/in/system.cnf`, 57 bytes |
| `.txt` | 10,253 files; each family's layout and reader are on the page named |
| `prefetchdata/` `.txt` | 9,341: the per-language prefetch lists (9,340) and `add-on/events/250.txt`; [Prefetch manifests](prefetch-manifests.md) |
| `cubemapconfigs.txt` | 451, one per map folder under `gamedata/d3d11/artdata/map/`; [Map cubemaps](../Graphics/map-cubemaps.md) |
| `proceduraltextureconfigs.txt`, `nomodelgroupmaps.txt` | 451 and 1; [Map art](../World-Areas-And-Travel/map-art.md) |
| `idmaps.txt`, `phyremaps.txt` | 1 each, `gamedata/d3d11/artdata/shared/`; [Phyre asset files](../PhyreEngine/phyre-asset-files.md) |
| `texlist.txt` | 1, `gamedata/d3d11/artdata/menu/`; [Prefetch manifests](prefetch-manifests.md) |
| `disableautosavelist.txt` | 1; [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md) |
| `ps2data/add_motion/` `.txt` | 4: `add_motion_list.txt` and three files no path names; [Add-motion tables](../Graphics/add-motion-tables.md) |
| `jsondata/` `.txt` | 1, `parametersmanagermonstergallerystruct.txt`, which no path names; [JSON configs](json-configs.md) |
| `.dat` | 2,948 files; each family's layout and reader are on the page named |
| `menuhandbook_<family>.dat`, `menuhandbook_<family>NNN.dat` | 2,876 in `ps2data/image/ff12/myoshiok/<lang>/handbook/`: 54 unlock tables, 101 text bundles and 2,721 picture bundles; [Handbook files](handbook-files.md) |
| `menuquest.dat` | 9, one per language's `quest/` folder; [Quest menu files](quest-menu-files.md) |
| font `.dat` | 63 in `gamedata/d3d11/artdata/font/<lang>/`; [Font files](../Menus-And-HUD/fonts-files.md) |
| the 19 files whose lines or header no other table reads | one row each in [`standard-file-formats-small-files.tsv`](standard-file-formats-small-files.tsv): `texlist.txt`, the four `ps2data/add_motion` texts, `parametersmanagermonstergallerystruct.txt`, the nine `eventlist.csv`, `parametersmanageruisizestruct.csv`, the two `.tga` and `sead.win.config`; size, SHA-256, the copies with the same bytes, first bytes, the header or record count read with the page's layout, and that page |

## Loader behaviour

### The title images

`0x00473E80(index)`, whose one caller is `0x0034E340`, returns for an index above 3 and otherwise takes
the name from the four-entry table at `0x01F26568`: `warning.tga`, `SQEX Logo size_FFX.tga`,
`rating_01.tga`, `thankyou.tga`. The test is signed (`0x00473EA3`), so a negative index is not refused and
reads its name pointer from `0x01F26568 + 8 × index`, before the table (`0x00473F6D`-`0x00473F86`).

It maps the language from `0x00229E40` to a folder (1 `us`, 2 `fr`, 3 `de`, 4 `it`, 5 `es`, 10 `in`;
any other language gets an empty folder), formats `/GameData/titleimage/<folder>/<name>` with
`"%s%s/%s"`, and probes it with `0x002DF8E0`. When the probe gives less than 1 byte it formats the path
again with folder `in`. Only `in/` ships, so every language reads the `in/` images, and indexes 2
and 3 name files that ship nowhere.

The path goes to `0x00183180` → `0x001D8D60(picture, path)`, the decoder, with the screen picture object
`[0x01F82CE0]` (`0x001D8D30`). In order:

1. It releases the picture's old texture `+0x28` (`0x00183720`) and clears the pointer
   (`0x001D8D94`-`0x001D8DA2`), and while the picture still plays (byte `+0x00` non-zero) it runs
   `0x001D8FF0`, the stop that verb `0x5A4` also reaches (`0x001D8DAA`-`0x001D8DB2`).
2. It opens a stream on the path and returns without a texture when the open fails (`0x0059D920` and
   `0x0059FAC0` both answer 0, `0x001D8DCD`-`0x001D8DE2`), reads the 18-byte header, and creates a texture of the
   header's width and height (`0x00184380`).
3. When the texture is not created it closes the stream and returns with `+0x28` null
   (`0x001D8E1C`-`0x001D8E2B`).
4. Otherwise it reads `width × height × 3` bytes straight after the header into a block from `0x00210EC0`
   (the size from the width and height read as signed 16-bit words, `0x001D8E30`-`0x001D8E5C`), closes the
   stream, maps the texture (`0x0017EBD0`), and hands them to `0x001EE820` with its flip flag fixed at 0
   (`0x001D8E9E`).
5. It commits the texture (`0x0062C360`); when that returns 0 it stores `[0x01F7F5A0] % m`, the counter modulo the
   low 31 bits of the texture's `+0x30` (1 when they are 0), at `+0x0C` and 0 at `+0x08`
   (`0x001D8EC2`-`0x001D8EF9`). Here `m = [+0x30] & 0x7FFFFFFF`, or 1 when that is 0 (`cmovne`,
   `0x001D8EC9`-`0x001D8ED3`), and the unsigned `div ecx` (`0x001D8EDE`) runs before the commit call.
   It then frees the block (`0x00210EB0`).

- **Pixels.** `0x001EE820(dest, pitch, source, sourceRow, width, height, flip)` writes each pixel as bytes 2,
  1, 0 and `0xFF`, row 0 first, moving the destination on by the mapped pitch and the source by `sourceRow`
  per row (`0x001EE880`-`0x001EE8BA`).
- **Flip.** A non-zero flip flag starts at row `height − 1` and moves back one pitch per row
  (`0x001EE838`-`0x001EE847`, `0x001EE8B3`-`0x001EE8B6`). Nothing reads the image type, depth or descriptor, so a
  compressed, 32-bit or bottom-up TGA loads wrong.

Scripts ask for an image with verb `0x5A2`, whose native `0x0034E340` passes its argument on to
`0x00473E80`. Of the four, the player only ever sees the SQUARE ENIX logo:

| Index | File | Ships | Requested by | When the game shows it |
|---|---|---|---|---|
| 0 | `warning.tga` | yes, in `in/` | `スクリーン表示.Warning_page` of `ttl_a01` | never: the title loop of `ttl_a01` does not request it in any language set; only the `cn` and `kr` copies named `ttl_a01_e3` do, and the game loads no zone script by that name |
| 1 | `SQEX Logo size_FFX.tga` | yes, in `in/` | `スクリーン表示.Logo_page` of `ttl_a01` | before the title screen while `isFirstStartDone()` is 0: the SQUARE ENIX logo, white on black |
| 2 | `rating_01.tga` | no | `スクリーン表示.ESRBrating_page` of `ttl_a01` | never: the request needs verb `0x5B4` to be true |
| 3 | `thankyou.tga` | no | `RETURNTOTITLE.ShowMessage` of scenes `fon_b0100` and `lus_g0100`, and `RETURNTOTITLE.ShowThankyoupage` of the `ch`, `cn` and `kr` `gol_c01` and `nal_d01` | never: every request sits under verb `0x5B4` |

Verbs `0x5B1` and `0x5B4` both run `0x00355930`, which stores 0 as the verb's result through `0x0026B4E0`, so
both are always false. The script branches they guard are a build's rating page, its "thank you" return
to the title and the title's event 0; the autosave notice, shown while `0x5B4` is false, does appear.
`warning.tga` is a Japanese notice (ご注意) that distributing the game over the internet without the
rights holder's permission, or knowingly downloading such a copy, is illegal.

### Per-map render options: opt.csv

`0x001A9050`, called from the map-art set-up `0x001A2130`, first empties the tree at `+0x3E0` of the map-art
object (`0x001A5810`, `0x001A9079`). It opens `./PS2Data/opt.csv` through the stream helper `0x001D6F20` and
returns when that gives no stream (`0x001A9095`). It reads the file whole into a block of its size plus 2 with
a 0 after the last byte (`0x001A90B6`-`0x001A90E9`), frees the block and stops when its first byte is 0
(`0x001A90F7`), and otherwise walks it a line at a time, freeing the block at the end (`0x00210EB0`,
`0x001A927F`):

- a line ends at the next CR, and the next line starts two bytes later; a file without CR yields no
  rows;
- the walk stops at the first line with no CR before the end of the file and drops that line (`0x001A914F`,
  `0x001A9165`), and it stops when the byte two past a CR is 0 (`0x001A9266`);
- the first line is skipped as the header, and only lines with exactly five fields are kept;
- the map name is hashed with `0x00674A00` (start 5381, multiply by 33, add each byte as a signed value,
  `0x00674A17`, keep 31 bits);
- each of the other four fields becomes 1 when it starts with `Y` or `y`, and the four bytes go into a
  tree node keyed by the hash (tree at `+0x3E0` of the map-art object).

When a map is entered, `0x001A7A50` hashes the map name (the text after the backslash of
`<area>\<map>`) and looks it up. A hit copies byte 1 (FlipMapOpaqueOrder) to `+0x418` and byte 3
(ForceNoOpaqueChrFirst) to `+0x419` of the map-art object; a miss sets both to 0. `0x001A7A50` does not
use bytes 0 and 2.

[`standard-file-formats-opt-rows.tsv`](standard-file-formats-opt-rows.tsv) lists the 459 rows in file order:
the line as shipped, the map name and its hash, the four flags as `0x001A9050` keeps them, the zones whose
map-art lookup uses the row, with their field ids, map names and regions, and what the row changes. What the
rows do:

- FlipMapOpaqueOrder reverses the order the map's solid scenery is drawn in. It is Yes on seven maps: North
  End and Muthru Bazaar in Rabanastre, Sea Breeze Lane in Balfonheim Port, Platform 1 - Refinery in the
  Ogir-Yensa Sandsea, Augur Hill in the Nam-Yensa Sandsea, the Fane of the Path in Eruyt Village, and the
  Quietened Trace and Grand Bower of the Salikawood.
- The map walk of `RenderMapOpaqueObj` (`0x001F3570`) passes `+0x418` to `0x0018B1B0` as its reverse flag
  (`0x001F35FF`-`0x001F361B`): 0 runs the map entries of the render command list from the first filed to the
  last, 1 from the last to the first.
- ForceNoOpaqueChrFirst takes the characters' solid parts out of the map's opaque pass and leaves them to
  the general opaque pass. It is Yes on nine maps: the six Royal Palace maps from the Cellar Stores to the
  Garden Stairs (`rrp_a01` to `rrp_a06`), the Hall of the Light at Mt Bur-Omisace, the bridge of the
  Dreadnought Leviathan (`rsn_z01`) and the Rabanastre map `rbn_x01`.
- On a frame whose map pass posted `RenderMapOpaqueObj` (`0x001809A0`), its draw `0x001F3570` normally walks the
  characters' opaque objects just before the map's (`0x001F3586`-`0x001F35D0`), and the draw of
  `RenderOpaqueObj`, `0x001F36B0`, leaves them out (`0x001F36B9`-`0x001F36D7`). With `+0x419` set, `0x001F3594`
  skips that walk and `0x001F36C7` lets `0x001F36B0` draw them where `RenderOpaqueObj` sits in the list (filed
  by `0x0017F070` at `0x0022B38F`).
- ForceMSAAOff (Yes on no map) and SMAA (Yes on all 459) change nothing: the entry has one lookup,
  `0x001A7A50`, which keeps bytes 1 and 3 only (`0x001A7BA2`, `0x001A7BAD`), and the tree at `+0x3E0` of the
  map-art context is addressed only by its builder `0x001A2130`, the reader `0x001A9050` and that lookup.
- A map with no row gets both bytes 0 (`0x001A7BD6`): scenery first to last and characters before it. One zone
  is in that case, `ttl_d01` (pack `tst0102`). No two shipped names share a hash, so no map takes another's
  row.
- A flag is Yes only when it starts with `Y` or `y` (`0x001A91B6`-`0x001A91F6`), so `1`, `true` or an empty
  field is No. A line without exactly five fields is skipped, and a later row whose name hashes the same
  replaces the earlier entry (`0x001A9253`).
- Seven rows are never looked up. `fon0113` and `mrm0213` are no zone's map pack, and `dst0109`, `dst0110`,
  `frs0109`, `frs0110` and `gil0303` belong to the zones that `0x00379A10` sends to the art of `dst0103`,
  `dst0105`, `frs0101`, `frs0106` and `gil0301`, whose rows they use instead.

### Soft-particle tables

`0x0024C970` (from `0x00259180`) clears four 0x800-byte tables and reads `chara`, `event`, `magic` and
`common` into them (`0x02F96B40`, `0x02F96340`, `0x02F95B40`, `0x02F95340`) with `0x0024F240`, then reads
`softparticle_bg.csv` with `0x0024EF90`.

The same body first clears the `0x1670` bytes from `0x020910A0` (`0x0024C983`), sets the five 16-bit effect masks
`0x0209215E` to `0x02092166` to `0x3FF` and `0x020926F4` to `0x4003C` (`0x0024C98A`-`0x0024CB18`), and selects arena 8 with
`0x0036C1D0(8, 10)` (`0x0024CB25`) before the tables. After `0x0024EF90` it pops the arena (`0x0036C140`, `0x0024CBCB`) and
sets `0x02092700` to -1 (`0x0024CBD0`) ([startup constants](../Engine-Core/startup-constants.md)).

- `0x0024F240(path, table)` opens the file through `0x001D6F20` and returns when that gives no stream
  (`0x0024F26C`). It reads the file whole into a block of its size plus 2 from `0x0036A100`, ending it with a
  0, and returns after freeing the block (`0x003697F0`, `0x0024F397`) when the first byte is 0 (`0x0024F2B8`) or
  once the walk is done.
- `0x0024F240` scans each CR-terminated line with `"%c%d.efx,%s"`. With three matches, the entry for
  the effect number gets byte 0 = (the rest does not start with `N`); when it is set, `"Yes,%d"` gives
  the factor at `+2`, or 10 without a number. The header line fails the scan. The effect number is not
  bounded against the table's 512 entries, and it is read as signed, so a negative one writes before the
  table (`0x0024F32A`, `0x0024F332`).
- The scan is `sscanf` (`0x0018A330`, `0x0024F31B`): the letter `%c` is compared with nothing, and the rest
  goes into a 32-byte stack buffer with no width limit (`0x0024F2FD`). With byte 0 clear the factor word is
  left as it was (`0x0024F33E`), and the factor is stored as 16 bits (`0x0024F365`).
- The walk stops at the first line with no CR before the end of the file and drops that line (`0x0024F2E6`,
  `0x0024F2F4`), and it stops when the byte two past a CR is 0 (`0x0024F381`).
- `0x0024EF90` keeps lines with exactly five fields, copies the map name, reads GroupId with `"%d,"`,
  and, when that succeeds, writes the next 4-byte entry of `0x02F8F340`: GroupId, UseSoftParticle not
  `N`, factor with `"%d"`.
- Each time the map name differs from the previous kept row's, `0x0024EF90` appends a 16-byte record (name, first
  row) to `0x02F93340`. The kept-row count goes to `0x02092714` and the record count, one per run of rows with the
  same map name, to `0x02092718` (433 records for the 418 shipped maps). VFXName is not stored.

[`standard-file-formats-softparticle-rows.tsv`](standard-file-formats-softparticle-rows.tsv) lists the 853
effect rows of the four per-type tables and
[`standard-file-formats-softparticle-bg-rows.tsv`](standard-file-formats-softparticle-bg-rows.tsv) the 2,373
rows of `softparticle_bg.csv`, each in file order with the values the readers keep, the effect file or the
map and zones it joins to, whether the game reads it and what it changes. What the rows do:

- With the Soft Particles option on, a soft effect fades out where it comes close to the scenery or a
  character behind it, instead of cutting a hard edge into them. The fade spans `factor / 100` in
  depth: 0.1 for the shipped 10, up to 5 for the five map rows with 500.
- Effects drawn as a `GiSprite` (`0x008647C0`) or a VU program packet (`0x001DB840`) take the answer of
  `0x0024D140` and pass it to the primitive renderer's slot `+0x58` (`0x006CAD90`, called at `0x008646D3` and
  `0x001DB416`), which keeps the switch at `+0x208E8` and the factor at `+0x208EC`; `0x006C8920` copies both
  into the draw record at `+0x854` and `+0x858`.
- The draw `0x006C8CA0` turns the fade on only when the record's Soft Particles option byte `+0x855` is set as
  well (`0x006C982E`-`0x006C98B6`; slot `+0x60`, `0x006CADB0`, stores the option), and uploads
  `softParticleEnabled` and `softParticleFactor` to the pixel-shader constants (`$Globals` `+0x28` and
  `+0x38`).
- The three pixel shaders that read them (`0x01F33068`, `0x01F346B8`, `0x01F39544`) take both depths as
  `100 / (1000 - 999.9 * d)`, the scene's from the depth texture, and multiply the effect's alpha by their
  difference over the factor, capped at 1, `diff / factor > 1 ? 1 : diff / factor`. A pixel more than 0.5
  behind the scene keeps its alpha.
- Magic effects are soft but for 29 of the 362, 21 of them Quickening and Concurrence cinematics (ids 120 to
  153); 146 of the 147 listed common-bank effects are soft, all but `c0141`; no event effect is, all 218
  rows being No. Four character effects are soft: those of the Bomb and the Pineapple (`h0003`), the King
  Bomb (`h0033`), the Purobolos (`h0034`) and the Air Cutter Remora (`h0090`, factor 30).
- On the maps, 288 of the 2,373 rows say Yes, and 125 of them, on 94 maps, reach an effect the map draws,
  with factors from 10 to 500. The key is the effect's channel: `0x0024D140` compares the map-bank instance's
  word `+4` with each GroupId of the map's run (`0x0024D221`-`0x0024D246`), and every shipped GroupId is a
  channel from 0 to 63.
- An effect number a table does not list is hard with factor 0.1, because `0x0024C970` clears the tables
  first; so is any number of 512 or more (`0x0024D1CE`, `0x0024D26B`, `0x0024D297`, `0x0024D2C0`). Location and
  quest effects have event ids from 512 up (`0x003B2310`, copied into the context at `0x003B2242`), so they are
  never soft.
- In the per-type files a value is Yes unless it starts with a capital `N` (`0x0024F325`), so `no` or `0` is
  Yes. A Yes whose text does not scan as `Yes,%d`, such as `Yes`, `yes,20` or `Yes,abc`, gets factor 10
  (`0x0024F371`); a line that does not scan as `%c%d.efx,%s` is skipped (`0x0024F323`). Any letter may stand
  before the number.
- In `softparticle_bg.csv` a GroupId that does not scan drops the row (`0x0024F110`); a factor that does not
  scan repeats the previous row's, since `0x0024F149` ignores the scan's result; a GroupId above 255 keeps
  only its low byte (`0x0024F129`), so 261 acts as 5. A map with no rows stores -1 as its first row
  (`0x0024F83F`), and all its effects are hard (`0x0024D1F8`).
- 820 map rows are never read. 210 are on 39 maps no zone loads, the 14 `dgl01` maps and test maps such as
  `rbn_test` among them; 162 are in a second run of 14 maps of Giruvegan, the Great Crystal and the Golmore
  Jungle, as `0x0024F790` takes only a map's first run (`0x0024F810`-`0x0024F835`); 442 repeat a channel an
  earlier row of the run names, and the first match wins (`0x0024D23C`).
- The other 6 name a channel no row of the map's effect bank uses (`rbn0101`, `rbn0301`, `var0103`). Of the
  per-type rows, 15 name effects the game never loads: `h0000`, which the character-effect table does not
  name, and the event effects 0, 11 to 13, 47, 48, 95 to 98, 172 and 190 to 192, which no script loads with
  `effectread` or `effectread_e0`.

### Event prefetch schedule: eventList.csv

`0x001D9A40`, run by the prefetch worker `0x001DADC0`, opens
`/PrefetchData/<language>/eventList.csv`, scans `"%s"` tokens and steps past each by its length plus
two, drops tokens starting `##`, and parses each token with `"%d,%d,%d,%d"`. A record with four
values keeps the second (as `u16`) and third fields; the first and fourth are dropped. What the
schedule triggers is on [Prefetch manifests](prefetch-manifests.md).

### The JSON reader

`0x00200BF0(document, path)` opens a stream on the path (`0x00597970`), and when the stream has a
positive length reads it whole, terminates it with a zero byte and parses it into the document
(`0x00200E60`). An empty or missing file parses nothing. Keys are then fetched with `0x001FF740` and
read as numbers or strings (see [Graphics settings](../Engine-Core/graphics-settings.md)
for the readers and the lookup order). Every reader below goes through `0x00200BF0`.

### init.json and monstergallery.json

`0x001C3760` (from `0x00186CD0`) parses `JsonData/init.json` into the global document `0x01F813C8`. Each
`ModelsToPreload` string goes to `0x001BB920`, which builds
`./GameData/D3D11/ArtData/chr/<name>_D3D11.ah` and loads that asset list (all six shipped names have
one). `TrackingMapScreenRateX`/`Y` and `TrackingMapScreenSuperWideMul`/`Plus`, when present, go to
`0x002B6670`, `0x002B6680`, `0x002B6690` and `0x002B66A0`. The same function then parses
`JsonData/MonsterGallery.json` into `0x01F81308`; the monster viewer reads it from there
([Clan Primer](../Menus-And-HUD/clan-primer.md)).

`0x001C7360` and `0x001C7520`, both called from the developer menu `0x001D1660`, are the only writers: when
the key holds a non-null value, they store new tracking values in `0x01F813C8` and write the whole document
back to `JsonData/init.json` through an output file stream (`0x00202930`).

- `0x001C7360(x, y)` looks up `TrackingMapScreenRateX` and tests its tag (`0x001FF740`, `0x00200BE0`) twice, the
  first result unused, and returns when its value is null (`0x001C73BC`). It then stores `x` and `y` as doubles
  in `TrackingMapScreenRateX` and `TrackingMapScreenRateY` (`0x001FEE10`, `0x001C73E1`, `0x001C7406`); only the
  first key is tested.
- The lookup adds an absent key to `0x01F813C8` with a null value (`0x001FF4F0`, `0x001FF5E1`), so that early return
  leaves the key in the document as null without writing the file.
- `0x001C7520(mul, plus)` does the same with `TrackingMapScreenSuperWideMul`, which it tests (`0x001C757C`), and
  `TrackingMapScreenSuperWidePlus` (`0x001C75A1`, `0x001C75C6`).
- Both build the path string `JsonData/init.json` (18 bytes through `memmove`, `0x001C74AA`, `0x001C766A`) and
  call `0x00202930(0x01F813C8, path, 1, 0)` (`0x001C74CE`, `0x001C768E`).
- `0x00202930(document, path, a, b)` opens the file for output (`0x0019B990`, mode 2) and, when that fails, sets
  the stream's fail bit and writes nothing (`0x00202A35`-`0x00202A64`). Otherwise it writes the document with
  `0x00201460(document, stream, a, b)` (`0x00202A76`) and closes the file (`0x0019B8C0`, `0x00202A80`), setting
  the fail bit when the close fails (`0x00202A85`-`0x00202AA2`).

### Map, cutscene, font-colour and layout documents

- Maps: `0x001C61F0` (from `0x00214C30`) runs while `0x01DF6E48` (1 as shipped, written only by the
  developer menu) or `0x01F81282` is set. `0x001C53F0` takes the map-art object's `<area>\<map>` string
  (the text at `+0x241` of the object `0x001A9930` returns), keeps the text after the first backslash, or
  the whole string when it has no backslash (`0x001C54B1`), and appends `.json` (`0x001B31E0`, `0x001C551C`).
- When that name differs from the last one (`0x01F81388`), it becomes the last name and
  `JsonData/Maps/<map>.json` is parsed into `0x01F81328` (`0x001C627B`-`0x001C62A1`); the area scene-config
  loader `0x001C7940` then applies it. `0x001C7940` also runs on the document as it is when the name is the
  same (`0x001C626A`, `0x001C62DA`). A name that is `.json` alone, from an empty map name, loads and applies
  nothing (`0x001C622B`-`0x001C6244`).
- Cutscenes: `0x001C5930`, entered by a tail jump from `0x001EC600`, parses
  `JsonData/CutScenes/<name>.json` into `0x01F813A8 + slot × 0x10` and `<name>_2ndScreen.json` into
  `0x01F813D8 + slot × 0x10`, the slot being `0x01DF6E4C`. `0x001C5750`, reached from
  `0x0020AC30` for names containing `sum_`, parses `JsonData/CutScenes/<name>.json` into a local
  document and passes `Common.mDofFocusDistance` and `Common.mDofApertureFnumber` to `0x00194250`.
- `0x001C6E20` (from `0x001F3500`) parses `JsonData/0.json`, takes its `ChangedFileName` string as a
  cutscene name for the cutscene document slots. The shipped `0.json` is `{}`. It searches the string it took
  for `2ndScreen` with `0x001C34D0(begin, end, pattern, patternEnd)`, the byte-range search that returns where the
  pattern starts, or `end`; `0x0020AC30` searches a name for `sum_`, `0001` and `spc_` with it.
- Font colours: `0x001E94E0(manager, n)` for `n` below 28, the first time entry `n` is used, formats
  `fontclut_%d` and calls `0x001C5F20`, which parses `JsonData/FontCluts/fontclut_<n>.json` into
  `0x01F81378` (gated like the map files).
- `0x001C76E0` then reads `mClutIndex`, selects that entry (`0x24` bytes at manager `+0xF68`), stores
  `mShadowRed/Green/Blue/Alpha` and `mFontRed/Green/Blue/Alpha` as integers at `+0x04` to `+0x20`,
  and clears the document. Nothing fetches `mClutComment`.
- When the document has no `mClutIndex` (the lookup gives the tag-6 entry, `0x00200BE0`), `0x001C76E0` returns at once
  without clearing it (`0x001C76FA`-`0x001C7701`). The lookup `0x001FF740` has already added `mClutIndex` to it with a tag-6
  value (`0x001FF4F0`: `0x001FF5E1`, `0x001FF647`), after making a document that is not an object (tag 3) an empty object
  (`0x001FF6B0`: `0x001FF6CF`-`0x001FF713`).
- The entry comes from `0x001E94E0(0x001B5FA0(), index)` (`0x001C7733`), which takes entry 0 for an index above 27 or below
  0, the compare being unsigned (`0x001E94F6`-`0x001E94FA`, `0x001E9560`); the clear is the tail jump to `0x00202880`
  (`0x001C783B`).
- Layouts: `0x001C6C00` (from `0x001B1580`) loads `UISize.json` or `UISize_sd.json`
  ([Screen layouts](../Menus-And-HUD/screen-layouts.md)).
- `0x001C2F50` (from `0x0017D6E0`) parses `/Tools/AutoTest/MapIndex.json` for a `MapIndex` value; no such
  file ships.

The walker is the auto-test that visits every map in turn. Each frame the pump calls it. It does nothing unless the
application object's auto-test byte `+0x10D4` is set (`0x001C2F7C`), which retail never sets, and its own enable word
`0x01F8127C` is non-zero (`0x001C2F89`). Its steps:

1. While `0x01DF6E40` is set it reads the starting index `MapIndex` from `/Tools/AutoTest/MapIndex.json` (path
   pointer `0x01DF6E38` to `0x008F9E00`), stores it in `0x01F81278` (`0x00200B80`, `0x001C30B2`), and clears the byte.
2. While the arrival word `0x01EEBADC` is set it moves the index on by one. For an index up to `0x522`, if the map
   table's entry `0x01DF6E60 + index × 0x10` has a name pointer at `+0x08`, it clears the arrival word and makes the
   call `0x0016D6A0(0x4B, entry +0x00, 0)` (`0x001C30E3`-`0x001C3110`). That stub only returns, so the jump is compiled out.
   Past `0x522` it sets the document's `MapIndex` to 0 (`0x001FEDA0`, `0x001C3218`).
3. While the arrival word is 0 it waits. Once the application time (`0x0017D8D0`, the application object's `+0x40`)
   less `0x022BDD50` is above 120.0 (`0x008F9E30`), it puts the current index in the document's `MapIndex` (`0x001C332E`)
   and stores 1 through a null pointer (`0x001C3339`, `rbx` 0), which stops the game.
4. A fade that starts on a layer whose last fade had finished arms both words. `0x002EFA70` sets each to 1 when it is
   0, and `0x022BDD50` to 0 ([Screen fades](../Graphics/screen-fades.md)).
5. The `eventsync` verbs' polls `0x00355F60` (`0x00ED`) and `0x00355970` (`0x00EE`) set the arrival word to 1 when the
   auto-test byte is non-zero (`0x001C3370`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01DF6E40` | `u8` | 1 | 1 until the walker has read its starting index | `0x001C2F50`, 0 (`0x001C30B8`) | `0x001C2F50` (`0x001C2FAA`) |
| `0x01F81278` | `i32` | 0 (zero-filled tail of `.data`) | the map table index the walker is on | `0x001C2F50` (`0x001C30B2`, from the file; `0x001C30DD`, plus 1) | `0x001C2F50` (`0x001C30D5`, `0x001C3115`, `0x001C332E`) |
| `0x01F8127C` | `u32` | 0 (zero-filled tail of `.data`) | the walker's enable word, non-zero after the first fade that starts on a finished layer | `0x002EFA70` (`0x002EFB7E`, 1 when it was 0) | `0x001C2F50` (`0x001C2F89`, its low byte); `0x002EFA70` (`0x002EFB67`) |
| `0x01EEBADC` | `u32` | 1 | the arrival word: set when a map has been reached, cleared when the walker moves on | `0x001C2F50`, its low byte 0 (`0x001C30FF`, a 1-byte store; the other bytes are 0 from the start); `0x002EFA70` (`0x002EFB90`, 1 when it was 0); `0x00355970` (`0x00355983`) and `0x00355F60` (`0x00355F73`), 1 | `0x001C2F50` (`0x001C30C8`, its low byte); `0x002EFA70` (`0x002EFB84`) |
| `0x022BDD50` | `f64` | 0 (zero-filled tail of `.data`) | the time base of the walker's 120-second wait; the only store writes 0.0 | `0x002EFA70` (`0x002EFB72`) | `0x001C2F50` (`0x001C3227`) |

### The document-name strings

The map and cutscene loaders keep their document names in static EASTL strings (`+0x00` begin, `+0x08` end,
`+0x10` capacity end), which start-up initialisers build empty and `atexit` destructors free:

- `0x01F81288`, the map document name (initialiser `0x0015C9E0`, destructor `0x008A6B90`): `0x001C53F0` empties it
  (`0x001C5429`) and rebuilds it through `0x001A5760` (`0x001C544E`): first the whole `<area>\<map>` string
  (`0x001C5458`), then the part it keeps, cut out with `0x001A9E50` (`0x001C54C6`, `0x001C54DB`).
- `0x01F81388`, the last map name (initialiser `0x0015C8D0`, destructor `0x008A6B30`): `0x001C61F0` compares the new name
  with it (`0x001C624A`, `memcmp` at `0x001C6263`) and, when they differ, assigns it through `0x001A5760` (`0x001C6274`).
- `0x01F812A8`, the cutscene document name (initialiser `0x0015C7C0`, destructor `0x008A6AD0`): `0x001C5930` reads its
  length (`0x001C5978`) and assigns it through `0x001A5760` (`0x001C59EB`); `0x001C5040` empties it (`0x001C504B`-`0x001C505E`).

`0x001A5760` (assign) and `0x001A52A0` (grow), which it calls, reach the fields through the string's address.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F81298` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the map document name `0x01F81288` | `0x0015C9E0` (`0x0015C9FE`, `0x0015CA69`, `0x0015CA8E`); `0x001A52A0` (`0x001A537F`) | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A6B90` (`0x008A6B9D`) |
| `0x01F812B0` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` end of the cutscene document name `0x01F812A8` | `0x0015C7C0` (`0x0015C7F3`, `0x0015C839`, `0x0015C867`, `0x0015C884`); `0x001A52A0` (`0x001A538E`, `0x001A53D3`); `0x001A5760` (`0x001A57BC`); `0x001C5040` (`0x001C505E`) | `0x001A52A0` (`0x001A52C0`, `0x001A5318`, `0x001A53A0`, `0x001A53B7`, `0x001A53C5`, `0x001A53D3`); `0x001A5760` (`0x001A5774`, `0x001A5798`, `0x001A57BC`, `0x001A57C2`, `0x001A57CF`); `0x001C5040` (`0x001C504B`); `0x001C5930` (`0x001C5978`, the low 4 bytes) |
| `0x01F812B8` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the cutscene document name `0x01F812A8` | `0x0015C7C0` (`0x0015C7DE`, `0x0015C849`, `0x0015C86E`); `0x001A52A0` (`0x001A537F`) | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A6AD0` (`0x008A6ADD`) |
| `0x01F81390` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` end of the last map name `0x01F81388` | `0x0015C8D0` (`0x0015C903`, `0x0015C949`, `0x0015C977`, `0x0015C994`); `0x001A52A0` (`0x001A538E`, `0x001A53D3`); `0x001A5760` (`0x001A57BC`) | `0x001A52A0` (`0x001A52C0`, `0x001A5318`, `0x001A53A0`, `0x001A53B7`, `0x001A53C5`, `0x001A53D3`); `0x001A5760` (`0x001A5774`, `0x001A5798`, `0x001A57BC`, `0x001A57C2`, `0x001A57CF`); `0x001C61F0` (`0x001C624A`, the low 4 bytes) |
| `0x01F81398` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the last map name `0x01F81388` | `0x0015C8D0` (`0x0015C8EE`, `0x0015C959`, `0x0015C97E`); `0x001A52A0` (`0x001A537F`) | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A6B30` (`0x008A6B3D`) |

No other instruction reaches these words: no other RIP-relative, image-base-relative or disp32 reference names them.
The strings' addresses are taken only at the sites above.

### The PS2 memory-card icon pair

`0x00582790` asks `0x00249210` for kind 7 id `0x2C` (`icon.sys`) and kind 7 id `0x2D` (`icon1.ico`),
storing the data pointers at `+0x110` and `+0x118` of the save object (`0x00582814`, `0x0058282F`).

It asks only while byte `+0xC1` of the save object is 0 (`0x005827DD`), takes the two from arenas 3 and 2,
bottom-up (`0x005827F6`, `0x0058281B`), and then stores `0x00393600(2)` at `+0x120` (`0x0058283D`); both requests go into
the screen's request group, with no completion of their own.

`0x00249210` sizes the file from the [file size table](file-size-tables-fst.md) (`0x0032E400`),
allocates a buffer and queues the read (`0x0032E620`); for a size below 1 it does neither and the data pointer
stays null (`0x0024929F`).

Every kind-7 array that `0x002DF9A0` installs holds the pair at ids 44 and 45. The KR, CH and CN arrays
(languages 7, 8 and 11; `0x01E0E530`, `0x01E5A3D0`, `0x01EABBA0`) name the `ch` copies, the others the `in`
copies. Ids 46 and 47 name `icon2.ico` and `icon3.ico`, which ship nowhere and are sized -1 in every
table.

`0x005832B0`, called from state 7 of the save transaction `0x00581DA0`, uses `icon.sys` as a template.
It clears a `0x3C4`-byte image, stamps `PS2D` (`0x00583307`), writes a title of play time and save
number at `+0xC0` and its line-break position at `+0x06`, copies bytes `+0x0C` to `+0xBF` from the
loaded `icon.sys`, and writes the name `0x005837F0` returns for kinds 2, 3 and 4 (`static.ico`) at
`+0x104`, `+0x144` and `+0x184`.

State 7 builds this image at `+0xE8` of the transaction record; the storage request it then files
(`0x00582540`) names only the numbered slot file. How the slot files are written and deleted is on
[Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md).

[`standard-file-formats-icon-rows.tsv`](standard-file-formats-icon-rows.tsv) lists the four files, with
size, SHA-256, kind-7 id and the locale ids that load each copy, then every field of `icon.sys` and
`icon1.ico`: the 16 fields of `icon.sys`, the five header fields, 36 vertices, animation header, frame
record and texture of `icon1.ico`, each with the code that reads it.

- Of `icon.sys` the image takes bytes `+0x0C` to `+0xBF`: `0x005832B0` copies one dword and eleven 16-byte
  blocks (`0x005835AF`-`0x0058363C`), ending at the file's last byte. Bytes `+0x00` to `+0x0B` are not copied:
  the image is cleared, and the game writes its own `PS2D` (`0x00583307`) and line break.
- In the PS2 layout these bytes are the memory-card browser's background (transparency 109 of 128 and four
  corner colours, (39, 24, 6) on the left and (186, 164, 125) on the right), three light directions and
  colours and the ambient light of the 3D icon.
- `icon1.ico` is a one-shape, one-frame model of 36 vertices with a 128 x 128 texture of 16-bit texels,
  which ends the file. Of the functions that hold the save object, `0x00582790`, `0x00582860`, `0x00582FC0`,
  `0x005832B0` and every other reader of its global `0x02CA99B8`, only `0x00582FC0` reads `+0x118`, to free the
  buffer (`0x00583010`).
- A replacement `icon.sys` needs at least `0xC0` bytes and a matching size-table entry for id `0x2C`, as the
  copy reads `0xC0` bytes of the buffer and the read is sized by the table. No field holds a value out of
  range.

### The boot descriptor

`ps2data/cdi/in/system.cnf` is kind 0, id 0: entry 0 of the array `0x01E461F0`, which `0x002DF9A0`
stores at `0x0215F000`. Every `.fst` sizes it at 57 bytes. It is the first of twelve kind-0 paths (ids 0 to 6, 10,
11 and 14 to 16; the slots for ids 7 to 9, 12, 13 and 17 are null). The other eleven, the PS2 executable
`SLPM_667.50`, the path `PS2Data\pad2` and the modules `ioprp300.img`, `mcman.irx`, `mcserv.irx`, `dbcman.irx`,
`libsd.irx`, `sio2d.irx`, `sio2man.irx`, `iopsound.irx` and `pad2\ds2o.irx`, ship nowhere in the archive.

Its three lines are the PS2 console's boot settings: `BOOT2` names the program the console starts,
`cdrom0:\SLPM_667.50;1` (the disc file `SLPM_667.50`, file version 1), `VER` is the disc version 0.01 and `VMODE`
the video mode, NTSC. No `.exe` or `.dll` in `x64` holds the text `BOOT2`, `VER =`, `VMODE =` or `cdrom0`, or any
of the three lines, ASCII or UTF-16, in any case; `SLPM_667.50` occurs once, in the path
`program\dvd\in\SLPM_667.50` at `0x00A029C0`.
[`standard-file-formats-system-cnf-rows.tsv`](standard-file-formats-system-cnf-rows.tsv) lists the lines with the
file's SHA-256.

### Movies

`0x001B7F30` gets a path with `0x002DF980(0x1C, movie × 2)`: `0x002DF980` returns
`[[0x0215F000 + kind × 8] + index × 8]`, and kind 28 is the movie kind. That entry is a PS2
`movie_finish\<lang>\<NAME>.md` path. The player keeps the text between the last backslash and the
last dot, formats `"%s%s.webm"` with the prefix `/GameData/D3D11/ArtData/video/` (`0x01DF6E28`), and
opens it with `0x0067A480` on the player object at its `+0x678`. A null path entry stops the movie.

- Before the path it starts the reading thread (`0x0067A350`). The arm that sets the state `+0x04` to 0 and
  returns when that call answers 0 (`0x001B7F6A`, `0x001B80B5`) is never taken: `0x0067A350` has one exit, returns 1
  (`0x0067A3FF`) and drops the result of the thread start `0x005CD1E0` (`0x0067A3F5`).
- The name is found with `strrchr` for `\` and `.` (`0x001B7FB4`, `0x001B7FC5`) and copied with `strncpy` into
  a zeroed 32-byte buffer, the count being the last dot less the character after the backslash
  (`0x001B7FD0`-`0x001B7FF7`). With no dot after the last backslash that count wraps around and `strncpy`
  writes past the buffer.
- A path with no backslash resets the player with `0x001B7690` (`0x001B7FCE`, `0x001B803A`), and a failed open
  sets the state to 0 and resets it the same way (`0x001B8030`-`0x001B803A`).

The first 98 ids of kind 28 hold 45 `.md` paths at even ids, each followed by its `.mh` path, and
four empty pairs. 40 of the 45 base names have a `.webm`; `dlb`, `opd`, `se1`, `se2` and `bd2` have
no `.webm`. Which script step opens each movie id, and so what each `.webm` is shown for, is in
[`movies-by-id.tsv`](../Graphics/movies-by-id.tsv) ([movies](../Graphics/movies.md)).

### Files no path names

No string in the executable, ASCII or UTF-16, in any case, names `monstertoweapon.json`,
`parametersmanageruisizestruct.csv`, `ff12mapjump_custom_nocrystal.csv` or any of the six `.h` files.

The six `.h` files are C headers that the developers' converters (`CnvWorldMap`, `CnvSubLocation`, `CnvQuestData`)
wrote from the spreadsheets `ff12worldmapdata.xls` and `ff12menuquest.xls`.
[`standard-file-formats-header-rows.tsv`](standard-file-formats-header-rows.tsv) lists 136 of their 146 `#define`
lines, all but the six include guards and the four `NgDebMap_GetLocaMapOffsetX`/`Y` accessor macros of
`menumap_world_debug.h` (lines 76, 77, 81 and 82), and the 48 rows of the debug offset table, with an English
reading of every Japanese comment.

- Where the shipped data counts the same thing, the TSV gives that count beside the define. 12 region slots,
  39 areas, 60 World Map routes (45 normal, 15 special), 18 Strahl destinations and 48 sub-location files all
  match; the region and area `_MAX` values are the highest index (11 and 38).
- Each language's `menuquest.dat` (`us`, `kr`, `cn`) holds 66 quests, the highest quest id 172, in three groups,
  as its header says; `menuquest_group_MAX` is 3 while the highest group id is 2.
- `menumap_world_debug.h` defines its table only under `#ifdef DEBUG` and gives every sub-location the offset
  (0, 0).
`JsonData/debugMenuSettings.json` (`0x008FCCB0`) is a string with no code reference and no shipped file.

[`standard-file-formats-mapjump-nocrystal-rows.tsv`](standard-file-formats-mapjump-nocrystal-rows.tsv) lists
the 1,777 lines of `prefetchdata/ff12mapjump_custom_nocrystal.csv` in file order: the header line
(`name(src),id(src),name(dest),id(dest)` and eleven empty columns), then 1,776 rows. Each row names a source
zone and a zone it leads to, by internal name and field id, followed by eleven empty columns; the TSV adds
both places and the `mapjump` calls of the source zone's US script that reach the destination.

- No code reads the file, so it changes nothing in the game. The only strings
  holding `csv` in any case are the seven read paths (`opt.csv`, `eventList.csv` and the five soft-particle
  names, each referenced by one function), and no string holds `crystal` or `ff12map`, so no format string
  can build the name.
- Every prefetch path is `/PrefetchData/` (`0x00900648`) with a language folder and a fixed tail: `common.txt`
  (`0x001DA610`), `Maps/<map>.txt` (`0x001DA290`), `eventList.csv` (`0x001D9A40`) and `Events/<n>.txt`
  (`0x001D9DA0`), whose add-on form is the one path without a language. No path ends at the folder's top level,
  the executable imports no directory search, and no prefetch list, `.ah`, JSON, CSV or text file in the
  archive names the file.
- The rows are the zone-to-zone jumps the zone scripts make, without the crystal warps: 1,616 pairs are
  literal `mapjump` destinations of the source zone's script and 27 are reached through a variable the
  script sets; 26 are pairs the scripts reach only with mode 10, the gate-crystal warp's mode. Every name
  agrees with its field id in the [zone asset list](../World-Areas-And-Travel/zone-asset-list.md).
- The other 107 rows name jumps no script spells out: 99 link each Trial Mode stage to the next (`tri_a01`
  to `tri_t05`), where the stage script computes the destination; the rest lead from `bhm_c01`, `ttl_a01`
  and `ttl_b01` to `naf_a01`, from three `dor_e` rooms to `dor_e01`, and from `var_b01` to `rwf_a01` and
  `bhm_z01`.
- The other way round, 1,995 literal mode-10 calls in the scripts name a pair the file does not list,
  against 20 pairs of the other modes: 9 lead to fields without a zone script (293, 294, 434 and 769), 6
  from the three `dor_a` rooms to `dor_c12` and `dor_e01`, 3 to `byu_b01`, one from `fon_b01` to `fon_a04`,
  and one from `gil_a01` to itself.

## Modding notes

- Title images: write an uncompressed 24-bit TGA with no id field and the first row at the top. Put
  it in `gamedata/titleimage/in/`; a language folder (`us`, `fr`, `de`, `it`, `es`) is tried first
  and wins when the file is there.
- Keep every `opt.csv` line, header included, to at most 6 commas, and map names to 15 characters.
  `0x001A9050` stores one pointer per comma into four stack slots before it checks the field count, so
  more commas, or a longer name copied into its 16-byte buffer, overwrite the stack cookie at
  `[rbp + 0x2F]` and the game ends on the cookie check.
- `opt.csv` and the soft-particle tables need CRLF line ends and exactly the field count shown.
  `opt.csv` always skips line 1, so keep its header. Only FlipMapOpaqueOrder and
  ForceNoOpaqueChrFirst reach the map-art object through `0x001A7A50`.
- Keep soft-particle effect numbers below 512, `softparticle_bg.csv` map names to 13 characters,
  its rows to 4,096 and its map runs to 512; every change of map name between rows starts a new
  map record.
- Editing a JSON value is enough; the documents are read by key, and absent keys fall back as
  [Graphics settings](../Engine-Core/graphics-settings.md) describes. The developer
  menu's tracking-camera rows rewrite `init.json` (`0x001C7360`, `0x001C7520`).
- A new font colour needs `fontclut_<n>.json` with `mClutIndex` equal to `n`, for `n` below 28.
- A movie is replaced by a `.webm` of the same base name in `gamedata/d3d11/artdata/video/`.
- `icon.sys` supplies only the colour and light block (`+0x0C` to `+0xBF`) of the image
  `0x005832B0` builds; the title and icon names are written by the game.

## Related

- [Bigfile archive](bigfile-archive.md): the archive that holds every file here.
- [File size tables](file-size-tables-fst.md): the kind path arrays and the sizes the icon pair and boot descriptor are read by.
- [File path resolution](file-path-resolution.md): how a path such as `JsonData/init.json` becomes bytes.
- [Prefetch manifests](prefetch-manifests.md): `eventList.csv` and the `.ah` lists `ModelsToPreload` loads.
- [Graphics settings](../Engine-Core/graphics-settings.md): where the map, cutscene and `init.json` keys land.
- [Screen layouts](../Menus-And-HUD/screen-layouts.md): the `UISize` documents.
- [Clan Primer](../Menus-And-HUD/clan-primer.md): `monstergallery.json`.
- [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md): the save transaction that uses `icon.sys`.
