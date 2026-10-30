---
title: "Trial Mode scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Trial Mode that does something a player can observe. It covers the
hundred zone scripts of the region, one per stage, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `tri_a01` | zone | stage 1, field `1155` | 17 | 22 | 3 | 0 |
| `tri_a02` | zone | stage 2, field `1156` | 14 | 19 | 3 | 0 |
| `tri_a03` | zone | stage 3, field `1157` | 18 | 23 | 3 | 0 |
| `tri_a04` | zone | stage 4, field `1158` | 16 | 21 | 3 | 0 |
| `tri_a05` | zone | stage 5, field `1159` | 17 | 22 | 3 | 0 |
| `tri_b01` | zone | stage 6, field `1163` | 16 | 21 | 3 | 0 |
| `tri_b02` | zone | stage 7, field `1164` | 15 | 20 | 3 | 0 |
| `tri_b03` | zone | stage 8, field `1165` | 16 | 21 | 3 | 0 |
| `tri_b04` | zone | stage 9, field `1166` | 15 | 21 | 3 | 0 |
| `tri_b05` | zone | stage 10, field `1167` | 12 | 18 | 3 | 0 |
| `tri_c01` | zone | stage 11, field `1171` | 12 | 18 | 3 | 0 |
| `tri_c02` | zone | stage 12, field `1172` | 20 | 25 | 3 | 0 |
| `tri_c03` | zone | stage 13, field `1173` | 13 | 20 | 3 | 0 |
| `tri_c04` | zone | stage 14, field `1174` | 16 | 22 | 3 | 0 |
| `tri_c05` | zone | stage 15, field `1175` | 14 | 20 | 3 | 0 |
| `tri_d01` | zone | stage 16, field `1179` | 17 | 23 | 3 | 0 |
| `tri_d02` | zone | stage 17, field `1180` | 15 | 22 | 3 | 0 |
| `tri_d03` | zone | stage 18, field `1181` | 11 | 16 | 3 | 0 |
| `tri_d04` | zone | stage 19, field `1182` | 11 | 16 | 3 | 0 |
| `tri_d05` | zone | stage 20, field `1183` | 16 | 21 | 3 | 0 |
| `tri_e01` | zone | stage 21, field `1187` | 15 | 21 | 3 | 0 |
| `tri_e02` | zone | stage 22, field `1188` | 19 | 24 | 3 | 0 |
| `tri_e03` | zone | stage 23, field `1189` | 19 | 24 | 3 | 0 |
| `tri_e04` | zone | stage 24, field `1190` | 19 | 24 | 3 | 0 |
| `tri_e05` | zone | stage 25, field `1191` | 19 | 24 | 3 | 0 |
| `tri_f01` | zone | stage 26, field `1195` | 19 | 24 | 3 | 0 |
| `tri_f02` | zone | stage 27, field `1196` | 15 | 20 | 3 | 0 |
| `tri_f03` | zone | stage 28, field `1197` | 15 | 20 | 3 | 0 |
| `tri_f04` | zone | stage 29, field `1198` | 17 | 22 | 3 | 0 |
| `tri_f05` | zone | stage 30, field `1199` | 16 | 22 | 4 | 0 |
| `tri_g01` | zone | stage 31, field `1203` | 19 | 27 | 6 | 0 |
| `tri_g02` | zone | stage 32, field `1204` | 17 | 24 | 4 | 0 |
| `tri_g03` | zone | stage 33, field `1205` | 14 | 19 | 3 | 0 |
| `tri_g04` | zone | stage 34, field `1206` | 14 | 19 | 3 | 0 |
| `tri_g05` | zone | stage 35, field `1207` | 16 | 24 | 5 | 0 |
| `tri_h01` | zone | stage 36, field `1211` | 17 | 23 | 4 | 0 |
| `tri_h02` | zone | stage 37, field `1212` | 17 | 26 | 3 | 0 |
| `tri_h03` | zone | stage 38, field `1213` | 13 | 18 | 3 | 0 |
| `tri_h04` | zone | stage 39, field `1214` | 14 | 20 | 3 | 0 |
| `tri_h05` | zone | stage 40, field `1215` | 14 | 20 | 3 | 0 |
| `tri_i01` | zone | stage 41, field `1219` | 15 | 21 | 3 | 0 |
| `tri_i02` | zone | stage 42, field `1220` | 16 | 22 | 3 | 0 |
| `tri_i03` | zone | stage 43, field `1221` | 15 | 20 | 3 | 0 |
| `tri_i04` | zone | stage 44, field `1222` | 16 | 21 | 3 | 0 |
| `tri_i05` | zone | stage 45, field `1223` | 19 | 24 | 3 | 0 |
| `tri_j01` | zone | stage 46, field `1227` | 16 | 21 | 3 | 0 |
| `tri_j02` | zone | stage 47, field `1228` | 12 | 17 | 3 | 0 |
| `tri_j03` | zone | stage 48, field `1229` | 15 | 20 | 3 | 0 |
| `tri_j04` | zone | stage 49, field `1230` | 14 | 20 | 3 | 0 |
| `tri_j05` | zone | stage 50, field `1231` | 15 | 21 | 3 | 0 |
| `tri_k01` | zone | stage 51, field `1235` | 14 | 19 | 3 | 0 |
| `tri_k02` | zone | stage 52, field `1236` | 12 | 17 | 3 | 0 |
| `tri_k03` | zone | stage 53, field `1237` | 13 | 18 | 3 | 0 |
| `tri_k04` | zone | stage 54, field `1238` | 15 | 24 | 4 | 0 |
| `tri_k05` | zone | stage 55, field `1239` | 16 | 25 | 4 | 0 |
| `tri_l01` | zone | stage 56, field `1243` | 17 | 26 | 4 | 0 |
| `tri_l02` | zone | stage 57, field `1244` | 16 | 21 | 3 | 0 |
| `tri_l03` | zone | stage 58, field `1245` | 16 | 22 | 3 | 0 |
| `tri_l04` | zone | stage 59, field `1246` | 15 | 20 | 3 | 0 |
| `tri_l05` | zone | stage 60, field `1247` | 15 | 20 | 3 | 0 |
| `tri_m01` | zone | stage 61, field `1251` | 18 | 23 | 3 | 0 |
| `tri_m02` | zone | stage 62, field `1252` | 19 | 26 | 5 | 0 |
| `tri_m03` | zone | stage 63, field `1253` | 15 | 20 | 3 | 0 |
| `tri_m04` | zone | stage 64, field `1254` | 13 | 18 | 3 | 0 |
| `tri_m05` | zone | stage 65, field `1255` | 13 | 18 | 3 | 0 |
| `tri_n01` | zone | stage 66, field `1259` | 16 | 21 | 3 | 0 |
| `tri_n02` | zone | stage 67, field `1260` | 12 | 17 | 3 | 0 |
| `tri_n03` | zone | stage 68, field `1261` | 14 | 20 | 3 | 0 |
| `tri_n04` | zone | stage 69, field `1262` | 17 | 23 | 3 | 0 |
| `tri_n05` | zone | stage 70, field `1263` | 18 | 24 | 3 | 0 |
| `tri_o01` | zone | stage 71, field `1267` | 17 | 23 | 3 | 0 |
| `tri_o02` | zone | stage 72, field `1268` | 13 | 18 | 3 | 0 |
| `tri_o03` | zone | stage 73, field `1269` | 15 | 20 | 3 | 0 |
| `tri_o04` | zone | stage 74, field `1270` | 15 | 20 | 3 | 0 |
| `tri_o05` | zone | stage 75, field `1271` | 15 | 20 | 3 | 0 |
| `tri_p01` | zone | stage 76, field `1275` | 15 | 20 | 3 | 0 |
| `tri_p02` | zone | stage 77, field `1276` | 15 | 20 | 3 | 0 |
| `tri_p03` | zone | stage 78, field `1277` | 15 | 20 | 3 | 0 |
| `tri_p04` | zone | stage 79, field `1278` | 13 | 18 | 3 | 0 |
| `tri_p05` | zone | stage 80, field `1279` | 13 | 18 | 3 | 0 |
| `tri_q01` | zone | stage 81, field `1283` | 18 | 24 | 3 | 0 |
| `tri_q02` | zone | stage 82, field `1284` | 17 | 23 | 4 | 0 |
| `tri_q03` | zone | stage 83, field `1285` | 14 | 20 | 4 | 0 |
| `tri_q04` | zone | stage 84, field `1286` | 17 | 24 | 4 | 0 |
| `tri_q05` | zone | stage 85, field `1287` | 14 | 20 | 4 | 0 |
| `tri_r01` | zone | stage 86, field `1291` | 20 | 30 | 4 | 0 |
| `tri_r02` | zone | stage 87, field `1292` | 13 | 20 | 5 | 0 |
| `tri_r03` | zone | stage 88, field `1293` | 16 | 22 | 4 | 0 |
| `tri_r04` | zone | stage 89, field `1294` | 13 | 22 | 3 | 0 |
| `tri_r05` | zone | stage 90, field `1295` | 13 | 22 | 3 | 0 |
| `tri_s01` | zone | stage 91, field `1299` | 19 | 26 | 5 | 0 |
| `tri_s02` | zone | stage 92, field `1300` | 16 | 22 | 4 | 0 |
| `tri_s03` | zone | stage 93, field `1301` | 14 | 20 | 3 | 0 |
| `tri_s04` | zone | stage 94, field `1302` | 13 | 19 | 4 | 0 |
| `tri_s05` | zone | stage 95, field `1303` | 27 | 51 | 18 | 0 |
| `tri_t01` | zone | stage 96, field `1307` | 20 | 25 | 3 | 0 |
| `tri_t02` | zone | stage 97, field `1308` | 14 | 22 | 5 | 0 |
| `tri_t03` | zone | stage 98, field `1309` | 13 | 19 | 4 | 0 |
| `tri_t04` | zone | stage 99, field `1310` | 23 | 42 | 14 | 0 |
| `tri_t05` | zone | stage 100, field `1311` | 18 | 29 | 6 | 0 |

No Trial Mode script carries one of the five helper actors that many zone scripts share ([Shared zone-script
actors](shared-zone-script-actors.md)), so the Shared helpers column is 0 throughout. The stages load one scene,
`pos_z0000` (event 427), which is described on [Victory pose scenes](victory-pose-scenes.md).

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step).

### What the scripts do

- The stages are `tri_a01` to `tri_t05`: the letter is the block of five stages and the digit the stage in it, so
  `tri_k04` is stage 54. Each block takes eight field ids and uses five: stages 1 to 5 are fields 1155 to 1159, stages
  6 to 10 fields 1163 to 1167, and stages 96 to 100 fields 1307 to 1311.
- A Trial Mode start loads stage 1: with load mode 3 the save handover `0x00584210` stores `0x483`, field 1155, as the
  destination field ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).
- Every stage script runs the same `トライアル監督` code and branches on the current field. `main` waits on the variable
  `scratch1_var_1` (`waitv`), fades out over 15 frames, removes every foe and jumps to the next stage: the current
  field plus 1, or plus 4 after the fifth stage of a block.
- On the last stage, field 1311, `main` loads scene `pos_z0000` (event 427) and jumps to `ttl_d01`, field 1147, the
  Trial Mode completion screen, which offers New Game- ([titles scripts](titles-scripts.md), [strong and weak
  mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)). Before the scene it unlocks achievement 40
  (`unkCall_5ad(40)`); after stage 50 it unlocks achievement 39.
- On twenty-five stages the boss gauge opens: stages 10, 13, 15, 16, 18, 19, 21, 29, 32, 35, 39, 42, 49, 50, 68, 81,
  84, 87, 89, 90, 94, 95, 97, 98 and 99 ([battle menu](../Menus-And-HUD/battle-menu.md)).
- After stages 10, 20, 30, 40, 50, 60, 70, 80 and 90 the director plays music 86 and gives a reward package with
  `additemmes`, listed below ([scene rewards](scene-rewards.md)).
- The stages hold 250 treasure chests: two in seventy-nine stages, three in thirteen, four in five, five in one,
  twelve in stage 99 (`tri_t04`) and sixteen in stage 95 (`tri_s05`).
- On the first stage after each reward, stages 11, 21, 31, 41, 51, 61, 71, 81 and 91 (fields 1171 to 1299 in steps of
  16), `main` shows "You will now have the option of saving your game." the first time the party arrives
  (`global_var_1` below the field), opens the save menu (`openfullscreenmenu_48d` with `0x8005`) and reads music 35,
  45, 15, 85, 60, 88, 48, 75 and 57 on those stages in turn.
- Five stage scripts, `tri_k04`, `tri_k05`, `tri_l01`, `tri_s05` and `tri_t04` (stages 54, 55, 56, 95 and 99), set
  flags `0x00FD` to `0x0103` in `Map_Director.init`, the map-icon flags of The Great Crystal's maps ([story flag
  ids](story-flag-ids.md)).

| After stage | Field | Package | Contents |
|---:|---:|---|---|
| 10 | 1167 | `0x9123` | 1000 gil, Hi-Potion x10, Handkerchief x15 |
| 20 | 1183 | `0x9124` | 2000 gil, Phoenix Down x10, Domaine Calvados x5 |
| 30 | 1199 | `0x9125` | 3000 gil, Ether x10, Echo Herbs x15 |
| 40 | 1215 | `0x9126` | 4000 gil, Phoenix Down x10, Reverse Mote x3 |
| 50 | 1231 | `0x9127` | 5000 gil, X-Potion x10, Chronos Tear x15 |
| 60 | 1247 | `0x9128` | 6000 gil, Phoenix Down x10, Scathe Mote x3 |
| 70 | 1263 | `0x9129` | 7000 gil, Hi-Ether x10, Serum x15 |
| 80 | 1279 | `0x912A` | 8000 gil, Elixir x3, Bubble Mote x3 |
| 90 | 1295 | `0x912B` | 9000 gil, Megalixir x2, Remedy x15 |

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

The steps table [`trial-mode-script-steps.tsv`](trial-mode-script-steps.tsv) has one row for each step of every
function of the hundred scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 158,706 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `tri_a01` | 1,626 | `tri_k01` | 1,532 |
| `tri_a02` | 1,532 | `tri_k02` | 1,526 |
| `tri_a03` | 1,556 | `tri_k03` | 1,531 |
| `tri_a04` | 1,621 | `tri_k04` | 1,968 |
| `tri_a05` | 1,561 | `tri_k05` | 1,973 |
| `tri_b01` | 1,556 | `tri_l01` | 1,978 |
| `tri_b02` | 1,541 | `tri_l02` | 1,546 |
| `tri_b03` | 1,546 | `tri_l03` | 1,584 |
| `tri_b04` | 1,547 | `tri_l04` | 1,541 |
| `tri_b05` | 1,546 | `tri_l05` | 1,541 |
| `tri_c01` | 1,529 | `tri_m01` | 1,556 |
| `tri_c02` | 1,564 | `tri_m02` | 1,601 |
| `tri_c03` | 1,572 | `tri_m03` | 1,541 |
| `tri_c04` | 1,584 | `tri_m04` | 1,531 |
| `tri_c05` | 1,574 | `tri_m05` | 1,531 |
| `tri_d01` | 1,563 | `tri_n01` | 1,546 |
| `tri_d02` | 1,582 | `tri_n02` | 1,526 |
| `tri_d03` | 1,521 | `tri_n03` | 1,547 |
| `tri_d04` | 1,521 | `tri_n04` | 1,589 |
| `tri_d05` | 1,542 | `tri_n05` | 1,594 |
| `tri_e01` | 1,580 | `tri_o01` | 1,589 |
| `tri_e02` | 1,561 | `tri_o02` | 1,531 |
| `tri_e03` | 1,561 | `tri_o03` | 1,541 |
| `tri_e04` | 1,561 | `tri_o04` | 1,541 |
| `tri_e05` | 1,561 | `tri_o05` | 1,541 |
| `tri_f01` | 1,561 | `tri_p01` | 1,541 |
| `tri_f02` | 1,541 | `tri_p02` | 1,541 |
| `tri_f03` | 1,541 | `tri_p03` | 1,541 |
| `tri_f04` | 1,552 | `tri_p04` | 1,531 |
| `tri_f05` | 1,564 | `tri_p05` | 1,531 |
| `tri_g01` | 1,615 | `tri_q01` | 1,580 |
| `tri_g02` | 1,593 | `tri_q02` | 1,569 |
| `tri_g03` | 1,536 | `tri_q03` | 1,554 |
| `tri_g04` | 1,536 | `tri_q04` | 1,581 |
| `tri_g05` | 1,593 | `tri_q05` | 1,554 |
| `tri_h01` | 1,576 | `tri_r01` | 1,641 |
| `tri_h02` | 1,623 | `tri_r02` | 1,567 |
| `tri_h03` | 1,531 | `tri_r03` | 1,566 |
| `tri_h04` | 1,547 | `tri_r04` | 1,629 |
| `tri_h05` | 1,539 | `tri_r05` | 1,629 |
| `tri_i01` | 1,544 | `tri_s01` | 1,600 |
| `tri_i02` | 1,563 | `tri_s02` | 1,564 |
| `tri_i03` | 1,541 | `tri_s03` | 1,574 |
| `tri_i04` | 1,546 | `tri_s04` | 1,549 |
| `tri_i05` | 1,562 | `tri_s05` | 2,299 |
| `tri_j01` | 1,546 | `tri_t01` | 1,567 |
| `tri_j02` | 1,526 | `tri_t02` | 1,594 |
| `tri_j03` | 1,542 | `tri_t03` | 1,555 |
| `tri_j04` | 1,547 | `tri_t04` | 2,189 |
| `tri_j05` | 1,589 | `tri_t05` | 1,673 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). No script of Trial Mode carries
one of them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 131,354 |
| empty | 27,352 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the standard motion that `stdmotionplay` plays or the variable that receives a result, and `-`
otherwise.

A function reads from top to bottom. In `tri_b05`, stage 10, `トライアル監督.main` opens the boss gauge, waits on
`scratch1_var_1`, turns user control off, closes the boss gauge and waits 30 frames. It reads quest effect 43 and
music 86, plays the music and the effect's parts 0, 1 and 2 with waits of 30 and 90 frames, plays sound 39 and gives
package `0x9123` with `additemmes`. It then fades out over 15 frames, removes every foe and jumps to field 1171, stage
11.

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

The script list [`trial-mode-script-list.tsv`](trial-mode-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`trial-mode-script-steps.tsv`](trial-mode-script-steps.tsv) has one row per step:

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

- [Titles scripts](titles-scripts.md) - the Trial Mode completion screen `ttl_d01` that the last stage jumps to.
- [Victory pose scenes](victory-pose-scenes.md) - the scene `pos_z0000` that the stage scripts load.
- [Shared zone-script actors](shared-zone-script-actors.md) - the helper actors other regions share.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
