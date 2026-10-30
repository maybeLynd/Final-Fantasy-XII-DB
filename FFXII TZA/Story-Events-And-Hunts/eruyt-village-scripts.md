---
title: "Eruyt Village scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Eruyt Village that does something a player can observe. It covers the
three zone scripts and the five scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `vic_a01` | zone | Fane of the Path, field `766` | 48 | 215 | 28 | 1 |
| `vic_a02` | zone | The Spiritwood, field `767` | 78 | 298 | 39 | 0 |
| `vic_a03` | zone | Road of Verdant Praise, field `768` | 23 | 76 | 17 | 5 |
| `vic_a0100` | scene | event `253` | 25 | 402 | 23 | 0 |
| `vic_a0280` | scene | event `733` | 18 | 72 | 0 | 0 |
| `vic_a0300` | scene | event `255` | 25 | 300 | 32 | 0 |
| `vic_a0301` | scene | event `256` | 20 | 181 | 13 | 0 |
| `vic_a0380` | scene | event `734` | 13 | 62 | 1 | 0 |

Road of Verdant Praise carries the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; Fane of the Path carries the key-item and message helper alone. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

The scene `vic_a0300` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

Two exits of The Spiritwood (`__MJ_CTRL002`, `__MJ_CTRL003`) lead to field `769`, which the map name table names by its
code, `vic_a04`. The script `vic_a04` ships under `plan_map/vic_a`, but the zone-script list has no entry for field
`769`, so it has no rows here; its steps are in the steps table.

`vic_a04` holds `Map_Director`, whose `init` returns at once, and two map exits, `__MJ_CTRL000` and `__MJ_CTRL001`, to
The Spiritwood (field `767`, entrances 3 and 4); the Spiritwood exits jump to field `769` (entrances 1 and 2), but the
field has no zone-script entry, so these jumps load no zone script and no jump reaches `vic_a04`.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Eruyt
Village scenes](eruyt-village-scenes.md).

### What the scripts do

- Road of Verdant Praise: `イベント管理.ミュリンを呼んできて_再生`, requested by `常駐監督.init`, loads scene `vic_a0380` (event 734) and
  writes 1740, after Go and fetch Mjrn. The Spiritwood: `イベント管理.侵入者の気配_再生` loads scene `vic_a0280` (event 733) and
  writes 1745, after signs of an intruder.
- Fane of the Path: while the story counter is from 1,745 to below 1,756, `SAKIYOMI_vic_a0100.init` loads scene
  `vic_a0100` (event 253), in which Jote turns the party away and tells that Mjrn has gone west; touching `SB5_ヨーテ`
  requests `イベント管理.ヨーテ前半_再生`, which writes 1756, after the first half of Jote.
- Road of Verdant Praise: `イベント管理.ヨーテ後半_再生` loads scene `vic_a0301` (event 256) and writes 1790, Rescue Mjrn. Fane of
  the Path: `イベント管理.姉と妹_再生` loads scene `vic_a0300` (event 255), which gives Lente's Tear, writes 1950, after the
  sisters, and jumps to Road of Verdant Praise, field `768`.
- The dewdrop pebbles: the sparkling lights of Fane of the Path (`キラリＡ` to `キラリＤ`) and The Spiritwood (`キラリＥ` to
  `キラリＪ`, and `森ヴィエラ２３Ｔ.talk_COCKATRICE`, requested by `キラリＨ.talk`) each give a Dewdrop Pebble ("You find a milk-white
  pebble. It would make for a fine gift.").
- Mjrn (`妹ミュリン０１Ｔ.talk_COCKATRICE`) takes the pebbles for the cockatrice and requests `イベント管理.チィ帰る_再生`, which takes
  them all; in its lines (`ＡＤ`) the bird remembers Terra and leaves for Giza, it gives a reward package with the
  Yoichi Bow, and it sets Bank2048 flag `0x00DE`, so the tag reads Chit.
- The pebbles stay in the village: touching `キラキラ石持ち出しチェック_RECT` in The Spiritwood jumps to Road of Verdant Praise,
  where `常駐監督.main` takes every Dewdrop Pebble ("The dewdrop pebbles vanish on the wind.") and sets flag `0x0044`, the
  location map's exits between Eruyt Village and Golmore Jungle.
- The Spiritwood: `イベント管理.バニークリア_再生` takes the Rabbit's Tail; in its lines (`ＡＤ`) Nera thanks the party for the
  dreamhare's tail and Alja speaks of the vision dust, and it sets the name flags of Nera (`0x0200`) and Alja
  (`0x01FC`). Rael and Kjrs speak of the vorpal bunny (`talk_vorpal_bunny`) and of a creature even Kjrs cannot match
  (`talk_wild_morbol`); Rael's functions set Kjrs's name flag `0x01FD`, and Kjrs's set Rael's, `0x0201`.
- Road of Verdant Praise: Lulucce (`０２ルルチェ.talk_地図屋`) sells the Eruyt Village map, with system message 83, "Your
  location map for this area is complete!", and tests the story counter against 3,000 and 5,150. `Map_Director.init`
  sets and tests flag `0x010C`, which The Needlebrake (Golmore Jungle) also sets or tests.
  `choco_sum_ctrl_murasawa.sumcho_byebye`, requested by the teleport, releases flag `0x0073`, riding a chocobo.
- The villagers speak of the Wood and of Mjrn: Hala, Alja, Nera, Rena, Wood-dwellers and Wood-warders in Fane of the
  Path and The Spiritwood, and the moogles Lulucce and `０１テトラン_SHOP` in Road of Verdant Praise.
- Fane of the Path and The Spiritwood hold 1 and 2 treasure chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | the second argument is a section 2 text id; the choices are in that text |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname`, `releasetalknpcname`, `istalknpcname` | `0x399`-`0x39B` | `0x0034DFA0`, `0x0034E320`, `0x0034E980` | `flags_*` | `Bank2048` flag: the name tag ([story flag ids](story-flag-ids.md), [NPC names](../Characters-And-Objects/npc-names.md)) |
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

The steps table [`eruyt-village-script-steps.tsv`](eruyt-village-script-steps.tsv) has one row for each step of every
function of the nine scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 17,914 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `vic_a01` | 3,663 | `vic_a0300` | 2,918 |
| `vic_a02` | 4,471 | `vic_a0301` | 1,613 |
| `vic_a03` | 1,169 | `vic_a0380` | 578 |
| `vic_a0100` | 2,986 | `vic_a04` | 63 |
| `vic_a0280` | 453 | | |

`vic_a04`, which no field loads, has 63 steps: those of `Map_Director.init` and of its two map exits.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Eruyt Village has 39 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 17,402 |
| empty | 512 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its functions. In `vic_a0280` (event `733`), `ＡＤ.Ｃ０３_ヴァン登場` starts scene cut 3,
sets `scratch1_var_1` to 3, files `EventLightActor.setEventLight` and files `カット０３` on fourteen actors at once, Vaan
among them. It waits 121 frames, files the camera's `常駐復帰`, calls `crossfade(0, 1, 8)` and waits for each actor's
`カット０３`.

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
is shown is written `[value]`. Some zone lines begin with a name the text itself carries (`Fran`, and the pebbles' `Sparkling Light`).

The script list [`eruyt-village-script-list.tsv`](eruyt-village-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`eruyt-village-script-steps.tsv`](eruyt-village-script-steps.tsv) has one row per step:

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
- [Eruyt Village scenes](eruyt-village-scenes.md) - the five scenes these scripts load.
- [Henne Mines scripts](henne-mines-scripts.md) - Ore Separation's jump leads to Fane of the Path.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
