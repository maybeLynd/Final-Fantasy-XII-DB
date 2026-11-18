[Home](../../README.md) / [Menus and HUD](README.md) / Cerobi Steppe dialogue

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Cerobi Steppe dialogue: every line and caption of the Cerobi Steppe scripts in all nine languages | reference | Menus and HUD | Dialogue / Archades | Every string of sections 2 and 3 of the Cerobi Steppe zone scripts side by side in the nine language trees: the lines the message verbs show and the captions the field signs show, keyed by script, section and text id as the Cerobi Steppe scripts table names them, with the row count per language, where the languages differ, the strings drawn with the alternate font and the choice lists. | 0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350 |

## What it lists

[cerobi-steppe-dialogue.tsv](cerobi-steppe-dialogue.tsv) has one row per string of sections 2 and 3 of the Cerobi Steppe scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 880 rows from 8 zone scripts under `plan_map/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes`¹, which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff`² look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign`³ and `fieldsignmesbyid`⁴ read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record⁵, and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative⁶.
- The `lines` column of [`cerobi-steppe-scripts.tsv`](../Story-Events-And-Hunts/cerobi-steppe-scripts.tsv), the table of [Cerobi Steppe scripts](../Story-Events-And-Hunts/cerobi-steppe-scripts.md), names section 2 rows by the same key: 134 of its rows name 837 of the 880 section 2 rows here.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00348DF0` |
| ² | `0x0034ADA0` |
| ³ | `0x00355A00` |
| ⁴ | `0x00357120` |
| ⁵ | `0x00355A2E` |
| ⁶ | `0x00355A90`-`0x00355AD0` |

</details>

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table |
|---|---|---:|---:|---:|
| `srb_a01` | zone | 104 | 0 | 103 |
| `srb_a02` | zone | 107 | 0 | 104 |
| `srb_a03` | zone | 107 | 0 | 104 |
| `srb_a04` | zone | 131 | 0 | 106 |
| `srb_b01` | zone | 108 | 0 | 104 |
| `srb_b02` | zone | 105 | 0 | 104 |
| `srb_b03` | zone | 104 | 0 | 103 |
| `srb_b04` | zone | 114 | 0 | 109 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 880 rows.

Empty strings per tree: `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9. No `in`, `kr`, `cn` or `ch` string is empty.

9 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record¹ ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002AD151` |

</details>

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>`¹: `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001B6350` |

</details>

No string of these scripts carries `{alt-font}`, so every one takes the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)).

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

191 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E`¹ ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 186 with 2, 2 with 3, 2 with 11, 1 with 26.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002AC825` |

</details>

Strings with a choice list per tree: `us` 191, `de` 191, `es` 191, `fr` 191, `it` 191, `in` 191, `kr` 191, `cn` 191, `ch` 191.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `srb_a01` 2/29, a line with a line break (`{line}`). `us`: `{name:A283E1}{line}Nothing to it, kupo!`; `in`: `{spacing:8181}{name:A283E1}{line}お安いご用クポ！`.
- `srb_a04` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.

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
| rows | 880: 880 in section 2, 0 in section 3 |
| scripts | 8: 8 zone, 0 scene |
| strings per tree | `us` 880, `de` 880, `es` 880, `fr` 880, `it` 880, `in` 880, `kr` 880, `cn` 880, `ch` 880 |
| non-empty strings per tree | `us` 871, `de` 871, `es` 871, `fr` 871, `it` 871, `in` 880, `kr` 880, `cn` 880, `ch` 880 |
| strings with `{alt-font}` | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| strings with a choice list | `us` 191, `de` 191, `es` 191, `fr` 191, `it` 191, `in` 191, `kr` 191, `cn` 191, `ch` 191 |
| section 2 rows the scripts table names | 837 |
| speakers | 880 section 2 rows: 829 by the line's own name; 8 from the scripts table's `speaker` cells; 31 from the actors whose functions show the line; 10 shown with no speaker (screen text, gauge labels, field signs, name text); 2 no script asks for |

## Related

- [Cerobi Steppe scripts](../Story-Events-And-Hunts/cerobi-steppe-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 39 calls with 8 other topics</summary>

**Characters and objects** (explained on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [script requests](../Scripts-And-Script-Commands/script-requests.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00355A00`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | calls | [`0x0025D5E0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00269F20`](enemy-names-on-screen.md) (on enemy names on screen)<br>[`0x0026B4A0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x00357120`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | calls | [`0x00269F20`](enemy-names-on-screen.md) (on enemy names on screen) |

**Movement and pathfinding** (explained on [party control modes](../Engine-Core/party-control-modes.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00355A00`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | calls | [`0x0026AB60`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026B0C0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0026B620`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0026BB00`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026BC70`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026BD50`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026BDD0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026BFF0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |

**Graphics** (explained on [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001FDD60`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x001B4590`](fonts.md) (on fonts) |

**Game files and data tables** (explained on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [sprite batcher](../Graphics/sprite-batcher.md), [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md), [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00674A00`](fonts.md) (on fonts) | is called by | [`0x001A7A50`](../World-Areas-And-Travel/map-art.md) (on map art)<br>[`0x001A9050`](../Game-Files-And-Data-Tables/standard-file-formats.md) (on standard file formats)<br>[`0x001B1440`](../Graphics/sprite-batcher.md) (on sprite batcher)<br>[`0x001B1C10`](../Graphics/sprite-batcher.md) (on sprite batcher)<br>[`0x0020BE50`](../Engine-Core/call-signatures.md) (on call signatures)<br>[`0x0020C1B0`](../Game-Files-And-Data-Tables/file-path-resolution.md) (on file path resolution) |

**Scripts and script commands** (explained on [npc names](../Characters-And-Objects/npc-names.md), [archades scenes](../Story-Events-And-Hunts/archades-scenes.md), [archades scripts](../Story-Events-And-Hunts/archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002642C0`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00355A00`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) |
| [`0x00264D60`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](../Story-Events-And-Hunts/archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](../Story-Events-And-Hunts/nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x00264D90`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00355A00`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue)<br>[`0x00357120`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) |
| [`0x00348DF0`](../Story-Events-And-Hunts/archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](../Story-Events-And-Hunts/archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](../Story-Events-And-Hunts/archades-scripts.md) (on archades scripts) |
| [`0x0034ADA0`](../Story-Events-And-Hunts/nalbina-town-scripts.md) (on nalbina town scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034ADA0`](../Story-Events-And-Hunts/nalbina-town-scripts.md) (on nalbina town scripts) | is called by | [`0x0034B760`](../Story-Events-And-Hunts/nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x0034BB10`](../Story-Events-And-Hunts/nalbina-town-scripts.md) (on nalbina town scripts) |
| [`0x00355A00`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00357120`](aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

</details>
