---
title: "Stilshrine of Miriam dialogue: every line and caption of the Stilshrine of Miriam scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[stilshrine-of-miriam-dialogue.tsv](stilshrine-of-miriam-dialogue.tsv) has one row per string of sections 2 and 3 of the Stilshrine of Miriam scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 204 rows from 12 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Section 2 holds the lines (139 rows) and section 3 the captions (65 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`stilshrine-of-miriam-scripts.tsv`](../Story-Events-And-Hunts/stilshrine-of-miriam-scripts.tsv), the table of [Stilshrine of Miriam scripts](../Story-Events-And-Hunts/stilshrine-of-miriam-scripts.md), names section 2 rows by the same key: 58 of its rows name 82 of the 139 section 2 rows here. The `quoted_lines` column of its steps table quotes 82 of them, in 149 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `mrm_e0101` | scene | 1 | 0 | 1 | 1 |
| `mrm_f0100` | scene | 18 | 0 | 16 | 16 |
| `mrm_g0101` | scene | 1 | 0 | 1 | 1 |
| `mrm_a02` | zone | 40 | 1 | 14 | 14 |
| `mrm_b01` | zone | 15 | 8 | 15 | 15 |
| `mrm_b02` | zone | 1 | 5 | 0 | 0 |
| `mrm_b03` | zone | 7 | 10 | 7 | 7 |
| `mrm_b04` | zone | 7 | 15 | 7 | 7 |
| `mrm_c01` | zone | 11 | 14 | 8 | 8 |
| `mrm_d02` | zone | 4 | 1 | 4 | 4 |
| `mrm_d03` | zone | 25 | 0 | 0 | 0 |
| `mrm_d04` | zone | 6 | 5 | 6 | 6 |
| `mrm_e01` | zone | 1 | 2 | 1 | 1 |
| `mrm_f01` | zone | 0 | 1 | 0 | 0 |
| `mrm_g01` | zone | 2 | 3 | 2 | 2 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 204 rows.

Empty strings per tree: `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9. No `in`, `kr`, `cn` or `ch` string is empty.

9 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `mrm_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `mrm_e01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `mrm_g01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 20 | 20 | 20 | 20 |
| `fontex_expand` | 184 | 184 | 184 | 184 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 3, `de` 3, `es` 3, `fr` 3, `it` 3.

### Choice lists

46 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 16 with 2, 24 with 3, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 46, `de` 46, `es` 46, `fr` 46, `it` 46, `in` 46, `kr` 46, `cn` 46, `ch` 46.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `mrm_d04` 2/5, a line with a line break (`{line}`). `us`: `{speed:8180}{line}The magicks binding the door fade.`; `in`: `{spacing:8181}{speed:8180}扉に施された封印が解けた。`.
- `mrm_f0100` 2/7, a line drawn with the alternate font. `us`: `{alt-font}{speed:8180}{center:8180}{line}It has been roused.`; `in`: `{spacing:8180}{alt-font}{speed:8180}ざわめいてるわ`.
- `mrm_f0100` 2/1, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `mrm_a02` 3/0, a caption. `us`: `Ancient Door`; `de`: `Altes Portal`; `in`: `{spacing:8181}古の扉`.

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
| rows | 204: 139 in section 2, 65 in section 3 |
| scripts | 15: 12 zone, 3 scene |
| strings per tree | `us` 204, `de` 204, `es` 204, `fr` 204, `it` 204, `in` 204, `kr` 204, `cn` 204, `ch` 204 |
| non-empty strings per tree | `us` 195, `de` 195, `es` 195, `fr` 195, `it` 195, `in` 204, `kr` 204, `cn` 204, `ch` 204 |
| strings with `{alt-font}` | `us` 20, `de` 20, `es` 20, `fr` 20, `it` 20, `in` 20, `kr` 20, `cn` 20, `ch` 20 |
| strings with a choice list | `us` 46, `de` 46, `es` 46, `fr` 46, `it` 46, `in` 46, `kr` 46, `cn` 46, `ch` 46 |
| section 2 rows the scripts table names | 82 |
| section 2 rows a step quotes | 82, in 149 steps |

## Related

- [Stilshrine of Miriam scripts](../Story-Events-And-Hunts/stilshrine-of-miriam-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Stilshrine of Miriam scenes](../Story-Events-And-Hunts/stilshrine-of-miriam-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
