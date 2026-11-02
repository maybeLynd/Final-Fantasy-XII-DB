---
title: "Necrohol of Nabudis scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Necrohol of Nabudis that does something a player can observe. It covers
the thirteen zone scripts, eight with a field entry and five without, and the seven scene scripts of the region, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `bds_a01` | zone | Hall of Effulgent Light, field `421` | 26 | 40 | 12 | 0 |
| `bds_a02` | zone | Cloister of Distant Song, field `422` | 32 | 80 | 14 | 0 |
| `bds_a03` | zone | field `423`, which has no zone-script entry | 3 | 5 | 2 | 0 |
| `bds_b01` | zone | Cloister of the Highborn, field `426` | 37 | 101 | 17 | 0 |
| `bds_b02` | zone | field `427`, which has no zone-script entry | 3 | 5 | 2 | 0 |
| `bds_c01` | zone | Hall of the Ivory Covenant, field `430` | 32 | 79 | 14 | 0 |
| `bds_c02` | zone | Hall of Slumbering Might, field `431` | 25 | 38 | 11 | 0 |
| `bds_d01` | zone | field `433`, which has no zone-script entry | 4 | 7 | 3 | 0 |
| `bds_d02` | zone | field `434`, which has no zone-script entry | 4 | 7 | 3 | 0 |
| `bds_d03` | zone | field `435`, which has no zone-script entry | 4 | 7 | 3 | 0 |
| `bds_e01` | zone | The Crucible, field `438` | 19 | 55 | 5 | 0 |
| `bds_f01` | zone | Cloister of Solace, field `441` | 16 | 60 | 5 | 1 |
| `bds_g01` | zone | Cloister of Reason, field `444` | 16 | 60 | 5 | 1 |
| `bds_a0100` | scene | event `226` | 16 | 136 | 5 | 0 |
| `bds_e0100` | scene | event `224` | 11 | 45 | 0 | 0 |
| `bds_e0101` | scene | event `225` | 15 | 70 | 15 | 0 |
| `bds_f0100` | scene | event `220` | 16 | 95 | 0 | 0 |
| `bds_f0101` | scene | event `221` | 19 | 128 | 0 | 0 |
| `bds_g0100` | scene | event `222` | 16 | 101 | 0 | 0 |
| `bds_g0101` | scene | event `223` | 17 | 79 | 0 | 0 |

Cloister of Solace and Cloister of Reason carry the key-item and message helper `イベント特殊効果画面`, one of the five helper
actors that many zone scripts share. Its functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts it.

The scene `bds_e0101` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

Five more zone scripts of the region ship under `plan_map/bds_a`, `bds_b` and `bds_d`: `bds_a03`, `bds_b02`, `bds_d01`,
`bds_d02` and `bds_d03`. The map name table names fields `423`, `427` and `433` to `435` by these codes, but the
zone-script list has no entry for those fields, so no field loads them.

Each of the five has a row in the script list above, with
the place `field <id>, which has no zone-script entry`, and its map exits have rows in the main table: two each in
`bds_a03` and `bds_b02` and three each in `bds_d01` to `bds_d03`, to fields `421`, `422`, `426`, `441` and `444` of the
region, to Field of the Fallen Lord (field `180`, Nabreus Deadlands), and between `bds_a03` and `bds_d02` and between
`bds_b02` and `bds_d03`. One exit of Cloister of Distant Song (`__MJ_CTRL001`) leads to field `434`, `bds_d02`.

Each script holds `Map_Director`, whose `init` returns at once, and map exits `__MJ_CTRL00n`, each of which turns user
control off, fades out and calls `mapjump`:

- `bds_a03`, field `423`, has two exits, to field `434` (`bds_d02`), entrance 1, and to Cloister of Distant Song, field
  `422`, entrance 3; the only `mapjump` that names field `423` is `bds_d02`'s, which no field loads, so no jump reaches
  `bds_a03`.
- `bds_b02`, field `427`, has two exits, to Field of the Fallen Lord (Nabreus Deadlands), field `180`, entrance 2, and
  to field `435` (`bds_d03`), entrance 1; the only `mapjump` that names field `427` is `bds_d03`'s, which no field
  loads, so no jump reaches `bds_b02`.
- `bds_d01`, field `433`, has three exits, to Hall of Effulgent Light (field `421`, entrance 2), Cloister of Distant
  Song (field `422`, entrance 1) and Cloister of the Highborn (field `426`, entrance 1); no `mapjump` names field `433`,
  so no jump reaches `bds_d01`.
- `bds_d02`, field `434`, has three exits, to field `423` (`bds_a03`, entrance 2), Cloister of Distant Song (field
  `422`, entrance 2) and Cloister of Solace (field `441`, entrance 1); `bds_a02`'s `__MJ_CTRL001` jumps to field `434`
  (entrance 2), as does `bds_a03`, but field `434` has no zone-script entry, so these jumps load no zone script and no
  jump reaches `bds_d02`.
- `bds_d03`, field `435`, has three exits, to field `427` (`bds_b02`, entrance 2), Cloister of the Highborn (field
  `426`, entrance 3) and Cloister of Reason (field `444`, entrance 1); the only `mapjump` that names field `435` is
  `bds_b02`'s, which no field loads, so no jump reaches `bds_d03`.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Necrohol of
Nabudis scenes](necrohol-of-nabudis-scenes.md).

### What the scripts do

- Hall of Effulgent Light: `監督.main` tests the story counter against 3,050 and 3,210, loads scene `bds_a0100` (event
  226), in which the party find what remains of Nabudis, and sets flag `0x0035`, the location map's exits between
  Necrohol of Nabudis and The Salikawood. `Map_Director.init` sets and tests flag `0x0161`, which Corridor of Ages
  (The Salikawood) also sets or tests.
- Hall of Slumbering Might: `監督.main` sets and tests flag `0x0041`, the exits between Nabreus Deadlands and Necrohol
  of Nabudis, and loads scene `ttl_z0002` (event 217). `Map_Director.init` sets and tests flag `0x0160`, which Field
  of the Fallen Lord (Nabreus Deadlands) also sets or tests.
- The medallion doors (`メダル扉.talk`) of Cloister of Distant Song, Cloister of the Highborn and Hall of the Ivory
  Covenant are held fast.
- At these doors each depression names a medallion ("The word "bravery" has been carved within."); the door takes the
  Medallion of Bravery, of Might or of Love, sets flag `0x013A`, `0x013B` or `0x013C`, and jumps to Cloister of
  Solace, The Crucible or Cloister of Reason. `メダル扉.init` sets and releases the same three flags.
- Cloister of Solace and Cloister of Reason: `監督.main` shows the boss gauge, removes the foes and loads the fight's
  two scenes (`bds_f0100` and `bds_f0101`, events 220 and 221; `bds_g0100` and `bds_g0101`, events 222 and 223) and
  `pos_z0000` (event 427).
- Cloister of Solace and Cloister of Reason: then `監督.main` takes the Lusterless Medallion and gives the Medallion of
  Might, or shows system message 141, "The Lusterless Medallion keens..."; in Cloister of Solace it also gives the
  Necrohol of Nabudis map with system message 108, "Your location map for this area is complete!"
- The Crucible: `監督.main` shows the boss gauge, removes the foes and loads scenes `bds_e0100` (event 224), `bds_e0101`
  (event 225), which gives Chaos, and `pos_z0000`. In The Crucible, Cloister of Solace and Cloister of Reason the door
  `ボスマップ扉` leads back to Cloister of the Highborn, Cloister of Distant Song or Hall of the Ivory Covenant, and
  `Map_Director.init` sets flag `0x004E`, `0x004F` or `0x0050`.
- Hall of the Ivory Covenant: `hunt_kansi.main` gives the Gravesoil Trophy and removes the foes of a group. Cloister
  of the Highborn and Hall of Slumbering Might: `wanted_kansi.main` removes the foes of a group.
- Hall of Effulgent Light, Cloister of Distant Song, Cloister of the Highborn, Hall of the Ivory Covenant, Hall of
  Slumbering Might, The Crucible, Cloister of Solace and Cloister of Reason hold 8, 9, 11, 8, 6, 1, 1 and 1 treasure
  chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | the second argument is a section 2 text id; the choices are in that text |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
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

The steps table [`necrohol-of-nabudis-script-steps.tsv`](necrohol-of-nabudis-script-steps.tsv) has one row for each step
of every function of the twenty scripts, in the order the function runs them: each call, request, store, branch, loop,
case and return. It has 12,204 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `bds_a01` | 494 | `bds_e0101` | 881 |
| `bds_a02` | 1,154 | `bds_f0100` | 605 |
| `bds_b01` | 1,407 | `bds_f0101` | 860 |
| `bds_c01` | 1,165 | `bds_g0100` | 666 |
| `bds_c02` | 351 | `bds_g0101` | 545 |
| `bds_e01` | 681 | `bds_a03` | 63 |
| `bds_f01` | 661 | `bds_b02` | 63 |
| `bds_g01` | 648 | `bds_d01` | 94 |
| `bds_a0100` | 1,196 | `bds_d02` | 94 |
| `bds_e0100` | 482 | `bds_d03` | 94 |

The five zone scripts no field loads, last in the table, have 408 steps: those of `Map_Director.init` and of their map
exits.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Necrohol of Nabudis has 20 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it
runs; this table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 11,425 |
| empty | 779 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its functions. In `bds_a0100` (event `226`), `監督.ナブレウス湿原F` starts scene cut 0,
reads an effect into effect slot 0 and waits for it, hides the party and starts cut 1. It files `cut_01_c3` on the
camera and the music actor together, fades the screen in over 60 frames, plays the effect, waits 240 frames and fades
out over 30 frames. At cut 99 it shows the party again and places it with `setposparty`.

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

The script list [`necrohol-of-nabudis-script-list.tsv`](necrohol-of-nabudis-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id; a zone script that no field loads reads `field <id>, which has no zone-script entry` |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`necrohol-of-nabudis-script-steps.tsv`](necrohol-of-nabudis-script-steps.tsv) has one row per step:

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
- [Necrohol of Nabudis scenes](necrohol-of-nabudis-scenes.md) - the seven scenes these scripts load.
- [Nabreus Deadlands scripts](nabreus-deadlands-scripts.md) - the region beyond Hall of Slumbering Might, where the
  Acolyte gives the medallions.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
