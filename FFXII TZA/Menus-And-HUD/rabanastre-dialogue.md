---
title: "Rabanastre dialogue: every line and caption of the Rabanastre scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[rabanastre-dialogue.tsv](rabanastre-dialogue.tsv) has one row per string of sections 2 and 3 of the Rabanastre scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 1,946 rows from 17 zone scripts under `plan_map/` and 16 scene scripts under `event/`. Section 2 holds the lines (1,914 rows) and section 3 the captions (32 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `rabanastre-scripts.tsv`, the table of [Rabanastre scripts](../Story-Events-And-Hunts/rabanastre-scripts.md), names section 2 rows by the same key: 354 of its rows name 1,797 of the 1,914 section 2 rows here. The `quoted_lines` column of its steps table quotes 1,797 of them, in 2,508 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `rbn_a0100` | scene | 25 | 0 | 24 | 24 |
| `rbn_a0200` | scene | 12 | 0 | 9 | 9 |
| `rbn_a0300` | scene | 26 | 0 | 26 | 26 |
| `rbn_a0380` | scene | 16 | 0 | 16 | 16 |
| `rbn_a0381` | scene | 13 | 0 | 13 | 13 |
| `rbn_a0382` | scene | 10 | 0 | 10 | 10 |
| `rbn_a0480` | scene | 13 | 0 | 13 | 13 |
| `rbn_a0980` | scene | 15 | 0 | 14 | 14 |
| `rbn_a1300` | scene | 42 | 0 | 42 | 42 |
| `rbn_a1600` | scene | 22 | 0 | 22 | 22 |
| `rbn_a1601` | scene | 17 | 0 | 17 | 17 |
| `rbn_a1700` | scene | 17 | 0 | 17 | 17 |
| `rbn_a1701` | scene | 38 | 0 | 38 | 38 |
| `rbn_x0100` | scene | 21 | 0 | 21 | 21 |
| `rbn_y0100` | scene | 66 | 0 | 64 | 64 |
| `rbn_z0100` | scene | 6 | 0 | 6 | 6 |
| `rbn_a01` | zone | 109 | 4 | 106 | 106 |
| `rbn_a02` | zone | 137 | 2 | 136 | 136 |
| `rbn_a03` | zone | 142 | 7 | 135 | 135 |
| `rbn_a04` | zone | 121 | 3 | 119 | 119 |
| `rbn_a07` | zone | 38 | 1 | 36 | 36 |
| `rbn_a08` | zone | 23 | 1 | 23 | 23 |
| `rbn_a09` | zone | 56 | 1 | 54 | 54 |
| `rbn_a10` | zone | 39 | 1 | 38 | 38 |
| `rbn_a11` | zone | 29 | 1 | 29 | 29 |
| `rbn_a12` | zone | 34 | 2 | 34 | 34 |
| `rbn_a13` | zone | 0 | 1 | 0 | 0 |
| `rbn_a14` | zone | 254 | 1 | 247 | 247 |
| `rbn_a16` | zone | 161 | 1 | 154 | 154 |
| `rbn_a17` | zone | 94 | 2 | 69 | 69 |
| `rbn_a18` | zone | 72 | 2 | 48 | 48 |
| `rbn_a19` | zone | 90 | 2 | 64 | 64 |
| `rbn_b01` | zone | 156 | 0 | 153 | 153 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 1,946 rows.

Empty strings per tree: `us` 24, `de` 24, `es` 24, `fr` 24, `it` 25. No `in`, `kr`, `cn` or `ch` string is empty.

24 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `rbn_a02` 3/1: empty in `it`.

The rows that carry a choice list in some trees only:

- `rbn_a14` 2/110: in `de`, `es`, `fr`, `it`, `in`, `kr`, `cn` and `ch`, not in `us`.
- `rbn_a14` 2/112: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`, not in `es`.
- `rbn_a17` 2/63: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`, not in `es`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 371 | 371 | 371 | 371 |
| `fontex_expand` | 1,575 | 1,575 | 1,575 | 1,575 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

214 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 176 with 2, 19 with 3, 5 with 6, 2 with 7, 6 with 11, 1 with 13, 1 with 14, 3 with 26, 1 with 32.

Strings with a choice list per tree: `us` 214, `de` 215, `es` 213, `fr` 215, `it` 215, `in` 215, `kr` 215, `cn` 215, `ch` 215.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `rbn_a10` 2/23, a line with a line break (`{line}`). `us`: `{instant:8181}???{line}Is it...is it really you!?`; `in`: `{spacing:8181}{instant:8181}？？？？{line}兄さん！`.
- `rbn_a0100` 2/8, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}As if I'd know.`; `in`: `{spacing:8180}{speed:8180}{alt-font}そんなの知らないよ`.
- `rbn_y0100` 2/1, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `rbn_a01` 3/0, a caption. `us`: `Stair to Lowtown`; `de`: `Treppe zur Unterstadt`; `in`: `{spacing:8181}ダウンタウンへの階段`.

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
| rows | 1,946: 1,914 in section 2, 32 in section 3 |
| scripts | 33: 17 zone, 16 scene |
| strings per tree | `us` 1,946, `de` 1,946, `es` 1,946, `fr` 1,946, `it` 1,946, `in` 1,946, `kr` 1,946, `cn` 1,946, `ch` 1,946 |
| non-empty strings per tree | `us` 1,922, `de` 1,922, `es` 1,922, `fr` 1,922, `it` 1,921, `in` 1,946, `kr` 1,946, `cn` 1,946, `ch` 1,946 |
| strings with `{alt-font}` | `us` 371, `de` 371, `es` 371, `fr` 371, `it` 371, `in` 371, `kr` 371, `cn` 371, `ch` 371 |
| strings with a choice list | `us` 214, `de` 215, `es` 213, `fr` 215, `it` 215, `in` 215, `kr` 215, `cn` 215, `ch` 215 |
| section 2 rows the scripts table names | 1,797 |
| section 2 rows a step quotes | 1,797, in 2,508 steps |

## Related

- [Rabanastre scripts](../Story-Events-And-Hunts/rabanastre-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Rabanastre scenes](../Story-Events-And-Hunts/rabanastre-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
