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
runs; this table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 32,644 |
| empty | 2,110 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

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
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test`. After the enclosing tests come, in listing order, the ways the function leaves before the step: a `return`, a `break` (it leaves its repeat or switch), a `continue` (it skips the rest of the pass) or a `goto` past the step that an earlier test sends the run to, and a repeat that never ends. Each is written as the test that keeps the run on its way to the step: `not (regI0 == 0)` after `if (regI0 == 0) { return; }`, or `not ((test) and (test))` when several tests together lead away. A test inside a repeat counts for the pass the step runs in, and a test the run does not reach counts as one that does not hold. After a repeat that a `return` or a `goto` can also leave, a step reached only when the repeat ends by itself carries `the repeat at line N ended at its own test or a break` (`through a break` for an endless repeat), and a way out of it reads `the repeat at line N was left at line M`. When a `goto`, or a case that runs on into the next case, also leads to the step, only the enclosing tests that hold on every way to the step are written, followed by the same items for the ways that miss it. A function that a `goto` of another function enters at one of its labels runs either from its top or from that label: an item then names where the run came in, `the run began at the top of the function` or `the run entered at line N through a goto from another function`. A `case` or `default` step is a test of its switch, so it runs whenever the switch runs. `unreachable in the listing` marks a step that no path of the function in the decompiled listing reaches; it rests on the labels the listing prints for jump targets |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test. A number with a fraction is the listing's print of a 32-bit float to nine significant digits, here and in `condition`: 1.60000002 is the float nearest to 1.6, and 2.36000005e-06 is 2.36000005 times 10 to the power -6 |
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
- [Giza Plains scenes](giza-plains-scenes.md) - the five scenes these scripts load.
- [Dalmasca Estersand scripts](dalmasca-estersand-scripts.md) - the region beyond Gizas South Bank.
- [Dalmasca Westersand scripts](dalmasca-westersand-scripts.md) - the region beyond Starfall Field.
- [Ozmone Plain scripts](ozmone-plain-scripts.md) - the region south of Starfall Field.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
