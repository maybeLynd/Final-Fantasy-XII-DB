---
title: "Pharos - First Ascent scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00352EA0, 0x00353390, 0x00354000, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of the `rbl` scripts that does something a player can observe. It covers the
thirty-one zone scripts and the ten scene scripts of the group, from `plan_master/us`. Eleven maps are in Pharos -
First Ascent, eight in Pharos - Second Ascent, nine in Pharos - Subterra and three in Pharos - Third Ascent:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `rbl_a01` | zone | The Wellspring, field `1101` | 41 | 177 | 18 | 5 |
| `rbl_a02` | zone | Horizon's Break, field `1102` | 27 | 137 | 7 | 5 |
| `rbl_a03` | zone | The Reach, field `1103` | 48 | 216 | 25 | 5 |
| `rbl_a04` | zone | Reach of the Damned, field `1104` | 29 | 145 | 7 | 5 |
| `rbl_a05` | zone | Reach of the Occult, field `1105` | 28 | 148 | 5 | 5 |
| `rbl_b01` | zone | Wellspring Labyrinth, field `1111` | 50 | 166 | 24 | 1 |
| `rbl_c01` | zone | Dunes of Profaning Wind, field `1113` | 17 | 41 | 4 | 0 |
| `rbl_c02` | zone | Blackrock Vault, field `1114` | 9 | 52 | 2 | 0 |
| `rbl_d01` | zone | Wellspring Ravel - 1st Flight, field `1115` | 56 | 203 | 16 | 0 |
| `rbl_d02` | zone | Wellspring Ravel - 2nd Flight, field `1116` | 32 | 88 | 10 | 0 |
| `rbl_e01` | zone | Wellspring Ravel - 3rd Flight, field `1118` | 43 | 139 | 13 | 0 |
| `rbl_e02` | zone | Wellspring Ravel - 4th Flight, field `1119` | 29 | 84 | 6 | 0 |
| `rbl_f01` | zone | Marsh of Profaning Wind, field `1121` | 10 | 20 | 3 | 0 |
| `rbl_f02` | zone | Horizon's Cusp, field `1122` | 31 | 148 | 10 | 0 |
| `rbl_g01` | zone | Penumbra - Interior, field `1123` | 29 | 122 | 8 | 0 |
| `rbl_g02` | zone | Penumbra - North, field `1124` | 56 | 188 | 19 | 0 |
| `rbl_g03` | zone | Penumbra - South, field `1125` | 44 | 157 | 13 | 0 |
| `rbl_h01` | zone | Umbra - Interior, field `1126` | 29 | 121 | 7 | 0 |
| `rbl_h02` | zone | Umbra - North, field `1127` | 45 | 159 | 15 | 0 |
| `rbl_h03` | zone | Umbra - South, field `1128` | 55 | 178 | 19 | 0 |
| `rbl_i01` | zone | Abyssal - Interior, field `1129` | 29 | 121 | 7 | 0 |
| `rbl_i02` | zone | Abyssal - North, field `1130` | 58 | 188 | 22 | 0 |
| `rbl_i03` | zone | Abyssal - South, field `1131` | 59 | 190 | 23 | 0 |
| `rbl_j01` | zone | Cleft of Profaning Wind, field `1132` | 14 | 24 | 6 | 0 |
| `rbl_j02` | zone | The Bounds of Truth, field `1133` | 37 | 168 | 21 | 0 |
| `rbl_k01` | zone | Station of Banishment, field `1134` | 34 | 102 | 16 | 0 |
| `rbl_l01` | zone | Station of Suffering, field `1136` | 37 | 131 | 15 | 1 |
| `rbl_m01` | zone | Station of Ascension, field `1138` | 38 | 119 | 18 | 0 |
| `rbl_n01` | zone | Spire Ravel - 1st Flight, field `1140` | 66 | 205 | 31 | 1 |
| `rbl_n02` | zone | Spire Ravel - 2nd Flight, field `1141` | 74 | 200 | 38 | 0 |
| `rbl_q01` | zone | Empyrean Ravel, field `1143` | 42 | 178 | 15 | 5 |
| `rbl_c0100` | scene | event `376` | 19 | 81 | 0 | 0 |
| `rbl_c0101` | scene | event `377` | 20 | 77 | 0 | 0 |
| `rbl_f0100` | scene | event `392` | 14 | 61 | 0 | 0 |
| `rbl_f0101` | scene | event `126` | 13 | 57 | 0 | 0 |
| `rbl_g0200` | scene | event `129` | 11 | 68 | 0 | 0 |
| `rbl_g0201` | scene | event `136` | 13 | 47 | 0 | 0 |
| `rbl_j0100` | scene | event `127` | 13 | 59 | 0 | 0 |
| `rbl_j0101` | scene | event `128` | 15 | 55 | 0 | 0 |
| `rbl_n0200` | scene | event `378` | 14 | 58 | 0 | 0 |
| `rbl_q0100` | scene | event `379` | 17 | 143 | 15 | 0 |

The Wellspring, Horizon's Break, The Reach, Reach of the Damned, Reach of the Occult and Empyrean Ravel carry the five
helper actors that many zone scripts share: the crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`,
`saveactor`) and the key-item and message helper `イベント特殊効果画面`; Wellspring Labyrinth, Station of Suffering and Spire
Ravel - 1st Flight carry the key-item and message helper alone. Their functions are described once on [Shared
zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

They Who Thirst Not (Pharos - First Ascent, field `522`) is on [Ridorana Cataract
scripts](ridorana-cataract-scripts.md); the Womb of the Sun-cryst and Heaven's Challenge (Pharos - Third Ascent) and
Hell's Challenge (Pharos - Subterra) are on [Pharos - Third Ascent scripts](pharos-third-ascent-scripts.md).

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Pharos -
First Ascent scenes](pharos-first-ascent-scenes.md).

### What the scripts do

- Entering the Pharos: The Wellspring's `常駐ディレクター.main` sets flag `0x004A`, the location map's exits between Pharos -
  First Ascent and Ridorana Cataract, and loads scene `ttl_z0008` (event 358); one exit of The Wellspring leads to
  They Who Thirst Not, field `522`.
- Entering the Pharos: the same function of The Reach sets `0x007C` (between Pharos - First Ascent and Pharos - Second
  Ascent), of Penumbra - Interior `0x007D` (Pharos - First Ascent and Pharos - Subterra) and of Spire Ravel - 1st
  Flight `0x007B` (Pharos - Second Ascent and Pharos - Third Ascent), each loading `ttl_z0008`.
- Wellspring Ravel - 1st Flight's `常駐ディレクター.main` writes 5320, used the Pharos teleporter.
- The seals of The Wellspring: the altars `map_gmk_s`, `map_gmk_n` and `map_gmk_e` each take a Black Orb ("The beasts
  here dwelling oft possess black orbs. Herewith approach, by thine offering sealed way to open.") and set flag
  `0x00E4`, a map icon in Wellspring Labyrinth: "The third seal has been broken. The Seal of Night loses its power."
- The orbs (`o_tama`, `tama01` to `tama05`) of Wellspring Labyrinth and of Penumbra, Umbra and Abyssal - North and
  South give Black Orbs.
- In Subterra the pedestals `daiza_w` and `daiza_e` take 1, 5 or 10 Black Orbs ("The chamber brightens. The pedestal
  appears full.", "The pedestal swallows the black orbs. They are lost. The number of orbs was too great.").
- The three watchers: the doors before them say "Ahead the watcher waits, first of three. Ye without wisdom, return
  whence you came." (Wellspring Labyrinth, to Dunes of Profaning Wind), "second of three. Ye without strength"
  (Horizon's Cusp, to Marsh of Profaning Wind) and "third of three. Ye who crave wealth" (The Bounds of Truth, to
  Cleft of Profaning Wind).
- The watchers' fights: in Dunes and Marsh of Profaning Wind `常駐ディレクター.main` loads the two scenes of the fight, and
  `ボス監視.ボスバトルコード`, requested by touching `map_boss_rect`, shows the boss gauge, removes the foes, loads `pos_z0000`
  (event 427) and has `Map_Director.map_return2rbl` jump to Blackrock Vault or Horizon's Cusp.
- In Cleft of Profaning Wind `常駐ディレクター.main` shows the boss gauge, removes the foes, loads `rbl_j0100`, `rbl_j0101`
  and `pos_z0000` and jumps back to The Bounds of Truth.
- Penumbra - North's `常駐ディレクター.main` shows the boss gauge, removes the foes and loads `rbl_g0200`, `rbl_g0201` and
  `pos_z0000`. Blackrock Vault's `Map_Director.main` shows "The magicks binding the way stone fade."
- The four offerings: the statues of The Reach (`statusgmk_nw_戦`, `statusgmk_sw_魔`, `statusgmk_ne_具`,
  `statusgmk_se_技`) ask the party to make an offering of its Steel, Magicks, Wealth or Knowledge ("Steel avails you
  not."); each sets its own flag, `0x0152`, `0x0153`, `0x0151` or `0x0154`, with `0x0146` and `0x0147`.
- The statues of The Bounds of Truth set the same flags with `0x0155`, and request `ele.エレベーター解放`, which shows "Your
  abilities are again your own." and sets `0x0072` and `0x0147`; `Map_Director.init` of The Reach and of The Bounds of
  Truth sets and releases these flags as the map opens.
- The daises: the dais (`ele.talk`) of The Wellspring, Horizon's Break, The Reach, Reach of the Damned, Reach of the
  Occult, Wellspring Ravel - 1st and 3rd Flight, Horizon's Cusp, the three Subterra interiors, The Bounds of Truth,
  Spire Ravel - 2nd Flight and Empyrean Ravel tests story counter above 6,000 and carries the party between the dais
  maps; most of them set those maps' icons.
- In The Wellspring and the Subterra interiors the dais shows "The dais returns to its original floor under power of
  some mysterious force.", elsewhere "Nothing happens. This chamber appears to be affecting the dais."
- The Bounds of Truth's `Map_Director.map_ele_ev_read` requests `SAKIYOMI_ev_dgl_a0100` and `SAKIYOMI_ev_dgl_a0101`,
  which load scenes `dgl_a0100` (event 383) and `dgl_a0101` (event 384).
- The teleport devices (`warp`, `warp_bef`) of The Wellspring, The Reach, Reach of the Occult, Wellspring Ravel - 1st
  Flight, Horizon's Cusp and Spire Ravel - 1st Flight jump to the field a script variable holds ("By this, return ye
  to the Wellspring. By other means, return ye back to this place.").
- `map_warp_hintflg_ctrl.map_warp_hintflg_set` sets the map icons `0x00DB` (The Wellspring), `0x00DE` (The Reach) and
  `0x010F` (Reach of the Occult).
- In Spire Ravel the devices `s_warp_*` carry the party between points of the 1st and 2nd Flights.
- The maps: `大灯台下層地図` in Wellspring Labyrinth gives Pharos: First Ascent with system message 126, `大灯台中層地図` in Station
  of Suffering gives Pharos: Second Ascent with message 125 and `大灯台上層地図` in Spire Ravel - 1st Flight gives Pharos:
  Third Ascent with message 124 ("Your location map for this area is complete!"); each sets a Bank512 second-half
  flag, `0x0019`, `0x0018` or `0x0017`.
- The summit: Spire Ravel - 2nd Flight's `SAKIYOMI_ev_rbl_n0200.init` loads scene `rbl_n0200` (event 378). In Empyrean
  Ravel, below story counter 5,370, `Read_Event_RBL_Q01.init` loads scene `rbl_q0100` (event 379) and touching
  `イベント起動` writes 5370, after To the summit; the device `常駐イベント.転送装置`, requested by `warp.talk`, jumps to Womb of the
  Sun-cryst, field `666`.
- Marks: `wanted_kansi.main` of Penumbra, Umbra and Abyssal - Interior removes the foes of a group; Station of
  Ascension's `hunt_kansi.main` gives the Vile Trophy and removes the foes of a group. The Wellspring, Horizon's
  Break, The Reach, Reach of the Damned, Reach of the Occult and Empyrean Ravel:
  `choco_sum_ctrl_murasawa.sumcho_byebye`, requested by the teleport, releases flag `0x0073`, riding a chocobo.
- The pillars (`kotobashira`) of most maps show their inscriptions ("Ancient letters hang in an effulgent glow."),
  from "This tower, wrought by Hands Undying, Heaven-bound path." in The Wellspring to "To Heaven's last height you
  now ascend." in Empyrean Ravel.
- The Wellspring, Wellspring Labyrinth, Wellspring Ravel - 1st to 4th Flight, Horizon's Cusp, Penumbra - North and
  South, Umbra - North and South, Abyssal - North and South, Cleft of Profaning Wind, The Bounds of Truth, Station of
  Banishment, Station of Suffering, Station of Ascension, Spire Ravel - 1st and 2nd Flight and Empyrean Ravel hold 2,
  7, 7, 4, 6, 2, 4, 5, 3, 4, 6, 9, 9, 4, 4, 9, 7, 10, 5, 6 and 4 treasure chests, 117 in all.

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

- The speaker is the second name of each pair the actor's `setnpcname` calls name in `us` `npcdic.bin`. The
  message window opener `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`pharos-first-ascent-script-steps.tsv`](pharos-first-ascent-script-steps.tsv) has one row for each
step of every function of the forty-one scripts, in the order the function runs them: each call, request, store,
branch, loop, case and return. It has 101,284 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `rbl_a01` | 3,169 | `rbl_i01` | 2,456 |
| `rbl_a02` | 2,153 | `rbl_i02` | 4,208 |
| `rbl_a03` | 5,189 | `rbl_i03` | 4,323 |
| `rbl_a04` | 2,423 | `rbl_j01` | 566 |
| `rbl_a05` | 2,255 | `rbl_j02` | 4,817 |
| `rbl_b01` | 3,200 | `rbl_k01` | 1,959 |
| `rbl_c01` | 706 | `rbl_l01` | 2,204 |
| `rbl_c02` | 603 | `rbl_m01` | 2,249 |
| `rbl_d01` | 3,891 | `rbl_n01` | 3,915 |
| `rbl_d02` | 2,553 | `rbl_n02` | 5,593 |
| `rbl_e01` | 3,570 | `rbl_q01` | 2,316 |
| `rbl_e02` | 2,280 | `rbl_c0100` | 1,292 |
| `rbl_f01` | 310 | `rbl_c0101` | 1,242 |
| `rbl_f02` | 2,588 | `rbl_f0100` | 867 |
| `rbl_g01` | 2,490 | `rbl_f0101` | 729 |
| `rbl_g02` | 4,398 | `rbl_g0200` | 1,114 |
| `rbl_g03` | 3,748 | `rbl_g0201` | 459 |
| `rbl_h01` | 2,456 | `rbl_j0100` | 1,034 |
| `rbl_h02` | 3,811 | `rbl_j0101` | 561 |
| `rbl_h03` | 4,110 | `rbl_n0200` | 1,708 |
| | | `rbl_q0100` | 1,769 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Pharos - First Ascent has 204 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has none.

The `resolution` column says how far each step is known:

| Resolution | Steps |
|---|---:|
| `resolved` | 91,480 |
| what was searched, when no page yet gives what the arguments name | 9,803 |
| `does not ship`, with the fact | 1 |

The one `does not ship` row is a `motionread` call in `rbl_c0101` that reads entry 2 of `rbl_c0101.mot`, an empty
entry. When no page yet gives what a step's arguments name, the cell says what was searched, for example the standard
motion table that `stdmotionplay` reads, or a verb that no page describes yet.

A scene reads from top to bottom in its functions. In `rbl_c0100` (event `376`), `ＡＤ.s01_つなぎ` starts scene cut 0, sets
`scratch1_var_2` to 0, files `EventLightActor.setEventLight` and files `cut1_つなぎ` on eleven actors at once, among them
the camera, the event sound and music and the four party members. It waits for the event sound and the four party
members, then 20 frames more.

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

The script list [`pharos-first-ascent-script-list.tsv`](pharos-first-ascent-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`pharos-first-ascent-script-steps.tsv`](pharos-first-ascent-script-steps.tsv) has one row per step:

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
- [Pharos - First Ascent scenes](pharos-first-ascent-scenes.md) - the ten scenes these scripts load.
- [Ridorana Cataract scripts](ridorana-cataract-scripts.md) - Ridorana Cataract and They Who Thirst Not, the way into
  the Pharos.
- [Pharos - Third Ascent scripts](pharos-third-ascent-scripts.md) - the Womb of the Sun-cryst, Heaven's Challenge and
  Hell's Challenge, and the scenes `dgl_a0100` and `dgl_a0101` loaded in The Bounds of Truth.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
