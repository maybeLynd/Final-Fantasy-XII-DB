---
title: "Handbook files: the hctg, hchk, hdat and himg files behind Clan Primer entries, how each is read, and what each field shows"
kind: "format"
category: "Game files and data tables"
addresses: "0x005771F0, 0x00576F50, 0x00575870, 0x00575C30, 0x00575A50, 0x00575710, 0x00575B80, 0x005778F0, 0x00575D10, 0x00575DD0, 0x00576030, 0x005760A0, 0x00576740, 0x00576A50, 0x00577550, 0x00575E80, 0x00576860, 0x00576E30, 0x00576300, 0x00577A40, 0x00574900, 0x00D23740, 0x02CA9738"
---

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
| `+0x12` | `u16` | sectionCount sections; bounds every caption index (0x00576A50) |  |
| `+0x14` | `u16` | textBundles | number of hdat files; the first picture file follows them (`0x005773D2`) |
| `+0x16` | `u8[2]` | pictureFiles number of picture files the page map names; read by no function: the catalog readers 0x005778F0, 0x00575D10, 0x00575DD0, 0x00576030, 0x005760A0, 0x005766E0, 0x00576740 and 0x00576A50 (the functions that load [slot 0 +0xF0]) read nothing at +0x16; nothing fixes its width |  |
| `+0x18` | `i32` | caption[sectionCount] | text id of each section caption; -1 = none |

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
| `+0x00` | `i32` | text | name; -1 = none. Families 0-4: message id (`0x002F9920`); Bestiary: battle-text word (`0x003214B0`, `0x002B58B0`) |
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
| `+0x0A` | `u8[2]` | unused | 18 or 0; read by no function: the six tables, manager `+0xC8` to `+0xF0`, are read only by `0x00577550` (`0x005775C1`, `0x00577660`), which walks the records with `0x00575E80`, and neither reads `+0x0A`; nothing fixes its width |
| `+0x0C` | `rec[count]` | 8 bytes each, 16 for the Bestiary |  |

Families 0-4, 8 bytes per entry, evaluated by `0x00575E80`. A field holding all ones (`0xFF`, `0xFFFF`) is
skipped; every other field must hold:

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

### hdat: a text bundle

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "hdat"; the loaders ignore it |
| `+0x04` | `u32` | version | 103; not read |
| `+0x08` | `u16` | first | entry number of the bundle's first record |
| `+0x0A` | `u16` | count | records; the bundle holds entries first to first + count - 1 |
| `+0x0C` | `i32` | sheet | offset of a TIM2 glyph sheet; -1 = none (`0x00575710`) |
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
| `+0x00` | `u16` | textAt | offset of the text from the entry itself; `0xFFFF` = none (an empty line) |
| `+0x02` | `u8` | opCount | line-program operations (`0x00577A40`) |
| `+0x03` | `u8` | pad |  |
| `+0x04` | `...` | {u8 op, u8 index, u8 value, u8 pad}[opCount] |  |

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
| [`handbook-files-glyphs.tsv`](handbook-files-glyphs.tsv) | 7,164 | sheet glyph of a `story`, `world`, `person` or `knowledge` bundle in each tree: its character where decoded, the two best match scores and one use |
| [`handbook-files-strings-decoded.tsv`](handbook-files-strings-decoded.tsv) | 2,952 | the string entries of those four families, with each decoded sheet character in place |
| [`handbook-files-entry-names.tsv`](handbook-files-entry-names.tsv) | 49 | entry whose text gives its name: the name and the rule that gives it |

`handbook-files-files.tsv`:

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

`handbook-files-entries.tsv`:

| Column | Meaning |
|---|---|
| `language`, `family`, `entry` | the entry; `entry` is the record index in the catalog |
| `name_text` | record `+0x00`: families 0-4 a message id, the Bestiary a battle-text word; `none` for -1 |
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
| `nibble_index`, `nibble_value`, `bit_index`, `marker`, `story_flag`, `story_minimum` | families 0-4: the unlock record's fields, `none` for a field of all ones; empty for the Bestiary |
| `slot_mode` | Bestiary: 0, 1 or 2 from the unlock record's `mode`; empty for the other families |
| `slot_mode_word` | Bestiary: the unlock record's `+0x0E` |
| `slot_thresholds` | Bestiary: the seven slot words in order, `empty` for `0xFF` in mode 0 and `0xFFFF` in modes 1 and 2 |
| `unlock_test` | the record's tests in words: for families 0-4 each field that is not all ones, or `none`; for the Bestiary what the slot thresholds count |

`handbook-files-sections.tsv`:

| Column | Meaning |
|---|---|
| `language`, `family`, `section` | the section |
| `caption_text` | `caption[section]`, a message id; `none` for -1 |
| `entries`, `first_entry` | the number of entries whose `section` is this one, and the lowest of them |
| `gate` | `yes` when `gateAt` has an offset for the section |
| `gate_low_nibble` | the gate's `flags` low nibble |
| `conditions`, `condition_ids` | the gate's condition count C and its ids |
| `maps`, `map_numbers` | the gate's map count M and its map numbers |

`handbook-files-page-map.tsv`:

| Column | Meaning |
|---|---|
| `language`, `family`, `page` | the page number |
| `page_map_value` | `pageMap[page]` |
| `picture_file`, `picture_file_name` | `textBundles + pageMap[page]` and that file |
| `picture_in_file` | `page - first` of that file |

`handbook-files-pictures.tsv`:

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

`handbook-files-strings.tsv`:

| Column | Meaning |
|---|---|
| `language`, `family` | the tree and the family |
| `bundle` | the `hdat` file number |
| `entry`, `record` | the entry number, and `entry - first`, the record in the bundle |
| `slot` | the text slot, from 0 |
| `string_entry_at` | `stringsAt + string[slot]`, the string entry's offset in the file |
| `text_at`, `line_operations` | the string entry's `textAt` and `opCount` |
| `text` | the string, written as the [Clan Primer text](../Menus-And-HUD/text-handbook.md) table writes it: control codes as the placeholders of [Text codes](../Menus-And-HUD/text-codes.md), a Bestiary bundle's characters through its own expansion list, Traveler's Tips expansion characters as `{exp:0xN}`; the `story`, `world`, `person` and `knowledge` text is decoded with the Japanese font in every tree, as in [Unrequested handbook text](../Menus-And-HUD/text-handbook-unrequested.md) |

## Loader behaviour

### The data manager and its three slots

The data manager `0x005771F0`, published at `0x02CA9738`, creates three load slots (`0x00575870`) at its
`+0x108`, `+0x110` and `+0x118`: slot 0 holds the catalog, slot 1 a text bundle, slot 2 a picture bundle.
A request names a family, a file number and an entry or page. `0x00575C30` builds the id as
`[0x00D23740 + 2 x family]` plus the slot's offset plus, for slots 1 and 2, the file number:

- slot 0 has offset 0, so it loads the catalog;
- slot 1 starts with offset 2 (`0x005759E2`), so file number `n` is `menuhandbook_<family>NNN.dat` with `NNN = n`;
- slot 2 gets `textBundles + 2` once the catalog has loaded (`0x005773D2`), so its file numbers count from the first picture file.

`0x00575A50` treats a request for the slot's own file (the same family `+0xD2` and, when the slot byte
`+0xC8` is 1 or 2, the same file number `+0xCC`; `0x00575A60`-`0x00575A92`) by the slot's state `+0xC9`:

- loaded (1): it only changes the entry or page `+0xCE` and returns 1 (`0x00575B58`-`0x00575B63`);
- loading (2): the request is dropped, with no write (`0x00575B4B`);
- loading with the buffer to be freed when it finishes (3): the state goes back to 2 (`0x00575B44`), so the
  finishing load is kept. The completion message `0x10` of `0x00575870` turns state 2 into 1, and state 3
  into 0 after freeing the buffer.

Any other request, including one for a different file while a load is pending, frees the slot's buffer and
loads the new file (`0x00575640` at `0x00575B20`, `0x00575C30` at `0x00575B2B`). The queue at `+0xD3` / `+0xD6` is
written only by code that no path reaches (`0x00575ACC`-`0x00575B10`), so no request waits.

### The unlock tables

With its creation flag set, `0x00576F50` loads the six unlock tables (base + 1) into the manager's
`+0xC8` to `+0xF0` and `menuquest.dat` (`0x128`) into `+0xF8`. `0x00577550(family)` evaluates them:

- families 0-4: each record through `0x00575E80`, the result written as the entry's unlock bit through
  `0x00315910(byte [0x00D23750 + family], entry, result)`;
- Bestiary: for each entry and slot, slot 7 and every empty slot get their read mark set
  (`0x00315AD0(6, entry, slot, 1)`); the slot thresholds are not saved.

`0x00576E30(family, entry, slot)` answers whether a Bestiary slot is open, each time it is asked; other families
always answer yes. Mode 0 compares the entry's kill count (`0x00315420`) with the threshold, mode 1 the story
counter, and mode 2 opens when this monster or the monster the threshold names has a kill.

### Reading the catalog

- `0x005778F0(entry)` opens an entry: `0x00575D10` asks slot 1 for the record's `bundle` with the entry
  number, then `0x00575DD0` asks slot 2 for the record's `page`.
- `0x00575DD0` bounds the page by `pageCount`, takes `pageMap[page]` as the file number and the page as the
  picture. Its `0xFFFF` test compares the zero-extended word with -1 (`0x00575E26`), so it never matches.
- `0x005760A0(entry)` fills the detail record: the name, the section, the entry number, the flag, and for the
  Bestiary the kill count and, from the slot-count byte, each slot's threshold (`0x00576860`).
- Bestiary text ids `0x4210` to `0x421C` also get a second line, an Esper's name read through `0x0035D330`.
- `0x00576740(section)` gives a section's caption, its first entry, its entry count and the number of its
  entries that pass the family's unlock test for that entry (`0x00576CA0`, `0x003154B0`).

### Section captions

`0x00576A50(section)` returns the caption text. Without a gate, or with a gate that lists no conditions and
no maps, the caption is the message `caption[section]`. Otherwise it is shown when any condition id passes
`0x00309EC0`, or any listed map has at least one bit set in its 32-byte bit set (`0x00255120`; for the
current map the live set, `0x00255060`); when none does, the caption reads message `0x3EC` (`0x002F9860`).
A caption of -1 yields no text.

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

When the entry page shows a line (`0x00574900`), it runs that string's line program (`0x00577A40`). The
nibbles and bits are the ones the unlock records test:

| `op` | Effect |
|---|---|
| 0 | set save nibble `index` to `value`, at most 15 (`0x00315CD0`) |
| 1 | set save bit `index` when `value` is 1, else clear it (`0x00315A20`) |
| 2 | add `value` to save nibble `index`, at most 15 |
| 3 | subtract `value` from save nibble `index`, at least 0 |

For the Bestiary the program runs only while the slot's read mark is clear (`0x00576F30`), and the mark is
then set (`0x00577A20`). For the other families it runs every time a line is shown, and the entry is marked
read on its last line.

### The glyph sheet

When slot 1 finishes loading, `0x00575710` registers the bundle's sheet when `sheet` is not -1
(`0x0039BEC0`). For `tutorial` it also calls `0x0017FBC0(6)`; for `monster` it registers it as font
`handbook_monster<NNN>.txt`, `NNN` the bundle number (`0x0017FA90`, `0x0017F790`).

A text writes a sheet character as two bytes, shown as `{exp:0xN}` in the tables:

- **Code.** `0x002AC2F0` takes the `0x00916570` table value for the lead byte's low nibble, plus the second byte less
  `0x20` (`0x002AC3B4`-`0x002AC3BC`).
- **Sheet or font.** A lead at or above `[0x01E0CDF8]` is drawn from a sheet. `0x002AB7D0` sets that word to `0x18`, or
  to `0x1C` for the locales its test picks (`0x002AB7D9`-`0x002AB7E9`).
- **Record.** The sheet block is the renderer's `+0x68`, or `0x0039BA30` of its font slot `+0xA6`
  (`0x002AC417`-`0x002AC440`), and the record is `0x0020E600([block + 0x0C]) + 8 × code` (`0x002AC498`-`0x002AC4A7`).
- **Cell.** Bits 0-9 of the record are x, 10-19 y, 20-24 width and 25-29 height, as `0x002B0280` reads them
  (`0x002B08BC`-`0x002B0918`).

The `story`, `world`, `person` and `knowledge` bundles are the same bytes in all nine trees, and so are their 796
sheet glyphs. Each glyph was matched against the JIS X 0208 characters drawn in seven faces of the Japanese system
fonts MS Gothic, MS Mincho, Meiryo and Yu Gothic. A glyph
counts as decoded when its best match leads the second by at least 0.011 and the word it makes reads in its
sentence. That decodes 753 of the 796; the other 43 stay `{exp:0xN}`:

| Family | Glyphs | Decoded | Left | Uses | Uses decoded |
|---|---:|---:|---:|---:|---:|
| `story` | 124 | 119 | 5 | 267 | 256 |
| `world` | 207 | 196 | 11 | 569 | 538 |
| `person` | 184 | 175 | 9 | 506 | 483 |
| `knowledge` | 281 | 263 | 18 | 500 | 474 |

In each tree, 73 of the strings still hold an undecoded character
([`handbook-files-strings-decoded.tsv`](handbook-files-strings-decoded.tsv)). 49 of the 300 entries give their
name in their own text ([`handbook-files-entry-names.tsv`](handbook-files-entry-names.tsv)).

`handbook-files-glyphs.tsv`:

| Column | Meaning |
|---|---|
| `language`, `family`, `bundle`, `N` | the tree, the family, the `hdat` number and the sheet record `N` of `{exp:0xN}` |
| `character` | the decoded character, or `-` |
| `best_score`, `second_score`, `best`, `second` | the two best matching characters and their scores |
| `context` | one use, with the glyph in brackets and six characters each side |
| `candidates` | `jis` when the best match was taken over JIS X 0208; `game` when it was taken over the characters of the game's own `jp` fonts, after no JIS character led by 0.011 |
| `decision` | `corpus:` words of the game's other Japanese text that hold the decoded word; `reading:` the word read in the sentence; `shape:` the margin that is too small; `reading, rejected:` the reading that refuses the best match |

### Pictures

`0x00575B80` binds a picture when slot 2's page lies in the file's window and differs from the bound one: it
registers the TIM2 at `pictureAt[page - first]` as the image label `hb_tex` (`0x0024A440`). It does nothing
for `tutorial`, so Traveler's Tips shows no picture: the entry page still requests the page's file into
slot 2 (`0x005778F0` → `0x00575DD0`, which has no family test), so `menuhandbook_tutorial001.dat` loads, but no
`hb_tex` label is made, and the picture pane `0x00570630` draws nothing because `0x00576C70`, its only source, returns
slot 2's label `+0xF8`, which stays 0 (`0x0057068E`).

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
- A line program changes save nibbles and bits each time its line is shown; shipped strings have none.
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
