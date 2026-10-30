---
title: "Necrohol of Nabudis dialogue: every line and caption of the Necrohol of Nabudis scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[necrohol-of-nabudis-dialogue.tsv](necrohol-of-nabudis-dialogue.tsv) has one row per string of sections 2 and 3 of the Necrohol of Nabudis scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 68 rows from 7 zone scripts under `plan_map/` and 6 scene scripts under `event/`. Section 2 holds the lines (53 rows) and section 3 the captions (15 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `necrohol-of-nabudis-scripts.tsv`, the table of [Necrohol of Nabudis scripts](../Story-Events-And-Hunts/necrohol-of-nabudis-scripts.md), names section 2 rows by the same key: 21 of its rows name 44 of the 53 section 2 rows here. The `quoted_lines` column of its steps table quotes 44 of them, in 82 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `bds_a0100` | scene | 12 | 0 | 12 | 12 |
| `bds_e0101` | scene | 1 | 0 | 1 | 1 |
| `bds_f0100` | scene | 1 | 0 | 0 | 0 |
| `bds_f0101` | scene | 1 | 0 | 0 | 0 |
| `bds_g0100` | scene | 1 | 0 | 0 | 0 |
| `bds_g0101` | scene | 1 | 0 | 0 | 0 |
| `bds_a02` | zone | 9 | 4 | 9 | 9 |
| `bds_b01` | zone | 12 | 4 | 10 | 10 |
| `bds_c01` | zone | 9 | 4 | 9 | 9 |
| `bds_c02` | zone | 1 | 0 | 0 | 0 |
| `bds_e01` | zone | 1 | 1 | 1 | 1 |
| `bds_f01` | zone | 2 | 1 | 1 | 1 |
| `bds_g01` | zone | 2 | 1 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 68 rows.

Empty strings per tree: `us` 5, `de` 5, `es` 5, `fr` 5, `it` 5. No `in`, `kr`, `cn` or `ch` string is empty.

5 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `bds_f0100` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bds_f0101` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bds_g0100` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bds_g0101` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bds_e01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bds_f01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bds_g01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 10 | 10 | 10 | 10 |
| `fontex_expand` | 58 | 58 | 58 | 58 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 3, `de` 3, `es` 3, `fr` 3, `it` 3.

### Choice lists

22 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 13 with 2, 9 with 3.

Strings with a choice list per tree: `us` 22, `de` 22, `es` 22, `fr` 22, `it` 22, `in` 22, `kr` 22, `cn` 22, `ch` 22.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `bds_a0100` 2/2, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}This? In just 2 years?{line}How?`; `in`: `{spacing:8180}{speed:8180}{alt-font}ウソだろ！？{line}たった２年で{blank}こんなになるのかよ！？`.
- `bds_a02` 3/0, a caption. `us`: `Door of Horrors`; `de`: `Pforte des Grauens`; `in`: `{spacing:8181}恐怖の扉`.

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
| rows | 68: 53 in section 2, 15 in section 3 |
| scripts | 13: 7 zone, 6 scene |
| strings per tree | `us` 68, `de` 68, `es` 68, `fr` 68, `it` 68, `in` 68, `kr` 68, `cn` 68, `ch` 68 |
| non-empty strings per tree | `us` 63, `de` 63, `es` 63, `fr` 63, `it` 63, `in` 68, `kr` 68, `cn` 68, `ch` 68 |
| strings with `{alt-font}` | `us` 10, `de` 10, `es` 10, `fr` 10, `it` 10, `in` 10, `kr` 10, `cn` 10, `ch` 10 |
| strings with a choice list | `us` 22, `de` 22, `es` 22, `fr` 22, `it` 22, `in` 22, `kr` 22, `cn` 22, `ch` 22 |
| section 2 rows the scripts table names | 44 |
| section 2 rows a step quotes | 44, in 82 steps |

## Related

- [Necrohol of Nabudis scripts](../Story-Events-And-Hunts/necrohol-of-nabudis-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Necrohol of Nabudis scenes](../Story-Events-And-Hunts/necrohol-of-nabudis-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
