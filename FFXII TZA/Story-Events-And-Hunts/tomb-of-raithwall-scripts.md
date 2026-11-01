---
title: "Tomb of Raithwall scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

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
- Valley of the Dead: the pirate `NPC_海賊手下` speaks of the avion and the tomb ("You...you killed the avion? Amazing!"
  ... "Me, I value life over loot. I go no farther...").
- The devices ("Magicks stir within this device.") jump between the tomb's halls, each to the field its listing
  stores: in the Valley of the Dead `rwg_warp_bef` (from story counter 1355) and `rwg_warp_aft` (from 1364) to Hall of
  the Destroyer, field 406; in Hall of the Destroyer `gil_warp` to Royal Passage, field 410, and `gil_warp_fromout` to
  the Valley of the Dead, field 403.
- The devices: in Royal Passage `古の仕掛けA` leads to Hall of the Destroyer, and `古の仕掛けB` and `古の仕掛けC` to Northfall
  Passage, field 412, and Southfall Passage, field 411; in Southfall and Northfall Passage `ワープ装置` leads to Royal
  Passage. Several answer "Nothing happens. There must be a corresponding device elsewhere." instead.
- Hall of the Destroyer: below story counter 1364, `常駐ディレクター.init` loads scene `rwg_b0103` (event 324), the talk of
  the devices ("One touch, and off you're whisked to you know not where."); `main` plays it, writes 1364, the value
  after entering the tomb, and loads scene `rwg_b0100` (event 330).
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
- Hall of the Sentinel: eight braziers (`gimmick_sw01n` to `gimmick_sw04s`) bear the tomb-watchers' words "Wakes it
  with the flames. Follows it their shadow. Ne'er straying." Touching one shows "The Demon Wall halts its advance.";
  the four from `gimmick_sw02n` to `gimmick_sw03s` also hold "The Demon Wall hastens its advance..."
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
  whose own functions give the Dawn Shard; touching `暁の断片起動` writes 1390, the value after the Dawn Shard. From 1390
  the way stone (`ワープ装置`), whose inscription reads "By this, return ye to the Hall of the Destroyer.", jumps to Hall
  of the Destroyer, field 406; before, it shows "Nothing happens. The device remains asleep."
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
- An actor these steps leave unnamed whose bind verbs name one `n` entry of the manifest takes the name the game
  gives the other actors bound to that `n` model, by these steps or as a voice cue's speaker
  ([Voices](../Sound-And-Music/voices.md)), when they all give one name and two or more actors give it or the bestiary
  gives the same.
- Failing that, it takes the [bestiary](../Enemy-Spawning/bestiary.md) name of that model id (its
  `model_id` cell), when the bestiary gives it one name. A `c` model is left out of these two steps, since the
  bestiary can name a battle alias there: Amalia for Ashe's `c11`.
- Any other line without a name reads `no name shown`, apart from a scene subtitle, which keeps its row's cell `-`. A
  line whose name is `???` reads `???`: the game prints `???` as that speaker's name at that line. A row lists its
  speakers in line order, each once.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`tomb-of-raithwall-script-steps.tsv`](tomb-of-raithwall-script-steps.tsv) has one row for each step
of every function of the twenty-three scripts, in the order the function runs them: each call, request, store, branch,
loop, case and return. It has 25,349 rows.

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
| `resolved` | 25,261 |
| empty | 86 |
| `does not ship`, with the fact | 2 |

The two `does not ship` rows are `motionread` calls that read an empty entry: entry 1 of `rwg_a0180.mot` and entry 1
of `rwg_a0181.mot`. A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the
arguments as the script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry
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
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Tomb of Raithwall scenes](tomb-of-raithwall-scenes.md) - the fifteen scenes these scripts own.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Nam-Yensa Sandsea scripts](nam-yensa-sandsea-scripts.md) - the region beyond the Valley of the Dead.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
