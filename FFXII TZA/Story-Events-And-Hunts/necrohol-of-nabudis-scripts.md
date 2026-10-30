---
title: "Necrohol of Nabudis scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Necrohol of Nabudis that does something a player can observe. It covers
the eight zone scripts with a field entry and the seven scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `bds_a01` | zone | Hall of Effulgent Light, field `421` | 26 | 40 | 12 | 0 |
| `bds_a02` | zone | Cloister of Distant Song, field `422` | 32 | 80 | 14 | 0 |
| `bds_b01` | zone | Cloister of the Highborn, field `426` | 37 | 101 | 17 | 0 |
| `bds_c01` | zone | Hall of the Ivory Covenant, field `430` | 32 | 79 | 14 | 0 |
| `bds_c02` | zone | Hall of Slumbering Might, field `431` | 25 | 38 | 11 | 0 |
| `bds_e01` | zone | The Crucible, field `438` | 19 | 55 | 5 | 0 |
| `bds_f01` | zone | Cloister of Solace, field `441` | 16 | 60 | 5 | 1 |
| `bds_g01` | zone | Cloister of Reason, field `444` | 16 | 60 | 5 | 1 |
| `bds_a0100` | scene | event `226` | 16 | 136 | 5 | 0 |
| `bds_e0100` | scene | event `224` | 11 | 45 | 0 | 0 |
| `bds_e0101` | scene | event `225` | 15 | 70 | 15 | 0 |
| `bds_f0100` | scene | event `220` | 16 | 95 | 0 | 0 |
| `bds_f0101` | scene | event `221` | 19 | 128 | 0 | 0 |
| `bds_g0100` | scene | event `222` | 16 | 101 | 0 | 0 |
| `bds_g0101` | scene | event `223` | 17 | 79 | 0 | 0 |

Cloister of Solace and Cloister of Reason carry the key-item and message helper `イベント特殊効果画面`, one of the five helper
actors that many zone scripts share. Its functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts it.

The scene `bds_e0101` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

Five more zone scripts of the region ship under `plan_map/bds_a`, `bds_b` and `bds_d`: `bds_a03`, `bds_b02`, `bds_d01`,
`bds_d02` and `bds_d03`. The map name table names fields `423`, `427` and `433` to `435` by these codes, but the
zone-script list has no entry for those fields, so the five scripts have no rows here; their steps are in the steps
table. One exit of Cloister of Distant Song (`__MJ_CTRL001`) leads to field `434`, `bds_d02`.

Each script holds `Map_Director`, whose `init` returns at once, and map exits `__MJ_CTRL00n`, each of which turns user
control off, fades out and calls `mapjump`:

- `bds_a03`, field `423`, has two exits, to field `434` (`bds_d02`), entrance 1, and to Cloister of Distant Song, field
  `422`, entrance 3; the only `mapjump` that names field `423` is `bds_d02`'s, which no field loads, so no jump reaches
  `bds_a03`.
- `bds_b02`, field `427`, has two exits, to Field of the Fallen Lord (Nabreus Deadlands), field `180`, entrance 2, and
  to field `435` (`bds_d03`), entrance 1; the only `mapjump` that names field `427` is `bds_d03`'s, which no field
  loads, so no jump reaches `bds_b02`.
- `bds_d01`, field `433`, has three exits, to Hall of Effulgent Light (field `421`, entrance 2), Cloister of Distant
  Song (field `422`, entrance 1) and Cloister of the Highborn (field `426`, entrance 1); no `mapjump` names field `433`,
  so no jump reaches `bds_d01`.
- `bds_d02`, field `434`, has three exits, to field `423` (`bds_a03`, entrance 2), Cloister of Distant Song (field
  `422`, entrance 2) and Cloister of Solace (field `441`, entrance 1); `bds_a02`'s `__MJ_CTRL001` jumps to field `434`
  (entrance 2), as does `bds_a03`, but field `434` has no zone-script entry, so these jumps load no zone script and no
  jump reaches `bds_d02`.
- `bds_d03`, field `435`, has three exits, to field `427` (`bds_b02`, entrance 2), Cloister of the Highborn (field
  `426`, entrance 3) and Cloister of Reason (field `444`, entrance 1); the only `mapjump` that names field `435` is
  `bds_b02`'s, which no field loads, so no jump reaches `bds_d03`.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Necrohol of
Nabudis scenes](necrohol-of-nabudis-scenes.md).

### What the scripts do

- Hall of Effulgent Light: `監督.main` tests the story counter against 3,050 and 3,210, loads scene `bds_a0100` (event
  226), in which the party find what remains of Nabudis, and sets flag `0x0035`, the location map's exits between
  Necrohol of Nabudis and The Salikawood. `Map_Director.init` sets and tests flag `0x0161`, which Corridor of Ages
  (The Salikawood) also sets or tests.
- Hall of Slumbering Might: `監督.main` sets and tests flag `0x0041`, the exits between Nabreus Deadlands and Necrohol
  of Nabudis, and loads scene `ttl_z0002` (event 217). `Map_Director.init` sets and tests flag `0x0160`, which Field
  of the Fallen Lord (Nabreus Deadlands) also sets or tests.
- The medallion doors (`メダル扉.talk`) of Cloister of Distant Song, Cloister of the Highborn and Hall of the Ivory
  Covenant are held fast.
- At these doors each depression names a medallion ("The word "bravery" has been carved within."); the door takes the
  Medallion of Bravery, of Might or of Love, sets flag `0x013A`, `0x013B` or `0x013C`, and jumps to Cloister of
  Solace, The Crucible or Cloister of Reason. `メダル扉.init` sets and releases the same three flags.
- Cloister of Solace and Cloister of Reason: `監督.main` shows the boss gauge, removes the foes and loads the fight's
  two scenes (`bds_f0100` and `bds_f0101`, events 220 and 221; `bds_g0100` and `bds_g0101`, events 222 and 223) and
  `pos_z0000` (event 427).
- Cloister of Solace and Cloister of Reason: then `監督.main` takes the Lusterless Medallion and gives the Medallion of
  Might, or shows system message 141, "The Lusterless Medallion keens..."; in Cloister of Solace it also gives the
  Necrohol of Nabudis map with system message 108, "Your location map for this area is complete!"
- The Crucible: `監督.main` shows the boss gauge, removes the foes and loads scenes `bds_e0100` (event 224), `bds_e0101`
  (event 225), which gives Chaos, and `pos_z0000`. In The Crucible, Cloister of Solace and Cloister of Reason the door
  `ボスマップ扉` leads back to Cloister of the Highborn, Cloister of Distant Song or Hall of the Ivory Covenant, and
  `Map_Director.init` sets flag `0x004E`, `0x004F` or `0x0050`.
- Hall of the Ivory Covenant: `hunt_kansi.main` gives the Gravesoil Trophy and removes the foes of a group. Cloister
  of the Highborn and Hall of Slumbering Might: `wanted_kansi.main` removes the foes of a group.
- Hall of Effulgent Light, Cloister of Distant Song, Cloister of the Highborn, Hall of the Ivory Covenant, Hall of
  Slumbering Might, The Crucible, Cloister of Solace and Cloister of Reason hold 8, 9, 11, 8, 6, 1, 1 and 1 treasure
  chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | the second argument is a section 2 text id; the choices are in that text |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember`, `removepartymember`, `addguestbattlemember`, `removeguestbattlemember` | `0x353`, `0x355`, `0x354`, `0x35B`, `0x35C` | `0x0034C030`, `0x0034D4E0`, `0x0034C030`, `0x00352190`, `0x00352AF0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

The story counter is the script's global `short` at offset 0, named `シナリオフラグ` in these scripts: every
assignment to it is a write and every comparison a test ([story counter values](story-counter-values.md)).

### The four message verbs reach one window call

The four message verbs all end in `mes` (`0x461`, `0x00348DF0`), which looks the text id up in the issuing script's
section 2 ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)):

1. `amese` (`0x0034A420`) pushes 0, 0, 0 and -1; `amest` (`0x0034A090`) pushes 0; `ames` (`0x00349BF0`) pushes 1. Each then
   jumps to `0x00349800`, the body of `ames_1fe`.
2. `0x00349800` pops two values (`0x00349827`, `0x00349831`), pushes 0 and 0 (`0x0034983D`, `0x00349847`) and then pushes the
   two values back in their original order (`0x00349851`, `0x0034985B`), so the zeros lie beneath them; it jumps to
   `0x00348DF0` (`0x00349884`).
3. `0x00348DF0` pops eight values. The seventh, the script's second argument, is passed with the current field context
   to `0x00264D60` (`0x00348E6A`-`0x00348E74`), the section 2 lookup, which keeps the low 24 bits of the id.

### Speakers, places and scenes

- The speaker is the second name of each pair the actor's `setnpcname` calls name in `us` `npcdic.bin`. The
  message window opener `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`necrohol-of-nabudis-script-steps.tsv`](necrohol-of-nabudis-script-steps.tsv) has one row for each step
of every function of the twenty scripts, in the order the function runs them: each call, request, store, branch, loop,
case and return. It has 12,204 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `bds_a01` | 494 | `bds_e0101` | 881 |
| `bds_a02` | 1,154 | `bds_f0100` | 605 |
| `bds_b01` | 1,407 | `bds_f0101` | 860 |
| `bds_c01` | 1,165 | `bds_g0100` | 666 |
| `bds_c02` | 351 | `bds_g0101` | 545 |
| `bds_e01` | 681 | `bds_a03` | 63 |
| `bds_f01` | 661 | `bds_b02` | 63 |
| `bds_g01` | 648 | `bds_d01` | 94 |
| `bds_a0100` | 1,196 | `bds_d02` | 94 |
| `bds_e0100` | 482 | `bds_d03` | 94 |

The five zone scripts no field loads, last in the table, have 408 steps: those of `Map_Director.init` and of their map
exits.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Necrohol of Nabudis has 20 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 11,425 |
| empty | 779 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its functions. In `bds_a0100` (event `226`), `監督.ナブレウス湿原F` starts scene cut 0,
reads an effect into effect slot 0 and waits for it, hides the party and starts cut 1. It files `cut_01_c3` on the
camera and the music actor together, fades the screen in over 60 frames, plays the effect, waits 240 frames and fades
out over 30 frames. At cut 99 it shows the party again and places it with `setposparty`.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line; a system message is not spoken by the actor |
| `lines` | the section 2 entries the function passes to the message and ask verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join or leave, guests who join or leave, and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [`necrohol-of-nabudis-script-list.tsv`](necrohol-of-nabudis-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`necrohol-of-nabudis-script-steps.tsv`](necrohol-of-nabudis-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v`, a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test` |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its control codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

The shared steps table [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv) has the same columns from `at`
on, after these:

| Column | Meaning |
|---|---|
| `template` | the template id that the `shared template` rows name |
| `actor`, `function`, `step` | the shared actor, its function and the step number |
| `reference` | the script whose copy of the function the steps were read from, and where the function starts there |

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids, section
3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other scripts' copies
differ only in these.

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Necrohol of Nabudis scenes](necrohol-of-nabudis-scenes.md) - the seven scenes these scripts load.
- [Nabreus Deadlands scripts](nabreus-deadlands-scripts.md) - the region beyond Hall of Slumbering Might, where the
  Acolyte gives the medallions.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
