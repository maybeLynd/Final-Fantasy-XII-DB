[Home](../../README.md) / [Story, events and hunts](README.md) / Trial Mode scripts

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Trial Mode scripts: what each script function shows, sets, gives and starts | reference | Story, events and hunts | Scenes and scripts by area / Opening, ending and Trial Mode | Every function of the hundred Trial Mode stage scripts that a player can observe: what triggers it, the lines it shows, the flags it sets, the reward packages and treasure chests it gives, the stage-to-stage map jumps, the boss gauge and foe removal, and the scene it loads after the last stage. | 0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0 |

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

The script list also gives each stage's foes, chests, reward, entry and what changes between attempts. A stage is entered by clearing the one before: the director `トライアル監督.main` waits while scratch1 word `0x06` is 0 (`waitv`), removes every foe (`bosskillall`, `zakokillall`) and jumps to the next field. None of the 250 chests has a flag (`flag_id` `0xFF`), so each is there and rolled again on every attempt, and the nine packages are given again on every clear; the save prompt of stages 11 to 91 comes once, while script global word `0x0CF4` is below the field.

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

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `amese` pushes 0, 0, 0 and -1; `amest` pushes 0; `ames` pushes 1. Each then jumps to `0x00349800`, the body of `ames_1fe`. | `0x0034A420`<br>`0x0034A090`<br>`0x00349BF0` |
| 2 | `0x00349800` pops two values, pushes 0 and 0 and then pushes the two values back in their original order, so the zeros lie beneath them; it jumps to `0x00348DF0`. | `0x00349827`, `0x00349831`<br>`0x0034983D`, `0x00349847`<br>`0x00349851`, `0x0034985B`<br>`0x00349884` |
| 3 | `0x00348DF0` pops eight values. The seventh, the script's second argument, is passed with the current field context to `0x00264D60`, the section 2 lookup, which keeps the low 24 bits of the id. | `0x00348E6A`-`0x00348E74` |
| 4 | `0x00348DF0` reads the entry's flag through `0x002673A0`, bit `0x1` of the entry's upper half, and opens the window through `0x002E16B0` only when that flag is clear. With the flag set it still makes its six slot calls and fills the call record but opens no window ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)). | `0x00348E85`<br>`0x00348EE0`-`0x00348EFF`<br>`0x00348E91`-`0x00348ECA`<br>`0x00348ED7`-`0x00348EDC` |

### Speakers, places and scenes

- The speaker of a line is the name its window shows. A `{name:P}` header (escape `0F 8`) names pair P in `us`
  `npcdic.bin`, P read as the parser `0x003FFB00` reads it. A plain name before the first line break,
  after `{instant:8181}` or at the start of a zone line, shows that name. An `{actor-name}` header (escape `0F >`)
  shows the name `0x00263990` gives the actor the window speaks for.
- The header's name comes from `0x002639E0`, which three of the five callers of `0x003FFB00` call next
 ¹: the first name while the pair's name flag is clear, the second once it is set. The
  `speaker` cell gives the second name. The window sets the flag of the pair of the actor it speaks for (next
  item), and `settalknpcname` sets any pair's ([NPC names](../Characters-And-Objects/npc-names.md)).
- The window speaks for the message call's target, the calling actor or the actor an `X.` prefix names: `0x002621D0`
  passes it to the verb, and `0x00348DF0` hands it to `0x002E16B0`. That actor's name is the second name of each pair its
  `setnpcname` calls name; `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- `0x00348DF0` makes that `0x002E16B0` call only for a line whose section 2 flag is clear²; for a flagged
  line it opens no window, so the actor's name flag is not set there.
- An actor no `setnpcname` or `setshopname` call names keeps the name id `0xFFFF` and the empty text the record set-up
  `0x00266530` writes³, so its `{actor-name}` header shows no name; that line reads
  `no name shown`. A system message reads `system message`.
- A line whose text carries no name takes the window actor's `setnpcname` name. Failing that, a scene subtitle
  (centred, or in the subtitle font `{alt-font}`) takes the character the window speaks for.
- Then any line without a name takes the speaker of the voice cue joined to it ([Voices](../Sound-And-Music/voices.md)),
  else the actor of the row's `TAGmes_<actor>_<n>` function, else the actor whose mouth function (`paku_on`,
  `unapaku_on`, `クチウナオン`, `kutipaku_on`, `kutipakuON`) is requested in its window or around the request of its
  function.
- A scene subtitle these steps leave without a speaker takes the speaker of the one voice cue that starts on the frame
  the subtitle opens or within 10 frames after, else of the one speaker whose cues play through at least half the
  frames it is shown while no other speaker's cues play through more than a fifth. Every showing of the line must give
  the same speaker, and a subtitle of two speakers, which starts `- `, takes no speaker by this step.
- The frames are those of the clock of [Voices](../Sound-And-Music/voices.md) ("How a cue is joined to its line"), which
  runs every function of the scene, one that no other function starts on a clock of its own. A variable keeps the
  value its declaration or its last store gives.
- Each case of a `switch` on a value the run cannot know runs on a clock of its own, a `sysReqwait` for a function
  another function requested waits for the end of that request, and a line stays shown until the next message call or
  `mesclose` on its window.
- A cue whose `speaker` cell names no actor takes the character its sound code belongs to, the letters after the
  number in its `sound` name ([Voices](../Sound-And-Music/voices.md)), when three or more cues with that code name a
  speaker and three quarters of them or more name that one character.
- A cue whose sound code belongs to another character than its speaker plays through another actor's slot, so it names
  no speaker by these two steps, unless the two characters share a party model. A line shown on a movie's frames takes
  no cue's speaker: its function, or each function that requests it, waits on `getmovieframe` before showing it.
- A character's game name is the second name its `setnpcname` gives; else the party member whose model its bind verbs
  name, the `c` entries of the script's [actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) read
  against the `model` column of the [party table](../Party/party-table.md), a main member before a guest; else
  the NPC name or string table row whose `in` cell is the actor's name.
- The actor `REX` of `naf_a0100`, `naf_b0100`, `naf_b0400` and `naf_b0401` (`Rex` in `naf_a0201`) has no `c`
  entry. Its bind verb names a `C` entry, a high-detail model, `high/c10/c1025/hc1025_02` (`hc1025_01` in
  `naf_a0201`); `chara/c10/c1025/c1025` is model `c15`, and row 6 of the party table, model `c15`, is Reks, the
  name the rows of these scenes give that actor.
- An actor these steps leave unnamed whose bind verbs name one `n` entry of the manifest takes the name the game
  gives the other actors bound to that `n` model, by these steps or as a voice cue's speaker
  ([Voices](../Sound-And-Music/voices.md)), when they all give one name and two or more actors give it or the bestiary
  gives the same.
- Failing that, it takes the [bestiary](../Enemy-Spawning/bestiary.md) name of that model id (its
  `model_id` cell), when the bestiary gives it one name. A `c` model is left out of these two steps, since the
  bestiary can name a battle alias there: Amalia for Ashe's `c11`.
- An actor these steps leave unnamed whose only body is `capturepc(-1)`, the character the player controls, speaks as
  Reks in a scene each of whose loading steps runs while the story counter is below 25: until then the party is
  [scenario preset](../Party/scenario-presets.md) 0, Reks alone, and the
  [party table](../Party/party-table.md) gives no join below 25.
- Failing that, an actor every one of whose voice cues in the scene carries a sound code that belongs to one
  character, by the sound-code step above, takes that character's name. An actor bound to a `c` model is left out of
  this step, since two party rows can share one: Larsa and Lamont share `c16`.
- An actor bound to `c16` is the guest row its `capturebattleid` names; else the one `c16` guest the party holds at
  every story counter value the scene's loading steps allow, by the joins and leaves of the
  [party table](../Party/party-table.md): Lamont (row 10) from story progress 546 until 645, Larsa (row 13) from
  story progress 1640 until 2000. Any other `c16` actor reads its label, as below.
- Any other line without a name reads `no name shown`. A scene subtitle shows no name on screen, so its cell gives
  what the data holds: `movie subtitle` for a line shown on a movie's frames; for a line whose voice cue's actor has
  no game name, that actor's label as the script writes it, marked `(script label)`; else `no name shown`.
- A Japanese label carries an English gloss after a comma: the game's own English name where its text has one, as
  `グラミス (script label, Gramis)`, by line 19 of `alc_z0101` in
  [Archades dialogue](../Menus-And-HUD/archades-dialogue.md); else a plain translation, as
  `平ジャッジ (script label, rank-and-file Judge)`, or a plain reading of an abbreviation the text does not spell out.
- A line whose name is `???` reads `???`: the game prints `???` as that speaker's name at that line. A row lists its
  speakers in line order, each once.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin`⁴, and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin`⁵.
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ADDAA`, `0x002B16D4`, `0x002B52EF` |
| ² | `0x00348EE0` |
| ³ | `0x0026668B`, `0x0026669B`-`0x002666B4` |
| ⁴ | `0x00377B60` |
| ⁵ | `0x00264F90` |

</details>

### Every step

The steps table [`trial-mode-script-steps.tsv`](trial-mode-script-steps.tsv) has one row for each step of every
function of the hundred scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 158,706 rows. That leaves out the 1,668 functions in the spawn groups of the scripts' foes (entry,
spawn and respawn); [Bestiary](../Enemy-Spawning/bestiary.md) reads their entry functions as enemy
placements.

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
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 157,306 |
| empty | 1,400 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

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
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown`, `system message`, `movie subtitle`, or an actor's label marked `(script label)`; `-` for a row without a section 2 line |
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
| `stage` | the stage number, 1 to 100 |
| `foes` | the enemies the stage places ([bestiary](../Enemy-Spawning/bestiary.md), [`enemy-placements.tsv`](../Enemy-Spawning/enemy-placements.tsv)), by name and level, `xN` for more than one |
| `chests` | the number of chests, then each chest actor with its contents and its contents with Treasure Hunter on the leader ([treasure chests](../World-Areas-And-Travel/treasure-chests.md), [`treasure-chest-list.tsv`](../World-Areas-And-Travel/treasure-chest-list.tsv)) |
| `reward` | the package the director gives on clearing the stage and its contents; on stage 100 the achievement, scene and completion screen; `no reward` on a stage that gives none of these |
| `entry` | how the stage is reached: from the Trial Mode start, or by clearing the stage before |
| `between_attempts` | what is the same or different when the stage is played again |

The steps table [`trial-mode-script-steps.tsv`](trial-mode-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test`. A case whose values meet an earlier case's is followed by `not (x = w)` for each such earlier case `w`, so the cell names only the values the case runs on: `x = lte(78); not (x = lt(78))` runs when x is 78. After the enclosing tests come, in listing order, the ways the function leaves before the step: a `return`, a `break` (it leaves its repeat or switch), a `continue` (it skips the rest of the pass) or a `goto` past the step that an earlier test sends the run to, and a repeat that never ends. Each is written as the test that keeps the run on its way to the step: `not (regI0 == 0)` after `if (regI0 == 0) { return; }`, or `not ((test) and (test))` when several tests together lead away. When such a way passes a case that an earlier case overlaps, the item counts only the values that case takes: after `case lt(0x0177)`, a `case lt(0x0182)` that returns gives the item `not (x = lt(0x0182)) or x = lt(0x0177)`, which holds unless 0x0177 <= x < 0x0182. A test inside a repeat counts for the pass the step runs in, and a test the run does not reach counts as one that does not hold. After a repeat that a `return` or a `goto` can also leave, a step reached only when the repeat ends by itself carries `the repeat at line N ended at its own test or a break` (`through a break` for an endless repeat), and a way out of it reads `the repeat at line N was left at line M`. When a `goto`, or a case that runs on into the next case, also leads to the step, only the enclosing tests that hold on every way to the step are written, followed by the same items for the ways that miss it. A function that a `goto` of another function enters at one of its labels runs either from its top or from that label: an item then names where the run came in, `the run began at the top of the function` or `the run entered at line N through a goto from another function`. A `case` or `default` step is a test of its switch, so it runs whenever the switch runs. `unreachable in the listing` marks a step that no path of the function in the decompiled listing reaches; it rests on the labels the listing prints for jump targets, and, for a case whose every value an earlier case already matches, on the case values |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test. A number with a fraction is the listing's print of a 32-bit float to nine significant digits, here and in `condition`: 1.60000002 is the float nearest to 1.6, and 2.36000005e-06 is 2.36000005 times 10 to the power -6 |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

In `arguments` and `condition`, `bitor`, `or` and `and` stand for the listing's `|`, `||` and `&&`. A comparison
`A == B` that is an operand of `bitor` is written in brackets, `(A == B) bitor (C == D)`, because the script evaluates
the comparison first.

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 142 calls with 26 other topics</summary>

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md), [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [npc names](../Characters-And-Objects/npc-names.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00265B60`](../Characters-And-Objects/actor-record.md) (on actor record) |
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | calls | [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) |
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00272CB0`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen)<br>[`0x00272CE0`](../Characters-And-Objects/npc-names.md) (on npc names) |
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00266AD0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00266BD0`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x00268EA0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DB280`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x003DB580`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DBB60`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | is called by | [`0x002679F0`](../EBP-Script-Files/ebp-script-image.md) Actor storage: allocate and initialize records (on ebp script image) |
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x0025D5E0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |

**Movement and pathfinding** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00265FF0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x00268380`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x0026D6D0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |

**Party** (explained on [debug menu](../Engine-Core/debug-menu.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0034D4E0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | calls | [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list)<br>[`0x0026DC40`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003271D0`](../Scripts-And-Script-Commands/party-verbs.md) Party focus: get preferred definition selector (on party verbs)<br>[`0x00327850`](../Party/party-leader.md) Party focus: set preferred definition selector and refresh (on party leader)<br>[`0x00328DB0`](../Party/party-members.md) Party configuration: reconcile runtime roster first three from requested selectors (on party members)<br>[`0x00359C00`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x0035A050`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003601B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x00352190`](mt-bur-omisace-scripts.md) (on mt bur omisace scripts) | calls | [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list)<br>[`0x003170E0`](../Party/party-members.md) Party configuration: add selector07 to25 to available primary index (on party members)<br>[`0x00322350`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) |
| [`0x00352AF0`](mt-bur-omisace-scripts.md) (on mt bur omisace scripts) | calls | [`0x00322350`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003288F0`](../Party/party-members.md) Party configuration: remove selector07 to25 (on party members) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |

**Steam and achievements** (explained on [loading a save](../Saving-Loading-And-Settings/loading-a-save.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00316810`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x002639E0`](../Menus-And-HUD/text-npc-names.md) (on text npc names) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x003FFB00`](archades-scripts.md) (on archades scripts) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |

**Random numbers** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00379CF0`](../Engine-Core/startup-constants.md) (on startup constants) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Saving, loading and settings** (explained on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [party control modes](../Engine-Core/party-control-modes.md), [global state accessors](../Engine-Core/global-state-accessors.md), [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |
| [`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x002EF410`](../World-Areas-And-Travel/chocobos-and-airships.md) Save transition metadata: restore from record (on chocobos and airships)<br>[`0x002EF640`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |
| [`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | is called by | [`0x00582860`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |

**Scripts and script commands** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md), [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | calls | [`0x003DC240`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003DC270`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch)<br>[`0x003DC2A0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | is called by | [`0x0025E4C0`](../Scripts-And-Script-Commands/script-interpreter.md) World actor script vm: interpret bytecode (on script interpreter) |
| [`0x00264D60`](../Menus-And-HUD/aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x00357450`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x0050CDE0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x002673A0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x002E16B0`](../Menus-And-HUD/message-windows.md) (on message windows) | is called by | [`0x0033F950`](../Menus-And-HUD/message-windows.md) (on message windows)<br>[`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x003449A0`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x00345080`](victory-pose-scripts.md) (on victory pose scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x003459C0`](mt-bur-omisace-scripts.md) (on mt bur omisace scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x00349800`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00348DF0`](archades-scripts.md) (on archades scripts) |
| [`0x00349800`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349BF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034A090`](ending-message-scripts.md) (on ending message scripts)<br>[`0x0034A420`](archades-scripts.md) (on archades scripts)<br>[`0x0034A7A0`](archades-scripts.md) (on archades scripts) |
| [`0x00349BF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x0034A090`](ending-message-scripts.md) (on ending message scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x0034A420`](archades-scripts.md) (on archades scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x0034A6D0`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts) | is called by | [`0x0034B760`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x0034BB10`](nalbina-town-scripts.md) (on nalbina town scripts) |
| [`0x0034B760`](nalbina-town-scripts.md) (on nalbina town scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts) |
| [`0x0034B9A0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034BB10`](nalbina-town-scripts.md) (on nalbina town scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts) |
| [`0x0034C030`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034D4E0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034DD90`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034DFA0`](bhujerba-scripts.md) (on bhujerba scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034E0B0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x0034E320`](bhujerba-scripts.md) (on bhujerba scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034E980`](bhujerba-scripts.md) (on bhujerba scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x0034EE20`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00352190`](mt-bur-omisace-scripts.md) (on mt bur omisace scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00352AF0`](mt-bur-omisace-scripts.md) (on mt bur omisace scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**Menus and HUD** (explained on [augments](../Damage-And-Battle-Formulas/augments.md), [zone asset list](../World-Areas-And-Travel/zone-asset-list.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x002AC5F0`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x002639E0`](../Menus-And-HUD/text-npc-names.md) (on text npc names) | is called by | [`0x002AC5F0`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x0029C530`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x0029C530`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0029C530`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x003FFB00`](archades-scripts.md) (on archades scripts) | is called by | [`0x002AC5F0`](../Menus-And-HUD/text-drawing.md) (on text drawing) |

**World, areas and travel** (explained on [changing areas](../World-Areas-And-Travel/changing-areas.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [debug menu](../Engine-Core/debug-menu.md), [script variables](../Scripts-And-Script-Commands/script-variables.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x003C0450`](../Game-Files-And-Data-Tables/menu-map-files.md) (on menu map files)<br>[`0x0057FB00`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) |
| [`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x0057FB00`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0057FB00`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00269A20`](../Saving-Loading-And-Settings/save-data-fields.md) World persistence: import group persistent bank (on save data fields)<br>[`0x00314DC0`](../Saving-Loading-And-Settings/loading-a-save.md) World transition: set active or pending field id (on loading a save) |

</details>
