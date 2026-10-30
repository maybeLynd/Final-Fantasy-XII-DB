---
title: "Garamsythe Waterway scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [garamsythe-waterway-scripts.tsv](garamsythe-waterway-scripts.tsv) has one row per script function of the
Garamsythe Waterway that does something a player can observe. It covers the twenty-eight zone scripts and the sixteen
scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `grm_a01` | zone | Central Spur Stairs, field `311` | 18 | 54 | 5 | 5 |
| `grm_a02` | zone | East Waterway Control, field `312` | 23 | 36 | 11 | 0 |
| `grm_a03` | zone | North Spur Sluiceway, field `313` | 31 | 90 | 16 | 0 |
| `grm_a04` | zone | East Spur Stairs, field `314` | 26 | 88 | 8 | 5 |
| `grm_a05` | zone | Northern Sluiceway, field `315` | 21 | 30 | 8 | 0 |
| `grm_a06` | zone | East Waterway Control, field `316` | 24 | 46 | 7 | 1 |
| `grm_b01` | zone | No. 11 Channel, field `318` | 21 | 31 | 8 | 0 |
| `grm_b02` | zone | East Sluice Control, field `319` | 27 | 84 | 8 | 5 |
| `grm_b03` | zone | West Sluice Control, field `320` | 17 | 22 | 4 | 0 |
| `grm_b04` | zone | No. 10 Channel, field `321` | 22 | 31 | 7 | 0 |
| `grm_b05` | zone | Central Waterway Control, field `322` | 20 | 86 | 7 | 5 |
| `grm_c01` | zone | Southern Sluiceway, field `326` | 18 | 37 | 6 | 0 |
| `grm_d01` | zone | Overflow Cloaca, field `329` | 11 | 48 | 3 | 0 |
| `grm_e01` | zone | No. 11 Channel, field `838` | 23 | 35 | 10 | 0 |
| `grm_e02` | zone | No. 11 Channel, field `839` | 31 | 49 | 16 | 0 |
| `grm_e03` | zone | East Sluice Control, field `840` | 20 | 57 | 7 | 5 |
| `grm_e04` | zone | Southern Sluiceway, field `841` | 12 | 26 | 3 | 1 |
| `grm_e05` | zone | West Sluice Control, field `842` | 18 | 32 | 3 | 1 |
| `grm_e06` | zone | No. 10 Channel, field `843` | 22 | 34 | 10 | 0 |
| `grm_e07` | zone | No. 10 Channel, field `844` | 30 | 48 | 16 | 0 |
| `grm_e08` | zone | No. 3 Cloaca Spur, field `845` | 16 | 27 | 10 | 0 |
| `grm_e09` | zone | No. 3 Cloaca Spur, field `846` | 26 | 68 | 16 | 0 |
| `grm_e10` | zone | No. 1 Cloaca, field `847` | 25 | 39 | 10 | 0 |
| `grm_e11` | zone | No. 4 Cloaca Spur, field `848` | 16 | 27 | 10 | 0 |
| `grm_e12` | zone | No. 4 Cloaca Spur, field `849` | 26 | 68 | 16 | 0 |
| `grm_e13` | zone | Central Waterway Control, field `850` | 44 | 172 | 29 | 5 |
| `grm_f01` | zone | No. 1 Cloaca, field `342` | 24 | 44 | 12 | 0 |
| `grm_g01` | zone | Overflow Cloaca, field `1145` | 18 | 65 | 4 | 0 |
| `grm_a0200` | scene | event `237` | 16 | 116 | 2 | 0 |
| `grm_a0380` | scene | event `715` | 7 | 27 | 0 | 0 |
| `grm_a0400` | scene | event `317` | 16 | 102 | 14 | 0 |
| `grm_a0401` | scene | event `318` | 7 | 29 | 1 | 0 |
| `grm_a0480` | scene | event `738` | 9 | 47 | 13 | 0 |
| `grm_b0200` | scene | event `319` | 28 | 189 | 6 | 0 |
| `grm_b0202` | scene | event `238` | 18 | 160 | 17 | 0 |
| `grm_b0280` | scene | event `716` | 13 | 72 | 20 | 0 |
| `grm_c0100` | scene | event `310` | 15 | 116 | 0 | 0 |
| `grm_c0101` | scene | event `311` | 17 | 92 | 0 | 0 |
| `grm_d0100` | scene | event `312` | 15 | 126 | 0 | 0 |
| `grm_d0102` | scene | event `236` | 29 | 246 | 2 | 0 |
| `grm_f0100` | scene | event `314` | 11 | 45 | 0 | 0 |
| `grm_f0101` | scene | event `315` | 17 | 77 | 15 | 0 |
| `grm_g0100` | scene | event `235` | 8 | 61 | 11 | 0 |
| `grm_g0101` | scene | event `267` | 12 | 64 | 4 | 0 |

Central Spur Stairs, East Spur Stairs, East Sluice Control (field 319), Central Waterway Control (field 322), East
Sluice Control (field 840) and Central Waterway Control (field 850) carry the five helper actors that many zone
scripts share: the crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the
key-item and message helper `イベント特殊効果画面`.

East Waterway Control (field 316), Southern Sluiceway (field 841) and West Sluice Control (field 842) carry the
key-item and message helper alone. Their functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Garamsythe
Waterway scenes](garamsythe-waterway-scenes.md).

### What the scripts do

- Central Spur Stairs: on the first arrival (`g_com_mnp_ガラムサイズ水路ロケタイ` 0), `常駐監督.main` loads the location title
  `ttl_z0001` (event 216), sets that variable to 1, shows the crystal and sets flag `0x001E`; later, arriving by
  entrance 2, the one North Sprawl (Lowtown) jumps to, sets `0x001E`. From story counter 180 to 290 it releases flag
  `0x0059`, a map icon in North Sprawl.
- Central Spur Stairs: an exit leads to North Sprawl (Lowtown), field 701. Below story counter 350 the exit to No. 10
  Channel leads to field 321; from 350 it leads to field 843 or field 844 by the state of the sluice gate that `スイッチあ`
  in Central Waterway Control (field 850) operates.
- East Waterway Control (field 312): at story counter 175, `常駐ディレクター.main` plays scene `grm_a0200` (event 237), writes
  180 and jumps to South Sprawl (Lowtown), field 702. Below 350 its exit to No. 11 Channel leads to field 318, from
  350 to field 838 or 839; East Waterway Control (field 316) does the same.
- North Spur Sluiceway: from story counter 180 to 189, `SAKIYOMI_grm_a0380.init` loads scene `grm_a0380` (event 715).
  Touching `SB1_王宮突入` asks "The palace should be right up these stairs." and "Won't be easy getting out. Am I ready
  for this?"; "Climb the stairs." and "It's now or never." play the scene, write 190 and jump to Cellar Stores (Royal
  Palace), field 567.
- North Spur Sluiceway: the gate (`閉じた扉`) shows "The gate is tightly shut."
- East Spur Stairs: from story counter 225 to 229, `常駐監督.init` requests `イベント管理.即席パーティー結成_再生`, which adds Fran and
  Balthier to the party, sets the fighting party to Vaan, Balthier and Fran, plays scene `grm_a0400` (event 317) and
  writes 235, the start of the escape from the waterway.
- East Spur Stairs: from story counter 235 to 243, `SAKIYOMI_grm_a0480` loads scene `grm_a0480` (event 738),
  Balthier's talk on gambits; touching `TUTORIAL_イベント管理` plays it and writes 244.
- East Spur Stairs: from story counter 225 to 289, `常駐監督.init` places two bodies (`ダルマスカ兵士死体`, `ダルマスカ兵士死体２`). Talking
  to `ダルマスカ兵士死体` the first time plays scene `grm_a0401` (event 318); after that it shows one line by the controlled
  character: Balthier ("Boys with too much hate and too little experience."), Fran, Amalia ("...") or, for any other,
  Vaan ("there's just no time. Sorry...").
- East Spur Stairs holds the crystal. East Waterway Control (field 316): the urn `ガラムサイズ地図宝壺` gives the area map,
  Garamsythe Waterway, with system message 103 ("Your location map for this area is complete!").
- East Sluice Control (field 319): from story counter 244 to 256, while `g_btl_ガラムサイズ帝国兵` is 1, `常駐監督.main` loads and
  plays scenes `grm_b0200` (event 319) and `grm_b0202` (event 238) and shows the boss gauge; touching `ボス起動レクト`
  requests `ボスイベント起動.ガラムサイズ帝国兵`, which runs the fight.
- East Sluice Control (field 319): when that fight ends, `ボスイベント起動.ガラムサイズ帝国兵` removes every foe, sets
  `g_btl_ガラムサイズ帝国兵` to 2, writes 257 and loads scene `grm_b0280` (event 716). From 257 to 259, touching `アーシェ前` adds
  Amalia to the party as a guest, plays `grm_b0280`, writes 260 and shows "Unlike other party members, guests can only
  use certain actions and abilities."
- East Sluice Control (field 319) and Central Waterway Control (field 322) hold crystals. In Central Waterway Control
  (field 322) the four sluice gate devices (`スイッチあ` to `スイッチえ`) show "It is currently locked in place.", and the door
  `tobira_to_19` leads to Overflow Cloaca, field 329.
- Southern Sluiceway (field 326): from story counter 260 to 264, while `g_btl_プリン` is 1, `常駐監督.main` loads and plays
  scenes `grm_c0100` (event 310) and `grm_c0101` (event 311) and shows the boss gauge; touching `ボス起動レクト_プリン` starts
  the fight.
- Southern Sluiceway (field 326): when the fight ends, `ボスイベント起動.プリン` removes every foe, loads the victory pose scene
  `pos_z0000` (event 427, [Victory pose scenes](victory-pose-scenes.md)), sets `g_btl_プリン` to 2 and writes 265, the
  value after the Flan battle.
- Overflow Cloaca (field 329): `常駐監督.main` sets flag `0x001F`. From story counter 265 to 274, while `g_btl_ブッシュファイア`
  is 1, it loads and plays scenes `grm_d0100` (event 312) and `grm_d0102` (event 236) and runs the fight under the
  boss gauge; when it ends it removes every foe, sets `g_btl_ブッシュファイア` to 2, writes 285 and jumps to North Sprawl
  (Lowtown), field 701.
- Overflow Cloaca (field 329): the door `SOUTH_door` opens once `g_btl_ブッシュファイア` is not 1 and leads to Central
  Waterway Control: field 322 below story counter 290, field 850 from 290.
- East Sluice Control (field 840): arriving by entrance 6, the one Terminus No. 7 (Barheim Passage) jumps to, sets
  flag `0x0040`, the location map's exits between Barheim Passage and the Garamsythe Waterway; an exit leads to
  Terminus No. 7, field 71. East Sluice Control holds the crystal.
- East Sluice Control (field 840): the urn `ガラムキャンドル宝壺` gives the Garamsythe Candle with system message 118 ("The
  candle reveals hidden areas on your map of the [value]!").
- Southern Sluiceway (field 841): when the `g_btl_nm_オルトロス` fight ends, `wanted_kansi.main` gives the Stolen Articles
  and removes the foes of a group. West Sluice Control (field 842): when the `g_btl_nm_ホワイトムース` fight ends,
  `wanted_kansi.main` gives the Broken Key and removes the foes of a group.
- No. 10 Channel (field 844): `hunt_kansi.main` gives the Fur-scaled Trophy and removes the foes of a group.
- No. 3 Cloaca Spur (field 846) and No. 4 Cloaca Spur (field 849): the controls `水門真中２` ("The No. 1 South sluice gates
  are open.") and `水門真中１` ("The No. 1 North sluice gates are open.") offer to close or open the gates; doing so shows
  "You hear a sluice gate move in the distance."
- Central Waterway Control (field 850) holds the crystal. Without the sluice gate key its four devices (`スイッチあ` to
  `スイッチえ`) show "The device is locked in place. You will need a sluice gate key to operate it."; with it, the first
  use offers "Use the sluice gate key.", and then each offers "Close the sluice gates." or "Open the sluice gates."
- Central Waterway Control (field 850): while two of the four devices are switched on, the other two show "Nothing
  happens. It appears only two of the devices can be activated at once."
- Central Waterway Control (field 850): each operated gate adds its device to a five-step record; the order `スイッチえ`,
  `スイッチう`, `スイッチえ`, `スイッチい`, `スイッチう` sets bit `0x1` of `g_iw_メダル関係フラグ[0]`. From story counter 290, while bit `0x1` is
  set and bit `0x2` clear, the spot `メダルレクト` gives the Dull Fragment and sets bit `0x2`.
- Central Waterway Control (field 850): holding the Black Bottle, the light the rats swarm over (`ネズミボトルレクト`) asks
  "Hold the bottle nearer to the light?"; Yes shows "Without warning, the black bottle shatters!", gives an Elixir,
  takes the Black Bottle and gives the Onyx Message. The script's three other bottle spots test fields 171, 163 and
  1151, so none is placed here.
- Central Waterway Control (field 850): the door `tobira_to_19` leads to Overflow Cloaca, field 1145.
- No. 1 Cloaca: while `g_btl_キュクレイン` is 1, `常駐監督.main` loads and plays scenes `grm_f0100` (event 314) and `grm_f0101`
  (event 315) and shows the boss gauge; touching `ボス起動レクト_キュクレイン` starts the fight, and when it ends removes every
  foe, loads `pos_z0000` (event 427) and sets `g_btl_キュクレイン` to 2.
- Overflow Cloaca (field 1145): `常駐監督.main` sets flag `0x001F`. Below story counter 27 it loads and plays scenes
  `grm_g0101` (event 267) and `grm_g0100` (event 235) and runs the fight under the boss gauge; when it ends it removes
  every foe, sets `g_btl_ネズミ` to 2, writes 33 and jumps to Muthru Bazaar (Rabanastre), field 290.
- Overflow Cloaca (field 1145): from story counter 27, while `g_btl_nm_レイス` is 1, `常駐監督.賞金首レイス監視` waits for that fight
  to end, adds 1 to `quest_global_flag[6]`, sets `g_btl_nm_レイス` to 2 and removes the foes. The door `SOUTH_door_e13`
  shows "The door is securely closed." below 350 and leads to Central Waterway Control, field 850, from 350.
- North Spur Sluiceway, Northern Sluiceway, East Waterway Control (field 316), No. 11 Channel (field 318), West Sluice
  Control (field 320), No. 10 Channel (field 321), Southern Sluiceway (field 326), No. 11 Channel (field 839), No. 10
  Channel (field 844), No. 3 Cloaca Spur (field 846) and No. 4 Cloaca Spur (field 849) hold 8, 6, 4, 6, 2, 4, 2, 6, 5,
  3 and 3 treasure chests.

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

The steps table [`garamsythe-waterway-script-steps.tsv`](garamsythe-waterway-script-steps.tsv) has one row for each
step of every function of the forty-four scripts, in the order the function runs them: each call, request, store,
branch, loop, case and return. It has 36,351 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `grm_a01` | 455 | `grm_e10` | 1,068 |
| `grm_a02` | 563 | `grm_e11` | 919 |
| `grm_a03` | 809 | `grm_e12` | 1,286 |
| `grm_a04` | 598 | `grm_e13` | 3,622 |
| `grm_a05` | 324 | `grm_f01` | 1,391 |
| `grm_a06` | 453 | `grm_g01` | 788 |
| `grm_b01` | 299 | `grm_a0200` | 623 |
| `grm_b02` | 761 | `grm_a0380` | 256 |
| `grm_b03` | 241 | `grm_a0400` | 1,460 |
| `grm_b04` | 368 | `grm_a0401` | 312 |
| `grm_b05` | 601 | `grm_a0480` | 567 |
| `grm_c01` | 581 | `grm_b0200` | 1,647 |
| `grm_d01` | 662 | `grm_b0202` | 1,421 |
| `grm_e01` | 698 | `grm_b0280` | 996 |
| `grm_e02` | 849 | `grm_c0100` | 1,102 |
| `grm_e03` | 493 | `grm_c0101` | 744 |
| `grm_e04` | 148 | `grm_d0100` | 1,190 |
| `grm_e05` | 311 | `grm_d0102` | 1,320 |
| `grm_e06` | 703 | `grm_f0100` | 536 |
| `grm_e07` | 855 | `grm_f0101` | 890 |
| `grm_e08` | 920 | `grm_g0100` | 617 |
| `grm_e09` | 1,290 | `grm_g0101` | 614 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Garamsythe Waterway has 204 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 36,202 |
| empty | 149 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `grm_a0401` (event `318`), `AD.main` reads models
`0x03000000` to `0x03000002` and motion 1 of `grm_a0401.mot`, waits while `scratch1_var_1` is 0 and files `イベント準備` on
three actors, waiting for all three. At scene cut 1 it fades the music to volume 80 over 180 frames, starts `カット０１ａ`
on five actors together and fades in over 15 frames. It starts `カット０１ｂ`, waits 140 and 484 frames, starts `カット０１ｃ` at
cut 3, waits 260 frames, fades the music back to volume 127 and fades out over 15 frames.

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
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [garamsythe-waterway-script-list.tsv](garamsythe-waterway-script-list.tsv) holds the first table
above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`garamsythe-waterway-script-steps.tsv`](garamsythe-waterway-script-steps.tsv) has one row per step:

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
- [Garamsythe Waterway scenes](garamsythe-waterway-scenes.md) - the sixteen scenes these scripts own.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Lowtown scripts](lowtown-scripts.md) - North Sprawl and South Sprawl, beyond the waterway's exits.
- [Royal Palace scripts](royal-palace-scripts.md) - the Cellar Stores the stairs of North Spur Sluiceway lead to.
- [Rabanastre scripts](rabanastre-scripts.md) - Muthru Bazaar, where the first visit to Overflow Cloaca ends.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
