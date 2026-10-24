---
title: "Jahara scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table has one row per script function of Jahara that does something a player can observe. It covers the four
zone scripts and the three scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `glf_a01` | zone | Banks of the Sogoht, field `751` | 46 | 225 | 22 | 5 |
| `glf_a02` | zone | Lull of the Land, field `752` | 64 | 392 | 30 | 1 |
| `glf_a03` | zone | The Elderknoll, field `753` | 43 | 165 | 11 | 1 |
| `glf_z01` | zone | glf_z01, field `858` | 8 | 15 | 4 | 0 |
| `glf_a0200` | scene | event `327` | 22 | 217 | 34 | 0 |
| `glf_a0300` | scene | event `325` | 29 | 210 | 20 | 0 |
| `glf_z0100` | scene | event `326` | 18 | 203 | 43 | 0 |

Banks of the Sogoht carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`; Lull of
the Land and The Elderknoll carry the key-item and message helper alone. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them. The scene `glf_a0200` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its
functions have rows.

The fourth zone script, `glf_z01`, is field `858`, whose entry in `planmapname.bin` reads `glf_z01`; it exists to play
scene `glf_z0100`.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions
of its actor in `other_functions`. The scenes themselves, with their dialogue, are on
[Jahara scenes](jahara-scenes.md).

### What the scripts do

- Banks of the Sogoht: `常駐ディレクター.main` sets flag `0x0042`, the location map's exits to Ozmone Plain, and loads
  scene `ttl_z0000` (event 215). Talking to the gate guard requests `常駐イベント.コミューンへ`, which writes 1625, the
  entry into the garif village, and jumps to Lull of the Land, field `752`, entrance 1.
- Banks of the Sogoht: `常駐ディレクター.main` also requests `常駐イベント.旅立ち`, which writes 1650 ("After a moment's
  rest"); in it War-chief Supinelu ("So, you will leave.") gives a Killer Bow with Onion Arrows and a Recurve Crossbow with Onion Bolts. The moogle Gurdy hires out
  chocobos (`ガーディ.talk` sets flag `0x0073`) and jumps to Haulo Green (Ozmone Plain), field `527`.
- Lull of the Land: while the story counter is below 1,628, `常駐ディレクター.init` loads scene `glf_a0200`. Three
  stays move the story on: `Ev_Glf_a02_1stSTAY` writes 1626, `Ev_Glf_a02_2ndSTAY` (from the elder `ガリフ長老01`)
  writes 1627 and gives the Jaya Stick, and `Ev_Glf_a02_3rdSTAY` (from the War-chief `戦士長`) writes 1628, allowed
  to meet the chief.
- Lull of the Land: the War-chief takes the Jaya Stick; two other elders also write 1627; `常駐イベント.コカ` takes the
  Gift of the Great-chief and gives a Platinum Dagger; Judge Hausen, Larsa's escort, gives three Hi-Potions and an
  Ether. Garif warriors, herders and elders talk; several speak of the Catoblepas.
- The Elderknoll: while the story counter is below 1,640, `常駐ディレクター.init` loads scene `glf_a0300`. Touching
  `族長促しレクト` runs `常駐イベント.促し`, which writes 1640, after the legend of Giruvegan, and jumps to field
  `858`. Great-chief Uball-Ka gives the Gift of the Great-chief. The map holds two treasure chests.
- Field `858` (`glf_z01`): `常駐ディレクター.init` loads scene `glf_z0100`, and `常駐ディレクター.main` then jumps
  back to Lull of the Land, field `752`, entrance 0.

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
is shown is written `[value]`. Many zone lines begin with the speaker's name, which the text itself carries (`War-chief Supinelu`).

The script list [`jahara-script-list.tsv`](jahara-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Jahara scenes](jahara-scenes.md) - the three scenes these scripts load.
- [Ozmone Plain scripts](ozmone-plain-scripts.md) - the region beyond Banks of the Sogoht.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
