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
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions of
its actor in `other_functions`.

Cerobi Steppe has no scene script of its own; the scenes its fields load are the location title `ttl_z0002` ([Location
title scenes](titles-scenes.md)) and the Strahl scene `str_z0000` ([Strahl scene](strahl-scenes.md)).

### What the scripts do

- Old Elanise Road and South Liavell Hills: `監督.main` loads the location title `ttl_z0002` (event 217) on the first
  arrival and sets flag `0x002D` or `0x002E`, the location map's exits to the Tchita Uplands and to Balfonheim Port.
- The windmills: the Craftsmoogles' League is servicing the ten windmills of the steppe, one moogle (`大工モーグリ`) to each
  ("The Craftsmoogles' League have been called in to service all ten of the windmills on the Steppe, kupo.").
  Windmills 1 to 3 stand in North Liavell Hills, 4 and 5 in The Terraced Bank, 6 and 7 in Crossfield, and 8 to 10 in
  The Northsward (`風車レクト１` to `風車レクト１０`).
- Talking to a windmill (`風車レクトN.talk`) calls its moogle (`大工モーグリ.風車N挙動`). While the party holds the Yellow
  Bottle or the Auric Message, the moogle asks "She's running right now...need me to stop her?" or "She's stopped
  right now...need me to start her up?" and stops (`EV_H_風車N` 10) or starts (0) the windmill; otherwise it only talks.
- When such a talk leaves windmills 3, 4, 6, 8 and 10 stopped and the other five running, and `EV_H_暗号_黄` is not
  20, the Yellow Bottle shatters ("Without warning, the yellow bottle in your inventory shatters!"): the moogle
  gives a reward package with a Hi-Ether, takes the Yellow Bottle, gives the Auric Message and sets `EV_H_暗号_黄` to
  20.
- The Wyrm Philosopher (`竜じいさん`) dozes atop windmill No. 10 and wakes when its moogle finds him (`大工モーグリ.風車１０挙動`).
  While the party holds the Dragon Scale ("A scale found on the corpse of a vyraal.") and not the Ageworn Key, he
  takes the Dragon Scale and gives the Ageworn Key, "a key said to open the door to a chamber holding a most
  terrible wyrm".
- The Northsward: the Viera Wayfarer (`賞金首監督.main`) leads the hunt for the vyraal ("The vyraal that attacked me is a
  great creature with massive wings."); `wanted_kansi.main` removes the foes and gives a Viera Rucksack ("Visit me at
  the Whitecap in Balfonheim.").
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

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Strahl scene](strahl-scenes.md) - the private airship scene the anchor loads.
- [Golmore Jungle scripts](golmore-jungle-scripts.md) and [Paramina Rift scripts](paramina-rift-scripts.md) - other regions of this batch.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
