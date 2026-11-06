---
title: "Sochen Cave Palace dialogue: every line and caption of the Sochen Cave Palace scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[sochen-cave-palace-dialogue.tsv](sochen-cave-palace-dialogue.tsv) has one row per string of sections 2 and 3 of the Sochen Cave Palace scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 153 rows from 11 zone scripts under `plan_map/` and 2 scene scripts under `event/`. Section 2 holds the lines (100 rows) and section 3 the captions (53 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`sochen-cave-palace-scripts.tsv`](../Story-Events-And-Hunts/sochen-cave-palace-scripts.tsv), the table of [Sochen Cave Palace scripts](../Story-Events-And-Hunts/sochen-cave-palace-scripts.md), names section 2 rows by the same key: 44 of its rows name 43 of the 100 section 2 rows here. The `quoted_lines` column of its steps table quotes 43 of them, in 67 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `rui_a0400` | scene | 10 | 0 | 10 | 10 |
| `rui_d0101` | scene | 1 | 0 | 0 | 0 |
| `rui_a01` | zone | 5 | 1 | 5 | 5 |
| `rui_a02` | zone | 6 | 5 | 3 | 3 |
| `rui_a03` | zone | 27 | 3 | 1 | 1 |
| `rui_a04` | zone | 12 | 1 | 11 | 11 |
| `rui_a05` | zone | 26 | 2 | 1 | 1 |
| `rui_b01` | zone | 8 | 30 | 8 | 8 |
| `rui_b02` | zone | 1 | 2 | 0 | 0 |
| `rui_b03` | zone | 1 | 3 | 1 | 1 |
| `rui_c01` | zone | 1 | 2 | 1 | 1 |
| `rui_d01` | zone | 1 | 3 | 1 | 1 |
| `rui_e01` | zone | 1 | 1 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 153 rows.

Empty strings per tree: `us` 7, `de` 7, `es` 7, `fr` 7, `it` 8. No `in`, `kr`, `cn` or `ch` string is empty.

7 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `rui_b03` 3/2: empty in `it`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `rui_d0101` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `rui_a04` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `rui_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `rui_d01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `rui_e01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 10 | 10 | 10 | 10 |
| `fontex_expand` | 143 | 143 | 143 | 143 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 4, `de` 4, `es` 4, `fr` 4, `it` 4.

### Choice lists

35 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 19 with 2, 9 with 3, 1 with 5, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 35, `de` 35, `es` 35, `fr` 35, `it` 35, `in` 35, `kr` 35, `cn` 35, `ch` 35.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `rui_a04` 2/2, a line with a line break (`{line}`). `us`: `{speed:8180}You will now have the option{line}of saving your game.`; `in`: `{spacing:8181}{speed:8180}ここまでの進行をセーブします。`.
- `rui_a0400` 2/4, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}Won't the city watch{line}find us?`; `in`: `{spacing:8180}{speed:8180}{alt-font}街を歩いたら兵隊に捕まりそう`.
- `rui_a03` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `rui_a01` 3/0, a caption. `us`: `Mark of Counsel`; `de`: `Weisungszeichen`; `in`: `{spacing:8181}導きの印`.

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
| rows | 153: 100 in section 2, 53 in section 3 |
| scripts | 13: 11 zone, 2 scene |
| strings per tree | `us` 153, `de` 153, `es` 153, `fr` 153, `it` 153, `in` 153, `kr` 153, `cn` 153, `ch` 153 |
| non-empty strings per tree | `us` 146, `de` 146, `es` 146, `fr` 146, `it` 145, `in` 153, `kr` 153, `cn` 153, `ch` 153 |
| strings with `{alt-font}` | `us` 10, `de` 10, `es` 10, `fr` 10, `it` 10, `in` 10, `kr` 10, `cn` 10, `ch` 10 |
| strings with a choice list | `us` 35, `de` 35, `es` 35, `fr` 35, `it` 35, `in` 35, `kr` 35, `cn` 35, `ch` 35 |
| section 2 rows the scripts table names | 43 |
| section 2 rows a step quotes | 43, in 67 steps |

## Related

- [Sochen Cave Palace scripts](../Story-Events-And-Hunts/sochen-cave-palace-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Sochen Cave Palace scenes](../Story-Events-And-Hunts/sochen-cave-palace-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00355A00` calls `0x0025D5E0`, `0x00269F20`, `0x0026B4A0`; `0x00357120` calls `0x00269F20`; those functions are
  documented on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md).
- Movement: `0x00355A00` calls `0x0026B0C0`, `0x0026B620`, `0x0026BB00`, `0x0026BC70`, `0x0026BD50`, `0x0026BFF0`; those functions
  are documented on [party control modes](../Engine-Core/party-control-modes.md),
  [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md).
- Presentation: `0x001FDD60` is called by `0x001B4590`; those functions are documented on
  [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md).
- Resource: `0x00674A00` is called by `0x001A7A50`, `0x001A9050`, `0x001B1440`, `0x001B1C10`, `0x0020BE50`, `0x0020C1B0`; those
  functions are documented on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [sprite batcher](../Graphics/sprite-batcher.md).
- Resource: and on [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md),
  [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md).
- Script VM: `0x002642C0` is called by `0x00355A00`; `0x00264D60` is called by `0x00348DF0`, `0x0034ADA0`, `0x00352A50`,
  `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0`; `0x00264D90` is called by
  `0x00355A00`, `0x00357120`; `0x00348DF0` calls `0x00267E10`; `0x00348DF0` is called by `0x00349800`; `0x0034ADA0` calls
  `0x00267E10`; `0x0034ADA0` is called by `0x0034B760`, `0x0034BB10`.
- Script VM: `0x00355A00` calls `0x00267E10`; `0x00357120` calls `0x00267E10`; those functions are documented on
  [npc names](../Characters-And-Objects/npc-names.md),
  [archades scenes](../Story-Events-And-Hunts/archades-scenes.md),
  [archades scripts](../Story-Events-And-Hunts/archades-scripts.md),
  [ebp text sections](../EBP-Script-Files/ebp-text-sections.md).
- Script VM: and on [force fight mode](../Engine-Core/force-fight-mode.md).
