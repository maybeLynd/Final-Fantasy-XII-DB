---
title: "Standard file formats: the TGA, CSV, JSON, WebM, C-header and PS2 icon files the game ships, and which of them it reads"
kind: "format"
category: "Game files and data tables"
summary: "The archive files in public formats: two TGA title images, seventeen CSV tables, 830 JSON documents, forty WebM movies, six C headers, the PS2 memory-card icon pair and the PS2 boot descriptor. For each, its shipped counts and sizes, the function that opens it and what that function does with the bytes, and which files no path in the executable names."
addresses: "00473E80, 01F26568, 001D8D60, 001EE820, 001A9050, 001A7A50, 00674A00, 0024C970, 0024F240, 0024EF90, 001D9A40, 00200BF0, 001C3760, 001C7360, 001C7520, 00202930, 001C61F0, 001C53F0, 001C5F20, 001C76E0, 001C5930, 001C5750, 001C6E20, 001C2F50, 00582790, 00249210, 005832B0, 002DF9A0, 01E461F0, 002DF980, 001B7F30"
---

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
(`008F6560`), the five `.\PS2Data\soft_particle\softparticle_*.csv` names (`00915400`–`009154D8`),
`/eventList.csv` (`00900738`), the `JsonData/...` names (`008F9E38`–`008F9EE0`), the title-image
directory `/GameData/titleimage/` (`00D22660`) and the movie pattern `%s%s.webm` (`008F8D70`). The
PS2 icon pair and the boot descriptor are instead entries of the per-kind path arrays that
`002DF9A0` installs at boot, and are read by kind and id
(see [File size tables](file-size-tables-fst.md)).

## Layouts

### TGA title image

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | id length | 0 |
| `01` | `u8` | colour-map type | 0 |
| `02` | `u8` | image type | 2 (uncompressed true colour) |
| `03` | `u8[9]` | colour | map, origin 0 |
| `0C` | `u16` | width | 1920   <- read |
| `0E` | `u16` | height | 1080   <- read |
| `10` | `u8` | bits per pixel | 24 |
| `11` | `u8` | descriptor | `0x20` (top-left origin) |
| `12` | `u8[width*height*3]` | pixels, B G R, first row at the top |  |

The game reads only the width and height; it assumes the rest (no id field, 24-bit, top-left).

### CSV tables

All seventeen are CRLF text without quoting or a byte-order mark.

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

```
opt.csv entry (tree node +0x24, keyed by the map-name hash)
+0x00  u8   ForceMSAAOff starts with Y or y
+0x01  u8   FlipMapOpaqueOrder starts with Y or y
+0x02  u8   SMAA starts with Y or y
+0x03  u8   ForceNoOpaqueChrFirst starts with Y or y

soft-particle entry, 4 bytes, indexed by the effect number (per-type tables)
or by row number (softparticle_bg.csv)
+0x00  u8   GroupId                (bg only)
+0x00/+0x01  u8  UseSoftParticle != 'N'   (+0x00 per type, +0x01 bg)
+0x02  u16  SoftParticleFactor     (per type: 10 when "Yes" has no number)

bg map record, 16 bytes at 02F93340, one per run of rows with the same Map
+0x00  char[14]  map name
+0x0E  u16       first row of the run

eventList.csv record, 8 bytes
+0x00  u16  second field
+0x04  u32  third field          the first and fourth fields are read and dropped
```

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
| `00` | `char[4]` | "PS2D" |  |
| `06` | `u16` | 26 | title line-break position |
| `0C` | `u32` | 109 | background transparency |
| `10` | `u32[4][4]` | background corner colours (39,24,6,0 / 186,164,125,0 alternating) |  |
| `50` | `f32[3][4]` | light directions (0.5, 0.5, 0.5, 0) |  |
| `80` | `f32[3][4], f32[4]` | light colours, ambient | (a full PS2 icon.sys continues with the title at +`0xC0` and three icon names; this one ends here) |

Icon1.ico (33,688 bytes; PS2 icon model, not a Windows icon):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u32` | 0x00010000 | file id (the same four bytes a Windows .ico starts with) |
| `004` | `u32` | 1 | animation shapes |
| `008` | `u32` | 6 | texture type |
| `00C` | `f32` | 1.0 |  |
| `010` | `u32` | 36 | vertices |
| `014` | `36 x 24 bytes` | vertex, normal, uv, colour |  |
| `374` | `20 + 16 bytes` | animation header (one frame), frame record |  |
| `398` | `u16[128*128]` | texture (32,768 bytes) |  |

### PS2 boot descriptor

`system.cnf` is three CRLF lines, 57 bytes: `BOOT2 = cdrom0:\SLPM_667.50;1`, `VER = 0.01`,
`VMODE = NTSC`.

## Shipped data

| Fact | Value |
|---|---|
| archive | 89,414 entries, 48 extensions; eight are public formats |
| `.tga` | 2 files, 6,220,818 bytes each: `warning.tga`, `sqex logo size_ffx.tga`, both in `gamedata/titleimage/in/` |
| TGA header | both type 2, 1920 × 1080, 24 bpp, descriptor `0x20`; 18 + 1920 × 1080 × 3 = the file size |
| `.csv` | 17 files, 209,639 bytes |
| `ps2data/opt.csv` | 10,182 bytes, header + 459 rows; SMAA `Yes` in all 459, FlipMapOpaqueOrder in 7, ForceNoOpaqueChrFirst in 9, ForceMSAAOff in none |
| `ps2data/soft_particle/` | `bg` 65,112 bytes (2,373 rows; 418 maps in 433 runs), `chara` 2,187 (126 rows, ids 0–125), `common` 2,686 (147, ids 1–151), `event` 3,747 (218, ids 0–227), `magic` 6,528 (362, ids 0–396) |
| `prefetchdata/<lang>/eventlist.csv` | 9 identical files (`us fr it es de jp kr cn ch`), 4,912 bytes, 315 records |
| other CSV | `jsondata/parametersmanageruisizestruct.csv` 10,350 bytes; `prefetchdata/ff12mapjump_custom_nocrystal.csv` 64,639 bytes |
| `.json` | 830 files, 3,230,298 bytes; 775 CRLF, 29 on one line, 26 empty; none with a byte-order mark |
| `jsondata/` root | `0.json` 2 bytes, `init.json` 5,746, `monstergallery.json` 337,640, `monstertoweapon.json` 50,445 |
| `jsondata/maps/` | 459 files, 581,069 bytes; the same 459 map names as `opt.csv` |
| `jsondata/cutscenes/` | 337 files, 2,235,149 bytes; 39 `sum_*`, of which 26 are empty; one `_2ndscreen` file (`slm_z0100_2ndscreen.json`) |
| `jsondata/fontcluts/` | 28 files `fontclut_0` … `fontclut_27`, 8,160 bytes; each file's `mClutIndex` equals its number |
| `jsondata/uisize/` | `uisize.json` 7,478 bytes, `uisize_sd.json` 4,609 |
| not strict JSON | 4: `uisize.json` and `uisize_sd.json` end with a trailing comma, `maps/bhm0201.json` and `cutscenes/evt_t0005.json` each miss one comma |
| `.webm` | 40 files, 10,881,781,239 bytes (21,563,773 to 1,451,123,949) |
| WebM header | all 40 open with EBML `1A 45 DF A3`, doctype `webm`; the first 64 KiB declares `V_VP8` in all 40 and `A_VORBIS` in 39 (`ivt.webm` has no Vorbis track entry there) |
| `.h` | 6 files, 13,036 bytes: `us/worldmap/menumap_sub.h`, `menumap_world.h`, `menumap_world_debug.h`; `menuquest.h` in `us`, `kr`, `cn` |
| `.h` text | generated `#define` tables (converted from Excel sheets), CRLF, UTF-8; the `kr` and `cn` `menuquest.h` start with a UTF-8 byte-order mark |
| `.sys`, `.ico` | `icon.sys` (192 bytes) and `icon1.ico` (33,688 bytes) in `myoshiok/in/bin_menu/` and `myoshiok/ch/bin_menu/`; the two copies are byte-identical |
| `.cnf` | `ps2data/cdi/in/system.cnf`, 57 bytes |

## Loader behaviour

### The title images

`00473E80(index)`, whose one caller is `0034E340`, returns for an index above 3 and otherwise takes
the name from the four-entry table at `01F26568`: `warning.tga`, `SQEX Logo size_FFX.tga`,
`rating_01.tga`, `thankyou.tga`.

It maps the language from `00229E40` to a folder (1 `us`, 2 `fr`, 3 `de`, 4 `it`, 5 `es`, 10 `in`;
any other language gets an empty folder), formats `/GameData/titleimage/<folder>/<name>` with
`"%s%s/%s"`, and probes it with `002DF8E0`. When the probe gives less than 1 byte it formats the path
again with folder `in`. Only `in/` ships, so every language shows the `in/` images, and indexes 2
and 3 name files that ship nowhere.

The path goes to `00183180` → `001D8D60`, the decoder. It opens a stream on the path, returns
without a texture when the open fails, reads the 18-byte header, creates a texture of the header's
width and height (`00184380`), reads `width × height × 3` bytes straight after the header, and hands
them to `001EE820` with its flip flag fixed at 0 (`001D8E9E`). `001EE820` writes each pixel as
bytes 2, 1, 0 and `0xFF`, row 0 first. Nothing reads the image type, depth or descriptor, so a
compressed, 32-bit or bottom-up TGA loads wrong.

### Per-map render options: opt.csv

`001A9050`, called from the map-art set-up `001A2130`, opens `./PS2Data/opt.csv` through the stream
helper `001D6F20`, reads it whole and walks it a line at a time:

- a line ends at the next CR, and the next line starts two bytes later; a file without CR yields no
  rows;
- the first line is skipped as the header, and only lines with exactly five fields are kept;
- the map name is hashed with `00674A00` (start 5381, multiply by 33, add each byte, keep 31 bits);
- each of the other four fields becomes 1 when it starts with `Y` or `y`, and the four bytes go into a
  tree node keyed by the hash (tree at `+0x3E0` of the map-art object).

When a map is entered, `001A7A50` hashes the map name (the text after the backslash of
`<area>\<map>`) and looks it up. A hit copies byte 1 (FlipMapOpaqueOrder) to `+0x418` and byte 3
(ForceNoOpaqueChrFirst) to `+0x419` of the map-art object; a miss sets both to 0. `001A7A50` does not
use bytes 0 and 2.

### Soft-particle tables

`0024C970` (from `00259180`) clears four 0x800-byte tables and reads `chara`, `event`, `magic` and
`common` into them (`02F96B40`, `02F96340`, `02F95B40`, `02F95340`) with `0024F240`, then reads
`softparticle_bg.csv` with `0024EF90`.

- `0024F240` scans each CR-terminated line with `"%c%d.efx,%s"`. With three matches, the entry for
  the effect number gets byte 0 = (the rest does not start with `N`); when it is set, `"Yes,%d"` gives
  the factor at `+2`, or 10 without a number. The header line fails the scan. The effect number is not
  bounded against the table's 512 entries.
- `0024EF90` keeps lines with exactly five fields, copies the map name, reads GroupId with `"%d,"`,
  and, when that succeeds, writes the next 4-byte entry of `02F8F340`: GroupId, UseSoftParticle not
  `N`, factor with `"%d"`. Each time the map name differs from the previous row's, it appends a
  16-byte record (name, first row) to `02F93340`. The row count goes to `02092714` and the map count
  to `02092718`. VFXName is not stored.

### Event prefetch schedule: eventList.csv

`001D9A40`, run by the prefetch worker `001DADC0`, opens
`/PrefetchData/<language>/eventList.csv`, scans `"%s"` tokens and steps past each by its length plus
two, drops tokens starting `##`, and parses each token with `"%d,%d,%d,%d"`. A record with four
values keeps the second (as `u16`) and third fields; the first and fourth are dropped. What the
schedule triggers is on [Prefetch manifests](prefetch-manifests.md).

### The JSON reader

`00200BF0(document, path)` opens a stream on the path (`00597970`), and when the stream has a
positive length reads it whole, terminates it with a zero byte and parses it into the document
(`00200E60`). An empty or missing file parses nothing. Keys are then fetched with `001FF740` and
read as numbers or strings (see [Graphics settings](../Engine-Core/graphics-settings.md)
for the readers and the lookup order). Every reader below goes through `00200BF0`.

### init.json and monstergallery.json

`001C3760` (from `00186CD0`) parses `JsonData/init.json` into the global document `01F813C8`. Each
`ModelsToPreload` string goes to `001BB920`, which builds
`./GameData/D3D11/ArtData/chr/<name>_D3D11.ah` and loads that asset list (all six shipped names have
one). `TrackingMapScreenRateX`/`Y` and `TrackingMapScreenSuperWideMul`/`Plus`, when present, go to
`002B6670`, `002B6680`, `002B6690` and `002B66A0`. The same function then parses
`JsonData/MonsterGallery.json` into `01F81308`; the monster viewer reads it from there
([Clan Primer](../Menus-And-HUD/clan-primer.md)).

`001C7360` and `001C7520`, both called from the developer menu `001D1660`, are the only writers: when
`init.json` has the key, they store new tracking values in `01F813C8` and write the whole document
back to `JsonData/init.json` through an output file stream (`00202930`).

### Map, cutscene, font-colour and layout documents

- Maps: `001C61F0` (from `00214C30`) runs while `01DF6E48` (1 as shipped, written only by the
  developer menu) or `01F81282` is set. `001C53F0` takes the map-art object's `<area>\<map>` string,
  keeps the text after the first backslash and appends `.json`. When that name differs from the last
  one (`01F81388`), `JsonData/Maps/<map>.json` is parsed into `01F81328`; the area scene-config
  loader `001C7940` then applies it.
- Cutscenes: `001C5930`, entered by a tail jump from `001EC600`, parses
  `JsonData/CutScenes/<name>.json` into `01F813A8 + slot × 0x10` and `<name>_2ndScreen.json` into
  `01F813D8 + slot × 0x10`, the slot being `01DF6E4C`. `001C5750`, reached from
  `0020AC30` for names containing `sum_`, parses `JsonData/CutScenes/<name>.json` into a local
  document and passes `Common.mDofFocusDistance` and `Common.mDofApertureFnumber` to `00194250`.
- `001C6E20` (from `001F3500`) parses `JsonData/0.json`, takes its `ChangedFileName` string as a
  cutscene name for the cutscene document slots. The shipped `0.json` is `{}`.
- Font colours: `001E94E0(manager, n)` for `n` below 28, the first time entry `n` is used, formats
  `fontclut_%d` and calls `001C5F20`, which parses `JsonData/FontCluts/fontclut_<n>.json` into
  `01F81378` (gated like the map files).
- `001C76E0` then reads `mClutIndex`, selects that entry (`0x24` bytes at manager `+0xF68`), stores
  `mShadowRed/Green/Blue/Alpha` and `mFontRed/Green/Blue/Alpha` as integers at `+0x04` to `+0x20`,
  and clears the document. Nothing fetches `mClutComment`.
- Layouts: `001C6C00` (from `001B1580`) loads `UISize.json` or `UISize_sd.json`
  ([Screen layouts](../Menus-And-HUD/screen-layouts.md)).
- `001C2F50` (from `0017D6E0`) parses `/Tools/AutoTest/MapIndex.json` for a `MapIndex` value; no such
  file ships.

### The PS2 memory-card icon pair

`00582790` asks `00249210` for kind 7 id `0x2C` (`icon.sys`) and kind 7 id `0x2D` (`icon1.ico`),
storing the data pointers at `+0x110` and `+0x118` of the save object (`00582814`, `0058282F`).
`00249210` sizes the file from the [file size table](file-size-tables-fst.md) (`0032E400`),
allocates a buffer and queues the read (`0032E620`).

Every kind-7 array that `002DF9A0` installs holds the pair at ids 44 and 45. The KR, CH and CN arrays
(languages 7, 8 and 11; `01E0E530`, `01E5A3D0`, `01EABBA0`) name the `ch` copies, the others the `in`
copies. Ids 46 and 47 name `icon2.ico` and `icon3.ico`, which ship nowhere and are sized -1 in every
table.

`005832B0`, called from state 7 of the save transaction `00581DA0`, uses `icon.sys` as a template.
It clears a `0x3C4`-byte image, stamps `PS2D` (`00583307`), writes a title of play time and save
number at `+0xC0` and its line-break position at `+0x06`, copies bytes `+0x0C` to `+0xBF` from the
loaded `icon.sys`, and writes the name `005837F0` returns for kinds 2, 3 and 4 (`static.ico`) at
`+0x104`, `+0x144` and `+0x184`.

State 7 builds this image at `+0xE8` of the transaction record; the storage request it then files
(`00582540`) names only the numbered slot file. How the slot files are written and deleted is on
[Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md).

### The boot descriptor

`ps2data/cdi/in/system.cnf` is kind 0, id 0: entry 0 of the array `01E461F0`, which `002DF9A0`
stores at `0215F000`. Every `.fst` sizes it at 57 bytes. It is the first of seven kind-0 paths; the
other six, the PS2 executable `SLPM_667.50` and the modules `ioprp300.img`, `mcman.irx`, `mcserv.irx`,
`dbcman.irx` and `libsd.irx`, ship nowhere in the archive.

### Movies

`001B7F30` gets a path with `002DF980(0x1C, movie × 2)`: `002DF980` returns
`[[0215F000 + kind × 8] + index × 8]`, and kind 28 is the movie kind. That entry is a PS2
`movie_finish\<lang>\<NAME>.md` path. The player keeps the text between the last backslash and the
last dot, formats `"%s%s.webm"` with the prefix `/GameData/D3D11/ArtData/video/` (`01DF6E28`), and
opens it with `0067A480` on the player object at its `+0x678`. A null path entry stops the movie.

The first 98 ids of kind 28 hold 45 `.md` paths at even ids, each followed by its `.mh` path, and
four empty pairs. 40 of the 45 base names have a `.webm`; `dlb`, `opd`, `se1`, `se2` and `bd2` have
none.

### Files no path names

No string in the executable, ASCII or UTF-16, in any case, names `monstertoweapon.json`,
`parametersmanageruisizestruct.csv`, `ff12mapjump_custom_nocrystal.csv` or any of the six `.h` files.
`JsonData/debugMenuSettings.json` (`008FCCB0`) is a string with no code reference and no shipped file.

## Modding notes

- Title images: write an uncompressed 24-bit TGA with no id field and the first row at the top. Put
  it in `gamedata/titleimage/in/`; a language folder (`us`, `fr`, `de`, `it`, `es`) is tried first
  and wins when the file is there.
- Keep every `opt.csv` line, header included, to at most 6 commas, and map names to 15 characters.
  `001A9050` stores one pointer per comma into four stack slots before it checks the field count, so
  more commas, or a longer name copied into its 16-byte buffer, overwrite the stack cookie at
  `[rbp + 0x2F]` and the game ends on the cookie check.
- `opt.csv` and the soft-particle tables need CRLF line ends and exactly the field count shown.
  `opt.csv` always skips line 1, so keep its header. Only FlipMapOpaqueOrder and
  ForceNoOpaqueChrFirst reach the map-art object through `001A7A50`.
- Keep soft-particle effect numbers below 512, `softparticle_bg.csv` map names to 13 characters,
  its rows to 4,096 and its map runs to 512; every change of map name between rows starts a new
  map record.
- Editing a JSON value is enough; the documents are read by key, and absent keys fall back as
  [Graphics settings](../Engine-Core/graphics-settings.md) describes. The developer
  menu's tracking-camera rows rewrite `init.json` (`001C7360`, `001C7520`).
- A new font colour needs `fontclut_<n>.json` with `mClutIndex` equal to `n`, for `n` below 28.
- A movie is replaced by a `.webm` of the same base name in `gamedata/d3d11/artdata/video/`.
- `icon.sys` supplies only the colour and light block (`+0x0C` to `+0xBF`) of the image
  `005832B0` builds; the title and icon names are written by the game.

## Related

- [Bigfile archive](bigfile-archive.md): the archive that holds every file here.
- [File size tables](file-size-tables-fst.md): the kind path arrays and the sizes the icon pair and boot descriptor are read by.
- [File path resolution](file-path-resolution.md): how a path such as `JsonData/init.json` becomes bytes.
- [Prefetch manifests](prefetch-manifests.md): `eventList.csv` and the `.ah` lists `ModelsToPreload` loads.
- [Graphics settings](../Engine-Core/graphics-settings.md): where the map, cutscene and `init.json` keys land.
- [Screen layouts](../Menus-And-HUD/screen-layouts.md): the `UISize` documents.
- [Clan Primer](../Menus-And-HUD/clan-primer.md): `monstergallery.json`.
- [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md): the save transaction that uses `icon.sys`.
