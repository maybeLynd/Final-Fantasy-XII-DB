---
title: "Dalmasca Estersand dialogue: every line and caption of the Dalmasca Estersand scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[dalmasca-estersand-dialogue.tsv](dalmasca-estersand-dialogue.tsv) has one row per string of sections 2 and 3 of the Dalmasca Estersand scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 565 rows from 10 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Section 2 holds the lines (562 rows) and section 3 the captions (3 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`dalmasca-estersand-scripts.tsv`](../Story-Events-And-Hunts/dalmasca-estersand-scripts.tsv), the table of [Dalmasca Estersand scripts](../Story-Events-And-Hunts/dalmasca-estersand-scripts.md), names section 2 rows by the same key: 95 of its rows name 495 of the 562 section 2 rows here. The `quoted_lines` column of its steps table quotes 495 of them, in 5,981 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `dst_a0181` | scene | 4 | 0 | 4 | 4 |
| `dst_a0580` | scene | 6 | 0 | 6 | 6 |
| `dst_b0100` | scene | 85 | 0 | 85 | 85 |
| `dst_a01` | zone | 4 | 0 | 2 | 2 |
| `dst_a02` | zone | 3 | 0 | 1 | 1 |
| `dst_a04` | zone | 2 | 0 | 1 | 1 |
| `dst_a05` | zone | 38 | 0 | 12 | 12 |
| `dst_a06` | zone | 7 | 1 | 7 | 7 |
| `dst_a07` | zone | 52 | 0 | 49 | 49 |
| `dst_b01` | zone | 260 | 0 | 229 | 229 |
| `dst_b02` | zone | 98 | 0 | 97 | 97 |
| `dst_c01` | zone | 2 | 0 | 2 | 2 |
| `dst_c02` | zone | 1 | 2 | 0 | 0 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 565 rows.

Empty strings per tree: `us` 13, `de` 13, `es` 14, `fr` 13, `it` 13. No `in`, `kr`, `cn` or `ch` string is empty.

13 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `dst_b02` 2/28: empty in `es`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `dst_a01` 2/2: in `us`, `de`, `es`, `fr` and `it`.
- `dst_a05` 2/36: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 9 | 9 | 9 | 9 |
| `fontex_expand` | 556 | 556 | 556 | 556 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

68 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 44 with 2, 10 with 3, 4 with 4, 1 with 5, 1 with 6, 2 with 7, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 68, `de` 68, `es` 68, `fr` 68, `it` 68, `in` 68, `kr` 68, `cn` 68, `ch` 68.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

A code the table writes by its own bytes is the code with those bytes on Text codes: `{0F3D:8180}` is `0F 3D` with the payload `81 80`. Such codes in all nine columns: `{0F3D:...}` 594.

Examples, by script, section and id:

- `dst_b01` 2/194, a line with a line break (`{line}`). `us`: `{name:8281AA}{line}{0F3D:8180}Gimme the sign, boy!`; `in`: `{spacing:8181}{name:8281AA}{line}{0F3D:8180}どの魚が来たか、サインで教えてくれ！`.
- `dst_a0580` 2/3, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}By your leave, Captain.`; `in`: `{spacing:8180}{speed:8180}{alt-font}かまわんな{blank}将軍？`.
- `dst_a05` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `dst_a06` 3/0, a caption. `us`: `Weather-beaten Door`; `de`: `Verwitterte Tür`; `in`: `{spacing:8181}古ぼけた扉`.

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
| `speaker` | who speaks the line, by these rules in order. `caption` on a section 3 row. The line's own name: the `{name}` header before its first `{line}`, read as the game reads it (the second name of the npcdic pair), or a plain name there. Else the `speaker` cell of the row of the scripts table that names the line: a cell lists its speakers in line order, each once, so as many speakers as lines gives one each, one speaker gives every line, and otherwise the line takes the speakers the order of first appearance allows it (a line whose voice cue names one of them keeps that one); a one-line row with more speakers than lines gives them all, joined with " & ", as they say the line together; a cell that the actor's name verbs fill gives the names the actor takes, and a save crystal takes the name its map's crystal number selects. Else the actors whose functions pass the line's id to a message verb in the script's decompiled listing, with the name the actor's `setnpcname` gives, or `no name shown`; a scene subtitle of an actor without a name takes the speaker of its joined voice cue. A voice cue names its character's game name, or else the speaker's label in the form `LABEL (script label)`, and names no speaker when its sound code belongs to another character; a cue with the label `REX` or `Rex` and the sound code `Rx` names Reks, whose high-detail model the actor of that label binds. Several speakers are joined with " or ": the actors who speak in that scene, the names one actor takes, or the speakers of each function that shows the line; one of them shows or says it, and each group is followed by the function that shows it (`actor.function`). For lines no message window shows: `screen text, no speaker`, `gauge label, no speaker`, `field sign, no speaker`, `name text over an actor, no speaker`; `no script asks for this line` when no verb of the script passes the line's id; `no us script holds this line` for a script the us tree does not ship |

An empty cell under a language not in `missing` is an empty string.

## Data

| Fact | Value |
|---|---|
| rows | 565: 562 in section 2, 3 in section 3 |
| scripts | 13: 10 zone, 3 scene |
| strings per tree | `us` 565, `de` 565, `es` 565, `fr` 565, `it` 565, `in` 565, `kr` 565, `cn` 565, `ch` 565 |
| non-empty strings per tree | `us` 552, `de` 552, `es` 551, `fr` 552, `it` 552, `in` 565, `kr` 565, `cn` 565, `ch` 565 |
| strings with `{alt-font}` | `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9, `in` 9, `kr` 9, `cn` 9, `ch` 9 |
| strings with a choice list | `us` 68, `de` 68, `es` 68, `fr` 68, `it` 68, `in` 68, `kr` 68, `cn` 68, `ch` 68 |
| section 2 rows the scripts table names | 495 |
| section 2 rows a step quotes | 495, in 5,981 steps |
| speakers | 562 section 2 rows: 367 by the line's own name; 127 from the scripts table's `speaker` cells; 52 from the actors whose functions show the line; 8 shown with no speaker (screen text, gauge labels, field signs, name text); 8 no script asks for; 3 captions |

## Related

- [Dalmasca Estersand scripts](../Story-Events-And-Hunts/dalmasca-estersand-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Dalmasca Estersand scenes](../Story-Events-And-Hunts/dalmasca-estersand-scenes.md) - the scenes these scripts load.
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
- Movement: `0x00355A00` calls `0x0026AB60`, `0x0026B0C0`, `0x0026B620`, `0x0026BB00`, `0x0026BC70`, `0x0026BD50`, `0x0026BDD0`,
  `0x0026BFF0`; those functions
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
