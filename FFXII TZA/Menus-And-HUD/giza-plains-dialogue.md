---
title: "Giza Plains dialogue: every line and caption of the Giza Plains scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[giza-plains-dialogue.tsv](giza-plains-dialogue.tsv) has one row per string of sections 2 and 3 of the Giza Plains scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 508 rows from 16 zone scripts under `plan_map/` and 5 scene scripts under `event/`. Section 2 holds the lines (481 rows) and section 3 the captions (27 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `giza-plains-scripts.tsv`, the table of [Giza Plains scripts](../Story-Events-And-Hunts/giza-plains-scripts.md), names section 2 rows by the same key: 145 of its rows name 354 of the 481 section 2 rows here. The `quoted_lines` column of its steps table quotes 354 of them, in 470 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `sav_b0100` | scene | 11 | 0 | 11 | 11 |
| `sav_b0180` | scene | 3 | 0 | 2 | 2 |
| `sav_b0181` | scene | 7 | 0 | 5 | 5 |
| `sav_c0280` | scene | 7 | 0 | 6 | 6 |
| `sav_c0281` | scene | 5 | 0 | 4 | 4 |
| `sav_a01` | zone | 4 | 0 | 2 | 2 |
| `sav_a02` | zone | 9 | 2 | 8 | 8 |
| `sav_a03` | zone | 12 | 2 | 10 | 10 |
| `sav_a04` | zone | 4 | 0 | 2 | 2 |
| `sav_b01` | zone | 234 | 0 | 206 | 206 |
| `sav_c01` | zone | 9 | 2 | 8 | 8 |
| `sav_c02` | zone | 41 | 0 | 14 | 14 |
| `sav_c03` | zone | 9 | 2 | 8 | 8 |
| `sav_d01` | zone | 4 | 3 | 4 | 4 |
| `sav_d03` | zone | 3 | 3 | 3 | 3 |
| `sav_d04` | zone | 3 | 3 | 3 | 3 |
| `sav_e01` | zone | 45 | 3 | 19 | 19 |
| `sav_f01` | zone | 5 | 3 | 3 | 3 |
| `sav_f02` | zone | 54 | 3 | 27 | 27 |
| `sav_f03` | zone | 4 | 1 | 4 | 4 |
| `sav_g01` | zone | 8 | 0 | 5 | 5 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 508 rows.

Empty strings per tree: `us` 25, `de` 25, `es` 25, `fr` 25, `it` 25. No `in`, `kr`, `cn` or `ch` string is empty.

25 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `sav_b0180` 2/0: in `es`.
- `sav_b0181` 2/0: in `es`.
- `sav_b0181` 2/1: in `es`.
- `sav_c0280` 2/0: in `es`.
- `sav_c0281` 2/0: in `es`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 10 | 10 | 10 | 10 |
| `fontex_expand` | 498 | 498 | 498 | 498 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

88 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 64 with 2, 10 with 3, 1 with 4, 1 with 7, 8 with 11, 4 with 26.

Strings with a choice list per tree: `us` 88, `de` 88, `es` 88, `fr` 88, `it` 88, `in` 88, `kr` 88, `cn` 88, `ch` 88.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `sav_b0181` 2/5, a line with a line break (`{line}`). `us`: `{instant:8181}Penelo{line}Well, you ready to go?`; `in`: `{spacing:8181}{instant:8181}パンネロ{line}じゃあ、行こっか。`.
- `sav_b0100` 2/4, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}What? I'm being good.`; `in`: `{spacing:8180}{speed:8180}{alt-font}なんでもないって`.
- `sav_b01` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `sav_a02` 3/0, a caption. `us`: `Dark Crystal`; `de`: `Obsidiant`; `in`: `{spacing:8181}黒水晶`.

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
| rows | 508: 481 in section 2, 27 in section 3 |
| scripts | 21: 16 zone, 5 scene |
| strings per tree | `us` 508, `de` 508, `es` 508, `fr` 508, `it` 508, `in` 508, `kr` 508, `cn` 508, `ch` 508 |
| non-empty strings per tree | `us` 483, `de` 483, `es` 483, `fr` 483, `it` 483, `in` 508, `kr` 508, `cn` 508, `ch` 508 |
| strings with `{alt-font}` | `us` 10, `de` 10, `es` 10, `fr` 10, `it` 10, `in` 10, `kr` 10, `cn` 10, `ch` 10 |
| strings with a choice list | `us` 88, `de` 88, `es` 88, `fr` 88, `it` 88, `in` 88, `kr` 88, `cn` 88, `ch` 88 |
| section 2 rows the scripts table names | 354 |
| section 2 rows a step quotes | 354, in 470 steps |

## Related

- [Giza Plains scripts](../Story-Events-And-Hunts/giza-plains-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Giza Plains scenes](../Story-Events-And-Hunts/giza-plains-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
