[Home](../../README.md) / [Story, events and hunts](README.md) / Tomb of Raithwall scripts

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Tomb of Raithwall scripts: what each script function shows, sets, gives and starts | reference | Story, events and hunts | Scenes and scripts by area / Dalmasca desert | Every function of the Tomb of Raithwall zone and scene scripts that a player can observe, apart from the shared crystal and item-message helpers counted per script: what triggers it, the lines it shows and who speaks them, the story flags and story counter values it sets or tests, the items it gives or takes, its map jumps, battle calls and scene loads. | 0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0 |

## What it lists

The table [tomb-of-raithwall-scripts.tsv](tomb-of-raithwall-scripts.tsv) has one row per script function of The Tomb
of Raithwall that does something a player can observe. It covers the eight zone scripts and the fifteen scene scripts
of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `rwg_a01` | zone | Valley of the Dead, field `403` | 39 | 194 | 14 | 5 |
| `rwg_b01` | zone | Hall of the Destroyer, field `406` | 25 | 137 | 13 | 0 |
| `rwg_b02` | zone | Hall of the Sentinel, field `407` | 28 | 144 | 17 | 0 |
| `rwg_c01` | zone | Royal Passage, field `410` | 45 | 169 | 19 | 1 |
| `rwg_c02` | zone | Southfall Passage, field `411` | 40 | 126 | 15 | 0 |
| `rwg_c03` | zone | Northfall Passage, field `412` | 38 | 123 | 14 | 0 |
| `rwg_d01` | zone | Cloister of Flame, field `415` | 25 | 112 | 11 | 0 |
| `rwg_e01` | zone | Chamber of First Light, field `418` | 15 | 74 | 5 | 0 |
| `rwg_a0100` | scene | event `338` | 26 | 202 | 9 | 0; differs: system_crystal_actor |
| `rwg_a0180` | scene | event `346` | 12 | 41 | 0 | 0 |
| `rwg_a0181` | scene | event `347` | 10 | 40 | 0 | 0 |
| `rwg_b0100` | scene | event `330` | 16 | 96 | 1 | 0 |
| `rwg_b0101` | scene | event `331` | 15 | 63 | 0 | 0 |
| `rwg_b0102` | scene | event `332` | 13 | 54 | 0 | 0 |
| `rwg_b0103` | scene | event `324` | 17 | 86 | 3 | 0 |
| `rwg_b0200` | scene | event `333` | 16 | 72 | 1 | 0 |
| `rwg_b0201` | scene | event `334` | 16 | 67 | 0 | 0 |
| `rwg_b0202` | scene | event `335` | 12 | 57 | 0 | 0 |
| `rwg_c0100` | scene | event `322` | 14 | 121 | 9 | 0 |
| `rwg_d0100` | scene | event `336` | 14 | 70 | 0 | 0 |
| `rwg_d0101` | scene | event `337` | 25 | 180 | 7 | 0 |
| `rwg_d0102` | scene | event `323` | 14 | 99 | 8 | 0 |
| `rwg_e0100` | scene | event `339` | 18 | 209 | 18 | 0 |

Valley of the Dead carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`; Royal Passage
carries the key-item and message helper alone. Their functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Tomb of
Raithwall scenes](tomb-of-raithwall-scenes.md).

### What the scripts do

- Valley of the Dead: `EventDirector.main` sets flag `0x0048`, the location map's exits between the Nam-Yensa Sandsea
  and the Tomb of Raithwall. Below story counter 1342 it writes 1342, shows "You will now have the option of saving
  your game." and opens a full-screen menu; below 1345 it plays movie 9 and writes 1345, the value after the view over
  the Valley of the Dead. The way back leads to Trail of Fading Warmth (Nam-Yensa Sandsea), field 399.
- Valley of the Dead: while `g_btl_ガルーダ強` is 1, `EventDirector.main` loads and plays scenes `rwg_a0180` (event 346)
  and `rwg_a0181` (event 347); touching `ボス登場` sets `Boss_Enter_End[3]`, writes 1352 and starts the fight under the
  boss gauge. When `Boss_Enter_End[3]` is already 1, `EventDirector.main` loads only `rwg_a0181` and runs the same
  fight itself.
- Valley of the Dead: when the Garuda fight ends, the function that runs it removes every foe, loads the victory pose
  scene `pos_z0000` (event 427, [Victory pose scenes](victory-pose-scenes.md)), shows "The ancient device stirs."
  (system message 131), writes 1355, the value after the Garuda battle, plays scene `rwg_a0100` (event 338), sets flag
  `0x0067` (a map icon) and writes 1360.
- Valley of the Dead: from story counter 1390 to 1449, touching `後半ムービー起動` plays movie 3, writes 1450, the value after
  the Leviathan returns, removes Vossler from the party as a guest and jumps to Bridge (Dreadnought Leviathan), field
  871.
- Valley of the Dead: the pirate `NPC_海賊手下` speaks of the avion and the tomb ("You...you killed the avion? Amazing!
  And this— I've never seen such a magnificent structure!" ... "And a hoard of ravenous monsters, I don't doubt. Me, I
  value life over loot. I go no farther... But, should you find something, I'm sure I could be persuaded to part with
  a few gil for it! And if you need aught, of course, I'm your man!").
- The devices ("Magicks stir within this device.") jump between the tomb's halls, each to the field its listing
  stores: in the Valley of the Dead `rwg_warp_bef` (from story counter 1355) and `rwg_warp_aft` (from 1364) to Hall of
  the Destroyer, field 406; in Hall of the Destroyer `gil_warp` to Royal Passage, field 410, and `gil_warp_fromout` to
  the Valley of the Dead, field 403.
- The devices: in Royal Passage `古の仕掛けA` leads to Hall of the Destroyer, and `古の仕掛けB` and `古の仕掛けC` to Northfall
  Passage, field 412, and Southfall Passage, field 411; in Southfall and Northfall Passage `ワープ装置` leads to Royal
  Passage. Several answer "Nothing happens. There must be a corresponding device elsewhere." instead.
- Hall of the Destroyer: below story counter 1364, `常駐ディレクター.init` loads scene `rwg_b0103` (event 324), the talk of
  the devices ("A contraption you'd find in all but the most rudimentary ancient ruin. One touch, and off you're
  whisked to you know not where."); `main` plays it, writes 1364, the value after entering the tomb, and loads scene
  `rwg_b0100` (event 330).
- Hall of the Destroyer: from story counter 1364, while `g_btl_デモンズウォールA` is 1, `Map_Director.main` loads scenes
  `rwg_b0100` (event 330) and `rwg_b0102` (event 332) and requests `map_AD.map_dwbtl_start_id_check`, which loads
  scene `rwg_b0101` (event 331) and shows the boss gauge; when the fight ends it removes every foe, loads `pos_z0000`
  (event 427) and sets `g_btl_デモンズウォールA` to 2.
- Hall of the Destroyer: a jewel in the wall (`step_switch`, "A luminous azure jewel is set in the wall.") answers
  "Nothing happens. You glimpse some manner of device behind the jewel."
- Hall of the Sentinel: while `g_btl_デモンズウォールB` is 1 and the counter is below 1372, `Map_Director.main` loads scenes
  `rwg_b0200` (event 333) and `rwg_b0202` (event 335) and requests `map_AD.map_dwbtl_start_id_check`, which loads
  scene `rwg_b0201` (event 334) and shows the boss gauge; when the fight ends it writes 1372, the value after the
  second Demon Wall battle, removes every foe and loads `pos_z0000` (event 427).
- Hall of the Sentinel: eight braziers (`gimmick_sw01n` to `gimmick_sw04s`) bear the tomb-watchers' words "These words
  have been left by the tomb-watchers: 'Wakes it with the flames. Follows it their shadow. Ne'er straying.'" Touching
  one shows "The Demon Wall halts its advance."; the four from `gimmick_sw02n` to `gimmick_sw03s` also hold "The Demon
  Wall hastens its advance..."
- Royal Passage: when the story counter is 1372 and the party arrives by entrance 1, `常駐ディレクター.init` loads scene
  `rwg_c0100` (event 322); `main` plays it and writes 1374, the value after entering the inverted pyramid area. The
  urn `レイス王墓地図宝壺` gives the area map, Tomb of Raithwall, with system message 107.
- Southfall Passage and Northfall Passage: talking to the jewel on each pedestal (`古の仕掛け`: "A luminous berylline jewel
  is set in the pedestal.", "A luminous crimson jewel is set in the pedestal.") sets map-icon flags `0x00A0` and
  `0x00A1`, and the altar (`顔の台座`) shows "Half of the altar stone has sunk into the floor." Northfall Passage:
  `hunt_kansi.main` gives the Soulless Trophy and removes the foes of a group.
- Cloister of Flame: up to story counter 1374, `常駐ディレクター.init` loads scene `rwg_d0102` (event 323), the talk of the
  Mist; `main` plays it and writes 1374 and 1376, the value after the Mist explanation.
- Cloister of Flame: while `g_btl_ベリアス` is 1, `常駐ディレクター.main` loads and plays scenes `rwg_d0100` (event 336) and
  `rwg_d0101` (event 337); touching `ボス登場` starts the fight under the boss gauge, and when it ends removes every foe,
  sets `g_btl_ベリアス` to 2 and writes 1380, the value after the Belias battle, from which the summon command and
  Quickenings are available.
- Chamber of First Light: below story counter 1390, `常駐ディレクター.init` loads and starts scene `rwg_e0100` (event 339),
  whose own functions give the Dawn Shard; touching `暁の断片起動` writes 1390, the value after the Dawn Shard.
- Chamber of First Light: from 1390 the way stone (`ワープ装置`), whose inscription reads "'By this, return ye to the Hall
  of the Destroyer. By other means, return ye back to this place.'", jumps to Hall of the Destroyer, field 406;
  before, it shows "Nothing happens. The device remains asleep."
- Royal Passage, Southfall Passage, Northfall Passage and Cloister of Flame hold 5, 8, 6 and 4 treasure chests.

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

The steps table [`tomb-of-raithwall-script-steps.tsv`](tomb-of-raithwall-script-steps.tsv) has one row for each step
of every function of the twenty-three scripts, in the order the function runs them: each call, request, store, branch,
loop, case and return. It has 25,349 rows. That leaves out the 411 functions in the spawn groups of the scripts' foes
(entry, spawn and respawn); [Bestiary](../Enemy-Spawning/bestiary.md) reads their entry functions as
enemy placements.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `rwg_a01` | 2,398 | `rwg_b0100` | 965 |
| `rwg_b01` | 2,042 | `rwg_b0101` | 416 |
| `rwg_b02` | 2,586 | `rwg_b0102` | 391 |
| `rwg_c01` | 1,695 | `rwg_b0103` | 639 |
| `rwg_c02` | 1,272 | `rwg_b0200` | 655 |
| `rwg_c03` | 1,260 | `rwg_b0201` | 401 |
| `rwg_d01` | 1,138 | `rwg_b0202` | 394 |
| `rwg_e01` | 704 | `rwg_c0100` | 1,058 |
| `rwg_a0100` | 1,491 | `rwg_d0100` | 600 |
| `rwg_a0180` | 226 | `rwg_d0101` | 1,809 |
| `rwg_a0181` | 258 | `rwg_d0102` | 1,014 |
| | | `rwg_e0100` | 1,937 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Tomb of Raithwall has 39 such rows.

Some actors run another actor's code: `PlayerJack1` in `rwg_a01` starts at the same place as `PlayerJack0` and runs
the same functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 3 of these
rows: 3 in `rwg_a01`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 25,276 |
| empty | 71 |
| `does not ship`, with the fact | 2 |

The two `does not ship` rows are `motionread` calls that read an empty entry: entry 1 of `rwg_a0180.mot` and entry 1
of `rwg_a0181.mot`. A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the
arguments as the script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry
what they give for the step, for example the variable that holds the standard motion `stdmotionplay` plays, or the
variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `rwg_a0180` (event `346`), `監督.main` reads motion 0 of
`rwg_a0180.mot` and event sound slots 0 and 1, waiting for each, and waits while `scratch1_var_1` is 0. It fades out
over 10 frames, files `乗っ取る` on `ボス` and the four `PC乗っ取り` actors, waiting for all five, then stops the current music,
loads track 205 and fades in over 5 frames. At the next cut it starts camera shot `CAM_GARUDA_1` and `ボス.cut01`, then
plays animations 0 to 2 of motion 0 on `カメラアクター` in turn.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown`, `system message`, `movie subtitle`, or an actor's label marked `(script label)`; `-` for a row without a section 2 line |
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

The script list [tomb-of-raithwall-script-list.tsv](tomb-of-raithwall-script-list.tsv) holds the first table above,
one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`tomb-of-raithwall-script-steps.tsv`](tomb-of-raithwall-script-steps.tsv) has one row per step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Tomb of Raithwall scenes](tomb-of-raithwall-scenes.md) - the fifteen scenes these scripts own.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Nam-Yensa Sandsea scripts](nam-yensa-sandsea-scripts.md) - the region beyond the Valley of the Dead.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 121 calls with 22 other topics</summary>

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md), [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [npc names](../Characters-And-Objects/npc-names.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00265B60`](../Characters-And-Objects/actor-record.md) (on actor record) |
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | calls | [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) |
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00272CB0`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen)<br>[`0x00272CE0`](../Characters-And-Objects/npc-names.md) (on npc names) |
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00266AD0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00266BD0`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x00268EA0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DB280`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x003DB580`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DBB60`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | is called by | [`0x002679F0`](../EBP-Script-Files/ebp-script-image.md) Actor storage: allocate and initialize records (on ebp script image) |
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
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
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |

**Graphics** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x002639E0`](../Menus-And-HUD/text-npc-names.md) (on text npc names) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x003FFB00`](archades-scripts.md) (on archades scripts) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Saving, loading and settings** (explained on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |

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
| [`0x0034B9A0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034C030`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034D4E0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034DD90`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034E0B0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x0034EE20`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00352EA0`](barheim-passage-scripts.md) (on barheim passage scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00353390`](barheim-passage-scripts.md) (on barheim passage scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354000`](barheim-passage-scripts.md) (on barheim passage scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
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

**World, areas and travel** (explained on [changing areas](../World-Areas-And-Travel/changing-areas.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x003C0450`](../Game-Files-And-Data-Tables/menu-map-files.md) (on menu map files)<br>[`0x0057FB00`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) |
| [`0x003778B0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x0057FB00`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0057FB00`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |

</details>
