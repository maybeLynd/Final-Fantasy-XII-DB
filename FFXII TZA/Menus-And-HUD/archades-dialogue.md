---
title: "Archades dialogue: every line and caption of the Archades scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[archades-dialogue.tsv](archades-dialogue.tsv) has one row per string of sections 2 and 3 of the Archades scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 1,091 rows from 13 zone scripts under `plan_map/` and 10 scene scripts under `event/`. Section 2 holds the lines (1,077 rows) and section 3 the captions (14 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`archades-scripts.tsv`](../Story-Events-And-Hunts/archades-scripts.tsv), the table of [Archades scripts](../Story-Events-And-Hunts/archades-scripts.md), names section 2 rows by the same key: 318 of its rows name 984 of the 1,077 section 2 rows here. The `quoted_lines` column of its steps table quotes 984 of them, in 1,309 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `alc_a0100` | scene | 7 | 0 | 6 | 6 |
| `alc_a0280` | scene | 18 | 0 | 18 | 18 |
| `alc_b0400` | scene | 20 | 0 | 19 | 19 |
| `alc_c0180` | scene | 15 | 0 | 15 | 15 |
| `alc_z0100` | scene | 36 | 0 | 35 | 35 |
| `alc_z0101` | scene | 46 | 0 | 45 | 45 |
| `alc_z0102` | scene | 16 | 0 | 15 | 15 |
| `alc_z0103` | scene | 45 | 0 | 44 | 44 |
| `alc_z0104` | scene | 35 | 0 | 34 | 34 |
| `alc_z0200` | scene | 29 | 0 | 28 | 28 |
| `alc_a01` | zone | 26 | 1 | 26 | 26 |
| `alc_a02` | zone | 22 | 0 | 20 | 20 |
| `alc_b03` | zone | 98 | 2 | 95 | 95 |
| `alc_b04` | zone | 71 | 0 | 70 | 70 |
| `alc_b05` | zone | 38 | 1 | 34 | 34 |
| `alc_b06` | zone | 38 | 1 | 34 | 34 |
| `alc_c01` | zone | 58 | 2 | 33 | 33 |
| `alc_e01` | zone | 137 | 0 | 111 | 111 |
| `alc_f01` | zone | 70 | 2 | 67 | 67 |
| `alc_f02` | zone | 97 | 2 | 94 | 94 |
| `alc_f03` | zone | 34 | 1 | 30 | 30 |
| `alc_f04` | zone | 94 | 1 | 88 | 88 |
| `alc_f05` | zone | 27 | 1 | 23 | 23 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 1,091 rows.

Empty strings per tree: `us` 25, `de` 24, `es` 25, `fr` 25, `it` 28. No `in`, `kr`, `cn` or `ch` string is empty.

24 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `alc_a01` 3/0: empty in `it`.
- `alc_b04` 2/2: empty in `us`, `es` and `fr`.
- `alc_c01` 3/0: empty in `it`.
- `alc_c01` 3/1: empty in `it`.
- `alc_f02` 2/31: empty in `it`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `alc_a02` 2/0: in `us` and `es`.

The rows that carry a choice list in some trees only:

- `alc_b04` 2/2: in `de`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `alc_f02` 2/31: in `us`, `de`, `es`, `fr`, `in`, `kr`, `cn` and `ch`; empty in the other trees.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 224 | 224 | 224 | 224 |
| `fontex_expand` | 867 | 867 | 867 | 867 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 1, `de` 1, `es` 1, `fr` 1, `it` 1.

### Choice lists

212 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 179 with 2, 23 with 3, 1 with 5, 1 with 7, 1 with 10, 4 with 11, 2 with 26, 1 with 32.

Strings with a choice list per tree: `us` 212, `de` 213, `es` 212, `fr` 212, `it` 212, `in` 213, `kr` 213, `cn` 213, `ch` 213.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `alc_c01` 2/55, a line with a line break (`{line}`). `us`: `{instant:8181}Cabbie{line}S-Sir? Yes, sir!`; `in`: `{spacing:8181}{instant:8181}タクシー運転手{line}ハ、ハイ!?`.
- `alc_b0400` 2/4, a line drawn with the alternate font. `us`: `{alt-font}{speed:8180}{center:8180}{line}You've changed, Vaan.`; `in`: `{spacing:8180}{alt-font}{speed:8180}ヴァン{blank}変わったよ`.
- `alc_b0400` 2/0, a line that ends in a choice list. `us`: `View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}もう一度？{line}{choice:2}[もう一度|やめる]`.
- `alc_b03` 3/1, a caption. `us`: `Bulward's Technicks`; `de`: `Techniken-Handlung 'Bulwart'`; `in`: `{spacing:8181}ブルワード技店`.

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
| rows | 1,091: 1,077 in section 2, 14 in section 3 |
| scripts | 23: 13 zone, 10 scene |
| strings per tree | `us` 1,091, `de` 1,091, `es` 1,091, `fr` 1,091, `it` 1,091, `in` 1,091, `kr` 1,091, `cn` 1,091, `ch` 1,091 |
| non-empty strings per tree | `us` 1,066, `de` 1,067, `es` 1,066, `fr` 1,066, `it` 1,063, `in` 1,091, `kr` 1,091, `cn` 1,091, `ch` 1,091 |
| strings with `{alt-font}` | `us` 224, `de` 224, `es` 224, `fr` 224, `it` 224, `in` 224, `kr` 224, `cn` 224, `ch` 224 |
| strings with a choice list | `us` 212, `de` 213, `es` 212, `fr` 212, `it` 212, `in` 213, `kr` 213, `cn` 213, `ch` 213 |
| section 2 rows the scripts table names | 984 |
| section 2 rows a step quotes | 984, in 1,309 steps |

## Related

- [Archades scripts](../Story-Events-And-Hunts/archades-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Archades scenes](../Story-Events-And-Hunts/archades-scenes.md) - the scenes these scripts load.
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
