[Home](../../README.md) / [Story, events and hunts](README.md) / Barheim Passage scripts

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Barheim Passage scripts: what each script function shows, sets, gives and starts | reference | Story, events and hunts | Scenes and scripts by area / Nalbina and the Mosphoran Highwaste | Every function of the Barheim Passage zone and scene scripts that a player can observe, apart from the shared crystal and item-message helpers counted per script: what triggers it, the lines it shows and who speaks them, the story flags and story counter values it sets or tests, the items it gives or takes, its map jumps, battle calls and scene loads. | 0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0 |

## What it lists

The table [barheim-passage-scripts.tsv](barheim-passage-scripts.tsv) has one row per script function of Barheim
Passage that does something a player can observe. It covers the seventeen zone scripts and the nine scene scripts of
the region that the path arrays name, and the five zone scripts of the region that no path array names, all from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `mic_a01` | zone | The Lightworks, field `53` | 40 | 210 | 14 | 5 |
| `mic_a02` | zone | Great Eastern Passage, field `54` | 36 | 81 | 13 | 1 |
| `mic_a03` | zone | Op Sector 36, field `55` | 26 | 50 | 6 | 0 |
| `mic_a04` | zone | Special Op Sector 3, field `56` | 30 | 83 | 9 | 0 |
| `mic_a05` | zone | Op Sector 37, field `57` | 27 | 84 | 9 | 0 |
| `mic_a06` | zone | Op Sector 29, field `58` | 26 | 55 | 8 | 0 |
| `mic_b01` | zone | Great Central Passage, field `61` | 28 | 55 | 10 | 0 |
| `mic_b02` | zone | The Zeviah Subterrane, field `62` | 40 | 104 | 16 | 0 |
| `mic_b06` | zone | North-South Junction, field `66` | 18 | 61 | 4 | 5 |
| `mic_c01` | zone | Terminus No. 4, field `69` | 22 | 46 | 2 | 0 |
| `mic_c02` | zone | Terminus No. 4 Adjunct, field `70` | 20 | 71 | 3 | 5 |
| `mic_d01` | zone | Terminus No. 7, field `71` | 21 | 49 | 6 | 0 |
| `mic_e01` | zone | East-West Bypass, field `891` | 25 | 35 | 8 | 0 |
| `mic_e02` | zone | The Zeviah Span, field `892` | 48 | 146 | 18 | 1 |
| `mic_e03` | zone | West Annex, field `893` | 33 | 53 | 17 | 0 |
| `mic_e04` | zone | Terminus No. 7 Adjunct, field `894` | 18 | 50 | 5 | 5 |
| `mic_e05` | zone | Special Op Sector 5, field `895` | 21 | 31 | 9 | 0 |
| `mic_a0100` | scene | event `185` | 23 | 136 | 15 | 0 |
| `mic_a0600` | scene | event `184` | 16 | 80 | 5 | 0 |
| `mic_b0600` | scene | event `186` | 16 | 158 | 11 | 0 |
| `mic_b0601` | scene | event `188` | 25 | 282 | 3 | 0 |
| `mic_c0100` | scene | event `180` | 24 | 126 | 0 | 0 |
| `mic_c0101` | scene | event `181` | 34 | 158 | 0 | 0 |
| `mic_d0100` | scene | event `182` | 13 | 63 | 0 | 0 |
| `mic_d0101` | scene | event `183` | 17 | 82 | 15 | 0 |
| `mic_e0400` | scene | event `187` | 14 | 85 | 1 | 0 |
| `mic_b03` | zone | named by no path array | 3 | 5 | 2 | 0 |
| `mic_b04` | zone | named by no path array | 4 | 7 | 3 | 0 |
| `mic_b05` | zone | named by no path array | 4 | 7 | 3 | 0 |
| `mic_b07` | zone | named by no path array | 14 | 43 | 3 | 5 |
| `mic_b08` | zone | named by no path array | 2 | 3 | 1 | 0 |

The Lightworks, North-South Junction, Terminus No. 4 Adjunct, Terminus No. 7 Adjunct and `mic_b07` carry the five
helper actors that many zone scripts share: the crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`,
`saveactor`) and the key-item and message helper `イベント特殊効果画面`; Great Eastern Passage and The Zeviah Span carry the
key-item and message helper alone. Their functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Barheim
Passage scenes](barheim-passage-scenes.md).

### What the scripts do

- The Lightworks: up to story counter 316, `イベント常駐監督.main` loads scene `mic_a0100` (event 185), adds Basch to the
  party as a guest, plays the scene and writes 317.
- The Lightworks: pressing the power relay switch (`電気スイッチ`) the first time requests `古びた装置イベント1`: Vaan's "Huh. Guess
  it's not working." and Balthier's "Let's have a look. Hm...the fuse is blown. That would explain why there's no
  power reaching the switch. If the wiring is any indication, I'd say this is a central power relay of some sort. As
  it stands, I doubt we'll find much still running down here."
- The Lightworks: the bangaa `SHOP_NPC_バンガ` gives the Tube Fuse ("Made that tube fuse from parts I found down in these
  very tunnels. It's good as any you'll find, and better 'an most, mark my words.") and writes 319; at 319 the switch
  offers "Install the tube fuse.", which takes the fuse and writes 321, the value that marks the power restored.
- The Lightworks: the gate switch (`ドアスイッチ`) holds "Nothing happens. The power to the gate has been cut.", and the
  gate (`可動柵ＨＥＬＰメッセージ`) "The gate is far too heavy to force. There must be a switch or lever somewhere to operate it."
- The Lightworks: `イベント常駐監督.錆びた突起物イベント1` requests the bangaa's `バッテリー会話`: with the gate open, he says, fierce beasts
  come out in the dark when the charge drops, the gauge shows the charge left, opening a gate of that size uses up
  some of it, and the switchboards lead the way through.
- Great Eastern Passage: the urn `バルハイム地図宝壷` gives the area map, Barheim Passage, with system message 104.
- Special Op Sector 3: the gate (`可動柵`) holds the same line. Op Sector 37: the rusted switch (`ドアスイッチ`) holds "You
  hear a loud sound from the south. The gate is open." and "Nothing happens. There doesn't seem to be enough power
  reaching the switch."
- Op Sector 29: up to story counter 321, `常駐監督.main` loads and plays scene `mic_a0600` (event 184), the talk of the
  Mimics, and writes 323, the value after the secret of the Battery Mimic.
- The Zeviah Subterrane: `常駐監督.main` sets flag `0x0022`, the location map's exits between Barheim Passage and the
  Dalmasca Estersand; an exit leads to Murmuring Defile (Dalmasca Estersand), field 232. `閉じた扉` shows "The gate is
  firmly closed."
- North-South Junction: up to story counter 323, `常駐監督.main` loads and plays scenes `mic_b0600` (event 186) and
  `mic_b0601` (event 188), writes 325, 330 and 333, the value after Basch's apology, and replaces Basch's guest entry
  (`removeguestbattlemember(8)`, `addguestbattlemember(9)`).
- Terminus No. 4: `常駐監督.main` first writes 340, the value at the start of the Mimic Queen battle; while
  `g_btl_ミミッククイーン` is 1 it loads and plays scenes `mic_c0100` (event 180) and `mic_c0101` (event 181) and shows the
  boss gauge; when the fight ends it removes every foe, writes 341 and jumps to Passage Entrance (Dalmasca Estersand),
  field 231.
- Terminus No. 7: arriving by entrance 2 sets flag `0x0040`, the location map's exits between Barheim Passage and the
  Garamsythe Waterway; an exit leads to East Sluice Control (Garamsythe Waterway), field 840. While `g_btl_ザルエラ` is 1,
  `常駐監督.main` loads and plays scenes `mic_d0100` (event 182) and `mic_d0101` (event 183).
- Terminus No. 7: touching `ボス登場` requests `常駐監督.監視`, which sets a gauge timer to 300 (`setgaugetimer(0x012c)`) and
  shows the boss gauge. When `getgaugetimer(1)` reaches 0 it jumps to Terminus No. 7 Adjunct, field 894; after the
  fight it removes every foe, loads the victory pose scene `pos_z0000` (event 427, [Victory pose
  scenes](victory-pose-scenes.md)) and sets `g_btl_ザルエラ` to 2.
- Terminus No. 7 Adjunct: `常駐監督.main` loads and plays scene `mic_e0400` (event 187) while `ザルエラ制御_状況` is 10 and
  `Boss_Enter_End[1]` is 0.
- East-West Bypass and The Zeviah Span: `hunt_kansi.main` gives the Bony Trophy and removes the foes of a group. West
  Annex: `wanted_kansi.main` removes the foes of a group.
- The Zeviah Span: while `EV_H_暗号` is 0 and five further global values are 1, touching `宝レクト` shows Gilgamesh's
  message below, gives the Matamune and sets `EV_H_暗号` to 30. Talking to `バルハイムキャンドル` gives the Barheim Candle with
  system message 119 ("The candle reveals hidden areas on your map of the [value]!").

Gilgamesh at the Zeviah Span: "Too long has it been, my friends! It is I, Gilgamesh!!! Ah, but do not worry! I am not
here to spill your blood today! I came here on a rumor that I might find a treasure of legend sleeping in these
tunnels. Alas! There was no treasure. A useless stick I found, and nothing more! A waste of precious time! It bears no
hint of semblance with the sword of legend I seek. Yours for the taking, should such rubbish appeal to you!"

- The Lightworks, Great Eastern Passage, Op Sector 36, Special Op Sector 3, Op Sector 37, Op Sector 29, Great Central
  Passage, The Zeviah Subterrane, Terminus No. 7, East-West Bypass, The Zeviah Span, West Annex, Terminus No. 7
  Adjunct and Special Op Sector 5 hold 3, 7, 3, 3, 5, 3, 4, 9, 2, 5, 12, 13, 1 and 8 treasure chests.
- The five zone scripts that no path array names, `mic_b03`, `mic_b04`, `mic_b05`, `mic_b07` and `mic_b08`:
  - the zone path array names no file at kind 5 ids 189 to 197 and 201 to 206, the zone entries of fields 63 to 65,
    67 and 68 ([asset paths](../Game-Files-And-Data-Tables/asset-paths.md)), and those fields have no map
    name ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md));
  - their rows are map jumps among fields 63, 64, 65 and 67, and out to Great Central Passage, field 61 (from
    `mic_b03` and `mic_b08`), and Terminus No. 7, field 71 (from `mic_b07`). Fields 63 to 65 and 67 have no map
    name, so their `jumps` cells start with the comma before `field`;
  - no other row of the area script tables names field 63, 64, 65, 67 or 68 as a jump destination;
  - `mic_b07` also carries the five helper actors and the chocobo dismount
    `choco_sum_ctrl_murasawa.sumcho_byebye`, which releases flag `0x0073`.

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

The steps table [`barheim-passage-script-steps.tsv`](barheim-passage-script-steps.tsv) has one row for each step of
every function of the thirty-one scripts, in the order the function runs them: each call, request, store, branch,
loop, case and return. It has 36,957 rows. That leaves out the 1,061 functions in the spawn groups of the scripts'
foes (entry, spawn, respawn and talk); [Bestiary](../Enemy-Spawning/bestiary.md) reads their entry
functions as enemy placements.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `mic_a01` | 2,135 | `mic_e04` | 297 |
| `mic_a02` | 3,215 | `mic_e05` | 260 |
| `mic_a03` | 2,389 | `mic_a0100` | 1,052 |
| `mic_a04` | 2,776 | `mic_a0600` | 894 |
| `mic_a05` | 2,786 | `mic_b0600` | 1,511 |
| `mic_a06` | 2,577 | `mic_b0601` | 2,319 |
| `mic_b01` | 1,761 | `mic_c0100` | 850 |
| `mic_b02` | 3,405 | `mic_c0101` | 1,246 |
| `mic_b06` | 540 | `mic_d0100` | 674 |
| `mic_c01` | 972 | `mic_d0101` | 924 |
| `mic_c02` | 584 | `mic_e0400` | 433 |
| `mic_d01` | 819 | `mic_b03` | 63 |
| `mic_e01` | 295 | `mic_b04` | 94 |
| `mic_e02` | 1,316 | `mic_b05` | 94 |
| `mic_e03` | 492 | `mic_b07` | 152 |
| | | `mic_b08` | 32 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Barheim Passage has 165 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 36,856 |
| empty | 101 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `mic_a0100` (event `185`), `ディレクター.main` starts scene
cut 0 and starts `準備` on seven actors together, among them `バルフレア`, `バッシュ` and `ダミーカメラ`, waiting for each to end and
for effect slot 0. It files `ディレクター.イベント進行` and waits until it ends. When `skipcheck(0)` holds, it fades out over 0
frames, sets system message 47 for message slot 0 and waits on the window; otherwise it files
`イベント特殊効果画面_EV.システムメッセージ表示` and waits until it ends.

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
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [barheim-passage-script-list.tsv](barheim-passage-script-list.tsv) holds the first table above, one
row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`barheim-passage-script-steps.tsv`](barheim-passage-script-steps.tsv) has one row per step:

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
- [Barheim Passage scenes](barheim-passage-scenes.md) - the nine scenes these scripts own.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Dalmasca Estersand scripts](dalmasca-estersand-scripts.md) - the region beyond The Zeviah Subterrane and Terminus No. 4.
- [Hunts](hunts.md) - the marks and their petitioners.
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
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x0025D5E0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |

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
| [`0x00352EA0`](barheim-passage-scripts.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00353390`](barheim-passage-scripts.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354000`](barheim-passage-scripts.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
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
