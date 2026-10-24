---
title: "Zertinan Caverns scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00352EA0, 0x00353390, 0x00354000, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table has one row per script function of Zertinan Caverns that does something a player can observe. It covers the
ten zone scripts and the two scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `ztc_a01` | zone | Invitation to Heresy, field `576` | 29 | 53 | 13 | 1 |
| `ztc_a02` | zone | Sandfalls, field `577` | 34 | 93 | 10 | 0 |
| `ztc_a03` | zone | Hourglass Basin, field `578` | 33 | 82 | 11 | 0 |
| `ztc_b01` | zone | The Undershore, field `581` | 33 | 74 | 11 | 5 |
| `ztc_b02` | zone | Halls of Ardent Darkness, field `582` | 22 | 33 | 9 | 0 |
| `ztc_c01` | zone | The Balamka Fault, field `585` | 37 | 67 | 15 | 1 |
| `ztc_c02` | zone | Drybeam Cavern, field `586` | 27 | 41 | 11 | 0 |
| `ztc_c03` | zone | Darkened Wharf, field `587` | 25 | 36 | 8 | 0 |
| `ztc_c04` | zone | Canopy of Clay, field `588` | 23 | 68 | 6 | 0 |
| `ztc_d01` | zone | Athroza Quicksands, field `590` | 20 | 53 | 10 | 0 |
| `ztc_d0100` | scene | event `320` | 18 | 106 | 0 | 0 |
| `ztc_d0101` | scene | event `321` | 19 | 109 | 13 | 0 |

The Undershore carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`; Invitation to
Heresy and The Balamka Fault carry the key-item and message helper alone. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

The scene `ztc_d0101` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions
of its actor in `other_functions`. The scenes themselves, with their dialogue, are on
[Zertinan Caverns scenes](zertinan-caverns-scenes.md).

### What the scripts do

- The exits to the neighbouring regions: on the five maps below, `常駐ディレクター.main` loads scene `ttl_z0001` (event 216)
  and sets the flag that opens the location map's exits between the Zertinan Caverns and the region the map's exit
  leads to.

| Map | Flag | Region | Exit |
|---|---|---|---|
| Invitation to Heresy | `0x0039` | Dalmasca Westersand | Shimmering Horizons, field `347` |
| Halls of Ardent Darkness | `0x003B` | Ozmone Plain | The Switchback, field `526` |
| The Balamka Fault | `0x003C` | Ogir-Yensa Sandsea | East Junction, field `381` |
| Darkened Wharf | `0x003D` | Nam-Yensa Sandsea | Yellow Sands, field `393` |
| Canopy of Clay | `0x003E`, `0x003F` | Ogir-Yensa Sandsea, Nam-Yensa Sandsea | Central Junction, field `383`; Withering Shores, field `391` or field `1153` |

- Invitation to Heresy, Sandfalls, Hourglass Basin, The Undershore, Halls of Ardent Darkness, The Balamka Fault,
  Drybeam Cavern, Darkened Wharf and Canopy of Clay hold 9, 5, 4, 5, 6, 7, 6, 3 and 1 treasure chests.
- Hourglass Basin: `常駐ディレクター.main` holds the lines of War-chief Supinelu on the Catoblepas hunt ("We have arrived. The
  Catoblepas is here. I would defeat it, whatever the cost."), and `wanted_kansi.main` removes the foes of group 0 and
  of a group and shows his thanks ("At last, it is done. Long have I dreamt this day would come.").
- Invitation to Heresy: `wanted_kansi.main` gives the Serpentwyne Must and removes the foes of a group. The
  Undershore: `hunt_kansi.main` gives the Fell Trophy and removes the foes of a group.
- The Balamka Fault: the pot `ゼルテニアン地図宝壺` gives the Zertinan Caverns map through the helper, shows system message 105,
  "Your location map for this area is complete!", and sets treasure flag `0x0006`.
- Canopy of Clay: talking to `ztc0110流砂ギミック実行` sets flag `0x0159`, which draws the location map's link between
  Darkened Wharf and Canopy of Clay.
- Athroza Quicksands: `監督.main` shows the boss gauge, removes the foes of a group and loads scenes `ztc_d0100` (event
  320), `ztc_d0101` (event 321) and `pos_z0000` (event 427); `ztc_d0101` gives Adrammelech. Touching any of the four
  rectangles `ボス登場01` to `ボス登場04` shows the boss gauge, removes the foes of a group and loads `pos_z0000`.

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
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line; a system message is not spoken by the actor |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [`zertinan-caverns-script-list.tsv`](zertinan-caverns-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Zertinan Caverns scenes](zertinan-caverns-scenes.md) - the two scenes these scripts load.
- [Dalmasca Westersand scripts](dalmasca-westersand-scripts.md) - the region beyond Invitation to Heresy.
- [Ozmone Plain scripts](ozmone-plain-scripts.md) - the region beyond Halls of Ardent Darkness.
- [Nam-Yensa Sandsea scripts](nam-yensa-sandsea-scripts.md) - the region beyond Darkened Wharf and Canopy of Clay.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
