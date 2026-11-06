---
title: "Dreadnought Leviathan dialogue: every line and caption of the Dreadnought Leviathan scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[dreadnought-leviathan-dialogue.tsv](dreadnought-leviathan-dialogue.tsv) has one row per string of sections 2 and 3 of the Dreadnought Leviathan scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 343 rows from 9 zone scripts under `plan_map/` and 12 scene scripts under `event/`. Section 2 holds the lines (316 rows) and section 3 the captions (27 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`dreadnought-leviathan-scripts.tsv`](../Story-Events-And-Hunts/dreadnought-leviathan-scripts.tsv), the table of [Dreadnought Leviathan scripts](../Story-Events-And-Hunts/dreadnought-leviathan-scripts.md), names section 2 rows by the same key: 145 of its rows name 253 of the 316 section 2 rows here. The `quoted_lines` column of its steps table quotes 253 of them, in 317 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `rsn_a0100` | scene | 15 | 0 | 15 | 15 |
| `rsn_a0101` | scene | 11 | 0 | 11 | 11 |
| `rsn_a0102` | scene | 11 | 0 | 10 | 10 |
| `rsn_b0100` | scene | 23 | 0 | 23 | 23 |
| `rsn_b0180` | scene | 7 | 0 | 6 | 6 |
| `rsn_d0100` | scene | 1 | 0 | 1 | 1 |
| `rsn_d0180` | scene | 6 | 0 | 6 | 6 |
| `rsn_y0100` | scene | 10 | 0 | 10 | 10 |
| `rsn_z0100` | scene | 37 | 0 | 35 | 35 |
| `rsn_z0101` | scene | 34 | 0 | 34 | 34 |
| `rsn_z0200` | scene | 30 | 0 | 29 | 29 |
| `rsn_z0201` | scene | 24 | 0 | 23 | 23 |
| `rsn_a01` | zone | 28 | 1 | 2 | 2 |
| `rsn_b01` | zone | 3 | 1 | 1 | 1 |
| `rsn_b02` | zone | 12 | 3 | 12 | 12 |
| `rsn_b03` | zone | 6 | 2 | 6 | 6 |
| `rsn_b04` | zone | 17 | 4 | 17 | 17 |
| `rsn_c01` | zone | 2 | 3 | 2 | 2 |
| `rsn_d01` | zone | 6 | 8 | 4 | 4 |
| `rsn_y01` | zone | 32 | 5 | 5 | 5 |
| `rsn_z02` | zone | 1 | 0 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 343 rows.

Empty strings per tree: `us` 16, `de` 16, `es` 17, `fr` 16, `it` 22. No `in`, `kr`, `cn` or `ch` string is empty.

16 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `rsn_z0101` 2/10: empty in `es`.
- `rsn_d01` 3/1: empty in `it`.
- `rsn_d01` 3/2: empty in `it`.
- `rsn_d01` 3/3: empty in `it`.
- `rsn_d01` 3/4: empty in `it`.
- `rsn_d01` 3/5: empty in `it`.
- `rsn_d01` 3/6: empty in `it`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `rsn_a01` 2/25: in `us`, `de`, `es`, `fr` and `it`.
- `rsn_d01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `rsn_z02` 2/0: in `us`, `de`, `es`, `fr` and `it`.

The rows that carry `{alt-font}` in some trees only:

- `rsn_z0101` 2/10: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `rsn_z0200` 2/4: in `us`, `de`, `es`, `fr`, `it`, `in`, `cn` and `ch`, not in `kr`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 196 | 195 | 196 | 196 |
| `fontex_expand` | 147 | 148 | 147 | 147 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 2, `de` 2, `es` 2, `fr` 2, `it` 2.

### Choice lists

36 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 20 with 2, 10 with 3, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 36, `de` 36, `es` 36, `fr` 36, `it` 36, `in` 36, `kr` 36, `cn` 36, `ch` 36.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `rsn_b02` 2/1, a line with a line break (`{line}`). `us`: `{speed:8180}{actor-name:8180}{line}"Insert access key."`; `in`: `{spacing:8181}{speed:8180}{actor-name:8180}{line}「制御キーを挿入してください。」{line}この端末の操作には制御キーが必要なようだ。`.
- `rsn_z0100` 2/12, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}The Resistance.`; `in`: `{spacing:8180}{speed:8180}{alt-font}解放軍です`.
- `rsn_z0100` 2/0, a line that ends in a choice list. `us`: `{speed:8180}View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}{speed:8180}Replay？{line}{choice:2}[yes|no]`.
- `rsn_a01` 3/0, a caption. `us`: `West Block`; `de`: `Westblock-Schleuse`; `in`: `{spacing:8181}中層西ブロックへの扉`.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script file under `plan_master/<language>/`: `plan_map/...` for a zone script, `event/...` for a scene script |
| `section` | `2` for a line of the message bank, `3` for a caption |
| `id` | the entry number in that section, from 0: the text id a verb passes |
| `us` to `ch` | the string in that language tree, decoded with the tree's font |
| `missing` | the languages whose tree has no string at this key (no such script, or a shorter section), comma-separated; empty when all nine have one |
| `same_bytes` | the groups of languages whose string bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more, and the languages in `missing` take no part |
| `shown_when` | when the game shows the line, in game terms: what starts the function that prints it (a talk, a touch, a scene's start, a request from another function with that function's own start, a slot change), then the tests the printing step runs under, each with its line in the script's decompiled listing; several printing steps are joined with "or". A value the scripts save is named by its label in [saved-value-stores.tsv](../World-Areas-And-Travel/saved-value-stores.tsv), whose rows give each store of it with its own condition. `-` on a caption (section 3): a caption is not shown by a message verb; the field sign verbs give it to an actor as its name text |

An empty cell under a language not in `missing` is an empty string.

## Data

| Fact | Value |
|---|---|
| rows | 343: 316 in section 2, 27 in section 3 |
| scripts | 21: 9 zone, 12 scene |
| strings per tree | `us` 343, `de` 343, `es` 343, `fr` 343, `it` 343, `in` 343, `kr` 343, `cn` 343, `ch` 343 |
| non-empty strings per tree | `us` 327, `de` 327, `es` 326, `fr` 327, `it` 321, `in` 343, `kr` 343, `cn` 343, `ch` 343 |
| strings with `{alt-font}` | `us` 196, `de` 196, `es` 195, `fr` 196, `it` 196, `in` 196, `kr` 195, `cn` 196, `ch` 196 |
| strings with a choice list | `us` 36, `de` 36, `es` 36, `fr` 36, `it` 36, `in` 36, `kr` 36, `cn` 36, `ch` 36 |
| section 2 rows the scripts table names | 253 |
| section 2 rows a step quotes | 253, in 317 steps |

## Related

- [Dreadnought Leviathan scripts](../Story-Events-And-Hunts/dreadnought-leviathan-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Dreadnought Leviathan scenes](../Story-Events-And-Hunts/dreadnought-leviathan-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
