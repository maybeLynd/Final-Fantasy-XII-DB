---
title: "Dreadnought Leviathan scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [dreadnought-leviathan-scripts.tsv](dreadnought-leviathan-scripts.tsv) has one row per script function of
the Dreadnought Leviathan that does something a player can observe. It covers the ten zone scripts and the twelve
scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `rsn_a01` | zone | Port Launch, field `552` | 28 | 111 | 5 | 5 |
| `rsn_b01` | zone | Port Section, field `555` | 44 | 140 | 14 | 1 |
| `rsn_b02` | zone | Large Freight Stores, field `556` | 40 | 106 | 16 | 0 |
| `rsn_b03` | zone | Starboard Section, field `557` | 41 | 129 | 11 | 0 |
| `rsn_b04` | zone | Sub-control Room, field `558` | 39 | 116 | 10 | 0 |
| `rsn_c01` | zone | Airship Berth Access, field `561` | 33 | 106 | 4 | 0 |
| `rsn_d01` | zone | Central Brig Access, field `564` | 26 | 97 | 5 | 1 |
| `rsn_y01` | zone | Brig No. 1, field `876` | 37 | 160 | 10 | 5 |
| `rsn_z01` | zone | Bridge, field `871` | 9 | 18 | 4 | 0 |
| `rsn_z02` | zone | Battle Launch, field `872` | 12 | 20 | 4 | 0 |
| `rsn_a0100` | scene | event `283` | 31 | 319 | 14 | 0 |
| `rsn_a0101` | scene | event `288` | 32 | 216 | 5 | 0 |
| `rsn_a0102` | scene | event `285` | 34 | 164 | 7 | 0 |
| `rsn_b0100` | scene | event `287` | 21 | 189 | 35 | 0 |
| `rsn_b0180` | scene | event `703` | 10 | 45 | 4 | 0 |
| `rsn_d0100` | scene | event `280` | 23 | 120 | 1 | 0 |
| `rsn_d0180` | scene | event `704` | 16 | 95 | 6 | 0 |
| `rsn_y0100` | scene | event `284` | 16 | 112 | 22 | 0 |
| `rsn_z0100` | scene | event `282` | 28 | 384 | 17 | 0 |
| `rsn_z0101` | scene | event `289` | 30 | 583 | 1 | 0 |
| `rsn_z0200` | scene | event `279` | 45 | 388 | 11 | 0 |
| `rsn_z0201` | scene | event `286` | 50 | 326 | 11 | 0 |

Port Launch and Brig No. 1 carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`.

Port Section and Central Brig Access carry the key-item and message helper alone. Their functions are described once
on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Dreadnought
Leviathan scenes](dreadnought-leviathan-scenes.md).

### What the scripts do

- Port Launch (field 552) holds the crystal. From story counter 890 and below 920, `常駐監督.init` requests
  `イベント管理.ウォースラー救援_再生`, which adds Vossler as a guest, loads and plays scene `rsn_a0100` (event 283) and writes 920,
  the value after Vossler's rescue and the start of Rescue Ashe. The bulkhead (`隔壁ジャンプ`) leads to Port Section, field
  555.
- Port Launch: from story counter 1000 and below 1010, while `g_btl_ギース` is 1, `常駐監督.main` loads scenes `rsn_a0101`
  (event 288) and `rsn_a0102` (event 285) and runs the Ghis fight under the boss gauge. When it ends it removes every
  foe, sets `g_btl_ギース` to 2, writes 1090, the value after the escape from the Leviathan, and jumps to the Aerodrome
  (Bhujerba), field 791.
- Port Section (field 555): from story counter 920 and below 930, `init` places a touch area; touching it
  (`イベント起動_警報`) has `イベント管理.警報ギミックチュートリアル_再生` play scene `rsn_b0180` (event 703), the warning about the alarm beams,
  and write 930, the value after the Leviathan tutorial. The bulkhead leads back to Port Launch, field 552, and the
  exits to Large Freight Stores, field 556.
- Port Section: from story counter 990 and below 1000, touching the area of `イベント起動_合流` has `イベント管理.パンネロ合流_再生` add
  Penelo to the party, play scene `rsn_b0100` (event 287) and write 1000, the value after Penelo rejoins; Vossler
  leaves the party as a guest.
- Large Freight Stores (field 556) and Sub-control Room (field 558): the alarm consoles (`警報解除西`, `警報解除東`, `警報解除`)
  answer "Insert access key."; with the Systems Access Key, choosing "Use the systems access key." shows "Systems
  access key verified. Access granted." and three choices. While the party holds the key, `main` sets flags `0x0095`
  and `0x0096` in the Large Freight Stores and `0x0094` in the Sub-control Room.
- Alarm consoles: "View security report." sets flags `0x0094` and `0x0095`, map icons in the Sub-control Room and the
  Large Freight Stores, and `0x0096`. "Reset alarm." answers "The alarm is not currently active. Reset aborted." at
  970 or below.
- Alarm consoles: the security report has two pages. Above story counter 970 the first gives anomalous activity in
  Brig No. 1 and a level 3 shipwide alert, else no anomalous activity; the second gives the Large Freight Stores and
  the Sub-control Room as nominal, with the console's own room (`nowmap()` 556 or 558) as the station in use.
- Alarm consoles: above story counter 970, "Reset alarm." asks "Upon resetting, you will have 60 seconds in which to
  dispose of the source of the anomaly.", then silences the alarm, starts the timer and shows "The alarm has been
  reset. If you do not dispose of the source of the anomaly within 60 seconds, the alarm will sound again."
- Starboard Section (field 557): beside the release, "An advisory is posted beside this unusual device."; the advisory
  reads "Be advised! This release is to be used under normal operating conditions and will not function during an
  alert." While the alarm sounds, "Activate the release." shows "Nothing happens."; otherwise "The Sub-control Room
  bulkhead is now unlocked."
- Starboard Section: until its release is used, the bulkhead (`隔壁ジャンプ`) answers "The bulkhead is securely locked.
  There must be a corresponding release mechanism somewhere."; then it leads to the Sub-control Room, field 558. The
  exits lead back to the Large Freight Stores, whose bulkhead leads to Airship Berth Access, field 561.
- Sub-control Room (field 558): its release works the same way and shows "The Airship Berth Access bulkhead is now
  unlocked."; until then the lower bulkhead (`隔壁ジャンプ下`) is locked, and it leads to Airship Berth Access, field 561.
  The upper bulkhead (`隔壁ジャンプ上`) leads back to Starboard Section, field 557.
- Airship Berth Access (field 561): the bulkhead to the Sub-control Room (`rsn0105へ`) stays locked until the
  Sub-control Room's release is used; from story counter 990 `main` opens it. The other doors lead to Central Brig
  Access, field 564, and the Large Freight Stores, field 556.
- Central Brig Access (field 564): from story counter 930 and below 966, `常駐監督.main` loads scene `rsn_d0100` (event
  280) and runs the fight with the lesser judges under the boss gauge. When it ends it sets `g_btl_ザコジャッジ` to 2,
  removes every foe, loads and plays `pos_z0000` (event 427), writes 966, the value after the battle with the lesser
  judges, and gives the No. 1 Brig Key.
- Central Brig Access: from story counter 970 and below 990, `常駐監督.init` requests `イベント管理.リヴァイサン脱出開始_再生`, which plays
  scene `rsn_d0180` (event 704) and writes 990, the start of Escape the Leviathan. The door to Brig No. 1 (`rsn5201へ`)
  shows "The bulkhead is locked." ("Use the No. 1 Brig key." / "Do nothing."), then "The lock opens.", and leads to
  Brig No. 1, field 876.
- Brig No. 1 (field 876) holds the crystal, and `Map_Director.init` sets flag `0x0062`. Below story counter 970 the
  field loads scene `rsn_y0100` (event 284); Ashe's cell (`イベント部屋`) has `イベント管理.アーシェ救出` add Ashe to the party, play
  the scene and write 970, the value after Ashe is rescued. The door leads back to Central Brig Access.
- Brig No. 1: once cell door `DOOR_C03` is open, the moogle merchant (`テトラン_ShopNpc`) and Lulucce speak, in the two
  messages below. The pot `コンパネキー宝壺` gives the Systems Access Key once (Bank512 second half `0x0020`).

The moogle merchant in Brig No. 1: "Kupo? You don't look like any Imperial I've ever seen, kupo. Me, kupo? I am but a
humble traveling merchant. As luck would have it, I happen to be traveling here. Would you like to see my wares? I'll
warn you, though. I only sell to one kind of customer: the paying kind, kupo!"

Lulucce in Brig No. 1: "Kupo! Not a word from you, kupo. I know why you've come! Oh, and thank you for opening the
cell door, by the way. Most gracious of you! After this treatment, I think it's safe to say we won't be visiting any
more Imperial warships in the near future. The road calls, kupo!"

- Bridge (field 871): from story counter 830 and below 890, `常駐監督.init` requests `イベント管理.ＳＢ３イベント_再生`, which plays
  scene `rsn_z0100` (event 282), writes 890, the value on the Leviathan's bridge, takes the Goddess's Magicite and
  jumps to Port Launch, field 552.
- Bridge: from story counter 1450 and below 1452, `イベント管理.ＳＢ４イベント_再生` plays scene `rsn_z0101` (event 289), writes
  1460, the value after a small fighter launches from the Leviathan, takes the Dawn Shard and jumps to Battle Launch
  (Light Cruiser Shiva), field 872.
- Battle Launch (field 872): from story counter 1460 and below 1470, `常駐監督.init` sets flag `0x005E`, and `main` loads
  scenes `rsn_z0200` (event 279) and `rsn_z0201` (event 286) and runs the Vossler fight under the boss gauge. When it
  ends it removes every foe, sets `g_btl_ウォースラ` to 2, writes 1520, the value after the Leviathan fleet is destroyed,
  gives the Dawn Shard, releases `0x005E` and jumps to `alc_z02` (Archades), field 867.
- Port Section, Large Freight Stores, Starboard Section and Sub-control Room hold 4, 6, 6 and 4 treasure chests.

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

The steps table [`dreadnought-leviathan-script-steps.tsv`](dreadnought-leviathan-script-steps.tsv) has one row for
each step of every function of the twenty-two scripts, in the order the function runs them: each call, request, store,
branch, loop, case and return. It has 35,427 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `rsn_a01` | 1,185 | `rsn_a0101` | 1,649 |
| `rsn_b01` | 1,539 | `rsn_a0102` | 1,337 |
| `rsn_b02` | 1,443 | `rsn_b0100` | 1,820 |
| `rsn_b03` | 2,036 | `rsn_b0180` | 512 |
| `rsn_b04` | 1,515 | `rsn_d0100` | 824 |
| `rsn_c01` | 1,359 | `rsn_d0180` | 871 |
| `rsn_d01` | 1,238 | `rsn_y0100` | 970 |
| `rsn_y01` | 1,611 | `rsn_z0100` | 2,963 |
| `rsn_z01` | 149 | `rsn_z0101` | 3,452 |
| `rsn_z02` | 289 | `rsn_z0200` | 3,720 |
| `rsn_a0100` | 2,341 | `rsn_z0201` | 2,604 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Dreadnought Leviathan has 78 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 35,344 |
| empty | 83 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `rsn_d0100` (event `280`), `雑魚ジャッジ登場.main` reads model
`0x03000000`, motions 1 to 3 of `rsn_d0100.mot` and event sound slots 0 and 1, waiting for each, and hides the party.
It files `取得` on eleven actors and waits for all eleven, then `配置1` on eight and waits for all eight, and waits while
`scratch1_var_1` is 0. At scene cut 1 it files `カット.１` and waits until it ends; at cut 2 it files `カット.２` and `カット.３`
in turn, waiting until each ends.

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

The script list [dreadnought-leviathan-script-list.tsv](dreadnought-leviathan-script-list.tsv) holds the first table
above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`dreadnought-leviathan-script-steps.tsv`](dreadnought-leviathan-script-steps.tsv) has one row per
step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message actors, described once.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Bhujerba scripts](bhujerba-scripts.md) - the Aerodrome the escape from Port Launch ends in.
- [Archades scripts](archades-scripts.md) - the field Battle Launch jumps to.

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
- Party: `0x0034D4E0` calls `0x00263750`, `0x003271D0`, `0x00327850`, `0x00328DB0`, `0x00359C00`, `0x0035A050`; `0x00355830` calls
  `0x003590D0`.
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
  `0x00267E10`; `0x0034B9A0` calls `0x00267E10`; `0x0034C030` calls `0x00267E10`; `0x0034D4E0` calls `0x00267E10`; `0x0034DD90` calls
  `0x00267E10`; `0x0034E0B0` calls `0x00267E10`, `0x0026B4E0`.
- Script VM: `0x0034EE20` calls `0x00267E10`; `0x00351880` calls `0x00267E10`; `0x003529E0` calls `0x00267E10`, `0x00267F90`;
  `0x00352EA0` calls `0x00267E10`; `0x00353390` calls `0x00267E10`; `0x00354000` calls `0x00267E10`, `0x0026B4E0`; `0x00354D00` calls
  `0x00267E10`; `0x00355830` calls `0x00267E10`.
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
