---
title: "Dalmasca Estersand dialogue: every line and caption of the Dalmasca Estersand scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[dalmasca-estersand-dialogue.tsv](dalmasca-estersand-dialogue.tsv) has one row per string of sections 2 and 3 of the Dalmasca Estersand scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 565 rows from 10 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Section 2 holds the lines (562 rows) and section 3 the captions (3 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `dalmasca-estersand-scripts.tsv`, the table of [Dalmasca Estersand scripts](../Story-Events-And-Hunts/dalmasca-estersand-scripts.md), names section 2 rows by the same key: 95 of its rows name 495 of the 562 section 2 rows here. The `quoted_lines` column of its steps table quotes 495 of them, in 5,981 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `dst_a0181` | scene | 4 | 0 | 4 | 4 |
| `dst_a0580` | scene | 6 | 0 | 6 | 6 |
| `dst_b0100` | scene | 85 | 0 | 85 | 85 |
| `dst_a01` | zone | 4 | 0 | 2 | 2 |
| `dst_a02` | zone | 3 | 0 | 1 | 1 |
| `dst_a04` | zone | 2 | 0 | 1 | 1 |
| `dst_a05` | zone | 38 | 0 | 12 | 12 |
| `dst_a06` | zone | 7 | 1 | 7 | 7 |
| `dst_a07` | zone | 52 | 0 | 49 | 49 |
| `dst_b01` | zone | 260 | 0 | 229 | 229 |
| `dst_b02` | zone | 98 | 0 | 97 | 97 |
| `dst_c01` | zone | 2 | 0 | 2 | 2 |
| `dst_c02` | zone | 1 | 2 | 0 | 0 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 565 rows.

Empty strings per tree: `us` 13, `de` 13, `es` 14, `fr` 13, `it` 13. No `in`, `kr`, `cn` or `ch` string is empty.

13 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `dst_b02` 2/28: empty in `es`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `dst_a01` 2/2: in `us`, `de`, `es`, `fr` and `it`.
- `dst_a05` 2/36: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 9 | 9 | 9 | 9 |
| `fontex_expand` | 556 | 556 | 556 | 556 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

68 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 44 with 2, 10 with 3, 4 with 4, 1 with 5, 1 with 6, 2 with 7, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 68, `de` 68, `es` 68, `fr` 68, `it` 68, `in` 68, `kr` 68, `cn` 68, `ch` 68.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

A code the table writes by its own bytes is the code with those bytes on Text codes: `{0F3D:8180}` is `0F 3D` with the payload `81 80`. Such codes in all nine columns: `{0F3D:...}` 594.

Examples, by script, section and id:

- `dst_b01` 2/194, a line with a line break (`{line}`). `us`: `{name:8281AA}{line}{0F3D:8180}Gimme the sign, boy!`; `in`: `{spacing:8181}{name:8281AA}{line}{0F3D:8180}どの魚が来たか、サインで教えてくれ！`.
- `dst_a0580` 2/3, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}By your leave, Captain.`; `in`: `{spacing:8180}{speed:8180}{alt-font}かまわんな{blank}将軍？`.
- `dst_a05` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `dst_a06` 3/0, a caption. `us`: `Weather-beaten Door`; `de`: `Verwitterte Tür`; `in`: `{spacing:8181}古ぼけた扉`.

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
| rows | 565: 562 in section 2, 3 in section 3 |
| scripts | 13: 10 zone, 3 scene |
| strings per tree | `us` 565, `de` 565, `es` 565, `fr` 565, `it` 565, `in` 565, `kr` 565, `cn` 565, `ch` 565 |
| non-empty strings per tree | `us` 552, `de` 552, `es` 551, `fr` 552, `it` 552, `in` 565, `kr` 565, `cn` 565, `ch` 565 |
| strings with `{alt-font}` | `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9, `in` 9, `kr` 9, `cn` 9, `ch` 9 |
| strings with a choice list | `us` 68, `de` 68, `es` 68, `fr` 68, `it` 68, `in` 68, `kr` 68, `cn` 68, `ch` 68 |
| section 2 rows the scripts table names | 495 |
| section 2 rows a step quotes | 495, in 5,981 steps |

## Related

- [Dalmasca Estersand scripts](../Story-Events-And-Hunts/dalmasca-estersand-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Dalmasca Estersand scenes](../Story-Events-And-Hunts/dalmasca-estersand-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
