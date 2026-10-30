---
title: "Eruyt Village dialogue: every line and caption of the Eruyt Village scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[eruyt-village-dialogue.tsv](eruyt-village-dialogue.tsv) has one row per string of sections 2 and 3 of the Eruyt Village scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 334 rows from 3 zone scripts under `plan_map/` and 4 scene scripts under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `eruyt-village-scripts.tsv`, the table of [Eruyt Village scripts](../Story-Events-And-Hunts/eruyt-village-scripts.md), names section 2 rows by the same key: 126 of its rows name 296 of the 334 section 2 rows here. The `quoted_lines` column of its steps table quotes 296 of them, in 343 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `vic_a0100` | scene | 26 | 0 | 26 | 26 |
| `vic_a0300` | scene | 41 | 0 | 40 | 40 |
| `vic_a0301` | scene | 18 | 0 | 18 | 18 |
| `vic_a0380` | scene | 4 | 0 | 3 | 3 |
| `vic_a01` | zone | 79 | 0 | 75 | 75 |
| `vic_a02` | zone | 109 | 0 | 105 | 105 |
| `vic_a03` | zone | 57 | 0 | 29 | 29 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 334 rows.

Empty strings per tree: `us` 5, `de` 5, `es` 5, `fr` 5, `it` 5. No `in`, `kr`, `cn` or `ch` string is empty.

5 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 86 | 86 | 86 | 86 |
| `fontex_expand` | 248 | 248 | 248 | 248 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

25 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 18 with 2, 2 with 3, 1 with 4, 1 with 7, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 25, `de` 25, `es` 25, `fr` 25, `it` 25, `in` 25, `kr` 25, `cn` 25, `ch` 25.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `vic_a01` 2/6, a line with a line break (`{line}`). `us`: `{instant:8181}{name:A281FF}{line}Have you remembered?`; `in`: `{spacing:8181}{instant:8181}{name:A281FF}{line}何か……思い出したの？`.
- `vic_a0100` 2/4, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}If you can find her.`; `in`: `{spacing:8180}{speed:8180}{alt-font}会えるものか`.
- `vic_a03` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.

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
| rows | 334: 334 in section 2, 0 in section 3 |
| scripts | 7: 3 zone, 4 scene |
| strings per tree | `us` 334, `de` 334, `es` 334, `fr` 334, `it` 334, `in` 334, `kr` 334, `cn` 334, `ch` 334 |
| non-empty strings per tree | `us` 329, `de` 329, `es` 329, `fr` 329, `it` 329, `in` 334, `kr` 334, `cn` 334, `ch` 334 |
| strings with `{alt-font}` | `us` 86, `de` 86, `es` 86, `fr` 86, `it` 86, `in` 86, `kr` 86, `cn` 86, `ch` 86 |
| strings with a choice list | `us` 25, `de` 25, `es` 25, `fr` 25, `it` 25, `in` 25, `kr` 25, `cn` 25, `ch` 25 |
| section 2 rows the scripts table names | 296 |
| section 2 rows a step quotes | 296, in 343 steps |

## Related

- [Eruyt Village scripts](../Story-Events-And-Hunts/eruyt-village-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Eruyt Village scenes](../Story-Events-And-Hunts/eruyt-village-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
