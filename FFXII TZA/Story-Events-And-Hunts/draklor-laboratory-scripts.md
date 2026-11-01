---
title: "Draklor Laboratory scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Draklor Laboratory that does something a player can observe. It covers
the eighty-three zone scripts, seventy-one with a field entry and twelve without, and the five scene scripts of the
region that have an event id, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `dor_a01` | zone | 66th Floor, field `1008` | 21 | 104 | 14 | 0 |
| `dor_a02` | zone | Rm 6613 West, field `1009` | 13 | 59 | 3 | 1 |
| `dor_a03` | zone | Rm 6613 East, field `1010` | 16 | 76 | 11 | 0 |
| `dor_a04` | zone | Rm 6612 West, field `1011` | 16 | 76 | 11 | 0 |
| `dor_a05` | zone | field `1012`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_a06` | zone | Rm 6611 West, field `1013` | 16 | 76 | 11 | 0 |
| `dor_a07` | zone | Rm 6611 East, field `1014` | 15 | 62 | 3 | 0 |
| `dor_a08` | zone | Rm 6602 West, field `1015` | 15 | 74 | 11 | 0 |
| `dor_a09` | zone | Rm 6601 West, field `1016` | 5 | 5 | 0 | 0 |
| `dor_a10` | zone | Rm 6602 East, field `1017` | 15 | 74 | 11 | 0 |
| `dor_a11` | zone | Rm 6601 East, field `1018` | 15 | 74 | 11 | 0 |
| `dor_a12` | zone | 67th Floor, field `1019` | 19 | 100 | 12 | 0 |
| `dor_a13` | zone | Rm 6711 West, field `1020` | 5 | 5 | 0 | 0 |
| `dor_a14` | zone | Rm 6711 East, field `1021` | 16 | 76 | 11 | 0 |
| `dor_a15` | zone | field `1022`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_a16` | zone | Rm 6703 West, field `1023` | 15 | 74 | 11 | 0 |
| `dor_a17` | zone | Rm 6704 East, field `1024` | 15 | 74 | 11 | 0 |
| `dor_a18` | zone | Rm 6703 East, field `1025` | 14 | 60 | 3 | 0 |
| `dor_a19` | zone | Rm 6702 West, field `1026` | 15 | 74 | 11 | 0 |
| `dor_a20` | zone | Rm 6701 West, field `1027` | 15 | 74 | 11 | 0 |
| `dor_a21` | zone | Rm 6702 East, field `1028` | 15 | 74 | 11 | 0 |
| `dor_a22` | zone | field `1029`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_a23` | zone | 68th Floor, field `1030` | 17 | 75 | 9 | 0 |
| `dor_a24` | zone | 69th Floor, field `1031` | 7 | 13 | 0 | 0 |
| `dor_b01` | zone | Energy Transitarium, field `286` | 19 | 35 | 6 | 0 |
| `dor_c01` | zone | 66th Floor, field `1036` | 44 | 142 | 17 | 0 |
| `dor_c02` | zone | Rm 6613 West, field `1037` | 15 | 62 | 3 | 1 |
| `dor_c03` | zone | Rm 6613 East, field `1038` | 20 | 83 | 14 | 0 |
| `dor_c04` | zone | Rm 6612 West, field `1039` | 16 | 76 | 11 | 0 |
| `dor_c05` | zone | field `1040`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_c06` | zone | Rm 6611 West, field `1041` | 16 | 76 | 11 | 0 |
| `dor_c07` | zone | Rm 6611 East, field `1042` | 16 | 76 | 11 | 0 |
| `dor_c08` | zone | Rm 6602 West, field `1043` | 9 | 43 | 3 | 0 |
| `dor_c09` | zone | Rm 6601 West, field `1044` | 9 | 43 | 3 | 0 |
| `dor_c10` | zone | Rm 6602 East, field `1045` | 9 | 43 | 3 | 0 |
| `dor_c11` | zone | Rm 6601 East, field `1046` | 15 | 74 | 11 | 0 |
| `dor_c12` | zone | 70th Floor, field `1047` | 28 | 123 | 13 | 5 |
| `dor_c13` | zone | Rm 7002 West, field `1048` | 15 | 74 | 11 | 0 |
| `dor_c14` | zone | Rm 7001 West, field `1049` | 15 | 74 | 11 | 0 |
| `dor_c15` | zone | Rm 7002 East, field `1050` | 18 | 79 | 13 | 0 |
| `dor_c16` | zone | field `1051`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_d01` | zone | 67th Floor, field `1054` | 37 | 123 | 16 | 0 |
| `dor_d02` | zone | Rm 6711 West, field `1055` | 14 | 52 | 6 | 0 |
| `dor_d03` | zone | Rm 6711 East, field `1056` | 16 | 76 | 11 | 0 |
| `dor_d04` | zone | field `1057`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_d05` | zone | Rm 6703 West, field `1058` | 15 | 74 | 11 | 0 |
| `dor_d06` | zone | Rm 6704 East, field `1059` | 23 | 114 | 13 | 5 |
| `dor_d07` | zone | Rm 6703 East, field `1060` | 9 | 43 | 3 | 0 |
| `dor_d08` | zone | Rm 6702 West, field `1061` | 15 | 74 | 11 | 0 |
| `dor_d09` | zone | Rm 6701 West, field `1062` | 15 | 74 | 11 | 0 |
| `dor_d10` | zone | Rm 6702 East, field `1063` | 15 | 74 | 11 | 0 |
| `dor_d11` | zone | field `1064`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_e01` | zone | 68th Floor, field `1067` | 48 | 155 | 18 | 0 |
| `dor_e02` | zone | Rm 6814 West, field `1068` | 16 | 76 | 11 | 0 |
| `dor_e03` | zone | Rm 6814 East, field `1069` | 21 | 57 | 3 | 0 |
| `dor_e04` | zone | Rm 6813 West, field `1070` | 14 | 61 | 3 | 1 |
| `dor_e05` | zone | Rm 6813 East, field `1071` | 11 | 47 | 3 | 0 |
| `dor_e06` | zone | Rm 6812 West, field `1072` | 10 | 45 | 3 | 0 |
| `dor_e07` | zone | Rm 6812 East, field `1073` | 16 | 76 | 11 | 0 |
| `dor_e08` | zone | Rm 6811 West, field `1074` | 10 | 45 | 3 | 0 |
| `dor_e09` | zone | Rm 6811 East, field `1075` | 16 | 63 | 3 | 1 |
| `dor_e10` | zone | Rm 6804 West, field `1076` | 15 | 74 | 11 | 0 |
| `dor_e11` | zone | Rm 6803 West, field `1077` | 15 | 74 | 11 | 0 |
| `dor_e12` | zone | Rm 6804 East, field `1078` | 15 | 74 | 11 | 0 |
| `dor_e13` | zone | Rm 6803 East, field `1079` | 15 | 74 | 11 | 0 |
| `dor_e14` | zone | Rm 6802 West, field `1080` | 10 | 44 | 3 | 0 |
| `dor_e15` | zone | Rm 6801 West, field `1081` | 20 | 83 | 15 | 0 |
| `dor_e16` | zone | Rm 6802 East, field `1082` | 9 | 43 | 3 | 0 |
| `dor_e17` | zone | Rm 6801 East, field `1083` | 15 | 74 | 11 | 0 |
| `dor_f01` | zone | 69th Floor, field `1086` | 8 | 15 | 0 | 0 |
| `dor_f02` | zone | field `1087`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_f03` | zone | Rm 6912 East, field `1088` | 6 | 7 | 0 | 0 |
| `dor_f04` | zone | Rm 6911 West, field `1089` | 6 | 7 | 0 | 0 |
| `dor_f05` | zone | field `1090`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_f06` | zone | Rm 6904 West, field `1091` | 11 | 36 | 8 | 0 |
| `dor_f07` | zone | field `1092`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_f08` | zone | field `1093`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_f09` | zone | Rm 6903 East, field `1094` | 5 | 5 | 0 | 0 |
| `dor_f10` | zone | Rm 6902 West, field `1095` | 5 | 5 | 0 | 0 |
| `dor_f11` | zone | Rm 6901 West, field `1096` | 11 | 36 | 8 | 0 |
| `dor_f12` | zone | field `1097`, which has no zone-script entry | 1 | 1 | 0 | 0 |
| `dor_f13` | zone | Rm 6901 East, field `1098` | 11 | 36 | 8 | 0 |
| `dor_z01` | zone | field `854` | 8 | 19 | 1 | 1 |
| `dor_a0100` | scene | event `179` | 17 | 115 | 6 | 0 |
| `dor_b0100` | scene | event `176` | 26 | 273 | 12 | 0 |
| `dor_b0101` | scene | event `177` | 41 | 471 | 12 | 0 |
| `dor_c1200` | scene | event `175` | 21 | 147 | 1 | 0 |
| `dor_z0100` | scene | event `178` | 18 | 126 | 19 | 0 |

The 70th Floor (`dor_c12`) and Rm 6704 East (`dor_d06`) carry the five helper actors that many zone scripts share: the
crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message
helper `イベント特殊効果画面`; `dor_a02`, `dor_c02`, `dor_e04`, `dor_e09` and `dor_z01` carry the key-item and message helper
alone. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no
rows here; the Shared helpers column counts them.

The scene `dor_z0100` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Draklor
Laboratory scenes](draklor-laboratory-scenes.md).

Twelve more zone scripts ship under `plan_map/dor_*`: `dor_a05`, `dor_a15`, `dor_a22`, `dor_c05`, `dor_c16`,
`dor_d04`, `dor_d11`, `dor_f02`, `dor_f05`, `dor_f07`, `dor_f08` and `dor_f12`. Each holds one actor, `Map_Director`,
whose `init` returns at once. Their fields, 1012, 1022, 1029, 1040, 1051, 1057, 1064, 1087, 1090, 1092, 1093 and 1097,
have map names (Rm 6612 East, Rm 6704 West and so on) but no zone-script entry, and no `mapjump` of the `us` scripts
names them, so no field loads these scripts.

Each of the twelve has a row in the script list above, with the place
`field <id>, which has no zone-script entry`, and its steps in the steps table; it has no row in the main table,
since `Map_Director.init` makes none of the calls the table reads.

### What the scripts do

- The region has two sets of floor maps. Fields 1008 to 1031 (`dor_a01` to `dor_a24`) hold the 66th to 69th Floors and
  their rooms; fields 1036 to 1098 (`dor_c01` to `dor_f13`) hold the 66th to 70th Floors and theirs. The Energy
  Transitarium (`dor_b01`) is field 286 and `dor_z01` is field 854. Archades' `alc_c01` (field 756) jumps into the
  66th Floor, field 1008, entrance 3 ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).
- 66th Floor (`dor_a01`): `EventDirector.main` loads scene `dor_a0100` (event 179) and writes 3350. Touching `死体発見レクト`
  writes 3355, the bodies found, with a line from each party member, from Vaan's "What happened here?" to Penelo's
  "What happened!?". The door `閉じた扉` turns the party back: "We've come this far. No turnin' back now."
- Lifts stand on the 66th, 67th and 68th Floors of the first set (`dor_a01`, `dor_a12`, `dor_a23`) and on the 66th,
  67th, 68th and 70th Floors of the second (`dor_c01`, `dor_d01`, `dor_e01`, `dor_c12`).
- The north lift asks "Select destination" and its `北ＥＶ実処理` functions, run below story counter 3400, jump to the floor
  the choice stores. The south lift jumps to the 70th Floor (field 1047) or the 68th Floor (field 1067, entrance 34);
  its lines include "A Lab Access Card is needed to operate this lift."
- The floors of the second set open into their rooms: `dor_c01` has seven room doors, `dor_d01` five, `dor_e01` nine
  and `dor_c12` one, each showing "Access to this room appears to be restricted." and jumping into the room. In both
  sets a room's door `扉.talk` jumps back to the field the party came from (`lastmap()`).
- Fifty-one rooms hold the bulkhead switch `切り替え.talk`: "This device controls the lab security bulkheads. The blue
  bulkheads are currently closed." Opening the blue bulkheads closes the red ones, and the other way round. The
  researcher `NPC_LABO_0` stands in thirty-seven rooms and explains them: "The bulkheads, red and blue, are activated
  alternately. When one opens, the other locks."
- 67th Floor of the first set (`dor_a12`): `door_cid.talk` jumps to `dor_z01`, field 854. There `常駐監督.main` loads
  scene `dor_z0100` (event 178), writes 3400 and jumps to the 67th Floor of the second set, field 1054, entrance 2.
  The scene gives the Lab Access Card and the location map Draklor Laboratories.
- 70th Floor (`dor_c12`): `EventDirector.main` loads scene `dor_c1200` (event 175) and writes 3440. The map exit
  `__MJ_CTRL000` leads to the Energy Transitarium (field 286), and `door11_in` to Rm 7002 East (field 1050).
- Energy Transitarium (`dor_b01`): `EventDirector.main` loads scenes `dor_b0100` and `dor_b0101` (events 176 and 177),
  opens the boss gauge, removes every foe after the fight, writes 4000 and jumps to field 922, entrance 0, which the
  map name table names `bhm_y01` (Sky Fortress Bahamut). Its exit `__MJ_CTRL000` leads back to the 70th Floor.
- The director `HED_DIREC` keeps the map icons: on the seven floors with lifts its `init` sets, releases and tests
  flags `0x0068` to `0x006E` and the floors' map-icon flags, and in fifty-one rooms its `main` sets and tests map-icon
  flags such as `0x0126` (66th Floor) ([story flag ids](story-flag-ids.md)).
- Treasure chests: two in the Energy Transitarium, three each in Rm 6613 East (`dor_c03`) and Rm 6711 West
  (`dor_d02`), two in Rm 7002 East (`dor_c15`) and four in Rm 6801 West (`dor_e15`).
- The 69th Floor of the second set (`dor_f01`) and its rooms have no lift, door or switch row; `dor_f06`, `dor_f11`
  and `dor_f13` hold the researcher.

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

The steps table [`draklor-laboratory-script-steps.tsv`](draklor-laboratory-script-steps.tsv) has one row for each step
of every function of the eighty-eight scripts, in the order the function runs them: each call, request, store, branch,
loop, case and return. It has 112,889 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `dor_a01` | 3,778 | `dor_d10` | 2,021 |
| `dor_a02` | 685 | `dor_e01` | 2,573 |
| `dor_a03` | 2,029 | `dor_e02` | 2,110 |
| `dor_a04` | 2,110 | `dor_e03` | 806 |
| `dor_a06` | 2,034 | `dor_e04` | 698 |
| `dor_a07` | 779 | `dor_e05` | 672 |
| `dor_a08` | 2,042 | `dor_e06` | 750 |
| `dor_a09` | 9 | `dor_e07` | 2,110 |
| `dor_a10` | 2,021 | `dor_e08` | 669 |
| `dor_a11` | 2,021 | `dor_e09` | 708 |
| `dor_a12` | 3,110 | `dor_e10` | 1,965 |
| `dor_a13` | 9 | `dor_e11` | 1,965 |
| `dor_a14` | 2,131 | `dor_e12` | 1,938 |
| `dor_a16` | 1,965 | `dor_e13` | 1,938 |
| `dor_a17` | 1,959 | `dor_e14` | 686 |
| `dor_a18` | 688 | `dor_e15` | 2,138 |
| `dor_a19` | 2,042 | `dor_e16` | 661 |
| `dor_a20` | 2,042 | `dor_e17` | 2,021 |
| `dor_a21` | 2,042 | `dor_f01` | 90 |
| `dor_a23` | 1,406 | `dor_f03` | 12 |
| `dor_a24` | 87 | `dor_f04` | 12 |
| `dor_b01` | 510 | `dor_f06` | 1,369 |
| `dor_c01` | 2,455 | `dor_f09` | 9 |
| `dor_c02` | 700 | `dor_f10` | 9 |
| `dor_c03` | 2,102 | `dor_f11` | 1,369 |
| `dor_c04` | 2,110 | `dor_f13` | 1,369 |
| `dor_c06` | 2,034 | `dor_z01` | 75 |
| `dor_c07` | 2,029 | `dor_a0100` | 994 |
| `dor_c08` | 682 | `dor_b0100` | 2,895 |
| `dor_c09` | 682 | `dor_b0101` | 2,877 |
| `dor_c10` | 661 | `dor_c1200` | 1,050 |
| `dor_c11` | 2,021 | `dor_z0100` | 1,801 |
| `dor_c12` | 1,713 | `dor_a05` | 1 |
| `dor_c13` | 2,042 | `dor_a15` | 1 |
| `dor_c14` | 2,042 | `dor_a22` | 1 |
| `dor_c15` | 2,071 | `dor_c05` | 1 |
| `dor_d01` | 2,015 | `dor_c16` | 1 |
| `dor_d02` | 823 | `dor_d04` | 1 |
| `dor_d03` | 2,131 | `dor_d11` | 1 |
| `dor_d05` | 1,965 | `dor_f02` | 1 |
| `dor_d06` | 2,078 | `dor_f05` | 1 |
| `dor_d07` | 578 | `dor_f07` | 1 |
| `dor_d08` | 2,042 | `dor_f08` | 1 |
| `dor_d09` | 2,042 | `dor_f12` | 1 |

The twelve zone scripts no field loads, last in the table, have one step each: the `return` of `Map_Director.init`.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Draklor Laboratory has 108 such rows.

Some actors run another actor's code: `NPC02` in `dor_a01` starts at the same place as `NPC01` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 288 of these rows, in
forty-nine of the scripts; `dor_a01` has the most, 22.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 103,831 |
| empty | 9,056 |
| `does not ship`, with the fact | 2 |

The two `does not ship` rows are `motionread` calls in `EventDirector.init` of `dor_a07` and `dor_a18`, whose motion
files `dor_a07.mot` and `dor_a18.mot` are not in the archive. A row whose `resolution` cell is empty gives the step as
the listing writes it: the verb, and the arguments as the script writes them (`-` for a verb that takes none). Its
`addresses`, `timing` and `sync` cells carry what they give for the step, for example the variable that holds the
standard motion `stdmotionplay` plays, or the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `dor_a0100` (event `179`), `監督.main` jumps over its
music block, files `BGM監督.get_music_number` on channel 1 and waits until it ends, hides the HUD, waits 6 frames and
readies movie 14. It plays the movie, files `movieSkip監督.Skip監視`, `ムービー用セリフ.テキスト表示` and `BGM監督.cut_movie` without
waiting, waits until the skip watcher ends and the movie ends, and closes message windows 0 to 7.

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
is shown is written `[value]`.

The script list [`draklor-laboratory-script-list.tsv`](draklor-laboratory-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id; a zone script that no field loads reads `field <id>, which has no zone-script entry` |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`draklor-laboratory-script-steps.tsv`](draklor-laboratory-script-steps.tsv) has one row per step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message
  helpers, described once.
- [Draklor Laboratory scenes](draklor-laboratory-scenes.md) - the five scenes these scripts load.
- [Archades scripts](archades-scripts.md) - the city whose `alc_c01` leads into the 66th Floor.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
