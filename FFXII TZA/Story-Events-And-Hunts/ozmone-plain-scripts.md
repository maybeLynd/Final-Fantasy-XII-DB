---
title: "Ozmone Plain scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table has one row per script function of Ozmone Plain that does something a player can observe. It covers the
eight zone scripts and the two scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `ozm_a01` | zone | Field of Fallen Wings, field `525` | 26 | 43 | 13 | 0 |
| `ozm_a02` | zone | The Switchback, field `526` | 31 | 51 | 16 | 0 |
| `ozm_a03` | zone | Haulo Green, field `527` | 33 | 51 | 17 | 0 |
| `ozm_b01` | zone | Dagan Flats, field `530` | 26 | 37 | 10 | 0 |
| `ozm_b02` | zone | Field of Light Winds, field `531` | 24 | 37 | 7 | 0 |
| `ozm_b03` | zone | The Greensnake, field `532` | 21 | 29 | 6 | 0 |
| `ozm_b04` | zone | Sunlit Path, field `533` | 39 | 152 | 14 | 5 |
| `ozm_c01` | zone | The Shred, field `536` | 55 | 147 | 24 | 1 |
| `ozm_b0400` | scene | event `268` | 22 | 151 | 6 | 0 |
| `ozm_c0180` | scene | event `396` | 25 | 103 | 2 | 0 |

Sunlit Path carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`; The
Shred carries the key-item and message helper alone. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions
of its actor in `other_functions`. The scenes themselves, with their dialogue, are on
[Ozmone Plain scenes](ozmone-plain-scenes.md).

### What the scripts do

- Field of Fallen Wings: `常駐ディレクター.main` sets flag `0x0031`, the location map's exits to Giza Plains, and loads
  scene `ttl_z0000` (event 215). Its exit to Starfall Field jumps to field `247` or field `264`.
- The Switchback: `常駐ディレクター.main` sets flag `0x003B`, the location map's exits to the Zertinan Caverns, and loads
  scene `ttl_z0000`; one exit leads to Halls of Ardent Darkness (Zertinan Caverns), field `582`. `hunt_kansi.main`
  gives the Metallic Trophy and removes the foes of a group.
- Haulo Green: `常駐ディレクター.main` sets flag `0x0042`, the location map's exits to Jahara, and one exit leads to
  Banks of the Sogoht (Jahara), field `751`.
- Field of Fallen Wings, The Switchback, Haulo Green, Dagan Flats, Field of Light Winds, The Greensnake and The Shred
  hold 9, 8, 11, 7, 2, 3 and 9 treasure chests.
- Sunlit Path: when the story counter is 1,650, `常駐ディレクター.init` loads scene `ozm_b0400` and writes 1658; at 1,658
  `常駐ディレクター.main` jumps to field `869` (`alc_z04`, Archades). `常駐ディレクター.main` also sets flag `0x0043`,
  the location map's exits to Golmore Jungle; one exit leads to Paths of Chained Light (Golmore Jungle), field `447`.
- Sunlit Path also holds an Imperial soldier who asks for a potion for his friend: `常駐イベント.ポーション` takes a
  Potion, and the scrap of paper `手紙キラリン` gives two Prince's Kisses with a letter of thanks. Two game
  hunters talk, and talking to `system_anchor_actor` requests `ym_shutoraljump.shtjump`, which loads scene
  `str_z0000` (event 211) and jumps to the field a script variable holds.
- The Shred: `常駐ディレクター.main` sets flag `0x0045`, the location map's exits to the Henne Mines. While the story
  counter is at most 1,790, `Read_Event_OZM_C01.init` loads scene `ozm_c0180`; below 1,790 an Imperial turns the
  party away from the mines, and at 1,790 touching `イベント起動` writes 1810, the dead Imperial soldiers at the
  Henne entrance.
- The Shred also holds a wayward chocobo that lets the party ride it for Gysahl Greens (`野良騎乗チョコボ.talk` takes
  them and sets flag `0x0073`), and `wanted_kansi.main` removes the foes of a group and gives an Errmonea Leaf.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
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

The script list [`ozmone-plain-script-list.tsv`](ozmone-plain-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Ozmone Plain scenes](ozmone-plain-scenes.md) - the two scenes these scripts load.
- [Giza Plains scripts](giza-plains-scripts.md) - the region beyond Field of Fallen Wings.
- [Jahara scripts](jahara-scripts.md) - the region beyond Haulo Green.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
