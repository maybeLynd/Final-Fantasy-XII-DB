[Home](../../README.md) / [EBP script files](README.md) / EBP script container

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| EBP script container: the twenty-slot directory of every zone and event script, and the walk that hands each section to its loader | format | EBP script files | Script files | The .ebp file: how a zone or event script is requested by kind and index with its companion files, read whole into a resource arena, and walked by one function that dispatches each present section of its twenty-slot directory to its own handler; the header and section table, the pending word that holds the script back until every part is bound, the teardown, and the shipped files measured over all nine language trees. | 0x003304A0, 0x0032FCA0, 0x0032FC30, 0x00330310, 0x0032E400, 0x0032E620, 0x002DF980, 0x002DF9A0, 0x0036A100, 0x0036C660, 0x00332250, 0x022C6E48, 0x022C6C00, 0x0032F1B0, 0x0032ED80, 0x0032F430, 0x0032F850, 0x00330190, 0x00330220, 0x00332100, 0x00330060, 0x0032FA10, 0x0032FAC0, 0x00331610, 0x003316B0, 0x0032FB70, 0x00330110, 0x003320E0, 0x00332110, 0x003320D0, 0x0032ED70, 0x00332130 |

## What the player sees

Everything a map does beyond its scenery comes from one `.ebp` file: the people who walk and talk,
the doors, chests and save crystals, the weather, the camera cuts and lighting of a cutscene, the
signs on the map. Each zone has one, each event has one, and entering a zone or starting an event
loads it. The container is the file's table of contents: it says which of these parts a given zone
or event carries and where each one starts.

## Where it comes from

Zone scripts sit at `ps2data/plan_master/<language>/plan_map/<area>/<zone>/global/<zone>.ebp` and
event scripts at `ps2data/plan_master/<language>/event/<group>/<event>/<event>.ebp`, in nine
language trees. Four control scripts (`btlctrl`, `ctrl`, `evctrl`, `mapctrl`) sit under
`ps2data/image/ff12/<language>/bin/` in the `in` and `ch` trees only.

The game never opens a script by name. `0x0032FCA0(manager, id)` turns a script manager index and a
script id into a `(kind, index)` pair of a [resource kind](../Game-Files-And-Data-Tables/file-size-tables-fst.md) and resolves it through the path tables
(`0x002DF980` returns `[0x0215F000 + kind × 8][index]`, the tables `0x002DF9A0` installs per
language; see [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md)):

| Manager | Kind | Index | Files at index, +1, +2, +3 |
|---|---|---|---|
| 0 (zone) | 5 | id × 3 | `.ebp`, `.mot`, `.fpk` |
| 1 to 3 (events) | 8 | id × 4 | `.ebp`, `.mot`, `.snd`, `.vpc` |
| 4 | 1 | id + `0x6B` | the script only |

The zone script is requested from `0x00314020` (`0x003140BA`, manager 0, the id held at `0x01EED064`).
Event scripts go to managers 1 to 3: `0x003522C0` and `0x00353080` add 1 to their argument and clamp
it to 1 to 3, and `0x00353590`, `0x003CA07C` and `0x00306BD0` use manager 3.

A zone script is fetched with its `.mot` file, and an event script with its `.mot`, `.snd` and `.vpc` files. The game
reads the whole script at once and hands each part to its own system, and builds the scene's actors only after every
requested file and part has arrived.

## Layouts

All multi-byte fields are little-endian.

### Container header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | magic | 'EBP2' in every shipped container |
| `+0x04` | `u32` | slotCount | 20; slot n is dispatched only when slotCount > n |
| `+0x08` | `u8[4]` | reserved | 0 in all 10,036 containers; read by no function: the buffer `0x022C6C00`[manager] is stored by `0x00330310` (`0x003303C5`) and `0x0032F430` (`0x0032F450`), freed by `0x0032ED80` (`0x0032F127`-`0x0032F139`), and read by the walk `0x003304A0`, which takes the slot count `+0x04` and the offsets from `+0x10` and hands the handlers section addresses; the preload copy of script `0xD4` (`0x00330407`) moves the image whole; nothing fixes its width |
| `+0x0C` | `u8[4]` | reserved | 0 in all 10,036 containers; read by no function: the buffer `0x022C6C00`[manager] is stored by `0x00330310` (`0x003303C5`) and `0x0032F430` (`0x0032F450`), freed by `0x0032ED80` (`0x0032F127`-`0x0032F139`), and read by the walk `0x003304A0`, which takes the slot count `+0x04` and the offsets from `+0x10` and hands the handlers section addresses; the preload copy of script `0xD4` (`0x00330407`) moves the image whole; nothing fixes its width |
| `+0x10` | `u32[20]` | sectionOff | indexed by section number; file-relative offset, 0 = absent |
| `+0x60` | `u8[32]` | padding | 0; the first section starts at `+0x80` |

A section has no stored length: it runs to the next present offset, and the last one to the end of
the file. The walker passes each section on as `fileBase + offset` with the manager index in the
low four bits, so every offset must be a multiple of 16.

### Section table

| Slot | First bytes | Handler, then binder | Kept in | Documented in |
|---|---|---|---|---|
| 0 | `0x8000000B` | `0x0032F850` → `0x0026C8C0` | `0x022C6C28` | [script image](ebp-script-image.md) |
| 2 | | `0x00330190` → `0x0026C880` | `0x022C6CA0` | [script text](ebp-text-sections.md) |
| 3 | | `0x00330220` → `0x0026C8A0` | `0x022C6CC8` | [script text](ebp-text-sections.md) |
| 4 | `NAVI` | `0x00332100` → `0x003DFDC0` | | [navigation icons](ebp-navigation-icons.md) |
| 6 | `TIM2` | `0x00330060` → `0x0026C860`, `0x0017F790`, `0x0029CAC0` | `0x022C6CF0` | [TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md) |
| 8 | `CML1` | `0x0032FA10` → `0x0026CE00`, then `0x003DA1F0` when record `+0xE0` is set (`0x0032FA4F`) | `0x022C6D80` | [camera tables](ebp-camera-tables.md) |
| 9 | `CAM7` | `0x0032FAC0` → `0x002566E0`, `0x002561C0`, `0x0026CE20` | `0x022C6D58` | [camera tables](ebp-camera-tables.md) |
| 10 | `CML1` | `0x00331610` → `0x0026D3A0`, `0x003DD120` | `0x022C6DF8` | [camera shake](ebp-camera-shake.md) |
| 11 | `SHK1` | `0x003316B0` → `0x0026D3C0`, `0x0037DC30`, `0x0037DA90` | `0x022C6DD0` | [camera shake](ebp-camera-shake.md) |
| 12 | | `0x0032FB70` → `0x0026CE40` | `0x022C6DA8` | [actor manifest](ebp-actor-manifest.md) |
| 14 | `LGT2` | `0x00330110`, bound later by `0x0032F1B0` | `0x022C6E20` | [lighting](ebp-lighting-lgt2.md) |
| 16 | `FF12` | `0x003320E0` → `0x003DFE60(0, section)` | | [position entries](ebp-position-entries.md) |
| 17 | | `0x00332110` → `0x003DFE60(1, section)` | | [position entries](ebp-position-entries.md) |
| 19 | `FF12` | `0x003320D0` → `0x003EAA00` | | [area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md) |

The "Kept in" arrays hold one qword per manager. Slots 1, 5, 7, 13, 15 and 18 have no dispatch:
the walker never reads their offsets. Slot 17 is the same format as slot 16, bound under the
other selector.

## Shipped data

Measured over every `.ebp` in `FFXII_TZA.vbf`.

| Fact | Value |
|---|---|
| `.ebp` files | 10,045: 1,115 per language tree (`kr` and `cn` 1,116), plus the 8 control scripts |
| containers | 10,036; the 9 others are `event/evt_t/evt_t0020/evt_t0020.ebp` in each tree, 2,416 bytes beginning with the word `0x80000007` and no header |
| `us` tree | 1,114 containers: 769 zone scripts and 345 event scripts |
| header | magic `EBP2`, slot count 20, both reserved words 0, padding zero, first offset `0x80`: all 10,036 |
| section offsets | 50,912, every one a multiple of `0x40`, ascending and inside the file in every container |
| container size | 640 to 468,352 bytes (`us` 640 to 421,184) |
| slots never present | 1, 5, 7, 13, 15, 17 and 18, in all 10,036 |
| `us` occupancy | 0: 1,114; 2: 828; 3: 359; 4: 209; 6: 67; 8 and 9: 423; 10 and 11: 113; 12: 842; 14: 140; 16: 517; 19: 271 |
| all-tree occupancy | 0: 10,036; 2: 7,466; 3: 3,232; 4: 1,881; 6: 2,719; 8 and 9: 3,807; 10 and 11: 1,017; 12: 7,578; 14: 1,260; 16: 4,653; 19: 2,439 |
| pairs | 8 and 9 always occur together, and 10 and 11; 2 and 3 do not (2,953 both, 4,513 only 2, 279 only 3) |
| zone-only sections (`us`) | 3, 4, 16 and 19 occur only in zone scripts; 14 only in event scripts |
| section 6 by tree | 67 or 68 files in each Latin-script tree; 556 `kr`, 584 `cn`, 603 `ch`, 633 `in`; plus 3 control scripts in each of `in` and `ch` |
| first bytes | the word or tag in the section table, the same in every file that has the section |
| file tables | [ebp-script-container-files-event.tsv](ebp-script-container-files-event.tsv), 3,114 event scripts, and [ebp-script-container-files-plan-map.tsv](ebp-script-container-files-plan-map.tsv), 6,923 zone scripts: every file of every tree with its bytes, SHA-256, the path-array entry that names it, the size check, the decode check and whether the game loads it |
| control file table | [ebp-script-container-files-control.tsv](ebp-script-container-files-control.tsv), the 8 control scripts, in the same columns |
| named by a path array | 2,934 event scripts (326 per tree), each at an index 4 × id of kind 8, and 6,372 zone scripts (708 per tree), each at an index 3 × id of kind 5; in all 9,306 every naming language's size table gives the file's exact size |
| decode | 10,036 files read to their end: the directory walk above, the sections cut at each next offset and the last at the end of the file, and section 0 disassembled through the image's `length` (`+0x04`), the rest of the section zero padding under 64 bytes; the 9 `evt_t0020` files stop at offset 0, where no header begins |
| named by no path array | 180 event scripts, 20 per tree (`dst_z9900` and the developer scripts `evt_t0005` to `evt_t0509`), and 551 zone scripts, 61 per tree and 62 in `kr` and `cn` (31 `bts_` test maps, 12 `dor_`, 5 `bds_`, 5 `mic_b`, 3 `pre_`, 2 `asp_b`, 2 `tst_`, `vic_a04`, and `ttl_a01_e3` in `kr` and `cn`): no language's path array names them, and the script load `0x0032FCA0` takes a script's path from those arrays through the resolver `0x002DF980` |
| control scripts | the 8 are named by no path array either. Kind 1 entries 109 to 112, the indices `id + 0x6B` of manager 4 for ids 2 to 5, lie past the end of every path array, and the US, FR, DE, IT, ES, UK, KR and CN size tables give them 11,584, 38,720, 40,832 and 32,448 bytes, the sizes of `ctrl.ebp`, `evctrl.ebp`, `mapctrl.ebp` and `btlctrl.ebp` |

### Per-file tables

The three tables have one row per shipped file, in path order within each language tree:

| Column | Meaning |
|---|---|
| `language` | the language tree: `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr` or `us` |
| `family` | `event`, `plan_map` or `control` |
| `path` | the file's path in the archive |
| `bytes`, `sha256` | the file's size and SHA-256 |
| `named_by` | each size-table kind and id whose path array names the file, with the languages of that array ([file size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)); `-` when no array names it. Kind 37 entries are listed too: `0x0032FCA0` asks kind 37 only for index + 3, the `.vpcjp` |
| `fst_size_matches` | `yes` when the size table of every naming language that sizes the entry gives the file's size; `-` for a file no array names |
| `decodes` | `yes` when the file reads to its end as the decode row of Shipped data states, otherwise `no at` the offset where reading stops |
| `loaded` | `read by` the languages whose kind 5 or 8 array names the file at a script index with a size, or `named by no path array`. UK's size table has no entry in kinds 5 and 8, so no UK language is listed |

### Language trees

The eight other trees carry the `us` scripts with their own text. Against the `us` file of the same path:

- sections 8 to 12, 14, 16 and 19 are byte-identical in every tree;
- section 4 differs in four maps (`bhm_a02`, `gil_i01`, `gil_i02`, `naf_b04`) in `ch`, `cn`, `de`, `es`, `in` and
  `kr`, the same blocks in all six ([navigation icons](ebp-navigation-icons.md)): `gil_i01` has two minimap markers
  more (gates 257 and 258) and `gil_i02` two fewer, and `naf_b04` lacks its icon-24 marker;
- sections 2 and 3 hold each tree's text, and section 6 its glyph sheets: 67 or 68 files in the Latin-script trees,
  556 to 633 in `in`, `kr`, `cn` and `ch`, every one in a file that has text section 2 or 3;
- the script image (section 0) differs in 2,323 files: `ch`, `cn` and `kr` 311, `in` 294, `de`, `es`, `fr` and `it`
  274; `cn` and `kr` also ship `ttl_a01_e3`, a second title script with no `us` file.

In most of those images the code is the `us` code and the difference is in the msp area (`+0x40`): the picture block
that scripts register with `registshape` and place with `setshapepos_183`. Ten pictures occur. Each tree redraws them,
most in its own words: `GATE TIMER` becomes `TOR GEÖFFNET` in `de` and `NOTORIETY` becomes `噂レベル` in `in`.
Where a tree's picture is larger or holds more colours, the image grows and the references behind it move.

The code changes are:

- the screen positions of picture parts and message windows;
- the message slot of the Royal Palace icon window;
- in `ch`, `cn` and `kr`, 392 calls `setcharclipall(1)`, and code for an early-ending build that does not run: it
  sits under verb `0x5B4`, which always answers 0 (`0x00355930`), or in `ttl_a01_e3`, which no path array names.

[Language-tree script differences](../Story-Events-And-Hunts/script-language-differences.md) says what each
one does in the game.

Differences per tree and kind, with the scripts in brackets:

| Kind | `ch` | `cn` | `de` | `es` | `fr` | `in` | `it` | `kr` |
|---|---|---|---|---|---|---|---|---|
| picture block bytes (`data-area-constant`) | 682 (294) | 684 (295) | 564 (274) | 564 (274) | 564 (274) | 682 (294) | 873 (274) | 684 (295) |
| screen position (`coordinate-or-camera`) | 29 (14) | 29 (14) | 17 (14) | 648 (27) | 22 (11) | 29 (14) | 1,232 (129) | - |
| code added or removed (`call-added-or-removed`) | 413 (17) | 435 (18) | - | - | - | - | - | 435 (18) |
| image length (`image-length`) | 52 (52) | 53 (53) | - | - | - | 39 (39) | 103 (103) | 53 (53) |
| message slot (`message-slot`) | 13 (2) | 13 (2) | 13 (2) | 13 (2) | 13 (2) | 13 (2) | 13 (2) | 13 (2) |
| minimap marker, section 4 (`navigation-icon`) | 13 (4) | 13 (4) | 13 (4) | 13 (4) | - | 13 (4) | - | 13 (4) |
| reference into the msp area (`data-area-reference`) | 10 (4) | 10 (4) | - | - | - | 10 (4) | 1 (1) | 10 (4) |
| listing numbering, no byte change in the code (`listing-renumbering`) | 16 (2) | 38 (3) | - | - | - | - | - | 38 (3) |
| variables of added code (`variable-declaration`, `variable-offset`) | 4 (2) | 14 (3) | - | - | - | - | - | 14 (3) |
| branch condition (`branch-condition`) | 1 (1) | 4 (2) | - | - | - | - | - | 4 (2) |
| fade length, verb argument (`wait-or-timing`, `verb-argument`) | - | 3 (1) | - | - | - | - | - | 3 (1) |
| image header table (`header-table`) | - | - | - | - | - | 1 (1) | - | - |
| file with no `us` twin (`script-file-added`) | - | 1 (1) | - | - | - | - | - | 1 (1) |

No tree changes a text id passed to a verb, a camera verb, or the author, source name or build stamp of an image, and
no script of any tree calls `setbehindcameratype` (`0x1CB`).

| Table | Rows | One row per |
|---|---:|---|
| [`ebp-language-differences.tsv`](ebp-language-differences.tsv) | 9,251 | tree, script, actor, function and difference: `kind`, the `us` and tree code or bytes, what it changes, and the listing line or image offset it was read at |
| [`ebp-language-summary.tsv`](ebp-language-summary.tsv) | 60 | tree and kind: scripts and differences |
| [`ebp-language-pictures.tsv`](ebp-language-pictures.tsv) | 10 | picture block: size, frames, scripts, and per tree whether it differs and the words it draws |

### Columns of ebp-language-differences.tsv and ebp-language-pictures.tsv

| Column | Holds |
|---|---|
| `tree_value` | in ebp-language-differences.tsv, the tree's side of the difference, in the same form as `us`: the tree's code line, value, size or byte count at that place; `-` where the tree lacks what `us` has or `us` lacks what the tree adds (for example `us` is `-` and `tree_value` is `setcharclipall(1);` on the 1,176 rows of that call) |
| `cite` | where the difference was read: `us L` and `L` with the line numbers in the two listings; the tree's added lines and the `us` line they come before (`ch L54-54, before us L54`); `image` with an offset, a byte range or a header field (`image +0x3C`) of the script image; `section` with an offset in that container section and the file offset in brackets; or, for the one script with no `us` twin, its path |
| `key` | in ebp-language-pictures.tsv, the first 10 hex digits of the SHA-1 of the `us` picture: the bytes of its TIM2 image from the start of the pixel data to the end of the palette, inside the `MSP` picture block of the script image's msp area (offset `+0x40`, size `+0x3C`); scripts whose `us` pictures hold the same bytes form one row, and the key of each row's first script reproduces from its shipped `us` file on all 10 rows |
| `first_scripts` | in ebp-language-pictures.tsv, the scripts whose picture block holds the picture, every one of them (as many names as `scripts`) |
| `us_words` | the words the `us` picture draws, separated by semicolons |
| `ch_differs`, `cn_differs`, `de_differs`, `es_differs`, `fr_differs`, `in_differs`, `it_differs`, `kr_differs` | how many of the picture's scripts have a different picture block in that tree: on every row either all of them or 0 (picture `g07` in `de`, `es`, `fr` and `it`) |
| `ch_words`, `cn_words`, `de_words`, `es_words`, `fr_words`, `in_words`, `it_words`, `kr_words` | the words the tree's picture draws where they differ from `us`, `same words` for the rest when they are the `us` words, and `as us` when the tree's picture block is the `us` one |

## Loader behaviour

### Requesting a script

`0x0032FC30(manager, id)` calls `0x0032FCA0` and then `0x0025D4D0(manager)`, which clears bit `0x2` of the manager slot's
`+0x10`, and, for manager 0, sets bit `0x1` of the manager's pending
word (`0x0032FC77`-`0x0032FC8B`). For manager 0 it first reads the area data (`0x003EA6E0(id, [0x022C6D1D])`, `0x0032FC4B`);
the call `0x003319D0(id)` behind `0x005C5230(5)`, which returns 0, does not run (`0x0032FC67`-`0x0032FC72`). `0x0032FCA0`:

1. tears down the manager's previous script (`0x0032ED80`, below) and records the id at `0x022C6D28`
   and `0x022C6D40`;
2. picks the kind and index from the table above;
3. for managers 0 to 3, requests the companion files: index + 1 into the `0x88`-byte buffer
   `0x022C6E70` (pending bit `0x2000`), and, for managers 1 to 3, index + 2 into `0x022C6E98` (bit `0x1000`);
4. for managers 1 to 3, requests index + 3 of kind 8 into the `0x208`-byte buffer `0x022C6EE8`
   (bit `0x8000`) and the same index of kind 37 into `0x022C6EC0` (bit `0x4000`); each request is made only
   when `0x0032E400` reports a size;
5. pushes the arena the image will live in: 5 for manager 0, `0xD` for managers 1 and 2 and `0xE`
   for manager 3 when that arena is enabled (`0x0036B200`), otherwise 5;
6. calls `0x00330310` to read the script itself.

Kind 37's table is the `in` tree's (`0x01ECBCF0`; the `ch` tree's `0x01EA4D00` for language codes
7, 8 and 11), so its index + 3 names a `.vpcjp` file such as
`in\event\nal_a\nal_a0100\nal_a0100.vpcjp` where kind 8 names the `.vpc`. The four companion buffers are allocated once,
for all five managers, by `0x0032F430`.

### Reading it whole

`0x00330310(manager, id, kind, index)`:

1. takes the size from `0x0032E400`, which rounds the size table's figure up to a multiple of 64 when it is
   positive and returns a figure of 0 or less as it is (`0x0032E43B`-`0x0032E448`);
2. sets pending bit `0x20000` (`0x0033036A`), before it tests the size: a size of 0 or less skips steps 3 to 6
   (`0x00330378`), so nothing is allocated or read and the bit stays set with no walk to clear it;
3. allocates that many bytes with `0x0036A100` in the current arena and labels the block with
   `0x0036C660` (source name `atelload.c`, tag `0x95C`);
4. stores the buffer at `0x022C6C00[manager]`, sets the manager record's `+0x11` bit `0x8`, and forms the
   packed value `buffer | manager`;
5. calls `0x00332250`, which for kinds 5, 8 and 37 cuts a folder name out of the path (such as
   `event\nal_a\nal_a0100`) and hands it to the text layer under the packed value (`0x0017FA90`);
6. files an asynchronous whole-file read (`0x0032E620`) whose completion is `0x003304A0(packed)`;
7. for manager 0, files a `0x800`-byte pre-read of the zone's index + 2, its `.fpk` (`0x0032EB40`), which no
   zone ships, so it reads nothing. This step runs whatever the size, also after a size of 0 or less; it sits
   behind `0x005C5230(5)`, which returns 0 (`0x0033045B`-`0x0033048B`).

`0x00332250(kind, index, packed, 1)` takes the size again from `0x0032E400` and does nothing when it is 0 or less
(`0x00332280`, `0x003322A9`). It copies the path from `0x002DF980` (`0x003322C8`) and counts `\` and `/` back from its end
(`0x0033231C`-`0x00332322`): for kinds 8 and 37 the name runs from the fourth separator to the first (`0x0033229F`), and
for kind 5 from the fifth to the second (`0x00332298`), so a zone script gives `plan_map\<area>\<zone>`.

A name end at offset `0x104` or more goes to `__report_rangecheckfailure` (`0x00332343`, `0x003323A4`). The name is
formatted with `"%s"` (`0x00332369`) and handed over as `0x0017FA90(packed, 1, name, 0)` (`0x0033236E`-`0x0033237F`).

Script id `0xD4` (kind 8 index `0x350`, `event/pre_z/pre_z0000` in the `us` tables) is
preloaded once by `0x0032F430` into `0x022C6F10`; a request for it copies that image into the new
buffer and walks it at once instead of reading the file.

`0x0032F430` sizes the preload with `0x0032E400(8, 0x350)` (`0x0032F617`), allocates it and files its read with `0x0032E620`
(`0x0032F670`); the size it keeps is the length `0x00330310` copies:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C6D3C` | `i32` | 0 (zero-filled tail of `.data`) | the byte size of the preloaded script `0xD4` at `0x022C6F10` | `0x0032F430`, 0 (`0x0032F611`) and then the size `0x0032E400` returned when it is above 0 (`0x0032F65B`) | `0x00330310`, for a request of `0xD4` while `0x022C6F10` is set: as the read size (`0x00330347`) and as the `memcpy` length into the new buffer (`0x003303FD`, sign-extended) |

### The directory walk

`0x003304A0` (570 bytes) recovers the file base with `and rdi, 0xFFFFFFF0` (`0x003304D9`) and the
manager from the low nibble. It sets pending bit `0x2`, and bit `0x200` when slot 12 is present
(`0x003304DE`–`0x003304F5`). It then tests each slot in a fixed order with the same five steps:
`slotCount > n` (unsigned), offset non-zero, `base + offset`, `or` the manager into the low nibble,
call the handler. There is no loop and no table: fifteen `cmp dword ptr [rdi + 4], n` sites cover
fourteen slots, slot 12 being tested twice.

The order is 0, 2, 3, 6, then 9, 8, 11, 10, 12, 16, 17, 4, 19, and last 14, which is skipped for
manager 0 (`0x0033066B`). The first four calls are bracketed by the text-layer calls `0x0017FB70` and
`0x0017FBE0`. The walk reads nothing else: not the magic, not the reserved words and not the padding.

A packed value whose base is 0 calls no handler (`0x003304DC`, `0x003304FC`, `0x00330572`, `0x0033066F`). The walk
still sets bit `0x2` (`0x003304D1`) and clears bit `0x20000` at its end (`0x00330696`), so bit `0x2` stays set and
the walk does not run `0x0032F1B0`.

The packed value is carried in 32 bits (`0x00330510 or eax, ebx`, `0x00330512 mov ecx, eax`), and each
handler masks it back with `0xFFFFFFF0`, so the buffer must lie below 4 GiB and every section offset
must keep the low four bits clear.

### Handlers

Each handler that keeps its section stores the pointer in its manager array (section table) and
calls its binder; the slot-0 handler `0x0032F850` first rejects an image whose first byte is 0
([script image](ebp-script-image.md)). Sections 4, 16, 17 and 19 go straight to their subsystem
and are not tracked per manager. Section 14 is only stored; `0x0032F1B0` binds it.

### Pending word and finish

`0x022C6E48[manager]` holds the manager's outstanding work:

| Bit | Set by | Cleared by |
|---|---|---|
| `0x1` | `0x0032ED70` after an event request, `0x0032FC30` for manager 0 | `0x00332130` |
| `0x2` | the walk | the slot-0 handler `0x0032F850` |
| `0x200` | the walk, when slot 12 is present | the slot-12 handler `0x0032FB70` |
| `0x1000`, `0x2000`, `0x4000`, `0x8000` | `0x0032FCA0`, per companion request | their completions `0x00331760`, `0x003302B0`, `0x003317C0`, `0x00331820` |
| `0x20000` | `0x00330310` | the end of the walk (`0x00330696`) |

The other handlers clear the bits under mask `0x10DF0`, which nothing on this route sets. Every
clearer applies the same rule: when the word without bit `0x1` becomes zero it clears the record's
`+0x11` bit `0x8`; when the whole word goes from non-zero to zero it runs `0x0032F1B0(manager)`.

`0x0032F1B0` binds section 14 through `0x0037AA90` for managers above 0 (`0x0032F1BB`), with its light bookkeeping
(`0x0037B230`, `0x003DE920`, `0x0037B290`): every manager above 0 gets its light group reset and its ready byte cleared,
and only one whose section pointer `0x022C6E20[manager]` is set (`0x0032F1F2`) gets the bind, the ready byte again and
its `+0x1FC` store ([lighting](ebp-lighting-lgt2.md)).

Then, for every manager, it runs `0x0026CE60`, which builds
the manager's actors from the image ([actor managers](../Characters-And-Objects/actor-managers.md)), and returns
`0x00263C30(manager)` through its tail jump (`0x0032F233`): the manager's record count `+0x20` while bit `0x1` of
`+0x10` is set, else 0.

Bit `0x1` therefore holds `0x0032F1B0` back after every part has arrived, until `0x00332130` clears it
(its callers include `0x00354B20`, `0x00354E80` and `0x00378120`).
For manager 0, `0x0032F850` and `0x0032FB70` also run `0x0025AFC0(0)` once bits `0x2` and `0x200` are both clear.
They then call `0x002EACC0(0x00331990, [0x022C6D28])` (`0x0032F9DF`-`0x0032F9EE`, `0x0032FC00`-`0x0032FC0F`), which stores
`0x00331990` at `0x0215FD98` and the zone id at `0x021641F0` (`0x002EACC0`-`0x002EACC7`).

### Teardown

`0x0032ED80(manager)` runs before every new request. It unbinds what the handlers bound: section 6
(`0x002E0780`, `0x0017FA50`, `0x0029CB10`), section 14 on managers above 0 (`0x0037AA50`), section 9
(`0x002561A0`, `0x002566E0`, `0x0026CE20(manager, 0)`), section 8 (`0x0026CE00`), section 11 (`0x0037DA70`,
`0x0026D3C0`), section 10 (`0x0026D3A0`) and section 12 (`0x0026CE40`), and resets the four shake slots
(`0x0037DC30(manager, 0..3)`).

It zeroes every manager array
entry and the pending word, and frees the file buffer `0x022C6C00[manager]` (`0x003697F0`). The
per-section frees beside each unbind sit behind `0x005C5230`, which returns 0, so they never run.

## Modding notes

- The magic, the reserved words and the padding are never read; the slot count is, and lowering it
  disables every slot at or above it.
- A section added to slot 1, 5, 7, 13, 15 or 18 is never looked at. Slot 17 is live and takes the
  slot-16 format.
- Keep section offsets multiples of 16 (the shipped files use 64); the low four bits carry the
  manager index.
- Nothing checks a section's extent against the next offset or the file size.
- Section 14 has no effect in a zone script, which manager 0 loads.

## Related

- [Script image](ebp-script-image.md): section 0, the code the interpreter runs.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the record the bind fills and `0x0026CE60`.
- [File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md): the path tables and the read.
- [Resource arenas](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md): `0x0036A100`, the arena stack and block labels.
- [Script interpreter](../Scripts-And-Script-Commands/script-interpreter.md): what runs the image once it is bound.
