---
title: "Sky Fortress Bahamut scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [sky-fortress-bahamut-scripts.tsv](sky-fortress-bahamut-scripts.tsv) has one row per script function of the
Sky Fortress Bahamut that does something a player can observe. It covers the nine zone scripts and the twelve scene
scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `bhm_a01` | zone | Periphery, field `774` | 25 | 63 | 13 | 0 |
| `bhm_a02` | zone | Catwalk, field `775` | 19 | 52 | 8 | 0 |
| `bhm_a03` | zone | Antechamber, field `776` | 24 | 60 | 10 | 0 |
| `bhm_a04` | zone | Antechamber, field `777` | 22 | 88 | 8 | 5 |
| `bhm_b01` | zone | Central Lift, field `779` | 15 | 59 | 6 | 0 |
| `bhm_c01` | zone | Central Shaft, field `782` | 27 | 48 | 3 | 0 |
| `bhm_d01` | zone | Cannon Superstructure, field `785` | 12 | 22 | 2 | 0 |
| `bhm_y01` | zone | field `922` | 7 | 9 | 1 | 0 |
| `bhm_z01` | zone | field `924` | 7 | 9 | 2 | 0 |
| `bhm_a0200` | scene | event `150` | 20 | 144 | 16 | 0 |
| `bhm_a0400` | scene | event `141` | 21 | 106 | 4 | 0 |
| `bhm_b0100` | scene | event `155` | 23 | 179 | 15 | 0 |
| `bhm_b0101` | scene | event `156` | 32 | 221 | 7 | 0 |
| `bhm_c0100` | scene | event `157` | 26 | 257 | 10 | 0 |
| `bhm_c0101` | scene | event `158` | 35 | 416 | 8 | 0 |
| `bhm_c0102` | scene | event `159` | 39 | 1068 | 24 | 0 |
| `bhm_d0100` | scene | event `142` | 15 | 120 | 9 | 0 |
| `bhm_d0101` | scene | event `151` | 23 | 147 | 4 | 0 |
| `bhm_y0100` | scene | event `153` | 27 | 205 | 37 | 0 |
| `bhm_y0101` | scene | event `154` | 16 | 79 | 14 | 0 |
| `bhm_z0100` | scene | event `152` | 28 | 225 | 13 | 0 |

Antechamber (field 777) carries the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have
no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Sky
Fortress Bahamut scenes](sky-fortress-bahamut-scenes.md).

### What the scripts do

- Periphery (field 774): eight doors (`door_nw` to `door_se`) lead into the Antechamber, six to field 776 and two to
  field 777, and the Antechamber's doors lead back. The Periphery's exits lead to Catwalk, field 775, whose own exits
  lead back and to Central Lift, field 779.
- Sky Fortress Bahamut: `Map_Director.init` of every field from the Periphery to the Cannon Superstructure releases
  flags `0x0104`, `0x0105` and `0x0106`, map icons in Catwalk, and sets one of them by field: `0x0104` in fields 774
  to 777 and 779, `0x0105` in Central Shaft, field 782, and `0x0106` in Cannon Superstructure, field 785.
- Catwalk: below story counter 6550, `常駐監督.init` loads scene `bhm_a0200` (event 150), and `main` plays it and writes
  6550, the value after the shaking Bahamut, then 6600, the value after the fierce battle.
- Antechamber (field 777) holds the crystal. Below story counter 6450, `常駐監督.init` loads scene `bhm_a0400` (event
  141), and `main` plays it and writes 6450, the value after storming the Bahamut.
- Antechamber (field 777): the closed door (`閉じた扉`) answers with the line of the controlled party member, one for each
  of the six, among them "We can't leave until we stop Vayne. Then we can go back to Rabanastre...back home." (Vaan)
  and "It is too soon now to leave. There is still much to be done." (Fran).
- Central Lift: below story counter 6700 the field's setup sets `g_btl_ガブラスバハムート` to 1; while it is 1 and the counter
  is at most 6700, `ボス監督.main` loads scenes `bhm_b0100` (event 155) and `bhm_b0101` (event 156). Below 6750, "Engage
  the lift." on the lift panel (`alift_ctrl`, "This panel can be used to operate the lift.") starts the Gabranth fight
  under the boss gauge (`ボス監督.イベント制御`).
- Central Lift: when the Gabranth fight ends, `ボス監督.イベント制御` removes every foe, sets `g_btl_ガブラスバハムート` to 2 and writes
  6700, the value after the Gabranth battle on the Bahamut, then 6750, the value after the bond. From 6750, "Engage
  the lift." takes the party up to Central Shaft, field 782 (`Map_Director.map_jump`).
- Central Shaft: while the story counter is at most 6850 and `g_btl_ヴェイン` is 1, `ボス監督.main` loads scenes `bhm_c0100`
  (event 157) and `bhm_c0101` (event 158) and runs the Vayne fight under the boss gauge. When it ends it removes every
  foe, has `読込監督.bhm_c0102制御` load and play scene `bhm_c0102` (event 159), sets `g_btl_ヴェイン` to 2 and
  `g_btl_ハイパー・ヴェイン` to 1 and writes 6850, the value after the Vayne battle.
- Central Shaft: the second fight follows in the same function under a new boss gauge. When it ends the director
  writes 6900, the value after Vayne's second form, removes every foe, sets `g_btl_ハイパー・ヴェイン` to 2, writes 7000, the
  value after Vayne's blow, and jumps to Cannon Superstructure, field 785.
- Cannon Superstructure: while the story counter is at most 7150 and `g_btl_ラスト・ヴェイン` is 1, `ボス監督.main` loads scenes
  `bhm_d0100` (event 142) and `bhm_d0101` (event 151), writes 7100, the value after the decisive battle, and runs the
  last Vayne fight under the boss gauge.
- Cannon Superstructure: when the last fight ends, `ボス監督.main` sets `g_btl_ラスト・ヴェイン` to 2, writes 7150, the value
  after the last Vayne battle, loads and plays the ending message `msg_z0001` (event 399, [Ending message
  scenes](ending-message-scenes.md)) and jumps to field 13, where the staff roll plays ([Location title
  scripts](titles-scripts.md)).
- Field 922 (`bhm_y01`): below story counter 4050, `常駐監督.main` loads and plays scene `bhm_y0101` (event 154), writes
  4050, the value after the warship scene, and jumps to `var_z01` (Balfonheim Port), field 918; from 4050 and below
  6300 it loads and plays `bhm_y0100` (event 153), writes 6400, the value after the Strahl closes on the Bahamut, and
  jumps to the Antechamber, field 777.
- Field 924 (`bhm_z01`): below story counter 6150, `常駐監督.init` loads scene `bhm_z0100` (event 152), and `main` plays
  it, writes 6250, the value after the battle's opening, and jumps to field 922 (`bhm_y01`).
- Antechamber (field 776) and Antechamber (field 777) hold 3 and 1 treasure chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember` | `0x353`, `0x355` | `0x0034C030`, `0x0034D4E0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

The story counter is the script's global `short` at offset 0, named `シナリオフラグ` in the scripts of this table that write
or test it: every assignment to it is a write and every comparison a test ([story counter
values](story-counter-values.md)).

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

The steps table [`sky-fortress-bahamut-script-steps.tsv`](sky-fortress-bahamut-script-steps.tsv) has one row for each
step of every function of the twenty-one scripts, in the order the function runs them: each call, request, store,
branch, loop, case and return. It has 34,968 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `bhm_a01` | 731 | `bhm_a0400` | 1,255 |
| `bhm_a02` | 523 | `bhm_b0100` | 1,800 |
| `bhm_a03` | 593 | `bhm_b0101` | 2,160 |
| `bhm_a04` | 597 | `bhm_c0100` | 1,621 |
| `bhm_b01` | 887 | `bhm_c0101` | 3,319 |
| `bhm_c01` | 970 | `bhm_c0102` | 6,530 |
| `bhm_d01` | 337 | `bhm_d0100` | 1,765 |
| `bhm_y01` | 68 | `bhm_d0101` | 5,463 |
| `bhm_z01` | 58 | `bhm_y0100` | 1,575 |
| `bhm_a0200` | 1,830 | `bhm_y0101` | 819 |
| | | `bhm_z0100` | 2,067 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Sky Fortress Bahamut has 29 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 34,732 |
| empty | 236 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its functions. In `bhm_a0400` (event `141`), `ディレクター.main` starts scene cut 0,
files `パーティー全体.イベント開始前準備` and starts `準備` on seven actors together, among them `アーシェ`, `バッシュ` and `フラン`. It waits for
effect slot 0 and for six of the `準備` and the `イベント開始前準備` to end, then files `ディレクター.イベント進行`, which files `ＡＤ.s01` to
`ＡＤ.s05` and `ＡＤ.バインドオフ` one after another, waiting until each ends. Back in `main`, it files `イベント曲.music_stop`,
waits until it ends and fades the screen out over 0 frames.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line |
| `lines` | the section 2 entries the function passes to the message verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [sky-fortress-bahamut-script-list.tsv](sky-fortress-bahamut-script-list.tsv) holds the first table
above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`sky-fortress-bahamut-script-steps.tsv`](sky-fortress-bahamut-script-steps.tsv) has one row per step:

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

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message actors, described once.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Ending message scenes](ending-message-scenes.md) - the scene the Cannon Superstructure loads after the last fight.
- [Location title scripts](titles-scripts.md) - field 13, where the staff roll plays.
- [Balfonheim Port scripts](balfonheim-port-scripts.md) - the port field 922 jumps to.
