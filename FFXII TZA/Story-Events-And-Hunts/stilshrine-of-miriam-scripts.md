---
title: "Stilshrine of Miriam scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [stilshrine-of-miriam-scripts.tsv](stilshrine-of-miriam-scripts.tsv) has one row per script function of the
Stilshrine of Miriam that does something a player can observe. It covers the fourteen zone scripts and the seven scene
scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `mrm_a01` | zone | Walk of Sky, field `593` | 17 | 52 | 8 | 0 |
| `mrm_a02` | zone | Walk of Mind, field `594` | 32 | 155 | 14 | 5 |
| `mrm_b01` | zone | Ward of Measure, field `597` | 44 | 201 | 10 | 0 |
| `mrm_b02` | zone | Cold Distance, field `598` | 33 | 114 | 8 | 1 |
| `mrm_b03` | zone | Walk of Prescience, field `599` | 26 | 103 | 7 | 0 |
| `mrm_b04` | zone | Walk of Reason, field `600` | 45 | 148 | 16 | 0 |
| `mrm_c01` | zone | Ward of Steel, field `603` | 31 | 147 | 9 | 1 |
| `mrm_d01` | zone | Ward of Velitation, field `606` | 28 | 71 | 8 | 0 |
| `mrm_d02` | zone | Walk of Torn Illusion, field `607` | 28 | 83 | 5 | 0 |
| `mrm_d03` | zone | Walk of Revelation, field `608` | 23 | 72 | 5 | 5 |
| `mrm_d04` | zone | Ward of the Sword-King, field `609` | 32 | 112 | 7 | 0 |
| `mrm_e01` | zone | Hall of Worth, field `612` | 23 | 80 | 5 | 0 |
| `mrm_f01` | zone | Vault of the Champion, field `615` | 16 | 90 | 4 | 0 |
| `mrm_g01` | zone | Throne of Veiled Gods, field `618` | 33 | 121 | 5 | 0 |
| `mrm_c0100` | scene | event `360` | 13 | 55 | 0 | 0 |
| `mrm_c0101` | scene | event `361` | 14 | 59 | 0 | 0 |
| `mrm_e0100` | scene | event `362` | 14 | 69 | 0 | 0 |
| `mrm_e0101` | scene | event `363` | 16 | 68 | 13 | 0 |
| `mrm_f0100` | scene | event `366` | 30 | 412 | 10 | 0 |
| `mrm_g0100` | scene | event `364` | 10 | 46 | 0 | 0 |
| `mrm_g0101` | scene | event `365` | 15 | 61 | 13 | 0 |

Walk of Mind and Walk of Revelation carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; Cold Distance and Ward of Steel carry the key-item and message helper alone. Their functions are
described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers
column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Stilshrine
of Miriam scenes](stilshrine-of-miriam-scenes.md).

### What the scripts do

- Walk of Sky: while the story counter is below 2050, `EventDirector.main` loads the location title `ttl_z0000` (event
  215) on an arrival by entrance 1 with flag `0x0036` clear, and sets `0x0036`, the location map's exits between the
  Paramina Rift and the Stilshrine of Miriam; from 2050 on, `EventDirector.init` sets the flag on that arrival. The
  way back leads to Silverflow's End (Paramina Rift), field 475.
- Walk of Mind holds the crystal. Three Kiltias (`NPC_キルティア教徒・扉右`, `NPC_キルティア教徒・扉左` and `NPC_キルティア教徒・銅像`) speak of the
  sealed doors below story counter 2050 ("Only by the will of the Gran Kiltias may the seal on these doors be
  broken.") and of the Sword of Kings from 2050 ("The Sword of Kings, gift of King Raithwall, rests within.").
- Walk of Mind: from story counter 2200 the first of the three Kiltias talks through `talk_after`, with one line below
  2250, one below 4000 and one from 4000 ("The same fleet we saw descend upon Bur-Omisace not long before you emerged
  from the shrine.").
- Walk of Mind: from story counter 2200 to 2249, touching `ムービー起動` plays movie 10 and writes 2250, the value after the
  Alexander in flight. The zone script holds the lines the movie's line controller (`CTRL_ムービー台詞.ムービー台詞`) requests:
  "The Empire's debts grow legion.", "There!", "Smoke?" and "What could it mean?". `DOOR.talk` leads to Ward of
  Measure, field 597.
- Ward of Measure: below story counter 2057, `EventDirector.main` loads the location title `ttl_z0000` (event 215) and
  writes 2057.
- Ward of Measure: the pedestal (`祭壇`) bears Raithwall's words "Treaty-seeker: relic held, this pedestal embrace."
  Touched while `getequipitemid(4)` returns item 0x1183, it shows "The magicks binding the ruins fade." and
  `テレポエフェクト.telepo_ef` jumps to Ward of Velitation, field 606; with another item it shows "The pedestal appears
  unchanged."
- Ward of Measure: `door2` shows only its inscription ("In time of strife, the Treaty-seeker these doors to unbar.")
  until the statue in Ward of the Sword-King has been read (`巨大像のヒント.talk` sets the global both scripts test); after
  that its choice "Touch the door." leads to Cold Distance, field 598.
- Ward of Measure: `door3` shows "The door is locked from within." until the party has come through it from Cold
  Distance (entrance 3), and then leads to Cold Distance as well.
- Ward of Measure: above story counter 2200, with the Stone of the Condemner held, the device (`ワープ装置`) offers "Use
  the [value].", which takes the stone, shows "You use the [value]." and jumps to Throne of Veiled Gods, field 618,
  and "Touch the device.", which jumps to Ward of the Sword-King, field 609.
- Ward of Measure: once the stone is used the device jumps to Throne of Veiled Gods; otherwise, once the statue in
  Ward of the Sword-King has been read, to Ward of the Sword-King; else it shows "Nothing happens. The device remains
  asleep."
- Walk of Prescience, Walk of Reason and Ward of Steel: each holds a statue (`statue_fs_ALL`) with Raithwall's words
  "Guardians three, face ye the blade." Examining it finds a mechanism in its base, and it can be turned clockwise or
  counterclockwise. The turn that brings all three into place shows "The colossus has undergone some change..."
- Walk of Prescience, Walk of Reason and Ward of Steel: each turn of a statue sets one of its four map-icon flags and
  releases the others (`0x00AD` to `0x00B0` in Walk of Prescience, `0x00B1` to `0x00B4` in Walk of Reason, `0x00B5` to
  `0x00B8` in Ward of Steel).
- Cold Distance: on the next arrival after that turn, `mrm_big_statue_fs.main` shows "The way past the colossus is
  open!" (system message 138).
- Ward of Steel: while `g_btl_メタルドラゴン` is 1, `EventDirector.main` loads scenes `mrm_c0100` (event 360) and `mrm_c0101`
  (event 361); `ボス登場.main` shows the boss gauge and, when the fight ends, removes every foe, loads the victory pose
  scene `pos_z0000` (event 427, [Victory pose scenes](victory-pose-scenes.md)) and writes 2100, the value after the
  Vinuskar battle.
- Ward of Steel: talking to `ロケ地図` gives the area map, Stilshrine of Miriam, with system message 111 ("Your location
  map for this area is complete!").
- Ward of Velitation: `hunt_kansi.main` gives the Eternal Trophy and removes the foes of a group.
- Walk of Torn Illusion: the pedestal `MRM_0207_STAIRS_GIMM` ("Treaty-seeker: relic held, this pedestal embrace. Paths
  untrod discover.") shows "A hidden path is revealed." and releases map-icon flag `0x00BA` when touched while
  `getequipitemid(4)` returns item 0x1183; otherwise it shows "The pedestal appears unchanged."
- Walk of Revelation holds a crystal that `クリスタル監視さん.init` hides while `g_btl_クリスタルミミックグリーン` is 1; while it is 1,
  `クリスタル監視さん.main` shows "A crystal appears!" (system message 129), sets it to 2 and removes the foes of a group.
- Ward of the Sword-King: the statue `巨大像のヒント` bears "To guardians three I trust, that the worthy may pass, all others
  be shunned."; its first reading also shows "The magicks binding the door fade." The device (`ワープ装置`, "Magicks stir
  within this device.") jumps to Ward of Measure, field 597, and the door `ボスマップ扉` ("Wisdom proven, assay now your
  power.") leads to Hall of Worth, field 612.
- Hall of Worth: while `g_btl_マティウス` is 1, `EventDirector.main` loads scenes `mrm_e0100` (event 362) and `mrm_e0101`
  (event 363) and shows the boss gauge; when the fight ends it removes every foe, loads `pos_z0000` (event 427) and
  writes 2150, the value after the Mateus battle. Its doors lead to Ward of the Sword-King, field 609, and Vault of
  the Champion, field 615.
- Vault of the Champion: while the story counter is below 2200, `SAKIYOMI_mrm_f0100.init` loads scene `mrm_f0100`
  (event 366); touching `イベントレクト` plays it, writes 2200 and gives the Sword of Kings.
- Throne of Veiled Gods: while `g_btl_ゼロムス` is 1, `EventDirector.main` loads scenes `mrm_g0100` (event 364) and
  `mrm_g0101` (event 365); `ボス登場.main` shows the boss gauge and, when the fight ends, removes every foe and loads
  `pos_z0000` (event 427). While `g_btl_ゼロムス` is not 2, `Map_Director.init` sets flag `0x010E`, which shows Throne of
  Veiled Gods on the location map. The device (`ワープ装置`) jumps to Ward of the Sword-King, field 609.
- Walk of Sky, Walk of Mind, Cold Distance, Walk of Prescience, Walk of Reason, Ward of Steel, Ward of Velitation and
  Hall of Worth hold 3, 1, 1, 1, 10, 1, 3 and 2 treasure chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settreasureflag`, `releasetreasureflag`, `istreasureflag` | `0x3F1`, `0x3F2`, `0x3F5` | `0x00352EA0`, `0x00353390`, `0x00354000` | `flags_*` | `Bank512, second half` flag ([story flag ids](story-flag-ids.md)) |
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

The steps table [`stilshrine-of-miriam-script-steps.tsv`](stilshrine-of-miriam-script-steps.tsv) has one row for each
step of every function of the twenty-one scripts, in the order the function runs them: each call, request, store,
branch, loop, case and return. It has 28,618 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `mrm_a01` | 1,382 | `mrm_d04` | 1,145 |
| `mrm_a02` | 1,584 | `mrm_e01` | 1,002 |
| `mrm_b01` | 2,986 | `mrm_f01` | 1,701 |
| `mrm_b02` | 851 | `mrm_g01` | 1,353 |
| `mrm_b03` | 1,856 | `mrm_c0100` | 542 |
| `mrm_b04` | 2,376 | `mrm_c0101` | 600 |
| `mrm_c01` | 2,708 | `mrm_e0100` | 682 |
| `mrm_d01` | 1,607 | `mrm_e0101` | 917 |
| `mrm_d02` | 695 | `mrm_f0100` | 2,980 |
| `mrm_d03` | 360 | `mrm_g0100` | 420 |
| | | `mrm_g0101` | 871 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Stilshrine of Miriam has 78 such rows.

Some actors run another actor's code: `PlayerJack1` in `mrm_a01` starts at the same place as `PlayerJack0` and runs
the same functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 27 of these
rows: 3 in `mrm_a01`, 3 in `mrm_a02`, 3 in `mrm_b01`, 3 in `mrm_c01`, 3 in `mrm_d01`, 3 in `mrm_d03`, 3 in `mrm_e01`,
3 in `mrm_f01` and 3 in `mrm_g01`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 28,513 |
| empty | 105 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that holds the standard motion `stdmotionplay` plays, or the variable that
receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `mrm_c0100` (event `360`), `監督.main` reads motion 1 of
`mrm_c0100.mot` and waits while `scratch1_var_1` is 0. It files `背景曲.曲読み込み`, reads event sound slots 0 and 1 and
effect file `e0166.efx`, files `ボス.ボス乗っ取る` and `PC乗っ取る` on the four `PC乗っ取り` actors, waits for all of them and fades
in over 30 frames. At the next cut it starts `カメラ.カメラc1`, `PC配置` on the four, `シェイク.シェイクc1` and four more requests
together, waits 50 frames and starts `ボス.穴から出現c1`.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line; a system message is not spoken by the actor |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank512, second half` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; `the item held in` and the variable for an item a variable holds; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `field held in` and the variable when the target field is a variable |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [stilshrine-of-miriam-script-list.tsv](stilshrine-of-miriam-script-list.tsv) holds the first table
above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`stilshrine-of-miriam-script-steps.tsv`](stilshrine-of-miriam-script-steps.tsv) has one row per step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Stilshrine of Miriam scenes](stilshrine-of-miriam-scenes.md) - the seven scenes these scripts own.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Paramina Rift scripts](paramina-rift-scripts.md) - the region beyond the Walk of Sky.
- [Mt Bur-Omisace scripts](mt-bur-omisace-scripts.md) - the holy mountain the Kiltias speak of.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
