---
title: "Developer scripts: the debug menus and test scenes no path array names"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0032FCA0, 0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034ADA0, 0x0034B760, 0x0034BB10, 0x00352190, 0x00352AF0"
---

## What it lists

The table [developer-scripts.tsv](developer-scripts.tsv) has one row per script function of the developer scripts
that does something a player can observe. It covers the eighteen scripts under `event/evt_t` of `plan_master/us`.

The nineteenth folder there, `evt_t0020`, holds a bare script image of version 7 in place of an `EBP2` container
([EBP script container](../EBP-Script-Files/ebp-script-container.md),
[story counter values](story-counter-values.md)). Its first word is `0x80000007`, version 7 with the marker
`0x8000`, its length word at +0x4 is `0x970`, the file's 2,416 bytes, and +0x90 holds the build stamp `07/09 18:02`.
The file is byte-identical in all nine language folders, and no language folder holds an `EBP2` copy of it.

Its directory holds 11 actors in 0x20-byte entries, the size the engine reads below version 8
([script image](../EBP-Script-Files/ebp-script-image.md)): `Map_Director` of type 0, with `init`, `main` and
`open`, and ten of type 5, each with `init` and `main`: `door1`, `master1` to `master5` and `camera1` also have
`talk`, `sample1` to `sample3` do not. The image declares no variable.

No path array names these scripts: the [asset path table](../Game-Files-And-Data-Tables/asset-paths.md) has no
entry for any of them. An event id `n` names the scene script at index `4n` of the event file table, so none of them
has an event id. Their `place` cell reads `developer script, named by no path array`, and their kind in the script
list is `developer`.

| Script | Actors | Functions | Rows |
|---|---:|---:|---:|
| `evt_t0005` | 51 | 163 | 1 |
| `evt_t0009` | 1 | 2 | 1 |
| `evt_t0015` | 5 | 20 | 13 |
| `evt_t0016` | 1 | 2 | 1 |
| `evt_t0023` | 3 | 7 | 1 |
| `evt_t0080` | 1 | 2 | 1 |
| `evt_t0081` | 8 | 68 | 1 |
| `evt_t0082` | 18 | 116 | 7 |
| `evt_t0083` | 16 | 213 | 4 |
| `evt_t0084` | 7 | 233 | 4 |
| `evt_t0085` | 21 | 219 | 6 |
| `evt_t0086` | 11 | 95 | 3 |
| `evt_t0090` | 3 | 11 | 6 |
| `evt_t0094` | 2 | 3 | 1 |
| `evt_t0096` | 1 | 3 | 1 |
| `evt_t0500` | 1 | 2 | 1 |
| `evt_t0505` | 10 | 29 | 4 |
| `evt_t0509` | 5 | 13 | 1 |

No script of the group carries a shared helper actor, so the `shared_actors` cell is 0 on every row.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes table
[developer-scenes.tsv](developer-scenes.tsv) has one row per script, with its section 2 entries and their text.

### What the scripts do

- Most of them are debug menus, by their actors' names:
  - `Map_Debug_menu_mtanaka` (`evt_t0080`, `evt_t0081`, `evt_t0086`);
  - `Map_Debug_menu_t_hirose` (`evt_t0082`, `evt_t0084`);
  - `Map_Debug_menu_naomif` (`evt_t0083`) and `Map_Debug_menu_s_ohzono` (`evt_t0085`);
  - `デバッグ監督` (`evt_t0090`);
  - `トライアルデバッグメニュー` (`evt_t0094`, a Trial Mode debug menu);
  - `イベントデバッグメニュー` (`evt_t0500`).
- `evt_t0096`, `evt_t0505` and `evt_t0509` show menus too, by their section 2 entries: `MoB menu`, the party
  question `パーティー構成は？` and `Map Jump(Set Location ID)`.
- A menu asks its question with `aask` (`evt_t0083` and `evt_t0090` also with `aaske`, and `evt_t0083` with
  `aask_1ff`) and acts on the answer. Of the table's 57 rows, 18 jump to a field, 10 write the
  story counter, 21 give or take items and 7 change the party. The counter writes are in the nine scripts
  that [story counter values](story-counter-values.md) counts as developer menus.
- Three scripts load scenes by a literal event id: `evt_t0016` (12 scenes), `evt_t0090` (10) and `evt_t0500`
  (19).
- `evt_t0005` has 51 actors. Its motion calls name entries 1 and 2 of `evt_t0005.mot`, the motion file in its own
  folder; both entries are empty (see [Every step](#every-step)).
- `evt_t0015` carries `イベント特殊効果画面_EV`, whose functions give the item held in a variable and show system
  messages. It is not the shared helper `イベント特殊効果画面`, so its functions have rows.
- `evt_t0009` sets the body radius of the four party slots from the answer to its question (the example under
  [Every step](#every-step)).

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | a question and its choices: the second argument is a section 2 text id (`0x0034B760` and `0x0034BB10` jump to `0x0034ADA0`) |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember` | `0x353`, `0x355` | `0x0034C030`, `0x0034D4E0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |
| `removepartymember`, `addguestbattlemember`, `removeguestbattlemember` | `0x354`, `0x35B`, `0x35C` | `0x0034C030`, `0x00352190`, `0x00352AF0` | `party` | party row selectors: a member leaves, a guest joins, a guest leaves ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

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
4. `0x00348DF0` reads the entry's flag through `0x002673A0`, bit `0x1` of the entry's upper half (`0x00348E85`), and
   opens the window through `0x002E16B0` only when that flag is clear (`0x00348EE0`-`0x00348EFF`). With the flag set it
   still makes its six slot calls (`0x00348E91`-`0x00348ECA`) and fills the call record (`0x00348ED7`-`0x00348EDC`) but
   opens no window ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

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
- `0x00348DF0` makes that `0x002E16B0` call only for a line whose section 2 flag is clear (`0x00348EE0`); for a flagged
  line it opens no window, so the actor's name flag is not set there.
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
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`developer-script-steps.tsv`](developer-script-steps.tsv) has one row for each step of every function
of the eighteen scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 78,071 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `evt_t0005` | 1,340 | `evt_t0084` | 9,529 |
| `evt_t0009` | 52 | `evt_t0085` | 7,718 |
| `evt_t0015` | 248 | `evt_t0086` | 11,231 |
| `evt_t0016` | 142 | `evt_t0090` | 5,823 |
| `evt_t0023` | 65 | `evt_t0094` | 308 |
| `evt_t0080` | 289 | `evt_t0096` | 2,742 |
| `evt_t0081` | 10,615 | `evt_t0500` | 952 |
| `evt_t0082` | 6,018 | `evt_t0505` | 9,760 |
| `evt_t0083` | 9,893 | `evt_t0509` | 1,346 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv).
None of these scripts carries one of them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 76,982 |
| `does not ship` | 63 |
| empty | 1,026 |

A script that no path array names has no motion or sound entry there. For these scripts the steps read the `.mot` and
`.snd` in the script's own folder, when one ships there, and the `resolution` cell says so. Only `evt_t0005` and
`evt_t0015` ship a `.mot`, no developer script ships a `.snd`, and only `evt_t0005`'s steps name its file.

The 63 `does not ship` rows are all in `evt_t0005`: its `motionread` and `motionplay_bb` calls name entries 1 and
2 of `evt_t0005.mot`, and both entries of the file are empty, so the calls play nothing.

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A menu reads from top to bottom in its main function. In `evt_t0009`, `Map_Director.main` sets the area map to not
jammed (`setnavimapjamming(0)`), closes message windows 0 to 7, waits 2 frames and asks a question in window 6. The
answers 1 to 4 store 40, 45, 50 or 55 in `file_var_s0_1`.

For any answer it then takes party slots 0 to 3 in turn
(`capturepc`), sets each one's body radius to that value divided by 100 (`setradius((file_var_s0_1 / 100))`, on
the `float` `file_var_s0_1`, so 0.40 to 0.55), waits a frame and releases it (`releasepc_404`); a frame's wait also
comes between `capturepc` and `setradius`. It then waits a frame and ends the event (`eventdispose`).

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | `developer script, named by no path array` on every row |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `main`), or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown`, `system message`, `movie subtitle`, or an actor's label marked `(script label)`; `-` for a row without a section 2 line |
| `lines` | the section 2 entries the function passes to the message verbs and the ask verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_tested` | `-` on every row: no listed function sets or tests a story flag |
| `flags_released` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set`, `counter_tested` | the story counter values written and tested, each written value with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `items` | items the function gives or takes, by name; a fixed count is written `xN`, a count the game computes reads `, as many as <expression> gives`, and an item the script holds in a variable is named by the variable |
| `jumps` | the field and entrance of each `mapjump`, the field as map name (region) and field id; a field the script holds in a variable or computes is named by the expression |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join or leave, as guests too, and the fighting party the function sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` on every row: no listed function belongs to a shared helper actor |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [developer-script-list.tsv](developer-script-list.tsv) holds the first table above, one row per
script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `developer`, and `developer script, named by no path array` |
| `actors`, `functions` | the script's actors and functions |
| `rows` | the script's rows in the main table |
| `shared_actors` | 0 on every row: no script carries a shared helper actor |

The scenes table [developer-scenes.tsv](developer-scenes.tsv) has one row per script:

| Column | Meaning |
|---|---|
| `scene` | the script, by its file name |
| `event_id`, `next` | `-` on every row: no script has an event id |
| `loaded_by` | that the script has no event id: the asset path table has no entry for it |
| `lines` | the number of entries in the script's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; a scene with no non-empty entry: one sentence of what its script does; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items`, `party`, `flags_set`, `counter_set` | what the script's own functions give or take, change in the party, set and write, as in the main table |
| `plays_when` | that no scene load names the script: it has no event id, and every scene load in the `us` scripts names one |

The steps table [`developer-script-steps.tsv`](developer-script-steps.tsv) has one row per step:

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

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Story counter values](story-counter-values.md) - the counter values these menus write, and the developers' names
  for them from the `evt_t0505` scenario menu.
- [Script calls in every script](script-censuses.md) - the developer scripts in the counts of every us script.
- [Script language differences](script-language-differences.md) - the calls the `kr`, `cn` and `ch` copies of these
  scripts add.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00266530` calls `0x00265B60`; those functions are documented on
  [actor record](../Characters-And-Objects/actor-record.md).
- Actor entity: `0x002621D0` calls `0x00358940`; `0x00263990` is called by `0x0025C230`, `0x0025C830`, `0x00268D10`, `0x00272CB0`,
  `0x00272CE0`; `0x00266530` calls `0x00266AD0`, `0x00266BD0`, `0x00268EA0`, `0x003DB280`, `0x003DB580`, `0x003DBB60`; `0x00266530` is
  called by `0x002679F0`; `0x0032FCA0` calls `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`; `0x00355830` calls `0x0025D5E0`,
  `0x003588B0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md),
  [npc names](../Characters-And-Objects/npc-names.md).
- Actor entity: and on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [actor record](../Characters-And-Objects/actor-record.md).
- Actor entity: and on [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md); and on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Core runtime: `0x00354D00` calls `0x00229EA0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x00266530` calls `0x00265FF0`, `0x00268380`; `0x00355830` calls `0x0026D6D0`; those functions are documented on
  [actor record fields](../Characters-And-Objects/actor-record-fields.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md).
- Party: `0x0034D4E0` calls `0x00263750`, `0x0026DC40`, `0x003271D0`, `0x00327850`, `0x00328DB0`, `0x00359C00`, `0x0035A050`,
  `0x003601B0`; `0x00352190` calls `0x00263750`, `0x003170E0`, `0x00322350`; `0x00352AF0` calls `0x00322350`, `0x003288F0`; `0x00355830`
  calls `0x003590D0`.
- Party: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Presentation: `0x00263990` is called by `0x002B0280`; `0x002639E0` is called by `0x002B0280`; `0x00377B60` is called by
  `0x002B7B80`, `0x002BAF80`; `0x003FFB00` is called by `0x002B0280`; those functions are documented on
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`; `0x00351880` calls `0x001D6A70`; `0x003529E0` calls
  `0x001D6A70`; those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Save load settings: `0x00264F90` is called by `0x00583D60`; those functions are documented on
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md).
- Script VM: `0x002621D0` calls `0x003DC240`, `0x003DC270`, `0x003DC2A0`; `0x002621D0` is called by `0x0025E4C0`; `0x00264D60` is
  called by `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`,
  `0x00356B70`, `0x0050EAB0`; `0x00264F90` is called by `0x00357450`, `0x0050CDE0`; `0x002673A0` is called by `0x00348DF0`,
  `0x0034ADA0`, `0x003545B0`, `0x0050EAB0`.
- Script VM: `0x002E16B0` is called by `0x0033F950`, `0x00348DF0`, `0x0034ADA0`, `0x0050EAB0`; `0x003449A0` calls `0x00267E10`,
  `0x0026B4E0`; `0x00345080` calls `0x00267E10`, `0x00267F90`, `0x0026B4E0`; `0x003459C0` calls `0x00267E10`, `0x0026B4E0`; `0x00348DF0`
  calls `0x00267E10`; `0x00348DF0` is called by `0x00349800`; `0x00349800` calls `0x00267E10`, `0x00267F90`, `0x00348DF0`.
- Script VM: `0x00349800` is called by `0x00349BF0`, `0x0034A090`, `0x0034A420`, `0x0034A7A0`; `0x00349BF0` calls `0x00267F90`,
  `0x00349800`; `0x0034A090` calls `0x00267F90`, `0x00349800`; `0x0034A420` calls `0x00267F90`, `0x00349800`; `0x0034A6D0` calls
  `0x00267E10`; `0x0034ADA0` calls `0x00267E10`; `0x0034ADA0` is called by `0x0034B760`, `0x0034BB10`; `0x0034B760` calls
  `0x00267F90`, `0x0034ADA0`; `0x0034B9A0` calls `0x00267E10`.
- Script VM: `0x0034BB10` calls `0x00267F90`, `0x0034ADA0`; `0x0034C030` calls `0x00267E10`; `0x0034D4E0` calls `0x00267E10`;
  `0x0034DD90` calls `0x00267E10`; `0x0034E0B0` calls `0x00267E10`, `0x0026B4E0`; `0x0034EE20` calls `0x00267E10`; `0x00351880` calls
  `0x00267E10`; `0x00352190` calls `0x00267E10`; `0x003529E0` calls `0x00267E10`, `0x00267F90`; `0x00352AF0` calls `0x00267E10`;
  `0x00354D00` calls `0x00267E10`; `0x00355830` calls `0x00267E10`.
- Script VM: those functions are documented on [identifier spaces](../Engine-Core/identifier-spaces.md),
  [native commands](../Scripts-And-Script-Commands/native-commands.md),
  [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md), [archades scenes](archades-scenes.md),
  [archades scripts](archades-scripts.md).
- Script VM: and on [ebp text sections](../EBP-Script-Files/ebp-text-sections.md),
  [npc names](../Characters-And-Objects/npc-names.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- UI: `0x00263990` is called by `0x002AC5F0`; `0x002639E0` is called by `0x002AC5F0`; `0x00264F90` is called by `0x0029C530`;
  `0x003778B0` is called by `0x0029C530`; `0x00377B60` is called by `0x0029C530`; `0x003FFB00` is called by `0x002AC5F0`; those
  functions are documented on [augments](../Damage-And-Battle-Formulas/augments.md),
  [zone asset list](../World-Areas-And-Travel/zone-asset-list.md).
- World area: `0x00264F90` is called by `0x003145E0`, `0x003778B0`, `0x003C0450`, `0x0057FB00`; `0x0032FCA0` is called by
  `0x0032FC30`; `0x003778B0` calls `0x00264F90`; `0x003778B0` is called by `0x0057FB00`; `0x00377B60` is called by `0x0057FB00`.
- World area: those functions are documented on [changing areas](../World-Areas-And-Travel/changing-areas.md),
  [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md),
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md).
- World area: and on [debug menu](../Engine-Core/debug-menu.md).
