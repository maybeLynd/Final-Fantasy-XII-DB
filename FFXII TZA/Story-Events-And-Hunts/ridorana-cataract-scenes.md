---
title: "Ridorana Cataract scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Ridorana Cataract under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `rwf_a0100` | `372` | Footfalls of the Past | 15 | - |
| `rwf_c0100` | `370` | They Who Thirst Not | 0 | scene `rwf_c0101` |
| `rwf_c0101` | `371` | They Who Thirst Not | 0 | scene `rwf_c0100` |
| `rwf_c0102` | `373` | They Who Thirst Not | 20 | - |
| `rwf_d0100` | `374` | Colosseum | 0 | scene `rwf_d0101` |
| `rwf_d0101` | `375` | Colosseum | 0 | scene `pos_z0000` |

### What the scenes give

- No scene row lists an item, a party change, a story counter value or a flag.
- `rwf_a0100`, loaded in Footfalls of the Past below story counter 5,200: "A tower on distant shore. And about its
  peak, a piercing Mist. And in that Mist, the Sun-cryst waits." Vaan is told that if something untoward should
  happen, "you're taking the Strahl." Its first entry is the choice list "View scene again?" (Yes, No), and its last
  the word "Skip".
- `rwf_c0102`, loaded in They Who Thirst Not by `Read_Event_RWF_C01.sakiyomi_init`, reads the words engraved on the
  wall, signed "In blood, Raithwall", and the party learn that "The Dynast-King took his sword from the Occuria. It
  was here he claimed the nethicite." It begins with two choice lists, "From Cut 01" or "From Cut 12 (door opens)",
  and "View scene again?" (Yes, No).
- `rwf_c0100` and `rwf_c0101` (They Who Thirst Not) and `rwf_d0100` and `rwf_d0101` (Colosseum) open the boss fights
  and have no section 2 entries; `常駐監督.main` and `監督.main` load each pair in turn, and in the Colosseum `pos_z0000`
  follows.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Ridorana Cataract scripts](ridorana-cataract-scripts.md)): its actors, camera shots, motions, effects, music and loads.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Ridorana Cataract scripts](ridorana-cataract-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Pharos - First Ascent scenes](pharos-first-ascent-scenes.md) - the scenes of the Pharos beyond.
