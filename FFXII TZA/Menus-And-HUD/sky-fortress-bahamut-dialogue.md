---
title: "Sky Fortress Bahamut dialogue: every line and caption of the Sky Fortress Bahamut scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[sky-fortress-bahamut-dialogue.tsv](sky-fortress-bahamut-dialogue.tsv) has one row per string of sections 2 and 3 of the Sky Fortress Bahamut scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 373 rows from 7 zone scripts under `plan_map/` and 12 scene scripts under `event/`. Section 2 holds the lines (345 rows) and section 3 the captions (28 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `sky-fortress-bahamut-scripts.tsv`, the table of [Sky Fortress Bahamut scripts](../Story-Events-And-Hunts/sky-fortress-bahamut-scripts.md), names section 2 rows by the same key: 164 of its rows name 308 of the 345 section 2 rows here. The `quoted_lines` column of its steps table quotes 308 of them, in 358 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `bhm_a0200` | scene | 23 | 0 | 22 | 22 |
| `bhm_a0400` | scene | 7 | 0 | 7 | 7 |
| `bhm_b0100` | scene | 16 | 0 | 16 | 16 |
| `bhm_b0101` | scene | 11 | 0 | 11 | 11 |
| `bhm_c0100` | scene | 19 | 0 | 18 | 18 |
| `bhm_c0101` | scene | 11 | 0 | 10 | 10 |
| `bhm_c0102` | scene | 16 | 0 | 16 | 16 |
| `bhm_d0100` | scene | 12 | 0 | 11 | 11 |
| `bhm_d0101` | scene | 91 | 0 | 89 | 89 |
| `bhm_y0100` | scene | 54 | 0 | 52 | 52 |
| `bhm_y0101` | scene | 15 | 0 | 14 | 14 |
| `bhm_z0100` | scene | 34 | 0 | 31 | 31 |
| `bhm_a01` | zone | 0 | 8 | 0 | 0 |
| `bhm_a02` | zone | 0 | 1 | 0 | 0 |
| `bhm_a03` | zone | 0 | 8 | 0 | 0 |
| `bhm_a04` | zone | 32 | 9 | 7 | 7 |
| `bhm_b01` | zone | 2 | 2 | 2 | 2 |
| `bhm_c01` | zone | 1 | 0 | 1 | 1 |
| `bhm_d01` | zone | 1 | 0 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 373 rows.

Empty strings per tree: `us` 12, `de` 12, `es` 15, `fr` 12, `it` 12. No `in`, `kr`, `cn` or `ch` string is empty.

12 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `bhm_y0100` 2/36: empty in `es`.
- `bhm_y0100` 2/42: empty in `es`.
- `bhm_y0100` 2/43: empty in `es`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `bhm_b01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bhm_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `bhm_d01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

The rows that carry `{alt-font}` in some trees only:

- `bhm_a0200` 2/16: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `bhm_a0200` 2/17: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `bhm_a0200` 2/18: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `bhm_a0200` 2/20: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `bhm_y0100` 2/36: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `bhm_y0100` 2/37: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `bhm_y0100` 2/42: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `bhm_y0100` 2/43: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `bhm_z0100` 2/31: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `bhm_z0100` 2/32: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 275 | 275 | 275 | 275 |
| `fontex_expand` | 98 | 98 | 98 | 98 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 3, `de` 3, `es` 3, `fr` 3, `it` 3.

### Choice lists

25 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 4 with 1, 11 with 2, 5 with 3, 1 with 4, 1 with 7, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 25, `de` 25, `es` 25, `fr` 25, `it` 25, `in` 25, `kr` 25, `cn` 25, `ch` 25.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `bhm_a04` 2/28, a line with a line break (`{line}`). `us`: `{instant:8181}Basch{line}This is no time for doubt. Here we end this.`; `in`: `{spacing:8181}{instant:8181}バッシュ{line}逃げ出すことなどできない。{line}今ここで、すべてに決着をつけなくては。`.
- `bhm_b0101` 2/2, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}Let this end, Noah.`; `in`: `{spacing:8180}{speed:8180}{alt-font}そうだろう{blank}ノア`.
- `bhm_c0100` 2/0, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `bhm_a01` 3/0, a caption. `us`: `Bulkhead 1`; `de`: `Schott 1`; `in`: `{spacing:8181}第１隔壁`.

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
| rows | 373: 345 in section 2, 28 in section 3 |
| scripts | 19: 7 zone, 12 scene |
| strings per tree | `us` 373, `de` 373, `es` 373, `fr` 373, `it` 373, `in` 373, `kr` 373, `cn` 373, `ch` 373 |
| non-empty strings per tree | `us` 361, `de` 361, `es` 358, `fr` 361, `it` 361, `in` 373, `kr` 373, `cn` 373, `ch` 373 |
| strings with `{alt-font}` | `us` 282, `de` 282, `es` 279, `fr` 282, `it` 282, `in` 275, `kr` 275, `cn` 275, `ch` 275 |
| strings with a choice list | `us` 25, `de` 25, `es` 25, `fr` 25, `it` 25, `in` 25, `kr` 25, `cn` 25, `ch` 25 |
| section 2 rows the scripts table names | 308 |
| section 2 rows a step quotes | 308, in 358 steps |

## Related

- [Sky Fortress Bahamut scripts](../Story-Events-And-Hunts/sky-fortress-bahamut-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Sky Fortress Bahamut scenes](../Story-Events-And-Hunts/sky-fortress-bahamut-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
