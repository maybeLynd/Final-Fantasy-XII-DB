[Home](../../README.md) / [Menus and HUD](README.md) / Developer dialogue

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Developer dialogue: every line and caption of the Developer scripts in all nine languages | reference | Menus and HUD | Dialogue / Developer and test maps | Every string of sections 2 and 3 of the Developer scene scripts side by side in the nine language trees: the lines the message verbs show and the captions the field signs show, keyed by script, section and text id as the Developer scripts table names them, with the row count per language, where the languages differ, the strings drawn with the alternate font and the choice lists. | 0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350 |

## What it lists

[developer-dialogue.tsv](developer-dialogue.tsv) has one row per string of sections 2 and 3 of the Developer scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 774 rows from 15 scene scripts under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

The other three of the eighteen developer scripts, `evt_t0009`, `evt_t0015` and `evt_t0016`, hold no entry in section 2 or 3 in any tree. The table is read from the `EBP2` containers, so it has no row from `evt_t0020`, the folder beside them that holds a bare script image of version 7 in place of an `EBP2` container, byte-identical in all nine trees ([Developer scripts](../Story-Events-And-Hunts/developer-scripts.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`developer-scripts.tsv`](../Story-Events-And-Hunts/developer-scripts.tsv), the table of [Developer scripts](../Story-Events-And-Hunts/developer-scripts.md), names section 2 rows by the same key: 30 of its rows name 771 of the 774 section 2 rows here.
- The `quoted_lines` column of that table's steps table quotes 771 of them, in 2,326 steps. 12 more rows and 16 more steps name text ids of `evt_t0009`, `evt_t0015` and `evt_t0016`, which have no section 2.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `evt_t0005` | scene | 1 | 0 | 1 | 1 |
| `evt_t0023` | scene | 3 | 0 | 3 | 3 |
| `evt_t0080` | scene | 9 | 0 | 9 | 9 |
| `evt_t0081` | scene | 105 | 0 | 105 | 105 |
| `evt_t0082` | scene | 67 | 0 | 67 | 67 |
| `evt_t0083` | scene | 125 | 0 | 124 | 124 |
| `evt_t0084` | scene | 87 | 0 | 87 | 87 |
| `evt_t0085` | scene | 94 | 0 | 94 | 94 |
| `evt_t0086` | scene | 68 | 0 | 68 | 68 |
| `evt_t0090` | scene | 40 | 0 | 40 | 40 |
| `evt_t0094` | scene | 1 | 0 | 1 | 1 |
| `evt_t0096` | scene | 48 | 0 | 48 | 48 |
| `evt_t0500` | scene | 15 | 0 | 14 | 14 |
| `evt_t0505` | scene | 59 | 0 | 58 | 58 |
| `evt_t0509` | scene | 52 | 0 | 52 | 52 |

### Where the languages differ

Every row but one has a string in all nine trees:

- `evt_t0005` 2/0 ships only in `in`, `kr`, `cn` and `ch` (`event/evt_t/evt_t0005/evt_t0005.ebp`).

Empty strings per tree: `us` 3, `de` 3, `es` 3, `fr` 3, `it` 3. No `in`, `kr`, `cn` or `ch` string is empty.

3 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

593 rows hold Japanese text, kana or kanji in all five of `us`, `de`, `es`, `fr` and `it`.

The rows that carry a choice list in some trees only:

- `evt_t0080` 2/8: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `evt_t0086` 2/3: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `evt_t0086` 2/6: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `evt_t0086` 2/7: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

No string of these scripts carries `{alt-font}`, so every one takes the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)).

No `kr`, `cn` or `ch` font holds an expansion list keyed by an `evt_t` script path ([Font expansion lists](fonts-expansion-lists.md) lists them in the `jp` and `us` fonts only), so the table writes the expansion codes of those three trees as `{exp:0xN}`, N its ordinal, in 1,446 cells: `kr` 457, `cn` 436, `ch` 553.

Every expansion code of the `in` column has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 335, `de` 335, `es` 335, `fr` 335, `it` 335.

### Choice lists

684 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 46 with 2, 112 with 3, 62 with 4, 51 with 5, 59 with 6, 48 with 7, 31 with 8, 39 with 9, 41 with 10, 41 with 11, 20 with 12, 17 with 13, 10 with 14, 10 with 15, 8 with 16, 28 with 17, 3 with 18, 8 with 19, 2 with 20, 26 with 21, 3 with 22, 7 with 24, 1 with 25, 2 with 26, 2 with 30, 1 with 31, 2 with 32, 1 with 40, 1 with 47, 1 with 57, 1 with 101.

In the `in`, `kr`, `cn` and `ch` trees four lists hold option lengths that do not fit the 7-bit length field: `evt_t0080` 2/8, `evt_t0086` 2/3, `evt_t0086` 2/6 and `evt_t0086` 2/7. The interpreter masks the length the same way (`0x002AC946`), so it reads past those options ([Text codes](text-codes.md)); the table writes each such list as one code by its own bytes, `{0E...}`, from its `0E` byte to the `00` on which that masked walk stops, and those cells do not count as a choice list below.

That `00` ends the string itself only in the `cn` cell of `evt_t0080` 2/8. The other three cells of that row run on through 17 (`in`), 25 (`kr`) and 56 (`ch`) bytes of the zero fill that ends the section, and the twelve `evt_t0086` cells through the strings of the next 1 to 8 entries, which have rows of their own.

Strings with a choice list per tree: `us` 684, `de` 684, `es` 684, `fr` 684, `it` 684, `in` 681, `kr` 681, `cn` 681, `ch` 681.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `evt_t0086` 2/22, a line with a line break (`{line}`). `us`: `{size%:81DA}{speed:8180}Sugatanaki hashi {arg:8290}  {icon:B:82}{icon:D:82}: Move  START: Clear(mapump){line}{icon:@:82}: Appear  {icon:I:82}: Cancel`; `in`: `{spacing:8181}{size%:81DA}{speed:8180}Sugatanaki hashi {arg:8290}  {icon:B:82}{icon:D:82}: Move  START: Clear(mapump){line}{icon:@:82}: Appear  {icon:I:82}: Cancel`.
- `evt_t0086` 2/43, a line that ends in a choice list. `us`: `{size%:81D0}{speed:8180}{choice:2}[Cancel|Progress]`; `in`: `{spacing:8181}{size%:81D0}{speed:8180}{choice:2}[Cancel|Progress]`.

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
| rows | 774: 774 in section 2, 0 in section 3 |
| scripts | 15: 0 zone, 15 scene |
| strings per tree | `us` 773, `de` 773, `es` 773, `fr` 773, `it` 773, `in` 774, `kr` 774, `cn` 774, `ch` 774 |
| non-empty strings per tree | `us` 770, `de` 770, `es` 770, `fr` 770, `it` 770, `in` 774, `kr` 774, `cn` 774, `ch` 774 |
| strings with `{alt-font}` | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| strings with a choice list | `us` 684, `de` 684, `es` 684, `fr` 684, `it` 684, `in` 681, `kr` 681, `cn` 681, `ch` 681 |
| section 2 rows the scripts table names | 771 |
| section 2 rows a step quotes | 771, in 2,326 steps |
| speakers | 774 section 2 rows: 771 from the scripts table's `speaker` cells; 1 shown with no speaker (screen text, gauge labels, field signs, name text); 2 no script asks for |

## Related

- [Developer scripts](../Story-Events-And-Hunts/developer-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
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

| Function | | Functions |
|---|---|---|
| `0x00355A00` | calls | `0x0025D5E0`, `0x00269F20`, `0x0026B4A0` |
| `0x00357120` | calls | `0x00269F20` |

**Movement and pathfinding** (explained on [party control modes](../Engine-Core/party-control-modes.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md))

| Function | | Functions |
|---|---|---|
| `0x00355A00` | calls | `0x0026AB60`, `0x0026B0C0`, `0x0026B620`, `0x0026BB00`, `0x0026BC70`, `0x0026BD50`, `0x0026BDD0`, `0x0026BFF0` |

**Graphics** (explained on [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md))

| Function | | Functions |
|---|---|---|
| `0x001FDD60` | is called by | `0x001B4590` |

**Game files and data tables** (explained on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [sprite batcher](../Graphics/sprite-batcher.md))

| Function | | Functions |
|---|---|---|
| `0x00674A00` | is called by | `0x001A7A50`, `0x001A9050`, `0x001B1440`, `0x001B1C10`, `0x0020BE50`, `0x0020C1B0` |

**Game files and data tables** (explained on [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md), [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md))

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x002642C0` | is called by | `0x00355A00` |
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x00264D90` | is called by | `0x00355A00`, `0x00357120` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x0034ADA0` | calls | `0x00267E10` |
| `0x0034ADA0` | is called by | `0x0034B760`, `0x0034BB10` |

**Scripts and script commands** (explained on [npc names](../Characters-And-Objects/npc-names.md), [archades scenes](../Story-Events-And-Hunts/archades-scenes.md), [archades scripts](../Story-Events-And-Hunts/archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md))

| Function | | Functions |
|---|---|---|
| `0x00355A00` | calls | `0x00267E10` |
| `0x00357120` | calls | `0x00267E10` |

**Scripts and script commands** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

</details>
