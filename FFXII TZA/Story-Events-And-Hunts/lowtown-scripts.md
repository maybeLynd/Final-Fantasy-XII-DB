---
title: "Lowtown scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [lowtown-scripts.tsv](lowtown-scripts.tsv) has one row per script function of Lowtown that does something a
player can observe. It covers the five zone scripts and the seven scene scripts of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `slm_a01` | zone | North Sprawl, field `701` | 51 | 281 | 34 | 1 |
| `slm_a02` | zone | South Sprawl, field `702` | 46 | 245 | 31 | 1 |
| `slm_a03` | zone | Dalan's House, field `703` | 35 | 195 | 15 | 1 |
| `slm_a04` | zone | Residence, field `704` | 19 | 100 | 6 | 1 |
| `slm_z01` | zone | Dalan's Marker, field `856` | 8 | 15 | 1 | 0 |
| `slm_a0100` | scene | event `110` | 36 | 312 | 17 | 0 |
| `slm_a0101` | scene | event `113` | 17 | 109 | 19 | 0 |
| `slm_a0280` | scene | event `720` | 11 | 74 | 26 | 0 |
| `slm_a0300` | scene | event `112` | 16 | 88 | 1 | 0 |
| `slm_a0380` | scene | event `722` | 12 | 105 | 24 | 0 |
| `slm_a0381` | scene | event `714` | 12 | 80 | 19 | 0 |
| `slm_z0100` | scene | event `111` | 20 | 266 | 15 | 0 |

North Sprawl, South Sprawl, Dalan's House and Residence carry the key-item and message helper alone (`イベント特殊効果画面`).
Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here;
the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions of
its actor in `other_functions`. The scenes themselves, with their dialogue, are on [Lowtown
scenes](lowtown-scenes.md).

### What the scripts do

- North Sprawl: when the story counter is 285, `常駐監督.main` removes the guest Amalia, calls
  `takeaway_item_and_equip`, takes the Goddess's Magicite, removes Balthier and Fran, sets the fighting party to
  Vaan alone and loads scene `slm_a0100` (event 110), the capture; it then writes 290 and jumps to `rbn_z01`
  (Rabanastre), field 50.
- North Sprawl: at 386 the same function loads scene `slm_a0101` (event 113), writes 390 and adds Basch to the party.
- North Sprawl: the Resistance man Balzac (`解放軍`) jumps the party to Dalan's Marker, field 856, and posts the ring
  wyrm hunt (`talk_wanted`). The contrite thief (`空き巣シーク`) takes the Stolen Articles, gives the Blackened Fragment and
  sets name-tag flag `0x025F`, after which her name tag reads "Samal".
- North Sprawl: touching the storehouse door (`制御レクト０２`) gives a reward package of two Potions and four Eye Drops and
  shows "Hey, Vaan! I finally worked out how to get the door on the left side open!"
- South Sprawl: while the counter is from 160 to 169, `読み込み監督０１.init` loads scene `slm_a0280` (event 720), Penelo's
  farewell; `制御レクト.パンネロ離脱touch` sets the fighting party to Vaan, plays it, writes 170 and jumps to Dalan's House,
  field 703.
- Dalan's House: `常駐監督.EVダラン登場` loads scene `slm_a0381` (event 714), Dalan's appearance, and writes 115 and 120.
  Talking to Dalan (`ダラン.talk_step01`) takes the Sunstone and requests the two functions below.
- Dalan's House: `EV王宮の潜入方法2` plays scene `slm_a0380` (event 722), the way into the palace, which gives the Crescent
  Stone; it writes 175 and sets flag `0x0059`. `ダランの情報` plays scene `slm_a0300` (event 112), gives the Sword of the
  Order, writes 375 and sets flag `0x0058`.
- Dalan's House: Roh'kenmou (`モウ`), come from Nabudis, takes the Dull, Blackened and Grimy Fragments. At the Residence
  a letter on the table (`置き手紙`) gives the Dusty Letter ("I have divided it into four pieces...").
- Dalan's Marker: `常駐監督.EVウォースラ将軍前半` loads scene `slm_z0100` (event 111), General Vossler in the hideout; it writes
  386, takes the Sword of the Order and jumps to North Sprawl, field 701.
- North Sprawl's doors lead to North End and East End (Rabanastre) and to the Garamsythe Waterway; South Sprawl's gate
  leads to Southgate (Rabanastre) once the story counter is at least 100.
- North Sprawl and South Sprawl hold 6 and 5 treasure chests.

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
| `lines` | the section 2 entries the function passes to the message verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank2048` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; `the item held in` and the variable for an item a variable holds; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [lowtown-script-list.tsv](lowtown-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Lowtown scenes](lowtown-scenes.md) - the seven scenes these scripts load.
- [Royal Palace scripts](royal-palace-scripts.md) - the palace Dalan's directions lead into.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
