---
title: "Title screen and location title dialogue: every line and caption of the Title screen and location title scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[titles-dialogue.tsv](titles-dialogue.tsv) has one row per string of sections 2 and 3 of the Title screen and location title scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 4 rows from 4 zone scripts under `plan_map/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`titles-scripts.tsv`](../Story-Events-And-Hunts/titles-scripts.tsv), the table of [Title screen and location title scripts](../Story-Events-And-Hunts/titles-scripts.md), names section 2 rows by the same key: 2 of its rows name 2 of the 4 section 2 rows here.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table |
|---|---|---:|---:|---:|
| `ttl_a01` | zone | 1 | 0 | 0 |
| `ttl_a01_e3` | zone | 1 | 0 | 0 |
| `ttl_b01` | zone | 1 | 0 | 1 |
| `ttl_d01` | zone | 1 | 0 | 1 |

### Where the languages differ

Every row but one has a string in all nine trees:

- `ttl_a01_e3` 2/0 ships only in `kr` and `cn` (`plan_map/ttl_a/ttl_a01/global/ttl_a01_e3.ebp`).

No string is empty in any tree.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

No string of these scripts carries `{alt-font}`, so every one takes the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)).

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

2 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 2 with 2.

Strings with a choice list per tree: `us` 2, `de` 2, `es` 2, `fr` 2, `it` 2, `in` 2, `kr` 2, `cn` 2, `ch` 2.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

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
| rows | 4: 4 in section 2, 0 in section 3 |
| scripts | 4: 4 zone, 0 scene |
| strings per tree | `us` 3, `de` 3, `es` 3, `fr` 3, `it` 3, `in` 3, `kr` 4, `cn` 4, `ch` 3 |
| non-empty strings per tree | `us` 3, `de` 3, `es` 3, `fr` 3, `it` 3, `in` 3, `kr` 4, `cn` 4, `ch` 3 |
| strings with `{alt-font}` | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| strings with a choice list | `us` 2, `de` 2, `es` 2, `fr` 2, `it` 2, `in` 2, `kr` 2, `cn` 2, `ch` 2 |
| section 2 rows the scripts table names | 2 |

## Related

- [Title screen and location title scripts](../Story-Events-And-Hunts/titles-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Location title scenes](../Story-Events-And-Hunts/titles-scenes.md) - the scenes these scripts load.
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
