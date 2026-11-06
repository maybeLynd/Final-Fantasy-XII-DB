---
title: "Cerobi Steppe scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034ADA0, 0x0034B760, 0x0034BB10, 0x00352190, 0x00352AF0"
---

## What it lists

The table [cerobi-steppe-scripts.tsv](cerobi-steppe-scripts.tsv) has one row per script function of the Cerobi Steppe
that does something a player can observe. It covers the eight zone scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `srb_a01` | zone | Old Elanise Road, field `497` | 41 | 152 | 41 | 1 |
| `srb_a02` | zone | Crossfield, field `498` | 44 | 159 | 41 | 1 |
| `srb_a03` | zone | The Terraced Bank, field `499` | 41 | 153 | 38 | 1 |
| `srb_a04` | zone | Journey's Rest, field `500` | 26 | 141 | 26 | 5 |
| `srb_b01` | zone | North Liavell Hills, field `503` | 42 | 157 | 40 | 1 |
| `srb_b02` | zone | South Liavell Hills, field `504` | 41 | 152 | 42 | 1 |
| `srb_b03` | zone | Feddik River, field `505` | 43 | 152 | 39 | 1 |
| `srb_b04` | zone | The Northsward, field `506` | 47 | 165 | 44 | 1 |

Journey's Rest carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`; Old Elanise Road,
Crossfield, The Terraced Bank, North Liavell Hills, South Liavell Hills, Feddik River and The Northsward carry the
key-item and message helper alone. Their functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step).

Cerobi Steppe has no scene script of its own; the scenes its fields load are the location title `ttl_z0002` ([Location
title scenes](titles-scenes.md)) and the Strahl scene `str_z0000` ([Strahl scene](strahl-scenes.md)).

### What the scripts do

- Old Elanise Road and South Liavell Hills: `監督.main` loads the location title `ttl_z0002` (event 217) on the first
  arrival and sets flag `0x002D` or `0x002E`, the location map's exits to the Tchita Uplands and to Balfonheim Port.
- The windmills: the Craftsmoogles' League is servicing the ten windmills of the steppe, one moogle (`大工モーグリ`) to each
  (the moogle of windmill 1: "The Craftsmoogles' League have been called in to service all ten of the windmills on the
  Steppe, kupo. This is the No. 1 mill."). Windmills 1 to 3 stand in North Liavell Hills, 4 and 5 in The Terraced
  Bank, 6 and 7 in Crossfield, and 8 to 10 in The Northsward (`風車レクト１` to `風車レクト１０`).
- Talking to a windmill (`風車レクトN.talk`) calls its moogle (`大工モーグリ.風車N挙動`). While the party holds the Yellow Bottle or
  the Auric Message, the moogle asks (at windmill 1) "This is the No. 1 mill, kupo. She's running right now...need me
  to stop her?" or "This is the No. 1 mill, kupo. She's stopped right now...need me to start her up?" and stops
  (`EV_H_風車N` 10) or starts (0) the windmill; otherwise it only talks.
- When such a talk leaves windmills 3, 4, 6, 8 and 10 stopped and the other five running, and `EV_H_暗号_黄` is not
  20, the Yellow Bottle shatters ("Without warning, the yellow bottle in your inventory shatters!"): the moogle
  gives a reward package with a Hi-Ether, takes the Yellow Bottle, gives the Auric Message and sets `EV_H_暗号_黄` to
  20.
- The Wyrm Philosopher (`竜じいさん`) dozes atop windmill No. 10 and wakes when its moogle finds him (`大工モーグリ.風車１０挙動`).
  While the party holds the Dragon Scale and not the Ageworn Key, he takes the Dragon Scale and gives the Ageworn Key.
  The Dragon Scale's description: "A scale found on the corpse of a vyraal. Natural philosophers studying wyrms and
  their kin are known to pay well for such."
- The Wyrm Philosopher's thanks as he gives the Ageworn Key: "Thank you! Thank you so much! My life's work is
  complete! I shall treasure this for the rest of my days. I must give you something by way of thanks... Here, take
  this. It is a key said to open the door to a chamber holding a most terrible wyrm."
- The Northsward: the Viera Wayfarer (`賞金首監督.main`) leads the hunt for the vyraal ("The vyraal that attacked me is a
  great creature with massive wings. It will not be far. Come!"); `wanted_kansi.main` removes the foes and gives a
  Viera Rucksack ("We are victorious. I would reward you for your courage. Visit me at the Whitecap in Balfonheim. I
  shall wait for you there.").
- Crossfield and Feddik River: `hunt_kansi.main` gives the Cruel Trophy and the Adamantine Trophy and removes the foes
  of a group.
- Journey's Rest holds the crystal. Talking to `system_anchor_actor` requests `ym_shutoraljump.shtjump`, which loads
  scene `str_z0000` (event 211) and jumps to the field a script variable holds ([Strahl scene](strahl-scenes.md)).
- Old Elanise Road, Crossfield, The Terraced Bank, North Liavell Hills, South Liavell Hills, Feddik River and The
  Northsward hold 16, 14, 14, 13, 15, 15 and 14 treasure chests.

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

The steps table [`cerobi-steppe-script-steps.tsv`](cerobi-steppe-script-steps.tsv) has one row for each step of every
function of the eight scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 27,352 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `srb_a01` | 3,195 | `srb_b01` | 3,654 |
| `srb_a02` | 3,554 | `srb_b02` | 3,285 |
| `srb_a03` | 3,473 | `srb_b03` | 3,195 |
| `srb_a04` | 3,105 | `srb_b04` | 3,891 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Cerobi Steppe has 99 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 27,252 |
| empty | 20 |
| `does not ship`, with the fact | 80 |

The eighty `does not ship` rows are `motionread` calls that read entry 0, an empty entry, of `srb_a01.mot`,
`srb_a02.mot`, `srb_a03.mot`, `srb_a04.mot`, `srb_b01.mot`, `srb_b02.mot`, `srb_b03.mot` and `srb_b04.mot`, ten in
each. A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as
the script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they
give for the step, for example the variable that receives a result, and `-` otherwise.

A function reads from top to bottom. In `srb_b03` (Feddik River), `hunt_kansi.main` runs when
`g_btl_hunt_srb_アダマンタイマイ` is 1 or `unkCall_5a9()` holds. It waits while `scratch1_var_1` is 0, turns user control off,
closes the boss gauge, waits 30 frames and suspends the battle. It fades the music to volume 32 over 30 frames, gives
the Adamantine Trophy (`additemmes(0x80d4, 1)`), fades the music back to 127, adds 1 to `quest_global_flag[8]`, sets
the hunt variable to 2, removes every foe of the group and resumes the battle with user control on.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown`, `system message`, `movie subtitle`, or an actor's label marked `(script label)`; `-` for a row without a section 2 line |
| `lines` | the section 2 entries the function passes to the message verbs and the ask verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `field held in` and the variable when the target field is a variable |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [cerobi-steppe-script-list.tsv](cerobi-steppe-script-list.tsv) holds the first table above, one row
per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`cerobi-steppe-script-steps.tsv`](cerobi-steppe-script-steps.tsv) has one row per step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Strahl scene](strahl-scenes.md) - the private airship scene the anchor loads.
- [Golmore Jungle scripts](golmore-jungle-scripts.md) and [Paramina Rift scripts](paramina-rift-scripts.md) - other regions of this batch.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
