---
title: "PS2-era .bin families: every .bin file family under ps2data, the loader that reads it and what it holds"
kind: "reference"
category: "Game files and data tables"
addresses: "0x002DF9A0, 0x01E0280C, 0x0032E400, 0x0032E620, 0x00249210, 0x00249180, 0x00384420, 0x002368D0, 0x00238260, 0x002385D0, 0x01E09F68, 0x00378540, 0x00268750, 0x002467A0, 0x00246A10, 0x00280750, 0x00280670, 0x002808D0, 0x00280980, 0x00280AD0, 0x003658F0, 0x003643A0, 0x0039C3F0, 0x0039C150, 0x0036FFF0, 0x0037CCC0, 0x00259DF0, 0x003DCBC0, 0x0029CED0, 0x002C8EE0, 0x00291C80, 0x00561390"
---

## What it lists

Every `.bin` file in the archive is under `ps2data/`: 1,439 files, 2,481,360,070 bytes. A family is one
file name with the language folder and digit runs folded, so `menumap_sub00.bin` to `menumap_sub47.bin`
in nine languages are one row; there are 146 families.

For each family the list gives how the executable reaches it and what the bytes are. Families that
another page documents carry that page; the rest are described in the row and, where there is more to say,
in the sections below. The six small tables are on [their own page](small-bin-tables.md).

One more file under `ps2data/` is outside the list, because its archive name does not end in `.bin`:
`ps2data/debglobal.bin/file1`, 148 bytes. It holds four 16-byte NUL-padded strings, the IPv4 addresses
`10.0.5.238`, `10.0.5.255`, `10.0.5.254` and `10.0.16.26`, followed by 84 zero bytes;
[`ps2data-bin-families-debglobal-rows.tsv`](ps2data-bin-families-debglobal-rows.tsv) lists them with the file's
SHA-256.

- The executable names it once, `PS2Data\DebGlobal.bin` at `0x00D22C58`, and the string's only reference is the
  pointer at `0x01F2C750`. No RIP-relative, image-base-relative, absolute-pointer or RVA operand or data word names an
  address from `0x01F2C750` to `0x01F2C75F`.
- The data on either side belongs to other readers. Before it, an image ends at `0x01F2C74F`: a 0x10-byte header,
  0x1000 bytes of pixels and a 256-entry palette at `0x01F2C350`, read by `0x0051D220` and `0x0051D270`. After it, six
  16-byte records start at `0x01F2C760`, which `0x00521450` walks forward from `0x0052177E`.
- None of the four addresses occurs as text in any `.exe` or `.dll` in `x64`.

The archive's only other file without an extension is `ps2data/square_ff12/ff12config`, 2,048 bytes: the settings defaults that `0x00408C30` copies into the settings globals. Its reader and layout are on [Game settings](../Saving-Loading-And-Settings/game-settings.md).

## Columns

| Column | Meaning |
|---|---|
| `family` | path under `ps2data/image/ff12/` (or `ps2data/` for `add_motion`), `<lang>` for the language folder, `#` for a digit run (except the literal `tex2pack`) |
| `files` | shipped files in the family |
| `locales` | language folders the family ships in; `common` when the path has no language folder |
| `bytes` | total size of the family's files |
| `lead` | the first four bytes as ASCII when printable, else as a little-endian dword; `varies` when the copies differ |
| `kind_id` | resource kind and ids, `kind/ids`, from the path arrays `0x002DF9A0` installs, counting only entries whose `.fst` size equals the shipped file |
| `named` | locale copies whose path occurs as a string in the executable |
| `read_by` | for each copy, the languages whose arrays and size table resolve to it; `—` when no language does |
| `loader` | the function that requests the file, with the id base when the id is computed; `literal path` for a loader that opens a path string; `—` when no call site passes the family's kind and id as a constant or a constant base |
| `holds` | what the bytes are, measured from the shipped files |
| `page` | the page that documents the family, relative to this one; `—` when this page is the description |
| `explanation` | what the family is for, in plain words: from the title or summary of the page in `page`, and for the battle tables from the registry-slot names on [Item and ability ids](../Engine-Core/item-and-ability-ids.md); where `page` is `—`, from this page's own sections ("Families no path names", "Request entries") and, for `planmapname.bin`, from [area flags](../World-Areas-And-Travel/area-flags-navimapdata.md); a family no path names is marked as never loaded, and a loose battle table as unread because the game reads its `battle_pack.bin` copy (see below); empty where the row is already plain or no shipped source states the purpose |

### The two file tables

| Column | Meaning |
|---|---|
| `language` | the language folder |
| `file` | the file name |
| `path` | the path in the archive |
| `bytes` | the file's size |
| `sha256` | the SHA-256 of the file |
| `same_bytes_as` | the other language folders whose copy has the same bytes |
| `form` | the format: `st2e`, `licd`, `pack`, `word banks`, `FLAGROM1`, `FLAGDEF1`, `NAV`, `NPC0`, `PLMN`, `QST1`, `script section`, `path list`, `name list`, `record list`, or `table` for another layout |
| `header` | the header fields, decoded as the format's page gives them |
| `kind_id` | the resource kind and id whose array entry names this copy; empty when no array entry names it |
| `named_by` | the languages whose array names this copy |
| `read_by` | of those, the languages whose size table sizes the entry |
| `fst_size_matches` | `yes` when every reading language's size equals the file's size |
| `loader` | the function that requests the kind and id |
| `battle_pack_entry` | (test_battle only) the same folder's pack entry of the file's id: equal for the file's length, differing from a byte, empty, or no entry |
| `used` | `used: read by` the languages, or `unused` with the reason |

## Data

[`ps2data-bin-families.tsv`](ps2data-bin-families.tsv), 146 rows.

The two kind 9 files no code path requests have their rows in two tables:
[`ps2data-bin-families-test-map-ref-rows.tsv`](ps2data-bin-families-test-map-ref-rows.tsv), the 274 rows of
`common/test_map_ref.bin` beside the same rows of `map_ref.bin`, and
[`ps2data-bin-families-fhmusicdata-rows.tsv`](ps2data-bin-families-fhmusicdata-rows.tsv), the 27 records of
`common/fhmusicdata.bin` with the shipped music file and `musicinfo.bin` bytes of each id.

Two tables list the files of two folders one by one:
[`ps2data-bin-families-lang-bin-files.tsv`](ps2data-bin-families-lang-bin-files.tsv) the 58 `.bin` files under
`<lang>/bin/`, and [`ps2data-bin-families-test-battle-files.tsv`](ps2data-bin-families-test-battle-files.tsv) the
495 under `test_battle/<lang>/binaryfile/`. Each row gives the file's size, SHA-256, the copies with the same bytes,
its decoded header, the kind and id the path arrays give it, the languages that read it, the loader, and whether
the game reads it.

[`ps2data-bin-families-common-files.tsv`](ps2data-bin-families-common-files.tsv) lists the seven files of
`image/ff12/common/`, 4,892 bytes in all: `behindcamera.bin`, `eventmemorylist.bin`, `eventvib.bin`,
`fhmusicdata.bin`, `soundfoottable.bin`, `summoneffectdata.bin` and `test_map_ref.bin`. Each row gives the file's
size, its SHA-256 and its first four bytes in hex; no two of the seven have the same bytes.

[`ps2data-bin-families-myoshiok-files.tsv`](ps2data-bin-families-myoshiok-files.tsv) lists the 3,733 `.bin` and
`.dat` files under `myoshiok/`, and [`ps2data-bin-families-lang-common-files.tsv`](ps2data-bin-families-lang-common-files.tsv)
the 28 `.bin` files under `<lang>/common/`. Each row gives the file's path under `image/ff12/`, its size, every
path-array entry that names it (kind, id and the languages whose array holds it), and the languages whose size table
gives that entry the file's size.

- All 2,885 `.dat` files and all 28 `<lang>/common` files are named, and 824 of the 848 `.bin` files. The other 24
  are the copies no path names: `menuhandbook.bin` and `menuhandbook_order.bin` in `cn`, `de`, `es`, `fr`, `it`,
  `kr` and `us` and the `it` fonts (How a family is reached), the four `in_sdver` packs, and the four `_e3` sloc
  files (Families no path names).
- Every language whose array names one of these files sizes that entry at the file's size.
- 3,621 entries name a `myoshiok` file the archive does not hold. Every language whose array holds one gives it −1,
  so it is never read.

| Fact | Value |
|---|---|
| families, files | 146, 1,439 |
| families by language set | 50 in all nine language folders, 41 in `ch`, `cn`, `in`, `kr`, 24 in `ch` and `in`, 13 in `cn` and `kr`, 10 with no language folder, 4 in nine plus `in_sdver`, 2 in six, 1 in three, 1 in `in` and `us` |
| files the executable names | 1,256 |
| files some language reads through a path array | 1,250 |
| families with no copy named | 20, 41 files |
| families with a loader | 81; two of them through a literal path |
| families with no loader | 65: the 20 unnamed ones, 40 loose battle tables, and five more |
| families documented on another page | 114 |

Row tables for the six `packfiles` packs (Pack directories) and for four small `bin_menu` files of `ch` and `in`,
decoded with the family rows and, for `fontcolor.bin`, the colour table on [Text drawing](../Menus-And-HUD/text-drawing.md).
Each distinct content is listed once with the folders that hold it. A TIM2 entry's sprite record count runs from its
record table to the end of the picture header ([Menu sprites](../Menus-And-HUD/menu-sprites.md)).

| table | rows | one row per |
|---|---:|---|
| [`ps2data-bin-families-packfiles-files-rows.tsv`](ps2data-bin-families-packfiles-files-rows.tsv) | 52 | pack copy: folder, size, SHA-256, the folders with the same bytes and the directory |
| [`ps2data-bin-families-packfiles-rows.tsv`](ps2data-bin-families-packfiles-rows.tsv) | 688 | directory entry: offset, size, SHA-256, the folders whose entry has the same bytes, magic, the picture it is bound as, and the TIM2 or CLT2 header with the sprite record count |
| [`ps2data-bin-families-bin-menu-files-rows.tsv`](ps2data-bin-families-bin-menu-files-rows.tsv) | 10 | copy of `fontcolor.bin`, `item_clut.bin`, `license_chip.bin`, `menu_version.bin` and `monotone_chr.bin`: size, SHA-256, first bytes and header |
| [`ps2data-bin-families-fontcolor-rows.tsv`](ps2data-bin-families-fontcolor-rows.tsv) | 263 | `fontcolor.bin` entry: the RGBA colour and its bytes, the byte `+4` and bytes `+5` to `+7` |
| [`ps2data-bin-families-license-chip-rows.tsv`](ps2data-bin-families-license-chip-rows.tsv) | 361 | `license_chip.bin` record: its 64 bytes in 16 four-byte columns by offset |
| [`ps2data-bin-families-menu-version-rows.tsv`](ps2data-bin-families-menu-version-rows.tsv) | 1 | `menu_version.bin`: its 16 ASCII bytes |
| [`ps2data-bin-families-monotone-chr-rows.tsv`](ps2data-bin-families-monotone-chr-rows.tsv) | 6 | `monotone_chr.bin` palette: the CLT2 header fields, the palette's SHA-256 and the count of each alpha byte |

The colours of `item_clut.bin` are on [Menu graphics containers](as7-menu-graphics.md), the lists inside the
`mrppack_ys.bin` entries on [UI typed lists](ui-typed-lists.md) and the glyph records of `fontpack_fs.bin` on
[ExFont bitmaps](btm-exfont-bitmaps.md).

### How a family is reached

- **Path arrays.** `0x002DF9A0` installs 41 path-array pointers at `0x0215F000`. Kinds 1, 2, 5, 7, 8, 9 and
  12 get a per-language array; the others are shared. The `.fst` gives each entry's size, and the
  request path takes a file by kind and id ([file size tables](file-size-tables-fst.md)).
- **Which copy.** In 47 families only the `in` copy is named, read by most languages, and the `ch`
  copy, read by Korean and the two Chinese languages: `questbase.bin`, the two `mapjumpgroup` files,
  `navimapdata.bin`, `menuhandbook.bin`, `menuhandbook_order.bin` and the loose battle tables. Their
  other language copies ship but no path names them. Japanese, ASIA and IN read the `in` copy of the
  per-language families.
- **Italian fonts.** The `it` copies of `fontpack_fs.bin` and `fontpack_it.bin` are not named; Italian
  reads the `us` copies, as do French, German, Spanish and UK.
- **UK.** For 39 named families the UK arrays name a `uk` copy, among them `battle_pack.bin`, the text
  groups, `npcdic.bin`, `planmapname.bin` and the menu-map files. No `uk` folder ships and the UK size
  table marks those entries −1, so in UK those files are never read.
- **`in_sdver`.** The `in_sdver` copies of the four `*pack_ys` files, like the other `in_sdver` paths,
  are named only in a replacement list `0x002DF9A0` writes over the kind 7 array when its second argument is 0.
  That argument is the dword `0x01E0280C`, which the image initialises to 1 and no instruction writes
  (its readers are `0x0022A0B0`, which passes it, and `0x002465D0`); the replacement never runs.

### Request entries

The `loader` column comes from every call of the request entries, with kind and id followed back to
their constants: `0x0032E400` (size) and `0x0032E620` (request), `0x0051ED10`, `0x0024AB90`, the menu-set
wrappers `0x00249180`, `0x00249210`, `0x00249320`, `0x00249350`, `0x00249380`, `0x002493D0` (kind in `edx`, id in
`r8d`), and the kind-2 entry `0x00384420` (id in `ecx`). Computed ids were read from the callers' bodies:

| Loader | Id | Family |
|---|---|---|
| `0x002385D0` | the byte table `0x01E09F68[group]` (`0xFF`, 20-23, 1, 43-56, 24, 25, 62-67) | text groups 1 to 27 |
| `0x00238260` | `0x47 +` board | `board_1.bin` to `board_12.bin` |
| `0x002EA530` | `0x0B +` i, i = 0 to 9 | `charseinfo_*.bin` |
| `0x002CEAE0` | `0x10 +` byte `[0x0209AC30] + 0xB2D` | `face_guest#.bin` |
| `0x003C9950` | `0x0E +` byte `+0xC1` of its object | `map_efe#.bin` |
| `0x00291C80` | `0x98` to `0xA1` | `itemgra_c.tm2`, `item_clut.bin`, `Item_Gra00` to `07.as7` |
| `0x002C8EE0` | `0x74`, `0x75` | `monotone_chr.bin`, `Char_Silhouette.as7` |
| `0x003800D0` | `0x12A +` n, or `0x129` | `menuquest#.bin`, `menuquest.nfs` |
| `0x00575C30` | the six-entry table `0x00D23740` | the six `hctg` handbook files |
| `0x003C1DF0` | `0x496 +` n | `menumap_guide#.bin` |
| `0x003C1F00` | `0x142 +` n | `menumap_sub#.bin` |

The kind-2 entry `0x00384420` has three callers: the battle-pack load (`0x003843F0` from `0x002368D0` and
`0x00236C30`, id `0x13`), the board load and the text-group load. No call site passes another kind-2 id,
so the loose battle tables have no loader.

Kind 7 is requested at 70 call sites: five direct calls of `0x0032E620` (`0x00291D04`, `0x002C900B`, `0x003658C7`,
`0x00365967`, `0x0039C45D`) and 65 calls of the menu-set wrappers and of the table loops `0x003933F0`, `0x00393460` and
`0x003934F0`, every one with kind 7 in `edx` or fixed in the loop. The other request sites take the kind from a caller,
a record or a script ([File requests](file-requests-and-the-read-queue.md)). The by-path request `0x0032E7C0` is
reached only from the area loaders `0x003306E0` and `0x003319D0` and from `0x00377DC0`, which copies a kind's path
(`0x002DF880` at `0x00377E09`).

| table | rows | one row per |
|---|---:|---|
| [`myoshiok-file-meanings.tsv`](myoshiok-file-meanings.tsv) | 4,137 | file of the 844 `.bin`, 2,885 `.dat` and 408 `.tm2` files under `myoshiok/` outside `in_sdver`: path, extension, kind 7 id, the request site, the screen, what the file is there, the page for that screen, the languages whose array names it, and whether a kind 7 site, formula or table gives its id with the shipped data |

The ids per folder, with the site that asks for them:

- `bin_menu`: one fixed id per site, except `face_guest07` to `16`, id `0x10` + the guest's character id
  (`0x002CEAE0` at `0x002CEB1A`), and `map_efe00` to `06`, id `0x0E` + the number of the lowest area-flag bit set
  (`0x003C9950` at `0x003C999B`).
- `handbook`: `menuhandbook.bin` `0xC8` (`0x003158B0` at `0x003158F8`) and `menuhandbook_order.bin` `0xC9` (`0x00572D80`
  at `0x00572DEB`); each family's files from the base `[0x00D23740 + 2 x family]`: the catalog + 0 and file `NNN` + 2 +
  `NNN` (`0x00575C30` at `0x00575CAD`), the unlock table + 1 (`0x00576F50` at `0x00577027`, all six families).
- `packfiles`: fixed ids, `fontpack_fs.bin` `0xD2` (`0x003658F0`), `mrppack_ys.bin` `0xD3` and `clutpack_ys.bin`
  `0xD4` (`0x002808D0`), `fontpack_it.bin` `0xD5` (`0x0039C3F0`), `texpack_ys.bin` `0xD6` (`0x002467A0`) and
  `tex2pack_ys.bin` `0xD7` (`0x00280750`).
- `quest`: `menuquest.dat` `0x128` (`0x0037F4D0` at `0x0037F740`, `0x00576F50` at `0x00577057`); `menuquest00` to `02.bin`
  `0x12A` + the quest's group (`0x003800D0` at `0x00380145`).
- `worldmap`: `menumap_world`, `_location` and `_common.bin` `0xA2` to `0xA4` (`0x003BC2D0`), `menumap_area.bin`
  `0xA5` (`0x00253780`), `menumap_guideNN.bin` `0x496` + the schedule entry's file byte (`0x003C1DF0` at `0x003C1EBC`),
  `menumap_subNN.bin` `0x142` + the sub-location (`0x003C1F00` at `0x003C200D`).

A kind 7 site, formula or table gives the id of 760 of the `.bin` files and 1,856 of the `.dat` files with the
shipped data, and no id of these:

- 20 `.bin` copies no path array names: `menuhandbook.bin` and `menuhandbook_order.bin` in `cn`, `de`, `es`, `fr`,
  `it`, `kr` and `us`, the two `it` fonts and the four `_e3` sloc files.
- The two `menu_version.bin` copies: no site of the 70 passes id `0x90`.
- The 26 copies of `menumap_guide01.bin` to `04`: the file byte is 0 in all 77 schedule entries, so `0x003C1DF0` asks
  only for `0x496`.
- The `story`, `world`, `person` and `knowledge` catalogs, text bundles and picture bundles, 990 files: no Clan
  Primer category opens those families, so only their unlock tables load ([Handbook files](handbook-files.md)).
- 75 picture bundles no page-map slot names: seven `tutorial` files in each language and the 2, 3 and 7 extra
  `monster` files of `kr`, `ch` and `cn`.

Outside these sites, the script verb `debug_fileread` (`0x0050DFE0`) requests whatever kind and id its script
pushes.

The loaders of the kind 9 families, of `fontcolor.bin` and of the two `add_motion` files:

- `0x00259DF0` sizes `behindcamera.bin` (kind 9, id 3) with `0x0032E400`. At 0 or less it zeroes `0x02098DF0` and
  requests nothing (`0x00259E07`, `0x00259E81`); otherwise it allocates that many bytes under arena 6
  (`0x0036C1D0(6, 5)`, `0x0036C1A0(3)`, `0x0036A190`) and files the read with the completion `0x00259370` (`0x00259E6E`).
- `0x00268750` zeroes `0x02099D88`, `0x02099D90` and `0x02099D98` (`0x0026876B`-`0x00268779`) and sizes `map_ref.bin` (kind
  9, id 4); a negative size stops it (`0x00268782`). It allocates the block the same way into `0x02099D88`, tags it
  `MapRef` (`0x0036C660`) and files the read with the completion `0x002678A0` (`0x00268809`).
- It then sizes `test_area_ref.bin` (kind 9, id 2); unless that is negative (`0x0026881D`) it allocates the block
  with `0x00267930`, stores it at `0x02099D98` (`0x00268829`) and files the read with no descriptor (`0x0026883E`).
  [Weather](../World-Areas-And-Travel/weather.md) has both files.
- `0x0029CED0` runs `0x0029DC90`, which requests `key_signal_data.bin` (kind 7, id `0x24`) only while `0x0209C4A0` is
  null. On every call it then requests `fontcolor.bin` (kind 7, id 5) through `0x00249210` with 3 and 1 and no
  completion (`0x0029CEF6`), and tail-jumps to `0x002DD810` (`0x0029CF03`).
- `0x002DD810` zeroes `0x0215E6B8` and `0x0215E6C8` and stores the request record's buffer, its `+0x08`, at `0x0215E6C0`.
- The two `literal path` loaders, `0x0036FFF0` and `0x0037CCC0`, read `./PS2Data/add_motion/SkeletonMapping.bin` and
  `HighModelReplace.bin` whole ([Add-motion tables](../Graphics/add-motion-tables.md)).

### Pack directories

The six `packfiles/*.bin` files share one container: a fixed directory of `u32` offsets from the file
start, padded with `0xFFFFFFFF`, then the sub-files.

```python
+0x00  u32[16] or u32[32]  offset of each sub-file; the first entry equals the directory size
                           (0x40 or 0x80), unused entries 0xFFFFFFFF
```

| File | Directory | Used entries | Contents | Binder and destination |
|---|---|---|---|---|
| `texpack_ys.bin` | 16 | 5 (4 in `in_sdver`) | TIM2 | `0x00246A10` binds entries 0-4 through `0x0024A1D0` into the five texture objects `0x002467A0` set up, each at the pack start plus its directory offset; it does nothing while the pack pointer `0x0208EA88` is null (`0x00246A1E`) and skips a null texture object (`0x00246A2E`-`0x00246AA5`); `0x002467A0` returns at once while `0x0208EA88` is set (`0x002467B1`), sets up only the objects that are still null, and stores the pack buffer `0x00249180` returns at `0x0208EA88` (`0x0024688C`) |
| `tex2pack_ys.bin` | 16 | 11 | TIM2 | `0x00280670` binds entries 0-9 into `[0x0209AC30] + 0x338`..`0x380`; entry 10 is stored unbound at `+0x388`; it does nothing while the pack buffer `+0x3D8` is null (`0x00280683`), skips a null slot (`0x002806A7`), stores entry 10 only while `+0x388` is null (`0x002806D3`), and then releases and zeroes `0x0209AC38` and `0x0209AC40` when set (`0x00183720`, `0x0028070C`, `0x00280728`) |
| `mrppack_ys.bin` | 32 | 23 (21 in `in_sdver`) | MRP | `0x00280980` stores entries 0-22 at `[0x0209AC30] + 8 × i` and relocates each with `0x002A00F0`, each the start of the pack at `+0x3D0` plus its directory offset; it does nothing while `+0x3D0` is null (`0x00280993`) and stores and relocates each entry only while its slot is null (`0x002809A8`) |
| `clutpack_ys.bin` | 16 | 4 | CLT2 | `0x00280AD0` stores entries 0-3 at `[0x0209AC30] + 0x390`..`0x3A8`, each the start of the pack at `+0x3C8` plus its directory offset; it does nothing while `+0x3C8` is null (`0x00280AE1`) and stores each entry only while its slot is null (`0x00280AEF`-`0x00280B56`) |
| `fontpack_fs.bin` | 16 | 7 | font tables | `0x003643A0`: entry 0 (the font block) to `+0x08` (walked by `0x00366080`), 1 (the palette block) to `+0x190`, 2, 4, 5, 6 to `+0x110`, `+0x120`, `+0x128`, `+0x130`, the sheets of faces 0, 2, 3 and 4, whose font ids `0xB`, `0xD`, `0xE`, `0xF` it registers ([header](btm-exfont-bitmaps.md#layouts)); the binder skips entry 3, which repeats entry 2's offset in all six files; it returns at once while `[0x022CBE00]` is null (`0x003643AE`), fills each sheet slot only while that slot is null, and sets the face's ready bit and registers its id either way (`0x003643E5`-`0x0036449E`) |
| `fontpack_it.bin` | 16 | 6 | 2 TIM2, 4 tables | `0x0039C150`: entries 0-5 to `0x02AEE810`, `0x02AEE850`, `0x02AEE870`, `0x02AEE878`, `0x02AEE880`, `0x02AEE888`; entries 6 and 7, both `0xFFFFFFFF` in every file, would go to `0x02AEE848` and over `0x02AEE880` |

The font-table destinations are relative to the font object `[0x022CBE00]`. No binder checks an entry
against `0xFFFFFFFF` except `0x0039C150`'s entry 6, so a directory must keep every entry its binder reads.

`0x002808D0` requests `mrppack_ys.bin` and `clutpack_ys.bin` without a callback; `0x00253780` calls
`0x00280980`, which ends by calling `0x00280AD0`. Each request goes through `0x00249180` with kind 7, 3 and 1, and only
while its buffer slot is null: `mrppack_ys.bin` into `[0x0209AC30] + 0x3D0` (`0x002808E8`-`0x00280916`) and
`clutpack_ys.bin` into `+0x3C8` (`0x00280924`-`0x0028095D`). It then tail-jumps to `0x00280750`, the `tex2pack_ys.bin`
request (`0x0028096C`).

### Families no path names

20 families, 41 files, whose names occur nowhere in the executable and whose kind and id no array gives:

- **Script sections.** `btlctrl.bin`, `ctrl.bin`, `evctrl.bin` and `mapctrl.bin` (`ch`, `in`) begin with
  `0x8000000B`, the dword at the first section offset of every `.ebp` file: bare script sections without
  the `EBP2` wrapper.
- **`filelistlocalin.bin`.** The `ch` and `in` copies are identical: 38 section offsets, each section a
  count and string offsets, over 24,358 PS2 disc paths rooted at `%`. Section 0 starts with
  `%\cdi\in\system.cnf` and section 11 with `%\effect_finish\jp\magic\m0000.efx`, the first sized paths
  of resource kinds 0 and 11.
- **`katano/event.bin`.** Two nested `ashd` streams around a script section; the scheme is below.
- **`menumap_sub#_e#.bin`.** Four `sloc` files (`in` and `us`) beside the named `menumap_sub#.bin`.
- **Battle tables in `cn` and `kr` only.** Ten `st2e` tables, the two name tables and `logicpack.bin`.
  The `cn` and `kr` copies of each are identical.

The ten `st2e` headers read as `{tag, rows, row bytes, data offset}`:

| File | Rows × bytes | Header covers |
|---|---|---|
| `basic_skill.bin`, `growth_rate.bin`, `unit_data.bin` | 1,345 × 56, 128 × 56, 495 × 84 | the whole file |
| `actionchip_data.bin`, `bukitye_data.bin` | 0 × 8, 23 × 0 | none of the 32 bytes |
| `mons_act.bin` | 359 × 0 | none of 11,756 bytes |
| `mons_category.bin`, `mons_race.bin`, `object_data.bin`, `target_data.bin` | 16 × 2, 64 × 2, 66 × 8, 1,090 × 8 | 64 of 156, 160 of 444, 560 of 1,708, 8,752 of 39,000 bytes |

`basic_skill_basic_skill_name.bin` and `growth_rate_growth_rate_name.bin` hold one UTF-16LE string per
row of their `st2e` sibling (1,345 and 128), Japanese designer labels such as `LEVEL-00基本値` and
`テスト成長値`. `logicpack.bin` has the same count-and-offsets frame over 1,310 records.

The `ashd` scheme of `katano/event.bin`, decoded by the measurement script:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` |  | the magic "ashd" |
| `+0x04` | `u32` |  | the value `0x2509`, which the decoding does not use |
| `+0x08` | `u32` |  | decoded size |
| `+0x0C` | `tokens` |  | the compressed stream, read one token byte t at a time: an even t copies the next t / 2 bytes; an odd t forms u16 w = t + (next << 8) and copies (w >> 12) + 3 bytes from ((w >> 1) & `0x7FF`) + 1 bytes back |

The file decodes to exactly `0xB10` bytes, which are another `ashd` stream; that decodes to exactly
`0x23E0` bytes, a script section tagged `0x80000002` with the time stamp `09/18 20:20:10` and the source name
`event.src`.

The script has 26 actors and 1,617 instructions, in two tables:
[`ps2data-bin-families-katano-event-actors.tsv`](ps2data-bin-families-katano-event-actors.tsv), one row per actor,
and [`ps2data-bin-families-katano-event-steps.tsv`](ps2data-bin-families-katano-event-steps.tsv), one row per
instruction.

- The actors are `control`, `コントロール` and `バッシュ00` to `バッシュ23`. Each `バッシュ` actor has the functions
  `init`, `appear`, `disappear`, `setpc` and `clearpc`. `type` is the actor record's u16 at `+0x04`: 0 for
  `control` and 5 for the others.
- The header is `0x54` bytes. Its words `+0x00` to `+0x50` are the fields of the shipped sections' `0x90`-byte
  header, which adds `+0x54` to `+0x8F`.
- The actor records are `0x20` bytes, the first eight words of the shipped `0x30`-byte record. Each actor's
  instructions run from its record's start offset for its record's count with no gap, and every jump lands on an
  instruction of the same actor.
- Calls are given by id: this section numbers its calls differently from the shipped verb table. It calls id `0x0A`,
  the shipped `cos`, which pops a float, with no argument and tests bit `0x1` of the result.
- The game never loads it: no path array names `katano/event.bin`, and the executable holds neither `event.bin`
  nor `katano/event` as text, so replacing or removing the file changes nothing. The three `katano` strings the
  executable holds are source file names: `atelareaload.c`, `ateldecode.c` and `atelload.c`.

### Loose battle tables

Under `test_battle/<lang>/binaryfile/`, 40 named families have no loader and repeat the bytes at an
entry of the same language's `battle_pack.bin`, for the file's length, in some or all of their copies:
the `in`, `ch`, `cn` and `kr` copies for most, every language's for `battle_message.bin` and `word.bin`,
only `cn` and `kr` for `ability_data.bin`, `menkyo_data.bin` and `savemember_data.bin`, only `ch` and
`in` for `action_data.bin`, and `in`, `cn` and `kr` for `horidashi.bin`.

The game reads those
tables from the pack ([authored data tables](authored-data-tables.md)). `license_data.bin` and
`movie.bin` match no pack entry.

### Named but not shipped

The arrays also name `.bin` files the archive does not hold, with size −1 in every table: text group 27
`menu05.bin` (kind 2, id 67), `npc_name.bin`, `questhint.bin` and `questhittext.bin` (kind 9, ids 29, 34,
35), and further `menuquest03.bin` to `menuquest05.bin` and other kind 7 entries.

### The language folders file by file

The 58 `.bin` files under `<lang>/bin/` hold 27 different contents. The `ch` and `in` folders also hold each script
section's `.ebp`, `.dbg`, `.msb` and `.sbn`, 32 files
([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md)).

Of the 27 contents, 26 are read:

| Files | Read by |
|---|---|
| `npcdic.bin`, `planmapname.bin`, one per folder | that folder's language; Japanese, ASIA and IN read `in` |
| `mapjumpgroupflagrom.bin`, `mapjumpgroupinit.bin`, `navimapdata.bin`, `questbase.bin` in `in` | Japanese, US, French, German, Italian, Spanish, UK, ASIA and IN |
| the same four in `ch` | Korean and the two Chinese languages |

The other 32 are never read:

- 22 copies that no array names: `mapjumpgroupflagrom.bin`, `mapjumpgroupinit.bin` and `questbase.bin` in `cn`,
  `de`, `es`, `fr`, `it`, `kr` and `us`, and the `cn` `navimapdata.bin`. Each has the same bytes as the `in` and
  `ch` copies the arrays name.
- The 10 files no path names (Families no path names): the four script sections and `filelistlocalin.bin` in
  `ch` and `in`.

The `ch` and `in` copies of each script section are identical. `btlctrl.bin`, `ctrl.bin` and `mapctrl.bin` are the
same bytes as their folder's `.ebp` from offset `0x80`, for the `.bin` file's whole length. `evctrl.bin` (22,320
bytes) occurs nowhere in `evctrl.ebp` (38,720 bytes), so it is another build of that script.

### The battle tables file by file

The 495 files under `test_battle/` hold 329 different contents. 267 are read:

| Files | Copies read | Loader |
|---|---|---|
| `battle_pack.bin` | all nine, one per language as the arrays give it | `0x002368D0` (id `0x13`) |
| the 26 shipped text groups, `key_signal.bin` to `menu04.bin` | all nine | `0x002385D0`, id from the byte table `0x01E09F68` |
| `board_1.bin` to `board_12.bin` | `in` and `ch` | `0x00238260` (id `0x47 +` board) |

The other 228 are never read:

- 98 copies the arrays name but no call site requests: the `ch` and `in` copies of the 40 loose battle tables,
  and `battle_message.bin` and `word.bin` in all nine folders. `0x00384420`, the one kind-2 request, has three
  callers, the pack (`0x0038440A`), the boards (`0x0023837D`) and the text groups (`0x0023861E`).
- 104 copies no array names: the `cn` and `kr` copies of the same 40 tables and of the twelve boards.
- 26 files no path names: the 13 families that ship only in `cn` and `kr` (Families no path names).

### The battle pack's own copies

Every language's `battle_pack.bin` has 71 entries, and the same 29 of them are empty, their start equal to the
next one's: id 19, the pack itself, the 27 text-group ids (1, 20-25, 43-56, 62-67), which the game loads as files
of their own, and id 40, which no array names. The `battle_pack_entry` column compares each loose table with the
entry of its own id in the same folder's pack.

161 copies equal their entry for the file's length. 17 differ, each an earlier or later table:

| Table | Copies | File | Pack entry |
|---|---|---|---|
| `ability_data.bin` (id 58) | `ch`, `in` | 128 rows of 8 | 129 rows |
| `license_data.bin` (id 12) | `ch`, `in` | 360 rows of 24 | 361 rows |
| `license_data.bin` (id 12) | `cn`, `kr` | 361 rows, differing from byte `0x20` | 361 rows |
| `menkyo_data.bin` (id 26) | `ch`, `in` | 31 rows of 8 | 32 rows |
| `movie.bin` (id 69) | `ch`, `cn`, `in`, `kr` | 38 rows of 8 | 49 rows |
| `savemember_data.bin` (id 59) | `ch`, `in` | 226 rows of 44, differing from byte `0x4F4` | 226 rows |
| `horidashi.bin` (id 57) | `ch` | 128 rows of 36, differing from byte `0x1228` | 128 rows |
| `action_data.bin` (id 14) | `cn`, `kr` | 543 rows of 60, differing from byte `0x18B4` | 543 rows |

The game reads only the pack's tables, so none of these differences reaches play.

### Replacing a file

- A file read by kind and id is read at the size its language's size table gives: the request is sized with
  `0x0032E400` and that many bytes are allocated and requested (`0x00384420`;
  [File size tables](file-size-tables-fst.md)). A replacement of another length needs the entry changed in the
  `.fst` of every language that reads the copy (the `read_by` column).
- A size entry of -1 is never read, and the requester is told the file was delivered
  ([File requests](file-requests-and-the-read-queue.md)).
- Edit a battle table inside `battle_pack.bin`: the loose copies under `test_battle/` are never requested.
- `common/fhmusicdata.bin` and `common/test_map_ref.bin` are requested by no code path (Data, above), so a
  replacement of either has no effect in play and no layout to keep.
- Edit the copy the language reads, the `read_by` column. For the files whose only named copies are in `in` and
  `ch`, `in` serves the Western languages, Japanese, ASIA and IN, and `ch` serves Korean and the two Chinese
  languages; the copies in the other folders are never read.

## Related

- [File size tables](file-size-tables-fst.md): the path arrays and the sizes behind `kind_id`.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the request entries.
- [Bigfile archive](bigfile-archive.md): where the files are read from.
- [Small .bin tables](small-bin-tables.md): footsteps, vibration, battle windows, the button legend,
  quest texts and summon colours.
- [Authored data tables](authored-data-tables.md): `battle_pack.bin` and the license boards.
- [Battle and menu text tables](battle-text-tables.md): the text groups.
- [Area battle data](ard-area-battle-data.md): the `.ard` files.
- [Character sound tables](character-se-tables-chse.md), [TIM2 images](tim2-images.md) and
  [UI typed lists](ui-typed-lists.md): the `charseinfo`, picture and MRP families.
- The menu families: [as7 menu graphics](as7-menu-graphics.md),
  [CL2 colour tables](cl2-menu-colour-tables.md), [MRP packages](mrp-menu-resource-packages.md),
  [exfont bitmaps](btm-exfont-bitmaps.md), [bin_menu images](binmenu-images.md),
  [menu map files](menu-map-files.md), [handbook files](handbook-files.md) and
  [quest menu files](quest-menu-files.md).

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Platform online achievements: `0x00408C30` calls `0x00862A20`; those functions are documented on
  [save file format](../Saving-Loading-And-Settings/save-file-format.md).
