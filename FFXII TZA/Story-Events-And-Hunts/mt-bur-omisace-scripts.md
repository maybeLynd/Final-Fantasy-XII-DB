---
title: "Mt Bur-Omisace scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x00351880, 0x00345080, 0x003449A0, 0x0034A6D0, 0x003459C0, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x00377B60, 0x003778B0"
---

## What it lists

The table [mt-bur-omisace-scripts.tsv](mt-bur-omisace-scripts.tsv) has one row per script function of Mt
Bur-Omisace that does something a player can observe. It covers the five zone scripts and the five scene scripts of
the area, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `bul_a01` | zone | Hall of the Light, field `736` | 17 | 91 | 7 | 1 |
| `bul_a02` | zone | Hall of the Light, field `737` | 15 | 55 | 2 | 1 |
| `bul_a03` | zone | Temple Grounds, field `738` | 32 | 148 | 9 | 1 |
| `bul_b01` | zone | Temple Approach, field `741` | 28 | 113 | 8 | 0 |
| `bul_b02` | zone | Sand-strewn Pass, field `742` | 36 | 178 | 10 | 5 |
| `bul_a0100` | scene | event `193` | 28 | 342 | 20 | 0 |
| `bul_a0101` | scene | event `194` | 26 | 318 | 32 | 0 |
| `bul_a0200` | scene | event `195` | 22 | 265 | 15 | 0 |
| `bul_a0201` | scene | event `196` | 24 | 274 | 25 | 0 |
| `bul_a0380` | scene | event `740` | 8 | 47 | 1 | 0 |

The Sand-strewn Pass carries the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`. The two Hall of the Light scripts and the Temple Grounds carry only `イベント特殊効果画面`.
Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows
here; the Shared helpers column counts them.

The scene `bul_a0101` holds its own actor `イベント特殊効果画面_EV`, whose functions take the item and message from
script variables; it is not one of the shared helpers, so its rows are listed.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below or loads a scene. Functions that only move,
animate, wait, play sound or set the camera are not listed; each listed row counts the other functions of its actor
in `other_functions`. The scenes themselves, with their dialogue, are on
[Mt Bur-Omisace scenes](mt-bur-omisace-scenes.md).

### What the scripts do

- Sand-strewn Pass: `配置監督.main` sets flag `0x0037`, which opens the location map's exits between Mt Bur-Omisace
  and the Paramina Rift, and writes 1982. Gurdy (`ガーディ.talk_gardy`) tells of the Trickster, sets flag `0x0073`,
  riding a chocobo, and jumps to the Freezing Gorge (Paramina Rift), field `465`, entrance 3.
- Temple Approach: on entry while the story counter is below 1984, `配置監督.init` writes 1984; while it is 2250,
  `配置監督.main` writes 2290. The camp actor `NPC01.talk` takes the Ring of the Light, and the Wyrm Snout
  (`behibehi_rect.talk_kirari`) gives the reward package that holds 500000 gil and a Rod of Faith.
- Hall of the Light, field 736: while the counter is below 2000, `先読み監督.init` loads scene `bul_a0100`;
  `配置監督.main` loads scene `bul_a0101` and then writes 2010 and 2050. Touching `アルシド起動レクト` writes 1998
  and jumps to `alc_z01` (Archades), field `866`.
- Hall of the Light, field 737: `配置監督.main` loads scenes `bul_a0200` and `bul_a0201`, shows the boss gauge,
  removes the foes, writes 2300, 2350 and 3000 and jumps to the Temple Grounds, field `738`, entrance 2.
- Temple Grounds: `配置監督.main` loads scene `bul_a0380` and writes 3050 after it; the same function also writes
  1986. The door of the audience chamber (`謁見の間ドア.talk`) jumps to a field held in a variable. One treasure
  chest stands here.
- The Sand-strewn Pass holds a crystal; what touching it does, the teleport and its Teleport Stone are on
  [Shared zone-script actors](shared-zone-script-actors.md).

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread_e8` | `0x0E8` | `0x00351880` | `scenes` | the event id, the second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `talktreasure` | `0x2BF` | `0x00355830` | `items` | a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |

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
  second name while that flag is set. An actor whose `setnpcname` calls name several pairs lists each second name,
  separated by `; `.
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
| `speaker` | for a row with lines, the names `setnpcname` gives the actor |
| `lines` | the section 2 entries the function passes to the message verbs; `system message N` for a message the function hands to the shared item and message helper, `N or M` when it is chosen at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; `(empty string)` for an entry with no text |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; `the item held in` and the variable for an item a variable holds; for an item the function hands to the shared item and message helper, the item it stores for it first, `A or B (which one is decided at run time)` when it is chosen at run time |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [mt-bur-omisace-script-list.tsv](mt-bur-omisace-script-list.tsv) holds the first table above, one
row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Mt Bur-Omisace scenes](mt-bur-omisace-scenes.md) - the five scenes these scripts load.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
- [Boss fights](../Battle-Actions/boss-fights.md) - the boss gauge and the foe removal of the Judge Bergan battle.
