[Home](../../README.md) / [Game files and data tables](README.md) / Prefetch and asset-header manifests

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Prefetch and asset-header manifests: the text lists that preload files into the file cache, and the .ah lists that name the parts of a model, map or font | format | Game files and data tables | Archives and file loading | The plain-text manifests the game reads by whitespace-separated tokens: the prefetch lists (common.txt at start-up, one per map on map entry, one per event, eventList.csv's event schedule, the add-on folder) and the background thread that opens their names into the RAM file cache under protected stamps; and the .ah asset-header lists that name, in order, the .phyre files of every model, map, font and procedural texture set and load each of them, with the AssetListManager pools and the pass that resolves asset imports once a list has loaded; the prefetch manager's language folder, lists and event watch; and the menu TexList.txt. Includes the shipped counts and the rules both formats impose. | 0x001DA0F0, 0x008F4438, 0x0018A330, 0x001DA610, 0x001DA290, 0x001D9FD0, 0x001D9A40, 0x001D9EC0, 0x001D9DA0, 0x001DA9E0, 0x001DA090, 0x0020C1A0, 0x001DAAC0, 0x001DADC0, 0x009005E8, 0x0019EB60, 0x0019E7B0, 0x0019EF20, 0x001A0BB0, 0x001A07B0, 0x001A0F80, 0x001A7A50, 0x001B44A0, 0x001BB2B0, 0x001BE730, 0x0020C300, 0x001DAD60, 0x001D9400, 0x001D9930, 0x001D99C0, 0x001DA970, 0x0019EF40, 0x0019DA30, 0x0019E740, 0x0019EE50, 0x0063DA50, 0x00677CE0, 0x001B14E0, 0x001B07A0, 0x001B1800, 0x002E98F0, 0x0017F000 |

## What the player sees

Shorter loading. At start-up, on entering a map and before an event, a background worker reads the
next scene's files into the RAM file cache while the game is idle, so they are in memory when the scene
asks for them. Separately, every character, weapon, monster, map and font in the remastered art is
assembled from a `.ah` list of its parts; a part the list does not name is never loaded. The few
menu textures that are not part of a picture, such as the target lines, come from one more list.

The list read on entering a map is named after that map's zone script file. The lists read for events are the ones the
`eventlist.csv` records name for the current story progress, and the worker reloads them whenever that progress
changes.

## Where it comes from

Both are plain text in the archive. Prefetch manifests live under `prefetchdata/<language>/`
(`common.txt`, `eventlist.csv`, `maps/<map>.txt`, `events/<n>.txt`) and `prefetchdata/add-on/`. The
`.ah` lists sit beside their assets under `gamedata/d3d11/artdata/` as `<asset>_d3d11.ah`, with a
`_d3d11_srm.ah` list beside many of them. The menu texture list is
`gamedata/d3d11/artdata/menu/texlist.txt`.

Binding a PS2-era model also queues its remastered parts: the game turns the model's PS2 file path into a character
name and requests the `.ah` list of that name and its shadow list. Each line of a list names a `.phyre` file, and the
game loads every one.

## Layouts

A manifest is text, so it has no byte order.

| File | Unit | Separator | Comments | Header, count or version |
|---|---|---|---|---|
| prefetch manifest | a file name | whitespace; the reader steps by the name's length plus 2, so each name starts its line and ends with CRLF (`0x001DA15E`) | a token beginning `##` is dropped | no header; the shipped `##Total_data_Size:_361_MB` is a comment |
| `eventlist.csv` | a record of four integers | commas within a record | a line beginning `##` is skipped | no header |
| `.ah` list | a path such as `/GameData/D3D11/ArtData/chr/...phyre`, in load order | whitespace; the parser steps by the path's length plus 2, so each path starts its line and ends with CRLF (`0x0019E82F`) | no comments | no header |
| `TexList.txt` | a texture file name, relative to `GameData/D3D11/ArtData/menu/` | CRLF line ends | no comments | no header |

A prefetch manifest is whitespace-separated tokens, each a file name. The reader steps from one scan start
to the next by the token's length plus 2, so a name works only at the start of its line and followed by CRLF
(Loader behaviour). A token beginning `##` is a
comment and is dropped; the shipped header `##Total_data_Size:_361_MB` is written with underscores so
that it stays one token. `eventlist.csv` is records of four comma-separated integers, with `##`
lines likewise skipped.

The game keeps two of a record's four integers. The second, stored as a 16-bit word, is the key the
story-progress word is compared with, and the third is the number `<n>` of the `events/<n>.txt` list the
record loads. The first and fourth are converted and then dropped: `0x001D9C86` scans all four, and the
8-byte record takes only the second and third¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001D9C90`-`0x001D9CAE` |

</details>

A `.ah` list is whitespace-separated tokens, each a path such as
`/GameData/D3D11/ArtData/chr/...phyre`, in load order, with no comment convention, header, count or
version.

`TexList.txt` is one texture file name per line, relative to `GameData/D3D11/ArtData/menu/`, each line
ending in CRLF.

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| prefetch entries | 9,351 files, 283,340,853 bytes |
| languages | `us` 1,040, `fr` 1,040, `it` 1,040, `es` 1,040, `de` 1,042, `jp` 1,039, `kr` 1,036, `cn` 1,036, `ch` 1,036 |
| per language (US) | `common.txt` 1, `eventlist.csv` 1, `maps/` 709, `events/` 329 |
| `maps/` lists the game can request | the 709 names the kind 5 arrays give, the same in every language's array; every language folder ships those 709, and `de` also ships `mic_b03.txt` and `rui_b04.txt`, which no map number names |
| `events/` lists the game can request | 236 per language, the distinct third integers of its 315 `eventlist.csv` records, each with a shipped list; named by no record: 93 in `us`, `de`, `es`, `fr` and `it`, 92 in `jp`, 89 in `kr`, `ch` and `cn`; `add-on/events/250.txt` is named by a record in every language |
| outside the language folders | `prefetchdata/add-on/events/250.txt`, `prefetchdata/ff12mapjump_custom_nocrystal.csv` |
| prefetch `.txt` files | 579 begin with a `##Total_data_Size:_…` token, no list with a spaced header; 3,506,346 name tokens in all |
| `.ah` files | 2,564, 12,235,216 bytes, all CRLF; 2,559 begin `/Gam`, 5 (the font lists) `font` |
| `.ah` tokens | 142,481, of which 62 (in the five font lists) are not paths |
| `texlist.txt` | 301 bytes, 11 CRLF lines, each a `.dds.phyre` name that exists under `gamedata/d3d11/artdata/menu/` (`targetline_p`, its six `_clut_` variants, `chain_item`, `chainflash`, and `w_line01` with its `_clut_1`); one row per name in [`prefetch-manifests-texlist-rows.tsv`](prefetch-manifests-texlist-rows.tsv) |
| `.ah` groups | `chr/weapon` 308, `chr/monster` 258, `chr_shadow/monster` 249, `chr/npc` 172, `chr_shadow/npc` 171, `chr/high` 134, `chr_shadow/high` 130, `chr/gadget` 103; 457 `_srm` lists |
| `.ah` targets | 95,076 path tokens name a shipped file; 47,343 name a map texture path that `shared/phyremaps.txt` maps to a shipped file under `shared/map/`; the 62 font tokens each name a font whose files sit beside the list |

Every token of every `.ah` list, one row each, in list order:

| table | rows | lists |
|---|---:|---|
| [`prefetch-manifests-ah-tokens-map.tsv`](prefetch-manifests-ah-tokens-map.tsv) | 128,268 | the 914 map lists |
| [`prefetch-manifests-ah-tokens-chr.tsv`](prefetch-manifests-ah-tokens-chr.tsv) | 11,802 | the 1,057 `chr/` lists |
| [`prefetch-manifests-ah-tokens-chr_shadow.tsv`](prefetch-manifests-ah-tokens-chr_shadow.tsv) | 2,349 | the 588 `chr_shadow/` lists |
| [`prefetch-manifests-ah-tokens-font.tsv`](prefetch-manifests-ah-tokens-font.tsv) | 62 | the five `fontlist.ah` |

| Column | Meaning |
|---|---|
| `list` | the `.ah` file's path in the archive |
| `position` | the token's place in the list, from 0 |
| `token` | the token as written |
| `target` | `file` when the path names a shipped file; `phyremaps` when `shared/phyremaps.txt` maps it to a shipped file; `font name` for a font list's token |
| `resolved_to` | for `phyremaps`, the shipped shared file; for a font name, the files of that name beside the list |

Every `chr/` and `chr_shadow/` list with the character name that builds it (see Asset-header lists):

| table | rows | lists |
|---|---:|---|
| [`prefetch-manifests-ah-lists-chr.tsv`](prefetch-manifests-ah-lists-chr.tsv) | 1,057 | the `chr/` lists: 1,050 built from a model's path, 6 of them also from `init.json`; `global/MaterialSphere/MaterialSphere` for model id −1; 6 named by no model path |
| [`prefetch-manifests-ah-lists-chr_shadow.tsv`](prefetch-manifests-ah-lists-chr_shadow.tsv) | 588 | the `chr_shadow/` lists: 586 built from a model's path, 6 of them also from `init.json`; 2 named by no model path |

| Column | Meaning |
|---|---|
| `list` | the `.ah` file's path in the archive |
| `bytes`, `sha256` | the file's size and SHA-256 |
| `model` | the character name that builds the list's path; `-` when no model path builds it |
| `bound_ids` | the bound ids whose model path gives that name ([Model asset list](../Graphics/model-asset-list.md)) |
| `named_by` | the model path, `init.json` `ModelsToPreload`, model id −1, or `named by no model path` |
| `requested` | when the game files the list: when that model binds, and at start-up for the six `ModelsToPreload` names; `-` for a list no model path names |

- No model's path builds the six `chr/` lists `high/n10/n1021/hn1021_01`, `high/n10/n1081/hn1081_01` and the `mws/` lists of `m1022`, `m1025`, `m1084` and `m1085`, or the `chr_shadow/` lists of `hn1021_01` and `hn1081_01`: no entry of the US path arrays ([Asset paths](asset-paths.md)) and no language's sized entry in the size tables is `hn1021_01.cm` or `hn1081_01.cm`.
- Each of the four `mws/` lists names the same files as its model's own list (`chr/monster/m10/m1022/m1022_D3D11.ah` for `m1022`), which the model's binding requests.
- Model paths build 34 `chr/` and 498 `chr_shadow/` list names that the archive does not ship, among them 19 weapons and 8 `high/` models for `chr/`. Such a request completes with no entries (Asset-header list records).
- Every `chr_shadow/` list names its mesh and exactly the files that mesh imports (588 of 588). Of the `chr/` lists, 57 name their mesh and exactly its imports, 886 add only the `_n` and `_spec` files or other palettes of textures the mesh imports, and 114 also name textures their mesh does not import ([PhyreEngine asset files](../PhyreEngine/phyre-asset-files.md) `imports`).

Every prefetch list, every name it holds and every entry, in three kinds of table:

- The 9,351 files hold 7,912 different contents; a file with the same bytes as an earlier one points to it and has
  no entry rows of its own.
- The nine `common.txt` hold four more lines starting `##`: `##PhyreShader`, `##UI`, `##JSON` and `##OTHERS`, at lines
  1, 25, 34 and 873; `section_lines` gives them.
- Of the 61,235 different names, 61,119 name a shipped file as the archive lookup reads them (it skips leading
  `.`, `/` and `\`, turns `\` into `/` and lower-cases the rest, `0x0059F114`-`0x0059F185`), and 31 name one only
  once their doubled slashes are removed.
- 85 names name no file in the archive: 44 `_GNM.ta` animation names under `map/`, 15 `chr`, `chr_shadow` and `map`
  model and texture files, 12 `JsonData/CutScenes` files, 6 under `shared/map/`, 5 under `shaders/`, 2 under
  `effect_finish/uk/event/`, and `PS2Data/oldsave/new077`, which 5,823 lists name.

| table | rows | one row per |
|---|---:|---|
| [`prefetch-manifests-lists.tsv`](prefetch-manifests-lists.tsv) | 9,351 | file under `prefetchdata/`: `maps` 6,383, `events` 2,949, `common.txt` 9, `eventlist.csv` 9, `ff12mapjump_custom_nocrystal.csv` 1 |
| [`prefetch-manifests-lists-reached.tsv`](prefetch-manifests-lists-reached.tsv) | 9,332 | `maps/` and `events/` list: whether the game can request it, and the map numbers or `eventlist.csv` records that name it (Loader behaviour) |
| [`prefetch-manifests-names.tsv`](prefetch-manifests-names.tsv) | 61,235 | different name |
| [`prefetch-manifests-entries-us.tsv`](prefetch-manifests-entries-us.tsv) | 355,723 | entry of a `us` list with its own bytes |
| [`prefetch-manifests-entries-fr.tsv`](prefetch-manifests-entries-fr.tsv) | 355,826 | the same for `fr` |
| [`prefetch-manifests-entries-de.tsv`](prefetch-manifests-entries-de.tsv) | 355,658 | `de` |
| [`prefetch-manifests-entries-it.tsv`](prefetch-manifests-entries-it.tsv) | 356,005 | `it` |
| [`prefetch-manifests-entries-es.tsv`](prefetch-manifests-entries-es.tsv) | 355,739 | `es` |
| [`prefetch-manifests-entries-jp.tsv`](prefetch-manifests-entries-jp.tsv) | 351,880 | `jp` |
| [`prefetch-manifests-entries-kr.tsv`](prefetch-manifests-entries-kr.tsv) | 337,966 | `kr` |
| [`prefetch-manifests-entries-cn.tsv`](prefetch-manifests-entries-cn.tsv) | 337,989 | `cn` |
| [`prefetch-manifests-entries-ch.tsv`](prefetch-manifests-entries-ch.tsv) | 338,862 | `ch` |
| [`prefetch-manifests-entries-add-on.tsv`](prefetch-manifests-entries-add-on.tsv) | 31 | entry of `add-on/events/250.txt` |

| Column | Meaning |
|---|---|
| `list` | the list's number, its row in [`prefetch-manifests-lists.tsv`](prefetch-manifests-lists.tsv) |
| `path`, `language`, `part` | the file, its language folder (`-` for the file outside them), and its folder or file name within it |
| `bytes`, `sha256` | the file's size and SHA-256 |
| `size_token` | the list's `##Total_data_Size:_` token, which the parser drops; empty when the list has no such token |
| `names` | the list's entries |
| `same_bytes_as` | the earlier list with the same bytes, whose entries this one has |
| `section_lines` | the list's lines starting `##` other than the `##Total_data_Size` token, each with its line number; `-` when it has none |
| `name`, `text` | the name's number and the name as written |
| `lists` | the lists that name it |
| `target` | `file`; `file once doubled slashes and ./ are removed`; or `no shipped file` |
| `position` | the entry's place in its list, from 0, `##` tokens not counted |

</details>

## Loader behaviour

### Prefetch manifests

- **Parsing.** `0x001DA0F0` scans tokens with `"%s"` (`0x008F4438`, through `0x0018A330`) until a scan fails,
  frees any token whose first two bytes are `##`, and appends the rest to a list. Nothing reads the
  size header. Each token is scanned into a 256-byte block of its own, without a bound¹.
- **Stepping.** Like the `.ah` parser, `0x001DA0F0` steps the text by the token's length plus 2 from the scan start
 ², and it also stops once those steps add up to the text's length³. It answers 0 for a null text⁴ and 1 otherwise.
- **The shipped lists.** Each of the 9,341 shipped prefetch `.txt` lists starts every name at a line start and
  ends it with CRLF, so the steps land on each next name. 3,126 of them end in further whitespace, where the
  next scan fails and the list ends.
- **The worker thread.** `0x001DAAC0` sets the manager's `+0x20` to 1, starts the thread through `0x005CD1E0` with
  the entry `0x001DADB0`, a jump to `0x001DADC0`, a stack of `0xF000` bytes, the priority selector 3 and the name,
  and then sets `+0x18` to 1
 ⁵.
- **Start-up.** The prefetch worker `0x001DADC0` (started by `0x001DAAC0`, the only user of the name
  `FileCachePrefetchManager`) first calls `0x001DA610`: with the RAM cache on, it reads
  `/PrefetchData/<language>/common.txt`, parses it, and opens every name with selector 5, closing the
  stream at once. It then reads `eventList.csv`⁶, keeping records whose four fields all
  convert.
- **Map entry.** `0x001DA290`, which `0x002EF910` reaches through `0x001D6C80`, (when the cache is on, the byte
  `0x01F83441` is 0, and the map number changed and is not negative) builds
  `/PrefetchData/<language>/Maps/<map>.txt` and files it as a whole-text request; its completion `0x001D9FD0`
  parses the tokens into the map list.
- **The map list's completion.** Under the lock `+0x38`, `0x001D9FD0` first empties the map list of the previous
  map's names, logging `[FileCache] Prefetch On Enter Map End`⁷, and then parses the text
  into it⁸. With names in the list it clears the empty byte `+0x78`; with the list empty it
  logs the same line⁹. It then frees the text and zeroes `+0x30`¹⁰.
- **The map list's name.** `<map>` is the file name, less folder and extension, of the map's zone script:
  `0x0032F170(0, map)` gives kind 5 and id 3 × map¹¹, `0x002DF980` returns that entry of
  the language's kind 5 array as it stands¹², and `0x001DA3BD`-`0x001DA47A` take the text
  between its last `\` and its last `.`. The map aliases of `0x01EF9490` play no part on this path.
- **Events.** `0x001D9EC0` walks the records in key order against the manager's word `+0xE8`, the
  story-progress value it last stored. Records keyed with that value load unless `+0x1BC` already holds it.
- **An event's lists.** Under the lock `+0xF0`, `0x001D9DA0(manager, n)` logs `[FileCache] LoadEventFileList : event
  %d` and loads two lists into the event list through `0x001DA9E0`. Both names come from `"%s%s%s%d%s"`¹³:
  `/PrefetchData/<language>/Events/<n>.txt` and `/PrefetchData//add-on//Events/<n>.txt`¹⁴.
- **The add-on name.** The archive lookup keeps the doubled slashes¹⁵. The shipped
  archive's index holds the digest of `prefetchdata/add-on/events/250.txt` but not that of
  `prefetchdata//add-on//events/250.txt`, so in the shipped game the add-on list never opens, for 250 as for
  every other number.
- **The next key.** Of the keys above that value, the lowest key's records load and that key is stored at
  `+0x1BC`; when the lowest key already equalled `+0x1BC`, the next key's records load as well and that key
  is stored instead¹⁶.
- **Story progress 0.** `0x001DA220`, which the title asset's factory `0x00394460` reaches through `0x001D6C60`,
  stores 0 at `+0xE8` when the cache is on, `0x01F83441` is 0 and the story-progress word is 0, empties the
  event list and runs the same walk¹⁷, so the records keyed 0 and the lowest key
  above 0 load there.
- **Map jumps.** `0x001DA090(map)` records the new and previous map numbers and writes them into the
  cache's protected words (`0x0020C1A0`: `+0x80` = new, `+0x84` = previous).
- `0x001DA090` ignores a negative map number¹⁸. Otherwise it sets the manager's byte `+0x88`
 ¹⁹, the byte `0x001D6B70` reads for the cache's backfill. Only for a map other than `+0x7C` does it move
  `+0x7C` to `+0x80`, store the new number at `+0x7C`, call `0x0020C1A0` and log `[FileCache] OnMapJumpBefore (%d)`
 ²⁰.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001DA129` |
| ² | `0x001DA15E`-`0x001DA162` |
| ³ | `0x001DA179`-`0x001DA183`, `0x001DA120` |
| ⁴ | `0x001DA103` |
| ⁵ | `0x001DAAC9`-`0x001DAB26` |
| ⁶ | `0x001D9A40` |
| ⁷ | `0x001DA004`-`0x001DA01E` |
| ⁸ | `0x001DA0F0`, `0x001DA02D` |
| ⁹ | `0x001DA032`-`0x001DA04B` |
| ¹⁰ | `0x001DA058`-`0x001DA06B` |
| ¹¹ | `0x0032F19E`-`0x0032F1A8` |
| ¹² | `0x002DF98D`-`0x002DF991` |
| ¹³ | `0x00900798` |
| ¹⁴ | `0x001D9E31`, `0x001D9E6B` |
| ¹⁵ | `0x0059F114`-`0x0059F185` |
| ¹⁶ | `0x001D9EF1`-`0x001D9F4F` |
| ¹⁷ | `0x001DA229`-`0x001DA276` |
| ¹⁸ | `0x001DA092` |
| ¹⁹ | `0x001DA0A3` |
| ²⁰ | `0x001DA0AD`-`0x001DA0DC` |

</details>

The worker then loops while running: it stops when `0x01F83441` is set; it sleeps 100 ms while requests
are pending or too little time has passed since the last activity, or when both lists are empty;
otherwise it sleeps 10 ms and opens one name, first from the event list (selector 3) and, when that is
empty, from the map list (selector 4), closing the stream at once.

When a file is missing:

- **A name that opens no file.** The worker takes the name off its list before opening it, does not
  test the open, and frees the name¹, so the
  name is not tried again.
- **The open's log.** When neither the RAM cache's name map² nor any of up
  to five archives³ holds the name, the open logs
  `[FFXII_ERROR] Big file open failed %s` with the name and returns 10⁴.
- **A map list that does not open.** The whole-text request stores 0 as the text⁵
  and `0x001D9FD0` returns without touching the map list⁶, so names left from the
  previous map stay queued.
- **A map number whose kind 5 entry is 0.** `0x001DA290` measures the returned path with no null test
 ⁷, so it reads address 0.
- **An event list that does not open**, in the language folder or in `add-on`, adds no name
 ⁸; the other of the two still loads. The add-on name never opens (Events, above), so
  for every number the add-on open fails and logs as above.
- `0x001DA9E0` opens with selector 0⁹, so the RAM cache is not tried. A list of 0 bytes, or one whose
  block cannot be allocated, adds no name either¹⁰. A parse that leaves names in the event
  list clears its empty byte `+0x130`¹¹; the block is then freed¹².
- **A story-progress value no record is keyed with.** The walk skips the records keyed below it and
  loads the keys above it as described; above the highest key the event list stays empty.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001DAEE3`-`0x001DAF0F`, `0x001DAF89`, `0x001DAFCC`-`0x001DAFEB` |
| ² | `0x0020C242`-`0x0020C2C7` |
| ³ | `0x0019AF85`-`0x0019AFA8` |
| ⁴ | `0x0059F1C0`-`0x0059F1D1` |
| ⁵ | `0x001A0FB4`-`0x001A0FC4` |
| ⁶ | `0x001D9FE6`-`0x001D9FEB` |
| ⁷ | `0x001DA342`-`0x001DA34C` |
| ⁸ | `0x001DAA10`-`0x001DAA28` |
| ⁹ | `0x001DA9FE` |
| ¹⁰ | `0x001DAA28`, `0x001DAA41` |
| ¹¹ | `0x001DAA6F`-`0x001DAA78` |
| ¹² | `0x0019C590` |

</details>

### The prefetch manager

`0x001DAD60` builds the manager once, `0x1C0` bytes at `0x01F82CF0`, with `0x001D9400`; with a null block it skips the
constructor and stores the null¹. The constructor sets up
the lists and their locks, stores itself as the file cache's owner (`[0x0020C700()] + 0x18`, so the
cache's group word `+0xE8` is the manager's), and picks the language folder from `0x0017E270()`: 0 and
10 give `jp`, 2 `fr`, 3 `de`, 4 `it`, 5 `es`, 7 `kr`, 8 `ch`, 11 `cn`, and any other value `us`. The
paths are built by inserting that code and `/PrefetchData/` in front of the file name².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001DAD89` |
| ² | `0x001DAB30` |

</details>

- `0x001D9A40` keeps each `eventList.csv` record as an 8-byte pair in the list `+0xD0`, the second integer as
  a word at `+0` and the third as a dword at `+4`¹, and then sorts the list by that
  word, ascending (`0x001D9200`, a merge sort that merges with `0x001D9150`).
- The map list's completion is the stub `0x001D9920`, which passes the manager to `0x001D9FD0`.
- `0x001D99C0` empties the map list `+0x60` and `0x001D9930` the event list `+0x118`, freeing each name;
  each sets its list's empty byte (`+0x78`, `+0x130`). `0x001D9D80` is true when both are set.
- A list that is already empty is left as it is: the function returns before the byte store². Each frees the names³ and then the 24-byte nodes through the list's allocator.
- `0x001DA970`, called on each pass of the worker that gets past the busy test (`+0x24` and `+0x28` both 0,
  `0x001DAE25`-`0x001DAE35`) and the time test⁴, reloads the event list when the story-progress word
 ⁵ is positive and differs from `+0xE8`: it stores the value, empties the list under its lock
  `+0xF0` and runs `0x001D9EC0`. It does nothing while the RAM cache is off⁶.
- The worker takes the map list's first name with `0x001DAD30` and logs
  `[FileCache] Prefetch On Enter Map End` when that empties the list.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001D9C90`-`0x001D9CAE` |
| ² | `0x001D99D4`, `0x001D9947` |
| ³ | `0x00210EB0` |
| ⁴ | `0x001DAE5A` |
| ⁵ | `0x00265270` |
| ⁶ | `0x001D6B20`, `0x001DA980` |

</details>

The two busy counters `+0x24` and `+0x28` and the activity time `+0x8C` are what the worker tests
before opening a name. The asynchronous loader raises counter `+0x24` around every load it runs¹ and lowers it afterwards², which also stamps the time.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001D9F70` |
| ² | `0x001D9F90` |

</details>

Opening a name is what loads it. In the resolver a name that passes the cache's name filter is read
whole into the RAM cache when it misses, and the hit or new entry is stamped by its selector, a hit by
`0x0020C300` and a new entry by `0x0020B680`, which takes the selector as the entry's kind: selector 5 makes
it kind 5, which eviction never frees; selector 3 stamps its group word;
selector 4 stamps the current map number.

Eviction¹ first frees only entries of neither the current map (`+0x80`) nor the previous one
(`+0x84`); when that frees too little it calls `0x0020B840` with its third argument 1², which keeps
only the current map's entries³. Both passes keep kind 5 entries and entries whose
group word is the manager's `+0xE8`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020BFA0` |
| ² | `0x0020C0EF` |
| ³ | `0x0020B8D3`-`0x0020B8E6` |
| ⁴ | `0x0020C02E`-`0x0020C04C`, `0x0020B89E`-`0x0020B8C1` |

</details>

A name the filter rejects is opened and closed and not cached. The filter¹ tests single
characters, not a suffix: it rejects a name of 4 characters or fewer, or one with `.` 4th or 5th from the end,
`w` 4th from the end, `m` or `e` 3rd from the end, `a` or `b` 2nd from the end, or `b` or `m` last, so `.ah`
and `.cm` names are not cached either. The manifests are advisory: a file no manifest names still opens
normally.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0059EF4B`-`0x0059EFA9` |

</details>

### Asset-header lists

`0x0019EB60(manager, path)` files a `.ah` as a whole-text request whose completion `0x0019EF20` jumps to
the parser `0x0019E7B0`. It takes a list record (`0x001BA860` on `+0x08`), empties its entries, clears its done byte
`+0x128` and text `+0x120`, and copies the path to `+0x00`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0019EB81`-`0x0019EBBD` |

</details>

Its request is kind 4 with the list record as argument, the byte `+0x18` set to 1 and the text slot `+0x120` as
result¹, filed at the head of the queue². It returns the list record.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0019EBCF`-`0x0019EBFF` |
| ² | `0x001A0BB0`, `0x0019EC14` |

</details>

A text with no token makes no entry and files no request, so the parser leaves the done byte `+0x128` at the 0
that `0x0019EB60` stored¹, and no entry completion reaches `0x0019E740` to queue `0x0019EE50`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0019E8F5` |

</details>

The parser returns at once for a null list record¹; otherwise it:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0019E7B3` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | scans tokens with `"%s"` into a 256-byte stack buffer, without a bound, and steps the text by the token's length plus 2 from the scan start, so lines must end in CRLF with no leading whitespace; it stops when a scan fails; | `0x0019E817` |
| 2 | makes an entry per token, with its position in the list as a `u16` at `+0`, a done byte at `+2` and the name from `+3`, `+0x108` zeroed and the list record at `+0x110`; there is no `##` filter, so every token is taken as a path; | `0x0019E852`-`0x0019E894` |
| 3 | frees the text and, from the last entry to the first, files a load request (kind 1) for each name, prefixed with `.` when it does not start with one, whose result goes to the entry's `+0x108`; |   |
| 4 | clears each entry's done byte before that entry's request, which points at it. | `0x0019E92B`, `0x0019E995` |

The lists are built from these patterns: map `.\GameData\%s\ArtData\map\%s\%s_%s.ah` and its `_srm`
form¹; character `./GameData/%s/ArtData/chr/%s_%s.ah` and the flat and grouped `chr_shadow`
forms²; procedural textures `./GameData/%s/ArtData/map/proceduralTexture/proceduralTexture_%s.ah`³; and five literal font lists `./GameData/D3D11/ArtData/font/<jp|us|ch|cn|kr>/fontlist.ah`⁴. The varying `%s` is always `D3D11`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001A7A50` |
| ² | `0x001BB2B0` |
| ³ | `0x001BE730` |
| ⁴ | `0x001B44A0` |

</details>

`0x001A7A50` requests the `_srm` form when `0x0019EAA0` can open it and the plain form otherwise (`0x001A7C14`-`0x001A7C53`;
[Map art](../World-Areas-And-Travel/map-art.md)). `0x001BE730`, the procedural-texture context's constructor, keeps the
list record `0x0019EB60` returns at `+0x00`¹ and writes
`/ArtData/map/ProceduralTexture/proceduralTextureConfigs.txt` at `+0xB4`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BE87B` |
| ² | `0x001BE891` |

</details>

`0x001BB2B0` takes a character's name from its PS2 model path: `0x002E98F0` turns the model id into a kind
and index (`0x002ED6F0`, adding `0x33` to the index for kind 1), `0x002DF980` returns that path, and the
text after `PS2Data\obj_finish\in\`, less its last three characters (`.cm`), with `\` turned into
`/`, is the name. Model id −1 uses `global/MaterialSphere/MaterialSphere` (`0x008F91E0`, copied at `0x001BB3DC`).

With that name N, `0x001BB2B0` files two lists through `0x0019EB60`: `./GameData/D3D11/ArtData/chr/N_D3D11.ah`¹ and, for a model id of 0 or more², a shadow list³. When N starts with `h`
the shadow list is `chr_shadow/N_D3D11.ah`⁴; otherwise it is
`chr_shadow/<N less its last 11 characters><S>/<S>_D3D11.ah`⁵, S being N's last five characters.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BB7D9` |
| ² | `0x001BB7E8` |
| ³ | `0x001BB8B9` |
| ⁴ | `0x008F9180` |
| ⁵ | `0x008F91B0` |

</details>

The model's record holds the `chr` list and a mark that a shadow list exists¹; the
shadow list gets its own record, filed under −2 − id². `0x001BB040` reports a model's
lists loaded only when the shadow record, for a marked model, and then the model's own record are done³. At start-up `0x001C3760` hands each `init.json` `ModelsToPreload` name to `0x001BB920`,
which files the same two lists for that name⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BB7E1`, `0x001BB894` |
| ² | `0x001BB8C9`-`0x001BB8E2` |
| ³ | `0x001BB09F`-`0x001BB10E` |
| ⁴ | `0x001BB9C6`, `0x001BBAF1` |

</details>

`0x0017F000(id)` asks the object at `0x01F81240` (`0x001BC000`, null before it exists) for a model's list
record through `0x001BB2B0` and returns it. While the object is null it requests nothing and returns 0¹. The binding's load `0x002EAD50` calls it before it files the
model's own file and ignores the result, so binding a character model also queues its `.ah` lists.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0017F010` |

</details>

### Asset-header list records

The lists live in the `AssetListManager` that `0x0019EF40` builds once (`0x188` bytes at `0x01F81158`, `0x0019DA30`): a pool
of 192 list records of `0x130` bytes at `+0x08`¹ and a pool of 3,072 entry records of `0x118` bytes at
`+0xC8`², each pool with its own lock. The constructor passes the flag 1 to both pools³, which is what creates the locks; it also stores the vtable `0x008F4430` (RTTI `AssetListManager`,
`0x0019DA4D`) and returns the manager⁴. With a null block `0x0019EF40` skips the constructor and stores the
null⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0019D5B0` |
| ² | `0x0019D740` |
| ³ | `0x0019DA54`, `0x0019DA69` |
| ⁴ | `0x0019DA77` |
| ⁵ | `0x0019EF69` |

</details>

`0x0019EB60` takes a list record and the parser takes one entry record per token¹ and writes to it without a
test, so the 3,072 entry records bound every list loaded at once. `0x0019EB60` writes to its list record without a
test too², so the 192 list records bound the lists held at once.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001BA860` |
| ² | `0x0019EB9B` |

</details>

- The text is read as a kind 4 request whose completion, `0x0019EF20`, runs on the loading thread, so
  the parse does too.
- The parser files its entry requests at the tail of the queue¹ from the last entry to
  the first, so the entries load in list order ahead of anything already waiting.
- Each entry's request (kind 1) completes in the frame pump through `0x0019EF00`, which passes the
  manager and the entry to `0x0019E740`.
- When the entry is the list's last (`u16 +0` equals the count less one), `0x0019E740` queues a job
  `{0x0019EE50, list}` on the second `AsyncJobManager` (`0x01F81100`, through `0x00199F10` and `0x0019A000`). An entry
  whose list record `+0x110` is null queues nothing².
- `0x0019EE50` runs `0x0063DA50` and then `0x0063B010` on each entry's loaded cluster and sets the list's
  done byte `+0x128`. `0x00796350` runs the same two passes over an array of clusters.
- `0x0063DA50` walks the cluster chain (`+0x98`), skipping a cluster whose `+0x80` bit `0x1` is set,
  hands every `PAssetReferenceImport` object (descriptor `0x02D3E780`) to `0x00677CE0`, and sets that bit.
  `0x0063B010` runs `0x0063B040` on each cluster of the chain until one returns non-zero.
- In a cluster, `0x0063DA50` takes each node of the list at `+0x38` whose type `+0x50` is `0x02D3E780` or reaches it
  through the types' `+0x78` links and whose count `+0x74` is above 0³.
  It visits that many objects from `+0x60`, `[type + 0x38]` bytes apart, skipping each slot that is the next entry
  of the node's `+0x10` chain⁴.
- It passes object + `[type + 0xF8]` to `0x00677CE0`⁵. It sets the bit on a cluster with no
  import too⁶, and returns 0, at once for a null chain⁷.
- `0x00677CE0` looks the import's name up among the registered assets⁸. A miss logs
  `Failed to find asset %s of type %s, using fallback` and takes the type's fallback⁹; a
  hit of another type logs `Found asset %s of wrong type, wanted %s, got %s`. Every pointer chained to
  the import is then set to the asset.
- An import whose chain `+0x10` is null returns 0 with no lookup¹⁰. The name is `+0x08` with bit `0x1`
  cleared and the wanted type is `+0x00`; a hit counts as the wanted type when its type `+0x40` is that type or
  reaches it through `+0x78`¹¹, and a hit of another type still gives its asset `+0x38`. Both
  messages go to `0x005CDAA0` with level 2.
- The value stored is the asset or fallback less the wanted type's i32 `+0xF4`¹². Each
  pointer's old value names the next one¹³; `+0x10` is then zeroed¹⁴ and it
  returns 0.
- A token whose file does not open leaves its entry's cluster null: `0x0019CB20` returns 0 when `0x00637C50`
  fails¹⁵, the kind 1 request stores that 0 and still sets the done byte
 ¹⁶, and both passes of `0x0019EE50` return at once for a null cluster¹⁷, so the list is still marked done. An import elsewhere that names an asset of that file takes
  the type's fallback as above.
- A list file that does not open leaves the list record's text null: the kind 4 request stores 0 when the
  open fails¹⁸, and the parser then empties the list's entries and sets its done byte
 ¹⁹, so the list completes with no entries.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001A0C50` |
| ² | `0x0019E750` |
| ³ | `0x0063DAB6`-`0x0063DADD`, `0x0063DB82`-`0x0063DBA4` |
| ⁴ | `0x0063DB15`-`0x0063DB29`, `0x0063DB4B`-`0x0063DB59` |
| ⁵ | `0x0063DB30`-`0x0063DB36` |
| ⁶ | `0x0063DBEB` |
| ⁷ | `0x0063DA5C`, `0x0063DC26` |
| ⁸ | `0x00676BD0` |
| ⁹ | `0x0063BC00` |
| ¹⁰ | `0x00677CF4` |
| ¹¹ | `0x00677D50`-`0x00677D6C` |
| ¹² | `0x00677D9E`-`0x00677DB2` |
| ¹³ | `0x00677DC0`-`0x00677DCC` |
| ¹⁴ | `0x00677DCE` |
| ¹⁵ | `0x0019CC20`-`0x0019CC36` |
| ¹⁶ | `0x001A0822`-`0x001A083D` |
| ¹⁷ | `0x0063DA5C`, `0x0063B019` |
| ¹⁸ | `0x001A0FB4`-`0x001A0FC4` |
| ¹⁹ | `0x0019E7EC`, `0x0019EA03`-`0x0019EA11` |

</details>

The pools' record vectors are sized with `0x0019EC40` (list records: grow with `0x0019E010`, shrink with
`0x0019EA20`) and `0x0019ED80` (entry records: grow with `0x0019E2C0`); `0x0019DF90` frees the entry vectors of a
range of list records, and `0x0019DCC0` the list pool.

### The menu texture list

At start-up `0x001B1630` (through `0x001B1580`) calls `0x001B1750` on the menu sprite batcher¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01F811E8` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x001B14E0` opens `GameData/D3D11/ArtData/menu/TexList.txt`, reads it whole into a zero-terminated block and closes it; when it does not open it logs `UI TextureList load failed!` and the list stays empty. It frees the block after step 2. | `0x001D6F20`<br>`0x001D6E80`<br>`0x001B157A` |
| 2 | `0x001B07A0` splits the text at each LF, up to 1,024 lines, drops the line's last character (the CR), and stores `./GameData/D3D11/ArtData/menu/` plus the rest (`"%s%s"`, `0x008F80F0`) as a string in the batcher's vector `+0x00` (`0x001AB6B0` grows it). |   |
| 3 | For each string, in order, `0x001B1800` files a kind 1 load at the head of the queue with the completion `0x001B1C10` and the result slot `batcher + 0x108 + 8 × i`; an empty line files nothing. |   |

A line of 128 characters or more before its CR stops the game (`__report_rangecheckfailure`). So does a
line with no character before its LF, as the length less one is compared unsigned¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B0830`-`0x001B0850` |

</details>

The request `0x001B1800` files takes the vector's string `i` as its argument¹ and has no
done byte². The string becomes the request's path as the format of `0x001A1E40`³, so a `%`
in a name is read as a conversion.
`0x001B1C10` registers each loaded texture under the hash of its lower-cased path in the batcher's tree
`+0x28`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B1881`-`0x001B188B` |
| ² | `0x001B18A9` |
| ³ | `0x001B18B7` |

</details>

A draw names a texture and a palette number. The sprite batcher looks up the plain name for 0 and
`<name>_clut_<n>` (`%s_clut_%d`, `0x008F8118`) for any other n: `0x001B0A20`¹, reached
through `0x00181390`, and `0x00215F80`², the record method that `0x00215E50` picks for a
record `0x001B2410` filled with `+0x110` and `+0x118` at 0, as `0x00181930` fills it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B0A6D`-`0x001B0A90` |
| ² | `0x00215FC2`-`0x00215FD4` |

</details>

`0x001819A0` sets `+0x110`¹, so its record takes `0x00216020`, which looks the name up with no suffix². A name the
tree does not hold draws nothing ([Sprite batcher](../Graphics/sprite-batcher.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001819DD` |
| ² | `0x001B10D0` |

</details>

The code references to the two names (`targetline_p` at `0x009152A0` and the pointer `0x01E0C1E0`, `w_line01` at
`0x009159E8`) give these draws; the other references only register or look up the PS2 pictures of the same names¹, among them the name tables `0x00D231C0` (its pointer at `0x00D23220`, which `0x00562F90`
passes to `0x002493D0`) and `0x00D23270` (its pointer at `0x00D232C8`, which `0x00563110` passes to `0x0024A5A0`;
`0x00D232D0` is that table's end):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024A4E0`, `0x0024A5A0` |

</details>

| Draw | Texture | Palette number | Variant asked for |
|---|---|---|---|
| a target line, `0x003F5430` (`0x003F55E4`, `0x003F5A79`) | `targetline_p` | `0x002713B0` of the line's kind `+0x840`: 0, 1, 3 or 5 | plain, `_clut_1`, `_clut_3`, `_clut_5` |
| a `+0x10F40` mark, `0x003F3710` (`0x003F3860`) | `targetline_p` | `[0x02B5F1F4]`, the mark's `+0x48`, which `0x002911D0` sets from `0x002713B0` (`0x00291204`-`0x00291216`, `0x003F3660`): 0, 1, 3 or 5 | plain, `_clut_1`, `_clut_3`, `_clut_5` |
| a `+0x10F30` mark, `0x003F70F0` (`0x003F71A4`) | `targetline_p` | `+0x330` + 2 x `+0x32C`: 0 in the mark `0x00291010` zero-fills (`0x002910CB`), then `0x003F77F0` sets `+0x32C` to 0 and `+0x330` to 4 when `0x0030BEF0` answers above 0, else 1 (`0x003F78AC`-`0x003F78BF`) | plain, `_clut_1`, `_clut_4` |
| a target ring, `0x0028D980` (`0x0028DA24`) | `targetline_p` | `+0xD7C` + 2 x `+0xD78`: `+0xD78` = 0 and `+0xD7C` = the byte of `0x00916010` (`04 00 01 00`) for the ring style 0 to 3 (`0x0029189B`-`0x002918A1`; `0x0028C7EE`-`0x0028C7FB`) | plain, `_clut_1`, `_clut_4` |
| a world sprite of kind -2, `0x003F0610` (`0x003F1076`) | `targetline_p` | the sprite's `+0xEC`, which `0x003FBA80` sets to 4 for the part's `+0x26C` (`0x003FA659`) 2 or 3, else 3 (`0x003FBB94`-`0x003FBC4A`) | `_clut_3`, `_clut_4` |
| the World Map path, `0x005621A0` (`0x00562347`) and `0x00562A30` (`0x00562ADE`), through `0x001819A0` | `w_line01` | 0 (`0x00562354`, `0x00562AEB`) | plain |
| the widget line, `0x00274CB0` (`0x00274DC5`) | `w_line01` | 1 (`0x00274DA3`, `0x00274DC2`) | `_clut_1` |

So the draws ask for `targetline_p` and its `_clut_1`, `_clut_3`, `_clut_4` and `_clut_5`, and for `w_line01` and
`w_line01_clut_1`. `targetline_p_clut_2` and `targetline_p_clut_6` are loaded and registered at start-up, and
these draws ask for neither.

## Modding notes

- A prefetch name only speeds up loading; leaving a file out of every manifest still loads it, just
  later.
- Comment a prefetch manifest with `##`; a `.ah` has no comments, and a `#` line in it is requested as a
  file.
- In a `.ah`, end every line with CRLF, start no line with whitespace, and keep paths to 255
  characters or fewer.
- A part not named in its `.ah` is never loaded for that model.
- In `TexList.txt`, end every line with CRLF (the loader drops each line's last character), keep each
  name under 128 characters, and list at most 1,024 names.

## Related

- [File path resolution](file-path-resolution.md): the RAM cache, its name filter and the selector stamps.
- [Texture animation lists](texture-animation-lists-ta.md): the other list format read the same way.
- [Fonts](../Menus-And-HUD/fonts.md): the font list selection by language.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 35 calls with 7 other topics</summary>

**Gameplay** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00394460`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |

**Party** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0030BEF0`](prefetch-manifests.md) | calls | [`0x0031B7E0`](../Engine-Core/identifier-spaces.md) (on identifier spaces) |

**Menus and HUD** (explained on [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md), [binmenu images](binmenu-images.md), [clan primer](../Menus-And-HUD/clan-primer.md), [hud](../Menus-And-HUD/hud.md), [subsystem update flags](../Engine-Core/subsystem-update-flags.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [widget messages](../Menus-And-HUD/widget-messages.md), [tim2 images](tim2-images.md), [battle text tables](battle-text-tables.md), [mrp menu resource packages](mrp-menu-resource-packages.md), [world map mesh mg](world-map-mesh-mg.md), [map screens](../Menus-And-HUD/map-screens.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001819A0`](prefetch-manifests.md) | is called by | [`0x002A0440`](../Engine-Core/ps2-cpu-emulation.md) (on ps2 cpu emulation) |
| [`0x0024A5A0`](binmenu-images.md) (on binmenu images) | is called by | [`0x00279E20`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00280DE0`](../Menus-And-HUD/opening-the-main-menu.md) (on opening the main menu)<br>[`0x002814E0`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen)<br>[`0x00281AE0`](binmenu-images.md) (on binmenu images)<br>[`0x00291010`](prefetch-manifests.md)<br>[`0x002911D0`](prefetch-manifests.md)<br>[`0x002915C0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002917E0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002D70F0`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x003C9E50`](binmenu-images.md) (on binmenu images)<br>[`0x003EE420`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00558FB0`](../Menus-And-HUD/license-board-screen.md) (on license board screen) |
| [`0x0024A5A0`](binmenu-images.md) (on binmenu images) | is also called by | [`0x00560910`](battle-text-tables.md) (on battle text tables)<br>[`0x00562F90`](world-map-mesh-mg.md) (on world map mesh mg)<br>[`0x00563110`](world-map-mesh-mg.md) (on world map mesh mg) |
| [`0x002713B0`](prefetch-manifests.md) | is called by | [`0x002911D0`](prefetch-manifests.md) |
| [`0x00291010`](prefetch-manifests.md) | calls | [`0x003F6FD0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F7380`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F73D0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F73F0`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x00291010`](prefetch-manifests.md) | is called by | [`0x00290300`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x002911D0`](prefetch-manifests.md) | calls | [`0x003F34D0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F3510`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F3580`](prefetch-manifests.md) |
| [`0x002911D0`](prefetch-manifests.md) | is called by | [`0x0028EA20`](prefetch-manifests.md) |
| [`0x0030BEF0`](prefetch-manifests.md) | is called by | [`0x003F77F0`](prefetch-manifests.md) |
| [`0x003F3660`](prefetch-manifests.md) | is called by | [`0x003F3510`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x003F77F0`](prefetch-manifests.md) | calls | [`0x002732E0`](prefetch-manifests.md) |
| [`0x003F77F0`](prefetch-manifests.md) | is called by | [`0x003F6BB0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F7CC0`](prefetch-manifests.md) |
| [`0x005621A0`](../Menus-And-HUD/map-screens.md) (on map screens) | is called by | [`0x005512B0`](prefetch-manifests.md) |
| [`0x00562A30`](../Menus-And-HUD/map-screens.md) (on map screens) | is called by | [`0x005551F0`](../Menus-And-HUD/map-screens.md) (on map screens) |

</details>
