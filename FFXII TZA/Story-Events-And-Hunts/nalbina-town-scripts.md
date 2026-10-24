---
title: "Nalbina Town scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x003459C0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [nalbina-town-scripts.tsv](nalbina-town-scripts.tsv) has one row per script function of Nalbina Town that
does something a player can observe. It covers the four zone scripts and the one scene script of the area, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `nac_a01` | zone | West Barbican, field `630` | 46 | 300 | 22 | 5 |
| `nac_a02` | zone | Jajim Bazaar, field `631` | 50 | 320 | 46 | 1 |
| `nac_a03` | zone | West Ward, field `632` | 51 | 381 | 52 | 0 |
| `nac_b01` | zone | Aerodrome, field `800` | 38 | 261 | 30 | 0 |
| `nac_a0300` | scene | event `125` | 24 | 167 | 6 | 0 |

West Barbican carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`.
Jajim Bazaar carries only `イベント特殊効果画面`. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map or loads a scene. Functions that only move, animate, wait, play sound or set the camera
are not listed; each listed row counts the other functions of its actor in `other_functions`. The scene itself, with
its dialogue, is on [Nalbina Town scenes](nalbina-town-scenes.md).

### What the scripts do

- West Barbican: `監督.main` sets flags `0x0025` and `0x0020`, which open the location map's exits between Nalbina
  Town and the Mosphoran Highwaste and the Dalmasca Estersand.
- West Barbican: the roadblock actor `通行止め監督` turns back a party that slips past the soldiers toward the
  Mosphoran Highwaste ("Imperial army's engaged in a sweep of the Mosphoran Highwaste. No civilians allowed."); the
  soldiers' blocking area is removed only while the story counter is above 1520.
- West Barbican: the same actor's `通行解除イベント再生` shows the soldiers Deweg and Gibbs ("You're not afraid of
  the chocobo, are you, Gibbs?"), and
  `山通行解除.解除` sets flag `0x0144`. Gurdy, the chocobo seller (`NAC_ガーディ.talk_gardy`), sets flag `0x0073`,
  riding a chocobo.
- Jajim Bazaar: the notice board (`掲示板.talk`) shows the hunt bills, and the petitioners Burrogh and Popol
  (`依頼人ブロッホ`, `依頼人ポポル`) talk about their marks, the atomos and the deathscythe ([Hunts](hunts.md)).
- West Ward: `監督.main` writes 300, loads and plays scene `nac_a0300`, writes 301 and jumps to the Stockade
  (Nalbina Dungeons), field `48`, entrance 0. The petitioners Morgen and Barrong talk about the Roblon and Goliath.
- West Ward: Jovy (`ジョニー`) speaks from six `talk_step` functions, and `ロケイベント監督.ジョニーお礼渡す` gives the reward
  package that holds an Elixir and a Knot of Rust. The door `扉.開く` jumps to the Aerodrome, field `800`, entrance 1.
- Aerodrome: the airship counters (`乗船カウンタートーク`) show the boarding lines ("You are now free to board.",
  "you don't have enough gil"), set flag `0x005E` and jump to the Sky Saloon or the Observation Parlour
  (Skyferry) or to the aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port.
- Aerodrome: `監督.main` and `発着イベント監視.イベント再生とマップジャンプ` load scene `pas_z0000`
  ([Aerodrome airship scene](aerodrome-airship-scenes.md)).
- Aerodrome: the private airship desk (`シュトラール受付.talk_step01`) loads scene `str_z0000`
  ([Strahl scene](strahl-scenes.md)) and jumps to a field held in a variable. Nono talks about the
  Strahl's repair, and the petitioner Zammadria talks about her mark, Carrot.
- West Barbican holds a crystal; what touching it does, the teleport and its Teleport Stone are on
  [Shared zone-script actors](shared-zone-script-actors.md).

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname` | `0x399` | `0x0034DFA0` | `flags_set` | Bank2048 flag, the name-tag flags ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem_47f`, `additemmes`, `subitem` | `0x47F`, `0x480`, `0x2F2` | `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |

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
| `lines` | the section 2 entries the function passes to the message verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a Bank2048 flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [nalbina-town-script-list.tsv](nalbina-town-script-list.tsv) holds the first table above, one row
per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Nalbina Town scenes](nalbina-town-scenes.md) - the scene these scripts own.
- [Aerodrome airship scene](aerodrome-airship-scenes.md) and [Strahl scene](strahl-scenes.md) - the two scenes the Aerodrome loads.
- [Nalbina Dungeons scripts](nalbina-dungeons-scripts.md) - the Stockade, where West Ward's jump leads.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
- [Hunts](hunts.md) - the marks the petitioners post.
