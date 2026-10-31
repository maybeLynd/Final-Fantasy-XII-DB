---
title: "Garamsythe Waterway dialogue: every line and caption of the Garamsythe Waterway scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[garamsythe-waterway-dialogue.tsv](garamsythe-waterway-dialogue.tsv) has one row per string of sections 2 and 3 of the Garamsythe Waterway scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 341 rows from 16 zone scripts under `plan_map/` and 12 scene scripts under `event/`. Section 2 holds the lines (321 rows) and section 3 the captions (20 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `garamsythe-waterway-scripts.tsv`, the table of [Garamsythe Waterway scripts](../Story-Events-And-Hunts/garamsythe-waterway-scripts.md), names section 2 rows by the same key: 121 of its rows name 145 of the 321 section 2 rows here. The `quoted_lines` column of its steps table quotes 145 of them, in 247 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `grm_a0200` | scene | 5 | 0 | 4 | 4 |
| `grm_a0400` | scene | 22 | 0 | 22 | 22 |
| `grm_a0401` | scene | 7 | 0 | 7 | 7 |
| `grm_a0480` | scene | 9 | 0 | 7 | 7 |
| `grm_b0200` | scene | 7 | 0 | 7 | 7 |
| `grm_b0202` | scene | 25 | 0 | 25 | 25 |
| `grm_b0280` | scene | 14 | 0 | 13 | 13 |
| `grm_d0100` | scene | 1 | 0 | 0 | 0 |
| `grm_d0102` | scene | 3 | 0 | 2 | 2 |
| `grm_f0101` | scene | 1 | 0 | 1 | 1 |
| `grm_g0100` | scene | 11 | 0 | 11 | 11 |
| `grm_g0101` | scene | 4 | 0 | 4 | 4 |
| `grm_a01` | zone | 25 | 0 | 0 | 0 |
| `grm_a03` | zone | 4 | 1 | 3 | 3 |
| `grm_a04` | zone | 31 | 0 | 4 | 4 |
| `grm_a06` | zone | 3 | 0 | 0 | 0 |
| `grm_b02` | zone | 28 | 0 | 2 | 2 |
| `grm_b05` | zone | 26 | 5 | 1 | 1 |
| `grm_c01` | zone | 2 | 0 | 1 | 1 |
| `grm_d01` | zone | 1 | 1 | 1 | 1 |
| `grm_e03` | zone | 27 | 0 | 0 | 0 |
| `grm_e04` | zone | 2 | 0 | 0 | 0 |
| `grm_e05` | zone | 2 | 0 | 0 | 0 |
| `grm_e09` | zone | 3 | 1 | 3 | 3 |
| `grm_e12` | zone | 3 | 1 | 3 | 3 |
| `grm_e13` | zone | 51 | 9 | 21 | 21 |
| `grm_f01` | zone | 1 | 0 | 1 | 1 |
| `grm_g01` | zone | 3 | 2 | 2 | 2 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 341 rows.

Empty strings per tree: `us` 24, `de` 24, `es` 24, `fr` 24, `it` 24. No `in`, `kr`, `cn` or `ch` string is empty.

24 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `grm_a0480` 2/0: in `es`.
- `grm_a0480` 2/4: in `es`.
- `grm_d0100` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `grm_b02` 2/25: in `us`, `de`, `es`, `fr` and `it`.
- `grm_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `grm_d01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `grm_f01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `grm_g01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

The rows that carry a choice list in some trees only:

- `grm_e13` 2/40: in `us`, `de`, `es`, `it`, `in`, `kr`, `cn` and `ch`, not in `fr`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 93 | 93 | 93 | 93 |
| `fontex_expand` | 248 | 248 | 248 | 248 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 5, `de` 5, `es` 5, `fr` 5, `it` 5.

### Choice lists

97 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 62 with 2, 17 with 3, 12 with 11, 6 with 26.

Strings with a choice list per tree: `us` 97, `de` 97, `es` 97, `fr` 96, `it` 97, `in` 97, `kr` 97, `cn` 97, `ch` 97.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `grm_a0480` 2/7, a line with a line break (`{line}`). `us`: `{instant:8181}Balthier{line}Let's be off then, shall we?`; `in`: `{spacing:8181}{instant:8181}バルフレア{line}さて、行くとするか……。`.
- `grm_a0400` 2/3, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}Bah. Forget it.`; `in`: `{spacing:8180}{speed:8180}{alt-font}もういい{blank}ほっとけ`.
- `grm_a0200` 2/0, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `grm_a03` 3/0, a caption. `us`: `Improvised Gate`; `de`: `Provisorische Absperrung`; `in`: `{spacing:8181}急ごしらえのフェンス`.

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
| rows | 341: 321 in section 2, 20 in section 3 |
| scripts | 28: 16 zone, 12 scene |
| strings per tree | `us` 341, `de` 341, `es` 341, `fr` 341, `it` 341, `in` 341, `kr` 341, `cn` 341, `ch` 341 |
| non-empty strings per tree | `us` 317, `de` 317, `es` 317, `fr` 317, `it` 317, `in` 341, `kr` 341, `cn` 341, `ch` 341 |
| strings with `{alt-font}` | `us` 93, `de` 93, `es` 93, `fr` 93, `it` 93, `in` 93, `kr` 93, `cn` 93, `ch` 93 |
| strings with a choice list | `us` 97, `de` 97, `es` 97, `fr` 96, `it` 97, `in` 97, `kr` 97, `cn` 97, `ch` 97 |
| section 2 rows the scripts table names | 145 |
| section 2 rows a step quotes | 145, in 247 steps |

## Related

- [Garamsythe Waterway scripts](../Story-Events-And-Hunts/garamsythe-waterway-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Garamsythe Waterway scenes](../Story-Events-And-Hunts/garamsythe-waterway-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
