---
title: "Nalbina Dungeons dialogue: every line and caption of the Nalbina Dungeons scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[nalbina-dungeons-dialogue.tsv](nalbina-dungeons-dialogue.tsv) has one row per string of sections 2 and 3 of the Nalbina Dungeons scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 229 rows from 3 zone scripts under `plan_map/` and 6 scene scripts under `event/`. Section 2 holds the lines (227 rows) and section 3 the captions (2 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `nalbina-dungeons-scripts.tsv`, the table of [Nalbina Dungeons scripts](../Story-Events-And-Hunts/nalbina-dungeons-scripts.md), names section 2 rows by the same key: 93 of its rows name 176 of the 227 section 2 rows here. The `quoted_lines` column of its steps table quotes 176 of them, in 1,791 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `nal_a0100` | scene | 12 | 0 | 12 | 12 |
| `nal_b0100` | scene | 6 | 0 | 6 | 6 |
| `nal_b0101` | scene | 45 | 0 | 45 | 45 |
| `nal_c0101` | scene | 3 | 0 | 3 | 3 |
| `nal_c0200` | scene | 6 | 0 | 6 | 6 |
| `nal_d0100` | scene | 29 | 0 | 29 | 29 |
| `nal_a01` | zone | 99 | 0 | 73 | 73 |
| `nal_c01` | zone | 1 | 1 | 1 | 1 |
| `nal_c02` | zone | 26 | 1 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 229 rows.

Empty strings per tree: `us` 4, `de` 4, `es` 3, `fr` 34, `it` 4. No `in`, `kr`, `cn` or `ch` string is empty.

3 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

32 more rows are empty in some trees only: 31 in `fr`; 1 in `us`, `de` and `it`.

The rows that carry `{alt-font}` in some trees only:

- `nal_b0101` 2/36: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

The rows that carry a choice list in some trees only:

- `nal_a01` 2/69: in `us`, `de`, `es`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `nal_a01` 2/82: in `us`, `de`, `es`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 98 | 98 | 98 | 98 |
| `fontex_expand` | 131 | 131 | 131 | 131 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

25 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 15 with 2, 4 with 3, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 25, `de` 25, `es` 25, `fr` 23, `it` 25, `in` 25, `kr` 25, `cn` 25, `ch` 25.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `nal_a01` 2/62, a line with a line break (`{line}`). `us`: `{instant:8181}{name:A280F6}{line}Unh...ahh... W-Water...`; `in`: `{spacing:8181}{instant:8181}{name:A280F6}{line}う……あ……、{line}み、水……。`.
- `nal_b0100` 2/5, a line drawn with the alternate font. `us`: `{alt-font}{speed:8180}{center:8180}{line}You all right, Vaan?`; `in`: `{spacing:8180}{alt-font}{speed:8180}大丈夫か{blank}ヴァン？`.
- `nal_a01` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `nal_c01` 3/0, a caption. `us`: `Door`; `de`: `Tür`; `in`: `{spacing:8181}扉`.

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
| rows | 229: 227 in section 2, 2 in section 3 |
| scripts | 9: 3 zone, 6 scene |
| strings per tree | `us` 229, `de` 229, `es` 229, `fr` 229, `it` 229, `in` 229, `kr` 229, `cn` 229, `ch` 229 |
| non-empty strings per tree | `us` 225, `de` 225, `es` 226, `fr` 195, `it` 225, `in` 229, `kr` 229, `cn` 229, `ch` 229 |
| strings with `{alt-font}` | `us` 99, `de` 99, `es` 99, `fr` 99, `it` 99, `in` 98, `kr` 98, `cn` 98, `ch` 98 |
| strings with a choice list | `us` 25, `de` 25, `es` 25, `fr` 23, `it` 25, `in` 25, `kr` 25, `cn` 25, `ch` 25 |
| section 2 rows the scripts table names | 176 |
| section 2 rows a step quotes | 176, in 1,791 steps |

## Related

- [Nalbina Dungeons scripts](../Story-Events-And-Hunts/nalbina-dungeons-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Nalbina Dungeons scenes](../Story-Events-And-Hunts/nalbina-dungeons-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
