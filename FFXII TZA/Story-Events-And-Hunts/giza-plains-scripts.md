---
title: "Giza Plains scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00352EA0, 0x00353390, 0x00354000, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Giza Plains that does something a player can observe. It covers the
seventeen zone scripts and the five scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `sav_a01` | zone | Throne Road, field `236` | 37 | 96 | 16 | 1 |
| `sav_a02` | zone | Warrior's Wash, field `237` | 41 | 142 | 17 | 1 |
| `sav_a03` | zone | Gizas North Bank, field `238` | 49 | 153 | 21 | 1 |
| `sav_a04` | zone | Toam Hills, field `239` | 37 | 94 | 15 | 1 |
| `sav_b01` | zone | Nomad Village, field `243` | 68 | 432 | 74 | 5 |
| `sav_c01` | zone | Starfall Field, field `247` | 48 | 155 | 25 | 1 |
| `sav_c02` | zone | Crystal Glade, field `248` | 41 | 153 | 17 | 5 |
| `sav_c03` | zone | Gizas South Bank, field `249` | 43 | 144 | 18 | 1 |
| `sav_d01` | zone | Throne Road, field `253` | 28 | 81 | 12 | 0 |
| `sav_d02` | zone | Warrior's Wash, field `254` | 23 | 32 | 9 | 0 |
| `sav_d03` | zone | Gizas North Bank, field `255` | 24 | 73 | 9 | 0 |
| `sav_d04` | zone | Toam Hills, field `256` | 27 | 78 | 11 | 0 |
| `sav_e01` | zone | Nomad Village, field `260` | 32 | 136 | 9 | 5 |
| `sav_f01` | zone | Starfall Field, field `264` | 34 | 100 | 15 | 1 |
| `sav_f02` | zone | Crystal Glade, field `265` | 38 | 165 | 12 | 5 |
| `sav_f03` | zone | Gizas South Bank, field `266` | 31 | 75 | 13 | 0 |
| `sav_g01` | zone | Tracks of the Beast, field `270` | 27 | 52 | 12 | 1 |
| `sav_b0100` | scene | event `170` | 24 | 118 | 22 | 0 |
| `sav_b0180` | scene | event `719` | 10 | 53 | 1 | 0 |
| `sav_b0181` | scene | event `737` | 8 | 41 | 13 | 0 |
| `sav_c0280` | scene | event `717` | 10 | 58 | 16 | 0 |
| `sav_c0281` | scene | event `718` | 9 | 46 | 3 | 0 |

Nomad Village and Crystal Glade (fields `243`, `248`, `260` and `265`) carry the five helper actors that many zone
scripts share: the crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the
key-item and message helper `イベント特殊効果画面`; the scripts with 1 in the Shared helpers column carry the key-item
and message helper alone. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md)
and have no rows here.

The scenes `sav_b0100`, `sav_b0181` and `sav_c0280` hold their own helper `イベント特殊効果画面_EV`, which is not one of
the five, so its functions have rows.

Each map name appears twice. Fields `236` to `249` (`sav_a`, `sav_b`, `sav_c`) are the Dry; fields `253` to `270`
(`sav_d` to `sav_g`) are the Rains, where lines say the village is left during the Rains and the
scripts' `Map_Director` sets flag `0x0109`, which lists Giza Plains on the map screens.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Giza Plains
scenes](giza-plains-scenes.md).

### What the scripts do

- Nomad Village (Dry): while the story counter is from 120 to 129, `SAKIYOMI_sav_b0100` loads scene `sav_b0100`, in
  which Penelo meets Vaan. `１３マシュア.talk_taiyo_ＯＫ` writes 125, and `イベント管理.ギーザパンネロ合流_再生` makes
  Penelo join, sets the fighting party to Vaan and Penelo, writes 130 and requests `SAKIYOMI_sav_b0181`, which loads
  scene `sav_b0181`.
- Nomad Village (Dry): touching a tutorial rectangle runs `イベント管理.パンネロチュートリアル_再生`, which writes 140 and
  sends the party out to Throne Road, Gizas North Bank or Toam Hills. `イベント管理.太陽石できた後半_再生` writes 160
  (Sunstone obtained) and loads scene `sav_b0180`.
- Crystal Glade (Dry): Jinn sits with a hurt leg. `SAKIYOMI_sav_c0280.sakiyomi_init` loads scene `sav_c0280`, whose
  lines have Jinn hand over a shadestone and explain the dark crystals; `イベント管理.太陽石の作り方_再生` writes 145
  and sets the four dark crystal map icons (`0x005A`, `0x0091`, `0x0092`, `0x0093`), and
  `イベント管理.太陽石できた前半_再生` loads scene `sav_c0281` and jumps back to Nomad Village.
- Dark crystals in Warrior's Wash, Gizas North Bank, Starfall Field and Gizas South Bank: talking to `黒水晶Ａ` charges
  the Shadestone, and when the charge is full `満タン判定` takes the Shadestone and gives the Sunstone through the
  helper; below story counter 160 it then jumps to Crystal Glade, field `248`.
- Nomad Village (Dry) quests: Masyua gives gil, Holy Stones and Potions, takes the Sunstone and gives a Shadestone; Lesina
  takes an Errmonea Leaf for two Remedies; Elder Brunoa takes the Ring of the Toad; Terra gives two Hi-Ethers for the
  escaped cockatrices; `イベント管理.ギルガメクリア_再生` takes the Silent Urn after the gil snapper.
- Nomad Village (Dry) name tags: functions of the nomads set their Bank2048 name flags, so the tags read Nanau,
  Roaklo, Elder Brunoa, Camina, Terra and Nutsy instead of their generic names.
- The Dry maps: Throne Road, Warrior's Wash, Gizas North Bank, Toam Hills, Starfall Field and Gizas South Bank hold
  7, 7, 7, 7, 11 and 6 treasure chests.
- The Dry maps' exits: `常駐監督.main` of Throne Road sets flag `0x001C` (exits to Rabanastre) and
  loads scene `ttl_z0004` (event 431); Starfall Field sets `0x0030` and `0x0031` (Dalmasca Westersand, Ozmone Plain);
  Gizas South Bank sets `0x0021` (Dalmasca Estersand). Starfall Field's `hunt_kansi.main` gives the Maned Trophy.
- The Rains maps: Throne Road, Warrior's Wash, Gizas North Bank, Toam Hills, Nomad Village, Starfall Field, Gizas
  South Bank and Tracks of the Beast hold 4, 6, 5, 6, 1, 7, 6 and 7 treasure chests. Dead trees drift with the
  water (`kareki`), and on Gizas South Bank "with several more pieces of driftwood, it should be possible to cross
  to the other bank".
- Nomad Village (Rains): Sadeen asks for her ring, "South of...Starfall Field". On Crystal Glade (Rains) Nanau and Roaklo ask for help with the gil snapper and leave a soggy
  letter, and Nanau gives the Silent Urn; in Tracks of the Beast Bansat of Clan Centurio joins that hunt and `賞金首ギルガメ監視` removes the foes
  and shows "The gil snapper was drawn into the urn."
- Starfall Field (Rains): `wanted_kansi.main` removes the foes of a group and gives the Ring of the Toad.
- Tracks of the Beast: `Map_Director.init` sets flag `0x005B`, which shows the map on the location map, and the pot
  `コカトーク宝壺` gives the Feather of the Flock through the helper and sets treasure flag `0x0021`.
- Crystal Glade (Dry and Rains): talking to `system_anchor_actor` requests `ym_shutoraljump.shtjump`, which loads
  scene `str_z0000` (event 211) and jumps to the field a script variable holds.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | the second argument is a section 2 text id; the choices are in that text |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname`, `releasetalknpcname`, `istalknpcname` | `0x399`-`0x39B` | `0x0034DFA0`, `0x0034E320`, `0x0034E980` | `flags_*` | `Bank2048` flag: the name tag ([story flag ids](story-flag-ids.md), [NPC names](../Characters-And-Objects/npc-names.md)) |
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

The steps table [`giza-plains-script-steps.tsv`](giza-plains-script-steps.tsv) has one row for each step of every
function of the twenty-two scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 34,754 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `sav_a01` | 1,263 | `sav_d04` | 847 |
| `sav_a02` | 2,210 | `sav_e01` | 1,449 |
| `sav_a03` | 2,444 | `sav_f01` | 1,011 |
| `sav_a04` | 1,121 | `sav_f02` | 1,975 |
| `sav_b01` | 9,131 | `sav_f03` | 809 |
| `sav_c01` | 2,534 | `sav_g01` | 481 |
| `sav_c02` | 1,890 | `sav_b0100` | 1,147 |
| `sav_c03` | 2,310 | `sav_b0180` | 400 |
| `sav_d01` | 976 | `sav_b0181` | 632 |
| `sav_d02` | 261 | `sav_c0280` | 669 |
| `sav_d03` | 797 | `sav_c0281` | 397 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Giza Plains has 196 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has none.

The `resolution` column says how far each step is known:

| Resolution | Steps |
|---|---:|
| `resolved` | 32,097 |
| what was searched, when no page yet gives what the arguments name | 2,657 |

When no page yet gives what a step's arguments name, the cell says what was searched, for example the standard motion
table that `stdmotionplay` reads, or a verb that no page describes yet.

A scene reads from top to bottom in its director's function. In `sav_b0180` (event `719`), `監督.main` files `ＡＤ.準備`,
`ＡＤ.Ｃ０１_集落遠景`, `ＡＤ.Ｃ０２_集落に帰る` and `ＡＤ.Ｃ０３_マシュアお礼` in turn, each waited for to its end, and then `ＡＤ.終了`. It then
starts scene cut 0 and disposes of the event.

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
is shown is written `[value]`. Many zone lines begin with the speaker's name, which the text itself carries (`Penelo`, `Jinn`).

The script list [`giza-plains-script-list.tsv`](giza-plains-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`giza-plains-script-steps.tsv`](giza-plains-script-steps.tsv) has one row per step:

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
| `resolution` | `resolved`; `does not ship:` and the fact; or, when no page yet gives what the arguments name, what was searched |
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
- [Giza Plains scenes](giza-plains-scenes.md) - the five scenes these scripts load.
- [Dalmasca Estersand scripts](dalmasca-estersand-scripts.md) - the region beyond Gizas South Bank.
- [Dalmasca Westersand scripts](dalmasca-westersand-scripts.md) - the region beyond Starfall Field.
- [Ozmone Plain scripts](ozmone-plain-scripts.md) - the region south of Starfall Field.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
