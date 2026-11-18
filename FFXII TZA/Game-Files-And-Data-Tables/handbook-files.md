[Home](../../README.md) / [Game files and data tables](README.md) / Handbook files

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Handbook files: the hctg, hchk, hdat and himg files behind Clan Primer entries, how each is read, and what each field shows | format | Game files and data tables | Menu and map files | The menuhandbook files of the six handbook families: the hctg family catalog with its entry records, section captions, page map and Bestiary slot counts; the hchk unlock tables; the hdat text bundles with their glyph sheets, gated text slots and line programs; the himg picture bundles; how the data manager turns an entry into kind-7 resource ids and reads each field; the shipped files; and the rules an edit must keep. | 0x005771F0, 0x00576F50, 0x00575870, 0x00575C30, 0x00575A50, 0x00575710, 0x00575B80, 0x005778F0, 0x00575D10, 0x00575DD0, 0x00576030, 0x005760A0, 0x00576740, 0x00576A50, 0x00577550, 0x00575E80, 0x00576860, 0x00576E30, 0x00576300, 0x00577A40, 0x00574900, 0x00D23740, 0x02CA9738 |

## What the player sees

The Clan Primer's Traveler's Tips and Bestiary pages list entries under section captions. Opening an
entry shows its text, one line or page at a time, and for the Bestiary a picture page, the monster's name,
its kill count and the lore lines unlocked so far. Every name, caption, line of text, picture and unlock
condition comes from the files on this page. Four more families, `story`, `world`, `person` and
`knowledge`, ship complete but no category opens them ([Clan Primer](../Menus-And-HUD/clan-primer.md)).

## Where it comes from

Each language folder `ps2data/image/ff12/myoshiok/<lang>/handbook/` holds, for each family `story`,
`world`, `person`, `knowledge`, `tutorial` (Traveler's Tips) and `monster` (Bestiary):

| File | Magic | Content |
|---|---|---|
| `menuhandbook_<family>.bin` | `hctg` | the family catalog: entries, sections, page map |
| `menuhandbook_<family>.dat` | `hchk` | one unlock record per entry |
| `menuhandbook_<family>000.dat` onward, the first `hctg +0x14` numbers | `hdat` | text bundles |
| the numbered files after them | `himg` | picture bundles |

All are kind-7 resources. The family's base id is the `u16` at `0x00D23740 + 2 x family`
(`0x228`, `0x294`, `0x2CC`, `0x2F4`, `0x31C`, `0x354`); the catalog is base + 0, the unlock table base + 1
and numbered file `NNN` base + 2 + `NNN`, matching the `us` kind-7 path array at `0x01EC73A0`. The same folder
holds `menuhandbook.bin` and `menuhandbook_order.bin`, which the Clan Primer page covers.

Opening an entry reads its catalog record, which names the text bundle that holds its words and a picture page; the
page map turns that page into one of the picture files. The family's unlock table has one row per entry, each testing
save flags or story progress, and the result becomes the entry's unlock mark.

## Layouts

All multi-byte fields are little-endian.

Offsets are from the start of the file. Every offset field is relative to the file unless noted.

### hctg: the family catalog

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "hctg"; the loaders ignore it |
| `+0x04` | `u32` | version | 102; not read |
| `+0x08` | `u16` | family | low nibble = family number 0-5 (`0x00576740`); the word >> 4 is copied out (`0x00576030`) |
| `+0x0A` | `u16` | recordsAt | offset of the entry records |
| `+0x0C` | `u16` | pageMapAt | offset of the page map, u16[pageCount] |
| `+0x0E` | `u16` | entryCount | entries; bounds every record index |
| `+0x10` | `u16` | pageCount | pages; bounds every page number (`0x00575DD0`) |
| `+0x12` | `u16` | sectionCount | sections; bounds every caption index (`0x00576A50`) |
| `+0x14` | `u16` | textBundles | number of hdat files; the first picture file follows them (`0x005773D2`) |
| `+0x16` | `u8[2]` | pictureFiles | number of picture files the page map names; read by no function: the catalog readers `0x005778F0`, `0x00575D10`, `0x00575DD0`, `0x00576030`, `0x005760A0`, `0x005766E0`, `0x00576740` and `0x00576A50` (the functions that load [slot 0 `+0xF0`]) read nothing at `+0x16`; nothing fixes its width |
| `+0x18` | `i32` | caption[sectionCount] | text id of each section caption; -1 = no caption |

```
...    u16      gateCount, u16 gateAt[gateCount]   caption gates, offsets from gateCount's own position
```

A caption gate, reached through `gateAt[section]`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags | low nibble: copied to the caption record `+0x0A`; high nibble: condition count C |
| `+0x01` | `u8` | mapCount | M |
| `+0x02` | `u16` | condition[C] | encoded ids tested with `0x00309EC0`(id, 0) |

```
...    u16  map[M]         map numbers
```

An entry record, 12 bytes, at `recordsAt + 12 x entry`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | text | name; -1 = no name. Families 0-4: message id (`0x002F9920`); Bestiary: battle-text word (`0x003214B0`, `0x002B58B0`) |
| `+0x04` | `u16` | section | the caption the entry is listed under (`0x00576740`) |
| `+0x06` | `u16` | bundle | which hdat file holds the entry's text (`0x00575D10`) |
| `+0x08` | `u16` | page | picture page number, through the page map (`0x005778F0`) |
| `+0x0A` | `u8` | flag | copied to the detail record `+0x14` (`0x005760A0`) |
| `+0x0B` | `u8` | pad | 0 |

After the records, at `recordsAt + 12 x entryCount`, sits `u16 count, u16 at[count]`; `at[entry]` is an
offset from the `count` word to one byte, the entry's number of Bestiary text slots (`0x005760A0`). Only the
Bestiary catalog fills it; the other families end with `count` 0.

The page map gives, for each page number, the picture file as an offset from the first picture file:
page `p` is in file `textBundles + pageMap[p]`.

### hchk: the unlock table

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "hchk"; the loaders ignore it |
| `+0x04` | `u32` | version | 103; not read |
| `+0x08` | `u16` | count | records; `0x00577550` walks this many |
| `+0x0A` | `u8[2]` | unused | 18 or 0; read by no function: the six tables, manager `+0xC8` to `+0xF0`, are read by `0x00577550` (`0x005775C1`, `0x00577660`), which walks families 0-4 with `0x00575E80` and the Bestiary with `0x005768E0` and `0x00576860`, and the Bestiary's table `+0xF0` also by `0x00576860`, `0x005768E0` and `0x00576E30` (`0x00576870`, `0x005768EA`, `0x00576E73`); none of them reads `+0x0A`; nothing fixes its width |
| `+0x0C` | `rec[count]` |  | 8 bytes each, 16 for the Bestiary |

Families 0-4, 8 bytes per entry, evaluated by `0x00575E80`, which answers 1 when every test holds and 0 at the
first one that fails (`0x00575E9D`, `0x00575EEE`). A field holding all ones (`0xFF`, `0xFFFF`) is skipped; every
other field must hold. The nibble test is skipped on `nibbleIndex` alone (`0x00575E8C`), so with a real index a
`nibbleValue` of `0xFF` never matches (`0x00315470` answers 0 to 15), and the story counter is taken as a signed
16-bit value against `storyMinimum` (`0x00575EE3`-`0x00575EEC`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | nibbleIndex | save nibble `0x00315470`(index), one of 256 at save `+0x336C`, must equal `+0x01` |
| `+0x01` | `u8` | nibbleValue |  |
| `+0x02` | `u8` | bitIndex | save bit `0x00315620`(index), one of 256 at save `+0x334C`, must be set |
| `+0x03` | `u8` | marker | not read |
| `+0x04` | `u16` | storyFlag | `0x0032A8A0`(flag) must pass |
| `+0x06` | `u16` | storyMinimum | the story counter `0x00265270` must be at least this |

Bestiary, 16 bytes per entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | slot[7] | threshold of each text slot (`0x00576860`); `0xFF` (mode 0) or `0xFFFF` (modes 1, 2) = empty |
| `+0x0E` | `u16` | mode | bit `0x2` = mode 2, else bit `0x1` = mode 1, else mode 0 (`0x00576E30`, `0x005768E0`) |

`0x00576860(manager, family, entry, slot)` reads a threshold: 0 for a family other than 5 or no manager, the mode's
empty value when the table `+0xF0` is missing or `slot` is 7 or more, and otherwise the word at
`+0x0C + 16 × entry + 2 × slot`, with no bound on the entry (`0x00576863`-`0x005768DA`).

### hdat: a text bundle

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "hdat"; the loaders ignore it |
| `+0x04` | `u32` | version | 103; not read |
| `+0x08` | `u16` | first | entry number of the bundle's first record |
| `+0x0A` | `u16` | count | records; the bundle holds entries first to first + count - 1 |
| `+0x0C` | `i32` | sheet | offset of a TIM2 glyph sheet; -1 = no sheet (`0x00575710`) |
| `+0x10` | `u16` | stringsAt | base of the string offsets |
| `+0x12` | `u16` | recordAt[count] | offset of each record |

A record, `4 + 4 x slots + 8` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | slots | text slots |
| `+0x01` | `u8` | serial | read by no function: the bundle, [slot 1 `+0xF0`], is loaded by `0x00576300` (`0x00576376`), `0x00577A40` (`0x00577A8E`) and the sheet registration `0x00575710` (`0x00575750`, which reads `+0x0C` of the bundle only), and the two record readers take `+0x00` and the tail after the slots; nothing fixes its width |
| `+0x02` | `u8[2]` | entry | the record's entry number; read by no function: the bundle is loaded by `0x00576300`, `0x00577A40` and `0x00575710` (as `+0x01`), and no instruction of the three reads a record's `+0x02`; nothing fixes its width |
| `+0x04` | `i32` | string[slots] | offset from stringsAt of each slot's string entry |

```
...    u16, u16, u16, u8, u8   copied to the entry's line record +0x48, +0x4A, +0x4C, +0x4E (0x00576300)
```

A string entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | textAt | offset of the text from the entry itself; `0xFFFF` = no text (an empty line) |
| `+0x02` | `u8` | opCount | line-program operations (`0x00577A40`) |
| `+0x03` | `u8` | pad |  |
| `+0x04` | `...` |  | {u8 op, u8 index, u8 value, u8 pad}[opCount] |

```
...    text in the game's encoded text, zero-terminated
```

### himg: a picture bundle

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "himg"; the loaders ignore it |
| `+0x04` | `u32` | version | 100; not read |
| `+0x08` | `u16` | first | page number of the file's first picture |
| `+0x0A` | `u16` | count | pictures; the file holds pages first to first + count - 1 |
| `+0x0C` | `u32` | pictureAt[count] | offset of each TIM2 picture |

Each picture is a one-picture TIM2 image ([TIM2 images](tim2-images.md)). In every shipped file the
pictures follow one another, each `0x10` plus its picture's total size long, the last ending the file.
The extra `monster` files in `kr`, `ch` and `cn` repeat page windows the page map already gives to other files.

## Shipped data

Measured over all nine languages (`ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us`):

| Fact | Value |
|---|---|
| files | 54 `hctg`, 54 `hchk`, 101 `hdat`, 2,721 `himg`; every numbered file below `textBundles` is `hdat`, every one from it `himg` |
| entries | `story` 69, `world` 74, `person` 57, `knowledge` 100, `tutorial` 16, `monster` 384, in every language |
| sections | 4, 10, 4, 7, 4, 32 in the same order; every entry's `section` is below the count and every section is used |
| pages | 65, 46, 41, 45, 1, 384; every page resolves to a picture file whose window holds it |
| text bundles | 1 for `story`, `world`, `person`, `tutorial`; 2 for `knowledge`; `monster` 4 (`de`, `it`, `kr`, `us`), 5 (`ch`, `cn`, `es`, `fr`), 11 (`in`) |
| bundle windows | each bundle's `first` is the running total of the earlier bundles, and they add up to `entryCount` |
| picture files shipped and named by the page map | `story` 26 and 17, `world` 22 and 12, `person` 26 and 21, `knowledge` 27 and 12, `tutorial` 8 and 1; `monster` 192 and 192, with 2, 3 and 7 more unnamed files in `kr`, `ch` and `cn` |
| page map | non-decreasing, never `0xFFFF`; `monster` maps page `p` to `p / 2` |
| pictures | 6,693: files of 1 (72), 2 (1,983), 3 (9) and 4 (657) pictures; all 8-bit; 512 x 896 (3,480), 512 x 224 (2,754), 512 x 448 (450), 1024 x 448 (9) |
| glyph sheets | in every `story`, `world`, `person` and `knowledge` bundle; in `tutorial` and `monster` bundles only for `ch`, `cn`, `in`, `kr` |
| text slots | 1 per record except `world` (46 with 1, 28 with 2) and `monster` (164 with 2, 215 with 3, 5 with 7); the Bestiary slot-count bytes equal the bundle's `slots` for all 384 entries |
| string entries | 12,168, every one starting `04 00 00 00`: text at +4 and no line program |
| record tail | `00 80 00 80 FF FF FF` then one byte, in every record |
| Bestiary caption gates | 32 per language: 7 without maps, 14 with 1, 9 with 2, 1 with 3, 1 with 5; no condition ids |
| Bestiary slot modes (`us`) | 370 entries by kill count, 13 by story counter, 1 by another monster |
| other unlock records (`us`) | `story`: all 69 by story counter; `world` 5 and `tutorial` 5 by story counter; every other record has no test and is always unlocked |
| path array and size table | the `us` kind-7 array names numbered files up to `story099`, `world049`, `person029`, `knowledge029`, `tutorial049`, `monster299`; the US size table sizes exactly the shipped `us` files |

Bestiary entry 211 is the one record that differs between languages: `us` opens its slots by kill count (thresholds
1 and 1), the other eight trees by story counter (78 and 78), so those trees have 369 entries by kill count and 14 by
story counter. The `story`, `world`, `person` and `knowledge` text bundles are byte-identical in all nine trees.

Every instance of the 2,930 files, decoded with the layouts above, one row per instance in each language:

| table | rows | one row per |
|---|---:|---|
| [`handbook-files-files.tsv`](handbook-files-files.tsv) | 2,930 | shipped file: path, magic, size, SHA-256, family, number and window |
| [`handbook-files-entries.tsv`](handbook-files-entries.tsv) | 6,300 | catalog entry: its record, its text bundle and window, its picture page and file, and its unlock record |
| [`handbook-files-sections.tsv`](handbook-files-sections.tsv) | 549 | section: caption text id, the entries listed under it, and its caption gate |
| [`handbook-files-page-map.tsv`](handbook-files-page-map.tsv) | 5,238 | page-map slot: the picture file and the picture in that file |
| [`handbook-files-pictures.tsv`](handbook-files-pictures.tsv) | 6,693 | `himg` picture: offset, size, depth and byte count |
| [`handbook-files-strings.tsv`](handbook-files-strings.tsv) | 12,168 | string entry: bundle, entry, record, slot and the decoded text |
| [`handbook-files-glyphs.tsv`](handbook-files-glyphs.tsv) | 7,164 | sheet glyph of a `story`, `world`, `person` or `knowledge` bundle in each tree: its character, the two best match scores, one use and how the character was read |
| [`handbook-files-strings-decoded.tsv`](handbook-files-strings-decoded.tsv) | 2,952 | the string entries of those four families, with each sheet character in place |
| [`handbook-files-entry-names.tsv`](handbook-files-entry-names.tsv) | 49 | entry whose text gives its name: the name and the rule that gives it |
| [`handbook-files-entry-name-ids.tsv`](handbook-files-entry-name-ids.tsv) | 300 | `story`, `world`, `person` or `knowledge` entry: its name text id, the string that id finds in each tree, the name its text gives and its first line |

[`handbook-files-files.tsv`](handbook-files-files.tsv):

| Column | Meaning |
|---|---|
| `language` | the language folder |
| `path` | the file's path in the archive |
| `magic` | `+0x00`: `hctg`, `hchk`, `hdat` or `himg` |
| `bytes` | the file size |
| `sha256` | the SHA-256 of the file's bytes |
| `family` | `story`, `world`, `person`, `knowledge`, `tutorial` or `monster` |
| `number` | `NNN` of a numbered file; empty for the catalog and the unlock table |
| `version` | `+0x04` |
| `window_first`, `window_count` | `hdat`: `first` and `count`, the entries it holds; `himg`: `first` and `count`, the pages it holds; empty for `hctg` and `hchk` |

[`handbook-files-entries.tsv`](handbook-files-entries.tsv):

| Column | Meaning |
|---|---|
| `language`, `family`, `entry` | the entry; `entry` is the record index in the catalog |
| `name_text` | record `+0x00`: families 0-4 a message id, the Bestiary a battle-text word; `-` for -1 |
| `section` | record `+0x04` |
| `bundle`, `bundle_file` | record `+0x06` and the `hdat` file it names |
| `bundle_first_entry`, `bundle_last_entry` | that bundle's window, `first` to `first + count - 1` |
| `record_in_bundle` | `entry - first`, the index into the bundle's `recordAt` |
| `text_slots` | the bundle record's `slots` |
| `slot_count_byte` | Bestiary: the entry's slot-count byte after the catalog records; empty for the other families |
| `page` | record `+0x08` |
| `picture_file`, `picture_file_name` | `textBundles + pageMap[page]` and that file |
| `picture_in_file` | `page - first` of that `himg` file |
| `flag` | record `+0x0A` |
| `nibble_index`, `nibble_value`, `bit_index`, `marker`, `story_flag`, `story_minimum` | families 0-4: the unlock record's fields, `-` for a field of all ones; empty for the Bestiary |
| `slot_mode` | Bestiary: 0, 1 or 2 from the unlock record's `mode`; empty for the other families |
| `slot_mode_word` | Bestiary: the unlock record's `+0x0E` |
| `slot_thresholds` | Bestiary: the seven slot words in order, `empty` for `0xFF` in mode 0 and `0xFFFF` in modes 1 and 2 |
| `unlock_test` | the record's tests in words: for families 0-4 each field that is not all ones, or `no test` when every field is all ones; for the Bestiary what the slot thresholds count |

[`handbook-files-sections.tsv`](handbook-files-sections.tsv):

| Column | Meaning |
|---|---|
| `language`, `family`, `section` | the section |
| `caption_text` | `caption[section]`, a message id; `-` for -1 |
| `entries`, `first_entry` | the number of entries whose `section` is this one, and the lowest of them |
| `gate` | `yes` when `gateAt` has an offset for the section |
| `gate_low_nibble` | the gate's `flags` low nibble |
| `conditions`, `condition_ids` | the gate's condition count C and its ids |
| `maps`, `map_numbers` | the gate's map count M and its map numbers |

[`handbook-files-page-map.tsv`](handbook-files-page-map.tsv):

| Column | Meaning |
|---|---|
| `language`, `family`, `page` | the page number |
| `page_map_value` | `pageMap[page]` |
| `picture_file`, `picture_file_name` | `textBundles + pageMap[page]` and that file |
| `picture_in_file` | `page - first` of that file |

[`handbook-files-pictures.tsv`](handbook-files-pictures.tsv):

| Column | Meaning |
|---|---|
| `language`, `family`, `file`, `file_number` | the `himg` file |
| `picture_in_file`, `page` | the index into `pictureAt`, and `first` plus that index |
| `offset` | `pictureAt[index]` |
| `width`, `height` | the picture header's `width` and `height` |
| `depth_bits` | bits per pixel: 8 for image type 5 |
| `image_type` | the picture header's `imageType` |
| `psm` | the pixel format in `gsTex0` |
| `clut_colours` | the picture header's `clutColors` |
| `bytes` | `0x10` plus the picture's `totalSize`, its length in the file |

[`handbook-files-strings.tsv`](handbook-files-strings.tsv):

| Column | Meaning |
|---|---|
| `language`, `family` | the tree and the family |
| `bundle` | the `hdat` file number |
| `entry`, `record` | the entry number, and `entry - first`, the record in the bundle |
| `slot` | the text slot, from 0 |
| `string_entry_at` | `stringsAt + string[slot]`, the string entry's offset in the file |
| `text_at`, `line_operations` | the string entry's `textAt` and `opCount` |
| `text` | the string, written as the [Clan Primer text](../Menus-And-HUD/text-handbook.md) table writes it: text codes as the placeholders of [Text codes](../Menus-And-HUD/text-codes.md), a Bestiary bundle's characters through its own expansion list, Traveler's Tips expansion characters as `{exp:0xN}`; the `story`, `world`, `person` and `knowledge` text is decoded with the Japanese font in every tree, as in [Unrequested handbook text](../Menus-And-HUD/text-handbook-unrequested.md) |

## Loader behaviour

### The data manager and its three slots

The data manager `0x005771F0`, published at `0x02CA9738`, creates three load slots (`0x00575870`) at its
`+0x108`, `+0x110` and `+0x118`: slot 0 holds the catalog, slot 1 a text bundle, slot 2 a picture bundle.
A request names a family, a file number and an entry or page. `0x00575C30` builds the id as
`[0x00D23740 + 2 x family]` plus the slot's offset plus, for slots 1 and 2, the file number:

- slot 0 has offset 0, so it loads the catalog;
- slot 1 starts with offset 2 (`0x005759E2`), so file number `n` is `menuhandbook_<family>NNN.dat` with `NNN = n`;
- slot 2 gets `textBundles + 2` once the catalog has loaded (`0x005773D2`), so its file numbers count from the first picture file.

`0x00575C30` files the request in a request group (`0x00249580`, closed with `0x00249410`) as
`0x00249210(group, 7, id, arena, top)`: slot 0 in arena 3, slots 1 and 2 in arena 2, and slot 2 with `top` = 1, so
its block comes from `0x0036A190` instead of `0x0036A100` (`0x00575C5B`-`0x00575CAD`). It sets the state to 2, keeps the
family, file number and entry or page at `+0xD2`, `+0xCC` and `+0xCE` (`0x00575CC7`-`0x00575CE9`) and returns the
request's buffer (`0x00575CF0`), which stays null when the size table gives no positive size.

`0x00575A50` treats a request for the slot's own file (the same family `+0xD2` and, when the slot byte
`+0xC8` is 1 or 2, the same file number `+0xCC`; `0x00575A60`-`0x00575A92`) by the slot's state `+0xC9`:

- loaded (1): it only changes the entry or page `+0xCE` and returns 1 (`0x00575B58`-`0x00575B63`);
- loading (2): the request is dropped, with no write (`0x00575B4B`);
- loading with the buffer to be freed when it finishes (3): the state goes back to 2 (`0x00575B44`), so the
  finishing load is kept.

The slot's procedure `0x00575870` handles four messages:

- `0x10`, the load's completion: state 2 becomes 1, `0x00575710` runs and the owner `+0xC0` gets message `0x10`
  with the slot number `+0xC8` (`0x005758D3`-`0x0057594E`, `0x00247510`). State 3 frees the buffer (`0x003697F0`),
  becomes 0 and reports the slot number plus 3, after refiling a queued request when the queue count `+0xD3` is
  above 0 (`0x005758F1`-`0x0057594E`). Any other state ignores it.
- `1`, creation: the slot number and owner from the creation record, state 0, `+0xCA` = 0 (2 for slot 1,
  `0x005759E2`), `+0xD0` = `0xFFFF`, and `+0xEC`, `+0xD3`, `+0xF0` and `+0xF8` cleared; it then registers with the
  manager `[0x02CA9738]` (`0x00244960`, `0x005759F8`).
- `2`: when bit `0x1` of `+0xEC` is set and the state is 0, it clears the bit and closes the slot (`0x00244F00`,
  `0x00575982`).
- `0x12` goes to the owner with the slot number (`0x005758B8`); every other message goes to `0x005C5230`
  (`0x0057589F`).

Any other request, including one for a different file while a load is pending, frees the slot's buffer and
loads the new file (`0x00575640` at `0x00575B20`, `0x00575C30` at `0x00575B2B`), keeping the new buffer at `+0xF0`
(`0x00575B30`). A slot byte above 2 matches no request (`0x00575A85`). `0x00575A50` returns 1 in the loaded case only.

Every such request also stores 0 in the queue count `+0xD3` (`0x00575AB4`), as creation does (`0x005759C9`). The
queue entries from `+0xD4` and the count's increase are written only by code that no path reaches
(`0x00575ACC`-`0x00575B10`), so the count stays 0, the completion never refiles and no request waits.

#### A load replaced while it is pending

Of the four calls of `0x00575A50`, the completion's queue call (`0x00575931`) is never reached, and the other three
come from two requesters. Neither tests whether the slot is busy: the busy test `0x00576DA0` has one caller, the
content page's page turn inside an entry (`0x005745C1`).

- slot 0: `0x00577880(family)` (`0x005778C8`), which the mid pane `0x0056F2A0` calls (`0x0056F351`) when the player
  confirms Traveler's Tips or the Bestiary in the Clan Primer. Confirming the other one while the first catalog
  is still loading sends a different file. Hunts and Sky Pirate's Den call `0x005776D0` instead (`0x0056F2CF`).
- `0x005776D0` turns a loading slot's state 2 into 3, so that load is kept and freed when it completes
  (`0x00577714`, `0x00577750`, `0x0057778C`), and sets bit `0x40`, which makes `0x00577880` and `0x005778F0` refuse
  (`0x00577893`, `0x0057790D`).
- slots 1 and 2: `0x005778F0(entry)`, through `0x00575D10` (`0x00577969`) and `0x00575DD0` (`0x005779BE`), when an entry
  page opens (`0x00570280`). The mid pane opens one each time the player confirms an entry in the family index
  (`0x0056F1B8`; `0x0056F1F6`, `0x0056EC10`).
- Opening an entry whose text bundle or picture file differs from the one still loading for the previous entry
  sends a different file to that slot. Traveler's Tips always asks slot 2 for page 0's file, so for it only
  slot 1 changes file.

Freeing the buffer of a pending load does not cancel its read. The read completes into the freed block, and its
completion marks the new load done before the new read has finished:

1. `0x00249210` returns its 40-byte request record (`0x00249301`): `+0x00` the group, `+0x08` the buffer
   (`0x002492DE`), bit `0x1` of `+0x20` busy. It drops the id `0x0032E620` returns (`0x002492F3`), and `0x00575C30`
   returns only the record's `+0x08` (`0x00575CF0`), which becomes `+0xF0` (`0x00575B30`). The slot keeps the
   buffer, not the request.
2. `0x00575640` frees `+0xF0` through `0x003697F0` and `0x00369860` (`0x005756C7`), which work on the heap alone: the
   in-use bit `0x1` of the block's `+0x14` is cleared (`0x00369B09`), its size comes off the arena counts
   (`0x00369B18`, `0x00369B34`) and it is merged with free neighbours. The read queue's cancel `0x0032E590` is called
   only at `0x002FC426`, `0x003B13AF`, `0x003B17BD` and `0x003B199D`.
3. The read keeps the freed block as its destination. `0x0032E870` files at the tail of the pending list and the
   pump `0x0032E070` serves the head, so the earlier read completes first and writes the earlier file there.
4. Its completion `0x002495C0` counts it on the earlier group, whose widget is the slot (`0x00249580` at `0x00575C92`,
   `0x002495B7`), and calls the slot's first word with message `0x10` (`0x0024960B`-`0x00249632`). That word is
   `0x00575870`, written at creation (`0x00575848`; `0x00244F50`, `0x00246641`).
5. The new load has set state 2 (`0x00575CC7`), so `0x00575870` sets state 1, runs `0x00575710` over the new buffer
   before the new read has written it (`0x005758D3`-`0x005758DA`) and reports the slot ready to its owner `+0xC0`
   (`0x00575942`-`0x0057594E`). The new read's own message `0x10` then finds state 1 and changes nothing
   (`0x005758E9`, `0x005759FD`).

### The unlock tables

`0x00576F50` first tests whether the text groups 7 and 8 are resident (`0x002F8040`); for each one that is not it sets bit
`0x10` or `0x20` of the manager's `+0x100` and adds the group to its request group (`0x002491B0`). When the
bits `0x4`, `0x10` and `0x20` are all clear it returns 0 (`0x00576F83`-`0x00576F8C`).

With its creation flag (bit `0x4`) set, `0x00576F50` loads the six unlock tables (base + 1) into the manager's
`+0xC8` to `+0xF0` and `menuquest.dat` (`0x128`) into `+0xF8`, each through `0x00249210(group, 7, id, 3, 0)`, and
sets bit `0x2` (`0x0057706F`). It closes the group (`0x00249410`) and returns 1.

`0x00577550(family)` evaluates them. It answers 0 when the manager is missing or bit `0x2` is set (`0x00577567`), for
a negative family or one above 7, and when the family's table is missing; otherwise it answers 1:

- families 0-4: each record through `0x00575E80`, the result written as the entry's unlock bit through
  `0x00315910(byte [0x00D23750 + family], entry, result)`;
- Bestiary: for each entry and slot, slot 7 and every empty slot get their read mark set
  (`0x00315AD0(6, entry, slot, 1)`); the slot thresholds are not saved. The entry's mode comes from `0x005768E0`
  and each threshold from `0x00576860` (`0x005775EB`, `0x00577608`);
- family 6 does nothing, and family 7 runs the field-frame sweep `0x00316930` (`0x005775B2`).

`0x00576E30(family, entry, slot)` answers whether a Bestiary slot is open, each time it is asked; other families
always answer yes. An empty slot (`0xFF` in mode 0, `0xFFFF` in modes 1 and 2) answers no (`0x00576EB3`,
`0x00576ED3`, `0x00576EFF`), and so does every slot from the eighth on, for which `0x00576860` returns the empty value.

Mode 0 compares the entry's kill count (`0x00315420`) with the threshold and opens at a count of at least the
threshold, compared unsigned (`0x00576EC4`). The count −1, which `0x00315420` gives an entry whose save byte
`+0x3404` is still 0, therefore passes every threshold. Mode 1 compares the story counter: `0x00265270` taken as a
signed 16-bit value, compared unsigned with the threshold (`0x00576F0C`-`0x00576F11`). Mode 2 opens when this monster
or the monster the threshold names has a kill: a count above 0 for this one, at least 1 for the other
(`0x00576EE4`, `0x00576EF0`).

#### The Bestiary kill count

`0x00315420(entry)` reads the count from the save `[0x020927C0]` (`0x002536A0`): an entry of `0x200` or more gives -1
(`0x0031542C`), a byte `+0x3404` + entry of 0 gives -1 (`0x0031544A`), and any other byte gives the byte less 1
(`0x00315469`). `0x00315820` stores the count plus one there for each counted defeat (`0x0031588E`).

`0x00576E30` is asked only about a listed entry: by the slot list `0x00576300` (`0x005764A9`), by the read count
`0x00576920` after the unlock test `0x003154B0` (`0x0057697E`, `0x005769EA`) and by the index row's read test `0x00576D20`
(`0x00576D5A`, from `0x00570930` at `0x0057095D`). An entry without a rule is listed only once its count is above 0,
so a count of -1 meets a mode 0 test only for an entry a rule of `menuhandbook.bin` opens.

Every language's path array names the `in` copy of `menuhandbook.bin` (`ch` for KR, CH and CN; the two copies
hold the same rules). Of the 15 entries a rule opens, the one with mode 0 slots is Rogue Tomato (211), in the us
`menuhandbook_monster.dat` alone; every other copy in the archive gives it mode 1
([Clan Primer entries](../Menus-And-HUD/clan-primer-entries.md)). The UK size table gives the `uk` catalog and table
(kind 7, ids `0x354` and `0x355`) -1, so `0x00249210` files no request for them (`0x0024929F`).

### Reading the catalog

- `0x005778F0(entry)` opens an entry: `0x00575D10` asks slot 1 for the record's `bundle` with the entry
  number, then `0x00575DD0` asks slot 2 for the record's `page`, and it returns 1. It returns 0 and asks nothing
  while the manager is cancelling (`+0x100` bit `0x40`, `0x0057790D`), or when slot 0's family is `0xFF`, its
  catalog is not loaded, or the entry is negative or not below `entryCount` (`0x00577922`-`0x0057795F`), and with no
manager at `0x02CA9738` (`0x00577903`). After `0x00575D10` it reads slot 0 again and returns 0 without asking slot 2 if
those catalog tests no longer pass (`0x0057796E`-`0x005779B3`).
- `0x00575D10(manager, family, entry)` acts only when slot 1 exists, the catalog is loaded and the entry is below
  `entryCount` (`0x00575D1A`-`0x00575D66`). It clears slot 1's bit `0x100` of the manager's `+0x100` (`0x00575D8B`)
  and, when slot 1 already holds that bundle (`0x00575A50` answers 1), sends the manager message `0x10` with 1 at
  once, the message a finished load sends (`0x00575DBA`).
- `0x00575D10` takes slot 0 from the manager at `0x02CA9738`, not from its argument (`0x00575D32`-`0x00575D3D`), and
  reads the slot's state byte (`0x00575D44`) ahead of the slot's null test (`0x00575D4E`), so a null slot 0 makes
  that a read at address `0xC9`; its one caller `0x005778F0` tests the manager and slot 0 first (`0x00577900`,
  `0x00577922`). The record address is a 32-bit sum of the catalog pointer and `recordsAt` (`0x00575D70`).
- `0x00575DD0` and the second read in `0x005778F0` have the same order: the state byte of slot 0 is compared
  (`0x00575DF8`, `0x0057797C`) before the slot's null test (`0x00575E01`, `0x00577986`).
- `0x00575DD0` bounds the page by `pageCount`, takes `pageMap[page]` as the file number and the page as the
  picture. Its `0xFFFF` test compares the zero-extended word with -1 (`0x00575E26`), so it never matches.
- `0x00575DD0` acts only when slot 2 exists and the catalog is loaded (`0x00575DDD`-`0x00575E10`). It clears bit
  `0x200` of `+0x100` (`0x00575E2C`) and, when slot 2 already holds that file, binds the page at once (`0x00575B80`,
  `0x00575E5C`) and sends message `0x10` with 2 (`0x00575E72`).
- `0x005760A0(record, entry)` fills the 32-byte detail record, which it first zeroes: the name `+0x00`, the
  section `+0x10`, the entry number `+0x12`, the flag `+0x14`, and for the Bestiary the kill count `+0x16` (a
  count of −1 kept as 0, `0x00576233`) and, from the slot-count byte (`+0x15`), each slot's threshold (`0x00576860`).
- `0x005760A0` keeps each threshold as one byte from `+0x18`, the low byte of the `u16` (`0x005762B5`). It answers 1,
  or 0 when the manager or the catalog is missing or the entry is negative or not below `entryCount`
  (`0x005760D4`-`0x00576122`); a name of -1 leaves `+0x00` at 0.
- Bestiary text ids `0x4210` to `0x421C` also get a second line, an Esper's name read through `0x0035D330`.
- That line is kept at `+0x08`: `0x0035D330(0x14, 0x106 + t)`, its `+0x18` read by `0x002B58B0`, with `t` = 0, 11,
  9, 8, 3, 4, 6, 1, 5, 2, 7, 10 and 12 for ids `0x4210` to `0x421C` (the words at `0x00D237A0`, `0x00D23790` and
  `0x00D237B0` and the 12 at `0x005761BE`; `0x0057619B`-`0x005761FF`).
- `0x00576030(header)` copies the catalog header: slot 0's family `+0xD2` to `+0x00`, the word `+0x08` shifted
  right by 4 to `+0x04`, `sectionCount` to `+0x06`, `entryCount` to `+0x08` and `pageCount` to `+0x0A`. It
  answers 1, or 0 with nothing written when slot 0's state byte `+0xC9` is not 1 or its catalog pointer
  `+0xF0` is null (`0x0057603E`-`0x0057608F`).
- `0x00576030` tests neither the manager `[0x02CA9738]` nor slot 0 before it reads them: it loads slot 0 from the
  manager's `+0x108` (`0x00576037`) and reads the slot's state byte (`0x0057603E`) ahead of the slot's null test
  (`0x00576047`), so a null manager makes that a read at address `0x108` and a null slot 0 a read at address
  `0xC9`.
- `0x00576740(record, section)` gives a section's caption, its first entry, its entry count and the number of its
  entries that pass the family's unlock test for that entry (`0x00576CA0`, `0x003154B0`).
- `0x00576740` writes the caption `+0x00` (from `0x00576A50`), the section `+0x08`, the first entry `+0x0A` (`0xFFFF`
  when no entry lists it), the count `+0x0C` and the unlocked count `+0x0E`, the family being the low nibble of
  the catalog's `+0x08`. It answers 1, or 0 when `0x00576A50` answers 0 (`0x0057678B`) or the catalog is not loaded.

### Section captions

`0x00576A50(section)` returns the caption text. Without a gate, or with a gate that lists no conditions and
no maps, the caption is the message `caption[section]`. Otherwise it is shown when any condition id passes
`0x00309EC0`, or any listed map has at least one bit set in its 32-byte bit set (`0x00255120`; for the
current map the live set, `0x00255060`); when no condition or map passes, the caption reads message `0x3EC`
(`0x002F9860`).
A caption of -1 yields no text.

A section has a gate when `gateCount` is above 0 and above the section (`0x00576AF5`-`0x00576B06`). A condition passes
when `0x00309EC0(id, 0)` answers above 0 (`0x00576B6A`); the current map is `0x003779F0(0x003148F0())`
(`0x00576B81`-`0x00576B88`). The caption record holds the text at `+0x00` (0 for a caption of -1), the section at
`+0x08` and the gate's low nibble at `+0x0A`, or `0xFF` without a gate (`0x00576C09`-`0x00576C43`).
`0x00576A50` answers 1, or 0 with nothing written when the manager is missing, the catalog is not loaded or the
section is not below `sectionCount` (`0x00576A66`-`0x00576AAB`).

The same two map-bit tests serve the achievement check `0x003160C0`, which needs every map flagged in
`menuhandbook.bin` to have a revealed tile
([achievements](../Steam-And-Achievements/achievements.md)). The Clan Primer's index builder
`0x00571F60` reads the entries through `0x00576030`, `0x005760A0`, `0x00576740`, `0x00576CA0` and `0x00577550`
([Clan Primer](../Menus-And-HUD/clan-primer.md)).

### Entry text

`0x00576300` builds the open entry's lines from slot 1's bundle. The entry number must lie in the bundle's
window `first` to `first + count - 1`; `recordAt[entry - first]` gives the record. Slots are read in order
and the first one `0x00576E30` refuses ends the list, so Bestiary lore appears slot by slot as its thresholds
are met. Each string's text is `entry + textAt`; `0xFFFF` gives an empty line (`0x01CEB638`).

The entry number is slot 1's `+0xCE` and the family slot 0's `+0xD2` (`0xFF` without slot 0). The line record,
`0x50` bytes zeroed first (`0x00576317`), gets the entry at `+0x00`, the number of lines at `+0x03` (`0x0057650F`), one
text pointer per line from `+0x08` and the record tail at `+0x48` to `+0x4E`. `0x00576300` answers 1, or 0 when
the manager is missing, slot 1 holds no loaded bundle or the entry lies outside the window
(`0x00576323`-`0x0057639E`).

When the entry page shows a line (`0x00574900`), it runs that string's line program (`0x00577A40`). The
nibbles and bits are the ones the unlock records test:

| `op` | Effect |
|---|---|
| 0 | set save nibble `index` to `value`, at most 15 (`0x00315CD0`) |
| 1 | set save bit `index` when `value` is 1, else clear it (`0x00315A20`) |
| 2 | add `value` to save nibble `index`, at most 15 |
| 3 | subtract `value` from save nibble `index`, at least 0 |
| 4 to 255 | nothing (`0x00577B2A`) |

`0x00577A40(line)` takes the string of that slot of the open entry (slot 1's `+0xCE`) and answers 1, or 0 when
slot 1 holds no loaded bundle, the entry lies outside its window or the line is not below the record's `slots`
(`0x00577A83`-`0x00577AD6`).

For the Bestiary the program runs only while the slot's read mark is clear (`0x00576F30`): `0x00574900` sets the
mark (`0x00577A20`, `0x0057497C`) and then runs the program (`0x00574996`). For the other families it runs every time a
line is shown, and the entry is marked read on its last line, the line equal to the line record's `+0x03`
less 1 (`0x0057494B`-`0x0057495C`).

### The glyph sheet

`0x00575710` runs when a slot finishes loading (`0x005758DA`). For slot 2 it binds the picture (`0x00575B80`,
`0x00575746`); for slot 0 it does nothing. When slot 1 finishes loading, `0x00575710` registers the bundle's sheet
when `sheet` is not -1 (`0x0039BEC0`), keeping the sheet's address, formed with a 32-bit addition, at `+0xF8`
(`0x00575763`-`0x00575765`); a `sheet` of -1 stores 0 there (`0x005757EC`).

With a sheet, for `tutorial` it also calls `0x0017FBC0(6)`; for `monster` it registers it as font
`handbook_monster<NNN>.txt`, `NNN` the bundle number (`0x0017FA90`, `0x0017F790`): it prints the name from the format at
`0x00D23770` (`0x0017D2E0`), then calls `0x0017FA90(NNN + 1, 1, name, 7)`, `0x0017FB70(NNN + 1)`,
`0x0017F790(NNN, sheet)` and `0x0017FBE0()` (`0x00575782`-`0x005757D9`). The other families register the sheet alone.

A text writes a sheet character as two bytes, shown as `{exp:0xN}` in the tables:

- **Code.** `0x002AC2F0` takes the value for the lead byte's low nibble from the table at `0x00916570`, or from the
  table at `0x009165B0` when `[0x0209CC38]` is set, plus the second byte less `0x20` (`0x002AC399`-`0x002AC3BC`).
  `0x002AB7D0`, the word's only writer, sets it to 1 for the same locales for which it picks `0x1C` below.
- **Sheet or font.** A lead at or above `[0x01E0CDF8]` is drawn from a sheet. `0x002AB7D0` sets that word to `0x18`, or
  to `0x1C` for the locales its test picks (`0x002AB7D9`-`0x002AB7E9`).
- **Record.** The sheet block is the renderer's `+0x68`, or `0x0039BA30` of its font slot `+0xA6`
  (`0x002AC417`-`0x002AC440`), and the record is `0x0020E600([block + 0x0C]) + 8 × code` (`0x002AC498`-`0x002AC4A7`).
- **Cell.** The bits under mask `0x3FF` of the record are x, `0xFFC00` y, `0x1F00000` width and `0x3E000000` height, as `0x002B0280` reads them
  (`0x002B08BC`-`0x002B0918`).

The `story`, `world`, `person` and `knowledge` bundles are the same bytes in all nine trees, and so are their 796
sheet glyphs. Each glyph was matched against the JIS X 0208 characters drawn in seven faces of the Japanese system
fonts MS Gothic, MS Mincho, Meiryo and Yu Gothic. A glyph
counts as decoded when its best match leads the second by at least 0.011 and the word it makes reads in its
sentence. That decodes 753 of the 796.

The other 43 are 25 distinct cells: the same pixels stand in several bundles (由 five times). Each was read from its
4-bit values. The five sheets are drawn in one face, so a part the character shares with a decoded glyph repeats in
the same place: the left part of 嫡 matches the 女 of 妙 with one pixel whose 4-bit values differ by more than 2,
against 32 such pixels for the 扌 of 括.
The part that tells a character from its look-alike was read stroke by stroke: 由 carries its middle upright above
the box, and 田 does not.

Glyph `0xA5` of the `world` sheet has the same pixels as 搭, glyph `0xB4` of the first `knowledge` sheet, and its
text writes 搭と周辺; the `world` sheet holds 塔 as `0x9E`. All 796 glyphs are decoded:

| Family | Glyphs | By match | By cell | Uses |
|---|---:|---:|---:|---:|
| `story` | 124 | 119 | 5 | 267 |
| `world` | 207 | 196 | 11 | 569 |
| `person` | 184 | 175 | 9 | 506 |
| `knowledge` | 281 | 263 | 18 | 500 |

No string of the four families holds an undecoded character
([`handbook-files-strings-decoded.tsv`](handbook-files-strings-decoded.tsv)). 49 of the 300 entries give their
name in their own text ([`handbook-files-entry-names.tsv`](handbook-files-entry-names.tsv)).

The catalog record's name, `+0x00`, is a text id that `0x002F9920` finds in `penelosdiary.bin` (group 7), as the row
whose own id it is. For 58 entries that row holds a name: 57 `world` entries and one `knowledge` entry. The ids of
the other 242 entries, and the 25 section captions of the four families, find rows that point at one string, offset
`0xAB0` of the text block, as 589 of the file's 682 rows do in every tree. That string is empty in `us` and `it`,
`/Unused` in `de`, `DUMMY` in `es`, `NOT USED` in `fr`, and `／` in `in`, `kr`, `cn` and `ch`.

Of those 242 entries, 48 give their name in their text. No field of the records of the other 194 holds a name
([`handbook-files-entry-name-ids.tsv`](handbook-files-entry-name-ids.tsv)):

- the catalog record: the name id above, the section, the bundle, the page of a picture, the flag (0 in all 194)
  and a zero byte;
- the unlock record: its tests and the marker byte;
- the text-bundle record: the slot count, the serial byte, the entry number (equal to the entry in all 194), the
  string offsets and the tail. Every byte of the five bundles is one of these fields, a string entry, its text, a
  zero byte or the glyph sheet, except two bytes before the first record that no offset names
  (`menuhandbook_world000.dat` `0xA6`-`0xA7`, `menuhandbook_person000.dat` `0x84`-`0x85`);
- the text: the first line of slot 0 is a sentence ending in 。 in 192 of them, and `story` entry 24 and `knowledge`
  entry 17 hold only 現在不使用.

[`handbook-files-glyphs.tsv`](handbook-files-glyphs.tsv):

| Column | Meaning |
|---|---|
| `language`, `family`, `bundle`, `N` | the tree, the family, the `hdat` number and the sheet record `N` of `{exp:0xN}` |
| `character` | the decoded character |
| `best_score`, `second_score`, `best`, `second` | the two best matching characters and their scores |
| `context` | one use, with the glyph in brackets and six characters each side |
| `candidates` | `jis` when the best match was taken over JIS X 0208; `game` when it was taken over the characters of the game's own `jp` fonts, after no JIS character led by 0.011; `cell` when the character was read from the cell |
| `decision` | `corpus:` words of the game's other Japanese text that hold the decoded word; `reading:` the word read in the sentence; `cell:` the parts of the cell, by row and column of its 4-bit values, the decoded glyphs whose parts they repeat with the count of pixels apart by more than 2, and the strokes that tell it from its look-alike |

[`handbook-files-entry-name-ids.tsv`](handbook-files-entry-name-ids.tsv):

| Column | Meaning |
|---|---|
| `family`, `entry` | the entry |
| `name_text_id` | the catalog record's `+0x00` |
| `text_row` | the row of `penelosdiary.bin` whose own id it is (`0x002F9920`) |
| `us` to `ch` | that row's string in each tree, as the [string tables](../Menus-And-HUD/text-string-tables.md) give it; `-` for an empty string |
| `text_name`, `text_name_rule` | the name the entry's text gives and the rule, from [`handbook-files-entry-names.tsv`](handbook-files-entry-names.tsv); `-` when the text gives no name |
| `first_line` | the first line of slot 0, with each sheet character in place |

### Pictures

`0x00575B80` binds a picture when slot 2's page lies in the file's window and differs from the bound one: it
registers the TIM2 at `pictureAt[page - first]` as the image label `hb_tex` (`0x0024A440`). It needs slot 2 with a
buffer, and compares the page `+0xCE` with the window and with the bound page `+0xD0` (`0x00575B86`-`0x00575BC9`).

`0x00575B80` first releases the bound label (`0x00575A10`: `0x0024A680` on `+0xF8`, then `+0xF8` = 0 and `+0xD0` =
`0xFFFF`). It forms the picture's address with a 32-bit addition, registers it as `0x0024A440(picture, "hb_tex", 2)`
and keeps the label at `+0xF8` and the page at `+0xD0` (`0x00575C0D`-`0x00575C20`).

`0x00575B80` does nothing for `tutorial` (`0x00575BD2`), so Traveler's Tips shows no picture: the entry page still
requests the page's file into slot 2 (`0x005778F0` → `0x00575DD0`, which has no family test), so
`menuhandbook_tutorial001.dat` loads, but no `hb_tex` label is made, and the picture pane `0x00570630` draws nothing
because `0x00576C70`, its only source, returns slot 2's label `+0xF8`, which stays 0 (`0x0057068E`).

The Clan Primer opens only the `tutorial` and `monster` families ([Clan Primer](../Menus-And-HUD/clan-primer.md)), so of the
other four only the unlock tables load (`0x00576F50`); their catalogs, text bundles and picture bundles, 990 files,
get no id from a kind 7 site, formula or table with the shipped data. Slot 2 asks only for the file the open
entry's page maps to, so the picture bundles no page-map slot names get no id either: seven `tutorial` files in each language and the 2, 3 and 7 extra
`monster` files of `kr`, `ch` and `cn`.

Of the 2,930 files, a kind 7 site, formula or table gives the id of 1,865 with the shipped data: the 54 unlock tables, and the catalogs, text bundles and named picture
bundles of Traveler's Tips and the Bestiary. [`myoshiok-file-meanings.tsv`](myoshiok-file-meanings.tsv) gives each
file's kind 7 id, request site and the entries it holds.

### Address width

The readers form addresses inside the loaded files with 32-bit additions (`0x00575E1F`, the catalog
record in `0x005760A0`, the sheet in `0x00575710`, the picture in `0x00575B80`), so each buffer must lie below 4 GB.

## Modding notes

- Entry count, page count, section count and `textBundles` in the catalog bound every lookup; keep them equal to
  what the files hold. The unlock table's `count` must equal `entryCount`, and the text bundles' windows must cover
  every entry, in order, since an entry is looked up only in the bundle its record names.
- A page-map value of `0xFFFF` is not treated as missing; it requests file `textBundles + 0xFFFF`.
- New numbered files need a path in the kind-7 array (`story099`, `world049`, `person029`, `knowledge029`,
  `tutorial049` and `monster299` are the last) and an entry in the language's size table
  ([File size tables](file-size-tables-fst.md)).
- Bestiary lore appears in slot order and stops at the first locked slot; a slot after a locked one never shows.
- Set the Bestiary slot-count byte to the bundle record's `slots`; the detail record copies that many thresholds.
- A line program changes save nibbles and bits each time its line is shown; shipped strings have no line program.
- Traveler's Tips pictures are never drawn, whatever the page map says: the only binder, `0x00575B80`, refuses
  family 4 (`0x00575BD2`). Only `tutorial001` is ever loaded (page 0, a 1,024 x 448 parchment); `tutorial002` to
  `tutorial008` hold pages 4 to 29, which the one-page page map cannot name, and all 26 are the same "Dummy"
  placeholder with the page number.

## Related

- [Clan Primer](../Menus-And-HUD/clan-primer.md): the pages that show these files, the unlock and read marks, and `menuhandbook.bin` and `menuhandbook_order.bin`.
- [TIM2 images](tim2-images.md): the picture and glyph-sheet format and the registry the sheets enter.
- [Battle text tables](battle-text-tables.md): the bank words the Bestiary names resolve through.
- [File size tables](file-size-tables-fst.md): the kind-7 path arrays and sizes.
- [File requests and the read queue](file-requests-and-the-read-queue.md): how the slots' kind-7 requests are read.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md): the kill counts the Bestiary slots test.
- [Story progress](../Story-Events-And-Hunts/story-progress.md): the story counter the unlock records test.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x003148F0` is called by `0x00261F90`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x003148F0` is called by `0x0033A720`, `0x003ED190`, `0x003ED3F0`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
- Save load settings: `0x00249210` is called by `0x00582790`; `0x00249410` is called by `0x00582790`; `0x00249580` is called by
  `0x00582790`; those functions are documented on [mrp menu resource packages](mrp-menu-resource-packages.md).
- Spawn encounter lifecycle: `0x003148F0` is called by `0x00233780`; those functions are documented on
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md).
- World area: `0x0024A680` is called by `0x003C63A0`; `0x0032E620` is called by `0x00378540`; `0x0036A190` is called by
  `0x00378540`; those functions are documented on [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md),
  [ps2data bin families](ps2data-bin-families.md).
