---
title: "Mosphoran Highwaste scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table has one row per script function of Mosphoran Highwaste that does something a player can observe. It covers
the ten zone scripts and the two scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `mnt_a01` | zone | Southern Skirts, field `209` | 22 | 35 | 10 | 0 |
| `mnt_a02` | zone | Summit Path, field `210` | 29 | 47 | 14 | 0 |
| `mnt_b01` | zone | Rays of Ashen Light, field `215` | 27 | 52 | 13 | 0 |
| `mnt_b02` | zone | Empyrean Way, field `216` | 27 | 40 | 12 | 0 |
| `mnt_b03` | zone | Skyreach Ridge, field `217` | 24 | 43 | 11 | 0 |
| `mnt_b04` | zone | Trail of Sky-flung Stone, field `218` | 28 | 67 | 11 | 0 |
| `mnt_b05` | zone | Northern Skirts, field `219` | 28 | 43 | 12 | 0 |
| `mnt_b06` | zone | Halny Crossing, field `220` | 12 | 19 | 5 | 0 |
| `mnt_c01` | zone | Empyrean Seat, field `223` | 10 | 15 | 2 | 0 |
| `mnt_d01` | zone | Babbling Vale, field `1151` | 88 | 329 | 63 | 5 |
| `mnt_c0100` | scene | event `130` | 12 | 89 | 0 | 0 |
| `mnt_c0101` | scene | event `131` | 15 | 76 | 13 | 0 |

Babbling Vale carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`. Their functions
are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared
helpers column counts them.

The scene `mnt_c0101` holds its own helper `イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions
of its actor in `other_functions`. The scenes themselves, with their dialogue, are on
[Mosphoran Highwaste scenes](mosphoran-highwaste-scenes.md).

### What the scripts do

- Southern Skirts: `常駐ディレクター.main` sets flag `0x0025`, the location map's exits between Mosphoran Highwaste and
  Nalbina Town, and loads scene `ttl_z0002` (event 217); one exit leads to West Barbican (Nalbina Town), field `630`.
- Summit Path: `常駐ディレクター.main` sets flag `0x0024`, the exits to Dalmasca Estersand, and loads `ttl_z0002`; one exit
  leads to Broken Sands (Dalmasca Estersand), field `133`. Halny Crossing: `常駐ディレクター.main` sets flag `0x0026`, the
  exits to The Salikawood, and one exit leads to The Omen-Spur (The Salikawood), field `151`.
- Southern Skirts, Summit Path, Rays of Ashen Light, Empyrean Way, Skyreach Ridge, Trail of Sky-flung Stone, Northern
  Skirts, Halny Crossing and Babbling Vale hold 5, 7, 5, 5, 4, 5, 9, 2 and 4 treasure chests.
- Rays of Ashen Light: a wayward chocobo (`野良騎乗チョコボ.talk`) takes Gysahl Greens and sets flag `0x0073`, riding a
  chocobo. The exits to Babbling Vale from Summit Path, Rays of Ashen Light, Empyrean Way, Skyreach Ridge and Trail of
  Sky-flung Stone release `0x0073`.
- Skyreach Ridge: `hunt_kansi.main` gives the Leathern Trophy and removes the foes of a group; a Learned Man
  (`研究員.talk`) came to climb the mountain after reading about its shrines in Archades. The exit to Empyrean Seat shows
  "The chocobo is nervous and refuses to go further. Something ahead must be frightening it." Northern Skirts:
  `wanted_kansi.main` removes the foes of a group.
- Trail of Sky-flung Stone: talking to the rock `rock_north` sets flags `0x0075` and `0x015A`, the second of which
  draws the location map's link between Rays of Ashen Light and Trail of Sky-flung Stone.
- Empyrean Seat: `監督.main` shows the boss gauge, removes the foes, and loads scenes `mnt_c0100` (event 130),
  `mnt_c0101` (event 131) and `pos_z0000` (event 427); `mnt_c0101` gives Exodus.
- Babbling Vale is the camp of Adair's Caravan: the Caravaner, Adair, Va'Kansa, a Scout, a Learned Man or a Viera
  Wayfarer, a Determined Traveler and a Concerned Woman, and three Craftsmoogles who came to check the shrines.
- Babbling Vale: the Caravaner's `００きゃらばん男_隊長.talk_atmos`, requested by `常駐監督.init`, warns of an atomos raging before
  the Salikawood; `０６ヴァカンサ_緑.talk_bligh` holds Va'Kansa's lines about the partner he lost in the Salikawood. The
  Concerned Woman's `talk_石崩した直後`, requested by `rock.talk`, says "We were almost crushed by that boulder!"
- Babbling Vale: the map seller `３０スカウト_地図屋` sells the Mosphoran Highwaste map and shows system message 92. Four
  bottle spots (`小舟ボトルレクト`, `廃屋ボトルレクト`, `祠ボトルレクト`, `ネズミボトルレクト`) each take the blue, green, red or black bottle, show
  "Without warning, the ... bottle shatters!", and give a message (Wanly Limned, Green-hued, Vermillion, Onyx) with a
  reward package (an X-Potion, a Hastega Mote, a Holy Mote, an Elixir).
- Babbling Vale: from story counter 3,070, talking to each of the six shrines (`uki00_mnt0104a` to `uki05_mnt0106a`)
  lofts the floatweed ("The surrounding floatweed is lofted into the air by the steam coming from the shrine.") and
  sets its map icon, `0x00E5` to `0x00EA`.
- Babbling Vale: the actors `anime_uki00` to `anime_uki05` set and release the map icons `0x00EB` to `0x00F0` in Rays
  of Ashen Light, Empyrean Way and Skyreach Ridge, and the functions of `モグマーカー監督` set and release the map icons
  `0x00BB` to `0x00BE` in The Salikawood.
- Babbling Vale: talking to `system_anchor_actor` requests `ym_shutoraljump.shtjump`, which loads scene `str_z0000`
  (event 211) and jumps to the field a script variable holds. Its exits lead to Summit Path, Rays of Ashen Light,
  Empyrean Way, Skyreach Ridge and Trail of Sky-flung Stone.

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

The script list [`mosphoran-highwaste-script-list.tsv`](mosphoran-highwaste-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Mosphoran Highwaste scenes](mosphoran-highwaste-scenes.md) - the two scenes these scripts load.
- [Dalmasca Estersand scripts](dalmasca-estersand-scripts.md) - the region beyond Summit Path.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
