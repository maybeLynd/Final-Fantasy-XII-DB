---
title: "String tables: every menu, help and battle message string of the st2e text tables in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x002FA560, 0x02F973C0, 0x002F9860, 0x002F9920, 0x00248700, 0x00236C30, 0x02EBF018, 0x00536410, 0x002B49F0, 0x002B4090, 0x002B40C0, 0x00254A10, 0x02EBF058, 0x0031C5D0, 0x002AC5F0"
---

## What it lists

[text-string-tables.tsv](text-string-tables.tsv) has one row per string of an `st2e` text table, with the string in
each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 7,422 rows from 32 tables. The
tables are files under `ps2data/image/ff12/test_battle/<language>/binaryfile/`, plus the text block of section 57 of
`battle_pack.bin`. [Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md) gives
their layout and how a text id finds a string.

### The tables and the code that reads them

- **Text groups.** 24 tables, groups 1 to 24: `menu_command` to `questtitle` and `menu00` to `menu02`. `0x002FA560`
  loads a group when a menu widget asks for it (`0x00248700`) and binds it into `0x02F973C0[group]`; `0x002F9860` reads
  string `id % 1000` of group `id / 1000`, and `0x002F9920` finds a row by its own id.
- **`battle_message.bin`.** The battle log's message templates, `battle_pack.bin` entry 2, bound to `0x02EBF018` by
  `0x00236C30` (`0x00236C7B`-`0x00236C86`). The loose file in each tree repeats the pack entry's bytes
  ([PS2-era .bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md)).
- **`battle_pack.bin#57`.** The text block of the bazaar table, section 57 of `battle_pack.bin`, bound to
  `0x02EBF058` (`0x00236F6E`-`0x00236F7C`). `horidashi.bin` is the loose file of the same table in the `in`, `kr`, `cn`
  and `ch` trees.
- **Korean and Chinese tables.** `mons_act`, `mons_category`, `mons_race`, `object_data` and `target_data` ship
  only in the `kr` and `cn` trees, byte for byte the same in both, and no path in the executable names them.

The credits text, `menu03` and `menu04` (groups 25 and 26), is UTF-16 text listed on [Staff roll](staff-roll.md)
and is not in this table. Group 27's file, `menu05`, does not ship.

### How a battle message is filled

`0x00536410` takes a message's string id `& 0x7FFF` and reads that string of the table's text block through the
table's `+0x14` sub-directory (`0x005368C2`-`0x005368D1`, `0x0053692B`-`0x0053693A`). It fills the template with the
formatter `0x002B49F0`: through the untyped entry `0x002B4090` when `0x00254A10` returns 1 (`0x005368FB`), otherwise through
the typed entry `0x002B40C0` (`0x0053696D`). `0x005369C0` builds the log line and `0x0035B990` posts it
([Battle log](../Battle-Actions/battle-log.md)).

`0x002B40C0(size, out, template, ...)` clears sixteen `0x10`-byte argument slots (`0x002B40EE`-`0x002B40FB`) and has
`0x002B4810` type them from the template (`0x002B4108`). It fills slot i, for every slot up to the last typed one, with
its i-th variadic argument: the low 32 bits for a slot of type 1 and all eight bytes otherwise, an untyped slot
below the last typed one included (`0x002B410D`-`0x002B41AD`). It then calls `0x002B49F0(size, out, template, slots, 1)`
(`0x002B41AF`-`0x002B41C9`). The untyped entry `0x002B4090` hands `0x002B49F0` its variadic arguments in place, with 0
(`0x002B409E`-`0x002B40AB`).

`0x00254A10` returns 1 for the locale ids 0, 7, 8, 10 and 11 and 0 for ids 1 to 6 and 9. Only the typed path acts on
the escapes `0F 6C`, `0F 6D` and `0F 6E`, which the `us`, `de`, `es`, `fr` and `it` templates use for counts, plurals
and articles ([Text codes](text-codes.md)).

### The bazaar text block

The bazaar goods take their names from the word banks and their descriptions from the text groups: the query filler
`0x0031C5D0` reads the name word (`0x0031D9BF`-`0x0031DA13`) and passes the description id to `0x002F9860` (`0x0031DA29`)
([Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md)).

The section's own text block holds 128 copies of one four-character string: bytes `25 25 25 25` in the `us`, `de`, `es`, `fr`, `it`, `kr`, `cn` and `ch` packs, and
`12 8B 12 8B 12 8B 12 8B` in the `in` pack. The loose `horidashi.bin` repeats its tree's pack in `in`, `kr` and `cn`;
the `ch` copy holds the `in` bytes.

### The Korean and Chinese tables

`mons_category` and `mons_race` hold the bytes `25 25 25 25` in every string. `mons_act`, `object_data` and
`target_data` hold two-byte codes. Through the `in` font, `object_data` strings 0 to 2 read `裂果`, `鉄` and `蹴破`;
the `kr` and `cn` columns show the same bytes through the Korean and Chinese fonts. 249 strings in the `kr` column
hold codes the Korean font has no glyph for, written `{glyph:0xN}`.

The two name lists of those trees, `basic_skill_basic_skill_name.bin` and `growth_rate_growth_rate_name.bin`, are
not `st2e` tables. Each is a `u32` count, `count + 1` `u32` offsets from the file start, the last equal to the file
size, and the strings in UTF-16LE, each ended by a zero unit, with no gap between them.

[`text-string-tables-name-lists.tsv`](text-string-tables-name-lists.tsv) gives their 1,473 strings, 1,345 and 128,
one per row of the `st2e` table of the same stem: Japanese designer labels such as `LEVEL-00基本値` and
`テスト成長値`. The `kr` and `cn` copies are identical, and no path in the game names either file
([PS2-era .bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md)).

### The map and region names

`planmapname.bin`, one in each language's `bin` folder, holds the area and region names. Its header and its three
readers `0x00377B60`, `0x00377870` and `0x003778B0` are on
[Area flags and navigation map data](../World-Areas-And-Travel/area-flags-navimapdata.md): `PLMN`, 1,312 area
entries, 59 region entries, and a `u16` offset per entry from `+0x10`. All nine copies have the same counts.

[`text-string-tables-planmapname.tsv`](text-string-tables-planmapname.tsv) gives the 1,371 entries in all nine
languages, each string decoded with its tree's font, with no byte left as a raw code. An area entry's index is the
field id `0x00377B60` takes; a region entry follows the 1,312 area entries.

- Areas: 749 entries have a name in all nine languages, and the other 563 have offset 0 (written `-`) in all nine.
  708 entries carry a zone of the [Zone asset list](../World-Areas-And-Travel/zone-asset-list.md). The 45 named
  entries with no zone there include the `dgl_*` and `bds_*` names, Dhebon Jilaam Avaa (948) and the Rm rooms
  1012-1097.
- Areas 293 and 294 read `NOT USED` in `us`; the other eight trees name them, `de` Südstadt and Hauptstraße.
- Regions: region 0 has offset 0 in every tree. `us`, `de`, `fr`, `it`, `in` and `kr` name the other 58. `es` has
  offset 0 for regions 4, 5, 6, 35, 41 and 44, and `cn` and `ch` for 4, 5, 6, 35 and 51. Regions 4, 5, 6, 35 and
  51 carry development names (`bts01`, `mts01`, `pre01`, `mrm02`, `rwr01`) where they have a name. Regions 41 and 44
  read `NOT USED` in `us`, while `de` names 41 Königliches Rabanastre.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or
`{name:payload}` with the payload bytes in hex; the `placeholder` column of [Text codes](text-codes.md) gives
each code's form. A backslash comes before a literal backslash, brace, square bracket or bar in the game text.

| Row | Language | Text |
|---|---|---|
| `help_action.bin` 18 | `us` | `Deal heavy {baseline:C1FE}{symbol:8190}{baseline:8180} holy damage to one foe.` |
| `battle_message.bin` 36 | `us` | `You obtain {color:8091}{count:818080}{plural:8081}{color:8080}!` |
| `battle_message.bin` 36 | `in` | `{icon:Z:82}{color:8091}{string:808080}{color:8080}×{color:8091}{number:8180}{color:8080}を手に入れた！` |

- `help_action.bin` 18 raises the baseline, draws symbol 16 of the symbol escape (the holy element symbol) and lowers
  the baseline again.
- The `us` form of message 36 writes the count from argument slot 1 and then the item named by the word row in slot
  0, singular or plural by that count, in the highlight colour.
- The `in` form inserts the item name from slot 0 as a string, a `×` and the number from slot 1.

`{exp:0xN}` is a two-byte code at or above the expansion lead byte that this table has no expansion list for. In the
`de`, `fr` and `it` trees, `menu_command_template` strings 202, 306 and 410 (a backslash in `us`) are the bytes `18 20`, and
`de` string 436 ends with `18 21` (`{exp:0x1}`).

## Columns

| Column | Meaning |
|---|---|
| `file` | the table: its file name, or `battle_pack.bin#57` for the bazaar section's text block |
| `index` | the string's position in the table's text block, from 0; for a text group, the `row` of `0x002F9860`'s `group x 1000 + row` |
| `us` to `ch` | the string in that language tree, decoded with the tree's font |
| `missing` | the languages whose tree has no string at this `file` and `index` (no such file, or a shorter text block), comma-separated; empty when all nine have one |
| `same_bytes` | the groups of languages whose string bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more, and the languages in `missing` take no part |

### text-string-tables-name-lists.tsv

| Column | Meaning |
|---|---|
| `file` | the name list's file name |
| `index` | the string's place in the list, from 0 |
| `offset` | the string's offset from the file start |
| `string` | the string |
| `same_bytes` | the trees whose copy holds this string: `kr cn` |

An empty cell under a language not in `missing` is an empty string: every string offset of these tables lies inside
its text block.

### text-string-tables-planmapname.tsv

| Column | Meaning |
|---|---|
| `entry` | the entry's place in the offset table at `+0x10`, from 0 |
| `kind` | `area` for entries 0-1,311, `region` for 1,312-1,370 |
| `id` | the area entry's field id, or the region number (the entry less 1,312) |
| `zone` | the zone with this field id in the Zone asset list; `-` for a region or a field id with no zone |
| `name_us`, `name_de`, `name_es`, `name_fr`, `name_it`, `name_in`, `name_kr`, `name_cn`, `name_ch` | the entry's string in that language tree (English, German, Spanish, French, Italian, Japanese, Korean, Simplified Chinese, Traditional Chinese), decoded with the tree's font; `-` where the entry's offset is 0 |

## Data

Strings per table. Every table not listed here has the same count in all nine trees.

| Table | `us` `de` `es` `fr` `it` | `in` | `kr` `cn` | `ch` |
|---|---:|---:|---:|---:|
| `battle_message.bin` | 102 | 100 | 100 | 100 |
| `horidashi.bin` | 0 | 128 | 128 | 128 |
| `mons_act.bin` | 0 | 0 | 359 | 0 |
| `mons_category.bin` | 0 | 0 | 16 | 0 |
| `mons_race.bin` | 0 | 0 | 64 | 0 |
| `object_data.bin` | 0 | 0 | 66 | 0 |
| `target_data.bin` | 0 | 0 | 1,090 | 0 |
| all 32 tables | 5,699 | 5,825 | 7,420 | 5,825 |

Strings 100 and 101 of `battle_message.bin`, in `us` both
`Added {color:8091}{count:818080}{plural:8081}{color:8080} to inventory.`, exist only in the `us`, `de`, `es`, `fr`
and `it` tables.

| Table | Group | Strings in each tree |
|---|---:|---:|
| `menu_command.bin` | 1 | 428 |
| `menu_message.bin` | 2 | 204 |
| `help_menu.bin` | 3 | 398 |
| `help_action.bin` | 4 | 322 |
| `key_signal.bin` | 5 | 69 |
| `menu_mapname.bin` | 6 | 285 |
| `penelosdiary.bin` | 7 | 682 |
| `help_penelosdiary.bin` | 8 | 13 |
| `listhelp_common.bin` | 9 | 26 |
| `listhelp_action.bin` | 10 | 251 |
| `listhelp_sobicategory.bin` | 11 | 8 |
| `listhelp_status.bin` | 12 | 32 |
| `listhelp_ability.bin` | 13 | 64 |
| `listhelp_eventitem.bin` | 14 | 512 |
| `listhelp_gambit.bin` | 15 | 96 |
| `listhelp_targetchip.bin` | 16 | 256 |
| `listhelp_license.bin` | 17 | 35 |
| `menu_command_template.bin` | 18 | 457 |
| `menu_expansion.bin` | 19 | 303 |
| `listhelp_daijinamono.bin` | 20 | 512 |
| `questtitle.bin` | 21 | 257 |
| `menu00.bin` | 22 | 128 |
| `menu01.bin` | 23 | 71 |
| `menu02.bin` | 24 | 60 |
| `battle_pack.bin#57` | no group | 128 |

Empty strings per tree: `us` 2,713, `de` 9, `es` 1, `fr` 437, `it` 2,410, `in` 1, `kr` 2, `cn` 16, `ch` 20. Where the
`us` and `it` tables leave an unused string empty, `de` writes `/Unused`, `es` `DUMMY` and `fr` `/`, as in
`menu_mapname.bin` strings 49 to 54.

`menu_command_template.bin` (4 strings) and `menu_expansion.bin` (88 strings) hold UTF-16 strings, written
`{ex00}...` ([Text codes](text-codes.md), Two-byte number templates). In `us` the 4 are number templates, and the
88 are 57 captions (such as `HP`, `STONES` and `GRAPHICS SETTINGS`), 17 number templates and 14 empty strings.

## Related

- [Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md) - the table layout, the
  group loader and the two id forms.
- [Battle message list](../Battle-Actions/battle-message-list.md) - every `battle_message.bin` row with its
  argument slots.
- [Battle log](../Battle-Actions/battle-log.md) - which result posts which message.
- [Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md) - the table section 57 belongs to.
- [Text codes](text-codes.md) - every text code and its placeholder.
- [Text drawing](text-drawing.md) - how the strings are drawn.
- [Staff roll](staff-roll.md) - the credits text of `menu03` and `menu04`.
- [Word bank](text-word-bank.md) - the names the battle messages insert.
