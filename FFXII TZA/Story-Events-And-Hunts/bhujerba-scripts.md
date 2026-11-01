---
title: "Bhujerba scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [bhujerba-scripts.tsv](bhujerba-scripts.tsv) has one row per script function of Bhujerba that does something
a player can observe. It covers the eighteen zone scripts and the thirteen scene scripts of the region, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `byu_a01` | zone | Travica Way, field `803` | 51 | 251 | 30 | 1 |
| `byu_a02` | zone | Cloudborne Row, field `804` | 34 | 161 | 14 | 1 |
| `byu_a03` | zone | Miners' End, field `805` | 33 | 186 | 22 | 1 |
| `byu_a04` | zone | Lhusu Square, field `806` | 42 | 199 | 27 | 5 |
| `byu_a07` | zone | Khus Skygrounds, field `809` | 24 | 109 | 10 | 1 |
| `byu_a08` | zone | Kaff Terrace, field `810` | 23 | 92 | 8 | 1 |
| `byu_a11` | zone | Targe's Arms, field `813` | 20 | 106 | 8 | 1 |
| `byu_a12` | zone | Rithil's Protectives, field `814` | 20 | 106 | 8 | 1 |
| `byu_a14` | zone | Mait's Magicks, field `816` | 20 | 106 | 8 | 1 |
| `byu_a15` | zone | Clio's Technicks, field `817` | 41 | 195 | 9 | 1 |
| `byu_a16` | zone | Bashketi's Gambits, field `818` | 21 | 109 | 8 | 1 |
| `byu_a17` | zone | The Staras Residence, field `819` | 22 | 129 | 13 | 1 |
| `byu_a18` | zone | The Cloudborne, field `820` | 28 | 148 | 12 | 1 |
| `byu_b01` | zone | Aerodrome, field `791` | 41 | 169 | 18 | 5 |
| `byu_w01` | zone | field `912` | 7 | 10 | 1 | 0 |
| `byu_x01` | zone | field `914` | 7 | 10 | 1 | 0 |
| `byu_y01` | zone | field `864` | 8 | 16 | 3 | 0 |
| `byu_z01` | zone | field `862` | 7 | 10 | 1 | 0 |
| `byu_a0100` | scene | event `271` | 31 | 384 | 11 | 0 |
| `byu_a0400` | scene | event `272` | 20 | 247 | 11 | 0 |
| `byu_a0480` | scene | event `705` | 18 | 88 | 1 | 0 |
| `byu_a0481` | scene | event `725` | 24 | 169 | 9 | 0 |
| `byu_a1880` | scene | event `265` | 24 | 216 | 14 | 0 |
| `byu_b0100` | scene | event `276` | 26 | 162 | 4 | 0 |
| `byu_b0101` | scene | event `278` | 32 | 214 | 3 | 0 |
| `byu_w0100` | scene | event `277` | 27 | 233 | 19 | 0 |
| `byu_x0100` | scene | event `275` | 18 | 145 | 11 | 0 |
| `byu_y0100` | scene | event `273` | 24 | 293 | 15 | 0 |
| `byu_y0101` | scene | event `274` | 18 | 207 | 16 | 0 |
| `byu_z0100` | scene | event `270` | 25 | 162 | 6 | 0 |
| `byu_z9900` | scene | event `606` | 3 | 8 | 0 | 0 |

Lhusu Square and Aerodrome carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`.

Travica Way, Cloudborne Row, Miners' End, Khus Skygrounds, Kaff Terrace, Targe's Arms, Rithil's Protectives, Mait's
Magicks, Clio's Technicks, Bashketi's Gambits, The Staras Residence and The Cloudborne carry the key-item and message
helper alone. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have
no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Bhujerba
scenes](bhujerba-scenes.md).

### What the scripts do

- Aerodrome (field 791) holds the crystal. At story counter 490 `常駐監督.init` writes 520, the value after the floating
  continent; at 520 `main` loads and plays scene `byu_b0101` (event 278) and writes 546, the value after the runaway
  escapes, in the aerodrome.
- Aerodrome: at story counter 1090 `常駐監督.main` loads and plays scene `byu_b0100` (event 276) and writes 1095, the
  value after Escape the Leviathan, then 1100, the value after the return to Bhujerba. When `event_global_flag[3]` is
  2, the same function loads and plays `pas_z0000` (event 214, [Aerodrome airship
  scenes](aerodrome-airship-scenes.md)).
- Aerodrome: below story counter 6100 the counter (`乗船カウンタートーク`) sells passage ("Good day, sir. This counter serves
  travelers wishing to book passage to Rabanastre."). The departure (`発着イベント監視`) sets flag `0x005E`, loads `pas_z0000`
  and jumps aboard the Skyferry, to the Sky Saloon, field 125, or the Observation Parlour, field 124, or to another
  aerodrome.
- Travica Way (field 803): at story counter 546 `常駐監督.main` loads and plays scene `byu_a0100` (event 271), adds Lamont
  as a guest and writes 550, the value after the runaway escapes. Below 680 five ways are closed ("Sorry, but this way
  is closed, on the authority of the Marquis."), and the estate gate (`オンドール通行禁止レクト`) answers "Beyond this point is
  the property of His Excellency the Marquis."
- Travica Way: at story counter 730, `NPC01` at the estate says "Haa, we've been expecting you. His Excellency the
  Marquis awaits." and, after "I'm ready.", "His Excellency the Marquis is otherwise occupied until sunset.", and
  takes the party to field 864 (`byu_y01`); at 1100 "His Excellency has given orders that you are to be granted an
  audience." leads there too.
- Travica Way and Miners' End: `Map_Director.init` releases flag `0x0158` below story counter 710 and sets it from
  710.
- Travica Way's signs name Targe's Arms, Rithil's Protectives and Mait's Magicks (fields 813, 814 and 816), whose
  doors lead in and back. Miners' End's signs name Clio's Technicks and Bashketi's Gambits (fields 817 and 818), and
  Khus Skygrounds (field 809) has the sign of Kweli's Last Stand.
- Travica Way and Lhusu Square: the Cartographers' Guild moogle (`NPC01`) sells the map of Bhujerba or of the Lhusu
  Mines ("Select a map to purchase:").
- Every town field: a bottle of spirits (`魂レクト`, "The label says") gives Bhujerban Madhu ("Take it."), and in each
  field a townsperson buys it for 1000 gil ("Sell it to me, bhadra! I'll give you [value] gil!" in Travica Way).
- Cloudborne Row (field 804) leads to Travica Way, Miners' End, The Cloudborne (field 820) and The Staras Residence
  (field 819); Miners' End (field 805) to Travica Way, Cloudborne Row, Lhusu Square (field 806) and Kaff Terrace
  (field 810); Khus Skygrounds and the Aerodrome lead to Travica Way.
- Miners' End: below story counter 680 two ways are closed ("Sorry, sir, but this way is temporarily closed."). Miclio
  (`幽霊小僧`) speaks of his bill ("Yes, I speak of Diabolos."), and a townsperson's lines include "If you had not killed
  the raksas, we would be waiting here still, bhadra! Our thanks!"
- Lhusu Square (field 806) holds the crystal. Below story counter 580 the field loads scene `byu_a0480` (event 705);
  touching the mine entrance (`突入イベントレクト`) plays it, writes 580, the start of the mystery of the Lhusu Mines, and
  jumps to Shaft Entry (Lhusu Mines), field 357.
- Lhusu Square: from story counter 658 to 670, `配置監督.init` loads and plays scene `byu_a0400` (event 272), and `main`
  writes 680, the value after the mystery of the Lhusu Mines.
- Lhusu Square: at story counter 680, touching `オレバッシュレクト` plays scene `byu_a0481` (event 725), loaded from 658,
  writes 710, the start of Marquis Ondore, and starts the rumour: the gauge (`オレバッシュゲージ監督`) appears, and while the
  rumour runs every town field's `オレバッシュ監督.init` loads and plays `byu_z9900` (event 606).
- Town fields: while the rumour runs, a button press has Vaan shout ("I'm Captain Basch fon Ronsenburg of Dalmasca!",
  "Basch lives!"), the people around answer (`全員注目`), and "[value] Bhujerbans heed your words." or "No one heeds your
  words." follows. At 100 on the gauge, "You. Boy. You will come with us.": `オレバッシュ監督.main` writes 710 and jumps to
  The Cloudborne, field 820; below 100 the gauge falls.
- Lhusu Square: the talk of Basch, Balthier and Fran in the square includes "Spread the rumor that I still live, and
  the Resistance here in Bhujerba will come out of their hiding places to ascertain the truth." and "Look to where
  people gather."
- Khus Skygrounds: Pilika (`NPC01`) gives the Merchant's Armband and asks for her diary ("I've left my dearest diary
  at work!"); in Clio's Technicks (field 817) `日記レクト` gives Pilika's Diary ("Pilika's diary is lying here.").
  Returned, it brings a Bangle for "Read it." and a Jade Collar for "I've done nothing."
- The Staras Residence (field 819): from story counter 1982 and clan rank 5, `NPC01`'s talk ("Oh, bhadra, both my
  children are missing!") gives the Site 3 Key, with the miner's lines (`エキストラ作業員`): "This is the key to the gate in
  Site 2 of the mines. Open the gate, and you will have access to the depths beyond."
- The Cloudborne (field 820): at story counter 710, after the rumour, `配置監督.main` loads and plays scene `byu_a1880`
  (event 265) and jumps to field 914 (`byu_x01`); at 720 it plays the scene again and writes 730, the value after
  Marquis Ondore.
- The Cloudborne: the notice board (`掲示板`) lists the marks ("Which bill would you like to read?"), and Ondore's
  attendant says "His Excellency the Marquis will meet with you shortly, bhadra."
- Field 862 (`byu_z01`): at story counter 460 `常駐監督.main` loads and plays scene `byu_z0100` (event 270), writes 490,
  the value after the captive Penelo, then 520, and jumps to the Aerodrome, field 791.
- Field 864 (`byu_y01`): at story counter 730 `常駐監督.main` plays scene `byu_y0100` (event 273), writes 800, the value
  after the laughing marquis, and jumps to `rbn_x01` (Rabanastre), field 860; at 1100 it plays `byu_y0101` (event
  274), writes 1120, the value after learning where the Dawn Shard is, and jumps to field 912 (`byu_w01`).
- Field 912 (`byu_w01`): at story counter 1120 `常駐監督.main` plays scene `byu_w0100` (event 277), writes 1130, the value
  after the princess is taken, and jumps to `alc_z01` (Archades), field 866.
- Field 914 (`byu_x01`): at story counter 710 `常駐監督.main` plays scene `byu_x0100` (event 275), writes 720, the value
  after Larsa and Penelo, and jumps to The Cloudborne, field 820.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname`, `releasetalknpcname`, `istalknpcname` | `0x399`-`0x39B` | `0x0034DFA0`, `0x0034E320`, `0x0034E980` | `flags_*` | `Bank2048` flag: the name tag ([story flag ids](story-flag-ids.md), [NPC names](../Characters-And-Objects/npc-names.md)) |
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

The steps table [`bhujerba-script-steps.tsv`](bhujerba-script-steps.tsv) has one row for each step of every function
of the thirty-one scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 82,332 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `byu_a01` | 9,082 | `byu_x01` | 48 |
| `byu_a02` | 6,635 | `byu_y01` | 135 |
| `byu_a03` | 7,523 | `byu_z01` | 51 |
| `byu_a04` | 3,431 | `byu_a0100` | 1,831 |
| `byu_a07` | 3,801 | `byu_a0400` | 1,551 |
| `byu_a08` | 4,052 | `byu_a0480` | 564 |
| `byu_a11` | 3,549 | `byu_a0481` | 1,432 |
| `byu_a12` | 2,288 | `byu_a1880` | 1,927 |
| `byu_a14` | 2,957 | `byu_b0100` | 1,831 |
| `byu_a15` | 3,602 | `byu_b0101` | 1,216 |
| `byu_a16` | 2,912 | `byu_w0100` | 1,963 |
| `byu_a17` | 2,500 | `byu_x0100` | 1,230 |
| `byu_a18` | 5,250 | `byu_y0100` | 1,728 |
| `byu_b01` | 6,295 | `byu_y0101` | 1,749 |
| `byu_w01` | 47 | `byu_z0100` | 1,119 |
| | | `byu_z9900` | 33 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Bhujerba has 178 such rows.

Some actors run another actor's code: `NPC02` in `byu_a01` starts at the same place as `NPC01` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 208 of these rows: 19
in `byu_a01`, 17 in `byu_a02`, 20 in `byu_a03`, 9 in `byu_a04`, 20 in `byu_a07`, 23 in `byu_a08`, 15 in `byu_a11`, 4
in `byu_a12`, 10 in `byu_a14`, 14 in `byu_a15`, 13 in `byu_a16`, 4 in `byu_a17`, 19 in `byu_a18` and 21 in `byu_b01`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 82,190 |
| empty | 130 |
| `does not ship`, with the fact | 12 |

The twelve `does not ship` rows are `motionread` calls that read an empty entry: entry 1 of `byu_a04.mot`, entry 1 of
`byu_a12.mot` (two rows), entry 1 of `byu_a14.mot`, entry 2 of `byu_a14.mot`, entry 1 of `byu_a15.mot` (two rows),
entry 2 of `byu_a15.mot`, entry 1 of `byu_a16.mot` (two rows), entry 2 of `byu_a16.mot` and entry 1 of `byu_a17.mot`.

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `byu_a0480` (event `705`), `DIRECTOR.main` reads
motion 1 of `byu_a0480.mot` and models `0x03000000` to `0x03000005`, waits for them, and waits while `scratch1_var_2`
is 0. It fades the screen out over 1 frame and files `MUSIC.music_1_vol`, waiting until it ends. It then files
`AD.準備_ad`, `AD.カット１_ad` to `AD.カット４_ad` and `AD.終了_ad` one after another, waiting until each ends, frees the motion
and the six models, fades out over 0 frames and disposes of event manager slot 0.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank2048` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `field held in` and the variable when the target field is a variable |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [bhujerba-script-list.tsv](bhujerba-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`bhujerba-script-steps.tsv`](bhujerba-script-steps.tsv) has one row per step:

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

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message actors, described once.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Aerodrome airship scenes](aerodrome-airship-scenes.md) - the scene the Aerodrome loads.
- [Dreadnought Leviathan scripts](dreadnought-leviathan-scripts.md) - Port Launch, which jumps to the Aerodrome.
- [Rabanastre scripts](rabanastre-scripts.md) - field 860, where field 864 sends the party.
- [Archades scripts](archades-scripts.md) - field 866, where field 912 sends the party.
