---
title: "Golmore Jungle dialogue: every line and caption of the Golmore Jungle scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[golmore-jungle-dialogue.tsv](golmore-jungle-dialogue.tsv) has one row per string of sections 2 and 3 of the Golmore Jungle scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 61 rows from 7 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Section 2 holds the lines (60 rows) and section 3 the captions (1 row) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`golmore-jungle-scripts.tsv`](../Story-Events-And-Hunts/golmore-jungle-scripts.tsv), the table of [Golmore Jungle scripts](../Story-Events-And-Hunts/golmore-jungle-scripts.md), names section 2 rows by the same key: 21 of its rows name 28 of the 60 section 2 rows here.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table |
|---|---|---:|---:|---:|
| `gol_a0200` | scene | 20 | 0 | 20 |
| `gol_c0100` | scene | 1 | 0 | 0 |
| `gol_c0101` | scene | 1 | 0 | 0 |
| `gol_a01` | zone | 3 | 0 | 0 |
| `gol_a02` | zone | 2 | 1 | 2 |
| `gol_a03` | zone | 1 | 0 | 1 |
| `gol_a04` | zone | 28 | 0 | 3 |
| `gol_b01` | zone | 2 | 0 | 0 |
| `gol_c01` | zone | 1 | 0 | 1 |
| `gol_d01` | zone | 1 | 0 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 61 rows.

Empty strings per tree: `us` 6, `de` 6, `es` 6, `fr` 6, `it` 6. No `in`, `kr`, `cn` or `ch` string is empty.

6 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `gol_c0100` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `gol_c0101` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `gol_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 20 | 20 | 20 | 20 |
| `fontex_expand` | 41 | 41 | 41 | 41 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 1, `de` 1, `es` 1, `fr` 1, `it` 1.

### Choice lists

17 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 11 with 2, 3 with 3, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 17, `de` 17, `es` 17, `fr` 17, `it` 17, `in` 17, `kr` 17, `cn` 17, `ch` 17.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `gol_a04` 2/13, a line with a line break (`{line}`). `us`: `{actor-name:8180}{line}{speed:8180}A strong Mist prevents saving.`; `in`: `{spacing:8181}{actor-name:8180}{line}{speed:8180}ミストの干渉により、セーブすることはできません。`.
- `gol_a0200` 2/9, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}Our choices are few.`; `in`: `{spacing:8180}{speed:8180}{alt-font}他に方法がないから`.
- `gol_a04` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `gol_a02` 3/0, a caption. `us`: `Hidden Path`; `de`: `Verborgener Pfad`; `in`: `{spacing:8181}森に閉ざされた路`.

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
| rows | 61: 60 in section 2, 1 in section 3 |
| scripts | 10: 7 zone, 3 scene |
| strings per tree | `us` 61, `de` 61, `es` 61, `fr` 61, `it` 61, `in` 61, `kr` 61, `cn` 61, `ch` 61 |
| non-empty strings per tree | `us` 55, `de` 55, `es` 55, `fr` 55, `it` 55, `in` 61, `kr` 61, `cn` 61, `ch` 61 |
| strings with `{alt-font}` | `us` 20, `de` 20, `es` 20, `fr` 20, `it` 20, `in` 20, `kr` 20, `cn` 20, `ch` 20 |
| strings with a choice list | `us` 17, `de` 17, `es` 17, `fr` 17, `it` 17, `in` 17, `kr` 17, `cn` 17, `ch` 17 |
| section 2 rows the scripts table names | 28 |

## Related

- [Golmore Jungle scripts](../Story-Events-And-Hunts/golmore-jungle-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Golmore Jungle scenes](../Story-Events-And-Hunts/golmore-jungle-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
