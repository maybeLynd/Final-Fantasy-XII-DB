---
title: "Ridorana Cataract dialogue: every line and caption of the Ridorana Cataract scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[ridorana-cataract-dialogue.tsv](ridorana-cataract-dialogue.tsv) has one row per string of sections 2 and 3 of the Ridorana Cataract scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 96 rows from 4 zone scripts under `plan_map/` and 2 scene scripts under `event/`. Section 2 holds the lines (95 rows) and section 3 the captions (1 row) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of [`ridorana-cataract-scripts.tsv`](../Story-Events-And-Hunts/ridorana-cataract-scripts.tsv), the table of [Ridorana Cataract scripts](../Story-Events-And-Hunts/ridorana-cataract-scripts.md), names section 2 rows by the same key: 17 of its rows name 37 of the 95 section 2 rows here. The `quoted_lines` column of its steps table quotes 37 of them, in 38 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `rwf_a0100` | scene | 15 | 0 | 13 | 13 |
| `rwf_c0102` | scene | 20 | 0 | 18 | 18 |
| `rwf_a01` | zone | 28 | 0 | 3 | 3 |
| `rwf_b02` | zone | 25 | 0 | 0 | 0 |
| `rwf_c01` | zone | 3 | 1 | 2 | 2 |
| `rwf_d01` | zone | 4 | 0 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 96 rows.

Empty strings per tree: `us` 7, `de` 7, `es` 7, `fr` 7, `it` 7. No `in`, `kr`, `cn` or `ch` string is empty.

7 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `rwf_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `rwf_d01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 30 | 30 | 30 | 30 |
| `fontex_expand` | 66 | 66 | 66 | 66 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 2, `de` 2, `es` 2, `fr` 2, `it` 2.

### Choice lists

30 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 18 with 2, 6 with 3, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 30, `de` 30, `es` 30, `fr` 30, `it` 30, `in` 30, `kr` 30, `cn` 30, `ch` 30.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `rwf_a01` 2/13, a line with a line break (`{line}`). `us`: `{actor-name:8180}{line}{speed:8180}A strong Mist prevents saving.`; `in`: `{spacing:8181}{actor-name:8180}{line}{speed:8180}ミストの干渉により、セーブすることはできません。`.
- `rwf_c0102` 2/14, a line drawn with the alternate font. `us`: `{alt-font}{speed:8180}{center:8180}{line}Does it startle you?`; `in`: `{spacing:8180}{alt-font}{speed:8180}驚くほどのことかしら`.
- `rwf_a0100` 2/1, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `rwf_c01` 3/0, a caption. `us`: `Inscription`; `de`: `Wandinschrift`; `in`: `{spacing:8181}壁の碑文`.

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
| rows | 96: 95 in section 2, 1 in section 3 |
| scripts | 6: 4 zone, 2 scene |
| strings per tree | `us` 96, `de` 96, `es` 96, `fr` 96, `it` 96, `in` 96, `kr` 96, `cn` 96, `ch` 96 |
| non-empty strings per tree | `us` 89, `de` 89, `es` 89, `fr` 89, `it` 89, `in` 96, `kr` 96, `cn` 96, `ch` 96 |
| strings with `{alt-font}` | `us` 30, `de` 30, `es` 30, `fr` 30, `it` 30, `in` 30, `kr` 30, `cn` 30, `ch` 30 |
| strings with a choice list | `us` 30, `de` 30, `es` 30, `fr` 30, `it` 30, `in` 30, `kr` 30, `cn` 30, `ch` 30 |
| section 2 rows the scripts table names | 37 |
| section 2 rows a step quotes | 37, in 38 steps |

## Related

- [Ridorana Cataract scripts](../Story-Events-And-Hunts/ridorana-cataract-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Ridorana Cataract scenes](../Story-Events-And-Hunts/ridorana-cataract-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
