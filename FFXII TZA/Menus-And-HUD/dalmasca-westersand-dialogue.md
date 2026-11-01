---
title: "Dalmasca Westersand dialogue: every line and caption of the Dalmasca Westersand scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[dalmasca-westersand-dialogue.tsv](dalmasca-westersand-dialogue.tsv) has one row per string of sections 2 and 3 of the Dalmasca Westersand scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 73 rows from 6 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of [`dalmasca-westersand-scripts.tsv`](../Story-Events-And-Hunts/dalmasca-westersand-scripts.tsv), the table of [Dalmasca Westersand scripts](../Story-Events-And-Hunts/dalmasca-westersand-scripts.md), names section 2 rows by the same key: 23 of its rows name 39 of the 73 section 2 rows here. The `quoted_lines` column of its steps table quotes 39 of them, in 41 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `wdl_a0600` | scene | 13 | 0 | 13 | 13 |
| `wdl_b0100` | scene | 1 | 0 | 0 | 0 |
| `wdl_b0101` | scene | 1 | 0 | 0 | 0 |
| `wdl_a01` | zone | 2 | 0 | 1 | 1 |
| `wdl_a02` | zone | 1 | 0 | 1 | 1 |
| `wdl_a03` | zone | 3 | 0 | 2 | 2 |
| `wdl_a05` | zone | 5 | 0 | 2 | 2 |
| `wdl_a06` | zone | 44 | 0 | 18 | 18 |
| `wdl_b01` | zone | 3 | 0 | 2 | 2 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 73 rows.

Empty strings per tree: `us` 5, `de` 5, `es` 5, `fr` 5, `it` 5. No `in`, `kr`, `cn` or `ch` string is empty.

5 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `wdl_b0100` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `wdl_b0101` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `wdl_b01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `wdl_b01` 2/1: in `us`, `de`, `es`, `fr` and `it`.

The rows that carry `{alt-font}` in some trees only:

- `wdl_a0600` 2/11: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `wdl_a0600` 2/12: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 11 | 11 | 11 | 11 |
| `fontex_expand` | 62 | 62 | 62 | 62 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 1, `de` 1, `es` 1, `fr` 1, `it` 1.

### Choice lists

20 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 14 with 2, 3 with 3, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 20, `de` 20, `es` 20, `fr` 20, `it` 20, `in` 20, `kr` 20, `cn` 20, `ch` 20.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `wdl_a03` 2/0, a line with a line break (`{line}`). `us`: `{line}{speed:8180}The chocobo refuses to go any further.`; `in`: `{spacing:8181}{line}{speed:8180}チョコボがイヤがっていて、先に進むことができません。`.
- `wdl_a0600` 2/0, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}This "come in handy" often?`; `in`: `{spacing:8180}{speed:8180}{alt-font}これも仕事柄ですか`.
- `wdl_a06` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script file under `plan_master/<language>/`: `plan_map/...` for a zone script, `event/...` for a scene script |
| `section` | `2` for a line of the message bank, `3` for a caption |
| `id` | the entry number in that section, from 0: the text id a verb passes |
| `us` to `ch` | the string in that language tree, decoded with the tree's font |
| `missing` | the languages whose tree has no string at this key (no such script, or a shorter section), comma-separated; empty when all nine have one |
| `same_bytes` | the groups of languages whose string bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more, and the languages in `missing` take no part |

An empty cell under a language not in `missing` is an empty string.

## Data

| Fact | Value |
|---|---|
| rows | 73: 73 in section 2, 0 in section 3 |
| scripts | 9: 6 zone, 3 scene |
| strings per tree | `us` 73, `de` 73, `es` 73, `fr` 73, `it` 73, `in` 73, `kr` 73, `cn` 73, `ch` 73 |
| non-empty strings per tree | `us` 68, `de` 68, `es` 68, `fr` 68, `it` 68, `in` 73, `kr` 73, `cn` 73, `ch` 73 |
| strings with `{alt-font}` | `us` 13, `de` 13, `es` 13, `fr` 13, `it` 13, `in` 11, `kr` 11, `cn` 11, `ch` 11 |
| strings with a choice list | `us` 20, `de` 20, `es` 20, `fr` 20, `it` 20, `in` 20, `kr` 20, `cn` 20, `ch` 20 |
| section 2 rows the scripts table names | 39 |
| section 2 rows a step quotes | 39, in 41 steps |

## Related

- [Dalmasca Westersand scripts](../Story-Events-And-Hunts/dalmasca-westersand-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Dalmasca Westersand scenes](../Story-Events-And-Hunts/dalmasca-westersand-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
