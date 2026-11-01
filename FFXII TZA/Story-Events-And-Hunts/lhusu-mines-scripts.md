---
title: "Lhusu Mines scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00352EA0, 0x00353390, 0x00354000, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Lhusu Mines that does something a player can observe. It covers the
twenty zone scripts and the eleven scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `lus_a01` | zone | Shaft Entry, field `357` | 35 | 113 | 20 | 0 |
| `lus_a02` | zone | Oltam Span, field `358` | 28 | 58 | 10 | 0 |
| `lus_a03` | zone | Transitway 1, field `359` | 38 | 111 | 21 | 0 |
| `lus_a04` | zone | Transitway 2, field `360` | 21 | 64 | 6 | 5 |
| `lus_b01` | zone | Shunia Twinspan, field `365` | 32 | 46 | 13 | 0 |
| `lus_b02` | zone | Site 2, field `366` | 30 | 91 | 11 | 0 |
| `lus_b03` | zone | Site 3, field `367` | 25 | 36 | 10 | 0 |
| `lus_c01` | zone | Tasche Span, field `369` | 17 | 24 | 5 | 0 |
| `lus_d01` | zone | Site 9, field `372` | 48 | 185 | 24 | 0 |
| `lus_d03` | zone | Site 11, field `374` | 38 | 108 | 17 | 0 |
| `lus_e01` | zone | Site 7, field `376` | 18 | 29 | 5 | 0 |
| `lus_f01` | zone | Lasche Span, field `901` | 15 | 22 | 5 | 0 |
| `lus_f02` | zone | Site 5, field `902` | 43 | 121 | 21 | 1 |
| `lus_f03` | zone | Site 6 South, field `903` | 25 | 36 | 10 | 0 |
| `lus_f04` | zone | Site 6 North, field `904` | 16 | 20 | 3 | 0 |
| `lus_f05` | zone | Staging Area, field `905` | 16 | 47 | 4 | 5 |
| `lus_g01` | zone | Site 2, field `933` | 32 | 62 | 17 | 0 |
| `lus_g02` | zone | Shunia Twinspan, field `934` | 23 | 35 | 11 | 0 |
| `lus_g03` | zone | Transitway 1, field `935` | 25 | 37 | 12 | 0 |
| `lus_g04` | zone | Oltam Span, field `936` | 20 | 28 | 7 | 0 |
| `lus_a0100` | scene | event `296` | 32 | 253 | 8 | 0 |
| `lus_a0180` | scene | event `702` | 10 | 41 | 2 | 0 |
| `lus_c0100` | scene | event `290` | 14 | 88 | 1 | 0 |
| `lus_c0101` | scene | event `291` | 12 | 58 | 5 | 0 |
| `lus_c0102` | scene | event `292` | 15 | 78 | 0 | 0 |
| `lus_e0100` | scene | event `293` | 14 | 70 | 2 | 0 |
| `lus_e0101` | scene | event `294` | 13 | 63 | 4 | 0 |
| `lus_e0102` | scene | event `295` | 19 | 111 | 0 | 0 |
| `lus_g0100` | scene | event `297` | 30 | 507 | 2 | 0 |
| `lus_g0101` | scene | event `299` | 17 | 66 | 1 | 0 |
| `lus_g0280` | scene | event `701` | 9 | 29 | 0 | 0 |

Transitway 2 and the Staging Area carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; Site 5 carries the key-item and message helper alone. Their functions are described once on [Shared
zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

Four map names appear twice. Fields `933` to `936` (`lus_g01` to `lus_g04`) are second versions of Site 2, Shunia
Twinspan, Transitway 1 and Oltam Span: the exits of Shunia Twinspan and of the second versions test the story counter
(below 660, or from 645 to below 660) to choose between the two versions of the next map.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Lhusu Mines
scenes](lhusu-mines-scenes.md).

### What the scripts do

- Shaft Entry: from story counter 580 to below 610, `SAKIYOMI_lus_a0100.init` loads scene `lus_a0100` (event 296), in
  which the Marquis of Bhujerba, Halim Ondore IV, is named; `常駐監督.main` sets and tests flag `0x0032`, the location
  map's exits between Bhujerba and Lhusu Mines. Touching `イベント起動_気配` requests `イベント管理.帝国軍の気配_再生`, which writes 610,
  after signs of the imperial army. One exit leads to Lhusu Square (Bhujerba), field `806`.
- Site 2 (field `933`): touching `ボス起動レクト` requests `ボスイベント起動.バッガモナン`, which shows the boss gauge, removes the foes
  and writes 645, after the secret of the mines, and 660, after the Ba'Gamnan battle; `常駐監督.main` loads scenes
  `lus_g0100` (event 297), in which the party are shown manufacted nethicite from the Draklor Laboratory, and
  `lus_g0101` (event 299), and writes 660.
- The chase: from story counter 645 to below 660, `常駐監督.init` of Oltam Span, Transitway 1, Shunia Twinspan and the
  four second-version maps loads `lus_g0101`; `イベント管理.逃げるラーサー_再生` of Oltam Span, Transitway 1, Shunia Twinspan and
  fields `934` to `936` shows the boss gauge, removes the foes, loads scene `lus_g0280` (event 701) and writes 660.
- Shaft Entry: `イベント管理.バッガモナン振り切った_再生` loads scene `lus_a0180` (event 702) and writes 660 ("We've lost them.").
- The carts (`トロッコ_手前`, `トロッコ_奥`) of Shaft Entry, Transitway 1, Site 9, Site 11 and Site 5 jump between Transitway 1,
  Shaft Entry and Site 9, or between Site 5 and Site 11, and set each map's cart icon flag, `0x00F1` to `0x00F5`;
  until their route is cleared they show "This cart can be used to traverse the mines, however it is presently
  inoperable."
- The switches (`スイッチ.talk`) of Shaft Entry, Transitway 1, Site 2, Site 9 and Site 11 set the five gate icon flags
  `0x00F6` to `0x00FA` ("The switch has already been pressed."), and the gates (`鉄柵メッセージ`) say "There must be a switch
  or lever somewhere to operate it."
- Site 9: the gate `鉱区の扉` sets flags `0x0157`, `0x007E` and `0x0141` ("The gate is locked. The [value] should open
  it."). `賞金首アントリオン監視.main` removes the foes of a group. Kait (`カイト_AT.talk`, Transitway 2) says her brother went
  deeper into the mines and that she fears the antlion; the lines of `ＡＤ` in Site 9, requested by
  `イベント管理.アントリオン倒した_再生`, have her brother found, the key to the depths dropped, and the two return to Bhujerba.
- Gilgamesh: in Tasche Span `常駐監督.main` shows the boss gauge, removes the foes and loads scenes `lus_c0100` (event
  290), `lus_c0102` (event 292), `lus_c0101` (event 291) and `pos_z0000` (event 427); in Site 7 it loads `lus_e0100`
  (event 293), `lus_e0102` (event 295), `lus_e0101` (event 294) and `pos_z0000`. Site 7: the `伝説の剣` shows "It appears
  to be an ordinary sword of legend.", and touching `ギルガメッシュ剣奪還` jumps to the Staging Area, field `905`.
- Site 5: the pot `ルースキャンドル宝壺` gives the Lhusu Candle, shows system message 120, "The candle reveals hidden areas on
  your map of the [value]!", and sets treasure flag `0x0007`. Site 5 and Site 6 South: `hunt_kansi.main` gives the
  Accursed Trophy and removes the foes of a group. Transitway 1, Site 2 and Site 11: `wanted_kansi.main` removes the
  foes of a group.
- Transitway 2 and the Staging Area: `choco_sum_ctrl_murasawa.sumcho_byebye`, requested by the teleport, releases flag
  `0x0073`, riding a chocobo.
- Shaft Entry, Oltam Span, Transitway 1, Shunia Twinspan, Site 3, Site 9, Site 11, Site 7, Lasche Span, Site 5, Site 6
  South, Site 6 North, the Staging Area and Site 2 (field `933`) hold 6, 3, 3, 3, 8, 7, 7, 1, 1, 12, 5, 2, 1 and 8
  treasure chests.

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

The steps table [`lhusu-mines-script-steps.tsv`](lhusu-mines-script-steps.tsv) has one row for each step of every
function of the thirty-one scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 35,121 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `lus_a01` | 3,626 | `lus_f05` | 193 |
| `lus_a02` | 670 | `lus_g01` | 1,044 |
| `lus_a03` | 3,800 | `lus_g02` | 869 |
| `lus_a04` | 338 | `lus_g03` | 975 |
| `lus_b01` | 702 | `lus_g04` | 618 |
| `lus_b02` | 1,009 | `lus_a0100` | 2,115 |
| `lus_b03` | 308 | `lus_a0180` | 386 |
| `lus_c01` | 689 | `lus_c0100` | 788 |
| `lus_d01` | 4,348 | `lus_c0101` | 746 |
| `lus_d03` | 1,619 | `lus_c0102` | 709 |
| `lus_e01` | 626 | `lus_e0100` | 654 |
| `lus_f01` | 183 | `lus_e0101` | 757 |
| `lus_f02` | 1,517 | `lus_e0102` | 1,160 |
| `lus_f03` | 348 | `lus_g0100` | 3,256 |
| `lus_f04` | 127 | `lus_g0101` | 494 |
| | | `lus_g0280` | 447 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Lhusu Mines has 68 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 32,320 |
| empty | 2,800 |
| `does not ship`, with the fact | 1 |

The one `does not ship` row is a `motionread` call in `lus_a04`, whose motion file `lus_a04.mot` is not in the archive.
A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its functions. In `lus_a0180` (event `702`), `ＡＤ.Ｃ０２_しつこいなぁ` starts scene cut 2,
sets `scratch1_var_1` to 2 and files `カット０２ａ` on the camera, voice and subtitle actors, Balthier and Fran together. It
waits 170 frames and until the voice and subtitle finish, then starts cut 102 with `カット０２ｂ` and waits 200 frames. At
cut 202 it fades out over 15 frames and waits for the remaining actors.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
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
is shown is written `[value]`. Some zone lines begin with a name the text itself carries (`Sword of Legend`).

The script list [`lhusu-mines-script-list.tsv`](lhusu-mines-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`lhusu-mines-script-steps.tsv`](lhusu-mines-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test` |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
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
- [Lhusu Mines scenes](lhusu-mines-scenes.md) - the eleven scenes these scripts load.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
