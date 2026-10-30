---
title: "Archades scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Archades that does something a player can observe. It covers the
seventeen zone scripts and the ten scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `alc_a01` | zone | Grand Arcade, field `635` | 46 | 329 | 20 | 0 |
| `alc_a02` | zone | Highgarden Terrace, field `636` | 20 | 109 | 8 | 1 |
| `alc_b03` | zone | Molberry, field `640` | 40 | 337 | 29 | 1 |
| `alc_b04` | zone | Trant, field `641` | 34 | 243 | 22 | 1 |
| `alc_b05` | zone | Charlotte's Magickery, field `642` | 15 | 100 | 8 | 1 |
| `alc_b06` | zone | Bulward's Technicks, field `643` | 18 | 111 | 9 | 1 |
| `alc_c01` | zone | Tsenoble, field `756` | 46 | 325 | 23 | 5 |
| `alc_e01` | zone | Aerodrome, field `794` | 34 | 204 | 20 | 5 |
| `alc_f01` | zone | Nilbasse, field `745` | 39 | 298 | 26 | 1 |
| `alc_f02` | zone | Rienna, field `746` | 35 | 279 | 26 | 1 |
| `alc_f03` | zone | Vint's Armaments, field `747` | 17 | 112 | 9 | 1 |
| `alc_f04` | zone | Granch's Requisites, field `748` | 16 | 98 | 8 | 1 |
| `alc_f05` | zone | Lebleu's Gambits, field `749` | 17 | 104 | 8 | 1 |
| `alc_z01` | zone | `alc_z01`, field `866` | 7 | 9 | 1 | 0 |
| `alc_z02` | zone | `alc_z02`, field `867` | 7 | 9 | 1 | 0 |
| `alc_z03` | zone | `alc_z03`, field `868` | 7 | 9 | 1 | 0 |
| `alc_z04` | zone | `alc_z04`, field `869` | 7 | 9 | 1 | 0 |
| `alc_a0100` | scene | event `307` | 18 | 81 | 2 | 0 |
| `alc_a0280` | scene | event `731` | 11 | 112 | 18 | 0 |
| `alc_b0400` | scene | event `306` | 23 | 213 | 6 | 0 |
| `alc_c0180` | scene | event `732` | 12 | 116 | 12 | 0 |
| `alc_z0100` | scene | event `300` | 13 | 106 | 35 | 0 |
| `alc_z0101` | scene | event `301` | 12 | 164 | 45 | 0 |
| `alc_z0102` | scene | event `303` | 12 | 67 | 6 | 0 |
| `alc_z0103` | scene | event `304` | 18 | 158 | 16 | 0 |
| `alc_z0104` | scene | event `305` | 36 | 383 | 16 | 0 |
| `alc_z0200` | scene | event `302` | 26 | 215 | 12 | 0 |

Tsenoble and the Aerodrome carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; Highgarden Terrace, Molberry, Trant, Nilbasse, Rienna and the five shops carry the key-item and message
helper alone. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have
no rows here; the Shared helpers column counts them.

The map name table gives fields `866` to `869` their codes, `alc_z01` to `alc_z04`, as their names. Their zone scripts
play the scenes of the imperial court.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Archades
scenes](archades-scenes.md).

### What the scripts do

- Trant: at story counter 3,250 `EventDirector.main` loads scene `alc_b0400` (event 306), writes 3250, after slipping
  into the imperial capital, and sets flag `0x0135`, the location map's exits between Archades and Old Archades;
  touching `RECT_SPLIT_BAL` writes 3253, met Reddas's man in the capital, as Balthier leaves ("We go our separate ways
  here, Vaan."). One exit of Trant leads to Alley of Muted Sighs (Old Archades), field `762`.
- Nilbasse: below story counter 3,255 `SAKIYOMI_ev_alc_a0280` loads scene `alc_a0280` (event 731), in which Jules
  meets the party at the cab.
- Nilbasse: Jules (`NPC_JULES.talk`) and the Cab Guide (`NPC_タクシー受付.talk`) test the counter below 3,255 and write
  3255, Reddas's man caused trouble in the capital; Jules sets the map icon `0x00C3` (Nilbasse), and the Cab Guide
  sets `0x00C3` and `0x00C2` (Tsenoble): "Only those with [value] or more chops may ride this cab, boy." The cab
  (`map_ダミーＰＣ.タクシー乗る`) runs between Nilbasse and Tsenoble.
- The chops: the townsfolk of Molberry, Trant, Nilbasse and Rienna (`NPC_WEB_*`) ask for and settle each other's
  errands.
- Of those functions, 9 in Molberry, 6 in Trant, 6 in Nilbasse and 7 in Rienna give a Pinewood Chop and show system
  message 139, "You are now free to ride the cab.", and as many again test the story counter below 3,255;
  `QuestAcceptMenu.disp_accept` lists the errands' titles ("The Eight & Twenty Chops", "A Ticket to the Farce") and
  `disp_clear` closes the list, each setting and releasing flag `0x006F`.
- In each of the five shops the Chopmaster (`NPC_GUILD.talk`) counts the chops ("Ah, [value] chops, I see.") and takes
  28 Pinewood Chops for a Sandalwood Chop, and `RECT_LEAF.talk` gives a Sandalwood or a Pinewood Chop.
- Tsenoble: below story counter 3,260 `EventDirector.main` writes 3260, the start of the infiltration of Draklor
  Laboratory, as Balthier tells of the light airship of the Draklor researchers.
- Tsenoble: below story counter 3,300 `SAKIYOMI_alc_a0100` loads scene `alc_a0100` (event 307); touching `RECT_ジャッジ`
  writes 3300, after Draklor Laboratory, and from 3,300 to below 3,330 `SAKIYOMI_alc_c0180` loads scene `alc_c0180`
  (event 732), in which Jules has had Vaan collect the chops; touching `RECT_ジュールと再会` writes 3330, met Jules in the
  capital.
- Tsenoble: the Cab Guide's cab jumps to the 66th Floor (Draklor Laboratory), field `1008`.
- Tsenoble and the Grand Arcade: the Docent at the lift (`NPC_エレベーターガール.talk`) tests story counter below 4,000 ("No
  one is allowed to enter Central at this time.") and turns away a party without a sandalwood chop; the lifts
  (`map_ダミーＰＣ.エレベーター開く`) run between the Grand Arcade and Tsenoble.
- The court: `alc_z01`'s `常駐監督.main` loads scenes `alc_z0100` (event 300), `alc_z0101` (event 301), `alc_z0102` (event
  303), `alc_z0104` (event 305) and `alc_z0103` (event 304); it writes 1180, 1660, 1976, 2000 and 5020 and jumps to
  The Western Divide (Dalmasca Westersand), Sunlit Path (Ozmone Plain), Freezing Gorge (Paramina Rift), Hall of the
  Light (Mt Bur-Omisace) or Gate of Wind (Giruvegan).
- The court: `alc_z02` loads `alc_z0200` (event 302), writes 1550, after the Senate, and jumps to The Muted Scarp
  (Nabreus Deadlands); `alc_z03` loads `alc_z0103` and jumps to Gate of Wind; `alc_z04` loads `alc_z0101` and jumps to
  Sunlit Path.
- Grand Arcade: Agytha (`NPC_COCATRICE.talk`) hears that the one she seeks is in Old Archades and gives a reward
  package with the Tumulus. Highgarden Terrace: the Hunt Club Owner (`NPC_HUNTLOOP_A.talk`), a backer who wagers on
  the Hunt Club's hunts, hears that the party did for the mark and gives six reward packages of two zodiac gems each,
  from the Aries and Libra Gems to the Virgo and Pisces Gems.
- Charlotte's Magickery: a man who sold his moonsilver medallion to one Otto (`NPC01.talk_01a`) takes the Moonsilver
  Medallion; July the streetear (`talk_02a`), met in Nalbina, thanks the party and gives a reward package with the
  Salamand Halcyon; `talk_04a` sets the name flags `0x03A0` and `0x03A1` (Foppish Man, Sultry Woman). Vint's
  Armaments: `NPC01.talk_04a` sets `0x03BA` and `0x03BB` (Willful Woman, Meek Man).
- Bulward's Technicks: the Cartographers' Guild moogle (`地図屋.talk`) sells the Tchita Uplands or the Archades map, with
  system message 100 or 85; which one is decided at run time. Granch's Requisites: the notice board (`掲示板.talk`) lists
  the bills ("Bill No. [value]") and sets a Bank2048 name flag that the function picks from a table.
- Aerodrome: `EventDirector.main` loads scene `pas_z0000` (event 214).
- Aerodrome: the boarding counter (`乗船カウンタートーク.カウンター処理`, requested by `NPC01.talk_10a` to `talk_12a`) sells passage,
  testing story counter below 6,100.
- Aerodrome: `発着イベント監視.イベント再生とマップジャンプ` sets flag `0x005E`, releases `0x0073`, loads `pas_z0000` and jumps to the Sky
  Saloon or the Observation Parlour (Skyferry) or to the aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades
  and Balfonheim Port, and `高速移動時のマップジャンプ` sets `0x005E` and jumps without the scene.
- Aerodrome: the private airship desk (`NPC01.talk_09a`) tests story counter at least 5,150, below 1,475 and at least
  1,620, sets and releases flags `0x0107` and `0x0108`, and lets the party enter the hangar ("Very well. You may enter
  the hangar from the gate."), loads scene `str_z0000` (event 211) and jumps to the field a script variable holds.
- Tsenoble and the Aerodrome: `choco_sum_ctrl_murasawa.sumcho_byebye`, requested by the teleport, releases flag
  `0x0073`, riding a chocobo.
- The Grand Arcade holds 1 treasure chest.

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

The steps table [`archades-script-steps.tsv`](archades-script-steps.tsv) has one row for each step of every function
of the twenty-seven scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 82,454 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `alc_a01` | 6,036 | `alc_z01` | 170 |
| `alc_a02` | 2,738 | `alc_z02` | 51 |
| `alc_b03` | 8,629 | `alc_z03` | 47 |
| `alc_b04` | 7,073 | `alc_z04` | 47 |
| `alc_b05` | 2,463 | `alc_a0100` | 756 |
| `alc_b06` | 2,593 | `alc_a0280` | 711 |
| `alc_c01` | 6,649 | `alc_b0400` | 1,766 |
| `alc_e01` | 5,675 | `alc_c0180` | 691 |
| `alc_f01` | 7,129 | `alc_z0100` | 1,558 |
| `alc_f02` | 7,374 | `alc_z0101` | 2,682 |
| `alc_f03` | 2,733 | `alc_z0102` | 1,049 |
| `alc_f04` | 3,190 | `alc_z0103` | 2,393 |
| `alc_f05` | 2,549 | `alc_z0104` | 3,907 |
| | | `alc_z0200` | 1,795 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Archades has 158 such rows.

Some actors run another actor's code: `NPC02` in `alc_a01` starts at the same place as `NPC01` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 191 of these rows: 5
in `alc_a01`, 13 in `alc_a02`, 23 in `alc_b03`, 23 in `alc_b04`, 9 in `alc_b05`, 9 in `alc_b06`, 12 in `alc_c01`, 17
in `alc_e01`, 22 in `alc_f01`, 25 in `alc_f02`, 9 in `alc_f03`, 11 in `alc_f04` and 13 in `alc_f05`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 78,370 |
| empty | 4,084 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the variable that holds the standard motion `stdmotionplay` plays, or the variable that receives a
result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `alc_c0180` (event `732`), `プロデューサー.main` reads its
models (`0x03000000` to `0x03000006`) and motion 1 of `alc_c0180.mot`, and waits while `scratch1_var_1` is 0. It then
files `監督.ジュールとの取引` and waits until it ends, turns every light cut off and disposes of event manager slot 0.

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
is shown is written `[value]`. Some zone lines begin with the speaker's name, which the text itself carries (`Balthier`, `Vaan`, `Notice Board`).

The script list [`archades-script-list.tsv`](archades-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`archades-script-steps.tsv`](archades-script-steps.tsv) has one row per step:

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
- [Archades scenes](archades-scenes.md) - the ten scenes these scripts load.
- [Skyferry scripts](skyferry-scripts.md) - the airship the Aerodrome's boarding counter sells passage to.
- [Balfonheim Port scripts](balfonheim-port-scripts.md) - another aerodrome of the same boarding counters, and a
  notice board of the same form.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
