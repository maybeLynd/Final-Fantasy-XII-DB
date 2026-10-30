---
title: "Title screen and location title scripts: what each script function shows, sets and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034ADA0, 0x0034B760, 0x0034BB10, 0x00352190, 0x00352AF0"
---

## What it lists

The table [titles-scripts.tsv](titles-scripts.tsv) has one row per script function of the title group `ttl` that does
something a player can observe. It covers the four zone scripts and the ten scene scripts of the group, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `ttl_a01` | zone | field `12` | 19 | 63 | 4 | 0 |
| `ttl_b01` | zone | field `13` | 1 | 2 | 1 | 0 |
| `ttl_c01` | zone | field `14` | 7 | 15 | 2 | 0 |
| `ttl_d01` | zone | field `1147` | 1 | 2 | 1 | 0 |
| `ttl_z0000` | scene | event `215` | 11 | 71 | 0 | 0 |
| `ttl_z0001` | scene | event `216` | 11 | 91 | 0 | 0 |
| `ttl_z0002` | scene | event `217` | 11 | 84 | 0 | 0 |
| `ttl_z0003` | scene | event `430` | 14 | 53 | 0 | 0 |
| `ttl_z0004` | scene | event `431` | 12 | 49 | 0 | 0 |
| `ttl_z0005` | scene | event `432` | 13 | 55 | 0 | 0 |
| `ttl_z0006` | scene | event `433` | 21 | 83 | 0 | 0 |
| `ttl_z0007` | scene | event `434` | 15 | 58 | 0 | 0 |
| `ttl_z0008` | scene | event `358` | 20 | 94 | 0 | 0 |
| `ttl_z0009` | scene | event `436` | 4 | 16 | 1 | 0 |

[Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) gives the four fields no map name, so the `place`
column names each by its script; the region after it, Pharos at Ridorana, is the entry their `map_ref.bin` rows
select.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions of
its actor in `other_functions`. The scenes themselves, with their dialogue, are on [Location title
scenes](titles-scenes.md).

### What the scripts do

- Title screen (`ttl_a01`, field 12): `常駐監督.main` runs the start-up pages and then the title screen, in a loop. The
  rating page, the logo page and the autosave page (`AUTOSAVEPAGE.ShowPage`) each appear only while the game's first
  start is not done (`isFirstStartDone() == 0`); then it requests `スクリーン表示.EF_タイトル画面`.
- The title screen script holds one line of text, the autosave notice: "This game will occasionally save
  automatically. Please do not exit the game while the save icon is visible."
- `EF_タイトル画面` shows the title commands (`コマンド制御.表示`) and, under a test, loads event 0 in slot 0
  (`eventread_e8(0, 0)`); the asset path table names no scene script for event 0, so its `scenes` cell reads
  `event, event 0`.
- The icon rows (`アイコン制御.初期設定`, `表示`, `消去`) set flag `0x006F` and release it again within the function;
  `title_c_fade.cfadein` and `cfadeout` in `ttl_c01` do the same around their fades.
- The ending hands over to the staff roll: in the Cannon Superstructure (Sky Fortress Bahamut), `bhm_d01`'s
  `ボス監督.main` writes story counter 7150, loads the ending message `msg_z0001` (event 399) and jumps to field 13
  ([Ending message scenes](ending-message-scenes.md)).
- Staff roll (`ttl_b01`, field 13): `監督.main` loads and plays scene `men_z0005` (event 429), the staff roll
  (its actors are `staffroll_ask`, `staffroll_main` and others), then asks "You can now begin your adventure anew in
  New Game+ mode." with the choices Begin New Game+ and Return to title. The first starts New Game+
  (`btlAtelResetNgPlus`, `fsttl_newgamestart`); the other returns to the title (`softwarereset`).
- Trial Mode hands over to `ttl_d01`: every Trial Mode stage script (`tri_`) runs the same `トライアル監督.main`, and
  only on field 1311 (`tri_t05`, the last stage) does it load event 427 (`pos_z0000`) and then jump to field 1147.
  That stage's clear also unlocks the achievement Imperator (40, verb `0x5AD`) before `mapjump(0x047b, 0, 1)`
  ([Achievements](../Steam-And-Achievements/achievements.md)).
- Trial Mode completion (`ttl_d01`, field 1147): `監督.main` fills in the play time and asks "Congratulations on
  completing Trial Mode! ... Your triumph has gained you access to New Game-. In New Game-, your characters will gain
  no experience." with Begin New Game- and Return to title. The first starts New Game- (`btlAtelResetNgMinus`,
  `fsttl_newgamestart`); the other returns to the title.
- Both questions are asked with the choice verb `aask_1ff`. They are not the only way in: the title screen's New Game
  list offers Begin New Game+ and Begin New Game- on every start
  ([New Game+ and New Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)).
- `ttl_c01` (field 14) is a second title script, with the actors `titlecommand`, `titlemenu`, `configcommand` and
  `movie_skip_ctrl`; its rows are the `title_c_fade` fades.
- The ten scene scripts `ttl_z0000` to `ttl_z0009` are location titles; [Location title scenes](titles-scenes.md)
  names the fields of other regions whose scripts load them. Only `ttl_z0009` has a row: its `ディレクター.main` sets flag
  `0x002F`, the location map's exits between Garamsythe Waterway and Royal Palace.

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

### Speakers, places and scenes

- The speaker is the second name of each pair the actor's `setnpcname` calls name in `us` `npcdic.bin`. The
  message window opener `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line |
| `lines` | the section 2 entries the function passes to the message verbs and the ask verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set`, `counter_tested` | `-` on every row: no listed function writes or tests the story counter |
| `items` | `-` on every row: no listed function gives or takes an item |
| `jumps` | `-` on every row: no listed function calls `mapjump` |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id; `event, event N` for an event id whose entry in the asset path table names no scene script |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [titles-script-list.tsv](titles-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Location title scenes](titles-scenes.md) - the ten scenes of this group, with the fields that load them.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
