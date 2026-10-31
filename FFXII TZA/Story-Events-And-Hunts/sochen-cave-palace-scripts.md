---
title: "Sochen Cave Palace scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [sochen-cave-palace-scripts.tsv](sochen-cave-palace-scripts.tsv) has one row per script function of the
Sochen Cave Palace that does something a player can observe. It covers the eleven zone scripts and the nine scene
scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `rui_a01` | zone | Falls of Time, field `184` | 34 | 81 | 20 | 0 |
| `rui_a02` | zone | Mirror of the Soul, field `185` | 39 | 105 | 18 | 1 |
| `rui_a03` | zone | The Acolyte's Burden, field `186` | 27 | 110 | 8 | 5 |
| `rui_a04` | zone | Doubt Abandoned, field `187` | 31 | 80 | 15 | 0 |
| `rui_a05` | zone | Skybent Chamber, field `188` | 21 | 84 | 5 | 5 |
| `rui_b01` | zone | Destiny's March, field `192` | 60 | 167 | 39 | 0 |
| `rui_b02` | zone | Temptation Eluded, field `193` | 23 | 69 | 7 | 0 |
| `rui_b03` | zone | Chamber of the Chosen, field `194` | 11 | 51 | 4 | 0 |
| `rui_c01` | zone | Hall of Shadowlight, field `198` | 24 | 71 | 8 | 0 |
| `rui_d01` | zone | Hall of Lambent Darkness, field `200` | 23 | 75 | 8 | 0 |
| `rui_e01` | zone | Hall of the Wroth God, field `202` | 16 | 58 | 6 | 0 |
| `rui_a0400` | scene | event `168` | 13 | 99 | 8 | 0 |
| `rui_a0500` | scene | event `169` | 12 | 93 | 0 | 0 |
| `rui_b0300` | scene | event `166` | 13 | 103 | 0 | 0 |
| `rui_c0100` | scene | event `160` | 11 | 48 | 0 | 0 |
| `rui_c0101` | scene | event `161` | 12 | 54 | 0 | 0 |
| `rui_d0100` | scene | event `162` | 23 | 107 | 0 | 0 |
| `rui_d0101` | scene | event `163` | 25 | 156 | 0 | 0 |
| `rui_e0100` | scene | event `164` | 14 | 47 | 0 | 0 |
| `rui_e0101` | scene | event `165` | 15 | 56 | 1 | 0 |

The Acolyte's Burden and Skybent Chamber carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; Mirror of the Soul carries the key-item and message helper alone. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Sochen Cave
Palace scenes](sochen-cave-palace-scenes.md).

### What the scripts do

- Falls of Time: an inscription (`gim_sign`) reads "You who are yet drawn toward the Pilgrim's Door, journey Heaven
  and Earth in search of the heart, and you will surely reach it.", and `Map_Director.main` holds the lines "You hear
  a door open in the distance." and "The waterfalls seem to have returned to their original course."
- Mirror of the Soul: two doors (`gim_door01`, `gim_door02`) bear the Pilgrim's Door inscription ("From the heart look
  north to Heaven. From the heart step south to Earth. Walk in Time's footfalls to open the way."). `hunt_kansi.main`
  gives the Ensanguined Trophy and removes the foes of a group, and `ソーヘン地下宮殿地図` gives the area map, Sochen Cave
  Palace, with system message 112.
- The Acolyte's Burden holds a crystal that `クリスタル監視さん.init` hides while `g_btl_クリスタルミミックブルー` is 1; while it is 1,
  `クリスタル監視さん.main` shows "A crystal appears!" (system message 129), sets it to 2 and removes the foes of a group. A
  corpse (`バンガ死体レクト１`) reads "An adventurer bound for the capital. It would seem he didn't make it."
- Doubt Abandoned: `DIRECTOR.main` sets flag `0x002B`, the location map's exits between the Sochen Cave Palace and the
  Tchita Uplands; the exit leads to Fields of Eternity (Tchita Uplands), field 140.
- Doubt Abandoned: below story counter 3120, `監督.main` writes 3120, shows "You will now have the option of saving your
  game." and opens a full-screen menu; below 3130 it then loads and plays scene `rui_a0400` (event 168) and writes
  3130, the value after the Sochen Cave Palace.
- Doubt Abandoned: while `g_btl_nm_オーバーロード` is 1, `監督.main` gives `THIRD_シーク`, the Insecure Seeq, the lines "Let's
  find this overlord. Don't wanna keep the ladies waiting!" and "Hrm? No sign of this overlord...";
  `wanted_kansi.main`, also while it is 1, sets it to 2, removes the foes and holds the seeq's line "Ha ha! I did it!"
- Doubt Abandoned: the door `big_door_01` shows "The door is locked. You will need the soul ward key to open it.";
  with the key held it offers "Use the soul ward key.", sets flag `0x014C` and leads to Hall of Lambent Darkness,
  field 200.
- Skybent Chamber and Chamber of the Chosen: the lift device (`ele_switch`, "Activate the lift.") sets map-icon flags
  `0x00C1` and `0x011B` and carries the party between the two, field 194 and field 188. Skybent Chamber's exit leads
  to Alley of Low Whispers (Old Archades), field 763.
- Skybent Chamber and Chamber of the Chosen: arriving from the other chamber (in Skybent Chamber, from field 194 by
  entrance 0), `DIRECTOR.init` loads scenes `rui_b0300` (event 166) and `rui_a0500` (event 169) and `main` plays both;
  any other arrival loads and plays `rui_a0500` alone in Skybent Chamber and `rui_b0300` alone in Chamber of the
  Chosen.
- Destiny's March: the inscription (`gim_sign`) reads "You who are yet drawn toward the Ascetic's Door, in circles
  travel from land of Sun's birth. Stray but once, another day must you return." The door `secret_door` bears "count
  out your steps tracing Sun's round. At journey's end, the Door embrace you."
- Destiny's March: twenty actors (`gim_door02` to `gim_door17b`) hold the line "You hear a door open in the distance."
  and request `secret_door.map_door_ok`, which sets flag `0x014D`.
- Destiny's March: `big_door_02` shows "The door is securely locked. With the proper key, it might be possible to open
  it."; with the ageworn key held it offers "Use the ageworn key.", sets flag `0x014E` and leads to Hall of the Wroth
  God, field 202. `hunt_kansi.main` gives the Frigid Trophy and removes the foes of a group.
- Temptation Eluded: `wanted_kansi.main` removes the foes of a group.
- Hall of Shadowlight: while `g_btl_アーリマン` is 1, `監督.main` loads and plays scenes `rui_c0100` (event 160) and
  `rui_c0101` (event 161) and shows the boss gauge; when the fight ends it writes 3200, the value after the Ahriman
  battle, removes every foe and loads the victory pose scene `pos_z0000` (event 427, [Victory pose
  scenes](victory-pose-scenes.md)).
- Hall of Lambent Darkness: while `g_btl_マンドラゴラーズ` is 1, `監督.main` loads and plays scenes `rui_d0100` (event 162) and
  `rui_d0101` (event 163) and shows the boss gauge; when the fight ends it writes 3150, the value after the
  Mandragoras battle, removes every foe and loads `pos_z0000` (event 427).
- Hall of the Wroth God: while `g_btl_魔神竜` is 1, `監督.main` loads scenes `rui_e0100` (event 164) and `rui_e0101` (event
  165) when `Boss_Enter_End[5]` is not 1, setting it, and `rui_e0101` alone otherwise, and shows the boss gauge; when
  the fight ends it removes every foe, loads `pos_z0000` (event 427) and sets `g_btl_魔神竜` to 2.
- Falls of Time, Mirror of the Soul, The Acolyte's Burden, Doubt Abandoned, Destiny's March, Temptation Eluded, Hall
  of Shadowlight, Hall of Lambent Darkness and Hall of the Wroth God hold 8, 8, 2, 9, 7, 4, 5, 4 and 4 treasure
  chests.

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

- The speaker of a line is the name its window shows. A `{name:P}` header (escape `0F 8`) names pair P in `us`
  `npcdic.bin`, P read as the parser `0x003FFB00` reads it. A plain name before the first line break,
  after `{instant:8181}` or at the start of a zone line, shows that name. An `{actor-name}` header (escape `0F >`)
  shows the name `0x00263990` gives the actor the window speaks for.
- The header's name comes from `0x002639E0`, which three of the five callers of `0x003FFB00` call next
  (`0x002ADDAA`, `0x002B16D4`, `0x002B52EF`): the first name while the pair's name flag is clear, the second once it is set. The
  `speaker` cell gives the second name. The window sets the flag of the pair of the actor it speaks for (next
  item), and `settalknpcname` sets any pair's ([NPC names](../Characters-And-Objects/npc-names.md)).
- The window speaks for the message call's target, the calling actor or the actor an `X.` prefix names: `0x002621D0`
  passes it to the verb, and `0x00348DF0` hands it to `0x002E16B0`. That actor's name is the second name of each pair its
  `setnpcname` calls name; `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- An actor no `setnpcname` or `setshopname` call names keeps the name id `0xFFFF` and the empty text the record set-up
  `0x00266530` writes (`0x0026668B`, `0x0026669B`-`0x002666B4`), so its `{actor-name}` header shows no name; that line reads
  `no name shown`. A system message reads `system message`.
- A line whose text carries no name takes the window actor's `setnpcname` name. Failing that, a scene subtitle
  (centred, or in the subtitle font `{alt-font}`) takes the character the window speaks for.
- Then any line without a name takes the speaker of the voice cue joined to it ([Voices](../Sound-And-Music/voices.md)),
  else the actor of the row's `TAGmes_<actor>_<n>` function, else the actor whose mouth function (`paku_on`,
  `unapaku_on`, `クチウナオン`, `kutipaku_on`, `kutipakuON`) is requested in its window or around the request of its
  function.
- A character's game name is the second name its `setnpcname` gives; else the party member whose model its bind verbs
  name, the `c` entries of the script's [actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) read
  against the `model` column of the [party table](../Party/party-table.md), a main member before a guest; else
  the NPC name or string table row whose `in` cell is the actor's name.
- Any other line without a name reads `no name shown`, apart from a scene subtitle, which keeps its row's cell `-`. A
  line whose name is `???` reads `???`: the game prints `???` as that speaker's name at that line. A row lists its
  speakers in line order, each once.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`sochen-cave-palace-script-steps.tsv`](sochen-cave-palace-script-steps.tsv) has one row for each step
of every function of the twenty scripts, in the order the function runs them: each call, request, store, branch, loop,
case and return. It has 21,607 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `rui_a01` | 1,337 | `rui_e01` | 860 |
| `rui_a02` | 1,099 | `rui_a0400` | 1,142 |
| `rui_a03` | 717 | `rui_a0500` | 1,665 |
| `rui_a04` | 934 | `rui_b0300` | 1,867 |
| `rui_a05` | 789 | `rui_c0100` | 423 |
| `rui_b01` | 3,306 | `rui_c0101` | 491 |
| `rui_b02` | 569 | `rui_d0100` | 1,263 |
| `rui_b03` | 459 | `rui_d0101` | 995 |
| `rui_c01` | 783 | `rui_e0100` | 1,030 |
| `rui_d01` | 865 | `rui_e0101` | 1,013 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Sochen Cave Palace has 68 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 21,559 |
| empty | 48 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `rui_e0100` (event `164`), `DIRECTOR.main` files
`AD.START_ad`, reads motion 1 of `rui_e0100.mot` and model `0x03000000`, waits for all three and waits while
`scratch1_var_1` is 0. It reads event sound slots 0 and 1 and effect file `e0149.efx`, waiting for each. It files
`AD.カット１_ad`, plays effect slot 0 and waits until `AD.カット１_ad` ends, then files `AD.END_s_ad`, frees the motion, sound
slot 1 and the effect, and waits until `AD.END_s_ad` and `BGM.CUT01` end.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank512, second half` flag carries its bank name |
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

The script list [sochen-cave-palace-script-list.tsv](sochen-cave-palace-script-list.tsv) holds the first table above,
one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`sochen-cave-palace-script-steps.tsv`](sochen-cave-palace-script-steps.tsv) has one row per step:

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
- [Sochen Cave Palace scenes](sochen-cave-palace-scenes.md) - the nine scenes these scripts own.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Tchita Uplands scripts](tchita-uplands-scripts.md) and [Old Archades scripts](old-archades-scripts.md) - the regions beyond the exits.
- [Cerobi Steppe scripts](cerobi-steppe-scripts.md) - the Wyrm Philosopher, who gives the Ageworn Key.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
