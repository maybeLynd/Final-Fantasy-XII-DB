---
title: "Jahara dialogue: every line and caption of the Jahara scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[jahara-dialogue.tsv](jahara-dialogue.tsv) has one row per string of sections 2 and 3 of the Jahara scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 414 rows from 3 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `jahara-scripts.tsv`, the table of [Jahara scripts](../Story-Events-And-Hunts/jahara-scripts.md), names section 2 rows by the same key: 136 of its rows name 384 of the 414 section 2 rows here. The `quoted_lines` column of its steps table quotes 384 of them, in 548 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `glf_a0200` | scene | 32 | 0 | 32 | 32 |
| `glf_a0300` | scene | 28 | 0 | 28 | 28 |
| `glf_z0100` | scene | 62 | 0 | 62 | 62 |
| `glf_a01` | zone | 65 | 0 | 39 | 39 |
| `glf_a02` | zone | 176 | 0 | 174 | 174 |
| `glf_a03` | zone | 51 | 0 | 49 | 49 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 414 rows.

Empty strings per tree: `us` 7, `de` 7, `es` 7, `fr` 7, `it` 7. No `in`, `kr`, `cn` or `ch` string is empty.

7 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 121 | 121 | 121 | 121 |
| `fontex_expand` | 293 | 293 | 293 | 293 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

33 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 26 with 2, 3 with 3, 1 with 7, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 33, `de` 33, `es` 33, `fr` 33, `it` 33, `in` 33, `kr` 33, `cn` 33, `ch` 33.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `glf_a01` 2/60, a line with a line break (`{line}`). `us`: `{instant:8181}Garif War-chief{line}.........`; `in`: `{spacing:8181}{instant:8181}ガリフ族の戦士長{line}…………。`.
- `glf_z0100` 2/42, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}Did that make sense?`; `in`: `{spacing:8180}{speed:8180}{alt-font}王子が死んだ時`.
- `glf_a01` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.

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
| rows | 414: 414 in section 2, 0 in section 3 |
| scripts | 6: 3 zone, 3 scene |
| strings per tree | `us` 414, `de` 414, `es` 414, `fr` 414, `it` 414, `in` 414, `kr` 414, `cn` 414, `ch` 414 |
| non-empty strings per tree | `us` 407, `de` 407, `es` 407, `fr` 407, `it` 407, `in` 414, `kr` 414, `cn` 414, `ch` 414 |
| strings with `{alt-font}` | `us` 121, `de` 121, `es` 121, `fr` 121, `it` 121, `in` 121, `kr` 121, `cn` 121, `ch` 121 |
| strings with a choice list | `us` 33, `de` 33, `es` 33, `fr` 33, `it` 33, `in` 33, `kr` 33, `cn` 33, `ch` 33 |
| section 2 rows the scripts table names | 384 |
| section 2 rows a step quotes | 384, in 548 steps |

## Related

- [Jahara scripts](../Story-Events-And-Hunts/jahara-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Jahara scenes](../Story-Events-And-Hunts/jahara-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
