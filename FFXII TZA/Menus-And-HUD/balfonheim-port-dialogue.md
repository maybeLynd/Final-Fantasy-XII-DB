---
title: "Balfonheim Port dialogue: every line and caption of the Balfonheim Port scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[balfonheim-port-dialogue.tsv](balfonheim-port-dialogue.tsv) has one row per string of sections 2 and 3 of the Balfonheim Port scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 845 rows from 13 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Section 2 holds the lines (835 rows) and section 3 the captions (10 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`balfonheim-port-scripts.tsv`](../Story-Events-And-Hunts/balfonheim-port-scripts.tsv), the table of [Balfonheim Port scripts](../Story-Events-And-Hunts/balfonheim-port-scripts.md), names section 2 rows by the same key: 226 of its rows name 769 of the 835 section 2 rows here. The `quoted_lines` column of its steps table quotes 769 of them, in 838 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `var_z0100` | scene | 64 | 0 | 64 | 64 |
| `var_z0101` | scene | 46 | 0 | 46 | 46 |
| `var_z0102` | scene | 47 | 0 | 47 | 47 |
| `var_a01` | zone | 85 | 0 | 60 | 60 |
| `var_a02` | zone | 38 | 0 | 38 | 38 |
| `var_a03` | zone | 46 | 3 | 43 | 43 |
| `var_a04` | zone | 99 | 0 | 96 | 96 |
| `var_a05` | zone | 39 | 0 | 37 | 37 |
| `var_a06` | zone | 41 | 2 | 40 | 40 |
| `var_a11` | zone | 10 | 1 | 10 | 10 |
| `var_a12` | zone | 17 | 1 | 17 | 17 |
| `var_a13` | zone | 8 | 1 | 8 | 8 |
| `var_a14` | zone | 120 | 1 | 115 | 115 |
| `var_a15` | zone | 16 | 1 | 16 | 16 |
| `var_b01` | zone | 158 | 0 | 132 | 132 |
| `var_z01` | zone | 1 | 0 | 0 | 0 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 845 rows.

Empty strings per tree: `us` 12, `de` 12, `es` 12, `fr` 12, `it` 12. No `in`, `kr`, `cn` or `ch` string is empty.

12 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 156 | 156 | 156 | 156 |
| `fontex_expand` | 689 | 689 | 689 | 689 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

116 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 98 with 2, 10 with 3, 1 with 7, 4 with 11, 2 with 26, 1 with 32.

Strings with a choice list per tree: `us` 116, `de` 116, `es` 116, `fr` 116, `it` 116, `in` 116, `kr` 116, `cn` 116, `ch` 116.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `var_a14` 2/4, a line with a line break (`{line}`). `us`: `{speed:8180}Notice Board{line}No new bills posted.`; `in`: `{spacing:8181}{speed:8180}掲示板{line}新しいモブ情報はありません。`.
- `var_z0100` 2/44, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}You're well informed.`; `in`: `{spacing:8180}{speed:8180}{alt-font}妙にお詳しいな`.
- `var_a01` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `var_a03` 3/0, a caption. `us`: `Odo's Technicks`; `de`: `Audes Trickkiste`; `in`: `{spacing:8181}オードの技ショップ`.

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
| rows | 845: 835 in section 2, 10 in section 3 |
| scripts | 16: 13 zone, 3 scene |
| strings per tree | `us` 845, `de` 845, `es` 845, `fr` 845, `it` 845, `in` 845, `kr` 845, `cn` 845, `ch` 845 |
| non-empty strings per tree | `us` 833, `de` 833, `es` 833, `fr` 833, `it` 833, `in` 845, `kr` 845, `cn` 845, `ch` 845 |
| strings with `{alt-font}` | `us` 156, `de` 156, `es` 156, `fr` 156, `it` 156, `in` 156, `kr` 156, `cn` 156, `ch` 156 |
| strings with a choice list | `us` 116, `de` 116, `es` 116, `fr` 116, `it` 116, `in` 116, `kr` 116, `cn` 116, `ch` 116 |
| section 2 rows the scripts table names | 769 |
| section 2 rows a step quotes | 769, in 838 steps |

## Related

- [Balfonheim Port scripts](../Story-Events-And-Hunts/balfonheim-port-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Balfonheim Port scenes](../Story-Events-And-Hunts/balfonheim-port-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
