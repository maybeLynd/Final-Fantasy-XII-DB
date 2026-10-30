---
title: "Ridorana Cataract scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00352EA0, 0x00353390, 0x00354000, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of the `rwf` scripts that does something a player can observe. It covers the
six zone scripts and the six scene scripts of the group, from `plan_master/us`; five maps are in Ridorana Cataract and
one, They Who Thirst Not, is in Pharos - First Ascent:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `rwf_a01` | zone | Footfalls of the Past, field `509` | 18 | 55 | 7 | 5 |
| `rwf_a03` | zone | Echoes from Time's Garden, field `511` | 27 | 42 | 13 | 0 |
| `rwf_b01` | zone | City of Other Days, field `517` | 27 | 40 | 12 | 0 |
| `rwf_b02` | zone | Path of Hidden Blessing, field `518` | 18 | 50 | 6 | 5 |
| `rwf_c01` | zone | They Who Thirst Not, field `522` | 23 | 77 | 12 | 0 |
| `rwf_d01` | zone | Colosseum, field `898` | 26 | 68 | 16 | 1 |
| `rwf_a0100` | scene | event `372` | 19 | 139 | 6 | 0 |
| `rwf_c0100` | scene | event `370` | 13 | 70 | 0 | 0 |
| `rwf_c0101` | scene | event `371` | 13 | 56 | 0 | 0 |
| `rwf_c0102` | scene | event `373` | 18 | 195 | 7 | 0 |
| `rwf_d0100` | scene | event `374` | 12 | 54 | 0 | 0 |
| `rwf_d0101` | scene | event `375` | 14 | 53 | 0 | 0 |

Footfalls of the Past and Path of Hidden Blessing carry the five helper actors that many zone scripts share: the
crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message
helper `イベント特殊効果画面`; the Colosseum carries the key-item and message helper alone. Their functions are described once
on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

The Pharos maps beyond The Wellspring are on [Pharos - First Ascent scripts](pharos-first-ascent-scripts.md).

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Ridorana
Cataract scenes](ridorana-cataract-scenes.md).

### What the scripts do

- Footfalls of the Past: below story counter 5,200, `常駐ディレクター.init` loads scene `rwf_a0100` (event 372), and
  `常駐ディレクター.main` writes 5200, after Ridorana Cataract and the Pharos.
- Footfalls of the Past: talking to `system_anchor_actor` requests `ym_shutoraljump.shtjump`, which loads scene
  `str_z0000` (event 211) and jumps to the field a script variable holds. `system_anchor_actor.init` sets and releases
  flags `0x0002` to `0x0013`, which the anchor actors of twelve other maps also set and release, and tests `0x4022`, a
  story schedule record that is true from story counter 5,150.
- Path of Hidden Blessing: `常駐ディレクター.init` loads scene `ttl_z0002` (event 217); `ロケタイイベント.起動`, requested by the exit
  `__MJ_CTRL000`, sets flag `0x004A`, the location map's exits between Pharos - First Ascent and Ridorana Cataract.
- They Who Thirst Not: `常駐監督.main` loads scenes `rwf_c0100` (event 370) and `rwf_c0101` (event 371) and tests the
  story counter from 5,300 to below 5,303.
- They Who Thirst Not: touching `ボス登場` shows the boss gauge, removes the foes, loads `pos_z0000` (event 427), requests
  `Read_Event_RWF_C01.sakiyomi_init`, which loads scene `rwf_c0102` (event 373), and writes 5300, after a boss battle.
  At 5,300, touching the door `扉開く` writes 5303, after the door of the Pharos, and jumps to The Wellspring (Pharos -
  First Ascent), field `1101`.
- They Who Thirst Not: the wall `レイスウォールの文字` shows the words cut into the stone ("Lo, seeker in days unborn, god-blade
  bearer! Know you: this tower challenges the sky."), signed "In blood, Raithwall". `wanted_kansi.main` removes the
  foes of a group.
- Colosseum: `監督.main` shows the boss gauge, removes the foes and loads scenes `rwf_d0100` (event 374), `rwf_d0101`
  (event 375) and `pos_z0000`; touching `ボス登場01` or `ボス登場02` shows the boss gauge, removes the foes and loads
  `pos_z0000`. The pot `大瀑布地図宝壺` gives the Ridorana Cataract map, shows system message 102, "Your location map for
  this area is complete!", and sets treasure flag `0x0016`.
- Echoes from Time's Garden: `hunt_kansi.main` gives the Reptilian Trophy and removes the foes of a group.
- Footfalls of the Past and Path of Hidden Blessing: `choco_sum_ctrl_murasawa.sumcho_byebye`, requested by the
  teleport, releases flag `0x0073`, riding a chocobo.
- Echoes from Time's Garden, City of Other Days, Path of Hidden Blessing, They Who Thirst Not and the Colosseum hold
  9, 9, 1, 4 and 10 treasure chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | the second argument is a section 2 text id; the choices are in that text |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settreasureflag`, `releasetreasureflag`, `istreasureflag` | `0x3F1`, `0x3F2`, `0x3F5` | `0x00352EA0`, `0x00353390`, `0x00354000` | `flags_*` | `Bank512, second half` flag ([story flag ids](story-flag-ids.md)) |
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

The steps table [`ridorana-cataract-script-steps.tsv`](ridorana-cataract-script-steps.tsv) has one row for each step
of every function of the twelve scripts, in the order the function runs them: each call, request, store, branch, loop,
case and return. It has 8,877 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `rwf_a01` | 490 | `rwf_a0100` | 1,077 |
| `rwf_a03` | 391 | `rwf_c0100` | 591 |
| `rwf_b01` | 360 | `rwf_c0101` | 447 |
| `rwf_b02` | 276 | `rwf_c0102` | 1,677 |
| `rwf_c01` | 994 | `rwf_d0100` | 687 |
| `rwf_d01` | 1,354 | `rwf_d0101` | 533 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Ridorana Cataract has 68 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 8,081 |
| empty | 796 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its functions. In `rwf_c0101` (event `371`), `ＡＤ.死亡Ｓ０２` plays cuts 2 to 4. At cut
2 it files `シーン０２` on the camera, `演出`, sound, vibration and `ハイドラ` actors together and waits 40 frames. Cuts 3 and 4
each file a crossfade on a camera actor, call `crossfade(0, 1, 10)` and file `シーン０３` or `シーン０４` on the vibration actor
and `ハイドラ`, waiting 40 and 49 frames.

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

The script list [`ridorana-cataract-script-list.tsv`](ridorana-cataract-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`ridorana-cataract-script-steps.tsv`](ridorana-cataract-script-steps.tsv) has one row per step:

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
- [Ridorana Cataract scenes](ridorana-cataract-scenes.md) - the six scenes these scripts load.
- [Pharos - First Ascent scripts](pharos-first-ascent-scripts.md) - the Pharos beyond They Who Thirst Not.
- [Balfonheim Port scripts](balfonheim-port-scripts.md) - Saccio Lane, where story counter 5160 (heard about Ridorana)
  is written.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
