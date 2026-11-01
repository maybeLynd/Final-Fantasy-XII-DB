---
title: "Bhujerba dialogue: every line and caption of the Bhujerba scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[bhujerba-dialogue.tsv](bhujerba-dialogue.tsv) has one row per string of sections 2 and 3 of the Bhujerba scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 1,903 rows from 14 zone scripts under `plan_map/` and 12 scene scripts under `event/`. Section 2 holds the lines (1,887 rows) and section 3 the captions (16 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `bhujerba-scripts.tsv`, the table of [Bhujerba scripts](../Story-Events-And-Hunts/bhujerba-scripts.md), names section 2 rows by the same key: 244 of its rows name 1,788 of the 1,887 section 2 rows here. The `quoted_lines` column of its steps table quotes 1,788 of them, in 1,948 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `byu_a0100` | scene | 21 | 0 | 20 | 20 |
| `byu_a0400` | scene | 30 | 0 | 29 | 29 |
| `byu_a0480` | scene | 4 | 0 | 4 | 4 |
| `byu_a0481` | scene | 14 | 0 | 14 | 14 |
| `byu_a1880` | scene | 20 | 0 | 20 | 20 |
| `byu_b0100` | scene | 19 | 0 | 19 | 19 |
| `byu_b0101` | scene | 9 | 0 | 7 | 7 |
| `byu_w0100` | scene | 38 | 0 | 38 | 38 |
| `byu_x0100` | scene | 26 | 0 | 26 | 26 |
| `byu_y0100` | scene | 30 | 0 | 28 | 28 |
| `byu_y0101` | scene | 28 | 0 | 28 | 28 |
| `byu_z0100` | scene | 15 | 0 | 15 | 15 |
| `byu_a01` | zone | 236 | 3 | 231 | 231 |
| `byu_a02` | zone | 136 | 3 | 134 | 134 |
| `byu_a03` | zone | 179 | 2 | 174 | 174 |
| `byu_a04` | zone | 100 | 0 | 72 | 72 |
| `byu_a07` | zone | 104 | 0 | 100 | 100 |
| `byu_a08` | zone | 90 | 0 | 88 | 88 |
| `byu_a11` | zone | 83 | 1 | 81 | 81 |
| `byu_a12` | zone | 50 | 1 | 48 | 48 |
| `byu_a14` | zone | 74 | 1 | 72 | 72 |
| `byu_a15` | zone | 73 | 1 | 70 | 70 |
| `byu_a16` | zone | 68 | 1 | 66 | 66 |
| `byu_a17` | zone | 49 | 1 | 46 | 46 |
| `byu_a18` | zone | 183 | 2 | 177 | 177 |
| `byu_b01` | zone | 208 | 0 | 181 | 181 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 1,903 rows.

Empty strings per tree: `us` 24, `de` 24, `es` 25, `fr` 24, `it` 24. No `in`, `kr`, `cn` or `ch` string is empty.

24 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `byu_y0100` 2/20: empty in `es`.

The rows that carry `{alt-font}` in some trees only:

- `byu_y0100` 2/20: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `byu_y0100` 2/25: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 243 | 243 | 243 | 243 |
| `fontex_expand` | 1,660 | 1,660 | 1,660 | 1,660 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

148 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 130 with 2, 9 with 3, 2 with 7, 4 with 11, 2 with 26, 1 with 32.

Strings with a choice list per tree: `us` 148, `de` 148, `es` 148, `fr` 148, `it` 148, `in` 148, `kr` 148, `cn` 148, `ch` 148.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

A code the table writes by its own bytes is the code with those bytes on Text codes: `{0F3D:8180}` is `0F 3D` with the payload `81 80`. Such codes in all nine columns: `{0F3D:...}` 765.

Examples, by script, section and id:

- `byu_a01` 2/1, a line with a line break (`{line}`). `us`: `Vaan{line}{0F3D:8180}I'm Captain Basch!`; `in`: `{spacing:8181}ヴァン{line}{0F3D:8180}オレがバッシュだ！`.
- `byu_a1880` 2/15, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{line}I should like nothing more.`; `in`: `{spacing:8180}{speed:8180}{alt-font}さて{blank}なんと言うかな`.
- `byu_a0100` 2/1, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `byu_a01` 3/0, a caption. `us`: `Rithil's Protectives`; `de`: `Zum Harten Harnisch`; `in`: `{spacing:8181}リシル防具店`.

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
| rows | 1,903: 1,887 in section 2, 16 in section 3 |
| scripts | 26: 14 zone, 12 scene |
| strings per tree | `us` 1,903, `de` 1,903, `es` 1,903, `fr` 1,903, `it` 1,903, `in` 1,903, `kr` 1,903, `cn` 1,903, `ch` 1,903 |
| non-empty strings per tree | `us` 1,879, `de` 1,879, `es` 1,878, `fr` 1,879, `it` 1,879, `in` 1,903, `kr` 1,903, `cn` 1,903, `ch` 1,903 |
| strings with `{alt-font}` | `us` 244, `de` 244, `es` 243, `fr` 244, `it` 244, `in` 243, `kr` 243, `cn` 243, `ch` 243 |
| strings with a choice list | `us` 148, `de` 148, `es` 148, `fr` 148, `it` 148, `in` 148, `kr` 148, `cn` 148, `ch` 148 |
| section 2 rows the scripts table names | 1,788 |
| section 2 rows a step quotes | 1,788, in 1,948 steps |

## Related

- [Bhujerba scripts](../Story-Events-And-Hunts/bhujerba-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Bhujerba scenes](../Story-Events-And-Hunts/bhujerba-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
